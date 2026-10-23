"""
MuhammedAI Local Developer - Decorations
Decorations system for code editor.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum


class DecorationType(Enum):
    """Decoration type."""
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
    HINT = "hint"
    SUCCESS = "success"
    CUSTOM = "custom"


class DecorationPosition(Enum):
    """Decoration position."""
    INLINE = "inline"
    GUTTER = "gutter"
    OVERVIEW = "overview"
    MINIMAP = "minimap"


@dataclass
class DecorationRange:
    """Decoration range."""
    start_line: int
    start_column: int
    end_line: int
    end_column: int


@dataclass
class Decoration:
    """Decoration."""
    id: str
    type: DecorationType
    range: DecorationRange
    message: str
    position: DecorationPosition = DecorationPosition.INLINE
    is_enabled: bool = True
    is_visible: bool = True
    priority: int = 0
    color: Optional[str] = None
    icon: Optional[str] = None


@dataclass
class DecorationsConfig:
    """Decorations configuration."""
    enabled: bool = True
    show_errors: bool = True
    show_warnings: bool = True
    show_info: bool = True
    show_hints: bool = True
    show_in_gutter: bool = True
    show_in_overview: bool = True
    show_in_minimap: bool = False
    max_decorations: int = 100
    animate_decorations: bool = True


@dataclass
class DecorationsResult:
    """Decorations result."""
    success: bool
    decorations: List[Decoration] = field(default_factory=list)
    html: Optional[str] = None
    errors: List[str] = field(default_factory=list)
    message: Optional[str] = None


class DecorationsManager:
    """
    Decorations manager.
    
    Özellikler:
    - Error decorations
    - Warning decorations
    - Info decorations
    - Hint decorations
    - Custom decorations
    - Decoration positioning
    - Decoration priority
    - Decoration filtering
    - Decoration visibility
    - Decoration animations
    - Decoration scope
    - Decoration context
    """
    
    def __init__(self, config: Optional[DecorationsConfig] = None):
        """
        Initialize decorations manager.
        
        Args:
            config: Decorations configuration
        """
        self.config = config or DecorationsConfig()
        self.decorations: Dict[str, Decoration] = {}
        self.decoration_id_counter = 0
        self._next_id()
    
    def _next_id(self) -> str:
        """
        Generate next decoration ID.
        
        Returns:
            str: Decoration ID
        """
        self.decoration_id_counter += 1
        return f"decoration_{self.decoration_id_counter}"
    
    def add_decoration(self, decoration: Decoration) -> DecorationsResult:
        """
        Add a decoration.
        
        Args:
            decoration: Decoration to add
            
        Returns:
            DecorationsResult: Add result
        """
        result = DecorationsResult(success=True)
        
        try:
            if not decoration.id:
                decoration.id = self._next_id()
            
            self.decorations[decoration.id] = decoration
            
            # Limit decorations
            if len(self.decorations) > self.config.max_decorations:
                oldest_id = min(self.decorations.keys(), key=lambda k: self.decorations[k].priority)
                del self.decorations[oldest_id]
            
            result.decorations = self.get_all_decorations()
            result.message = f"Decoration '{decoration.id}' added"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def remove_decoration(self, decoration_id: str) -> DecorationsResult:
        """
        Remove a decoration.
        
        Args:
            decoration_id: Decoration ID
            
        Returns:
            DecorationsResult: Remove result
        """
        result = DecorationsResult(success=False)
        
        try:
            if decoration_id in self.decorations:
                del self.decorations[decoration_id]
                result.success = True
                result.decorations = self.get_all_decorations()
                result.message = f"Decoration '{decoration_id}' removed"
            else:
                result.errors.append("Decoration not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_decoration(self, decoration_id: str) -> Optional[Decoration]:
        """
        Get decoration by ID.
        
        Args:
            decoration_id: Decoration ID
            
        Returns:
            Optional[Decoration]: Decoration
        """
        return self.decorations.get(decoration_id)
    
    def get_all_decorations(self) -> List[Decoration]:
        """
        Get all decorations.
        
        Returns:
            List[Decoration]: All decorations
        """
        return list(self.decorations.values())
    
    def get_decorations_by_type(self, decoration_type: DecorationType) -> List[Decoration]:
        """
        Get decorations by type.
        
        Args:
            decoration_type: Decoration type
            
        Returns:
            List[Decoration]: Decorations
        """
        return [d for d in self.decorations.values() if d.type == decoration_type]
    
    def get_decorations_by_position(self, position: DecorationPosition) -> List[Decoration]:
        """
        Get decorations by position.
        
        Args:
            position: Decoration position
            
        Returns:
            List[Decoration]: Decorations
        """
        return [d for d in self.decorations.values() if d.position == position]
    
    def add_error(self, range: DecorationRange, message: str) -> DecorationsResult:
        """
        Add error decoration.
        
        Args:
            range: Decoration range
            message: Error message
            
        Returns:
            DecorationsResult: Add result
        """
        if not self.config.show_errors:
            result = DecorationsResult(success=False)
            result.message = "Error decorations disabled"
            return result
        
        decoration = Decoration(
            id="",
            type=DecorationType.ERROR,
            range=range,
            message=message,
            position=DecorationPosition.INLINE
        )
        
        return self.add_decoration(decoration)
    
    def add_warning(self, range: DecorationRange, message: str) -> DecorationsResult:
        """
        Add warning decoration.
        
        Args:
            range: Decoration range
            message: Warning message
            
        Returns:
            DecorationsResult: Add result
        """
        if not self.config.show_warnings:
            result = DecorationsResult(success=False)
            result.message = "Warning decorations disabled"
            return result
        
        decoration = Decoration(
            id="",
            type=DecorationType.WARNING,
            range=range,
            message=message,
            position=DecorationPosition.INLINE
        )
        
        return self.add_decoration(decoration)
    
    def add_info(self, range: DecorationRange, message: str) -> DecorationsResult:
        """
        Add info decoration.
        
        Args:
            range: Decoration range
            message: Info message
            
        Returns:
            DecorationsResult: Add result
        """
        if not self.config.show_info:
            result = DecorationsResult(success=False)
            result.message = "Info decorations disabled"
            return result
        
        decoration = Decoration(
            id="",
            type=DecorationType.INFO,
            range=range,
            message=message,
            position=DecorationPosition.INLINE
        )
        
        return self.add_decoration(decoration)
    
    def add_hint(self, range: DecorationRange, message: str) -> DecorationsResult:
        """
        Add hint decoration.
        
        Args:
            range: Decoration range
            message: Hint message
            
        Returns:
            DecorationsResult: Add result
        """
        if not self.config.show_hints:
            result = DecorationsResult(success=False)
            result.message = "Hint decorations disabled"
            return result
        
        decoration = Decoration(
            id="",
            type=DecorationType.HINT,
            range=range,
            message=message,
            position=DecorationPosition.INLINE
        )
        
        return self.add_decoration(decoration)
    
    def clear_decorations(self) -> DecorationsResult:
        """
        Clear all decorations.
        
        Returns:
            DecorationsResult: Clear result
        """
        result = DecorationsResult(success=True)
        
        try:
            self.decorations.clear()
            result.message = "All decorations cleared"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def clear_decorations_by_type(self, decoration_type: DecorationType) -> DecorationsResult:
        """
        Clear decorations by type.
        
        Args:
            decoration_type: Decoration type
            
        Returns:
            DecorationsResult: Clear result
        """
        result = DecorationsResult(success=True)
        
        try:
            to_remove = [id for id, d in self.decorations.items() if d.type == decoration_type]
            for id in to_remove:
                del self.decorations[id]
            
            result.message = f"Cleared {len(to_remove)} {decoration_type.value} decorations"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def set_decoration_enabled(self, decoration_id: str, enabled: bool) -> DecorationsResult:
        """
        Set decoration enabled state.
        
        Args:
            decoration_id: Decoration ID
            enabled: Enabled state
            
        Returns:
            DecorationsResult: Set result
        """
        result = DecorationsResult(success=False)
        
        try:
            decoration = self.decorations.get(decoration_id)
            if decoration:
                decoration.is_enabled = enabled
                result.success = True
                result.message = f"Decoration '{decoration_id}' {'enabled' if enabled else 'disabled'}"
            else:
                result.errors.append("Decoration not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def set_decoration_visible(self, decoration_id: str, visible: bool) -> DecorationsResult:
        """
        Set decoration visible state.
        
        Args:
            decoration_id: Decoration ID
            visible: Visible state
            
        Returns:
            DecorationsResult: Set result
        """
        result = DecorationsResult(success=False)
        
        try:
            decoration = self.decorations.get(decoration_id)
            if decoration:
                decoration.is_visible = visible
                result.success = True
                result.message = f"Decoration '{decoration_id}' {'visible' if visible else 'hidden'}"
            else:
                result.errors.append("Decoration not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def update_config(self, config: DecorationsConfig) -> DecorationsResult:
        """
        Update decorations configuration.
        
        Args:
            config: New configuration
            
        Returns:
            DecorationsResult: Update result
        """
        result = DecorationsResult(success=True)
        
        try:
            self.config = config
            result.message = "Config updated"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def get_config(self) -> DecorationsConfig:
        """
        Get decorations configuration.
        
        Returns:
            DecorationsConfig: Configuration
        """
        return self.config


if __name__ == "__main__":
    # Basit test
    config = DecorationsConfig()
    manager = DecorationsManager(config)
    
    # Decoration ekle
    range = DecorationRange(0, 0, 0, 10)
    result = manager.add_error(range, "Test error")
    
    print(f"Decoration added: {result.message}")
    
    # Tüm decoration'ları al
    decorations = manager.get_all_decorations()
    
    print(f"Total decorations: {len(decorations)}")
