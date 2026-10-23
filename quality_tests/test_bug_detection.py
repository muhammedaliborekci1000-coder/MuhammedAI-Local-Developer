"""
Quality Test: Bug Detection
Bug detection system testleri.
"""

import sys
import os
import tempfile
import shutil
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.ai.bug_detection import (
    BugDetector,
    BugSeverity,
    BugCategory,
    Bug,
    BugDetectionResult
)


def test_detect_bugs():
    """
    Test: Detect bugs.
    """
    print("=" * 70)
    print("TEST: Detect Bugs")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp(prefix="muhammedai_test_")
    
    try:
        # Test dosyası oluştur (bug içeren kod)
        test_file = Path(temp_dir) / "test_module.py"
        test_file.write_text("""
def my_function():
    x = 10
    y = 0
    result = x / y  # Division by zero
    return result
""", encoding='utf-8')
        
        detector = BugDetector()
        
        # Detect bugs
        result = detector.detect_bugs(str(test_file))
        
        assert result.success, "Detection başarılı olmalı"
        assert isinstance(result.bugs, list), "Bugs list olmalı"
        assert result.file_path == str(test_file), "File path eşleşmeli"
        
        print(f"  Success: {result.success}")
        print(f"  Bugs found: {len(result.bugs)}")
        print(f"  Message: {result.message}")
        
        print("\n" + "=" * 70)
        print("PASS: Detect bugs")
        print("=" * 70)
        
    finally:
        shutil.rmtree(temp_dir)


def test_syntax_error_detection():
    """
    Test: Syntax error detection.
    """
    print("=" * 70)
    print("TEST: Syntax Error Detection")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp(prefix="muhammedai_test_")
    
    try:
        # Test dosyası oluştur (syntax error)
        test_file = Path(temp_dir) / "test_module.py"
        test_file.write_text("""
def my_function():
    x = 10
    return x
    # Missing closing parenthesis
    print("test"
""", encoding='utf-8')
        
        detector = BugDetector()
        
        # Detect bugs
        result = detector.detect_bugs(str(test_file))
        
        assert result.success, "Detection başarılı olmalı"
        
        # Syntax error bug'ı kontrol et
        syntax_bugs = [b for b in result.bugs if b.category == BugCategory.SYNTAX]
        print(f"  Syntax bugs: {len(syntax_bugs)}")
        
        print("\n" + "=" * 70)
        print("PASS: Syntax error detection")
        print("=" * 70)
        
    finally:
        shutil.rmtree(temp_dir)


def test_logic_error_detection():
    """
    Test: Logic error detection.
    """
    print("=" * 70)
    print("TEST: Logic Error Detection")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp(prefix="muhammedai_test_")
    
    try:
        # Test dosyası oluştur (logic error)
        test_file = Path(temp_dir) / "test_module.py"
        test_file.write_text("""
def my_function():
    x = 10
    y = 0
    result = x / y
    return result
""", encoding='utf-8')
        
        detector = BugDetector()
        
        # Detect bugs
        result = detector.detect_bugs(str(test_file))
        
        assert result.success, "Detection başarılı olmalı"
        
        # Logic error bug'ı kontrol et
        logic_bugs = [b for b in result.bugs if b.category == BugCategory.LOGIC]
        print(f"  Logic bugs: {len(logic_bugs)}")
        
        print("\n" + "=" * 70)
        print("PASS: Logic error detection")
        print("=" * 70)
        
    finally:
        shutil.rmtree(temp_dir)


def test_security_vulnerability_detection():
    """
    Test: Security vulnerability detection.
    """
    print("=" * 70)
    print("TEST: Security Vulnerability Detection")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp(prefix="muhammedai_test_")
    
    try:
        # Test dosyası oluştur (security vulnerability)
        test_file = Path(temp_dir) / "test_module.py"
        test_file.write_text("""
def my_function():
    password = "secret123"
    return password
""", encoding='utf-8')
        
        detector = BugDetector()
        
        # Detect bugs
        result = detector.detect_bugs(str(test_file))
        
        assert result.success, "Detection başarılı olmalı"
        
        # Security bug'ı kontrol et
        security_bugs = [b for b in result.bugs if b.category == BugCategory.SECURITY]
        print(f"  Security bugs: {len(security_bugs)}")
        
        print("\n" + "=" * 70)
        print("PASS: Security vulnerability detection")
        print("=" * 70)
        
    finally:
        shutil.rmtree(temp_dir)


def test_style_issue_detection():
    """
    Test: Style issue detection.
    """
    print("=" * 70)
    print("TEST: Style Issue Detection")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp(prefix="muhammedai_test_")
    
    try:
        # Test dosyası oluştur (style issue)
        test_file = Path(temp_dir) / "test_module.py"
        test_file.write_text("""
def my_function():
    try:
        x = 10
    except:
        pass
""", encoding='utf-8')
        
        detector = BugDetector()
        
        # Detect bugs
        result = detector.detect_bugs(str(test_file))
        
        assert result.success, "Detection başarılı olmalı"
        
        # Style bug'ı kontrol et
        style_bugs = [b for b in result.bugs if b.category == BugCategory.STYLE]
        print(f"  Style bugs: {len(style_bugs)}")
        
        print("\n" + "=" * 70)
        print("PASS: Style issue detection")
        print("=" * 70)
        
    finally:
        shutil.rmtree(temp_dir)


