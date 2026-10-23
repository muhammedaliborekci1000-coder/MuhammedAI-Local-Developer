"""
MuhammedAI Local Developer - Join Lines
Join lines engine for code editor.
"""

from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from enum import Enum


class JoinMode(Enum):
    """Join mode."""
    SPACE = "space"
    NO_SPACE = "no_space"
    NEWLINE = "newline"
    SEMICOLON = "semicolon"
    COMMA = "comma"


class JoinScope(Enum):
    """Join scope."""
    LINE = "line"
    SELECTION = "selection"
    DOCUMENT = "document"


@dataclass
class JoinRange:
    """Join range."""
    start_line: int
    end_line: int
    start_column: int = 0
    end_column: int = 0


@dataclass
class JoinConfig:
    """Join configuration."""
    mode: JoinMode = JoinMode.SPACE
    scope: JoinScope = JoinScope.SELECTION
    trim_whitespace: bool = True
    preserve_indentation: bool = False
    remove_blank_lines: bool = True
    smart_join: bool = True


@dataclass
class JoinResult:
    """Join result."""
    success: bool
    modified_content: str = ""
    original_content: str = ""
    lines_joined: int = 0
    characters_added: int = 0
    errors: List[str] = field(default_factory=list)
    message: Optional[str] = None


class JoinLinesEngine:
    """
    Join lines engine.
    
    Özellikler:
    - Join lines with space
    - Join lines without space
    - Join lines with newline
    - Join lines with semicolon
    - Join lines with comma
    - Join selection
    - Join document
    - Join line
    - Trim whitespace
    - Preserve indentation
    - Remove blank lines
    - Smart join
    - Undo support
    - Join history
    - Smart detection
    """
    
    def __init__(self, config: Optional[JoinConfig] = None):
        """Initialize join lines engine."""
        self.config = config or JoinConfig()
        self.join_history: List[Dict[str, Any]] = []
    
    def join_lines(
        self,
        content: str,
        join_range: Optional[JoinRange] = None
    ) -> JoinResult:
        """
        Satırları birleştir.
        
        Args:
            content: Dosya içeriği
            join_range: Birleştirme aralığı
            
        Returns:
            JoinResult: Birleştirme sonucu
        """
        result = JoinResult(success=False)
        result.original_content = content
        
        try:
            lines = content.splitlines()
            
            if self.config.scope == JoinScope.DOCUMENT:
                modified_content = self._join_document(lines)
            elif self.config.scope == JoinScope.SELECTION and join_range:
                modified_content = self._join_selection(lines, join_range)
            elif self.config.scope == JoinScope.LINE and join_range:
                modified_content = self._join_line(lines, join_range.start_line)
            else:
                modified_content = self._join_document(lines)
            
            # Count characters added
            characters_added = len(modified_content) - len(content)
            
            # Geçmişe ekle
            self.join_history.append({
                "original": content,
                "modified": modified_content,
                "mode": self.config.mode.value,
                "scope": self.config.scope.value
            })
            
            result.success = True
            result.modified_content = modified_content
            result.lines_joined = len(lines)
            result.characters_added = characters_added
            result.message = f"Lines joined ({characters_added} chars added)"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def _join_document(self, lines: List[str]) -> str:
        """
        Dokümanı birleştir.
        
        Args:
            lines: Satırlar
            
        Returns:
            str: Birleştirilmiş içerik
        """
        separator = self._get_separator()
        joined_lines = []
        
        for line in lines:
            if self.config.trim_whitespace:
                line = line.strip()
            
            if line or not self.config.remove_blank_lines:
                joined_lines.append(line)
        
        return separator.join(joined_lines)
    
    def _join_selection(self, lines: List[str], join_range: JoinRange) -> str:
        """
        Seçimi birleştir.
        
        Args:
            lines: Satırlar
            join_range: Birleştirme aralığı
            
        Returns:
            str: Birleştirilmiş içerik
        """
        separator = self._get_separator()
        modified_lines = lines.copy()
        
        # Get lines to join
        lines_to_join = []
        for i in range(join_range.start_line, min(join_range.end_line + 1, len(lines))):
            line = lines[i]
            if self.config.trim_whitespace:
                line = line.strip()
            lines_to_join.append(line)
        
        # Join lines
        joined = separator.join(lines_to_join)
        
        # Replace lines with joined line
        modified_lines[join_range.start_line:join_range.end_line + 1] = [joined]
        
        return "\n".join(modified_lines)
    
    def _join_line(self, lines: List[str], line_number: int) -> str:
        """
        Satırı birleştir.
        
        Args:
            lines: Satırlar
            line_number: Satır numarası
            
        Returns:
            str: Birleştirilmiş içerik
        """
        if line_number >= len(lines) - 1:
            return "\n".join(lines)
        
        separator = self._get_separator()
        modified_lines = lines.copy()
        
        # Join current line with next line
        current_line = lines[line_number]
        next_line = lines[line_number + 1]
        
        if self.config.trim_whitespace:
            current_line = current_line.strip()
            next_line = next_line.strip()
        
        joined = f"{current_line}{separator}{next_line}"
        
        # Replace two lines with one
        modified_lines[line_number:line_number + 2] = [joined]
        
        return "\n".join(modified_lines)
    
    def _get_separator(self) -> str:
        """
        Ayırıcı al.
        
        Returns:
            str: Ayırıcı
        """
        if self.config.mode == JoinMode.SPACE:
            return " "
        elif self.config.mode == JoinMode.NO_SPACE:
            return ""
        elif self.config.mode == JoinMode.NEWLINE:
            return "\n"
        elif self.config.mode == JoinMode.SEMICOLON:
            return "; "
        elif self.config.mode == JoinMode.COMMA:
            return ", "
        else:
            return " "
    
    def join_with_space(self, content: str, join_range: Optional[JoinRange] = None) -> JoinResult:
        """
        Space ile birleştir.
        
        Args:
            content: Dosya içeriği
            join_range: Birleştirme aralığı
            
        Returns:
            JoinResult: Birleştirme sonucu
        """
        original_mode = self.config.mode
        self.config.mode = JoinMode.SPACE
        result = self.join_lines(content, join_range)
        self.config.mode = original_mode
        return result
    
    def join_without_space(self, content: str, join_range: Optional[JoinRange] = None) -> JoinResult:
        """
        Space olmadan birleştir.
        
        Args:
            content: Dosya içeriği
            join_range: Birleştirme aralığı
            
        Returns:
            JoinResult: Birleştirme sonucu
        """
        original_mode = self.config.mode
        self.config.mode = JoinMode.NO_SPACE
        result = self.join_lines(content, join_range)
        self.config.mode = original_mode
        return result
    
    def join_with_semicolon(self, content: str, join_range: Optional[JoinRange] = None) -> JoinResult:
        """
        Semicolon ile birleştir.
        
        Args:
            content: Dosya içeriği
            join_range: Birleştirme aralığı
            
        Returns:
            JoinResult: Birleştirme sonucu
        """
        original_mode = self.config.mode
        self.config.mode = JoinMode.SEMICOLON
        result = self.join_lines(content, join_range)
        self.config.mode = original_mode
        return result
    
    def join_with_comma(self, content: str, join_range: Optional[JoinRange] = None) -> JoinResult:
        """
        Virgül ile birleştir.
        
        Args:
            content: Dosya içeriği
            join_range: Birleştirme aralığı
            
        Returns:
            JoinResult: Birleştirme sonucu
        """
        original_mode = self.config.mode
        self.config.mode = JoinMode.COMMA
        result = self.join_lines(content, join_range)
        self.config.mode = original_mode
        return result
    
    def undo_join(self) -> JoinResult:
        """
        Birleştirmeyi geri al.
        
        Returns:
            JoinResult: Geri alma sonucu
        """
        result = JoinResult(success=False)
        
        try:
            if not self.join_history:
                result.errors.append("No join history")
                return result
            
            last_join = self.join_history.pop()
            
            result.success = True
            result.modified_content = last_join["original"]
            result.original_content = last_join["modified"]
            result.message = "Join operation undone"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_join_history(self) -> List[Dict[str, Any]]:
        """
        Birleştirme geçmişini al.
        
        Returns:
            List[Dict[str, Any]]: Geçmiş
        """
        return self.join_history
    
    def clear_history(self) -> JoinResult:
        """
        Geçmişi temizle.
        
        Returns:
            JoinResult: Temizleme sonucu
        """
        result = JoinResult(success=False)
        
        try:
            self.join_history.clear()
            result.success = True
            result.message = "Join history cleared"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def update_config(self, config: JoinConfig) -> JoinResult:
        """
        Konfigürasyon güncelle.
        
        Args:
            config: Yeni konfigürasyon
            
        Returns:
            JoinResult: Güncelleme sonucu
        """
        result = JoinResult(success=False)
        
        try:
            self.config = config
            result.success = True
            result.message = "Config updated"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_config(self) -> JoinConfig:
        """
        Konfigürasyon al.
        
        Returns:
            JoinConfig: Konfigürasyon
        """
        return self.config


if __name__ == "__main__":
    # Basit test
    engine = JoinLinesEngine()
    
    content = "line1\nline2\nline3"
    result = engine.join_lines(content)
    print(f"Join: {result.success}")
    print(f"Modified: {result.modified_content}")
