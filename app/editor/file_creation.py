"""
MuhammedAI Local Developer - File Creation
File creation engine for code editor.
"""

from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from enum import Enum
import os
from datetime import datetime


class FileType(Enum):
    """File type."""
    TEXT = "text"
    CODE = "code"
    MARKDOWN = "markdown"
    JSON = "json"
    XML = "xml"
    HTML = "html"
    CSS = "css"
    JAVASCRIPT = "javascript"
    PYTHON = "python"
    BINARY = "binary"


class CreateMode(Enum):
    """Create mode."""
    EMPTY = "empty"
    TEMPLATE = "template"
    COPY = "copy"
    FROM_CONTENT = "from_content"


@dataclass
class FileTemplate:
    """File template."""
    name: str
    content: str
    file_type: FileType


@dataclass
class CreateConfig:
    """Create configuration."""
    mode: CreateMode = CreateMode.EMPTY
    file_type: FileType = FileType.TEXT
    encoding: str = "utf-8"
    line_ending: str = "\n"
    add_newline_at_end: bool = True
    create_parent_directories: bool = True
    show_notification: bool = True


@dataclass
class CreateResult:
    """Create result."""
    success: bool
    message: Optional[str] = None
    errors: List[str] = field(default_factory=list)
    created_path: Optional[str] = None
    created_count: int = 0


