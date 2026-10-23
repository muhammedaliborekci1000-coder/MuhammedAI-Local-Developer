"""
MuhammedAI Local Developer - Tooltip UI
Tooltip UI system for web UI.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum


class TooltipPosition(Enum):
    """Tooltip position."""
    TOP = "top"
    BOTTOM = "bottom"
    LEFT = "left"
    RIGHT = "right"
    TOP_LEFT = "top_left"
    TOP_RIGHT = "top_right"
    BOTTOM_LEFT = "bottom_left"
    BOTTOM_RIGHT = "bottom_right"
    AUTO = "auto"
    CUSTOM = "custom"


class TooltipTrigger(Enum):
    """Tooltip trigger."""
    HOVER = "hover"
    CLICK = "click"
    FOCUS = "focus"
    MANUAL = "manual"
    CUSTOM = "custom"


@dataclass
class Tooltip:
    """Tooltip."""
    id: str
    content: str
    target_id: str
    position: TooltipPosition = TooltipPosition.TOP
    trigger: TooltipTrigger = TooltipTrigger.HOVER
    is_visible: bool = False
    delay: int = 0  # milliseconds
    duration: Optional[int] = None  # milliseconds, None for no auto-hide
    max_width: int = 300
    is_enabled: bool = True
    show_arrow: bool = True
    animation: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TooltipConfig:
    """Tooltip configuration."""
    enabled: bool = True
    default_position: TooltipPosition = TooltipPosition.TOP
    default_trigger: TooltipTrigger = TooltipTrigger.HOVER
    default_delay: int = 0
    default_duration: Optional[int] = None
    default_max_width: int = 300
    show_arrow: bool = True
    enable_animation: bool = True
    animation_duration: int = 200  # milliseconds
    max_tooltips: int = 50
    enable_z_index: bool = True
    z_index: int = 1000


@dataclass
class TooltipResult:
    """Tooltip result."""
    success: bool
    tooltip: Optional[Tooltip] = None
    tooltips: List[Tooltip] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    message: Optional[str] = None


class TooltipUIManager:
    """
    Tooltip UI manager.
    
    Özellikler:
    - Tooltip positions (top, bottom, left, right, top_left, top_right, bottom_left, bottom_right, auto)
    - Tooltip triggers (hover, click, focus, manual)
    - Tooltip visibility
    - Delay and duration
    - Max width
    - Arrow
    - Animation
    - Z-index
    """
    
    def __init__(self, config: Optional[TooltipConfig] = None):
        """
        Initialize tooltip UI manager.
        
        Args:
            config: Tooltip configuration
        """
        self.config = config or TooltipConfig()
        self.tooltips: Dict[str, Tooltip] = {}
        self.tooltip_id_counter = 0
        self._next_tooltip_id()
    
    def _next_tooltip_id(self) -> str:
        """
        Generate next tooltip ID.
        
        Returns:
            str: Tooltip ID
        """
        self.tooltip_id_counter += 1
        return f"tooltip_{self.tooltip_id_counter}"
    
    def add_tooltip(self, tooltip: Tooltip) -> TooltipResult:
        """
        Add a tooltip.
        
        Args:
            tooltip: Tooltip to add
            
        Returns:
            TooltipResult: Add result
        """
        result = TooltipResult(success=True)
        
        try:
            if len(self.tooltips) >= self.config.max_tooltips:
                result.errors.append(f"Maximum tooltips reached (max {self.config.max_tooltips})")
                result.success = False
                return result
            
            if not tooltip.id:
                tooltip.id = self._next_tooltip_id()
            
            self.tooltips[tooltip.id] = tooltip
            result.tooltip = tooltip
            result.tooltips = self.get_all_tooltips()
            result.message = f"Tooltip '{tooltip.id}' added"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def remove_tooltip(self, tooltip_id: str) -> TooltipResult:
        """
        Remove a tooltip.
        
        Args:
            tooltip_id: Tooltip ID
            
        Returns:
            TooltipResult: Remove result
        """
        result = TooltipResult(success=False)
        
        try:
            if tooltip_id in self.tooltips:
                del self.tooltips[tooltip_id]
                result.success = True
                result.tooltips = self.get_all_tooltips()
                result.message = f"Tooltip '{tooltip_id}' removed"
            else:
                result.errors.append("Tooltip not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_tooltip(self, tooltip_id: str) -> Optional[Tooltip]:
        """
        Get tooltip by ID.
        
        Args:
            tooltip_id: Tooltip ID
            
        Returns:
            Optional[Tooltip]: Tooltip
        """
        return self.tooltips.get(tooltip_id)
    
    def get_all_tooltips(self) -> List[Tooltip]:
        """
        Get all tooltips.
        
        Returns:
            List[Tooltip]: All tooltips
        """
        return list(self.tooltips.values())
    
    def get_tooltip_by_target(self, target_id: str) -> Optional[Tooltip]:
        """
        Get tooltip by target ID.
        
        Args:
            target_id: Target ID
            
        Returns:
            Optional[Tooltip]: Tooltip
        """
        for tooltip in self.tooltips.values():
            if tooltip.target_id == target_id:
                return tooltip
        return None
    
    def show_tooltip(self, tooltip_id: str) -> TooltipResult:
        """
        Show a tooltip.
        
        Args:
            tooltip_id: Tooltip ID
            
        Returns:
            TooltipResult: Show result
        """
        result = TooltipResult(success=False)
        
        try:
            tooltip = self.tooltips.get(tooltip_id)
            if tooltip:
                if tooltip.is_enabled:
                    tooltip.is_visible = True
                    result.success = True
                    result.tooltip = tooltip
                    result.message = f"Tooltip '{tooltip_id}' shown"
                else:
                    result.errors.append("Tooltip is disabled")
            else:
                result.errors.append("Tooltip not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def hide_tooltip(self, tooltip_id: str) -> TooltipResult:
        """
        Hide a tooltip.
        
        Args:
            tooltip_id: Tooltip ID
            
        Returns:
            TooltipResult: Hide result
        """
        result = TooltipResult(success=False)
        
        try:
            tooltip = self.tooltips.get(tooltip_id)
            if tooltip:
                tooltip.is_visible = False
                result.success = True
                result.tooltip = tooltip
                result.message = f"Tooltip '{tooltip_id}' hidden"
            else:
                result.errors.append("Tooltip not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def set_tooltip_position(self, tooltip_id: str, position: TooltipPosition) -> TooltipResult:
        """
        Set tooltip position.
        
        Args:
            tooltip_id: Tooltip ID
            position: Tooltip position
            
        Returns:
            TooltipResult: Set result
        """
        result = TooltipResult(success=False)
        
        try:
            tooltip = self.tooltips.get(tooltip_id)
            if tooltip:
                tooltip.position = position
                result.success = True
                result.tooltip = tooltip
                result.message = f"Tooltip '{tooltip_id}' position set to {position.value}"
            else:
                result.errors.append("Tooltip not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def set_tooltip_content(self, tooltip_id: str, content: str) -> TooltipResult:
        """
        Set tooltip content.
        
        Args:
            tooltip_id: Tooltip ID
            content: Tooltip content
            
        Returns:
            TooltipResult: Set result
        """
        result = TooltipResult(success=False)
        
        try:
            tooltip = self.tooltips.get(tooltip_id)
            if tooltip:
                tooltip.content = content
                result.success = True
                result.tooltip = tooltip
                result.message = f"Tooltip '{tooltip_id}' content updated"
            else:
                result.errors.append("Tooltip not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def set_tooltip_enabled(self, tooltip_id: str, enabled: bool) -> TooltipResult:
        """
        Set tooltip enabled state.
        
        Args:
            tooltip_id: Tooltip ID
            enabled: Enabled state
            
        Returns:
            TooltipResult: Set result
        """
        result = TooltipResult(success=False)
        
        try:
            tooltip = self.tooltips.get(tooltip_id)
            if tooltip:
                tooltip.is_enabled = enabled
                result.success = True
                result.tooltip = tooltip
                result.message = f"Tooltip '{tooltip_id}' {'enabled' if enabled else 'disabled'}"
            else:
                result.errors.append("Tooltip not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def set_tooltip_delay(self, tooltip_id: str, delay: int) -> TooltipResult:
        """
        Set tooltip delay.
        
        Args:
            tooltip_id: Tooltip ID
            delay: Delay in milliseconds
            
        Returns:
            TooltipResult: Set result
        """
        result = TooltipResult(success=False)
        
        try:
            tooltip = self.tooltips.get(tooltip_id)
            if tooltip:
                tooltip.delay = delay
                result.success = True
                result.tooltip = tooltip
                result.message = f"Tooltip '{tooltip_id}' delay set to {delay}ms"
            else:
                result.errors.append("Tooltip not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def set_tooltip_duration(self, tooltip_id: str, duration: Optional[int]) -> TooltipResult:
        """
        Set tooltip duration.
        
        Args:
            tooltip_id: Tooltip ID
            duration: Duration in milliseconds (None for no auto-hide)
            
        Returns:
            TooltipResult: Set result
        """
        result = TooltipResult(success=False)
        
        try:
            tooltip = self.tooltips.get(tooltip_id)
            if tooltip:
                tooltip.duration = duration
                result.success = True
                result.tooltip = tooltip
                result.message = f"Tooltip '{tooltip_id}' duration set"
            else:
                result.errors.append("Tooltip not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def hide_all_tooltips(self) -> TooltipResult:
        """
        Hide all tooltips.
        
        Returns:
            TooltipResult: Hide result
        """
        result = TooltipResult(success=True)
        
        try:
            for tooltip in self.tooltips.values():
                tooltip.is_visible = False
            
            result.message = "All tooltips hidden"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def clear_all_tooltips(self) -> TooltipResult:
        """
        Clear all tooltips.
        
        Returns:
            TooltipResult: Clear result
        """
        result = TooltipResult(success=True)
        
        try:
            self.tooltips.clear()
            result.message = "All tooltips cleared"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def update_config(self, config: TooltipConfig) -> TooltipResult:
        """
        Update tooltip configuration.
        
        Args:
            config: New configuration
            
        Returns:
            TooltipResult: Update result
        """
        result = TooltipResult(success=True)
        
        try:
            self.config = config
            result.message = "Config updated"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def get_config(self) -> TooltipConfig:
        """
        Get tooltip configuration.
        
        Returns:
            TooltipConfig: Configuration
        """
        return self.config


if __name__ == "__main__":
    # Basit test
    config = TooltipConfig()
    manager = TooltipUIManager(config)
    
    # Tooltip ekle
    tooltip = Tooltip(
        id="",
        content="This is a tooltip",
        target_id="button_1"
    )
    
    result = manager.add_tooltip(tooltip)
    
    print(f"Tooltip added: {result.message}")
    
    # Tüm tooltip'ları al
    tooltips = manager.get_all_tooltips()
    
    print(f"Total tooltips: {len(tooltips)}")
