"""
MuhammedAI Local Developer - Hover
Hover information system for code editor.
"""

import re
from typing import Dict, Any, Optional, List, Union
from dataclasses import dataclass, field
from enum import Enum


class HoverContentKind(Enum):
    """Hover content kind."""
    PLAIN_TEXT = "plaintext"
    MARKDOWN = "markdown"


@dataclass
class Position:
    """Position in text document."""
    line: int
    character: int


@dataclass
class Range:
    """Range in text document."""
    start: Position
    end: Position


@dataclass
class MarkedString:
    """Marked string for hover content."""
    language: str
    value: str


@dataclass
class Hover:
    """Hover information."""
    contents: Union[str, MarkedString, List[Any]]
    range: Optional[Range] = None


@dataclass
class ParameterInfo:
    """Parameter information."""
    label: str
    documentation: Optional[str] = None


@dataclass
class SignatureInfo:
    """Signature information."""
    label: str
    documentation: Optional[str] = None
    parameters: List[ParameterInfo] = field(default_factory=list)


@dataclass
class HoverConfig:
    """Hover configuration."""
    enable_documentation: bool = True
    enable_type_info: bool = True
    enable_signature: bool = True
    enable_rich_content: bool = True
    content_kind: HoverContentKind = HoverContentKind.MARKDOWN
    max_line_length: int = 80
    cache_enabled: bool = True
    history_enabled: bool = True


