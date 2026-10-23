"""
Quality Test: Code Formatting
Code formatting system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.code_formatting import (
    CodeFormatter,
    FormatStyle,
    FormatRule,
    FormatRuleViolation,
    FormattingResult
)


def test_format_python():
    """
    Test: Format Python code.
    """
    print("=" * 70)
    print("TEST: Format Python Code")
    print("=" * 70)
    
    code = """
def my_function( x,y ):
    result=x+y
    return result
"""
    
    formatter = CodeFormatter()
    result = formatter.format_code(code, language="python")
    
    assert result.success, "Formatting başarılı olmalı"
    assert result.formatted_code is not None, "Formatted code olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Original lines: {len(result.original_code.splitlines())}")
    print(f"  Formatted lines: {len(result.formatted_code.splitlines())}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Format Python code")
    print("=" * 70)


def test_format_generic():
    """
    Test: Format generic code.
    """
    print("=" * 70)
    print("TEST: Format Generic Code")
    print("=" * 70)
    
    code = """
function test() {
    var x = 10;
    return x;
}
"""
    
    formatter = CodeFormatter()
    result = formatter.format_code(code, language="javascript")
    
    assert result.success, "Formatting başarılı olmalı"
    assert result.formatted_code is not None, "Formatted code olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Format generic code")
    print("=" * 70)


def test_organize_imports():
    """
    Test: Organize imports.
    """
    print("=" * 70)
    print("TEST: Organize Imports")
    print("=" * 70)
    
    code = """
import sys
import os
from collections import defaultdict

def main():
    pass
"""
    
    formatter = CodeFormatter()
    result = formatter.organize_imports(code)
    
    assert result.success, "Organizing başarılı olmalı"
    assert result.formatted_code is not None, "Formatted code olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Organize imports")
    print("=" * 70)


def test_format_style_enum():
    """
    Test: FormatStyle enum.
    """
    print("=" * 70)
    print("TEST: FormatStyle Enum")
    print("=" * 70)
    
    assert FormatStyle.PEP8.value == "pep8"
    assert FormatStyle.GOOGLE.value == "google"
    assert FormatStyle.BLACK.value == "black"
    assert FormatStyle.YAPF.value == "yapf"
    assert FormatStyle.AUTOPEP8.value == "autopep8"
    
    print(f"  All enum values verified")
    print(f"  Total styles: {len(FormatStyle)}")
    
    print("\n" + "=" * 70)
    print("PASS: FormatStyle enum")
    print("=" * 70)


def test_format_rule_enum():
    """
    Test: FormatRule enum.
    """
    print("=" * 70)
    print("TEST: FormatRule Enum")
    print("=" * 70)
    
    assert FormatRule.INDENTATION.value == "indentation"
    assert FormatRule.LINE_LENGTH.value == "line_length"
    assert FormatRule.WHITESPACE.value == "whitespace"
    assert FormatRule.IMPORTS.value == "imports"
    assert FormatRule.BLANK_LINES.value == "blank_lines"
    assert FormatRule.QUOTES.value == "quotes"
    
    print(f"  All enum values verified")
    print(f"  Total rules: {len(FormatRule)}")
    
    print("\n" + "=" * 70)
    print("PASS: FormatRule enum")
    print("=" * 70)


def test_format_rule_violation_dataclass():
    """
    Test: FormatRuleViolation dataclass.
    """
    print("=" * 70)
    print("TEST: FormatRuleViolation Dataclass")
    print("=" * 70)
    
    violation = FormatRuleViolation(
        rule=FormatRule.LINE_LENGTH,
        line=10,
        column=80,
        message="Line too long",
        severity="warning"
    )
    
    assert violation.rule == FormatRule.LINE_LENGTH, "Rule eşleşmeli"
    assert violation.line == 10, "Line eşleşmeli"
    assert violation.severity == "warning", "Severity eşleşmeli"
    
    print(f"  Rule: {violation.rule.value}")
    print(f"  Line: {violation.line}")
    print(f"  Severity: {violation.severity}")
    
    print("\n" + "=" * 70)
    print("PASS: FormatRuleViolation dataclass")
    print("=" * 70)


def test_formatting_result_dataclass():
    """
    Test: FormattingResult dataclass.
    """
    print("=" * 70)
    print("TEST: FormattingResult Dataclass")
    print("=" * 70)
    
    result = FormattingResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.violations, list), "Violations list olmalı"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Violations: {len(result.violations)}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: FormattingResult dataclass")
    print("=" * 70)


def test_indentation_fixing():
    """
    Test: Indentation fixing.
    """
    print("=" * 70)
    print("TEST: Indentation Fixing")
    print("=" * 70)
    
    code = """
