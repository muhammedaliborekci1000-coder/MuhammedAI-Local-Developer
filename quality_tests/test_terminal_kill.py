"""
Quality Test: Terminal Kill
Terminal kill system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.tools.terminal_kill import (
    TerminalKillEngine,
    KillSignal,
    KillMode,
    KillScope,
    KillConfig,
    ProcessEntry,
    KillResult
)


def test_add_process():
    """
    Test: Add process.
    """
    print("=" * 70)
    print("TEST: Add Process")
    print("=" * 70)
    
    engine = TerminalKillEngine()
    process = engine.add_process("test command")
    
    assert process.pid == 1000, "PID eşleşmeli"
    assert process.command == "test command", "Komut eşleşmeli"
    assert process.status == "running", "Durum eşleşmeli"
    
    print(f"  PID: {process.pid}")
    print(f"  Command: {process.command}")
    print(f"  Status: {process.status}")
    
    print("\n" + "=" * 70)
    print("PASS: Add process")
    print("=" * 70)


def test_kill_process():
    """
    Test: Kill process.
    """
    print("=" * 70)
    print("TEST: Kill Process")
    print("=" * 70)
    
    engine = TerminalKillEngine()
    process = engine.add_process("test command")
    
    result = engine.kill_process(process.pid)
    
    assert result.success, "Öldürme başarılı olmalı"
    assert process.pid in result.killed_pids, "PID öldürülmüş olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Killed PIDs: {result.killed_pids}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Kill process")
    print("=" * 70)


def test_kill_by_signal():
    """
    Test: Kill by signal.
    """
    print("=" * 70)
    print("TEST: Kill By Signal")
    print("=" * 70)
    
    engine = TerminalKillEngine()
    process = engine.add_process("test command")
    
    result = engine.kill_by_signal(process.pid, KillSignal.SIGKILL)
    
    assert result.success, "Öldürme başarılı olmalı"
    assert result.signal == KillSignal.SIGKILL.value, "Sinyal eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Signal: {result.signal}")
    
    print("\n" + "=" * 70)
    print("PASS: Kill by signal")
    print("=" * 70)


def test_kill_group():
    """
    Test: Kill group.
    """
    print("=" * 70)
    print("TEST: Kill Group")
    print("=" * 70)
    
    engine = TerminalKillEngine()
    parent = engine.add_process("parent")
    child1 = engine.add_process("child1", parent_pid=parent.pid)
    child2 = engine.add_process("child2", parent_pid=parent.pid)
    
    result = engine.kill_group(parent.pid)
    
    assert result.success, "Öldürme başarılı olmalı"
    assert len(result.killed_pids) == 2, "2 süreç öldürülmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Killed PIDs: {result.killed_pids}")
    
    print("\n" + "=" * 70)
    print("PASS: Kill group")
    print("=" * 70)


def test_kill_tree():
    """
    Test: Kill tree.
    """
    print("=" * 70)
    print("TEST: Kill Tree")
    print("=" * 70)
    
    engine = TerminalKillEngine()
    root = engine.add_process("root")
    child1 = engine.add_process("child1", parent_pid=root.pid)
    child2 = engine.add_process("child2", parent_pid=root.pid)
    grandchild = engine.add_process("grandchild", parent_pid=child1.pid)
    
    result = engine.kill_tree(root.pid)
    
    assert result.success, "Öldürme başarılı olmalı"
    assert len(result.killed_pids) >= 1, "En az 1 süreç öldürülmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Killed PIDs: {result.killed_pids}")
    
    print("\n" + "=" * 70)
    print("PASS: Kill tree")
    print("=" * 70)


def test_kill_all():
    """
    Test: Kill all.
    """
    print("=" * 70)
    print("TEST: Kill All")
    print("=" * 70)
    
    engine = TerminalKillEngine()
    engine.add_process("process1", panel_id="panel_1")
    engine.add_process("process2", panel_id="panel_1")
    engine.add_process("process3", panel_id="panel_2")
    
    result = engine.kill_all(panel_id="panel_1")
    
    assert result.success, "Öldürme başarılı olmalı"
    assert len(result.killed_pids) == 2, "2 süreç öldürülmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Killed PIDs: {result.killed_pids}")
    
    print("\n" + "=" * 70)
    print("PASS: Kill all")
    print("=" * 70)


def test_force_kill():
    """
    Test: Force kill.
    """
    print("=" * 70)
    print("TEST: Force Kill")
    print("=" * 70)
    
    engine = TerminalKillEngine()
    process = engine.add_process("test command")
    
    result = engine.force_kill(process.pid)
    
    assert result.success, "Öldürme başarılı olmalı"
    assert result.signal == KillSignal.SIGKILL.value, "Sinyal SIGKILL olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Signal: {result.signal}")
    
    print("\n" + "=" * 70)
    print("PASS: Force kill")
    print("=" * 70)


def test_list_processes():
    """
    Test: List processes.
    """
    print("=" * 70)
    print("TEST: List Processes")
    print("=" * 70)
    
    engine = TerminalKillEngine()
    engine.add_process("process1", panel_id="panel_1")
    engine.add_process("process2", panel_id="panel_1")
    engine.add_process("process3", panel_id="panel_2")
    
    processes = engine.list_processes(panel_id="panel_1")
    
    assert len(processes) == 2, "2 süreç bulunmalı"
    
    print(f"  Processes: {len(processes)}")
    
    print("\n" + "=" * 70)
    print("PASS: List processes")
    print("=" * 70)


def test_get_process():
    """
    Test: Get process.
    """
    print("=" * 70)
    print("TEST: Get Process")
    print("=" * 70)
    
    engine = TerminalKillEngine()
    process = engine.add_process("test command")
    
    retrieved = engine.get_process(process.pid)
    
    assert retrieved is not None, "Süreç bulunmalı"
    assert retrieved.pid == process.pid, "PID eşleşmeli"
    
    print(f"  PID: {retrieved.pid}")
    print(f"  Command: {retrieved.command}")
    
    print("\n" + "=" * 70)
    print("PASS: Get process")
    print("=" * 70)


def test_get_kill_history():
    """
    Test: Get kill history.
    """
    print("=" * 70)
    print("TEST: Get Kill History")
    print("=" * 70)
    
    engine = TerminalKillEngine()
    process = engine.add_process("test command")
    engine.kill_process(process.pid)
    
    history = engine.get_kill_history()
    
    assert len(history) > 0, "Geçmiş olmalı"
    
    print(f"  History: {len(history)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get kill history")
    print("=" * 70)


def test_clear_history():
    """
    Test: Clear history.
    """
    print("=" * 70)
    print("TEST: Clear History")
    print("=" * 70)
    
    engine = TerminalKillEngine()
    process = engine.add_process("test command")
    engine.kill_process(process.pid)
    
    result = engine.clear_history()
    
    assert result.success, "Temizleme başarılı olmalı"
    assert len(engine.get_kill_history()) == 0, "Geçmiş temizlenmeli"
    
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
    
    engine = TerminalKillEngine()
    
    new_config = KillConfig(confirm_before_kill=False, force_kill=True)
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
    
    engine = TerminalKillEngine()
    
    config = engine.get_config()
    
    assert config is not None, "Config olmalı"
    assert config.confirm_before_kill == True, "Config eşleşmeli"
    
    print(f"  Confirm before kill: {config.confirm_before_kill}")
    print(f"  Force kill: {config.force_kill}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


def test_kill_signal_enum():
    """
    Test: KillSignal enum.
    """
    print("=" * 70)
    print("TEST: KillSignal Enum")
    print("=" * 70)
    
    assert KillSignal.SIGTERM.value == "SIGTERM"
    assert KillSignal.SIGKILL.value == "SIGKILL"
    assert KillSignal.SIGINT.value == "SIGINT"
    assert KillSignal.SIGHUP.value == "SIGHUP"
    assert KillSignal.SIGSTOP.value == "SIGSTOP"
    assert KillSignal.SIGCONT.value == "SIGCONT"
    
    print(f"  All enum values verified")
    print(f"  Total signals: {len(KillSignal)}")
    
    print("\n" + "=" * 70)
    print("PASS: KillSignal enum")
    print("=" * 70)


def test_kill_mode_enum():
    """
    Test: KillMode enum.
    """
    print("=" * 70)
    print("TEST: KillMode Enum")
    print("=" * 70)
    
    assert KillMode.SINGLE.value == "single"
    assert KillMode.GROUP.value == "group"
    assert KillMode.TREE.value == "tree"
    assert KillMode.ALL.value == "all"
    
    print(f"  All enum values verified")
    print(f"  Total modes: {len(KillMode)}")
    
    print("\n" + "=" * 70)
    print("PASS: KillMode enum")
    print("=" * 70)


def test_kill_scope_enum():
    """
    Test: KillScope enum.
    """
    print("=" * 70)
    print("TEST: KillScope Enum")
    print("=" * 70)
    
    assert KillScope.CURRENT.value == "current"
    assert KillScope.PANEL.value == "panel"
    assert KillScope.SESSION.value == "session"
    assert KillScope.GLOBAL.value == "global"
    
    print(f"  All enum values verified")
    print(f"  Total scopes: {len(KillScope)}")
    
    print("\n" + "=" * 70)
    print("PASS: KillScope enum")
    print("=" * 70)


def test_kill_config_dataclass():
    """
    Test: KillConfig dataclass.
    """
    print("=" * 70)
    print("TEST: KillConfig Dataclass")
    print("=" * 70)
    
    config = KillConfig(
        confirm_before_kill=False,
        force_kill=True,
        kill_children=False
    )
    
    assert config.confirm_before_kill == False, "Confirm eşleşmeli"
    assert config.force_kill == True, "Force kill eşleşmeli"
    assert config.kill_children == False, "Kill children eşleşmeli"
    
    print(f"  Confirm before kill: {config.confirm_before_kill}")
    print(f"  Force kill: {config.force_kill}")
    print(f"  Kill children: {config.kill_children}")
    
    print("\n" + "=" * 70)
    print("PASS: KillConfig dataclass")
    print("=" * 70)


def test_process_entry_dataclass():
    """
    Test: ProcessEntry dataclass.
    """
    print("=" * 70)
    print("TEST: ProcessEntry Dataclass")
    print("=" * 70)
    
    entry = ProcessEntry(
        pid=1000,
        command="test command",
        status="running"
    )
    
    assert entry.pid == 1000, "PID eşleşmeli"
    assert entry.command == "test command", "Komut eşleşmeli"
    assert entry.status == "running", "Durum eşleşmeli"
    
    print(f"  PID: {entry.pid}")
    print(f"  Command: {entry.command}")
    print(f"  Status: {entry.status}")
    
    print("\n" + "=" * 70)
    print("PASS: ProcessEntry dataclass")
    print("=" * 70)


def test_kill_result_dataclass():
    """
    Test: KillResult dataclass.
    """
    print("=" * 70)
    print("TEST: KillResult Dataclass")
    print("=" * 70)
    
    result = KillResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: KillResult dataclass")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_add_process()
        test2 = test_kill_process()
        test3 = test_kill_by_signal()
        test4 = test_kill_group()
        test5 = test_kill_tree()
        test6 = test_kill_all()
        test7 = test_force_kill()
        test8 = test_list_processes()
        test9 = test_get_process()
        test10 = test_get_kill_history()
        test11 = test_clear_history()
        test12 = test_update_config()
        test13 = test_get_config()
        test14 = test_kill_signal_enum()
        test15 = test_kill_mode_enum()
        test16 = test_kill_scope_enum()
        test17 = test_kill_config_dataclass()
        test18 = test_process_entry_dataclass()
        test19 = test_kill_result_dataclass()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Add Process: {'PASS' if test1 else 'FAIL'}")
        print(f"Kill Process: {'PASS' if test2 else 'FAIL'}")
        print(f"Kill By Signal: {'PASS' if test3 else 'FAIL'}")
        print(f"Kill Group: {'PASS' if test4 else 'FAIL'}")
        print(f"Kill Tree: {'PASS' if test5 else 'FAIL'}")
        print(f"Kill All: {'PASS' if test6 else 'FAIL'}")
        print(f"Force Kill: {'PASS' if test7 else 'FAIL'}")
        print(f"List Processes: {'PASS' if test8 else 'FAIL'}")
        print(f"Get Process: {'PASS' if test9 else 'FAIL'}")
        print(f"Get Kill History: {'PASS' if test10 else 'FAIL'}")
        print(f"Clear History: {'PASS' if test11 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test12 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test13 else 'FAIL'}")
        print(f"KillSignal Enum: {'PASS' if test14 else 'FAIL'}")
        print(f"KillMode Enum: {'PASS' if test15 else 'FAIL'}")
        print(f"KillScope Enum: {'PASS' if test16 else 'FAIL'}")
        print(f"KillConfig Dataclass: {'PASS' if test17 else 'FAIL'}")
        print(f"ProcessEntry Dataclass: {'PASS' if test18 else 'FAIL'}")
        print(f"KillResult Dataclass: {'PASS' if test19 else 'FAIL'}")
        
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
