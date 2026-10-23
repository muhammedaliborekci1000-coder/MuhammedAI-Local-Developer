"""
MuhammedAI Local Developer - File Save
File save engine for code editor.
"""

from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from enum import Enum
import os
from datetime import datetime


class SaveMode(Enum):
    """Save mode."""
    SAVE = "save"
    SAVE_AS = "save_as"
    AUTO_SAVE = "auto_save"
    BACKUP = "backup"


class Encoding(Enum):
    """Encoding."""
    UTF8 = "utf-8"
    UTF8_WITH_BOM = "utf-8-sig"
    UTF16 = "utf-16"
    UTF32 = "utf-32"
    ASCII = "ascii"
    LATIN1 = "latin-1"
    CP1252 = "cp1252"


class LineEnding(Enum):
    """Line ending."""
    LF = "\n"
    CRLF = "\r\n"
    CR = "\r"


@dataclass
class SaveConfig:
    """Save configuration."""
    mode: SaveMode = SaveMode.SAVE
    encoding: Encoding = Encoding.UTF8
    line_ending: LineEnding = LineEnding.LF
    add_newline_at_end: bool = True
    trim_trailing_whitespace: bool = False
    create_backup: bool = False
    auto_save_interval: int = 300  # seconds
    show_notification: bool = True


@dataclass
class SaveResult:
    """Save result."""
    success: bool
    message: Optional[str] = None
    errors: List[str] = field(default_factory=list)
    saved_path: Optional[str] = None
    saved_size: int = 0
    backup_path: Optional[str] = None


