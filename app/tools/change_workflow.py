from app.tools.change_planner import ChangePlanner
from app.tools.plan_validator import PlanValidator
from app.tools.safe_change_manager import SafeChangeManager


class ChangeWorkflow:

    def __init__(self):
        self.planner = ChangePlanner()
        self.validator = PlanValidator()
        self.manager = SafeChangeManager()

    def create_plan(
        self,
        file_path: str,
        problem: str,
    ) -> dict:

        plan = self.planner.create_plan(
            file_path,
            problem,
        )

        validation = self.validator.validate(plan)

        return {
            "plan": plan,
            "validation": validation,
        }

    def analyze_problem(
        self,
        file_path: str,
        problem: str,
    ) -> dict:

        return self.create_plan(
            file_path,
            problem,
        )

    def apply_change(
        self,
        plan: dict,
        test_file: str,
        approved: bool = False,
    ) -> dict:

        if not approved:
            return {
                "success": False,
                "status": "NOT_APPROVED",
                "message": (
                    "Değişiklik uygulanmadı. "
                    "Kullanıcı onayı gerekli."
                ),
            }

        validation = self.validator.validate(plan)

        if not validation.get("valid"):
            return {
                "success": False,
                "status": "INVALID_PLAN",
                "validation": validation,
                "message": (
                    "Değişiklik uygulanmadı. "
                    "Plan doğrulaması başarısız."
                ),
            }

        return self.manager.apply_patch_and_test(
            file_path=plan["file"],
            old_code=plan["old_code"],
            new_code=plan["new_code"],
            test_file=test_file,
        )
