"""
Fake ChangeWorkflow for testing without real Ollama
"""
from app.tools.plan_validator import PlanValidator


class FakeChangePlanner:
    """Fake planner that returns deterministic plans without Ollama"""

    def create_plan(self, file_path: str, problem: str) -> dict:
        """Return a deterministic fake plan"""
        return {
            "file": file_path,
            "function": "greet",
            "problem": problem,
            "change": "Merhaba mesajını Merhaba Muhammed olarak değiştirmek",
            "old_code": 'return "Merhaba"',
            "new_code": 'return "Merhaba Muhammed"',
            "reason": "Fake test plan"
        }


class FakeChangeWorkflow:
    """Fake ChangeWorkflow that doesn't call Ollama"""

    def __init__(self):
        self.planner = FakeChangePlanner()
        self.validator = PlanValidator()
        # SafeChangeManager'ı import etmiyoruz çünkü subprocess çağrısı yapıyor
        # Testlerde apply_change çağrılmayacak veya mocklanacak

    def create_plan(self, file_path: str, problem: str) -> dict:
        """Create a fake plan"""
        plan = self.planner.create_plan(file_path, problem)
        validation = self.validator.validate(plan)

        return {
            "plan": plan,
            "validation": validation,
        }

    def analyze_problem(self, file_path: str, problem: str) -> dict:
        """Alias for create_plan"""
        return self.create_plan(file_path, problem)

    def apply_change(self, plan: dict, test_file: str, approved: bool = False) -> dict:
        """Fake apply_change - just returns success if approved"""
        if not approved:
            return {
                "success": False,
                "status": "NOT_APPROVED",
                "message": "Değişiklik uygulanmadı. Kullanıcı onayı gerekli.",
            }

        validation = self.validator.validate(plan)

        if not validation.get("valid"):
            return {
                "success": False,
                "status": "INVALID_PLAN",
                "validation": validation,
                "message": "Değişiklik uygulanmadı. Plan doğrulaması başarısız.",
            }

        # Fake success response
        return {
            "success": True,
            "backup": "/fake/backup/path",
            "patch": {"success": True},
            "syntax": "OK",
            "test": {"success": True},
        }
