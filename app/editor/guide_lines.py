"""
MuhammedAI Local Developer - Guide Lines
Guide lines system for code editor.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum


class GuideLineType(Enum):
    """Guide line type."""
    INDENT = "indent"
    BRACKET = "bracket"
    COLUMN = "column"
    EDGE = "edge"
    CUSTOM = "custom"


class GuideLineStyle(Enum):
    """Guide line style."""
    SOLID = "solid"
    DASHED = "dashed"
    DOTTED = "dotted"
    DOUBLE = "double"


@dataclass
class GuideLine:
    """Guide line."""
    id: str
    type: GuideLineType
    column: int
    style: GuideLineStyle = GuideLineStyle.DASHED
    color: str = "#808080"
    is_enabled: bool = True
    is_visible: bool = True


@dataclass
class GuideLinesConfig:
    """Guide lines configuration."""
    enabled: bool = True
    show_indent_guides: bool = True
    show_bracket_guides: bool = True
    show_column_guides: bool = False
    show_edge_guides: bool = True
    indent_size: int = 4
    tab_size: int = 4
    guide_color: str = "#808080"
    guide_style: GuideLineStyle = GuideLineStyle.DASHED
    custom_columns: List[int] = field(default_factory=list)
    show_in_selection: bool = True


@dataclass
class GuideLinesResult:
    """Guide lines result."""
    success: bool
    guide_lines: List[GuideLine] = field(default_factory=list)
    html: Optional[str] = None
    errors: List[str] = field(default_factory=list)
    message: Optional[str] = None


class GuideLinesManager:
    """
    Guide lines manager.
    
    Özellikler:
    - Indent guides
    - Bracket guides
    - Column guides
    - Edge guides
    - Custom guides
    - Guide line styling
    - Guide line coloring
    - Guide line positioning
    - Guide line visibility
    - Guide line filtering
    - Guide line scope
    - Guide line context
    """
    
    def __init__(self, config: Optional[GuideLinesConfig] = None):
        """
        Initialize guide lines manager.
        
        Args:
            config: Guide lines configuration
        """
        self.config = config or GuideLinesConfig()
        self.guide_lines: Dict[str, GuideLine] = {}
        self.guide_line_id_counter = 0
        self._next_id()
    
    def _next_id(self) -> str:
        """
        Generate next guide line ID.
        
        Returns:
            str: Guide line ID
        """
        self.guide_line_id_counter += 1
        return f"guide_{self.guide_line_id_counter}"
    
    def add_guide_line(self, guide_line: GuideLine) -> GuideLinesResult:
        """
        Add a guide line.
        
        Args:
            guide_line: Guide line to add
            
        Returns:
            GuideLinesResult: Add result
        """
        result = GuideLinesResult(success=True)
        
        try:
            if not guide_line.id:
                guide_line.id = self._next_id()
            
            self.guide_lines[guide_line.id] = guide_line
            result.guide_lines = self.get_all_guide_lines()
            result.message = f"Guide line '{guide_line.id}' added"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def remove_guide_line(self, guide_line_id: str) -> GuideLinesResult:
        """
        Remove a guide line.
        
        Args:
            guide_line_id: Guide line ID
            
        Returns:
            GuideLinesResult: Remove result
        """
        result = GuideLinesResult(success=False)
        
        try:
            if guide_line_id in self.guide_lines:
                del self.guide_lines[guide_line_id]
                result.success = True
                result.guide_lines = self.get_all_guide_lines()
                result.message = f"Guide line '{guide_line_id}' removed"
            else:
                result.errors.append("Guide line not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_guide_line(self, guide_line_id: str) -> Optional[GuideLine]:
        """
        Get guide line by ID.
        
        Args:
            guide_line_id: Guide line ID
            
        Returns:
            Optional[GuideLine]: Guide line
        """
        return self.guide_lines.get(guide_line_id)
    
    def get_all_guide_lines(self) -> List[GuideLine]:
        """
        Get all guide lines.
        
        Returns:
            List[GuideLine]: All guide lines
        """
        return list(self.guide_lines.values())
    
    def get_guide_lines_by_type(self, guide_type: GuideLineType) -> List[GuideLine]:
        """
        Get guide lines by type.
        
        Args:
            guide_type: Guide line type
            
        Returns:
            List[GuideLine]: Guide lines
        """
        return [gl for gl in self.guide_lines.values() if gl.type == guide_type]
    
    def generate_indent_guides(self, text: str) -> GuideLinesResult:
        """
        Generate indent guides.
        
        Args:
            text: Text content
            
        Returns:
            GuideLinesResult: Generate result
        """
        result = GuideLinesResult(success=True)
        
        if not self.config.show_indent_guides:
            result.message = "Indent guides disabled"
            return result
        
        try:
            lines = text.splitlines()
            indent_size = self.config.indent_size
            
            for line_idx, line in enumerate(lines):
                # Count leading spaces/tabs
                leading_spaces = len(line) - len(line.lstrip())
                
                # Generate guide lines at indent positions
                for indent_level in range(1, (leading_spaces // indent_size) + 1):
                    column = indent_level * indent_size
                    
                    guide_line = GuideLine(
                        id="",
                        type=GuideLineType.INDENT,
                        column=column,
                        style=self.config.guide_style,
                        color=self.config.guide_color
                    )
                    
                    self.add_guide_line(guide_line)
            
            result.guide_lines = self.get_all_guide_lines()
            result.message = "Indent guides generated"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def add_column_guide(self, column: int) -> GuideLinesResult:
        """
        Add column guide.
        
        Args:
            column: Column position
            
        Returns:
            GuideLinesResult: Add result
        """
        if not self.config.show_column_guides:
            result = GuideLinesResult(success=False)
            result.message = "Column guides disabled"
            return result
        
        guide_line = GuideLine(
            id="",
            type=GuideLineType.COLUMN,
            column=column,
            style=self.config.guide_style,
            color=self.config.guide_color
        )
        
        return self.add_guide_line(guide_line)
    
    def add_edge_guide(self, edge: str) -> GuideLinesResult:
        """
        Add edge guide (left or right).
        
        Args:
            edge: Edge position ("left" or "right")
            
        Returns:
            GuideLinesResult: Add result
        """
        if not self.config.show_edge_guides:
            result = GuideLinesResult(success=False)
            result.message = "Edge guides disabled"
            return result
        
        column = 0 if edge == "left" else 100
        
        guide_line = GuideLine(
            id="",
            type=GuideLineType.EDGE,
            column=column,
            style=self.config.guide_style,
            color=self.config.guide_color
        )
        
        return self.add_guide_line(guide_line)
    
    def set_guide_line_enabled(self, guide_line_id: str, enabled: bool) -> GuideLinesResult:
        """
        Set guide line enabled state.
        
        Args:
            guide_line_id: Guide line ID
            enabled: Enabled state
            
        Returns:
            GuideLinesResult: Set result
        """
        result = GuideLinesResult(success=False)
        
        try:
            guide_line = self.guide_lines.get(guide_line_id)
            if guide_line:
                guide_line.is_enabled = enabled
                result.success = True
                result.message = f"Guide line '{guide_line_id}' {'enabled' if enabled else 'disabled'}"
            else:
                result.errors.append("Guide line not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def set_guide_line_visible(self, guide_line_id: str, visible: bool) -> GuideLinesResult:
        """
        Set guide line visible state.
        
        Args:
            guide_line_id: Guide line ID
            visible: Visible state
            
        Returns:
            GuideLinesResult: Set result
        """
        result = GuideLinesResult(success=False)
        
        try:
            guide_line = self.guide_lines.get(guide_line_id)
            if guide_line:
                guide_line.is_visible = visible
                result.success = True
                result.message = f"Guide line '{guide_line_id}' {'visible' if visible else 'hidden'}"
            else:
                result.errors.append("Guide line not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def clear_guide_lines(self) -> GuideLinesResult:
        """
        Clear all guide lines.
        
        Returns:
            GuideLinesResult: Clear result
        """
        result = GuideLinesResult(success=True)
        
        try:
            self.guide_lines.clear()
            result.message = "All guide lines cleared"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def update_config(self, config: GuideLinesConfig) -> GuideLinesResult:
        """
        Update guide lines configuration.
        
        Args:
            config: New configuration
            
        Returns:
            GuideLinesResult: Update result
        """
        result = GuideLinesResult(success=True)
        
        try:
            self.config = config
            result.message = "Config updated"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def get_config(self) -> GuideLinesConfig:
        """
        Get guide lines configuration.
        
        Returns:
            GuideLinesConfig: Configuration
        """
        return self.config


if __name__ == "__main__":
    # Basit test
    config = GuideLinesConfig()
    manager = GuideLinesManager(config)
    
    # Guide line ekle
    guide_line = GuideLine(
        id="",
        type=GuideLineType.COLUMN,
        column=80
    )
    
    result = manager.add_guide_line(guide_line)
    
    print(f"Guide line added: {result.message}")
    
    # Tüm guide line'ları al
    guide_lines = manager.get_all_guide_lines()
    
    print(f"Total guide lines: {len(guide_lines)}")
