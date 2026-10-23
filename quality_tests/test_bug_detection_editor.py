"""
Quality Test: Bug Detection (Editor)
Bug detection system testleri for editor module.
"""

import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from app.editor.bug_detection import (
    BugSeverity,
    BugCategory,
    BugRange,
    Bug,
    BugDetectionConfig,
    BugDetectionResult,
    BugDetectionManager
)


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
    assert BugCategory.RUNTIME.value == "runtime"
    assert BugCategory.LOGIC.value == "logic"
    assert BugCategory.PERFORMANCE.value == "performance"
    assert BugCategory.SECURITY.value == "security"
    assert BugCategory.STYLE.value == "style"
    assert BugCategory.TYPE.value == "type"
    assert BugCategory.CUSTOM.value == "custom"
    
    print(f"  All enum values verified")
    print(f"  Total categories: {len(BugCategory)}")
    
    print("\n" + "=" * 70)
    print("PASS: BugCategory enum")
    print("=" * 70)


def test_bug_range_dataclass():
    """
    Test: BugRange dataclass.
    """
    print("=" * 70)
    print("TEST: BugRange Dataclass")
    print("=" * 70)
    
    range = BugRange(
        start_line=0,
        start_column=0,
        end_line=10,
        end_column=20
    )
    
    assert range.start_line == 0, "Start line eşleşmeli"
    assert range.start_column == 0, "Start column eşleşmeli"
    assert range.end_line == 10, "End line eşleşmeli"
    assert range.end_column == 20, "End column eşleşmeli"
    
    print(f"  Start: ({range.start_line}, {range.start_column})")
    print(f"  End: ({range.end_line}, {range.end_column})")
    
    print("\n" + "=" * 70)
    print("PASS: BugRange dataclass")
    print("=" * 70)


def test_bug_dataclass():
    """
    Test: Bug dataclass.
    """
    print("=" * 70)
    print("TEST: Bug Dataclass")
    print("=" * 70)
    
    range = BugRange(0, 0, 0, 10)
    bug = Bug(
        id="bug_1",
        category=BugCategory.SYNTAX,
        severity=BugSeverity.CRITICAL,
        range=range,
        message="Syntax error",
        file_path="test.py"
    )
    
    assert bug.id == "bug_1", "ID eşleşmeli"
    assert bug.category == BugCategory.SYNTAX, "Category eşleşmeli"
    assert bug.severity == BugSeverity.CRITICAL, "Severity eşleşmeli"
    assert bug.message == "Syntax error", "Message eşleşmeli"
    assert bug.file_path == "test.py", "File path eşleşmeli"
    
    print(f"  ID: {bug.id}")
    print(f"  Category: {bug.category.value}")
    print(f"  Severity: {bug.severity.value}")
    print(f"  Message: {bug.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Bug dataclass")
    print("=" * 70)


def test_bug_detection_config_dataclass():
    """
    Test: BugDetectionConfig dataclass.
    """
    print("=" * 70)
    print("TEST: BugDetectionConfig Dataclass")
    print("=" * 70)
    
    config = BugDetectionConfig(
        enabled=True,
        min_severity=BugSeverity.LOW
    )
    
    assert config.enabled == True, "Enabled eşleşmeli"
    assert config.min_severity == BugSeverity.LOW, "Min severity eşleşmeli"
    
    print(f"  Enabled: {config.enabled}")
    print(f"  Min severity: {config.min_severity.value}")
    
    print("\n" + "=" * 70)
    print("PASS: BugDetectionConfig dataclass")
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


def test_bug_detection_manager_initialization():
    """
    Test: BugDetectionManager initialization.
    """
    print("=" * 70)
    print("TEST: BugDetectionManager Initialization")
    print("=" * 70)
    
    config = BugDetectionConfig()
    manager = BugDetectionManager(config)
    
    assert manager.config == config, "Config eşleşmeli"
    assert len(manager.bugs) == 0, "Bugs boş olmalı"
    assert manager.cache == {}, "Cache boş olmalı"
    
    print(f"  Bugs: {len(manager.bugs)}")
    print(f"  Cache: {len(manager.cache)}")
    
    print("\n" + "=" * 70)
    print("PASS: BugDetectionManager initialization")
    print("=" * 70)


