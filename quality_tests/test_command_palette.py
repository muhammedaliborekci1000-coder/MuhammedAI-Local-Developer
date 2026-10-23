"""
Quality Test: Command Palette
Command palette system testleri.
"""

import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from app.editor.command_palette import (
    CommandType,
    Command,
    CommandPaletteConfig,
    CommandPaletteResult,
    CommandPaletteEngine
)


def test_command_type_enum():
    """
    Test: CommandType enum.
    """
    print("=" * 70)
    print("TEST: CommandType Enum")
    print("=" * 70)
    
    assert CommandType.FILE.value == "file"
    assert CommandType.EDIT.value == "edit"
    assert CommandType.VIEW.value == "view"
    assert CommandType.NAVIGATION.value == "navigation"
    assert CommandType.SEARCH.value == "search"
    assert CommandType.TOOLS.value == "tools"
    assert CommandType.PREFERENCES.value == "preferences"
    assert CommandType.CUSTOM.value == "custom"
    
    print(f"  All enum values verified")
    print(f"  Total types: {len(CommandType)}")
    
    print("\n" + "=" * 70)
    print("PASS: CommandType enum")
    print("=" * 70)


def test_command_dataclass():
    """
    Test: Command dataclass.
    """
    print("=" * 70)
    print("TEST: Command Dataclass")
    print("=" * 70)
    
    command = Command(
        id="test.command",
        title="Test Command",
        type=CommandType.TOOLS,
        description="Test description",
        shortcut="Ctrl+T",
        category="Tools"
    )
    
    assert command.id == "test.command", "ID eşleşmeli"
    assert command.title == "Test Command", "Title eşleşmeli"
    assert command.type == CommandType.TOOLS, "Type eşleşmeli"
    
    print(f"  ID: {command.id}")
    print(f"  Title: {command.title}")
    print(f"  Type: {command.type.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Command dataclass")
    print("=" * 70)


def test_command_palette_config_dataclass():
    """
    Test: CommandPaletteConfig dataclass.
    """
    print("=" * 70)
    print("TEST: CommandPaletteConfig Dataclass")
    print("=" * 70)
    
    config = CommandPaletteConfig(
        max_results=10,
        fuzzy_search=True
    )
    
    assert config.max_results == 10, "Max results eşleşmeli"
    assert config.fuzzy_search == True, "Fuzzy search eşleşmeli"
    
    print(f"  Max results: {config.max_results}")
    print(f"  Fuzzy search: {config.fuzzy_search}")
    
    print("\n" + "=" * 70)
    print("PASS: CommandPaletteConfig dataclass")
    print("=" * 70)


def test_command_palette_result_dataclass():
    """
    Test: CommandPaletteResult dataclass.
    """
    print("=" * 70)
    print("TEST: CommandPaletteResult Dataclass")
    print("=" * 70)
    
    result = CommandPaletteResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.commands, list), "Commands list olmalı"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Commands: {len(result.commands)}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: CommandPaletteResult dataclass")
    print("=" * 70)


def test_command_palette_engine_initialization():
    """
    Test: CommandPaletteEngine initialization.
    """
    print("=" * 70)
    print("TEST: CommandPaletteEngine Initialization")
    print("=" * 70)
    
    config = CommandPaletteConfig()
    engine = CommandPaletteEngine(config)
    
    assert engine.config == config, "Config eşleşmeli"
    assert len(engine.commands) > 0, "Commands olmalı"
    
    print(f"  Commands: {len(engine.commands)}")
    
    print("\n" + "=" * 70)
    print("PASS: CommandPaletteEngine initialization")
    print("=" * 70)


def test_register_command():
    """
    Test: Register command.
    """
    print("=" * 70)
    print("TEST: Register Command")
    print("=" * 70)
    
    engine = CommandPaletteEngine()
    
    command = Command(
        id="test.custom",
        title="Custom Command",
        type=CommandType.CUSTOM,
        description="Custom description"
    )
    
    result = engine.register_command(command)
    
    assert result == True, "Registration başarılı olmalı"
    assert "test.custom" in engine.commands, "Command kaydedilmeli"
    
    print(f"  Command registered: {command.title}")
    
    print("\n" + "=" * 70)
    print("PASS: Register command")
    print("=" * 70)


