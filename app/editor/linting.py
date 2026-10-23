"""
MuhammedAI Local Developer - Linting
Linting engine for code editor.
"""

import ast
import re
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from enum import Enum


class LintSeverity(Enum):
    """Lint severity."""
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
    HINT = "hint"


class LintCategory(Enum):
    """Lint category."""
    SYNTAX = "syntax"
    STYLE = "style"
    UNUSED = "unused"
    IMPORT = "import"
    COMPLEXITY = "complexity"
    SECURITY = "security"
    BEST_PRACTICE = "best_practice"
    PEP8 = "pep8"
    TYPE = "type"


class LintRule(Enum):
    """Lint rule."""
    SYNTAX_ERROR = "syntax_error"
    INDENTATION = "indentation"
    LINE_LENGTH = "line_length"
    TRAILING_WHITESPACE = "trailing_whitespace"
    UNUSED_VARIABLE = "unused_variable"
    UNUSED_IMPORT = "unused_import"
    IMPORT_ORDER = "import_order"
    MISSING_DOCSTRING = "missing_docstring"
    TOO_MANY_ARGUMENTS = "too_many_arguments"
    TOO_MANY_BRANCHES = "too_many_branches"
    TOO_MANY_STATEMENTS = "too_many_statements"
    SECURITY_RISK = "security_risk"
    HARD_CODED_PASSWORD = "hard_coded_password"
    SQL_INJECTION = "sql_injection"
    EVAL_USAGE = "eval_usage"
    EXEC_USAGE = "exec_usage"
    PRINT_USAGE = "print_usage"
    GLOBAL_VARIABLE = "global_variable"
    SHADOWING = "shadowing"
    MISSING_RETURN = "missing_return"
    UNREACHABLE_CODE = "unreachable_code"


@dataclass
class LintIssue:
    """Lint issue."""
    rule: LintRule
    category: LintCategory
    severity: LintSeverity
    line: int
    column: int
    message: str
    suggestion: Optional[str] = None
    file_path: Optional[str] = None


@dataclass
class LintResult:
    """Lint result."""
    success: bool
    issues: List[LintIssue] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    file_path: Optional[str] = None
    message: Optional[str] = None


