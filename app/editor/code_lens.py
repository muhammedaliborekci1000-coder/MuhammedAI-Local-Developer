"""
MuhammedAI Local Developer - Code Lens
Code lens system for code editor.
"""

from typing import Dict, Any, Optional, List, Callable
from dataclasses import dataclass, field
from enum import Enum


class LensType(Enum):
    """Lens type."""
    REFERENCE = "reference"
    IMPLEMENTATION = "implementation"
    DEFINITION = "definition"
    TEST = "test"
    DOCUMENTATION = "documentation"
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
    CUSTOM = "custom"


@dataclass
class LensPosition:
    """Lens position."""
    line: int
    column: int


@dataclass
class LensAction:
    """Lens action."""
    id: str
    title: str
    command: Optional[str] = None
    callback: Optional[Callable] = None


@dataclass
class CodeLens:
    """Code lens."""
    id: str
    title: str
    type: LensType = LensType.INFO
    position: Optional[LensPosition] = None
    actions: List[LensAction] = field(default_factory=list)
    is_enabled: bool = True
    is_visible: bool = True
    priority: int = 0
    tooltip: Optional[str] = None
    icon: Optional[str] = None


@dataclass
class CodeLensConfig:
    """Code lens configuration."""
    enabled: bool = True
    show_reference_lenses: bool = True
    show_implementation_lenses: bool = True
    show_definition_lenses: bool = True
    show_test_lenses: bool = True
    show_documentation_lenses: bool = False
    show_icons: bool = True
    show_tooltips: bool = True
    max_lenses_per_line: int = 5
    enable_click_actions: bool = True
    animate_lenses: bool = True


@dataclass
class CodeLensResult:
    """Code lens result."""
    success: bool
    lenses: List[CodeLens] = field(default_factory=list)
    html: Optional[str] = None
    errors: List[str] = field(default_factory=list)
    message: Optional[str] = None


