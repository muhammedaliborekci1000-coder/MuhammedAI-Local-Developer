"""
MuhammedAI Local Developer - Sidebar UI
Sidebar UI system for web UI.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum


class SidebarPosition(Enum):
    """Sidebar position."""
    LEFT = "left"
    RIGHT = "right"
    CUSTOM = "custom"


class SidebarPanel(Enum):
    """Sidebar panel type."""
    FILE_EXPLORER = "file_explorer"
    SEARCH = "search"
    GIT = "git"
    DEBUG = "debug"
    EXTENSIONS = "extensions"
    OUTLINE = "outline"
    PROBLEMS = "problems"
    OUTPUT = "output"
    TERMINAL = "terminal"
    CUSTOM = "custom"


@dataclass
class SidebarItem:
    """Sidebar item."""
    id: str
    panel: SidebarPanel
    title: str
    icon: str
    is_enabled: bool = True
    is_visible: bool = True
    is_active: bool = False
    is_collapsed: bool = False
    order: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SidebarConfig:
    """Sidebar configuration."""
    enabled: bool = True
    position: SidebarPosition = SidebarPosition.LEFT
    width: int = 300
    min_width: int = 200
    max_width: int = 600
    show_icons: bool = True
    show_badges: bool = True
    enable_collapse: bool = True
    enable_resize: bool = True
    enable_drag_drop: bool = True
    auto_hide: bool = False
    theme: str = "default"


@dataclass
class SidebarResult:
    """Sidebar result."""
    success: bool
    item: Optional[SidebarItem] = None
    items: List[SidebarItem] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    message: Optional[str] = None


class SidebarUIManager:
    """
    Sidebar UI manager.
    
    Özellikler:
    - Sidebar panels (file explorer, search, git, debug, extensions, outline, problems, output, terminal)
    - Sidebar position (left, right)
    - Sidebar width management
    - Panel ordering
    - Panel visibility
    - Panel collapse/expand
    - Icons
    - Badges
    - Drag and drop
    - Resize
    - Auto hide
    """
    
    def __init__(self, config: Optional[SidebarConfig] = None):
        """
        Initialize sidebar UI manager.
        
        Args:
            config: Sidebar configuration
        """
        self.config = config or SidebarConfig()
        self.items: Dict[str, SidebarItem] = {}
        self.active_item_id: Optional[str] = None
        self.item_id_counter = 0
        self._next_item_id()
    
    def _next_item_id(self) -> str:
        """
        Generate next item ID.
        
        Returns:
            str: Item ID
        """
        self.item_id_counter += 1
        return f"item_{self.item_id_counter}"
    
    def add_item(self, item: SidebarItem) -> SidebarResult:
        """
        Add a sidebar item.
        
        Args:
            item: Sidebar item to add
            
        Returns:
            SidebarResult: Add result
        """
        result = SidebarResult(success=True)
        
        try:
            if not item.id:
                item.id = self._next_item_id()
            
            self.items[item.id] = item
            result.item = item
            result.items = self.get_all_items()
            result.message = f"Item '{item.id}' added"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def remove_item(self, item_id: str) -> SidebarResult:
        """
        Remove a sidebar item.
        
        Args:
            item_id: Item ID
            
        Returns:
            SidebarResult: Remove result
        """
        result = SidebarResult(success=False)
        
        try:
            if item_id in self.items:
                del self.items[item_id]
                if self.active_item_id == item_id:
                    self.active_item_id = None
                result.success = True
                result.items = self.get_all_items()
                result.message = f"Item '{item_id}' removed"
            else:
                result.errors.append("Item not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_item(self, item_id: str) -> Optional[SidebarItem]:
        """
        Get item by ID.
        
        Args:
            item_id: Item ID
            
        Returns:
            Optional[SidebarItem]: Item
        """
        return self.items.get(item_id)
    
    def get_all_items(self) -> List[SidebarItem]:
        """
        Get all items.
        
        Returns:
            List[SidebarItem]: All items
        """
        return sorted(self.items.values(), key=lambda x: x.order)
    
    def get_items_by_panel(self, panel: SidebarPanel) -> List[SidebarItem]:
        """
        Get items by panel type.
        
        Args:
            panel: Panel type
            
        Returns:
            List[SidebarItem]: Items
        """
        return [i for i in self.items.values() if i.panel == panel]
    
    def set_active_item(self, item_id: str) -> SidebarResult:
        """
        Set active item.
        
        Args:
            item_id: Item ID
            
        Returns:
            SidebarResult: Set result
        """
        result = SidebarResult(success=False)
        
        try:
            # Deactivate current active item
            if self.active_item_id and self.active_item_id in self.items:
                self.items[self.active_item_id].is_active = False
            
            # Activate new item
            if item_id in self.items:
                self.items[item_id].is_active = True
                self.active_item_id = item_id
                result.success = True
                result.item = self.items[item_id]
                result.message = f"Item '{item_id}' set as active"
            else:
                result.errors.append("Item not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def collapse_item(self, item_id: str) -> SidebarResult:
        """
        Collapse an item.
        
        Args:
            item_id: Item ID
            
        Returns:
            SidebarResult: Collapse result
        """
        result = SidebarResult(success=False)
        
        try:
            item = self.items.get(item_id)
            if item:
                item.is_collapsed = True
                result.success = True
                result.item = item
                result.message = f"Item '{item_id}' collapsed"
            else:
                result.errors.append("Item not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def expand_item(self, item_id: str) -> SidebarResult:
        """
        Expand an item.
        
        Args:
            item_id: Item ID
            
        Returns:
            SidebarResult: Expand result
        """
        result = SidebarResult(success=False)
        
        try:
            item = self.items.get(item_id)
            if item:
                item.is_collapsed = False
                result.success = True
                result.item = item
                result.message = f"Item '{item_id}' expanded"
            else:
                result.errors.append("Item not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def set_item_enabled(self, item_id: str, enabled: bool) -> SidebarResult:
        """
        Set item enabled state.
        
        Args:
            item_id: Item ID
            enabled: Enabled state
            
        Returns:
            SidebarResult: Set result
        """
        result = SidebarResult(success=False)
        
        try:
            item = self.items.get(item_id)
            if item:
                item.is_enabled = enabled
                result.success = True
                result.item = item
                result.message = f"Item '{item_id}' {'enabled' if enabled else 'disabled'}"
            else:
                result.errors.append("Item not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def set_item_visible(self, item_id: str, visible: bool) -> SidebarResult:
        """
        Set item visible state.
        
        Args:
            item_id: Item ID
            visible: Visible state
            
        Returns:
            SidebarResult: Set result
        """
        result = SidebarResult(success=False)
        
        try:
            item = self.items.get(item_id)
            if item:
                item.is_visible = visible
                result.success = True
                result.item = item
                result.message = f"Item '{item_id}' {'visible' if visible else 'hidden'}"
            else:
                result.errors.append("Item not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def reorder_item(self, item_id: str, new_order: int) -> SidebarResult:
        """
        Reorder an item.
        
        Args:
            item_id: Item ID
            new_order: New order
            
        Returns:
            SidebarResult: Reorder result
        """
        result = SidebarResult(success=False)
        
        try:
            item = self.items.get(item_id)
            if item:
                item.order = new_order
                result.success = True
                result.item = item
                result.message = f"Item '{item_id}' reordered to {new_order}"
            else:
                result.errors.append("Item not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def set_position(self, position: SidebarPosition) -> SidebarResult:
        """
        Set sidebar position.
        
        Args:
            position: Sidebar position
            
        Returns:
            SidebarResult: Set result
        """
        result = SidebarResult(success=True)
        
        try:
            self.config.position = position
            result.message = f"Position set to {position.value}"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def set_width(self, width: int) -> SidebarResult:
        """
        Set sidebar width.
        
        Args:
            width: Width in pixels
            
        Returns:
            SidebarResult: Set result
        """
        result = SidebarResult(success=True)
        
        try:
            if width < self.config.min_width or width > self.config.max_width:
                result.errors.append(f"Width must be between {self.config.min_width} and {self.config.max_width}")
                result.success = False
                return result
            
            self.config.width = width
            result.message = f"Width set to {width}"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def clear_all_items(self) -> SidebarResult:
        """
        Clear all items.
        
        Returns:
            SidebarResult: Clear result
        """
        result = SidebarResult(success=True)
        
        try:
            self.items.clear()
            self.active_item_id = None
            result.message = "All items cleared"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def update_config(self, config: SidebarConfig) -> SidebarResult:
        """
        Update sidebar configuration.
        
        Args:
            config: New configuration
            
        Returns:
            SidebarResult: Update result
        """
        result = SidebarResult(success=True)
        
        try:
            self.config = config
            result.message = "Config updated"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def get_config(self) -> SidebarConfig:
        """
        Get sidebar configuration.
        
        Returns:
            SidebarConfig: Configuration
        """
        return self.config


if __name__ == "__main__":
    # Basit test
    config = SidebarConfig()
    manager = SidebarUIManager(config)
    
    # Item ekle
    item = SidebarItem(
        id="",
        panel=SidebarPanel.FILE_EXPLORER,
        title="File Explorer",
        icon="folder"
    )
    
    result = manager.add_item(item)
    
    print(f"Item added: {result.message}")
    
    # Tüm item'ları al
    items = manager.get_all_items()
    
    print(f"Total items: {len(items)}")
