"""
MuhammedAI Local Developer - Diff Highlighter
Diff highlighter engine for code editor.
"""

from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from enum import Enum


class HighlightType(Enum):
    """Highlight type."""
    ADDED = "added"
    REMOVED = "removed"
    MODIFIED = "modified"
    UNCHANGED = "unchanged"
    CONTEXT = "context"
    HEADER = "header"
    KEYWORD = "keyword"
    STRING = "string"
    COMMENT = "comment"
    FUNCTION = "function"
    VARIABLE = "variable"
    NUMBER = "number"
    OPERATOR = "operator"


class HighlightStyle(Enum):
    """Highlight style."""
    BACKGROUND = "background"
    FOREGROUND = "foreground"
    BORDER = "border"
    UNDERLINE = "underline"
    BOLD = "bold"
    ITALIC = "italic"


class HighlightScope(Enum):
    """Highlight scope."""
    LINE = "line"
    WORD = "word"
    CHARACTER = "character"
    BLOCK = "block"


@dataclass
class ColorScheme:
    """Color scheme."""
    added_bg: str = "#d4edda"
    added_fg: str = "#155724"
    removed_bg: str = "#f8d7da"
    removed_fg: str = "#721c24"
    modified_bg: str = "#fff3cd"
    modified_fg: str = "#856404"
    unchanged_bg: str = "#ffffff"
    unchanged_fg: str = "#000000"
    context_bg: str = "#f8f9fa"
    context_fg: str = "#6c757d"
    header_bg: str = "#e9ecef"
    header_fg: str = "#495057"


@dataclass
class HighlightRange:
    """Highlight range."""
    start: int
    end: int
    highlight_type: HighlightType
    style: HighlightStyle = HighlightStyle.BACKGROUND


@dataclass
class HighlightedLine:
    """Highlighted line."""
    line_number: int
    content: str
    line_type: str
    highlights: List[HighlightRange] = field(default_factory=list)
    background_color: Optional[str] = None
    foreground_color: Optional[str] = None


@dataclass
class HighlighterConfig:
    """Highlighter configuration."""
    enable_syntax_highlighting: bool = True
    enable_diff_coloring: bool = True
    enable_line_highlighting: bool = True
    enable_word_highlighting: bool = True
    enable_change_highlighting: bool = True
    color_scheme: ColorScheme = field(default_factory=ColorScheme)
    highlight_keywords: bool = True
    highlight_strings: bool = True
    highlight_comments: bool = True
    highlight_functions: bool = True
    highlight_variables: bool = True
    highlight_numbers: bool = True
    highlight_operators: bool = True
    case_sensitive: bool = True


@dataclass
class HighlighterResult:
    """Highlighter result."""
    success: bool
    action: Optional[str] = None
    message: Optional[str] = None
    errors: List[str] = field(default_factory=list)
    highlighted_lines: List[HighlightedLine] = field(default_factory=list)
    total_lines: int = 0
    total_highlights: int = 0