class FileCreationEngine:
    """
    File creation engine.
    
    Özellikler:
    - Create empty files
    - Create from template
    - Create from content
    - Create from copy
    - Create directories
    - Create parent directories
    - File type detection
    - Encoding support
    - Line ending support
    - Template management
    - Create history
    - Undo support
    - Permission check
    - Smart detection
    """
    
    def __init__(self, config: Optional[CreateConfig] = None):
        """Initialize file creation engine."""
        self.config = config or CreateConfig()
        self.create_history: List[Dict[str, Any]] = []
        self.templates: Dict[str, FileTemplate] = self._init_templates()
    
    def _init_templates(self) -> Dict[str, FileTemplate]:
        """
        Şablonları başlat.
        
        Returns:
            Dict[str, FileTemplate]: Şablonlar
        """
        return {
            "python": FileTemplate(
                name="Python",
                content='"""\nPython file template.\n"""\n',
                file_type=FileType.PYTHON
            ),
            "javascript": FileTemplate(
                name="JavaScript",
                content="// JavaScript file template\n",
                file_type=FileType.JAVASCRIPT
            ),
            "html": FileTemplate(
                name="HTML",
                content='<!DOCTYPE html>\n<html>\n<head>\n    <title></title>\n</head>\n<body>\n</body>\n</html>\n',
                file_type=FileType.HTML
            ),
            "css": FileTemplate(
                name="CSS",
                content="/* CSS file template */\n",
                file_type=FileType.CSS
            ),
            "json": FileTemplate(
                name="JSON",
                content='{\n    \n}\n',
                file_type=FileType.JSON
            ),
            "markdown": FileTemplate(
                name="Markdown",
                content="# Title\n\n",
                file_type=FileType.MARKDOWN
            )
        }
    
    def create_file(self, path: str, content: Optional[str] = None, template_name: Optional[str] = None) -> CreateResult:
        """
        Dosya oluştur.
        
        Args:
            path: Dosya yolu
            content: İçerik
            template_name: Şablon adı
            
        Returns:
            CreateResult: Oluşturma sonucu
        """
        result = CreateResult(success=False)
        
        try:
            if os.path.exists(path):
                result.errors.append(f"File already exists: {path}")
                return result
            
            # Create parent directories if needed
            parent_dir = os.path.dirname(path)
            if parent_dir and self.config.create_parent_directories:
                os.makedirs(parent_dir, exist_ok=True)
            
            # Determine content based on mode
            if self.config.mode == CreateMode.EMPTY:
                final_content = ""
            elif self.config.mode == CreateMode.TEMPLATE and template_name:
                final_content = self._get_template_content(template_name)
            elif self.config.mode == CreateMode.FROM_CONTENT and content:
                final_content = content
            elif self.config.mode == CreateMode.COPY and content:
                # Copy from source file
                if os.path.exists(content):
                    with open(content, 'r', encoding=self.config.encoding) as f:
                        final_content = f.read()
                else:
                    result.errors.append(f"Source file not found: {content}")
                    return result
            else:
                final_content = ""
            
            # Add newline at end if configured
            if self.config.add_newline_at_end and final_content and not final_content.endswith(self.config.line_ending):
                final_content += self.config.line_ending
            
            # Write file
            with open(path, 'w', encoding=self.config.encoding, newline='') as f:
                f.write(final_content)
            
            # Add to history
            self.create_history.append({
                "path": path,
                "mode": self.config.mode.value,
                "timestamp": datetime.now().isoformat(),
                "deleted": False
            })
            
            result.success = True
            result.created_path = path
            result.created_count = 1
            result.message = f"File created: {path}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def create_directory(self, path: str) -> CreateResult:
        """
        Dizin oluştur.
        
        Args:
            path: Dizin yolu
            
        Returns:
            CreateResult: Oluşturma sonucu
        """
        result = CreateResult(success=False)
        
        try:
            if os.path.exists(path):
                result.errors.append(f"Directory already exists: {path}")
                return result
            
            os.makedirs(path, exist_ok=True)
            
            # Add to history
            self.create_history.append({
                "path": path,
                "mode": "directory",
                "timestamp": datetime.now().isoformat(),
                "deleted": False
            })
            
            result.success = True
            result.created_path = path
            result.created_count = 1
            result.message = f"Directory created: {path}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def create_multiple(self, paths: List[str], contents: Optional[List[str]] = None) -> CreateResult:
        """
        Toplu oluştur.
        
        Args:
            paths: Dosya yolları
            contents: İçerikler
            
        Returns:
            CreateResult: Oluşturma sonucu
        """
        result = CreateResult(success=False)
        
        try:
            created_count = 0
            created_path = None
            
            for i, path in enumerate(paths):
                content = contents[i] if contents and i < len(contents) else None
                sub_result = self.create_file(path, content)
                
                if sub_result.success:
                    created_count += 1
                    created_path = sub_result.created_path
                else:
                    result.errors.extend(sub_result.errors)
            
            result.success = created_count > 0
            result.created_count = created_count
            result.created_path = created_path
            result.message = f"Created {created_count} files"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def _get_template_content(self, template_name: str) -> str:
        """
        Şablon içeriğini al.
        
        Args:
            template_name: Şablon adı
            
        Returns:
            str: Şablon içeriği
        """
        template = self.templates.get(template_name)
        if template:
            return template.content
        return ""
    
    def add_template(self, name: str, content: str, file_type: FileType) -> CreateResult:
        """
        Şablon ekle.
        
        Args:
            name: Şablon adı
            content: İçerik
            file_type: Dosya tipi
            
        Returns:
            CreateResult: Ekleme sonucu
        """
        result = CreateResult(success=False)
        
        try:
            self.templates[name] = FileTemplate(
                name=name,
                content=content,
                file_type=file_type
            )
            
            result.success = True
            result.message = f"Template added: {name}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def remove_template(self, name: str) -> CreateResult:
        """
        Şablon kaldır.
        
        Args:
            name: Şablon adı
            
        Returns:
            CreateResult: Kaldırma sonucu
        """
        result = CreateResult(success=False)
        
        try:
            if name in self.templates:
                del self.templates[name]
                result.success = True
                result.message = f"Template removed: {name}"
            else:
                result.errors.append(f"Template not found: {name}")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_template(self, name: str) -> Optional[FileTemplate]:
        """
        Şablon al.
        
        Args:
            name: Şablon adı
            
        Returns:
            Optional[FileTemplate]: Şablon
        """
        return self.templates.get(name)
    
    def get_all_templates(self) -> Dict[str, FileTemplate]:
        """
        Tüm şablonları al.
        
        Returns:
            Dict[str, FileTemplate]: Şablonlar
        """
        return self.templates
    
    def undo_create(self, path: str) -> CreateResult:
        """
        Oluşturmayı geri al.
        
        Args:
            path: Dosya yolu
            
        Returns:
            CreateResult: Geri alma sonucu
        """
        result = CreateResult(success=False)
        
        try:
            # Find in history
            for item in reversed(self.create_history):
                if item["path"] == path and not item["deleted"]:
                    # Delete the file/directory
                    if os.path.isfile(path):
                        os.remove(path)
                    elif os.path.isdir(path):
                        import shutil
                        shutil.rmtree(path)
                    
                    item["deleted"] = True
                    result.success = True
                    result.message = f"File deleted: {path}"
                    return result
            
            result.errors.append("Create history not found")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_create_history(self) -> List[Dict[str, Any]]:
        """
        Oluşturma geçmişini al.
        
        Returns:
            List[Dict[str, Any]]: Geçmiş
        """
        return self.create_history
    
    def clear_history(self) -> CreateResult:
        """
        Geçmişi temizle.
        
        Returns:
            CreateResult: Temizleme sonucu
        """
        result = CreateResult(success=False)
        
        try:
            self.create_history.clear()
            result.success = True
            result.message = "Create history cleared"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def update_config(self, config: CreateConfig) -> CreateResult:
        """
        Konfigürasyon güncelle.
        
        Args:
            config: Yeni konfigürasyon
            
        Returns:
            CreateResult: Güncelleme sonucu
        """
        result = CreateResult(success=False)
        
        try:
            self.config = config
            result.success = True
            result.message = "Config updated"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_config(self) -> CreateConfig:
        """
        Konfigürasyon al.
        
        Returns:
            CreateConfig: Konfigürasyon
        """
        return self.config
    
    def can_create(self, path: str) -> bool:
        """
        Oluşturulabilir mi?
        
        Args:
            path: Dosya yolu
            
        Returns:
            bool: Oluşturulabilir mi
        """
        try:
            if os.path.exists(path):
                return False
            
            # Check parent directory permissions
            parent_dir = os.path.dirname(path)
            if parent_dir and not os.path.exists(parent_dir):
                return True  # Will create parent directories
            
            if parent_dir and not os.access(parent_dir, os.W_OK):
                return False
            
            return True
        
        except Exception:
            return False
    
    def detect_file_type(self, path: str) -> FileType:
        """
       -Dosya tipini tespit et.
        
        Args:
            path: Dosya yolu
            
        Returns:
            FileType: Dosya tipi
        """
        extension = os.path.splitext(path)[1].lower()
        
        type_map = {
            ".py": FileType.PYTHON,
            ".js": FileType.JAVASCRIPT,
            ".html": FileType.HTML,
            ".htm": FileType.HTML,
            ".css": FileType.CSS,
            ".json": FileType.JSON,
            ".xml": FileType.XML,
            ".md": FileType.MARKDOWN,
            ".txt": FileType.TEXT
        }
        
        return type_map.get(extension, FileType.TEXT)


if __name__ == "__main__":
    # Basit test
    engine = FileCreationEngine()
    
    result = engine.can_create("test.txt")
    print(f"Can create: {result}")
