from pathlib import Path
from typing import Optional, Dict, Any

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

    def read(self, relative_path: str, offset: int = 0, limit: Optional[int] = None) -> Any:
        """
        Proje içindeki bir metin dosyasını okur.

        Args:
            relative_path: Dosya yolu
            offset: Başlangıç satırı (0-indexed, varsayılan 0)
            limit: Okunacak maksimum satır sayısı (None = tüm dosya)

        Returns:
            Any: 
            - offset=0 ve limit=None (varsayılan): str (dosya içeriği)
            - offset>0 veya limit belirtilmişse: Dict[str, Any] with metadata
                - content: Dosya içeriği
                - total_lines: Toplam satır sayısı
                - read_lines: Okunan satır sayısı
                - offset: Başlangıç satırı
                - truncated: Kesilmiş mi (True/False)
        """

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
            content = path.read_text(
                encoding="utf-8-sig",  # BOM'u otomatik kaldırır
                errors="replace",
            )

            # Satır bazlı okuma
            lines = content.splitlines()
            total_lines = len(lines)

            # Offset ve limit uygula
            if offset > 0 or limit is not None:
                end = offset + limit if limit is not None else None
                lines = lines[offset:end]
                content = "\n".join(lines)

                # truncated: Dosyanın sonuna ulaşılmadı mı?
                # offset + read_lines < total_lines ise truncated = True
                truncated = (offset + len(lines)) < total_lines

                return {
                    "content": content,
                    "total_lines": total_lines,
                    "read_lines": len(lines),
                    "offset": offset,
                    "truncated": truncated
                }
            else:
                # Her zaman dict formatında döndür
                return {
                    "content": "\n".join(lines),
                    "total_lines": total_lines,
                    "read_lines": total_lines,
                    "offset": 0,
                    "truncated": False
                }
        except OSError as exc:
            raise OSError(
                f"Dosya okunamadı: {relative_path}"
            ) from exc