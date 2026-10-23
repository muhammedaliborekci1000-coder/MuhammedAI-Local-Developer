"""
MuhammedAI Local Developer - Overview Ruler
Overview ruler system for code editor.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum


class OverviewRulerPosition(Enum):
    """Overview ruler position."""
    LEFT = "left"
    RIGHT = "right"


class OverviewRulerColor(Enum):
    """Overview ruler color."""
    ERROR = "#FF0000"
    WARNING = "#FFA500"
    INFO = "#0000FF"
    HINT = "#00FF00"
    SUCCESS = "#008000"
    CUSTOM = "#808080"


@dataclass
class OverviewRulerMark:
    """Overview ruler mark."""
    id: str
    line: int
    color: str
    position: OverviewRulerPosition = OverviewRulerPosition.RIGHT
    is_enabled: bool = True
    is_visible: bool = True
    tooltip: Optional[str] = None
    priority: int = 0


@dataclass
class OverviewRulerConfig:
    """Overview ruler configuration."""
    enabled: bool = True
    position: OverviewRulerPosition = OverviewRulerPosition.RIGHT
    width: int = 14
    show_errors: bool = True
    show_warnings: bool = True
    show_info: bool = True
    show_hints: bool = True
    show_selection: bool = True
    show_minimap: bool = True
    animate_marks: bool = True
    max_marks: int = 100


@dataclass
class OverviewRulerResult:
    """Overview ruler result."""
    success: bool
    marks: List[OverviewRulerMark] = field(default_factory=list)
    html: Optional[str] = None
    errors: List[str] = field(default_factory=list)
    message: Optional[str] = None


class OverviewRulerManager:
    """
    Overview ruler manager.
    
    Özellikler:
    - Error marks
    - Warning marks
    - Info marks
    - Hint marks
    - Success marks
    - Custom marks
    - Mark positioning
    - Mark priority
    - Mark filtering
    - Mark visibility
    - Mark animations
    - Mark scope
    - Mark context
    """
    
    def __init__(self, config: Optional[OverviewRulerConfig] = None):
        """
        Initialize overview ruler manager.
        
        Args:
            config: Overview ruler configuration
        """
        self.config = config or OverviewRulerConfig()
        self.marks: Dict[str, OverviewRulerMark] = {}
        self.mark_id_counter = 0
        self._next_id()
    
    def _next_id(self) -> str:
        """
        Generate next mark ID.
        
        Returns:
            str: Mark ID
        """
        self.mark_id_counter += 1
        return f"mark_{self.mark_id_counter}"
    
    def add_mark(self, mark: OverviewRulerMark) -> OverviewRulerResult:
        """
        Add a mark.
        
        Args:
            mark: Mark to add
            
        Returns:
            OverviewRulerResult: Add result
        """
        result = OverviewRulerResult(success=True)
        
        try:
            if not mark.id:
                mark.id = self._next_id()
            
            self.marks[mark.id] = mark
            
            # Limit marks
            if len(self.marks) > self.config.max_marks:
                oldest_id = min(self.marks.keys(), key=lambda k: self.marks[k].priority)
                del self.marks[oldest_id]
            
            result.marks = self.get_all_marks()
            result.message = f"Mark '{mark.id}' added"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def remove_mark(self, mark_id: str) -> OverviewRulerResult:
        """
        Remove a mark.
        
        Args:
            mark_id: Mark ID
            
        Returns:
            OverviewRulerResult: Remove result
        """
        result = OverviewRulerResult(success=False)
        
        try:
            if mark_id in self.marks:
                del self.marks[mark_id]
                result.success = True
                result.marks = self.get_all_marks()
                result.message = f"Mark '{mark_id}' removed"
            else:
                result.errors.append("Mark not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_mark(self, mark_id: str) -> Optional[OverviewRulerMark]:
        """
        Get mark by ID.
        
        Args:
            mark_id: Mark ID
            
        Returns:
            Optional[OverviewRulerMark]: Mark
        """
        return self.marks.get(mark_id)
    
    def get_all_marks(self) -> List[OverviewRulerMark]:
        """
        Get all marks.
        
        Returns:
            List[OverviewRulerMark]: All marks
        """
        return list(self.marks.values())
    
    def get_marks_at_line(self, line: int) -> List[OverviewRulerMark]:
        """
        Get marks at specific line.
        
        Args:
            line: Line number
            
        Returns:
            List[OverviewRulerMark]: Marks
        """
        return [m for m in self.marks.values() if m.line == line]
    
    def add_error_mark(self, line: int, tooltip: str = "") -> OverviewRulerResult:
        """
        Add error mark.
        
        Args:
            line: Line number
            tooltip: Tooltip text
            
        Returns:
            OverviewRulerResult: Add result
        """
        if not self.config.show_errors:
            result = OverviewRulerResult(success=False)
            result.message = "Error marks disabled"
            return result
        
        mark = OverviewRulerMark(
            id="",
            line=line,
            color=OverviewRulerColor.ERROR.value,
            position=self.config.position,
            tooltip=tooltip
        )
        
        return self.add_mark(mark)
    
    def add_warning_mark(self, line: int, tooltip: str = "") -> OverviewRulerResult:
        """
        Add warning mark.
        
        Args:
            line: Line number
            tooltip: Tooltip text
            
        Returns:
            OverviewRulerResult: Add result
        """
        if not self.config.show_warnings:
            result = OverviewRulerResult(success=False)
            result.message = "Warning marks disabled"
            return result
        
        mark = OverviewRulerMark(
            id="",
            line=line,
            color=OverviewRulerColor.WARNING.value,
            position=self.config.position,
            tooltip=tooltip
        )
        
        return self.add_mark(mark)
    
    def add_info_mark(self, line: int, tooltip: str = "") -> OverviewRulerResult:
        """
        Add info mark.
        
        Args:
            line: Line number
            tooltip: Tooltip text
            
        Returns:
            OverviewRulerResult: Add result
        """
        if not self.config.show_info:
            result = OverviewRulerResult(success=False)
            result.message = "Info marks disabled"
            return result
        
        mark = OverviewRulerMark(
            id="",
            line=line,
            color=OverviewRulerColor.INFO.value,
            position=self.config.position,
            tooltip=tooltip
        )
        
        return self.add_mark(mark)
    
    def add_hint_mark(self, line: int, tooltip: str = "") -> OverviewRulerResult:
        """
        Add hint mark.
        
        Args:
            line: Line number
            tooltip: Tooltip text
            
        Returns:
            OverviewRulerResult: Add result
        """
        if not self.config.show_hints:
            result = OverviewRulerResult(success=False)
            result.message = "Hint marks disabled"
            return result
        
        mark = OverviewRulerMark(
            id="",
            line=line,
            color=OverviewRulerColor.HINT.value,
            position=self.config.position,
            tooltip=tooltip
        )
        
        return self.add_mark(mark)
    
    def add_success_mark(self, line: int, tooltip: str = "") -> OverviewRulerResult:
        """
        Add success mark.
        
        Args:
            line: Line number
            tooltip: Tooltip text
            
        Returns:
            OverviewRulerResult: Add result
        """
        mark = OverviewRulerMark(
            id="",
            line=line,
            color=OverviewRulerColor.SUCCESS.value,
            position=self.config.position,
            tooltip=tooltip
        )
        
        return self.add_mark(mark)
    
    def add_custom_mark(self, line: int, color: str, tooltip: str = "") -> OverviewRulerResult:
        """
        Add custom mark.
        
        Args:
            line: Line number
            color: Color string
            tooltip: Tooltip text
            
        Returns:
            OverviewRulerResult: Add result
        """
        mark = OverviewRulerMark(
            id="",
            line=line,
            color=color,
            position=self.config.position,
            tooltip=tooltip
        )
        
        return self.add_mark(mark)
    
    def clear_marks(self) -> OverviewRulerResult:
        """
        Clear all marks.
        
        Returns:
            OverviewRulerResult: Clear result
        """
        result = OverviewRulerResult(success=True)
        
        try:
            self.marks.clear()
            result.message = "All marks cleared"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def set_mark_enabled(self, mark_id: str, enabled: bool) -> OverviewRulerResult:
        """
        Set mark enabled state.
        
        Args:
            mark_id: Mark ID
            enabled: Enabled state
            
        Returns:
            OverviewRulerResult: Set result
        """
        result = OverviewRulerResult(success=False)
        
        try:
            mark = self.marks.get(mark_id)
            if mark:
                mark.is_enabled = enabled
                result.success = True
                result.message = f"Mark '{mark_id}' {'enabled' if enabled else 'disabled'}"
            else:
                result.errors.append("Mark not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def set_mark_visible(self, mark_id: str, visible: bool) -> OverviewRulerResult:
        """
        Set mark visible state.
        
        Args:
            mark_id: Mark ID
            visible: Visible state
            
        Returns:
            OverviewRulerResult: Set result
        """
        result = OverviewRulerResult(success=False)
        
        try:
            mark = self.marks.get(mark_id)
            if mark:
                mark.is_visible = visible
                result.success = True
                result.message = f"Mark '{mark_id}' {'visible' if visible else 'hidden'}"
            else:
                result.errors.append("Mark not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def update_config(self, config: OverviewRulerConfig) -> OverviewRulerResult:
        """
        Update overview ruler configuration.
        
        Args:
            config: New configuration
            
        Returns:
            OverviewRulerResult: Update result
        """
        result = OverviewRulerResult(success=True)
        
        try:
            self.config = config
            result.message = "Config updated"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def get_config(self) -> OverviewRulerConfig:
        """
        Get overview ruler configuration.
        
        Returns:
            OverviewRulerConfig: Configuration
        """
        return self.config


if __name__ == "__main__":
    # Basit test
    config = OverviewRulerConfig()
    manager = OverviewRulerManager(config)
    
    # Mark ekle
    result = manager.add_error_mark(10, "Test error")
    
    print(f"Mark added: {result.message}")
    
    # Tüm mark'ları al
    marks = manager.get_all_marks()
    
    print(f"Total marks: {len(marks)}")
