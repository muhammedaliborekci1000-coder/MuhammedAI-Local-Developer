"""
MuhammedAI Local Developer - Status Bar
Status bar system for code editor.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum


class StatusItemPosition(Enum):
    """Status item position."""
    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"


class StatusItemPriority(Enum):
    """Status item priority."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class StatusItem:
    """Status bar item."""
    id: str
    label: str
    position: StatusItemPosition = StatusItemPosition.LEFT
    priority: StatusItemPriority = StatusItemPriority.MEDIUM
    icon: Optional[str] = None
    tooltip: Optional[str] = None
    is_clickable: bool = False
    is_visible: bool = True
    value: Optional[str] = None


@dataclass
class StatusBarConfig:
    """Status bar configuration."""
    enabled: bool = True
    show_line_column: bool = True
    show_file_encoding: bool = True
    show_file_type: bool = True
    show_git_branch: bool = True
    show_indentation: bool = True
    show_language: bool = True
    show_cursor_position: bool = True
    show_selection_info: bool = True
    max_items_per_section: int = 5


@dataclass
class StatusBarResult:
    """Status bar result."""
    success: bool
    items: List[StatusItem] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    message: Optional[str] = None


class StatusBarManager:
    """
    Status bar manager.
    
    Özellikler:
    - Status bar items
    - Line/column display
    - File encoding
    - File type
    - Git branch
    - Indentation
    - Language
    - Cursor position
    - Selection info
    - Custom items
    - Item positioning
    - Item priority
    - Clickable items
    - Item tooltips
    - Item visibility
    - Status bar customization
    - Dynamic updates
    """
    
    def __init__(self, config: Optional[StatusBarConfig] = None):
        """
        Initialize status bar manager.
        
        Args:
            config: Status bar configuration
        """
        self.config = config or StatusBarConfig()
        self.items: Dict[str, StatusItem] = {}
        self._initialize_builtin_items()
    
    def _initialize_builtin_items(self) -> None:
        """Initialize built-in status bar items."""
        # Line/Column
        if self.config.show_line_column:
            self.add_item(StatusItem(
                id="line_column",
                label="Ln 1, Col 1",
                position=StatusItemPosition.LEFT,
                priority=StatusItemPriority.HIGH,
                icon="location"
            ))
        
        # File encoding
        if self.config.show_file_encoding:
            self.add_item(StatusItem(
                id="encoding",
                label="UTF-8",
                position=StatusItemPosition.RIGHT,
                priority=StatusItemPriority.LOW,
                icon="encoding"
            ))
        
        # File type
        if self.config.show_file_type:
            self.add_item(StatusItem(
                id="file_type",
                label="Python",
                position=StatusItemPosition.RIGHT,
                priority=StatusItemPriority.MEDIUM,
                icon="file"
            ))
        
        # Git branch
        if self.config.show_git_branch:
            self.add_item(StatusItem(
                id="git_branch",
                label="main",
                position=StatusItemPosition.RIGHT,
                priority=StatusItemPriority.HIGH,
                icon="git"
            ))
        
        # Indentation
        if self.config.show_indentation:
            self.add_item(StatusItem(
                id="indentation",
                label="Spaces: 4",
                position=StatusItemPosition.RIGHT,
                priority=StatusItemPriority.LOW,
                icon="indent"
            ))
        
        # Language
        if self.config.show_language:
            self.add_item(StatusItem(
                id="language",
                label="Python",
                position=StatusItemPosition.RIGHT,
                priority=StatusItemPriority.MEDIUM,
                icon="language"
            ))
    
    def add_item(self, item: StatusItem) -> StatusBarResult:
        """
        Add status bar item.
        
        Args:
            item: Status item
            
        Returns:
            StatusBarResult: Add result
        """
        result = StatusBarResult(success=True)
        
        try:
            self.items[item.id] = item
            result.items = self.get_items()
            result.message = f"Item '{item.id}' added"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def remove_item(self, item_id: str) -> StatusBarResult:
        """
        Remove status bar item.
        
        Args:
            item_id: Item ID
            
        Returns:
            StatusBarResult: Remove result
        """
        result = StatusBarResult(success=False)
        
        try:
            if item_id in self.items:
                del self.items[item_id]
                result.success = True
                result.items = self.get_items()
                result.message = f"Item '{item_id}' removed"
            else:
                result.errors.append("Item not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_item(self, item_id: str) -> Optional[StatusItem]:
        """
        Get status bar item.
        
        Args:
            item_id: Item ID
            
        Returns:
            Optional[StatusItem]: Status item
        """
        return self.items.get(item_id)
    
    def get_items(self) -> List[StatusItem]:
        """
        Get all status bar items.
        
        Returns:
            List[StatusItem]: All items
        """
        return list(self.items.values())
    
    def get_items_by_position(self, position: StatusItemPosition) -> List[StatusItem]:
        """
        Get items by position.
        
        Args:
            position: Position
            
        Returns:
            List[StatusItem]: Items
        """
        items = [item for item in self.items.values() if item.position == position]
        
        # Sort by priority
        priority_order = {StatusItemPriority.HIGH: 0, StatusItemPriority.MEDIUM: 1, StatusItemPriority.LOW: 2}
        items.sort(key=lambda x: priority_order.get(x.priority, 999))
        
        # Limit items
        if len(items) > self.config.max_items_per_section:
            items = items[:self.config.max_items_per_section]
        
        return items
    
    def update_item(self, item_id: str, label: Optional[str] = None, value: Optional[str] = None) -> StatusBarResult:
        """
        Update status bar item.
        
        Args:
            item_id: Item ID
            label: New label
            value: New value
            
        Returns:
            StatusBarResult: Update result
        """
        result = StatusBarResult(success=False)
        
        try:
            if item_id in self.items:
                item = self.items[item_id]
                if label is not None:
                    item.label = label
                if value is not None:
                    item.value = value
                
                result.success = True
                result.items = self.get_items()
                result.message = f"Item '{item_id}' updated"
            else:
                result.errors.append("Item not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def set_line_column(self, line: int, column: int) -> StatusBarResult:
        """
        Set line and column.
        
        Args:
            line: Line number
            column: Column number
            
        Returns:
            StatusBarResult: Set result
        """
        return self.update_item("line_column", label=f"Ln {line}, Col {column}")
    
    def set_file_encoding(self, encoding: str) -> StatusBarResult:
        """
        Set file encoding.
        
        Args:
            encoding: Encoding
            
        Returns:
            StatusBarResult: Set result
        """
        return self.update_item("encoding", label=encoding)
    
    def set_file_type(self, file_type: str) -> StatusBarResult:
        """
        Set file type.
        
        Args:
            file_type: File type
            
        Returns:
            StatusBarResult: Set result
        """
        return self.update_item("file_type", label=file_type)
    
    def set_git_branch(self, branch: str) -> StatusBarResult:
        """
        Set git branch.
        
        Args:
            branch: Branch name
            
        Returns:
            StatusBarResult: Set result
        """
        return self.update_item("git_branch", label=branch)
    
    def set_indentation(self, indent_type: str, indent_size: int) -> StatusBarResult:
        """
        Set indentation.
        
        Args:
            indent_type: Indent type (Spaces/Tabs)
            indent_size: Indent size
            
        Returns:
            StatusBarResult: Set result
        """
        return self.update_item("indentation", label=f"{indent_type}: {indent_size}")
    
    def set_language(self, language: str) -> StatusBarResult:
        """
        Set language.
        
        Args:
            language: Language
            
        Returns:
            StatusBarResult: Set result
        """
        return self.update_item("language", label=language)
    
    def update_config(self, config: StatusBarConfig) -> StatusBarResult:
        """
        Update status bar configuration.
        
        Args:
            config: New configuration
            
        Returns:
            StatusBarResult: Update result
        """
        result = StatusBarResult(success=True)
        
        try:
            self.config = config
            result.message = "Config updated"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def get_config(self) -> StatusBarConfig:
        """
        Get status bar configuration.
        
        Returns:
            StatusBarConfig: Configuration
        """
        return self.config


if __name__ == "__main__":
    # Basit test
    config = StatusBarConfig()
    manager = StatusBarManager(config)
    
    # Line/Column güncelle
    manager.set_line_column(10, 5)
    
    # Tüm item'ları al
    items = manager.get_items()
    
    print(f"Status bar items: {len(items)}")
    for item in items:
        print(f"  - {item.label}")
