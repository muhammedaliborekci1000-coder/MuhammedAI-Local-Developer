"""
Quality Test: Terminal UI
Terminal UI system testleri for UI module.
"""

import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from app.ui.terminal_ui import (
    TerminalMode,
    TerminalTheme,
    ShellType,
    TerminalSession,
    TerminalOutput,
    TerminalUIConfig,
    TerminalUIResult,
    TerminalUIManager
)
from datetime import datetime


def test_terminal_mode_enum():
    """
    Test: TerminalMode enum.
    """
    print("=" * 70)
    print("TEST: TerminalMode Enum")
    print("=" * 70)
    
    assert TerminalMode.NORMAL.value == "normal"
    assert TerminalMode.INSERT.value == "insert"
    assert TerminalMode.VISUAL.value == "visual"
    assert TerminalMode.COMMAND.value == "command"
    assert TerminalMode.CUSTOM.value == "custom"
    
    print(f"  All enum values verified")
    print(f"  Total modes: {len(TerminalMode)}")
    
    print("\n" + "=" * 70)
    print("PASS: TerminalMode enum")
    print("=" * 70)


def test_terminal_theme_enum():
    """
    Test: TerminalTheme enum.
    """
    print("=" * 70)
    print("TEST: TerminalTheme Enum")
    print("=" * 70)
    
    assert TerminalTheme.LIGHT.value == "light"
    assert TerminalTheme.DARK.value == "dark"
    assert TerminalTheme.HIGH_CONTRAST.value == "high_contrast"
    assert TerminalTheme.SOLARIZED.value == "solarized"
    assert TerminalTheme.DRACULA.value == "dracula"
    assert TerminalTheme.MONOKAI.value == "monokai"
    assert TerminalTheme.CUSTOM.value == "custom"
    
    print(f"  All enum values verified")
    print(f"  Total themes: {len(TerminalTheme)}")
    
    print("\n" + "=" * 70)
    print("PASS: TerminalTheme enum")
    print("=" * 70)


def test_shell_type_enum():
    """
    Test: ShellType enum.
    """
    print("=" * 70)
    print("TEST: ShellType Enum")
    print("=" * 70)
    
    assert ShellType.BASH.value == "bash"
    assert ShellType.ZSH.value == "zsh"
    assert ShellType.FISH.value == "fish"
    assert ShellType.POWERSHELL.value == "powershell"
    assert ShellType.CMD.value == "cmd"
    assert ShellType.SH.value == "sh"
    assert ShellType.CUSTOM.value == "custom"
    
    print(f"  All enum values verified")
    print(f"  Total types: {len(ShellType)}")
    
    print("\n" + "=" * 70)
    print("PASS: ShellType enum")
    print("=" * 70)


def test_terminal_session_dataclass():
    """
    Test: TerminalSession dataclass.
    """
    print("=" * 70)
    print("TEST: TerminalSession Dataclass")
    print("=" * 70)
    
    session = TerminalSession(
        id="session_1",
        title="Terminal 1",
        shell_type=ShellType.BASH,
        working_directory="/home",
        created_at=datetime.now()
    )
    
    assert session.id == "session_1", "ID eşleşmeli"
    assert session.title == "Terminal 1", "Title eşleşmeli"
    assert session.shell_type == ShellType.BASH, "Shell type eşleşmeli"
    assert session.working_directory == "/home", "Working directory eşleşmeli"
    
    print(f"  ID: {session.id}")
    print(f"  Title: {session.title}")
    print(f"  Shell: {session.shell_type.value}")
    
    print("\n" + "=" * 70)
    print("PASS: TerminalSession dataclass")
    print("=" * 70)


def test_terminal_output_dataclass():
    """
    Test: TerminalOutput dataclass.
    """
    print("=" * 70)
    print("TEST: TerminalOutput Dataclass")
    print("=" * 70)
    
    output = TerminalOutput(
        id="output_1",
        session_id="session_1",
        content="Hello World",
        timestamp=datetime.now()
    )
    
    assert output.id == "output_1", "ID eşleşmeli"
    assert output.session_id == "session_1", "Session ID eşleşmeli"
    assert output.content == "Hello World", "Content eşleşmeli"
    
    print(f"  ID: {output.id}")
    print(f"  Session ID: {output.session_id}")
    print(f"  Content: {output.content}")
    
    print("\n" + "=" * 70)
    print("PASS: TerminalOutput dataclass")
    print("=" * 70)


