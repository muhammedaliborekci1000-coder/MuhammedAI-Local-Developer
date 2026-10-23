"""
MuhammedAI Local Developer - Layout Manager
Layout manager system for web UI.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum


class LayoutType(Enum):
    """Layout type."""
    SINGLE = "single"
    SPLIT_VERTICAL = "split_vertical"
    SPLIT_HORIZONTAL = "split_horizontal"
    GRID = "grid"
    TABS = "tabs"
    CUSTOM = "custom"


class PanelType(Enum):
    """Panel type."""
    EDITOR = "editor"
    SIDEBAR = "sidebar"
    TERMINAL = "terminal"
    OUTPUT = "output"
    EXPLORER = "explorer"
    SEARCH = "search"
    DEBUG = "debug"
    CUSTOM = "custom"


class ResizeDirection(Enum):
    """Resize direction."""
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"
    BOTH = "both"
    CUSTOM = "custom"


@dataclass
class Panel:
    """Panel."""
    id: str
    type: PanelType
    title: str
    x: int = 0
    y: int = 0
    width: int = 100
    height: int = 100
    min_width: int = 50
    min_height: int = 50
    max_width: Optional[int] = None
    max_height: Optional[int] = None
    is_resizable: bool = True
    is_visible: bool = True
    is_collapsed: bool = False
    parent_id: Optional[str] = None
    children: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Layout:
    """Layout."""
    id: str
    name: str
    type: LayoutType
    panels: List[str] = field(default_factory=list)
    is_active: bool = False
    is_default: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class LayoutConfig:
    """Layout configuration."""
    enabled: bool = True
    default_layout: Optional[str] = None
    enable_resizing: bool = True
    enable_drag_drop: bool = True
    enable_collapsing: bool = True
    enable_saving: bool = True
    auto_save: bool = True
    max_panels: int = 20
    min_panel_size: int = 50
    animation_duration: int = 200  # milliseconds


@dataclass
class LayoutResult:
    """Layout result."""
    success: bool
    layout: Optional[Layout] = None
    layouts: List[Layout] = field(default_factory=list)
    panel: Optional[Panel] = None
    panels: List[Panel] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    message: Optional[str] = None


class LayoutManager:
    """
    Layout manager.
    
    Özellikler:
    - Layout types (single, split_vertical, split_horizontal, grid, tabs)
    - Panel types (editor, sidebar, terminal, output, explorer, search, debug)
    - Panel positioning
    - Panel resizing
    - Panel collapsing
    - Layout switching
    - Layout saving
    - Drag and drop
    - Animation
    """
    
    def __init__(self, config: Optional[LayoutConfig] = None):
        """
        Initialize layout manager.
        
        Args:
            config: Layout configuration
        """
        self.config = config or LayoutConfig()
        self.layouts: Dict[str, Layout] = {}
        self.panels: Dict[str, Panel] = {}
        self.active_layout_id: Optional[str] = None
        self.layout_id_counter = 0
        self.panel_id_counter = 0
        self._next_layout_id()
        self._next_panel_id()
    
    def _next_layout_id(self) -> str:
        """
        Generate next layout ID.
        
        Returns:
            str: Layout ID
        """
        self.layout_id_counter += 1
        return f"layout_{self.layout_id_counter}"
    
    def _next_panel_id(self) -> str:
        """
        Generate next panel ID.
        
        Returns:
            str: Panel ID
        """
        self.panel_id_counter += 1
        return f"panel_{self.panel_id_counter}"
    
    def add_layout(self, layout: Layout) -> LayoutResult:
        """
        Add a layout.
        
        Args:
            layout: Layout to add
            
        Returns:
            LayoutResult: Add result
        """
        result = LayoutResult(success=True)
        
        try:
            if not layout.id:
                layout.id = self._next_layout_id()
            
            self.layouts[layout.id] = layout
            
            if not self.active_layout_id:
                self.active_layout_id = layout.id
                layout.is_active = True
            
            result.layout = layout
            result.layouts = self.get_all_layouts()
            result.message = f"Layout '{layout.id}' added"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def remove_layout(self, layout_id: str) -> LayoutResult:
        """
        Remove a layout.
        
        Args:
            layout_id: Layout ID
            
        Returns:
            LayoutResult: Remove result
        """
        result = LayoutResult(success=False)
        
        try:
            if layout_id in self.layouts:
                del self.layouts[layout_id]
                
                if self.active_layout_id == layout_id:
                    self.active_layout_id = None
                    if self.layouts:
                        first_layout_id = list(self.layouts.keys())[0]
                        self.active_layout_id = first_layout_id
                        self.layouts[first_layout_id].is_active = True
                
                result.success = True
                result.layouts = self.get_all_layouts()
                result.message = f"Layout '{layout_id}' removed"
            else:
                result.errors.append("Layout not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_layout(self, layout_id: str) -> Optional[Layout]:
        """
        Get layout by ID.
        
        Args:
            layout_id: Layout ID
            
        Returns:
            Optional[Layout]: Layout
        """
        return self.layouts.get(layout_id)
    
    def get_all_layouts(self) -> List[Layout]:
        """
        Get all layouts.
        
        Returns:
            List[Layout]: All layouts
        """
        return list(self.layouts.values())
    
    def set_active_layout(self, layout_id: str) -> LayoutResult:
        """
        Set active layout.
        
        Args:
            layout_id: Layout ID
            
        Returns:
            LayoutResult: Set result
        """
        result = LayoutResult(success=False)
        
        try:
            # Deactivate current active layout
            if self.active_layout_id and self.active_layout_id in self.layouts:
                self.layouts[self.active_layout_id].is_active = False
            
            # Activate new layout
            if layout_id in self.layouts:
                self.layouts[layout_id].is_active = True
                self.active_layout_id = layout_id
                result.success = True
                result.layout = self.layouts[layout_id]
                result.message = f"Layout '{layout_id}' set as active"
            else:
                result.errors.append("Layout not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def add_panel(self, panel: Panel) -> LayoutResult:
        """
        Add a panel.
        
        Args:
            panel: Panel to add
            
        Returns:
            LayoutResult: Add result
        """
        result = LayoutResult(success=True)
        
        try:
            if len(self.panels) >= self.config.max_panels:
                result.errors.append(f"Maximum panels reached (max {self.config.max_panels})")
                result.success = False
                return result
            
            if not panel.id:
                panel.id = self._next_panel_id()
            
            self.panels[panel.id] = panel
            
            # Add to active layout
            if self.active_layout_id and self.active_layout_id in self.layouts:
                self.layouts[self.active_layout_id].panels.append(panel.id)
            
            result.panel = panel
            result.panels = self.get_all_panels()
            result.message = f"Panel '{panel.id}' added"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def remove_panel(self, panel_id: str) -> LayoutResult:
        """
        Remove a panel.
        
        Args:
            panel_id: Panel ID
            
        Returns:
            LayoutResult: Remove result
        """
        result = LayoutResult(success=False)
        
        try:
            if panel_id in self.panels:
                panel = self.panels[panel_id]
                
                # Remove from parent's children
                if panel.parent_id and panel.parent_id in self.panels:
                    parent = self.panels[panel.parent_id]
                    if panel_id in parent.children:
                        parent.children.remove(panel_id)
                
                # Remove from layouts
                for layout in self.layouts.values():
                    if panel_id in layout.panels:
                        layout.panels.remove(panel_id)
                
                del self.panels[panel_id]
                result.success = True
                result.panels = self.get_all_panels()
                result.message = f"Panel '{panel_id}' removed"
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
    
    def get_panels_by_type(self, panel_type: PanelType) -> List[Panel]:
        """
        Get panels by type.
        
        Args:
            panel_type: Panel type
            
        Returns:
            List[Panel]: Panels
        """
        return [p for p in self.panels.values() if p.type == panel_type]
    
    def resize_panel(self, panel_id: str, width: Optional[int] = None, height: Optional[int] = None) -> LayoutResult:
        """
        Resize a panel.
        
        Args:
            panel_id: Panel ID
            width: New width
            height: New height
            
        Returns:
            LayoutResult: Resize result
        """
        result = LayoutResult(success=False)
        
        try:
            if not self.config.enable_resizing:
                result.errors.append("Resizing disabled")
                return result
            
            panel = self.panels.get(panel_id)
            if panel:
                if panel.is_resizable:
                    if width is not None:
                        if panel.max_width and width > panel.max_width:
                            width = panel.max_width
                        if width < panel.min_width:
                            width = panel.min_width
                        panel.width = width
                    
                    if height is not None:
                        if panel.max_height and height > panel.max_height:
                            height = panel.max_height
                        if height < panel.min_height:
                            height = panel.min_height
                        panel.height = height
                    
                    result.success = True
                    result.panel = panel
                    result.message = f"Panel '{panel_id}' resized"
                else:
                    result.errors.append("Panel not resizable")
            else:
                result.errors.append("Panel not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def move_panel(self, panel_id: str, x: int, y: int) -> LayoutResult:
        """
        Move a panel.
        
        Args:
            panel_id: Panel ID
            x: X position
            y: Y position
            
        Returns:
            LayoutResult: Move result
        """
        result = LayoutResult(success=False)
        
        try:
            panel = self.panels.get(panel_id)
            if panel:
                panel.x = x
                panel.y = y
                result.success = True
                result.panel = panel
                result.message = f"Panel '{panel_id}' moved to ({x}, {y})"
            else:
                result.errors.append("Panel not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def collapse_panel(self, panel_id: str) -> LayoutResult:
        """
        Collapse a panel.
        
        Args:
            panel_id: Panel ID
            
        Returns:
            LayoutResult: Collapse result
        """
        result = LayoutResult(success=False)
        
        try:
            if not self.config.enable_collapsing:
                result.errors.append("Collapsing disabled")
                return result
            
            panel = self.panels.get(panel_id)
            if panel:
                panel.is_collapsed = True
                result.success = True
                result.panel = panel
                result.message = f"Panel '{panel_id}' collapsed"
            else:
                result.errors.append("Panel not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def expand_panel(self, panel_id: str) -> LayoutResult:
        """
        Expand a panel.
        
        Args:
            panel_id: Panel ID
            
        Returns:
            LayoutResult: Expand result
        """
        result = LayoutResult(success=False)
        
        try:
            panel = self.panels.get(panel_id)
            if panel:
                panel.is_collapsed = False
                result.success = True
                result.panel = panel
                result.message = f"Panel '{panel_id}' expanded"
            else:
                result.errors.append("Panel not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def set_panel_visible(self, panel_id: str, visible: bool) -> LayoutResult:
        """
        Set panel visibility.
        
        Args:
            panel_id: Panel ID
            visible: Visible state
            
        Returns:
            LayoutResult: Set result
        """
        result = LayoutResult(success=False)
        
        try:
            panel = self.panels.get(panel_id)
            if panel:
                panel.is_visible = visible
                result.success = True
                result.panel = panel
                result.message = f"Panel '{panel_id}' {'visible' if visible else 'hidden'}"
            else:
                result.errors.append("Panel not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def clear_all_panels(self) -> LayoutResult:
        """
        Clear all panels.
        
        Returns:
            LayoutResult: Clear result
        """
        result = LayoutResult(success=True)
        
        try:
            self.panels.clear()
            for layout in self.layouts.values():
                layout.panels.clear()
            result.message = "All panels cleared"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def clear_all_layouts(self) -> LayoutResult:
        """
        Clear all layouts.
        
        Returns:
            LayoutResult: Clear result
        """
        result = LayoutResult(success=True)
        
        try:
            self.layouts.clear()
            self.active_layout_id = None
            result.message = "All layouts cleared"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def update_config(self, config: LayoutConfig) -> LayoutResult:
        """
        Update layout configuration.
        
        Args:
            config: New configuration
            
        Returns:
            LayoutResult: Update result
        """
        result = LayoutResult(success=True)
        
        try:
            self.config = config
            result.message = "Config updated"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def get_config(self) -> LayoutConfig:
        """
        Get layout configuration.
        
        Returns:
            LayoutConfig: Configuration
        """
        return self.config


if __name__ == "__main__":
    # Basit test
    config = LayoutConfig()
    manager = LayoutManager(config)
    
    # Layout ekle
    layout = Layout(
        id="",
        name="Default",
        type=LayoutType.SINGLE
    )
    
    result = manager.add_layout(layout)
    
    print(f"Layout added: {result.message}")
    
    # Tüm layout'ları al
    layouts = manager.get_all_layouts()
    
    print(f"Total layouts: {len(layouts)}")
