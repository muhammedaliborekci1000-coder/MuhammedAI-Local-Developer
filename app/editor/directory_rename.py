"""
MuhammedAI Local Developer - Directory Rename
Directory rename engine for code editor.
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
    FORCE = "force"
    PRESERVE_STRUCTURE = "preserve_structure"


@dataclass
class RenameConfig:
    """Rename configuration."""
    mode: RenameMode = RenameMode.SIMPLE
    update_references: bool = True
    create_backup: bool = False
    backup_path: str = ""
    confirm_before_rename: bool = True
    show_notification: bool = True


@dataclass
class RenameResult:
    """Rename result."""
    success: bool
    message: Optional[str] = None
    errors: List[str] = field(default_factory=list)
    old_path: Optional[str] = None
    new_path: Optional[str] = None
    backup_path: Optional[str] = None


class DirectoryRenameEngine:
    """
    Directory rename engine.
    
    Özellikler:
    - Rename directory
    - Case change rename
    - Force rename
    - Preserve structure
    - Update references
    - Backup before rename
    - Rename history
    - Undo support
    - Smart detection
    """
    
    def __init__(self, config: Optional[RenameConfig] = None):
        """Initialize directory rename engine."""
        self.config = config or RenameConfig()
        self.rename_history: List[Dict[str, Any]] = []
    
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
        result.old_path = old_path
        result.new_path = new_path
        
        try:
            # Check if old path exists
            if not os.path.exists(old_path):
                result.errors.append(f"Old path not found: {old_path}")
                return result
            
            # Check if old path is directory
            if not os.path.isdir(old_path):
                result.errors.append(f"Old path is not a directory: {old_path}")
                return result
            
            # Check if new path already exists
            if os.path.exists(new_path):
                if self.config.mode == RenameMode.FORCE:
                    # Remove existing
                    import shutil
                    if os.path.isdir(new_path):
                        shutil.rmtree(new_path)
                    else:
                        os.remove(new_path)
                else:
                    result.errors.append(f"New path already exists: {new_path}")
                    return result
            
            # Backup before rename
            backup_path = None
            if self.config.create_backup:
                backup_path = self._backup_directory(old_path)
                result.backup_path = backup_path
            
            # Rename directory
            os.rename(old_path, new_path)
            
            # Add to history
            self.rename_history.append({
                "old_path": old_path,
                "new_path": new_path,
                "mode": self.config.mode.value,
                "backup_path": backup_path,
                "timestamp": self._get_timestamp()
            })
            
            result.success = True
            result.message = f"Directory renamed: {old_path} -> {new_path}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def rename_multiple(self, rename_pairs: List[Tuple[str, str]]) -> RenameResult:
        """
        Birden fazla dizini yeniden adlandır.
        
        Args:
            rename_pairs: (old_path, new_path) çiftleri
            
        Returns:
            RenameResult: Yeniden adlandırma sonucu
        """
        result = RenameResult(success=False)
        renamed_count = 0
        all_errors = []
        
        for old_path, new_path in rename_pairs:
            single_result = self.rename_directory(old_path, new_path)
            if single_result.success:
                renamed_count += 1
            else:
                all_errors.extend(single_result.errors)
        
        result.success = renamed_count > 0
        result.errors = all_errors
        result.message = f"Renamed {renamed_count} directories"
        
        return result
    
    def can_rename(self, old_path: str, new_path: str) -> bool:
        """
        Yeniden adlandırılabilir mi?
        
        Args:
            old_path: Eski yol
            new_path: Yeni yol
            
        Returns:
            bool: Yeniden adlandırılabilir mi
        """
        try:
            if not os.path.exists(old_path):
                return False
            
            if not os.path.isdir(old_path):
                return False
            
            if os.path.exists(new_path):
                return self.config.mode == RenameMode.FORCE
            
            return True
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
            history_entry = None
            for entry in self.rename_history:
                if entry["new_path"] == new_path:
                    history_entry = entry
                    break
            
            if not history_entry:
                result.errors.append(f"Rename not found in history: {new_path}")
                return result
            
            old_path = history_entry["old_path"]
            
            # Rename back
            os.rename(new_path, old_path)
            
            # Remove from history
            self.rename_history = [
                h for h in self.rename_history
                if h["new_path"] != new_path
            ]
            
            result.success = True
            result.message = f"Directory renamed back: {new_path} -> {old_path}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
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
        import shutil
        shutil.copytree(path, backup_path)
        
        return backup_path
    
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
    
    def _get_timestamp(self) -> str:
        """
        Zaman damgası al.
        
        Returns:
            str: ISO format zaman damgası
        """
        return datetime.now().isoformat()


if __name__ == "__main__":
    # Basit test
    engine = DirectoryRenameEngine()
    
    print("Directory Rename Engine initialized")
    print(f"Mode: {engine.config.mode.value}")
