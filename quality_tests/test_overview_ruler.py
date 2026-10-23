"""
Quality Test: Overview Ruler
Overview ruler system testleri.
"""

import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from app.editor.overview_ruler import (
    OverviewRulerPosition,
    OverviewRulerColor,
    OverviewRulerMark,
    OverviewRulerConfig,
    OverviewRulerResult,
    OverviewRulerManager
)


def test_overview_ruler_position_enum():
    """
    Test: OverviewRulerPosition enum.
    """
    print("=" * 70)
    print("TEST: OverviewRulerPosition Enum")
    print("=" * 70)
    
    assert OverviewRulerPosition.LEFT.value == "left"
    assert OverviewRulerPosition.RIGHT.value == "right"
    
    print(f"  All enum values verified")
    print(f"  Total positions: {len(OverviewRulerPosition)}")
    
    print("\n" + "=" * 70)
    print("PASS: OverviewRulerPosition enum")
    print("=" * 70)


def test_overview_ruler_color_enum():
    """
    Test: OverviewRulerColor enum.
    """
    print("=" * 70)
    print("TEST: OverviewRulerColor Enum")
    print("=" * 70)
    
    assert OverviewRulerColor.ERROR.value == "#FF0000"
    assert OverviewRulerColor.WARNING.value == "#FFA500"
    assert OverviewRulerColor.INFO.value == "#0000FF"
    assert OverviewRulerColor.HINT.value == "#00FF00"
    assert OverviewRulerColor.SUCCESS.value == "#008000"
    assert OverviewRulerColor.CUSTOM.value == "#808080"
    
    print(f"  All enum values verified")
    print(f"  Total colors: {len(OverviewRulerColor)}")
    
    print("\n" + "=" * 70)
    print("PASS: OverviewRulerColor enum")
    print("=" * 70)


def test_overview_ruler_mark_dataclass():
    """
    Test: OverviewRulerMark dataclass.
    """
    print("=" * 70)
    print("TEST: OverviewRulerMark Dataclass")
    print("=" * 70)
    
    mark = OverviewRulerMark(
        id="mark_1",
        line=10,
        color="#FF0000"
    )
    
    assert mark.id == "mark_1", "ID eşleşmeli"
    assert mark.line == 10, "Line eşleşmeli"
    assert mark.color == "#FF0000", "Color eşleşmeli"
    
    print(f"  ID: {mark.id}")
    print(f"  Line: {mark.line}")
    print(f"  Color: {mark.color}")
    
    print("\n" + "=" * 70)
    print("PASS: OverviewRulerMark dataclass")
    print("=" * 70)


def test_overview_ruler_config_dataclass():
    """
    Test: OverviewRulerConfig dataclass.
    """
    print("=" * 70)
    print("TEST: OverviewRulerConfig Dataclass")
    print("=" * 70)
    
    config = OverviewRulerConfig(
        enabled=True,
        position=OverviewRulerPosition.RIGHT
    )
    
    assert config.enabled == True, "Enabled eşleşmeli"
    assert config.position == OverviewRulerPosition.RIGHT, "Position eşleşmeli"
    
    print(f"  Enabled: {config.enabled}")
    print(f"  Position: {config.position.value}")
    
    print("\n" + "=" * 70)
    print("PASS: OverviewRulerConfig dataclass")
    print("=" * 70)


def test_overview_ruler_result_dataclass():
    """
    Test: OverviewRulerResult dataclass.
    """
    print("=" * 70)
    print("TEST: OverviewRulerResult Dataclass")
    print("=" * 70)
    
    result = OverviewRulerResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.marks, list), "Marks list olmalı"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Marks: {len(result.marks)}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: OverviewRulerResult dataclass")
    print("=" * 70)


def test_overview_ruler_manager_initialization():
    """
    Test: OverviewRulerManager initialization.
    """
    print("=" * 70)
    print("TEST: OverviewRulerManager Initialization")
    print("=" * 70)
    
    config = OverviewRulerConfig()
    manager = OverviewRulerManager(config)
    
    assert manager.config == config, "Config eşleşmeli"
    assert len(manager.marks) == 0, "Marks boş olmalı"
    
    print(f"  Marks: {len(manager.marks)}")
    
    print("\n" + "=" * 70)
    print("PASS: OverviewRulerManager initialization")
    print("=" * 70)


def test_add_mark():
    """
    Test: Add mark.
    """
    print("=" * 70)
    print("TEST: Add Mark")
    print("=" * 70)
    
    manager = OverviewRulerManager()
    
    mark = OverviewRulerMark(
        id="",
        line=10,
        color="#FF0000"
    )
    
    result = manager.add_mark(mark)
    
    assert result.success == True, "Ekleme başarılı olmalı"
    assert len(manager.marks) > 0, "Mark eklenmeli"
    
    print(f"  Mark added: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add mark")
    print("=" * 70)


