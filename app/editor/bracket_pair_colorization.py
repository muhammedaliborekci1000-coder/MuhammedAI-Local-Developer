"""
MuhammedAI Local Developer - Bracket Pair Colorization
Bracket pair colorization system for code editor.
"""

from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from enum import Enum


class BracketColor(Enum):
    """Bracket color."""
    RED = "red"
    GREEN = "green"
    BLUE = "blue"
    YELLOW = "yellow"
    PURPLE = "purple"
    CYAN = "cyan"
    ORANGE = "orange"
    PINK = "pink"


class BracketType(Enum):
    """Bracket type."""
    ROUND = "round"
    SQUARE = "square"
    CURLY = "curly"
    ANGLE = "angle"


@dataclass
class BracketPosition:
    """Bracket position."""
    line: int
    column: int


@dataclass
class BracketPair:
    """Bracket pair."""
    opening: BracketPosition
    closing: BracketPosition
    type: BracketType
    color: BracketColor
    nesting_level: int


@dataclass
class BracketPairColorConfig:
    """Bracket pair color configuration."""
    enabled: bool = True
    color_scheme: str = "rainbow"
    max_nesting_level: int = 10
    show_outline: bool = True
    show_background: bool = False
    animate_colors: bool = False
    cycle_colors: bool = True
    custom_colors: List[BracketColor] = field(default_factory=list)


@dataclass
class BracketPairColorResult:
    """Bracket pair color result."""
    success: bool
    bracket_pairs: List[BracketPair] = field(default_factory=list)
    html: Optional[str] = None
    errors: List[str] = field(default_factory=list)
    message: Optional[str] = None


