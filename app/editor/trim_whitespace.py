"""
MuhammedAI Local Developer - Trim Whitespace
Trim whitespace engine for code editor.
"""

from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from enum import Enum


class TrimScope(Enum):
    """Trim scope."""
    LINE = "line"
    SELECTION = "selection"
    DOCUMENT = "document"
    ALL_LINES = "all_lines"


class TrimMode(Enum):
    """Trim mode."""
    TRAILING = "trailing"
    LEADING = "leading"
    BOTH = "both"
    ALL = "all"


@dataclass
class TrimRange:
    """Trim range."""
    start_line: int
    end_line: int
    start_column: int = 0
    end_column: int = 0


@dataclass
class TrimConfig:
    """Trim configuration."""
    scope: TrimScope = TrimScope.DOCUMENT
    mode: TrimMode = TrimMode.TRAILING
    trim_empty_lines: bool = True
    preserve_blank_lines: bool = True
    max_blank_lines: int = 2
    trim_final_newline: bool = False
    normalize_line_endings: bool = True


@dataclass
class TrimResult:
    """Trim result."""
    success: bool
    modified_content: str = ""
    original_content: str = ""
    lines_trimmed: int = 0
    whitespace_removed: int = 0
    errors: List[str] = field(default_factory=list)
    message: Optional[str] = None


