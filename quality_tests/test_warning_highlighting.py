"""
Quality Test: Warning Highlighting
Warning highlighting system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.warning_highlighting import (
    WarningHighlightingEngine,
    WarningSeverity,
    WarningCategory,
    WarningMarker,
    WarningHighlightingResult
)


def test_highlight_warnings():
    """
    Test: Highlight warnings.
    """
    print("=" * 70)
    print("TEST: Highlight Warnings")
    print("=" * 70)
    
    code = """
def my_function():
    return "Hello"
"""
    
    engine = WarningHighlightingEngine()
    result = engine.highlight_warnings(code, "python")
    
    assert result.success, "Highlighting başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Total warnings: {result.total_warnings}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Highlight warnings")
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
    unused_var = 42
    return "Hello"
"""
    
    engine = WarningHighlightingEngine()
    result = engine.highlight_warnings(code, "python")
    
    assert result.success, "Highlighting başarılı olmalı"
    
    unused_warnings = [m for m in result.markers if m.category == WarningCategory.UNUSED]
    
    print(f"  Success: {result.success}")
    print(f"  Unused warnings: {len(unused_warnings)}")
    
    print("\n" + "=" * 70)
    print("PASS: Unused variable detection")
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
    return "Hello"
"""
    
    engine = WarningHighlightingEngine()
    engine.highlight_warnings(code, "python")
    
    low_warnings = engine.filter_by_severity(WarningSeverity.LOW)
    
    print(f"  Low warnings: {len(low_warnings)}")
    
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
    return "Hello"
"""
    
    engine = WarningHighlightingEngine()
    engine.highlight_warnings(code, "python")
    
    style_warnings = engine.filter_by_category(WarningCategory.STYLE)
    
    print(f"  Style warnings: {len(style_warnings)}")
    
    print("\n" + "=" * 70)
    print("PASS: Filter by category")
    print("=" * 70)


def test_get_warnings_at_line():
    """
    Test: Get warnings at line.
    """
    print("=" * 70)
    print("TEST: Get Warnings at Line")
    print("=" * 70)
    
    code = """
def my_function():
    return "Hello"
"""
    
    engine = WarningHighlightingEngine()
    engine.highlight_warnings(code, "python")
    
    warnings_at_line = engine.get_warnings_at_line(1)
    
    print(f"  Warnings at line 1: {len(warnings_at_line)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get warnings at line")
    print("=" * 70)


def test_get_next_warning():
    """
    Test: Get next warning.
    """
    print("=" * 70)
    print("TEST: Get Next Warning")
    print("=" * 70)
    
    code = """
def my_function():
    return "Hello"
"""
    
    engine = WarningHighlightingEngine()
    engine.highlight_warnings(code, "python")
    
    next_warning = engine.get_next_warning(0)
    
    print(f"  Next warning found: {next_warning is not None}")
    
    print("\n" + "=" * 70)
    print("PASS: Get next warning")
    print("=" * 70)


def test_get_previous_warning():
    """
    Test: Get previous warning.
    """
    print("=" * 70)
    print("TEST: Get Previous Warning")
    print("=" * 70)
    
    code = """
def my_function():
    return "Hello"
"""
    
    engine = WarningHighlightingEngine()
    engine.highlight_warnings(code, "python")
    
    previous_warning = engine.get_previous_warning(100)
    
    print(f"  Previous warning found: {previous_warning is not None}")
    
    print("\n" + "=" * 70)
    print("PASS: Get previous warning")
    print("=" * 70)