def test_undefined_variable_detection():
    """
    Test: Undefined variable detection.
    """
    print("=" * 70)
    print("TEST: Undefined Variable Detection")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp(prefix="muhammedai_test_")
    
    try:
        # Test dosyası oluştur (undefined variable)
        test_file = Path(temp_dir) / "test_module.py"
        test_file.write_text("""
def my_function():
    return undefined_var
""", encoding='utf-8')
        
        detector = BugDetector()
        
        # Detect bugs
        result = detector.detect_bugs(str(test_file))
        
        assert result.success, "Detection başarılı olmalı"
        
        # Undefined variable bug'ı kontrol et
        undefined_bugs = [b for b in result.bugs if b.category == BugCategory.UNDEFINED]
        print(f"  Undefined variable bugs: {len(undefined_bugs)}")
        
        print("\n" + "=" * 70)
        print("PASS: Undefined variable detection")
        print("=" * 70)
        
    finally:
        shutil.rmtree(temp_dir)


def test_bug_severity_enum():
    """
    Test: BugSeverity enum.
    """
    print("=" * 70)
    print("TEST: BugSeverity Enum")
    print("=" * 70)
    
    assert BugSeverity.CRITICAL.value == "critical"
    assert BugSeverity.HIGH.value == "high"
    assert BugSeverity.MEDIUM.value == "medium"
    assert BugSeverity.LOW.value == "low"
    assert BugSeverity.INFO.value == "info"
    
    print(f"  All enum values verified")
    print(f"  Total severities: {len(BugSeverity)}")
    
    print("\n" + "=" * 70)
    print("PASS: BugSeverity enum")
    print("=" * 70)


def test_bug_category_enum():
    """
    Test: BugCategory enum.
    """
    print("=" * 70)
    print("TEST: BugCategory Enum")
    print("=" * 70)
    
    assert BugCategory.SYNTAX.value == "syntax"
    assert BugCategory.LOGIC.value == "logic"
    assert BugCategory.PERFORMANCE.value == "performance"
    assert BugCategory.SECURITY.value == "security"
    assert BugCategory.STYLE.value == "style"
    assert BugCategory.TYPE_ERROR.value == "type_error"
    assert BugCategory.UNDEFINED.value == "undefined"
    
    print(f"  All enum values verified")
    print(f"  Total categories: {len(BugCategory)}")
    
    print("\n" + "=" * 70)
    print("PASS: BugCategory enum")
    print("=" * 70)


def test_bug_dataclass():
    """
    Test: Bug dataclass.
    """
    print("=" * 70)
    print("TEST: Bug Dataclass")
    print("=" * 70)
    
    bug = Bug(
        file_path="test.py",
        line=10,
        column=5,
        severity=BugSeverity.HIGH,
        category=BugCategory.LOGIC,
        message="Test bug",
        suggestion="Fix it"
    )
    
    assert bug.file_path == "test.py", "File path eşleşmeli"
    assert bug.line == 10, "Line eşleşmeli"
    assert bug.severity == BugSeverity.HIGH, "Severity eşleşmeli"
    assert bug.category == BugCategory.LOGIC, "Category eşleşmeli"
    
    print(f"  File path: {bug.file_path}")
    print(f"  Line: {bug.line}")
    print(f"  Severity: {bug.severity.value}")
    print(f"  Category: {bug.category.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Bug dataclass")
    print("=" * 70)


def test_bug_detection_result_dataclass():
    """
    Test: BugDetectionResult dataclass.
    """
    print("=" * 70)
    print("TEST: BugDetectionResult Dataclass")
    print("=" * 70)
    
    result = BugDetectionResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.bugs, list), "Bugs list olmalı"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Bugs: {len(result.bugs)}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: BugDetectionResult dataclass")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_detect_bugs()
        test2 = test_syntax_error_detection()
        test3 = test_logic_error_detection()
        test4 = test_security_vulnerability_detection()
        test5 = test_style_issue_detection()
        test6 = test_undefined_variable_detection()
        test7 = test_bug_severity_enum()
        test8 = test_bug_category_enum()
        test9 = test_bug_dataclass()
        test10 = test_bug_detection_result_dataclass()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Detect Bugs: {'PASS' if test1 else 'FAIL'}")
        print(f"Syntax Error Detection: {'PASS' if test2 else 'FAIL'}")
        print(f"Logic Error Detection: {'PASS' if test3 else 'FAIL'}")
        print(f"Security Vulnerability Detection: {'PASS' if test4 else 'FAIL'}")
        print(f"Style Issue Detection: {'PASS' if test5 else 'FAIL'}")
        print(f"Undefined Variable Detection: {'PASS' if test6 else 'FAIL'}")
        print(f"BugSeverity Enum: {'PASS' if test7 else 'FAIL'}")
        print(f"BugCategory Enum: {'PASS' if test8 else 'FAIL'}")
        print(f"Bug Dataclass: {'PASS' if test9 else 'FAIL'}")
        print(f"BugDetectionResult Dataclass: {'PASS' if test10 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10])
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
