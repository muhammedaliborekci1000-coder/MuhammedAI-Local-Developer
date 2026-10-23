"""
Quality Test: Keybindings
Keybinding system testleri.
"""

import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from app.editor.keybindings import (
    KeyModifier,
    KeybindingScope,
    Keybinding,
    KeybindingConfig,
    KeybindingResult,
    KeybindingManager
)


def test_key_modifier_enum():
    """
    Test: KeyModifier enum.
    """
    print("=" * 70)
    print("TEST: KeyModifier Enum")
    print("=" * 70)
    
    assert KeyModifier.CTRL.value == "ctrl"
    assert KeyModifier.ALT.value == "alt"
    assert KeyModifier.SHIFT.value == "shift"
    assert KeyModifier.META.value == "meta"
    assert KeyModifier.CMD.value == "cmd"
    
    print(f"  All enum values verified")
    print(f"  Total modifiers: {len(KeyModifier)}")
    
    print("\n" + "=" * 70)
    print("PASS: KeyModifier enum")
    print("=" * 70)


def test_keybinding_scope_enum():
    """
    Test: KeybindingScope enum.
    """
    print("=" * 70)
    print("TEST: KeybindingScope Enum")
    print("=" * 70)
    
    assert KeybindingScope.GLOBAL.value == "global"
    assert KeybindingScope.EDITOR.value == "editor"
    assert KeybindingScope.TERMINAL.value == "terminal"
    assert KeybindingScope.EXPLORER.value == "explorer"
    assert KeybindingScope.SEARCH.value == "search"
    assert KeybindingScope.DEBUG.value == "debug"
    
    print(f"  All enum values verified")
    print(f"  Total scopes: {len(KeybindingScope)}")
    
    print("\n" + "=" * 70)
    print("PASS: KeybindingScope enum")
    print("=" * 70)


def test_keybinding_dataclass():
    """
    Test: Keybinding dataclass.
    """
    print("=" * 70)
    print("TEST: Keybinding Dataclass")
    print("=" * 70)
    
    keybinding = Keybinding(
        id="test.binding",
        key="s",
        modifiers=[KeyModifier.CTRL],
        command="test.command",
        scope=KeybindingScope.GLOBAL,
        description="Test keybinding"
    )
    
    assert keybinding.id == "test.binding", "ID eşleşmeli"
    assert keybinding.key == "s", "Key eşleşmeli"
    assert keybinding.command == "test.command", "Command eşleşmeli"
    
    print(f"  ID: {keybinding.id}")
    print(f"  Key: {keybinding.key}")
    print(f"  Command: {keybinding.command}")
    
    print("\n" + "=" * 70)
    print("PASS: Keybinding dataclass")
    print("=" * 70)


def test_keybinding_config_dataclass():
    """
    Test: KeybindingConfig dataclass.
    """
    print("=" * 70)
    print("TEST: KeybindingConfig Dataclass")
    print("=" * 70)
    
    config = KeybindingConfig(
        enable_conflict_detection=True,
        allow_overrides=False
    )
    
    assert config.enable_conflict_detection == True, "Conflict detection eşleşmeli"
    assert config.allow_overrides == False, "Allow overrides eşleşmeli"
    
    print(f"  Conflict detection: {config.enable_conflict_detection}")
    print(f"  Allow overrides: {config.allow_overrides}")
    
    print("\n" + "=" * 70)
    print("PASS: KeybindingConfig dataclass")
    print("=" * 70)


def test_keybinding_result_dataclass():
    """
    Test: KeybindingResult dataclass.
    """
    print("=" * 70)
    print("TEST: KeybindingResult Dataclass")
    print("=" * 70)
    
    result = KeybindingResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.conflicts, list), "Conflicts list olmalı"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Conflicts: {len(result.conflicts)}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: KeybindingResult dataclass")
    print("=" * 70)


def test_keybinding_manager_initialization():
    """
    Test: KeybindingManager initialization.
    """
    print("=" * 70)
    print("TEST: KeybindingManager Initialization")
    print("=" * 70)
    
    config = KeybindingConfig()
    manager = KeybindingManager(config)
    
    assert manager.config == config, "Config eşleşmeli"
    assert len(manager.keybindings) > 0, "Keybindings olmalı"
    
    print(f"  Keybindings: {len(manager.keybindings)}")
    
    print("\n" + "=" * 70)
    print("PASS: KeybindingManager initialization")
    print("=" * 70)


def test_register_keybinding():
    """
    Test: Register keybinding.
    """
    print("=" * 70)
    print("TEST: Register Keybinding")
    print("=" * 70)
    
    manager = KeybindingManager()
    
    keybinding = Keybinding(
        id="test.custom",
        key="t",
        modifiers=[KeyModifier.CTRL],
        command="test.command",
        scope=KeybindingScope.GLOBAL
    )
    
    result = manager.register_keybinding(keybinding)
    
    assert result.success == True, "Registration başarılı olmalı"
    assert "test.custom" in manager.keybindings, "Keybinding kaydedilmeli"
    
    print(f"  Keybinding registered: {keybinding.id}")
    
    print("\n" + "=" * 70)
    print("PASS: Register keybinding")
    print("=" * 70)


