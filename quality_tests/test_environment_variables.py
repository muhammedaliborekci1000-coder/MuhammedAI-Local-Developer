"""
Quality Test: Environment Variables
Environment variables system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.tools.environment_variables import (
    EnvironmentVariablesEngine,
    VariableScope,
    VariableAction,
    VariableConfig,
    VariableEntry,
    VariableResult
)


def test_set_variable():
    """
    Test: Set variable.
    """
    print("=" * 70)
    print("TEST: Set Variable")
    print("=" * 70)
    
    engine = EnvironmentVariablesEngine()
    result = engine.set_variable("TEST_VAR", "test_value")
    
    assert result.success, "Ayarlama başarılı olmalı"
    assert result.variable_name == "TEST_VAR", "Değişken adı eşleşmeli"
    assert result.variable_value == "test_value", "Değer eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Variable name: {result.variable_name}")
    print(f"  Variable value: {result.variable_value}")
    
    print("\n" + "=" * 70)
    print("PASS: Set variable")
    print("=" * 70)


def test_set_variable_with_scope():
    """
    Test: Set variable with scope.
    """
    print("=" * 70)
    print("TEST: Set Variable With Scope")
    print("=" * 70)
    
    engine = EnvironmentVariablesEngine()
    result = engine.set_variable("TEST_VAR", "test_value", VariableScope.GLOBAL)
    
    assert result.success, "Ayarlama başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Scope: {engine.variables['TEST_VAR'].scope.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Set variable with scope")
    print("=" * 70)


def test_get_variable():
    """
    Test: Get variable.
    """
    print("=" * 70)
    print("TEST: Get Variable")
    print("=" * 70)
    
    engine = EnvironmentVariablesEngine()
    engine.set_variable("TEST_VAR", "test_value")
    
    result = engine.get_variable("TEST_VAR")
    
    assert result.success, "Alma başarılı olmalı"
    assert result.variable_value == "test_value", "Değer eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Variable value: {result.variable_value}")
    
    print("\n" + "=" * 70)
    print("PASS: Get variable")
    print("=" * 70)


def test_unset_variable():
    """
    Test: Unset variable.
    """
    print("=" * 70)
    print("TEST: Unset Variable")
    print("=" * 70)
    
    engine = EnvironmentVariablesEngine()
    engine.set_variable("TEST_VAR", "test_value")
    
    result = engine.unset_variable("TEST_VAR")
    
    assert result.success, "Kaldırma başarılı olmalı"
    assert "TEST_VAR" not in engine.variables, "Değişken kaldırılmış olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Unset variable")
    print("=" * 70)


def test_list_variables():
    """
    Test: List variables.
    """
    print("=" * 70)
    print("TEST: List Variables")
    print("=" * 70)
    
    engine = EnvironmentVariablesEngine()
    engine.set_variable("VAR1", "value1")
    engine.set_variable("VAR2", "value2")
    
    result = engine.list_variables()
    
    assert result.success, "Listeleme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: List variables")
    print("=" * 70)


def test_list_variables_with_scope():
    """
    Test: List variables with scope.
    """
    print("=" * 70)
    print("TEST: List Variables With Scope")
    print("=" * 70)
    
    engine = EnvironmentVariablesEngine()
    engine.set_variable("VAR1", "value1", VariableScope.GLOBAL)
    engine.set_variable("VAR2", "value2", VariableScope.SESSION)
    
    result = engine.list_variables(scope=VariableScope.GLOBAL)
    
    assert result.success, "Listeleme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: List variables with scope")
    print("=" * 70)


def test_clear_variables():
    """
    Test: Clear variables.
    """
    print("=" * 70)
    print("TEST: Clear Variables")
    print("=" * 70)
    
    engine = EnvironmentVariablesEngine()
    engine.set_variable("VAR1", "value1")
    engine.set_variable("VAR2", "value2")
    
    result = engine.clear_variables()
    
    assert result.success, "Temizleme başarılı olmalı"
    assert len(engine.variables) == 0, "Değişkenler temizlenmeli"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear variables")
    print("=" * 70)


def test_clear_variables_with_scope():
    """
    Test: Clear variables with scope.
    """
    print("=" * 70)
    print("TEST: Clear Variables With Scope")
    print("=" * 70)
    
    engine = EnvironmentVariablesEngine()
    engine.set_variable("VAR1", "value1", VariableScope.GLOBAL)
    engine.set_variable("VAR2", "value2", VariableScope.SESSION)
    
    result = engine.clear_variables(scope=VariableScope.GLOBAL)
    
    assert result.success, "Temizleme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear variables with scope")
    print("=" * 70)


def test_export_variables():
    """
    Test: Export variables.
    """
    print("=" * 70)
    print("TEST: Export Variables")
    print("=" * 70)
    
    engine = EnvironmentVariablesEngine()
    engine.set_variable("VAR1", "value1")
    
    result = engine.export_variables(format="json")
    
    assert result.success, "Dışa aktarma başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Export variables")
    print("=" * 70)


def test_import_variables():
    """
    Test: Import variables.
    """
    print("=" * 70)
    print("TEST: Import Variables")
    print("=" * 70)
    
    engine = EnvironmentVariablesEngine()
    
    data = {"VAR1": "value1", "VAR2": "value2"}
    result = engine.import_variables(data)
    
    assert result.success, "İçe aktarma başarılı olmalı"
    assert len(engine.variables) == 2, "2 değişken aktarılmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Import variables")
    print("=" * 70)


def test_get_variable_history():
    """
    Test: Get variable history.
    """
    print("=" * 70)
    print("TEST: Get Variable History")
    print("=" * 70)
    
    engine = EnvironmentVariablesEngine()
    engine.set_variable("TEST_VAR", "test_value")
    
    history = engine.get_variable_history()
    
    assert len(history) > 0, "Geçmiş olmalı"
    
    print(f"  History: {len(history)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get variable history")
    print("=" * 70)


def test_clear_history():
    """
    Test: Clear history.
    """
    print("=" * 70)
    print("TEST: Clear History")
    print("=" * 70)
    
    engine = EnvironmentVariablesEngine()
    engine.set_variable("TEST_VAR", "test_value")
    
    result = engine.clear_history()
    
    assert result.success, "Temizleme başarılı olmalı"
    assert len(engine.get_variable_history()) == 0, "Geçmiş temizlenmeli"
    
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
    
    engine = EnvironmentVariablesEngine()
    
    new_config = VariableConfig(persist_variables=False)
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
    
    engine = EnvironmentVariablesEngine()
    
    config = engine.get_config()
    
    assert config is not None, "Config olmalı"
    assert config.persist_variables == True, "Config eşleşmeli"
    
    print(f"  Persist variables: {config.persist_variables}")
    print(f"  Auto load from system: {config.auto_load_from_system}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


def test_variable_scope_enum():
    """
    Test: VariableScope enum.
    """
    print("=" * 70)
    print("TEST: VariableScope Enum")
    print("=" * 70)
    
    assert VariableScope.SESSION.value == "session"
    assert VariableScope.TERMINAL.value == "terminal"
    assert VariableScope.GLOBAL.value == "global"
    
    print(f"  All enum values verified")
    print(f"  Total scopes: {len(VariableScope)}")
    
    print("\n" + "=" * 70)
    print("PASS: VariableScope enum")
    print("=" * 70)


def test_variable_action_enum():
    """
    Test: VariableAction enum.
    """
    print("=" * 70)
    print("TEST: VariableAction Enum")
    print("=" * 70)
    
    assert VariableAction.SET.value == "set"
    assert VariableAction.GET.value == "get"
    assert VariableAction.UNSET.value == "unset"
    assert VariableAction.LIST.value == "list"
    assert VariableAction.CLEAR.value == "clear"
    assert VariableAction.IMPORT.value == "import"
    assert VariableAction.EXPORT.value == "export"
    
    print(f"  All enum values verified")
    print(f"  Total actions: {len(VariableAction)}")
    
    print("\n" + "=" * 70)
    print("PASS: VariableAction enum")
    print("=" * 70)


def test_variable_config_dataclass():
    """
    Test: VariableConfig dataclass.
    """
    print("=" * 70)
    print("TEST: VariableConfig Dataclass")
    print("=" * 70)
    
    config = VariableConfig(
        persist_variables=False,
        auto_load_from_system=False
    )
    
    assert config.persist_variables == False, "Persist eşleşmeli"
    assert config.auto_load_from_system == False, "Auto load eşleşmeli"
    
    print(f"  Persist variables: {config.persist_variables}")
    print(f"  Auto load from system: {config.auto_load_from_system}")
    
    print("\n" + "=" * 70)
    print("PASS: VariableConfig dataclass")
    print("=" * 70)


def test_variable_entry_dataclass():
    """
    Test: VariableEntry dataclass.
    """
    print("=" * 70)
    print("TEST: VariableEntry Dataclass")
    print("=" * 70)
    
    entry = VariableEntry(
        name="TEST_VAR",
        value="test_value",
        scope=VariableScope.SESSION,
        timestamp="2024-01-01T00:00:00"
    )
    
    assert entry.name == "TEST_VAR", "Ad eşleşmeli"
    assert entry.value == "test_value", "Değer eşleşmeli"
    
    print(f"  Name: {entry.name}")
    print(f"  Value: {entry.value}")
    
    print("\n" + "=" * 70)
    print("PASS: VariableEntry dataclass")
    print("=" * 70)


def test_variable_result_dataclass():
    """
    Test: VariableResult dataclass.
    """
    print("=" * 70)
    print("TEST: VariableResult Dataclass")
    print("=" * 70)
    
    result = VariableResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: VariableResult dataclass")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_set_variable()
        test2 = test_set_variable_with_scope()
        test3 = test_get_variable()
        test4 = test_unset_variable()
        test5 = test_list_variables()
        test6 = test_list_variables_with_scope()
        test7 = test_clear_variables()
        test8 = test_clear_variables_with_scope()
        test9 = test_export_variables()
        test10 = test_import_variables()
        test11 = test_get_variable_history()
        test12 = test_clear_history()
        test13 = test_update_config()
        test14 = test_get_config()
        test15 = test_variable_scope_enum()
        test16 = test_variable_action_enum()
        test17 = test_variable_config_dataclass()
        test18 = test_variable_entry_dataclass()
        test19 = test_variable_result_dataclass()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Set Variable: {'PASS' if test1 else 'FAIL'}")
        print(f"Set Variable With Scope: {'PASS' if test2 else 'FAIL'}")
        print(f"Get Variable: {'PASS' if test3 else 'FAIL'}")
        print(f"Unset Variable: {'PASS' if test4 else 'FAIL'}")
        print(f"List Variables: {'PASS' if test5 else 'FAIL'}")
        print(f"List Variables With Scope: {'PASS' if test6 else 'FAIL'}")
        print(f"Clear Variables: {'PASS' if test7 else 'FAIL'}")
        print(f"Clear Variables With Scope: {'PASS' if test8 else 'FAIL'}")
        print(f"Export Variables: {'PASS' if test9 else 'FAIL'}")
        print(f"Import Variables: {'PASS' if test10 else 'FAIL'}")
        print(f"Get Variable History: {'PASS' if test11 else 'FAIL'}")
        print(f"Clear History: {'PASS' if test12 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test13 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test14 else 'FAIL'}")
        print(f"VariableScope Enum: {'PASS' if test15 else 'FAIL'}")
        print(f"VariableAction Enum: {'PASS' if test16 else 'FAIL'}")
        print(f"VariableConfig Dataclass: {'PASS' if test17 else 'FAIL'}")
        print(f"VariableEntry Dataclass: {'PASS' if test18 else 'FAIL'}")
        print(f"VariableResult Dataclass: {'PASS' if test19 else 'FAIL'}")
        
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
