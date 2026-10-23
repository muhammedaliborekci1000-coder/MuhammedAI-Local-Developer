"""
MuhammedAI Local Developer - Formatting
Code formatting system for code editor.
"""

import re
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum


class FormattingMode(Enum):
    """Formatting mode."""
    FULL = "full"
    RANGE = "range"
    ON_TYPE = "on_type"


class FormattingTriggerKind(Enum):
    """Formatting trigger kind."""
    ON_SAVE = "on_save"
    ON_TYPE = "on_type"
    MANUAL = "manual"


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
class TextEdit:
    """Text edit."""
    range: Range
    newText: str


@dataclass
class FormattingOptions:
    """Formatting options."""
    tab_size: int = 4
    insert_spaces: bool = True
    trim_trailing_whitespace: bool = True
    insert_final_newline: bool = True
    trim_final_newlines: bool = True
    keep_line_length: Optional[int] = None


@dataclass
class DocumentFormattingParams:
    """Document formatting parameters."""
    options: FormattingOptions
    range: Optional[Range] = None


@dataclass
class FormattingConfig:
    """Formatting configuration."""
    mode: FormattingMode = FormattingMode.FULL
    trigger_kind: FormattingTriggerKind = FormattingTriggerKind.ON_SAVE
    auto_format: bool = False
    format_on_save: bool = True
    format_on_type: bool = False
    max_line_length: int = 88
    indent_size: int = 4
    use_tabs: bool = False
    trim_trailing_whitespace: bool = True
    insert_final_newline: bool = True


