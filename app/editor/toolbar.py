"""
MuhammedAI Local Developer - Toolbar
Toolbar system for code editor.
"""

from typing import Dict, Any, Optional, List, Callable
from dataclasses import dataclass, field
from enum import Enum


class ToolbarItemPosition(Enum):
    """Toolbar item position."""
    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"


class ToolbarItemType(Enum):
    """Toolbar item type."""
    BUTTON = "button"
    SEPARATOR = "separator"
    DROPDOWN = "dropdown"
    TOGGLE = "toggle"
    INPUT = "input"


@dataclass
class ToolbarItem:
    """Toolbar item."""
    id: str
    title: str
    type: ToolbarItemType = ToolbarItemType.BUTTON
    icon: Optional[str] = None
    shortcut: Optional[str] = None
    tooltip: Optional[str] = None
    is_enabled: bool = True
    is_visible: bool = True
    is_checked: bool = False
    position: ToolbarItemPosition = ToolbarItemPosition.LEFT
    priority: int = 0
    action: Optional[Callable] = None
    items: List['ToolbarItem'] = field(default_factory=list)


@dataclass
class ToolbarConfig:
    """Toolbar configuration."""
    show_icons: bool = True
    show_shortcuts: bool = True
    show_tooltips: bool = True
    position: ToolbarItemPosition = ToolbarItemPosition.LEFT
    enable_keyboard_navigation: bool = True
    max_items: int = 20
    enable_animation: bool = True
    show_separator: bool = True


@dataclass
class ToolbarResult:
    """Toolbar result."""
    success: bool
    items: List[ToolbarItem] = field(default_factory=list)
    selected_item: Optional[ToolbarItem] = None
    errors: List[str] = field(default_factory=list)
    message: Optional[str] = None


