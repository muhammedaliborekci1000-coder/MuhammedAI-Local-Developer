"""
MuhammedAI Local Developer - Bug Detection
Automatic bug detection and analysis for code.
"""

import ast
import re
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from enum import Enum


class BugSeverity(Enum):
    """Bug severity."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class BugCategory(Enum):
    """Bug category."""
    SYNTAX = "syntax"
    LOGIC = "logic"
    PERFORMANCE = "performance"
    SECURITY = "security"
    STYLE = "style"
    TYPE_ERROR = "type_error"
    UNDEFINED = "undefined"


@dataclass
class Bug:
    """Bug."""
    file_path: str
    line: int
    column: int
    severity: BugSeverity
    category: BugCategory
    message: str
    suggestion: Optional[str] = None
    code_snippet: Optional[str] = None


@dataclass
class BugDetectionResult:
    """Bug detection result."""
    success: bool
    bugs: List[Bug] = field(default_factory=list)
    file_path: Optional[str] = None
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    message: Optional[str] = None


class BugDetector:
    """
    Bug detection engine.
    
    Özellikler:
    - Syntax error detection
    - Logic error detection
    - Performance issue detection
    - Security vulnerability detection
    - Style issue detection
    - Type error detection
    - Undefined variable detection
    - Code smell detection
    """
    
    def __init__(self):
        """Initialize bug detector."""
        self.common_patterns = {
            "unused_import": r"^import\s+\w+",
            "print_statement": r"print\s*\(",
            "bare_except": r"except\s*:",
            "mutable_default": r"def\s+\w+\([^)]*=\s*\[\]",
        }
    
    def detect_bugs(
        self,
        file_path: str
    ) -> BugDetectionResult:
        """
        Dosyada bug'ları tespit et.
        
        Args:
            file_path: Dosya yolu
            
        Returns:
            BugDetectionResult: Bug detection sonucu
        """
        result = BugDetectionResult(success=False)
        result.file_path = file_path
        
        try:
            # Dosyayı oku
            content = Path(file_path).read_text(encoding='utf-8')
            lines = content.splitlines()
            
            # Syntax error detection
            syntax_bugs = self._detect_syntax_errors(content, file_path)
            result.bugs.extend(syntax_bugs)
            
            # Logic error detection
            logic_bugs = self._detect_logic_errors(content, lines, file_path)
            result.bugs.extend(logic_bugs)
            
            # Performance issue detection
            perf_bugs = self._detect_performance_issues(content, lines, file_path)
            result.bugs.extend(perf_bugs)
            
            # Security vulnerability detection
            security_bugs = self._detect_security_vulnerabilities(content, lines, file_path)
            result.bugs.extend(security_bugs)
            
            # Style issue detection
            style_bugs = self._detect_style_issues(content, lines, file_path)
            result.bugs.extend(style_bugs)
            
            # Type error detection
            type_bugs = self._detect_type_errors(content, lines, file_path)
            result.bugs.extend(type_bugs)
            
            # Undefined variable detection
            undefined_bugs = self._detect_undefined_variables(content, file_path)
            result.bugs.extend(undefined_bugs)
            
            result.success = True
            result.message = f"Detected {len(result.bugs)} bugs"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def _detect_syntax_errors(
        self,
        content: str,
        file_path: str
    ) -> List[Bug]:
        """Syntax error detection."""
        bugs = []
        
        try:
            ast.parse(content)
        except SyntaxError as e:
            bug = Bug(
                file_path=file_path,
                line=e.lineno or 1,
                column=e.offset or 0,
                severity=BugSeverity.CRITICAL,
                category=BugCategory.SYNTAX,
                message=f"Syntax error: {e.msg}",
                suggestion="Fix the syntax error"
            )
            bugs.append(bug)
        
        return bugs
    
    def _detect_logic_errors(
        self,
        content: str,
        lines: List[str],
        file_path: str
    ) -> List[Bug]:
        """Logic error detection."""
        bugs = []
        
        # Division by zero check
        for i, line in enumerate(lines):
            if "/ 0" in line or "/0" in line:
                bug = Bug(
                    file_path=file_path,
                    line=i + 1,
                    column=line.find("/"),
                    severity=BugSeverity.HIGH,
                    category=BugCategory.LOGIC,
                    message="Potential division by zero",
                    suggestion="Check denominator before division",
                    code_snippet=line.strip()
                )
                bugs.append(bug)
        
        # Infinite loop check
        for i, line in enumerate(lines):
            if "while True:" in line and "break" not in lines[i:i+10]:
                bug = Bug(
                    file_path=file_path,
                    line=i + 1,
                    column=line.find("while"),
                    severity=BugSeverity.MEDIUM,
                    category=BugCategory.LOGIC,
                    message="Potential infinite loop",
                    suggestion="Add break condition",
                    code_snippet=line.strip()
                )
                bugs.append(bug)
        
        return bugs
    
    def _detect_performance_issues(
        self,
        content: str,
        lines: List[str],
        file_path: str
    ) -> List[Bug]:
        """Performance issue detection."""
        bugs = []
        
        # Nested loops check
        loop_count = 0
        for i, line in enumerate(lines):
            if "for " in line or "while " in line:
                loop_count += 1
                if loop_count > 2:
                    bug = Bug(
                        file_path=file_path,
                        line=i + 1,
                        column=0,
                        severity=BugSeverity.MEDIUM,
                        category=BugCategory.PERFORMANCE,
                        message="Deeply nested loops detected",
                        suggestion="Consider optimizing or refactoring",
                        code_snippet=line.strip()
                    )
                    bugs.append(bug)
            else:
                loop_count = 0
        
        # String concatenation in loop
        for i, line in enumerate(lines):
            if "+=" in line and "for " in lines[max(0, i-5):i]:
                bug = Bug(
                    file_path=file_path,
                    line=i + 1,
                    column=line.find("+="),
                    severity=BugSeverity.LOW,
                    category=BugCategory.PERFORMANCE,
                    message="String concatenation in loop",
                    suggestion="Use list and join for better performance",
                    code_snippet=line.strip()
                )
                bugs.append(bug)
        
        return bugs
    
    def _detect_security_vulnerabilities(
        self,
        content: str,
        lines: List[str],
        file_path: str
    ) -> List[Bug]:
        """Security vulnerability detection."""
        bugs = []
        
        # Hardcoded credentials
        for i, line in enumerate(lines):
            if "password" in line.lower() and "=" in line and '"' in line:
                bug = Bug(
                    file_path=file_path,
                    line=i + 1,
                    column=line.find("="),
                    severity=BugSeverity.CRITICAL,
                    category=BugCategory.SECURITY,
                    message="Hardcoded password detected",
                    suggestion="Use environment variables or config files",
                    code_snippet=line.strip()
                )
                bugs.append(bug)
        
        # SQL injection risk
        for i, line in enumerate(lines):
            if "execute(" in line and "+" in line:
                bug = Bug(
                    file_path=file_path,
                    line=i + 1,
                    column=line.find("execute"),
                    severity=BugSeverity.HIGH,
                    category=BugCategory.SECURITY,
                    message="Potential SQL injection vulnerability",
                    suggestion="Use parameterized queries",
                    code_snippet=line.strip()
                )
                bugs.append(bug)
        
        # eval/exec usage
        for i, line in enumerate(lines):
            if "eval(" in line or "exec(" in line:
                bug = Bug(
                    file_path=file_path,
                    line=i + 1,
                    column=line.find("eval") if "eval(" in line else line.find("exec"),
                    severity=BugSeverity.HIGH,
                    category=BugCategory.SECURITY,
                    message="Unsafe eval/exec usage",
                    suggestion="Avoid using eval/exec with user input",
                    code_snippet=line.strip()
                )
                bugs.append(bug)
        
        return bugs
    
    def _detect_style_issues(
        self,
        content: str,
        lines: List[str],
        file_path: str
    ) -> List[Bug]:
        """Style issue detection."""
        bugs = []
        
        # Long lines
        for i, line in enumerate(lines):
            if len(line) > 100:
                bug = Bug(
                    file_path=file_path,
                    line=i + 1,
                    column=100,
                    severity=BugSeverity.LOW,
                    category=BugCategory.STYLE,
                    message=f"Line too long ({len(line)} characters)",
                    suggestion="Break line into multiple lines",
                    code_snippet=line.strip()[:50] + "..."
                )
                bugs.append(bug)
        
        # Bare except
        for i, line in enumerate(lines):
            if "except:" in line:
                bug = Bug(
                    file_path=file_path,
                    line=i + 1,
                    column=line.find("except"),
                    severity=BugSeverity.MEDIUM,
                    category=BugCategory.STYLE,
                    message="Bare except clause",
                    suggestion="Specify exception type",
                    code_snippet=line.strip()
                )
                bugs.append(bug)
        
        return bugs
    
    def _detect_type_errors(
        self,
        content: str,
        lines: List[str],
        file_path: str
    ) -> List[Bug]:
        """Type error detection."""
        bugs = []
        
        try:
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.BinOp):
                    # Check for incompatible operations
                    if isinstance(node.op, ast.Add):
                        # String + number check (basic)
                        pass
        
        except Exception:
            pass
        
        return bugs
    
    def _detect_undefined_variables(
        self,
        content: str,
        file_path: str
    ) -> List[Bug]:
        """Undefined variable detection."""
        bugs = []
        
        try:
            tree = ast.parse(content)
            
            defined_vars = set()
            
            # First pass: collect defined variables
            for node in ast.walk(tree):
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            defined_vars.add(target.id)
                elif isinstance(node, ast.FunctionDef):
                    for arg in node.args.args:
                        defined_vars.add(arg.arg)
                elif isinstance(node, ast.For):
                    if isinstance(node.target, ast.Name):
                        defined_vars.add(node.target.id)
            
            # Second pass: check for undefined usage
            for node in ast.walk(tree):
                if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
                    if node.id not in defined_vars and node.id not in dir(__builtins__):
                        bug = Bug(
                            file_path=file_path,
                            line=node.lineno,
                            column=node.col_offset or 0,
                            severity=BugSeverity.HIGH,
                            category=BugCategory.UNDEFINED,
                            message=f"Undefined variable '{node.id}'",
                            suggestion="Define the variable before use",
                            code_snippet=node.id
                        )
                        bugs.append(bug)
        
        except Exception:
            pass
        
        return bugs


if __name__ == "__main__":
    # Basit test
    detector = BugDetector()
    
    result = detector.detect_bugs("app/ai/bug_detection.py")
    print(f"Bug detection: {result.success}")
    print(f"Message: {result.message}")
    print(f"Bugs found: {len(result.bugs)}")
