"""
MuhammedAI Local Developer - Agent Loop
AI → Tool → Result → AI döngüsünü yönetir.
"""

from typing import Dict, Any, Optional, Callable, List
from dataclasses import dataclass
import logging

from app.ai.ollama_client import OllamaClient
from app.ai.tool_parser import ToolParser, ToolCall, ParseResult
from app.ai.conversation_memory import ConversationMemory
from app.ai.change_orchestrator import ChangeOrchestrator
from app.tools.tool_registry import ToolRegistry
from app.core.config import PROJECT_ROOT


@dataclass
class LoopConfig:
    """Agent Loop yapılandırması."""
    max_iterations: int = 10
    max_tool_output_length: int = 2000  # Karakter cinsinden
    enable_logging: bool = True
    max_no_tool_retries: int = 2  # Tool çağrısı olmadığında maksimum yeniden deneme sayısı


@dataclass
class LoopResult:
    """Loop sonucu."""
    success: bool
    final_response: str
    iterations: int
    tool_calls: List[Dict[str, Any]]
    error: Optional[str] = None


class AgentLoop:
    """
    AI → Tool → Result → AI döngüsünü yönetir.

    Özellikler:
    - Çok adımlı görevler
    - Maksimum iteration sınırı
    - Sonsuz döngü engelleme
    - Tool güvenliği ve doğrulama
    - Kullanıcı onayı mekanizması (bypass edilemez)
    - Tool çıktı boyutu sınırı
    - Logging
    """

    def __init__(
        self,
        ollama_client: OllamaClient,
        tool_registry: ToolRegistry,
        config: Optional[LoopConfig] = None,
        approval_callback: Optional[Callable[[str, Dict[str, Any]], bool]] = None
    ):
        """
        Args:
            ollama_client: Ollama istemcisi
            tool_registry: Tool kayıt sistemi
            config: Loop yapılandırması
            approval_callback: Onay için callback fonksiyonu
                             (tool_name, arguments) -> bool
        """
        self.ai = ollama_client
        self.registry = tool_registry
        self.config = config or LoopConfig()
        self.approval_callback = approval_callback

        self.parser = ToolParser()
        self.memory = ConversationMemory()

        # ChangeOrchestrator - dosya değişikliği için modelden bağımsız orkestrasyon
        self.change_orchestrator = ChangeOrchestrator(
            workflow=self.registry.workflow,
            approval_callback=approval_callback
        )

        # Logger
        self.logger = logging.getLogger(__name__)
        if self.config.enable_logging:
            logging.basicConfig(level=logging.INFO)

        # İstatistikler
        self.tool_call_log: List[Dict[str, Any]] = []

        # Duplicate tracking: (tool_name, frozenset(arguments.items())) -> (count, last_result)
        self._call_history: Dict[tuple, tuple] = {}

    def _truncate_tool_output(self, output: Any) -> str:
        """
        Tool çıktısını boyut sınırına göre kırpır.

        Args:
            output: Tool çıktısı
        
        Returns:
            str: Kırpılmış veya orijinal çıktı
        """
        output_str = str(output)

        if len(output_str) <= self.config.max_tool_output_length:
            return output_str

        truncated = output_str[:self.config.max_tool_output_length]
        return truncated + "\n\n[SONUÇ KISALTILDI - Orijinal sonuç çok uzun]"

    def _validate_tool_call(self, tool_call: ToolCall) -> tuple[bool, Optional[str]]:
        """
        Tool çağrısını parametre doğrulaması yapar.

        Args:
            tool_call: Tool çağrısı

        Returns:
            (is_valid, error_message): Geçerliyse (True, None), değilse (False, error)
        """
        tool_name = tool_call.name
        arguments = tool_call.arguments

        # Tool mevcut mu?
        if not self.registry.has(tool_name):
            return False, f"Tool bulunamadı: {tool_name}"

        # Tool şemasını al
        schema = self.registry.get_tool_schema(tool_name)
        if schema is None:
            return False, f"Tool şeması alınamadı: {tool_name}"

        expected_params = schema["parameters"]

        # Parametreleri kontrol et
        expected_param_names = {p["name"] for p in expected_params}
        required_param_names = {p["name"] for p in expected_params if p["required"]}
        provided_param_names = set(arguments.keys())

        # Eksik zorunlu parametreler
        missing_required = required_param_names - provided_param_names
        if missing_required:
            return False, f"Eksik zorunlu parametreler: {missing_required}. Beklenen: {expected_param_names}"

        # Fazladan parametreler
        extra_params = provided_param_names - expected_param_names
        if extra_params:
            return False, f"Fazladan parametreler: {extra_params}. Beklenen: {expected_param_names}"

        # Parametre tipi kontrolü (basit)
        for param in expected_params:
            param_name = param["name"]
            if param_name in arguments:
                param_value = arguments[param_name]
                param_type = param["type"]

                if param_type == "str" and not isinstance(param_value, str):
                    return False, f"Parametre tipi hatası: {param_name} str olmalı, {type(param_value).__name__} alındı"
                elif param_type == "int" and not isinstance(param_value, int):
                    return False, f"Parametre tipi hatası: {param_name} int olmalı, {type(param_value).__name__} alındı"
                elif param_type == "bool" and not isinstance(param_value, bool):
                    return False, f"Parametre tipi hatası: {param_name} bool olmalı, {type(param_value).__name__} alındı"
                elif param_type == "dict" and not isinstance(param_value, dict):
                    return False, f"Parametre tipi hatası: {param_name} dict olmalı, {type(param_value).__name__} alındı"

        return True, None

    def _check_duplicate_call(self, tool_call: ToolCall) -> tuple[bool, Optional[str], Optional[Dict[str, Any]]]:
        """
        Aynı tool çağrısının tekrar edilip edilmediğini kontrol eder.

        Args:
            tool_call: Tool çağrısı

        Returns:
            (is_duplicate, message, cached_result):
            - Tekrar değilse: (False, None, None)
            - Tekrar ise: (True, message, cached_result)
            - 2 kez başarısız olduysa: (True, error_message, None)
        """
        tool_name = tool_call.name
        arguments = tool_call.arguments

        # arguments dict'ini hashable yap
        try:
            args_key = frozenset((k, str(v)) for k, v in sorted(arguments.items()))
        except Exception:
            # Hashable yapılamazsa, string'e çevir
            args_key = frozenset((k, str(v)) for k, v in arguments.items())

        call_key = (tool_name, args_key)

        if call_key in self._call_history:
            count, last_result = self._call_history[call_key]

            # 2 kez başarısız oldu mu?
            if count >= 2 and not last_result.get("success", True):
                error_msg = (
                    f"Bu tool çağrısı ({tool_name} {arguments}) "
                    f"2 kez başarısız oldu. Lütfen farklı bir strateji deneyin."
                )
                return True, error_msg, None

            # Aynı çağrı tekrar edildi mi?
            if count >= 1:
                message = (
                    f"Bu tool çağrısı ({tool_name} {arguments}) "
                    f"aynı görev sırasında zaten çalıştırıldı ve aynı sonuç alındı."
                )
                return True, message, last_result

        return False, None, None

    def _request_approval(self, tool_name: str, arguments: Dict[str, Any]) -> bool:
        """
        Kullanıcı onayı ister.

        NOT: auto_approve mekanizması YOK.
        requires_approval=True araçlar her zaman onay gerektirir.

        Args:
            tool_name: Tool adı
            arguments: Tool argümanları

        Returns:
            bool: Kullanıcı onay verdiyse True
        """
        if self.approval_callback is None:
            # Callback yoksa varsayılan olarak onay verme
            self.logger.warning(
                f"Onay callback yok. {tool_name} için onay REDDEDİLDİ."
            )
            return False

        try:
            return self.approval_callback(tool_name, arguments)
        except Exception as exc:
            self.logger.error(f"Onay callback hatası: {exc}")
            return False

    def _execute_tool_call(
        self,
        tool_call: ToolCall
    ) -> Dict[str, Any]:
        """
        Tool çağrısını güvenli şekilde çalıştırır.

        Args:
            tool_call: Tool çağrısı

        Returns:
            Dict: Sonuç
        """
        tool_name = tool_call.name
        arguments = tool_call.arguments

        # 1. Parametre doğrulaması
        is_valid, validation_error = self._validate_tool_call(tool_call)
        if not is_valid:
            return {
                "success": False,
                "error": f"Tool çağrısı geçersiz: {validation_error}"
            }

        # 2. Duplicate kontrolü
        is_duplicate, duplicate_message, cached_result = self._check_duplicate_call(tool_call)
        if is_duplicate:
            if cached_result is not None:
                # Cached sonuç var, onu döndür
                self._update_call_history(tool_call, cached_result)
                return {
                    "success": cached_result.get("success", False),
                    "cached": True,
                    "result": cached_result,
                    "message": duplicate_message
                }
            else:
                # 2 kez başarısız oldu, hata döndür
                return {
                    "success": False,
                    "error": duplicate_message
                }

        # 3. Tool kayıt kontrolü
        if not self.registry.has(tool_name):
            return {
                "success": False,
                "error": f"Tool bulunamadı: {tool_name}"
            }

        tool_info = self.registry.get_tool_info(tool_name)

        # 4. create_change_plan için özel orkestrasyon
        if tool_name == "create_change_plan":
            # test_file'i arguments'tan çıkar, create_plan bunu kabul etmez
            plan_args = {k: v for k, v in arguments.items() if k != "test_file"}
            test_file = arguments.get("test_file")
            
            result = self.registry.execute(name=tool_name, arguments=plan_args, approved=True)
            
            self.logger.info(f"create_change_plan sonucu: success={result.get('success')}")
            
            # Plan başarılıysa orkestratöre kaydet
            if result.get("success"):
                # result yapısını kontrol et
                result_data = result.get("result", {})
                if isinstance(result_data, dict):
                    validation = result_data.get("validation", {})
                    plan = result_data.get("plan")
                    
                    # Only a validated plan may enter the approval flow.
                    if validation.get("valid") and isinstance(plan, dict):
                        # Reuse the plan already generated by the registry.
                        self.change_orchestrator.set_plan_result(result_data)
                        
                        # test_file yoksa otomatik ara
                        if not test_file:
                            self.logger.info("test_file sağlanmadı, otomatik aranıyor...")
                            # Basit strateji: aynı dizindeki test_*.py dosyasını ara
                            from pathlib import Path
                            target_file = Path(arguments["file_path"])
                            target_dir = target_file.parent
                            
                            # test_ ile başlayan .py dosyasını ara
                            test_files = sorted(target_dir.glob("test_*.py"))
                            if test_files:
                                # Proje köküne göre relative path
                                project_root = Path(PROJECT_ROOT).resolve()
                                try:
                                    test_file = str(
                                        test_files[0].resolve().relative_to(project_root)
                                    )
                                except ValueError:
                                    test_file = None

                            if test_file:
                                self.logger.info(f"test_file bulundu: {test_file}")
                            else:
                                # Bulunamazsa hata
                                failure = {
                                    "success": False,
                                    "error": "test_file gerekli ve otomatik bulunamadı. Lütfen güvenli bir proje içi test dosyası belirtin.",
                                    "plan_result": result_data,
                                    "orchestration": {
                                        "state": self.change_orchestrator.get_state(),
                                        "approval": "not_requested",
                                        "apply_change": "not_started",
                                    },
                                }
                                self._update_call_history(tool_call, failure)
                                return failure
                        
                        # Orkestratör üzerinden onay iste
                        approved = self.change_orchestrator.request_approval()
                        
                        if approved:
                            # Orkestratör üzerinden apply_change
                            apply_result = self.change_orchestrator.apply_change(test_file)
                            
                            apply_result["orchestration"] = {
                                "state": self.change_orchestrator.get_state(),
                                "approval": "approved",
                                "test_file": test_file,
                                "apply_change": (
                                    "completed"
                                    if apply_result.get("success")
                                    else "failed"
                                ),
                            }
                            # apply_change sonucunu döndür
                            self._update_call_history(tool_call, apply_result)
                            return apply_result
                        else:
                            # Onay reddedildi
                            failure = {
                                "success": False,
                                "error": "Kullanıcı onayı reddedildi. Değişiklik uygulanmadı.",
                                "requires_approval": True,
                                "orchestration": {
                                    "state": self.change_orchestrator.get_state(),
                                    "approval": "rejected",
                                    "apply_change": "not_started",
                                },
                            }
                            self._update_call_history(tool_call, failure)
                            return failure
                    else:
                        self.logger.warning(f"Plan validation başarısız: {validation}")
                        failure = {
                            "success": False,
                            "error": "Değişiklik planı doğrulamadan geçemedi.",
                            "plan_result": result_data,
                            "orchestration": {
                                "state": self.change_orchestrator.get_state(),
                                "apply_change": "not_started",
                            },
                        }
                        self._update_call_history(tool_call, failure)
                        return failure
                else:
                    self.logger.warning(f"result beklenen formatta değil: {type(result_data)}")
                    failure = {
                        "success": False,
                        "error": "Değişiklik planı beklenen formatta değil.",
                    }
                    self._update_call_history(tool_call, failure)
                    return failure
            else:
                # Plan başarısız
                self._update_call_history(tool_call, result)
                return result

        # 5. Diğer araçlar için normal akış
        requires_approval = tool_info.get("requires_approval", False)

        if requires_approval:
            # Kullanıcı onayı iste
            approved = self._request_approval(tool_name, arguments)

            if not approved:
                # Call history'yi güncelle (başarısız)
                self._update_call_history(tool_call, {"success": False})
                return {
                    "success": False,
                    "error": f"Kullanıcı {tool_name} için onayı reddetti.",
                    "requires_approval": True
                }
        else:
            # Onay gerektirmeyen araçlar için approved=True
            approved = True

        # 6. Tool'u çalıştır
        # approved parametresi ToolRegistry'nin kendi güvenlik kontrolü için
        result = self.registry.execute(
            name=tool_name,
            arguments=arguments,
            approved=approved
        )

        # 7. Call history'yi güncelle
        self._update_call_history(tool_call, result)

        return result

    def _update_call_history(self, tool_call: ToolCall, result: Dict[str, Any]) -> None:
        """
        Call history'yi günceller.

        Args:
            tool_call: Tool çağrısı
            result: Tool sonucu
        """
        tool_name = tool_call.name
        arguments = tool_call.arguments

        try:
            args_key = frozenset((k, str(v)) for k, v in sorted(arguments.items()))
        except Exception:
            args_key = frozenset((k, str(v)) for k, v in arguments.items())

        call_key = (tool_name, args_key)

        if call_key in self._call_history:
            count, _ = self._call_history[call_key]
            self._call_history[call_key] = (count + 1, result)
        else:
            self._call_history[call_key] = (1, result)

    def _format_ai_prompt(self, user_task: str) -> str:
        """
        AI için sistem promptu oluşturur.

        Args:
            user_task: Kullanıcı görevi

        Returns:
            str: Tam prompt
        """
        tools_info = self.registry.get_detailed_tools_for_prompt()

        prompt = f"""Sen MuhammedAI Local Developer adlı yerel yazılım geliştirme asistanısın.

GÖREVİN:
{user_task}

{tools_info}

ARAÇ KULLANIM KURALLARI:
1. Bir araç kullanmak için JSON formatında çağrı yap:
   {{"tool": "tool_name", "arguments": {{"param": "value"}}}}

2. Her araç için DOĞRU parametre isimlerini ve türlerini kullanın.
   Yukarıdaki şemada belirtilen parametreleri kesinlikle takip edin.

3. DOSYA YOLLARI İÇİN ÖZEL KURALLAR:
   - Dosya yollarında mutlaka forward slash (/) kullanın, backslash (\) kullanmayın.
   - Dosya yollarında asla boşluk kullanmayın.
   - Directory ve dosya isimlerini tam ve doğru yazın, kısaltma veya typo yapmayın.
   - Örnek doğru format: "quality_tests/e2e_workspace/agent_task.py"
   - Örnek yanlış format: "quality_tests/e2: e2e_workspace/agent_task.py"

4. Birden fazla araç çağrısı gerekiyorsa, bunları sırayla yap.
   Her araç sonucunu alıp sonra bir sonrakini çağır.

5. run_python_file kullanıcı onayı gerektirir. create_change_plan ise plan için kullanıcı onayı alır ve onaydan sonra apply_change'i orkestratör üzerinden çalıştırır.

6. Aynı araç çağrısını tekrar tekrar yapmayın.
   Bir araç çağrısı başarısız olursa, farklı bir strateji deneyin.

7. DOSYA OKUMA: Kullanıcı proje dosyasını okuması isteniyorsa, read_file aracını MUTLAKA kullan.
   Dosyayı tahmin etmeyin, gerçekten okuyun.

8. KOD ARAMA: Kod içinde arama isteniyorsa, search_code aracını MUTLAKA kullan.

9. PROJE TARAMA: Proje/dosya taraması isteniyorsa, project_scan veya uygun tarama aracını MUTLAKA kullan.

10. HATA KONTROLÜ: Hata kontrolü isteniyorsa, detect_errors aracını MUTLAKA kullan.

11. DOSYA ÇALIŞTIRMA: Python dosyası çalıştırılması isteniyorsa, run_python_file aracını MUTLAKA kullan.
    Bu araç kullanıcı onayı gerektirir.

12. DOSYA DEĞİŞİKLİĞİ: Kullanıcı dosyada değişiklik istediğinde şu akışı KESİNLİKLE izle:
    - Gerekli dosyayı oku (read_file)
    - create_change_plan ile plan oluştur
    - Sistem planı kullanıcı onayına sunar; onay verilirse apply_change'i orkestratör üzerinden çalıştırır
    - Tool sonucu içindeki orchestration alanını kontrol ederek apply ve doğrulama durumunu bildir
    - Sonucu bildir
    Onay verilmeden apply_change kesinlikle çalışmamalı. Model onayı varsayamaz veya approved parametresiyle bypass edemez.
    create_change_plan sonucu orchestration.apply_change alanını içeriyorsa apply aşaması sistemce tamamlanmıştır;
    ayrıca apply_change çağrısı yapma.

    test_file parametresi için şu kuralları uygula:
    - İlgili test dosyası biliniyorsa create_change_plan çağrısında test_file olarak ver.
    - test_file verilmezse sistem yalnızca hedef dosyanın yanındaki test_*.py dosyasını otomatik arar.
    - Uygun test bulunamazsa rastgele dosya seçme; kullanıcıdan test dosyası iste.

    Ek kurallar:
    - create_change_plan sonucunu aldıktan sonra aynı planı gereksiz yere tekrar oluşturma.
    - Sadece plan oluşturmak görevi tamamlamak değildir. Kullanıcı açıkça kod değişikliği istediğinde, approval alındıktan sonra değişikliği gerçekten uygulamaya çalış.
    - Approval mekanizmasını hiçbir şekilde atlama. Approval alınmadan apply_change çalıştırma.
    - Dosya değişikliği görevlerinde final cevap vermeden önce değişikliğin gerçekten uygulanıp uygulanmadığını kontrol et.

13. Araç sonucunu aldıktan sonra, gerekiyorsa başka araç çağırabilirsin.
    Bir tool başarıyla sonuç döndürdüyse ve kullanıcı görevi henüz tamamlanmadıysa,
    tool sonucunu kullanarak bir sonraki gerekli tool çağrısını değerlendir.

14. Görev tamamlandığında, doğrudan kullanıcıya cevap ver.
    Araç çağrısı yapma.

15. Tahmin yapma. Bilmediğin şeyi "BİLİNMİYOR" olarak belirt.

16. Kod değişikliği yaparken mümkün olan en küçük değişikliği yap.

ÖNEMLİ:
- Genel bilgi, sohbet, kavramsal sorular için tool kullanmak zorunlu değil.
- Bir kullanıcı isteği gerçek proje dosyası, kod, hata, arama, çalıştırma veya değişiklik işlemi gerektiriyorsa,
  araç sonucu alınmadan görevin tamamlandığını söyleme.
- Dosya içeriğini tahmin etme veya genel bilgiyle gerçek dosya hakkında cevap verme.
- Parametre isimlerini yanlış kullanırsanız araç çalışmayacaktır.
"""

        return prompt

    def _requires_file_operation(self, user_task: str) -> bool:
        """
        Kullanıcı görevinin dosya okuma veya inceleme gerektirip gerektirmediğini tespit eder.

        Args:
            user_task: Kullanıcı görevi

        Returns:
            bool: Dosya işlemi gerekiyorsa True
        """
        file_keywords = [
            "oku", "içeriğini", "incele", "göster", "dosyadan", "bul",
            "read", "content", "show", "file", "inspect", "examine"
        ]

        user_task_lower = user_task.lower()

        # Dosya uzantısı kontrolü (.py, .txt, .md vb.)
        if "." in user_task and any(ext in user_task for ext in [".py", ".txt", ".md", ".json", ".yaml", ".yml"]):
            return True

        # Anahtar kelime kontrolü
        for keyword in file_keywords:
            if keyword in user_task_lower:
                return True

        return False

    def run(self, user_task: str) -> LoopResult:
        """
        Agent loop'u başlatır.

        Args:
            user_task: Kullanıcı görevi
        
        Returns:
            LoopResult: Sonuç
        """
        # Memory'yi temizle
        self.memory.clear()
        self.change_orchestrator.reset()

        # İlk kullanıcı mesajını ekle
        self.memory.add_user_message(user_task)

        # İstatistikleri sıfırla
        self.tool_call_log.clear()
        self._call_history.clear()

        iteration = 0
        final_response = ""
        no_tool_retry_count = 0  # Tool çağrısı olmadığında yeniden deneme sayacı

        while iteration < self.config.max_iterations:
            iteration += 1

            self.logger.info(f"Iteration {iteration}/{self.config.max_iterations}")

            # AI promptunu oluştur
            conversation = self.memory.get_conversation_text()
            system_prompt = self._format_ai_prompt(user_task)

            full_prompt = f"{system_prompt}\n\nKONUŞMA GEÇMİŞİ:\n{conversation}\n\nCEVABIN:"

            # AI'dan yanıt al
            try:
                ai_response = self.ai.chat(full_prompt)
            except Exception as exc:
                error_msg = f"AI hatası: {exc}"
                self.logger.error(error_msg)
                return LoopResult(
                    success=False,
                    final_response=error_msg,
                    iterations=iteration,
                    tool_calls=[],
                    error=error_msg
                )

            # AI yanıtını memory'ye ekle
            self.memory.add_assistant_message(ai_response)

            # Tool çağrılarını parse et
            parse_result = self.parser.parse(ai_response)

            if not parse_result.success:
                error_msg = f"Parse hatası: {parse_result.error}"
                self.logger.error(error_msg)
                return LoopResult(
                    success=False,
                    final_response=error_msg,
                    iterations=iteration,
                    tool_calls=[],
                    error=error_msg
                )

            # Tool çağrısı yoksa, kontrol et
            if not parse_result.tool_calls:
                # Sadece hiç tool çağrısı yapılmadıysa (ilk deneme) ve dosya işlemi gerekiyorsa yeniden den
                if not self.tool_call_log and self._requires_file_operation(user_task):
                    no_tool_retry_count += 1
                    self.logger.warning(f"Tool çağrısı yok, dosya işlemi gerekli. Yeniden deneme {no_tool_retry_count}/{self.config.max_no_tool_retries}")

                    if no_tool_retry_count < self.config.max_no_tool_retries:
                        # Modele görevin tamamlanmadığını bildir
                        self.memory.add_system_message(
                            "Bu görev dosya okuma veya inceleme gerektiriyor. "
                            "Dosya içeriğini tahmin etme veya genel bilgi verme. "
                            "read_file aracını kullanarak gerçek dosyayı oku."
                        )
                        continue
                    else:
                        # Sınır aşıldı, hata döndür
                        error_msg = (
                            "Bu görev dosya okuma gerektiriyor ancak tool çağrısı yapılmadı. "
                            "Dosya içeriğini tahmin edemiyorum. Lütfen görevi netleştirin."
                        )
                        self.logger.error(error_msg)
                        return LoopResult(
                            success=False,
                            final_response=error_msg,
                            iterations=iteration,
                            tool_calls=[],
                            error=error_msg
                        )
                else:
                    # Genel sohbet, bilgi görevi veya daha önce tool çağrısı yapıldı - bitir
                    final_response = ai_response
                    self.logger.info("Tool çağrısı yok, döngü tamamlandı.")
                    break

            # Tool çağrılarını çalıştır
            for tool_call in parse_result.tool_calls:
                # Tool'u doğrula
                available_tools = set(self.registry.list_tools())
                if not self.parser.validate_tool_call(tool_call, available_tools):
                    error_msg = f"Geçersiz tool çağrısı: {tool_call.name}"
                    self.logger.error(error_msg)

                    # Hatayı modele bildir
                    self.memory.add_tool_result(
                        tool_call.name,
                        {"error": error_msg},
                        False
                    )
                    continue

                # Tool'u çalıştır
                self.logger.info(f"Tool çağrılıyor: {tool_call.name}")

                try:
                    result = self._execute_tool_call(tool_call)
                except Exception as exc:
                    result = {
                        "success": False,
                        "error": f"Tool çalıştırma hatası: {exc}"
                    }
                    self.logger.error(f"Tool hatası: {exc}")

                # Sonucu logla
                log_entry = {
                    "iteration": iteration,
                    "tool": tool_call.name,
                    "arguments": tool_call.arguments,
                    "result": result
                }
                self.tool_call_log.append(log_entry)

                # Sonucu kırp ve memory'ye ekle
                truncated_result = self._truncate_tool_output(result)
                self.memory.add_tool_result(
                    tool_call.name,
                    truncated_result,
                    result.get("success", False)
                )

        # Maksimum iteration'a ulaşıldı mı?
        if iteration >= self.config.max_iterations:
            self.logger.warning(
                f"Maksimum iteration ({self.config.max_iterations}) aşıldı."
            )
            final_response = ai_response if ai_response else "Iteration limiti aşıldı."

        return LoopResult(
            success=True,
            final_response=final_response,
            iterations=iteration,
            tool_calls=self.tool_call_log
        )

    def get_tool_call_log(self) -> List[Dict[str, Any]]:
        """Tool çağrı logunu döndürür."""
        return self.tool_call_log.copy()

    def get_conversation_history(self) -> List[Dict[str, str]]:
        """Konuşma geçmişini döndürür."""
        return self.memory.get_messages()


if __name__ == "__main__":
    # Basit test (Ollama çalışmadığı için sadece import testi)
    print("AgentLoop modülü yüklendi.")
