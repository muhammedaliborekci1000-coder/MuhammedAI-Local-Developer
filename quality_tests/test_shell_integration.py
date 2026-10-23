"""
Quality Test: Shell Integration
Shell integration system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.tools.shell_integration import (
    ShellIntegrationEngine,
    ShellType,
    ShellScope,
    ShellAction,
    ShellConfig,
    ShellEntry,
    ShellResult
)


def test_create_shell():
    """
    Test: Create shell.
    """
    print("=" * 70)
    print("TEST: Create Shell")
    print("=" * 70)
    
    engine = ShellIntegrationEngine()
    result = engine.create_shell("Default")
    
    assert result.success, "Oluşturma başarılı olmalı"
    assert result.shell_name == "Default", "Shell adı eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Shell ID: {result.shell_id}")
    print(f"  Shell name: {result.shell_name}")
    
    print("\n" + "=" * 70)
    print("PASS: Create shell")
    print("=" * 70)


def test_create_shell_with_options():
    """
    Test: Create shell with options.
    """
    print("=" * 70)
    print("TEST: Create Shell With Options")
    print("=" * 70)
    
    engine = ShellIntegrationEngine()
    
    result = engine.create_shell(
        "Custom",
        shell_type=ShellType.ZSH,
        path="/bin/zsh",
        environment={"HOME": "/home/user", "PATH": "/usr/bin"},
        working_directory="/home/user"
    )
    
    assert result.success, "Oluşturma başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Shell ID: {result.shell_id}")
    
    print("\n" + "=" * 70)
    print("PASS: Create shell with options")
    print("=" * 70)


def test_update_shell():
    """
    Test: Update shell.
    """
    print("=" * 70)
    print("TEST: Update Shell")
    print("=" * 70)
    
    engine = ShellIntegrationEngine()
    result = engine.create_shell("Default")
    shell_id = result.shell_id
    
    result = engine.update_shell(shell_id, name="Updated", path="/bin/zsh")
    
    assert result.success, "Güncelleme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Update shell")
    print("=" * 70)


def test_delete_shell():
    """
    Test: Delete shell.
    """
    print("=" * 70)
    print("TEST: Delete Shell")
    print("=" * 70)
    
    engine = ShellIntegrationEngine()
    result = engine.create_shell("Default")
    shell_id = result.shell_id
    
    result = engine.delete_shell(shell_id)
    
    assert result.success, "Silme başarılı olmalı"
    assert shell_id not in engine.shells, "Shell silinmiş olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Delete shell")
    print("=" * 70)


def test_get_shell():
    """
    Test: Get shell.
    """
    print("=" * 70)
    print("TEST: Get Shell")
    print("=" * 70)
    
    engine = ShellIntegrationEngine()
    result = engine.create_shell("Default")
    shell_id = result.shell_id
    
    result = engine.get_shell(shell_id)
    
    assert result.success, "Alma başarılı olmalı"
    assert result.shell_name == "Default", "Shell adı eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Shell name: {result.shell_name}")
    
    print("\n" + "=" * 70)
    print("PASS: Get shell")
    print("=" * 70)


def test_list_shells():
    """
    Test: List shells.
    """
    print("=" * 70)
    print("TEST: List Shells")
    print("=" * 70)
    
    engine = ShellIntegrationEngine()
    engine.create_shell("Shell1")
    engine.create_shell("Shell2")
    
    result = engine.list_shells()
    
    assert result.success, "Listeleme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: List shells")
    print("=" * 70)


def test_list_shells_with_scope():
    """
    Test: List shells with scope.
    """
    print("=" * 70)
    print("TEST: List Shells With Scope")
    print("=" * 70)
    
    engine = ShellIntegrationEngine()
    engine.create_shell("Shell1", scope=ShellScope.GLOBAL)
    engine.create_shell("Shell2", scope=ShellScope.SESSION)
    
    result = engine.list_shells(scope=ShellScope.GLOBAL)
    
    assert result.success, "Listeleme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: List shells with scope")
    print("=" * 70)


def test_activate_shell():
    """
    Test: Activate shell.
    """
    print("=" * 70)
    print("TEST: Activate Shell")
    print("=" * 70)
    
    engine = ShellIntegrationEngine()
    result = engine.create_shell("Default")
    shell_id = result.shell_id
    
    result = engine.activate_shell(shell_id)
    
    assert result.success, "Aktifleştirme başarılı olmalı"
    assert engine.shells[shell_id].is_active, "Shell aktif olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Activate shell")
    print("=" * 70)


def test_clone_shell():
    """
    Test: Clone shell.
    """
    print("=" * 70)
    print("TEST: Clone Shell")
    print("=" * 70)
    
    engine = ShellIntegrationEngine()
    result = engine.create_shell("Default")
    shell_id = result.shell_id
    
    result = engine.clone_shell(shell_id, "Cloned")
    
    assert result.success, "Klonlama başarılı olmalı"
    assert result.shell_name == "Cloned", "Yeni ad eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  New shell ID: {result.shell_id}")
    print(f"  New shell name: {result.shell_name}")
    
    print("\n" + "=" * 70)
    print("PASS: Clone shell")
    print("=" * 70)


def test_export_shell():
    """
    Test: Export shell.
    """
    print("=" * 70)
    print("TEST: Export Shell")
    print("=" * 70)
    
    engine = ShellIntegrationEngine()
    result = engine.create_shell("Default")
    shell_id = result.shell_id
    
    result = engine.export_shell(shell_id, format="json")
    
    assert result.success, "Dışa aktarma başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Export shell")
    print("=" * 70)


def test_import_shell():
    """
    Test: Import shell.
    """
    print("=" * 70)
    print("TEST: Import Shell")
    print("=" * 70)
    
    engine = ShellIntegrationEngine()
    
    data = {
        "name": "Imported",
        "shell_type": "zsh",
        "path": "/bin/zsh",
        "environment": {"HOME": "/home/user"},
        "working_directory": "/home/user"
    }
    
    result = engine.import_shell(data)
    
    assert result.success, "İçe aktarma başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Import shell")
    print("=" * 70)


def test_set_default_shell():
    """
    Test: Set default shell.
    """
    print("=" * 70)
    print("TEST: Set Default Shell")
    print("=" * 70)
    
    engine = ShellIntegrationEngine()
    result = engine.create_shell("Default")
    shell_id = result.shell_id
    
    result = engine.set_default_shell(shell_id)
    
    assert result.success, "Ayarlama başarılı olmalı"
    assert engine.shells[shell_id].is_default, "Shell varsayılan olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set default shell")
    print("=" * 70)


def test_execute_command():
    """
    Test: Execute command.
    """
    print("=" * 70)
    print("TEST: Execute Command")
    print("=" * 70)
    
    engine = ShellIntegrationEngine()
    result = engine.create_shell("Default")
    shell_id = result.shell_id
    
    result = engine.execute_command(shell_id, "ls -la")
    
    assert result.success, "Çalıştırma başarılı olmalı"
    assert result.output is not None, "Çıktı olmalı"
    assert result.exit_code == 0, "Çıkış kodu 0 olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Output: {result.output}")
    
    print("\n" + "=" * 70)
    print("PASS: Execute command")
    print("=" * 70)


def test_reset_shell():
    """
    Test: Reset shell.
    """
    print("=" * 70)
    print("TEST: Reset Shell")
    print("=" * 70)
    
    engine = ShellIntegrationEngine()
    result = engine.create_shell("Default")
    shell_id = result.shell_id
    
    result = engine.reset_shell(shell_id)
    
    assert result.success, "Sıfırlama başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Reset shell")
    print("=" * 70)


def test_get_shell_history():
    """
    Test: Get shell history.
    """
    print("=" * 70)
    print("TEST: Get Shell History")
    print("=" * 70)
    
    engine = ShellIntegrationEngine()
    engine.create_shell("Default")
    
    history = engine.get_shell_history()
    
    assert len(history) > 0, "Geçmiş olmalı"
    
    print(f"  History: {len(history)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get shell history")
    print("=" * 70)


def test_clear_history():
    """
    Test: Clear history.
    """
    print("=" * 70)
    print("TEST: Clear History")
    print("=" * 70)
    
    engine = ShellIntegrationEngine()
    engine.create_shell("Default")
    
    result = engine.clear_history()
    
    assert result.success, "Temizleme başarılı olmalı"
    assert len(engine.get_shell_history()) == 0, "Geçmiş temizlenmeli"
    
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
    
    engine = ShellIntegrationEngine()
    
    new_config = ShellConfig(persist_shells=False)
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
    
    engine = ShellIntegrationEngine()
    
    config = engine.get_config()
    
    assert config is not None, "Config olmalı"
    assert config.persist_shells == True, "Config eşleşmeli"
    
    print(f"  Persist shells: {config.persist_shells}")
    print(f"  Auto load shells: {config.auto_load_shells}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
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
    assert ShellType.CSH.value == "csh"
    assert ShellType.TCSH.value == "tcsh"
    assert ShellType.KSH.value == "ksh"
    assert ShellType.CUSTOM.value == "custom"
    
    print(f"  All enum values verified")
    print(f"  Total types: {len(ShellType)}")
    
    print("\n" + "=" * 70)
    print("PASS: ShellType enum")
    print("=" * 70)


def test_shell_scope_enum():
    """
    Test: ShellScope enum.
    """
    print("=" * 70)
    print("TEST: ShellScope Enum")
    print("=" * 70)
    
    assert ShellScope.SESSION.value == "session"
    assert ShellScope.TERMINAL.value == "terminal"
    assert ShellScope.GLOBAL.value == "global"
    
    print(f"  All enum values verified")
    print(f"  Total scopes: {len(ShellScope)}")
    
    print("\n" + "=" * 70)
    print("PASS: ShellScope enum")
    print("=" * 70)


def test_shell_action_enum():
    """
    Test: ShellAction enum.
    """
    print("=" * 70)
    print("TEST: ShellAction Enum")
    print("=" * 70)
    
    assert ShellAction.CREATE.value == "create"
    assert ShellAction.UPDATE.value == "update"
    assert ShellAction.DELETE.value == "delete"
    assert ShellAction.GET.value == "get"
    assert ShellAction.LIST.value == "list"
    assert ShellAction.ACTIVATE.value == "activate"
    assert ShellAction.CLONE.value == "clone"
    assert ShellAction.IMPORT.value == "import"
    assert ShellAction.EXPORT.value == "export"
    assert ShellAction.SET_DEFAULT.value == "set_default"
    assert ShellAction.EXECUTE.value == "execute"
    assert ShellAction.RESET.value == "reset"
    
    print(f"  All enum values verified")
    print(f"  Total actions: {len(ShellAction)}")
    
    print("\n" + "=" * 70)
    print("PASS: ShellAction enum")
    print("=" * 70)


def test_shell_config_dataclass():
    """
    Test: ShellConfig dataclass.
    """
    print("=" * 70)
    print("TEST: ShellConfig Dataclass")
    print("=" * 70)
    
    config = ShellConfig(
        persist_shells=False,
        auto_load_shells=False
    )
    
    assert config.persist_shells == False, "Persist eşleşmeli"
    assert config.auto_load_shells == False, "Auto load eşleşmeli"
    
    print(f"  Persist shells: {config.persist_shells}")
    print(f"  Auto load shells: {config.auto_load_shells}")
    
    print("\n" + "=" * 70)
    print("PASS: ShellConfig dataclass")
    print("=" * 70)


def test_shell_entry_dataclass():
    """
    Test: ShellEntry dataclass.
    """
    print("=" * 70)
    print("TEST: ShellEntry Dataclass")
    print("=" * 70)
    
    entry = ShellEntry(
        id="shell_1",
        name="Default",
        shell_type=ShellType.BASH,
        path="/bin/bash",
        environment={"HOME": "/home/user"},
        scope=ShellScope.SESSION,
        timestamp="2024-01-01T00:00:00"
    )
    
    assert entry.id == "shell_1", "ID eşleşmeli"
    assert entry.name == "Default", "Ad eşleşmeli"
    
    print(f"  ID: {entry.id}")
    print(f"  Name: {entry.name}")
    
    print("\n" + "=" * 70)
    print("PASS: ShellEntry dataclass")
    print("=" * 70)


def test_shell_result_dataclass():
    """
    Test: ShellResult dataclass.
    """
    print("=" * 70)
    print("TEST: ShellResult Dataclass")
    print("=" * 70)
    
    result = ShellResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: ShellResult dataclass")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_create_shell()
        test2 = test_create_shell_with_options()
        test3 = test_update_shell()
        test4 = test_delete_shell()
        test5 = test_get_shell()
        test6 = test_list_shells()
        test7 = test_list_shells_with_scope()
        test8 = test_activate_shell()
        test9 = test_clone_shell()
        test10 = test_export_shell()
        test11 = test_import_shell()
        test12 = test_set_default_shell()
        test13 = test_execute_command()
        test14 = test_reset_shell()
        test15 = test_get_shell_history()
        test16 = test_clear_history()
        test17 = test_update_config()
        test18 = test_get_config()
        test19 = test_shell_type_enum()
        test20 = test_shell_scope_enum()
        test21 = test_shell_action_enum()
        test22 = test_shell_config_dataclass()
        test23 = test_shell_entry_dataclass()
        test24 = test_shell_result_dataclass()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Create Shell: {'PASS' if test1 else 'FAIL'}")
        print(f"Create Shell With Options: {'PASS' if test2 else 'FAIL'}")
        print(f"Update Shell: {'PASS' if test3 else 'FAIL'}")
        print(f"Delete Shell: {'PASS' if test4 else 'FAIL'}")
        print(f"Get Shell: {'PASS' if test5 else 'FAIL'}")
        print(f"List Shells: {'PASS' if test6 else 'FAIL'}")
        print(f"List Shells With Scope: {'PASS' if test7 else 'FAIL'}")
        print(f"Activate Shell: {'PASS' if test8 else 'FAIL'}")
        print(f"Clone Shell: {'PASS' if test9 else 'FAIL'}")
        print(f"Export Shell: {'PASS' if test10 else 'FAIL'}")
        print(f"Import Shell: {'PASS' if test11 else 'FAIL'}")
        print(f"Set Default Shell: {'PASS' if test12 else 'FAIL'}")
        print(f"Execute Command: {'PASS' if test13 else 'FAIL'}")
        print(f"Reset Shell: {'PASS' if test14 else 'FAIL'}")
        print(f"Get Shell History: {'PASS' if test15 else 'FAIL'}")
        print(f"Clear History: {'PASS' if test16 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test17 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test18 else 'FAIL'}")
        print(f"ShellType Enum: {'PASS' if test19 else 'FAIL'}")
        print(f"ShellScope Enum: {'PASS' if test20 else 'FAIL'}")
        print(f"ShellAction Enum: {'PASS' if test21 else 'FAIL'}")
        print(f"ShellConfig Dataclass: {'PASS' if test22 else 'FAIL'}")
        print(f"ShellEntry Dataclass: {'PASS' if test23 else 'FAIL'}")
        print(f"ShellResult Dataclass: {'PASS' if test24 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14, test15, test16, test17, test18, test19, test20, test21, test22, test23, test24])
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
