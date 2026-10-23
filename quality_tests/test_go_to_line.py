"""
Quality Test: Go to Line
Go to line system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.go_to_line import (
    GoToLineEngine,
    NavigationMode,
    LinePosition,
    LineInfo,
    GoToLineConfig,
    GoToLineResult
)


def test_go_to_line():
    """
    Test: Go to line.
    """
    print("=" * 70)
    print("TEST: Go to Line")
    print("=" * 70)
    
    engine = GoToLineEngine()
    content = "line1\nline2\nline3\nline4\nline5"
    engine.set_content(content)
    
    result = engine.go_to_line(3)
    
    assert result.success, "Gitme başarılı olmalı"
    assert result.line_number == 3, "Satır numarası 3 olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Line number: {result.line_number}")
    
    print("\n" + "=" * 70)
    print("PASS: Go to line")
    print("=" * 70)


def test_go_to_relative():
    """
    Test: Go to relative.
    """
    print("=" * 70)
    print("TEST: Go to Relative")
    print("=" * 70)
    
    engine = GoToLineEngine()
    content = "line1\nline2\nline3\nline4\nline5"
    engine.set_content(content)
    engine.go_to_line(2)
    
    result = engine.go_to_relative(2)
    
    assert result.success, "Göreceli gitme başarılı olmalı"
    assert result.line_number == 4, "Satır numarası 4 olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Line number: {result.line_number}")
    
    print("\n" + "=" * 70)
    print("PASS: Go to relative")
    print("=" * 70)


def test_go_to_percentage():
    """
    Test: Go to percentage.
    """
    print("=" * 70)
    print("TEST: Go to Percentage")
    print("=" * 70)
    
    engine = GoToLineEngine()
    content = "line1\nline2\nline3\nline4\nline5"
    engine.set_content(content)
    
    result = engine.go_to_percentage(0.5)
    
    assert result.success, "Yüzde bazlı gitme başarılı olmalı"
    assert result.line_number == 3, "Satır numarası 3 olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Line number: {result.line_number}")
    
    print("\n" + "=" * 70)
    print("PASS: Go to percentage")
    print("=" * 70)


def test_go_to_position():
    """
    Test: Go to position.
    """
    print("=" * 70)
    print("TEST: Go to Position")
    print("=" * 70)
    
    engine = GoToLineEngine()
    content = "line1\nline2\nline3\nline4\nline5"
    engine.set_content(content)
    
    result = engine.go_to_position(LinePosition.START)
    
    assert result.success, "Pozisyona gitme başarılı olmalı"
    assert result.line_number == 1, "Satır numarası 1 olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Line number: {result.line_number}")
    
    print("\n" + "=" * 70)
    print("PASS: Go to position")
    print("=" * 70)


def test_go_to_start():
    """
    Test: Go to start.
    """
    print("=" * 70)
    print("TEST: Go to Start")
    print("=" * 70)
    
    engine = GoToLineEngine()
    content = "line1\nline2\nline3\nline4\nline5"
    engine.set_content(content)
    engine.go_to_line(5)
    
    result = engine.go_to_start()
    
    assert result.success, "Başlangıca gitme başarılı olmalı"
    assert result.line_number == 1, "Satır numarası 1 olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Line number: {result.line_number}")
    
    print("\n" + "=" * 70)
    print("PASS: Go to start")
    print("=" * 70)


def test_go_to_end():
    """
    Test: Go to end.
    """
    print("=" * 70)
    print("TEST: Go to End")
    print("=" * 70)
    
    engine = GoToLineEngine()
    content = "line1\nline2\nline3\nline4\nline5"
    engine.set_content(content)
    
    result = engine.go_to_end()
    
    assert result.success, "Sona gitme başarılı olmalı"
    assert result.line_number == 5, "Satır numarası 5 olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Line number: {result.line_number}")
    
    print("\n" + "=" * 70)
    print("PASS: Go to end")
    print("=" * 70)


def test_go_to_middle():
    """
    Test: Go to middle.
    """
    print("=" * 70)
    print("TEST: Go to Middle")
    print("=" * 70)
    
    engine = GoToLineEngine()
    content = "line1\nline2\nline3\nline4\nline5"
    engine.set_content(content)
    
    result = engine.go_to_middle()
    
    assert result.success, "Ortaya gitme başarılı olmalı"
    assert result.line_number == 3, "Satır numarası 3 olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Line number: {result.line_number}")
    
    print("\n" + "=" * 70)
    print("PASS: Go to middle")
    print("=" * 70)


def test_get_current_line():
    """
    Test: Get current line.
    """
    print("=" * 70)
    print("TEST: Get Current Line")
    print("=" * 70)
    
    engine = GoToLineEngine()
    content = "line1\nline2\nline3\nline4\nline5"
    engine.set_content(content)
    engine.go_to_line(3)
    
    result = engine.get_current_line()
    
    assert result.success, "Mevcut satır alma başarılı olmalı"
    assert result.line_number == 3, "Satır numarası 3 olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Line number: {result.line_number}")
    
    print("\n" + "=" * 70)
    print("PASS: Get current line")
    print("=" * 70)


def test_get_line_info():
    """
    Test: Get line info.
    """
    print("=" * 70)
    print("TEST: Get Line Info")
    print("=" * 70)
    
    engine = GoToLineEngine()
    content = "line1\nline2\nline3\nline4\nline5"
    
    result = engine.get_line_info(3, content)
    
    assert result.success, "Satır bilgisi alma başarılı olmalı"
    assert result.line_number == 3, "Satır numarası 3 olmalı"
    assert result.line_info.line_content == "line3", "Satır içeriği eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Line number: {result.line_number}")
    print(f"  Line content: {result.line_info.line_content}")
    
    print("\n" + "=" * 70)
    print("PASS: Get line info")
    print("=" * 70)


def test_go_back():
    """
    Test: Go back.
    """
    print("=" * 70)
    print("TEST: Go Back")
    print("=" * 70)
    
    engine = GoToLineEngine()
    content = "line1\nline2\nline3\nline4\nline5"
    engine.set_content(content)
    engine.go_to_line(2)
    engine.go_to_line(4)
    
    result = engine.go_back()
    
    assert result.success, "Geri gitme başarılı olmalı"
    assert result.line_number == 2, "Satır numarası 2 olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Line number: {result.line_number}")
    
    print("\n" + "=" * 70)
    print("PASS: Go back")
    print("=" * 70)


def test_clear_history():
    """
    Test: Clear history.
    """
    print("=" * 70)
    print("TEST: Clear History")
    print("=" * 70)
    
    engine = GoToLineEngine()
    content = "line1\nline2\nline3\nline4\nline5"
    engine.set_content(content)
    engine.go_to_line(2)
    engine.go_to_line(4)
    
    result = engine.clear_history()
    
    assert result.success, "Geçmiş temizleme başarılı olmalı"
    assert len(engine.get_history()) == 0, "Geçmiş boş olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  History: {len(engine.get_history())}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear history")
    print("=" * 70)


def test_get_history():
    """
    Test: Get history.
    """
    print("=" * 70)
    print("TEST: Get History")
    print("=" * 70)
    
    engine = GoToLineEngine()
    content = "line1\nline2\nline3\nline4\nline5"
    engine.set_content(content)
    engine.go_to_line(2)
    engine.go_to_line(4)
    
    history = engine.get_history()
    
    assert len(history) > 0, "Geçmiş olmalı"
    
    print(f"  History: {history}")
    
    print("\n" + "=" * 70)
    print("PASS: Get history")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    engine = GoToLineEngine()
    
    new_config = GoToLineConfig(center_on_navigation=False)
    result = engine.update_config(new_config)
    
    assert result.success, "Güncelleme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    
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
    
    engine = GoToLineEngine()
    
    config = engine.get_config()
    
    assert config is not None, "Config olmalı"
    assert config.center_on_navigation == True, "Config eşleşmeli"
    
    print(f"  Center on navigation: {config.center_on_navigation}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


def test_navigation_mode_enum():
    """
    Test: NavigationMode enum.
    """
    print("=" * 70)
    print("TEST: NavigationMode Enum")
    print("=" * 70)
    
    assert NavigationMode.ABSOLUTE.value == "absolute"
    assert NavigationMode.RELATIVE.value == "relative"
    assert NavigationMode.PERCENTAGE.value == "percentage"
    
    print(f"  All enum values verified")
    print(f"  Total modes: {len(NavigationMode)}")
    
    print("\n" + "=" * 70)
    print("PASS: NavigationMode enum")
    print("=" * 70)


def test_line_position_enum():
    """
    Test: LinePosition enum.
    """
    print("=" * 70)
    print("TEST: LinePosition Enum")
    print("=" * 70)
    
    assert LinePosition.START.value == "start"
    assert LinePosition.END.value == "end"
    assert LinePosition.MIDDLE.value == "middle"
    assert LinePosition.CUSTOM.value == "custom"
    
    print(f"  All enum values verified")
    print(f"  Total positions: {len(LinePosition)}")
    
    print("\n" + "=" * 70)
    print("PASS: LinePosition enum")
    print("=" * 70)


def test_line_info_dataclass():
    """
    Test: LineInfo dataclass.
    """
    print("=" * 70)
    print("TEST: LineInfo Dataclass")
    print("=" * 70)
    
    line_info = LineInfo(
        line_number=5,
        column=10,
        line_content="test line",
        is_visible=True
    )
    
    assert line_info.line_number == 5, "Line number eşleşmeli"
    assert line_info.column == 10, "Column eşleşmeli"
    assert line_info.line_content == "test line", "Line content eşleşmeli"
    
    print(f"  Line number: {line_info.line_number}")
    print(f"  Column: {line_info.column}")
    print(f"  Line content: {line_info.line_content}")
    
    print("\n" + "=" * 70)
    print("PASS: LineInfo dataclass")
    print("=" * 70)


def test_go_to_line_config_dataclass():
    """
    Test: GoToLineConfig dataclass.
    """
    print("=" * 70)
    print("TEST: GoToLineConfig Dataclass")
    print("=" * 70)
    
    config = GoToLineConfig(
        center_on_navigation=True,
        scroll_animation=True,
        highlight_line=True
    )
    
    assert config.center_on_navigation == True, "Center on navigation eşleşmeli"
    assert config.scroll_animation == True, "Scroll animation eşleşmeli"
    assert config.highlight_line == True, "Highlight line eşleşmeli"
    
    print(f"  Center on navigation: {config.center_on_navigation}")
    print(f"  Scroll animation: {config.scroll_animation}")
    print(f"  Highlight line: {config.highlight_line}")
    
    print("\n" + "=" * 70)
    print("PASS: GoToLineConfig dataclass")
    print("=" * 70)


def test_go_to_line_result_dataclass():
    """
    Test: GoToLineResult dataclass.
    """
    print("=" * 70)
    print("TEST: GoToLineResult Dataclass")
    print("=" * 70)
    
    result = GoToLineResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: GoToLineResult dataclass")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_go_to_line()
        test2 = test_go_to_relative()
        test3 = test_go_to_percentage()
        test4 = test_go_to_position()
        test5 = test_go_to_start()
        test6 = test_go_to_end()
        test7 = test_go_to_middle()
        test8 = test_get_current_line()
        test9 = test_get_line_info()
        test10 = test_go_back()
        test11 = test_clear_history()
        test12 = test_get_history()
        test13 = test_update_config()
        test14 = test_get_config()
        test15 = test_navigation_mode_enum()
        test16 = test_line_position_enum()
        test17 = test_line_info_dataclass()
        test18 = test_go_to_line_config_dataclass()
        test19 = test_go_to_line_result_dataclass()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Go to Line: {'PASS' if test1 else 'FAIL'}")
        print(f"Go to Relative: {'PASS' if test2 else 'FAIL'}")
        print(f"Go to Percentage: {'PASS' if test3 else 'FAIL'}")
        print(f"Go to Position: {'PASS' if test4 else 'FAIL'}")
        print(f"Go to Start: {'PASS' if test5 else 'FAIL'}")
        print(f"Go to End: {'PASS' if test6 else 'FAIL'}")
        print(f"Go to Middle: {'PASS' if test7 else 'FAIL'}")
        print(f"Get Current Line: {'PASS' if test8 else 'FAIL'}")
        print(f"Get Line Info: {'PASS' if test9 else 'FAIL'}")
        print(f"Go Back: {'PASS' if test10 else 'FAIL'}")
        print(f"Clear History: {'PASS' if test11 else 'FAIL'}")
        print(f"Get History: {'PASS' if test12 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test13 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test14 else 'FAIL'}")
        print(f"NavigationMode Enum: {'PASS' if test15 else 'FAIL'}")
        print(f"LinePosition Enum: {'PASS' if test16 else 'FAIL'}")
        print(f"LineInfo Dataclass: {'PASS' if test17 else 'FAIL'}")
        print(f"GoToLineConfig Dataclass: {'PASS' if test18 else 'FAIL'}")
        print(f"GoToLineResult Dataclass: {'PASS' if test19 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14, test15, test16, test17, test18, test19])
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
