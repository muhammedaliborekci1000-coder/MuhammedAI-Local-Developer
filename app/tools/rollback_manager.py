from pathlib import Path
import shutil

from app.core.config import PROJECT_ROOT


class RollbackManager:

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
                "Proje klasörü dışındaki dosyalar geri yüklenemez."
            )

        return full_path

    def rollback(
        self,
        relative_path: str,
        backup_path: str,
    ) -> str:
        """Belirtilen dosyayı yedekten geri yükler."""

        target = self._validate_path(relative_path)
        backup = Path(backup_path).resolve()

        if not backup.exists():
            raise FileNotFoundError(
                f"Yedek bulunamadı: {backup_path}"
            )

        if not backup.is_file():
            raise ValueError(
                f"Yedek bir dosya değil: {backup_path}"
            )

        try:
            backup.relative_to(
                self.backup_root.resolve()
            )
        except ValueError:
            raise ValueError(
                "Sadece MuhammedAI backup klasöründeki "
                "yedekler kullanılabilir."
            )

        target.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        shutil.copy2(
            backup,
            target,
        )

        return (
            f"Dosya yedekten geri yüklendi: "
            f"{relative_path}"
        )