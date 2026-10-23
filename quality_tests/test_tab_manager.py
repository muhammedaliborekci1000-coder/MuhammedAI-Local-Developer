"""
Quality Test: Tab Manager
Tab manager system testleri.
"""

import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from app.editor.tab_manager import (
    TabState,
    TabGroup,
    Tab,
    TabConfig,
    TabManager
)


def test_tab_state_enum():
    """
    Test: TabState enum.
    """
    print("=" * 70)
    print("TEST: TabState Enum")
    print("=" * 70)
    
    assert TabState.ACTIVE.value == "active"
    assert TabState.INACTIVE.value == "inactive"
    assert TabState.MODIFIED.value == "modified"
    assert TabState.PINNED.value == "pinned"
    
    print(f"  All enum values verified")
    print(f"  Total states: {len(TabState)}")
    
    print("\n" + "=" * 70)
    print("PASS: TabState enum")
    print("=" * 70)


def test_tab_group_enum():
    """
    Test: TabGroup enum.
    """
    print("=" * 70)
    print("TEST: TabGroup Enum")
    print("=" * 70)
    
    assert TabGroup.UNGROUPED.value == "ungrouped"
    assert TabGroup.GROUP_1.value == "group_1"
    assert TabGroup.GROUP_2.value == "group_2"
    assert TabGroup.GROUP_3.value == "group_3"
    
    print(f"  All enum values verified")
    print(f"  Total groups: {len(TabGroup)}")
    
    print("\n" + "=" * 70)
    print("PASS: TabGroup enum")
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
        uri="file:///test.py",
        title="test.py"
    )
    
    assert tab.id == "tab_1", "ID eşleşmeli"
    assert tab.uri == "file:///test.py", "URI eşleşmeli"
    assert tab.title == "test.py", "Title eşleşmeli"
    
    print(f"  ID: {tab.id}")
    print(f"  Title: {tab.title}")
    
    print("\n" + "=" * 70)
    print("PASS: Tab dataclass")
    print("=" * 70)


def test_tab_config_dataclass():
    """
    Test: TabConfig dataclass.
    """
    print("=" * 70)
    print("TEST: TabConfig Dataclass")
    print("=" * 70)
    
    config = TabConfig(
        max_tabs=100,
        enable_preview=True
    )
    
    assert config.max_tabs == 100, "Max tabs eşleşmeli"
    assert config.enable_preview == True, "Enable preview eşleşmeli"
    
    print(f"  Max tabs: {config.max_tabs}")
    print(f"  Enable preview: {config.enable_preview}")
    
    print("\n" + "=" * 70)
    print("PASS: TabConfig dataclass")
    print("=" * 70)


def test_tab_manager_initialization():
    """
    Test: TabManager initialization.
    """
    print("=" * 70)
    print("TEST: TabManager Initialization")
    print("=" * 70)
    
    config = TabConfig()
    manager = TabManager(config)
    
    assert manager.config == config, "Config eşleşmeli"
    assert len(manager.tabs) == 0, "Tabs boş olmalı"
    
    print(f"  Tabs: {len(manager.tabs)}")
    
    print("\n" + "=" * 70)
    print("PASS: TabManager initialization")
    print("=" * 70)


def test_add_tab():
    """
    Test: Add tab.
    """
    print("=" * 70)
    print("TEST: Add Tab")
    print("=" * 70)
    
    manager = TabManager()
    
    tab = manager.add_tab("file:///test.py", "test.py", "python")
    
    assert tab is not None, "Tab olmalı"
    assert tab.title == "test.py", "Title eşleşmeli"
    assert len(manager.tabs) == 1, "Tabs sayısı 1 olmalı"
    
    print(f"  Tab: {tab.title}")
    print(f"  Total tabs: {len(manager.tabs)}")
    
    print("\n" + "=" * 70)
    print("PASS: Add tab")
    print("=" * 70)


def test_close_tab():
    """
    Test: Close tab.
    """
    print("=" * 70)
    print("TEST: Close Tab")
    print("=" * 70)
    
    manager = TabManager()
    
    tab = manager.add_tab("file:///test.py", "test.py", "python")
    result = manager.close_tab(tab.id)
    
    assert result == True, "Close başarılı olmalı"
    assert len(manager.tabs) == 0, "Tabs boş olmalı"
    
    print(f"  Tab closed: {tab.title}")
    print(f"  Total tabs: {len(manager.tabs)}")
    
    print("\n" + "=" * 70)
    print("PASS: Close tab")
    print("=" * 70)


