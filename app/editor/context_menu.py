"""
MuhammedAI Local Developer - Context Menu
Context menu system for code editor.
"""

from typing import Dict, Any, Optional, List, Callable
from dataclasses import dataclass, field
from enum import Enum


class MenuItemType(Enum):
    """Menu item type."""
    ACTION = "action"
    SUBMENU = "submenu"
    SEPARATOR = "separator"
    CHECKBOX = "checkbox"
    RADIO = "radio"


@dataclass
class MenuItem:
    """Menu item."""
    id: str
    label: str
    type: MenuItemType = MenuItemType.ACTION
    icon: Optional[str] = None
    shortcut: Optional[str] = None
    is_enabled: bool = True
    is_visible: bool = True
    is_checked: bool = False
    action: Optional[Callable] = None
    submenu: Optional[List['MenuItem']] = None
    tooltip: Optional[str] = None


@dataclass
class ContextMenuConfig:
    """Context menu configuration."""
    show_icons: bool = True
    show_shortcuts: bool = True
    show_tooltips: bool = False
    enable_keyboard_navigation: bool = True
    max_menu_items: int = 20
    enable_animation: bool = True
    show_checkboxes: bool = True


@dataclass
class ContextMenuResult:
    """Context menu result."""
    success: bool
    items: List[MenuItem] = field(default_factory=list)
    selected_item: Optional[MenuItem] = None
    errors: List[str] = field(default_factory=list)
    message: Optional[str] = None


