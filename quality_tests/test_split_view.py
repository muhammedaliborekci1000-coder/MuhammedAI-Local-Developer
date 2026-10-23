"""
Quality Test: Split View
Split view system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.split_view import (
    SplitViewEngine,
    SplitDirection,
    SplitMode,
    ViewPane,
    SplitViewConfig,
    SplitViewResult
)


def test_split_view():
    """
    Test: Split view.
    """
    print("=" * 70)
    print("TEST: Split View")
    print("=" * 70)
    
    config = SplitViewConfig()
    engine = SplitViewEngine(config)
    
    result = engine.split_view(SplitDirection.HORIZONTAL, "test.py", "print('hello')")
    
    assert result.success, "Split başarılı olmalı"
    assert len(result.panes) > 0, "Pane'lar oluşturulmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Panes: {len(result.panes)}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Split view")
    print("=" * 70)


def test_unsplit_view():
    """
    Test: Unsplit view.
    """
    print("=" * 70)
    print("TEST: Unsplit View")
    print("=" * 70)
    
    config = SplitViewConfig()
    engine = SplitViewEngine(config)
    
    # İki pane ekle
    engine.split_view(SplitDirection.HORIZONTAL, "test.py", "print('hello')")
    engine.split_view(SplitDirection.HORIZONTAL, "test2.py", "print('world')")
    
    # Unsplit
    result = engine.unsplit_view()
    
    assert result.success, "Unsplit başarılı olmalı"
    assert len(result.panes) == 1, "Tek pane kalmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Panes: {len(result.panes)}")
    
    print("\n" + "=" * 70)
    print("PASS: Unsplit view")
    print("=" * 70)


def test_focus_pane():
    """
    Test: Focus pane.
    """
    print("=" * 70)
    print("TEST: Focus Pane")
    print("=" * 70)
    
    config = SplitViewConfig()
    engine = SplitViewEngine(config)
    
    # İki pane ekle
    engine.split_view(SplitDirection.HORIZONTAL, "test.py", "print('hello')")
    result1 = engine.split_view(SplitDirection.HORIZONTAL, "test2.py", "print('world')")
    
    # İlk pane'a focus yap
    result = engine.focus_pane(result1.panes[0].pane_id)
    
    assert result.success, "Focus başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Active pane: {result.active_pane_id}")
    
    print("\n" + "=" * 70)
    print("PASS: Focus pane")
    print("=" * 70)


def test_get_active_pane():
    """
    Test: Get active pane.
    """
    print("=" * 70)
    print("TEST: Get Active Pane")
    print("=" * 70)
    
    config = SplitViewConfig()
    engine = SplitViewEngine(config)
    
    engine.split_view(SplitDirection.HORIZONTAL, "test.py", "print('hello')")
    
    active_pane = engine.get_active_pane()
    
    assert active_pane is not None, "Aktif pane olmalı"
    assert active_pane.is_active == True, "Aktif olmalı"
    
    print(f"  Active pane: {active_pane.pane_id}")
    
    print("\n" + "=" * 70)
    print("PASS: Get active pane")
    print("=" * 70)


def test_get_pane_by_id():
    """
    Test: Get pane by ID.
    """
    print("=" * 70)
    print("TEST: Get Pane By ID")
    print("=" * 70)
    
    config = SplitViewConfig()
    engine = SplitViewEngine(config)
    
    result = engine.split_view(SplitDirection.HORIZONTAL, "test.py", "print('hello')")
    pane_id = result.panes[0].pane_id
    
    pane = engine.get_pane_by_id(pane_id)
    
    assert pane is not None, "Pane bulunmalı"
    assert pane.pane_id == pane_id, "ID eşleşmeli"
    
    print(f"  Pane found: {pane.pane_id}")
    
    print("\n" + "=" * 70)
    print("PASS: Get pane by ID")
    print("=" * 70)


def test_update_pane_content():
    """
    Test: Update pane content.
    """
    print("=" * 70)
    print("TEST: Update Pane Content")
    print("=" * 70)
    
    config = SplitViewConfig()
    engine = SplitViewEngine(config)
    
    result = engine.split_view(SplitDirection.HORIZONTAL, "test.py", "print('hello')")
    pane_id = result.panes[0].pane_id
    
    update_result = engine.update_pane_content(pane_id, "print('world')")
    
    assert update_result.success, "Güncelleme başarılı olmalı"
    
    print(f"  Success: {update_result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Update pane content")
    print("=" * 70)


def test_update_pane_cursor():
    """
    Test: Update pane cursor.
    """
    print("=" * 70)
    print("TEST: Update Pane Cursor")
    print("=" * 70)
    
    config = SplitViewConfig()
    engine = SplitViewEngine(config)
    
    result = engine.split_view(SplitDirection.HORIZONTAL, "test.py", "print('hello')")
    pane_id = result.panes[0].pane_id
    
    update_result = engine.update_pane_cursor(pane_id, 5, 10)
    
    assert update_result.success, "Güncelleme başarılı olmalı"
    
    print(f"  Success: {update_result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Update pane cursor")
    print("=" * 70)


def test_update_pane_scroll():
    """
    Test: Update pane scroll.
    """
    print("=" * 70)
    print("TEST: Update Pane Scroll")
    print("=" * 70)
    
    config = SplitViewConfig()
    engine = SplitViewEngine(config)
    
    result = engine.split_view(SplitDirection.HORIZONTAL, "test.py", "print('hello')")
    pane_id = result.panes[0].pane_id
    
    update_result = engine.update_pane_scroll(pane_id, 100)
    
    assert update_result.success, "Güncelleme başarılı olmalı"
    
    print(f"  Success: {update_result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Update pane scroll")
    print("=" * 70)


def test_set_split_direction():
    """
    Test: Set split direction.
    """
    print("=" * 70)
    print("TEST: Set Split Direction")
    print("=" * 70)
    
    config = SplitViewConfig()
    engine = SplitViewEngine(config)
    
    result = engine.set_split_direction(SplitDirection.VERTICAL)
    
    assert result.success, "Ayar başarılı olmalı"
    assert engine.config.direction == SplitDirection.VERTICAL, "Direction eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Direction: {engine.config.direction.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Set split direction")
    print("=" * 70)


def test_set_split_ratio():
    """
    Test: Set split ratio.
    """
    print("=" * 70)
    print("TEST: Set Split Ratio")
    print("=" * 70)
    
    config = SplitViewConfig()
    engine = SplitViewEngine(config)
    
    result = engine.set_split_ratio(0.7)
    
    assert result.success, "Ayar başarılı olmalı"
    assert engine.config.split_ratio == 0.7, "Ratio eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Ratio: {engine.config.split_ratio}")
    
    print("\n" + "=" * 70)
    print("PASS: Set split ratio")
    print("=" * 70)


def test_toggle_sync_scrolling():
    """
    Test: Toggle sync scrolling.
    """
    print("=" * 70)
    print("TEST: Toggle Sync Scrolling")
    print("=" * 70)
    
    config = SplitViewConfig()
    engine = SplitViewEngine(config)
    
    result = engine.toggle_sync_scrolling()
    
    assert result.success, "Toggle başarılı olmalı"
    assert engine.config.sync_scrolling == False, "Disabled olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Sync scrolling: {engine.config.sync_scrolling}")
    
    print("\n" + "=" * 70)
    print("PASS: Toggle sync scrolling")
    print("=" * 70)


def test_toggle_sync_cursor():
    """
    Test: Toggle sync cursor.
    """
    print("=" * 70)
    print("TEST: Toggle Sync Cursor")
    print("=" * 70)
    
    config = SplitViewConfig()
    engine = SplitViewEngine(config)
    
    result = engine.toggle_sync_cursor()
    
    assert result.success, "Toggle başarılı olmalı"
    assert engine.config.sync_cursor == True, "Enabled olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Sync cursor: {engine.config.sync_cursor}")
    
    print("\n" + "=" * 70)
    print("PASS: Toggle sync cursor")
    print("=" * 70)


def test_get_all_panes():
    """
    Test: Get all panes.
    """
    print("=" * 70)
    print("TEST: Get All Panes")
    print("=" * 70)
    
    config = SplitViewConfig()
    engine = SplitViewEngine(config)
    
    engine.split_view(SplitDirection.HORIZONTAL, "test.py", "print('hello')")
    
    panes = engine.get_all_panes()
    
    assert len(panes) > 0, "Pane'lar olmalı"
    
    print(f"  Panes: {len(panes)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get all panes")
    print("=" * 70)


def test_get_pane_count():
    """
    Test: Get pane count.
    """
    print("=" * 70)
    print("TEST: Get Pane Count")
    print("=" * 70)
    
    config = SplitViewConfig()
    engine = SplitViewEngine(config)
    
    engine.split_view(SplitDirection.HORIZONTAL, "test.py", "print('hello')")
    engine.split_view(SplitDirection.HORIZONTAL, "test2.py", "print('world')")
    
    count = engine.get_pane_count()
    
    assert count == 2, "Count eşleşmeli"
    
    print(f"  Count: {count}")
    
    print("\n" + "=" * 70)
    print("PASS: Get pane count")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    config = SplitViewConfig()
    engine = SplitViewEngine(config)
    
    new_config = SplitViewConfig(enabled=False)
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
    
    config = SplitViewConfig()
    engine = SplitViewEngine(config)
    
    retrieved_config = engine.get_config()
    
    assert retrieved_config is not None, "Config olmalı"
    assert retrieved_config.enabled == True, "Config eşleşmeli"
    
    print(f"  Enabled: {retrieved_config.enabled}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


def test_split_direction_enum():
    """
    Test: SplitDirection enum.
    """
    print("=" * 70)
    print("TEST: SplitDirection Enum")
    print("=" * 70)
    
    assert SplitDirection.HORIZONTAL.value == "horizontal"
    assert SplitDirection.VERTICAL.value == "vertical"
    
    print(f"  All enum values verified")
    print(f"  Total directions: {len(SplitDirection)}")
    
    print("\n" + "=" * 70)
    print("PASS: SplitDirection enum")
    print("=" * 70)


def test_split_mode_enum():
    """
    Test: SplitMode enum.
    """
    print("=" * 70)
    print("TEST: SplitMode Enum")
    print("=" * 70)
    
    assert SplitMode.SPLIT.value == "split"
    assert SplitMode.UNSPLIT.value == "unsplit"
    assert SplitMode.FOCUS.value == "focus"
    
    print(f"  All enum values verified")
    print(f"  Total modes: {len(SplitMode)}")
    
    print("\n" + "=" * 70)
    print("PASS: SplitMode enum")
    print("=" * 70)


def test_view_pane_dataclass():
    """
    Test: ViewPane dataclass.
    """
    print("=" * 70)
    print("TEST: ViewPane Dataclass")
    print("=" * 70)
    
    pane = ViewPane(
        pane_id="pane_0",
        file_path="test.py",
        content="print('hello')",
        cursor_line=0,
        cursor_column=0,
        is_active=True
    )
    
    assert pane.pane_id == "pane_0", "Pane ID eşleşmeli"
    assert pane.file_path == "test.py", "File path eşleşmeli"
    assert pane.is_active == True, "Active eşleşmeli"
    
    print(f"  Pane ID: {pane.pane_id}")
    print(f"  File path: {pane.file_path}")
    print(f"  Active: {pane.is_active}")
    
    print("\n" + "=" * 70)
    print("PASS: ViewPane dataclass")
    print("=" * 70)


def test_split_view_config_dataclass():
    """
    Test: SplitViewConfig dataclass.
    """
    print("=" * 70)
    print("TEST: SplitViewConfig Dataclass")
    print("=" * 70)
    
    config = SplitViewConfig(
        enabled=True,
        direction=SplitDirection.HORIZONTAL,
        split_ratio=0.5
    )
    
    assert config.enabled == True, "Enabled eşleşmeli"
    assert config.direction == SplitDirection.HORIZONTAL, "Direction eşleşmeli"
    assert config.split_ratio == 0.5, "Ratio eşleşmeli"
    
    print(f"  Enabled: {config.enabled}")
    print(f"  Direction: {config.direction.value}")
    print(f"  Ratio: {config.split_ratio}")
    
    print("\n" + "=" * 70)
    print("PASS: SplitViewConfig dataclass")
    print("=" * 70)


def test_split_view_result_dataclass():
    """
    Test: SplitViewResult dataclass.
    """
    print("=" * 70)
    print("TEST: SplitViewResult Dataclass")
    print("=" * 70)
    
    result = SplitViewResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.panes, list), "Panes list olmalı"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Panes: {len(result.panes)}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: SplitViewResult dataclass")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_split_view()
        test2 = test_unsplit_view()
        test3 = test_focus_pane()
        test4 = test_get_active_pane()
        test5 = test_get_pane_by_id()
        test6 = test_update_pane_content()
        test7 = test_update_pane_cursor()
        test8 = test_update_pane_scroll()
        test9 = test_set_split_direction()
        test10 = test_set_split_ratio()
        test11 = test_toggle_sync_scrolling()
        test12 = test_toggle_sync_cursor()
        test13 = test_get_all_panes()
        test14 = test_get_pane_count()
        test15 = test_update_config()
        test16 = test_get_config()
        test17 = test_split_direction_enum()
        test18 = test_split_mode_enum()
        test19 = test_view_pane_dataclass()
        test20 = test_split_view_config_dataclass()
        test21 = test_split_view_result_dataclass()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Split View: {'PASS' if test1 else 'FAIL'}")
        print(f"Unsplit View: {'PASS' if test2 else 'FAIL'}")
        print(f"Focus Pane: {'PASS' if test3 else 'FAIL'}")
        print(f"Get Active Pane: {'PASS' if test4 else 'FAIL'}")
        print(f"Get Pane By ID: {'PASS' if test5 else 'FAIL'}")
        print(f"Update Pane Content: {'PASS' if test6 else 'FAIL'}")
        print(f"Update Pane Cursor: {'PASS' if test7 else 'FAIL'}")
        print(f"Update Pane Scroll: {'PASS' if test8 else 'FAIL'}")
        print(f"Set Split Direction: {'PASS' if test9 else 'FAIL'}")
        print(f"Set Split Ratio: {'PASS' if test10 else 'FAIL'}")
        print(f"Toggle Sync Scrolling: {'PASS' if test11 else 'FAIL'}")
        print(f"Toggle Sync Cursor: {'PASS' if test12 else 'FAIL'}")
        print(f"Get All Panes: {'PASS' if test13 else 'FAIL'}")
        print(f"Get Pane Count: {'PASS' if test14 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test15 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test16 else 'FAIL'}")
        print(f"SplitDirection Enum: {'PASS' if test17 else 'FAIL'}")
        print(f"SplitMode Enum: {'PASS' if test18 else 'FAIL'}")
        print(f"ViewPane Dataclass: {'PASS' if test19 else 'FAIL'}")
        print(f"SplitViewConfig Dataclass: {'PASS' if test20 else 'FAIL'}")
        print(f"SplitViewResult Dataclass: {'PASS' if test21 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14, test15, test16, test17, test18, test19, test20, test21])
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
