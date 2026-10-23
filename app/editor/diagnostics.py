"""
MuhammedAI Local Developer - Diagnostics
Code diagnostics system for error detection and reporting.
"""

import re
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum


class DiagnosticSeverity(Enum):
    """Diagnostic severity levels."""
    ERROR = 1
    WARNING = 2
    INFORMATION = 3
    HINT = 4


class DiagnosticTag(Enum):
    """Diagnostic tags."""
    UNNECESSARY = 1
    DEPRECATED = 2


class DiagnosticSource(Enum):
    """Diagnostic source."""
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    LINT = "lint"
    TYPE_CHECK = "type-check"
    SYNTAX = "syntax"
    STYLE = "style"


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
class Diagnostic:
    """Diagnostic information."""
    range: Range
    severity: Optional[DiagnosticSeverity] = None
    code: Optional[Union[str, int]] = None
    source: Optional[str] = None
    message: str = ""
    tags: Optional[List[DiagnosticTag]] = None
    relatedInformation: Optional[List[Any]] = None


@dataclass
class PublishDiagnosticsParams:
    """Publish diagnostics parameters."""
    uri: str
    version: Optional[int] = None
    diagnostics: List[Diagnostic] = field(default_factory=list)


@dataclass
class DiagnosticConfig:
    """Diagnostic configuration."""
    enable_errors: bool = True
    enable_warnings: bool = True
    enable_information: bool = True
    enable_hints: bool = True
    max_diagnostics: int = 100
    check_syntax: bool = True
    check_lint: bool = True
    check_type: bool = True
    check_style: bool = False
    auto_fix: bool = False


