"""
MuhammedAI Local Developer - Change Orchestrator
Modelden bağımsız deterministik dosya değişikliği orkestrasyonu.
"""

from typing import Dict, Any, Optional, Callable
from enum import Enum
import logging


class OrchestratorState(Enum):
    """Orkestratör durumları."""
    ANALYZE = "ANALYZE"
    PLAN_READY = "PLAN_READY"
    WAITING_FOR_USER_APPROVAL = "WAITING_FOR_USER_APPROVAL"
    APPLY = "APPLY"
    COMPLETE = "COMPLETE"
    REJECTED = "REJECTED"  # Kullanıcı reddi
    APPLY_FAILED = "APPLY_FAILED"  # Test başarısızlığı


class ChangeOrchestrator:
    """
    Dosya değişikliği iş akışını modelden bağımsız şekilde yönetir.
    
    Durum akışı:
    ANALYZE → PLAN_READY → WAITING_FOR_USER_APPROVAL → APPLY → VERIFY → COMPLETE
    
    Güvenlik:
    - Modelin approved parametresini yoksayar
    - Yalnızca approval_callback sonucuna güvenir
    - Callback yoksa veya hata verirse işlem reddedilir
    """

    def __init__(
        self,
        workflow,
        approval_callback: Optional[Callable[[str, Dict[str, Any]], bool]] = None
    ):
        """
        Args:
            workflow: ChangeWorkflow örneği
            approval_callback: Onay callback fonksiyonu (tool_name, arguments) -> bool
        """
        self.workflow = workflow
        self.approval_callback = approval_callback
        self._current_plan: Optional[Dict[str, Any]] = None
        self._state: OrchestratorState = OrchestratorState.ANALYZE
        self._approval_result: Optional[bool] = None
        
        self.logger = logging.getLogger(__name__)

    def get_state(self) -> str:
        """Mevcut durumu döndürür."""
        return self._state.value

    def get_current_plan(self) -> Optional[Dict[str, Any]]:
        """Mevcut planı döndürür."""
        return self._current_plan

    def reset(self) -> None:
        """Orkestratörü sıfırlar."""
        self._current_plan = None
        self._state = OrchestratorState.ANALYZE
        self._approval_result = None

    def reset_for_correction(self) -> None:
        """
        Correction loop için orchestrator'ı hazırla.

        Sadece APPLY_FAILED durumunda çalışır ve state'i ANALYZE yaparak
        yeni plan oluşturulmasına izin verir.
        """
        if self._state == OrchestratorState.APPLY_FAILED:
            self._current_plan = None
            self._state = OrchestratorState.ANALYZE
            self._approval_result = None
            self.logger.info("Correction için orchestrator sıfırlandı. Durum: ANALYZE")
        else:
            self.logger.warning(
                f"reset_for_correction yanlış durumda çağrıldı: {self._state.value}"
            )

    def create_plan(
        self,
        file_path: str,
        problem: str
    ) -> Dict[str, Any]:
        """
        Değişiklik planı oluşturur ve saklar.
        
        Args:
            file_path: Hedef dosya yolu
            problem: Problem tanımı
            
        Returns:
            create_change_plan sonucu
        """
        # Aynı plan zaten var mı?
        if self._current_plan and self._state == OrchestratorState.PLAN_READY:
            self.logger.info("Plan zaten mevcut, tekrar oluşturulmuyor.")
            return {
                "success": True,
                "cached": True,
                "plan": self._current_plan,
                "validation": {"valid": True, "errors": []}
            }
        
        # Yeni plan oluştur
        result = self.workflow.create_plan(file_path, problem)
        self.set_plan_result(result)
        return result

    def set_plan_result(self, result: Dict[str, Any]) -> bool:
        """Daha önce üretilmiş planı doğrulama sonucu ile birlikte saklar."""
        validation = result.get("validation", {})
        plan = result.get("plan")

        if not validation.get("valid") or not isinstance(plan, dict):
            self._current_plan = None
            self._state = OrchestratorState.ANALYZE
            self._approval_result = None
            self.logger.warning(
                f"Plan geçersiz. Hatalar: {validation.get('errors', [])}"
            )
            return False

        self._current_plan = plan
        self._state = OrchestratorState.PLAN_READY
        self._approval_result = None
        self.logger.info(
            f"Plan oluşturuldu ve saklandı. Durum: {self._state.value}"
        )
        return True

    def request_approval(self) -> bool:
        """
        Kullanıcı onayı ister.
        
        Yalnızca PLAN_READY durumunda çalışır.
        Modelin approved parametresini yoksayar, yalnızca callback'e güvenir.
        
        Returns:
            True ise onay verildi, False ise reddedildi
        """
        if self._state != OrchestratorState.PLAN_READY:
            self.logger.warning(f"request_approval yanlış durumda çağrıldı: {self._state.value}")
            return False
        
        if self.approval_callback is None:
            self.logger.warning("Onay callback yok. İşlem reddedildi.")
            self._state = OrchestratorState.REJECTED
            self._approval_result = False
            return False
        
        self._state = OrchestratorState.WAITING_FOR_USER_APPROVAL
        
        try:
            # Callback'i çağır
            result = self.approval_callback(
                "apply_change",
                {"plan": self._current_plan}
            )
            
            # Awaitable kontrolü - async callback senkron çağrıldıysa
            import inspect
            if inspect.isawaitable(result):
                # Coroutine ise kapat (RuntimeWarning önlemek için)
                if inspect.iscoroutine(result):
                    result.close()
                self.logger.error(
                    "Onay callback awaitable döndürdü (async callback senkron çağrıldı). "
                    "İşlem reddedildi."
                )
                self._state = OrchestratorState.REJECTED
                self._approval_result = False
                return False
            
            # Sonucun gerçek bool olduğunu kontrol et
            if not isinstance(result, bool):
                self.logger.error(
                    f"Onay callback bool döndürmedi: {type(result)}. İşlem reddedildi."
                )
                self._state = OrchestratorState.REJECTED
                self._approval_result = False
                return False
            
            self._approval_result = result
            
            if result:
                self._state = OrchestratorState.APPLY
                self.logger.info("Kullanıcı onayı verildi. Durum: APPLY")
            else:
                self._state = OrchestratorState.REJECTED
                self.logger.info("Kullanıcı onayı reddedildi. Durum: REJECTED")
            
            return result
            
        except Exception as exc:
            self.logger.error(f"Onay callback hatası: {exc}")
            self._state = OrchestratorState.REJECTED
            self._approval_result = False
            return False

    def apply_change(self, test_file: str) -> Dict[str, Any]:
        """
        Değişikliği uygular.
        
        Yalnızca APPLY durumunda çalışır.
        Mevcut planı kullanır ve approved=True ile çağırır.
        
        Args:
            test_file: Test dosyası yolu
            
        Returns:
            apply_change sonucu
        """
        self.logger.info(f"apply_change çağrıldı. State: {self._state.value}, test_file: {test_file}")

        if self._state != OrchestratorState.APPLY:
            error_msg = f"apply_change yanlış durumda çağrıldı: {self._state.value}"
            self.logger.warning(error_msg)
            return {
                "success": False,
                "error": error_msg,
                "state": self._state.value
            }
        
        if self._current_plan is None:
            error_msg = "Mevcut plan yok"
            self.logger.error(error_msg)
            return {
                "success": False,
                "error": error_msg
            }
        
        # test_file kontrolü
        if not test_file:
            error_msg = "test_file parametresi gerekli"
            self.logger.error(error_msg)
            self._state = OrchestratorState.REJECTED
            return {
                "success": False,
                "error": error_msg
            }
        
        self.logger.info(f"Değişiklik uygulanıyor. Plan: {self._current_plan.get('file')}")

        # Değişikliği uygula (approved=True - orkestratör onayını doğruladı)
        result = self.workflow.apply_change(
            plan=self._current_plan,
            test_file=test_file,
            approved=True  # Yalnızca orkestratör doğrulaması ile
        )

        self.logger.info(f"apply_change sonucu: success={result.get('success')}")

        if result.get("success"):
            self._state = OrchestratorState.COMPLETE
            self.logger.info("Değişiklik başarıyla uygulandı. Durum: COMPLETE")
        else:
            self._state = OrchestratorState.APPLY_FAILED
            self.logger.warning(f"Değişiklik başarısız: {result.get('error')}")
        
        return result

    def get_result(self) -> Dict[str, Any]:
        """
        Orkestratörün son durumunu döndürür.
        
        Returns:
            Durum bilgisi
        """
        return {
            "state": self._state.value,
            "has_plan": self._current_plan is not None,
            "approval_result": self._approval_result,
            "plan": self._current_plan
        }
