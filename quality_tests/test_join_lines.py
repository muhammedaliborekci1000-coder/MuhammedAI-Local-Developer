"""
Quality Test: Join Lines
Join lines system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.join_lines import (
    JoinLinesEngine,
    JoinMode,
    JoinScope,
    JoinRange,
    JoinConfig,
    JoinResult
)


def test_join_lines():
    """
    Test: Join lines.
    """
    print("=" * 70)
    print("TEST: Join Lines")
    print("=" * 70)
    
    engine = JoinLinesEngine()
    
    content = "line1\nline2\nline3"
    result = engine.join_lines(content)
    
    assert result.success, "Birleştirme başarılı olmalı"
    assert "\n" not in result.modified_content, "Satırlar birleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Modified: {result.modified_content}")
    
    print("\n" + "=" * 70)
    print("PASS: Join lines")
    print("=" * 70)


def test_join_with_space():
    """
    Test: Join with space.
    """
    print("=" * 70)
    print("TEST: Join with Space")
    print("=" * 70)
    
    engine = JoinLinesEngine()
    
    content = "line1\nline2\nline3"
    result = engine.join_with_space(content)
    
    assert result.success, "Birleştirme başarılı olmalı"
    assert " " in result.modified_content, "Space olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Modified: {result.modified_content}")
    
    print("\n" + "=" * 70)
    print("PASS: Join with space")
    print("=" * 70)


def test_join_without_space():
    """
    Test: Join without space.
    """
    print("=" * 70)
    print("TEST: Join without Space")
    print("=" * 70)
    
    engine = JoinLinesEngine()
    
    content = "line1\nline2\nline3"
    result = engine.join_without_space(content)
    
    assert result.success, "Birleştirme başarılı olmalı"
    assert " " not in result.modified_content, "Space olmamalı"
    
    print(f"  Success: {result.success}")
    print(f"  Modified: {result.modified_content}")
    
    print("\n" + "=" * 70)
    print("PASS: Join without space")
    print("=" * 70)


def test_join_with_semicolon():
    """
    Test: Join with semicolon.
    """
    print("=" * 70)
    print("TEST: Join with Semicolon")
    print("=" * 70)
    
    engine = JoinLinesEngine()
    
    content = "line1\nline2\nline3"
    result = engine.join_with_semicolon(content)
    
    assert result.success, "Birleştirme başarılı olmalı"
    assert ";" in result.modified_content, "Semicolon olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Modified: {result.modified_content}")
    
    print("\n" + "=" * 70)
    print("PASS: Join with semicolon")
    print("=" * 70)


def test_join_with_comma():
    """
    Test: Join with comma.
    """
    print("=" * 70)
    print("TEST: Join with Comma")
    print("=" * 70)
    
    engine = JoinLinesEngine()
    
    content = "line1\nline2\nline3"
    result = engine.join_with_comma(content)
    
    assert result.success, "Birleştirme başarılı olmalı"
    assert "," in result.modified_content, "Comma olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Modified: {result.modified_content}")
    
    print("\n" + "=" * 70)
    print("PASS: Join with comma")
    print("=" * 70)


def test_join_selection():
    """
    Test: Join selection.
    """
    print("=" * 70)
    print("TEST: Join Selection")
    print("=" * 70)
    
    config = JoinConfig(scope=JoinScope.SELECTION)
    engine = JoinLinesEngine(config)
    
    content = "line1\nline2\nline3"
    join_range = JoinRange(start_line=0, end_line=1)
    result = engine.join_lines(content, join_range)
    
    assert result.success, "Birleştirme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Modified: {result.modified_content}")
    
    print("\n" + "=" * 70)
    print("PASS: Join selection")
    print("=" * 70)


def test_join_line():
    """
    Test: Join line.
    """
    print("=" * 70)
    print("TEST: Join Line")
    print("=" * 70)
    
    config = JoinConfig(scope=JoinScope.LINE)
    engine = JoinLinesEngine(config)
    
    content = "line1\nline2\nline3"
    join_range = JoinRange(start_line=0, end_line=0)
    result = engine.join_lines(content, join_range)
    
    assert result.success, "Birleştirme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Modified: {result.modified_content}")
    
    print("\n" + "=" * 70)
    print("PASS: Join line")
    print("=" * 70)


def test_join_document():
    """
    Test: Join document.
    """
    print("=" * 70)
    print("TEST: Join Document")
    print("=" * 70)
    
    config = JoinConfig(scope=JoinScope.DOCUMENT)
    engine = JoinLinesEngine(config)
    
    content = "line1\nline2\nline3"
    result = engine.join_lines(content)
    
    assert result.success, "Birleştirme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Modified: {result.modified_content}")
    
    print("\n" + "=" * 70)
    print("PASS: Join document")
    print("=" * 70)


def test_undo_join():
    """
    Test: Undo join.
    """
    print("=" * 70)
    print("TEST: Undo Join")
    print("=" * 70)
    
    engine = JoinLinesEngine()
    
    content = "line1\nline2\nline3"
    engine.join_lines(content)
    result = engine.undo_join()
    
    assert result.success, "Geri alma başarılı olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Undo join")
    print("=" * 70)


def test_get_join_history():
    """
    Test: Get join history.
    """
    print("=" * 70)
    print("TEST: Get Join History")
    print("=" * 70)
    
    engine = JoinLinesEngine()
    
    content = "line1\nline2\nline3"
    engine.join_lines(content)
    history = engine.get_join_history()
    
    assert len(history) > 0, "Geçmiş olmalı"
    
    print(f"  History: {len(history)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get join history")
    print("=" * 70)


def test_clear_history():
    """
    Test: Clear history.
    """
    print("=" * 70)
    print("TEST: Clear History")
    print("=" * 70)
    
    engine = JoinLinesEngine()
    
    content = "line1\nline2\nline3"
    engine.join_lines(content)
    result = engine.clear_history()
    
    assert result.success, "Temizleme başarılı olmalı"
    assert len(engine.get_join_history()) == 0, "Geçmiş temizlenmeli"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear history")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    engine = JoinLinesEngine()
    
    new_config = JoinConfig(mode=JoinMode.COMMA)
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
    
    engine = JoinLinesEngine()
    
    config = engine.get_config()
    
    assert config is not None, "Config olmalı"
    assert config.mode == JoinMode.SPACE, "Config eşleşmeli"
    
    print(f"  Mode: {config.mode.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


def test_join_mode_enum():
    """
    Test: JoinMode enum.
    """
    print("=" * 70)
    print("TEST: JoinMode Enum")
    print("=" * 70)
    
    assert JoinMode.SPACE.value == "space"
    assert JoinMode.NO_SPACE.value == "no_space"
    assert JoinMode.NEWLINE.value == "newline"
    assert JoinMode.SEMICOLON.value == "semicolon"
    assert JoinMode.COMMA.value == "comma"
    
    print(f"  All enum values verified")
    print(f"  Total modes: {len(JoinMode)}")
    
    print("\n" + "=" * 70)
    print("PASS: JoinMode enum")
    print("=" * 70)


def test_join_scope_enum():
    """
    Test: JoinScope enum.
    """
    print("=" * 70)
    print("TEST: JoinScope Enum")
    print("=" * 70)
    
    assert JoinScope.LINE.value == "line"
    assert JoinScope.SELECTION.value == "selection"
    assert JoinScope.DOCUMENT.value == "document"
    
    print(f"  All enum values verified")
    print(f"  Total scopes: {len(JoinScope)}")
    
    print("\n" + "=" * 70)
    print("PASS: JoinScope enum")
    print("=" * 70)


def test_join_range_dataclass():
    """
    Test: JoinRange dataclass.
    """
    print("=" * 70)
    print("TEST: JoinRange Dataclass")
    print("=" * 70)
    
    join_range = JoinRange(
        start_line=0,
        end_line=5,
        start_column=0,
        end_column=10
    )
    
    assert join_range.start_line == 0, "Start line eşleşmeli"
    assert join_range.end_line == 5, "End line eşleşmeli"
    
    print(f"  Start line: {join_range.start_line}")
    print(f"  End line: {join_range.end_line}")
    
    print("\n" + "=" * 70)
    print("PASS: JoinRange dataclass")
    print("=" * 70)


def test_join_config_dataclass():
    """
    Test: JoinConfig dataclass.
    """
    print("=" * 70)
    print("TEST: JoinConfig Dataclass")
    print("=" * 70)
    
    config = JoinConfig(
        mode=JoinMode.SPACE,
        scope=JoinScope.SELECTION,
        trim_whitespace=True
    )
    
    assert config.mode == JoinMode.SPACE, "Mode eşleşmeli"
    assert config.scope == JoinScope.SELECTION, "Scope eşleşmeli"
    assert config.trim_whitespace == True, "Trim whitespace eşleşmeli"
    
    print(f"  Mode: {config.mode.value}")
    print(f"  Scope: {config.scope.value}")
    print(f"  Trim whitespace: {config.trim_whitespace}")
    
    print("\n" + "=" * 70)
    print("PASS: JoinConfig dataclass")
    print("=" * 70)


def test_join_result_dataclass():
    """
    Test: JoinResult dataclass.
    """
    print("=" * 70)
    print("TEST: JoinResult Dataclass")
    print("=" * 70)
    
    result = JoinResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: JoinResult dataclass")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_join_lines()
        test2 = test_join_with_space()
        test3 = test_join_without_space()
        test4 = test_join_with_semicolon()
        test5 = test_join_with_comma()
        test6 = test_join_selection()
        test7 = test_join_line()
        test8 = test_join_document()
        test9 = test_undo_join()
        test10 = test_get_join_history()
        test11 = test_clear_history()
        test12 = test_update_config()
        test13 = test_get_config()
        test14 = test_join_mode_enum()
        test15 = test_join_scope_enum()
        test16 = test_join_range_dataclass()
        test17 = test_join_config_dataclass()
        test18 = test_join_result_dataclass()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Join Lines: {'PASS' if test1 else 'FAIL'}")
        print(f"Join with Space: {'PASS' if test2 else 'FAIL'}")
        print(f"Join without Space: {'PASS' if test3 else 'FAIL'}")
        print(f"Join with Semicolon: {'PASS' if test4 else 'FAIL'}")
        print(f"Join with Comma: {'PASS' if test5 else 'FAIL'}")
        print(f"Join Selection: {'PASS' if test6 else 'FAIL'}")
        print(f"Join Line: {'PASS' if test7 else 'FAIL'}")
        print(f"Join Document: {'PASS' if test8 else 'FAIL'}")
        print(f"Undo Join: {'PASS' if test9 else 'FAIL'}")
        print(f"Get Join History: {'PASS' if test10 else 'FAIL'}")
        print(f"Clear History: {'PASS' if test11 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test12 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test13 else 'FAIL'}")
        print(f"JoinMode Enum: {'PASS' if test14 else 'FAIL'}")
        print(f"JoinScope Enum: {'PASS' if test15 else 'FAIL'}")
        print(f"JoinRange Dataclass: {'PASS' if test16 else 'FAIL'}")
        print(f"JoinConfig Dataclass: {'PASS' if test17 else 'FAIL'}")
        print(f"JoinResult Dataclass: {'PASS' if test18 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14, test15, test16, test17, test18])
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