class Linter:
    """
    Linting engine.
    
    Özellikler:
    - Syntax error detection
    - Style issue detection
    - Unused variable detection
    - Unused import detection
    - Code complexity analysis
    - Security vulnerability detection
    - Best practice violations
    - PEP8 compliance checking
    - Multiple severity levels
    - Auto-fix suggestions
    """
    
    def __init__(self):
        """Initialize linter."""
        self.max_line_length = 88
        self.max_function_length = 50
        self.max_complexity = 10
        self.max_arguments = 5
    
    def lint(
        self,
        code: str,
        file_path: Optional[str] = None,
        language: str = "python"
    ) -> LintResult:
        """
        Kodu lint et.
        
        Args:
            code: Kod içeriği
            file_path: Dosya yolu
            language: Programlama dili
            
        Returns:
            LintResult: Lint sonucu
        """
        result = LintResult(success=False)
        result.file_path = file_path
        
        try:
            issues = []
            
            if language == "python":
                issues = self._lint_python(code, file_path)
            else:
                issues = self._lint_generic(code, file_path)
            
            result.issues = issues
            result.success = True
            result.message = f"Found {len(issues)} issues"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def _lint_python(
        self,
        code: str,
        file_path: Optional[str] = None
    ) -> List[LintIssue]:
        """Python kodunu lint et."""
        issues = []
        lines = code.splitlines()
        
        # Syntax error kontrolü
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            issues.append(LintIssue(
                rule=LintRule.SYNTAX_ERROR,
                category=LintCategory.SYNTAX,
                severity=LintSeverity.ERROR,
                line=e.lineno or 1,
                column=e.offset or 0,
                message=f"Syntax error: {e.msg}",
                file_path=file_path
            ))
            return issues
        
        # Line-by-line kontrol
        for i, line in enumerate(lines, 1):
            # Line length
            if len(line) > self.max_line_length:
                issues.append(LintIssue(
                    rule=LintRule.LINE_LENGTH,
                    category=LintCategory.PEP8,
                    severity=LintSeverity.WARNING,
                    line=i,
                    column=self.max_line_length,
                    message=f"Line too long ({len(line)} > {self.max_line_length})",
                    suggestion="Break the line into multiple lines",
                    file_path=file_path
                ))
            
            # Trailing whitespace
            if line != line.rstrip():
                issues.append(LintIssue(
                    rule=LintRule.TRAILING_WHITESPACE,
                    category=LintCategory.STYLE,
                    severity=LintSeverity.WARNING,
                    line=i,
                    column=len(line.rstrip()),
                    message="Trailing whitespace",
                    suggestion="Remove trailing whitespace",
                    file_path=file_path
                ))
            
            # Indentation
            if line.startswith(" ") and not line.startswith("    ") and not line.startswith("        "):
                issues.append(LintIssue(
                    rule=LintRule.INDENTATION,
                    category=LintCategory.PEP8,
                    severity=LintSeverity.ERROR,
                    line=i,
                    column=0,
                    message="Indentation not multiple of 4",
                    suggestion="Use 4 spaces per indentation level",
                    file_path=file_path
                ))
        
        # AST-based kontrol
        issues.extend(self._check_unused_variables(tree, file_path))
        issues.extend(self._check_unused_imports(tree, file_path))
        issues.extend(self._check_missing_docstrings(tree, file_path))
        issues.extend(self._check_complexity(tree, file_path))
        issues.extend(self._check_security_issues(tree, file_path))
        issues.extend(self._check_best_practices(tree, file_path))
        
        return issues
    
    def _lint_generic(
        self,
        code: str,
        file_path: Optional[str] = None
    ) -> List[LintIssue]:
        """Genel kod lint et."""
        issues = []
        lines = code.splitlines()
        
        for i, line in enumerate(lines, 1):
            # Trailing whitespace
            if line != line.rstrip():
                issues.append(LintIssue(
                    rule=LintRule.TRAILING_WHITESPACE,
                    category=LintCategory.STYLE,
                    severity=LintSeverity.WARNING,
                    line=i,
                    column=len(line.rstrip()),
                    message="Trailing whitespace",
                    file_path=file_path
                ))
        
        return issues
    
    def _check_unused_variables(
        self,
        tree: ast.AST,
        file_path: Optional[str] = None
    ) -> List[LintIssue]:
        """Unused variable kontrolü."""
        issues = []
        
        # Basit kontrol - function scope
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                assigned_vars = set()
                used_vars = set()
                
                for child in ast.walk(node):
                    if isinstance(child, ast.Assign):
                        for target in child.targets:
                            if isinstance(target, ast.Name):
                                assigned_vars.add(target.id)
                    elif isinstance(child, ast.Name):
                        if isinstance(child.ctx, ast.Load):
                            used_vars.add(child.id)
                
                unused = assigned_vars - used_vars
                for var in unused:
                    if var != "_":  # _ kullanılmadığını belirtmek için
                        issues.append(LintIssue(
                            rule=LintRule.UNUSED_VARIABLE,
                            category=LintCategory.UNUSED,
                            severity=LintSeverity.WARNING,
                            line=node.lineno,
                            column=node.col_offset,
                            message=f"Unused variable '{var}'",
                            suggestion=f"Remove or use variable '{var}'",
                            file_path=file_path
                        ))
        
        return issues
    
    def _check_unused_imports(
        self,
        tree: ast.AST,
        file_path: Optional[str] = None
    ) -> List[LintIssue]:
        """Unused import kontrolü."""
        issues = []
        
        imported_names = set()
        used_names = set()
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imported_names.add(alias.asname or alias.name)
            elif isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    imported_names.add(alias.asname or alias.name)
            elif isinstance(node, ast.Name):
                used_names.add(node.id)
        
        unused = imported_names - used_names
        for name in unused:
            issues.append(LintIssue(
                rule=LintRule.UNUSED_IMPORT,
                category=LintCategory.IMPORT,
                severity=LintSeverity.WARNING,
                line=1,
                column=0,
                message=f"Unused import '{name}'",
                suggestion=f"Remove unused import '{name}'",
                file_path=file_path
            ))
        
        return issues
    
    def _check_missing_docstrings(
        self,
        tree: ast.AST,
        file_path: Optional[str] = None
    ) -> List[LintIssue]:
        """Missing docstring kontrolü."""
        issues = []
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                # Docstring kontrolü
                has_docstring = (
                    node.body and
                    isinstance(node.body[0], ast.Expr) and
                    isinstance(node.body[0].value, ast.Constant) and
                    isinstance(node.body[0].value.value, str)
                )
                
                if not has_docstring:
                    issues.append(LintIssue(
                        rule=LintRule.MISSING_DOCSTRING,
                        category=LintCategory.BEST_PRACTICE,
                        severity=LintSeverity.INFO,
                        line=node.lineno,
                        column=node.col_offset,
                        message=f"Missing docstring for {node.__class__.__name__} '{node.name}'",
                        suggestion=f"Add docstring to {node.__class__.__name__} '{node.name}'",
                        file_path=file_path
                    ))
        
        return issues
    
    def _check_complexity(
        self,
        tree: ast.AST,
        file_path: Optional[str] = None
    ) -> List[LintIssue]:
        """Complexity kontrolü."""
        issues = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Argument count
                arg_count = len(node.args.args)
                if arg_count > self.max_arguments:
                    issues.append(LintIssue(
                        rule=LintRule.TOO_MANY_ARGUMENTS,
                        category=LintCategory.COMPLEXITY,
                        severity=LintSeverity.WARNING,
                        line=node.lineno,
                        column=node.col_offset,
                        message=f"Too many arguments ({arg_count} > {self.max_arguments})",
                        suggestion="Consider using dataclasses or configuration objects",
                        file_path=file_path
                    ))
        
        return issues
    
    def _check_security_issues(
        self,
        tree: ast.AST,
        file_path: Optional[str] = None
    ) -> List[LintIssue]:
        """Security issue kontrolü."""
        issues = []
        
        for node in ast.walk(tree):
            # eval/exec usage
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    if node.func.id == "eval":
                        issues.append(LintIssue(
                            rule=LintRule.EVAL_USAGE,
                            category=LintCategory.SECURITY,
                            severity=LintSeverity.ERROR,
                            line=node.lineno,
                            column=node.col_offset,
                            message="Use of eval() is dangerous",
                            suggestion="Avoid using eval() for security reasons",
                            file_path=file_path
                        ))
                    elif node.func.id == "exec":
                        issues.append(LintIssue(
                            rule=LintRule.EXEC_USAGE,
                            category=LintCategory.SECURITY,
                            severity=LintSeverity.ERROR,
                            line=node.lineno,
                            column=node.col_offset,
                            message="Use of exec() is dangerous",
                            suggestion="Avoid using exec() for security reasons",
                            file_path=file_path
                        ))
        
        return issues
    
    def _check_best_practices(
        self,
        tree: ast.AST,
        file_path: Optional[str] = None
    ) -> List[LintIssue]:
        """Best practice kontrolü."""
        issues = []
        
        for node in ast.walk(tree):
            # print usage
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    if node.func.id == "print":
                        issues.append(LintIssue(
                            rule=LintRule.PRINT_USAGE,
                            category=LintCategory.BEST_PRACTICE,
                            severity=LintSeverity.INFO,
                            line=node.lineno,
                            column=node.col_offset,
                            message="Use of print() in production code",
                            suggestion="Consider using proper logging",
                            file_path=file_path
                        ))
        
        return issues


if __name__ == "__main__":
    # Basit test
    linter = Linter()
    
    code = """
def my_function(x, y, z, a, b, c):
    result = x + y
    unused_var = 10
    print(result)
    return result
"""
    
    result = linter.lint(code, language="python")
    print(f"Linting: {result.success}")
    print(f"Issues: {len(result.issues)}")
    
    for issue in result.issues:
        print(f"  - Line {issue.line}: {issue.message} ({issue.severity.value})")
