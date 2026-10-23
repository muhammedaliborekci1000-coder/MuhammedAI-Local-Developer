"""
MuhammedAI Local Developer - Convert Indentation
Convert indentation engine for code editor.
"""

from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from enum import Enum


class IndentationType(Enum):
    """Indentation type."""
    SPACES = "spaces"
    TABS = "tabs"


class ConvertScope(Enum):
    """Convert scope."""
    LINE = "line"
    SELECTION = "selection"
    DOCUMENT = "document"


@dataclass
class ConvertRange:
    """Convert range."""
    start_line: int
    end_line: int
    start_column: int = 0
    end_column: int = 0


@dataclass
class ConvertConfig:
    """Convert configuration."""
    target_type: IndentationType = IndentationType.SPACES
    tab_size: int = 4
    preserve_relative_indent: bool = True
    convert_leading_only: bool = True
    scope: ConvertScope = ConvertScope.DOCUMENT


@dataclass
class ConvertResult:
    """Convert result."""
    success: bool
    modified_content: str = ""
    original_content: str = ""
    lines_converted: int = 0
    tabs_converted: int = 0
    spaces_converted: int = 0
    errors: List[str] = field(default_factory=list)
    message: Optional[str] = None


class ConvertIndentationEngine:
    """
    Convert indentation engine.
    
    Özellikler:
    - Convert tabs to spaces
    - Convert spaces to tabs
    - Adjust tab size
    - Convert selection
    - Convert document
    - Convert line
    - Preserve relative indentation
    - Leading only conversion
    - Undo support
    - Convert history
    - Smart detection
    - Tab/space counting
    """
    
    def __init__(self, config: Optional[ConvertConfig] = None):
        """Initialize convert indentation engine."""
        self.config = config or ConvertConfig()
        self.convert_history: List[Dict[str, Any]] = []
    
    def convert_indentation(
        self,
        content: str,
        convert_range: Optional[ConvertRange] = None
    ) -> ConvertResult:
        """
        Indentation'ı dönüştür.
        
        Args:
            content: Dosya içeriği
            convert_range: Dönüştürme aralığı
            
        Returns:
            ConvertResult: Dönüştürme sonucu
        """
        result = ConvertResult(success=False)
        result.original_content = content
        
        try:
            lines = content.splitlines()
            
            if self.config.scope == ConvertScope.DOCUMENT:
                modified_lines = self._convert_document(lines)
            elif self.config.scope == ConvertScope.SELECTION and convert_range:
                modified_lines = self._convert_selection(lines, convert_range)
            elif self.config.scope == ConvertScope.LINE and convert_range:
                modified_lines = self._convert_line(lines, convert_range.start_line)
            else:
                modified_lines = self._convert_document(lines)
            
            modified_content = "\n".join(modified_lines)
            
            # Count conversions
            tabs_converted = content.count('\t') - modified_content.count('\t')
            spaces_converted = len(content) - len(modified_content) - tabs_converted
            
            # Geçmişe ekle
            self.convert_history.append({
                "original": content,
                "modified": modified_content,
                "target_type": self.config.target_type.value,
                "tab_size": self.config.tab_size
            })
            
            result.success = True
            result.modified_content = modified_content
            result.lines_converted = len(lines)
            result.tabs_converted = tabs_converted
            result.spaces_converted = spaces_converted
            result.message = f"Indentation converted to {self.config.target_type.value}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def _convert_document(self, lines: List[str]) -> List[str]:
        """
        Dokümanı dönüştür.
        
        Args:
            lines: Satırlar
            
        Returns:
            List[str]: Dönüştürülmüş satırlar
        """
        modified_lines = []
        
        for line in lines:
            if self.config.target_type == IndentationType.SPACES:
                modified = self._tabs_to_spaces(line)
            else:  # TABS
                modified = self._spaces_to_tabs(line)
            modified_lines.append(modified)
        
        return modified_lines
    
    def _convert_selection(self, lines: List[str], convert_range: ConvertRange) -> List[str]:
        """
        Seçimi dönüştür.
        
        Args:
            lines: Satırlar
            convert_range: Dönüştürme aralığı
            
        Returns:
            List[str]: Dönüştürülmüş satırlar
        """
        modified_lines = lines.copy()
        
        for i in range(convert_range.start_line, min(convert_range.end_line + 1, len(lines))):
            line = modified_lines[i]
            
            if self.config.target_type == IndentationType.SPACES:
                modified = self._tabs_to_spaces(line)
            else:  # TABS
                modified = self._spaces_to_tabs(line)
            
            modified_lines[i] = modified
        
        return modified_lines
    
    def _convert_line(self, lines: List[str], line_number: int) -> List[str]:
        """
        Satırı dönüştür.
        
        Args:
            lines: Satırlar
            line_number: Satır numarası
            
        Returns:
            List[str]: Dönüştürülmüş satırlar
        """
        modified_lines = lines.copy()
        
        if line_number >= len(modified_lines):
            return modified_lines
        
        line = modified_lines[line_number]
        
        if self.config.target_type == IndentationType.SPACES:
            modified = self._tabs_to_spaces(line)
        else:  # TABS
            modified = self._spaces_to_tabs(line)
        
        modified_lines[line_number] = modified
        
        return modified_lines
    
    def _tabs_to_spaces(self, line: str) -> str:
        """
        Tab'ları space'lere dönüştür.
        
        Args:
            line: Satır
            
        Returns:
            str: Dönüştürülmüş satır
        """
        if self.config.convert_leading_only:
            # Sadece leading tab'ları dönüştür
            leading_whitespace = line[:len(line) - len(line.lstrip())]
            rest_of_line = line[len(line) - len(line.lstrip()):]
            
            converted = leading_whitespace.replace('\t', ' ' * self.config.tab_size)
            return converted + rest_of_line
        else:
            # Tüm tab'ları dönüştür
            return line.replace('\t', ' ' * self.config.tab_size)
    
    def _spaces_to_tabs(self, line: str) -> str:
        """
        Space'leri tab'lara dönüştür.
        
        Args:
            line: Satır
            
        Returns:
            str: Dönüştürülmüş satır
        """
        if self.config.convert_leading_only:
            # Sadece leading space'leri dönüştür
            leading_whitespace = line[:len(line) - len(line.lstrip())]
            rest_of_line = line[len(line) - len(line.lstrip()):]
            
            # Space'leri tab'lere dönüştür
            converted = ""
            space_count = 0
            for char in leading_whitespace:
                if char == ' ':
                    space_count += 1
                    if space_count == self.config.tab_size:
                        converted += '\t'
                        space_count = 0
                else:
                    converted += char
                    space_count = 0
            
            # Kalan space'leri ekle
            if space_count > 0:
                converted += ' ' * space_count
            
            return converted + rest_of_line
        else:
            # Tüm space'leri dönüştür
            converted = ""
            space_count = 0
            for char in line:
                if char == ' ':
                    space_count += 1
                    if space_count == self.config.tab_size:
                        converted += '\t'
                        space_count = 0
                else:
                    converted += char
                    space_count = 0
            
            # Kalan space'leri ekle
            if space_count > 0:
                converted += ' ' * space_count
            
            return converted
    
    def convert_tabs_to_spaces(self, content: str) -> ConvertResult:
        """
        Tab'ları space'lere dönüştür.
        
        Args:
            content: Dosya içeriği
            
        Returns:
            ConvertResult: Dönüştürme sonucu
        """
        original_type = self.config.target_type
        self.config.target_type = IndentationType.SPACES
        result = self.convert_indentation(content)
        self.config.target_type = original_type
        return result
    
    def convert_spaces_to_tabs(self, content: str) -> ConvertResult:
        """
        Space'leri tab'lara dönüştür.
        
        Args:
            content: Dosya içeriği
            
        Returns:
            ConvertResult: Dönüştürme sonucu
        """
        original_type = self.config.target_type
        self.config.target_type = IndentationType.TABS
        result = self.convert_indentation(content)
        self.config.target_type = original_type
        return result
    
    def set_tab_size(self, tab_size: int) -> ConvertResult:
        """
        Tab boyutu ayarla.
        
        Args:
            tab_size: Tab boyutu
            
        Returns:
            ConvertResult: Ayarlama sonucu
        """
        result = ConvertResult(success=False)
        
        try:
            if tab_size > 0:
                self.config.tab_size = tab_size
                result.success = True
                result.message = f"Tab size set to {tab_size}"
            else:
                result.errors.append("Tab size must be positive")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def undo_convert(self) -> ConvertResult:
        """
        Dönüştürmeyi geri al.
        
        Returns:
            ConvertResult: Geri alma sonucu
        """
        result = ConvertResult(success=False)
        
        try:
            if not self.convert_history:
                result.errors.append("No convert history")
                return result
            
            last_convert = self.convert_history.pop()
            
            result.success = True
            result.modified_content = last_convert["original"]
            result.original_content = last_convert["modified"]
            result.message = "Convert operation undone"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_convert_history(self) -> List[Dict[str, Any]]:
        """
        Dönüştürme geçmişini al.
        
        Returns:
            List[Dict[str, Any]]: Geçmiş
        """
        return self.convert_history
    
    def clear_history(self) -> ConvertResult:
        """
        Geçmişi temizle.
        
        Returns:
            ConvertResult: Temizleme sonucu
        """
        result = ConvertResult(success=False)
        
        try:
            self.convert_history.clear()
            result.success = True
            result.message = "Convert history cleared"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def update_config(self, config: ConvertConfig) -> ConvertResult:
        """
        Konfigürasyon güncelle.
        
        Args:
            config: Yeni konfigürasyon
            
        Returns:
            ConvertResult: Güncelleme sonucu
        """
        result = ConvertResult(success=False)
        
        try:
            self.config = config
            result.success = True
            result.message = "Config updated"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_config(self) -> ConvertConfig:
        """
        Konfigürasyon al.
        
        Returns:
            ConvertConfig: Konfigürasyon
        """
        return self.config


if __name__ == "__main__":
    # Basit test
    engine = ConvertIndentationEngine()
    
    content = "def test():\n\tpass\n\treturn"
    result = engine.convert_tabs_to_spaces(content)
    print(f"Convert: {result.success}")