class DiagnosticsEngine:
    """
    Diagnostics engine.
    
    Özellikler:
    - Syntax error detection
    - Linting
    - Type checking
    - Style checking
    - Error reporting
    - Warning reporting
    - Information reporting
    - Hint reporting
    - Diagnostic filtering
    - Diagnostic sorting
    - Diagnostic history
    - Configuration management
    - Multi-language support
    - Diagnostic tags
    - Related information
    - Auto-fix support
    """
    
    def __init__(self, config: Optional[DiagnosticConfig] = None):
        """
        Initialize diagnostics engine.
        
        Args:
            config: Diagnostic configuration
        """
        self.config = config or DiagnosticConfig()
        self.diagnostics_history: Dict[str, List[Diagnostic]] = {}
    
    def analyze(
        self,
        text: str,
        uri: str,
        language: str = "python"
    ) -> List[Diagnostic]:
        """
        Analyze text for diagnostics.
        
        Args:
            text: Document text
            uri: Document URI
            language: Language identifier
            
        Returns:
            List[Diagnostic]: Diagnostics
        """
        diagnostics = []
        
        # Syntax checking
        if self.config.check_syntax:
            syntax_diagnostics = self._check_syntax(text, uri, language)
            diagnostics.extend(syntax_diagnostics)
        
        # Lint checking
        if self.config.check_lint:
            lint_diagnostics = self._check_lint(text, uri, language)
            diagnostics.extend(lint_diagnostics)
        
        # Type checking
        if self.config.check_type:
            type_diagnostics = self._check_type(text, uri, language)
            diagnostics.extend(type_diagnostics)
        
        # Style checking
        if self.config.check_style:
            style_diagnostics = self._check_style(text, uri, language)
            diagnostics.extend(style_diagnostics)
        
        # Filter by severity
        diagnostics = self._filter_by_severity(diagnostics)
        
        # Limit results
        if len(diagnostics) > self.config.max_diagnostics:
            diagnostics = diagnostics[:self.config.max_diagnostics]
        
        # Store in history
        self.diagnostics_history[uri] = diagnostics
        
        return diagnostics
    
    def _check_syntax(self, text: str, uri: str, language: str) -> List[Diagnostic]:
        """
        Check syntax errors.
        
        Args:
            text: Document text
            uri: Document URI
            language: Language identifier
            
        Returns:
            List[Diagnostic]: Syntax diagnostics
        """
        diagnostics = []
        lines = text.split('\n')
        
        if language == "python":
            # Check for common Python syntax errors
            for i, line in enumerate(lines):
                # Check for unmatched brackets
                if line.count('(') != line.count(')'):
                    diagnostics.append(Diagnostic(
                        range=Range(
                            start=Position(line=i, character=0),
                            end=Position(line=i, character=len(line))
                        ),
                        severity=DiagnosticSeverity.ERROR,
                        source=DiagnosticSource.SYNTAX.value,
                        message="Unmatched parentheses"
                    ))
                
                # Check for unmatched brackets
                if line.count('[') != line.count(']'):
                    diagnostics.append(Diagnostic(
                        range=Range(
                            start=Position(line=i, character=0),
                            end=Position(line=i, character=len(line))
                        ),
                        severity=DiagnosticSeverity.ERROR,
                        source=DiagnosticSource.SYNTAX.value,
                        message="Unmatched brackets"
                    ))
                
                # Check for unmatched braces
                if line.count('{') != line.count('}'):
                    diagnostics.append(Diagnostic(
                        range=Range(
                            start=Position(line=i, character=0),
                            end=Position(line=i, character=len(line))
                        ),
                        severity=DiagnosticSeverity.ERROR,
                        source=DiagnosticSource.SYNTAX.value,
                        message="Unmatched braces"
                    ))
        
        elif language in ["javascript", "typescript"]:
            # Check for common JS/TS syntax errors
            for i, line in enumerate(lines):
                # Check for unmatched brackets
                if line.count('(') != line.count(')'):
                    diagnostics.append(Diagnostic(
                        range=Range(
                            start=Position(line=i, character=0),
                            end=Position(line=i, character=len(line))
                        ),
                        severity=DiagnosticSeverity.ERROR,
                        source=DiagnosticSource.SYNTAX.value,
                        message="Unmatched parentheses"
                    ))
        
        return diagnostics
    
    def _check_lint(self, text: str, uri: str, language: str) -> List[Diagnostic]:
        """
        Check linting issues.
        
        Args:
            text: Document text
            uri: Document URI
            language: Language identifier
            
        Returns:
            List[Diagnostic]: Lint diagnostics
        """
        diagnostics = []
        lines = text.split('\n')
        
        if language == "python":
            for i, line in enumerate(lines):
                # Check for lines too long
                if len(line) > 79:
                    diagnostics.append(Diagnostic(
                        range=Range(
                            start=Position(line=i, character=79),
                            end=Position(line=i, character=len(line))
                        ),
                        severity=DiagnosticSeverity.WARNING,
                        source=DiagnosticSource.LINT.value,
                        message=f"Line too long ({len(line)} > 79 characters)"
                    ))
                
                # Check for unused imports (simple check)
                if line.strip().startswith('import ') and ' as ' not in line:
                    import_name = line.strip().replace('import ', '').split(',')[0]
                    if import_name and not any(import_name in other_line for other_line in lines):
                        diagnostics.append(Diagnostic(
                            range=Range(
                                start=Position(line=i, character=0),
                                end=Position(line=i, character=len(line))
                            ),
                            severity=DiagnosticSeverity.WARNING,
                            source=DiagnosticSource.LINT.value,
                            message=f"Unused import: {import_name}",
                            tags=[DiagnosticTag.UNNECESSARY]
                        ))
        
        return diagnostics
    
    def _check_type(self, text: str, uri: str, language: str) -> List[Diagnostic]:
        """
        Check type errors.
        
        Args:
            text: Document text
            uri: Document URI
            language: Language identifier
            
        Returns:
            List[Diagnostic]: Type diagnostics
        """
        diagnostics = []
        
        # Simple type checking (placeholder)
        # In a real implementation, this would use a type checker like mypy or tsc
        
        return diagnostics
    
    def _check_style(self, text: str, uri: str, language: str) -> List[Diagnostic]:
        """
        Check style issues.
        
        Args:
            text: Document text
            uri: Document URI
            language: Language identifier
            
        Returns:
            List[Diagnostic]: Style diagnostics
        """
        diagnostics = []
        lines = text.split('\n')
        
        if language == "python":
            for i, line in enumerate(lines):
                # Check for trailing whitespace
                if line.endswith(' ') or line.endswith('\t'):
                    diagnostics.append(Diagnostic(
                        range=Range(
                            start=Position(line=i, character=len(line.rstrip())),
                            end=Position(line=i, character=len(line))
                        ),
                        severity=DiagnosticSeverity.WARNING,
                        source=DiagnosticSource.STYLE.value,
                        message="Trailing whitespace"
                    ))
                
                # Check for multiple consecutive blank lines
                if i > 0 and not lines[i-1].strip() and not line.strip():
                    diagnostics.append(Diagnostic(
                        range=Range(
                            start=Position(line=i, character=0),
                            end=Position(line=i, character=len(line))
                        ),
                        severity=DiagnosticSeverity.INFORMATION,
                        source=DiagnosticSource.STYLE.value,
                        message="Multiple consecutive blank lines"
                    ))
        
        return diagnostics
    
    def _filter_by_severity(self, diagnostics: List[Diagnostic]) -> List[Diagnostic]:
        """
        Filter diagnostics by severity.
        
        Args:
            diagnostics: Diagnostics list
            
        Returns:
            List[Diagnostic]: Filtered diagnostics
        """
        filtered = []
        
        for diagnostic in diagnostics:
            if diagnostic.severity == DiagnosticSeverity.ERROR and self.config.enable_errors:
                filtered.append(diagnostic)
            elif diagnostic.severity == DiagnosticSeverity.WARNING and self.config.enable_warnings:
                filtered.append(diagnostic)
            elif diagnostic.severity == DiagnosticSeverity.INFORMATION and self.config.enable_information:
                filtered.append(diagnostic)
            elif diagnostic.severity == DiagnosticSeverity.HINT and self.config.enable_hints:
                filtered.append(diagnostic)
            elif diagnostic.severity is None and self.config.enable_errors:
                filtered.append(diagnostic)
        
        return filtered
    
    def get_diagnostics(self, uri: str) -> List[Diagnostic]:
        """
        Get diagnostics for document.
        
        Args:
            uri: Document URI
            
        Returns:
            List[Diagnostic]: Diagnostics
        """
        return self.diagnostics_history.get(uri, [])
    
    def clear_diagnostics(self, uri: str) -> None:
        """
        Clear diagnostics for document.
        
        Args:
            uri: Document URI
        """
        if uri in self.diagnostics_history:
            del self.diagnostics_history[uri]
    
    def clear_all_diagnostics(self) -> None:
        """Clear all diagnostics."""
        self.diagnostics_history.clear()
    
    def get_diagnostic_count(self, uri: str, severity: Optional[DiagnosticSeverity] = None) -> int:
        """
        Get diagnostic count.
        
        Args:
            uri: Document URI
            severity: Severity filter
            
        Returns:
            int: Diagnostic count
        """
        diagnostics = self.diagnostics_history.get(uri, [])
        
        if severity:
            return len([d for d in diagnostics if d.severity == severity])
        
        return len(diagnostics)
    
    def get_error_count(self, uri: str) -> int:
        """
        Get error count.
        
        Args:
            uri: Document URI
            
        Returns:
            int: Error count
        """
        return self.get_diagnostic_count(uri, DiagnosticSeverity.ERROR)
    
    def get_warning_count(self, uri: str) -> int:
        """
        Get warning count.
        
        Args:
            uri: Document URI
            
        Returns:
            int: Warning count
        """
        return self.get_diagnostic_count(uri, DiagnosticSeverity.WARNING)
    
    def update_config(self, config: DiagnosticConfig) -> None:
        """
        Update diagnostic configuration.
        
        Args:
            config: New configuration
        """
        self.config = config
    
    def get_config(self) -> DiagnosticConfig:
        """
        Get diagnostic configuration.
        
        Returns:
            DiagnosticConfig: Configuration
        """
        return self.config
    
    def publish_diagnostics(self, uri: str, version: Optional[int] = None) -> PublishDiagnosticsParams:
        """
        Create publish diagnostics parameters.
        
        Args:
            uri: Document URI
            version: Document version
            
        Returns:
            PublishDiagnosticsParams: Publish parameters
        """
        diagnostics = self.get_diagnostics(uri)
        
        return PublishDiagnosticsParams(
            uri=uri,
            version=version,
            diagnostics=diagnostics
        )


if __name__ == "__main__":
    # Basit test
    config = DiagnosticConfig()
    engine = DiagnosticsEngine(config)
    
    text = """
def hello():
    print("Hello World")
    
def world():
    print("World")
"""
    
    diagnostics = engine.analyze(text, "file:///test.py", "python")
    
    print(f"Diagnostics: {len(diagnostics)}")
    for diagnostic in diagnostics:
        print(f"  - {diagnostic.message} ({diagnostic.severity.value if diagnostic.severity else 'N/A'})")
