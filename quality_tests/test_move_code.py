"""
Quality Test: Move Code
Move code system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.move_code import (
    MoveCodeEngine,
    MoveDirection,
    MoveScope,
    CodeBlock,
    MoveConfig,
    MoveResult
)


def test_move_up():
    """
    Test: Move up.
    """
    print("=" * 70)
    print("TEST: Move Up")
    print("=" * 70)
    
    engine = MoveCodeEngine()
    
    content = "line1\nline2\nline3"
    result = engine.move_code(content, 1, 1, MoveDirection.UP)
    
    assert result.success, "Taşıma başarılı olmalı"
    assert result.lines_moved > 0, "Satır taşınmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Lines moved: {result.lines_moved}")
    
    print("\n" + "=" * 70)
    print("PASS: Move up")
    print("=" * 70)


def test_move_down():
    """
    Test: Move down.
    """
    print("=" * 70)
    print("TEST: Move Down")
    print("=" * 70)
    
    engine = MoveCodeEngine()
    
    content = "line1\nline2\nline3"
    result = engine.move_code(content, 1, 1, MoveDirection.DOWN)
    
    assert result.success, "Taşıma başarılı olmalı"
    assert result.lines_moved > 0, "Satır taşınmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Lines moved: {result.lines_moved}")
    
    print("\n" + "=" * 70)
    print("PASS: Move down")
    print("=" * 70)


def test_move_left():
    """
    Test: Move left.
    """
    print("=" * 70)
    print("TEST: Move Left")
    print("=" * 70)
    
    engine = MoveCodeEngine()
    
    content = "    line1\n    line2\n    line3"
    result = engine.move_code(content, 1, 1, MoveDirection.LEFT)
    
    assert result.success, "Taşıma başarılı olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Move left")
    print("=" * 70)


def test_move_right():
    """
    Test: Move right.
    """
    print("=" * 70)
    print("TEST: Move Right")
    print("=" * 70)
    
    engine = MoveCodeEngine()
    
    content = "line1\nline2\nline3"
    result = engine.move_code(content, 1, 1, MoveDirection.RIGHT)
    
    assert result.success, "Taşıma başarılı olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Move right")
    print("=" * 70)


def test_move_multiple_steps():
    """
    Test: Move multiple steps.
    """
    print("=" * 70)
    print("TEST: Move Multiple Steps")
    print("=" * 70)
    
    engine = MoveCodeEngine()
    
    content = "line1\nline2\nline3\nline4"
    result = engine.move_code(content, 2, 2, MoveDirection.UP, steps=2)
    
    assert result.success, "Taşıma başarılı olmalı"
    assert result.lines_moved == 2, "2 satır taşınmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Lines moved: {result.lines_moved}")
    
    print("\n" + "=" * 70)
    print("PASS: Move multiple steps")
    print("=" * 70)


def test_move_block():
    """
    Test: Move block.
    """
    print("=" * 70)
    print("TEST: Move Block")
    print("=" * 70)
    
    engine = MoveCodeEngine()
    
    content = "line1\nline2\nline3\nline4"
    result = engine.move_code(content, 1, 2, MoveDirection.DOWN)
    
    assert result.success, "Taşıma başarılı olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Move block")
    print("=" * 70)


def test_move_invalid_range():
    """
    Test: Move invalid range.
    """
    print("=" * 70)
    print("TEST: Move Invalid Range")
    print("=" * 70)
    
    engine = MoveCodeEngine()
    
    content = "line1\nline2\nline3"
    result = engine.move_code(content, 10, 15, MoveDirection.DOWN)
    
    assert result.success == False, "Başarısız olmalı"
    assert len(result.errors) > 0, "Hata olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Errors: {result.errors}")
    
    print("\n" + "=" * 70)
    print("PASS: Move invalid range")
    print("=" * 70)


def test_move_empty_content():
    """
    Test: Move empty content.
    """
    print("=" * 70)
    print("TEST: Move Empty Content")
    print("=" * 70)
    
    engine = MoveCodeEngine()
    
    content = ""
    result = engine.move_code(content, 0, 0, MoveDirection.DOWN)
    
    assert result.success == False, "Başarısız olmalı"
    assert len(result.errors) > 0, "Hata olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Errors: {result.errors}")
    
    print("\n" + "=" * 70)
    print("PASS: Move empty content")
    print("=" * 70)


def test_undo_move():
    """
    Test: Undo move.
    """
    print("=" * 70)
    print("TEST: Undo Move")
    print("=" * 70)
    
    engine = MoveCodeEngine()
    
    content = "line1\nline2\nline3"
    engine.move_code(content, 1, 1, MoveDirection.DOWN)
    result = engine.undo_move()
    
    assert result.success, "Geri alma başarılı olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Undo move")
    print("=" * 70)


def test_get_move_history():
    """
    Test: Get move history.
    """
    print("=" * 70)
    print("TEST: Get Move History")
    print("=" * 70)
    
    engine = MoveCodeEngine()
    
    engine.move_code("line1\nline2\nline3", 1, 1, MoveDirection.DOWN)
    history = engine.get_move_history()
    
    assert len(history) > 0, "Geçmiş olmalı"
    
    print(f"  History: {len(history)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get move history")
    print("=" * 70)


def test_clear_history():
    """
    Test: Clear history.
    """
    print("=" * 70)
    print("TEST: Clear History")
    print("=" * 70)
    
    engine = MoveCodeEngine()
    
    engine.move_code("line1\nline2\nline3", 1, 1, MoveDirection.DOWN)
    result = engine.clear_history()
    
    assert result.success, "Temizleme başarılı olmalı"
    assert len(engine.get_move_history()) == 0, "Geçmiş temizlenmeli"
    
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
    
    engine = MoveCodeEngine()
    
    new_config = MoveConfig(preserve_indentation=False)
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
    
    engine = MoveCodeEngine()
    
    config = engine.get_config()
    
    assert config is not None, "Config olmalı"
    assert config.preserve_indentation == True, "Config eşleşmeli"
    
    print(f"  Preserve indentation: {config.preserve_indentation}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


def test_move_direction_enum():
    """
    Test: MoveDirection enum.
    """
    print("=" * 70)
    print("TEST: MoveDirection Enum")
    print("=" * 70)
    
    assert MoveDirection.UP.value == "up"
    assert MoveDirection.DOWN.value == "down"
    assert MoveDirection.LEFT.value == "left"
    assert MoveDirection.RIGHT.value == "right"
    
    print(f"  All enum values verified")
    print(f"  Total directions: {len(MoveDirection)}")
    
    print("\n" + "=" * 70)
    print("PASS: MoveDirection enum")
    print("=" * 70)


def test_move_scope_enum():
    """
    Test: MoveScope enum.
    """
    print("=" * 70)
    print("TEST: MoveScope Enum")
    print("=" * 70)
    
    assert MoveScope.LINE.value == "line"
    assert MoveScope.SELECTION.value == "selection"
    assert MoveScope.BLOCK.value == "block"
    assert MoveScope.FUNCTION.value == "function"
    
    print(f"  All enum values verified")
    print(f"  Total scopes: {len(MoveScope)}")
    
    print("\n" + "=" * 70)
    print("PASS: MoveScope enum")
    print("=" * 70)


def test_code_block_dataclass():
    """
    Test: CodeBlock dataclass.
    """
    print("=" * 70)
    print("TEST: CodeBlock Dataclass")
    print("=" * 70)
    
    code_block = CodeBlock(
        start_line=0,
        end_line=2,
        content="line1\nline2\nline3"
    )
    
    assert code_block.start_line == 0, "Start line eşleşmeli"
    assert code_block.end_line == 2, "End line eşleşmeli"
    
    print(f"  Start line: {code_block.start_line}")
    print(f"  End line: {code_block.end_line}")
    
    print("\n" + "=" * 70)
    print("PASS: CodeBlock dataclass")
    print("=" * 70)


def test_move_config_dataclass():
    """
    Test: MoveConfig dataclass.
    """
    print("=" * 70)
    print("TEST: MoveConfig Dataclass")
    print("=" * 70)
    
    config = MoveConfig(
        preserve_indentation=True,
        auto_indent=True,
        verify_syntax=True
    )
    
    assert config.preserve_indentation == True, "Preserve indentation eşleşmeli"
    assert config.auto_indent == True, "Auto indent eşleşmeli"
    assert config.verify_syntax == True, "Verify syntax eşleşmeli"
    
    print(f"  Preserve indentation: {config.preserve_indentation}")
    print(f"  Auto indent: {config.auto_indent}")
    print(f"  Verify syntax: {config.verify_syntax}")
    
    print("\n" + "=" * 70)
    print("PASS: MoveConfig dataclass")
    print("=" * 70)


def test_move_result_dataclass():
    """
    Test: MoveResult dataclass.
    """
    print("=" * 70)
    print("TEST: MoveResult Dataclass")
    print("=" * 70)
    
    result = MoveResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: MoveResult dataclass")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_move_up()
        test2 = test_move_down()
        test3 = test_move_left()
        test4 = test_move_right()
        test5 = test_move_multiple_steps()
        test6 = test_move_block()
        test7 = test_move_invalid_range()
        test8 = test_move_empty_content()
        test9 = test_undo_move()
        test10 = test_get_move_history()
        test11 = test_clear_history()
        test12 = test_update_config()
        test13 = test_get_config()
        test14 = test_move_direction_enum()
        test15 = test_move_scope_enum()
        test16 = test_code_block_dataclass()
        test17 = test_move_config_dataclass()
        test18 = test_move_result_dataclass()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Move Up: {'PASS' if test1 else 'FAIL'}")
        print(f"Move Down: {'PASS' if test2 else 'FAIL'}")
        print(f"Move Left: {'PASS' if test3 else 'FAIL'}")
        print(f"Move Right: {'PASS' if test4 else 'FAIL'}")
        print(f"Move Multiple Steps: {'PASS' if test5 else 'FAIL'}")
        print(f"Move Block: {'PASS' if test6 else 'FAIL'}")
        print(f"Move Invalid Range: {'PASS' if test7 else 'FAIL'}")
        print(f"Move Empty Content: {'PASS' if test8 else 'FAIL'}")
        print(f"Undo Move: {'PASS' if test9 else 'FAIL'}")
        print(f"Get Move History: {'PASS' if test10 else 'FAIL'}")
        print(f"Clear History: {'PASS' if test11 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test12 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test13 else 'FAIL'}")
        print(f"MoveDirection Enum: {'PASS' if test14 else 'FAIL'}")
        print(f"MoveScope Enum: {'PASS' if test15 else 'FAIL'}")
        print(f"CodeBlock Dataclass: {'PASS' if test16 else 'FAIL'}")
        print(f"MoveConfig Dataclass: {'PASS' if test17 else 'FAIL'}")
        print(f"MoveResult Dataclass: {'PASS' if test18 else 'FAIL'}")
        
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
