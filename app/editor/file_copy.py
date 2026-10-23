"""
MuhammedAI Local Developer - File Copy
File copy engine for code editor.
"""

from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from enum import Enum
import os
import shutil
from datetime import datetime


class CopyMode(Enum):
    """Copy mode."""
    SIMPLE = "simple"
    DEEP = "deep"
    SHALLOW = "shallow"
    PRESERVE_METADATA = "preserve_metadata"


class CopyScope(Enum):
    """Copy scope."""
    FILE = "file"
    DIRECTORY = "directory"
    MULTIPLE = "multiple"


@dataclass
class CopyTarget:
    """Copy target."""
    source: str
    destination: str
    is_directory: bool = False


@dataclass
class CopyConfig:
    """Copy configuration."""
    mode: CopyMode = CopyMode.SIMPLE
    overwrite: bool = False
    preserve_metadata: bool = True
    preserve_permissions: bool = True
    create_parent_directories: bool = True
    show_notification: bool = True


@dataclass
class CopyResult:
    """Copy result."""
    success: bool
    message: Optional[str] = None
    errors: List[str] = field(default_factory=list)
    copied_count: int = 0
    copied_size: int = 0
    source_paths: List[str] = field(default_factory=list)
    destination_paths: List[str] = field(default_factory=list)


