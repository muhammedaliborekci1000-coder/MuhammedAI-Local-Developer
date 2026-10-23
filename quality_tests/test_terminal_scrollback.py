"""
Quality Test: Terminal Scrollback
Terminal scrollback system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.tools.terminal_scrollback import (
    TerminalScrollbackEngine,
    ScrollbackMode,
    ScrollbackAction,
    ScrollbackConfig,
    ScrollbackEntry,
    ScrollbackResult
)


def test_add_line():
    """
    Test: Add line.
    """
    print("=" * 70)
    print("TEST: Add Line")
    print("=" * 70)
    
    engine = TerminalScrollbackEngine()
    result = engine.add_line("Test line")
    
    assert result.success, "Ekleme başarılı olmalı"
    assert result.count == 1, "1 satır olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Count: {result.count}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add line")
    print("=" * 70)


def test_add_line_with_details():
    """
    Test: Add line with details.
    """
    print("=" * 70)
    print("TEST: Add Line With Details")
    print("=" * 70)
    
    engine = TerminalScrollbackEngine()
    result = engine.add_line("Test line", panel_id="panel_1", command_id="cmd_1")
    
    assert result.success, "Ekleme başarılı olmalı"
    assert result.entries[0].panel_id == "panel_1", "Panel ID eşleşmeli"
    assert result.entries[0].command_id == "cmd_1", "Command ID eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Panel ID: {result.entries[0].panel_id}")
    print(f"  Command ID: {result.entries[0].command_id}")
    
    print("\n" + "=" * 70)
    print("PASS: Add line with details")
    print("=" * 70)


def test_clear_scrollback():
    """
    Test: Clear scrollback.
    """
    print("=" * 70)
    print("TEST: Clear Scrollback")
    print("=" * 70)
    
    engine = TerminalScrollbackEngine()
    engine.add_line("Line 1")
    engine.add_line("Line 2")
    
    result = engine.clear_scrollback()
    
    assert result.success, "Temizleme başarılı olmalı"
    assert result.count == 0, "Scrollback boş olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear scrollback")
    print("=" * 70)


def test_clear_scrollback_by_panel():
    """
    Test: Clear scrollback by panel.
    """
    print("=" * 70)
    print("TEST: Clear Scrollback By Panel")
    print("=" * 70)
    
    engine = TerminalScrollbackEngine()
    engine.add_line("Line 1", panel_id="panel_1")
    engine.add_line("Line 2", panel_id="panel_2")
    
    result = engine.clear_scrollback(panel_id="panel_1")
    
    assert result.success, "Temizleme başarılı olmalı"
    assert result.count == 1, "1 satır kalmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear scrollback by panel")
    print("=" * 70)


def test_search_scrollback():
    """
    Test: Search scrollback.
    """
    print("=" * 70)
    print("TEST: Search Scrollback")
    print("=" * 70)
    
    engine = TerminalScrollbackEngine()
    engine.add_line("Line 1")
    engine.add_line("Line 2")
    engine.add_line("Test line")
    
    result = engine.search_scrollback("Test")
    
    assert result.success, "Arama başarılı olmalı"
    assert result.count == 1, "1 sonuç bulunmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Count: {result.count}")
    
    print("\n" + "=" * 70)
    print("PASS: Search scrollback")
    print("=" * 70)


def test_search_scrollback_by_panel():
    """
    Test: Search scrollback by panel.
    """
    print("=" * 70)
    print("TEST: Search Scrollback By Panel")
    print("=" * 70)
    
    engine = TerminalScrollbackEngine()
    engine.add_line("Test line", panel_id="panel_1")
    engine.add_line("Test line", panel_id="panel_2")
    
    result = engine.search_scrollback("Test", panel_id="panel_1")
    
    assert result.success, "Arama başarılı olmalı"
    assert result.count == 1, "1 sonuç bulunmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Count: {result.count}")
    
    print("\n" + "=" * 70)
    print("PASS: Search scrollback by panel")
    print("=" * 70)


def test_get_scrollback():
    """
    Test: Get scrollback.
    """
    print("=" * 70)
    print("TEST: Get Scrollback")
    print("=" * 70)
    
    engine = TerminalScrollbackEngine()
    engine.add_line("Line 1")
    engine.add_line("Line 2")
    
    result = engine.get_scrollback()
    
    assert result.success, "Alma başarılı olmalı"
    assert result.count == 2, "2 satır bulunmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Count: {result.count}")
    
    print("\n" + "=" * 70)
    print("PASS: Get scrollback")
    print("=" * 70)


def test_get_scrollback_with_offset():
    """
    Test: Get scrollback with offset.
    """
    print("=" * 70)
    print("TEST: Get Scrollback With Offset")
    print("=" * 70)
    
    engine = TerminalScrollbackEngine()
    engine.add_line("Line 1")
    engine.add_line("Line 2")
    engine.add_line("Line 3")
    
    result = engine.get_scrollback(offset=1, limit=1)
    
    assert result.success, "Alma başarılı olmalı"
    assert result.count == 1, "1 satır bulunmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Count: {result.count}")
    
    print("\n" + "=" * 70)
    print("PASS: Get scrollback with offset")
    print("=" * 70)


def test_get_scrollback_by_panel():
    """
    Test: Get scrollback by panel.
    """
    print("=" * 70)
    print("TEST: Get Scrollback By Panel")
    print("=" * 70)
    
    engine = TerminalScrollbackEngine()
    engine.add_line("Line 1", panel_id="panel_1")
    engine.add_line("Line 2", panel_id="panel_2")
    
    result = engine.get_scrollback_by_panel("panel_1")
    
    assert result.success, "Alma başarılı olmalı"
    assert result.count == 1, "1 satır bulunmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Count: {result.count}")
    
    print("\n" + "=" * 70)
    print("PASS: Get scrollback by panel")
    print("=" * 70)


def test_export_scrollback():
    """
    Test: Export scrollback.
    """
    print("=" * 70)
    print("TEST: Export Scrollback")
    print("=" * 70)
    
    engine = TerminalScrollbackEngine()
    engine.add_line("Line 1")
    
    result = engine.export_scrollback(format="json")
    
    assert result.success, "Dışa aktarma başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Export scrollback")
    print("=" * 70)


def test_import_scrollback():
    """
    Test: Import scrollback.
    """
    print("=" * 70)
    print("TEST: Import Scrollback")
    print("=" * 70)
    
    engine = TerminalScrollbackEngine()
    
    data = [
        {
            "content": "Line 1",
            "panel_id": "panel_1"
        },
        {
            "content": "Line 2",
            "panel_id": "panel_1"
        }
    ]
    
    result = engine.import_scrollback(data)
    
    assert result.success, "İçe aktarma başarılı olmalı"
    assert result.count == 2, "2 satır aktarılmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Count: {result.count}")
    
    print("\n" + "=" * 70)
    print("PASS: Import scrollback")
    print("=" * 70)


def test_get_scrollback_history():
    """
    Test: Get scrollback history.
    """
    print("=" * 70)
    print("TEST: Get Scrollback History")
    print("=" * 70)
    
    engine = TerminalScrollbackEngine()
    engine.add_line("Line 1")
    
    history = engine.get_scrollback_history()
    
    assert len(history) > 0, "Geçmiş olmalı"
    
    print(f"  History: {len(history)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get scrollback history")
    print("=" * 70)


def test_clear_history():
    """
    Test: Clear history.
    """
    print("=" * 70)
    print("TEST: Clear History")
    print("=" * 70)
    
    engine = TerminalScrollbackEngine()
    engine.add_line("Line 1")
    
    result = engine.clear_history()
    
    assert result.success, "Temizleme başarılı olmalı"
    assert len(engine.get_scrollback_history()) == 0, "Geçmiş temizlenmeli"
    
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
    
    engine = TerminalScrollbackEngine()
    
    new_config = ScrollbackConfig(max_lines=500)
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
    
    engine = TerminalScrollbackEngine()
    
    config = engine.get_config()
    
    assert config is not None, "Config olmalı"
    assert config.max_lines == 1000, "Config eşleşmeli"
    
    print(f"  Max lines: {config.max_lines}")
    print(f"  Mode: {config.mode.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


def test_scrollback_mode_enum():
    """
    Test: ScrollbackMode enum.
    """
    print("=" * 70)
    print("TEST: ScrollbackMode Enum")
    print("=" * 70)
    
    assert ScrollbackMode.UNLIMITED.value == "unlimited"
    assert ScrollbackMode.LIMITED.value == "limited"
    assert ScrollbackMode.CIRCULAR.value == "circular"
    
    print(f"  All enum values verified")
    print(f"  Total modes: {len(ScrollbackMode)}")
    
    print("\n" + "=" * 70)
    print("PASS: ScrollbackMode enum")
    print("=" * 70)


def test_scrollback_action_enum():
    """
    Test: ScrollbackAction enum.
    """
    print("=" * 70)
    print("TEST: ScrollbackAction Enum")
    print("=" * 70)
    
    assert ScrollbackAction.ADD.value == "add"
    assert ScrollbackAction.CLEAR.value == "clear"
    assert ScrollbackAction.SEARCH.value == "search"
    assert ScrollbackAction.SAVE.value == "save"
    assert ScrollbackAction.LOAD.value == "load"
    
    print(f"  All enum values verified")
    print(f"  Total actions: {len(ScrollbackAction)}")
    
    print("\n" + "=" * 70)
    print("PASS: ScrollbackAction enum")
    print("=" * 70)


def test_scrollback_config_dataclass():
    """
    Test: ScrollbackConfig dataclass.
    """
    print("=" * 70)
    print("TEST: ScrollbackConfig Dataclass")
    print("=" * 70)
    
    config = ScrollbackConfig(
        max_lines=500,
        mode=ScrollbackMode.UNLIMITED
    )
    
    assert config.max_lines == 500, "Max lines eşleşmeli"
    assert config.mode == ScrollbackMode.UNLIMITED, "Mode eşleşmeli"
    
    print(f"  Max lines: {config.max_lines}")
    print(f"  Mode: {config.mode.value}")
    
    print("\n" + "=" * 70)
    print("PASS: ScrollbackConfig dataclass")
    print("=" * 70)


def test_scrollback_entry_dataclass():
    """
    Test: ScrollbackEntry dataclass.
    """
    print("=" * 70)
    print("TEST: ScrollbackEntry Dataclass")
    print("=" * 70)
    
    entry = ScrollbackEntry(
        id="scrollback_1",
        content="Test line",
        line_number=1,
        timestamp="2024-01-01T00:00:00"
    )
    
    assert entry.id == "scrollback_1", "ID eşleşmeli"
    assert entry.content == "Test line", "İçerik eşleşmeli"
    assert entry.line_number == 1, "Line number eşleşmeli"
    
    print(f"  ID: {entry.id}")
    print(f"  Content: {entry.content}")
    print(f"  Line number: {entry.line_number}")
    
    print("\n" + "=" * 70)
    print("PASS: ScrollbackEntry dataclass")
    print("=" * 70)


def test_scrollback_result_dataclass():
    """
    Test: ScrollbackResult dataclass.
    """
    print("=" * 70)
    print("TEST: ScrollbackResult Dataclass")
    print("=" * 70)
    
    result = ScrollbackResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: ScrollbackResult dataclass")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_add_line()
        test2 = test_add_line_with_details()
        test3 = test_clear_scrollback()
        test4 = test_clear_scrollback_by_panel()
        test5 = test_search_scrollback()
        test6 = test_search_scrollback_by_panel()
        test7 = test_get_scrollback()
        test8 = test_get_scrollback_with_offset()
        test9 = test_get_scrollback_by_panel()
        test10 = test_export_scrollback()
        test11 = test_import_scrollback()
        test12 = test_get_scrollback_history()
        test13 = test_clear_history()
        test14 = test_update_config()
        test15 = test_get_config()
        test16 = test_scrollback_mode_enum()
        test17 = test_scrollback_action_enum()
        test18 = test_scrollback_config_dataclass()
        test19 = test_scrollback_entry_dataclass()
        test20 = test_scrollback_result_dataclass()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Add Line: {'PASS' if test1 else 'FAIL'}")
        print(f"Add Line With Details: {'PASS' if test2 else 'FAIL'}")
        print(f"Clear Scrollback: {'PASS' if test3 else 'FAIL'}")
        print(f"Clear Scrollback By Panel: {'PASS' if test4 else 'FAIL'}")
        print(f"Search Scrollback: {'PASS' if test5 else 'FAIL'}")
        print(f"Search Scrollback By Panel: {'PASS' if test6 else 'FAIL'}")
        print(f"Get Scrollback: {'PASS' if test7 else 'FAIL'}")
        print(f"Get Scrollback With Offset: {'PASS' if test8 else 'FAIL'}")
        print(f"Get Scrollback By Panel: {'PASS' if test9 else 'FAIL'}")
        print(f"Export Scrollback: {'PASS' if test10 else 'FAIL'}")
        print(f"Import Scrollback: {'PASS' if test11 else 'FAIL'}")
        print(f"Get Scrollback History: {'PASS' if test12 else 'FAIL'}")
        print(f"Clear History: {'PASS' if test13 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test14 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test15 else 'FAIL'}")
        print(f"ScrollbackMode Enum: {'PASS' if test16 else 'FAIL'}")
        print(f"ScrollbackAction Enum: {'PASS' if test17 else 'FAIL'}")
        print(f"ScrollbackConfig Dataclass: {'PASS' if test18 else 'FAIL'}")
        print(f"ScrollbackEntry Dataclass: {'PASS' if test19 else 'FAIL'}")
        print(f"ScrollbackResult Dataclass: {'PASS' if test20 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14, test15, test16, test17, test18, test19, test20])
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