class ToolbarManager:
    """
    Toolbar manager.
    
    Özellikler:
    - Toolbar items
    - Toolbar actions
    - Toolbar separators
    - Toolbar dropdowns
    - Toolbar toggles
    - Toolbar positioning
    - Toolbar priority
    - Toolbar filtering
    - Toolbar visibility
    - Toolbar animations
    - Toolbar icons
    - Toolbar shortcuts
    - Toolbar tooltips
    - Toolbar scope
    - Toolbar context
    - Custom toolbar items
    """
    
    def __init__(self, config: Optional[ToolbarConfig] = None):
        """
        Initialize toolbar manager.
        
        Args:
            config: Toolbar configuration
        """
        self.config = config or ToolbarConfig()
        self.toolbar_items: Dict[str, ToolbarItem] = {}
        self._initialize_builtin_items()
    
    def _initialize_builtin_items(self) -> None:
        """Initialize built-in toolbar items."""
        # Save
        self.add_toolbar_item(ToolbarItem(
            id="save",
            title="Save",
            icon="save",
            shortcut="Ctrl+S",
            position=ToolbarItemPosition.LEFT
        ))
        
        # Undo
        self.add_toolbar_item(ToolbarItem(
            id="undo",
            title="Undo",
            icon="undo",
            shortcut="Ctrl+Z",
            position=ToolbarItemPosition.LEFT
        ))
        
        # Redo
        self.add_toolbar_item(ToolbarItem(
            id="redo",
            title="Redo",
            icon="redo",
            shortcut="Ctrl+Y",
            position=ToolbarItemPosition.LEFT
        ))
        
        # Separator
        self.add_toolbar_item(ToolbarItem(
            id="separator_1",
            title="",
            type=ToolbarItemType.SEPARATOR,
            position=ToolbarItemPosition.LEFT
        ))
        
        # Cut
        self.add_toolbar_item(ToolbarItem(
            id="cut",
            title="Cut",
            icon="cut",
            shortcut="Ctrl+X",
            position=ToolbarItemPosition.LEFT
        ))
        
        # Copy
        self.add_toolbar_item(ToolbarItem(
            id="copy",
            title="Copy",
            icon="copy",
            shortcut="Ctrl+C",
            position=ToolbarItemPosition.LEFT
        ))
        
        # Paste
        self.add_toolbar_item(ToolbarItem(
            id="paste",
            title="Paste",
            icon="paste",
            shortcut="Ctrl+V",
            position=ToolbarItemPosition.LEFT
        ))
    
    def add_toolbar_item(self, item: ToolbarItem) -> ToolbarResult:
        """
        Add toolbar item.
        
        Args:
            item: Toolbar item
            
        Returns:
            ToolbarResult: Add result
        """
        result = ToolbarResult(success=True)
        
        try:
            self.toolbar_items[item.id] = item
            result.items = self.get_all_items()
            result.message = f"Toolbar item '{item.id}' added"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def remove_toolbar_item(self, item_id: str) -> ToolbarResult:
        """
        Remove toolbar item.
        
        Args:
            item_id: Item ID
            
        Returns:
            ToolbarResult: Remove result
        """
        result = ToolbarResult(success=False)
        
        try:
            if item_id in self.toolbar_items:
                del self.toolbar_items[item_id]
                result.success = True
                result.items = self.get_all_items()
                result.message = f"Toolbar item '{item_id}' removed"
            else:
                result.errors.append("Toolbar item not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_toolbar_item(self, item_id: str) -> Optional[ToolbarItem]:
        """
        Get toolbar item by ID.
        
        Args:
            item_id: Item ID
            
        Returns:
            Optional[ToolbarItem]: Toolbar item
        """
        return self.toolbar_items.get(item_id)
    
    def get_all_items(self) -> List[ToolbarItem]:
        """
        Get all toolbar items.
        
        Returns:
            List[ToolbarItem]: All items
        """
        return list(self.toolbar_items.values())
    
    def get_items_by_type(self, item_type: ToolbarItemType) -> List[ToolbarItem]:
        """
        Get items by type.
        
        Args:
            item_type: Item type
            
        Returns:
            List[ToolbarItem]: Items
        """
        return [item for item in self.toolbar_items.values() if item.type == item_type]
    
    def get_items_by_position(self, position: ToolbarItemPosition) -> List[ToolbarItem]:
        """
        Get items by position.
        
        Args:
            position: Item position
            
        Returns:
            List[ToolbarItem]: Items
        """
        return [item for item in self.toolbar_items.values() if item.position == position]
    
    def execute_action(self, item_id: str) -> ToolbarResult:
        """
        Execute toolbar item action.
        
        Args:
            item_id: Item ID
            
        Returns:
            ToolbarResult: Execution result
        """
        result = ToolbarResult(success=False)
        
        try:
            item = self.toolbar_items.get(item_id)
            if item:
                if item.action and item.is_enabled:
                    item.action()
                    result.success = True
                    result.selected_item = item
                    result.message = f"Action '{item.title}' executed"
                elif not item.is_enabled:
                    result.errors.append("Item is disabled")
                else:
                    result.errors.append("No action defined")
            else:
                result.errors.append("Toolbar item not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def set_item_enabled(self, item_id: str, enabled: bool) -> ToolbarResult:
        """
        Set item enabled state.
        
        Args:
            item_id: Item ID
            enabled: Enabled state
            
        Returns:
            ToolbarResult: Set result
        """
        result = ToolbarResult(success=False)
        
        try:
            item = self.toolbar_items.get(item_id)
            if item:
                item.is_enabled = enabled
                result.success = True
                result.message = f"Item '{item_id}' {'enabled' if enabled else 'disabled'}"
            else:
                result.errors.append("Toolbar item not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def set_item_visible(self, item_id: str, visible: bool) -> ToolbarResult:
        """
        Set item visible state.
        
        Args:
            item_id: Item ID
            visible: Visible state
            
        Returns:
            ToolbarResult: Set result
        """
        result = ToolbarResult(success=False)
        
        try:
            item = self.toolbar_items.get(item_id)
            if item:
                item.is_visible = visible
                result.success = True
                result.message = f"Item '{item_id}' {'visible' if visible else 'hidden'}"
            else:
                result.errors.append("Toolbar item not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def set_item_checked(self, item_id: str, checked: bool) -> ToolbarResult:
        """
        Set item checked state.
        
        Args:
            item_id: Item ID
            checked: Checked state
            
        Returns:
            ToolbarResult: Set result
        """
        result = ToolbarResult(success=False)
        
        try:
            item = self.toolbar_items.get(item_id)
            if item:
                item.is_checked = checked
                result.success = True
                result.message = f"Item '{item_id}' {'checked' if checked else 'unchecked'}"
            else:
                result.errors.append("Toolbar item not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_visible_items(self) -> List[ToolbarItem]:
        """
        Get visible items.
        
        Returns:
            List[ToolbarItem]: Visible items
        """
        return [item for item in self.toolbar_items.values() if item.is_visible]
    
    def get_enabled_items(self) -> List[ToolbarItem]:
        """
        Get enabled items.
        
        Returns:
            List[ToolbarItem]: Enabled items
        """
        return [item for item in self.toolbar_items.values() if item.is_enabled]
    
    def update_config(self, config: ToolbarConfig) -> ToolbarResult:
        """
        Update toolbar configuration.
        
        Args:
            config: New configuration
            
        Returns:
            ToolbarResult: Update result
        """
        result = ToolbarResult(success=True)
        
        try:
            self.config = config
            result.message = "Config updated"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def get_config(self) -> ToolbarConfig:
        """
        Get toolbar configuration.
        
        Returns:
            ToolbarConfig: Configuration
        """
        return self.config


if __name__ == "__main__":
    # Basit test
    config = ToolbarConfig()
    manager = ToolbarManager(config)
    
    # Toolbar item ekle
    item = ToolbarItem(
        id="custom",
        title="Custom Action",
        icon="custom"
    )
    
    result = manager.add_toolbar_item(item)
    
    print(f"Toolbar item added: {result.message}")
    
    # Tüm item'ları al
    items = manager.get_all_items()
    
    print(f"Total toolbar items: {len(items)}")
    for item in items:
        print(f"  - {item.title}")
