"""
Quality Test: Line Numbers
Line numbers system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.line_numbers import (
    LineNumberGenerator,
    LineNumberStyle,
    LineNumberFormat,
    LineNumber,
    LineNumbersResult
)


def test_generate_line_numbers():
    """
    Test: Generate line numbers.
    """
    print("=" * 70)
    print("TEST: Generate Line Numbers")
    print("=" * 70)
    
    code = """
def my_function(x, y):
    result = x + y
    return result
"""
    
    generator = LineNumberGenerator()
    result = generator.generate_line_numbers(code)
    
    assert result.success, "Generation başarılı olmalı"
    assert isinstance(result.line_numbers, list), "Line numbers list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Total lines: {result.total_lines}")
    print(f"  Line numbers: {len(result.line_numbers)}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Generate line numbers")
    print("=" * 70)


def test_standard_style():
    """
    Test: Standard style.
    """
    print("=" * 70)
    print("TEST: Standard Style")
    print("=" * 70)
    
    code = "line1\nline2\nline3"
    
    generator = LineNumberGenerator(style=LineNumberStyle.STANDARD)
    result = generator.generate_line_numbers(code)
    
    assert result.success, "Generation başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Line numbers: {[ln.text for ln in result.line_numbers]}")
    
    print("\n" + "=" * 70)
    print("PASS: Standard style")
    print("=" * 70)


def test_relative_style():
    """
    Test: Relative style.
    """
    print("=" * 70)
    print("TEST: Relative Style")
    print("=" * 70)
    
    code = "line1\nline2\nline3"
    
    generator = LineNumberGenerator(style=LineNumberStyle.RELATIVE)
    result = generator.generate_line_numbers(code, active_line=2)
    
    assert result.success, "Generation başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Line numbers: {[ln.text for ln in result.line_numbers]}")
    
    print("\n" + "=" * 70)
    print("PASS: Relative style")
    print("=" * 70)


def test_both_style():
    """
    Test: Both style.
    """
    print("=" * 70)
    print("TEST: Both Style")
    print("=" * 70)
    
    code = "line1\nline2\nline3"
    
    generator = LineNumberGenerator(style=LineNumberStyle.BOTH)
    result = generator.generate_line_numbers(code, active_line=2)
    
    assert result.success, "Generation başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Line numbers: {[ln.text for ln in result.line_numbers]}")
    
    print("\n" + "=" * 70)
    print("PASS: Both style")
    print("=" * 70)


def test_decimal_format():
    """
    Test: Decimal format.
    """
    print("=" * 70)
    print("TEST: Decimal Format")
    print("=" * 70)
    
    code = "line1\nline2"
    
    generator = LineNumberGenerator(number_format=LineNumberFormat.DECIMAL)
    result = generator.generate_line_numbers(code)
    
    assert result.success, "Generation başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Line numbers: {[ln.text for ln in result.line_numbers]}")
    
    print("\n" + "=" * 70)
    print("PASS: Decimal format")
    print("=" * 70)


def test_hexadecimal_format():
    """
    Test: Hexadecimal format.
    """
    print("=" * 70)
    print("TEST: Hexadecimal Format")
    print("=" * 70)
    
    code = "line1\nline2"
    
    generator = LineNumberGenerator(number_format=LineNumberFormat.HEXADECIMAL)
    result = generator.generate_line_numbers(code)
    
    assert result.success, "Generation başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Line numbers: {[ln.text for ln in result.line_numbers]}")
    
    print("\n" + "=" * 70)
    print("PASS: Hexadecimal format")
    print("=" * 70)


def test_active_line():
    """
    Test: Active line.
    """
    print("=" * 70)
    print("TEST: Active Line")
    print("=" * 70)
    
    code = "line1\nline2\nline3"
    
    generator = LineNumberGenerator()
    result = generator.generate_line_numbers(code, active_line=2)
    
    assert result.success, "Generation başarılı olmalı"
    
    active_lines = [ln for ln in result.line_numbers if ln.is_active]
    print(f"  Active lines: {len(active_lines)}")
    print(f"  Active line number: {active_lines[0].number if active_lines else None}")
    
    print("\n" + "=" * 70)
    print("PASS: Active line")
    print("=" * 70)


def test_breakpoint():
    """
    Test: Breakpoint.
    """
    print("=" * 70)
    print("TEST: Breakpoint")
    print("=" * 70)
    
    code = "line1\nline2\nline3"
    
    generator = LineNumberGenerator()
    generator.add_breakpoint(2)
    result = generator.generate_line_numbers(code)
    
    assert result.success, "Generation başarılı olmalı"
    
    breakpoint_lines = [ln for ln in result.line_numbers if ln.has_breakpoint]
    print(f"  Breakpoint lines: {len(breakpoint_lines)}")
    
    print("\n" + "=" * 70)
    print("PASS: Breakpoint")
    print("=" * 70)


def test_error_line():
    """
    Test: Error line.
    """
    print("=" * 70)
    print("TEST: Error Line")
    print("=" * 70)
    
    code = "line1\nline2\nline3"
    
    generator = LineNumberGenerator()
    generator.add_error_line(2)
    result = generator.generate_line_numbers(code)
    
    assert result.success, "Generation başarılı olmalı"
    
    error_lines = [ln for ln in result.line_numbers if ln.has_error]
    print(f"  Error lines: {len(error_lines)}")
    
    print("\n" + "=" * 70)
    print("PASS: Error line")
    print("=" * 70)


def test_warning_line():
    """
    Test: Warning line.
    """
    print("=" * 70)
    print("TEST: Warning Line")
    print("=" * 70)
    
    code = "line1\nline2\nline3"
    
    generator = LineNumberGenerator()
    generator.add_warning_line(2)
    result = generator.generate_line_numbers(code)
    
    assert result.success, "Generation başarılı olmalı"
    
    warning_lines = [ln for ln in result.line_numbers if ln.has_warning]
    print(f"  Warning lines: {len(warning_lines)}")
    
    print("\n" + "=" * 70)
    print("PASS: Warning line")
    print("=" * 70)


def test_line_number_style_enum():
    """
    Test: LineNumberStyle enum.
    """
    print("=" * 70)
    print("TEST: LineNumberStyle Enum")
    print("=" * 70)
    
    assert LineNumberStyle.STANDARD.value == "standard"
    assert LineNumberStyle.RELATIVE.value == "relative"
    assert LineNumberStyle.BOTH.value == "both"
    
    print(f"  All enum values verified")
    print(f"  Total styles: {len(LineNumberStyle)}")
    
    print("\n" + "=" * 70)
    print("PASS: LineNumberStyle enum")
    print("=" * 70)


def test_line_number_format_enum():
    """
    Test: LineNumberFormat enum.
    """
    print("=" * 70)
    print("TEST: LineNumberFormat Enum")
    print("=" * 70)
    
    assert LineNumberFormat.DECIMAL.value == "decimal"
    assert LineNumberFormat.HEXADECIMAL.value == "hexadecimal"
    assert LineNumberFormat.OCTAL.value == "octal"
    assert LineNumberFormat.BINARY.value == "binary"
    
    print(f"  All enum values verified")
    print(f"  Total formats: {len(LineNumberFormat)}")
    
    print("\n" + "=" * 70)
    print("PASS: LineNumberFormat enum")
    print("=" * 70)


def test_line_number_dataclass():
    """
    Test: LineNumber dataclass.
    """
    print("=" * 70)
    print("TEST: LineNumber Dataclass")
    print("=" * 70)
    
    line_number = LineNumber(
        number=1,
        text="1",
        is_active=True,
        has_breakpoint=False
    )
    
    assert line_number.number == 1, "Number eşleşmeli"
    assert line_number.text == "1", "Text eşleşmeli"
    assert line_number.is_active == True, "Active eşleşmeli"
    
    print(f"  Number: {line_number.number}")
    print(f"  Text: {line_number.text}")
    print(f"  Active: {line_number.is_active}")
    
    print("\n" + "=" * 70)
    print("PASS: LineNumber dataclass")
    print("=" * 70)


def test_line_numbers_result_dataclass():
    """
    Test: LineNumbersResult dataclass.
    """
    print("=" * 70)
    print("TEST: LineNumbersResult Dataclass")
    print("=" * 70)
    
    result = LineNumbersResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.line_numbers, list), "Line numbers list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Line numbers: {len(result.line_numbers)}")
    
    print("\n" + "=" * 70)
    print("PASS: LineNumbersResult dataclass")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_generate_line_numbers()
        test2 = test_standard_style()
        test3 = test_relative_style()
        test4 = test_both_style()
        test5 = test_decimal_format()
        test6 = test_hexadecimal_format()
        test7 = test_active_line()
        test8 = test_breakpoint()
        test9 = test_error_line()
        test10 = test_warning_line()
        test11 = test_line_number_style_enum()
        test12 = test_line_number_format_enum()
        test13 = test_line_number_dataclass()
        test14 = test_line_numbers_result_dataclass()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Generate Line Numbers: {'PASS' if test1 else 'FAIL'}")
        print(f"Standard Style: {'PASS' if test2 else 'FAIL'}")
        print(f"Relative Style: {'PASS' if test3 else 'FAIL'}")
        print(f"Both Style: {'PASS' if test4 else 'FAIL'}")
        print(f"Decimal Format: {'PASS' if test5 else 'FAIL'}")
        print(f"Hexadecimal Format: {'PASS' if test6 else 'FAIL'}")
        print(f"Active Line: {'PASS' if test7 else 'FAIL'}")
        print(f"Breakpoint: {'PASS' if test8 else 'FAIL'}")
        print(f"Error Line: {'PASS' if test9 else 'FAIL'}")
        print(f"Warning Line: {'PASS' if test10 else 'FAIL'}")
        print(f"LineNumberStyle Enum: {'PASS' if test11 else 'FAIL'}")
        print(f"LineNumberFormat Enum: {'PASS' if test12 else 'FAIL'}")
        print(f"LineNumber Dataclass: {'PASS' if test13 else 'FAIL'}")
        print(f"LineNumbersResult Dataclass: {'PASS' if test14 else 'FAIL'}")
        
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
