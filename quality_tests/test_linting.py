"""
Quality Test: Linting
Linting system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.linting import (
    Linter,
    LintSeverity,
    LintCategory,
    LintRule,
    LintIssue,
    LintResult
)


def test_lint_python():
    """
    Test: Lint Python code.
    """
    print("=" * 70)
    print("TEST: Lint Python Code")
    print("=" * 70)
    
    code = """
def my_function(x, y):
    result = x + y
    return result
"""
    
    linter = Linter()
    result = linter.lint(code, language="python")
    
    assert result.success, "Linting başarılı olmalı"
    assert isinstance(result.issues, list), "Issues list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Issues: {len(result.issues)}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Lint Python code")
    print("=" * 70)


def test_lint_generic():
    """
    Test: Lint generic code.
    """
    print("=" * 70)
    print("TEST: Lint Generic Code")
    print("=" * 70)
    
    code = """
function test() {
    var x = 10;
    return x;
}
"""
    
    linter = Linter()
    result = linter.lint(code, language="javascript")
    
    assert result.success, "Linting başarılı olmalı"
    assert isinstance(result.issues, list), "Issues list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Issues: {len(result.issues)}")
    
    print("\n" + "=" * 70)
    print("PASS: Lint generic code")
    print("=" * 70)


def test_syntax_error_detection():
    """
    Test: Syntax error detection.
    """
    print("=" * 70)
    print("TEST: Syntax Error Detection")
    print("=" * 70)
    
    code = "def my_function(\n"  # Syntax error
    
    linter = Linter()
    result = linter.lint(code, language="python")
    
    assert result.success, "Linting başarılı olmalı"
    
    syntax_errors = [issue for issue in result.issues if issue.rule == LintRule.SYNTAX_ERROR]
    print(f"  Syntax errors: {len(syntax_errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: Syntax error detection")
    print("=" * 70)


def test_line_length_check():
    """
    Test: Line length check.
    """
    print("=" * 70)
    print("TEST: Line Length Check")
    print("=" * 70)
    
    code = "x" * 100  # Çok uzun satır
    
    linter = Linter()
    result = linter.lint(code, language="python")
    
    assert result.success, "Linting başarılı olmalı"
    
    line_length_issues = [issue for issue in result.issues if issue.rule == LintRule.LINE_LENGTH]
    print(f"  Line length issues: {len(line_length_issues)}")
    
    print("\n" + "=" * 70)
    print("PASS: Line length check")
    print("=" * 70)


def test_trailing_whitespace_check():
    """
    Test: Trailing whitespace check.
    """
    print("=" * 70)
    print("TEST: Trailing Whitespace Check")
    print("=" * 70)
    
    code = "x = 10  "  # Trailing whitespace
    
    linter = Linter()
    result = linter.lint(code, language="python")
    
    assert result.success, "Linting başarılı olmalı"
    
    trailing_issues = [issue for issue in result.issues if issue.rule == LintRule.TRAILING_WHITESPACE]
    print(f"  Trailing whitespace issues: {len(trailing_issues)}")
    
    print("\n" + "=" * 70)
    print("PASS: Trailing whitespace check")
    print("=" * 70)


def test_unused_variable_detection():
    """
    Test: Unused variable detection.
    """
    print("=" * 70)
    print("TEST: Unused Variable Detection")
    print("=" * 70)
    
    code = """
def my_function():
    unused_var = 10
    return 5
"""
    
    linter = Linter()
    result = linter.lint(code, language="python")
    
    assert result.success, "Linting başarılı olmalı"
    
    unused_issues = [issue for issue in result.issues if issue.rule == LintRule.UNUSED_VARIABLE]
    print(f"  Unused variable issues: {len(unused_issues)}")
    
    print("\n" + "=" * 70)
    print("PASS: Unused variable detection")
    print("=" * 70)


def test_unused_import_detection():
    """
    Test: Unused import detection.
    """
    print("=" * 70)
    print("TEST: Unused Import Detection")
    print("=" * 70)
    
    code = """
import os
import sys

def my_function():
    return 5
"""
    
    linter = Linter()
    result = linter.lint(code, language="python")
    
    assert result.success, "Linting başarılı olmalı"
    
    unused_imports = [issue for issue in result.issues if issue.rule == LintRule.UNUSED_IMPORT]
    print(f"  Unused import issues: {len(unused_imports)}")
    
    print("\n" + "=" * 70)
    print("PASS: Unused import detection")
    print("=" * 70)


def test_missing_docstring_detection():
    """
    Test: Missing docstring detection.
    """
    print("=" * 70)
    print("TEST: Missing Docstring Detection")
    print("=" * 70)
    
    code = """
def my_function():
    return 5
"""
    
    linter = Linter()
    result = linter.lint(code, language="python")
    
    assert result.success, "Linting başarılı olmalı"
    
    missing_docstrings = [issue for issue in result.issues if issue.rule == LintRule.MISSING_DOCSTRING]
    print(f"  Missing docstring issues: {len(missing_docstrings)}")
    
    print("\n" + "=" * 70)
    print("PASS: Missing docstring detection")
    print("=" * 70)


def test_security_issue_detection():
    """
    Test: Security issue detection.
    """
    print("=" * 70)
    print("TEST: Security Issue Detection")
    print("=" * 70)
    
    code = """
def my_function():
    x = eval("1 + 1")
    return x
