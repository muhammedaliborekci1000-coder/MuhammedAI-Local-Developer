"""
MuhammedAI Local Developer - Breadcrumbs
Breadcrumbs system for code editor.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum


class BreadcrumbType(Enum):
    """Breadcrumb type."""
    FILE = "file"
    SYMBOL = "symbol"
    DIRECTORY = "directory"
    PROJECT = "project"


class BreadcrumbSeparator(Enum):
    """Breadcrumb separator."""
    ARROW = "arrow"
    SLASH = "slash"
    DOT = "dot"
    NONE = "none"


@dataclass
class BreadcrumbItem:
    """Breadcrumb item."""
    id: str
    label: str
    type: BreadcrumbType
    path: Optional[str] = None
    line: Optional[int] = None
    icon: Optional[str] = None
    tooltip: Optional[str] = None
    is_clickable: bool = True
    is_active: bool = False


@dataclass
class BreadcrumbConfig:
    """Breadcrumb configuration."""
    enabled: bool = True
    show_file_breadcrumbs: bool = True
    show_symbol_breadcrumbs: bool = True
    separator: BreadcrumbSeparator = BreadcrumbSeparator.ARROW
    max_items: int = 10
    truncate_long_paths: bool = True
    max_path_length: int = 50
    show_icons: bool = True
    show_tooltips: bool = True
    enable_navigation: bool = True


@dataclass
class BreadcrumbResult:
    """Breadcrumb result."""
    success: bool
    items: List[BreadcrumbItem] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    message: Optional[str] = None


class BreadcrumbManager:
    """
    Breadcrumb manager.
    
    Özellikler:
    - Breadcrumb navigation
    - File path breadcrumbs
    - Symbol breadcrumbs
    - Clickable breadcrumbs
    - Breadcrumb customization
    - Breadcrumb filtering
    - Breadcrumb history
    - Breadcrumb icons
    - Breadcrumb separators
    - Breadcrumb truncation
    - Breadcrumb tooltips
    - Breadcrumb context menu
    - Breadcrumb navigation actions
    - Breadcrumb visibility
    - Breadcrumb ordering
    - Breadcrumb highlighting
    """
    
    def __init__(self, config: Optional[BreadcrumbConfig] = None):
        """
        Initialize breadcrumb manager.
        
        Args:
            config: Breadcrumb configuration
        """
        self.config = config or BreadcrumbConfig()
        self.current_items: List[BreadcrumbItem] = []
        self.navigation_history: List[List[BreadcrumbItem]] = []
    
    def generate_file_breadcrumbs(self, file_path: str) -> BreadcrumbResult:
        """
        Generate file path breadcrumbs.
        
        Args:
            file_path: File path
            
        Returns:
            BreadcrumbResult: Generation result
        """
        result = BreadcrumbResult(success=True)
        
        if not self.config.enabled or not self.config.show_file_breadcrumbs:
            result.message = "File breadcrumbs disabled"
            return result
        
        try:
            items = []
            
            # Split path
            parts = file_path.replace('\\', '/').split('/')
            
            for i, part in enumerate(parts):
                if not part:
                    continue
                
                # Determine type
                breadcrumb_type = BreadcrumbType.DIRECTORY if i < len(parts) - 1 else BreadcrumbType.FILE
                
                # Truncate if needed
                label = part
                if self.config.truncate_long_paths and len(part) > 20:
                    label = part[:17] + "..."
                
                item = BreadcrumbItem(
                    id=f"breadcrumb_{i}",
                    label=label,
                    type=breadcrumb_type,
                    path='/'.join(parts[:i+1]),
                    icon=self._get_icon_for_type(breadcrumb_type),
                    is_clickable=True,
                    is_active=(i == len(parts) - 1)
                )
                
                items.append(item)
            
            # Limit items
            if len(items) > self.config.max_items:
                items = items[-self.config.max_items:]
            
            self.current_items = items
            result.items = items
            result.message = f"Generated {len(items)} breadcrumbs"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def generate_symbol_breadcrumbs(self, code: str, current_line: int) -> BreadcrumbResult:
        """
        Generate symbol breadcrumbs from code.
        
        Args:
            code: Code content
            current_line: Current line number
            
        Returns:
            BreadcrumbResult: Generation result
        """
        result = BreadcrumbResult(success=True)
        
        if not self.config.enabled or not self.config.show_symbol_breadcrumbs:
            result.message = "Symbol breadcrumbs disabled"
            return result
        
        try:
            items = []
            lines = code.splitlines()
            
            # Simple symbol detection
            for i, line in enumerate(lines):
                if i > current_line:
                    break
                
                # Detect class/function
                stripped = line.strip()
                if stripped.startswith('class '):
                    class_name = stripped[6:].split('(')[0].split(':')[0].strip()
                    item = BreadcrumbItem(
                        id=f"symbol_{i}",
                        label=class_name,
                        type=BreadcrumbType.SYMBOL,
                        line=i,
                        icon="class",
                        is_clickable=True
                    )
                    items.append(item)
                elif stripped.startswith('def '):
                    func_name = stripped[4:].split('(')[0].strip()
                    item = BreadcrumbItem(
                        id=f"symbol_{i}",
                        label=func_name,
                        type=BreadcrumbType.SYMBOL,
                        line=i,
                        icon="function",
                        is_clickable=True
                    )
                    items.append(item)
            
            self.current_items = items
            result.items = items
            result.message = f"Generated {len(items)} symbol breadcrumbs"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def _get_icon_for_type(self, breadcrumb_type: BreadcrumbType) -> Optional[str]:
        """
        Get icon for breadcrumb type.
        
        Args:
            breadcrumb_type: Breadcrumb type
            
        Returns:
            Optional[str]: Icon name
        """
        icon_map = {
            BreadcrumbType.FILE: "file",
            BreadcrumbType.SYMBOL: "symbol",
            BreadcrumbType.DIRECTORY: "folder",
            BreadcrumbType.PROJECT: "project"
        }
        return icon_map.get(breadcrumb_type)
    
    def navigate_to_breadcrumb(self, breadcrumb_id: str) -> BreadcrumbResult:
        """
        Navigate to breadcrumb.
        
        Args:
            breadcrumb_id: Breadcrumb ID
            
        Returns:
            BreadcrumbResult: Navigation result
        """
        result = BreadcrumbResult(success=False)
        
        try:
            for item in self.current_items:
                if item.id == breadcrumb_id:
                    # Add to history
                    self._add_to_history()
                    
                    # Set as active
                    for i in self.current_items:
                        i.is_active = False
                    item.is_active = True
                    
                    result.success = True
                    result.message = f"Navigated to {item.label}"
                    return result
            
            result.errors.append("Breadcrumb not found")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def _add_to_history(self) -> None:
        """Add current items to history."""
        if self.current_items:
            self.navigation_history.append(list(self.current_items))
            
            # Limit history
            if len(self.navigation_history) > 50:
                self.navigation_history = self.navigation_history[-50:]
    
    def get_navigation_history(self) -> List[List[BreadcrumbItem]]:
        """
        Get navigation history.
        
        Returns:
            List[List[BreadcrumbItem]]: Navigation history
        """
        return self.navigation_history
    
    def clear_history(self) -> None:
        """Clear navigation history."""
        self.navigation_history.clear()
    
    def get_current_items(self) -> List[BreadcrumbItem]:
        """
        Get current breadcrumb items.
        
        Returns:
            List[BreadcrumbItem]: Current items
        """
        return self.current_items
    
    def set_separator(self, separator: BreadcrumbSeparator) -> BreadcrumbResult:
        """
        Set breadcrumb separator.
        
        Args:
            separator: Separator type
            
        Returns:
            BreadcrumbResult: Set result
        """
        result = BreadcrumbResult(success=True)
        
        try:
            self.config.separator = separator
            result.message = f"Separator set to {separator.value}"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def update_config(self, config: BreadcrumbConfig) -> BreadcrumbResult:
        """
        Update breadcrumb configuration.
        
        Args:
            config: New configuration
            
        Returns:
            BreadcrumbResult: Update result
        """
        result = BreadcrumbResult(success=True)
        
        try:
            self.config = config
            result.message = "Config updated"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def get_config(self) -> BreadcrumbConfig:
        """
        Get breadcrumb configuration.
        
        Returns:
            BreadcrumbConfig: Configuration
        """
        return self.config


if __name__ == "__main__":
    # Basit test
    config = BreadcrumbConfig()
    manager = BreadcrumbManager(config)
    
    # File breadcrumbs
    result = manager.generate_file_breadcrumbs("src/app/editor/main.py")
    
    print(f"Generated {len(result.items)} breadcrumbs")
    for item in result.items:
        print(f"  - {item.label} ({item.type.value})")
