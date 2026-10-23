"""
Quality Test: Keyboard Shortcuts
Keyboard shortcuts system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.keyboard_shortcuts import (
    KeyboardShortcutsEngine,
    ModifierKey,
    KeyCategory,
    KeyBinding,
    ShortcutConflict,
    KeyBindingResult
)


def test_register_binding():
    """
    Test: Register binding.
    """
    print("=" * 70)
    print("TEST: Register Binding")
    print("=" * 70)
    
    engine = KeyboardShortcutsEngine()
    
    binding = KeyBinding(
        key="q",
        modifiers=[ModifierKey.CTRL],
        action="quit",
        description="Quit",
        category=KeyCategory.CUSTOM
    )
    
    result = engine.register_binding(binding)
    
    assert result.success, "Register binding başarılı olmalı"
    assert result.action == "quit", "Action eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Action: {result.action}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Register binding")
    print("=" * 70)


def test_get_binding():
    """
    Test: Get binding.
    """
    print("=" * 70)
    print("TEST: Get Binding")
    print("=" * 70)
    
    engine = KeyboardShortcutsEngine()
    binding = engine.get_binding("s", [ModifierKey.CTRL])
    
    assert binding is not None, "Binding bulunmalı"
    assert binding.action == "save", "Action save olmalı"
    
    print(f"  Action: {binding.action}")
    print(f"  Description: {binding.description}")
    print(f"  Category: {binding.category.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Get binding")
    print("=" * 70)


def test_get_binding_by_action():
    """
    Test: Get binding by action.
    """
    print("=" * 70)
    print("TEST: Get Binding By Action")
    print("=" * 70)
    
    engine = KeyboardShortcutsEngine()
    binding = engine.get_binding_by_action("save")
    
    assert binding is not None, "Binding bulunmalı"
    assert binding.key == "s", "Key s olmalı"
    
    print(f"  Key: {binding.key}")
    print(f"  Action: {binding.action}")
    
    print("\n" + "=" * 70)
    print("PASS: Get binding by action")
    print("=" * 70)


def test_remove_binding():
    """
    Test: Remove binding.
    """
    print("=" * 70)
    print("TEST: Remove Binding")
    print("=" * 70)
    
    engine = KeyboardShortcutsEngine()
    
    # Custom binding ekle
    binding = KeyBinding(
        key="q",
        modifiers=[ModifierKey.CTRL],
        action="quit",
        description="Quit",
        category=KeyCategory.CUSTOM
    )
    engine.register_binding(binding)
    
    # Kaldır
    success = engine.remove_binding("q", [ModifierKey.CTRL])
    
    assert success, "Binding kaldırılmalı"
    
    # Verify
    found = engine.get_binding("q", [ModifierKey.CTRL])
    assert found is None, "Binding bulunmamalı"
    
    print(f"  Success: {success}")
    
    print("\n" + "=" * 70)
    print("PASS: Remove binding")
    print("=" * 70)


def test_get_bindings_by_category():
    """
    Test: Get bindings by category.
    """
    print("=" * 70)
    print("TEST: Get Bindings By Category")
    print("=" * 70)
    
    engine = KeyboardShortcutsEngine()
    bindings = engine.get_bindings_by_category(KeyCategory.EDITING)
    
    assert len(bindings) > 0, "Binding'lar olmalı"
    
    print(f"  Total bindings: {len(bindings)}")
    
    for binding in bindings[:5]:
        print(f"  - {binding.key}: {binding.action}")
    
    print("\n" + "=" * 70)
    print("PASS: Get bindings by category")
    print("=" * 70)


def test_get_all_bindings():
    """
    Test: Get all bindings.
    """
    print("=" * 70)
    print("TEST: Get All Bindings")
    print("=" * 70)
    
    engine = KeyboardShortcutsEngine()
    bindings = engine.get_all_bindings()
    
    assert len(bindings) > 0, "Binding'lar olmalı"
    
    print(f"  Total bindings: {len(bindings)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get all bindings")
    print("=" * 70)


def test_check_conflicts():
    """
    Test: Check conflicts.
    """
    print("=" * 70)
    print("TEST: Check Conflicts")
    print("=" * 70)
    
    engine = KeyboardShortcutsEngine()
    
    # Conflict oluştur
    binding = KeyBinding(
        key="s",
        modifiers=[ModifierKey.CTRL],
        action="custom_save",
        description="Custom save",
        category=KeyCategory.CUSTOM
    )
    
    conflicts = engine.check_conflicts(binding)
    
    # Builtin ile conflict olmaz, custom ile olur
    print(f"  Conflicts: {len(conflicts)}")
    
    print("\n" + "=" * 70)
    print("PASS: Check conflicts")
    print("=" * 70)


def test_validate_binding():
    """
    Test: Validate binding.
    """
    print("=" * 70)
    print("TEST: Validate Binding")
    print("=" * 70)
    
    engine = KeyboardShortcutsEngine()
    
    # Valid binding
    valid_binding = KeyBinding(
        key="q",
        modifiers=[ModifierKey.CTRL],
        action="quit",
        description="Quit",
        category=KeyCategory.CUSTOM
    )
    
    is_valid, errors = engine.validate_binding(valid_binding)
    assert is_valid, "Binding geçerli olmalı"
    
    # Invalid binding (no key)
    invalid_binding = KeyBinding(
        key="",
        modifiers=[ModifierKey.CTRL],
        action="quit",
        description="Quit",
        category=KeyCategory.CUSTOM
    )
    
    is_valid, errors = engine.validate_binding(invalid_binding)
    assert not is_valid, "Binding geçersiz olmalı"
    assert len(errors) > 0, "Hatalar olmalı"
    
    print(f"  Valid binding: {is_valid}")
    print(f"  Invalid binding errors: {errors}")
    
    print("\n" + "=" * 70)
    print("PASS: Validate binding")
    print("=" * 70)


def test_export_bindings():
    """
    Test: Export bindings.
    """
    print("=" * 70)
    print("TEST: Export Bindings")
    print("=" * 70)
    
    engine = KeyboardShortcutsEngine()
    
    # Custom binding ekle
    binding = KeyBinding(
        key="q",
        modifiers=[ModifierKey.CTRL],
        action="quit",
        description="Quit",
        category=KeyCategory.CUSTOM
    )
    engine.register_binding(binding)
    
    export_data = engine.export_bindings()
    
    assert "bindings" in export_data, "Bindings olmalı"
    assert len(export_data["bindings"]) > 0, "Export data olmalı"
    
    print(f"  Exported bindings: {len(export_data['bindings'])}")
    
    print("\n" + "=" * 70)
    print("PASS: Export bindings")
    print("=" * 70)


def test_import_bindings():
    """
    Test: Import bindings.
    """
    print("=" * 70)
    print("TEST: Import Bindings")
    print("=" * 70)
    
    engine = KeyboardShortcutsEngine()
    
    import_data = {
        "bindings": [
            {
                "key": "q",
                "modifiers": ["ctrl"],
                "action": "quit",
                "description": "Quit",
                "category": "custom",
                "when": ""
            }
        ]
    }
    
    result = engine.import_bindings(import_data)
    
    assert result.success, "Import başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Import bindings")
    print("=" * 70)


def test_reset_to_defaults():
    """
    Test: Reset to defaults.
    """
    print("=" * 70)
    print("TEST: Reset To Defaults")
    print("=" * 70)
    
    engine = KeyboardShortcutsEngine()
    
    # Custom binding ekle
    binding = KeyBinding(
        key="q",
        modifiers=[ModifierKey.CTRL],
        action="quit",
        description="Quit",
        category=KeyCategory.CUSTOM
    )
    engine.register_binding(binding)
    
    # Reset
    result = engine.reset_to_defaults()
    
    assert result.success, "Reset başarılı olmalı"
    
    # Verify
    found = engine.get_binding("q", [ModifierKey.CTRL])
    assert found is None, "Custom binding kaldırılmış olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Reset to defaults")
    print("=" * 70)


def test_get_categories():
    """
    Test: Get categories.
    """
    print("=" * 70)
    print("TEST: Get Categories")
    print("=" * 70)
    
    engine = KeyboardShortcutsEngine()
    categories = engine.get_categories()
    
    assert len(categories) > 0, "Kategoriler olmalı"
    
    print(f"  Categories: {[c.value for c in categories]}")
    
    print("\n" + "=" * 70)
    print("PASS: Get categories")
    print("=" * 70)


def test_modifier_key_enum():
    """
    Test: ModifierKey enum.
    """
    print("=" * 70)
    print("TEST: ModifierKey Enum")
    print("=" * 70)
    
    assert ModifierKey.CTRL.value == "ctrl"
    assert ModifierKey.ALT.value == "alt"
    assert ModifierKey.SHIFT.value == "shift"
    assert ModifierKey.META.value == "meta"
    assert ModifierKey.CMD.value == "cmd"
    
    print(f"  All enum values verified")
    print(f"  Total keys: {len(ModifierKey)}")
    
    print("\n" + "=" * 70)
    print("PASS: ModifierKey enum")
    print("=" * 70)


def test_key_category_enum():
    """
    Test: KeyCategory enum.
    """
    print("=" * 70)
    print("TEST: KeyCategory Enum")
    print("=" * 70)
    
    assert KeyCategory.EDITING.value == "editing"
    assert KeyCategory.NAVIGATION.value == "navigation"
    assert KeyCategory.SELECTION.value == "selection"
    assert KeyCategory.VIEW.value == "view"
    assert KeyCategory.SEARCH.value == "search"
    assert KeyCategory.TERMINAL.value == "terminal"
    assert KeyCategory.DEBUG.value == "debug"
    assert KeyCategory.GIT.value == "git"
    assert KeyCategory.CUSTOM.value == "custom"
    
    print(f"  All enum values verified")
    print(f"  Total categories: {len(KeyCategory)}")
    
    print("\n" + "=" * 70)
    print("PASS: KeyCategory enum")
    print("=" * 70)


def test_key_binding_dataclass():
    """
    Test: KeyBinding dataclass.
    """
    print("=" * 70)
    print("TEST: KeyBinding Dataclass")
    print("=" * 70)
    
    binding = KeyBinding(
        key="q",
        modifiers=[ModifierKey.CTRL],
        action="quit",
        description="Quit",
        category=KeyCategory.CUSTOM
    )
    
    assert binding.key == "q", "Key eşleşmeli"
    assert binding.action == "quit", "Action eşleşmeli"
    assert binding.category == KeyCategory.CUSTOM, "Category eşleşmeli"
    
    print(f"  Key: {binding.key}")
    print(f"  Action: {binding.action}")
    print(f"  Category: {binding.category.value}")
    
    print("\n" + "=" * 70)
    print("PASS: KeyBinding dataclass")
    print("=" * 70)


def test_shortcut_conflict_dataclass():
    """
    Test: ShortcutConflict dataclass.
    """
    print("=" * 70)
    print("TEST: ShortcutConflict Dataclass")
    print("=" * 70)
    
    binding1 = KeyBinding(key="q", modifiers=[ModifierKey.CTRL], action="quit", category=KeyCategory.CUSTOM)
    binding2 = KeyBinding(key="q", modifiers=[ModifierKey.CTRL], action="custom_quit", category=KeyCategory.CUSTOM)
    
    conflict = ShortcutConflict(
        existing_binding=binding1,
        new_binding=binding2
    )
    
    assert conflict.existing_binding.action == "quit", "Existing binding eşleşmeli"
    assert conflict.new_binding.action == "custom_quit", "New binding eşleşmeli"
    
    print(f"  Existing action: {conflict.existing_binding.action}")
    print(f"  New action: {conflict.new_binding.action}")
    
    print("\n" + "=" * 70)
    print("PASS: ShortcutConflict dataclass")
    print("=" * 70)


def test_key_binding_result_dataclass():
    """
    Test: KeyBindingResult dataclass.
    """
    print("=" * 70)
    print("TEST: KeyBindingResult Dataclass")
    print("=" * 70)
    
    result = KeyBindingResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.conflicts, list), "Conflicts list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Conflicts: {len(result.conflicts)}")
    
    print("\n" + "=" * 70)
    print("PASS: KeyBindingResult dataclass")
    print("=" * 70)


def test_builtin_shortcuts():
    """
    Test: Builtin shortcuts.
    """
    print("=" * 70)
    print("TEST: Builtin Shortcuts")
    print("=" * 70)
    
    engine = KeyboardShortcutsEngine()
    all_bindings = engine.get_all_bindings()
    
    builtin_count = len([b for b in all_bindings if b.is_builtin])
    
    assert builtin_count > 0, "Builtin shortcut'lar olmalı"
    
    print(f"  Builtin shortcuts: {builtin_count}")
    print(f"  Total shortcuts: {len(all_bindings)}")
    
    # Check some common shortcuts
    save_binding = engine.get_binding("s", [ModifierKey.CTRL])
    assert save_binding is not None, "Save shortcut olmalı"
    
    undo_binding = engine.get_binding("z", [ModifierKey.CTRL])
    assert undo_binding is not None, "Undo shortcut olmalı"
    
    print(f"  Save shortcut: {save_binding.action}")
    print(f"  Undo shortcut: {undo_binding.action}")
    
    print("\n" + "=" * 70)
    print("PASS: Builtin shortcuts")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_register_binding()
        test2 = test_get_binding()
        test3 = test_get_binding_by_action()
        test4 = test_remove_binding()
        test5 = test_get_bindings_by_category()
        test6 = test_get_all_bindings()
        test7 = test_check_conflicts()
        test8 = test_validate_binding()
        test9 = test_export_bindings()
        test10 = test_import_bindings()
        test11 = test_reset_to_defaults()
        test12 = test_get_categories()
        test13 = test_modifier_key_enum()
        test14 = test_key_category_enum()
        test15 = test_key_binding_dataclass()
        test16 = test_shortcut_conflict_dataclass()
        test17 = test_key_binding_result_dataclass()
        test18 = test_builtin_shortcuts()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Register Binding: {'PASS' if test1 else 'FAIL'}")
        print(f"Get Binding: {'PASS' if test2 else 'FAIL'}")
        print(f"Get Binding By Action: {'PASS' if test3 else 'FAIL'}")
        print(f"Remove Binding: {'PASS' if test4 else 'FAIL'}")
        print(f"Get Bindings By Category: {'PASS' if test5 else 'FAIL'}")
        print(f"Get All Bindings: {'PASS' if test6 else 'FAIL'}")
        print(f"Check Conflicts: {'PASS' if test7 else 'FAIL'}")
        print(f"Validate Binding: {'PASS' if test8 else 'FAIL'}")
        print(f"Export Bindings: {'PASS' if test9 else 'FAIL'}")
        print(f"Import Bindings: {'PASS' if test10 else 'FAIL'}")
        print(f"Reset To Defaults: {'PASS' if test11 else 'FAIL'}")
        print(f"Get Categories: {'PASS' if test12 else 'FAIL'}")
        print(f"ModifierKey Enum: {'PASS' if test13 else 'FAIL'}")
        print(f"KeyCategory Enum: {'PASS' if test14 else 'FAIL'}")
        print(f"KeyBinding Dataclass: {'PASS' if test15 else 'FAIL'}")
        print(f"ShortcutConflict Dataclass: {'PASS' if test16 else 'FAIL'}")
        print(f"KeyBindingResult Dataclass: {'PASS' if test17 else 'FAIL'}")
        print(f"Builtin Shortcuts: {'PASS' if test18 else 'FAIL'}")
        
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
