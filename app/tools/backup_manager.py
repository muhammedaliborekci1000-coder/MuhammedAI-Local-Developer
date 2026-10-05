from pathlib import Path
from datetime import datetime
import shutil

from app.core.config import PROJECT_ROOT


class BackupManager:

    def __init__(self, project_root: Path = PROJECT_ROOT):
        self.project_root = Path(project_root)
        self.backup_root = self.project_root / ".muhammedai_backups"

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
                "Proje klasörü dışındaki dosyalar yedeklenemez."
            )

        return full_path

    def create_backup(self, relative_path: str) -> str:
        """Belirtilen dosyanın zaman damgalı yedeğini oluşturur."""

        source = self._validate_path(relative_path)

        if not source.exists():
            raise FileNotFoundError(
                f"Dosya bulunamadı: {relative_path}"
            )

        if not source.is_file():
            raise ValueError(
                f"Bu bir dosya değil: {relative_path}"
            )

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        relative = Path(relative_path)

        backup_directory = (
            self.backup_root
            / timestamp
            / relative.parent
        )

        backup_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        backup_path = (
            backup_directory
            / relative.name
        )

        shutil.copy2(
            source,
            backup_path,
        )

        return str(backup_path)

    def list_backups(self):
        """Mevcut yedek klasörlerini listeler."""

        if not self.backup_root.exists():
            return []

        return sorted(
            [
                path
                for path in self.backup_root.iterdir()
                if path.is_dir()
            ],
            reverse=True,
        )