def test_add_bug():
    """
    Test: Add bug.
    """
    print("=" * 70)
    print("TEST: Add Bug")
    print("=" * 70)
    
    manager = BugDetectionManager()
    
    range = BugRange(0, 0, 0, 10)
    bug = Bug(
        id="",
        category=BugCategory.SYNTAX,
        severity=BugSeverity.CRITICAL,
        range=range,
        message="Syntax error",
        file_path="test.py"
    )
    
    result = manager.add_bug(bug)
    
    assert result.success == True, "Ekleme başarılı olmalı"
    assert len(manager.bugs) > 0, "Bug eklenmeli"
    
    print(f"  Bug added: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add bug")
    print("=" * 70)


def test_remove_bug():
    """
    Test: Remove bug.
    """
    print("=" * 70)
    print("TEST: Remove Bug")
    print("=" * 70)
    
    manager = BugDetectionManager()
    
    range = BugRange(0, 0, 0, 10)
    bug = Bug(
        id="",
        category=BugCategory.SYNTAX,
        severity=BugSeverity.CRITICAL,
        range=range,
        message="Syntax error",
        file_path="test.py"
    )
    
    result = manager.add_bug(bug)
    bug_id = result.bugs[0].id
    
    result = manager.remove_bug(bug_id)
    
    assert result.success == True, "Kaldırma başarılı olmalı"
    assert bug_id not in manager.bugs, "Bug silinmeli"
    
    print(f"  Bug removed: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Remove bug")
    print("=" * 70)


def test_get_bug():
    """
    Test: Get bug.
    """
    print("=" * 70)
    print("TEST: Get Bug")
    print("=" * 70)
    
    manager = BugDetectionManager()
    
    range = BugRange(0, 0, 0, 10)
    bug = Bug(
        id="",
        category=BugCategory.SYNTAX,
        severity=BugSeverity.CRITICAL,
        range=range,
        message="Syntax error",
        file_path="test.py"
    )
    
    result = manager.add_bug(bug)
    bug_id = result.bugs[0].id
    
    retrieved_bug = manager.get_bug(bug_id)
    
    assert retrieved_bug is not None, "Bug bulunmalı"
    assert retrieved_bug.id == bug_id, "ID eşleşmeli"
    
    print(f"  Bug: {retrieved_bug.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Get bug")
    print("=" * 70)


def test_get_all_bugs():
    """
    Test: Get all bugs.
    """
    print("=" * 70)
    print("TEST: Get All Bugs")
    print("=" * 70)
    
    manager = BugDetectionManager()
    
    range = BugRange(0, 0, 0, 10)
    bug = Bug(
        id="",
        category=BugCategory.SYNTAX,
        severity=BugSeverity.CRITICAL,
        range=range,
        message="Syntax error",
        file_path="test.py"
    )
    
    manager.add_bug(bug)
    bugs = manager.get_all_bugs()
    
    assert len(bugs) > 0, "Bugs olmalı"
    
    print(f"  Total bugs: {len(bugs)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get all bugs")
    print("=" * 70)


def test_get_bugs_by_category():
    """
    Test: Get bugs by category.
    """
    print("=" * 70)
    print("TEST: Get Bugs by Category")
    print("=" * 70)
    
    manager = BugDetectionManager()
    
    range = BugRange(0, 0, 0, 10)
    bug = Bug(
        id="",
        category=BugCategory.SYNTAX,
        severity=BugSeverity.CRITICAL,
        range=range,
        message="Syntax error",
        file_path="test.py"
    )
    
    manager.add_bug(bug)
    bugs = manager.get_bugs_by_category(BugCategory.SYNTAX)
    
    assert len(bugs) > 0, "Syntax bugs olmalı"
    
    print(f"  Syntax bugs: {len(bugs)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get bugs by category")
    print("=" * 70)


def test_get_bugs_by_severity():
    """
    Test: Get bugs by severity.
    """
    print("=" * 70)
    print("TEST: Get Bugs by Severity")
    print("=" * 70)
    
    manager = BugDetectionManager()
    
    range = BugRange(0, 0, 0, 10)
    bug = Bug(
        id="",
        category=BugCategory.SYNTAX,
        severity=BugSeverity.CRITICAL,
        range=range,
        message="Syntax error",
        file_path="test.py"
    )
    
    manager.add_bug(bug)
    bugs = manager.get_bugs_by_severity(BugSeverity.CRITICAL)
    
    assert len(bugs) > 0, "Critical bugs olmalı"
    
    print(f"  Critical bugs: {len(bugs)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get bugs by severity")
    print("=" * 70)


