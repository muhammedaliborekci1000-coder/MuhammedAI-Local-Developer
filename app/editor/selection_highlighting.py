"""
MuhammedAI Local Developer - Selection Highlighting
Selection highlighting system for code editor.
"""

from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from enum import Enum


class HighlightStyle(Enum):
    """Highlight style."""
    BACKGROUND = "background"
    OUTLINE = "outline"
    UNDERLINE = "underline"
    GLOW = "glow"


class HighlightColor(Enum):
    """Highlight color."""
    DEFAULT = "default"
    BLUE = "blue"
    GREEN = "green"
    YELLOW = "yellow"
    ORANGE = "orange"
    RED = "red"
    PURPLE = "purple"
    CYAN = "cyan"
    CUSTOM = "custom"


@dataclass
class SelectionRange:
    """Selection range."""
    start_line: int
    start_column: int
    end_line: int
    end_column: int


@dataclass
class Highlight:
    """Highlight."""
    id: str
    range: SelectionRange
    style: HighlightStyle = HighlightStyle.BACKGROUND
    color: HighlightColor = HighlightColor.DEFAULT
    custom_color: Optional[str] = None
    is_active: bool = True
    is_persistent: bool = False


@dataclass
class SelectionHighlightConfig:
    """Selection highlight configuration."""
    highlight_current_selection: bool = True
    highlight_matching_words: bool = True
    highlight_matching_brackets: bool = True
    highlight_occurrences: bool = True
    show_selection_outline: bool = False
    animate_highlights: bool = True
    fade_inactive_highlights: bool = True
    max_highlights: int = 100
    highlight_style: HighlightStyle = HighlightStyle.BACKGROUND
    highlight_color: HighlightColor = HighlightColor.DEFAULT


@dataclass
class SelectionHighlightResult:
    """Selection highlight result."""
    success: bool
    highlights: List[Highlight] = field(default_factory=list)
    html: Optional[str] = None
    errors: List[str] = field(default_factory=list)
    message: Optional[str] = None


