"""
Quality Test: Terminal Integration
Terminal integration system testleri.
"""

import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from app.editor.terminal_integration import (
    TerminalType,
    TerminalState,
    TerminalSession,
    TerminalConfig,
    TerminalResult,
    TerminalManager
)


def test_terminal_type_enum():
    """
    Test: TerminalType enum.
    """
    print("=" * 70)
    print("TEST: TerminalType Enum")
    print("=" * 70)
    
    assert TerminalType.COMMAND.value == "command"
    assert TerminalType.POWERSHELL.value == "powershell"
    assert TerminalType.BASH.value == "bash"
    assert TerminalType.ZSH.value == "zsh"
    assert TerminalType.FISH.value == "fish"
    assert TerminalType.PYTHON.value == "python"
    assert TerminalType.NODE.value == "node"
    
    print(f"  All enum values verified")
    print(f"  Total types: {len(TerminalType)}")
    
    print("\n" + "=" * 70)
    print("PASS: TerminalType enum")
    print("=" * 70)


def test_terminal_state_enum():
    """
    Test: TerminalState enum.
    """
    print("=" * 70)
    print("TEST: TerminalState Enum")
    print("=" * 70)
    
    assert TerminalState.IDLE.value == "idle"
    assert TerminalState.RUNNING.value == "running"
    assert TerminalState.PAUSED.value == "paused"
    assert TerminalState.CLOSED.value == "closed"
    
    print(f"  All enum values verified")
    print(f"  Total states: {len(TerminalState)}")
    
    print("\n" + "=" * 70)
    print("PASS: TerminalState enum")
    print("=" * 70)


def test_terminal_session_dataclass():
    """
    Test: TerminalSession dataclass.
    """
    print("=" * 70)
    print("TEST: TerminalSession Dataclass")
    print("=" * 70)
    
    session = TerminalSession(
        id="terminal_1",
        name="Terminal 1",
        terminal_type=TerminalType.COMMAND,
        state=TerminalState.IDLE
    )
    
    assert session.id == "terminal_1", "ID eşleşmeli"
    assert session.name == "Terminal 1", "Name eşleşmeli"
    assert session.terminal_type == TerminalType.COMMAND, "Type eşleşmeli"
    
    print(f"  ID: {session.id}")
    print(f"  Name: {session.name}")
    print(f"  Type: {session.terminal_type.value}")
    
    print("\n" + "=" * 70)
    print("PASS: TerminalSession dataclass")
    print("=" * 70)


def test_terminal_config_dataclass():
    """
    Test: TerminalConfig dataclass.
    """
    print("=" * 70)
    print("TEST: TerminalConfig Dataclass")
    print("=" * 70)
    
    config = TerminalConfig(
        default_type=TerminalType.COMMAND,
        max_history=1000
    )
    
    assert config.default_type == TerminalType.COMMAND, "Default type eşleşmeli"
    assert config.max_history == 1000, "Max history eşleşmeli"
    
    print(f"  Default type: {config.default_type.value}")
    print(f"  Max history: {config.max_history}")
    
    print("\n" + "=" * 70)
    print("PASS: TerminalConfig dataclass")
    print("=" * 70)


def test_terminal_result_dataclass():
    """
    Test: TerminalResult dataclass.
    """
    print("=" * 70)
    print("TEST: TerminalResult Dataclass")
    print("=" * 70)
    
    result = TerminalResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: TerminalResult dataclass")
    print("=" * 70)


def test_terminal_manager_initialization():
    """
    Test: TerminalManager initialization.
    """
    print("=" * 70)
    print("TEST: TerminalManager Initialization")
    print("=" * 70)
    
    config = TerminalConfig()
    manager = TerminalManager(config)
    
    assert manager.config == config, "Config eşleşmeli"
    assert len(manager.sessions) == 0, "Sessions boş olmalı"
    
    print(f"  Sessions: {len(manager.sessions)}")
    
    print("\n" + "=" * 70)
    print("PASS: TerminalManager initialization")
    print("=" * 70)


def test_create_session():
    """
    Test: Create session.
    """
    print("=" * 70)
    print("TEST: Create Session")
    print("=" * 70)
    
    manager = TerminalManager()
    
    result = manager.create_session("Terminal 1", TerminalType.COMMAND)
    
    assert result.success == True, "Creation başarılı olmalı"
    assert result.session is not None, "Session olmalı"
    assert result.session.name == "Terminal 1", "Name eşleşmeli"
    
    print(f"  Session created: {result.session.name}")
    
    print("\n" + "=" * 70)
    print("PASS: Create session")
    print("=" * 70)


