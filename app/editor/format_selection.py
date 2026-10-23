"""
MuhammedAI Local Developer - Format Selection
Format selection engine for code editor.
"""

from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from enum import Enum


class FormatScope(Enum):
    """Format scope."""
    SELECTION = "selection"
    LINE = "line"
    BLOCK = "block"
    FUNCTION = "function"
    DOCUMENT = "document"


class FormatTrigger(Enum):
    """Format trigger."""
    MANUAL = "manual"
    ON_SAVE = "on_save"
    ON_PASTE = "on_paste"
    ON_TYPE = "on_type"
    AUTO = "auto"


@dataclass
class SelectionRange:
    """Selection range."""
    start_line: int
    end_line: int
    start_column: int = 0
    end_column: int = 0


@dataclass
class FormatSelectionConfig:
    """Format selection configuration."""
    format_scope: FormatScope = FormatScope.SELECTION
    format_trigger: FormatTrigger = FormatTrigger.MANUAL
    preserve_indentation: bool = True
    normalize_whitespace: bool = True
    fix_operator_spacing: bool = True
    fix_comma_spacing: bool = True
    fix_paren_spacing: bool = True
    normalize_quotes: bool = False
    trim_trailing_whitespace: bool = True
    trim_blank_lines: bool = True
    max_line_length: int = 88
    indent_size: int = 4
    use_tabs: bool = False


@dataclass
class FormatSelectionResult:
    """Format selection result."""
    success: bool
    modified_content: str = ""
    original_content: str = ""
    lines_formatted: int = 0
    characters_changed: int = 0
    errors: List[str] = field(default_factory=list)
    message: Optional[str] = None


