import ast
from pathlib import Path

from app.core.config import (
    PROJECT_ROOT,
    IGNORED_DIRECTORIES,
)


class ProjectStructureAnalyzer:

    def __init__(self, project_root: Path = PROJECT_ROOT):
        self.project_root = Path(project_root)

    def analyze_file(self, file_path: Path) -> dict:
        relative_path = file_path.relative_to(
            self.project_root
        )

        result = {
            "file": str(relative_path),
            "classes": [],
            "functions": [],
            "imports": [],
            "syntax_error": None,
        }

        try:
            source = file_path.read_text(
                encoding="utf-8",
                errors="replace",
            )

            tree = ast.parse(
                source,
                filename=str(file_path),
            )

        except SyntaxError as exc:
            result["syntax_error"] = (
                f"{exc.msg} (satır {exc.lineno})"
            )
            return result

        except OSError as exc:
            result["syntax_error"] = str(exc)
            return result

        for node in ast.walk(tree):

            if isinstance(node, ast.ClassDef):
                result["classes"].append(
                    node.name
                )

            elif isinstance(node, ast.FunctionDef):
                result["functions"].append(
                    node.name
                )

            elif isinstance(node, ast.AsyncFunctionDef):
                result["functions"].append(
                    f"async {node.name}"
                )

            elif isinstance(node, ast.Import):
                for alias in node.names:
                    result["imports"].append(
                        alias.name
                    )

            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""

                result["imports"].append(
                    module
                )

        result["classes"] = sorted(
            set(result["classes"])
        )

        result["functions"] = sorted(
            set(result["functions"])
        )

        result["imports"] = sorted(
            set(result["imports"])
        )

        return result

    def analyze(self) -> list:
        if not self.project_root.exists():
            raise FileNotFoundError(
                f"Proje klasörü bulunamadı: "
                f"{self.project_root}"
            )

        results = []

        for path in sorted(
            self.project_root.rglob("*.py")
        ):

            if any(
                ignored in path.parts
                for ignored in IGNORED_DIRECTORIES
            ):
                continue

            results.append(
                self.analyze_file(path)
            )

        return results

    def format_results(
        self,
        results: list,
    ) -> str:

        lines = []

        for result in results:

            lines.append(
                f"DOSYA: {result['file']}"
            )

            if result["syntax_error"]:
                lines.append(
                    f"  SYNTAX HATASI: "
                    f"{result['syntax_error']}"
                )
                lines.append("")
                continue

            lines.append(
                "  SINIFLAR: "
                + (
                    ", ".join(result["classes"])
                    if result["classes"]
                    else "Yok"
                )
            )

            lines.append(
                "  FONKSIYONLAR: "
                + (
                    ", ".join(result["functions"])
                    if result["functions"]
                    else "Yok"
                )
            )

            lines.append(
                "  IMPORTLAR: "
                + (
                    ", ".join(result["imports"])
                    if result["imports"]
                    else "Yok"
                )
            )

            lines.append("")

        return "\n".join(lines)