class ContextMenuManager:
    """
    Context menu manager.
    
    Özellikler:
    - Context menu items
    - Menu actions
    - Submenus
    - Menu separators
    - Checkboxes
    - Radio buttons
    - Menu icons
    - Shortcuts
    - Tooltips
    - Keyboard navigation
    - Menu filtering
    - Menu customization
    - Dynamic menus
    - Context-aware menus
    - Menu positioning
    - Menu animations
    - Menu state management
    """
    
    def __init__(self, config: Optional[ContextMenuConfig] = None):
        """
        Initialize context menu manager.
        
        Args:
            config: Context menu configuration
        """
        self.config = config or ContextMenuConfig()
        self.menu_items: Dict[str, MenuItem] = {}
        self._initialize_builtin_items()
    
    def _initialize_builtin_items(self) -> None:
        """Initialize built-in menu items."""
        # Cut
        self.add_menu_item(MenuItem(
            id="cut",
            label="Cut",
            icon="cut",
            shortcut="Ctrl+X"
        ))
        
        # Copy
        self.add_menu_item(MenuItem(
            id="copy",
            label="Copy",
            icon="copy",
            shortcut="Ctrl+C"
        ))
        
        # Paste
        self.add_menu_item(MenuItem(
            id="paste",
            label="Paste",
            icon="paste",
            shortcut="Ctrl+V"
        ))
        
        # Separator
        self.add_menu_item(MenuItem(
            id="separator_1",
            label="",
            type=MenuItemType.SEPARATOR
        ))
        
        # Undo
        self.add_menu_item(MenuItem(
            id="undo",
            label="Undo",
            icon="undo",
            shortcut="Ctrl+Z"
        ))
        
        # Redo
        self.add_menu_item(MenuItem(
            id="redo",
            label="Redo",
            icon="redo",
            shortcut="Ctrl+Y"
        ))
    
    def add_menu_item(self, item: MenuItem) -> ContextMenuResult:
        """
        Add menu item.
        
        Args:
            item: Menu item
            
        Returns:
            ContextMenuResult: Add result
        """
        result = ContextMenuResult(success=True)
        
        try:
            self.menu_items[item.id] = item
            result.items = self.get_all_items()
            result.message = f"Menu item '{item.id}' added"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def remove_menu_item(self, item_id: str) -> ContextMenuResult:
        """
        Remove menu item.
        
        Args:
            item_id: Item ID
            
        Returns:
            ContextMenuResult: Remove result
        """
        result = ContextMenuResult(success=False)
        
        try:
            if item_id in self.menu_items:
                del self.menu_items[item_id]
                result.success = True
                result.items = self.get_all_items()
                result.message = f"Menu item '{item_id}' removed"
            else:
                result.errors.append("Menu item not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_menu_item(self, item_id: str) -> Optional[MenuItem]:
        """
        Get menu item by ID.
        
        Args:
            item_id: Item ID
            
        Returns:
            Optional[MenuItem]: Menu item
        """
        return self.menu_items.get(item_id)
    
    def get_all_items(self) -> List[MenuItem]:
        """
        Get all menu items.
        
        Returns:
            List[MenuItem]: All items
        """
        return list(self.menu_items.values())
    
    def get_items_by_type(self, item_type: MenuItemType) -> List[MenuItem]:
        """
        Get items by type.
        
        Args:
            item_type: Item type
            
        Returns:
            List[MenuItem]: Items
        """
        return [item for item in self.menu_items.values() if item.type == item_type]
    
    def execute_action(self, item_id: str) -> ContextMenuResult:
        """
        Execute menu item action.
        
        Args:
            item_id: Item ID
            
        Returns:
            ContextMenuResult: Execution result
        """
        result = ContextMenuResult(success=False)
        
        try:
            item = self.menu_items.get(item_id)
            if item:
                if item.action and item.is_enabled:
                    item.action()
                    result.success = True
                    result.selected_item = item
                    result.message = f"Action '{item.label}' executed"
                elif not item.is_enabled:
                    result.errors.append("Item is disabled")
                else:
                    result.errors.append("No action defined")
            else:
                result.errors.append("Menu item not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def set_item_enabled(self, item_id: str, enabled: bool) -> ContextMenuResult:
        """
        Set item enabled state.
        
        Args:
            item_id: Item ID
            enabled: Enabled state
            
        Returns:
            ContextMenuResult: Set result
        """
        result = ContextMenuResult(success=False)
        
        try:
            item = self.menu_items.get(item_id)
            if item:
                item.is_enabled = enabled
                result.success = True
                result.message = f"Item '{item_id}' {'enabled' if enabled else 'disabled'}"
            else:
                result.errors.append("Menu item not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def set_item_visible(self, item_id: str, visible: bool) -> ContextMenuResult:
        """
        Set item visible state.
        
        Args:
            item_id: Item ID
            visible: Visible state
            
        Returns:
            ContextMenuResult: Set result
        """
        result = ContextMenuResult(success=False)
        
        try:
            item = self.menu_items.get(item_id)
            if item:
                item.is_visible = visible
                result.success = True
                result.message = f"Item '{item_id}' {'visible' if visible else 'hidden'}"
            else:
                result.errors.append("Menu item not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def set_item_checked(self, item_id: str, checked: bool) -> ContextMenuResult:
        """
        Set item checked state.
        
        Args:
            item_id: Item ID
            checked: Checked state
            
        Returns:
            ContextMenuResult: Set result
        """
        result = ContextMenuResult(success=False)
        
        try:
            item = self.menu_items.get(item_id)
            if item:
                item.is_checked = checked
                result.success = True
                result.message = f"Item '{item_id}' {'checked' if checked else 'unchecked'}"
            else:
                result.errors.append("Menu item not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_visible_items(self) -> List[MenuItem]:
        """
        Get visible items.
        
        Returns:
            List[MenuItem]: Visible items
        """
        return [item for item in self.menu_items.values() if item.is_visible]
    
    def get_enabled_items(self) -> List[MenuItem]:
        """
        Get enabled items.
        
        Returns:
            List[MenuItem]: Enabled items
        """
        return [item for item in self.menu_items.values() if item.is_enabled]
    
    def update_config(self, config: ContextMenuConfig) -> ContextMenuResult:
        """
        Update context menu configuration.
        
        Args:
            config: New configuration
            
        Returns:
            ContextMenuResult: Update result
        """
        result = ContextMenuResult(success=True)
        
        try:
            self.config = config
            result.message = "Config updated"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def get_config(self) -> ContextMenuConfig:
        """
        Get context menu configuration.
        
        Returns:
            ContextMenuConfig: Configuration
        """
        return self.config


if __name__ == "__main__":
    # Basit test
    config = ContextMenuConfig()
    manager = ContextMenuManager(config)
    
    # Menu item ekle
    item = MenuItem(
        id="custom",
        label="Custom Action",
        icon="custom"
    )
    
    result = manager.add_menu_item(item)
    
    print(f"Menu item added: {result.message}")
    
    # Tüm item'ları al
    items = manager.get_all_items()
    
    print(f"Total menu items: {len(items)}")
    for item in items:
        print(f"  - {item.label}")