def test_remove_mark():
    """
    Test: Remove mark.
    """
    print("=" * 70)
    print("TEST: Remove Mark")
    print("=" * 70)
    
    manager = OverviewRulerManager()
    
    mark = OverviewRulerMark(
        id="",
        line=10,
        color="#FF0000"
    )
    
    result = manager.add_mark(mark)
    mark_id = result.marks[0].id
    
    result = manager.remove_mark(mark_id)
    
    assert result.success == True, "Kaldırma başarılı olmalı"
    assert mark_id not in manager.marks, "Mark silinmeli"
    
    print(f"  Mark removed: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Remove mark")
    print("=" * 70)


def test_get_mark():
    """
    Test: Get mark.
    """
    print("=" * 70)
    print("TEST: Get Mark")
    print("=" * 70)
    
    manager = OverviewRulerManager()
    
    mark = OverviewRulerMark(
        id="",
        line=10,
        color="#FF0000"
    )
    
    result = manager.add_mark(mark)
    mark_id = result.marks[0].id
    
    retrieved_mark = manager.get_mark(mark_id)
    
    assert retrieved_mark is not None, "Mark bulunmalı"
    assert retrieved_mark.id == mark_id, "ID eşleşmeli"
    
    print(f"  Mark: line {retrieved_mark.line}")
    
    print("\n" + "=" * 70)
    print("PASS: Get mark")
    print("=" * 70)


def test_get_all_marks():
    """
    Test: Get all marks.
    """
    print("=" * 70)
    print("TEST: Get All Marks")
    print("=" * 70)
    
    manager = OverviewRulerManager()
    
    mark = OverviewRulerMark(
        id="",
        line=10,
        color="#FF0000"
    )
    
    manager.add_mark(mark)
    marks = manager.get_all_marks()
    
    assert len(marks) > 0, "Marks olmalı"
    
    print(f"  Total marks: {len(marks)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get all marks")
    print("=" * 70)


def test_get_marks_at_line():
    """
    Test: Get marks at line.
    """
    print("=" * 70)
    print("TEST: Get Marks at Line")
    print("=" * 70)
    
    manager = OverviewRulerManager()
    
    mark = OverviewRulerMark(
        id="",
        line=10,
        color="#FF0000"
    )
    
    manager.add_mark(mark)
    marks = manager.get_marks_at_line(10)
    
    assert len(marks) > 0, "Line 10 marks olmalı"
    
    print(f"  Line 10 marks: {len(marks)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get marks at line")
    print("=" * 70)


def test_add_error_mark():
    """
    Test: Add error mark.
    """
    print("=" * 70)
    print("TEST: Add Error Mark")
    print("=" * 70)
    
    manager = OverviewRulerManager()
    
    result = manager.add_error_mark(10, "Test error")
    
    assert result.success == True, "Error mark başarılı olmalı"
    
    print(f"  Error mark added: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add error mark")
    print("=" * 70)


def test_add_warning_mark():
    """
    Test: Add warning mark.
    """
    print("=" * 70)
    print("TEST: Add Warning Mark")
    print("=" * 70)
    
    manager = OverviewRulerManager()
    
    result = manager.add_warning_mark(10, "Test warning")
    
    assert result.success == True, "Warning mark başarılı olmalı"
    
    print(f"  Warning mark added: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add warning mark")
    print("=" * 70)


def test_add_info_mark():
    """
    Test: Add info mark.
    """
    print("=" * 70)
    print("TEST: Add Info Mark")
    print("=" * 70)
    
    manager = OverviewRulerManager()
    
    result = manager.add_info_mark(10, "Test info")
    
    assert result.success == True, "Info mark başarılı olmalı"
    
    print(f"  Info mark added: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add info mark")
    print("=" * 70)


def test_add_hint_mark():
    """
    Test: Add hint mark.
    """
    print("=" * 70)
    print("TEST: Add Hint Mark")
    print("=" * 70)
    
    manager = OverviewRulerManager()
    
    result = manager.add_hint_mark(10, "Test hint")
    
    assert result.success == True, "Hint mark başarılı olmalı"
    
    print(f"  Hint mark added: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add hint mark")
    print("=" * 70)


def test_add_success_mark():
    """
    Test: Add success mark.
    """
    print("=" * 70)
    print("TEST: Add Success Mark")
    print("=" * 70)
    
    manager = OverviewRulerManager()
    
    result = manager.add_success_mark(10, "Test success")
    
    assert result.success == True, "Success mark başarılı olmalı"
    
    print(f"  Success mark added: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add success mark")
    print("=" * 70)


def test_add_custom_mark():
    """
    Test: Add custom mark.
    """
    print("=" * 70)
    print("TEST: Add Custom Mark")
    print("=" * 70)
    
    manager = OverviewRulerManager()
    
    result = manager.add_custom_mark(10, "#FF00FF", "Test custom")
    
    assert result.success == True, "Custom mark başarılı olmalı"
    
    print(f"  Custom mark added: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add custom mark")
    print("=" * 70)


