"""
MuhammedAI Local Developer - File Open
File open engine for code editor.
"""

from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from enum import Enum
import os
from datetime import datetime


class OpenMode(Enum):
    """Open mode."""
    OPEN = "open"
    OPEN_RECENT = "open_recent"
    OPEN_WITH_ENCODING = "open_with_encoding"
    OPEN_READONLY = "open_readonly"


class Encoding(Enum):
    """Encoding."""
    UTF8 = "utf-8"
    UTF8_WITH_BOM = "utf-8-sig"
    UTF16 = "utf-16"
    UTF32 = "utf-32"
    ASCII = "ascii"
    LATIN1 = "latin-1"
    CP1252 = "cp1252"
    AUTO_DETECT = "auto_detect"


class LineEnding(Enum):
    """Line ending."""
    LF = "\n"
    CRLF = "\r\n"
    CR = "\r"
    AUTO_DETECT = "auto_detect"


@dataclass
class OpenConfig:
    """Open configuration."""
    mode: OpenMode = OpenMode.OPEN
    encoding: Encoding = Encoding.AUTO_DETECT
    line_ending: LineEnding = LineEnding.AUTO_DETECT
    readonly: bool = False
    detect_encoding: bool = True
    detect_line_ending: bool = True
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    show_notification: bool = True


@dataclass
class OpenResult:
    """Open result."""
    success: bool
    message: Optional[str] = None
    errors: List[str] = field(default_factory=list)
    content: Optional[str] = None
    path: Optional[str] = None
    encoding: Optional[str] = None
    line_ending: Optional[str] = None
    file_size: int = 0


