"""
Quality Test: Error Highlighting
Error highlighting system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.error_highlighting import (
    ErrorHighlightingEngine,
    ErrorSeverity,
    ErrorCategory,
    ErrorMarker,
    ErrorHighlightingResult
)


def test_highlight_errors():
    """
    Test: Highlight errors.
    """
    print("=" * 70)
    print("TEST: Highlight Errors")
    print("=" * 70)
    
    code = """
def my_function():
    print("Hello")
"""
    
    engine = ErrorHighlightingEngine()
    result = engine.highlight_errors(code, "python")
    
    assert result.success, "Highlighting başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Total errors: {result.total_errors}")
    print(f"  Total warnings: {result.total_warnings}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Highlight errors")
    print("=" * 70)


def test_syntax_error_detection():
    """
    Test: Syntax error detection.
    """
    print("=" * 70)
    print("TEST: Syntax Error Detection")
    print("=" * 70)
    
    code = """
def my_function(
    print("Hello")
"""
    
    engine = ErrorHighlightingEngine()
    result = engine.highlight_errors(code, "python")
    
    assert result.success, "Highlighting başarılı olmalı"
    
    syntax_errors = [m for m in result.markers if m.category == ErrorCategory.SYNTAX]
    
    print(f"  Success: {result.success}")
    print(f"  Syntax errors: {len(syntax_errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: Syntax error detection")
    print("=" * 70)


def test_filter_by_severity():
    """
    Test: Filter by severity.
    """
    print("=" * 70)
    print("TEST: Filter by Severity")
    print("=" * 70)
    
    code = """
def my_function():
    print("Hello")
"""
    
    engine = ErrorHighlightingEngine()
    engine.highlight_errors(code, "python")
    
    errors = engine.filter_by_severity(ErrorSeverity.ERROR)
    
    print(f"  Errors: {len(errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: Filter by severity")
    print("=" * 70)


def test_filter_by_category():
    """
    Test: Filter by category.
    """
    print("=" * 70)
    print("TEST: Filter by Category")
    print("=" * 70)
    
    code = """
def my_function():
    print("Hello")
"""
    
    engine = ErrorHighlightingEngine()
    engine.highlight_errors(code, "python")
    
    syntax_errors = engine.filter_by_category(ErrorCategory.SYNTAX)
    
    print(f"  Syntax errors: {len(syntax_errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: Filter by category")
    print("=" * 70)


def test_get_errors_at_line():
    """
    Test: Get errors at line.
    """
    print("=" * 70)
    print("TEST: Get Errors at Line")
    print("=" * 70)
    
    code = """
def my_function():
    print("Hello")
"""
    
    engine = ErrorHighlightingEngine()
    engine.highlight_errors(code, "python")
    
    errors_at_line = engine.get_errors_at_line(1)
    
    print(f"  Errors at line 1: {len(errors_at_line)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get errors at line")
    print("=" * 70)


def test_get_next_error():
    """
    Test: Get next error.
    """
    print("=" * 70)
    print("TEST: Get Next Error")
    print("=" * 70)
    
    code = """
def my_function():
    print("Hello")
"""
    
    engine = ErrorHighlightingEngine()
    engine.highlight_errors(code, "python")
    
    next_error = engine.get_next_error(0)
    
    print(f"  Next error found: {next_error is not None}")
    
    print("\n" + "=" * 70)
    print("PASS: Get next error")
    print("=" * 70)


def test_get_previous_error():
    """
    Test: Get previous error.
    """
    print("=" * 70)
    print("TEST: Get Previous Error")
    print("=" * 70)
    
    code = """
def my_function():
    print("Hello")
"""
    
    engine = ErrorHighlightingEngine()
    engine.highlight_errors(code, "python")
    
    previous_error = engine.get_previous_error(100)
    
    print(f"  Previous error found: {previous_error is not None}")
    
    print("\n" + "=" * 70)
    print("PASS: Get previous error")
    print("=" * 70)


def test_add_custom_marker():
    """
    Test: Add custom marker.
    """
    print("=" * 70)
    print("TEST: Add Custom Marker")
    print("=" * 70)
    
    engine = ErrorHighlightingEngine()
    
    marker = engine.add_custom_marker(
        line=1,
        column=0,
        end_line=1,
        end_column=5,
        severity=ErrorSeverity.ERROR,
        category=ErrorCategory.SYNTAX,
        message="Custom error",
        suggestion="Fix it"
    )
    
    assert marker is not None, "Marker oluşturulmalı"
    assert len(engine.current_markers) > 0, "Marker listeye eklenmeli"
    
    print(f"  Marker created: {marker is not None}")
    print(f"  Total markers: {len(engine.current_markers)}")
    
    print("\n" + "=" * 70)
    print("PASS: Add custom marker")
    print("=" * 70)


def test_clear_markers():
    """
    Test: Clear markers.
    """
    print("=" * 70)
    print("TEST: Clear Markers")
    print("=" * 70)
    
    engine = ErrorHighlightingEngine()
    
    # Marker ekle
    engine.add_custom_marker(
        line=1,
        column=0,
        end_line=1,
        end_column=5,
        severity=ErrorSeverity.ERROR,
        category=ErrorCategory.SYNTAX,
        message="Custom error"
    )
    
    # Temizle
    engine.clear_markers()
    
    assert len(engine.current_markers) == 0, "Marker'lar temizlenmeli"
    
    print(f"  Markers cleared: {len(engine.current_markers) == 0}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear markers")
    print("=" * 70)


def test_error_severity_enum():
    """
    Test: ErrorSeverity enum.
    """
    print("=" * 70)
    print("TEST: ErrorSeverity Enum")
    print("=" * 70)
    
    assert ErrorSeverity.ERROR.value == "error"
    assert ErrorSeverity.WARNING.value == "warning"
    assert ErrorSeverity.INFO.value == "info"
    assert ErrorSeverity.HINT.value == "hint"
    
    print(f"  All enum values verified")
    print(f"  Total severities: {len(ErrorSeverity)}")
    
    print("\n" + "=" * 70)
    print("PASS: ErrorSeverity enum")
    print("=" * 70)


def test_error_category_enum():
    """
    Test: ErrorCategory enum.
    """
    print("=" * 70)
    print("TEST: ErrorCategory Enum")
    print("=" * 70)
    
    assert ErrorCategory.SYNTAX.value == "syntax"
    assert ErrorCategory.RUNTIME.value == "runtime"
    assert ErrorCategory.LINTING.value == "linting"
    assert ErrorCategory.TYPE.value == "type"
    assert ErrorCategory.IMPORT.value == "import"
    assert ErrorCategory.STYLE.value == "style"
    assert ErrorCategory.SECURITY.value == "security"
    assert ErrorCategory.PERFORMANCE.value == "performance"
    
    print(f"  All enum values verified")
    print(f"  Total categories: {len(ErrorCategory)}")
    
    print("\n" + "=" * 70)
    print("PASS: ErrorCategory enum")
    print("=" * 70)


def test_error_marker_dataclass():
    """
    Test: ErrorMarker dataclass.
    """
    print("=" * 70)
    print("TEST: ErrorMarker Dataclass")
    print("=" * 70)
    
    marker = ErrorMarker(
        line=1,
        column=0,
        end_line=1,
        end_column=5,
        severity=ErrorSeverity.ERROR,
        category=ErrorCategory.SYNTAX,
        message="Test error"
    )
    
    assert marker.line == 1, "Line eşleşmeli"
    assert marker.message == "Test error", "Message eşleşmeli"
    
    print(f"  Line: {marker.line}")
    print(f"  Message: {marker.message}")
    print(f"  Severity: {marker.severity.value}")
    
    print("\n" + "=" * 70)
    print("PASS: ErrorMarker dataclass")
    print("=" * 70)


def test_error_highlighting_result_dataclass():
    """
    Test: ErrorHighlightingResult dataclass.
    """
    print("=" * 70)
    print("TEST: ErrorHighlightingResult Dataclass")
    print("=" * 70)
    
    result = ErrorHighlightingResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.markers, list), "Markers list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Markers: {len(result.markers)}")
    
    print("\n" + "=" * 70)
    print("PASS: ErrorHighlightingResult dataclass")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_highlight_errors()
        test2 = test_syntax_error_detection()
        test3 = test_filter_by_severity()
        test4 = test_filter_by_category()
        test5 = test_get_errors_at_line()
        test6 = test_get_next_error()
        test7 = test_get_previous_error()
        test8 = test_add_custom_marker()
        test9 = test_clear_markers()
        test10 = test_error_severity_enum()
        test11 = test_error_category_enum()
        test12 = test_error_marker_dataclass()
        test13 = test_error_highlighting_result_dataclass()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Highlight Errors: {'PASS' if test1 else 'FAIL'}")
        print(f"Syntax Error Detection: {'PASS' if test2 else 'FAIL'}")
        print(f"Filter by Severity: {'PASS' if test3 else 'FAIL'}")
        print(f"Filter by Category: {'PASS' if test4 else 'FAIL'}")
        print(f"Get Errors at Line: {'PASS' if test5 else 'FAIL'}")
        print(f"Get Next Error: {'PASS' if test6 else 'FAIL'}")
        print(f"Get Previous Error: {'PASS' if test7 else 'FAIL'}")
        print(f"Add Custom Marker: {'PASS' if test8 else 'FAIL'}")
        print(f"Clear Markers: {'PASS' if test9 else 'FAIL'}")
        print(f"ErrorSeverity Enum: {'PASS' if test10 else 'FAIL'}")
        print(f"ErrorCategory Enum: {'PASS' if test11 else 'FAIL'}")
        print(f"ErrorMarker Dataclass: {'PASS' if test12 else 'FAIL'}")
        print(f"ErrorHighlightingResult Dataclass: {'PASS' if test13 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13])
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