def test_terminal_ui_config_dataclass():
    """
    Test: TerminalUIConfig dataclass.
    """
    print("=" * 70)
    print("TEST: TerminalUIConfig Dataclass")
    print("=" * 70)
    
    config = TerminalUIConfig(
        enabled=True,
        show_line_numbers=False
    )
    
    assert config.enabled == True, "Enabled eşleşmeli"
    assert config.show_line_numbers == False, "Show line numbers eşleşmeli"
    
    print(f"  Enabled: {config.enabled}")
    print(f"  Show line numbers: {config.show_line_numbers}")
    
    print("\n" + "=" * 70)
    print("PASS: TerminalUIConfig dataclass")
    print("=" * 70)


def test_terminal_ui_result_dataclass():
    """
    Test: TerminalUIResult dataclass.
    """
    print("=" * 70)
    print("TEST: TerminalUIResult Dataclass")
    print("=" * 70)
    
    result = TerminalUIResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.sessions, list), "Sessions list olmalı"
    assert isinstance(result.outputs, list), "Outputs list olmalı"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Sessions: {len(result.sessions)}")
    print(f"  Outputs: {len(result.outputs)}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: TerminalUIResult dataclass")
    print("=" * 70)


def test_terminal_ui_manager_initialization():
    """
    Test: TerminalUIManager initialization.
    """
    print("=" * 70)
    print("TEST: TerminalUIManager Initialization")
    print("=" * 70)
    
    config = TerminalUIConfig()
    manager = TerminalUIManager(config)
    
    assert manager.config == config, "Config eşleşmeli"
    assert len(manager.sessions) == 0, "Sessions boş olmalı"
    assert manager.active_session_id is None, "Active session None olmalı"
    
    print(f"  Sessions: {len(manager.sessions)}")
    print(f"  Active session: {manager.active_session_id}")
    
    print("\n" + "=" * 70)
    print("PASS: TerminalUIManager initialization")
    print("=" * 70)


def test_create_session():
    """
    Test: Create session.
    """
    print("=" * 70)
    print("TEST: Create Session")
    print("=" * 70)
    
    manager = TerminalUIManager()
    
    result = manager.create_session("Terminal 1", ShellType.BASH, "/home")
    
    assert result.success == True, "Oluşturma başarılı olmalı"
    assert result.session is not None, "Session olmalı"
    assert len(manager.sessions) > 0, "Session eklenmeli"
    
    print(f"  Session created: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Create session")
    print("=" * 70)


def test_delete_session():
    """
    Test: Delete session.
    """
    print("=" * 70)
    print("TEST: Delete Session")
    print("=" * 70)
    
    manager = TerminalUIManager()
    
    result = manager.create_session("Terminal 1", ShellType.BASH, "/home")
    session_id = result.session.id
    
    result = manager.delete_session(session_id)
    
    assert result.success == True, "Silme başarılı olmalı"
    assert session_id not in manager.sessions, "Session silinmeli"
    
    print(f"  Session deleted: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Delete session")
    print("=" * 70)


def test_get_session():
    """
    Test: Get session.
    """
    print("=" * 70)
    print("TEST: Get Session")
    print("=" * 70)
    
    manager = TerminalUIManager()
    
    result = manager.create_session("Terminal 1", ShellType.BASH, "/home")
    session_id = result.session.id
    
    retrieved_session = manager.get_session(session_id)
    
    assert retrieved_session is not None, "Session bulunmalı"
    assert retrieved_session.id == session_id, "ID eşleşmeli"
    
    print(f"  Session: {retrieved_session.title}")
    
    print("\n" + "=" * 70)
    print("PASS: Get session")
    print("=" * 70)


def test_get_all_sessions():
    """
    Test: Get all sessions.
    """
    print("=" * 70)
    print("TEST: Get All Sessions")
    print("=" * 70)
    
    manager = TerminalUIManager()
    
    manager.create_session("Terminal 1", ShellType.BASH, "/home")
    manager.create_session("Terminal 2", ShellType.ZSH, "/home")
    
    sessions = manager.get_all_sessions()
    
    assert len(sessions) == 2, "2 session olmalı"
    
    print(f"  Total sessions: {len(sessions)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get all sessions")
    print("=" * 70)


def test_set_active_session():
    """
    Test: Set active session.
    """
    print("=" * 70)
    print("TEST: Set Active Session")
    print("=" * 70)
    
    manager = TerminalUIManager()
    
    result = manager.create_session("Terminal 1", ShellType.BASH, "/home")
    session_id = result.session.id
    
    result = manager.set_active_session(session_id)
    
    assert result.success == True, "Set başarılı olmalı"
    assert manager.active_session_id == session_id, "Active session eşleşmeli"
    
    print(f"  Active session set: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set active session")
    print("=" * 70)


