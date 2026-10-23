"""
MuhammedAI Local Developer - Code Navigation
Code navigation system for code editor.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum


class NavigationType(Enum):
    """Navigation type."""
    DEFINITION = "definition"
    REFERENCE = "reference"
    IMPLEMENTATION = "implementation"
    TYPE_DEFINITION = "type_definition"
    DECLARATION = "declaration"


class NavigationMode(Enum):
    """Navigation mode."""
    SINGLE_FILE = "single_file"
    MULTI_FILE = "multi_file"
    PROJECT_WIDE = "project_wide"


@dataclass
class NavigationLocation:
    """Navigation location."""
    file_path: str
    line: int
    column: int
    symbol_name: Optional[str] = None


@dataclass
class NavigationTarget:
    """Navigation target."""
    id: str
    type: NavigationType
    location: NavigationLocation
    is_enabled: bool = True
    is_visible: bool = True


@dataclass
class NavigationHistory:
    """Navigation history."""
    locations: List[NavigationLocation] = field(default_factory=list)
    current_index: int = -1
    max_history: int = 100


@dataclass
class NavigationConfig:
    """Navigation configuration."""
    enabled: bool = True
    mode: NavigationMode = NavigationMode.PROJECT_WIDE
    enable_history: bool = True
    max_history: int = 100
    enable_preview: bool = True
    enable_cross_file: bool = True
    enable_goto_definition: bool = True
    enable_goto_reference: bool = True
    enable_goto_implementation: bool = True
    enable_goto_type_definition: bool = True


@dataclass
class NavigationResult:
    """Navigation result."""
    success: bool
    target: Optional[NavigationTarget] = None
    history: Optional[NavigationHistory] = None
    errors: List[str] = field(default_factory=list)
    message: Optional[str] = None


class CodeNavigationManager:
    """
    Code navigation manager.
    
    Özellikler:
    - Go to definition
    - Go to references
    - Go to implementation
    - Go to type definition
    - Go to declaration
    - Navigation history
    - Navigation back/forward
    - Navigation bookmarks
    - Navigation scope
    - Navigation context
    - Cross-file navigation
    - Project-wide navigation
    """
    
    def __init__(self, config: Optional[NavigationConfig] = None):
        """
        Initialize code navigation manager.
        
        Args:
            config: Navigation configuration
        """
        self.config = config or NavigationConfig()
        self.targets: Dict[str, NavigationTarget] = {}
        self.history = NavigationHistory()
        self.target_id_counter = 0
        self._next_id()
    
    def _next_id(self) -> str:
        """
        Generate next target ID.
        
        Returns:
            str: Target ID
        """
        self.target_id_counter += 1
        return f"target_{self.target_id_counter}"
    
    def add_target(self, target: NavigationTarget) -> NavigationResult:
        """
        Add a navigation target.
        
        Args:
            target: Target to add
            
        Returns:
            NavigationResult: Add result
        """
        result = NavigationResult(success=True)
        
        try:
            if not target.id:
                target.id = self._next_id()
            
            self.targets[target.id] = target
            result.target = target
            result.message = f"Target '{target.id}' added"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def remove_target(self, target_id: str) -> NavigationResult:
        """
        Remove a navigation target.
        
        Args:
            target_id: Target ID
            
        Returns:
            NavigationResult: Remove result
        """
        result = NavigationResult(success=False)
        
        try:
            if target_id in self.targets:
                del self.targets[target_id]
                result.success = True
                result.message = f"Target '{target_id}' removed"
            else:
                result.errors.append("Target not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_target(self, target_id: str) -> Optional[NavigationTarget]:
        """
        Get target by ID.
        
        Args:
            target_id: Target ID
            
        Returns:
            Optional[NavigationTarget]: Target
        """
        return self.targets.get(target_id)
    
    def get_all_targets(self) -> List[NavigationTarget]:
        """
        Get all targets.
        
        Returns:
            List[NavigationTarget]: All targets
        """
        return list(self.targets.values())
    
    def get_targets_by_type(self, nav_type: NavigationType) -> List[NavigationTarget]:
        """
        Get targets by type.
        
        Args:
            nav_type: Navigation type
            
        Returns:
            List[NavigationTarget]: Targets
        """
        return [t for t in self.targets.values() if t.type == nav_type]
    
    def navigate_to(self, location: NavigationLocation, nav_type: NavigationType = NavigationType.DEFINITION) -> NavigationResult:
        """
        Navigate to location.
        
        Args:
            location: Navigation location
            nav_type: Navigation type
            
        Returns:
            NavigationResult: Navigation result
        """
        result = NavigationResult(success=True)
        
        try:
            if not self.config.enabled:
                result.errors.append("Navigation disabled")
                result.success = False
                return result
            
            target = NavigationTarget(
                id="",
                type=nav_type,
                location=location
            )
            
            add_result = self.add_target(target)
            
            if add_result.success:
                result.target = add_result.target
                result.message = f"Navigated to {location.file_path}:{location.line}:{location.column}"
                
                # Add to history
                if self.config.enable_history:
                    self._add_to_history(location)
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def go_to_definition(self, location: NavigationLocation) -> NavigationResult:
        """
        Go to definition.
        
        Args:
            location: Current location
            
        Returns:
            NavigationResult: Navigation result
        """
        if not self.config.enable_goto_definition:
            result = NavigationResult(success=False)
            result.message = "Go to definition disabled"
            return result
        
        return self.navigate_to(location, NavigationType.DEFINITION)
    
    def go_to_reference(self, location: NavigationLocation) -> NavigationResult:
        """
        Go to reference.
        
        Args:
            location: Current location
            
        Returns:
            NavigationResult: Navigation result
        """
        if not self.config.enable_goto_reference:
            result = NavigationResult(success=False)
            result.message = "Go to reference disabled"
            return result
        
        return self.navigate_to(location, NavigationType.REFERENCE)
    
    def go_to_implementation(self, location: NavigationLocation) -> NavigationResult:
        """
        Go to implementation.
        
        Args:
            location: Current location
            
        Returns:
            NavigationResult: Navigation result
        """
        if not self.config.enable_goto_implementation:
            result = NavigationResult(success=False)
            result.message = "Go to implementation disabled"
            return result
        
        return self.navigate_to(location, NavigationType.IMPLEMENTATION)
    
    def go_to_type_definition(self, location: NavigationLocation) -> NavigationResult:
        """
        Go to type definition.
        
        Args:
            location: Current location
            
        Returns:
            NavigationResult: Navigation result
        """
        if not self.config.enable_goto_type_definition:
            result = NavigationResult(success=False)
            result.message = "Go to type definition disabled"
            return result
        
        return self.navigate_to(location, NavigationType.TYPE_DEFINITION)
    
    def _add_to_history(self, location: NavigationLocation) -> None:
        """
        Add location to history.
        
        Args:
            location: Navigation location
        """
        # Remove any locations after current index
        self.history.locations = self.history.locations[:self.history.current_index + 1]
        
        # Add new location
        self.history.locations.append(location)
        self.history.current_index += 1
        
        # Limit history size
        if len(self.history.locations) > self.config.max_history:
            self.history.locations.pop(0)
            self.history.current_index -= 1
    
    def go_back(self) -> NavigationResult:
        """
        Go back in history.
        
        Returns:
            NavigationResult: Navigation result
        """
        result = NavigationResult(success=False)
        
        try:
            if not self.config.enable_history:
                result.errors.append("History disabled")
                return result
            
            if self.history.current_index > 0:
                self.history.current_index -= 1
                location = self.history.locations[self.history.current_index]
                result.success = True
                result.message = f"Back to {location.file_path}:{location.line}:{location.column}"
                result.history = self.history
            else:
                result.errors.append("No more history")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def go_forward(self) -> NavigationResult:
        """
        Go forward in history.
        
        Returns:
            NavigationResult: Navigation result
        """
        result = NavigationResult(success=False)
        
        try:
            if not self.config.enable_history:
                result.errors.append("History disabled")
                return result
            
            if self.history.current_index < len(self.history.locations) - 1:
                self.history.current_index += 1
                location = self.history.locations[self.history.current_index]
                result.success = True
                result.message = f"Forward to {location.file_path}:{location.line}:{location.column}"
                result.history = self.history
            else:
                result.errors.append("No more history")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_history(self) -> NavigationHistory:
        """
        Get navigation history.
        
        Returns:
            NavigationHistory: History
        """
        return self.history
    
    def clear_history(self) -> NavigationResult:
        """
        Clear navigation history.
        
        Returns:
            NavigationResult: Clear result
        """
        result = NavigationResult(success=True)
        
        try:
            self.history.locations.clear()
            self.history.current_index = -1
            result.message = "History cleared"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def update_config(self, config: NavigationConfig) -> NavigationResult:
        """
        Update navigation configuration.
        
        Args:
            config: New configuration
            
        Returns:
            NavigationResult: Update result
        """
        result = NavigationResult(success=True)
        
        try:
            self.config = config
            result.message = "Config updated"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def get_config(self) -> NavigationConfig:
        """
        Get navigation configuration.
        
        Returns:
            NavigationConfig: Configuration
        """
        return self.config


if __name__ == "__main__":
    # Basit test
    config = NavigationConfig()
    manager = CodeNavigationManager(config)
    
    # Navigate to location
    location = NavigationLocation(
        file_path="test.py",
        line=10,
        column=5
    )
    
    result = manager.navigate_to(location)
    
    print(f"Navigation: {result.message}")
    
    # History al
    history = manager.get_history()
    
    print(f"History size: {len(history.locations)}")