def my_function():
x=10
return x
"""
    
    formatter = CodeFormatter()
    result = formatter.format_code(code, language="python")
    
    assert result.success, "Formatting başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Formatted code:\n{result.formatted_code}")
    
    print("\n" + "=" * 70)
    print("PASS: Indentation fixing")
    print("=" * 70)


def test_whitespace_normalization():
    """
    Test: Whitespace normalization.
    """
    print("=" * 70)
    print("TEST: Whitespace Normalization")
    print("=" * 70)
    
    code = "x  =  10"
    
    formatter = CodeFormatter()
    result = formatter.format_code(code, language="python")
    
    assert result.success, "Formatting başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Original: '{code}'")
    print(f"  Formatted: '{result.formatted_code.strip()}'")
    
    print("\n" + "=" * 70)
    print("PASS: Whitespace normalization")
    print("=" * 70)


def test_operator_spacing():
    """
    Test: Operator spacing.
    """
    print("=" * 70)
    print("TEST: Operator Spacing")
    print("=" * 70)
    
    code = "x=10+5"
    
    formatter = CodeFormatter()
    result = formatter.format_code(code, language="python")
    
    assert result.success, "Formatting başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Original: '{code}'")
    print(f"  Formatted: '{result.formatted_code.strip()}'")
    
    print("\n" + "=" * 70)
    print("PASS: Operator spacing")
    print("=" * 70)


def test_violation_checking():
    """
    Test: Violation checking.
    """
    print("=" * 70)
    print("TEST: Violation Checking")
    print("=" * 70)
    
    code = "x" * 100  # Çok uzun satır
    
    formatter = CodeFormatter()
    result = formatter.format_code(code, language="python")
    
    assert result.success, "Formatting başarılı olmalı"
    assert len(result.violations) > 0, "Violations olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Violations: {len(result.violations)}")
    
    for violation in result.violations:
        print(f"  - {violation.rule.value}: {violation.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Violation checking")
    print("=" * 70)


def test_format_selection():
    """
    Test: Format selection.
    """
    print("=" * 70)
    print("TEST: Format Selection")
    print("=" * 70)
    
    code = """
def my_function():
    x=10
    y=20
    return x+y
"""
    
    formatter = CodeFormatter()
    result = formatter.format_selection(code, 2, 3, language="python")
    
    assert result.success, "Selection formatting başarılı olmalı"
    assert result.lines_changed > 0, "Lines changed olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Lines changed: {result.lines_changed}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Format selection")
    print("=" * 70)


def test_format_on_save():
    """
    Test: Format on save.
    """
    print("=" * 70)
    print("TEST: Format On Save")
    print("=" * 70)
    
    code = """
def my_function():
    x=10
    return x
"""
    
    formatter = CodeFormatter()
    result = formatter.format_on_save(code, language="python")
    
    assert result.success, "Format on save başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Format on save")
    print("=" * 70)


def test_format_on_paste():
    """
    Test: Format on paste.
    """
    print("=" * 70)
    print("TEST: Format On Paste")
    print("=" * 70)
    
    code = "x=10+5"
    
    formatter = CodeFormatter()
    result = formatter.format_on_paste(code, language="python")
    
    assert result.success, "Format on paste başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Original: '{code}'")
    print(f"  Formatted: '{result.formatted_code.strip()}'")
    
    print("\n" + "=" * 70)
    print("PASS: Format on paste")
    print("=" * 70)


def test_preview_format():
    """
    Test: Preview format.
    """
    print("=" * 70)
    print("TEST: Preview Format")
    print("=" * 70)
    
    code = """
