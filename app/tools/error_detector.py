import ast
from pathlib import Path

from app.core.config import (
    PROJECT_ROOT,
    SUPPORTED_EXTENSIONS,
    IGNORED_DIRECTORIES,
)


class ErrorDetector:

    def __init__(self, project_root: Path = PROJECT_ROOT):
        self.project_root = Path(project_root)

    def scan_python_files(self):
        errors = []

        if not self.project_root.exists():
            raise FileNotFoundError(
                f"Proje klasörü bulunamadı: {self.project_root}"
            )

        for path in self.project_root.rglob("*.py"):

            if any(
                ignored in path.parts
                for ignored in IGNORED_DIRECTORIES
            ):
                continue

            try:
                content = path.read_text(
                    encoding="utf-8-sig",  # BOM'u otomatik kaldırır
                    errors="replace",
                )
            except OSError:
                continue

            try:
                ast.parse(content, filename=str(path))

            except SyntaxError as exc:

                relative_path = path.relative_to(
                    self.project_root
                )

                errors.append(
                    {
                        "file": str(relative_path),
                        "line": exc.lineno,
                        "column": exc.offset,
                        "message": exc.msg,
                        "text": exc.text.strip()
                        if exc.text
                        else "",
                    }
                )

        return errors

    def format_errors(self, errors):

        if not errors:
            return "Python syntax hatası bulunamadı."

        lines = [
            f"Toplam syntax hatası: {len(errors)}",
            "",
        ]

        for error in errors:

            lines.append(
                f"{error['file']}:{error['line']} "
                f"→ {error['message']}"
            )

            if error["text"]:
                lines.append(
                    f"    Kod: {error['text']}"
                )

        return "\n".join(lines)