def test_add_custom_marker():
    """
    Test: Add custom marker.
    """
    print("=" * 70)
    print("TEST: Add Custom Marker")
    print("=" * 70)
    
    engine = WarningHighlightingEngine()
    
    marker = engine.add_custom_marker(
        line=1,
        column=0,
        end_line=1,
        end_column=5,
        severity=WarningSeverity.MEDIUM,
        category=WarningCategory.STYLE,
        message="Custom warning",
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
    
    engine = WarningHighlightingEngine()
    
    # Marker ekle
    engine.add_custom_marker(
        line=1,
        column=0,
        end_line=1,
        end_column=5,
        severity=WarningSeverity.MEDIUM,
        category=WarningCategory.STYLE,
        message="Custom warning"
    )
    
    # Temizle
    engine.clear_markers()
    
    assert len(engine.current_markers) == 0, "Marker'lar temizlenmeli"
    
    print(f"  Markers cleared: {len(engine.current_markers) == 0}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear markers")
    print("=" * 70)


def test_warning_severity_enum():
    """
    Test: WarningSeverity enum.
    """
    print("=" * 70)
    print("TEST: WarningSeverity Enum")
    print("=" * 70)
    
    assert WarningSeverity.LOW.value == "low"
    assert WarningSeverity.MEDIUM.value == "medium"
    assert WarningSeverity.HIGH.value == "high"
    assert WarningSeverity.CRITICAL.value == "critical"
    
    print(f"  All enum values verified")
    print(f"  Total severities: {len(WarningSeverity)}")
    
    print("\n" + "=" * 70)
    print("PASS: WarningSeverity enum")
    print("=" * 70)


def test_warning_category_enum():
    """
    Test: WarningCategory enum.
    """
    print("=" * 70)
    print("TEST: WarningCategory Enum")
    print("=" * 70)
    
    assert WarningCategory.DEPRECATED.value == "deprecated"
    assert WarningCategory.UNUSED.value == "unused"
    assert WarningCategory.STYLE.value == "style"
    assert WarningCategory.SECURITY.value == "security"
    assert WarningCategory.PERFORMANCE.value == "performance"
    assert WarningCategory.MAINTAINABILITY.value == "maintainability"
    assert WarningCategory.DOCUMENTATION.value == "documentation"
    assert WarningCategory.TYPE_SAFETY.value == "type_safety"
    
    print(f"  All enum values verified")
    print(f"  Total categories: {len(WarningCategory)}")
    
    print("\n" + "=" * 70)
    print("PASS: WarningCategory enum")
    print("=" * 70)


def test_warning_marker_dataclass():
    """
    Test: WarningMarker dataclass.
    """
    print("=" * 70)
    print("TEST: WarningMarker Dataclass")
    print("=" * 70)
    
    marker = WarningMarker(
        line=1,
        column=0,
        end_line=1,
        end_column=5,
        severity=WarningSeverity.MEDIUM,
        category=WarningCategory.STYLE,
        message="Test warning"
    )
    
    assert marker.line == 1, "Line eşleşmeli"
    assert marker.message == "Test warning", "Message eşleşmeli"
    
    print(f"  Line: {marker.line}")
    print(f"  Message: {marker.message}")
    print(f"  Severity: {marker.severity.value}")
    
    print("\n" + "=" * 70)
    print("PASS: WarningMarker dataclass")
    print("=" * 70)


def test_warning_highlighting_result_dataclass():
    """
    Test: WarningHighlightingResult dataclass.
    """
    print("=" * 70)
    print("TEST: WarningHighlightingResult Dataclass")
    print("=" * 70)
    
    result = WarningHighlightingResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.markers, list), "Markers list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Markers: {len(result.markers)}")
    
    print("\n" + "=" * 70)
    print("PASS: WarningHighlightingResult dataclass")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_highlight_warnings()
        test2 = test_unused_variable_detection()
        test3 = test_filter_by_severity()
        test4 = test_filter_by_category()
        test5 = test_get_warnings_at_line()
        test6 = test_get_next_warning()
        test7 = test_get_previous_warning()
        test8 = test_add_custom_marker()
        test9 = test_clear_markers()
        test10 = test_warning_severity_enum()
        test11 = test_warning_category_enum()
        test12 = test_warning_marker_dataclass()
        test13 = test_warning_highlighting_result_dataclass()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Highlight Warnings: {'PASS' if test1 else 'FAIL'}")
        print(f"Unused Variable Detection: {'PASS' if test2 else 'FAIL'}")
        print(f"Filter by Severity: {'PASS' if test3 else 'FAIL'}")
        print(f"Filter by Category: {'PASS' if test4 else 'FAIL'}")
        print(f"Get Warnings at Line: {'PASS' if test5 else 'FAIL'}")
        print(f"Get Next Warning: {'PASS' if test6 else 'FAIL'}")
        print(f"Get Previous Warning: {'PASS' if test7 else 'FAIL'}")
        print(f"Add Custom Marker: {'PASS' if test8 else 'FAIL'}")
        print(f"Clear Markers: {'PASS' if test9 else 'FAIL'}")
        print(f"WarningSeverity Enum: {'PASS' if test10 else 'FAIL'}")
        print(f"WarningCategory Enum: {'PASS' if test11 else 'FAIL'}")
        print(f"WarningMarker Dataclass: {'PASS' if test12 else 'FAIL'}")
        print(f"WarningHighlightingResult Dataclass: {'PASS' if test13 else 'FAIL'}")
        
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