class FileCopyEngine:
    """
    File copy engine.
    
    Özellikler:
    - Copy files
    - Copy directories
    - Deep copy
    - Shallow copy
    - Preserve metadata
    - Preserve permissions
    - Batch copy
    - Copy history
    - Undo support
    - Permission check
    - Overwrite control
    - Parent directory creation
    - Smart detection
    """
    
    def __init__(self, config: Optional[CopyConfig] = None):
        """Initialize file copy engine."""
        self.config = config or CopyConfig()
        self.copy_history: List[Dict[str, Any]] = []
    
    def copy_file(self, source: str, destination: str) -> CopyResult:
        """
        Dosya kopyala.
        
        Args:
            source: Kaynak yol
            destination: Hedef yol
            
        Returns:
            CopyResult: Kopyalama sonucu
        """
        result = CopyResult(success=False)
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
            
            # Copy based on mode
            if self.config.mode == CopyMode.PRESERVE_METADATA:
                success = self._copy_with_metadata(source, destination)
            elif self.config.mode == CopyMode.DEEP:
                success = self._deep_copy(source, destination)
            elif self.config.mode == CopyMode.SHALLOW:
                success = self._shallow_copy(source, destination)
            else:
                success = self._simple_copy(source, destination)
            
            if success:
                # Add to history
                self.copy_history.append({
                    "source": source,
                    "destination": destination,
                    "mode": self.config.mode.value,
                    "timestamp": datetime.now().isoformat(),
                    "deleted": False
                })
                
                result.success = True
                result.copied_count = 1
                result.copied_size = size
                result.message = f"File copied: {source} -> {destination}"
            else:
                result.errors.append("Copy operation failed")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def copy_directory(self, source: str, destination: str) -> CopyResult:
        """
        Dizin kopyala.
        
        Args:
            source: Kaynak yol
            destination: Hedef yol
            
        Returns:
            CopyResult: Kopyalama sonucu
        """
        result = CopyResult(success=False)
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
            
            # Copy based on mode
            if self.config.mode == CopyMode.PRESERVE_METADATA:
                success = self._copy_directory_with_metadata(source, destination)
            elif self.config.mode == CopyMode.DEEP:
                success = self._deep_copy_directory(source, destination)
            elif self.config.mode == CopyMode.SHALLOW:
                success = self._shallow_copy_directory(source, destination)
            else:
                success = self._simple_copy_directory(source, destination)
            
            if success:
                # Add to history
                self.copy_history.append({
                    "source": source,
                    "destination": destination,
                    "mode": self.config.mode.value,
                    "timestamp": datetime.now().isoformat(),
                    "deleted": False
                })
                
                result.success = True
                result.copied_count = 1
                result.copied_size = size
                result.message = f"Directory copied: {source} -> {destination}"
            else:
                result.errors.append("Copy operation failed")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def copy_multiple(self, targets: List[CopyTarget]) -> CopyResult:
        """
        Toplu kopyala.
        
        Args:
            targets: Kopyalama hedefleri
            
        Returns:
            CopyResult: Kopyalama sonucu
        """
        result = CopyResult(success=False)
        
        try:
            copied_count = 0
            copied_size = 0
            source_paths = []
            destination_paths = []
            
            for target in targets:
                source_paths.append(target.source)
                destination_paths.append(target.destination)
                
                if target.is_directory:
                    sub_result = self.copy_directory(target.source, target.destination)
                else:
                    sub_result = self.copy_file(target.source, target.destination)
                
                if sub_result.success:
                    copied_count += sub_result.copied_count
                    copied_size += sub_result.copied_size
                else:
                    result.errors.extend(sub_result.errors)
            
            result.success = copied_count > 0
            result.copied_count = copied_count
            result.copied_size = copied_size
            result.source_paths = source_paths
            result.destination_paths = destination_paths
            result.message = f"Copied {copied_count} items"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def _simple_copy(self, source: str, destination: str) -> bool:
        """
        Basit kopyala.
        
        Args:
            source: Kaynak yol
            destination: Hedef yol
            
        Returns:
            bool: Başarılı mı
        """
        try:
            shutil.copy2(source, destination)
            return True
        except Exception:
            return False
    
    def _deep_copy(self, source: str, destination: str) -> bool:
        """
        Derin kopyala.
        
        Args:
            source: Kaynak yol
            destination: Hedef yol
            
        Returns:
            bool: Başarılı mı
        """
        try:
            shutil.copy2(source, destination)
            return True
        except Exception:
            return False
    
    def _shallow_copy(self, source: str, destination: str) -> bool:
        """
    -Sığ kopyala.
        
        Args:
            source: Kaynak yol
            destination: Hedef yol
            
        Returns:
            bool: Başarılı mı
        """
        try:
            shutil.copy(source, destination)
            return True
        except Exception:
            return False
    
    def _copy_with_metadata(self, source: str, destination: str) -> bool:
        """
        Metadata ile kopyala.
        
        Args:
            source: Kaynak yol
            destination: Hedef yol
            
        Returns:
            bool: Başarılı mı
        """
        try:
            shutil.copy2(source, destination)
            return True
        except Exception:
            return False
    
    def _simple_copy_directory(self, source: str, destination: str) -> bool:
        """
        Dizini basit kopyala.
        
        Args:
            source: Kaynak yol
            destination: Hedef yol
            
        Returns:
            bool: Başarılı mı
        """
        try:
            shutil.copytree(source, destination)
            return True
        except Exception:
            return False
    
    def _deep_copy_directory(self, source: str, destination: str) -> bool:
        """
        Dizini derin kopyala.
        
        Args:
            source: Kaynak yol
            destination: Hedef yol
            
        Returns:
            bool: Başarılı mı
        """
        try:
            shutil.copytree(source, destination)
            return True
        except Exception:
            return False
    
    def _shallow_copy_directory(self, source: str, destination: str) -> bool:
        """
        Dizini sığ kopyala.
        
        Args:
            source: Kaynak yol
            destination: Hedef yol
            
        Returns:
            bool: Başarılı mı
        """
        try:
            shutil.copytree(source, destination, copy_function=shutil.copy)
            return True
        except Exception:
            return False
    
    def _copy_directory_with_metadata(self, source: str, destination: str) -> bool:
        """
        Dizini metadata ile kopyala.
        
        Args:
            source: Kaynak yol
            destination: Hedef yol
            
        Returns:
            bool: Başarılı mı
        """
        try:
            shutil.copytree(source, destination, copy_function=shutil.copy2)
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
    
    def undo_copy(self, destination: str) -> CopyResult:
        """
        Kopyalamayı geri al.
        
        Args:
            destination: Hedef yol
            
        Returns:
            CopyResult: Geri alma sonucu
        """
        result = CopyResult(success=False)
        
        try:
            # Find in history
            for item in reversed(self.copy_history):
                if item["destination"] == destination and not item["deleted"]:
                    # Delete the copied file/directory
                    if os.path.isfile(destination):
                        os.remove(destination)
                    elif os.path.isdir(destination):
                        shutil.rmtree(destination)
                    
                    item["deleted"] = True
                    result.success = True
                    result.message = f"File deleted: {destination}"
                    return result
            
            result.errors.append("Copy history not found")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_copy_history(self) -> List[Dict[str, Any]]:
        """
        Kopyalama geçmişini al.
        
        Returns:
            List[Dict[str, Any]]: Geçmiş
        """
        return self.copy_history
    
    def clear_history(self) -> CopyResult:
        """
        Geçmişi temizle.
        
        Returns:
            CopyResult: Temizleme sonucu
        """
        result = CopyResult(success=False)
        
        try:
            self.copy_history.clear()
            result.success = True
            result.message = "Copy history cleared"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def update_config(self, config: CopyConfig) -> CopyResult:
        """
        Konfigürasyon güncelle.
        
        Args:
            config: Yeni konfigürasyon
            
        Returns:
            CopyResult: Güncelleme sonucu
        """
        result = CopyResult(success=False)
        
        try:
            self.config = config
            result.success = True
            result.message = "Config updated"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_config(self) -> CopyConfig:
        """
        Konfigürasyon al.
        
        Returns:
            CopyConfig: Konfigürasyon
        """
        return self.config
    
    def can_copy(self, source: str, destination: str) -> bool:
        """
        Kopyalanabilir mi?
        
        Args:
            source: Kaynak yol
            destination: Hedef yol
            
        Returns:
            bool: Kopyalanabilir mi
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
    engine = FileCopyEngine()
    
    result = engine.can_copy("test.txt", "test_copy.txt")
    print(f"Can copy: {result}")