def test_clear_marks():
    """
    Test: Clear marks.
    """
    print("=" * 70)
    print("TEST: Clear Marks")
    print("=" * 70)
    
    manager = OverviewRulerManager()
    
    mark = OverviewRulerMark(
        id="",
        line=10,
        color="#FF0000"
    )
    
    manager.add_mark(mark)
    result = manager.clear_marks()
    
    assert result.success == True, "Clear başarılı olmalı"
    assert len(manager.marks) == 0, "Marks temizlenmeli"
    
    print(f"  Cleared: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear marks")
    print("=" * 70)


def test_set_mark_enabled():
    """
    Test: Set mark enabled.
    """
    print("=" * 70)
    print("TEST: Set Mark Enabled")
    print("=" * 70)
    
    manager = OverviewRulerManager()
    
    mark = OverviewRulerMark(
        id="",
        line=10,
        color="#FF0000"
    )
    
    result = manager.add_mark(mark)
    mark_id = result.marks[0].id
    
    result = manager.set_mark_enabled(mark_id, False)
    
    assert result.success == True, "Set başarılı olmalı"
    
    print(f"  Mark enabled state: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set mark enabled")
    print("=" * 70)


def test_set_mark_visible():
    """
    Test: Set mark visible.
    """
    print("=" * 70)
    print("TEST: Set Mark Visible")
    print("=" * 70)
    
    manager = OverviewRulerManager()
    
    mark = OverviewRulerMark(
        id="",
        line=10,
        color="#FF0000"
    )
    
    result = manager.add_mark(mark)
    mark_id = result.marks[0].id
    
    result = manager.set_mark_visible(mark_id, False)
    
    assert result.success == True, "Set başarılı olmalı"
    
    print(f"  Mark visible state: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set mark visible")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    manager = OverviewRulerManager()
    
    new_config = OverviewRulerConfig(width=20)
    result = manager.update_config(new_config)
    
    assert result.success == True, "Update başarılı olmalı"
    assert manager.config.width == 20, "Config güncellenmeli"
    
    print(f"  Width: {manager.config.width}")
    
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
    
    config = OverviewRulerConfig(width=20)
    manager = OverviewRulerManager(config)
    
    retrieved_config = manager.get_config()
    
    assert retrieved_config.width == 20, "Config eşleşmeli"
    
    print(f"  Width: {retrieved_config.width}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_overview_ruler_position_enum()
        test2 = test_overview_ruler_color_enum()
        test3 = test_overview_ruler_mark_dataclass()
        test4 = test_overview_ruler_config_dataclass()
        test5 = test_overview_ruler_result_dataclass()
        test6 = test_overview_ruler_manager_initialization()
        test7 = test_add_mark()
        test8 = test_remove_mark()
        test9 = test_get_mark()
        test10 = test_get_all_marks()
        test11 = test_get_marks_at_line()
        test12 = test_add_error_mark()
        test13 = test_add_warning_mark()
        test14 = test_add_info_mark()
        test15 = test_add_hint_mark()
        test16 = test_add_success_mark()
        test17 = test_add_custom_mark()
        test18 = test_clear_marks()
        test19 = test_set_mark_enabled()
        test20 = test_set_mark_visible()
        test21 = test_update_config()
        test22 = test_get_config()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"OverviewRulerPosition Enum: {'PASS' if test1 else 'FAIL'}")
        print(f"OverviewRulerColor Enum: {'PASS' if test2 else 'FAIL'}")
        print(f"OverviewRulerMark Dataclass: {'PASS' if test3 else 'FAIL'}")
        print(f"OverviewRulerConfig Dataclass: {'PASS' if test4 else 'FAIL'}")
        print(f"OverviewRulerResult Dataclass: {'PASS' if test5 else 'FAIL'}")
        print(f"OverviewRulerManager Initialization: {'PASS' if test6 else 'FAIL'}")
        print(f"Add Mark: {'PASS' if test7 else 'FAIL'}")
        print(f"Remove Mark: {'PASS' if test8 else 'FAIL'}")
        print(f"Get Mark: {'PASS' if test9 else 'FAIL'}")
        print(f"Get All Marks: {'PASS' if test10 else 'FAIL'}")
        print(f"Get Marks at Line: {'PASS' if test11 else 'FAIL'}")
        print(f"Add Error Mark: {'PASS' if test12 else 'FAIL'}")
        print(f"Add Warning Mark: {'PASS' if test13 else 'FAIL'}")
        print(f"Add Info Mark: {'PASS' if test14 else 'FAIL'}")
        print(f"Add Hint Mark: {'PASS' if test15 else 'FAIL'}")
        print(f"Add Success Mark: {'PASS' if test16 else 'FAIL'}")
        print(f"Add Custom Mark: {'PASS' if test17 else 'FAIL'}")
        print(f"Clear Marks: {'PASS' if test18 else 'FAIL'}")
        print(f"Set Mark Enabled: {'PASS' if test19 else 'FAIL'}")
        print(f"Set Mark Visible: {'PASS' if test20 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test21 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test22 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14, test15, test16, test17, test18, test19, test20, test21, test22])
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
