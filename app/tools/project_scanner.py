from pathlib import Path
from typing import List

from app.core.config import (
    PROJECT_ROOT,
    SUPPORTED_EXTENSIONS,
    IGNORED_DIRECTORIES,
)


class ProjectScanner:
    def __init__(self, project_root: Path = PROJECT_ROOT):
        self.project_root = Path(project_root)

    def scan(self) -> List[Path]:
        """Projeyi tarar ve desteklenen dosyaları döndürür."""

        if not self.project_root.exists():
            raise FileNotFoundError(
                f"Proje klasörü bulunamadı: {self.project_root}"
            )

        files = []

        for path in self.project_root.rglob("*"):
            if not path.is_file():
                continue

            if any(
                ignored in path.parts
                for ignored in IGNORED_DIRECTORIES
            ):
                continue

            if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
                continue

            files.append(path)

        return sorted(files)

    def get_tree(self) -> str:
        """Projenin okunabilir dosya ağacını oluşturur."""

        files = self.scan()

        lines = [
            f"PROJE: {self.project_root}",
            f"TOPLAM DOSYA: {len(files)}",
            "",
        ]

        for file in files:
            relative = file.relative_to(self.project_root)
            lines.append(f"- {relative}")

        return "\n".join(lines)