def test_add_output():
    """
    Test: Add output.
    """
    print("=" * 70)
    print("TEST: Add Output")
    print("=" * 70)
    
    manager = TerminalUIManager()
    
    manager.create_session("Terminal 1", ShellType.BASH, "/home")
    
    result = manager.add_output("Hello World!")
    
    assert result.success == True, "Ekleme başarılı olmalı"
    assert result.output is not None, "Output olmalı"
    
    print(f"  Output added: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add output")
    print("=" * 70)


def test_get_outputs():
    """
    Test: Get outputs.
    """
    print("=" * 70)
    print("TEST: Get Outputs")
    print("=" * 70)
    
    manager = TerminalUIManager()
    
    manager.create_session("Terminal 1", ShellType.BASH, "/home")
    manager.add_output("Hello World!")
    
    outputs = manager.get_outputs()
    
    assert len(outputs) > 0, "Outputs olmalı"
    
    print(f"  Total outputs: {len(outputs)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get outputs")
    print("=" * 70)


def test_add_command_to_history():
    """
    Test: Add command to history.
    """
    print("=" * 70)
    print("TEST: Add Command to History")
    print("=" * 70)
    
    manager = TerminalUIManager()
    
    manager.create_session("Terminal 1", ShellType.BASH, "/home")
    
    result = manager.add_command_to_history("ls -la")
    
    assert result.success == True, "Ekleme başarılı olmalı"
    
    print(f"  Command added: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add command to history")
    print("=" * 70)


def test_get_history():
    """
    Test: Get history.
    """
    print("=" * 70)
    print("TEST: Get History")
    print("=" * 70)
    
    manager = TerminalUIManager()
    
    manager.create_session("Terminal 1", ShellType.BASH, "/home")
    manager.add_command_to_history("ls -la")
    
    history = manager.get_history()
    
    assert len(history) > 0, "History olmalı"
    
    print(f"  Total history: {len(history)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get history")
    print("=" * 70)


def test_set_working_directory():
    """
    Test: Set working directory.
    """
    print("=" * 70)
    print("TEST: Set Working Directory")
    print("=" * 70)
    
    manager = TerminalUIManager()
    
    manager.create_session("Terminal 1", ShellType.BASH, "/home")
    
    result = manager.set_working_directory("/home/user")
    
    assert result.success == True, "Set başarılı olmalı"
    
    print(f"  Working directory set: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set working directory")
    print("=" * 70)


def test_set_environment_variable():
    """
    Test: Set environment variable.
    """
    print("=" * 70)
    print("TEST: Set Environment Variable")
    print("=" * 70)
    
    manager = TerminalUIManager()
    
    manager.create_session("Terminal 1", ShellType.BASH, "/home")
    
    result = manager.set_environment_variable("PATH", "/usr/bin")
    
    assert result.success == True, "Set başarılı olmalı"
    
    print(f"  Environment variable set: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set environment variable")
    print("=" * 70)


def test_clear_outputs():
    """
    Test: Clear outputs.
    """
    print("=" * 70)
    print("TEST: Clear Outputs")
    print("=" * 70)
    
    manager = TerminalUIManager()
    
    manager.create_session("Terminal 1", ShellType.BASH, "/home")
    manager.add_output("Hello World!")
    
    result = manager.clear_outputs()
    
    assert result.success == True, "Clear başarılı olmalı"
    
    outputs = manager.get_outputs()
    assert len(outputs) == 0, "Outputs temizlenmeli"
    
    print(f"  Outputs cleared: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear outputs")
    print("=" * 70)


def test_clear_history():
    """
    Test: Clear history.
    """
    print("=" * 70)
    print("TEST: Clear History")
    print("=" * 70)
    
    manager = TerminalUIManager()
    
    manager.create_session("Terminal 1", ShellType.BASH, "/home")
    manager.add_command_to_history("ls -la")
    
    result = manager.clear_history()
    
    assert result.success == True, "Clear başarılı olmalı"
    
    history = manager.get_history()
    assert len(history) == 0, "History temizlenmeli"
    
    print(f"  History cleared: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear history")
    print("=" * 70)


