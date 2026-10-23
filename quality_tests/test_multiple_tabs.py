"""
Quality Test: Multiple Tabs
Multiple tabs system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.multiple_tabs import (
    TabManager,
    TabState,
    TabGroup,
    Tab,
    TabsResult
)


def test_create_tab():
    """
    Test: Create tab.
    """
    print("=" * 70)
    print("TEST: Create Tab")
    print("=" * 70)
    
    manager = TabManager()
    result = manager.create_tab("main.py", "def main():\n    pass")
    
    assert result.success, "Creation başarılı olmalı"
    assert len(result.tabs) == 1, "1 tab olmalı"
    assert result.active_tab is not None, "Aktif tab olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Total tabs: {result.total_tabs}")
    print(f"  Active tab: {result.active_tab.title if result.active_tab else None}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Create tab")
    print("=" * 70)


def test_close_tab():
    """
    Test: Close tab.
    """
    print("=" * 70)
    print("TEST: Close Tab")
    print("=" * 70)
    
    manager = TabManager()
    result1 = manager.create_tab("main.py", "def main():\n    pass")
    tab_id = result1.tabs[0].id
    
    result2 = manager.close_tab(tab_id)
    
    assert result2.success, "Closing başarılı olmalı"
    assert len(result2.tabs) == 0, "0 tab olmalı"
    
    print(f"  Success: {result2.success}")
    print(f"  Total tabs: {result2.total_tabs}")
    print(f"  Message: {result2.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Close tab")
    print("=" * 70)


def test_switch_tab():
    """
    Test: Switch tab.
    """
    print("=" * 70)
    print("TEST: Switch Tab")
    print("=" * 70)
    
    manager = TabManager()
    result1 = manager.create_tab("main.py", "def main():\n    pass")
    result2 = manager.create_tab("utils.py", "def helper():\n    pass")
    
    tab_id = result2.tabs[1].id
    result3 = manager.switch_tab(tab_id)
    
    assert result3.success, "Switching başarılı olmalı"
    assert result3.active_tab.id == tab_id, "Aktif tab değişmiş olmalı"
    
    print(f"  Success: {result3.success}")
    print(f"  Active tab: {result3.active_tab.title if result3.active_tab else None}")
    print(f"  Message: {result3.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Switch tab")
    print("=" * 70)


def test_get_active_tab():
    """
    Test: Get active tab.
    """
    print("=" * 70)
    print("TEST: Get Active Tab")
    print("=" * 70)
    
    manager = TabManager()
    manager.create_tab("main.py", "def main():\n    pass")
    
    active_tab = manager.get_active_tab()
    
    assert active_tab is not None, "Aktif tab olmalı"
    assert active_tab.title == "main.py", "Tab başlığı eşleşmeli"
    
    print(f"  Active tab: {active_tab.title}")
    print(f"  State: {active_tab.state.value}")
    
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
    manager.create_tab("main.py", "def main():\n    pass")
    manager.create_tab("utils.py", "def helper():\n    pass")
    
    all_tabs = manager.get_all_tabs()
    
    assert len(all_tabs) == 2, "2 tab olmalı"
    
    print(f"  Total tabs: {len(all_tabs)}")
    print(f"  Tab titles: {[tab.title for tab in all_tabs]}")
    
    print("\n" + "=" * 70)
    print("PASS: Get all tabs")
    print("=" * 70)


def test_get_tabs_by_group():
    """
    Test: Get tabs by group.
    """
    print("=" * 70)
    print("TEST: Get Tabs by Group")
    print("=" * 70)
    
    manager = TabManager()
    manager.create_tab("main.py", "def main():\n    pass", group=TabGroup.EDITORS)
    manager.create_tab("terminal", "bash", group=TabGroup.TERMINALS)
    
    editor_tabs = manager.get_tabs_by_group(TabGroup.EDITORS)
    
    assert len(editor_tabs) == 1, "1 editor tab olmalı"
    
    print(f"  Editor tabs: {len(editor_tabs)}")
    print(f"  Tab titles: {[tab.title for tab in editor_tabs]}")
    
    print("\n" + "=" * 70)
    print("PASS: Get tabs by group")
    print("=" * 70)


def test_update_tab_content():
    """
    Test: Update tab content.
    """
    print("=" * 70)
    print("TEST: Update Tab Content")
    print("=" * 70)
    
    manager = TabManager()
    result1 = manager.create_tab("main.py", "def main():\n    pass")
    tab_id = result1.tabs[0].id
    
    result2 = manager.update_tab_content(tab_id, "def new_main():\n    return 42")
    
    assert result2.success, "Update başarılı olmalı"
    assert result2.tabs[0].is_modified == True, "Modified olmalı"
    
    print(f"  Success: {result2.success}")
    print(f"  Is modified: {result2.tabs[0].is_modified}")
    print(f"  Message: {result2.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Update tab content")
    print("=" * 70)


def test_pin_tab():
    """
    Test: Pin tab.
    """
    print("=" * 70)
    print("TEST: Pin Tab")
    print("=" * 70)
    
    manager = TabManager()
    result1 = manager.create_tab("main.py", "def main():\n    pass")
    tab_id = result1.tabs[0].id
    
    result2 = manager.pin_tab(tab_id)
    
    assert result2.success, "Pinning başarılı olmalı"
    assert result2.tabs[0].is_pinned == True, "Pinned olmalı"
    
    print(f"  Success: {result2.success}")
    print(f"  Is pinned: {result2.tabs[0].is_pinned}")
    print(f"  Message: {result2.message}")
    
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
    result1 = manager.create_tab("main.py", "def main():\n    pass")
    tab_id = result1.tabs[0].id
    
    manager.pin_tab(tab_id)
    result2 = manager.unpin_tab(tab_id)
    
    assert result2.success, "Unpinning başarılı olmalı"
    assert result2.tabs[0].is_pinned == False, "Unpinned olmalı"
    
    print(f"  Success: {result2.success}")
    print(f"  Is pinned: {result2.tabs[0].is_pinned}")
    print(f"  Message: {result2.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Unpin tab")
    print("=" * 70)


def test_set_read_only():
    """
    Test: Set read-only.
    """
    print("=" * 70)
    print("TEST: Set Read-Only")
    print("=" * 70)
    
    manager = TabManager()
    result1 = manager.create_tab("main.py", "def main():\n    pass")
    tab_id = result1.tabs[0].id
    
    result2 = manager.set_read_only(tab_id, read_only=True)
    
    assert result2.success, "Setting read-only başarılı olmalı"
    assert result2.tabs[0].is_read_only == True, "Read-only olmalı"
    
    print(f"  Success: {result2.success}")
    print(f"  Is read-only: {result2.tabs[0].is_read_only}")
    print(f"  Message: {result2.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set read-only")
    print("=" * 70)


def test_update_cursor_position():
    """
    Test: Update cursor position.
    """
    print("=" * 70)
    print("TEST: Update Cursor Position")
    print("=" * 70)
    
    manager = TabManager()
    result1 = manager.create_tab("main.py", "def main():\n    pass")
    tab_id = result1.tabs[0].id
    
    result2 = manager.update_cursor_position(tab_id, line=5, column=10)
    
    assert result2.success, "Update başarılı olmalı"
    assert result2.tabs[0].cursor_position == (5, 10), "Pozisyon eşleşmeli"
    
    print(f"  Success: {result2.success}")
    print(f"  Cursor position: {result2.tabs[0].cursor_position}")
    print(f"  Message: {result2.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Update cursor position")
    print("=" * 70)


def test_search_tabs():
    """
    Test: Search tabs.
    """
    print("=" * 70)
    print("TEST: Search Tabs")
    print("=" * 70)
    
    manager = TabManager()
    manager.create_tab("main.py", "def main():\n    pass")
    manager.create_tab("utils.py", "def helper():\n    pass")
    
    results = manager.search_tabs("main")
    
    assert len(results) == 1, "1 sonuç bulunmalı"
    
    print(f"  Search results: {len(results)}")
    print(f"  Tab titles: {[tab.title for tab in results]}")
    
    print("\n" + "=" * 70)
    print("PASS: Search tabs")
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
    assert TabState.MODIFIED.value == "modified"
    assert TabState.READ_ONLY.value == "read_only"
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
    assert TabGroup.EDITORS.value == "editors"
    assert TabGroup.TERMINALS.value == "terminals"
    assert TabGroup.PREVIEW.value == "preview"
    assert TabGroup.DEBUG.value == "debug"
    
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
        id="tab_0",
        title="main.py",
        content="def main():\n    pass",
        language="python"
    )
    
    assert tab.id == "tab_0", "ID eşleşmeli"
    assert tab.title == "main.py", "Title eşleşmeli"
    assert tab.state == TabState.INACTIVE, "State eşleşmeli"
    
    print(f"  ID: {tab.id}")
    print(f"  Title: {tab.title}")
    print(f"  State: {tab.state.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Tab dataclass")
    print("=" * 70)


def test_tabs_result_dataclass():
    """
    Test: TabsResult dataclass.
    """
    print("=" * 70)
    print("TEST: TabsResult Dataclass")
    print("=" * 70)
    
    result = TabsResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.tabs, list), "Tabs list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Tabs: {len(result.tabs)}")
    
    print("\n" + "=" * 70)
    print("PASS: TabsResult dataclass")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_create_tab()
        test2 = test_close_tab()
        test3 = test_switch_tab()
        test4 = test_get_active_tab()
        test5 = test_get_all_tabs()
        test6 = test_get_tabs_by_group()
        test7 = test_update_tab_content()
        test8 = test_pin_tab()
        test9 = test_unpin_tab()
        test10 = test_set_read_only()
        test11 = test_update_cursor_position()
        test12 = test_search_tabs()
        test13 = test_tab_state_enum()
        test14 = test_tab_group_enum()
        test15 = test_tab_dataclass()
        test16 = test_tabs_result_dataclass()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Create Tab: {'PASS' if test1 else 'FAIL'}")
        print(f"Close Tab: {'PASS' if test2 else 'FAIL'}")
        print(f"Switch Tab: {'PASS' if test3 else 'FAIL'}")
        print(f"Get Active Tab: {'PASS' if test4 else 'FAIL'}")
        print(f"Get All Tabs: {'PASS' if test5 else 'FAIL'}")
        print(f"Get Tabs by Group: {'PASS' if test6 else 'FAIL'}")
        print(f"Update Tab Content: {'PASS' if test7 else 'FAIL'}")
        print(f"Pin Tab: {'PASS' if test8 else 'FAIL'}")
        print(f"Unpin Tab: {'PASS' if test9 else 'FAIL'}")
        print(f"Set Read-Only: {'PASS' if test10 else 'FAIL'}")
        print(f"Update Cursor Position: {'PASS' if test11 else 'FAIL'}")
        print(f"Search Tabs: {'PASS' if test12 else 'FAIL'}")
        print(f"TabState Enum: {'PASS' if test13 else 'FAIL'}")
        print(f"TabGroup Enum: {'PASS' if test14 else 'FAIL'}")
        print(f"Tab Dataclass: {'PASS' if test15 else 'FAIL'}")
        print(f"TabsResult Dataclass: {'PASS' if test16 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14, test15, test16])
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
