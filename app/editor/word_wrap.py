"""
MuhammedAI Local Developer - Word Wrap
Word wrap engine for code editor.
"""

from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from enum import Enum


class WrapMode(Enum):
    """Wrap mode."""
    NONE = "none"
    WORD = "word"
    CHARACTER = "character"
    BOUNDARY = "boundary"


class WrapColumn(Enum):
    """Wrap column."""
    COLUMN_80 = 80
    COLUMN_100 = 100
    COLUMN_120 = 120
    CUSTOM = "custom"


@dataclass
class WrappedLine:
    """Wrapped line."""
    original_line: int
    wrapped_lines: List[str]
    wrap_positions: List[int]


@dataclass
class WordWrapConfig:
    """Word wrap configuration."""
    enabled: bool = True
    wrap_mode: WrapMode = WrapMode.WORD
    wrap_column: WrapColumn = WrapColumn.COLUMN_80
    custom_column: int = 80
    show_wrap_glyph: bool = True
    wrap_glyph: str = "↵"
    indent_wrapped_lines: bool = True
    preserve_indentation: bool = True
    break_long_words: bool = False
    visual_wrap: bool = True


@dataclass
class WordWrapResult:
    """Word wrap result."""
    success: bool
    wrapped_code: Optional[str] = None
    wrapped_lines: List[WrappedLine] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    message: Optional[str] = None


