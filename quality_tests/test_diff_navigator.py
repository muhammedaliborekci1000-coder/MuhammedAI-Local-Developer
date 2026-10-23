"""
Quality Test: Diff Navigator
Diff navigator system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.diff_navigator import (
    DiffNavigatorEngine,
    NavigationMode,
    NavigationDirection,
    NavigationScope,
    NavigationAction,
    NavigationPosition,
    Bookmark,
    NavigationMark,
    NavigatorConfig,
    NavigatorResult
)


def test_navigate_to_hunk():
    """
    Test: Navigate to hunk.
    """
    print("=" * 70)
    print("TEST: Navigate To Hunk")
    print("=" * 70)
    
    engine = DiffNavigatorEngine()
    engine.set_hunks([(1, 10), (20, 30)])
    
    result = engine.navigate_to_hunk(0)
    
    assert result.success, "Navigasyon başarılı olmalı"
    assert result.action == NavigationAction.NAVIGATE.value, "Action eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Total hunks: {result.total_hunks}")
    print(f"  Position: {result.position}")
    
    print("\n" + "=" * 70)
    print("PASS: Navigate to hunk")
    print("=" * 70)


def test_navigate_to_line():
    """
    Test: Navigate to line.
    """
    print("=" * 70)
    print("TEST: Navigate To Line")
    print("=" * 70)
    
    engine = DiffNavigatorEngine()
    engine.set_hunks([(1, 10), (20, 30)])
    
    result = engine.navigate_to_line(5)
    
    assert result.success, "Navigasyon başarılı olmalı"
    assert result.position.line_number == 5, "Satır numarası eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Line number: {result.position.line_number}")
    
    print("\n" + "=" * 70)
    print("PASS: Navigate to line")
    print("=" * 70)


def test_navigate_to_file():
    """
    Test: Navigate to file.
    """
    print("=" * 70)
    print("TEST: Navigate To File")
    print("=" * 70)
    
    engine = DiffNavigatorEngine()
    engine.set_files(["file1.txt", "file2.txt"])
    
    result = engine.navigate_to_file(0, NavigationDirection.FIRST)
    
    assert result.success, "Navigasyon başarılı olmalı"
    assert result.position.file_index == 0, "Dosya indeksi eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  File index: {result.position.file_index}")
    
    print("\n" + "=" * 70)
    print("PASS: Navigate to file")
    print("=" * 70)


def test_jump_to_change():
    """
    Test: Jump to change.
    """
    print("=" * 70)
    print("TEST: Jump To Change")
    print("=" * 70)
    
    engine = DiffNavigatorEngine()
    engine.set_changes([5, 15, 25])
    
    result = engine.jump_to_change(NavigationDirection.NEXT)
    
    assert result.success, "Atlama başarılı olmalı"
    assert result.action == NavigationAction.JUMP.value, "Action eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Jump to change")
    print("=" * 70)


def test_next_hunk():
    """
    Test: Next hunk.
    """
    print("=" * 70)
    print("TEST: Next Hunk")
    print("=" * 70)
    
    engine = DiffNavigatorEngine()
    engine.set_hunks([(1, 10), (20, 30)])
    
    result = engine.next_hunk()
    
    assert result.success, "Geçiş başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Hunk index: {result.position.hunk_index}")
    
    print("\n" + "=" * 70)
    print("PASS: Next hunk")
    print("=" * 70)


def test_previous_hunk():
    """
    Test: Previous hunk.
    """
    print("=" * 70)
    print("TEST: Previous Hunk")
    print("=" * 70)
    
    engine = DiffNavigatorEngine()
    engine.set_hunks([(1, 10), (20, 30)])
    engine.navigate_to_hunk(1)
    
    result = engine.previous_hunk()
    
    assert result.success, "Geçiş başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Hunk index: {result.position.hunk_index}")
    
    print("\n" + "=" * 70)
    print("PASS: Previous hunk")
    print("=" * 70)


def test_first_hunk():
    """
    Test: First hunk.
    """
    print("=" * 70)
    print("TEST: First Hunk")
    print("=" * 70)
    
    engine = DiffNavigatorEngine()
    engine.set_hunks([(1, 10), (20, 30)])
    
    result = engine.first_hunk()
    
    assert result.success, "Geçiş başarılı olmalı"
    assert result.position.hunk_index == 0, "Hunk indeksi 0 olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Hunk index: {result.position.hunk_index}")
    
    print("\n" + "=" * 70)
    print("PASS: First hunk")
    print("=" * 70)


def test_last_hunk():
    """
    Test: Last hunk.
    """
    print("=" * 70)
    print("TEST: Last Hunk")
    print("=" * 70)
    
    engine = DiffNavigatorEngine()
    engine.set_hunks([(1, 10), (20, 30)])
    
    result = engine.last_hunk()
    
    assert result.success, "Geçiş başarılı olmalı"
    assert result.position.hunk_index == 1, "Hunk indeksi 1 olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Hunk index: {result.position.hunk_index}")
    
    print("\n" + "=" * 70)
    print("PASS: Last hunk")
    print("=" * 70)


def test_next_change():
    """
    Test: Next change.
    """
    print("=" * 70)
    print("TEST: Next Change")
    print("=" * 70)
    
    engine = DiffNavigatorEngine()
    engine.set_changes([5, 15, 25])
    
    result = engine.next_change()
    
    assert result.success, "Geçiş başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Line number: {result.position.line_number}")
    
    print("\n" + "=" * 70)
    print("PASS: Next change")
    print("=" * 70)


def test_previous_change():
    """
    Test: Previous change.
    """
    print("=" * 70)
    print("TEST: Previous Change")
    print("=" * 70)
    
    engine = DiffNavigatorEngine()
    engine.set_changes([5, 15, 25])
    engine.navigate_to_line(20)
    
    result = engine.previous_change()
    
    assert result.success, "Geçiş başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Line number: {result.position.line_number}")
    
    print("\n" + "=" * 70)
    print("PASS: Previous change")
    print("=" * 70)


def test_next_file():
    """
    Test: Next file.
    """
    print("=" * 70)
    print("TEST: Next File")
    print("=" * 70)
    
    engine = DiffNavigatorEngine()
    engine.set_files(["file1.txt", "file2.txt"])
    
    result = engine.next_file()
    
    assert result.success, "Geçiş başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  File index: {result.position.file_index}")
    
    print("\n" + "=" * 70)
    print("PASS: Next file")
    print("=" * 70)


def test_previous_file():
    """
    Test: Previous file.
    """
    print("=" * 70)
    print("TEST: Previous File")
    print("=" * 70)
    
    engine = DiffNavigatorEngine()
    engine.set_files(["file1.txt", "file2.txt"])
    engine.navigate_to_file(1)
    
    result = engine.previous_file()
    
    assert result.success, "Geçiş başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  File index: {result.position.file_index}")
    
    print("\n" + "=" * 70)
    print("PASS: Previous file")
    print("=" * 70)


def test_add_bookmark():
    """
    Test: Add bookmark.
    """
    print("=" * 70)
    print("TEST: Add Bookmark")
    print("=" * 70)
    
    engine = DiffNavigatorEngine()
    
    result = engine.add_bookmark("test_bookmark", "Test description")
    
    assert result.success, "Bookmark ekleme başarılı olmalı"
    assert "test_bookmark" in engine.bookmarks, "Bookmark bulunmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add bookmark")
    print("=" * 70)


def test_remove_bookmark():
    """
    Test: Remove bookmark.
    """
    print("=" * 70)
    print("TEST: Remove Bookmark")
    print("=" * 70)
    
    engine = DiffNavigatorEngine()
    engine.add_bookmark("test_bookmark")
    
    result = engine.remove_bookmark("test_bookmark")
    
    assert result.success, "Bookmark silme başarılı olmalı"
    assert "test_bookmark" not in engine.bookmarks, "Bookmark silinmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Remove bookmark")
    print("=" * 70)


def test_goto_bookmark():
    """
    Test: Goto bookmark.
    """
    print("=" * 70)
    print("TEST: Goto Bookmark")
    print("=" * 70)
    
    engine = DiffNavigatorEngine()
    engine.add_bookmark("test_bookmark")
    
    result = engine.goto_bookmark("test_bookmark")
    
    assert result.success, "Bookmark'a gitme başarılı olmalı"
    assert result.action == NavigationAction.GOTO.value, "Action eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Goto bookmark")
    print("=" * 70)


def test_add_mark():
    """
    Test: Add mark.
    """
    print("=" * 70)
    print("TEST: Add Mark")
    print("=" * 70)
    
    engine = DiffNavigatorEngine()
    
    result = engine.add_mark("change", "Test mark")
    
    assert result.success, "Mark ekleme başarılı olmalı"
    assert len(engine.marks) > 0, "Mark eklenmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add mark")
    print("=" * 70)


def test_get_current_position():
    """
    Test: Get current position.
    """
    print("=" * 70)
    print("TEST: Get Current Position")
    print("=" * 70)
    
    engine = DiffNavigatorEngine()
    engine.navigate_to_line(5)
    
    position = engine.get_current_position()
    
    assert position.line_number == 5, "Satır numarası eşleşmeli"
    
    print(f"  Line number: {position.line_number}")
    print(f"  Hunk index: {position.hunk_index}")
    
    print("\n" + "=" * 70)
    print("PASS: Get current position")
    print("=" * 70)


def test_get_bookmarks():
    """
    Test: Get bookmarks.
    """
    print("=" * 70)
    print("TEST: Get Bookmarks")
    print("=" * 70)
    
    engine = DiffNavigatorEngine()
    engine.add_bookmark("test_bookmark")
    
    bookmarks = engine.get_bookmarks()
    
    assert len(bookmarks) > 0, "Bookmarklar olmalı"
    
    print(f"  Bookmarks: {len(bookmarks)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get bookmarks")
    print("=" * 70)


def test_get_marks():
    """
    Test: Get marks.
    """
    print("=" * 70)
    print("TEST: Get Marks")
    print("=" * 70)
    
    engine = DiffNavigatorEngine()
    engine.add_mark("change")
    
    marks = engine.get_marks()
    
    assert len(marks) > 0, "Marklar olmalı"
    
    print(f"  Marks: {len(marks)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get marks")
    print("=" * 70)


def test_get_navigation_history():
    """
    Test: Get navigation history.
    """
    print("=" * 70)
    print("TEST: Get Navigation History")
    print("=" * 70)
    
    engine = DiffNavigatorEngine()
    engine.navigate_to_line(5)
    
    history = engine.get_navigation_history()
    
    assert len(history) > 0, "Geçmiş olmalı"
    
    print(f"  History: {len(history)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get navigation history")
    print("=" * 70)


def test_clear_history():
    """
    Test: Clear history.
    """
    print("=" * 70)
    print("TEST: Clear History")
    print("=" * 70)
    
    engine = DiffNavigatorEngine()
    engine.navigate_to_line(5)
    
    result = engine.clear_history()
    
    assert result.success, "Temizleme başarılı olmalı"
    assert len(engine.get_navigation_history()) == 0, "Geçmiş temizlenmeli"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear history")
    print("=" * 70)


def test_get_statistics():
    """
    Test: Get statistics.
    """
    print("=" * 70)
    print("TEST: Get Statistics")
    print("=" * 70)
    
    engine = DiffNavigatorEngine()
    engine.set_hunks([(1, 10), (20, 30)])
    engine.set_changes([5, 15, 25])
    engine.set_files(["file1.txt", "file2.txt"])
    
    stats = engine.get_statistics()
    
    assert stats is not None, "İstatistikler olmalı"
    assert stats["total_hunks"] == 2, "Toplam hunk 2 olmalı"
    
    print(f"  Total hunks: {stats['total_hunks']}")
    print(f"  Total changes: {stats['total_changes']}")
    print(f"  Total files: {stats['total_files']}")
    
    print("\n" + "=" * 70)
    print("PASS: Get statistics")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    engine = DiffNavigatorEngine()
    
    new_config = NavigatorConfig(wrap_around=False)
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
    
    engine = DiffNavigatorEngine()
    
    config = engine.get_config()
    
    assert config is not None, "Config olmalı"
    assert config.wrap_around == True, "Config eşleşmeli"
    
    print(f"  Wrap around: {config.wrap_around}")
    print(f"  Skip unchanged: {config.skip_unchanged}")
    
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
    
    assert NavigationMode.HUNK.value == "hunk"
    assert NavigationMode.LINE.value == "line"
    assert NavigationMode.FILE.value == "file"
    assert NavigationMode.CHANGE.value == "change"
    assert NavigationMode.CONFLICT.value == "conflict"
    
    print(f"  All enum values verified")
    print(f"  Total modes: {len(NavigationMode)}")
    
    print("\n" + "=" * 70)
    print("PASS: NavigationMode enum")
    print("=" * 70)


def test_navigation_direction_enum():
    """
    Test: NavigationDirection enum.
    """
    print("=" * 70)
    print("TEST: NavigationDirection Enum")
    print("=" * 70)
    
    assert NavigationDirection.NEXT.value == "next"
    assert NavigationDirection.PREVIOUS.value == "previous"
    assert NavigationDirection.FIRST.value == "first"
    assert NavigationDirection.LAST.value == "last"
    
    print(f"  All enum values verified")
    print(f"  Total directions: {len(NavigationDirection)}")
    
    print("\n" + "=" * 70)
    print("PASS: NavigationDirection enum")
    print("=" * 70)


def test_navigation_scope_enum():
    """
    Test: NavigationScope enum.
    """
    print("=" * 70)
    print("TEST: NavigationScope Enum")
    print("=" * 70)
    
    assert NavigationScope.CURRENT_FILE.value == "current_file"
    assert NavigationScope.ALL_FILES.value == "all_files"
    assert NavigationScope.VISIBLE.value == "visible"
    assert NavigationScope.SELECTED.value == "selected"
    
    print(f"  All enum values verified")
    print(f"  Total scopes: {len(NavigationScope)}")
    
    print("\n" + "=" * 70)
    print("PASS: NavigationScope enum")
    print("=" * 70)


def test_navigator_config_dataclass():
    """
    Test: NavigatorConfig dataclass.
    """
    print("=" * 70)
    print("TEST: NavigatorConfig Dataclass")
    print("=" * 70)
    
    config = NavigatorConfig(
        wrap_around=False,
        skip_unchanged=False
    )
    
    assert config.wrap_around == False, "Wrap around eşleşmeli"
    assert config.skip_unchanged == False, "Skip unchanged eşleşmeli"
    
    print(f"  Wrap around: {config.wrap_around}")
    print(f"  Skip unchanged: {config.skip_unchanged}")
    
    print("\n" + "=" * 70)
    print("PASS: NavigatorConfig dataclass")
    print("=" * 70)


def test_navigation_position_dataclass():
    """
    Test: NavigationPosition dataclass.
    """
    print("=" * 70)
    print("TEST: NavigationPosition Dataclass")
    print("=" * 70)
    
    position = NavigationPosition(
        file_index=0,
        line_number=5,
        hunk_index=1
    )
    
    assert position.file_index == 0, "File index eşleşmeli"
    assert position.line_number == 5, "Line number eşleşmeli"
    
    print(f"  File index: {position.file_index}")
    print(f"  Line number: {position.line_number}")
    
    print("\n" + "=" * 70)
    print("PASS: NavigationPosition dataclass")
    print("=" * 70)


def test_navigator_result_dataclass():
    """
    Test: NavigatorResult dataclass.
    """
    print("=" * 70)
    print("TEST: NavigatorResult Dataclass")
    print("=" * 70)
    
    result = NavigatorResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: NavigatorResult dataclass")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_navigate_to_hunk()
        test2 = test_navigate_to_line()
        test3 = test_navigate_to_file()
        test4 = test_jump_to_change()
        test5 = test_next_hunk()
        test6 = test_previous_hunk()
        test7 = test_first_hunk()
        test8 = test_last_hunk()
        test9 = test_next_change()
        test10 = test_previous_change()
        test11 = test_next_file()
        test12 = test_previous_file()
        test13 = test_add_bookmark()
        test14 = test_remove_bookmark()
        test15 = test_goto_bookmark()
        test16 = test_add_mark()
        test17 = test_get_current_position()
        test18 = test_get_bookmarks()
        test19 = test_get_marks()
        test20 = test_get_navigation_history()
        test21 = test_clear_history()
        test22 = test_get_statistics()
        test23 = test_update_config()
        test24 = test_get_config()
        test25 = test_navigation_mode_enum()
        test26 = test_navigation_direction_enum()
        test27 = test_navigation_scope_enum()
        test28 = test_navigator_config_dataclass()
        test29 = test_navigation_position_dataclass()
        test30 = test_navigator_result_dataclass()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Navigate To Hunk: {'PASS' if test1 else 'FAIL'}")
        print(f"Navigate To Line: {'PASS' if test2 else 'FAIL'}")
        print(f"Navigate To File: {'PASS' if test3 else 'FAIL'}")
        print(f"Jump To Change: {'PASS' if test4 else 'FAIL'}")
        print(f"Next Hunk: {'PASS' if test5 else 'FAIL'}")
        print(f"Previous Hunk: {'PASS' if test6 else 'FAIL'}")
        print(f"First Hunk: {'PASS' if test7 else 'FAIL'}")
        print(f"Last Hunk: {'PASS' if test8 else 'FAIL'}")
        print(f"Next Change: {'PASS' if test9 else 'FAIL'}")
        print(f"Previous Change: {'PASS' if test10 else 'FAIL'}")
        print(f"Next File: {'PASS' if test11 else 'FAIL'}")
        print(f"Previous File: {'PASS' if test12 else 'FAIL'}")
        print(f"Add Bookmark: {'PASS' if test13 else 'FAIL'}")
        print(f"Remove Bookmark: {'PASS' if test14 else 'FAIL'}")
        print(f"Goto Bookmark: {'PASS' if test15 else 'FAIL'}")
        print(f"Add Mark: {'PASS' if test16 else 'FAIL'}")
        print(f"Get Current Position: {'PASS' if test17 else 'FAIL'}")
        print(f"Get Bookmarks: {'PASS' if test18 else 'FAIL'}")
        print(f"Get Marks: {'PASS' if test19 else 'FAIL'}")
        print(f"Get Navigation History: {'PASS' if test20 else 'FAIL'}")
        print(f"Clear History: {'PASS' if test21 else 'FAIL'}")
        print(f"Get Statistics: {'PASS' if test22 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test23 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test24 else 'FAIL'}")
        print(f"NavigationMode Enum: {'PASS' if test25 else 'FAIL'}")
        print(f"NavigationDirection Enum: {'PASS' if test26 else 'FAIL'}")
        print(f"NavigationScope Enum: {'PASS' if test27 else 'FAIL'}")
        print(f"NavigatorConfig Dataclass: {'PASS' if test28 else 'FAIL'}")
        print(f"NavigationPosition Dataclass: {'PASS' if test29 else 'FAIL'}")
        print(f"NavigatorResult Dataclass: {'PASS' if test30 else 'FAIL'}")
        
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
