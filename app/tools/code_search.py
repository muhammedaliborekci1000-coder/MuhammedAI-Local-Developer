from pathlib import Path
from typing import List, Dict, Any

from app.core.config import (
    PROJECT_ROOT,
    SUPPORTED_EXTENSIONS,
    IGNORED_DIRECTORIES,
)


class CodeSearch:
    def __init__(self, project_root: Path = PROJECT_ROOT):
        self.project_root = Path(project_root)

    def search(
        self,
        query: str,
        max_results: int = 30,
    ) -> List[Dict[str, Any]]:
        """
        Proje içerisindeki desteklenen dosyalarda metin arar.

        Args:
            query: Aranacak metin.
            max_results: Döndürülecek maksimum sonuç sayısı.

        Returns:
            Bulunan sonuçların listesi.
        """

        if not query or not query.strip():
            raise ValueError("Arama metni boş olamaz.")

        query = query.strip()
        results = []

        if not self.project_root.exists():
            raise FileNotFoundError(
                f"Proje klasörü bulunamadı: {self.project_root}"
            )

        for path in self.project_root.rglob("*"):

            if len(results) >= max_results:
                break

            if not path.is_file():
                continue

            if any(
                ignored in path.parts
                for ignored in IGNORED_DIRECTORIES
            ):
                continue

            if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
                continue

            try:
                content = path.read_text(
                    encoding="utf-8",
                    errors="replace",
                )
            except (OSError, UnicodeError):
                continue

            for line_number, line in enumerate(
                content.splitlines(),
                start=1,
            ):
                if query.lower() in line.lower():

                    relative_path = path.relative_to(
                        self.project_root
                    )

                    results.append(
                        {
                            "file": str(relative_path),
                            "line": line_number,
                            "content": line.strip(),
                        }
                    )

                    if len(results) >= max_results:
                        break

        return results

    def format_results(
        self,
        results: List[Dict[str, Any]],
    ) -> str:
        """Arama sonuçlarını AI için okunabilir hale getirir."""

        if not results:
            return "Arama sonucu bulunamadı."

        lines = [
            f"Toplam sonuç: {len(results)}",
            "",
        ]

        for result in results:
            lines.append(
                f"{result['file']}:{result['line']} "
                f"→ {result['content']}"
            )

        return "\n".join(lines)