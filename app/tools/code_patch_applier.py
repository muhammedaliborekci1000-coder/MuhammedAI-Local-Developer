from pathlib import Path

from app.core.config import PROJECT_ROOT


class CodePatchApplier:

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

    def apply_patch(
        self,
        file_path: str,
        old_code: str,
        new_code: str,
    ) -> dict:
        """
        Dosyanın tamamını değiştirmek yerine
        sadece old_code bölümünü new_code ile değiştirir.
        """

        path = self._validate_path(file_path)

        if not path.exists():
            return {
                "success": False,
                "error": f"Dosya bulunamadı: {file_path}",
            }

        if not path.is_file():
            return {
                "success": False,
                "error": f"Bu bir dosya değil: {file_path}",
            }

        if not old_code.strip():
            return {
                "success": False,
                "error": "old_code boş olamaz.",
            }

        if old_code == new_code:
            return {
                "success": False,
                "error": (
                    "old_code ve new_code aynı. "
                    "Değişiklik yapılmadı."
                ),
            }

        try:
            content = path.read_text(
                encoding="utf-8",
                errors="replace",
            )
        except OSError as exc:
            return {
                "success": False,
                "error": f"Dosya okunamadı: {exc}",
            }

        occurrences = content.count(old_code)

        if occurrences == 0:
            return {
                "success": False,
                "error": (
                    "old_code dosyada bulunamadı. "
                    "Değişiklik yapılmadı."
                ),
            }

        if occurrences > 1:
            return {
                "success": False,
                "error": (
                    f"old_code dosyada {occurrences} kez bulundu. "
                    "Belirsiz değişiklik nedeniyle işlem durduruldu."
                ),
            }

        new_content = content.replace(
            old_code,
            new_code,
            1,
        )

        try:
            path.write_text(
                new_content,
                encoding="utf-8",
            )
        except OSError as exc:
            return {
                "success": False,
                "error": f"Dosya yazılamadı: {exc}",
            }

        return {
            "success": True,
            "file": file_path,
            "message": (
                "Kod parçası başarıyla değiştirildi."
            ),
        }