class FileOpenEngine:
    """
    File open engine.
    
    Özellikler:
    - Open files
    - Open recent files
    - Open with encoding
    - Open readonly
    - Auto-detect encoding
    - Auto-detect line ending
    - File size check
    - Permission check
    - Open history
    - Recent files management
    - Smart detection
    """
    
    def __init__(self, config: Optional[OpenConfig] = None):
        """Initialize file open engine."""
        self.config = config or OpenConfig()
        self.open_history: List[Dict[str, Any]] = []
        self.recent_files: List[str] = []
        self.max_recent_files: int = 20
    
    def open_file(self, path: str) -> OpenResult:
        """
        Dosya aç.
        
        Args:
            path: Dosya yolu
            
        Returns:
            OpenResult: Açma sonucu
        """
        result = OpenResult(success=False)
        result.path = path
        
        try:
            # Check if file exists
            if not os.path.exists(path):
                result.errors.append(f"File not found: {path}")
                return result
            
            # Check if file is directory
            if os.path.isdir(path):
                result.errors.append(f"Path is a directory: {path}")
                return result
            
            # Check file size
            file_size = os.path.getsize(path)
            result.file_size = file_size
            
            if file_size > self.config.max_file_size:
                result.errors.append(f"File too large: {file_size} bytes (max: {self.config.max_file_size})")
                return result
            
            # Check permissions
            if not os.access(path, os.R_OK):
                result.errors.append(f"Permission denied: {path}")
                return result
            
            # Detect encoding
            encoding = self._detect_encoding(path)
            result.encoding = encoding
            
            # Read file
            with open(path, 'r', encoding=encoding) as f:
                content = f.read()
            
            # Detect line ending
            line_ending = self._detect_line_ending(content)
            result.line_ending = line_ending
            
            # Add to history
            self.open_history.append({
                "path": path,
                "encoding": encoding,
                "line_ending": line_ending,
                "readonly": self.config.readonly,
                "timestamp": datetime.now().isoformat()
            })
            
            # Add to recent files
            self._add_to_recent_files(path)
            
            result.success = True
            result.content = content
            result.message = f"File opened: {path}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def open_with_encoding(self, path: str, encoding: Encoding) -> OpenResult:
        """
        Belirli encoding ile aç.
        
        Args:
            path: Dosya yolu
            encoding: Encoding
            
        Returns:
            OpenResult: Açma sonucu
        """
        original_encoding = self.config.encoding
        self.config.encoding = encoding
        self.config.mode = OpenMode.OPEN_WITH_ENCODING
        
        result = self.open_file(path)
        
        self.config.encoding = original_encoding
        self.config.mode = OpenMode.OPEN
        
        if result.success:
            result.message = f"File opened with {encoding.value}: {path}"
        
        return result
    
    def open_readonly(self, path: str) -> OpenResult:
        """
    -Salt okunur aç.
        
        Args:
            path: Dosya yolu
            
        Returns:
            OpenResult: Açma sonucu
        """
        original_readonly = self.config.readonly
        self.config.readonly = True
        self.config.mode = OpenMode.OPEN_READONLY
        
        result = self.open_file(path)
        
        self.config.readonly = original_readonly
        self.config.mode = OpenMode.OPEN
        
        if result.success:
            result.message = f"File opened readonly: {path}"
        
        return result
    
    def open_recent(self, index: int) -> OpenResult:
        """
        Son dosyadan aç.
        
        Args:
            index: İndex
            
        Returns:
            OpenResult: Açma sonucu
        """
        result = OpenResult(success=False)
        
        try:
            if index < 0 or index >= len(self.recent_files):
                result.errors.append(f"Invalid index: {index}")
                return result
            
            path = self.recent_files[index]
            self.config.mode = OpenMode.OPEN_RECENT
            
            result = self.open_file(path)
            
            if result.success:
                result.message = f"Recent file opened: {path}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def _detect_encoding(self, path: str) -> str:
        """
        Encoding tespit et.
        
        Args:
            path: Dosya yolu
            
        Returns:
            str: Encoding
        """
        if not self.config.detect_encoding or self.config.encoding != Encoding.AUTO_DETECT:
            return self.config.encoding.value
        
        try:
            # Try UTF-8 first
            with open(path, 'r', encoding='utf-8') as f:
                f.read()
            return 'utf-8'
        except UnicodeDecodeError:
            try:
                # Try UTF-8 with BOM
                with open(path, 'r', encoding='utf-8-sig') as f:
                    f.read()
                return 'utf-8-sig'
            except UnicodeDecodeError:
                try:
                    # Try Latin-1
                    with open(path, 'r', encoding='latin-1') as f:
                        f.read()
                    return 'latin-1'
                except UnicodeDecodeError:
                    # Fallback to cp1252
                    return 'cp1252'
        except Exception:
            return 'utf-8'
    
    def _detect_line_ending(self, content: str) -> str:
        """
        Line ending tespit et.
        
        Args:
            content: İçerik
            
        Returns:
            str: Line ending
        """
        if not self.config.detect_line_ending or self.config.line_ending != LineEnding.AUTO_DETECT:
            return self.config.line_ending.value
        
        # Count line endings
        crlf_count = content.count('\r\n')
        lf_count = content.count('\n') - crlf_count
        cr_count = content.count('\r') - crlf_count
        
        # Determine most common
        if crlf_count > lf_count and crlf_count > cr_count:
            return '\r\n'
        elif lf_count > cr_count:
            return '\n'
        elif cr_count > 0:
            return '\r'
        else:
            return '\n'
    
    def _add_to_recent_files(self, path: str) -> None:
        """
        Son dosyalara ekle.
        
        Args:
            path: Dosya yolu
        """
        if path in self.recent_files:
            self.recent_files.remove(path)
        self.recent_files.insert(0, path)
        if len(self.recent_files) > self.max_recent_files:
            self.recent_files.pop()
    
    def get_recent_files(self) -> List[str]:
        """
        Son dosyaları al.
        
        Returns:
            List[str]: Son dosya yolları
        """
        return self.recent_files
    
    def clear_recent_files(self) -> OpenResult:
        """
        Son dosyaları temizle.
        
        Returns:
            OpenResult: Temizleme sonucu
        """
        result = OpenResult(success=False)
        
        try:
            self.recent_files.clear()
            result.success = True
            result.message = "Recent files cleared"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_open_history(self) -> List[Dict[str, Any]]:
        """
        Açma geçmişini al.
        
        Returns:
            List[Dict[str, Any]]: Geçmiş
        """
        return self.open_history
    
    def clear_history(self) -> OpenResult:
        """
        Geçmişi temizle.
        
        Returns:
            OpenResult: Temizleme sonucu
        """
        result = OpenResult(success=False)
        
        try:
            self.open_history.clear()
            result.success = True
            result.message = "Open history cleared"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def can_open(self, path: str) -> bool:
        """
        Açılabilir mi?
        
        Args:
            path: Dosya yolu
            
        Returns:
            bool: Açılabilir mi
        """
        try:
            if not os.path.exists(path):
                return False
            
            if os.path.isdir(path):
                return False
            
            if not os.access(path, os.R_OK):
                return False
            
            file_size = os.path.getsize(path)
            if file_size > self.config.max_file_size:
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
            if os.path.exists(path) and os.path.isfile(path):
                return os.path.getsize(path)
            return 0
        except Exception:
            return 0
    
    def update_config(self, config: OpenConfig) -> OpenResult:
        """
        Konfigürasyon güncelle.
        
        Args:
            config: Yeni konfigürasyon
            
        Returns:
            OpenResult: Güncelleme sonucu
        """
        result = OpenResult(success=False)
        
        try:
            self.config = config
            result.success = True
            result.message = "Config updated"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_config(self) -> OpenConfig:
        """
        Konfigürasyon al.
        
        Returns:
            OpenConfig: Konfigürasyon
        """
        return self.config


if __name__ == "__main__":
    # Basit test
    engine = FileOpenEngine()
    
    result = engine.can_open("test.txt")
    print(f"Can open: {result}")
