"""
MuhammedAI Local Developer - Directory Deletion
Directory deletion engine for code editor.
"""

from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from enum import Enum
import os
import shutil
from datetime import datetime


class DeleteMode(Enum):
    """Delete mode."""
    SINGLE = "single"
    RECURSIVE = "recursive"
    FORCE = "force"
    SAFE = "safe"


class DeleteScope(Enum):
    """Delete scope."""
    CONTENTS_ONLY = "contents_only"
    DIRECTORY_ONLY = "directory_only"
    ALL = "all"


@dataclass
class DeleteConfig:
    """Delete configuration."""
    mode: DeleteMode = DeleteMode.RECURSIVE
    scope: DeleteScope = DeleteScope.ALL
    confirm_before_delete: bool = True
    move_to_trash: bool = False
    backup_before_delete: bool = False
    backup_path: str = ""
    show_notification: bool = True


@dataclass
class DeleteResult:
    """Delete result."""
    success: bool
    message: Optional[str] = None
    errors: List[str] = field(default_factory=list)
    deleted_path: Optional[str] = None
    deleted_count: int = 0
    backup_path: Optional[str] = None


class DirectoryDeletionEngine:
    """
    Directory deletion engine.
    
    Özellikler:
    - Delete directory
    - Delete recursively
    - Delete contents only
    - Force deletion
    - Safe deletion
    - Move to trash
    - Backup before delete
    - Delete history
    - Undo support
    - Smart detection
    """
    
    def __init__(self, config: Optional[DeleteConfig] = None):
        """Initialize directory deletion engine."""
        self.config = config or DeleteConfig()
        self.deletion_history: List[Dict[str, Any]] = []
    
    def delete_directory(self, path: str) -> DeleteResult:
        """
        Dizin sil.
        
        Args:
            path: Dizin yolu
            
        Returns:
            DeleteResult: Silme sonucu
        """
        result = DeleteResult(success=False)
        result.deleted_path = path
        
        try:
            # Check if exists
            if not os.path.exists(path):
                result.errors.append(f"Path not found: {path}")
                return result
            
            # Check if directory
            if not os.path.isdir(path):
                result.errors.append(f"Path is not a directory: {path}")
                return result
            
            # Backup before delete
            backup_path = None
            if self.config.backup_before_delete:
                backup_path = self._backup_directory(path)
                result.backup_path = backup_path
            
            # Delete based on scope
            if self.config.scope == DeleteScope.CONTENTS_ONLY:
                deleted_count = self._delete_contents(path)
            elif self.config.scope == DeleteScope.DIRECTORY_ONLY:
                # Only delete if empty
                if len(os.listdir(path)) > 0:
                    if self.config.mode == DeleteMode.FORCE:
                        deleted_count = self._delete_recursive(path)
                    else:
                        result.errors.append(f"Directory not empty: {path}")
                        return result
                else:
                    os.rmdir(path)
                    deleted_count = 1
            else:  # ALL
                deleted_count = self._delete_recursive(path)
            
            # Add to history
            self.deletion_history.append({
                "path": path,
                "mode": self.config.mode.value,
                "scope": self.config.scope.value,
                "backup_path": backup_path,
                "timestamp": self._get_timestamp()
            })
            
            result.success = True
            result.deleted_count = deleted_count
            result.message = f"Directory deleted: {path}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def delete_multiple(self, paths: List[str]) -> DeleteResult:
        """
        Birden fazla dizin sil.
        
        Args:
            paths: Dizin yolları
            
        Returns:
            DeleteResult: Silme sonucu
        """
        result = DeleteResult(success=False)
        deleted_count = 0
        all_errors = []
        
        for path in paths:
            single_result = self.delete_directory(path)
            if single_result.success:
                deleted_count += single_result.deleted_count
            else:
                all_errors.extend(single_result.errors)
        
        result.success = deleted_count > 0
        result.deleted_count = deleted_count
        result.errors = all_errors
        result.message = f"Deleted {deleted_count} items"
        
        return result
    
    def can_delete(self, path: str) -> bool:
        """
        Silinebilir mi?
        
        Args:
            path: Dizin yolu
            
        Returns:
            bool: Silinebilir mi
        """
        try:
            if not os.path.exists(path):
                return False
            
            if not os.path.isdir(path):
                return False
            
            # Check if empty for safe mode
            if self.config.mode == DeleteMode.SAFE:
                return len(os.listdir(path)) == 0
            
            return True
        except Exception:
            return False
    
    def undo_deletion(self, path: str) -> DeleteResult:
        """
        Silmeyi geri al.
        
        Args:
            path: Dizin yolu
            
        Returns:
            DeleteResult: Geri alma sonucu
        """
        result = DeleteResult(success=False)
        
        try:
            # Find in history
            history_entry = None
            for entry in self.deletion_history:
                if entry["path"] == path:
                    history_entry = entry
                    break
            
            if not history_entry:
                result.errors.append(f"Deletion not found in history: {path}")
                return result
            
            # Restore from backup
            backup_path = history_entry.get("backup_path")
            if backup_path and os.path.exists(backup_path):
                shutil.copytree(backup_path, path)
                
                # Remove backup
                shutil.rmtree(backup_path)
                
                # Remove from history
                self.deletion_history = [
                    h for h in self.deletion_history
                    if h["path"] != path
                ]
                
                result.success = True
                result.message = f"Directory restored: {path}"
            else:
                result.errors.append(f"Backup not found: {backup_path}")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def _delete_contents(self, path: str) -> int:
        """
        İçeriği sil.
        
        Args:
            path: Dizin yolu
            
        Returns:
            int: Silinen sayısı
        """
        deleted_count = 0
        
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            
            if os.path.isdir(item_path):
                deleted_count += self._delete_recursive(item_path)
            else:
                os.remove(item_path)
                deleted_count += 1
        
        return deleted_count
    
    def _delete_recursive(self, path: str) -> int:
        """
        Özyinelemeli sil.
        
        Args:
            path: Dizin yolu
            
        Returns:
            int: Silinen sayısı
        """
        deleted_count = 0
        
        if os.path.isdir(path):
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                deleted_count += self._delete_recursive(item_path)
            
            os.rmdir(path)
            deleted_count += 1
        else:
            os.remove(path)
            deleted_count += 1
        
        return deleted_count
    
    def _backup_directory(self, path: str) -> str:
        """
        Dizin yedeği al.
        
        Args:
            path: Dizin yolu
            
        Returns:
            str: Yedek yolu
        """
        if not self.config.backup_path:
            self.config.backup_path = os.path.join(
                os.path.expanduser("~"),
                ".muhammedai",
                "backups"
            )
        
        # Create backup directory
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{os.path.basename(path)}_{timestamp}"
        backup_path = os.path.join(self.config.backup_path, backup_name)
        
        # Create parent directories
        os.makedirs(self.config.backup_path, exist_ok=True)
        
        # Copy to backup
        shutil.copytree(path, backup_path)
        
        return backup_path
    
    def get_deletion_history(self) -> List[Dict[str, Any]]:
        """
        Silme geçmişini al.
        
        Returns:
            List[Dict[str, Any]]: Geçmiş
        """
        return self.deletion_history
    
    def clear_history(self) -> DeleteResult:
        """
        Geçmişi temizle.
        
        Returns:
            DeleteResult: Temizleme sonucu
        """
        result = DeleteResult(success=False)
        
        try:
            self.deletion_history.clear()
            result.success = True
            result.message = "Deletion history cleared"
        
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
    
    def _get_timestamp(self) -> str:
        """
        Zaman damgası al.
        
        Returns:
            str: ISO format zaman damgası
        """
        return datetime.now().isoformat()


if __name__ == "__main__":
    # Basit test
    engine = DirectoryDeletionEngine()
    
    print("Directory Deletion Engine initialized")
    print(f"Mode: {engine.config.mode.value}")