class FileSaveEngine:
    """
    File save engine.
    
    Özellikler:
    - Save files
    - Save as
    - Auto save
    - Backup creation
    - Encoding support
    - Line ending support
    - Trim trailing whitespace
    - Add newline at end
    - Save history
    - Undo support
    - Permission check
    - Smart detection
    """
    
    def __init__(self, config: Optional[SaveConfig] = None):
        """Initialize file save engine."""
        self.config = config or SaveConfig()
        self.save_history: List[Dict[str, Any]] = []
        self.auto_save_enabled: bool = False
    
    def save_file(self, path: str, content: str) -> SaveResult:
        """
        Dosya kaydet.
        
        Args:
            path: Dosya yolu
            content: İçerik
            
        Returns:
            SaveResult: Kaydetme sonucu
        """
        result = SaveResult(success=False)
        
        try:
            # Create backup if enabled
            backup_path = None
            if self.config.create_backup and os.path.exists(path):
                backup_path = self._create_backup(path)
            
            # Trim trailing whitespace if enabled
            if self.config.trim_trailing_whitespace:
                content = self._trim_trailing_whitespace(content)
            
            # Add newline at end if enabled
            if self.config.add_newline_at_end and content and not content.endswith(self.config.line_ending.value):
                content += self.config.line_ending.value
            
            # Create parent directories if needed
            parent_dir = os.path.dirname(path)
            if parent_dir and not os.path.exists(parent_dir):
                os.makedirs(parent_dir, exist_ok=True)
            
            # Write file
            with open(path, 'w', encoding=self.config.encoding.value, newline='') as f:
                f.write(content)
            
            # Get file size
            size = os.path.getsize(path)
            
            # Add to history
            self.save_history.append({
                "path": path,
                "mode": self.config.mode.value,
                "encoding": self.config.encoding.value,
                "timestamp": datetime.now().isoformat(),
                "restored": False
            })
            
            result.success = True
            result.saved_path = path
            result.saved_size = size
            result.backup_path = backup_path
            result.message = f"File saved: {path}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def save_as(self, original_path: str, new_path: str, content: str) -> SaveResult:
        """
    -Farklı kaydet.
        
        Args:
            original_path: Orijinal yol
            new_path: Yeni yol
            content: İçerik
            
        Returns:
            SaveResult: Kaydetme sonucu
        """
        result = SaveResult(success=False)
        
        try:
            # Save to new path
            result = self.save_file(new_path, content)
            
            if result.success:
                result.message = f"File saved as: {new_path}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def auto_save(self, path: str, content: str) -> SaveResult:
        """
        Otomatik kaydet.
        
        Args:
            path: Dosya yolu
            content: İçerik
            
        Returns:
            SaveResult: Kaydetme sonucu
        """
        if not self.auto_save_enabled:
            result = SaveResult(success=False)
            result.errors.append("Auto-save is disabled")
            return result
        
        # Use backup mode for auto-save
        original_mode = self.config.mode
        self.config.mode = SaveMode.AUTO_SAVE
        
        result = self.save_file(path, content)
        
        self.config.mode = original_mode
        
        if result.success:
            result.message = f"Auto-saved: {path}"
        
        return result
    
    def _create_backup(self, path: str) -> str:
        """
        Yedek oluştur.
        
        Args:
            path: Dosya yolu
            
        Returns:
            str: Yedek yolu
        """
        directory = os.path.dirname(path)
        filename = os.path.basename(path)
        name, ext = os.path.splitext(filename)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{name}_backup_{timestamp}{ext}"
        backup_path = os.path.join(directory, backup_name)
        
        shutil.copy2(path, backup_path)
        
        return backup_path
    
    def _trim_trailing_whitespace(self, content: str) -> str:
        """
        Sondaki boşlukları temizle.
        
        Args:
            content: İçerik
            
        Returns:
            str: Temizlenmiş içerik
        """
        lines = content.splitlines()
        trimmed_lines = [line.rstrip() for line in lines]
        return self.config.line_ending.value.join(trimmed_lines)
    
    def undo_save(self, path: str) -> SaveResult:
        """
        Kaydetmeyi geri al.
        
        Args:
            path: Dosya yolu
            
        Returns:
            SaveResult: Geri alma sonucu
        """
        result = SaveResult(success=False)
        
        try:
            # Find in history
            for item in reversed(self.save_history):
                if item["path"] == path and not item["restored"]:
                    # Restore from backup if exists
                    backup_path = self._find_latest_backup(path)
                    if backup_path and os.path.exists(backup_path):
                        shutil.copy2(backup_path, path)
                        item["restored"] = True
                        result.success = True
                        result.message = f"File restored from backup: {path}"
                        return result
                    else:
                        result.errors.append("No backup found")
                        return result
            
            result.errors.append("Save history not found")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def _find_latest_backup(self, path: str) -> Optional[str]:
        """
        En son yedeği bul.
        
        Args:
            path: Dosya yolu
            
        Returns:
            Optional[str]: Yedek yolu
        """
        directory = os.path.dirname(path)
        filename = os.path.basename(path)
        name, ext = os.path.splitext(filename)
        
        if not os.path.exists(directory):
            return None
        
        # Find all backup files
        backup_files = []
        for file in os.listdir(directory):
            if file.startswith(f"{name}_backup_") and file.endswith(ext):
                backup_files.append(file)
        
        if not backup_files:
            return None
        
        # Sort by timestamp (descending)
        backup_files.sort(reverse=True)
        
        return os.path.join(directory, backup_files[0])
    
    def get_save_history(self) -> List[Dict[str, Any]]:
        """
        Kaydetme geçmişini al.
        
        Returns:
            List[Dict[str, Any]]: Geçmiş
        """
        return self.save_history
    
    def clear_history(self) -> SaveResult:
        """
        Geçmişi temizle.
        
        Returns:
            SaveResult: Temizleme sonucu
        """
        result = SaveResult(success=False)
        
        try:
            self.save_history.clear()
            result.success = True
            result.message = "Save history cleared"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def enable_auto_save(self, interval: Optional[int] = None) -> SaveResult:
        """
        Otomatik kaydetmeyi etkinleştir.
        
        Args:
            interval: Aralık (saniye)
            
        Returns:
            SaveResult: Etkinleştirme sonucu
        """
        result = SaveResult(success=False)
        
        try:
            self.auto_save_enabled = True
            if interval is not None:
                self.config.auto_save_interval = interval
            result.success = True
            result.message = f"Auto-save enabled (interval: {self.config.auto_save_interval}s)"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def disable_auto_save(self) -> SaveResult:
        """
        Otomatik kaydetmeyi devre dışı bırak.
        
        Returns:
            SaveResult: Devre dışı bırakma sonucu
        """
        result = SaveResult(success=False)
        
        try:
            self.auto_save_enabled = False
            result.success = True
            result.message = "Auto-save disabled"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def update_config(self, config: SaveConfig) -> SaveResult:
        """
        Konfigürasyon güncelle.
        
        Args:
            config: Yeni konfigürasyon
            
        Returns:
            SaveResult: Güncelleme sonucu
        """
        result = SaveResult(success=False)
        
        try:
            self.config = config
            result.success = True
            result.message = "Config updated"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_config(self) -> SaveConfig:
        """
        Konfigürasyon al.
        
        Returns:
            SaveConfig: Konfigürasyon
        """
        return self.config
    
    def can_save(self, path: str) -> bool:
        """
        Kaydedilebilir mi?
        
        Args:
            path: Dosya yolu
            
        Returns:
            bool: Kaydedilebilir mi
        """
        try:
            # Check parent directory permissions
            parent_dir = os.path.dirname(path)
            if parent_dir:
                if not os.path.exists(parent_dir):
                    return True  # Will create parent directories
                if not os.access(parent_dir, os.W_OK):
                    return False
            
            return True
        
        except Exception:
            return False
    
    def get_file_content(self, path: str) -> Optional[str]:
        """
        Dosya içeriğini al.
        
        Args:
            path: Dosya yolu
            
        Returns:
            Optional[str]: İçerik
        """
        try:
            if not os.path.exists(path):
                return None
            
            with open(path, 'r', encoding=self.config.encoding.value) as f:
                return f.read()
        except Exception:
            return None


if __name__ == "__main__":
    import shutil
    
    # Basit test
    engine = FileSaveEngine()
    
    result = engine.can_save("test.txt")
    print(f"Can save: {result}")
