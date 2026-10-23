"""
Quality Test: Terminal Restart
Terminal restart system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.tools.terminal_restart import (
    TerminalRestartEngine,
    RestartMode,
    RestartScope,
    RestartConfig,
    RestartEntry,
    RestartResult
)


def test_add_terminal():
    """
    Test: Add terminal.
    """
    print("=" * 70)
    print("TEST: Add Terminal")
    print("=" * 70)
    
    engine = TerminalRestartEngine()
    terminal = engine.add_terminal("test command", "/home/user")
    
    assert terminal.id == "terminal_0", "ID eşleşmeli"
    assert terminal.command == "test command", "Komut eşleşmeli"
    assert terminal.working_directory == "/home/user", "Dizin eşleşmeli"
    
    print(f"  ID: {terminal.id}")
    print(f"  Command: {terminal.command}")
    print(f"  Working directory: {terminal.working_directory}")
    
    print("\n" + "=" * 70)
    print("PASS: Add terminal")
    print("=" * 70)


def test_restart_terminal():
    """
    Test: Restart terminal.
    """
    print("=" * 70)
    print("TEST: Restart Terminal")
    print("=" * 70)
    
    engine = TerminalRestartEngine()
    terminal = engine.add_terminal("test command", "/home/user")
    
    result = engine.restart_terminal(terminal.id)
    
    assert result.success, "Yeniden başlatma başarılı olmalı"
    assert result.restart_id is not None, "Restart ID olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Restart ID: {result.restart_id}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Restart terminal")
    print("=" * 70)


def test_restart_with_mode():
    """
    Test: Restart with mode.
    """
    print("=" * 70)
    print("TEST: Restart With Mode")
    print("=" * 70)
    
    engine = TerminalRestartEngine()
    terminal = engine.add_terminal("test command", "/home/user")
    
    result = engine.restart_terminal(terminal.id, RestartMode.FORCE)
    
    assert result.success, "Yeniden başlatma başarılı olmalı"
    assert result.mode == RestartMode.FORCE.value, "Mod eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Mode: {result.mode}")
    
    print("\n" + "=" * 70)
    print("PASS: Restart with mode")
    print("=" * 70)


def test_restart_with_command():
    """
    Test: Restart with command.
    """
    print("=" * 70)
    print("TEST: Restart With Command")
    print("=" * 70)
    
    engine = TerminalRestartEngine()
    terminal = engine.add_terminal("old command", "/home/user")
    
    result = engine.restart_with_command(terminal.id, "new command")
    
    assert result.success, "Yeniden başlatma başarılı olmalı"
    assert terminal.command == "new command", "Komut güncellenmeli"
    
    print(f"  Success: {result.success}")
    print(f"  New command: {terminal.command}")
    
    print("\n" + "=" * 70)
    print("PASS: Restart with command")
    print("=" * 70)


def test_restart_with_environment():
    """
    Test: Restart with environment.
    """
    print("=" * 70)
    print("TEST: Restart With Environment")
    print("=" * 70)
    
    engine = TerminalRestartEngine()
    terminal = engine.add_terminal("test command", "/home/user", {"VAR1": "value1"})
    
    new_env = {"VAR2": "value2"}
    result = engine.restart_with_environment(terminal.id, new_env)
    
    assert result.success, "Yeniden başlatma başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Environment: {terminal.environment}")
    
    print("\n" + "=" * 70)
    print("PASS: Restart with environment")
    print("=" * 70)


def test_restart_with_directory():
    """
    Test: Restart with directory.
    """
    print("=" * 70)
    print("TEST: Restart With Directory")
    print("=" * 70)
    
    engine = TerminalRestartEngine()
    terminal = engine.add_terminal("test command", "/home/user")
    
    result = engine.restart_with_directory(terminal.id, "/home/user/new")
    
    assert result.success, "Yeniden başlatma başarılı olmalı"
    assert terminal.working_directory == "/home/user/new", "Dizin güncellenmeli"
    
    print(f"  Success: {result.success}")
    print(f"  New directory: {terminal.working_directory}")
    
    print("\n" + "=" * 70)
    print("PASS: Restart with directory")
    print("=" * 70)


def test_auto_restart():
    """
    Test: Auto restart.
    """
    print("=" * 70)
    print("TEST: Auto Restart")
    print("=" * 70)
    
    engine = TerminalRestartEngine()
    terminal = engine.add_terminal("test command", "/home/user")
    
    result = engine.auto_restart(terminal.id)
    
    assert result.success, "Otomatik yeniden başlatma başarılı olmalı"
    assert result.mode == RestartMode.AUTO.value, "Mod AUTO olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Mode: {result.mode}")
    
    print("\n" + "=" * 70)
    print("PASS: Auto restart")
    print("=" * 70)


def test_get_terminal():
    """
    Test: Get terminal.
    """
    print("=" * 70)
    print("TEST: Get Terminal")
    print("=" * 70)
    
    engine = TerminalRestartEngine()
    terminal = engine.add_terminal("test command", "/home/user")
    
    retrieved = engine.get_terminal(terminal.id)
    
    assert retrieved is not None, "Terminal bulunmalı"
    assert retrieved.id == terminal.id, "ID eşleşmeli"
    
    print(f"  ID: {retrieved.id}")
    print(f"  Command: {retrieved.command}")
    
    print("\n" + "=" * 70)
    print("PASS: Get terminal")
    print("=" * 70)


def test_get_all_terminals():
    """
    Test: Get all terminals.
    """
    print("=" * 70)
    print("TEST: Get All Terminals")
    print("=" * 70)
    
    engine = TerminalRestartEngine()
    engine.add_terminal("command1", "/home/user")
    engine.add_terminal("command2", "/home/user")
    
    terminals = engine.get_all_terminals()
    
    assert len(terminals) == 2, "2 terminal bulunmalı"
    
    print(f"  Terminals: {len(terminals)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get all terminals")
    print("=" * 70)


def test_get_restart_history():
    """
    Test: Get restart history.
    """
    print("=" * 70)
    print("TEST: Get Restart History")
    print("=" * 70)
    
    engine = TerminalRestartEngine()
    terminal = engine.add_terminal("test command", "/home/user")
    engine.restart_terminal(terminal.id)
    
    history = engine.get_restart_history()
    
    assert len(history) > 0, "Geçmiş olmalı"
    
    print(f"  History: {len(history)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get restart history")
    print("=" * 70)


def test_clear_history():
    """
    Test: Clear history.
    """
    print("=" * 70)
    print("TEST: Clear History")
    print("=" * 70)
    
    engine = TerminalRestartEngine()
    terminal = engine.add_terminal("test command", "/home/user")
    engine.restart_terminal(terminal.id)
    
    result = engine.clear_history()
    
    assert result.success, "Temizleme başarılı olmalı"
    assert len(engine.get_restart_history()) == 0, "Geçmiş temizlenmeli"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear history")
    print("=" * 70)


def test_reset_restart_attempts():
    """
    Test: Reset restart attempts.
    """
    print("=" * 70)
    print("TEST: Reset Restart Attempts")
    print("=" * 70)
    
    engine = TerminalRestartEngine()
    terminal = engine.add_terminal("test command", "/home/user")
    engine.restart_terminal(terminal.id)
    
    result = engine.reset_restart_attempts(terminal.id)
    
    assert result.success, "Sıfırlama başarılı olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Reset restart attempts")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    engine = TerminalRestartEngine()
    
    new_config = RestartConfig(confirm_before_restart=False, auto_restart_on_crash=True)
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
    
    engine = TerminalRestartEngine()
    
    config = engine.get_config()
    
    assert config is not None, "Config olmalı"
    assert config.confirm_before_restart == True, "Config eşleşmeli"
    
    print(f"  Confirm before restart: {config.confirm_before_restart}")
    print(f"  Auto restart on crash: {config.auto_restart_on_crash}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


def test_restart_mode_enum():
    """
    Test: RestartMode enum.
    """
    print("=" * 70)
    print("TEST: RestartMode Enum")
    print("=" * 70)
    
    assert RestartMode.NORMAL.value == "normal"
    assert RestartMode.FORCE.value == "force"
    assert RestartMode.AUTO.value == "auto"
    
    print(f"  All enum values verified")
    print(f"  Total modes: {len(RestartMode)}")
    
    print("\n" + "=" * 70)
    print("PASS: RestartMode enum")
    print("=" * 70)


def test_restart_scope_enum():
    """
    Test: RestartScope enum.
    """
    print("=" * 70)
    print("TEST: RestartScope Enum")
    print("=" * 70)
    
    assert RestartScope.CURRENT.value == "current"
    assert RestartScope.PANEL.value == "panel"
    assert RestartScope.SESSION.value == "session"
    assert RestartScope.GLOBAL.value == "global"
    
    print(f"  All enum values verified")
    print(f"  Total scopes: {len(RestartScope)}")
    
    print("\n" + "=" * 70)
    print("PASS: RestartScope enum")
    print("=" * 70)


def test_restart_config_dataclass():
    """
    Test: RestartConfig dataclass.
    """
    print("=" * 70)
    print("TEST: RestartConfig Dataclass")
    print("=" * 70)
    
    config = RestartConfig(
        confirm_before_restart=False,
        auto_restart_on_crash=True,
        restart_delay=5
    )
    
    assert config.confirm_before_restart == False, "Confirm eşleşmeli"
    assert config.auto_restart_on_crash == True, "Auto restart eşleşmeli"
    assert config.restart_delay == 5, "Delay eşleşmeli"
    
    print(f"  Confirm before restart: {config.confirm_before_restart}")
    print(f"  Auto restart on crash: {config.auto_restart_on_crash}")
    print(f"  Restart delay: {config.restart_delay}")
    
    print("\n" + "=" * 70)
    print("PASS: RestartConfig dataclass")
    print("=" * 70)


def test_restart_entry_dataclass():
    """
    Test: RestartEntry dataclass.
    """
    print("=" * 70)
    print("TEST: RestartEntry Dataclass")
    print("=" * 70)
    
    entry = RestartEntry(
        id="terminal_1",
        command="test command",
        working_directory="/home/user",
        environment={"VAR": "value"},
        timestamp="2024-01-01T00:00:00"
    )
    
    assert entry.id == "terminal_1", "ID eşleşmeli"
    assert entry.command == "test command", "Komut eşleşmeli"
    assert entry.working_directory == "/home/user", "Dizin eşleşmeli"
    
    print(f"  ID: {entry.id}")
    print(f"  Command: {entry.command}")
    print(f"  Working directory: {entry.working_directory}")
    
    print("\n" + "=" * 70)
    print("PASS: RestartEntry dataclass")
    print("=" * 70)


def test_restart_result_dataclass():
    """
    Test: RestartResult dataclass.
    """
    print("=" * 70)
    print("TEST: RestartResult Dataclass")
    print("=" * 70)
    
    result = RestartResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: RestartResult dataclass")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_add_terminal()
        test2 = test_restart_terminal()
        test3 = test_restart_with_mode()
        test4 = test_restart_with_command()
        test5 = test_restart_with_environment()
        test6 = test_restart_with_directory()
        test7 = test_auto_restart()
        test8 = test_get_terminal()
        test9 = test_get_all_terminals()
        test10 = test_get_restart_history()
        test11 = test_clear_history()
        test12 = test_reset_restart_attempts()
        test13 = test_update_config()
        test14 = test_get_config()
        test15 = test_restart_mode_enum()
        test16 = test_restart_scope_enum()
        test17 = test_restart_config_dataclass()
        test18 = test_restart_entry_dataclass()
        test19 = test_restart_result_dataclass()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Add Terminal: {'PASS' if test1 else 'FAIL'}")
        print(f"Restart Terminal: {'PASS' if test2 else 'FAIL'}")
        print(f"Restart With Mode: {'PASS' if test3 else 'FAIL'}")
        print(f"Restart With Command: {'PASS' if test4 else 'FAIL'}")
        print(f"Restart With Environment: {'PASS' if test5 else 'FAIL'}")
        print(f"Restart With Directory: {'PASS' if test6 else 'FAIL'}")
        print(f"Auto Restart: {'PASS' if test7 else 'FAIL'}")
        print(f"Get Terminal: {'PASS' if test8 else 'FAIL'}")
        print(f"Get All Terminals: {'PASS' if test9 else 'FAIL'}")
        print(f"Get Restart History: {'PASS' if test10 else 'FAIL'}")
        print(f"Clear History: {'PASS' if test11 else 'FAIL'}")
        print(f"Reset Restart Attempts: {'PASS' if test12 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test13 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test14 else 'FAIL'}")
        print(f"RestartMode Enum: {'PASS' if test15 else 'FAIL'}")
        print(f"RestartScope Enum: {'PASS' if test16 else 'FAIL'}")
        print(f"RestartConfig Dataclass: {'PASS' if test17 else 'FAIL'}")
        print(f"RestartEntry Dataclass: {'PASS' if test18 else 'FAIL'}")
        print(f"RestartResult Dataclass: {'PASS' if test19 else 'FAIL'}")
        
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
