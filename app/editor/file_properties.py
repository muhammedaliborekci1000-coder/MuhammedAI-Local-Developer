"""
MuhammedAI Local Developer - File Properties
File properties management engine for code editor.
"""

from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from enum import Enum
import os
from datetime import datetime


class PropertyType(Enum):
    """Property type."""
    BASIC = "basic"
    ADVANCED = "advanced"
    ALL = "all"


@dataclass
class FileProperties:
    """File properties."""
    path: str
    name: str = ""
    extension: str = ""
    size: int = 0
    size_human: str = ""
    is_file: bool = False
    is_directory: bool = False
    is_symlink: bool = False
    created_at: str = ""
    modified_at: str = ""
    accessed_at: str = ""
    permissions: str = ""
    owner: str = ""
    group: str = ""
    mime_type: str = ""
    encoding: str = ""
    line_count: int = 0
    word_count: int = 0
    character_count: int = 0


@dataclass
class PropertiesConfig:
    """Properties configuration."""
    include_advanced: bool = True
    calculate_stats: bool = True
    show_notification: bool = True


@dataclass
class PropertiesResult:
    """Properties result."""
    success: bool
    message: Optional[str] = None
    errors: List[str] = field(default_factory=list)
    properties: Optional[FileProperties] = None


class FilePropertiesEngine:
    """
    File properties management engine.
    
    Özellikler:
    - Get file properties
    - Get directory properties
    - Basic properties
    - Advanced properties
    - File statistics
    - Timestamps
    - Permissions
    - MIME type detection
    - Encoding detection
    - Properties history
    - Platform independent
    - Smart detection
    """
    
    def __init__(self, config: Optional[PropertiesConfig] = None):
        """Initialize file properties engine."""
        self.config = config or PropertiesConfig()
        self.properties_history: List[Dict[str, Any]] = []
    
    def get_properties(self, path: str, property_type: PropertyType = PropertyType.ALL) -> PropertiesResult:
        """
        Dosya özelliklerini al.
        
        Args:
            path: Dosya yolu
            property_type: Özellik tipi
            
        Returns:
            PropertiesResult: Özellik sonucu
        """
        result = PropertiesResult(success=False)
        
        try:
            if not os.path.exists(path):
                result.errors.append(f"Path not found: {path}")
                return result
            
            # Get properties
            properties = self._get_file_properties(path, property_type)
            
            # Add to history
            self.properties_history.append({
                "path": path,
                "property_type": property_type.value,
                "timestamp": self._get_timestamp()
            })
            
            result.success = True
            result.properties = properties
            result.message = f"Properties retrieved: {path}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def _get_file_properties(self, path: str, property_type: PropertyType) -> FileProperties:
        """
        Dosya özelliklerini al.
        
        Args:
            path: Dosya yolu
            property_type: Özellik tipi
            
        Returns:
            FileProperties: Dosya özellikleri
        """
        try:
            stat_info = os.stat(path)
            
            # Basic properties
            name = os.path.basename(path)
            extension = os.path.splitext(name)[1]
            size = stat_info.st_size
            size_human = self._format_size(size)
            is_file = os.path.isfile(path)
            is_directory = os.path.isdir(path)
            is_symlink = os.path.islink(path)
            
            # Timestamps
            created_at = datetime.fromtimestamp(stat_info.st_ctime).isoformat()
            modified_at = datetime.fromtimestamp(stat_info.st_mtime).isoformat()
            accessed_at = datetime.fromtimestamp(stat_info.st_atime).isoformat()
            
            # Permissions
            permissions = oct(stat_info.st_mode)[-3:]
            
            # Owner and group (Unix-like systems only)
            try:
                owner = str(stat_info.st_uid)
                group = str(stat_info.st_gid)
            except Exception:
                owner = ""
                group = ""
            
            # Advanced properties
            mime_type = ""
            encoding = ""
            line_count = 0
            word_count = 0
            character_count = 0
            
            if self.config.include_advanced or property_type == PropertyType.ADVANCED or property_type == PropertyType.ALL:
                if is_file:
                    # MIME type
                    mime_type = self._detect_mime_type(extension)
                    
                    # Encoding
                    encoding = self._detect_encoding(path)
                    
                    # Statistics
                    if self.config.calculate_stats:
                        line_count, word_count, character_count = self._calculate_stats(path)
            
            return FileProperties(
                path=path,
                name=name,
                extension=extension,
                size=size,
                size_human=size_human,
                is_file=is_file,
                is_directory=is_directory,
                is_symlink=is_symlink,
                created_at=created_at,
                modified_at=modified_at,
                accessed_at=accessed_at,
                permissions=permissions,
                owner=owner,
                group=group,
                mime_type=mime_type,
                encoding=encoding,
                line_count=line_count,
                word_count=word_count,
                character_count=character_count
            )
        except Exception:
            return FileProperties(path=path)
    
    def _format_size(self, size: int) -> str:
        """
        Boyutu formatla.
        
        Args:
            size: Boyut
            
        Returns:
            str: Formatlanmış boyut
        """
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f"{size:.2f} {unit}"
            size /= 1024.0
        return f"{size:.2f} PB"
    
    def _detect_mime_type(self, extension: str) -> str:
        """
        MIME tipi tespit et.
        
        Args:
            extension: Dosya uzantısı
            
        Returns:
            str: MIME tipi
        """
        mime_types = {
            '.txt': 'text/plain',
            '.py': 'text/x-python',
            '.js': 'text/javascript',
            '.html': 'text/html',
            '.css': 'text/css',
            '.json': 'application/json',
            '.xml': 'application/xml',
            '.pdf': 'application/pdf',
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.gif': 'image/gif',
            '.svg': 'image/svg+xml',
            '.mp3': 'audio/mpeg',
            '.mp4': 'video/mp4',
            '.zip': 'application/zip',
            '.tar': 'application/x-tar',
            '.gz': 'application/gzip',
        }
        
        return mime_types.get(extension.lower(), 'application/octet-stream')
    
    def _detect_encoding(self, path: str) -> str:
        """
        Encoding tespit et.
        
        Args:
            path: Dosya yolu
            
        Returns:
            str: Encoding
        """
        try:
            # Try UTF-8 first
            with open(path, 'r', encoding='utf-8') as f:
                f.read()
            return 'utf-8'
        except UnicodeDecodeError:
            try:
                # Try Latin-1
                with open(path, 'r', encoding='latin-1') as f:
                    f.read()
                return 'latin-1'
            except UnicodeDecodeError:
                return 'unknown'
        except Exception:
            return 'unknown'
    
    def _calculate_stats(self, path: str) -> Tuple[int, int, int]:
        """
        İstatistikleri hesapla.
        
        Args:
            path: Dosya yolu
            
        Returns:
            Tuple[int, int, int]: Satır, kelime, karakter sayısı
        """
        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            lines = content.splitlines()
            line_count = len(lines)
            word_count = len(content.split())
            character_count = len(content)
            
            return line_count, word_count, character_count
        except Exception:
            return 0, 0, 0
    
    def get_properties_history(self) -> List[Dict[str, Any]]:
        """
        Özellik geçmişini al.
        
        Returns:
            List[Dict[str, Any]]: Geçmiş
        """
        return self.properties_history
    
    def clear_history(self) -> PropertiesResult:
        """
        Geçmişi temizle.
        
        Returns:
            PropertiesResult: Temizleme sonucu
        """
        result = PropertiesResult(success=False)
        
        try:
            self.properties_history.clear()
            result.success = True
            result.message = "Properties history cleared"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def update_config(self, config: PropertiesConfig) -> PropertiesResult:
        """
        Konfigürasyon güncelle.
        
        Args:
            config: Yeni konfigürasyon
            
        Returns:
            PropertiesResult: Güncelleme sonucu
        """
        result = PropertiesResult(success=False)
        
        try:
            self.config = config
            result.success = True
            result.message = "Config updated"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_config(self) -> PropertiesConfig:
        """
        Konfigürasyon al.
        
        Returns:
            PropertiesConfig: Konfigürasyon
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
    engine = FilePropertiesEngine()
    
    print("File Properties Engine initialized")
    print(f"Include advanced: {engine.config.include_advanced}")