def test_close_session():
    """
    Test: Close session.
    """
    print("=" * 70)
    print("TEST: Close Session")
    print("=" * 70)
    
    manager = TerminalManager()
    
    result = manager.create_session("Terminal 1", TerminalType.COMMAND)
    session_id = result.session.id
    
    close_result = manager.close_session(session_id)
    
    assert close_result.success == True, "Close başarılı olmalı"
    assert session_id not in manager.sessions, "Session silinmeli"
    
    print(f"  Session closed: {session_id}")
    
    print("\n" + "=" * 70)
    print("PASS: Close session")
    print("=" * 70)


def test_get_session():
    """
    Test: Get session.
    """
    print("=" * 70)
    print("TEST: Get Session")
    print("=" * 70)
    
    manager = TerminalManager()
    
    result = manager.create_session("Terminal 1", TerminalType.COMMAND)
    session_id = result.session.id
    
    session = manager.get_session(session_id)
    
    assert session is not None, "Session bulunmalı"
    assert session.id == session_id, "ID eşleşmeli"
    
    print(f"  Session found: {session.name}")
    
    print("\n" + "=" * 70)
    print("PASS: Get session")
    print("=" * 70)


def test_get_active_session():
    """
    Test: Get active session.
    """
    print("=" * 70)
    print("TEST: Get Active Session")
    print("=" * 70)
    
    manager = TerminalManager()
    
    manager.create_session("Terminal 1", TerminalType.COMMAND)
    
    active_session = manager.get_active_session()
    
    assert active_session is not None, "Active session olmalı"
    
    print(f"  Active session: {active_session.name}")
    
    print("\n" + "=" * 70)
    print("PASS: Get active session")
    print("=" * 70)


def test_get_all_sessions():
    """
    Test: Get all sessions.
    """
    print("=" * 70)
    print("TEST: Get All Sessions")
    print("=" * 70)
    
    manager = TerminalManager()
    
    manager.create_session("Terminal 1", TerminalType.COMMAND)
    manager.create_session("Terminal 2", TerminalType.POWERSHELL)
    
    all_sessions = manager.get_all_sessions()
    
    assert len(all_sessions) == 2, "2 session olmalı"
    
    print(f"  Total sessions: {len(all_sessions)}")
    
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
    
    manager = TerminalManager()
    
    result1 = manager.create_session("Terminal 1", TerminalType.COMMAND)
    result2 = manager.create_session("Terminal 2", TerminalType.POWERSHELL)
    
    set_result = manager.set_active_session(result1.session.id)
    
    assert set_result.success == True, "Set başarılı olmalı"
    assert manager.active_session_id == result1.session.id, "Active ID eşleşmeli"
    
    print(f"  Active session: {manager.get_active_session().name}")
    
    print("\n" + "=" * 70)
    print("PASS: Set active session")
    print("=" * 70)


def test_execute_command():
    """
    Test: Execute command.
    """
    print("=" * 70)
    print("TEST: Execute Command")
    print("=" * 70)
    
    manager = TerminalManager()
    
    manager.create_session("Terminal 1", TerminalType.COMMAND)
    
    result = manager.execute_command("echo hello")
    
    assert result.success == True, "Execution başarılı olmalı"
    assert result.session is not None, "Session olmalı"
    assert len(result.session.history) > 0, "History olmalı"
    
    print(f"  Command executed: {result.message}")
    print(f"  History: {len(result.session.history)}")
    
    print("\n" + "=" * 70)
    print("PASS: Execute command")
    print("=" * 70)


def test_set_working_directory():
    """
    Test: Set working directory.
    """
    print("=" * 70)
    print("TEST: Set Working Directory")
    print("=" * 70)
    
    manager = TerminalManager()
    
    manager.create_session("Terminal 1", TerminalType.COMMAND)
    
    result = manager.set_working_directory("/home/user")
    
    assert result.success == True, "Set başarılı olmalı"
    assert result.session.working_directory == "/home/user", "Directory eşleşmeli"
    
    print(f"  Working directory: {result.session.working_directory}")
    
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
    
    manager = TerminalManager()
    
    manager.create_session("Terminal 1", TerminalType.COMMAND)
    
    result = manager.set_environment_variable("TEST_VAR", "test_value")
    
    assert result.success == True, "Set başarılı olmalı"
    assert result.session.environment["TEST_VAR"] == "test_value", "Variable eşleşmeli"
    
    print(f"  Environment variable: {result.session.environment}")
    
    print("\n" + "=" * 70)
    print("PASS: Set environment variable")
    print("=" * 70)


def test_get_session_history():
    """
    Test: Get session history.
    """
    print("=" * 70)
    print("TEST: Get Session History")
    print("=" * 70)
    
    manager = TerminalManager()
    
    manager.create_session("Terminal 1", TerminalType.COMMAND)
    manager.execute_command("echo hello")
    manager.execute_command("echo world")
    
    history = manager.get_session_history()
    
    assert len(history) > 0, "History olmalı"
    
    print(f"  History: {len(history)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get session history")
    print("=" * 70)


