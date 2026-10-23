"""
MuhammedAI Local Developer - File Duplicate
File duplicate engine for code editor.
"""

from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from enum import Enum
import os
import shutil
from datetime import datetime


class DuplicateMode(Enum):
    """Duplicate mode."""
    NUMBERED = "numbered"
    TIMESTAMP = "timestamp"
    CUSTOM_SUFFIX = "custom_suffix"
    COPY_SUFFIX = "copy_suffix"


class DuplicateScope(Enum):
    """Duplicate scope."""
    FILE = "file"
    DIRECTORY = "directory"
    MULTIPLE = "multiple"


@dataclass
class DuplicateTarget:
    """Duplicate target."""
    source: str
    is_directory: bool = False


@dataclass
class DuplicateConfig:
    """Duplicate configuration."""
    mode: DuplicateMode = DuplicateMode.NUMBERED
    custom_suffix: str = ""
    preserve_metadata: bool = True
    show_notification: bool = True


@dataclass
class DuplicateResult:
    """Duplicate result."""
    success: bool
    message: Optional[str] = None
    errors: List[str] = field(default_factory=list)
    duplicated_count: int = 0
    duplicated_size: int = 0
    source_paths: List[str] = field(default_factory=list)
    destination_paths: List[str] = field(default_factory=list)