def test_unregister_command():
    """
    Test: Unregister command.
    """
    print("=" * 70)
    print("TEST: Unregister Command")
    print("=" * 70)
    
    engine = CommandPaletteEngine()
    
    command = Command(
        id="test.custom",
        title="Custom Command",
        type=CommandType.CUSTOM
    )
    
    engine.register_command(command)
    result = engine.unregister_command("test.custom")
    
    assert result == True, "Unregistration başarılı olmalı"
    assert "test.custom" not in engine.commands, "Command silinmeli"
    
    print(f"  Command unregistered: {command.title}")
    
    print("\n" + "=" * 70)
    print("PASS: Unregister command")
    print("=" * 70)


def test_get_command():
    """
    Test: Get command.
    """
    print("=" * 70)
    print("TEST: Get Command")
    print("=" * 70)
    
    engine = CommandPaletteEngine()
    
    command = engine.get_command("file.save")
    
    assert command is not None, "Command bulunmalı"
    assert command.id == "file.save", "ID eşleşmeli"
    
    print(f"  Command: {command.title}")
    
    print("\n" + "=" * 70)
    print("PASS: Get command")
    print("=" * 70)


def test_get_all_commands():
    """
    Test: Get all commands.
    """
    print("=" * 70)
    print("TEST: Get All Commands")
    print("=" * 70)
    
    engine = CommandPaletteEngine()
    
    all_commands = engine.get_all_commands()
    
    assert len(all_commands) > 0, "Commands olmalı"
    
    print(f"  Total commands: {len(all_commands)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get all commands")
    print("=" * 70)


def test_get_commands_by_type():
    """
    Test: Get commands by type.
    """
    print("=" * 70)
    print("TEST: Get Commands by Type")
    print("=" * 70)
    
    engine = CommandPaletteEngine()
    
    file_commands = engine.get_commands_by_type(CommandType.FILE)
    
    assert len(file_commands) > 0, "File commands olmalı"
    
    print(f"  File commands: {len(file_commands)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get commands by type")
    print("=" * 70)


def test_get_commands_by_category():
    """
    Test: Get commands by category.
    """
    print("=" * 70)
    print("TEST: Get Commands by Category")
    print("=" * 70)
    
    engine = CommandPaletteEngine()
    
    file_commands = engine.get_commands_by_category("File")
    
    assert len(file_commands) > 0, "File commands olmalı"
    
    print(f"  File commands: {len(file_commands)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get commands by category")
    print("=" * 70)


def test_search_commands():
    """
    Test: Search commands.
    """
    print("=" * 70)
    print("TEST: Search Commands")
    print("=" * 70)
    
    engine = CommandPaletteEngine()
    
    result = engine.search_commands("save")
    
    assert result.success == True, "Search başarılı olmalı"
    assert len(result.commands) > 0, "Commands bulunmalı"
    
    print(f"  Commands found: {len(result.commands)}")
    
    print("\n" + "=" * 70)
    print("PASS: Search commands")
    print("=" * 70)


def test_execute_command():
    """
    Test: Execute command.
    """
    print("=" * 70)
    print("TEST: Execute Command")
    print("=" * 70)
    
    engine = CommandPaletteEngine()
    
    result = engine.execute_command("file.save")
    
    assert result.success == True, "Execution başarılı olmalı"
    assert result.selected_command is not None, "Selected command olmalı"
    
    print(f"  Command executed: {result.selected_command.title}")
    
    print("\n" + "=" * 70)
    print("PASS: Execute command")
    print("=" * 70)