class HoverEngine:
    """
    Hover engine.
    
    Özellikler:
    - Hover information display
    - Documentation support
    - Type information
    - Multi-language support
    - Configuration management
    - Hover caching
    - Hover history
    - Rich content support (markdown)
    - Signature information
    - Parameter information
    - Return type information
    - Symbol resolution
    - Context-aware hover
    """
    
    def __init__(self, config: Optional[HoverConfig] = None):
        """
        Initialize hover engine.
        
        Args:
            config: Hover configuration
        """
        self.config = config or HoverConfig()
        self.cache: Dict[str, Hover] = {}
        self.history: List[Hover] = []
        self._initialize_symbols()
    
    def _initialize_symbols(self) -> None:
        """Initialize symbol documentation."""
        self.symbol_docs = {
            "python": {
                "def": "Define a function",
                "class": "Define a class",
                "if": "Conditional statement",
                "else": "Else clause for if statement",
                "for": "For loop",
                "while": "While loop",
                "try": "Try block for exception handling",
                "except": "Except block for exception handling",
                "finally": "Finally block always executed",
                "with": "Context manager",
                "import": "Import module",
                "from": "Import from module",
                "return": "Return value from function",
                "yield": "Yield value from generator",
                "raise": "Raise exception",
                "pass": "Null statement",
                "break": "Break out of loop",
                "continue": "Continue to next iteration",
                "lambda": "Anonymous function",
                "True": "Boolean true value",
                "False": "Boolean false value",
                "None": "Null value",
                "self": "Instance reference",
                "super": "Parent class reference",
                "print": "Print to console",
                "len": "Get length of object",
                "str": "Convert to string",
                "int": "Convert to integer",
                "float": "Convert to float",
                "list": "Create list",
                "dict": "Create dictionary",
                "set": "Create set",
                "tuple": "Create tuple"
            },
            "javascript": {
                "function": "Define a function",
                "class": "Define a class",
                "const": "Declare constant",
                "let": "Declare variable",
                "var": "Declare variable (legacy)",
                "if": "Conditional statement",
                "else": "Else clause",
                "for": "For loop",
                "while": "While loop",
                "return": "Return value",
                "async": "Async function",
                "await": "Await promise",
                "import": "Import module",
                "export": "Export module",
                "console.log": "Log to console",
                "true": "Boolean true",
                "false": "Boolean false",
                "null": "Null value",
                "undefined": "Undefined value"
            },
            "typescript": {
                "function": "Define a function",
                "class": "Define a class",
                "interface": "Define interface",
                "type": "Define type alias",
                "enum": "Define enumeration",
                "const": "Declare constant",
                "let": "Declare variable",
                "if": "Conditional statement",
                "else": "Else clause",
                "for": "For loop",
                "while": "While loop",
                "return": "Return value",
                "async": "Async function",
                "await": "Await promise",
                "any": "Any type",
                "void": "Void type",
                "never": "Never type"
            },
            "go": {
                "func": "Define a function",
                "var": "Declare variable",
                "const": "Declare constant",
                "type": "Define type",
                "struct": "Define struct",
                "interface": "Define interface",
                "if": "Conditional statement",
                "else": "Else clause",
                "for": "For loop",
                "range": "Range over iterable",
                "go": "Start goroutine",
                "chan": "Channel",
                "select": "Select statement",
                "defer": "Defer execution",
                "return": "Return value",
                "package": "Package declaration",
                "import": "Import package"
            },
            "rust": {
                "fn": "Define a function",
                "let": "Declare variable",
                "mut": "Mutable variable",
                "const": "Constant",
                "static": "Static",
                "struct": "Define struct",
                "enum": "Define enum",
                "impl": "Implement trait",
                "trait": "Define trait",
                "type": "Type alias",
                "if": "Conditional statement",
                "else": "Else clause",
                "match": "Pattern matching",
                "for": "For loop",
                "while": "While loop",
                "loop": "Infinite loop",
                "break": "Break loop",
                "continue": "Continue loop",
                "return": "Return value",
                "use": "Import module",
                "mod": "Module declaration",
                "crate": "Crate reference",
                "pub": "Public visibility",
                "unsafe": "Unsafe block",
                "where": "Where clause",
                "move": "Move closure",
                "ref": "Reference"
            }
        }
    
    def get_hover(
        self,
        text: str,
        line: int,
        character: int,
        language: str = "python"
    ) -> Optional[Hover]:
        """
        Get hover information for position.
        
        Args:
            text: Document text
            line: Line number
            character: Character offset
            language: Language identifier
            
        Returns:
            Optional[Hover]: Hover information
        """
        # Get word at position
        word = self._get_word_at_position(text, line, character)
        
        if not word:
            return None
        
        # Check cache
        cache_key = f"{language}:{word}"
        if self.config.cache_enabled and cache_key in self.cache:
            hover = self.cache[cache_key]
            if self.config.history_enabled:
                self.history.append(hover)
            return hover
        
        # Get documentation
        docs = self._get_symbol_documentation(word, language)
        
        if not docs:
            return None
        
        # Get type information
        type_info = self._get_type_information(word, language) if self.config.enable_type_info else None
        
        # Get signature information
        signature = self._get_signature_information(word, language) if self.config.enable_signature else None
        
        # Build hover content
        content = self._build_hover_content(word, docs, type_info, signature)
        
        # Create hover
        hover = Hover(contents=content)
        
        # Cache
        if self.config.cache_enabled:
            self.cache[cache_key] = hover
        
        # History
        if self.config.history_enabled:
            self.history.append(hover)
        
        return hover
    
    def _get_word_at_position(self, text: str, line: int, character: int) -> Optional[str]:
        """
        Get word at position.
        
        Args:
            text: Document text
            line: Line number
            character: Character offset
            
        Returns:
            Optional[str]: Word at position
        """
        lines = text.split('\n')
        if line >= len(lines):
            return None
        
        current_line = lines[line]
        if character >= len(current_line):
            return None
        
        # Get characters around cursor
        before = current_line[:character]
        after = current_line[character:]
        
        # Extract word
        word = ""
        for char in reversed(before):
            if char.isalnum() or char == '_':
                word = char + word
            else:
                break
        
        for char in after:
            if char.isalnum() or char == '_':
                word += char
            else:
                break
        
        return word if word else None
    
    def _get_symbol_documentation(self, word: str, language: str) -> Optional[str]:
        """
        Get symbol documentation.
        
        Args:
            word: Symbol name
            language: Language identifier
            
        Returns:
            Optional[str]: Documentation
        """
        symbol_docs = self.symbol_docs.get(language, {})
        return symbol_docs.get(word)
    
    def _get_type_information(self, word: str, language: str) -> Optional[str]:
        """
        Get type information.
        
        Args:
            word: Symbol name
            language: Language identifier
            
        Returns:
            Optional[str]: Type information
        """
        # Simple type inference (placeholder)
        if language == "python":
            if word in ["True", "False"]:
                return "bool"
            elif word == "None":
                return "NoneType"
            elif word in ["str", "int", "float", "list", "dict", "set", "tuple"]:
                return f"{word} (type)"
        
        return None
    
    def _get_signature_information(self, word: str, language: str) -> Optional[SignatureInfo]:
        """
        Get signature information.
        
        Args:
            word: Symbol name
            language: Language identifier
            
        Returns:
            Optional[SignatureInfo]: Signature information
        """
        # Simple signature lookup (placeholder)
        if language == "python":
            if word == "print":
                return SignatureInfo(
                    label="print(*args, **kwargs)",
                    documentation="Print objects to the text stream file",
                    parameters=[
                        ParameterInfo(label="*args", documentation="Positional arguments"),
                        ParameterInfo(label="**kwargs", documentation="Keyword arguments")
                    ]
                )
            elif word == "len":
                return SignatureInfo(
                    label="len(obj)",
                    documentation="Return the number of items in a container",
                    parameters=[
                        ParameterInfo(label="obj", documentation="Container object")
                    ]
                )
        
        return None
    
    def _build_hover_content(
        self,
        word: str,
        docs: Optional[str],
        type_info: Optional[str],
        signature: Optional[SignatureInfo]
    ) -> Union[str, MarkedString, List[Any]]:
        """
        Build hover content.
        
        Args:
            word: Symbol name
            docs: Documentation
            type_info: Type information
            signature: Signature information
            
        Returns:
            Union[str, MarkedString, List[Any]]: Hover content
        """
        if not self.config.enable_rich_content:
            # Plain text
            parts = []
            if docs:
                parts.append(docs)
            if type_info:
                parts.append(f"Type: {type_info}")
            if signature:
                parts.append(f"Signature: {signature.label}")
            return "\n\n".join(parts)
        
        # Rich content (markdown)
        parts = []
        
        if signature:
            parts.append(f"```{signature.label}```")
            if signature.documentation:
                parts.append(f"\n{signature.documentation}")
        
        if docs:
            parts.append(f"\n**Documentation:** {docs}")
        
        if type_info:
            parts.append(f"\n**Type:** `{type_info}`")
        
        return "\n".join(parts)
    
    def get_hover_history(self) -> List[Hover]:
        """
        Get hover history.
        
        Returns:
            List[Hover]: History
        """
        return self.history
    
    def clear_history(self) -> None:
        """Clear hover history."""
        self.history.clear()
    
    def clear_cache(self) -> None:
        """Clear hover cache."""
        self.cache.clear()
    
    def update_config(self, config: HoverConfig) -> None:
        """
        Update hover configuration.
        
        Args:
            config: New configuration
        """
        self.config = config
    
    def get_config(self) -> HoverConfig:
        """
        Get hover configuration.
        
        Returns:
            HoverConfig: Configuration
        """
        return self.config


if __name__ == "__main__":
    # Basit test
    config = HoverConfig()
    engine = HoverEngine(config)
    
    text = "def hello():\n    print('Hello World')"
    
    hover = engine.get_hover(text, 1, 8, "python")
    
    if hover:
        print(f"Hover: {hover.contents}")