def test_activate_tab():
    """
    Test: Activate tab.
    """
    print("=" * 70)
    print("TEST: Activate Tab")
    print("=" * 70)
    
    manager = TabManager()
    
    tab1 = manager.add_tab("file:///test1.py", "test1.py", "python", activate=False)
    tab2 = manager.add_tab("file:///test2.py", "test2.py", "python", activate=True)
    
    result = manager.activate_tab(tab1.id)
    
    assert result == True, "Activate başarılı olmalı"
    assert manager.active_tab_id == tab1.id, "Active tab ID eşleşmeli"
    
    print(f"  Active tab: {manager.get_active_tab().title}")
    
    print("\n" + "=" * 70)
    print("PASS: Activate tab")
    print("=" * 70)


def test_get_tab():
    """
    Test: Get tab.
    """
    print("=" * 70)
    print("TEST: Get Tab")
    print("=" * 70)
    
    manager = TabManager()
    
    tab = manager.add_tab("file:///test.py", "test.py", "python")
    retrieved_tab = manager.get_tab(tab.id)
    
    assert retrieved_tab is not None, "Tab bulunmalı"
    assert retrieved_tab.id == tab.id, "Tab ID eşleşmeli"
    
    print(f"  Tab: {retrieved_tab.title}")
    
    print("\n" + "=" * 70)
    print("PASS: Get tab")
    print("=" * 70)


def test_get_tab_by_uri():
    """
    Test: Get tab by URI.
    """
    print("=" * 70)
    print("TEST: Get Tab by URI")
    print("=" * 70)
    
    manager = TabManager()
    
    tab = manager.add_tab("file:///test.py", "test.py", "python")
    retrieved_tab = manager.get_tab_by_uri("file:///test.py")
    
    assert retrieved_tab is not None, "Tab bulunmalı"
    assert retrieved_tab.uri == "file:///test.py", "URI eşleşmeli"
    
    print(f"  Tab: {retrieved_tab.title}")
    
    print("\n" + "=" * 70)
    print("PASS: Get tab by URI")
    print("=" * 70)


def test_get_active_tab():
    """
    Test: Get active tab.
    """
    print("=" * 70)
    print("TEST: Get Active Tab")
    print("=" * 70)
    
    manager = TabManager()
    
    tab = manager.add_tab("file:///test.py", "test.py", "python")
    active_tab = manager.get_active_tab()
    
    assert active_tab is not None, "Active tab olmalı"
    assert active_tab.id == tab.id, "ID eşleşmeli"
    
    print(f"  Active tab: {active_tab.title}")
    
    print("\n" + "=" * 70)
    print("PASS: Get active tab")
    print("=" * 70)


def test_get_all_tabs():
    """
    Test: Get all tabs.
    """
    print("=" * 70)
    print("TEST: Get All Tabs")
    print("=" * 70)
    
    manager = TabManager()
    
    manager.add_tab("file:///test1.py", "test1.py", "python")
    manager.add_tab("file:///test2.py", "test2.py", "python")
    
    all_tabs = manager.get_all_tabs()
    
    assert len(all_tabs) == 2, "2 tab olmalı"
    
    print(f"  Total tabs: {len(all_tabs)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get all tabs")
    print("=" * 70)


def test_pin_tab():
    """
    Test: Pin tab.
    """
    print("=" * 70)
    print("TEST: Pin Tab")
    print("=" * 70)
    
    manager = TabManager()
    
    tab = manager.add_tab("file:///test.py", "test.py", "python")
    result = manager.pin_tab(tab.id)
    
    assert result == True, "Pin başarılı olmalı"
    assert tab.is_pinned == True, "Pinned olmalı"
    
    print(f"  Tab pinned: {tab.title}")
    
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
    
    manager = TabManager()
    
    tab = manager.add_tab("file:///test.py", "test.py", "python")
    manager.pin_tab(tab.id)
    result = manager.unpin_tab(tab.id)
    
    assert result == True, "Unpin başarılı olmalı"
    assert tab.is_pinned == False, "Unpinned olmalı"
    
    print(f"  Tab unpinned: {tab.title}")
    
    print("\n" + "=" * 70)
    print("PASS: Unpin tab")
    print("=" * 70)


def test_toggle_pin():
    """
    Test: Toggle pin.
    """
    print("=" * 70)
    print("TEST: Toggle Pin")
    print("=" * 70)
    
    manager = TabManager()
    
    tab = manager.add_tab("file:///test.py", "test.py", "python")
    manager.toggle_pin(tab.id)
    
    assert tab.is_pinned == True, "Pinned olmalı"
    
    manager.toggle_pin(tab.id)
    
    assert tab.is_pinned == False, "Unpinned olmalı"
    
    print(f"  Pin toggled: {tab.title}")
    
    print("\n" + "=" * 70)
    print("PASS: Toggle pin")
    print("=" * 70)