class FileDuplicateEngine:
    """
    File duplicate engine.
    
    Özellikler:
    - Duplicate files
    - Duplicate directories
    - Numbered duplicate
    - Timestamp duplicate
    - Custom suffix
    - Copy suffix
    - Batch duplicate
    - Duplicate history
    - Undo support
    - Permission check
    - Smart detection
    """
    
    def __init__(self, config: Optional[DuplicateConfig] = None):
        """Initialize file duplicate engine."""
        self.config = config or DuplicateConfig()
        self.duplicate_history: List[Dict[str, Any]] = []
    
    def duplicate_file(self, source: str) -> DuplicateResult:
        """
        Dosya çoğalt.
        
        Args:
            source: Kaynak yol
            
        Returns:
            DuplicateResult: Çoğaltma sonucu
        """
        result = DuplicateResult(success=False)
        result.source_paths = [source]
        
        try:
            if not os.path.exists(source):
                result.errors.append(f"Source not found: {source}")
                return result
            
            if os.path.isdir(source):
                result.errors.append(f"Source is a directory: {source}")
                return result
            
            # Generate destination path
            destination = self._generate_duplicate_path(source)
            
            # Get file size
            size = os.path.getsize(source)
            
            # Duplicate file
            if self.config.preserve_metadata:
                shutil.copy2(source, destination)
            else:
                shutil.copy(source, destination)
            
            # Add to history
            self.duplicate_history.append({
                "source": source,
                "destination": destination,
                "mode": self.config.mode.value,
                "timestamp": datetime.now().isoformat(),
                "deleted": False
            })
            
            result.success = True
            result.duplicated_count = 1
            result.duplicated_size = size
            result.destination_paths = [destination]
            result.message = f"File duplicated: {source} -> {destination}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def duplicate_directory(self, source: str) -> DuplicateResult:
        """
        Dizini çoğalt.
        
        Args:
            source: Kaynak yol
            
        Returns:
            DuplicateResult: Çoğaltma sonucu
        """
        result = DuplicateResult(success=False)
        result.source_paths = [source]
        
        try:
            if not os.path.exists(source):
                result.errors.append(f"Source not found: {source}")
                return result
            
            if not os.path.isdir(source):
                result.errors.append(f"Source is not a directory: {source}")
                return result
            
            # Generate destination path
            destination = self._generate_duplicate_path(source)
            
            # Calculate size
            size = self._calculate_directory_size(source)
            
            # Duplicate directory
            if self.config.preserve_metadata:
                shutil.copytree(source, destination, copy_function=shutil.copy2)
            else:
                shutil.copytree(source, destination, copy_function=shutil.copy)
            
            # Add to history
            self.duplicate_history.append({
                "source": source,
                "destination": destination,
                "mode": self.config.mode.value,
                "timestamp": datetime.now().isoformat(),
                "deleted": False
            })
            
            result.success = True
            result.duplicated_count = 1
            result.duplicated_size = size
            result.destination_paths = [destination]
            result.message = f"Directory duplicated: {source} -> {destination}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def duplicate_multiple(self, targets: List[DuplicateTarget]) -> DuplicateResult:
        """
        Toplu çoğalt.
        
        Args:
            targets: Çoğaltma hedefleri
            
        Returns:
            DuplicateResult: Çoğaltma sonucu
        """
        result = DuplicateResult(success=False)
        
        try:
            duplicated_count = 0
            duplicated_size = 0
            source_paths = []
            destination_paths = []
            
            for target in targets:
                source_paths.append(target.source)
                
                if target.is_directory:
                    sub_result = self.duplicate_directory(target.source)
                else:
                    sub_result = self.duplicate_file(target.source)
                
                if sub_result.success:
                    duplicated_count += sub_result.duplicated_count
                    duplicated_size += sub_result.duplicated_size
                    destination_paths.extend(sub_result.destination_paths)
                else:
                    result.errors.extend(sub_result.errors)
            
            result.success = duplicated_count > 0
            result.duplicated_count = duplicated_count
            result.duplicated_size = duplicated_size
            result.source_paths = source_paths
            result.destination_paths = destination_paths
            result.message = f"Duplicated {duplicated_count} items"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def _generate_duplicate_path(self, source: str) -> str:
        """
        Çoğaltma yolu oluştur.
        
        Args:
            source: Kaynak yol
            
        Returns:
            str: Çoğaltma yolu
        """
        directory = os.path.dirname(source)
        filename = os.path.basename(source)
        name, ext = os.path.splitext(filename)
        
        if self.config.mode == DuplicateMode.NUMBERED:
            counter = 1
            while True:
                new_name = f"{name} ({counter}){ext}"
                new_path = os.path.join(directory, new_name)
                if not os.path.exists(new_path):
                    return new_path
                counter += 1
        
        elif self.config.mode == DuplicateMode.TIMESTAMP:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            new_name = f"{name}_{timestamp}{ext}"
            return os.path.join(directory, new_name)
        
        elif self.config.mode == DuplicateMode.CUSTOM_SUFFIX:
            new_name = f"{name}{self.config.custom_suffix}{ext}"
            return os.path.join(directory, new_name)
        
        elif self.config.mode == DuplicateMode.COPY_SUFFIX:
            new_name = f"{name} - Copy{ext}"
            return os.path.join(directory, new_name)
        
        return source
    
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
    
    def undo_duplicate(self, destination: str) -> DuplicateResult:
        """
        Çoğaltmayı geri al.
        
        Args:
            destination: Hedef yol
            
        Returns:
            DuplicateResult: Geri alma sonucu
        """
        result = DuplicateResult(success=False)
        
        try:
            # Find in history
            for item in reversed(self.duplicate_history):
                if item["destination"] == destination and not item["deleted"]:
                    # Delete the duplicated file/directory
                    if os.path.isfile(destination):
                        os.remove(destination)
                    elif os.path.isdir(destination):
                        shutil.rmtree(destination)
                    
                    item["deleted"] = True
                    result.success = True
                    result.message = f"File deleted: {destination}"
                    return result
            
            result.errors.append("Duplicate history not found")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_duplicate_history(self) -> List[Dict[str, Any]]:
        """
        Çoğaltma geçmişini al.
        
        Returns:
            List[Dict[str, Any]]: Geçmiş
        """
        return self.duplicate_history
    
    def clear_history(self) -> DuplicateResult:
        """
        Geçmişi temizle.
        
        Returns:
            DuplicateResult: Temizleme sonucu
        """
        result = DuplicateResult(success=False)
        
        try:
            self.duplicate_history.clear()
            result.success = True
            result.message = "Duplicate history cleared"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def update_config(self, config: DuplicateConfig) -> DuplicateResult:
        """
        Konfigürasyon güncelle.
        
        Args:
            config: Yeni konfigürasyon
            
        Returns:
            DuplicateResult: Güncelleme sonucu
        """
        result = DuplicateResult(success=False)
        
        try:
            self.config = config
            result.success = True
            result.message = "Config updated"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_config(self) -> DuplicateConfig:
        """
        Konfigürasyon al.
        
        Returns:
            DuplicateConfig: Konfigürasyon
        """
        return self.config
    
    def can_duplicate(self, source: str) -> bool:
        """
        Çoğaltılabilir mi?
        
        Args:
            source: Kaynak yol
            
        Returns:
            bool: Çoğaltılabilir mi
        """
        try:
            if not os.path.exists(source):
                return False
            
            # Check permissions
            if not os.access(source, os.R_OK):
                return False
            
            # Check directory permissions
            directory = os.path.dirname(source)
            if directory and not os.access(directory, os.W_OK):
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
    engine = FileDuplicateEngine()
    
    result = engine.can_duplicate("test.txt")
    print(f"Can duplicate: {result}")