def test_add_syntax_bug():
    """
    Test: Add syntax bug.
    """
    print("=" * 70)
    print("TEST: Add Syntax Bug")
    print("=" * 70)
    
    manager = BugDetectionManager()
    
    range = BugRange(0, 0, 0, 10)
    result = manager.add_syntax_bug(range, "Syntax error", "test.py", 0.9)
    
    assert result.success == True, "Syntax bug başarılı olmalı"
    
    print(f"  Syntax bug: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add syntax bug")
    print("=" * 70)


def test_add_runtime_bug():
    """
    Test: Add runtime bug.
    """
    print("=" * 70)
    print("TEST: Add Runtime Bug")
    print("=" * 70)
    
    manager = BugDetectionManager()
    
    range = BugRange(0, 0, 0, 10)
    result = manager.add_runtime_bug(range, "Runtime error", "test.py", BugSeverity.HIGH, 0.8)
    
    assert result.success == True, "Runtime bug başarılı olmalı"
    
    print(f"  Runtime bug: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add runtime bug")
    print("=" * 70)


def test_add_logic_bug():
    """
    Test: Add logic bug.
    """
    print("=" * 70)
    print("TEST: Add Logic Bug")
    print("=" * 70)
    
    manager = BugDetectionManager()
    
    range = BugRange(0, 0, 0, 10)
    result = manager.add_logic_bug(range, "Logic error", "test.py", BugSeverity.MEDIUM, 0.7)
    
    assert result.success == True, "Logic bug başarılı olmalı"
    
    print(f"  Logic bug: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add logic bug")
    print("=" * 70)


def test_add_performance_bug():
    """
    Test: Add performance bug.
    """
    print("=" * 70)
    print("TEST: Add Performance Bug")
    print("=" * 70)
    
    manager = BugDetectionManager()
    
    range = BugRange(0, 0, 0, 10)
    result = manager.add_performance_bug(range, "Performance issue", "test.py", 0.7)
    
    assert result.success == True, "Performance bug başarılı olmalı"
    
    print(f"  Performance bug: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add performance bug")
    print("=" * 70)


def test_add_security_bug():
    """
    Test: Add security bug.
    """
    print("=" * 70)
    print("TEST: Add Security Bug")
    print("=" * 70)
    
    manager = BugDetectionManager()
    
    range = BugRange(0, 0, 0, 10)
    result = manager.add_security_bug(range, "Security issue", "test.py", BugSeverity.HIGH, 0.8)
    
    assert result.success == True, "Security bug başarılı olmalı"
    
    print(f"  Security bug: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add security bug")
    print("=" * 70)


def test_add_style_bug():
    """
    Test: Add style bug.
    """
    print("=" * 70)
    print("TEST: Add Style Bug")
    print("=" * 70)
    
    manager = BugDetectionManager()
    
    range = BugRange(0, 0, 0, 10)
    result = manager.add_style_bug(range, "Style issue", "test.py", 0.6)
    
    assert result.success == True, "Style bug başarılı olmalı"
    
    print(f"  Style bug: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add style bug")
    print("=" * 70)


def test_add_type_bug():
    """
    Test: Add type bug.
    """
    print("=" * 70)
    print("TEST: Add Type Bug")
    print("=" * 70)
    
    manager = BugDetectionManager()
    
    range = BugRange(0, 0, 0, 10)
    result = manager.add_type_bug(range, "Type error", "test.py", BugSeverity.MEDIUM, 0.8)
    
    assert result.success == True, "Type bug başarılı olmalı"
    
    print(f"  Type bug: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add type bug")
    print("=" * 70)


def test_filter_by_severity():
    """
    Test: Filter by severity.
    """
    print("=" * 70)
    print("TEST: Filter by Severity")
    print("=" * 70)
    
    manager = BugDetectionManager()
    
    range = BugRange(0, 0, 0, 10)
    manager.add_syntax_bug(range, "text1", "test.py", 0.9)
    manager.add_style_bug(range, "text2", "test.py", 0.6)
    
    filtered = manager.filter_by_severity(BugSeverity.HIGH)
    
    assert len(filtered) > 0, "Filtered bugs olmalı"
    
    print(f"  Filtered bugs: {len(filtered)}")
    
    print("\n" + "=" * 70)
    print("PASS: Filter by severity")
    print("=" * 70)


