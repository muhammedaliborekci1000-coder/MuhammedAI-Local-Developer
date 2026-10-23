"""
Quality Test: Terminal Tabs
Terminal tabs system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.tools.terminal_tabs import (
    TerminalTabsEngine,
    TabState,
    TabAction,
    TabConfig,
    Tab,
    TabResult
)


def test_create_tab():
    """
    Test: Create tab.
    """
    print("=" * 70)
    print("TEST: Create Tab")
    print("=" * 70)
    
    engine = TerminalTabsEngine()
    result = engine.create_tab("Test Tab")
    
    assert result.success, "Oluşturma başarılı olmalı"
    assert result.tab is not None, "Tab olmalı"
    assert result.tab.name == "Test Tab", "İsim eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Tab ID: {result.tab_id}")
    print(f"  Tab name: {result.tab.name}")
    
    print("\n" + "=" * 70)
    print("PASS: Create tab")
    print("=" * 70)


def test_create_tab_with_details():
    """
    Test: Create tab with details.
    """
    print("=" * 70)
    print("TEST: Create Tab With Details")
    print("=" * 70)
    
    engine = TerminalTabsEngine()
    result = engine.create_tab(
        "Test Tab",
        shell="cmd",
        working_directory="/path/to/project"
    )
    
    assert result.success, "Oluşturma başarılı olmalı"
    assert result.tab.shell == "cmd", "Shell eşleşmeli"
    assert result.tab.working_directory == "/path/to/project", "Working directory eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Shell: {result.tab.shell}")
    print(f"  Working directory: {result.tab.working_directory}")
    
    print("\n" + "=" * 70)
    print("PASS: Create tab with details")
    print("=" * 70)


def test_close_tab():
    """
    Test: Close tab.
    """
    print("=" * 70)
    print("TEST: Close Tab")
    print("=" * 70)
    
    engine = TerminalTabsEngine()
    create_result = engine.create_tab("Test Tab")
    
    result = engine.close_tab(create_result.tab_id)
    
    assert result.success, "Kapatma başarılı olmalı"
    assert engine.get_tab(create_result.tab_id) is None, "Tab silinmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Close tab")
    print("=" * 70)


def test_rename_tab():
    """
    Test: Rename tab.
    """
    print("=" * 70)
    print("TEST: Rename Tab")
    print("=" * 70)
    
    engine = TerminalTabsEngine()
    create_result = engine.create_tab("Test Tab")
    
    result = engine.rename_tab(create_result.tab_id, "Renamed Tab")
    
    assert result.success, "Yeniden adlandırma başarılı olmalı"
    assert result.tab.name == "Renamed Tab", "İsim değişmeli"
    
    print(f"  Success: {result.success}")
    print(f"  New name: {result.tab.name}")
    
    print("\n" + "=" * 70)
    print("PASS: Rename tab")
    print("=" * 70)


def test_focus_tab():
    """
    Test: Focus tab.
    """
    print("=" * 70)
    print("TEST: Focus Tab")
    print("=" * 70)
    
    engine = TerminalTabsEngine()
    create_result = engine.create_tab("Test Tab")
    
    result = engine.focus_tab(create_result.tab_id)
    
    assert result.success, "Odaklama başarılı olmalı"
    assert result.tab.state == TabState.ACTIVE, "Durum active olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  State: {result.tab.state.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Focus tab")
    print("=" * 70)


def test_move_tab():
    """
    Test: Move tab.
    """
    print("=" * 70)
    print("TEST: Move Tab")
    print("=" * 70)
    
    engine = TerminalTabsEngine()
    engine.create_tab("Tab 1")
    create_result = engine.create_tab("Tab 2")
    
    result = engine.move_tab(create_result.tab_id, 0)
    
    assert result.success, "Taşıma başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Move tab")
    print("=" * 70)


def test_pin_tab():
    """
    Test: Pin tab.
    """
    print("=" * 70)
    print("TEST: Pin Tab")
    print("=" * 70)
    
    engine = TerminalTabsEngine()
    create_result = engine.create_tab("Test Tab")
    
    result = engine.pin_tab(create_result.tab_id)
    
    assert result.success, "Sabitleme başarılı olmalı"
    assert result.tab.is_pinned == True, "Sabitlenmiş olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Is pinned: {result.tab.is_pinned}")
    
    print("\n" + "=" * 70)
    print("PASS: Pin tab")
    print("=" * 70)


def test_unpin_tab():
    """
    Test: Unpin tab.
    """
    print("=" * 70)
    print("TEST: Unpin Tab")
    print("=" * 70)
    
    engine = TerminalTabsEngine()
    create_result = engine.create_tab("Test Tab")
    engine.pin_tab(create_result.tab_id)
    
    result = engine.unpin_tab(create_result.tab_id)
    
    assert result.success, "Sabitleme kaldırma başarılı olmalı"
    assert result.tab.is_pinned == False, "Sabitlenmemiş olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Is pinned: {result.tab.is_pinned}")
    
    print("\n" + "=" * 70)
    print("PASS: Unpin tab")
    print("=" * 70)


def test_duplicate_tab():
    """
    Test: Duplicate tab.
    """
    print("=" * 70)
    print("TEST: Duplicate Tab")
    print("=" * 70)
    
    engine = TerminalTabsEngine()
    create_result = engine.create_tab("Test Tab")
    
    result = engine.duplicate_tab(create_result.tab_id)
    
    assert result.success, "Kopyalama başarılı olmalı"
    assert result.tab is not None, "Yeni tab olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  New tab ID: {result.tab_id}")
    
    print("\n" + "=" * 70)
    print("PASS: Duplicate tab")
    print("=" * 70)


def test_get_tab():
    """
    Test: Get tab.
    """
    print("=" * 70)
    print("TEST: Get Tab")
    print("=" * 70)
    
    engine = TerminalTabsEngine()
    create_result = engine.create_tab("Test Tab")
    
    tab = engine.get_tab(create_result.tab_id)
    
    assert tab is not None, "Tab olmalı"
    assert tab.name == "Test Tab", "İsim eşleşmeli"
    
    print(f"  Tab: {tab.name}")
    print(f"  State: {tab.state.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Get tab")
    print("=" * 70)


def test_get_all_tabs():
    """
    Test: Get all tabs.
    """
    print("=" * 70)
    print("TEST: Get All Tabs")
    print("=" * 70)
    
    engine = TerminalTabsEngine()
    engine.create_tab("Tab 1")
    engine.create_tab("Tab 2")
    
    tabs = engine.get_all_tabs()
    
    assert len(tabs) == 2, "2 tab olmalı"
    
    print(f"  Tab count: {len(tabs)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get all tabs")
    print("=" * 70)


def test_get_active_tab():
    """
    Test: Get active tab.
    """
    print("=" * 70)
    print("TEST: Get Active Tab")
    print("=" * 70)
    
    engine = TerminalTabsEngine()
    create_result = engine.create_tab("Test Tab")
    
    active_tab = engine.get_active_tab()
    
    assert active_tab is not None, "Aktif tab olmalı"
    assert active_tab.id == create_result.tab_id, "ID eşleşmeli"
    
    print(f"  Active tab: {active_tab.name}")
    
    print("\n" + "=" * 70)
    print("PASS: Get active tab")
    print("=" * 70)


def test_get_pinned_tabs():
    """
    Test: Get pinned tabs.
    """
    print("=" * 70)
    print("TEST: Get Pinned Tabs")
    print("=" * 70)
    
    engine = TerminalTabsEngine()
    create_result = engine.create_tab("Test Tab")
    engine.pin_tab(create_result.tab_id)
    
    pinned_tabs = engine.get_pinned_tabs()
    
    assert len(pinned_tabs) == 1, "1 sabitlenmiş tab olmalı"
    
    print(f"  Pinned tab count: {len(pinned_tabs)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get pinned tabs")
    print("=" * 70)


def test_get_tab_history():
    """
    Test: Get tab history.
    """
    print("=" * 70)
    print("TEST: Get Tab History")
    print("=" * 70)
    
    engine = TerminalTabsEngine()
    engine.create_tab("Test Tab")
    
    history = engine.get_tab_history()
    
    assert len(history) > 0, "Geçmiş olmalı"
    
    print(f"  History: {len(history)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get tab history")
    print("=" * 70)


def test_clear_history():
    """
    Test: Clear history.
    """
    print("=" * 70)
    print("TEST: Clear History")
    print("=" * 70)
    
    engine = TerminalTabsEngine()
    engine.create_tab("Test Tab")
    
    result = engine.clear_history()
    
    assert result.success, "Temizleme başarılı olmalı"
    assert len(engine.get_tab_history()) == 0, "Geçmiş temizlenmeli"
    
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
    
    engine = TerminalTabsEngine()
    
    new_config = TabConfig(shell="cmd")
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
    
    engine = TerminalTabsEngine()
    
    config = engine.get_config()
    
    assert config is not None, "Config olmalı"
    assert config.shell == "powershell", "Config eşleşmeli"
    
    print(f"  Shell: {config.shell}")
    print(f"  Font size: {config.font_size}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


def test_tab_state_enum():
    """
    Test: TabState enum.
    """
    print("=" * 70)
    print("TEST: TabState Enum")
    print("=" * 70)
    
    assert TabState.ACTIVE.value == "active"
    assert TabState.INACTIVE.value == "inactive"
    assert TabState.BUSY.value == "busy"
    assert TabState.ERROR.value == "error"
    
    print(f"  All enum values verified")
    print(f"  Total states: {len(TabState)}")
    
    print("\n" + "=" * 70)
    print("PASS: TabState enum")
    print("=" * 70)


def test_tab_action_enum():
    """
    Test: TabAction enum.
    """
    print("=" * 70)
    print("TEST: TabAction Enum")
    print("=" * 70)
    
    assert TabAction.CREATE.value == "create"
    assert TabAction.CLOSE.value == "close"
    assert TabAction.RENAME.value == "rename"
    assert TabAction.FOCUS.value == "focus"
    assert TabAction.MOVE.value == "move"
    assert TabAction.PIN.value == "pin"
    assert TabAction.UNPIN.value == "unpin"
    assert TabAction.DUPLICATE.value == "duplicate"
    
    print(f"  All enum values verified")
    print(f"  Total actions: {len(TabAction)}")
    
    print("\n" + "=" * 70)
    print("PASS: TabAction enum")
    print("=" * 70)


def test_tab_config_dataclass():
    """
    Test: TabConfig dataclass.
    """
    print("=" * 70)
    print("TEST: TabConfig Dataclass")
    print("=" * 70)
    
    config = TabConfig(
        shell="cmd",
        font_size=16
    )
    
    assert config.shell == "cmd", "Shell eşleşmeli"
    assert config.font_size == 16, "Font size eşleşmeli"
    
    print(f"  Shell: {config.shell}")
    print(f"  Font size: {config.font_size}")
    
    print("\n" + "=" * 70)
    print("PASS: TabConfig dataclass")
    print("=" * 70)


def test_tab_dataclass():
    """
    Test: Tab dataclass.
    """
    print("=" * 70)
    print("TEST: Tab Dataclass")
    print("=" * 70)
    
    tab = Tab(
        id="tab_1",
        name="Test Tab",
        state=TabState.ACTIVE,
        shell="powershell",
        working_directory="/path/to/project",
        theme="default",
        font_family="Consolas",
        font_size=14,
        is_pinned=False,
        created_at="2024-01-01T00:00:00",
        last_activity="2024-01-01T00:00:00"
    )
    
    assert tab.id == "tab_1", "ID eşleşmeli"
    assert tab.name == "Test Tab", "İsim eşleşmeli"
    assert tab.state == TabState.ACTIVE, "Durum eşleşmeli"
    
    print(f"  ID: {tab.id}")
    print(f"  Name: {tab.name}")
    print(f"  State: {tab.state.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Tab dataclass")
    print("=" * 70)


def test_tab_result_dataclass():
    """
    Test: TabResult dataclass.
    """
    print("=" * 70)
    print("TEST: TabResult Dataclass")
    print("=" * 70)
    
    result = TabResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: TabResult dataclass")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_create_tab()
        test2 = test_create_tab_with_details()
        test3 = test_close_tab()
        test4 = test_rename_tab()
        test5 = test_focus_tab()
        test6 = test_move_tab()
        test7 = test_pin_tab()
        test8 = test_unpin_tab()
        test9 = test_duplicate_tab()
        test10 = test_get_tab()
        test11 = test_get_all_tabs()
        test12 = test_get_active_tab()
        test13 = test_get_pinned_tabs()
        test14 = test_get_tab_history()
        test15 = test_clear_history()
        test16 = test_update_config()
        test17 = test_get_config()
        test18 = test_tab_state_enum()
        test19 = test_tab_action_enum()
        test20 = test_tab_config_dataclass()
        test21 = test_tab_dataclass()
        test22 = test_tab_result_dataclass()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Create Tab: {'PASS' if test1 else 'FAIL'}")
        print(f"Create Tab With Details: {'PASS' if test2 else 'FAIL'}")
        print(f"Close Tab: {'PASS' if test3 else 'FAIL'}")
        print(f"Rename Tab: {'PASS' if test4 else 'FAIL'}")
        print(f"Focus Tab: {'PASS' if test5 else 'FAIL'}")
        print(f"Move Tab: {'PASS' if test6 else 'FAIL'}")
        print(f"Pin Tab: {'PASS' if test7 else 'FAIL'}")
        print(f"Unpin Tab: {'PASS' if test8 else 'FAIL'}")
        print(f"Duplicate Tab: {'PASS' if test9 else 'FAIL'}")
        print(f"Get Tab: {'PASS' if test10 else 'FAIL'}")
        print(f"Get All Tabs: {'PASS' if test11 else 'FAIL'}")
        print(f"Get Active Tab: {'PASS' if test12 else 'FAIL'}")
        print(f"Get Pinned Tabs: {'PASS' if test13 else 'FAIL'}")
        print(f"Get Tab History: {'PASS' if test14 else 'FAIL'}")
        print(f"Clear History: {'PASS' if test15 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test16 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test17 else 'FAIL'}")
        print(f"TabState Enum: {'PASS' if test18 else 'FAIL'}")
        print(f"TabAction Enum: {'PASS' if test19 else 'FAIL'}")
        print(f"TabConfig Dataclass: {'PASS' if test20 else 'FAIL'}")
        print(f"Tab Dataclass: {'PASS' if test21 else 'FAIL'}")
        print(f"TabResult Dataclass: {'PASS' if test22 else 'FAIL'}")
        
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
