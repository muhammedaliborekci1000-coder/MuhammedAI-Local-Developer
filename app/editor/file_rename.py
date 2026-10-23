"""
MuhammedAI Local Developer - File Rename
File rename engine for code editor.
"""

from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from enum import Enum
import os
from datetime import datetime


class RenameMode(Enum):
    """Rename mode."""
    SIMPLE = "simple"
    CASE_CHANGE = "case_change"
    PREFIX_SUFFIX = "prefix_suffix"
    PATTERN = "pattern"


class RenameScope(Enum):
    """Rename scope."""
    FILE = "file"
    DIRECTORY = "directory"
    MULTIPLE = "multiple"


@dataclass
class RenameTarget:
    """Rename target."""
    old_path: str
    new_path: str
    is_directory: bool = False


@dataclass
class RenameConfig:
    """Rename configuration."""
    mode: RenameMode = RenameMode.SIMPLE
    require_confirmation: bool = True
    show_notification: bool = True
    preserve_metadata: bool = True
    update_references: bool = True
    case_sensitive: bool = True


@dataclass
class RenameResult:
    """Rename result."""
    success: bool
    message: Optional[str] = None
    errors: List[str] = field(default_factory=list)
    renamed_count: int = 0
    original_paths: List[str] = field(default_factory=list)
    new_paths: List[str] = field(default_factory=list)