def test_unregister_keybinding():
    """
    Test: Unregister keybinding.
    """
    print("=" * 70)
    print("TEST: Unregister Keybinding")
    print("=" * 70)
    
    manager = KeybindingManager()
    
    keybinding = Keybinding(
        id="test.custom",
        key="t",
        modifiers=[KeyModifier.CTRL],
        command="test.command",
        scope=KeybindingScope.GLOBAL
    )
    
    manager.register_keybinding(keybinding)
    result = manager.unregister_keybinding("test.custom")
    
    assert result.success == True, "Unregistration başarılı olmalı"
    assert "test.custom" not in manager.keybindings, "Keybinding silinmeli"
    
    print(f"  Keybinding unregistered: {keybinding.id}")
    
    print("\n" + "=" * 70)
    print("PASS: Unregister keybinding")
    print("=" * 70)


def test_get_keybinding():
    """
    Test: Get keybinding.
    """
    print("=" * 70)
    print("TEST: Get Keybinding")
    print("=" * 70)
    
    manager = KeybindingManager()
    
    keybinding = manager.get_keybinding("file.save")
    
    assert keybinding is not None, "Keybinding bulunmalı"
    assert keybinding.id == "file.save", "ID eşleşmeli"
    
    print(f"  Keybinding: {keybinding.id}")
    
    print("\n" + "=" * 70)
    print("PASS: Get keybinding")
    print("=" * 70)


def test_get_all_keybindings():
    """
    Test: Get all keybindings.
    """
    print("=" * 70)
    print("TEST: Get All Keybindings")
    print("=" * 70)
    
    manager = KeybindingManager()
    
    all_keybindings = manager.get_all_keybindings()
    
    assert len(all_keybindings) > 0, "Keybindings olmalı"
    
    print(f"  Total keybindings: {len(all_keybindings)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get all keybindings")
    print("=" * 70)


def test_get_keybindings_by_scope():
    """
    Test: Get keybindings by scope.
    """
    print("=" * 70)
    print("TEST: Get Keybindings by Scope")
    print("=" * 70)
    
    manager = KeybindingManager()
    
    global_keybindings = manager.get_keybindings_by_scope(KeybindingScope.GLOBAL)
    
    assert len(global_keybindings) > 0, "Global keybindings olmalı"
    
    print(f"  Global keybindings: {len(global_keybindings)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get keybindings by scope")
    print("=" * 70)


def test_get_keybindings_by_command():
    """
    Test: Get keybindings by command.
    """
    print("=" * 70)
    print("TEST: Get Keybindings by Command")
    print("=" * 70)
    
    manager = KeybindingManager()
    
    keybindings = manager.get_keybindings_by_command("file.save")
    
    assert len(keybindings) > 0, "Keybindings bulunmalı"
    
    print(f"  Keybindings for file.save: {len(keybindings)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get keybindings by command")
    print("=" * 70)


def test_find_keybinding_by_key():
    """
    Test: Find keybinding by key.
    """
    print("=" * 70)
    print("TEST: Find Keybinding by Key")
    print("=" * 70)
    
    manager = KeybindingManager()
    
    keybinding = manager.find_keybinding_by_key("s", [KeyModifier.CTRL], KeybindingScope.GLOBAL)
    
    assert keybinding is not None, "Keybinding bulunmalı"
    assert keybinding.key == "s", "Key eşleşmeli"
    
    print(f"  Found keybinding: {keybinding.id}")
    
    print("\n" + "=" * 70)
    print("PASS: Find keybinding by key")
    print("=" * 70)


def test_check_conflicts():
    """
    Test: Check conflicts.
    """
    print("=" * 70)
    print("TEST: Check Conflicts")
    print("=" * 70)
    
    manager = KeybindingManager()
    
    # Create conflicting keybinding
    keybinding = Keybinding(
        id="test.conflict",
        key="s",
        modifiers=[KeyModifier.CTRL],
        command="test.command",
        scope=KeybindingScope.GLOBAL
    )
    
    result = manager.check_conflicts(keybinding)
    
    assert result.success == False, "Conflict tespit edilmeli"
    assert len(result.conflicts) > 0, "Conflict'lar olmalı"
    
    print(f"  Conflicts found: {len(result.conflicts)}")
    
    print("\n" + "=" * 70)
    print("PASS: Check conflicts")
    print("=" * 70)


def test_update_keybinding():
    """
    Test: Update keybinding.
    """
    print("=" * 70)
    print("TEST: Update Keybinding")
    print("=" * 70)
    
    manager = KeybindingManager()
    
    # Get existing keybinding
    existing = manager.get_keybinding("file.save")
    
    # Update with new key
    new_keybinding = Keybinding(
        id="file.save",
        key="w",
        modifiers=[KeyModifier.CTRL],
        command="file.save",
        scope=KeybindingScope.GLOBAL
    )
    
    result = manager.update_keybinding("file.save", new_keybinding)
    
    assert result.success == True, "Update başarılı olmalı"
    
    print(f"  Keybinding updated: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Update keybinding")
    print("=" * 70)


