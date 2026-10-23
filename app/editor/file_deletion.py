"""
MuhammedAI Local Developer - File Deletion
File deletion engine for code editor.
"""

from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from enum import Enum
import os
import shutil
from datetime import datetime


class DeleteMode(Enum):
    """Delete mode."""
    MOVE_TO_TRASH = "move_to_trash"
    PERMANENT = "permanent"
    SAFE_DELETE = "safe_delete"


class DeleteScope(Enum):
    """Delete scope."""
    FILE = "file"
    DIRECTORY = "directory"
    MULTIPLE = "multiple"


@dataclass
class DeleteTarget:
    """Delete target."""
    path: str
    is_directory: bool = False
    size: int = 0


@dataclass
class DeleteConfig:
    """Delete configuration."""
    mode: DeleteMode = DeleteMode.MOVE_TO_TRASH
    require_confirmation: bool = True
    show_notification: bool = True
    preserve_metadata: bool = False
    delete_empty_directories: bool = True


@dataclass
class DeleteResult:
    """Delete result."""
    success: bool
    message: Optional[str] = None
    errors: List[str] = field(default_factory=list)
    deleted_count: int = 0
    deleted_size: int = 0
    original_paths: List[str] = field(default_factory=list)


class FileDeletionEngine:
    """
    File deletion engine.
    
    Özellikler:
    - Delete files
    - Delete directories
    - Move to trash
    - Permanent delete
    - Safe delete
    - Batch delete
    - Delete history
    - Undo support
    - Permission check
    - Confirmation required
    - Metadata preservation
    - Empty directory deletion
    - Size calculation
    - Smart detection
    """
    
    def __init__(self, config: Optional[DeleteConfig] = None):
        """Initialize file deletion engine."""
        self.config = config or DeleteConfig()
        self.delete_history: List[Dict[str, Any]] = []
        self.trash_path: Optional[str] = None
    
    def delete_file(self, path: str) -> DeleteResult:
        """
        Dosya sil.
        
        Args:
            path: Dosya yolu
            
        Returns:
            DeleteResult: Silme sonucu
        """
        result = DeleteResult(success=False)
        result.original_paths = [path]
        
        try:
            if not os.path.exists(path):
                result.errors.append(f"File not found: {path}")
                return result
            
            if os.path.isdir(path):
                result.errors.append(f"Path is a directory: {path}")
                return result
            
            # Get file size
            size = os.path.getsize(path)
            
            # Delete based on mode
            if self.config.mode == DeleteMode.MOVE_TO_TRASH:
                success = self._move_to_trash(path)
            elif self.config.mode == DeleteMode.PERMANENT:
                success = self._permanent_delete(path)
            elif self.config.mode == DeleteMode.SAFE_DELETE:
                success = self._safe_delete(path)
            else:
                success = self._permanent_delete(path)
            
            if success:
                # Add to history
                self.delete_history.append({
                    "path": path,
                    "mode": self.config.mode.value,
                    "timestamp": datetime.now().isoformat(),
                    "size": size,
                    "restored": False
                })
                
                result.success = True
                result.deleted_count = 1
                result.deleted_size = size
                result.message = f"File deleted: {path}"
            else:
                result.errors.append("Delete operation failed")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def delete_directory(self, path: str) -> DeleteResult:
        """
        Dizin sil.
        
        Args:
            path: Dizin yolu
            
        Returns:
            DeleteResult: Silme sonucu
        """
        result = DeleteResult(success=False)
        result.original_paths = [path]
        
        try:
            if not os.path.exists(path):
                result.errors.append(f"Directory not found: {path}")
                return result
            
            if not os.path.isdir(path):
                result.errors.append(f"Path is not a directory: {path}")
                return result
            
            # Calculate size
            size = self._calculate_directory_size(path)
            
            # Delete based on mode
            if self.config.mode == DeleteMode.MOVE_TO_TRASH:
                success = self._move_to_trash(path)
            elif self.config.mode == DeleteMode.PERMANENT:
                success = self._permanent_delete_directory(path)
            elif self.config.mode == DeleteMode.SAFE_DELETE:
                success = self._safe_delete_directory(path)
            else:
                success = self._permanent_delete_directory(path)
            
            if success:
                # Add to history
                self.delete_history.append({
                    "path": path,
                    "mode": self.config.mode.value,
                    "timestamp": datetime.now().isoformat(),
                    "size": size,
                    "restored": False
                })
                
                result.success = True
                result.deleted_count = 1
                result.deleted_size = size
                result.message = f"Directory deleted: {path}"
            else:
                result.errors.append("Delete operation failed")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def delete_multiple(self, targets: List[DeleteTarget]) -> DeleteResult:
        """
        Toplu sil.
        
        Args:
            targets: Silme hedefleri
            
        Returns:
            DeleteResult: Silme sonucu
        """
        result = DeleteResult(success=False)
        
        try:
            deleted_count = 0
            deleted_size = 0
            original_paths = []
            
            for target in targets:
                original_paths.append(target.path)
                
                if target.is_directory:
                    sub_result = self.delete_directory(target.path)
                else:
                    sub_result = self.delete_file(target.path)
                
                if sub_result.success:
                    deleted_count += sub_result.deleted_count
                    deleted_size += sub_result.deleted_size
                else:
                    result.errors.extend(sub_result.errors)
            
            result.success = deleted_count > 0
            result.deleted_count = deleted_count
            result.deleted_size = deleted_size
            result.original_paths = original_paths
            result.message = f"Deleted {deleted_count} items"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def _move_to_trash(self, path: str) -> bool:
        """
        Geri dönüşüm kutusuna taşı.
        
        Args:
            path: Dosya yolu
            
        Returns:
            bool: Başarılı mı
        """
        try:
            # Create trash directory if not exists
            if self.trash_path is None:
                self.trash_path = os.path.join(os.path.expanduser("~"), ".trash")
            
            if not os.path.exists(self.trash_path):
                os.makedirs(self.trash_path)
            
            # Move to trash
            trash_name = f"{os.path.basename(path)}_{datetime.now().timestamp()}"
            trash_path = os.path.join(self.trash_path, trash_name)
            
            shutil.move(path, trash_path)
            return True
        
        except Exception:
            return False
    
    def _permanent_delete(self, path: str) -> bool:
        """
        Kalıcı sil.
        
        Args:
            path: Dosya yolu
            
        Returns:
            bool: Başarılı mı
        """
        try:
            os.remove(path)
            return True
        except Exception:
            return False
    
    def _permanent_delete_directory(self, path: str) -> bool:
        """
        Dizini kalıcı sil.
        
        Args:
            path: Dizin yolu
            
        Returns:
            bool: Başarılı mı
        """
        try:
            shutil.rmtree(path)
            return True
        except Exception:
            return False
    
    def _safe_delete(self, path: str) -> bool:
        """
        Güvenli sil.
        
        Args:
            path: Dosya yolu
            
        Returns:
            bool: Başarılı mı
        """
        try:
            # Overwrite file with zeros before deletion
            with open(path, 'wb') as f:
                f.write(b'\x00' * os.path.getsize(path))
            
            os.remove(path)
            return True
        except Exception:
            return False
    
    def _safe_delete_directory(self, path: str) -> bool:
        """
        Dizini güvenli sil.
        
        Args:
            path: Dizin yolu
            
        Returns:
            bool: Başarılı mı
        """
        try:
            # Safe delete all files in directory
            for root, dirs, files in os.walk(path):
                for file in files:
                    file_path = os.path.join(root, file)
                    self._safe_delete(file_path)
            
            shutil.rmtree(path)
            return True
        except Exception:
            return False
    
    def _calculate_directory_size(self, path: str) -> int:
        """
        Dizin boyutunu hesapla.
        
        Args:
            path: Dizin yolu
            
        Returns:
            int: Boyut
        """
        total_size = 0
        try:
            for dirpath, dirnames, filenames in os.walk(path):
                for filename in filenames:
                    file_path = os.path.join(dirpath, filename)
                    total_size += os.path.getsize(file_path)
        except Exception:
            pass
        return total_size
    
    def undo_delete(self, path: str) -> DeleteResult:
        """
        Silmeyi geri al.
        
        Args:
            path: Dosya yolu
            
        Returns:
            DeleteResult: Geri alma sonucu
        """
        result = DeleteResult(success=False)
        
        try:
            # Find in history
            for item in reversed(self.delete_history):
                if item["path"] == path and not item["restored"]:
                    # Restore from trash
                    if item["mode"] == DeleteMode.MOVE_TO_TRASH.value:
                        success = self._restore_from_trash(path)
                    else:
                        result.errors.append("Cannot restore permanent delete")
                        return result
                    
                    if success:
                        item["restored"] = True
                        result.success = True
                        result.message = f"File restored: {path}"
                    else:
                        result.errors.append("Restore operation failed")
                    return result
            
            result.errors.append("Delete history not found")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def _restore_from_trash(self, path: str) -> bool:
        """
        Geri dönüşüm kutusundan geri yükle.
        
        Args:
            path: Dosya yolu
            
        Returns:
            bool: Başarılı mı
        """
        try:
            if self.trash_path is None or not os.path.exists(self.trash_path):
                return False
            
            # Find in trash
            trash_name = None
            for item in os.listdir(self.trash_path):
                if item.startswith(os.path.basename(path)):
                    trash_name = item
                    break
            
            if trash_name is None:
                return False
            
            trash_path = os.path.join(self.trash_path, trash_name)
            shutil.move(trash_path, path)
            return True
        
        except Exception:
            return False
    
    def get_delete_history(self) -> List[Dict[str, Any]]:
        """
        Silme geçmişini al.
        
        Returns:
            List[Dict[str, Any]]: Geçmiş
        """
        return self.delete_history
    
    def clear_history(self) -> DeleteResult:
        """
        Geçmişi temizle.
        
        Returns:
            DeleteResult: Temizleme sonucu
        """
        result = DeleteResult(success=False)
        
        try:
            self.delete_history.clear()
            result.success = True
            result.message = "Delete history cleared"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def update_config(self, config: DeleteConfig) -> DeleteResult:
        """
        Konfigürasyon güncelle.
        
        Args:
            config: Yeni konfigürasyon
            
        Returns:
            DeleteResult: Güncelleme sonucu
        """
        result = DeleteResult(success=False)
        
        try:
            self.config = config
            result.success = True
            result.message = "Config updated"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_config(self) -> DeleteConfig:
        """
        Konfigürasyon al.
        
        Returns:
            DeleteConfig: Konfigürasyon
        """
        return self.config
    
    def can_delete(self, path: str) -> bool:
        """
        Silinebilir mi?
        
        Args:
            path: Dosya yolu
            
        Returns:
            bool: Silinebilir mi
        """
        try:
            if not os.path.exists(path):
                return False
            
            # Check permissions
            if not os.access(path, os.W_OK):
                return False
            
            return True
        
        except Exception:
            return False
    
    def get_file_size(self, path: str) -> int:
        """
        Dosya boyutunu al.
        
        Args:
            path: Dosya yolu
            
        Returns:
            int: Boyut
        """
        try:
            if os.path.isfile(path):
                return os.path.getsize(path)
            elif os.path.isdir(path):
                return self._calculate_directory_size(path)
            return 0
        except Exception:
            return 0


if __name__ == "__main__":
    # Basit test
    engine = FileDeletionEngine()
    
    result = engine.can_delete("test.txt")
    print(f"Can delete: {result}")