def test_set_theme():
    """
    Test: Set theme.
    """
    print("=" * 70)
    print("TEST: Set Theme")
    print("=" * 70)
    
    manager = TerminalUIManager()
    
    result = manager.set_theme(TerminalTheme.LIGHT)
    
    assert result.success == True, "Set başarılı olmalı"
    assert manager.config.theme == TerminalTheme.LIGHT, "Theme eşleşmeli"
    
    print(f"  Theme set: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set theme")
    print("=" * 70)


def test_set_font_size():
    """
    Test: Set font size.
    """
    print("=" * 70)
    print("TEST: Set Font Size")
    print("=" * 70)
    
    manager = TerminalUIManager()
    
    result = manager.set_font_size(16)
    
    assert result.success == True, "Set başarılı olmalı"
    assert manager.config.font_size == 16, "Font size eşleşmeli"
    
    print(f"  Font size set: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set font size")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    manager = TerminalUIManager()
    
    new_config = TerminalUIConfig(max_history=2000)
    result = manager.update_config(new_config)
    
    assert result.success == True, "Update başarılı olmalı"
    assert manager.config.max_history == 2000, "Config güncellenmeli"
    
    print(f"  Max history: {manager.config.max_history}")
    
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
    
    config = TerminalUIConfig(max_history=2000)
    manager = TerminalUIManager(config)
    
    retrieved_config = manager.get_config()
    
    assert retrieved_config.max_history == 2000, "Config eşleşmeli"
    
    print(f"  Max history: {retrieved_config.max_history}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_terminal_mode_enum()
        test2 = test_terminal_theme_enum()
        test3 = test_shell_type_enum()
        test4 = test_terminal_session_dataclass()
        test5 = test_terminal_output_dataclass()
        test6 = test_terminal_ui_config_dataclass()
        test7 = test_terminal_ui_result_dataclass()
        test8 = test_terminal_ui_manager_initialization()
        test9 = test_create_session()
        test10 = test_delete_session()
        test11 = test_get_session()
        test12 = test_get_all_sessions()
        test13 = test_set_active_session()
        test14 = test_add_output()
        test15 = test_get_outputs()
        test16 = test_add_command_to_history()
        test17 = test_get_history()
        test18 = test_set_working_directory()
        test19 = test_set_environment_variable()
        test20 = test_clear_outputs()
        test21 = test_clear_history()
        test22 = test_set_theme()
        test23 = test_set_font_size()
        test24 = test_update_config()
        test25 = test_get_config()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"TerminalMode Enum: {'PASS' if test1 else 'FAIL'}")
        print(f"TerminalTheme Enum: {'PASS' if test2 else 'FAIL'}")
        print(f"ShellType Enum: {'PASS' if test3 else 'FAIL'}")
        print(f"TerminalSession Dataclass: {'PASS' if test4 else 'FAIL'}")
        print(f"TerminalOutput Dataclass: {'PASS' if test5 else 'FAIL'}")
        print(f"TerminalUIConfig Dataclass: {'PASS' if test6 else 'FAIL'}")
        print(f"TerminalUIResult Dataclass: {'PASS' if test7 else 'FAIL'}")
        print(f"TerminalUIManager Initialization: {'PASS' if test8 else 'FAIL'}")
        print(f"Create Session: {'PASS' if test9 else 'FAIL'}")
        print(f"Delete Session: {'PASS' if test10 else 'FAIL'}")
        print(f"Get Session: {'PASS' if test11 else 'FAIL'}")
        print(f"Get All Sessions: {'PASS' if test12 else 'FAIL'}")
        print(f"Set Active Session: {'PASS' if test13 else 'FAIL'}")
        print(f"Add Output: {'PASS' if test14 else 'FAIL'}")
        print(f"Get Outputs: {'PASS' if test15 else 'FAIL'}")
        print(f"Add Command to History: {'PASS' if test16 else 'FAIL'}")
        print(f"Get History: {'PASS' if test17 else 'FAIL'}")
        print(f"Set Working Directory: {'PASS' if test18 else 'FAIL'}")
        print(f"Set Environment Variable: {'PASS' if test19 else 'FAIL'}")
        print(f"Clear Outputs: {'PASS' if test20 else 'FAIL'}")
        print(f"Clear History: {'PASS' if test21 else 'FAIL'}")
        print(f"Set Theme: {'PASS' if test22 else 'FAIL'}")
        print(f"Set Font Size: {'PASS' if test23 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test24 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test25 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14, test15, test16, test17, test18, test19, test20, test21, test22, test23, test24, test25])
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