def test_search_keybindings():
    """
    Test: Search keybindings.
    """
    print("=" * 70)
    print("TEST: Search Keybindings")
    print("=" * 70)
    
    manager = KeybindingManager()
    
    results = manager.search_keybindings("save")
    
    assert len(results) > 0, "Sonuçlar bulunmalı"
    
    print(f"  Results: {len(results)}")
    
    print("\n" + "=" * 70)
    print("PASS: Search keybindings")
    print("=" * 70)


def test_export_keybindings():
    """
    Test: Export keybindings.
    """
    print("=" * 70)
    print("TEST: Export Keybindings")
    print("=" * 70)
    
    manager = KeybindingManager()
    
    export_data = manager.export_keybindings()
    
    assert "keybindings" in export_data, "Keybindings olmalı"
    assert len(export_data["keybindings"]) > 0, "Export data olmalı"
    
    print(f"  Exported keybindings: {len(export_data['keybindings'])}")
    
    print("\n" + "=" * 70)
    print("PASS: Export keybindings")
    print("=" * 70)


def test_import_keybindings():
    """
    Test: Import keybindings.
    """
    print("=" * 70)
    print("TEST: Import Keybindings")
    print("=" * 70)
    
    manager = KeybindingManager()
    
    import_data = {
        "keybindings": [
            {
                "id": "test.imported",
                "key": "i",
                "modifiers": ["ctrl"],
                "command": "test.command",
                "scope": "global",
                "description": "Imported keybinding"
            }
        ]
    }
    
    result = manager.import_keybindings(import_data)
    
    assert result.success == True, "Import başarılı olmalı"
    
    print(f"  Import result: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Import keybindings")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    manager = KeybindingManager()
    
    new_config = KeybindingConfig(allow_overrides=True)
    manager.update_config(new_config)
    
    assert manager.config.allow_overrides == True, "Config güncellenmeli"
    
    print(f"  Allow overrides: {manager.config.allow_overrides}")
    
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
    
    config = KeybindingConfig(allow_overrides=True)
    manager = KeybindingManager(config)
    
    retrieved_config = manager.get_config()
    
    assert retrieved_config.allow_overrides == True, "Config eşleşmeli"
    
    print(f"  Allow overrides: {retrieved_config.allow_overrides}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_key_modifier_enum()
        test2 = test_keybinding_scope_enum()
        test3 = test_keybinding_dataclass()
        test4 = test_keybinding_config_dataclass()
        test5 = test_keybinding_result_dataclass()
        test6 = test_keybinding_manager_initialization()
        test7 = test_register_keybinding()
        test8 = test_unregister_keybinding()
        test9 = test_get_keybinding()
        test10 = test_get_all_keybindings()
        test11 = test_get_keybindings_by_scope()
        test12 = test_get_keybindings_by_command()
        test13 = test_find_keybinding_by_key()
        test14 = test_check_conflicts()
        test15 = test_update_keybinding()
        test16 = test_search_keybindings()
        test17 = test_export_keybindings()
        test18 = test_import_keybindings()
        test19 = test_update_config()
        test20 = test_get_config()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"KeyModifier Enum: {'PASS' if test1 else 'FAIL'}")
        print(f"KeybindingScope Enum: {'PASS' if test2 else 'FAIL'}")
        print(f"Keybinding Dataclass: {'PASS' if test3 else 'FAIL'}")
        print(f"KeybindingConfig Dataclass: {'PASS' if test4 else 'FAIL'}")
        print(f"KeybindingResult Dataclass: {'PASS' if test5 else 'FAIL'}")
        print(f"KeybindingManager Initialization: {'PASS' if test6 else 'FAIL'}")
        print(f"Register Keybinding: {'PASS' if test7 else 'FAIL'}")
        print(f"Unregister Keybinding: {'PASS' if test8 else 'FAIL'}")
        print(f"Get Keybinding: {'PASS' if test9 else 'FAIL'}")
        print(f"Get All Keybindings: {'PASS' if test10 else 'FAIL'}")
        print(f"Get Keybindings by Scope: {'PASS' if test11 else 'FAIL'}")
        print(f"Get Keybindings by Command: {'PASS' if test12 else 'FAIL'}")
        print(f"Find Keybinding by Key: {'PASS' if test13 else 'FAIL'}")
        print(f"Check Conflicts: {'PASS' if test14 else 'FAIL'}")
        print(f"Update Keybinding: {'PASS' if test15 else 'FAIL'}")
        print(f"Search Keybindings: {'PASS' if test16 else 'FAIL'}")
        print(f"Export Keybindings: {'PASS' if test17 else 'FAIL'}")
        print(f"Import Keybindings: {'PASS' if test18 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test19 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test20 else 'FAIL'}")
        
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