def test_set_tab_group():
    """
    Test: Set tab group.
    """
    print("=" * 70)
    print("TEST: Set Tab Group")
    print("=" * 70)
    
    manager = TabManager()
    
    tab = manager.add_tab("file:///test.py", "test.py", "python")
    result = manager.set_tab_group(tab.id, TabGroup.GROUP_1)
    
    assert result == True, "Set group başarılı olmalı"
    assert tab.group == TabGroup.GROUP_1, "Group eşleşmeli"
    
    print(f"  Tab group: {tab.group.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Set tab group")
    print("=" * 70)


def test_move_tab():
    """
    Test: Move tab.
    """
    print("=" * 70)
    print("TEST: Move Tab")
    print("=" * 70)
    
    manager = TabManager()
    
    tab1 = manager.add_tab("file:///test1.py", "test1.py", "python")
    tab2 = manager.add_tab("file:///test2.py", "test2.py", "python")
    
    result = manager.move_tab(tab1.id, 1)
    
    assert result == True, "Move başarılı olmalı"
    assert manager.tabs[1].id == tab1.id, "Tab taşınmalı"
    
    print(f"  Tab moved: {tab1.title}")
    
    print("\n" + "=" * 70)
    print("PASS: Move tab")
    print("=" * 70)


def test_duplicate_tab():
    """
    Test: Duplicate tab.
    """
    print("=" * 70)
    print("TEST: Duplicate Tab")
    print("=" * 70)
    
    manager = TabManager()
    
    tab = manager.add_tab("file:///test.py", "test.py", "python")
    duplicated_tab = manager.duplicate_tab(tab.id)
    
    assert duplicated_tab is not None, "Duplicated tab olmalı"
    assert "Copy" in duplicated_tab.title, "Title 'Copy' içermeli"
    
    print(f"  Duplicated tab: {duplicated_tab.title}")
    
    print("\n" + "=" * 70)
    print("PASS: Duplicate tab")
    print("=" * 70)


def test_mark_modified():
    """
    Test: Mark modified.
    """
    print("=" * 70)
    print("TEST: Mark Modified")
    print("=" * 70)
    
    manager = TabManager()
    
    tab = manager.add_tab("file:///test.py", "test.py", "python")
    result = manager.mark_modified(tab.id)
    
    assert result == True, "Mark modified başarılı olmalı"
    assert tab.state == TabState.MODIFIED, "State MODIFIED olmalı"
    
    print(f"  Tab modified: {tab.title}")
    
    print("\n" + "=" * 70)
    print("PASS: Mark modified")
    print("=" * 70)


def test_mark_saved():
    """
    Test: Mark saved.
    """
    print("=" * 70)
    print("TEST: Mark Saved")
    print("=" * 70)
    
    manager = TabManager()
    
    tab = manager.add_tab("file:///test.py", "test.py", "python")
    manager.mark_modified(tab.id)
    result = manager.mark_saved(tab.id)
    
    assert result == True, "Mark saved başarılı olmalı"
    assert tab.state == TabState.INACTIVE, "State INACTIVE olmalı"
    
    print(f"  Tab saved: {tab.title}")
    
    print("\n" + "=" * 70)
    print("PASS: Mark saved")
    print("=" * 70)


def test_set_cursor_position():
    """
    Test: Set cursor position.
    """
    print("=" * 70)
    print("TEST: Set Cursor Position")
    print("=" * 70)
    
    manager = TabManager()
    
    tab = manager.add_tab("file:///test.py", "test.py", "python")
    result = manager.set_cursor_position(tab.id, 10, 5)
    
    assert result == True, "Set cursor position başarılı olmalı"
    assert tab.cursor_position == (10, 5), "Position eşleşmeli"
    
    print(f"  Cursor position: {tab.cursor_position}")
    
    print("\n" + "=" * 70)
    print("PASS: Set cursor position")
    print("=" * 70)


def test_get_tab_history():
    """
    Test: Get tab history.
    """
    print("=" * 70)
    print("TEST: Get Tab History")
    print("=" * 70)
    
    manager = TabManager()
    
    manager.add_tab("file:///test1.py", "test1.py", "python")
    manager.add_tab("file:///test2.py", "test2.py", "python")
    
    history = manager.get_tab_history()
    
    assert len(history) > 0, "History olmalı"
    
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
    
    manager = TabManager()
    
    manager.add_tab("file:///test1.py", "test1.py", "python")
    manager.clear_history()
    
    history = manager.get_tab_history()
    
    assert len(history) == 0, "History temizlenmeli"
    
    print(f"  History: {len(history)}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear history")
    print("=" * 70)


def test_close_all_tabs():
    """
    Test: Close all tabs.
    """
    print("=" * 70)
    print("TEST: Close All Tabs")
    print("=" * 70)
    
    manager = TabManager()
    
    manager.add_tab("file:///test1.py", "test1.py", "python")
    manager.add_tab("file:///test2.py", "test2.py", "python")
    
    manager.close_all_tabs()
    
    assert len(manager.tabs) == 0, "Tüm tablar kapanmalı"
    
    print(f"  Total tabs: {len(manager.tabs)}")
    
    print("\n" + "=" * 70)
    print("PASS: Close all tabs")
    print("=" * 70)