def test_filter_by_confidence():
    """
    Test: Filter by confidence.
    """
    print("=" * 70)
    print("TEST: Filter by Confidence")
    print("=" * 70)
    
    manager = BugDetectionManager()
    
    range = BugRange(0, 0, 0, 10)
    manager.add_syntax_bug(range, "text1", "test.py", 0.9)
    manager.add_syntax_bug(range, "text2", "test.py", 0.5)
    
    filtered = manager.filter_by_confidence(0.7)
    
    assert len(filtered) > 0, "Filtered bugs olmalı"
    
    print(f"  Filtered bugs: {len(filtered)}")
    
    print("\n" + "=" * 70)
    print("PASS: Filter by confidence")
    print("=" * 70)


def test_get_bugs_in_file():
    """
    Test: Get bugs in file.
    """
    print("=" * 70)
    print("TEST: Get Bugs in File")
    print("=" * 70)
    
    manager = BugDetectionManager()
    
    range = BugRange(0, 0, 0, 10)
    manager.add_syntax_bug(range, "text", "test.py", 0.8)
    
    bugs = manager.get_bugs_in_file("test.py")
    
    assert len(bugs) > 0, "test.py bugs olmalı"
    
    print(f"  test.py bugs: {len(bugs)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get bugs in file")
    print("=" * 70)


def test_get_bugs_at_line():
    """
    Test: Get bugs at line.
    """
    print("=" * 70)
    print("TEST: Get Bugs at Line")
    print("=" * 70)
    
    manager = BugDetectionManager()
    
    range = BugRange(0, 0, 10, 0)
    manager.add_syntax_bug(range, "text", "test.py", 0.8)
    
    bugs = manager.get_bugs_at_line("test.py", 5)
    
    assert len(bugs) > 0, "Line 5 bugs olmalı"
    
    print(f"  Line 5 bugs: {len(bugs)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get bugs at line")
    print("=" * 70)


def test_clear_bugs():
    """
    Test: Clear bugs.
    """
    print("=" * 70)
    print("TEST: Clear Bugs")
    print("=" * 70)
    
    manager = BugDetectionManager()
    
    range = BugRange(0, 0, 0, 10)
    manager.add_syntax_bug(range, "text", "test.py", 0.8)
    
    result = manager.clear_bugs()
    
    assert result.success == True, "Clear başarılı olmalı"
    assert len(manager.bugs) == 0, "Bugs temizlenmeli"
    
    print(f"  Cleared: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear bugs")
    print("=" * 70)


def test_clear_bugs_by_category():
    """
    Test: Clear bugs by category.
    """
    print("=" * 70)
    print("TEST: Clear Bugs by Category")
    print("=" * 70)
    
    manager = BugDetectionManager()
    
    range = BugRange(0, 0, 0, 10)
    manager.add_syntax_bug(range, "text", "test.py", 0.8)
    
    result = manager.clear_bugs_by_category(BugCategory.SYNTAX)
    
    assert result.success == True, "Clear başarılı olmalı"
    
    print(f"  Cleared by category: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear bugs by category")
    print("=" * 70)


def test_set_bug_enabled():
    """
    Test: Set bug enabled.
    """
    print("=" * 70)
    print("TEST: Set Bug Enabled")
    print("=" * 70)
    
    manager = BugDetectionManager()
    
    range = BugRange(0, 0, 0, 10)
    result = manager.add_syntax_bug(range, "text", "test.py", 0.8)
    bug_id = result.bugs[0].id
    
    result = manager.set_bug_enabled(bug_id, False)
    
    assert result.success == True, "Set başarılı olmalı"
    
    print(f"  Bug enabled state: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set bug enabled")
    print("=" * 70)


def test_set_bug_visible():
    """
    Test: Set bug visible.
    """
    print("=" * 70)
    print("TEST: Set Bug Visible")
    print("=" * 70)
    
    manager = BugDetectionManager()
    
    range = BugRange(0, 0, 0, 10)
    result = manager.add_syntax_bug(range, "text", "test.py", 0.8)
    bug_id = result.bugs[0].id
    
    result = manager.set_bug_visible(bug_id, False)
    
    assert result.success == True, "Set başarılı olmalı"
    
    print(f"  Bug visible state: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set bug visible")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    manager = BugDetectionManager()
    
    new_config = BugDetectionConfig(max_bugs=200)
    result = manager.update_config(new_config)
    
    assert result.success == True, "Update başarılı olmalı"
    assert manager.config.max_bugs == 200, "Config güncellenmeli"
    
    print(f"  Max bugs: {manager.config.max_bugs}")
    
    print("\n" + "=" * 70)
    print("PASS: Update config")
    print("=" * 70)