class CodeLensManager:
    """
    Code lens manager.
    
    Özellikler:
    - Reference lenses
    - Implementation lenses
    - Definition lenses
    - Test lenses
    - Documentation lenses
    - Lens actions
    - Lens positioning
    - Lens priority
    - Lens filtering
    - Lens visibility
    - Lens animations
    - Lens icons
    - Lens tooltips
    - Lens scope
    - Lens context
    - Custom lenses
    """
    
    def __init__(self, config: Optional[CodeLensConfig] = None):
        """
        Initialize code lens manager.
        
        Args:
            config: Code lens configuration
        """
        self.config = config or CodeLensConfig()
        self.lenses: Dict[str, CodeLens] = {}
        self.lens_id_counter = 0
        self._next_id()
    
    def _next_id(self) -> str:
        """
        Generate next lens ID.
        
        Returns:
            str: Lens ID
        """
        self.lens_id_counter += 1
        return f"lens_{self.lens_id_counter}"
    
    def add_lens(self, lens: CodeLens) -> CodeLensResult:
        """
        Add a lens.
        
        Args:
            lens: Lens to add
            
        Returns:
            CodeLensResult: Add result
        """
        result = CodeLensResult(success=True)
        
        try:
            if not lens.id:
                lens.id = self._next_id()
            
            self.lenses[lens.id] = lens
            result.lenses = self.get_all_lenses()
            result.message = f"Lens '{lens.id}' added"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def remove_lens(self, lens_id: str) -> CodeLensResult:
        """
        Remove a lens.
        
        Args:
            lens_id: Lens ID
            
        Returns:
            CodeLensResult: Remove result
        """
        result = CodeLensResult(success=False)
        
        try:
            if lens_id in self.lenses:
                del self.lenses[lens_id]
                result.success = True
                result.lenses = self.get_all_lenses()
                result.message = f"Lens '{lens_id}' removed"
            else:
                result.errors.append("Lens not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_lens(self, lens_id: str) -> Optional[CodeLens]:
        """
        Get lens by ID.
        
        Args:
            lens_id: Lens ID
            
        Returns:
            Optional[CodeLens]: Lens
        """
        return self.lenses.get(lens_id)
    
    def get_all_lenses(self) -> List[CodeLens]:
        """
        Get all lenses.
        
        Returns:
            List[CodeLens]: All lenses
        """
        return list(self.lenses.values())
    
    def get_lenses_by_type(self, lens_type: LensType) -> List[CodeLens]:
        """
        Get lenses by type.
        
        Args:
            lens_type: Lens type
            
        Returns:
            List[CodeLens]: Lenses
        """
        return [l for l in self.lenses.values() if l.type == lens_type]
    
    def get_lenses_at_line(self, line: int) -> List[CodeLens]:
        """
        Get lenses at specific line.
        
        Args:
            line: Line number
            
        Returns:
            List[CodeLens]: Lenses
        """
        return [l for l in self.lenses.values() if l.position and l.position.line == line]
    
    def add_reference_lens(self, title: str, position: LensPosition, count: int) -> CodeLensResult:
        """
        Add reference lens.
        
        Args:
            title: Lens title
            position: Position info
            count: Reference count
            
        Returns:
            CodeLensResult: Add result
        """
        if not self.config.show_reference_lenses:
            result = CodeLensResult(success=False)
            result.message = "Reference lenses disabled"
            return result
        
        lens = CodeLens(
            id="",
            title=f"{title} ({count} references)",
            type=LensType.REFERENCE,
            position=position
        )
        
        return self.add_lens(lens)
    
    def add_implementation_lens(self, title: str, position: LensPosition, count: int) -> CodeLensResult:
        """
        Add implementation lens.
        
        Args:
            title: Lens title
            position: Position info
            count: Implementation count
            
        Returns:
            CodeLensResult: Add result
        """
        if not self.config.show_implementation_lenses:
            result = CodeLensResult(success=False)
            result.message = "Implementation lenses disabled"
            return result
        
        lens = CodeLens(
            id="",
            title=f"{title} ({count} implementations)",
            type=LensType.IMPLEMENTATION,
            position=position
        )
        
        return self.add_lens(lens)
    
    def add_definition_lens(self, title: str, position: LensPosition) -> CodeLensResult:
        """
        Add definition lens.
        
        Args:
            title: Lens title
            position: Position info
            
        Returns:
            CodeLensResult: Add result
        """
        if not self.config.show_definition_lenses:
            result = CodeLensResult(success=False)
            result.message = "Definition lenses disabled"
            return result
        
        lens = CodeLens(
            id="",
            title=f"{title}",
            type=LensType.DEFINITION,
            position=position
        )
        
        return self.add_lens(lens)
    
    def add_test_lens(self, title: str, position: LensPosition, status: str) -> CodeLensResult:
        """
        Add test lens.
        
        Args:
            title: Lens title
            position: Position info
            status: Test status
            
        Returns:
            CodeLensResult: Add result
        """
        if not self.config.show_test_lenses:
            result = CodeLensResult(success=False)
            result.message = "Test lenses disabled"
            return result
        
        lens = CodeLens(
            id="",
            title=f"{title} ({status})",
            type=LensType.TEST,
            position=position
        )
        
        return self.add_lens(lens)
    
    def execute_lens_action(self, lens_id: str, action_id: str) -> CodeLensResult:
        """
        Execute lens action.
        
        Args:
            lens_id: Lens ID
            action_id: Action ID
            
        Returns:
            CodeLensResult: Execution result
        """
        result = CodeLensResult(success=False)
        
        try:
            lens = self.lenses.get(lens_id)
            if lens:
                for action in lens.actions:
                    if action.id == action_id:
                        if action.callback:
                            action.callback()
                            result.success = True
                            result.message = f"Action '{action.title}' executed"
                        elif action.command:
                            result.success = True
                            result.message = f"Command '{action.command}' executed"
                        else:
                            result.errors.append("No action defined")
                        break
                else:
                    result.errors.append("Action not found")
            else:
                result.errors.append("Lens not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def clear_lenses(self) -> CodeLensResult:
        """
        Clear all lenses.
        
        Returns:
            CodeLensResult: Clear result
        """
        result = CodeLensResult(success=True)
        
        try:
            self.lenses.clear()
            result.message = "All lenses cleared"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def update_config(self, config: CodeLensConfig) -> CodeLensResult:
        """
        Update code lens configuration.
        
        Args:
            config: New configuration
            
        Returns:
            CodeLensResult: Update result
        """
        result = CodeLensResult(success=True)
        
        try:
            self.config = config
            result.message = "Config updated"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def get_config(self) -> CodeLensConfig:
        """
        Get code lens configuration.
        
        Returns:
            CodeLensConfig: Configuration
        """
        return self.config


if __name__ == "__main__":
    # Basit test
    config = CodeLensConfig()
    manager = CodeLensManager(config)
    
    # Lens ekle
    position = LensPosition(line=0, column=0)
    lens = CodeLens(
        id="",
        title="Test Lens",
        type=LensType.INFO,
        position=position
    )
    
    result = manager.add_lens(lens)
    
    print(f"Lens added: {result.message}")
    
    # Tüm lens'leri al
    lenses = manager.get_all_lenses()
    
    print(f"Total lenses: {len(lenses)}")
