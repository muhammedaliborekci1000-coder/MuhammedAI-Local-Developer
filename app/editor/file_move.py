"""
MuhammedAI Local Developer - File Move
File move engine for code editor.
"""

from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from enum import Enum
import os
import shutil
from datetime import datetime


class MoveMode(Enum):
    """Move mode."""
    SIMPLE = "simple"
    PRESERVE_METADATA = "preserve_metadata"
    FORCE = "force"


class MoveScope(Enum):
    """Move scope."""
    FILE = "file"
    DIRECTORY = "directory"
    MULTIPLE = "multiple"


@dataclass
class MoveTarget:
    """Move target."""
    source: str
    destination: str
    is_directory: bool = False


@dataclass
class MoveConfig:
    """Move configuration."""
    mode: MoveMode = MoveMode.SIMPLE
    overwrite: bool = False
    preserve_metadata: bool = True
    create_parent_directories: bool = True
    show_notification: bool = True


@dataclass
class MoveResult:
    """Move result."""
    success: bool
    message: Optional[str] = None
    errors: List[str] = field(default_factory=list)
    moved_count: int = 0
    moved_size: int = 0
    source_paths: List[str] = field(default_factory=list)
    destination_paths: List[str] = field(default_factory=list)


class FileMoveEngine:
    """
    File move engine.
    
    Özellikler:
    - Move files
    - Move directories
    - Simple move
    - Preserve metadata
    - Force move
    - Batch move
    - Move history
    - Undo support
    - Permission check
    - Overwrite control
    - Parent directory creation
    - Smart detection
    """
    
    def __init__(self, config: Optional[MoveConfig] = None):
        """Initialize file move engine."""
        self.config = config or MoveConfig()
        self.move_history: List[Dict[str, Any]] = []
    
    def move_file(self, source: str, destination: str) -> MoveResult:
        """
        Dosya taşı.
        
        Args:
            source: Kaynak yol
            destination: Hedef yol
            
        Returns:
            MoveResult: Taşıma sonucu
        """
        result = MoveResult(success=False)
        result.source_paths = [source]
        result.destination_paths = [destination]
        
        try:
            if not os.path.exists(source):
                result.errors.append(f"Source not found: {source}")
                return result
            
            if os.path.isdir(source):
                result.errors.append(f"Source is a directory: {source}")
                return result
            
            if os.path.exists(destination) and not self.config.overwrite:
                result.errors.append(f"Destination already exists: {destination}")
                return result
            
            # Create parent directories if needed
            parent_dir = os.path.dirname(destination)
            if parent_dir and self.config.create_parent_directories:
                os.makedirs(parent_dir, exist_ok=True)
            
            # Get file size
            size = os.path.getsize(source)
            
            # Move based on mode
            if self.config.mode == MoveMode.PRESERVE_METADATA:
                success = self._move_with_metadata(source, destination)
            elif self.config.mode == MoveMode.FORCE:
                success = self._force_move(source, destination)
            else:
                success = self._simple_move(source, destination)
            
            if success:
                # Add to history
                self.move_history.append({
                    "source": source,
                    "destination": destination,
                    "mode": self.config.mode.value,
                    "timestamp": datetime.now().isoformat(),
                    "restored": False
                })
                
                result.success = True
                result.moved_count = 1
                result.moved_size = size
                result.message = f"File moved: {source} -> {destination}"
            else:
                result.errors.append("Move operation failed")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def move_directory(self, source: str, destination: str) -> MoveResult:
        """
        Dizin täşı.
        
        Args:
            source: Kaynak yol
            destination: Hedef yol
            
        Returns:
            MoveResult: Taşıma sonucu
        """
        result = MoveResult(success=False)
        result.source_paths = [source]
        result.destination_paths = [destination]
        
        try:
            if not os.path.exists(source):
                result.errors.append(f"Source not found: {source}")
                return result
            
            if not os.path.isdir(source):
                result.errors.append(f"Source is not a directory: {source}")
                return result
            
            if os.path.exists(destination) and not self.config.overwrite:
                result.errors.append(f"Destination already exists: {destination}")
                return result
            
            # Calculate size
            size = self._calculate_directory_size(source)
            
            # Move based on mode
            if self.config.mode == MoveMode.PRESERVE_METADATA:
                success = self._move_directory_with_metadata(source, destination)
            elif self.config.mode == MoveMode.FORCE:
                success = self._force_move_directory(source, destination)
            else:
                success = self._simple_move_directory(source, destination)
            
            if success:
                # Add to history
                self.move_history.append({
                    "source": source,
                    "destination": destination,
                    "mode": self.config.mode.value,
                    "timestamp": datetime.now().isoformat(),
                    "restored": False
                })
                
                result.success = True
                result.moved_count = 1
                result.moved_size = size
                result.message = f"Directory moved: {source} -> {destination}"
            else:
                result.errors.append("Move operation failed")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def move_multiple(self, targets: List[MoveTarget]) -> MoveResult:
        """
        Toplu taşı.
        
        Args:
            targets: Taşıma hedefleri
            
        Returns:
            MoveResult: Taşıma sonucu
        """
        result = MoveResult(success=False)
        
        try:
            moved_count = 0
            moved_size = 0
            source_paths = []
            destination_paths = []
            
            for target in targets:
                source_paths.append(target.source)
                destination_paths.append(target.destination)
                
                if target.is_directory:
                    sub_result = self.move_directory(target.source, target.destination)
                else:
                    sub_result = self.move_file(target.source, target.destination)
                
                if sub_result.success:
                    moved_count += sub_result.moved_count
                    moved_size += sub_result.moved_size
                else:
                    result.errors.extend(sub_result.errors)
            
            result.success = moved_count > 0
            result.moved_count = moved_count
            result.moved_size = moved_size
            result.source_paths = source_paths
            result.destination_paths = destination_paths
            result.message = f"Moved {moved_count} items"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def _simple_move(self, source: str, destination: str) -> bool:
        """
        Basit taşı.
        
        Args:
            source: Kaynak yol
            destination: Hedef yol
            
        Returns:
            bool: Başarılı mı
        """
        try:
            shutil.move(source, destination)
            return True
        except Exception:
            return False
    
    def _move_with_metadata(self, source: str, destination: str) -> bool:
        """
        Metadata ile taşı.
        
        Args:
            source: Kaynak yol
            destination: Hedef yol
            
        Returns:
            bool: Başarılı mı
        """
        try:
            shutil.move(source, destination)
            return True
        except Exception:
            return False
    
    def _force_move(self, source: str, destination: str) -> bool:
        """
        Zorla taşı.
        
        Args:
            source: Kaynak yol
            destination: Hedef yol
            
        Returns:
            bool: Başarılı mı
        """
        try:
            if os.path.exists(destination):
                if os.path.isdir(destination):
                    shutil.rmtree(destination)
                else:
                    os.remove(destination)
            shutil.move(source, destination)
            return True
        except Exception:
            return False
    
    def _simple_move_directory(self, source: str, destination: str) -> bool:
        """
        Dizini basit taşı.
        
        Args:
            source: Kaynak yol
            destination: Hedef yol
            
        Returns:
            bool: Başarılı mı
        """
        try:
            shutil.move(source, destination)
            return True
        except Exception:
            return False
    
    def _move_directory_with_metadata(self, source: str, destination: str) -> bool:
        """
        Dizini metadata ile taşı.
        
        Args:
            source: Kaynak yol
            destination: Hedef yol
            
        Returns:
            bool: Başarılı mı
        """
        try:
            shutil.move(source, destination)
            return True
        except Exception:
            return False
    
    def _force_move_directory(self, source: str, destination: str) -> bool:
        """
        Dizini zorla taşı.
        
        Args:
            source: Kaynak yol
            destination: Hedef yol
            
        Returns:
            bool: Başarılı mı
        """
        try:
            if os.path.exists(destination):
                shutil.rmtree(destination)
            shutil.move(source, destination)
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
    
    def undo_move(self, destination: str) -> MoveResult:
        """
        Taşımayı geri al.
        
        Args:
            destination: Hedef yol
            
        Returns:
            MoveResult: Geri alma sonucu
        """
        result = MoveResult(success=False)
        
        try:
            # Find in history
            for item in reversed(self.move_history):
                if item["destination"] == destination and not item["restored"]:
                    # Move back to original location
                    success = self._simple_move(destination, item["source"])
                    
                    if success:
                        item["restored"] = True
                        result.success = True
                        result.message = f"File moved back: {destination} -> {item['source']}"
                    else:
                        result.errors.append("Restore operation failed")
                    return result
            
            result.errors.append("Move history not found")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_move_history(self) -> List[Dict[str, Any]]:
        """
        Taşıma geçmişini al.
        
        Returns:
            List[Dict[str, Any]]: Geçmiş
        """
        return self.move_history
    
    def clear_history(self) -> MoveResult:
        """
        Geçmişi temizle.
        
        Returns:
            MoveResult: Temizleme sonucu
        """
        result = MoveResult(success=False)
        
        try:
            self.move_history.clear()
            result.success = True
            result.message = "Move history cleared"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def update_config(self, config: MoveConfig) -> MoveResult:
        """
        Konfigürasyon güncelle.
        
        Args:
            config: Yeni konfigürasyon
            
        Returns:
            MoveResult: Güncelleme sonucu
        """
        result = MoveResult(success=False)
        
        try:
            self.config = config
            result.success = True
            result.message = "Config updated"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_config(self) -> MoveConfig:
        """
        Konfigürasyon al.
        
        Returns:
            MoveConfig: Konfigürasyon
        """
        return self.config
    
    def can_move(self, source: str, destination: str) -> bool:
        """
        Taşınabilir mi?
        
        Args:
            source: Kaynak yol
            destination: Hedef yol
            
        Returns:
            bool: Taşınabilir mi
        """
        try:
            if not os.path.exists(source):
                return False
            
            # Check source permissions
            if not os.access(source, os.R_OK):
                return False
            
            # Check destination parent permissions
            parent_dir = os.path.dirname(destination)
            if parent_dir:
                if not os.path.exists(parent_dir):
                    return True  # Will create parent directories
                if not os.access(parent_dir, os.W_OK):
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
    engine = FileMoveEngine()
    
    result = engine.can_move("test.txt", "test_moved.txt")
    print(f"Can move: {result}")
