"""
Quality Test: Terminal Aliases
Terminal aliases system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.tools.terminal_aliases import (
    TerminalAliasesEngine,
    AliasScope,
    AliasAction,
    AliasConfig,
    AliasEntry,
    AliasResult
)


def test_add_alias():
    """
    Test: Add alias.
    """
    print("=" * 70)
    print("TEST: Add Alias")
    print("=" * 70)
    
    engine = TerminalAliasesEngine()
    result = engine.add_alias("ll", "ls -la")
    
    assert result.success, "Ekleme başarılı olmalı"
    assert result.alias_name == "ll", "Alias adı eşleşmeli"
    assert result.alias_command == "ls -la", "Komut eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Alias name: {result.alias_name}")
    print(f"  Alias command: {result.alias_command}")
    
    print("\n" + "=" * 70)
    print("PASS: Add alias")
    print("=" * 70)


def test_add_alias_with_description():
    """
    Test: Add alias with description.
    """
    print("=" * 70)
    print("TEST: Add Alias With Description")
    print("=" * 70)
    
    engine = TerminalAliasesEngine()
    result = engine.add_alias("ll", "ls -la", description="List all files")
    
    assert result.success, "Ekleme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Description: {engine.aliases['ll'].description}")
    
    print("\n" + "=" * 70)
    print("PASS: Add alias with description")
    print("=" * 70)


def test_remove_alias():
    """
    Test: Remove alias.
    """
    print("=" * 70)
    print("TEST: Remove Alias")
    print("=" * 70)
    
    engine = TerminalAliasesEngine()
    engine.add_alias("ll", "ls -la")
    
    result = engine.remove_alias("ll")
    
    assert result.success, "Kaldırma başarılı olmalı"
    assert "ll" not in engine.aliases, "Alias kaldırılmış olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Remove alias")
    print("=" * 70)


def test_get_alias():
    """
    Test: Get alias.
    """
    print("=" * 70)
    print("TEST: Get Alias")
    print("=" * 70)
    
    engine = TerminalAliasesEngine()
    engine.add_alias("ll", "ls -la")
    
    result = engine.get_alias("ll")
    
    assert result.success, "Alma başarılı olmalı"
    assert result.alias_command == "ls -la", "Komut eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Alias command: {result.alias_command}")
    
    print("\n" + "=" * 70)
    print("PASS: Get alias")
    print("=" * 70)


def test_list_aliases():
    """
    Test: List aliases.
    """
    print("=" * 70)
    print("TEST: List Aliases")
    print("=" * 70)
    
    engine = TerminalAliasesEngine()
    engine.add_alias("ll", "ls -la")
    engine.add_alias("la", "ls -A")
    
    result = engine.list_aliases()
    
    assert result.success, "Listeleme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: List aliases")
    print("=" * 70)


def test_list_aliases_with_scope():
    """
    Test: List aliases with scope.
    """
    print("=" * 70)
    print("TEST: List Aliases With Scope")
    print("=" * 70)
    
    engine = TerminalAliasesEngine()
    engine.add_alias("ll", "ls -la", AliasScope.GLOBAL)
    engine.add_alias("la", "ls -A", AliasScope.SESSION)
    
    result = engine.list_aliases(scope=AliasScope.GLOBAL)
    
    assert result.success, "Listeleme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: List aliases with scope")
    print("=" * 70)


def test_clear_aliases():
    """
    Test: Clear aliases.
    """
    print("=" * 70)
    print("TEST: Clear Aliases")
    print("=" * 70)
    
    engine = TerminalAliasesEngine()
    engine.add_alias("ll", "ls -la")
    engine.add_alias("la", "ls -A")
    
    result = engine.clear_aliases()
    
    assert result.success, "Temizleme başarılı olmalı"
    assert len(engine.aliases) == 0, "Aliasler temizlenmeli"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear aliases")
    print("=" * 70)


def test_clear_aliases_with_scope():
    """
    Test: Clear aliases with scope.
    """
    print("=" * 70)
    print("TEST: Clear Aliases With Scope")
    print("=" * 70)
    
    engine = TerminalAliasesEngine()
    engine.add_alias("ll", "ls -la", AliasScope.GLOBAL)
    engine.add_alias("la", "ls -A", AliasScope.SESSION)
    
    result = engine.clear_aliases(scope=AliasScope.GLOBAL)
    
    assert result.success, "Temizleme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear aliases with scope")
    print("=" * 70)


def test_export_aliases():
    """
    Test: Export aliases.
    """
    print("=" * 70)
    print("TEST: Export Aliases")
    print("=" * 70)
    
    engine = TerminalAliasesEngine()
    engine.add_alias("ll", "ls -la")
    
    result = engine.export_aliases(format="json")
    
    assert result.success, "Dışa aktarma başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Export aliases")
    print("=" * 70)


def test_import_aliases():
    """
    Test: Import aliases.
    """
    print("=" * 70)
    print("TEST: Import Aliases")
    print("=" * 70)
    
    engine = TerminalAliasesEngine()
    
    data = {"ll": "ls -la", "la": "ls -A"}
    result = engine.import_aliases(data)
    
    assert result.success, "İçe aktarma başarılı olmalı"
    assert len(engine.aliases) == 2, "2 alias aktarılmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Import aliases")
    print("=" * 70)


def test_execute_alias():
    """
    Test: Execute alias.
    """
    print("=" * 70)
    print("TEST: Execute Alias")
    print("=" * 70)
    
    engine = TerminalAliasesEngine()
    engine.add_alias("ll", "ls -la")
    
    result = engine.execute_alias("ll")
    
    assert result.success, "Çalıştırma başarılı olmalı"
    assert result.alias_command == "ls -la", "Komut eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Execute alias")
    print("=" * 70)


def test_get_alias_history():
    """
    Test: Get alias history.
    """
    print("=" * 70)
    print("TEST: Get Alias History")
    print("=" * 70)
    
    engine = TerminalAliasesEngine()
    engine.add_alias("ll", "ls -la")
    
    history = engine.get_alias_history()
    
    assert len(history) > 0, "Geçmiş olmalı"
    
    print(f"  History: {len(history)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get alias history")
    print("=" * 70)


def test_clear_history():
    """
    Test: Clear history.
    """
    print("=" * 70)
    print("TEST: Clear History")
    print("=" * 70)
    
    engine = TerminalAliasesEngine()
    engine.add_alias("ll", "ls -la")
    
    result = engine.clear_history()
    
    assert result.success, "Temizleme başarılı olmalı"
    assert len(engine.get_alias_history()) == 0, "Geçmiş temizlenmeli"
    
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
    
    engine = TerminalAliasesEngine()
    
    new_config = AliasConfig(persist_aliases=False)
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
    
    engine = TerminalAliasesEngine()
    
    config = engine.get_config()
    
    assert config is not None, "Config olmalı"
    assert config.persist_aliases == True, "Config eşleşmeli"
    
    print(f"  Persist aliases: {config.persist_aliases}")
    print(f"  Auto load from shell: {config.auto_load_from_shell}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


def test_alias_scope_enum():
    """
    Test: AliasScope enum.
    """
    print("=" * 70)
    print("TEST: AliasScope Enum")
    print("=" * 70)
    
    assert AliasScope.SESSION.value == "session"
    assert AliasScope.TERMINAL.value == "terminal"
    assert AliasScope.GLOBAL.value == "global"
    
    print(f"  All enum values verified")
    print(f"  Total scopes: {len(AliasScope)}")
    
    print("\n" + "=" * 70)
    print("PASS: AliasScope enum")
    print("=" * 70)


def test_alias_action_enum():
    """
    Test: AliasAction enum.
    """
    print("=" * 70)
    print("TEST: AliasAction Enum")
    print("=" * 70)
    
    assert AliasAction.ADD.value == "add"
    assert AliasAction.REMOVE.value == "remove"
    assert AliasAction.GET.value == "get"
    assert AliasAction.LIST.value == "list"
    assert AliasAction.CLEAR.value == "clear"
    assert AliasAction.IMPORT.value == "import"
    assert AliasAction.EXPORT.value == "export"
    assert AliasAction.EXECUTE.value == "execute"
    
    print(f"  All enum values verified")
    print(f"  Total actions: {len(AliasAction)}")
    
    print("\n" + "=" * 70)
    print("PASS: AliasAction enum")
    print("=" * 70)


def test_alias_config_dataclass():
    """
    Test: AliasConfig dataclass.
    """
    print("=" * 70)
    print("TEST: AliasConfig Dataclass")
    print("=" * 70)
    
    config = AliasConfig(
        persist_aliases=False,
        auto_load_from_shell=False
    )
    
    assert config.persist_aliases == False, "Persist eşleşmeli"
    assert config.auto_load_from_shell == False, "Auto load eşleşmeli"
    
    print(f"  Persist aliases: {config.persist_aliases}")
    print(f"  Auto load from shell: {config.auto_load_from_shell}")
    
    print("\n" + "=" * 70)
    print("PASS: AliasConfig dataclass")
    print("=" * 70)


def test_alias_entry_dataclass():
    """
    Test: AliasEntry dataclass.
    """
    print("=" * 70)
    print("TEST: AliasEntry Dataclass")
    print("=" * 70)
    
    entry = AliasEntry(
        name="ll",
        command="ls -la",
        description="List all files",
        scope=AliasScope.SESSION,
        timestamp="2024-01-01T00:00:00"
    )
    
    assert entry.name == "ll", "Ad eşleşmeli"
    assert entry.command == "ls -la", "Komut eşleşmeli"
    
    print(f"  Name: {entry.name}")
    print(f"  Command: {entry.command}")
    
    print("\n" + "=" * 70)
    print("PASS: AliasEntry dataclass")
    print("=" * 70)


def test_alias_result_dataclass():
    """
    Test: AliasResult dataclass.
    """
    print("=" * 70)
    print("TEST: AliasResult Dataclass")
    print("=" * 70)
    
    result = AliasResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: AliasResult dataclass")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_add_alias()
        test2 = test_add_alias_with_description()
        test3 = test_remove_alias()
        test4 = test_get_alias()
        test5 = test_list_aliases()
        test6 = test_list_aliases_with_scope()
        test7 = test_clear_aliases()
        test8 = test_clear_aliases_with_scope()
        test9 = test_export_aliases()
        test10 = test_import_aliases()
        test11 = test_execute_alias()
        test12 = test_get_alias_history()
        test13 = test_clear_history()
        test14 = test_update_config()
        test15 = test_get_config()
        test16 = test_alias_scope_enum()
        test17 = test_alias_action_enum()
        test18 = test_alias_config_dataclass()
        test19 = test_alias_entry_dataclass()
        test20 = test_alias_result_dataclass()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Add Alias: {'PASS' if test1 else 'FAIL'}")
        print(f"Add Alias With Description: {'PASS' if test2 else 'FAIL'}")
        print(f"Remove Alias: {'PASS' if test3 else 'FAIL'}")
        print(f"Get Alias: {'PASS' if test4 else 'FAIL'}")
        print(f"List Aliases: {'PASS' if test5 else 'FAIL'}")
        print(f"List Aliases With Scope: {'PASS' if test6 else 'FAIL'}")
        print(f"Clear Aliases: {'PASS' if test7 else 'FAIL'}")
        print(f"Clear Aliases With Scope: {'PASS' if test8 else 'FAIL'}")
        print(f"Export Aliases: {'PASS' if test9 else 'FAIL'}")
        print(f"Import Aliases: {'PASS' if test10 else 'FAIL'}")
        print(f"Execute Alias: {'PASS' if test11 else 'FAIL'}")
        print(f"Get Alias History: {'PASS' if test12 else 'FAIL'}")
        print(f"Clear History: {'PASS' if test13 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test14 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test15 else 'FAIL'}")
        print(f"AliasScope Enum: {'PASS' if test16 else 'FAIL'}")
        print(f"AliasAction Enum: {'PASS' if test17 else 'FAIL'}")
        print(f"AliasConfig Dataclass: {'PASS' if test18 else 'FAIL'}")
        print(f"AliasEntry Dataclass: {'PASS' if test19 else 'FAIL'}")
        print(f"AliasResult Dataclass: {'PASS' if test20 else 'FAIL'}")
        
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