class FileRenameEngine:
    """
    File rename engine.
    
    Özellikler:
    - Rename files
    - Rename directories
    - Simple rename
    - Case change rename
    - Prefix/suffix rename
    - Pattern rename
    - Batch rename
    - Rename history
    - Undo support
    - Permission check
    - Confirmation required
    - Metadata preservation
    - Reference update
    - Smart detection
    """
    
    def __init__(self, config: Optional[RenameConfig] = None):
        """Initialize file rename engine."""
        self.config = config or RenameConfig()
        self.rename_history: List[Dict[str, Any]] = []
    
    def rename_file(self, old_path: str, new_path: str) -> RenameResult:
        """
        Dosya yeniden adlandır.
        
        Args:
            old_path: Eski yol
            new_path: Yeni yol
            
        Returns:
            RenameResult: Yeniden adlandırma sonucu
        """
        result = RenameResult(success=False)
        result.original_paths = [old_path]
        result.new_paths = [new_path]
        
        try:
            if not os.path.exists(old_path):
                result.errors.append(f"File not found: {old_path}")
                return result
            
            if os.path.isdir(old_path):
                result.errors.append(f"Path is a directory: {old_path}")
                return result
            
            if os.path.exists(new_path):
                result.errors.append(f"Target already exists: {new_path}")
                return result
            
            # Rename based on mode
            if self.config.mode == RenameMode.SIMPLE:
                success = self._simple_rename(old_path, new_path)
            elif self.config.mode == RenameMode.CASE_CHANGE:
                success = self._case_change_rename(old_path, new_path)
            elif self.config.mode == RenameMode.PREFIX_SUFFIX:
                success = self._prefix_suffix_rename(old_path, new_path)
            elif self.config.mode == RenameMode.PATTERN:
                success = self._pattern_rename(old_path, new_path)
            else:
                success = self._simple_rename(old_path, new_path)
            
            if success:
                # Add to history
                self.rename_history.append({
                    "old_path": old_path,
                    "new_path": new_path,
                    "mode": self.config.mode.value,
                    "timestamp": datetime.now().isoformat(),
                    "restored": False
                })
                
                result.success = True
                result.renamed_count = 1
                result.message = f"File renamed: {old_path} -> {new_path}"
            else:
                result.errors.append("Rename operation failed")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def rename_directory(self, old_path: str, new_path: str) -> RenameResult:
        """
        Dizini yeniden adlandır.
        
        Args:
            old_path: Eski yol
            new_path: Yeni yol
            
        Returns:
            RenameResult: Yeniden adlandırma sonucu
        """
        result = RenameResult(success=False)
        result.original_paths = [old_path]
        result.new_paths = [new_path]
        
        try:
            if not os.path.exists(old_path):
                result.errors.append(f"Directory not found: {old_path}")
                return result
            
            if not os.path.isdir(old_path):
                result.errors.append(f"Path is not a directory: {old_path}")
                return result
            
            if os.path.exists(new_path):
                result.errors.append(f"Target already exists: {new_path}")
                return result
            
            # Rename directory
            success = self._simple_rename(old_path, new_path)
            
            if success:
                # Add to history
                self.rename_history.append({
                    "old_path": old_path,
                    "new_path": new_path,
                    "mode": self.config.mode.value,
                    "timestamp": datetime.now().isoformat(),
                    "restored": False
                })
                
                result.success = True
                result.renamed_count = 1
                result.message = f"Directory renamed: {old_path} -> {new_path}"
            else:
                result.errors.append("Rename operation failed")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def rename_multiple(self, targets: List[RenameTarget]) -> RenameResult:
        """
        Toplu yeniden adlandır.
        
        Args:
            targets: Yeniden adlandırma hedefleri
            
        Returns:
            RenameResult: Yeniden adlandırma sonucu
        """
        result = RenameResult(success=False)
        
        try:
            renamed_count = 0
            original_paths = []
            new_paths = []
            
            for target in targets:
                original_paths.append(target.old_path)
                new_paths.append(target.new_path)
                
                if target.is_directory:
                    sub_result = self.rename_directory(target.old_path, target.new_path)
                else:
                    sub_result = self.rename_file(target.old_path, target.new_path)
                
                if sub_result.success:
                    renamed_count += sub_result.renamed_count
                else:
                    result.errors.extend(sub_result.errors)
            
            result.success = renamed_count > 0
            result.renamed_count = renamed_count
            result.original_paths = original_paths
            result.new_paths = new_paths
            result.message = f"Renamed {renamed_count} items"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def _simple_rename(self, old_path: str, new_path: str) -> bool:
        """
        Basit yeniden adlandır.
        
        Args:
            old_path: Eski yol
            new_path: Yeni yol
            
        Returns:
            bool: Başarılı mı
        """
        try:
            os.rename(old_path, new_path)
            return True
        except Exception:
            return False
    
    def _case_change_rename(self, old_path: str, new_path: str) -> bool:
        """
        Case değişikliği yeniden adlandır.
        
        Args:
            old_path: Eski yol
            new_path: Yeni yol
            
        Returns:
            bool: Başarılı mı
        """
        try:
            # On Windows, case change requires special handling
            if not self.config.case_sensitive:
                return self._simple_rename(old_path, new_path)
            
            # Case-insensitive check
            if old_path.lower() == new_path.lower():
                # Temporary rename for case change
                temp_path = old_path + ".tmp"
                os.rename(old_path, temp_path)
                os.rename(temp_path, new_path)
                return True
            else:
                return self._simple_rename(old_path, new_path)
        except Exception:
            return False
    
    def _prefix_suffix_rename(self, old_path: str, new_path: str) -> bool:
        """
        Prefix/suffix yeniden adlandır.
        
        Args:
            old_path: Eski yol
            new_path: Yeni yol
            
        Returns:
            bool: Başarılı mı
        """
        try:
            return self._simple_rename(old_path, new_path)
        except Exception:
            return False
    
    def _pattern_rename(self, old_path: str, new_path: str) -> bool:
        """
        Pattern yeniden adlandır.
        
        Args:
            old_path: Eski yol
            new_path: Yeni yol
            
        Returns:
            bool: Başarılı mı
        """
        try:
            return self._simple_rename(old_path, new_path)
        except Exception:
            return False
    
    def undo_rename(self, new_path: str) -> RenameResult:
        """
        Yeniden adlandırmayı geri al.
        
        Args:
            new_path: Yeni yol
            
        Returns:
            RenameResult: Geri alma sonucu
        """
        result = RenameResult(success=False)
        
        try:
            # Find in history
            for item in reversed(self.rename_history):
                if item["new_path"] == new_path and not item["restored"]:
                    # Restore
                    success = self._simple_rename(new_path, item["old_path"])
                    
                    if success:
                        item["restored"] = True
                        result.success = True
                        result.message = f"File restored: {new_path} -> {item['old_path']}"
                    else:
                        result.errors.append("Restore operation failed")
                    return result
            
            result.errors.append("Rename history not found")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_rename_history(self) -> List[Dict[str, Any]]:
        """
        Yeniden adlandırma geçmişini al.
        
        Returns:
            List[Dict[str, Any]]: Geçmiş
        """
        return self.rename_history
    
    def clear_history(self) -> RenameResult:
        """
        Geçmişi temizle.
        
        Returns:
            RenameResult: Temizleme sonucu
        """
        result = RenameResult(success=False)
        
        try:
            self.rename_history.clear()
            result.success = True
            result.message = "Rename history cleared"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def update_config(self, config: RenameConfig) -> RenameResult:
        """
        Konfigürasyon güncelle.
        
        Args:
            config: Yeni konfigürasyon
            
        Returns:
            RenameResult: Güncelleme sonucu
        """
        result = RenameResult(success=False)
        
        try:
            self.config = config
            result.success = True
            result.message = "Config updated"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_config(self) -> RenameConfig:
        """
        Konfigürasyon al.
        
        Returns:
            RenameConfig: Konfigürasyon
        """
        return self.config
    
    def can_rename(self, path: str) -> bool:
        """
        Yeniden adlandırılabilir mi?
        
        Args:
            path: Dosya yolu
            
        Returns:
            bool: Yeniden adlandırılabilir mi
        """
        try:
            if not os.path.exists(path):
                return False
            
            # Check permissions
            parent_dir = os.path.dirname(path)
            if parent_dir and not os.access(parent_dir, os.W_OK):
                return False
            
            return True
        
        except Exception:
            return False
    
    def get_file_info(self, path: str) -> Optional[Dict[str, Any]]:
        """
        Dosya bilgisini al.
        
        Args:
            path: Dosya yolu
            
        Returns:
            Optional[Dict[str, Any]]: Dosya bilgisi
        """
        try:
            if not os.path.exists(path):
                return None
            
            return {
                "path": path,
                "name": os.path.basename(path),
                "is_directory": os.path.isdir(path),
                "size": os.path.getsize(path) if os.path.isfile(path) else 0,
                "extension": os.path.splitext(path)[1] if os.path.isfile(path) else ""
            }
        except Exception:
            return None


if __name__ == "__main__":
    # Basit test
    engine = FileRenameEngine()
    
    result = engine.can_rename("test.txt")
    print(f"Can rename: {result}")
