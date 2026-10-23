"""
Quality Test: Terminal History
Terminal history system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.tools.terminal_history import (
    TerminalHistoryEngine,
    HistoryAction,
    HistoryConfig,
    HistoryEntry,
    HistoryResult
)


def test_add_command():
    """
    Test: Add command.
    """
    print("=" * 70)
    print("TEST: Add Command")
    print("=" * 70)
    
    engine = TerminalHistoryEngine()
    result = engine.add_command("ls -la", "panel_1")
    
    assert result.success, "Ekleme başarılı olmalı"
    assert result.entry is not None, "Entry olmalı"
    assert result.entry.command == "ls -la", "Komut eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Command: {result.entry.command}")
    print(f"  Count: {result.count}")
    
    print("\n" + "=" * 70)
    print("PASS: Add command")
    print("=" * 70)


def test_add_command_with_details():
    """
    Test: Add command with details.
    """
    print("=" * 70)
    print("TEST: Add Command With Details")
    print("=" * 70)
    
    engine = TerminalHistoryEngine()
    result = engine.add_command(
        "python test.py",
        "panel_1",
        exit_code=0,
        duration=1.5,
        working_directory="/path/to/project"
    )
    
    assert result.success, "Ekleme başarılı olmalı"
    assert result.entry.exit_code == 0, "Exit code eşleşmeli"
    assert result.entry.duration == 1.5, "Süre eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Exit code: {result.entry.exit_code}")
    print(f"  Duration: {result.entry.duration}")
    
    print("\n" + "=" * 70)
    print("PASS: Add command with details")
    print("=" * 70)


def test_remove_command():
    """
    Test: Remove command.
    """
    print("=" * 70)
    print("TEST: Remove Command")
    print("=" * 70)
    
    engine = TerminalHistoryEngine()
    add_result = engine.add_command("ls -la", "panel_1")
    
    result = engine.remove_command(add_result.entry.id)
    
    assert result.success, "Silme başarılı olmalı"
    assert engine.get_all_history().count == 0, "Geçmiş boş olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Remove command")
    print("=" * 70)


def test_clear_history():
    """
    Test: Clear history.
    """
    print("=" * 70)
    print("TEST: Clear History")
    print("=" * 70)
    
    engine = TerminalHistoryEngine()
    engine.add_command("ls -la", "panel_1")
    engine.add_command("pwd", "panel_1")
    
    result = engine.clear_history()
    
    assert result.success, "Temizleme başarılı olmalı"
    assert result.count == 0, "Geçmiş boş olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear history")
    print("=" * 70)


def test_clear_history_by_panel():
    """
    Test: Clear history by panel.
    """
    print("=" * 70)
    print("TEST: Clear History By Panel")
    print("=" * 70)
    
    engine = TerminalHistoryEngine()
    engine.add_command("ls -la", "panel_1")
    engine.add_command("pwd", "panel_2")
    
    result = engine.clear_history(panel_id="panel_1")
    
    assert result.success, "Temizleme başarılı olmalı"
    assert result.count == 1, "1 entry kalmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear history by panel")
    print("=" * 70)


def test_search_history():
    """
    Test: Search history.
    """
    print("=" * 70)
    print("TEST: Search History")
    print("=" * 70)
    
    engine = TerminalHistoryEngine()
    engine.add_command("ls -la", "panel_1")
    engine.add_command("pwd", "panel_1")
    engine.add_command("ls -la /home", "panel_1")
    
    result = engine.search_history("ls")
    
    assert result.success, "Arama başarılı olmalı"
    assert result.count == 2, "2 sonuç bulunmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Count: {result.count}")
    
    print("\n" + "=" * 70)
    print("PASS: Search history")
    print("=" * 70)


def test_search_history_by_panel():
    """
    Test: Search history by panel.
    """
    print("=" * 70)
    print("TEST: Search History By Panel")
    print("=" * 70)
    
    engine = TerminalHistoryEngine()
    engine.add_command("ls -la", "panel_1")
    engine.add_command("ls -la", "panel_2")
    
    result = engine.search_history("ls", panel_id="panel_1")
    
    assert result.success, "Arama başarılı olmalı"
    assert result.count == 1, "1 sonuç bulunmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Count: {result.count}")
    
    print("\n" + "=" * 70)
    print("PASS: Search history by panel")
    print("=" * 70)


def test_get_history_by_panel():
    """
    Test: Get history by panel.
    """
    print("=" * 70)
    print("TEST: Get History By Panel")
    print("=" * 70)
    
    engine = TerminalHistoryEngine()
    engine.add_command("ls -la", "panel_1")
    engine.add_command("pwd", "panel_2")
    
    result = engine.get_history_by_panel("panel_1")
    
    assert result.success, "Alma başarılı olmalı"
    assert result.count == 1, "1 entry bulunmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Count: {result.count}")
    
    print("\n" + "=" * 70)
    print("PASS: Get history by panel")
    print("=" * 70)


def test_get_recent_commands():
    """
    Test: Get recent commands.
    """
    print("=" * 70)
    print("TEST: Get Recent Commands")
    print("=" * 70)
    
    engine = TerminalHistoryEngine()
    engine.add_command("cmd1", "panel_1")
    engine.add_command("cmd2", "panel_1")
    engine.add_command("cmd3", "panel_1")
    
    result = engine.get_recent_commands(limit=2)
    
    assert result.success, "Alma başarılı olmalı"
    assert result.count == 2, "2 entry bulunmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Count: {result.count}")
    
    print("\n" + "=" * 70)
    print("PASS: Get recent commands")
    print("=" * 70)


def test_get_frequent_commands():
    """
    Test: Get frequent commands.
    """
    print("=" * 70)
    print("TEST: Get Frequent Commands")
    print("=" * 70)
    
    engine = TerminalHistoryEngine()
    engine.add_command("ls -la", "panel_1")
    engine.add_command("ls -la", "panel_1")
    engine.add_command("pwd", "panel_1")
    
    result = engine.get_frequent_commands(limit=2)
    
    assert result.success, "Alma başarılı olmalı"
    assert result.count > 0, "En az 1 entry bulunmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Count: {result.count}")
    
    print("\n" + "=" * 70)
    print("PASS: Get frequent commands")
    print("=" * 70)


def test_get_all_history():
    """
    Test: Get all history.
    """
    print("=" * 70)
    print("TEST: Get All History")
    print("=" * 70)
    
    engine = TerminalHistoryEngine()
    engine.add_command("cmd1", "panel_1")
    engine.add_command("cmd2", "panel_1")
    
    result = engine.get_all_history()
    
    assert result.success, "Alma başarılı olmalı"
    assert result.count == 2, "2 entry bulunmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Count: {result.count}")
    
    print("\n" + "=" * 70)
    print("PASS: Get all history")
    print("=" * 70)


def test_export_history():
    """
    Test: Export history.
    """
    print("=" * 70)
    print("TEST: Export History")
    print("=" * 70)
    
    engine = TerminalHistoryEngine()
    engine.add_command("ls -la", "panel_1")
    
    result = engine.export_history(format="json")
    
    assert result.success, "Dışa aktarma başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Export history")
    print("=" * 70)


def test_import_history():
    """
    Test: Import history.
    """
    print("=" * 70)
    print("TEST: Import History")
    print("=" * 70)
    
    engine = TerminalHistoryEngine()
    
    data = [
        {
            "command": "ls -la",
            "panel_id": "panel_1",
            "timestamp": "2024-01-01T00:00:00"
        },
        {
            "command": "pwd",
            "panel_id": "panel_1",
            "timestamp": "2024-01-01T00:00:01"
        }
    ]
    
    result = engine.import_history(data)
    
    assert result.success, "İçe aktarma başarılı olmalı"
    assert result.count == 2, "2 entry aktarılmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Count: {result.count}")
    
    print("\n" + "=" * 70)
    print("PASS: Import history")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    engine = TerminalHistoryEngine()
    
    new_config = HistoryConfig(max_entries=500)
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
    
    engine = TerminalHistoryEngine()
    
    config = engine.get_config()
    
    assert config is not None, "Config olmalı"
    assert config.max_entries == 1000, "Config eşleşmeli"
    
    print(f"  Max entries: {config.max_entries}")
    print(f"  Persist to disk: {config.persist_to_disk}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


def test_history_action_enum():
    """
    Test: HistoryAction enum.
    """
    print("=" * 70)
    print("TEST: HistoryAction Enum")
    print("=" * 70)
    
    assert HistoryAction.ADD.value == "add"
    assert HistoryAction.REMOVE.value == "remove"
    assert HistoryAction.CLEAR.value == "clear"
    assert HistoryAction.SEARCH.value == "search"
    assert HistoryAction.EXPORT.value == "export"
    assert HistoryAction.IMPORT.value == "import"
    
    print(f"  All enum values verified")
    print(f"  Total actions: {len(HistoryAction)}")
    
    print("\n" + "=" * 70)
    print("PASS: HistoryAction enum")
    print("=" * 70)


def test_history_config_dataclass():
    """
    Test: HistoryConfig dataclass.
    """
    print("=" * 70)
    print("TEST: HistoryConfig Dataclass")
    print("=" * 70)
    
    config = HistoryConfig(
        max_entries=500,
        persist_to_disk=True
    )
    
    assert config.max_entries == 500, "Max entries eşleşmeli"
    assert config.persist_to_disk == True, "Persist to disk eşleşmeli"
    
    print(f"  Max entries: {config.max_entries}")
    print(f"  Persist to disk: {config.persist_to_disk}")
    
    print("\n" + "=" * 70)
    print("PASS: HistoryConfig dataclass")
    print("=" * 70)


def test_history_entry_dataclass():
    """
    Test: HistoryEntry dataclass.
    """
    print("=" * 70)
    print("TEST: HistoryEntry Dataclass")
    print("=" * 70)
    
    entry = HistoryEntry(
        id="history_1",
        command="ls -la",
        panel_id="panel_1",
        timestamp="2024-01-01T00:00:00"
    )
    
    assert entry.id == "history_1", "ID eşleşmeli"
    assert entry.command == "ls -la", "Komut eşleşmeli"
    assert entry.panel_id == "panel_1", "Panel ID eşleşmeli"
    
    print(f"  ID: {entry.id}")
    print(f"  Command: {entry.command}")
    print(f"  Panel ID: {entry.panel_id}")
    
    print("\n" + "=" * 70)
    print("PASS: HistoryEntry dataclass")
    print("=" * 70)


def test_history_result_dataclass():
    """
    Test: HistoryResult dataclass.
    """
    print("=" * 70)
    print("TEST: HistoryResult Dataclass")
    print("=" * 70)
    
    result = HistoryResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: HistoryResult dataclass")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_add_command()
        test2 = test_add_command_with_details()
        test3 = test_remove_command()
        test4 = test_clear_history()
        test5 = test_clear_history_by_panel()
        test6 = test_search_history()
        test7 = test_search_history_by_panel()
        test8 = test_get_history_by_panel()
        test9 = test_get_recent_commands()
        test10 = test_get_frequent_commands()
        test11 = test_get_all_history()
        test12 = test_export_history()
        test13 = test_import_history()
        test14 = test_update_config()
        test15 = test_get_config()
        test16 = test_history_action_enum()
        test17 = test_history_config_dataclass()
        test18 = test_history_entry_dataclass()
        test19 = test_history_result_dataclass()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Add Command: {'PASS' if test1 else 'FAIL'}")
        print(f"Add Command With Details: {'PASS' if test2 else 'FAIL'}")
        print(f"Remove Command: {'PASS' if test3 else 'FAIL'}")
        print(f"Clear History: {'PASS' if test4 else 'FAIL'}")
        print(f"Clear History By Panel: {'PASS' if test5 else 'FAIL'}")
        print(f"Search History: {'PASS' if test6 else 'FAIL'}")
        print(f"Search History By Panel: {'PASS' if test7 else 'FAIL'}")
        print(f"Get History By Panel: {'PASS' if test8 else 'FAIL'}")
        print(f"Get Recent Commands: {'PASS' if test9 else 'FAIL'}")
        print(f"Get Frequent Commands: {'PASS' if test10 else 'FAIL'}")
        print(f"Get All History: {'PASS' if test11 else 'FAIL'}")
        print(f"Export History: {'PASS' if test12 else 'FAIL'}")
        print(f"Import History: {'PASS' if test13 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test14 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test15 else 'FAIL'}")
        print(f"HistoryAction Enum: {'PASS' if test16 else 'FAIL'}")
        print(f"HistoryConfig Dataclass: {'PASS' if test17 else 'FAIL'}")
        print(f"HistoryEntry Dataclass: {'PASS' if test18 else 'FAIL'}")
        print(f"HistoryResult Dataclass: {'PASS' if test19 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14, test15, test16, test17, test18, test19])
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
