"""
Quality Test: Diff Viewer
Diff viewer system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.diff_viewer import (
    DiffViewerEngine,
    DiffViewMode,
    DiffTheme,
    ScrollMode,
    ZoomLevel,
    DiffLine,
    DiffHunk,
    DiffFile,
    ViewerConfig,
    ViewerState,
    ViewerResult
)


def test_load_diff():
    """
    Test: Load diff.
    """
    print("=" * 70)
    print("TEST: Load Diff")
    print("=" * 70)
    
    engine = DiffViewerEngine()
    old_content = "Line 1\nLine 2\nLine 3"
    new_content = "Line 1\nLine 2 modified\nLine 3"
    
    result = engine.load_diff(old_content, new_content, "test.txt")
    
    assert result.success, "Diff yükleme başarılı olmalı"
    assert result.total_files == 1, "1 dosya olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Total files: {result.total_files}")
    print(f"  Total added: {result.total_added}")
    print(f"  Total removed: {result.total_removed}")
    
    print("\n" + "=" * 70)
    print("PASS: Load diff")
    print("=" * 70)


def test_set_view_mode():
    """
    Test: Set view mode.
    """
    print("=" * 70)
    print("TEST: Set View Mode")
    print("=" * 70)
    
    engine = DiffViewerEngine()
    result = engine.set_view_mode(DiffViewMode.SIDE_BY_SIDE)
    
    assert result.success, "View mode ayarlama başarılı olmalı"
    assert engine.config.view_mode == DiffViewMode.SIDE_BY_SIDE, "Mode eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set view mode")
    print("=" * 70)


def test_set_theme():
    """
    Test: Set theme.
    """
    print("=" * 70)
    print("TEST: Set Theme")
    print("=" * 70)
    
    engine = DiffViewerEngine()
    result = engine.set_theme(DiffTheme.LIGHT)
    
    assert result.success, "Tema ayarlama başarılı olmalı"
    assert engine.config.theme == DiffTheme.LIGHT, "Tema eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set theme")
    print("=" * 70)


def test_set_scroll_mode():
    """
    Test: Set scroll mode.
    """
    print("=" * 70)
    print("TEST: Set Scroll Mode")
    print("=" * 70)
    
    engine = DiffViewerEngine()
    result = engine.set_scroll_mode(ScrollMode.INDEPENDENT)
    
    assert result.success, "Scroll mode ayarlama başarılı olmalı"
    assert engine.config.scroll_mode == ScrollMode.INDEPENDENT, "Mode eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set scroll mode")
    print("=" * 70)


def test_set_zoom_level():
    """
    Test: Set zoom level.
    """
    print("=" * 70)
    print("TEST: Set Zoom Level")
    print("=" * 70)
    
    engine = DiffViewerEngine()
    result = engine.set_zoom_level(ZoomLevel.LARGE)
    
    assert result.success, "Zoom level ayarlama başarılı olmalı"
    assert engine.config.zoom_level == ZoomLevel.LARGE, "Level eşleşmeli"
    assert engine.state.zoom_factor == 1.2, "Zoom faktörü eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Zoom factor: {engine.state.zoom_factor}")
    
    print("\n" + "=" * 70)
    print("PASS: Set zoom level")
    print("=" * 70)


def test_scroll_to():
    """
    Test: Scroll to.
    """
    print("=" * 70)
    print("TEST: Scroll To")
    print("=" * 70)
    
    engine = DiffViewerEngine()
    result = engine.scroll_to(100)
    
    assert result.success, "Scroll başarılı olmalı"
    assert engine.state.scroll_position == 100, "Pozisyon eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Scroll to")
    print("=" * 70)


def test_scroll_to_line():
    """
    Test: Scroll to line.
    """
    print("=" * 70)
    print("TEST: Scroll To Line")
    print("=" * 70)
    
    engine = DiffViewerEngine()
    result = engine.scroll_to_line(5)
    
    assert result.success, "Scroll başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Scroll to line")
    print("=" * 70)


def test_scroll_to_hunk():
    """
    Test: Scroll to hunk.
    """
    print("=" * 70)
    print("TEST: Scroll To Hunk")
    print("=" * 70)
    
    engine = DiffViewerEngine()
    old_content = "Line 1\nLine 2\nLine 3"
    new_content = "Line 1\nLine 2 modified\nLine 3"
    engine.load_diff(old_content, new_content, "test.txt")
    
    result = engine.scroll_to_hunk(0)
    
    assert result.success, "Scroll başarılı olmalı"
    assert engine.state.current_hunk_index == 0, "Hunk indeksi eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Scroll to hunk")
    print("=" * 70)


def test_next_hunk():
    """
    Test: Next hunk.
    """
    print("=" * 70)
    print("TEST: Next Hunk")
    print("=" * 70)
    
    engine = DiffViewerEngine()
    old_content = "Line 1\nLine 2\nLine 3"
    new_content = "Line 1\nLine 2 modified\nLine 3\nLine 4 added"
    engine.load_diff(old_content, new_content, "test.txt")
    
    result = engine.next_hunk()
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
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
    
    engine = DiffViewerEngine()
    old_content = "Line 1\nLine 2\nLine 3"
    new_content = "Line 1\nLine 2 modified\nLine 3"
    engine.load_diff(old_content, new_content, "test.txt")
    engine.scroll_to_hunk(0)
    
    result = engine.previous_hunk()
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Previous hunk")
    print("=" * 70)


def test_next_file():
    """
    Test: Next file.
    """
    print("=" * 70)
    print("TEST: Next File")
    print("=" * 70)
    
    engine = DiffViewerEngine()
    old_content = "Line 1\nLine 2"
    new_content = "Line 1 modified\nLine 2"
    engine.load_diff(old_content, new_content, "test1.txt")
    
    result = engine.next_file()
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
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
    
    engine = DiffViewerEngine()
    old_content = "Line 1\nLine 2"
    new_content = "Line 1 modified\nLine 2"
    engine.load_diff(old_content, new_content, "test1.txt")
    
    result = engine.previous_file()
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Previous file")
    print("=" * 70)


def test_get_current_file():
    """
    Test: Get current file.
    """
    print("=" * 70)
    print("TEST: Get Current File")
    print("=" * 70)
    
    engine = DiffViewerEngine()
    old_content = "Line 1\nLine 2"
    new_content = "Line 1 modified\nLine 2"
    engine.load_diff(old_content, new_content, "test.txt")
    
    file = engine.get_current_file()
    
    assert file is not None, "Dosya bulunmalı"
    assert file.file_path == "test.txt", "Dosya yolu eşleşmeli"
    
    print(f"  File path: {file.file_path}")
    print(f"  Added lines: {file.added_lines}")
    
    print("\n" + "=" * 70)
    print("PASS: Get current file")
    print("=" * 70)


def test_get_current_hunk():
    """
    Test: Get current hunk.
    """
    print("=" * 70)
    print("TEST: Get Current Hunk")
    print("=" * 70)
    
    engine = DiffViewerEngine()
    old_content = "Line 1\nLine 2\nLine 3"
    new_content = "Line 1\nLine 2 modified\nLine 3"
    engine.load_diff(old_content, new_content, "test.txt")
    
    hunk = engine.get_current_hunk()
    
    print(f"  Hunk: {hunk is not None}")
    
    print("\n" + "=" * 70)
    print("PASS: Get current hunk")
    print("=" * 70)


def test_get_scroll_position():
    """
    Test: Get scroll position.
    """
    print("=" * 70)
    print("TEST: Get Scroll Position")
    print("=" * 70)
    
    engine = DiffViewerEngine()
    engine.scroll_to(50)
    
    position = engine.get_scroll_position()
    
    assert position == 50, "Pozisyon eşleşmeli"
    
    print(f"  Scroll position: {position}")
    
    print("\n" + "=" * 70)
    print("PASS: Get scroll position")
    print("=" * 70)


def test_get_zoom_factor():
    """
    Test: Get zoom factor.
    """
    print("=" * 70)
    print("TEST: Get Zoom Factor")
    print("=" * 70)
    
    engine = DiffViewerEngine()
    engine.set_zoom_level(ZoomLevel.LARGE)
    
    factor = engine.get_zoom_factor()
    
    assert factor == 1.2, "Zoom faktörü eşleşmeli"
    
    print(f"  Zoom factor: {factor}")
    
    print("\n" + "=" * 70)
    print("PASS: Get zoom factor")
    print("=" * 70)


def test_get_viewer_history():
    """
    Test: Get viewer history.
    """
    print("=" * 70)
    print("TEST: Get Viewer History")
    print("=" * 70)
    
    engine = DiffViewerEngine()
    engine.load_diff("Line 1", "Line 2", "test.txt")
    
    history = engine.get_viewer_history()
    
    assert len(history) > 0, "Geçmiş olmalı"
    
    print(f"  History: {len(history)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get viewer history")
    print("=" * 70)


def test_clear_history():
    """
    Test: Clear history.
    """
    print("=" * 70)
    print("TEST: Clear History")
    print("=" * 70)
    
    engine = DiffViewerEngine()
    engine.load_diff("Line 1", "Line 2", "test.txt")
    
    result = engine.clear_history()
    
    assert result.success, "Temizleme başarılı olmalı"
    assert len(engine.get_viewer_history()) == 0, "Geçmiş temizlenmeli"
    
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
    
    engine = DiffViewerEngine()
    old_content = "Line 1\nLine 2"
    new_content = "Line 1 modified\nLine 2"
    engine.load_diff(old_content, new_content, "test.txt")
    
    stats = engine.get_statistics()
    
    assert stats is not None, "İstatistikler olmalı"
    assert stats["total_files"] == 1, "Toplam dosya 1 olmalı"
    
    print(f"  Total files: {stats['total_files']}")
    print(f"  Total added: {stats['total_added']}")
    print(f"  Total removed: {stats['total_removed']}")
    
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
    
    engine = DiffViewerEngine()
    
    new_config = ViewerConfig(view_mode=DiffViewMode.INLINE)
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
    
    engine = DiffViewerEngine()
    
    config = engine.get_config()
    
    assert config is not None, "Config olmalı"
    assert config.view_mode == DiffViewMode.UNIFIED, "Config eşleşmeli"
    
    print(f"  View mode: {config.view_mode.value}")
    print(f"  Theme: {config.theme.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


def test_get_state():
    """
    Test: Get state.
    """
    print("=" * 70)
    print("TEST: Get State")
    print("=" * 70)
    
    engine = DiffViewerEngine()
    
    state = engine.get_state()
    
    assert state is not None, "Durum olmalı"
    assert state.current_file_index == 0, "Dosya indeksi eşleşmeli"
    
    print(f"  Current file index: {state.current_file_index}")
    print(f"  Scroll position: {state.scroll_position}")
    
    print("\n" + "=" * 70)
    print("PASS: Get state")
    print("=" * 70)


def test_diff_view_mode_enum():
    """
    Test: DiffViewMode enum.
    """
    print("=" * 70)
    print("TEST: DiffViewMode Enum")
    print("=" * 70)
    
    assert DiffViewMode.UNIFIED.value == "unified"
    assert DiffViewMode.SIDE_BY_SIDE.value == "side_by_side"
    assert DiffViewMode.INLINE.value == "inline"
    assert DiffViewMode.SPLIT.value == "split"
    
    print(f"  All enum values verified")
    print(f"  Total modes: {len(DiffViewMode)}")
    
    print("\n" + "=" * 70)
    print("PASS: DiffViewMode enum")
    print("=" * 70)


def test_diff_theme_enum():
    """
    Test: DiffTheme enum.
    """
    print("=" * 70)
    print("TEST: DiffTheme Enum")
    print("=" * 70)
    
    assert DiffTheme.LIGHT.value == "light"
    assert DiffTheme.DARK.value == "dark"
    assert DiffTheme.HIGH_CONTRAST.value == "high_contrast"
    assert DiffTheme.MONOCHROME.value == "monochrome"
    
    print(f"  All enum values verified")
    print(f"  Total themes: {len(DiffTheme)}")
    
    print("\n" + "=" * 70)
    print("PASS: DiffTheme enum")
    print("=" * 70)


def test_scroll_mode_enum():
    """
    Test: ScrollMode enum.
    """
    print("=" * 70)
    print("TEST: ScrollMode Enum")
    print("=" * 70)
    
    assert ScrollMode.SYNC.value == "sync"
    assert ScrollMode.INDEPENDENT.value == "independent"
    assert ScrollMode.LOCKED.value == "locked"
    
    print(f"  All enum values verified")
    print(f"  Total modes: {len(ScrollMode)}")
    
    print("\n" + "=" * 70)
    print("PASS: ScrollMode enum")
    print("=" * 70)


def test_zoom_level_enum():
    """
    Test: ZoomLevel enum.
    """
    print("=" * 70)
    print("TEST: ZoomLevel Enum")
    print("=" * 70)
    
    assert ZoomLevel.SMALL.value == "small"
    assert ZoomLevel.NORMAL.value == "normal"
    assert ZoomLevel.LARGE.value == "large"
    assert ZoomLevel.EXTRA_LARGE.value == "extra_large"
    
    print(f"  All enum values verified")
    print(f"  Total levels: {len(ZoomLevel)}")
    
    print("\n" + "=" * 70)
    print("PASS: ZoomLevel enum")
    print("=" * 70)


def test_viewer_config_dataclass():
    """
    Test: ViewerConfig dataclass.
    """
    print("=" * 70)
    print("TEST: ViewerConfig Dataclass")
    print("=" * 70)
    
    config = ViewerConfig(
        view_mode=DiffViewMode.INLINE,
        theme=DiffTheme.LIGHT
    )
    
    assert config.view_mode == DiffViewMode.INLINE, "View mode eşleşmeli"
    assert config.theme == DiffTheme.LIGHT, "Theme eşleşmeli"
    
    print(f"  View mode: {config.view_mode.value}")
    print(f"  Theme: {config.theme.value}")
    
    print("\n" + "=" * 70)
    print("PASS: ViewerConfig dataclass")
    print("=" * 70)


def test_viewer_state_dataclass():
    """
    Test: ViewerState dataclass.
    """
    print("=" * 70)
    print("TEST: ViewerState Dataclass")
    print("=" * 70)
    
    state = ViewerState(
        current_file_index=0,
        scroll_position=100
    )
    
    assert state.current_file_index == 0, "File index eşleşmeli"
    assert state.scroll_position == 100, "Scroll position eşleşmeli"
    
    print(f"  Current file index: {state.current_file_index}")
    print(f"  Scroll position: {state.scroll_position}")
    
    print("\n" + "=" * 70)
    print("PASS: ViewerState dataclass")
    print("=" * 70)


def test_diff_line_dataclass():
    """
    Test: DiffLine dataclass.
    """
    print("=" * 70)
    print("TEST: DiffLine Dataclass")
    print("=" * 70)
    
    line = DiffLine(
        line_number=1,
        content="Line content",
        line_type="added"
    )
    
    assert line.line_number == 1, "Line number eşleşmeli"
    assert line.content == "Line content", "Content eşleşmeli"
    
    print(f"  Line number: {line.line_number}")
    print(f"  Content: {line.content}")
    
    print("\n" + "=" * 70)
    print("PASS: DiffLine dataclass")
    print("=" * 70)


def test_viewer_result_dataclass():
    """
    Test: ViewerResult dataclass.
    """
    print("=" * 70)
    print("TEST: ViewerResult Dataclass")
    print("=" * 70)
    
    result = ViewerResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: ViewerResult dataclass")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_load_diff()
        test2 = test_set_view_mode()
        test3 = test_set_theme()
        test4 = test_set_scroll_mode()
        test5 = test_set_zoom_level()
        test6 = test_scroll_to()
        test7 = test_scroll_to_line()
        test8 = test_scroll_to_hunk()
        test9 = test_next_hunk()
        test10 = test_previous_hunk()
        test11 = test_next_file()
        test12 = test_previous_file()
        test13 = test_get_current_file()
        test14 = test_get_current_hunk()
        test15 = test_get_scroll_position()
        test16 = test_get_zoom_factor()
        test17 = test_get_viewer_history()
        test18 = test_clear_history()
        test19 = test_get_statistics()
        test20 = test_update_config()
        test21 = test_get_config()
        test22 = test_get_state()
        test23 = test_diff_view_mode_enum()
        test24 = test_diff_theme_enum()
        test25 = test_scroll_mode_enum()
        test26 = test_zoom_level_enum()
        test27 = test_viewer_config_dataclass()
        test28 = test_viewer_state_dataclass()
        test29 = test_diff_line_dataclass()
        test30 = test_viewer_result_dataclass()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Load Diff: {'PASS' if test1 else 'FAIL'}")
        print(f"Set View Mode: {'PASS' if test2 else 'FAIL'}")
        print(f"Set Theme: {'PASS' if test3 else 'FAIL'}")
        print(f"Set Scroll Mode: {'PASS' if test4 else 'FAIL'}")
        print(f"Set Zoom Level: {'PASS' if test5 else 'FAIL'}")
        print(f"Scroll To: {'PASS' if test6 else 'FAIL'}")
        print(f"Scroll To Line: {'PASS' if test7 else 'FAIL'}")
        print(f"Scroll To Hunk: {'PASS' if test8 else 'FAIL'}")
        print(f"Next Hunk: {'PASS' if test9 else 'FAIL'}")
        print(f"Previous Hunk: {'PASS' if test10 else 'FAIL'}")
        print(f"Next File: {'PASS' if test11 else 'FAIL'}")
        print(f"Previous File: {'PASS' if test12 else 'FAIL'}")
        print(f"Get Current File: {'PASS' if test13 else 'FAIL'}")
        print(f"Get Current Hunk: {'PASS' if test14 else 'FAIL'}")
        print(f"Get Scroll Position: {'PASS' if test15 else 'FAIL'}")
        print(f"Get Zoom Factor: {'PASS' if test16 else 'FAIL'}")
        print(f"Get Viewer History: {'PASS' if test17 else 'FAIL'}")
        print(f"Clear History: {'PASS' if test18 else 'FAIL'}")
        print(f"Get Statistics: {'PASS' if test19 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test20 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test21 else 'FAIL'}")
        print(f"Get State: {'PASS' if test22 else 'FAIL'}")
        print(f"DiffViewMode Enum: {'PASS' if test23 else 'FAIL'}")
        print(f"DiffTheme Enum: {'PASS' if test24 else 'FAIL'}")
        print(f"ScrollMode Enum: {'PASS' if test25 else 'FAIL'}")
        print(f"ZoomLevel Enum: {'PASS' if test26 else 'FAIL'}")
        print(f"ViewerConfig Dataclass: {'PASS' if test27 else 'FAIL'}")
        print(f"ViewerState Dataclass: {'PASS' if test28 else 'FAIL'}")
        print(f"DiffLine Dataclass: {'PASS' if test29 else 'FAIL'}")
        print(f"ViewerResult Dataclass: {'PASS' if test30 else 'FAIL'}")
        
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