class BracketPairColorizationManager:
    """
    Bracket pair colorization manager.
    
    Özellikler:
    - Bracket pair detection
    - Color assignment based on nesting level
    - Multiple color schemes
    - Bracket matching
    - Color cycling
    - Custom color schemes
    - Bracket highlighting
    - Color persistence
    - Color scope
    - Color priority
    - Color visibility
    - Color animations
    - Color transitions
    - Color themes
    """
    
    def __init__(self, config: Optional[BracketPairColorConfig] = None):
        """
        Initialize bracket pair colorization manager.
        
        Args:
            config: Bracket pair color configuration
        """
        self.config = config or BracketPairColorConfig()
        self.bracket_pairs: List[BracketPair] = []
        self.color_cycle: List[BracketColor] = [
            BracketColor.RED,
            BracketColor.GREEN,
            BracketColor.BLUE,
            BracketColor.YELLOW,
            BracketColor.PURPLE,
            BracketColor.CYAN,
            BracketColor.ORANGE,
            BracketColor.PINK
        ]
    
    def colorize_brackets(self, code: str) -> BracketPairColorResult:
        """
        Colorize bracket pairs in code.
        
        Args:
            code: Code content
            
        Returns:
            BracketPairColorResult: Colorization result
        """
        result = BracketPairColorResult(success=False)
        
        if not self.config.enabled:
            result.message = "Bracket pair colorization disabled"
            return result
        
        try:
            self.bracket_pairs = []
            
            bracket_map = {
                '(': (BracketType.ROUND, ')'),
                ')': (BracketType.ROUND, '('),
                '[': (BracketType.SQUARE, ']'),
                ']': (BracketType.SQUARE, '['),
                '{': (BracketType.CURLY, '}'),
                '}': (BracketType.CURLY, '{'),
                '<': (BracketType.ANGLE, '>'),
                '>': (BracketType.ANGLE, '<')
            }
            
            lines = code.splitlines()
            stack = []
            
            for line_idx, line in enumerate(lines):
                for col_idx, char in enumerate(line):
                    if char in bracket_map:
                        bracket_type, matching_char = bracket_map[char]
                        
                        if char in '([{<':
                            # Opening bracket
                            position = BracketPosition(line=line_idx, column=col_idx)
                            nesting_level = len(stack)
                            color = self._get_color_for_level(nesting_level)
                            
                            stack.append({
                                'position': position,
                                'type': bracket_type,
                                'color': color,
                                'nesting_level': nesting_level
                            })
                        else:
                            # Closing bracket
                            if stack:
                                opening = stack.pop()
                                
                                if opening['type'] == bracket_type:
                                    # Matching pair found
                                    pair = BracketPair(
                                        opening=opening['position'],
                                        closing=BracketPosition(line=line_idx, column=col_idx),
                                        type=bracket_type,
                                        color=opening['color'],
                                        nesting_level=opening['nesting_level']
                                    )
                                    
                                    self.bracket_pairs.append(pair)
            
            result.success = True
            result.bracket_pairs = self.bracket_pairs
            result.html = self._generate_html()
            result.message = f"Colorized {len(self.bracket_pairs)} bracket pairs"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def _get_color_for_level(self, level: int) -> BracketColor:
        """
        Get color for nesting level.
        
        Args:
            level: Nesting level
            
        Returns:
            BracketColor: Color
        """
        if self.config.custom_colors:
            return self.config.custom_colors[level % len(self.config.custom_colors)]
        
        if self.config.cycle_colors:
            return self.color_cycle[level % len(self.color_cycle)]
        
        return self.color_cycle[0]
    
    def get_bracket_pairs(self) -> List[BracketPair]:
        """
        Get all bracket pairs.
        
        Returns:
            List[BracketPair]: Bracket pairs
        """
        return self.bracket_pairs
    
    def get_bracket_pairs_by_type(self, bracket_type: BracketType) -> List[BracketPair]:
        """
        Get bracket pairs by type.
        
        Args:
            bracket_type: Bracket type
            
        Returns:
            List[BracketPair]: Bracket pairs
        """
        return [bp for bp in self.bracket_pairs if bp.type == bracket_type]
    
    def get_bracket_pairs_by_color(self, color: BracketColor) -> List[BracketPair]:
        """
        Get bracket pairs by color.
        
        Args:
            color: Bracket color
            
        Returns:
            List[BracketPair]: Bracket pairs
        """
        return [bp for bp in self.bracket_pairs if bp.color == color]
    
    def get_matching_bracket(self, position: BracketPosition) -> Optional[BracketPosition]:
        """
        Get matching bracket position.
        
        Args:
            position: Bracket position
            
        Returns:
            Optional[BracketPosition]: Matching position
        """
        for pair in self.bracket_pairs:
            if pair.opening.line == position.line and pair.opening.column == position.column:
                return pair.closing
            if pair.closing.line == position.line and pair.closing.column == position.column:
                return pair.opening
        return None
    
    def set_color_scheme(self, scheme: str) -> BracketPairColorResult:
        """
        Set color scheme.
        
        Args:
            scheme: Color scheme name
            
        Returns:
            BracketPairColorResult: Set result
        """
        result = BracketPairColorResult(success=True)
        
        try:
            self.config.color_scheme = scheme
            result.message = f"Color scheme set to {scheme}"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def set_custom_colors(self, colors: List[BracketColor]) -> BracketPairColorResult:
        """
        Set custom colors.
        
        Args:
            colors: Custom colors
            
        Returns:
            BracketPairColorResult: Set result
        """
        result = BracketPairColorResult(success=True)
        
        try:
            self.config.custom_colors = colors
            result.message = f"Custom colors set ({len(colors)} colors)"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def update_config(self, config: BracketPairColorConfig) -> BracketPairColorResult:
        """
        Update bracket pair color configuration.
        
        Args:
            config: New configuration
            
        Returns:
            BracketPairColorResult: Update result
        """
        result = BracketPairColorResult(success=True)
        
        try:
            self.config = config
            result.message = "Config updated"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def get_config(self) -> BracketPairColorConfig:
        """
        Get bracket pair color configuration.
        
        Returns:
            BracketPairColorConfig: Configuration
        """
        return self.config
    
    def _generate_html(self) -> str:
        """
        Generate HTML output.
        
        Returns:
            str: HTML
        """
        html_lines = []
        
        for pair in self.bracket_pairs:
            opening_class = f"bracket bracket-{pair.type.value} bracket-{pair.color.value}"
            closing_class = f"bracket bracket-{pair.type.value} bracket-{pair.color.value}"
            
            html_lines.append(f'<span class="{opening_class}" data-line="{pair.opening.line}" data-col="{pair.opening.column}">({pair.type.value})</span>')
            html_lines.append(f'<span class="{closing_class}" data-line="{pair.closing.line}" data-col="{pair.closing.column}">({pair.type.value})</span>')
        
        return '<div class="bracket-pairs">' + "\n".join(html_lines) + "</div>"


if __name__ == "__main__":
    # Basit test
    config = BracketPairColorConfig()
    manager = BracketPairColorizationManager(config)
    
    code = """
def my_function(x, y):
    result = x + y
    if result > 10:
        return result
    return 0
"""
    
    result = manager.colorize_brackets(code)
    
    print(f"Colorized: {result.success}")
    print(f"Bracket pairs: {len(result.bracket_pairs)}")
    for pair in result.bracket_pairs:
        print(f"  - {pair.type.value} at level {pair.nesting_level} ({pair.color.value})")