def test_get_recent_commands():
    """
    Test: Get recent commands.
    """
    print("=" * 70)
    print("TEST: Get Recent Commands")
    print("=" * 70)
    
    engine = CommandPaletteEngine()
    
    # Execute some commands
    engine.execute_command("file.save")
    engine.execute_command("file.new")
    
    recent = engine.get_recent_commands()
    
    assert len(recent) > 0, "Recent commands olmalı"
    
    print(f"  Recent commands: {len(recent)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get recent commands")
    print("=" * 70)


def test_get_command_history():
    """
    Test: Get command history.
    """
    print("=" * 70)
    print("TEST: Get Command History")
    print("=" * 70)
    
    engine = CommandPaletteEngine()
    
    # Execute some commands
    engine.execute_command("file.save")
    engine.execute_command("file.new")
    
    history = engine.get_command_history()
    
    assert len(history) > 0, "History olmalı"
    
    print(f"  History: {len(history)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get command history")
    print("=" * 70)


def test_clear_history():
    """
    Test: Clear history.
    """
    print("=" * 70)
    print("TEST: Clear History")
    print("=" * 70)
    
    engine = CommandPaletteEngine()
    
    # Execute some commands
    engine.execute_command("file.save")
    engine.execute_command("file.new")
    
    engine.clear_history()
    
    history = engine.get_command_history()
    recent = engine.get_recent_commands()
    
    assert len(history) == 0, "History temizlenmeli"
    assert len(recent) == 0, "Recent temizlenmeli"
    
    print(f"  History cleared")
    
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
    
    engine = CommandPaletteEngine()
    
    new_config = CommandPaletteConfig(max_results=20)
    engine.update_config(new_config)
    
    assert engine.config.max_results == 20, "Config güncellenmeli"
    
    print(f"  Max results: {engine.config.max_results}")
    
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
    
    config = CommandPaletteConfig(max_results=20)
    engine = CommandPaletteEngine(config)
    
    retrieved_config = engine.get_config()
    
    assert retrieved_config.max_results == 20, "Config eşleşmeli"
    
    print(f"  Max results: {retrieved_config.max_results}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_command_type_enum()
        test2 = test_command_dataclass()
        test3 = test_command_palette_config_dataclass()
        test4 = test_command_palette_result_dataclass()
        test5 = test_command_palette_engine_initialization()
        test6 = test_register_command()
        test7 = test_unregister_command()
        test8 = test_get_command()
        test9 = test_get_all_commands()
        test10 = test_get_commands_by_type()
        test11 = test_get_commands_by_category()
        test12 = test_search_commands()
        test13 = test_execute_command()
        test14 = test_get_recent_commands()
        test15 = test_get_command_history()
        test16 = test_clear_history()
        test17 = test_update_config()
        test18 = test_get_config()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"CommandType Enum: {'PASS' if test1 else 'FAIL'}")
        print(f"Command Dataclass: {'PASS' if test2 else 'FAIL'}")
        print(f"CommandPaletteConfig Dataclass: {'PASS' if test3 else 'FAIL'}")
        print(f"CommandPaletteResult Dataclass: {'PASS' if test4 else 'FAIL'}")
        print(f"CommandPaletteEngine Initialization: {'PASS' if test5 else 'FAIL'}")
        print(f"Register Command: {'PASS' if test6 else 'FAIL'}")
        print(f"Unregister Command: {'PASS' if test7 else 'FAIL'}")
        print(f"Get Command: {'PASS' if test8 else 'FAIL'}")
        print(f"Get All Commands: {'PASS' if test9 else 'FAIL'}")
        print(f"Get Commands by Type: {'PASS' if test10 else 'FAIL'}")
        print(f"Get Commands by Category: {'PASS' if test11 else 'FAIL'}")
        print(f"Search Commands: {'PASS' if test12 else 'FAIL'}")
        print(f"Execute Command: {'PASS' if test13 else 'FAIL'}")
        print(f"Get Recent Commands: {'PASS' if test14 else 'FAIL'}")
        print(f"Get Command History: {'PASS' if test15 else 'FAIL'}")
        print(f"Clear History: {'PASS' if test16 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test17 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test18 else 'FAIL'}")
        
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
