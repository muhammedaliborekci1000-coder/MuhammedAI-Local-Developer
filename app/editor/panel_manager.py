"""
MuhammedAI Local Developer - Panel Manager
Panel management system for code editor.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum


class PanelType(Enum):
    """Panel type."""
    SIDEBAR = "sidebar"
    BOTTOM_PANEL = "bottom_panel"
    EXPLORER = "explorer"
    SEARCH = "search"
    GIT = "git"
    DEBUG = "debug"
    TERMINAL = "terminal"
    OUTPUT = "output"
    PROBLEMS = "problems"
    EXTENSIONS = "extensions"
    CUSTOM = "custom"


class PanelPosition(Enum):
    """Panel position."""
    LEFT = "left"
    RIGHT = "right"
    BOTTOM = "bottom"
    TOP = "top"


class PanelState(Enum):
    """Panel state."""
    VISIBLE = "visible"
    HIDDEN = "hidden"
    MINIMIZED = "minimized"
    MAXIMIZED = "maximized"


@dataclass
class Panel:
    """Panel information."""
    id: str
    name: str
    type: PanelType
    position: PanelPosition = PanelPosition.LEFT
    state: PanelState = PanelState.VISIBLE
    width: Optional[int] = None
    height: Optional[int] = None
    icon: Optional[str] = None
    is_pinned: bool = False
    is_resizable: bool = True
    is_closable: bool = True
    order: int = 0


@dataclass
class PanelConfig:
    """Panel configuration."""
    enable_animations: bool = True
    auto_hide: bool = False
    remember_position: bool = True
    remember_size: bool = True
    show_panel_icons: bool = True
    enable_panel_tabs: bool = True
    max_panels_per_side: int = 5


@dataclass
class PanelResult:
    """Panel result."""
    success: bool
    panel: Optional[Panel] = None
    panels: List[Panel] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    message: Optional[str] = None


class PanelManager:
    """
    Panel manager.
    
    Özellikler:
    - Panel management
    - Panel visibility
    - Panel positioning
    - Panel sizing
    - Panel pinning
    - Panel tabs
    - Panel ordering
    - Panel minimization
    - Panel maximization
    - Custom panels
    - Panel animations
    - Panel auto-hide
    - Panel memory
    - Panel icons
    - Panel resizing
    - Panel closing
    - Panel focusing
    - Panel grouping
    """
    
    def __init__(self, config: Optional[PanelConfig] = None):
        """
        Initialize panel manager.
        
        Args:
            config: Panel configuration
        """
        self.config = config or PanelConfig()
        self.panels: Dict[str, Panel] = {}
        self.active_panel_id: Optional[str] = None
        self._next_order = 0
        self._initialize_builtin_panels()
    
    def _initialize_builtin_panels(self) -> None:
        """Initialize built-in panels."""
        # Explorer
        self.register_panel(Panel(
            id="explorer",
            name="Explorer",
            type=PanelType.EXPLORER,
            position=PanelPosition.LEFT,
            state=PanelState.VISIBLE,
            icon="explorer",
            order=self._next_order
        ))
        self._next_order += 1
        
        # Search
        self.register_panel(Panel(
            id="search",
            name="Search",
            type=PanelType.SEARCH,
            position=PanelPosition.LEFT,
            state=PanelState.HIDDEN,
            icon="search",
            order=self._next_order
        ))
        self._next_order += 1
        
        # Git
        self.register_panel(Panel(
            id="git",
            name="Source Control",
            type=PanelType.GIT,
            position=PanelPosition.LEFT,
            state=PanelState.HIDDEN,
            icon="git",
            order=self._next_order
        ))
        self._next_order += 1
        
        # Terminal
        self.register_panel(Panel(
            id="terminal",
            name="Terminal",
            type=PanelType.TERMINAL,
            position=PanelPosition.BOTTOM,
            state=PanelState.VISIBLE,
            icon="terminal",
            order=self._next_order
        ))
        self._next_order += 1
        
        # Output
        self.register_panel(Panel(
            id="output",
            name="Output",
            type=PanelType.OUTPUT,
            position=PanelPosition.BOTTOM,
            state=PanelState.HIDDEN,
            icon="output",
            order=self._next_order
        ))
        self._next_order += 1
        
        # Problems
        self.register_panel(Panel(
            id="problems",
            name="Problems",
            type=PanelType.PROBLEMS,
            position=PanelPosition.BOTTOM,
            state=PanelState.HIDDEN,
            icon="problems",
            order=self._next_order
        ))
        self._next_order += 1
    
    def register_panel(self, panel: Panel) -> PanelResult:
        """
        Register a panel.
        
        Args:
            panel: Panel to register
            
        Returns:
            PanelResult: Registration result
        """
        result = PanelResult(success=True)
        
        try:
            self.panels[panel.id] = panel
            result.panel = panel
            result.panels = self.get_all_panels()
            result.message = f"Panel '{panel.id}' registered"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def unregister_panel(self, panel_id: str) -> PanelResult:
        """
        Unregister a panel.
        
        Args:
            panel_id: Panel ID
            
        Returns:
            PanelResult: Unregistration result
        """
        result = PanelResult(success=False)
        
        try:
            if panel_id in self.panels:
                del self.panels[panel_id]
                
                if self.active_panel_id == panel_id:
                    self.active_panel_id = None
                
                result.success = True
                result.panels = self.get_all_panels()
                result.message = f"Panel '{panel_id}' unregistered"
            else:
                result.errors.append("Panel not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_panel(self, panel_id: str) -> Optional[Panel]:
        """
        Get panel by ID.
        
        Args:
            panel_id: Panel ID
            
        Returns:
            Optional[Panel]: Panel
        """
        return self.panels.get(panel_id)
    
    def get_all_panels(self) -> List[Panel]:
        """
        Get all panels.
        
        Returns:
            List[Panel]: All panels
        """
        return list(self.panels.values())
    
    def get_panels_by_position(self, position: PanelPosition) -> List[Panel]:
        """
        Get panels by position.
        
        Args:
            position: Panel position
            
        Returns:
            List[Panel]: Panels
        """
        panels = [p for p in self.panels.values() if p.position == position]
        panels.sort(key=lambda x: x.order)
        return panels
    
    def get_panels_by_type(self, panel_type: PanelType) -> List[Panel]:
        """
        Get panels by type.
        
        Args:
            panel_type: Panel type
            
        Returns:
            List[Panel]: Panels
        """
        return [p for p in self.panels.values() if p.type == panel_type]
    
    def show_panel(self, panel_id: str) -> PanelResult:
        """
        Show panel.
        
        Args:
            panel_id: Panel ID
            
        Returns:
            PanelResult: Show result
        """
        result = PanelResult(success=False)
        
        try:
            panel = self.panels.get(panel_id)
            if panel:
                panel.state = PanelState.VISIBLE
                self.active_panel_id = panel_id
                result.success = True
                result.panel = panel
                result.message = f"Panel '{panel_id}' shown"
            else:
                result.errors.append("Panel not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def hide_panel(self, panel_id: str) -> PanelResult:
        """
        Hide panel.
        
        Args:
            panel_id: Panel ID
            
        Returns:
            PanelResult: Hide result
        """
        result = PanelResult(success=False)
        
        try:
            panel = self.panels.get(panel_id)
            if panel:
                panel.state = PanelState.HIDDEN
                
                if self.active_panel_id == panel_id:
                    self.active_panel_id = None
                
                result.success = True
                result.panel = panel
                result.message = f"Panel '{panel_id}' hidden"
            else:
                result.errors.append("Panel not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def toggle_panel(self, panel_id: str) -> PanelResult:
        """
        Toggle panel visibility.
        
        Args:
            panel_id: Panel ID
            
        Returns:
            PanelResult: Toggle result
        """
        result = PanelResult(success=False)
        
        try:
            panel = self.panels.get(panel_id)
            if panel:
                if panel.state == PanelState.VISIBLE:
                    return self.hide_panel(panel_id)
                else:
                    return self.show_panel(panel_id)
            else:
                result.errors.append("Panel not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def minimize_panel(self, panel_id: str) -> PanelResult:
        """
        Minimize panel.
        
        Args:
            panel_id: Panel ID
            
        Returns:
            PanelResult: Minimize result
        """
        result = PanelResult(success=False)
        
        try:
            panel = self.panels.get(panel_id)
            if panel:
                panel.state = PanelState.MINIMIZED
                result.success = True
                result.panel = panel
                result.message = f"Panel '{panel_id}' minimized"
            else:
                result.errors.append("Panel not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def maximize_panel(self, panel_id: str) -> PanelResult:
        """
        Maximize panel.
        
        Args:
            panel_id: Panel ID
            
        Returns:
            PanelResult: Maximize result
        """
        result = PanelResult(success=False)
        
        try:
            panel = self.panels.get(panel_id)
            if panel:
                panel.state = PanelState.MAXIMIZED
                self.active_panel_id = panel_id
                result.success = True
                result.panel = panel
                result.message = f"Panel '{panel_id}' maximized"
            else:
                result.errors.append("Panel not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def set_active_panel(self, panel_id: str) -> PanelResult:
        """
        Set active panel.
        
        Args:
            panel_id: Panel ID
            
        Returns:
            PanelResult: Set result
        """
        result = PanelResult(success=False)
        
        try:
            panel = self.panels.get(panel_id)
            if panel:
                self.active_panel_id = panel_id
                result.success = True
                result.panel = panel
                result.message = f"Active panel set to '{panel_id}'"
            else:
                result.errors.append("Panel not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_active_panel(self) -> Optional[Panel]:
        """
        Get active panel.
        
        Returns:
            Optional[Panel]: Active panel
        """
        if self.active_panel_id:
            return self.panels.get(self.active_panel_id)
        return None
    
    def pin_panel(self, panel_id: str) -> PanelResult:
        """
        Pin panel.
        
        Args:
            panel_id: Panel ID
            
        Returns:
            PanelResult: Pin result
        """
        result = PanelResult(success=False)
        
        try:
            panel = self.panels.get(panel_id)
            if panel:
                panel.is_pinned = True
                result.success = True
                result.panel = panel
                result.message = f"Panel '{panel_id}' pinned"
            else:
                result.errors.append("Panel not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def unpin_panel(self, panel_id: str) -> PanelResult:
        """
        Unpin panel.
        
        Args:
            panel_id: Panel ID
            
        Returns:
            PanelResult: Unpin result
        """
        result = PanelResult(success=False)
        
        try:
            panel = self.panels.get(panel_id)
            if panel:
                panel.is_pinned = False
                result.success = True
                result.panel = panel
                result.message = f"Panel '{panel_id}' unpinned"
            else:
                result.errors.append("Panel not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def resize_panel(self, panel_id: str, width: Optional[int] = None, height: Optional[int] = None) -> PanelResult:
        """
        Resize panel.
        
        Args:
            panel_id: Panel ID
            width: New width
            height: New height
            
        Returns:
            PanelResult: Resize result
        """
        result = PanelResult(success=False)
        
        try:
            panel = self.panels.get(panel_id)
            if panel:
                if width is not None:
                    panel.width = width
                if height is not None:
                    panel.height = height
                
                result.success = True
                result.panel = panel
                result.message = f"Panel '{panel_id}' resized"
            else:
                result.errors.append("Panel not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def update_config(self, config: PanelConfig) -> PanelResult:
        """
        Update panel configuration.
        
        Args:
            config: New configuration
            
        Returns:
            PanelResult: Update result
        """
        result = PanelResult(success=True)
        
        try:
            self.config = config
            result.message = "Config updated"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def get_config(self) -> PanelConfig:
        """
        Get panel configuration.
        
        Returns:
            PanelConfig: Configuration
        """
        return self.config


if __name__ == "__main__":
    # Basit test
    config = PanelConfig()
    manager = PanelManager(config)
    
    # Panel göster
    result = manager.show_panel("explorer")
    
    print(f"Panel shown: {result.message}")
    
    # Tüm panelleri al
    panels = manager.get_all_panels()
    
    print(f"Total panels: {len(panels)}")
    for panel in panels:
        print(f"  - {panel.name} ({panel.state.value})")
