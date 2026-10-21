from pathlib import Path
import py_compile

from app.tools.backup_manager import BackupManager
from app.tools.code_patch_applier import CodePatchApplier
from app.tools.rollback_manager import RollbackManager
from app.tools.python_runner import PythonRunner


class SafeChangeManager:

    def __init__(self):
        self.backup = BackupManager()
        self.patcher = CodePatchApplier()
        self.rollback = RollbackManager()
        self.runner = PythonRunner()

    def _validate_test_file(
        self,
        test_file: str,
    ) -> Path:
        requested = Path(test_file)

        if requested.is_absolute():
            raise ValueError(
                "Test dosyası mutlak yol olamaz."
            )

        if requested.suffix.lower() != ".py":
            raise ValueError(
                "Test dosyası Python (.py) olmalıdır."
            )

        full_path = (
            Path(self.runner.project_root)
            / requested
        ).resolve()

        root = (
            Path(self.runner.project_root)
            .resolve()
        )

        try:
            full_path.relative_to(root)
        except ValueError:
            raise ValueError(
                "Test dosyası proje klasörü dışında olamaz."
            )

        if not full_path.exists():
            raise FileNotFoundError(
                f"Test dosyası bulunamadı: {test_file}"
            )

        if not full_path.is_file():
            raise ValueError(
                f"Test yolu bir dosya değil: {test_file}"
            )

        return full_path

    def _rollback(
        self,
        file_path: str,
        backup_path: str,
        result: dict,
    ):
        try:
            result["rollback"] = self.rollback.rollback(
                file_path,
                backup_path,
            )
        except Exception as exc:
            result["rollback"] = (
                f"Rollback başarısız: {exc}"
            )

    def apply_patch_and_test(
        self,
        file_path: str,
        old_code: str,
        new_code: str,
        test_file: str,
    ) -> dict:
        import logging
        logger = logging.getLogger(__name__)

        logger.info(f"apply_patch_and_test çağrıldı: file_path={file_path}, test_file={test_file}")
        logger.info(f"old_code (repr): {repr(old_code)}")
        logger.info(f"new_code (repr): {repr(new_code)}")

        result = {
            "success": False,
            "backup": None,
            "patch": None,
            "syntax": None,
            "test": None,
            "rollback": None,
            "error": None,
        }

        # 0. Test dosyasını doğrula
        try:
            self._validate_test_file(test_file)

        except Exception as exc:
            result["error"] = (
                f"Test dosyası doğrulaması başarısız: {exc}"
            )
            return result

        # 1. Backup
        try:
            backup_path = self.backup.create_backup(
                file_path
            )

            result["backup"] = backup_path

        except Exception as exc:
            result["error"] = (
                f"Backup başarısız: {exc}"
            )
            return result

        # 2. Patch
        try:
            patch_result = self.patcher.apply_patch(
                file_path,
                old_code,
                new_code,
            )

            result["patch"] = patch_result

            if not patch_result.get("success"):
                result["error"] = patch_result.get(
                    "error",
                    "Patch uygulanamadı.",
                )
                return result

        except Exception as exc:
            result["error"] = (
                f"Patch başarısız: {exc}"
            )
            return result

        # 3. Syntax
        try:
            target = (
                Path(self.patcher.project_root)
                / file_path
            )

            py_compile.compile(
                str(target),
                doraise=True,
            )

            result["syntax"] = "OK"

        except Exception as exc:
            result["error"] = (
                f"Syntax kontrolü başarısız: {exc}"
            )

            self._rollback(
                file_path,
                result["backup"],
                result,
            )

            return result

        # 4. Test
        try:
            test_result = self.runner.run_file(
                test_file
            )

            result["test"] = test_result

            if not test_result.get("success"):
                # Test başarısız olduğunda detaylı bilgi agent context'ine ekle
                result["error"] = (
                    "Test başarısız oldu."
                )
                result["test_failure_details"] = {
                    "stdout": test_result.get("stdout", ""),
                    "stderr": test_result.get("stderr", ""),
                    "returncode": test_result.get("returncode"),
                    "error": test_result.get("error"),
                }

                self._rollback(
                    file_path,
                    result["backup"],
                    result,
                )

                return result

        except Exception as exc:

            result["error"] = (
                f"Test çalıştırılamadı: {exc}"
            )

            self._rollback(
                file_path,
                result["backup"],
                result,
            )

            return result

        # 5. Success
        result["success"] = True

        return result

    def apply_and_test(
        self,
        file_path: str,
        old_code: str,
        new_code: str,
        test_file: str,
    ) -> dict:
        """
        Eski API ile uyumluluk sağlar.

        Eski kod:
            apply_and_test(...)

        Yeni güvenli API:
            apply_patch_and_test(...)
        """

        return self.apply_patch_and_test(
            file_path=file_path,
            old_code=old_code,
            new_code=new_code,
            test_file=test_file,
        )