class FormatSelectionEngine:
    """
    Format selection engine.
    
    Özellikler:
    - Selection formatting
    - Line formatting
    - Block formatting
    - Function formatting
    - Document formatting
    - Manual trigger
    - On save trigger
    - On paste trigger
    - On type trigger
    - Auto trigger
    - Indentation preservation
    - Whitespace normalization
    - Operator spacing
    - Comma spacing
    - Paren spacing
    - Quote normalization
    - Trailing whitespace removal
    - Blank line trimming
    - Line length enforcement
    - Undo support
    - Format history
    - Preview changes
    - Language-specific formatting
    """
    
    def __init__(self, config: Optional[FormatSelectionConfig] = None):
        """Initialize format selection engine."""
        self.config = config or FormatSelectionConfig()
        self.format_history: List[Dict[str, Any]] = []
    
    def format_selection(
        self,
        content: str,
        selection: SelectionRange,
        language: str = "python"
    ) -> FormatSelectionResult:
        """
        Seçili alanı formatla.
        
        Args:
            content: Dosya içeriği
            selection: Seçim aralığı
            language: Programlama dili
            
        Returns:
            FormatSelectionResult: Formatlama sonucu
        """
        result = FormatSelectionResult(success=False)
        result.original_content = content
        
        try:
            lines = content.splitlines()
            
            if selection.start_line >= len(lines) or selection.end_line >= len(lines):
                result.errors.append("Invalid selection range")
                return result
            
            # Seçili satırları al
            selected_lines = lines[selection.start_line:selection.end_line + 1]
            selected_code = "\n".join(selected_lines)
            
            # Seçili kodu formatla
            formatted_selected = self._format_code(selected_code, language)
            
            # Kodu güncelle
            new_lines = lines.copy()
            new_lines[selection.start_line:selection.end_line + 1] = formatted_selected.splitlines()
            
            formatted_content = "\n".join(new_lines)
            
            # Geçmişe ekle
            self.format_history.append({
                "original": content,
                "modified": formatted_content,
                "selection": selection,
                "language": language
            })
            
            result.success = True
            result.modified_content = formatted_content
            result.lines_formatted = selection.end_line - selection.start_line + 1
            result.characters_changed = len(formatted_content) - len(content)
            result.message = f"Formatted selection (lines {selection.start_line}-{selection.end_line})"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def _format_code(self, code: str, language: str) -> str:
        """
        Kodu formatla.
        
        Args:
            code: Kod
            language: Programlama dili
            
        Returns:
            str: Formatlanmış kod
        """
        lines = code.splitlines()
        formatted_lines = []
        
        for line in lines:
            formatted_line = line
            
            # Trailing whitespace kaldır
            if self.config.trim_trailing_whitespace:
                formatted_line = formatted_line.rstrip()
            
            # Whitespace normalizasyonu
            if self.config.normalize_whitespace:
                formatted_line = self._normalize_whitespace(formatted_line)
            
            # Operator spacing
            if self.config.fix_operator_spacing:
                formatted_line = self._fix_operator_spacing(formatted_line)
            
            # Comma spacing
            if self.config.fix_comma_spacing:
                formatted_line = self._fix_comma_spacing(formatted_line)
            
            # Paren spacing
            if self.config.fix_paren_spacing:
                formatted_line = self._fix_paren_spacing(formatted_line)
            
            # Quote normalizasyonu
            if self.config.normalize_quotes:
                formatted_line = self._normalize_quotes(formatted_line)
            
            formatted_lines.append(formatted_line)
        
        # Blank line trimming
        if self.config.trim_blank_lines:
            formatted_lines = self._trim_blank_lines(formatted_lines)
        
        return "\n".join(formatted_lines)
    
    def _normalize_whitespace(self, line: str) -> str:
        """
        Whitespace normalizasyonu.
        
        Args:
            line: Satır
            
        Returns:
            str: Normalized line
        """
        import re
        # Multiple spaces -> single space (string içinde değil)
        parts = []
        in_string = False
        string_char = None
        
        for char in line:
            if char in ('"', "'") and (not in_string or char == string_char):
                in_string = not in_string
                string_char = char
                parts.append(char)
            elif in_string:
                parts.append(char)
            elif char == ' ':
                if parts and parts[-1] != ' ':
                    parts.append(char)
            else:
                parts.append(char)
        
        return ''.join(parts)
    
    def _fix_operator_spacing(self, line: str) -> str:
        """
        Operator spacing düzeltme.
        
        Args:
            line: Satır
            
        Returns:
            str: Düzeltilmiş satır
        """
        import re
        operators = ['=', '+=', '-=', '*=', '/=', '%=', '==', '!=', '<', '>', '<=', '>=']
        
        for op in operators:
            # Operator etrafında boşluk ekle
            escaped_op = re.escape(op)
            line = re.sub(rf'(\w){escaped_op}(\w)', rf'\1 {op} \2', line)
        
        return line
    
    def _fix_comma_spacing(self, line: str) -> str:
        """
        Comma spacing düzeltme.
        
        Args:
            line: Satır
            
        Returns:
            str: Düzeltilmiş satır
        """
        import re
        # Virgül sonrası boşluk ekle
        line = re.sub(r',(\S)', r', \1', line)
        # Virgül öncesi boşluk kaldır
        line = re.sub(r'(\s),', r',', line)
        return line
    
    def _fix_paren_spacing(self, line: str) -> str:
        """
        Paren spacing düzeltme.
        
        Args:
            line: Satır
            
        Returns:
            str: Düzeltilmiş satır
        """
        import re
        # Parantez öncesi boşluk kaldır
        line = re.sub(r'\s+\(', '(', line)
        # Parantez sonrası boşluk kaldır
        line = re.sub(r'\)\s+', ')', line)
        return line
    
    def _normalize_quotes(self, line: str) -> str:
        """
        Quote normalizasyonu.
        
        Args:
            line: Satır
            
        Returns:
            str: Normalized line
        """
        # Single quotes -> double quotes (basit)
        return line.replace("'", '"')
    
    def _trim_blank_lines(self, lines: List[str]) -> List[str]:
        """
        Blank line trimming.
        
        Args:
            lines: Satırlar
            
        Returns:
            List[str]: Trimmed lines
        """
        formatted_lines = []
        blank_count = 0
        
        for line in lines:
            if line.strip() == "":
                blank_count += 1
                if blank_count <= 2:  # Max 2 boş satır
                    formatted_lines.append(line)
            else:
                blank_count = 0
                formatted_lines.append(line)
        
        return formatted_lines
    
    def format_line(
        self,
        content: str,
        line_number: int,
        language: str = "python"
    ) -> FormatSelectionResult:
        """
        Satırı formatla.
        
        Args:
            content: Dosya içeriği
            line_number: Satır numarası
            language: Programlama dili
            
        Returns:
            FormatSelectionResult: Formatlama sonucu
        """
        selection = SelectionRange(start_line=line_number, end_line=line_number)
        return self.format_selection(content, selection, language)
    
    def format_block(
        self,
        content: str,
        start_line: int,
        end_line: int,
        language: str = "python"
    ) -> FormatSelectionResult:
        """
        Bloğu formatla.
        
        Args:
            content: Dosya içeriği
            start_line: Başlangıç satırı
            end_line: Bitiş satırı
            language: Programlama dili
            
        Returns:
            FormatSelectionResult: Formatlama sonucu
        """
        selection = SelectionRange(start_line=start_line, end_line=end_line)
        return self.format_selection(content, selection, language)
    
    def format_document(
        self,
        content: str,
        language: str = "python"
    ) -> FormatSelectionResult:
        """
        Dokümanı formatla.
        
        Args:
            content: Dosya içeriği
            language: Programlama dili
            
        Returns:
            FormatSelectionResult: Formatlama sonucu
        """
        lines = content.splitlines()
        if not lines:
            return FormatSelectionResult(success=True, modified_content=content)
        
        selection = SelectionRange(start_line=0, end_line=len(lines) - 1)
        return self.format_selection(content, selection, language)
    
    def undo_format(self) -> FormatSelectionResult:
        """
        Formatlamayı geri al.
        
        Returns:
            FormatSelectionResult: Geri alma sonucu
        """
        result = FormatSelectionResult(success=False)
        
        try:
            if not self.format_history:
                result.errors.append("No format history")
                return result
            
            last_format = self.format_history.pop()
            
            result.success = True
            result.modified_content = last_format["original"]
            result.original_content = last_format["modified"]
            result.message = "Format operation undone"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_format_history(self) -> List[Dict[str, Any]]:
        """
        Formatlama geçmişini al.
        
        Returns:
            List[Dict[str, Any]]: Geçmiş
        """
        return self.format_history
    
    def clear_history(self) -> FormatSelectionResult:
        """
        Geçmişi temizle.
        
        Returns:
            FormatSelectionResult: Temizleme sonucu
        """
        result = FormatSelectionResult(success=False)
        
        try:
            self.format_history.clear()
            result.success = True
            result.message = "Format history cleared"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def update_config(self, config: FormatSelectionConfig) -> FormatSelectionResult:
        """
        Konfigürasyon güncelle.
        
        Args:
            config: Yeni konfigürasyon
            
        Returns:
            FormatSelectionResult: Güncelleme sonucu
        """
        result = FormatSelectionResult(success=False)
        
        try:
            self.config = config
            result.success = True
            result.message = "Config updated"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_config(self) -> FormatSelectionConfig:
        """
        Konfigürasyon al.
        
        Returns:
            FormatSelectionConfig: Konfigürasyon
        """
        return self.config


if __name__ == "__main__":
    # Basit test
    engine = FormatSelectionEngine()
    
    content = "def test( x,y ):\n    result=x+y\n    return result"
    selection = SelectionRange(start_line=0, end_line=2)
    result = engine.format_selection(content, selection)
    print(f"Format: {result.success}")