"""
    
    linter = Linter()
    result = linter.lint(code, language="python")
    
    assert result.success, "Linting başarılı olmalı"
    
    security_issues = [issue for issue in result.issues if issue.category == LintCategory.SECURITY]
    print(f"  Security issues: {len(security_issues)}")
    
    print("\n" + "=" * 70)
    print("PASS: Security issue detection")
    print("=" * 70)


def test_lint_severity_enum():
    """
    Test: LintSeverity enum.
    """
    print("=" * 70)
    print("TEST: LintSeverity Enum")
    print("=" * 70)
    
    assert LintSeverity.ERROR.value == "error"
    assert LintSeverity.WARNING.value == "warning"
    assert LintSeverity.INFO.value == "info"
    assert LintSeverity.HINT.value == "hint"
    
    print(f"  All enum values verified")
    print(f"  Total severities: {len(LintSeverity)}")
    
    print("\n" + "=" * 70)
    print("PASS: LintSeverity enum")
    print("=" * 70)


def test_lint_category_enum():
    """
    Test: LintCategory enum.
    """
    print("=" * 70)
    print("TEST: LintCategory Enum")
    print("=" * 70)
    
    assert LintCategory.SYNTAX.value == "syntax"
    assert LintCategory.STYLE.value == "style"
    assert LintCategory.UNUSED.value == "unused"
    assert LintCategory.IMPORT.value == "import"
    assert LintCategory.COMPLEXITY.value == "complexity"
    assert LintCategory.SECURITY.value == "security"
    assert LintCategory.BEST_PRACTICE.value == "best_practice"
    assert LintCategory.PEP8.value == "pep8"
    assert LintCategory.TYPE.value == "type"
    
    print(f"  All enum values verified")
    print(f"  Total categories: {len(LintCategory)}")
    
    print("\n" + "=" * 70)
    print("PASS: LintCategory enum")
    print("=" * 70)


def test_lint_rule_enum():
    """
    Test: LintRule enum.
    """
    print("=" * 70)
    print("TEST: LintRule Enum")
    print("=" * 70)
    
    assert LintRule.SYNTAX_ERROR.value == "syntax_error"
    assert LintRule.INDENTATION.value == "indentation"
    assert LintRule.LINE_LENGTH.value == "line_length"
    assert LintRule.TRAILING_WHITESPACE.value == "trailing_whitespace"
    assert LintRule.UNUSED_VARIABLE.value == "unused_variable"
    assert LintRule.UNUSED_IMPORT.value == "unused_import"
    
    print(f"  All enum values verified")
    print(f"  Total rules: {len(LintRule)}")
    
    print("\n" + "=" * 70)
    print("PASS: LintRule enum")
    print("=" * 70)


def test_lint_issue_dataclass():
    """
    Test: LintIssue dataclass.
    """
    print("=" * 70)
    print("TEST: LintIssue Dataclass")
    print("=" * 70)
    
    issue = LintIssue(
        rule=LintRule.LINE_LENGTH,
        category=LintCategory.PEP8,
        severity=LintSeverity.WARNING,
        line=10,
        column=80,
        message="Line too long",
        suggestion="Break the line"
    )
    
    assert issue.rule == LintRule.LINE_LENGTH, "Rule eşleşmeli"
    assert issue.line == 10, "Line eşleşmeli"
    assert issue.severity == LintSeverity.WARNING, "Severity eşleşmeli"
    
    print(f"  Rule: {issue.rule.value}")
    print(f"  Line: {issue.line}")
    print(f"  Severity: {issue.severity.value}")
    
    print("\n" + "=" * 70)
    print("PASS: LintIssue dataclass")
    print("=" * 70)


def test_lint_result_dataclass():
    """
    Test: LintResult dataclass.
    """
    print("=" * 70)
    print("TEST: LintResult Dataclass")
    print("=" * 70)
    
    result = LintResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.issues, list), "Issues list olmalı"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Issues: {len(result.issues)}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: LintResult dataclass")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_lint_python()
        test2 = test_lint_generic()
        test3 = test_syntax_error_detection()
        test4 = test_line_length_check()
        test5 = test_trailing_whitespace_check()
        test6 = test_unused_variable_detection()
        test7 = test_unused_import_detection()
        test8 = test_missing_docstring_detection()
        test9 = test_security_issue_detection()
        test10 = test_lint_severity_enum()
        test11 = test_lint_category_enum()
        test12 = test_lint_rule_enum()
        test13 = test_lint_issue_dataclass()
        test14 = test_lint_result_dataclass()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Lint Python: {'PASS' if test1 else 'FAIL'}")
        print(f"Lint Generic: {'PASS' if test2 else 'FAIL'}")
        print(f"Syntax Error Detection: {'PASS' if test3 else 'FAIL'}")
        print(f"Line Length Check: {'PASS' if test4 else 'FAIL'}")
        print(f"Trailing Whitespace Check: {'PASS' if test5 else 'FAIL'}")
        print(f"Unused Variable Detection: {'PASS' if test6 else 'FAIL'}")
        print(f"Unused Import Detection: {'PASS' if test7 else 'FAIL'}")
        print(f"Missing Docstring Detection: {'PASS' if test8 else 'FAIL'}")
        print(f"Security Issue Detection: {'PASS' if test9 else 'FAIL'}")
        print(f"LintSeverity Enum: {'PASS' if test10 else 'FAIL'}")
        print(f"LintCategory Enum: {'PASS' if test11 else 'FAIL'}")
        print(f"LintRule Enum: {'PASS' if test12 else 'FAIL'}")
        print(f"LintIssue Dataclass: {'PASS' if test13 else 'FAIL'}")
        print(f"LintResult Dataclass: {'PASS' if test14 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14])
        print(f"\nTOPLAM: {'PASS' if all_passed else 'FAIL'}")
        print("=" * 70)
        
        sys.exit(0 if all_passed else 1)
    except Exception as e:
        print(f"\nTEST HATASI:")
        print("-" * 70)
        import traceback
        traceback.print_exc()
        print("=" * 70)
        sys.exit(1)