class WordWrapEngine:
    """
    Word wrap engine.
    
    Özellikler:
    - Word wrapping
    - Character wrapping
    - Boundary wrapping
    - Custom column width
    - Wrap glyph display
    - Indentation preservation
    - Visual wrapping
    - Long word breaking
    - Multi-line support
    - Wrap position tracking
    - Toggle wrap
    - Mode switching
    - Column configuration
    """
    
    def __init__(self, config: Optional[WordWrapConfig] = None):
        """Initialize word wrap engine."""
        self.config = config or WordWrapConfig()
        self.wrapped_lines: List[WrappedLine] = []
    
    def wrap_text(
        self,
        text: str,
        column: Optional[int] = None
    ) -> WordWrapResult:
        """
        Metni wrap et.
        
        Args:
            text: Metin
            column: Sütun genişliği
            
        Returns:
            WordWrapResult: Wrap sonucu
        """
        result = WordWrapResult(success=False)
        
        try:
            if not self.config.enabled:
                result.message = "Word wrap disabled"
                return result
            
            # Column belirle
            if column is None:
                if self.config.wrap_column == WrapColumn.CUSTOM:
                    column = self.config.custom_column
                else:
                    column = self.config.wrap_column.value
            
            lines = text.splitlines()
            wrapped_lines_list = []
            wrapped_result = []
            
            for line_idx, line in enumerate(lines):
                if len(line) <= column:
                    # Wrap gerekmiyor
                    wrapped_result.append(line)
                    wrapped_line = WrappedLine(
                        original_line=line_idx,
                        wrapped_lines=[line],
                        wrap_positions=[]
                    )
                    wrapped_lines_list.append(wrapped_line)
                else:
                    # Wrap yap
                    wrapped = self._wrap_line(line, column)
                    wrapped_result.extend(wrapped)
                    
                    wrap_positions = []
                    current_pos = 0
                    for i, w in enumerate(wrapped):
                        if i > 0:
                            wrap_positions.append(len(wrapped_result) - len(wrapped) + current_pos)
                        current_pos += len(w)
                    
                    wrapped_line = WrappedLine(
                        original_line=line_idx,
                        wrapped_lines=wrapped,
                        wrap_positions=wrap_positions
                    )
                    wrapped_lines_list.append(wrapped_line)
            
            self.wrapped_lines = wrapped_lines_list
            
            result.success = True
            result.wrapped_code = "\n".join(wrapped_result)
            result.wrapped_lines = wrapped_lines_list
            result.message = f"Wrapped {len(wrapped_lines_list)} lines"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def _wrap_line(self, line: str, column: int) -> List[str]:
        """
        Satırı wrap et.
        
        Args:
            line: Satır
            column: Sütun genişliği
            
        Returns:
            List[str]: Wrap edilmiş satırlar
        """
        if self.config.wrap_mode == WrapMode.NONE:
            return [line]
        
        if self.config.wrap_mode == WrapMode.CHARACTER:
            return self._wrap_character(line, column)
        
        if self.config.wrap_mode == WrapMode.WORD:
            return self._wrap_word(line, column)
        
        if self.config.wrap_mode == WrapMode.BOUNDARY:
            return self._wrap_boundary(line, column)
        
        return [line]
    
    def _wrap_character(self, line: str, column: int) -> List[str]:
        """
        Karakter bazlı wrap.
        
        Args:
            line: Satır
            column: Sütun
            
        Returns:
            List[str]: Wrap edilmiş satırlar
        """
        wrapped = []
        indent = ""
        
        if self.config.preserve_indentation:
            indent = line[:len(line) - len(line.lstrip())]
        
        current = indent
        for char in line[len(indent):]:
            if len(current) >= column:
                wrapped.append(current)
                if self.config.indent_wrapped_lines:
                    current = indent + "    "
                else:
                    current = ""
            current += char
        
        if current:
            wrapped.append(current)
        
        return wrapped
    
    def _wrap_word(self, line: str, column: int) -> List[str]:
        """
        Kelime bazlı wrap.
        
        Args:
            line: Satır
            column: Sütun
            
        Returns:
            List[str]: Wrap edilmiş satırlar
        """
        words = line.split()
        wrapped = []
        indent = ""
        
        if self.config.preserve_indentation:
            indent = line[:len(line) - len(line.lstrip())]
        
        current = indent
        for word in words:
            if len(current) + len(word) + 1 > column:
                if current.strip():
                    wrapped.append(current)
                if self.config.indent_wrapped_lines:
                    current = indent + "    "
                else:
                    current = ""
            
            if current and not current.endswith(" "):
                current += " "
            current += word
        
        if current.strip():
            wrapped.append(current)
        
        return wrapped
    
    def _wrap_boundary(self, line: str, column: int) -> List[str]:
        """
        Boundary bazlı wrap (kelime veya karakter).
        
        Args:
            line: Satır
            column: Sütun
            
        Returns:
            List[str]: Wrap edilmiş satırlar
        """
        # Önce kelime wrap dene, uzun kelime varsa karakter wrap
        wrapped = self._wrap_word(line, column)
        
        # Uzun kelimeleri kontrol et
        if self.config.break_long_words:
            result = []
            for w in wrapped:
                if len(w) > column:
                    result.extend(self._wrap_character(w, column))
                else:
                    result.append(w)
            return result
        
        return wrapped
    
    def unwrap_text(self, text: str) -> WordWrapResult:
        """
        Metni unwrap et.
        
        Args:
            text: Wrap edilmiş metin
            
        Returns:
            WordWrapResult: Unwrap sonucu
        """
        result = WordWrapResult(success=False)
        
        try:
            # Wrap glyph'ları kaldır
            lines = text.splitlines()
            unwrapped = []
            
            for line in lines:
                # Wrap glyph'ı kaldır
                unwrapped_line = line.replace(self.config.wrap_glyph, "")
                unwrapped.append(unwrapped_line)
            
            result.success = True
            result.wrapped_code = "\n".join(unwrapped)
            result.message = "Text unwrapped"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def update_config(self, config: WordWrapConfig) -> WordWrapResult:
        """
        Konfigürasyon güncelle.
        
        Args:
            config: Yeni konfigürasyon
            
        Returns:
            WordWrapResult: Güncelleme sonucu
        """
        result = WordWrapResult(success=False)
        
        try:
            self.config = config
            result.success = True
            result.message = "Config updated"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_config(self) -> WordWrapConfig:
        """
        Konfigürasyon al.
        
        Returns:
            WordWrapConfig: Konfigürasyon
        """
        return self.config
    
    def toggle_wrap(self) -> WordWrapResult:
        """
        Wrap'ı aç/kapat.
        
        Returns:
            WordWrapResult: Toggle sonucu
        """
        result = WordWrapResult(success=False)
        
        try:
            self.config.enabled = not self.config.enabled
            result.success = True
            result.message = f"Word wrap {'enabled' if self.config.enabled else 'disabled'}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def set_wrap_mode(self, mode: WrapMode) -> WordWrapResult:
        """
        Wrap modu ayarla.
        
        Args:
            mode: Wrap modu
            
        Returns:
            WordWrapResult: Ayarlama sonucu
        """
        result = WordWrapResult(success=False)
        
        try:
            self.config.wrap_mode = mode
            result.success = True
            result.message = f"Wrap mode set to {mode.value}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def set_wrap_column(self, column: WrapColumn) -> WordWrapResult:
        """
        Wrap sütunu ayarla.
        
        Args:
            column: Wrap sütunu
            
        Returns:
            WordWrapResult: Ayarlama sonucu
        """
        result = WordWrapResult(success=False)
        
        try:
            self.config.wrap_column = column
            result.success = True
            result.message = f"Wrap column set to {column.value}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def set_custom_column(self, column: int) -> WordWrapResult:
        """
        Özel sütun ayarla.
        
        Args:
            column: Sütun genişliği
            
        Returns:
            WordWrapResult: Ayarlama sonucu
        """
        result = WordWrapResult(success=False)
        
        try:
            if column > 0:
                self.config.custom_column = column
                self.config.wrap_column = WrapColumn.CUSTOM
                result.success = True
                result.message = f"Custom column set to {column}"
            else:
                result.errors.append("Column must be positive")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_wrapped_lines(self) -> List[WrappedLine]:
        """
        Wrap edilmiş satırları al.
        
        Returns:
            List[WrappedLine]: Wrap edilmiş satırlar
        """
        return self.wrapped_lines


if __name__ == "__main__":
    # Basit test
    config = WordWrapConfig()
    engine = WordWrapEngine(config)
    
    text = "This is a very long line that should be wrapped at column 80 for better readability in the editor."
    result = engine.wrap_text(text, column=20)
    
    print(f"Wrapped: {result.success}")
    print(f"Result:\n{result.wrapped_code}")
