"""
Quality Test: Duplicate Line
Duplicate line system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.duplicate_line import (
    DuplicateLineEngine,
    DuplicateScope,
    DuplicatePosition,
    DuplicateRange,
    DuplicateConfig,
    DuplicateResult
)


def test_duplicate_line():
    """
    Test: Duplicate line.
    """
    print("=" * 70)
    print("TEST: Duplicate Line")
    print("=" * 70)
    
    engine = DuplicateLineEngine()
    
    content = "def test():\n    pass\n    return"
    result = engine.duplicate_line(content, 1)
    
    assert result.success, "Çoğaltma başarılı olmalı"
    assert result.lines_duplicated == 1, "1 satır çoğaltılmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Lines duplicated: {result.lines_duplicated}")
    
    print("\n" + "=" * 70)
    print("PASS: Duplicate line")
    print("=" * 70)


def test_duplicate_line_above():
    """
    Test: Duplicate line above.
    """
    print("=" * 70)
    print("TEST: Duplicate Line Above")
    print("=" * 70)
    
    engine = DuplicateLineEngine()
    
    content = "def test():\n    pass\n    return"
    result = engine.duplicate_line(content, 1, position=DuplicatePosition.ABOVE)
    
    assert result.success, "Çoğaltma başarılı olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Duplicate line above")
    print("=" * 70)


def test_duplicate_selection():
    """
    Test: Duplicate selection.
    """
    print("=" * 70)
    print("TEST: Duplicate Selection")
    print("=" * 70)
    
    engine = DuplicateLineEngine()
    
    content = "def test():\n    pass\n    return"
    duplicate_range = DuplicateRange(start_line=0, end_line=2)
    result = engine.duplicate_selection(content, duplicate_range)
    
    assert result.success, "Çoğaltma başarılı olmalı"
    assert result.lines_duplicated == 3, "3 satır çoğaltılmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Lines duplicated: {result.lines_duplicated}")
    
    print("\n" + "=" * 70)
    print("PASS: Duplicate selection")
    print("=" * 70)


def test_duplicate_block():
    """
    Test: Duplicate block.
    """
    print("=" * 70)
    print("TEST: Duplicate Block")
    print("=" * 70)
    
    engine = DuplicateLineEngine()
    
    content = "def test():\n    pass\n    return"
    result = engine.duplicate_block(content, 0, 2)
    
    assert result.success, "Çoğaltma başarılı olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Duplicate block")
    print("=" * 70)


def test_duplicate_function():
    """
    Test: Duplicate function.
    """
    print("=" * 70)
    print("TEST: Duplicate Function")
    print("=" * 70)
    
    engine = DuplicateLineEngine()
    
    content = "def test():\n    pass\n    return\n\ndef test2():\n    pass"
    result = engine.duplicate_function(content, 1)
    
    assert result.success, "Çoğaltma başarılı olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Duplicate function")
    print("=" * 70)


def test_invalid_line_number():
    """
    Test: Invalid line number.
    """
    print("=" * 70)
    print("TEST: Invalid Line Number")
    print("=" * 70)
    
    engine = DuplicateLineEngine()
    
    content = "def test():\n    pass"
    result = engine.duplicate_line(content, 10)
    
    assert result.success == False, "Başarısız olmalı"
    assert len(result.errors) > 0, "Hata olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Errors: {result.errors}")
    
    print("\n" + "=" * 70)
    print("PASS: Invalid line number")
    print("=" * 70)


def test_invalid_range():
    """
    Test: Invalid range.
    """
    print("=" * 70)
    print("TEST: Invalid Range")
    print("=" * 70)
    
    engine = DuplicateLineEngine()
    
    content = "def test():\n    pass"
    duplicate_range = DuplicateRange(start_line=0, end_line=10)
    result = engine.duplicate_selection(content, duplicate_range)
    
    assert result.success == False, "Başarısız olmalı"
    assert len(result.errors) > 0, "Hata olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Errors: {result.errors}")
    
    print("\n" + "=" * 70)
    print("PASS: Invalid range")
    print("=" * 70)


def test_undo_duplicate():
    """
    Test: Undo duplicate.
    """
    print("=" * 70)
    print("TEST: Undo Duplicate")
    print("=" * 70)
    
    engine = DuplicateLineEngine()
    
    content = "def test():\n    pass"
    engine.duplicate_line(content, 1)
    result = engine.undo_duplicate()
    
    assert result.success, "Geri alma başarılı olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Undo duplicate")
    print("=" * 70)


def test_get_duplicate_history():
    """
    Test: Get duplicate history.
    """
    print("=" * 70)
    print("TEST: Get Duplicate History")
    print("=" * 70)
    
    engine = DuplicateLineEngine()
    
    content = "def test():\n    pass"
    engine.duplicate_line(content, 1)
    history = engine.get_duplicate_history()
    
    assert len(history) > 0, "Geçmiş olmalı"
    
    print(f"  History: {len(history)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get duplicate history")
    print("=" * 70)


def test_clear_history():
    """
    Test: Clear history.
    """
    print("=" * 70)
    print("TEST: Clear History")
    print("=" * 70)
    
    engine = DuplicateLineEngine()
    
    content = "def test():\n    pass"
    engine.duplicate_line(content, 1)
    result = engine.clear_history()
    
    assert result.success, "Temizleme başarılı olmalı"
    assert len(engine.get_duplicate_history()) == 0, "Geçmiş temizlenmeli"
    
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
    
    engine = DuplicateLineEngine()
    
    new_config = DuplicateConfig(position=DuplicatePosition.ABOVE)
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
    
    engine = DuplicateLineEngine()
    
    config = engine.get_config()
    
    assert config is not None, "Config olmalı"
    assert config.position == DuplicatePosition.BELOW, "Config eşleşmeli"
    
    print(f"  Position: {config.position.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


def test_duplicate_scope_enum():
    """
    Test: DuplicateScope enum.
    """
    print("=" * 70)
    print("TEST: DuplicateScope Enum")
    print("=" * 70)
    
    assert DuplicateScope.LINE.value == "line"
    assert DuplicateScope.SELECTION.value == "selection"
    assert DuplicateScope.BLOCK.value == "block"
    assert DuplicateScope.FUNCTION.value == "function"
    
    print(f"  All enum values verified")
    print(f"  Total scopes: {len(DuplicateScope)}")
    
    print("\n" + "=" * 70)
    print("PASS: DuplicateScope enum")
    print("=" * 70)


def test_duplicate_position_enum():
    """
    Test: DuplicatePosition enum.
    """
    print("=" * 70)
    print("TEST: DuplicatePosition Enum")
    print("=" * 70)
    
    assert DuplicatePosition.BELOW.value == "below"
    assert DuplicatePosition.ABOVE.value == "above"
    assert DuplicatePosition.CURRENT.value == "current"
    
    print(f"  All enum values verified")
    print(f"  Total positions: {len(DuplicatePosition)}")
    
    print("\n" + "=" * 70)
    print("PASS: DuplicatePosition enum")
    print("=" * 70)


def test_duplicate_range_dataclass():
    """
    Test: DuplicateRange dataclass.
    """
    print("=" * 70)
    print("TEST: DuplicateRange Dataclass")
    print("=" * 70)
    
    duplicate_range = DuplicateRange(
        start_line=0,
        end_line=5,
        start_column=0,
        end_column=10
    )
    
    assert duplicate_range.start_line == 0, "Start line eşleşmeli"
    assert duplicate_range.end_line == 5, "End line eşleşmeli"
    
    print(f"  Start line: {duplicate_range.start_line}")
    print(f"  End line: {duplicate_range.end_line}")
    
    print("\n" + "=" * 70)
    print("PASS: DuplicateRange dataclass")
    print("=" * 70)


def test_duplicate_config_dataclass():
    """
    Test: DuplicateConfig dataclass.
    """
    print("=" * 70)
    print("TEST: DuplicateConfig Dataclass")
    print("=" * 70)
    
    config = DuplicateConfig(
        scope=DuplicateScope.LINE,
        position=DuplicatePosition.BELOW,
        preserve_indentation=True
    )
    
    assert config.scope == DuplicateScope.LINE, "Scope eşleşmeli"
    assert config.position == DuplicatePosition.BELOW, "Position eşleşmeli"
    assert config.preserve_indentation == True, "Preserve indentation eşleşmeli"
    
    print(f"  Scope: {config.scope.value}")
    print(f"  Position: {config.position.value}")
    print(f"  Preserve indentation: {config.preserve_indentation}")
    
    print("\n" + "=" * 70)
    print("PASS: DuplicateConfig dataclass")
    print("=" * 70)


def test_duplicate_result_dataclass():
    """
    Test: DuplicateResult dataclass.
    """
    print("=" * 70)
    print("TEST: DuplicateResult Dataclass")
    print("=" * 70)
    
    result = DuplicateResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: DuplicateResult dataclass")
    print("=" * 70)


def test_find_function_start():
    """
    Test: Find function start.
    """
    print("=" * 70)
    print("TEST: Find Function Start")
    print("=" * 70)
    
    engine = DuplicateLineEngine()
    
    lines = ["def test():", "    pass", "    return"]
    start_line = engine._find_function_start(lines, 1)
    
    assert start_line == 0, "Fonksiyon başlangıcı bulunmalı"
    
    print(f"  Function start: {start_line}")
    
    print("\n" + "=" * 70)
    print("PASS: Find function start")
    print("=" * 70)


def test_find_function_end():
    """
    Test: Find function end.
    """
    print("=" * 70)
    print("TEST: Find Function End")
    print("=" * 70)
    
    engine = DuplicateLineEngine()
    
    lines = ["def test():", "    pass", "    return", ""]
    end_line = engine._find_function_end(lines, 0)
    
    assert end_line >= 0, "Fonksiyon bitişi bulunmalı"
    
    print(f"  Function end: {end_line}")
    
    print("\n" + "=" * 70)
    print("PASS: Find function end")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_duplicate_line()
        test2 = test_duplicate_line_above()
        test3 = test_duplicate_selection()
        test4 = test_duplicate_block()
        test5 = test_duplicate_function()
        test6 = test_invalid_line_number()
        test7 = test_invalid_range()
        test8 = test_undo_duplicate()
        test9 = test_get_duplicate_history()
        test10 = test_clear_history()
        test11 = test_update_config()
        test12 = test_get_config()
        test13 = test_duplicate_scope_enum()
        test14 = test_duplicate_position_enum()
        test15 = test_duplicate_range_dataclass()
        test16 = test_duplicate_config_dataclass()
        test17 = test_duplicate_result_dataclass()
        test18 = test_find_function_start()
        test19 = test_find_function_end()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Duplicate Line: {'PASS' if test1 else 'FAIL'}")
        print(f"Duplicate Line Above: {'PASS' if test2 else 'FAIL'}")
        print(f"Duplicate Selection: {'PASS' if test3 else 'FAIL'}")
        print(f"Duplicate Block: {'PASS' if test4 else 'FAIL'}")
        print(f"Duplicate Function: {'PASS' if test5 else 'FAIL'}")
        print(f"Invalid Line Number: {'PASS' if test6 else 'FAIL'}")
        print(f"Invalid Range: {'PASS' if test7 else 'FAIL'}")
        print(f"Undo Duplicate: {'PASS' if test8 else 'FAIL'}")
        print(f"Get Duplicate History: {'PASS' if test9 else 'FAIL'}")
        print(f"Clear History: {'PASS' if test10 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test11 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test12 else 'FAIL'}")
        print(f"DuplicateScope Enum: {'PASS' if test13 else 'FAIL'}")
        print(f"DuplicatePosition Enum: {'PASS' if test14 else 'FAIL'}")
        print(f"DuplicateRange Dataclass: {'PASS' if test15 else 'FAIL'}")
        print(f"DuplicateConfig Dataclass: {'PASS' if test16 else 'FAIL'}")
        print(f"DuplicateResult Dataclass: {'PASS' if test17 else 'FAIL'}")
        print(f"Find Function Start: {'PASS' if test18 else 'FAIL'}")
        print(f"Find Function End: {'PASS' if test19 else 'FAIL'}")
        
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
