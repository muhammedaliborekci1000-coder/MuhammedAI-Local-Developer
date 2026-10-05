from pathlib import Path

from app.core.config import PROJECT_ROOT


class ChangeApplier:

    def __init__(self, project_root: Path = PROJECT_ROOT):
        self.project_root = Path(project_root)

    def _validate_path(self, relative_path: str) -> Path:
        """Dosyanın proje içinde olduğunu kontrol eder."""

        requested = Path(relative_path)

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
                "Proje klasörü dışındaki dosyalar değiştirilemez."
            )

        return full_path

    def replace_file(
        self,
        relative_path: str,
        new_content: str,
    ) -> str:
        """Dosyanın tamamını verilen içerikle değiştirir."""

        path = self._validate_path(relative_path)

        if not path.exists():
            raise FileNotFoundError(
                f"Dosya bulunamadı: {relative_path}"
            )

        if not path.is_file():
            raise ValueError(
                f"Bu bir dosya değil: {relative_path}"
            )

        path.write_text(
            new_content,
            encoding="utf-8",
        )

        return (
            f"Dosya başarıyla güncellendi: "
            f"{relative_path}"
        )