class FormattingEngine:
    """
    Formatting engine.
    
    Özellikler:
    - Code formatting
    - Range formatting
    - On-type formatting
    - Multi-language support
    - Configuration management
    - Indentation handling
    - Trailing whitespace removal
    - Line length enforcement
    - Final newline handling
    - Auto-format on save
    - Format on type
    - Custom formatting rules
    - Text edit generation
    - Formatting options
    """
    
    def __init__(self, config: Optional[FormattingConfig] = None):
        """
        Initialize formatting engine.
        
        Args:
            config: Formatting configuration
        """
        self.config = config or FormattingConfig()
        self._initialize_rules()
    
    def _initialize_rules(self) -> None:
        """Initialize formatting rules."""
        self.rules = {
            "python": {
                "indent": self.config.indent_size,
                "use_tabs": self.config.use_tabs,
                "max_line_length": self.config.max_line_length
            },
            "javascript": {
                "indent": self.config.indent_size,
                "use_tabs": self.config.use_tabs,
                "max_line_length": self.config.max_line_length
            },
            "typescript": {
                "indent": self.config.indent_size,
                "use_tabs": self.config.use_tabs,
                "max_line_length": self.config.max_line_length
            },
            "go": {
                "indent": 4,
                "use_tabs": True,
                "max_line_length": 100
            },
            "rust": {
                "indent": 4,
                "use_tabs": False,
                "max_line_length": 100
            }
        }
    
    def format_document(
        self,
        text: str,
        language: str = "python",
        params: Optional[DocumentFormattingParams] = None
    ) -> List[TextEdit]:
        """
        Format document.
        
        Args:
            text: Document text
            language: Language identifier
            params: Formatting parameters
            
        Returns:
            List[TextEdit]: Text edits
        """
        if params is None:
            params = DocumentFormattingParams(options=FormattingOptions())
        
        edits = []
        formatted_text = text
        
        # Trim trailing whitespace
        if params.options.trim_trailing_whitespace or self.config.trim_trailing_whitespace:
            formatted_text = self._trim_trailing_whitespace(formatted_text)
        
        # Trim final newlines
        if params.options.trim_final_newlines:
            formatted_text = self._trim_final_newlines(formatted_text)
        
        # Insert final newline
        if params.options.insert_final_newline or self.config.insert_final_newline:
            formatted_text = self._insert_final_newline(formatted_text)
        
        # Enforce line length
        if params.options.keep_line_length:
            formatted_text = self._enforce_line_length(formatted_text, params.options.keep_line_length)
        
        # Apply indentation
        formatted_text = self._apply_indentation(formatted_text, language)
        
        # Generate edit if text changed
        if formatted_text != text:
            edits.append(TextEdit(
                range=Range(
                    start=Position(line=0, character=0),
                    end=Position(line=len(text.split('\n')), character=0)
                ),
                newText=formatted_text
            ))
        
        return edits
    
    def format_range(
        self,
        text: str,
        range_obj: Range,
        language: str = "python"
    ) -> List[TextEdit]:
        """
        Format range.
        
        Args:
            text: Document text
            range_obj: Range to format
            language: Language identifier
            
        Returns:
            List[TextEdit]: Text edits
        """
        lines = text.split('\n')
        start_line = range_obj.start.line
        end_line = range_obj.end.line
        
        # Extract range
        range_lines = lines[start_line:end_line + 1]
        range_text = '\n'.join(range_lines)
        
        # Format range
        formatted_range = self._apply_indentation(range_text, language)
        formatted_range = self._trim_trailing_whitespace(formatted_range)
        
        # Generate edit
        edits = []
        if formatted_range != range_text:
            edits.append(TextEdit(
                range=range_obj,
                newText=formatted_range
            ))
        
        return edits
    
    def _trim_trailing_whitespace(self, text: str) -> str:
        """
        Trim trailing whitespace.
        
        Args:
            text: Text to trim
            
        Returns:
            str: Trimmed text
        """
        lines = text.split('\n')
        trimmed_lines = [line.rstrip() for line in lines]
        return '\n'.join(trimmed_lines)
    
    def _trim_final_newlines(self, text: str) -> str:
        """
        Trim final newlines.
        
        Args:
            text: Text to trim
            
        Returns:
            str: Trimmed text
        """
        return text.rstrip('\n')
    
    def _insert_final_newline(self, text: str) -> str:
        """
        Insert final newline.
        
        Args:
            text: Text to modify
            
        Returns:
            str: Modified text
        """
        if text and not text.endswith('\n'):
            return text + '\n'
        return text
    
    def _enforce_line_length(self, text: str, max_length: int) -> str:
        """
        Enforce line length.
        
        Args:
            text: Text to format
            max_length: Maximum line length
            
        Returns:
            str: Formatted text
        """
        lines = text.split('\n')
        formatted_lines = []
        
        for line in lines:
            if len(line) <= max_length:
                formatted_lines.append(line)
            else:
                # Simple line breaking (placeholder)
                # In a real implementation, this would use a proper line-breaking algorithm
                formatted_lines.append(line[:max_length])
        
        return '\n'.join(formatted_lines)
    
    def _apply_indentation(self, text: str, language: str) -> str:
        """
        Apply indentation.
        
        Args:
            text: Text to indent
            language: Language identifier
            
        Returns:
            str: Indented text
        """
        rules = self.rules.get(language, self.rules.get("python", {}))
        indent_size = rules.get("indent", 4)
        use_tabs = rules.get("use_tabs", False)
        
        lines = text.split('\n')
        indented_lines = []
        indent_level = 0
        
        for line in lines:
            stripped = line.lstrip()
            
            # Adjust indent level based on line content
            if stripped.endswith(':') or stripped.startswith(('class ', 'def ', 'if ', 'else:', 'elif ', 'for ', 'while ', 'try:', 'except', 'finally:', 'with ')):
                # Increase indent after this line
                pass
            
            # Apply indentation
            if use_tabs:
                indent = '\t' * indent_level
            else:
                indent = ' ' * (indent_level * indent_size)
            
            indented_lines.append(indent + stripped)
            
            # Increase indent for next line
            if stripped.endswith(':') or stripped.startswith(('class ', 'def ', 'if ', 'for ', 'while ', 'try:', 'with ')):
                indent_level += 1
            
            # Decrease indent
            if stripped.startswith(('return', 'pass', 'break', 'continue', 'raise')):
                indent_level = max(0, indent_level - 1)
        
        return '\n'.join(indented_lines)
    
    def update_config(self, config: FormattingConfig) -> None:
        """
        Update formatting configuration.
        
        Args:
            config: New configuration
        """
        self.config = config
        self._initialize_rules()
    
    def get_config(self) -> FormattingConfig:
        """
        Get formatting configuration.
        
        Returns:
            FormattingConfig: Configuration
        """
        return self.config


if __name__ == "__main__":
    # Basit test
    config = FormattingConfig()
    engine = FormattingEngine(config)
    
    text = """
def hello():
pass
"""
    
    params = DocumentFormattingParams(options=FormattingOptions())
    edits = engine.format_document(text, "python", params)
    
    print(f"Edits: {len(edits)}")
    for edit in edits:
        print(f"  New text: {edit.newText}")
