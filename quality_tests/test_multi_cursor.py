"""
Quality Test: Multi-Cursor Editing
Multi-cursor editing system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.multi_cursor import (
    MultiCursorEngine,
    CursorAction,
    CursorMode,
    CursorPosition,
    CursorSelection,
    MultiCursorEdit,
    MultiCursorResult
)


def test_add_cursor():
    """
    Test: Add cursor.
    """
    print("=" * 70)
    print("TEST: Add Cursor")
    print("=" * 70)
    
    engine = MultiCursorEngine()
    
    result = engine.add_cursor(0, 0, is_primary=True)
    
    assert result.success, "Ekleme başarılı olmalı"
    assert len(result.cursors) > 0, "Cursor eklenmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Cursors: {len(result.cursors)}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add cursor")
    print("=" * 70)


def test_remove_cursor():
    """
    Test: Remove cursor.
    """
    print("=" * 70)
    print("TEST: Remove Cursor")
    print("=" * 70)
    
    engine = MultiCursorEngine()
    engine.add_cursor(0, 0)
    
    result = engine.remove_cursor(0)
    
    assert result.success, "Kaldırma başarılı olmalı"
    assert len(result.cursors) == 0, "Cursor kaldırılmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Cursors: {len(result.cursors)}")
    
    print("\n" + "=" * 70)
    print("PASS: Remove cursor")
    print("=" * 70)


def test_clear_cursors():
    """
    Test: Clear cursors.
    """
    print("=" * 70)
    print("TEST: Clear Cursors")
    print("=" * 70)
    
    engine = MultiCursorEngine()
    engine.add_cursor(0, 0)
    engine.add_cursor(1, 0)
    
    result = engine.clear_cursors()
    
    assert result.success, "Temizleme başarılı olmalı"
    assert len(result.cursors) == 0, "Cursor'lar temizlenmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Cursors: {len(result.cursors)}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear cursors")
    print("=" * 70)


def test_move_cursor():
    """
    Test: Move cursor.
    """
    print("=" * 70)
    print("TEST: Move Cursor")
    print("=" * 70)
    
    engine = MultiCursorEngine()
    engine.add_cursor(0, 0)
    
    result = engine.move_cursor(0, 5, 10)
    
    assert result.success, "Taşıma başarılı olmalı"
    assert engine.cursors[0].line == 5, "Satır güncellenmeli"
    assert engine.cursors[0].column == 10, "Sütun güncellenmeli"
    
    print(f"  Success: {result.success}")
    print(f"  New position: ({engine.cursors[0].line}, {engine.cursors[0].column})")
    
    print("\n" + "=" * 70)
    print("PASS: Move cursor")
    print("=" * 70)


def test_edit_at_cursors():
    """
    Test: Edit at cursors.
    """
    print("=" * 70)
    print("TEST: Edit At Cursors")
    print("=" * 70)
    
    engine = MultiCursorEngine()
    engine.add_cursor(0, 0, is_primary=True)
    engine.add_cursor(1, 0)
    
    code = "line1\nline2"
    result = engine.edit_at_cursors(code, "test_")
    
    assert result.success, "Düzenleme başarılı olmalı"
    assert result.edited_code is not None, "Kod düzenlenmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Edited code: {result.edited_code}")
    print(f"  Edits: {len(result.edits)}")
    
    print("\n" + "=" * 70)
    print("PASS: Edit at cursors")
    print("=" * 70)


def test_clone_cursors_down():
    """
    Test: Clone cursors down.
    """
    print("=" * 70)
    print("TEST: Clone Cursors Down")
    print("=" * 70)
    
    engine = MultiCursorEngine()
    engine.add_cursor(0, 0, is_primary=True)
    
    code = "line1\nline2\nline3"
    result = engine.clone_cursors_down(code)
    
    assert result.success, "Klonlama başarılı olmalı"
    assert len(result.cursors) > 1, "Cursor'lar klonlanmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Cursors: {len(result.cursors)}")
    
    print("\n" + "=" * 70)
    print("PASS: Clone cursors down")
    print("=" * 70)


def test_clone_cursors_up():
    """
    Test: Clone cursors up.
    """
    print("=" * 70)
    print("TEST: Clone Cursors Up")
    print("=" * 70)
    
    engine = MultiCursorEngine()
    engine.add_cursor(2, 0, is_primary=True)
    
    code = "line1\nline2\nline3"
    result = engine.clone_cursors_up(code)
    
    assert result.success, "Klonlama başarılı olmalı"
    assert len(result.cursors) > 1, "Cursor'lar klonlanmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Cursors: {len(result.cursors)}")
    
    print("\n" + "=" * 70)
    print("PASS: Clone cursors up")
    print("=" * 70)


def test_find_all_occurrences():
    """
    Test: Find all occurrences.
    """
    print("=" * 70)
    print("TEST: Find All Occurrences")
    print("=" * 70)
    
    engine = MultiCursorEngine()
    
    code = "test line1\ntest line2\ntest line3"
    result = engine.find_all_occurrences(code, "test")
    
    assert result.success, "Bulma başarılı olmalı"
    assert len(result.cursors) > 0, "Oluşumlar bulunmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Found: {len(result.cursors)} occurrences")
    
    print("\n" + "=" * 70)
    print("PASS: Find all occurrences")
    print("=" * 70)


def test_select_all_occurrences():
    """
    Test: Select all occurrences.
    """
    print("=" * 70)
    print("TEST: Select All Occurrences")
    print("=" * 70)
    
    engine = MultiCursorEngine()
    
    code = "test line1\ntest line2"
    result = engine.select_all_occurrences(code, "test")
    
    assert result.success, "Seçim başarılı olmalı"
    assert len(result.cursors) > 0, "Oluşumlar seçilmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Selected: {len(result.cursors)} occurrences")
    
    print("\n" + "=" * 70)
    print("PASS: Select all occurrences")
    print("=" * 70)


def test_merge_cursors():
    """
    Test: Merge cursors.
    """
    print("=" * 70)
    print("TEST: Merge Cursors")
    print("=" * 70)
    
    engine = MultiCursorEngine()
    engine.add_cursor(0, 0, is_primary=True)
    engine.add_cursor(1, 0)
    
    result = engine.merge_cursors()
    
    assert result.success, "Birleştirme başarılı olmalı"
    assert len(result.cursors) == 1, "Tek cursor kalmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Cursors: {len(result.cursors)}")
    
    print("\n" + "=" * 70)
    print("PASS: Merge cursors")
    print("=" * 70)


def test_jump_to_next_cursor():
    """
    Test: Jump to next cursor.
    """
    print("=" * 70)
    print("TEST: Jump To Next Cursor")
    print("=" * 70)
    
    engine = MultiCursorEngine()
    engine.add_cursor(0, 0, is_primary=True)
    engine.add_cursor(1, 0)
    
    result = engine.jump_to_next_cursor()
    
    assert result.success, "Atlama başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Primary index: {engine.primary_cursor_index}")
    
    print("\n" + "=" * 70)
    print("PASS: Jump to next cursor")
    print("=" * 70)


def test_jump_to_previous_cursor():
    """
    Test: Jump to previous cursor.
    """
    print("=" * 70)
    print("TEST: Jump To Previous Cursor")
    print("=" * 70)
    
    engine = MultiCursorEngine()
    engine.add_cursor(0, 0, is_primary=True)
    engine.add_cursor(1, 0)
    
    result = engine.jump_to_previous_cursor()
    
    assert result.success, "Atlama başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Primary index: {engine.primary_cursor_index}")
    
    print("\n" + "=" * 70)
    print("PASS: Jump to previous cursor")
    print("=" * 70)


def test_get_cursors():
    """
    Test: Get cursors.
    """
    print("=" * 70)
    print("TEST: Get Cursors")
    print("=" * 70)
    
    engine = MultiCursorEngine()
    engine.add_cursor(0, 0)
    
    cursors = engine.get_cursors()
    
    assert len(cursors) > 0, "Cursor'lar olmalı"
    
    print(f"  Cursors: {len(cursors)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get cursors")
    print("=" * 70)


def test_get_primary_cursor():
    """
    Test: Get primary cursor.
    """
    print("=" * 70)
    print("TEST: Get Primary Cursor")
    print("=" * 70)
    
    engine = MultiCursorEngine()
    engine.add_cursor(0, 0, is_primary=True)
    
    primary = engine.get_primary_cursor()
    
    assert primary is not None, "Primary cursor olmalı"
    assert primary.is_primary == True, "Primary olmalı"
    
    print(f"  Primary: ({primary.line}, {primary.column})")
    
    print("\n" + "=" * 70)
    print("PASS: Get primary cursor")
    print("=" * 70)


def test_set_cursor_mode():
    """
    Test: Set cursor mode.
    """
    print("=" * 70)
    print("TEST: Set Cursor Mode")
    print("=" * 70)
    
    engine = MultiCursorEngine()
    
    result = engine.set_cursor_mode(CursorMode.BLOCK)
    
    assert result.success, "Ayar başarılı olmalı"
    assert engine.cursor_mode == CursorMode.BLOCK, "Mode eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Mode: {engine.cursor_mode.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Set cursor mode")
    print("=" * 70)


def test_get_cursor_count():
    """
    Test: Get cursor count.
    """
    print("=" * 70)
    print("TEST: Get Cursor Count")
    print("=" * 70)
    
    engine = MultiCursorEngine()
    engine.add_cursor(0, 0)
    engine.add_cursor(1, 0)
    
    count = engine.get_cursor_count()
    
    assert count == 2, "Count eşleşmeli"
    
    print(f"  Count: {count}")
    
    print("\n" + "=" * 70)
    print("PASS: Get cursor count")
    print("=" * 70)


def test_cursor_action_enum():
    """
    Test: CursorAction enum.
    """
    print("=" * 70)
    print("TEST: CursorAction Enum")
    print("=" * 70)
    
    assert CursorAction.ADD.value == "add"
    assert CursorAction.REMOVE.value == "remove"
    assert CursorAction.MOVE.value == "move"
    assert CursorAction.SELECT.value == "select"
    assert CursorAction.CLEAR.value == "clear"
    
    print(f"  All enum values verified")
    print(f"  Total actions: {len(CursorAction)}")
    
    print("\n" + "=" * 70)
    print("PASS: CursorAction enum")
    print("=" * 70)


def test_cursor_mode_enum():
    """
    Test: CursorMode enum.
    """
    print("=" * 70)
    print("TEST: CursorMode Enum")
    print("=" * 70)
    
    assert CursorMode.NORMAL.value == "normal"
    assert CursorMode.BLOCK.value == "block"
    assert CursorMode.COLUMN.value == "column"
    
    print(f"  All enum values verified")
    print(f"  Total modes: {len(CursorMode)}")
    
    print("\n" + "=" * 70)
    print("PASS: CursorMode enum")
    print("=" * 70)


def test_cursor_position_dataclass():
    """
    Test: CursorPosition dataclass.
    """
    print("=" * 70)
    print("TEST: CursorPosition Dataclass")
    print("=" * 70)
    
    position = CursorPosition(line=5, column=10, is_primary=True)
    
    assert position.line == 5, "Line eşleşmeli"
    assert position.column == 10, "Column eşleşmeli"
    assert position.is_primary == True, "Primary eşleşmeli"
    
    print(f"  Line: {position.line}")
    print(f"  Column: {position.column}")
    print(f"  Primary: {position.is_primary}")
    
    print("\n" + "=" * 70)
    print("PASS: CursorPosition dataclass")
    print("=" * 70)


def test_cursor_selection_dataclass():
    """
    Test: CursorSelection dataclass.
    """
    print("=" * 70)
    print("TEST: CursorSelection Dataclass")
    print("=" * 70)
    
    selection = CursorSelection(
        start_line=0,
        start_column=0,
        end_line=5,
        end_column=10
    )
    
    assert selection.start_line == 0, "Start line eşleşmeli"
    assert selection.end_line == 5, "End line eşleşmeli"
    
    print(f"  Start: ({selection.start_line}, {selection.start_column})")
    print(f"  End: ({selection.end_line}, {selection.end_column})")
    
    print("\n" + "=" * 70)
    print("PASS: CursorSelection dataclass")
    print("=" * 70)


def test_multi_cursor_edit_dataclass():
    """
    Test: MultiCursorEdit dataclass.
    """
    print("=" * 70)
    print("TEST: MultiCursorEdit Dataclass")
    print("=" * 70)
    
    position = CursorPosition(line=0, column=0)
    edit = MultiCursorEdit(
        cursor_id="1",
        position=position,
        text="test"
    )
    
    assert edit.cursor_id == "1", "ID eşleşmeli"
    assert edit.text == "test", "Text eşleşmeli"
    
    print(f"  Cursor ID: {edit.cursor_id}")
    print(f"  Text: {edit.text}")
    
    print("\n" + "=" * 70)
    print("PASS: MultiCursorEdit dataclass")
    print("=" * 70)


def test_multi_cursor_result_dataclass():
    """
    Test: MultiCursorResult dataclass.
    """
    print("=" * 70)
    print("TEST: MultiCursorResult Dataclass")
    print("=" * 70)
    
    result = MultiCursorResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.cursors, list), "Cursors list olmalı"
    assert isinstance(result.edits, list), "Edits list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Cursors: {len(result.cursors)}")
    print(f"  Edits: {len(result.edits)}")
    
    print("\n" + "=" * 70)
    print("PASS: MultiCursorResult dataclass")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_add_cursor()
        test2 = test_remove_cursor()
        test3 = test_clear_cursors()
        test4 = test_move_cursor()
        test5 = test_edit_at_cursors()
        test6 = test_clone_cursors_down()
        test7 = test_clone_cursors_up()
        test8 = test_find_all_occurrences()
        test9 = test_select_all_occurrences()
        test10 = test_merge_cursors()
        test11 = test_jump_to_next_cursor()
        test12 = test_jump_to_previous_cursor()
        test13 = test_get_cursors()
        test14 = test_get_primary_cursor()
        test15 = test_set_cursor_mode()
        test16 = test_get_cursor_count()
        test17 = test_cursor_action_enum()
        test18 = test_cursor_mode_enum()
        test19 = test_cursor_position_dataclass()
        test20 = test_cursor_selection_dataclass()
        test21 = test_multi_cursor_edit_dataclass()
        test22 = test_multi_cursor_result_dataclass()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Add Cursor: {'PASS' if test1 else 'FAIL'}")
        print(f"Remove Cursor: {'PASS' if test2 else 'FAIL'}")
        print(f"Clear Cursors: {'PASS' if test3 else 'FAIL'}")
        print(f"Move Cursor: {'PASS' if test4 else 'FAIL'}")
        print(f"Edit At Cursors: {'PASS' if test5 else 'FAIL'}")
        print(f"Clone Cursors Down: {'PASS' if test6 else 'FAIL'}")
        print(f"Clone Cursors Up: {'PASS' if test7 else 'FAIL'}")
        print(f"Find All Occurrences: {'PASS' if test8 else 'FAIL'}")
        print(f"Select All Occurrences: {'PASS' if test9 else 'FAIL'}")
        print(f"Merge Cursors: {'PASS' if test10 else 'FAIL'}")
        print(f"Jump To Next Cursor: {'PASS' if test11 else 'FAIL'}")
        print(f"Jump To Previous Cursor: {'PASS' if test12 else 'FAIL'}")
        print(f"Get Cursors: {'PASS' if test13 else 'FAIL'}")
        print(f"Get Primary Cursor: {'PASS' if test14 else 'FAIL'}")
        print(f"Set Cursor Mode: {'PASS' if test15 else 'FAIL'}")
        print(f"Get Cursor Count: {'PASS' if test16 else 'FAIL'}")
        print(f"CursorAction Enum: {'PASS' if test17 else 'FAIL'}")
        print(f"CursorMode Enum: {'PASS' if test18 else 'FAIL'}")
        print(f"CursorPosition Dataclass: {'PASS' if test19 else 'FAIL'}")
        print(f"CursorSelection Dataclass: {'PASS' if test20 else 'FAIL'}")
        print(f"MultiCursorEdit Dataclass: {'PASS' if test21 else 'FAIL'}")
        print(f"MultiCursorResult Dataclass: {'PASS' if test22 else 'FAIL'}")
        
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
