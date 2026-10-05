import subprocess
import sys
from pathlib import Path

from app.core.config import PROJECT_ROOT


class PythonRunner:

    def __init__(self, project_root: Path = PROJECT_ROOT):
        self.project_root = Path(project_root)

    def _validate_path(self, file_path: str) -> Path:
        requested = Path(file_path)

        if requested.is_absolute():
            raise ValueError(
                "Mutlak dosya yollarına izin verilmiyor."
            )

        full_path = (
            self.project_root / requested
        ).resolve()

        root = self.project_root.resolve()

        try:
            full_path.relative_to(root)
        except ValueError:
            raise ValueError(
                "Proje klasörü dışındaki dosyalar çalıştırılamaz."
            )

        return full_path

    def run_file(
        self,
        file_path: str,
        timeout: int = 30,
    ) -> dict:

        try:
            path = self._validate_path(file_path)

        except ValueError as exc:
            return {
                "success": False,
                "returncode": None,
                "stdout": "",
                "stderr": "",
                "error": str(exc),
            }

        if not path.exists():
            return {
                "success": False,
                "returncode": None,
                "stdout": "",
                "stderr": "",
                "error": f"Dosya bulunamadı: {file_path}",
            }

        if not path.is_file():
            return {
                "success": False,
                "returncode": None,
                "stdout": "",
                "stderr": "",
                "error": f"Bu bir dosya değil: {file_path}",
            }

        try:
            result = subprocess.run(
                [sys.executable, str(path)],
                cwd=str(self.project_root),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=timeout,
            )

            return {
                "success": result.returncode == 0,
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "error": None,
            }

        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "returncode": None,
                "stdout": "",
                "stderr": "",
                "error": (
                    f"Program {timeout} saniye içinde "
                    "tamamlanmadı."
                ),
            }

        except OSError as exc:
            return {
                "success": False,
                "returncode": None,
                "stdout": "",
                "stderr": "",
                "error": f"Program çalıştırılamadı: {exc}",
            }