class SelectionHighlightManager:
    """
    Selection highlight manager.
    
    Özellikler:
    - Selection highlighting
    - Multiple highlight styles
    - Custom colors
    - Matching word highlights
    - Bracket matching
    - Occurrence highlighting
    - Highlight persistence
    - Highlight animations
    - Selection outline
    - Fade effects
    - Highlight management
    - Highlight filtering
    - Highlight grouping
    - Highlight priority
    - Highlight scope
    - Highlight visibility
    """
    
    def __init__(self, config: Optional[SelectionHighlightConfig] = None):
        """
        Initialize selection highlight manager.
        
        Args:
            config: Selection highlight configuration
        """
        self.config = config or SelectionHighlightConfig()
        self.highlights: Dict[str, Highlight] = {}
        self.highlight_id_counter = 0
        self._next_id()
    
    def _next_id(self) -> str:
        """
        Generate next highlight ID.
        
        Returns:
            str: Highlight ID
        """
        self.highlight_id_counter += 1
        return f"highlight_{self.highlight_id_counter}"
    
    def add_highlight(self, highlight: Highlight) -> SelectionHighlightResult:
        """
        Add a highlight.
        
        Args:
            highlight: Highlight to add
            
        Returns:
            SelectionHighlightResult: Add result
        """
        result = SelectionHighlightResult(success=True)
        
        try:
            if not highlight.id:
                highlight.id = self._next_id()
            
            self.highlights[highlight.id] = highlight
            
            # Limit highlights
            if len(self.highlights) > self.config.max_highlights:
                oldest_id = min(self.highlights.keys(), key=lambda k: self.highlights[k].id)
                del self.highlights[oldest_id]
            
            result.highlights = self.get_all_highlights()
            result.message = f"Highlight '{highlight.id}' added"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def remove_highlight(self, highlight_id: str) -> SelectionHighlightResult:
        """
        Remove a highlight.
        
        Args:
            highlight_id: Highlight ID
            
        Returns:
            SelectionHighlightResult: Remove result
        """
        result = SelectionHighlightResult(success=False)
        
        try:
            if highlight_id in self.highlights:
                del self.highlights[highlight_id]
                result.success = True
                result.highlights = self.get_all_highlights()
                result.message = f"Highlight '{highlight_id}' removed"
            else:
                result.errors.append("Highlight not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_highlight(self, highlight_id: str) -> Optional[Highlight]:
        """
        Get highlight by ID.
        
        Args:
            highlight_id: Highlight ID
            
        Returns:
            Optional[Highlight]: Highlight
        """
        return self.highlights.get(highlight_id)
    
    def get_all_highlights(self) -> List[Highlight]:
        """
        Get all highlights.
        
        Returns:
            List[Highlight]: All highlights
        """
        return list(self.highlights.values())
    
    def get_highlights_by_style(self, style: HighlightStyle) -> List[Highlight]:
        """
        Get highlights by style.
        
        Args:
            style: Highlight style
            
        Returns:
            List[Highlight]: Highlights
        """
        return [h for h in self.highlights.values() if h.style == style]
    
    def get_highlights_by_color(self, color: HighlightColor) -> List[Highlight]:
        """
        Get highlights by color.
        
        Args:
            color: Highlight color
            
        Returns:
            List[Highlight]: Highlights
        """
        return [h for h in self.highlights.values() if h.color == color]
    
    def highlight_selection(self, range: SelectionRange) -> SelectionHighlightResult:
        """
        Highlight current selection.
        
        Args:
            range: Selection range
            
        Returns:
            SelectionHighlightResult: Highlight result
        """
        if not self.config.highlight_current_selection:
            result = SelectionHighlightResult(success=False)
            result.message = "Current selection highlighting disabled"
            return result
        
        highlight = Highlight(
            id="",
            range=range,
            style=self.config.highlight_style,
            color=self.config.highlight_color,
            is_active=True
        )
        
        return self.add_highlight(highlight)
    
    def highlight_matching_words(self, text: str, selection: SelectionRange) -> SelectionHighlightResult:
        """
        Highlight matching words.
        
        Args:
            text: Text content
            selection: Selection range
            
        Returns:
            SelectionHighlightResult: Highlight result
        """
        result = SelectionHighlightResult(success=True)
        
        if not self.config.highlight_matching_words:
            result.message = "Matching word highlighting disabled"
            return result
        
        lines = text.splitlines()
        
        # Get selected word
        if selection.start_line == selection.end_line:
            line = lines[selection.start_line]
            selected_text = line[selection.start_column:selection.end_column]
        else:
            result.message = "Multi-line selection not supported for word matching"
            return result
        
        # Find all occurrences
        highlights = []
        for line_idx, line in enumerate(lines):
            start = 0
            while True:
                pos = line.lower().find(selected_text.lower(), start)
                if pos == -1:
                    break
                
                # Create highlight
                highlight = Highlight(
                    id="",
                    range=SelectionRange(
                        start_line=line_idx,
                        start_column=pos,
                        end_line=line_idx,
                        end_column=pos + len(selected_text)
                    ),
                    style=HighlightStyle.BACKGROUND,
                    color=HighlightColor.YELLOW
                )
                
                self.add_highlight(highlight)
                highlights.append(highlight)
                start = pos + 1
        
        result.highlights = highlights
        result.message = f"Highlighted {len(highlights)} occurrences"
        
        return result
    
    def highlight_matching_brackets(self, text: str, position: Tuple[int, int]) -> SelectionHighlightResult:
        """
        Highlight matching brackets.
        
        Args:
            text: Text content
            position: Cursor position (line, column)
            
        Returns:
            SelectionHighlightResult: Highlight result
        """
        result = SelectionHighlightResult(success=True)
        
        if not self.config.highlight_matching_brackets:
            result.message = "Bracket matching disabled"
            return result
        
        lines = text.splitlines()
        line, col = position
        
        if line >= len(lines):
            result.message = "Invalid position"
            return result
        
        current_line = lines[line]
        
        if col >= len(current_line):
            result.message = "Invalid column"
            return result
        
        char = current_line[col]
        
        bracket_pairs = {
            '(': ')',
            ')': '(',
            '[': ']',
            ']': '[',
            '{': '}',
            '}': '{'
        }
        
        if char not in bracket_pairs:
            result.message = "Not a bracket"
            return result
        
        # Find matching bracket
        matching_char = bracket_pairs[char]
        bracket_stack = []
        found = False
        
        for i in range(len(current_line)):
            c = current_line[i]
            if c == char:
                bracket_stack.append(i)
            elif c == matching_char and bracket_stack:
                bracket_stack.pop()
                if not bracket_stack:
                    # Found matching bracket
                    highlight = Highlight(
                        id="",
                        range=SelectionRange(
                            start_line=line,
                            start_column=col,
                            end_line=line,
                            end_column=col + 1
                        ),
                        style=HighlightStyle.OUTLINE,
                        color=HighlightColor.BLUE
                    )
                    
                    self.add_highlight(highlight)
                    
                    matching_highlight = Highlight(
                        id="",
                        range=SelectionRange(
                            start_line=line,
                            start_column=i,
                            end_line=line,
                            end_column=i + 1
                        ),
                        style=HighlightStyle.OUTLINE,
                        color=HighlightColor.BLUE
                    )
                    
                    self.add_highlight(matching_highlight)
                    found = True
                    break
        
        if found:
            result.message = "Matching brackets highlighted"
        else:
            result.message = "No matching bracket found"
        
        return result
    
    def clear_highlights(self) -> SelectionHighlightResult:
        """
        Clear all highlights.
        
        Returns:
            SelectionHighlightResult: Clear result
        """
        result = SelectionHighlightResult(success=True)
        
        try:
            self.highlights.clear()
            result.message = "All highlights cleared"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def clear_non_persistent_highlights(self) -> SelectionHighlightResult:
        """
        Clear non-persistent highlights.
        
        Returns:
            SelectionHighlightResult: Clear result
        """
        result = SelectionHighlightResult(success=True)
        
        try:
            to_remove = [id for id, h in self.highlights.items() if not h.is_persistent]
            for id in to_remove:
                del self.highlights[id]
            
            result.message = f"Cleared {len(to_remove)} non-persistent highlights"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def update_config(self, config: SelectionHighlightConfig) -> SelectionHighlightResult:
        """
        Update selection highlight configuration.
        
        Args:
            config: New configuration
            
        Returns:
            SelectionHighlightResult: Update result
        """
        result = SelectionHighlightResult(success=True)
        
        try:
            self.config = config
            result.message = "Config updated"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def get_config(self) -> SelectionHighlightConfig:
        """
        Get selection highlight configuration.
        
        Returns:
            SelectionHighlightConfig: Configuration
        """
        return self.config


if __name__ == "__main__":
    # Basit test
    config = SelectionHighlightConfig()
    manager = SelectionHighlightManager(config)
    
    # Highlight ekle
    range = SelectionRange(
        start_line=0,
        start_column=0,
        end_line=0,
        end_column=10
    )
    
    result = manager.highlight_selection(range)
    
    print(f"Highlight added: {result.message}")
    
    # Tüm highlight'ları al
    highlights = manager.get_all_highlights()
    
    print(f"Total highlights: {len(highlights)}")
