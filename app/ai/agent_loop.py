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
from app.ai.memory import MemorySystem
from app.ai.agent_session import AgentSession, SessionStatus
from app.ai.agent_context_builder import AgentContextBuilder
from app.ai.project_rules import ProjectRules
from app.tools.tool_registry import ToolRegistry
from app.core.config import PROJECT_ROOT


@dataclass
class LoopConfig:
    """Agent Loop yapılandırması."""
    max_iterations: int = 10
    max_tool_output_length: int = 2000  # Karakter cinsinden
    enable_logging: bool = True
    max_no_tool_retries: int = 2  # Tool çağrısı olmadığında maksimum yeniden deneme sayısı
    max_correction_attempts: int = 3  # Maksimum correction deneme sayısı


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

        # AgentSession ve ContextBuilder
        self.session: Optional[AgentSession] = None
        self.codebase_index = getattr(self.registry, 'codebase_index', None)
        self.memory_system = MemorySystem()
        self.project_rules = ProjectRules()
        self.context_builder = AgentContextBuilder(
            max_recent_messages=self.config.max_recent_messages if hasattr(self.config, 'max_recent_messages') else 10,
            max_tool_history=self.config.max_tool_history if hasattr(self.config, 'max_tool_history') else 5,
            max_test_history=self.config.max_test_history if hasattr(self.config, 'max_test_history') else 3,
            max_context_chars=self.config.max_context_chars if hasattr(self.config, 'max_context_chars') else 10000,
            codebase_index=self.codebase_index,
            memory_system=self.memory_system,
            project_rules=self.project_rules
        )

        # Logger
        self.logger = logging.getLogger(__name__)
        if self.config.enable_logging:
            logging.basicConfig(level=logging.INFO)

        # İstatistikler
        self.tool_call_log: List[Dict[str, Any]] = []

        # Duplicate tracking: (tool_name, frozenset(arguments.items())) -> (count, last_result)
        self._call_history: Dict[tuple, tuple] = {}

        # Correction loop tracking
        self._correction_history: List[Dict[str, Any]] = []
        self._correction_attempt: int = 0

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
            result = self.approval_callback(tool_name, arguments)
            
            # Awaitable kontrolü - async callback senkron çağrıldıysa
            import inspect
            if inspect.isawaitable(result):
                # Coroutine ise kapat (RuntimeWarning önlemek için)
                if inspect.iscoroutine(result):
                    result.close()
                self.logger.error(
                    f"Onay callback awaitable döndürdü (async callback senkron çağrıldı). "
                    f"{tool_name} için onay REDDEDİLDİ."
                )
                return False
            
            # Sonucun gerçek bool olduğunu kontrol et
            if not isinstance(result, bool):
                self.logger.error(
                    f"Onay callback bool döndürmedi: {type(result)}. "
                    f"{tool_name} için onay REDDEDİLDİ."
                )
                return False
            
            return result
        except Exception as exc:
            self.logger.error(f"Onay callback hatası: {exc}")
            return False

    def _execute_tool_call(
        self,
        tool_call: ToolCall,
        iteration: int = 0
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
                # Orchestration bilgisini koru
                return {
                    "success": cached_result.get("success", False),
                    "cached": True,
                    "result": cached_result,
                    "message": duplicate_message,
                    **{k: v for k, v in cached_result.items() if k not in ["success", "result"]}
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
            
            # Dosya henüz okunmamışsa otomatik olarak oku
            file_path = arguments.get("file_path")
            if file_path:
                # Dosyanın daha önce okunup okunmadığını kontrol et
                file_already_read = False
                for call in self.tool_call_log:
                    if call.get("tool") == "read_file" and call.get("arguments", {}).get("relative_path") == file_path:
                        file_already_read = True
                        break
                
                if not file_already_read:
                    self.logger.info(f"Dosya henüz okunmamış, otomatik okunuyor: {file_path}")
                    # read_file çağrısı yap
                    read_result = self.registry.execute(
                        name="read_file",
                        arguments={"relative_path": file_path},
                        approved=False
                    )
                    
                    # Sonucu tool_call_log'a ekle
                    log_entry = {
                        "iteration": iteration,
                        "tool": "read_file",
                        "arguments": {"relative_path": file_path},
                        "result": read_result,
                        "auto_inserted": True
                    }
                    self.tool_call_log.append(log_entry)
                    
                    # Sonucu memory'ye ekle
                    self.memory.add_tool_result(
                        "read_file",
                        read_result,
                        read_result.get("success", False)
                    )
                    
                    self.logger.info(f"Otomatik dosya okuma tamamlandı: success={read_result.get('success')}")
            
            result = self.registry.execute(name=tool_name, arguments=plan_args, approved=True)
            
            self.logger.info(f"create_change_plan sonucu: success={result.get('success')}")
            
            # Plan başarılıysa orkestratöre kaydet
            if result.get("success"):
                # result yapısını kontrol et
                result_data = result.get("result", {})
                if isinstance(result_data, dict):
                    validation = result_data.get("validation", {})
                    plan = result_data.get("plan")
                    
                    # Validation başarısızsa hata döndür
                    if not validation.get("valid"):
                        error_msg = f"Plan validation hatası: {validation.get('errors', [])}"
                        self.logger.warning(error_msg)
                        result["success"] = False
                        result["error"] = error_msg
                        return result
                    
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

                            # apply_change çağrısını tool_call_log'a ekle
                            log_entry = {
                                "iteration": iteration,
                                "tool": "apply_change",
                                "arguments": {
                                    "plan": result_data.get("plan"),
                                    "test_file": test_file,
                                    "approved": True
                                },
                                "result": apply_result
                            }
                            self.tool_call_log.append(log_entry)

                            # Test başarısız mı? Correction loop başlat
                            if not apply_result.get("success"):
                                # Maksimum deneme sınırını kontrol et (artırma öncesi)
                                if self._correction_attempt >= self.config.max_correction_attempts:
                                    # Maksimum deneme aşıldı, durdur
                                    failure = {
                                        "success": False,
                                        "error": f"Maksimum correction deneme sayısı aşıldı ({self.config.max_correction_attempts}). Son deneme başarısız oldu.",
                                        "correction_history": self._correction_history,
                                        "orchestration": {
                                            "state": self.change_orchestrator.get_state(),
                                            "approval": "approved",
                                            "apply_change": "failed",
                                            "max_attempts_reached": True
                                        }
                                    }
                                    self._update_call_history(tool_call, failure)
                                    return failure

                                # Sayaç artır
                                self._correction_attempt += 1

                                # Correction history'e ekle
                                correction_entry = {
                                    "attempt": self._correction_attempt,
                                    "test_file": test_file,
                                    "test_result": apply_result.get("test"),
                                    "test_failure_details": apply_result.get("test_failure_details"),
                                    "plan": result_data.get("plan"),
                                    "approval": "approved",
                                    "success": False
                                }
                                self._correction_history.append(correction_entry)

                                # Orchestrator'ı correction için hazırla
                                self.change_orchestrator.reset_for_correction()

                                # Test failure details'ı agent context'ine ekle
                                failure_details = apply_result.get("test_failure_details", {})
                                error_context = f"""
Test başarısız oldu (Deneme {self._correction_attempt}/{self.config.max_correction_attempts}):
Test dosyası: {test_file}
Hata: {failure_details.get('error', 'Bilinmeyen hata')}
Stdout: {failure_details.get('stdout', '')}
Stderr: {failure_details.get('stderr', '')}
Return code: {failure_details.get('returncode', '')}

Lütfen hatayı analiz edip yeni bir düzeltme planı oluşturun.
"""
                                self.memory.add_system_message(error_context)

                                # apply_change sonucunu döndür ama correction devam etsin
                                apply_result["correction_history"] = self._correction_history
                                apply_result["correction_attempt"] = self._correction_attempt
                                self._update_call_history(tool_call, apply_result)
                                return apply_result
                            else:
                                # Test başarılı, correction history'ye ekle
                                if self._correction_attempt > 0:
                                    correction_entry = {
                                        "attempt": self._correction_attempt,
                                        "test_file": test_file,
                                        "test_result": apply_result.get("test"),
                                        "plan": result_data.get("plan"),
                                        "approval": "approved",
                                        "success": True
                                    }
                                    self._correction_history.append(correction_entry)
                                    apply_result["correction_history"] = self._correction_history
                                    apply_result["correction_attempt"] = self._correction_attempt

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

                            # Correction history'ye ekle (onay reddedildi)
                            if self._correction_attempt > 0:
                                correction_entry = {
                                    "attempt": self._correction_attempt,
                                    "test_file": test_file,
                                    "plan": result_data.get("plan"),
                                    "approval": "rejected",
                                    "success": False
                                }
                                self._correction_history.append(correction_entry)
                                failure["correction_history"] = self._correction_history
                                failure["correction_attempt"] = self._correction_attempt

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
   - Dosya yollarında mutlaka forward slash (/) kullanın, backslash (\\) kullanmayın.
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
   read_file artık offset ve limit parametrelerini destekler. Uzun dosyalar için offset kullanarak devam okuma yapabilirsiniz.
   Örnek: İlk 100 satır için offset=0, limit=100; Sonraki 100 satır için offset=100, limit=100.

8. KOD ARAMA: Kod içinde arama isteniyorsa, search_code aracını MUTLAKA kullan.

9. PROJE TARAMA: Proje/dosya taraması isteniyorsa, project_scan veya uygun tarama aracını MUTLAKA kullan.

10. HATA KONTROLÜ: Hata kontrolü isteniyorsa, detect_errors aracını MUTLAKA kullan.

11. DOSYA ÇALIŞTIRMA: Python dosyası çalıştırılması isteniyorsa, run_python_file aracını MUTLAKA kullan.
    Bu araç kullanıcı onayı gerektirir.

12. TERMINAL KOMUTLARI: Terminal komutu çalıştırılması isteniyorsa (örn: git status, npm install), execute_terminal_command aracını MUTLAKA kullan.
    Bu araç kullanıcı onayı gerektirir. Komut çıktısı stdout ve stderr alanlarında döner.

13. DOSYA DEĞİŞİKLİĞİ: Kullanıcı dosyada değişiklik istediğinde şu akışı KESİNLİKLE izle:
    - Gerekli dosyayı oku (read_file)
    - create_change_plan ile plan oluştur (sadece file_path ve problem parametreleri)
    - Sistem planı kullanıcı onayına sunar; onay verilirse apply_change'i orkestratör üzerinden çalıştırır
    - Tool sonucu içindeki orchestration alanını kontrol ederek apply ve doğrulama durumunu bildir
    - Sonucu bildir
    Onay verilmeden apply_change kesinlikle çalışmamalı. Model onayı varsayamaz veya approved parametresiyle bypass edemez.
    create_change_plan sonucu orchestration.apply_change alanını içeriyorsa apply aşaması sistemce tamamlanmıştır;
    ayrıca apply_change çağrısı yapma.

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

16. KOD İNCELEME: Kullanıcı kod incelemesi istediğinde:
    - Dosyayı gerçekten oku (read_file kullan)
    - HATA BULMA SORUNLARINDA: Sadece dosyada gördüğün gerçek kodla desteklenen hataları bildir.
    - Kanıtınız yoksa veya dosya tam okunmadıysa hata uydurma.
    - Hata bulamazsanız açıkça "Hata bulunamadı" deyin, genel tahminlerde bulunma.
    - Dosya içeriği kesilmişse veya tam okunamadıysa bunu açıkça belirtin.
    - Genel Python açıklamaları yeterli değildir; bulgular mutlaka dosyadan alınan kodla desteklenmeli.

17. Kod değişikliği yaparken mümkün olan en küçük değişikliği yap.

18. ÖNEMLİ: Proje taraması (project_tree, project_scan) sadece proje yapısını anlamak içindir.
    Kullanıcı belirli bir dosyada değişiklik istiyorsa, proje taraması yapıp durma.
    Mutlaka ilgili dosyayı read_file ile oku ve create_change_plan ile değişiklik yap.
    Proje taraması sonrası görev tamamlanmış sayılmaz.

ÖNEMLİ:
- Genel bilgi, sohbet, kavramsal sorular için tool kullanmak zorunlu değil.
- Dosya içeriğini tahmin etme veya genel bilgiyle gerçek dosya hakkında cevap verme.
- Parametre isimlerini yanlış kullanırsanız araç çalışmayacaktır.
- Terminal komutları (git status, python --version vb.) için execute_terminal_command aracını KULLANMALISINIZ.
- Sistem bilgisi veya sürüm kontrolü için araç kullanmak ZORUNLUDUR.
- Terminal komutu çalıştırdıktan sonra sonucu kullanarak cevap verin, GEREKSİZ tool calls yapmayın.
- Git status, python --version gibi basit komutlar için sadece terminal aracı kullanın ve sonucu açıklayın.
- Git status sonucunu aldıktan sonra, sonucu doğrudan açıklayın. Proje taraması veya diğer araçlar yapmayın.
- KESİNLİKLE: Git status veya python --version gibi basit terminal komutlarında, komut sonucunu aldıktan sonra DİĞER HİÇBİR ARACI ÇAĞIRMA. Sadece sonucu açıkla ve görevi tamamla.
```"""

        return prompt

    def _requires_file_operation(self, user_task: str, has_target_file: bool = False) -> bool:
        r"""
        Kullanıcı görevinin dosya okuma veya inceleme gerektirip gerektirmediğini tespit eder.

        Args:
            user_task: Kullanıcı görevi
            has_target_file: Hedef dosya zaten belirlenmiş mi (inspection-only için)

        Returns:
            bool: Dosya işlemi gerekiyorsa True
        """
        # Inspection-only görevde hedef dosya zaten okunduysa ek işlem gerekmez
        if has_target_file:
            return False

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

    def _is_inspection_only_task(self, user_task: str) -> bool:
        """
        Kullanıcı görevinin yalnızca kod inceleme/hata bulma isteği olup olmadığını tespit eder.

        Args:
            user_task: Kullanıcı görevi

        Returns:
            bool: Sadece inceleme/hata bulma ise True
        """
        inspection_keywords = [
            "incele", "review", "analyze", "hata bul", "açıkla", "öner",
            "examine", "inspect", "analyze", "find error", "explain", "suggest",
            "kontrol et", "check", "investigate"
        ]

        # Negasyon anahtar kelimeleri (değiştirme isteği olmadığını belirtir)
        negation_keywords = [
            "değiştirme", "değişiklik yapma", "henüz değiştirme", "değiştirmeden",
            "don't change", "without changing", "without", "no change", "don't modify"
        ]

        user_task_lower = user_task.lower()

        # Inceleme anahtar kelimesi var mı?
        has_inspection_keyword = any(keyword in user_task_lower for keyword in inspection_keywords)

        # Negasyon var mı?
        has_negation = any(keyword in user_task_lower for keyword in negation_keywords)

        # Kod değişikliği anahtar kelimeleri
        code_change_keywords = [
            "oluştur", "ekle", "değiştir", "düzenle", "güncelle", "sil", "yaz", "implement",
            "create", "add", "change", "modify", "update", "delete", "write", "implement", "fix", "refactor"
        ]

        has_code_change_keyword = any(keyword in user_task_lower for keyword in code_change_keywords)

        # Inceleme anahtar kelimesi var, negasyon var VE kod değişikliği anahtar kelimesi yoksa inspection-only görev
        # Veya inceleme anahtar kelimesi var ama kod değişikliği anahtar kelimesi yoksa
        return has_inspection_keyword and (has_negation or not has_code_change_keyword)

    def _is_test_only_task(self, user_task: str) -> bool:
        """
        Kullanıcı görevinin yalnızca test/çalıştırma isteği olup olmadığını tespit eder.

        Args:
            user_task: Kullanıcı görevi

        Returns:
            bool: Sadece test/çalıştırma ise True
        """
        test_keywords = [
            "test", "çalıştır", "run", "verify", "doğrula", "kontrol et",
            "check", "execute", "test et", "çalıştır", "doğrula"
        ]

        user_task_lower = user_task.lower()

        # Test anahtar kelimesi var mı?
        has_test_keyword = any(keyword in user_task_lower for keyword in test_keywords)

        # Kod değişikliği anahtar kelimeleri
        code_change_keywords = [
            "oluştur", "ekle", "değiştir", "düzenle", "güncelle", "sil", "yaz", "implement",
            "create", "add", "change", "modify", "update", "delete", "write", "implement", "fix", "refactor"
        ]

        has_code_change_keyword = any(keyword in user_task_lower for keyword in code_change_keywords)

        # Test anahtar kelimesi var ama kod değişikliği anahtar kelimesi yoksa test-only görev
        return has_test_keyword and not has_code_change_keyword

    def _requires_code_change(self, user_task: str) -> bool:
        """
        Kullanıcı görevinin kod değişikliği gerektirip gerektirmediğini tespit eder.

        Args:
            user_task: Kullanıcı görevi

        Returns:
            bool: Kod değişikliği gerekiyorsa True
        """
        # Test-only görevleri hariç tut
        if self._is_test_only_task(user_task):
            return False

        # Inspection-only görevleri hariç tut
        if self._is_inspection_only_task(user_task):
            return False

        code_change_keywords = [
            "oluştur", "ekle", "değiştir", "düzenle", "güncelle", "sil", "yaz", "implement",
            "create", "add", "change", "modify", "update", "delete", "write", "implement", "fix", "refactor"
        ]

        user_task_lower = user_task.lower()

        # Dosya yolu ve kod değişikliği anahtar kelimesi kombinasyonu
        has_file_path = "." in user_task or "/" in user_task or "\\" in user_task

        for keyword in code_change_keywords:
            if keyword in user_task_lower:
                return True

        return False

    def _extract_file_path_from_task(self, user_task: str) -> Optional[str]:
        """
        Kullanıcı görevinden dosya yolunu çıkarır.

        Args:
            user_task: Kullanıcı görevi

        Returns:
            Optional[str]: Dosya yolu veya None
        """
        import re
        # Dosya yolu desenleri: .py, .txt, .md vb. uzantılı yollar
        patterns = [
            r'[\w/\\]+\.py',
            r'[\w/\\]+\.txt',
            r'[\w/\\]+\.md',
            r'[\w/\\]+\.json',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, user_task)
            if match:
                return match.group(0)
        
        return None

    def _find_test_file(self, file_path: str) -> Optional[str]:
        """
        Verilen dosya için test dosyasını bulur.

        Args:
            file_path: Kaynak dosya yolu

        Returns:
            Optional[str]: Test dosya yolu veya None
        """
        from pathlib import Path
        path = Path(file_path)
        
        # Aynı dizindeki test_*.py dosyalarını ara
        parent = path.parent
        test_files = list(parent.glob("test_*.py"))
        
        if test_files:
            return str(test_files[0])
        
        # Dosya adından test dosyası adı türet
        test_name = f"test_{path.name}"
        test_path = parent / test_name
        if test_path.exists():
            return str(test_path)
        
        return None

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
        self._correction_history.clear()
        self._correction_attempt = 0

        # Kod değişikliği görevi mi?
        is_code_change_task = self._requires_code_change(user_task)
        if is_code_change_task:
            self.logger.info("Kod değişikliği görevi tespit edildi")

        # Test-only görev mi?
        is_test_only_task = self._is_test_only_task(user_task)
        if is_test_only_task:
            self.logger.info("Test-only görev tespit edildi")

        # Inspection-only görev mi?
        is_inspection_only_task = self._is_inspection_only_task(user_task)
        if is_inspection_only_task:
            self.logger.info("Inspection-only görev tespit edildi")

        # Inspection-only görev için hedef dosya yolunu çıkar
        target_file_path = None
        target_file_content = None
        if is_inspection_only_task:
            target_file_path = self._extract_file_path_from_task(user_task)
            if target_file_path:
                self.logger.info(f"Hedef dosya: {target_file_path}")
                
                # Hedef dosyayı modelden önce oku (deterministik)
                try:
                    from app.tools.file_reader import FileReader
                    from app.core.config import PROJECT_ROOT
                    reader = FileReader(project_root=PROJECT_ROOT)
                    target_file_content = reader.read(target_file_path)
                    
                    # FileReader dictionary döndürebilir, content alanını al
                    if isinstance(target_file_content, dict):
                        content_to_show = target_file_content.get('content', '')
                        self.logger.info(f"Hedef dosya okundu: {len(content_to_show)} karakter")
                    else:
                        content_to_show = target_file_content
                        self.logger.info(f"Hedef dosya okundu: {len(content_to_show)} karakter")
                    
                    # Dosya içeriği çok uzunsa truncate et (model context limiti için)
                    max_content_length = 8000
                    if len(content_to_show) > max_content_length:
                        content_to_show = content_to_show[:max_content_length]
                        content_to_show += f"\n\n... (Dosya içeriği {len(target_file_content)} karakter, ilk {max_content_length} karakter gösteriliyor)"
                    
                    # Okunan içeriği modele bağlam olarak ver
                    self.memory.add_system_message(
                        f"HEDEF DOSYA İÇERİĞİ ({target_file_path}):\n{content_to_show}\n"
                        f"Bu dosya incelemesi için yukarıdaki içeriği kullan. "
                        f"Bu dosyayı tekrar okumaya çalışma."
                    )
                except FileNotFoundError:
                    error_msg = f"Hedef dosya bulunamadı: {target_file_path}"
                    self.logger.error(error_msg)
                    return LoopResult(
                        success=False,
                        final_response=error_msg,
                        iterations=0,
                        tool_calls=[],
                        error=error_msg
                    )
                except Exception as e:
                    error_msg = f"Hedef dosya okuma hatası: {e}"
                    self.logger.error(error_msg)
                    return LoopResult(
                        success=False,
                        final_response=error_msg,
                        iterations=0,
                        tool_calls=[],
                        error=error_msg
                    )

        iteration = 0
        final_response = ""
        no_tool_retry_count = 0  # Tool çağrısı olmadığında yeniden deneme sayacı

        while iteration < self.config.max_iterations:
            iteration += 1

            self.logger.info(f"Iteration {iteration}/{self.config.max_iterations}")

            # AI promptunu oluştur
            system_prompt = self._format_ai_prompt(user_task)
            
            # Conversation history'yi Ollama messages formatına çevir
            ollama_messages = self.memory.get_messages()
            
            # System prompt'u en başa ekle
            if ollama_messages and ollama_messages[0].get("role") != "system":
                ollama_messages.insert(0, {"role": "system", "content": system_prompt})
            elif not ollama_messages:
                ollama_messages = [{"role": "system", "content": system_prompt}]

            # AI'dan yanıt al (tools parametresiyle)
            tools = self.registry.get_ollama_tools() if hasattr(self.registry, 'get_ollama_tools') else None
            try:
                ai_response_dict = self.ai.chat(message="", tools=tools, messages=ollama_messages)
                ai_response = ai_response_dict.get("content", "")
                ai_tool_calls = ai_response_dict.get("tool_calls")
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

            # Native tool_calls kontrolü
            if ai_tool_calls:
                # Native tool calls var, tool_call_id'leri oluştur
                import uuid
                tool_call_ids = [str(uuid.uuid4()) for _ in ai_tool_calls]
                
                # AI yanıtını memory'ye ekle (tool_calls ve tool_call_ids ile)
                self.memory.add_assistant_message(ai_response, tool_calls=ai_tool_calls, tool_call_ids=tool_call_ids)
                
                # Native tool calls işle
                self.logger.info(f"Native tool_calls alındı: {len(ai_tool_calls)}")
                for tc, tool_call_id in zip(ai_tool_calls, tool_call_ids):
                    # Ollama tool_calls formatını ToolCall'a çevir
                    tool_name = tc.function.name if hasattr(tc, 'function') else tc.get('function', {}).get('name')
                    tool_args = tc.function.arguments if hasattr(tc, 'function') else tc.get('function', {}).get('arguments', {})
                    
                    # Kod değişikliği görevinde araç sınırlama
                    if is_code_change_task:
                        allowed_tools = {"read_file", "create_change_plan", "run_python_file", "search_code", "project_scan", "project_tree"}
                        if tool_name not in allowed_tools:
                            error_msg = f"Kod değişikliği görevi için izin verilmeyen araç: {tool_name}. Sadece dosya okuma, plan oluşturma ve test araçlarına izin var."
                            self.logger.warning(error_msg)
                            self.memory.add_tool_result(tool_name, {"error": error_msg}, False, tool_call_id=tool_call_id)
                            continue
                    
                    # Inspection-only görevde araç sınırlama
                    if is_inspection_only_task and target_file_path:
                        # Hedef dosya zaten okundu, sadece salt okunur araçlara izin ver
                        allowed_tools = {"search_code", "project_scan", "project_tree"}
                        if tool_name not in allowed_tools:
                            error_msg = f"Inspection-only görev için izin verilmeyen araç: {tool_name}. Hedef dosya zaten okundu. Sadece arama araçlarına izin var."
                            self.logger.warning(error_msg)
                            self.memory.add_tool_result(tool_name, {"error": error_msg}, False, tool_call_id=tool_call_id)
                            continue
                    
                    # Tekrarlanan başarısız çağrı kontrolü
                    call_key = (tool_name, frozenset(sorted(tool_args.items())))
                    if call_key in self._call_history:
                        count, prev_result = self._call_history[call_key]
                        if not prev_result.get("success", True) and count >= 3:
                            error_msg = f"Aynı araç çağrısı ({tool_name}) 3 kez başarısız oldu. Farklı bir strateji deneyin."
                            self.logger.warning(error_msg)
                            self.memory.add_tool_result(tool_name, {"error": error_msg}, False, tool_call_id=tool_call_id)
                            continue
                    
                    tool_call = ToolCall(name=tool_name, arguments=tool_args, raw_text=str(tc))
                    parse_result = ParseResult(success=True, tool_calls=[tool_call], raw_response=str(tc))
                    
                    # Tool çağrısını yürüt
                    result = self._execute_tool_call(tool_call, iteration)
                    
                    # Sonucu memory'ye ekle (tool_call_id ile)
                    self.memory.add_tool_result(tool_name, result, result.get("success", False), tool_call_id=tool_call_id)
                    
                    # Log
                    log_entry = {
                        "iteration": iteration,
                        "tool": tool_name,
                        "arguments": tool_args,
                        "result": result,
                        "tool_call_id": tool_call_id
                    }
                    self.tool_call_log.append(log_entry)
                
                # Native tool_calls işlendi, bir sonraki iterasyona geç
                continue
            
            # Tool çağrılarını parse et (metin tabanlı fallback)
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
                # Test-only görev: model tool çağrısı yapmadı, testleri doğrudan çalıştır
                if is_test_only_task:
                    self.logger.info("Test-only görev: testler doğrudan çalıştırılıyor")
                    
                    # Dosya yolunu çıkar
                    file_path = self._extract_file_path_from_task(user_task)
                    if not file_path:
                        error_msg = "Test dosyası belirsiz. Lütfen dosya yolunu belirtin."
                        self.logger.error(error_msg)
                        return LoopResult(
                            success=False,
                            final_response=error_msg,
                            iterations=iteration,
                            tool_calls=self.tool_call_log,
                            error=error_msg
                        )
                    
                    # Testi çalıştır
                    try:
                        run_result = self.registry.execute(
                            name="run_python_file",
                            arguments={"file_path": file_path},
                            approved=True  # Test-only görevler güvenli, onay gerekmez
                        )
                        
                        if run_result.get("success"):
                            output = run_result.get("stdout", "")
                            stderr = run_result.get("stderr", "")
                            returncode = run_result.get("returncode", 0)
                            
                            # Test sonucunu değerlendir
                            test_passed = returncode == 0 and not stderr
                            
                            response_msg = f"Test çalıştırıldı: {file_path}\n"
                            response_msg += f"Çıkış kodu: {returncode}\n"
                            if output:
                                response_msg += f"Çıktı:\n{output}\n"
                            if stderr:
                                response_msg += f"Hata:\n{stderr}\n"
                            response_msg += f"Sonuç: {'BAŞARILI' if test_passed else 'BAŞARISIZ'}"
                            
                            return LoopResult(
                                success=test_passed,
                                final_response=response_msg,
                                iterations=iteration,
                                tool_calls=self.tool_call_log,
                                error=None if test_passed else "Test başarısız"
                            )
                        else:
                            error_msg = f"Test çalıştırma hatası: {run_result.get('error', 'Bilinmeyen hata')}"
                            self.logger.error(error_msg)
                            return LoopResult(
                                success=False,
                                final_response=error_msg,
                                iterations=iteration,
                                tool_calls=self.tool_call_log,
                                error=error_msg
                            )
                    except Exception as e:
                        error_msg = f"Test çalıştırma hatası: {e}"
                        self.logger.error(error_msg)
                        return LoopResult(
                            success=False,
                            final_response=error_msg,
                            iterations=iteration,
                            tool_calls=self.tool_call_log,
                            error=error_msg
                        )
                
                # Kod değişikliği görevi: model tool çağrısı yapmadı
                # Gerekli araçlar (create_change_plan) çağrılmadıysa ChangeWorkflow'u tetikle
                if is_code_change_task:
                    has_create_change_plan = any(call.get("tool") == "create_change_plan" for call in self.tool_call_log)
                    
                    if not has_create_change_plan:
                        self.logger.info("Kod değişikliği görevi: gerekli araçlar çağrılmadı, ChangeWorkflow tetikleniyor")
                        
                        # Dosya yolunu kullanıcı görevinden çıkar
                        file_path = self._extract_file_path_from_task(user_task)
                        if not file_path:
                            error_msg = "Hedef dosya belirsiz. Lütfen dosya yolunu belirtin."
                            self.logger.error(error_msg)
                            return LoopResult(
                                success=False,
                                final_response=error_msg,
                                iterations=iteration,
                                tool_calls=self.tool_call_log,
                                error=error_msg
                            )
                        
                        # ChangeWorkflow'u kullan
                        from app.tools.change_workflow import ChangeWorkflow
                        workflow = ChangeWorkflow()
                        
                        # Dosyayı oku
                        try:
                            read_result = self.registry.execute(
                                name="read_file",
                                arguments={"relative_path": file_path},
                                approved=False
                            )
                            if not read_result.get("success"):
                                error_msg = f"Dosya okuma hatası: {read_result.get('error', 'Bilinmeyen hata')}"
                                self.logger.error(error_msg)
                                return LoopResult(
                                    success=False,
                                    final_response=error_msg,
                                    iterations=iteration,
                                    tool_calls=self.tool_call_log,
                                    error=error_msg
                                )
                        except Exception as e:
                            error_msg = f"Dosya okuma hatası: {e}"
                            self.logger.error(error_msg)
                            return LoopResult(
                                success=False,
                                final_response=error_msg,
                                iterations=iteration,
                                tool_calls=self.tool_call_log,
                                error=error_msg
                            )
                        
                        # Plan oluştur
                        problem = user_task  # Kullanıcı görevini problem olarak kullan
                        plan_result = workflow.create_plan(file_path, problem)
                        
                        if not plan_result.get("validation", {}).get("valid"):
                            error_msg = f"Plan doğrulama hatası: {plan_result.get('validation', {}).get('errors', [])}"
                            self.logger.error(error_msg)
                            return LoopResult(
                                success=False,
                                final_response=error_msg,
                                iterations=iteration,
                                tool_calls=self.tool_call_log,
                                error=error_msg
                            )
                        
                        # Onay iste
                        plan = plan_result.get("plan", {})
                        approved = self._request_approval(
                            tool_name="create_change_plan",
                            arguments={"file_path": file_path, "problem": problem}
                        )
                        
                        if not approved:
                            error_msg = "Değişiklik planı kullanıcı tarafından reddedildi."
                            self.logger.warning(error_msg)
                            return LoopResult(
                                success=False,
                                final_response=error_msg,
                                iterations=iteration,
                                tool_calls=self.tool_call_log,
                                error=error_msg
                            )
                        
                        # Değişikliği uygula
                        test_file = self._find_test_file(file_path)
                        
                        # Test dosyası yoksa, değişikliği uygulamayı durdur
                        if not test_file:
                            error_msg = f"Test dosyası bulunamadı: {file_path}. Değişiklik güvenli olarak uygulanamadı."
                            self.logger.error(error_msg)
                            return LoopResult(
                                success=False,
                                final_response=error_msg,
                                iterations=iteration,
                                tool_calls=self.tool_call_log,
                                error=error_msg
                            )
                        
                        apply_result = workflow.apply_change(plan, test_file, approved=True)
                        self.logger.info(f"Apply result: {apply_result}")
                        
                        if not apply_result.get("success"):
                            error_msg = f"Değişiklik uygulama hatası: {apply_result.get('message', str(apply_result))}"
                            self.logger.error(f"Apply failed: {apply_result}")
                            return LoopResult(
                                success=False,
                                final_response=error_msg,
                                iterations=iteration,
                                tool_calls=self.tool_call_log,
                                error=error_msg
                            )
                        
                        # Başarılı
                        final_response = f"Değişiklik başarıyla uygulandı: {file_path}"
                        self.logger.info(final_response)
                        return LoopResult(
                            success=True,
                            final_response=final_response,
                            iterations=iteration,
                            tool_calls=self.tool_call_log
                        )
                
                # Sadece hiç tool çağrısı yapılmadıysa (ilk deneme) ve dosya işlemi gerekiyorsa yeniden den
                if not self.tool_call_log and self._requires_file_operation(user_task, has_target_file=(target_file_path is not None)):
                    no_tool_retry_count += 1
                    self.logger.warning(f"Tool çağrısı yok, dosya işlemi gerekli. Yeniden deneme {no_tool_retry_count}/{self.config.max_no_tool_retries}")

                    if no_tool_retry_count < self.config.max_no_tool_retries:
                        # Modele görevin tamamlanmadığını bildir
                        # Inspection-only görevde hedef dosya belirtilmişse bunu vurgula
                        if is_inspection_only_task and target_file_path:
                            self.memory.add_system_message(
                                f"Bu görev dosya incelemesi gerektiriyor. "
                                f"Hedef dosya: {target_file_path}. "
                                f"Bu dosyayı read_file aracını kullanarak oku. "
                                f"Başka bir dosyayı okuma."
                            )
                        else:
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

                # Kod değişikliği görevinde araç sınırlama (metin tabanlı)
                if is_code_change_task:
                    allowed_tools = {"read_file", "create_change_plan", "run_python_file", "search_code", "project_scan", "project_tree"}
                    if tool_call.name not in allowed_tools:
                        error_msg = f"Kod değişikliği görevi için izin verilmeyen araç: {tool_call.name}. Sadece dosya okuma, plan oluşturma ve test araçlarına izin var."
                        self.logger.warning(error_msg)
                        self.memory.add_tool_result(tool_call.name, {"error": error_msg}, False)
                        continue
                
                # Inspection-only görevde araç sınırlama (metin tabanlı)
                if is_inspection_only_task and target_file_path:
                    allowed_tools = {"search_code", "project_scan", "project_tree"}
                    if tool_call.name not in allowed_tools:
                        error_msg = f"Inspection-only görev için izin verilmeyen araç: {tool_call.name}. Hedef dosya zaten okundu. Sadece arama araçlarına izin var."
                        self.logger.warning(error_msg)
                        self.memory.add_tool_result(tool_call.name, {"error": error_msg}, False)
                        continue

                # Tekrarlanan başarısız çağrı kontrolü (metin tabanlı)
                try:
                    args_key = frozenset((k, str(v)) for k, v in sorted(tool_call.arguments.items()))
                except Exception:
                    args_key = frozenset((k, str(v)) for k, v in tool_call.arguments.items())
                call_key = (tool_call.name, args_key)
                
                if call_key in self._call_history:
                    count, prev_result = self._call_history[call_key]
                    if not prev_result.get("success", True) and count >= 3:
                        error_msg = f"Aynı araç çağrısı ({tool_call.name}) 3 kez başarısız oldu. Farklı bir strateji deneyin."
                        self.logger.warning(error_msg)
                        self.memory.add_tool_result(tool_call.name, {"error": error_msg}, False)
                        continue

                # Tool'u çalıştır
                self.logger.info(f"Tool çağrılıyor: {tool_call.name}")

                try:
                    result = self._execute_tool_call(tool_call, iteration)
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

                # Maksimum deneme aşıldı mı? Döngüyü durdur
                if result.get("orchestration", {}).get("max_attempts_reached"):
                    self.logger.warning("Maksimum correction deneme sayısı aşıldı. Döngü durduruluyor.")
                    # Sonucu memory'ye ekle
                    truncated_result = self._truncate_tool_output(result)
                    self.memory.add_tool_result(
                        tool_call.name,
                        truncated_result,
                        result.get("success", False)
                    )
                    # Döngüyü durdur
                    break

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
            success = False
            error = f"Maksimum iteration limiti ({self.config.max_iterations}) aşıldı."
        else:
            # Inspection-only görev için başarı kontrolü
            # Hedef dosya modelden önce okunduysa başarılı
            success = True
            error = None

        if is_inspection_only_task and target_file_path:
            # Hedef dosya okundu mu kontrol et (ön okuma)
            if target_file_content is None:
                success = False
                error = f"Hedef dosya ({target_file_path}) okunamadı. Görev tamamlanamadı."
                self.logger.error(error)
                final_response = f"{final_response}\n\nHATA: {error}"

        return LoopResult(
            success=success,
            final_response=final_response,
            iterations=iteration,
            tool_calls=self.tool_call_log,
            error=error
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
