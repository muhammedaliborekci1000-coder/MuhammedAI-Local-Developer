"""
MuhammedAI Local Developer - Path Operations
Path operations engine for code editor.
"""

from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from enum import Enum
import os
from datetime import datetime


class PathSeparator(Enum):
    """Path separator."""
    FORWARD = "/"
    BACKWARD = "\\"
    AUTO = "auto"


class PathOperation(Enum):
    """Path operation."""
    JOIN = "join"
    NORMALIZE = "normalize"
    ABSOLUTE = "absolute"
    RELATIVE = "relative"
    BASENAME = "basename"
    DIRNAME = "dirname"
    EXTENSION = "extension"
    SPLIT = "split"
    VALIDATE = "validate"
    CONVERT = "convert"


@dataclass
class PathConfig:
    """Path configuration."""
    separator: PathSeparator = PathSeparator.AUTO
    normalize: bool = True
    show_notification: bool = True


@dataclass
class PathResult:
    """Path result."""
    success: bool
    message: Optional[str] = None
    errors: List[str] = field(default_factory=list)
    result: Optional[str] = None
    operation: Optional[str] = None


class PathOperationsEngine:
    """
    Path operations engine.
    
    Özellikler:
    - Join paths
    - Normalize paths
    - Get absolute path
    - Get relative path
    - Get basename
    - Get dirname
    - Get extension
    - Split path
    - Validate path
    - Convert separator
    - Path history
    - Smart detection
    """
    
    def __init__(self, config: Optional[PathConfig] = None):
        """Initialize path operations engine."""
        self.config = config or PathConfig()
        self.operation_history: List[Dict[str, Any]] = []
    
    def join_paths(self, *paths: str) -> PathResult:
        """
        Yolları birleştir.
        
        Args:
            *paths: Yollar
            
        Returns:
            PathResult: Birleştirme sonucu
        """
        result = PathResult(success=False)
        result.operation = PathOperation.JOIN.value
        
        try:
            joined = os.path.join(*paths)
            
            if self.config.normalize:
                joined = os.path.normpath(joined)
            
            # Add to history
            self.operation_history.append({
                "operation": "join",
                "paths": list(paths),
                "result": joined,
                "timestamp": self._get_timestamp()
            })
            
            result.success = True
            result.result = joined
            result.message = f"Paths joined: {joined}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def normalize_path(self, path: str) -> PathResult:
        """
        Yolu normalize et.
        
        Args:
            path: Yol
            
        Returns:
            PathResult: Normalizasyon sonucu
        """
        result = PathResult(success=False)
        result.operation = PathOperation.NORMALIZE.value
        
        try:
            normalized = os.path.normpath(path)
            
            # Add to history
            self.operation_history.append({
                "operation": "normalize",
                "path": path,
                "result": normalized,
                "timestamp": self._get_timestamp()
            })
            
            result.success = True
            result.result = normalized
            result.message = f"Path normalized: {normalized}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_absolute_path(self, path: str) -> PathResult:
        """
        Mutlak yolu al.
        
        Args:
            path: Yol
            
        Returns:
            PathResult: Mutlak yol sonucu
        """
        result = PathResult(success=False)
        result.operation = PathOperation.ABSOLUTE.value
        
        try:
            absolute = os.path.abspath(path)
            
            # Add to history
            self.operation_history.append({
                "operation": "absolute",
                "path": path,
                "result": absolute,
                "timestamp": self._get_timestamp()
            })
            
            result.success = True
            result.result = absolute
            result.message = f"Absolute path: {absolute}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_relative_path(self, path: str, start: str) -> PathResult:
        """
    - Göreli yolu al.
        
        Args:
            path: Yol
            start: Başlangıç yolu
            
        Returns:
            PathResult: Göreli yol sonucu
        """
        result = PathResult(success=False)
        result.operation = PathOperation.RELATIVE.value
        
        try:
            relative = os.path.relpath(path, start)
            
            # Add to history
            self.operation_history.append({
                "operation": "relative",
                "path": path,
                "start": start,
                "result": relative,
                "timestamp": self._get_timestamp()
            })
            
            result.success = True
            result.result = relative
            result.message = f"Relative path: {relative}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_basename(self, path: str) -> PathResult:
        """
        Dosya adını al.
        
        Args:
            path: Yol
            
        Returns:
            PathResult: Dosya adı sonucu
        """
        result = PathResult(success=False)
        result.operation = PathOperation.BASENAME.value
        
        try:
            basename = os.path.basename(path)
            
            # Add to history
            self.operation_history.append({
                "operation": "basename",
                "path": path,
                "result": basename,
                "timestamp": self._get_timestamp()
            })
            
            result.success = True
            result.result = basename
            result.message = f"Basename: {basename}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_dirname(self, path: str) -> PathResult:
        """
        Dizin adını al.
        
        Args:
            path: Yol
            
        Returns:
            PathResult: Dizin adı sonucu
        """
        result = PathResult(success=False)
        result.operation = PathOperation.DIRNAME.value
        
        try:
            dirname = os.path.dirname(path)
            
            # Add to history
            self.operation_history.append({
                "operation": "dirname",
                "path": path,
                "result": dirname,
                "timestamp": self._get_timestamp()
            })
            
            result.success = True
            result.result = dirname
            result.message = f"Dirname: {dirname}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_extension(self, path: str) -> PathResult:
        """
        Uzantıyı al.
        
        Args:
            path: Yol
            
        Returns:
            PathResult: Uzantı sonucu
        """
        result = PathResult(success=False)
        result.operation = PathOperation.EXTENSION.value
        
        try:
            _, extension = os.path.splitext(path)
            
            # Add to history
            self.operation_history.append({
                "operation": "extension",
                "path": path,
                "result": extension,
                "timestamp": self._get_timestamp()
            })
            
            result.success = True
            result.result = extension
            result.message = f"Extension: {extension}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def split_path(self, path: str) -> PathResult:
        """
        Yolu böl.
        
        Args:
            path: Yol
            
        Returns:
            PathResult: Bölme sonucu
        """
        result = PathResult(success=False)
        result.operation = PathOperation.SPLIT.value
        
        try:
            head, tail = os.path.split(path)
            split_result = f"head: {head}, tail: {tail}"
            
            # Add to history
            self.operation_history.append({
                "operation": "split",
                "path": path,
                "result": split_result,
                "timestamp": self._get_timestamp()
            })
            
            result.success = True
            result.result = split_result
            result.message = f"Path split: {split_result}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def validate_path(self, path: str) -> PathResult:
        """
        Yolu doğrula.
        
        Args:
            path: Yol
            
        Returns:
            PathResult: Doğrulama sonucu
        """
        result = PathResult(success=False)
        result.operation = PathOperation.VALIDATE.value
        
        try:
            is_valid = True
            errors = []
            
            # Check for invalid characters
            invalid_chars = '<>:"|?*'
            for char in invalid_chars:
                if char in path:
                    is_valid = False
                    errors.append(f"Invalid character: {char}")
            
            # Check for reserved names (Windows)
            reserved_names = ['CON', 'PRN', 'AUX', 'NUL', 'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9', 'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9']
            basename = os.path.basename(path).upper()
            if basename in reserved_names:
                is_valid = False
                errors.append(f"Reserved name: {basename}")
            
            # Add to history
            self.operation_history.append({
                "operation": "validate",
                "path": path,
                "result": is_valid,
                "errors": errors,
                "timestamp": self._get_timestamp()
            })
            
            result.success = True
            result.result = str(is_valid)
            result.message = f"Path valid: {is_valid}"
            if not is_valid:
                result.errors.extend(errors)
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def convert_separator(self, path: str, separator: PathSeparator) -> PathResult:
        """
        Ayırıcıyı dönüştür.
        
        Args:
            path: Yol
            separator: Ayırıcı
            
        Returns:
            PathResult: Dönüştürme sonucu
        """
        result = PathResult(success=False)
        result.operation = PathOperation.CONVERT.value
        
        try:
            converted = path
            
            if separator == PathSeparator.FORWARD:
                converted = path.replace("\\", "/")
            elif separator == PathSeparator.BACKWARD:
                converted = path.replace("/", "\\")
            elif separator == PathSeparator.AUTO:
                # Use system separator
                converted = path.replace("/", os.sep).replace("\\", os.sep)
            
            # Add to history
            self.operation_history.append({
                "operation": "convert",
                "path": path,
                "separator": separator.value,
                "result": converted,
                "timestamp": self._get_timestamp()
            })
            
            result.success = True
            result.result = converted
            result.message = f"Separator converted: {converted}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_operation_history(self) -> List[Dict[str, Any]]:
        """
        Operasyon geçmişini al.
        
        Returns:
            List[Dict[str, Any]]: Geçmiş
        """
        return self.operation_history
    
    def clear_history(self) -> PathResult:
        """
        Geçmişi temizle.
        
        Returns:
            PathResult: Temizleme sonucu
        """
        result = PathResult(success=False)
        
        try:
            self.operation_history.clear()
            result.success = True
            result.message = "Operation history cleared"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def update_config(self, config: PathConfig) -> PathResult:
        """
        Konfigürasyon güncelle.
        
        Args:
            config: Yeni konfigürasyon
            
        Returns:
            PathResult: Güncelleme sonucu
        """
        result = PathResult(success=False)
        
        try:
            self.config = config
            result.success = True
            result.message = "Config updated"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_config(self) -> PathConfig:
        """
        Konfigürasyon al.
        
        Returns:
            PathConfig: Konfigürasyon
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
    engine = PathOperationsEngine()
    
    print("Path Operations Engine initialized")
    print(f"Separator: {engine.config.separator.value}")
