"""
Quality Test: Delete Line
Delete line system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.delete_line import (
    DeleteLineEngine,
    DeleteScope,
    DeleteMode,
    DeleteRange,
    DeleteConfig,
    DeleteResult
)


def test_delete_line():
    """
    Test: Delete line.
    """
    print("=" * 70)
    print("TEST: Delete Line")
    print("=" * 70)
    
    engine = DeleteLineEngine()
    
    content = "def test():\n    pass\n    return"
    result = engine.delete_line(content, 1)
    
    assert result.success, "Silme başarılı olmalı"
    assert result.lines_deleted == 1, "1 satır silinmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Lines deleted: {result.lines_deleted}")
    
    print("\n" + "=" * 70)
    print("PASS: Delete line")
    print("=" * 70)


def test_delete_selection():
    """
    Test: Delete selection.
    """
    print("=" * 70)
    print("TEST: Delete Selection")
    print("=" * 70)
    
    engine = DeleteLineEngine()
    
    content = "def test():\n    pass\n    return"
    delete_range = DeleteRange(start_line=0, end_line=2)
    result = engine.delete_selection(content, delete_range)
    
    assert result.success, "Silme başarılı olmalı"
    assert result.lines_deleted == 3, "3 satır silinmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Lines deleted: {result.lines_deleted}")
    
    print("\n" + "=" * 70)
    print("PASS: Delete selection")
    print("=" * 70)


def test_delete_block():
    """
    Test: Delete block.
    """
    print("=" * 70)
    print("TEST: Delete Block")
    print("=" * 70)
    
    engine = DeleteLineEngine()
    
    content = "def test():\n    pass\n    return"
    result = engine.delete_block(content, 0, 2)
    
    assert result.success, "Silme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Delete block")
    print("=" * 70)


def test_delete_function():
    """
    Test: Delete function.
    """
    print("=" * 70)
    print("TEST: Delete Function")
    print("=" * 70)
    
    engine = DeleteLineEngine()
    
    content = "def test():\n    pass\n    return\n\ndef test2():\n    pass"
    result = engine.delete_function(content, 1)
    
    assert result.success, "Silme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Delete function")
    print("=" * 70)


def test_delete_word():
    """
    Test: Delete word.
    """
    print("=" * 70)
    print("TEST: Delete Word")
    print("=" * 70)
    
    engine = DeleteLineEngine()
    
    content = "x = 10 + 20"
    result = engine.delete_word(content, 0, 2)
    
    assert result.success, "Silme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Delete word")
    print("=" * 70)


def test_invalid_line_number():
    """
    Test: Invalid line number.
    """
    print("=" * 70)
    print("TEST: Invalid Line Number")
    print("=" * 70)
    
    engine = DeleteLineEngine()
    
    content = "def test():\n    pass"
    result = engine.delete_line(content, 10)
    
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
    
    engine = DeleteLineEngine()
    
    content = "def test():\n    pass"
    delete_range = DeleteRange(start_line=0, end_line=10)
    result = engine.delete_selection(content, delete_range)
    
    assert result.success == False, "Başarısız olmalı"
    assert len(result.errors) > 0, "Hata olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Errors: {result.errors}")
    
    print("\n" + "=" * 70)
    print("PASS: Invalid range")
    print("=" * 70)


def test_invalid_column():
    """
    Test: Invalid column.
    """
    print("=" * 70)
    print("TEST: Invalid Column")
    print("=" * 70)
    
    engine = DeleteLineEngine()
    
    content = "def test():\n    pass"
    result = engine.delete_word(content, 0, 100)
    
    assert result.success == False, "Başarısız olmalı"
    assert len(result.errors) > 0, "Hata olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Errors: {result.errors}")
    
    print("\n" + "=" * 70)
    print("PASS: Invalid column")
    print("=" * 70)


def test_undo_delete():
    """
    Test: Undo delete.
    """
    print("=" * 70)
    print("TEST: Undo Delete")
    print("=" * 70)
    
    engine = DeleteLineEngine()
    
    content = "def test():\n    pass"
    engine.delete_line(content, 1)
    result = engine.undo_delete()
    
    assert result.success, "Geri alma başarılı olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Undo delete")
    print("=" * 70)


def test_get_delete_history():
    """
    Test: Get delete history.
    """
    print("=" * 70)
    print("TEST: Get Delete History")
    print("=" * 70)
    
    engine = DeleteLineEngine()
    
    content = "def test():\n    pass"
    engine.delete_line(content, 1)
    history = engine.get_delete_history()
    
    assert len(history) > 0, "Geçmiş olmalı"
    
    print(f"  History: {len(history)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get delete history")
    print("=" * 70)


def test_clear_history():
    """
    Test: Clear history.
    """
    print("=" * 70)
    print("TEST: Clear History")
    print("=" * 70)
    
    engine = DeleteLineEngine()
    
    content = "def test():\n    pass"
    engine.delete_line(content, 1)
    result = engine.clear_history()
    
    assert result.success, "Temizleme başarılı olmalı"
    assert len(engine.get_delete_history()) == 0, "Geçmiş temizlenmeli"
    
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
    
    engine = DeleteLineEngine()
    
    new_config = DeleteConfig(mode=DeleteMode.MULTIPLE)
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
    
    engine = DeleteLineEngine()
    
    config = engine.get_config()
    
    assert config is not None, "Config olmalı"
    assert config.mode == DeleteMode.SINGLE, "Config eşleşmeli"
    
    print(f"  Mode: {config.mode.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


def test_delete_scope_enum():
    """
    Test: DeleteScope enum.
    """
    print("=" * 70)
    print("TEST: DeleteScope Enum")
    print("=" * 70)
    
    assert DeleteScope.LINE.value == "line"
    assert DeleteScope.SELECTION.value == "selection"
    assert DeleteScope.BLOCK.value == "block"
    assert DeleteScope.FUNCTION.value == "function"
    assert DeleteScope.WORD.value == "word"
    
    print(f"  All enum values verified")
    print(f"  Total scopes: {len(DeleteScope)}")
    
    print("\n" + "=" * 70)
    print("PASS: DeleteScope enum")
    print("=" * 70)


def test_delete_mode_enum():
    """
    Test: DeleteMode enum.
    """
    print("=" * 70)
    print("TEST: DeleteMode Enum")
    print("=" * 70)
    
    assert DeleteMode.SINGLE.value == "single"
    assert DeleteMode.MULTIPLE.value == "multiple"
    assert DeleteMode.ALL.value == "all"
    assert DeleteMode.SMART.value == "smart"
    
    print(f"  All enum values verified")
    print(f"  Total modes: {len(DeleteMode)}")
    
    print("\n" + "=" * 70)
    print("PASS: DeleteMode enum")
    print("=" * 70)


def test_delete_range_dataclass():
    """
    Test: DeleteRange dataclass.
    """
    print("=" * 70)
    print("TEST: DeleteRange Dataclass")
    print("=" * 70)
    
    delete_range = DeleteRange(
        start_line=0,
        end_line=5,
        start_column=0,
        end_column=10
    )
    
    assert delete_range.start_line == 0, "Start line eşleşmeli"
    assert delete_range.end_line == 5, "End line eşleşmeli"
    
    print(f"  Start line: {delete_range.start_line}")
    print(f"  End line: {delete_range.end_line}")
    
    print("\n" + "=" * 70)
    print("PASS: DeleteRange dataclass")
    print("=" * 70)


def test_delete_config_dataclass():
    """
    Test: DeleteConfig dataclass.
    """
    print("=" * 70)
    print("TEST: DeleteConfig Dataclass")
    print("=" * 70)
    
    config = DeleteConfig(
        scope=DeleteScope.LINE,
        mode=DeleteMode.SINGLE,
        preserve_empty_lines=False
    )
    
    assert config.scope == DeleteScope.LINE, "Scope eşleşmeli"
    assert config.mode == DeleteMode.SINGLE, "Mode eşleşmeli"
    assert config.preserve_empty_lines == False, "Preserve empty lines eşleşmeli"
    
    print(f"  Scope: {config.scope.value}")
    print(f"  Mode: {config.mode.value}")
    print(f"  Preserve empty lines: {config.preserve_empty_lines}")
    
    print("\n" + "=" * 70)
    print("PASS: DeleteConfig dataclass")
    print("=" * 70)


def test_delete_result_dataclass():
    """
    Test: DeleteResult dataclass.
    """
    print("=" * 70)
    print("TEST: DeleteResult Dataclass")
    print("=" * 70)
    
    result = DeleteResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: DeleteResult dataclass")
    print("=" * 70)


def test_find_word_start():
    """
    Test: Find word start.
    """
    print("=" * 70)
    print("TEST: Find Word Start")
    print("=" * 70)
    
    engine = DeleteLineEngine()
    
    line = "x = 10 + 20"
    start = engine._find_word_start(line, 4)
    
    assert start >= 0, "Kelime başlangıcı bulunmalı"
    
    print(f"  Word start: {start}")
    
    print("\n" + "=" * 70)
    print("PASS: Find word start")
    print("=" * 70)


def test_find_word_end():
    """
    Test: Find word end.
    """
    print("=" * 70)
    print("TEST: Find Word End")
    print("=" * 70)
    
    engine = DeleteLineEngine()
    
    line = "x = 10 + 20"
    end = engine._find_word_end(line, 4)
    
    assert end >= 0, "Kelime bitişi bulunmalı"
    
    print(f"  Word end: {end}")
    
    print("\n" + "=" * 70)
    print("PASS: Find word end")
    print("=" * 70)


def test_find_function_start():
    """
    Test: Find function start.
    """
    print("=" * 70)
    print("TEST: Find Function Start")
    print("=" * 70)
    
    engine = DeleteLineEngine()
    
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
    
    engine = DeleteLineEngine()
    
    lines = ["def test():", "    pass", "    return", ""]
    end_line = engine._find_function_end(lines, 0)
    
    assert end_line >= 0, "Fonksiyon bitişi bulunmalı"
    
    print(f"  Function end: {end_line}")
    
    print("\n" + "=" * 70)
    print("PASS: Find function end")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_delete_line()
        test2 = test_delete_selection()
        test3 = test_delete_block()
        test4 = test_delete_function()
        test5 = test_delete_word()
        test6 = test_invalid_line_number()
        test7 = test_invalid_range()
        test8 = test_invalid_column()
        test9 = test_undo_delete()
        test10 = test_get_delete_history()
        test11 = test_clear_history()
        test12 = test_update_config()
        test13 = test_get_config()
        test14 = test_delete_scope_enum()
        test15 = test_delete_mode_enum()
        test16 = test_delete_range_dataclass()
        test17 = test_delete_config_dataclass()
        test18 = test_delete_result_dataclass()
        test19 = test_find_word_start()
        test20 = test_find_word_end()
        test21 = test_find_function_start()
        test22 = test_find_function_end()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Delete Line: {'PASS' if test1 else 'FAIL'}")
        print(f"Delete Selection: {'PASS' if test2 else 'FAIL'}")
        print(f"Delete Block: {'PASS' if test3 else 'FAIL'}")
        print(f"Delete Function: {'PASS' if test4 else 'FAIL'}")
        print(f"Delete Word: {'PASS' if test5 else 'FAIL'}")
        print(f"Invalid Line Number: {'PASS' if test6 else 'FAIL'}")
        print(f"Invalid Range: {'PASS' if test7 else 'FAIL'}")
        print(f"Invalid Column: {'PASS' if test8 else 'FAIL'}")
        print(f"Undo Delete: {'PASS' if test9 else 'FAIL'}")
        print(f"Get Delete History: {'PASS' if test10 else 'FAIL'}")
        print(f"Clear History: {'PASS' if test11 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test12 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test13 else 'FAIL'}")
        print(f"DeleteScope Enum: {'PASS' if test14 else 'FAIL'}")
        print(f"DeleteMode Enum: {'PASS' if test15 else 'FAIL'}")
        print(f"DeleteRange Dataclass: {'PASS' if test16 else 'FAIL'}")
        print(f"DeleteConfig Dataclass: {'PASS' if test17 else 'FAIL'}")
        print(f"DeleteResult Dataclass: {'PASS' if test18 else 'FAIL'}")
        print(f"Find Word Start: {'PASS' if test19 else 'FAIL'}")
        print(f"Find Word End: {'PASS' if test20 else 'FAIL'}")
        print(f"Find Function Start: {'PASS' if test21 else 'FAIL'}")
        print(f"Find Function End: {'PASS' if test22 else 'FAIL'}")
        
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
