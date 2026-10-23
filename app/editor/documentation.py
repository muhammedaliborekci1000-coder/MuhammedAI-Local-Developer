"""
MuhammedAI Local Developer - Documentation
Documentation system for code editor.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum


class DocumentationType(Enum):
    """Documentation type."""
    FUNCTION = "function"
    CLASS = "class"
    MODULE = "module"
    VARIABLE = "variable"
    PARAMETER = "parameter"
    RETURN = "return"
    EXCEPTION = "exception"
    EXAMPLE = "example"
    CUSTOM = "custom"


class DocumentationFormat(Enum):
    """Documentation format."""
    PLAIN_TEXT = "plain_text"
    MARKDOWN = "markdown"
    HTML = "html"
    DOCSTRING = "docstring"
    RICH_TEXT = "rich_text"


@dataclass
class DocumentationRange:
    """Documentation range."""
    start_line: int
    start_column: int
    end_line: int
    end_column: int


@dataclass
class Documentation:
    """Documentation entry."""
    id: str
    type: DocumentationType
    range: DocumentationRange
    text: str
    format: DocumentationFormat = DocumentationFormat.MARKDOWN
    is_enabled: bool = True
    is_visible: bool = True
    language: Optional[str] = None
    symbol_name: Optional[str] = None
    signature: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DocumentationConfig:
    """Documentation configuration."""
    enabled: bool = True
    format: DocumentationFormat = DocumentationFormat.MARKDOWN
    show_functions: bool = True
    show_classes: bool = True
    show_modules: bool = True
    show_variables: bool = True
    show_parameters: bool = True
    show_returns: bool = True
    show_exceptions: bool = True
    show_examples: bool = True
    auto_generate: bool = True
    max_documentation: int = 100
    enable_cache: bool = True


@dataclass
class DocumentationResult:
    """Documentation result."""
    success: bool
    documentation: Optional[Documentation] = None
    documentation_list: List[Documentation] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    message: Optional[str] = None


class DocumentationManager:
    """
    Documentation manager.
    
    Özellikler:
    - Function documentation
    - Class documentation
    - Module documentation
    - Variable documentation
    - Parameter documentation
    - Return documentation
    - Exception documentation
    - Example documentation
    - Custom documentation
    - Documentation formats
    - Documentation filtering
    - Documentation caching
    - Documentation scope
    - Documentation context
    """
    
    def __init__(self, config: Optional[DocumentationConfig] = None):
        """
        Initialize documentation manager.
        
        Args:
            config: Documentation configuration
        """
        self.config = config or DocumentationConfig()
        self.documentation: Dict[str, Documentation] = {}
        self.cache: Dict[str, Documentation] = {}
        self.documentation_id_counter = 0
        self._next_id()
    
    def _next_id(self) -> str:
        """
        Generate next documentation ID.
        
        Returns:
            str: Documentation ID
        """
        self.documentation_id_counter += 1
        return f"doc_{self.documentation_id_counter}"
    
    def add_documentation(self, documentation: Documentation) -> DocumentationResult:
        """
        Add documentation.
        
        Args:
            documentation: Documentation to add
            
        Returns:
            DocumentationResult: Add result
        """
        result = DocumentationResult(success=True)
        
        try:
            if not documentation.id:
                documentation.id = self._next_id()
            
            self.documentation[documentation.id] = documentation
            
            # Cache if enabled
            if self.config.enable_cache:
                self.cache[documentation.id] = documentation
            
            result.documentation = documentation
            result.documentation_list = self.get_all_documentation()
            result.message = f"Documentation '{documentation.id}' added"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def remove_documentation(self, documentation_id: str) -> DocumentationResult:
        """
        Remove documentation.
        
        Args:
            documentation_id: Documentation ID
            
        Returns:
            DocumentationResult: Remove result
        """
        result = DocumentationResult(success=False)
        
        try:
            if documentation_id in self.documentation:
                del self.documentation[documentation_id]
                if documentation_id in self.cache:
                    del self.cache[documentation_id]
                result.success = True
                result.documentation_list = self.get_all_documentation()
                result.message = f"Documentation '{documentation_id}' removed"
            else:
                result.errors.append("Documentation not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_documentation(self, documentation_id: str) -> Optional[Documentation]:
        """
        Get documentation by ID.
        
        Args:
            documentation_id: Documentation ID
            
        Returns:
            Optional[Documentation]: Documentation
        """
        return self.documentation.get(documentation_id)
    
    def get_all_documentation(self) -> List[Documentation]:
        """
        Get all documentation.
        
        Returns:
            List[Documentation]: All documentation
        """
        return list(self.documentation.values())
    
    def get_documentation_by_type(self, doc_type: DocumentationType) -> List[Documentation]:
        """
        Get documentation by type.
        
        Args:
            doc_type: Documentation type
            
        Returns:
            List[Documentation]: Documentation
        """
        return [d for d in self.documentation.values() if d.type == doc_type]
    
    def add_function_documentation(self, range: DocumentationRange, text: str, symbol_name: str = "", signature: str = "") -> DocumentationResult:
        """
        Add function documentation.
        
        Args:
            range: Documentation range
            text: Documentation text
            symbol_name: Function name
            signature: Function signature
            
        Returns:
            DocumentationResult: Add result
        """
        if not self.config.show_functions:
            result = DocumentationResult(success=False)
            result.message = "Function documentation disabled"
            return result
        
        documentation = Documentation(
            id="",
            type=DocumentationType.FUNCTION,
            range=range,
            text=text,
            format=self.config.format,
            symbol_name=symbol_name,
            signature=signature
        )
        
        return self.add_documentation(documentation)
    
    def add_class_documentation(self, range: DocumentationRange, text: str, symbol_name: str = "") -> DocumentationResult:
        """
        Add class documentation.
        
        Args:
            range: Documentation range
            text: Documentation text
            symbol_name: Class name
            
        Returns:
            DocumentationResult: Add result
        """
        if not self.config.show_classes:
            result = DocumentationResult(success=False)
            result.message = "Class documentation disabled"
            return result
        
        documentation = Documentation(
            id="",
            type=DocumentationType.CLASS,
            range=range,
            text=text,
            format=self.config.format,
            symbol_name=symbol_name
        )
        
        return self.add_documentation(documentation)
    
    def add_module_documentation(self, range: DocumentationRange, text: str, symbol_name: str = "") -> DocumentationResult:
        """
        Add module documentation.
        
        Args:
            range: Documentation range
            text: Documentation text
            symbol_name: Module name
            
        Returns:
            DocumentationResult: Add result
        """
        if not self.config.show_modules:
            result = DocumentationResult(success=False)
            result.message = "Module documentation disabled"
            return result
        
        documentation = Documentation(
            id="",
            type=DocumentationType.MODULE,
            range=range,
            text=text,
            format=self.config.format,
            symbol_name=symbol_name
        )
        
        return self.add_documentation(documentation)
    
    def add_variable_documentation(self, range: DocumentationRange, text: str, symbol_name: str = "") -> DocumentationResult:
        """
        Add variable documentation.
        
        Args:
            range: Documentation range
            text: Documentation text
            symbol_name: Variable name
            
        Returns:
            DocumentationResult: Add result
        """
        if not self.config.show_variables:
            result = DocumentationResult(success=False)
            result.message = "Variable documentation disabled"
            return result
        
        documentation = Documentation(
            id="",
            type=DocumentationType.VARIABLE,
            range=range,
            text=text,
            format=self.config.format,
            symbol_name=symbol_name
        )
        
        return self.add_documentation(documentation)
    
    def add_parameter_documentation(self, range: DocumentationRange, text: str, symbol_name: str = "") -> DocumentationResult:
        """
        Add parameter documentation.
        
        Args:
            range: Documentation range
            text: Documentation text
            symbol_name: Parameter name
            
        Returns:
            DocumentationResult: Add result
        """
        if not self.config.show_parameters:
            result = DocumentationResult(success=False)
            result.message = "Parameter documentation disabled"
            return result
        
        documentation = Documentation(
            id="",
            type=DocumentationType.PARAMETER,
            range=range,
            text=text,
            format=self.config.format,
            symbol_name=symbol_name
        )
        
        return self.add_documentation(documentation)
    
    def add_return_documentation(self, range: DocumentationRange, text: str) -> DocumentationResult:
        """
        Add return documentation.
        
        Args:
            range: Documentation range
            text: Documentation text
            
        Returns:
            DocumentationResult: Add result
        """
        if not self.config.show_returns:
            result = DocumentationResult(success=False)
            result.message = "Return documentation disabled"
            return result
        
        documentation = Documentation(
            id="",
            type=DocumentationType.RETURN,
            range=range,
            text=text,
            format=self.config.format
        )
        
        return self.add_documentation(documentation)
    
    def add_exception_documentation(self, range: DocumentationRange, text: str, symbol_name: str = "") -> DocumentationResult:
        """
        Add exception documentation.
        
        Args:
            range: Documentation range
            text: Documentation text
            symbol_name: Exception name
            
        Returns:
            DocumentationResult: Add result
        """
        if not self.config.show_exceptions:
            result = DocumentationResult(success=False)
            result.message = "Exception documentation disabled"
            return result
        
        documentation = Documentation(
            id="",
            type=DocumentationType.EXCEPTION,
            range=range,
            text=text,
            format=self.config.format,
            symbol_name=symbol_name
        )
        
        return self.add_documentation(documentation)
    
    def add_example_documentation(self, range: DocumentationRange, text: str) -> DocumentationResult:
        """
        Add example documentation.
        
        Args:
            range: Documentation range
            text: Documentation text
            
        Returns:
            DocumentationResult: Add result
        """
        if not self.config.show_examples:
            result = DocumentationResult(success=False)
            result.message = "Example documentation disabled"
            return result
        
        documentation = Documentation(
            id="",
            type=DocumentationType.EXAMPLE,
            range=range,
            text=text,
            format=self.config.format
        )
        
        return self.add_documentation(documentation)
    
    def get_documentation_at_line(self, line: int) -> List[Documentation]:
        """
        Get documentation at specific line.
        
        Args:
            line: Line number
            
        Returns:
            List[Documentation]: Documentation
        """
        return [d for d in self.documentation.values() if d.range.start_line <= line <= d.range.end_line]
    
    def get_documentation_by_symbol(self, symbol_name: str) -> List[Documentation]:
        """
        Get documentation by symbol name.
        
        Args:
            symbol_name: Symbol name
            
        Returns:
            List[Documentation]: Documentation
        """
        return [d for d in self.documentation.values() if d.symbol_name == symbol_name]
    
    def clear_documentation(self) -> DocumentationResult:
        """
        Clear all documentation.
        
        Returns:
            DocumentationResult: Clear result
        """
        result = DocumentationResult(success=True)
        
        try:
            self.documentation.clear()
            self.cache.clear()
            result.message = "All documentation cleared"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def clear_documentation_by_type(self, doc_type: DocumentationType) -> DocumentationResult:
        """
        Clear documentation by type.
        
        Args:
            doc_type: Documentation type
            
        Returns:
            DocumentationResult: Clear result
        """
        result = DocumentationResult(success=True)
        
        try:
            to_remove = [id for id, d in self.documentation.items() if d.type == doc_type]
            for id in to_remove:
                del self.documentation[id]
                if id in self.cache:
                    del self.cache[id]
            
            result.message = f"Cleared {len(to_remove)} {doc_type.value} documentation"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def set_documentation_enabled(self, documentation_id: str, enabled: bool) -> DocumentationResult:
        """
        Set documentation enabled state.
        
        Args:
            documentation_id: Documentation ID
            enabled: Enabled state
            
        Returns:
            DocumentationResult: Set result
        """
        result = DocumentationResult(success=False)
        
        try:
            documentation = self.documentation.get(documentation_id)
            if documentation:
                documentation.is_enabled = enabled
                result.success = True
                result.message = f"Documentation '{documentation_id}' {'enabled' if enabled else 'disabled'}"
            else:
                result.errors.append("Documentation not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def set_documentation_visible(self, documentation_id: str, visible: bool) -> DocumentationResult:
        """
        Set documentation visible state.
        
        Args:
            documentation_id: Documentation ID
            visible: Visible state
            
        Returns:
            DocumentationResult: Set result
        """
        result = DocumentationResult(success=False)
        
        try:
            documentation = self.documentation.get(documentation_id)
            if documentation:
                documentation.is_visible = visible
                result.success = True
                result.message = f"Documentation '{documentation_id}' {'visible' if visible else 'hidden'}"
            else:
                result.errors.append("Documentation not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def update_config(self, config: DocumentationConfig) -> DocumentationResult:
        """
        Update documentation configuration.
        
        Args:
            config: New configuration
            
        Returns:
            DocumentationResult: Update result
        """
        result = DocumentationResult(success=True)
        
        try:
            self.config = config
            result.message = "Config updated"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def get_config(self) -> DocumentationConfig:
        """
        Get documentation configuration.
        
        Returns:
            DocumentationConfig: Configuration
        """
        return self.config


if __name__ == "__main__":
    # Basit test
    config = DocumentationConfig()
    manager = DocumentationManager(config)
    
    # Documentation ekle
    range = DocumentationRange(0, 0, 10, 0)
    result = manager.add_function_documentation(range, "This function does X", "test_function", "def test_function():")
    
    print(f"Documentation added: {result.message}")
    
    # Tüm documentation'ı al
    documentation = manager.get_all_documentation()
    
    print(f"Total documentation: {len(documentation)}")
