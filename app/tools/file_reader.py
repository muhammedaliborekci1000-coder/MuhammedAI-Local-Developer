from pathlib import Path

from app.core.config import (
    PROJECT_ROOT,
    IGNORED_DIRECTORIES,
)


class FileReader:
    def __init__(self, project_root: Path = PROJECT_ROOT):
        self.project_root = Path(project_root)

    def _validate_path(self, relative_path: str) -> Path:
        """Dosya yolunun proje dışına çıkmasını engeller."""

        requested = Path(relative_path)

        if requested.is_absolute():
            raise ValueError("Mutlak dosya yollarına izin verilmiyor.")

        if any(part in IGNORED_DIRECTORIES for part in requested.parts):
            raise ValueError("Bu klasöre erişim engellendi.")

        full_path = (self.project_root / requested).resolve()
        root = self.project_root.resolve()

        try:
            full_path.relative_to(root)
        except ValueError:
            raise ValueError(
                "Proje klasörü dışındaki dosyalara erişilemez."
            )

        return full_path

    def read(self, relative_path: str) -> str:
        """Proje içindeki bir metin dosyasını okur."""

        path = self._validate_path(relative_path)

        if not path.exists():
            raise FileNotFoundError(
                f"Dosya bulunamadı: {relative_path}"
            )

        if not path.is_file():
            raise ValueError(
                f"Bu bir dosya değil: {relative_path}"
            )

        try:
            return path.read_text(
                encoding="utf-8-sig",  # BOM'u otomatik kaldırır
                errors="replace",
            )
        except OSError as exc:
            raise OSError(
                f"Dosya okunamadı: {relative_path}"
            ) from exc