class TrimWhitespaceEngine:
    """
    Trim whitespace engine.
    
    Özellikler:
    - Trim trailing whitespace
    - Trim leading whitespace
    - Trim both leading and trailing
    - Trim all whitespace
    - Trim selection
    - Trim document
    - Trim line
    - Trim all lines
    - Empty line handling
    - Blank line preservation
    - Final newline handling
    - Line ending normalization
    - Undo support
    - Trim history
    - Smart detection
    - Whitespace counting
    """
    
    def __init__(self, config: Optional[TrimConfig] = None):
        """Initialize trim whitespace engine."""
        self.config = config or TrimConfig()
        self.trim_history: List[Dict[str, Any]] = []
    
    def trim_whitespace(
        self,
        content: str,
        trim_range: Optional[TrimRange] = None
    ) -> TrimResult:
        """
        Whitespace'i temizle.
        
        Args:
            content: Dosya içeriği
            trim_range: Temizleme aralığı
            
        Returns:
            TrimResult: Temizleme sonucu
        """
        result = TrimResult(success=False)
        result.original_content = content
        
        try:
            lines = content.splitlines()
            
            if self.config.scope == TrimScope.DOCUMENT:
                modified_lines = self._trim_document(lines)
            elif self.config.scope == TrimScope.SELECTION and trim_range:
                modified_lines = self._trim_selection(lines, trim_range)
            elif self.config.scope == TrimScope.LINE and trim_range:
                modified_lines = self._trim_line(lines, trim_range.start_line)
            elif self.config.scope == TrimScope.ALL_LINES:
                modified_lines = self._trim_all_lines(lines)
            else:
                modified_lines = self._trim_document(lines)
            
            # Line ending normalization
            if self.config.normalize_line_endings:
                modified_content = "\n".join(modified_lines)
            else:
                modified_content = "\n".join(modified_lines)
            
            # Final newline handling
            if not self.config.trim_final_newline and content.endswith("\n"):
                modified_content += "\n"
            
            # Whitespace removed count
            whitespace_removed = len(content) - len(modified_content)
            
            # Geçmişe ekle
            self.trim_history.append({
                "original": content,
                "modified": modified_content,
                "scope": self.config.scope.value,
                "mode": self.config.mode.value
            })
            
            result.success = True
            result.modified_content = modified_content
            result.lines_trimmed = len(lines)
            result.whitespace_removed = whitespace_removed
            result.message = f"Whitespace trimmed ({whitespace_removed} chars)"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def _trim_document(self, lines: List[str]) -> List[str]:
        """
        Dokümanı temizle.
        
        Args:
            lines: Satırlar
            
        Returns:
            List[str]: Temizlenmiş satırlar
        """
        modified_lines = []
        
        for line in lines:
            if self.config.mode == TrimMode.TRAILING:
                trimmed = line.rstrip()
            elif self.config.mode == TrimMode.LEADING:
                trimmed = line.lstrip()
            elif self.config.mode == TrimMode.BOTH:
                trimmed = line.strip()
            else:  # ALL
                trimmed = "".join(line.split())
            
            modified_lines.append(trimmed)
        
        # Blank line handling
        if self.config.preserve_blank_lines:
            modified_lines = self._preserve_blank_lines(modified_lines)
        
        # Empty line handling
        if self.config.trim_empty_lines:
            modified_lines = [line for line in modified_lines if line.strip() != ""]
        
        return modified_lines
    
    def _trim_selection(self, lines: List[str], trim_range: TrimRange) -> List[str]:
        """
        Seçimi temizle.
        
        Args:
            lines: Satırlar
            trim_range: Temizleme aralığı
            
        Returns:
            List[str]: Temizlenmiş satırlar
        """
        modified_lines = lines.copy()
        
        for i in range(trim_range.start_line, min(trim_range.end_line + 1, len(lines))):
            line = modified_lines[i]
            
            if self.config.mode == TrimMode.TRAILING:
                trimmed = line.rstrip()
            elif self.config.mode == TrimMode.LEADING:
                trimmed = line.lstrip()
            elif self.config.mode == TrimMode.BOTH:
                trimmed = line.strip()
            else:  # ALL
                trimmed = "".join(line.split())
            
            modified_lines[i] = trimmed
        
        return modified_lines
    
    def _trim_line(self, lines: List[str], line_number: int) -> List[str]:
        """
        Satırı temizle.
        
        Args:
            lines: Satırlar
            line_number: Satır numarası
            
        Returns:
            List[str]: Temizlenmiş satırlar
        """
        modified_lines = lines.copy()
        
        if line_number >= len(modified_lines):
            return modified_lines
        
        line = modified_lines[line_number]
        
        if self.config.mode == TrimMode.TRAILING:
            trimmed = line.rstrip()
        elif self.config.mode == TrimMode.LEADING:
            trimmed = line.lstrip()
        elif self.config.mode == TrimMode.BOTH:
            trimmed = line.strip()
        else:  # ALL
            trimmed = "".join(line.split())
        
        modified_lines[line_number] = trimmed
        
        return modified_lines
    
    def _trim_all_lines(self, lines: List[str]) -> List[str]:
        """
        Tüm satırları temizle.
        
        Args:
            lines: Satırlar
            
        Returns:
            List[str]: Temizlenmiş satırlar
        """
        return self._trim_document(lines)
    
    def _preserve_blank_lines(self, lines: List[str]) -> List[str]:
        """
        Boş satırları koru.
        
        Args:
            lines: Satırlar
            
        Returns:
            List[str]: İşlenmiş satırlar
        """
        max_blank = self.config.max_blank_lines
        result = []
        blank_count = 0
        
        for line in lines:
            if line.strip() == "":
                blank_count += 1
                if blank_count <= max_blank:
                    result.append(line)
            else:
                blank_count = 0
                result.append(line)
        
        return result
    
    def trim_trailing(self, content: str) -> TrimResult:
        """
        Trailing whitespace'i temizle.
        
        Args:
            content: Dosya içeriği
            
        Returns:
            TrimResult: Temizleme sonucu
        """
        original_mode = self.config.mode
        self.config.mode = TrimMode.TRAILING
        result = self.trim_whitespace(content)
        self.config.mode = original_mode
        return result
    
    def trim_leading(self, content: str) -> TrimResult:
        """
        Leading whitespace'i temizle.
        
        Args:
            content: Dosya içeriği
            
        Returns:
            TrimResult: Temizleme sonucu
        """
        original_mode = self.config.mode
        self.config.mode = TrimMode.LEADING
        result = self.trim_whitespace(content)
        self.config.mode = original_mode
        return result
    
    def trim_both(self, content: str) -> TrimResult:
        """
        Leading ve trailing whitespace'i temizle.
        
        Args:
            content: Dosya içeriği
            
        Returns:
            TrimResult: Temizleme sonucu
        """
        original_mode = self.config.mode
        self.config.mode = TrimMode.BOTH
        result = self.trim_whitespace(content)
        self.config.mode = original_mode
        return result
    
    def undo_trim(self) -> TrimResult:
        """
        Temizlemeyi geri al.
        
        Returns:
            TrimResult: Geri alma sonucu
        """
        result = TrimResult(success=False)
        
        try:
            if not self.trim_history:
                result.errors.append("No trim history")
                return result
            
            last_trim = self.trim_history.pop()
            
            result.success = True
            result.modified_content = last_trim["original"]
            result.original_content = last_trim["modified"]
            result.message = "Trim operation undone"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_trim_history(self) -> List[Dict[str, Any]]:
        """
        Temizleme geçmişini al.
        
        Returns:
            List[Dict[str, Any]]: Geçmiş
        """
        return self.trim_history
    
    def clear_history(self) -> TrimResult:
        """
        Geçmişi temizle.
        
        Returns:
            TrimResult: Temizleme sonucu
        """
        result = TrimResult(success=False)
        
        try:
            self.trim_history.clear()
            result.success = True
            result.message = "Trim history cleared"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def update_config(self, config: TrimConfig) -> TrimResult:
        """
        Konfigürasyon güncelle.
        
        Args:
            config: Yeni konfigürasyon
            
        Returns:
            TrimResult: Güncelleme sonucu
        """
        result = TrimResult(success=False)
        
        try:
            self.config = config
            result.success = True
            result.message = "Config updated"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_config(self) -> TrimConfig:
        """
        Konfigürasyon al.
        
        Returns:
            TrimConfig: Konfigürasyon
        """
        return self.config


if __name__ == "__main__":
    # Basit test
    engine = TrimWhitespaceEngine()
    
    content = "def test():\n    pass  \n    return  "
    result = engine.trim_whitespace(content)
    print(f"Trim: {result.success}")