def my_function():
    x=10
    return x
"""
    
    formatter = CodeFormatter()
    result = formatter.preview_format(code, language="python")
    
    assert result.success, "Preview başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Formatted code length: {len(result.formatted_code)}")
    
    print("\n" + "=" * 70)
    print("PASS: Preview format")
    print("=" * 70)


def test_configure_rules():
    """
    Test: Configure rules.
    """
    print("=" * 70)
    print("TEST: Configure Rules")
    print("=" * 70)
    
    formatter = CodeFormatter()
    rules = {
        FormatRule.INDENTATION: True,
        FormatRule.LINE_LENGTH: True,
        FormatRule.WHITESPACE: True
    }
    
    formatter.configure_rules(rules)
    
    assert hasattr(formatter, 'enabled_rules'), "Rules configured olmalı"
    
    print(f"  Rules configured: {len(formatter.enabled_rules)}")
    
    print("\n" + "=" * 70)
    print("PASS: Configure rules")
    print("=" * 70)


def test_get_style_config():
    """
    Test: Get style config.
    """
    print("=" * 70)
    print("TEST: Get Style Config")
    print("=" * 70)
    
    formatter = CodeFormatter()
    config = formatter.get_style_config()
    
    assert "style" in config, "Style olmalı"
    assert "max_line_length" in config, "Max line length olmalı"
    
    print(f"  Style: {config['style']}")
    print(f"  Max line length: {config['max_line_length']}")
    print(f"  Indent size: {config['indent_size']}")
    
    print("\n" + "=" * 70)
    print("PASS: Get style config")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_format_python()
        test2 = test_format_generic()
        test3 = test_organize_imports()
        test4 = test_format_style_enum()
        test5 = test_format_rule_enum()
        test6 = test_format_rule_violation_dataclass()
        test7 = test_formatting_result_dataclass()
        test8 = test_indentation_fixing()
        test9 = test_whitespace_normalization()
        test10 = test_operator_spacing()
        test11 = test_violation_checking()
        test12 = test_format_selection()
        test13 = test_format_on_save()
        test14 = test_format_on_paste()
        test15 = test_preview_format()
        test16 = test_configure_rules()
        test17 = test_get_style_config()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Format Python: {'PASS' if test1 else 'FAIL'}")
        print(f"Format Generic: {'PASS' if test2 else 'FAIL'}")
        print(f"Organize Imports: {'PASS' if test3 else 'FAIL'}")
        print(f"FormatStyle Enum: {'PASS' if test4 else 'FAIL'}")
        print(f"FormatRule Enum: {'PASS' if test5 else 'FAIL'}")
        print(f"FormatRuleViolation Dataclass: {'PASS' if test6 else 'FAIL'}")
        print(f"FormattingResult Dataclass: {'PASS' if test7 else 'FAIL'}")
        print(f"Indentation Fixing: {'PASS' if test8 else 'FAIL'}")
        print(f"Whitespace Normalization: {'PASS' if test9 else 'FAIL'}")
        print(f"Operator Spacing: {'PASS' if test10 else 'FAIL'}")
        print(f"Violation Checking: {'PASS' if test11 else 'FAIL'}")
        print(f"Format Selection: {'PASS' if test12 else 'FAIL'}")
        print(f"Format On Save: {'PASS' if test13 else 'FAIL'}")
        print(f"Format On Paste: {'PASS' if test14 else 'FAIL'}")
        print(f"Preview Format: {'PASS' if test15 else 'FAIL'}")
        print(f"Configure Rules: {'PASS' if test16 else 'FAIL'}")
        print(f"Get Style Config: {'PASS' if test17 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14, test15, test16, test17])
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