class DiffHighlighterEngine:
    """
    Diff highlighter engine.
    
    Özellikler:
    - Syntax highlighting
    - Diff coloring
    - Line highlighting
    - Word highlighting
    - Change highlighting
    - Custom color schemes
    - Multiple highlight styles
    - Multiple highlight scopes
    - Keyword highlighting
    - String highlighting
    - Comment highlighting
    - Function highlighting
    - Variable highlighting
    - Number highlighting
    - Operator highlighting
    - Case sensitivity
    - Configuration management
    - Highlight statistics
    - Highlight history
    """
    
    def __init__(self, config: Optional[HighlighterConfig] = None):
        """Initialize diff highlighter engine."""
        self.config = config or HighlighterConfig()
        self.highlighted_lines: List[HighlightedLine] = []
        self.highlighter_history: List[Tuple[str, str]] = []  # (action, target)
        
        # Python keywords
        self.keywords = {
            "def", "class", "if", "else", "elif", "for", "while", "return",
            "import", "from", "as", "try", "except", "finally", "with",
            "True", "False", "None", "and", "or", "not", "in", "is",
            "lambda", "yield", "async", "await", "pass", "break", "continue",
            "global", "nonlocal", "assert", "del", "raise", "super"
        }
        
        # Python operators
        self.operators = {
            "+", "-", "*", "/", "//", "%", "**", "=", "==", "!=", "<", ">",
            "<=", ">=", "&", "|", "^", "~", "<<", ">>", "+=", "-=", "*=",
            "/=", "//=", "%=", "**=", "&=", "|=", "^=", "<<=", ">>=", "->"
        }
    
    def highlight_line(
        self,
        line: str,
        line_number: int,
        line_type: str = "unchanged"
    ) -> HighlighterResult:
        """
        Satırı highlight et.
        
        Args:
            line: Satır içeriği
            line_number: Satır numarası
            line_type: Satır tipi
            
        Returns:
            HighlighterResult: Highlight sonucu
        """
        result = HighlighterResult(success=False)
        result.action = "highlight_line"
        
        try:
            highlighted = HighlightedLine(
                line_number=line_number,
                content=line,
                line_type=line_type
            )
            
            # Diff coloring
            if self.config.enable_diff_coloring:
                self._apply_diff_coloring(highlighted, line_type)
            
            # Syntax highlighting
            if self.config.enable_syntax_highlighting:
                self._apply_syntax_highlighting(highlighted, line)
            
            # Word highlighting
            if self.config.enable_word_highlighting:
                self._apply_word_highlighting(highlighted, line)
            
            # Change highlighting
            if self.config.enable_change_highlighting:
                self._apply_change_highlighting(highlighted, line, line_type)
            
            self.highlighted_lines.append(highlighted)
            
            result.highlighted_lines = [highlighted]
            result.total_lines = 1
            result.total_highlights = len(highlighted.highlights)
            result.success = True
            result.message = f"Highlighted line {line_number}"
            
            self.highlighter_history.append(("highlight_line", str(line_number)))
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def highlight_lines(
        self,
        lines: List[str],
        line_types: Optional[List[str]] = None
    ) -> HighlighterResult:
        """
        Satırları highlight et.
        
        Args:
            lines: Satır listesi
            line_types: Satır tipleri
            
        Returns:
            HighlighterResult: Highlight sonucu
        """
        result = HighlighterResult(success=False)
        result.action = "highlight_lines"
        
        try:
            if line_types is None:
                line_types = ["unchanged"] * len(lines)
            
            self.highlighted_lines.clear()
            
            for i, (line, line_type) in enumerate(zip(lines, line_types)):
                line_result = self.highlight_line(line, i + 1, line_type)
                if not line_result.success:
                    result.errors.extend(line_result.errors)
            
            result.highlighted_lines = self.highlighted_lines
            result.total_lines = len(self.highlighted_lines)
            result.total_highlights = sum(len(l.highlights) for l in self.highlighted_lines)
            result.success = True
            result.message = f"Highlighted {len(lines)} lines"
            
            self.highlighter_history.append(("highlight_lines", str(len(lines))))
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def highlight_word(
        self,
        line: str,
        word: str,
        line_number: int,
        highlight_type: HighlightType = HighlightType.MODIFIED
    ) -> HighlighterResult:
        """
        Kelimeyi highlight et.
        
        Args:
            line: Satır içeriği
            word: Kelime
            line_number: Satır numarası
            highlight_type: Highlight tipi
            
        Returns:
            HighlighterResult: Highlight sonucu
        """
        result = HighlighterResult(success=False)
        result.action = "highlight_word"
        
        try:
            highlighted = HighlightedLine(
                line_number=line_number,
                content=line,
                line_type="unchanged"
            )
            
            # Kelimeyi bul ve highlight et
            start = 0
            while True:
                if self.config.case_sensitive:
                    index = line.lower().find(word.lower(), start)
                else:
                    index = line.find(word, start)
                
                if index == -1:
                    break
                
                highlight = HighlightRange(
                    start=index,
                    end=index + len(word),
                    highlight_type=highlight_type,
                    style=HighlightStyle.BACKGROUND
                )
                highlighted.highlights.append(highlight)
                start = index + len(word)
            
            result.highlighted_lines = [highlighted]
            result.total_lines = 1
            result.total_highlights = len(highlighted.highlights)
            result.success = True
            result.message = f"Highlighted word '{word}' in line {line_number}"
            
            self.highlighter_history.append(("highlight_word", word))
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def highlight_changes(
        self,
        old_line: str,
        new_line: str,
        line_number: int
    ) -> HighlighterResult:
        """
        Değişiklikleri highlight et.
        
        Args:
            old_line: Eski satır
            new_line: Yeni satır
            line_number: Satır numarası
            
        Returns:
            HighlighterResult: Highlight sonucu
        """
        result = HighlighterResult(success=False)
        result.action = "highlight_changes"
        
        try:
            highlighted = HighlightedLine(
                line_number=line_number,
                content=new_line,
                line_type="modified"
            )
            
            # Basit diff algoritması
            old_words = old_line.split()
            new_words = new_line.split()
            
            # Eklenen kelimeleri highlight et
            for word in new_words:
                if word not in old_words:
                    start = new_line.find(word)
                    if start != -1:
                        highlight = HighlightRange(
                            start=start,
                            end=start + len(word),
                            highlight_type=HighlightType.ADDED,
                            style=HighlightStyle.BACKGROUND
                        )
                        highlighted.highlights.append(highlight)
            
            # Silinen kelimeleri highlight et
            for word in old_words:
                if word not in new_words:
                    start = old_line.find(word)
                    if start != -1:
                        highlight = HighlightRange(
                            start=start,
                            end=start + len(word),
                            highlight_type=HighlightType.REMOVED,
                            style=HighlightStyle.BACKGROUND
                        )
                        highlighted.highlights.append(highlight)
            
            result.highlighted_lines = [highlighted]
            result.total_lines = 1
            result.total_highlights = len(highlighted.highlights)
            result.success = True
            result.message = f"Highlighted changes in line {line_number}"
            
            self.highlighter_history.append(("highlight_changes", str(line_number)))
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def set_color_scheme(self, scheme: ColorScheme) -> HighlighterResult:
        """
        Renk şemasını ayarla.
        
        Args:
            scheme: Renk şeması
            
        Returns:
            HighlighterResult: Ayarlama sonucu
        """
        result = HighlighterResult(success=False)
        result.action = "set_color_scheme"
        
        try:
            self.config.color_scheme = scheme
            result.success = True
            result.message = "Color scheme updated"
            
            self.highlighter_history.append(("set_color_scheme", "custom"))
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_highlighted_lines(self) -> List[HighlightedLine]:
        """
        Highlight edilmiş satırları al.
        
        Returns:
            List[HighlightedLine]: Satır listesi
        """
        return self.highlighted_lines
    
    def get_line_highlights(self, line_number: int) -> Optional[HighlightedLine]:
        """
        Satır highlightlarını al.
        
        Args:
            line_number: Satır numarası
            
        Returns:
            Optional[HighlightedLine]: Highlight bilgisi
        """
        for line in self.highlighted_lines:
            if line.line_number == line_number:
                return line
        return None
    
    def get_highlighter_history(self) -> List[Tuple[str, str]]:
        """
        Highlighter geçmişini al.
        
        Returns:
            List[Tuple[str, str]]: Geçmiş
        """
        return self.highlighter_history
    
    def clear_history(self) -> HighlighterResult:
        """
        Geçmişi temizle.
        
        Returns:
            HighlighterResult: Temizleme sonucu
        """
        result = HighlighterResult(success=False)
        
        try:
            self.highlighter_history.clear()
            result.success = True
            result.message = "Highlighter history cleared"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        İstatistikleri al.
        
        Returns:
            Dict[str, Any]: İstatistikler
        """
        total_highlights = sum(len(l.highlights) for l in self.highlighted_lines)
        
        highlight_types = {}
        for line in self.highlighted_lines:
            for highlight in line.highlights:
                htype = highlight.highlight_type.value
                highlight_types[htype] = highlight_types.get(htype, 0) + 1
        
        return {
            "total_lines": len(self.highlighted_lines),
            "total_highlights": total_highlights,
            "highlight_types": highlight_types
        }
    
    def update_config(self, config: HighlighterConfig) -> HighlighterResult:
        """
        Konfigürasyon güncelle.
        
        Args:
            config: Yeni konfigürasyon
            
        Returns:
            HighlighterResult: Güncelleme sonucu
        """
        result = HighlighterResult(success=False)
        
        try:
            self.config = config
            result.success = True
            result.message = "Config updated"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_config(self) -> HighlighterConfig:
        """
        Konfigürasyon al.
        
        Returns:
            HighlighterConfig: Konfigürasyon
        """
        return self.config
    
    def _apply_diff_coloring(self, line: HighlightedLine, line_type: str):
        """Diff coloring uygula."""
        scheme = self.config.color_scheme
        
        if line_type == "added":
            line.background_color = scheme.added_bg
            line.foreground_color = scheme.added_fg
        elif line_type == "removed":
            line.background_color = scheme.removed_bg
            line.foreground_color = scheme.removed_fg
        elif line_type == "modified":
            line.background_color = scheme.modified_bg
            line.foreground_color = scheme.modified_fg
        elif line_type == "context":
            line.background_color = scheme.context_bg
            line.foreground_color = scheme.context_fg
        elif line_type == "header":
            line.background_color = scheme.header_bg
            line.foreground_color = scheme.header_fg
        else:
            line.background_color = scheme.unchanged_bg
            line.foreground_color = scheme.unchanged_fg
    
    def _apply_syntax_highlighting(self, line: HighlightedLine, content: str):
        """Syntax highlighting uygula."""
        words = content.split()
        
        for i, word in enumerate(words):
            # Keywords
            if self.config.highlight_keywords and word in self.keywords:
                start = content.find(word)
                if start != -1:
                    line.highlights.append(HighlightRange(
                        start=start,
                        end=start + len(word),
                        highlight_type=HighlightType.KEYWORD,
                        style=HighlightStyle.FOREGROUND
                    ))
            
            # Strings
            if self.config.highlight_strings and ('"' in word or "'" in word):
                start = content.find(word)
                if start != -1:
                    line.highlights.append(HighlightRange(
                        start=start,
                        end=start + len(word),
                        highlight_type=HighlightType.STRING,
                        style=HighlightStyle.FOREGROUND
                    ))
            
            # Numbers
            if self.config.highlight_numbers and word.replace(".", "").replace("-", "").isdigit():
                start = content.find(word)
                if start != -1:
                    line.highlights.append(HighlightRange(
                        start=start,
                        end=start + len(word),
                        highlight_type=HighlightType.NUMBER,
                        style=HighlightStyle.FOREGROUND
                    ))
            
            # Operators
            if self.config.highlight_operators and word in self.operators:
                start = content.find(word)
                if start != -1:
                    line.highlights.append(HighlightRange(
                        start=start,
                        end=start + len(word),
                        highlight_type=HighlightType.OPERATOR,
                        style=HighlightStyle.FOREGROUND
                    ))
    
    def _apply_word_highlighting(self, line: HighlightedLine, content: str):
        """Word highlighting uygula."""
        # Kelime bazlı highlight (değişkenler, fonksiyonlar vb.)
        words = content.split()
        
        for word in words:
            if word.startswith("def ") or word.startswith("class "):
                start = content.find(word)
                if start != -1:
                    line.highlights.append(HighlightRange(
                        start=start,
                        end=start + len(word),
                        highlight_type=HighlightType.FUNCTION,
                        style=HighlightStyle.BOLD
                    ))
    
    def _apply_change_highlighting(self, line: HighlightedLine, content: str, line_type: str):
        """Change highlighting uygula."""
        if line_type in ["added", "removed", "modified"]:
            # Tüm satırı highlight et
            line.highlights.append(HighlightRange(
                start=0,
                end=len(content),
                highlight_type=HighlightType.MODIFIED if line_type == "modified" else HighlightType(line_type),
                style=HighlightStyle.BACKGROUND
            ))


if __name__ == "__main__":
    # Basit test
    engine = DiffHighlighterEngine()
    
    line = "def hello_world():"
    result = engine.highlight_line(line, 1, "added")
    
    print(f"Highlight line: {result.success}")
    print(f"Total highlights: {result.total_highlights}")
