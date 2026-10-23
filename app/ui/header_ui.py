"""
MuhammedAI Local Developer - Header UI
Header UI system for web UI.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum


class HeaderAction(Enum):
    """Header action type."""
    MENU = "menu"
    BUTTON = "button"
    DROPDOWN = "dropdown"
    SEARCH = "search"
    LINK = "link"
    CUSTOM = "custom"


class HeaderPosition(Enum):
    """Header position."""
    TOP = "top"
    BOTTOM = "bottom"
    LEFT = "left"
    RIGHT = "right"
    CENTER = "center"
    CUSTOM = "custom"


@dataclass
class HeaderItem:
    """Header item."""
    id: str
    action: HeaderAction
    label: str
    icon: Optional[str] = None
    url: Optional[str] = None
    is_enabled: bool = True
    is_visible: bool = True
    is_active: bool = False
    badge: Optional[str] = None
    tooltip: Optional[str] = None
    position: HeaderPosition = HeaderPosition.RIGHT
    order: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class HeaderConfig:
    """Header configuration."""
    enabled: bool = True
    show_title: bool = True
    show_logo: bool = True
    show_search: bool = True
    show_user_menu: bool = True
    show_notifications: bool = True
    sticky: bool = False
    transparent: bool = False
    height: int = 60
    theme: str = "default"
    max_items: int = 10


@dataclass
class HeaderResult:
    """Header result."""
    success: bool
    item: Optional[HeaderItem] = None
    items: List[HeaderItem] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    message: Optional[str] = None


class HeaderUIManager:
    """
    Header UI manager.
    
    Özellikler:
    - Header items (menu, button, dropdown, search, link)
    - Header position (top, bottom, left, right, center)
    - Item ordering
    - Item visibility
    - Item badges
    - Tooltips
    - Logo
    - Title
    - Search
    - User menu
    - Notifications
    - Sticky header
    - Transparent header
    - Custom height
    """
    
    def __init__(self, config: Optional[HeaderConfig] = None):
        """
        Initialize header UI manager.
        
        Args:
            config: Header configuration
        """
        self.config = config or HeaderConfig()
        self.items: Dict[str, HeaderItem] = {}
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
    
    def add_item(self, item: HeaderItem) -> HeaderResult:
        """
        Add a header item.
        
        Args:
            item: Header item to add
            
        Returns:
            HeaderResult: Add result
        """
        result = HeaderResult(success=True)
        
        try:
            if len(self.items) >= self.config.max_items:
                result.errors.append(f"Maximum items reached (max {self.config.max_items})")
                result.success = False
                return result
            
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
    
    def remove_item(self, item_id: str) -> HeaderResult:
        """
        Remove a header item.
        
        Args:
            item_id: Item ID
            
        Returns:
            HeaderResult: Remove result
        """
        result = HeaderResult(success=False)
        
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
    
    def get_item(self, item_id: str) -> Optional[HeaderItem]:
        """
        Get item by ID.
        
        Args:
            item_id: Item ID
            
        Returns:
            Optional[HeaderItem]: Item
        """
        return self.items.get(item_id)
    
    def get_all_items(self) -> List[HeaderItem]:
        """
        Get all items.
        
        Returns:
            List[HeaderItem]: All items
        """
        return sorted(self.items.values(), key=lambda x: x.order)
    
    def get_items_by_action(self, action: HeaderAction) -> List[HeaderItem]:
        """
        Get items by action type.
        
        Args:
            action: Action type
            
        Returns:
            List[HeaderItem]: Items
        """
        return [i for i in self.items.values() if i.action == action]
    
    def set_active_item(self, item_id: str) -> HeaderResult:
        """
        Set active item.
        
        Args:
            item_id: Item ID
            
        Returns:
            HeaderResult: Set result
        """
        result = HeaderResult(success=False)
        
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
    
    def set_item_enabled(self, item_id: str, enabled: bool) -> HeaderResult:
        """
        Set item enabled state.
        
        Args:
            item_id: Item ID
            enabled: Enabled state
            
        Returns:
            HeaderResult: Set result
        """
        result = HeaderResult(success=False)
        
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
    
    def set_item_visible(self, item_id: str, visible: bool) -> HeaderResult:
        """
        Set item visible state.
        
        Args:
            item_id: Item ID
            visible: Visible state
            
        Returns:
            HeaderResult: Set result
        """
        result = HeaderResult(success=False)
        
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
    
    def set_item_badge(self, item_id: str, badge: Optional[str]) -> HeaderResult:
        """
        Set item badge.
        
        Args:
            item_id: Item ID
            badge: Badge text
            
        Returns:
            HeaderResult: Set result
        """
        result = HeaderResult(success=False)
        
        try:
            item = self.items.get(item_id)
            if item:
                item.badge = badge
                result.success = True
                result.item = item
                result.message = f"Item '{item_id}' badge set"
            else:
                result.errors.append("Item not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def set_item_tooltip(self, item_id: str, tooltip: Optional[str]) -> HeaderResult:
        """
        Set item tooltip.
        
        Args:
            item_id: Item ID
            tooltip: Tooltip text
            
        Returns:
            HeaderResult: Set result
        """
        result = HeaderResult(success=False)
        
        try:
            item = self.items.get(item_id)
            if item:
                item.tooltip = tooltip
                result.success = True
                result.item = item
                result.message = f"Item '{item_id}' tooltip set"
            else:
                result.errors.append("Item not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def reorder_item(self, item_id: str, new_order: int) -> HeaderResult:
        """
        Reorder an item.
        
        Args:
            item_id: Item ID
            new_order: New order
            
        Returns:
            HeaderResult: Reorder result
        """
        result = HeaderResult(success=False)
        
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
    
    def clear_all_items(self) -> HeaderResult:
        """
        Clear all items.
        
        Returns:
            HeaderResult: Clear result
        """
        result = HeaderResult(success=True)
        
        try:
            self.items.clear()
            self.active_item_id = None
            result.message = "All items cleared"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def update_config(self, config: HeaderConfig) -> HeaderResult:
        """
        Update header configuration.
        
        Args:
            config: New configuration
            
        Returns:
            HeaderResult: Update result
        """
        result = HeaderResult(success=True)
        
        try:
            self.config = config
            result.message = "Config updated"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def get_config(self) -> HeaderConfig:
        """
        Get header configuration.
        
        Returns:
            HeaderConfig: Configuration
        """
        return self.config


if __name__ == "__main__":
    # Basit test
    config = HeaderConfig()
    manager = HeaderUIManager(config)
    
    # Item ekle
    item = HeaderItem(
        id="",
        action=HeaderAction.BUTTON,
        label="Save",
        icon="save"
    )
    
    result = manager.add_item(item)
    
    print(f"Item added: {result.message}")
    
    # Tüm item'ları al
    items = manager.get_all_items()
    
    print(f"Total items: {len(items)}")