def test_get_config():
    """
    Test: Get config.
    """
    print("=" * 70)
    print("TEST: Get Config")
    print("=" * 70)
    
    config = BugDetectionConfig(max_bugs=200)
    manager = BugDetectionManager(config)
    
    retrieved_config = manager.get_config()
    
    assert retrieved_config.max_bugs == 200, "Config eşleşmeli"
    
    print(f"  Max bugs: {retrieved_config.max_bugs}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_bug_severity_enum()
        test2 = test_bug_category_enum()
        test3 = test_bug_range_dataclass()
        test4 = test_bug_dataclass()
        test5 = test_bug_detection_config_dataclass()
        test6 = test_bug_detection_result_dataclass()
        test7 = test_bug_detection_manager_initialization()
        test8 = test_add_bug()
        test9 = test_remove_bug()
        test10 = test_get_bug()
        test11 = test_get_all_bugs()
        test12 = test_get_bugs_by_category()
        test13 = test_get_bugs_by_severity()
        test14 = test_add_syntax_bug()
        test15 = test_add_runtime_bug()
        test16 = test_add_logic_bug()
        test17 = test_add_performance_bug()
        test18 = test_add_security_bug()
        test19 = test_add_style_bug()
        test20 = test_add_type_bug()
        test21 = test_filter_by_severity()
        test22 = test_filter_by_confidence()
        test23 = test_get_bugs_in_file()
        test24 = test_get_bugs_at_line()
        test25 = test_clear_bugs()
        test26 = test_clear_bugs_by_category()
        test27 = test_set_bug_enabled()
        test28 = test_set_bug_visible()
        test29 = test_update_config()
        test30 = test_get_config()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"BugSeverity Enum: {'PASS' if test1 else 'FAIL'}")
        print(f"BugCategory Enum: {'PASS' if test2 else 'FAIL'}")
        print(f"BugRange Dataclass: {'PASS' if test3 else 'FAIL'}")
        print(f"Bug Dataclass: {'PASS' if test4 else 'FAIL'}")
        print(f"BugDetectionConfig Dataclass: {'PASS' if test5 else 'FAIL'}")
        print(f"BugDetectionResult Dataclass: {'PASS' if test6 else 'FAIL'}")
        print(f"BugDetectionManager Initialization: {'PASS' if test7 else 'FAIL'}")
        print(f"Add Bug: {'PASS' if test8 else 'FAIL'}")
        print(f"Remove Bug: {'PASS' if test9 else 'FAIL'}")
        print(f"Get Bug: {'PASS' if test10 else 'FAIL'}")
        print(f"Get All Bugs: {'PASS' if test11 else 'FAIL'}")
        print(f"Get Bugs by Category: {'PASS' if test12 else 'FAIL'}")
        print(f"Get Bugs by Severity: {'PASS' if test13 else 'FAIL'}")
        print(f"Add Syntax Bug: {'PASS' if test14 else 'FAIL'}")
        print(f"Add Runtime Bug: {'PASS' if test15 else 'FAIL'}")
        print(f"Add Logic Bug: {'PASS' if test16 else 'FAIL'}")
        print(f"Add Performance Bug: {'PASS' if test17 else 'FAIL'}")
        print(f"Add Security Bug: {'PASS' if test18 else 'FAIL'}")
        print(f"Add Style Bug: {'PASS' if test19 else 'FAIL'}")
        print(f"Add Type Bug: {'PASS' if test20 else 'FAIL'}")
        print(f"Filter by Severity: {'PASS' if test21 else 'FAIL'}")
        print(f"Filter by Confidence: {'PASS' if test22 else 'FAIL'}")
        print(f"Get Bugs in File: {'PASS' if test23 else 'FAIL'}")
        print(f"Get Bugs at Line: {'PASS' if test24 else 'FAIL'}")
        print(f"Clear Bugs: {'PASS' if test25 else 'FAIL'}")
        print(f"Clear Bugs by Category: {'PASS' if test26 else 'FAIL'}")
        print(f"Set Bug Enabled: {'PASS' if test27 else 'FAIL'}")
        print(f"Set Bug Visible: {'PASS' if test28 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test29 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test30 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14, test15, test16, test17, test18, test19, test20, test21, test22, test23, test24, test25, test26, test27, test28, test29, test30])
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