def test_close_other_tabs():
    """
    Test: Close other tabs.
    """
    print("=" * 70)
    print("TEST: Close Other Tabs")
    print("=" * 70)
    
    manager = TabManager()
    
    tab1 = manager.add_tab("file:///test1.py", "test1.py", "python")
    tab2 = manager.add_tab("file:///test2.py", "test2.py", "python")
    
    result = manager.close_other_tabs(tab1.id)
    
    assert result == True, "Close other tabs başarılı olmalı"
    assert len(manager.tabs) == 1, "Sadece 1 tab kalmalı"
    
    print(f"  Total tabs: {len(manager.tabs)}")
    
    print("\n" + "=" * 70)
    print("PASS: Close other tabs")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    manager = TabManager()
    
    new_config = TabConfig(max_tabs=50)
    manager.update_config(new_config)
    
    assert manager.config.max_tabs == 50, "Config güncellenmeli"
    
    print(f"  Max tabs: {manager.config.max_tabs}")
    
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
    
    config = TabConfig(max_tabs=50)
    manager = TabManager(config)
    
    retrieved_config = manager.get_config()
    
    assert retrieved_config.max_tabs == 50, "Config eşleşmeli"
    
    print(f"  Max tabs: {retrieved_config.max_tabs}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_tab_state_enum()
        test2 = test_tab_group_enum()
        test3 = test_tab_dataclass()
        test4 = test_tab_config_dataclass()
        test5 = test_tab_manager_initialization()
        test6 = test_add_tab()
        test7 = test_close_tab()
        test8 = test_activate_tab()
        test9 = test_get_tab()
        test10 = test_get_tab_by_uri()
        test11 = test_get_active_tab()
        test12 = test_get_all_tabs()
        test13 = test_pin_tab()
        test14 = test_unpin_tab()
        test15 = test_toggle_pin()
        test16 = test_set_tab_group()
        test17 = test_move_tab()
        test18 = test_duplicate_tab()
        test19 = test_mark_modified()
        test20 = test_mark_saved()
        test21 = test_set_cursor_position()
        test22 = test_get_tab_history()
        test23 = test_clear_history()
        test24 = test_close_all_tabs()
        test25 = test_close_other_tabs()
        test26 = test_update_config()
        test27 = test_get_config()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"TabState Enum: {'PASS' if test1 else 'FAIL'}")
        print(f"TabGroup Enum: {'PASS' if test2 else 'FAIL'}")
        print(f"Tab Dataclass: {'PASS' if test3 else 'FAIL'}")
        print(f"TabConfig Dataclass: {'PASS' if test4 else 'FAIL'}")
        print(f"TabManager Initialization: {'PASS' if test5 else 'FAIL'}")
        print(f"Add Tab: {'PASS' if test6 else 'FAIL'}")
        print(f"Close Tab: {'PASS' if test7 else 'FAIL'}")
        print(f"Activate Tab: {'PASS' if test8 else 'FAIL'}")
        print(f"Get Tab: {'PASS' if test9 else 'FAIL'}")
        print(f"Get Tab by URI: {'PASS' if test10 else 'FAIL'}")
        print(f"Get Active Tab: {'PASS' if test11 else 'FAIL'}")
        print(f"Get All Tabs: {'PASS' if test12 else 'FAIL'}")
        print(f"Pin Tab: {'PASS' if test13 else 'FAIL'}")
        print(f"Unpin Tab: {'PASS' if test14 else 'FAIL'}")
        print(f"Toggle Pin: {'PASS' if test15 else 'FAIL'}")
        print(f"Set Tab Group: {'PASS' if test16 else 'FAIL'}")
        print(f"Move Tab: {'PASS' if test17 else 'FAIL'}")
        print(f"Duplicate Tab: {'PASS' if test18 else 'FAIL'}")
        print(f"Mark Modified: {'PASS' if test19 else 'FAIL'}")
        print(f"Mark Saved: {'PASS' if test20 else 'FAIL'}")
        print(f"Set Cursor Position: {'PASS' if test21 else 'FAIL'}")
        print(f"Get Tab History: {'PASS' if test22 else 'FAIL'}")
        print(f"Clear History: {'PASS' if test23 else 'FAIL'}")
        print(f"Close All Tabs: {'PASS' if test24 else 'FAIL'}")
        print(f"Close Other Tabs: {'PASS' if test25 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test26 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test27 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14, test15, test16, test17, test18, test19, test20, test21, test22, test23, test24, test25, test26, test27])
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