def test_get_session_output():
    """
    Test: Get session output.
    """
    print("=" * 70)
    print("TEST: Get Session Output")
    print("=" * 70)
    
    manager = TerminalManager()
    
    manager.create_session("Terminal 1", TerminalType.COMMAND)
    manager.execute_command("echo hello")
    
    output = manager.get_session_output()
    
    assert len(output) > 0, "Output olmalı"
    
    print(f"  Output: {len(output)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get session output")
    print("=" * 70)


def test_clear_session_output():
    """
    Test: Clear session output.
    """
    print("=" * 70)
    print("TEST: Clear Session Output")
    print("=" * 70)
    
    manager = TerminalManager()
    
    manager.create_session("Terminal 1", TerminalType.COMMAND)
    manager.execute_command("echo hello")
    
    result = manager.clear_session_output()
    
    assert result.success == True, "Clear başarılı olmalı"
    assert len(result.session.output) == 0, "Output temizlenmeli"
    
    print(f"  Output cleared")
    
    print("\n" + "=" * 70)
    print("PASS: Clear session output")
    print("=" * 70)


def test_clear_session_history():
    """
    Test: Clear session history.
    """
    print("=" * 70)
    print("TEST: Clear Session History")
    print("=" * 70)
    
    manager = TerminalManager()
    
    manager.create_session("Terminal 1", TerminalType.COMMAND)
    manager.execute_command("echo hello")
    
    result = manager.clear_session_history()
    
    assert result.success == True, "Clear başarılı olmalı"
    assert len(result.session.history) == 0, "History temizlenmeli"
    
    print(f"  History cleared")
    
    print("\n" + "=" * 70)
    print("PASS: Clear session history")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    manager = TerminalManager()
    
    new_config = TerminalConfig(max_history=500)
    manager.update_config(new_config)
    
    assert manager.config.max_history == 500, "Config güncellenmeli"
    
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
    
    config = TerminalConfig(max_history=500)
    manager = TerminalManager(config)
    
    retrieved_config = manager.get_config()
    
    assert retrieved_config.max_history == 500, "Config eşleşmeli"
    
    print(f"  Max history: {retrieved_config.max_history}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_terminal_type_enum()
        test2 = test_terminal_state_enum()
        test3 = test_terminal_session_dataclass()
        test4 = test_terminal_config_dataclass()
        test5 = test_terminal_result_dataclass()
        test6 = test_terminal_manager_initialization()
        test7 = test_create_session()
        test8 = test_close_session()
        test9 = test_get_session()
        test10 = test_get_active_session()
        test11 = test_get_all_sessions()
        test12 = test_set_active_session()
        test13 = test_execute_command()
        test14 = test_set_working_directory()
        test15 = test_set_environment_variable()
        test16 = test_get_session_history()
        test17 = test_get_session_output()
        test18 = test_clear_session_output()
        test19 = test_clear_session_history()
        test20 = test_update_config()
        test21 = test_get_config()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"TerminalType Enum: {'PASS' if test1 else 'FAIL'}")
        print(f"TerminalState Enum: {'PASS' if test2 else 'FAIL'}")
        print(f"TerminalSession Dataclass: {'PASS' if test3 else 'FAIL'}")
        print(f"TerminalConfig Dataclass: {'PASS' if test4 else 'FAIL'}")
        print(f"TerminalResult Dataclass: {'PASS' if test5 else 'FAIL'}")
        print(f"TerminalManager Initialization: {'PASS' if test6 else 'FAIL'}")
        print(f"Create Session: {'PASS' if test7 else 'FAIL'}")
        print(f"Close Session: {'PASS' if test8 else 'FAIL'}")
        print(f"Get Session: {'PASS' if test9 else 'FAIL'}")
        print(f"Get Active Session: {'PASS' if test10 else 'FAIL'}")
        print(f"Get All Sessions: {'PASS' if test11 else 'FAIL'}")
        print(f"Set Active Session: {'PASS' if test12 else 'FAIL'}")
        print(f"Execute Command: {'PASS' if test13 else 'FAIL'}")
        print(f"Set Working Directory: {'PASS' if test14 else 'FAIL'}")
        print(f"Set Environment Variable: {'PASS' if test15 else 'FAIL'}")
        print(f"Get Session History: {'PASS' if test16 else 'FAIL'}")
        print(f"Get Session Output: {'PASS' if test17 else 'FAIL'}")
        print(f"Clear Session Output: {'PASS' if test18 else 'FAIL'}")
        print(f"Clear Session History: {'PASS' if test19 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test20 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test21 else 'FAIL'}")
        
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
