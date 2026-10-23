"""
Quality Test: Refactoring (Editor)
Refactoring system testleri for editor module.
"""

import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from app.editor.refactoring import (
    RefactoringType,
    RefactoringScope,
    RefactoringRange,
    RefactoringChange,
    RefactoringOperation,
    RefactoringConfig,
    RefactoringResult,
    RefactoringManager
)


def test_refactoring_type_enum():
    """
    Test: RefactoringType enum.
    """
    print("=" * 70)
    print("TEST: RefactoringType Enum")
    print("=" * 70)
    
    assert RefactoringType.RENAME.value == "rename"
    assert RefactoringType.EXTRACT_FUNCTION.value == "extract_function"
    assert RefactoringType.EXTRACT_VARIABLE.value == "extract_variable"
    assert RefactoringType.INLINE_FUNCTION.value == "inline_function"
    assert RefactoringType.INLINE_VARIABLE.value == "inline_variable"
    assert RefactoringType.MOVE_CODE.value == "move_code"
    assert RefactoringType.CHANGE_SIGNATURE.value == "change_signature"
    assert RefactoringType.INTRODUCE_VARIABLE.value == "introduce_variable"
    assert RefactoringType.ENCAPSULATE_FIELD.value == "encapsulate_field"
    assert RefactoringType.PULL_UP.value == "pull_up"
    assert RefactoringType.PUSH_DOWN.value == "push_down"
    assert RefactoringType.CUSTOM.value == "custom"
    
    print(f"  All enum values verified")
    print(f"  Total types: {len(RefactoringType)}")
    
    print("\n" + "=" * 70)
    print("PASS: RefactoringType enum")
    print("=" * 70)


def test_refactoring_scope_enum():
    """
    Test: RefactoringScope enum.
    """
    print("=" * 70)
    print("TEST: RefactoringScope Enum")
    print("=" * 70)
    
    assert RefactoringScope.LOCAL.value == "local"
    assert RefactoringScope.FILE.value == "file"
    assert RefactoringScope.PROJECT.value == "project"
    
    print(f"  All enum values verified")
    print(f"  Total scopes: {len(RefactoringScope)}")
    
    print("\n" + "=" * 70)
    print("PASS: RefactoringScope enum")
    print("=" * 70)


def test_refactoring_range_dataclass():
    """
    Test: RefactoringRange dataclass.
    """
    print("=" * 70)
    print("TEST: RefactoringRange Dataclass")
    print("=" * 70)
    
    range = RefactoringRange(
        start_line=0,
        start_column=0,
        end_line=10,
        end_column=20
    )
    
    assert range.start_line == 0, "Start line eşleşmeli"
    assert range.start_column == 0, "Start column eşleşmeli"
    assert range.end_line == 10, "End line eşleşmeli"
    assert range.end_column == 20, "End column eşleşmeli"
    
    print(f"  Start: ({range.start_line}, {range.start_column})")
    print(f"  End: ({range.end_line}, {range.end_column})")
    
    print("\n" + "=" * 70)
    print("PASS: RefactoringRange dataclass")
    print("=" * 70)


def test_refactoring_change_dataclass():
    """
    Test: RefactoringChange dataclass.
    """
    print("=" * 70)
    print("TEST: RefactoringChange Dataclass")
    print("=" * 70)
    
    range = RefactoringRange(0, 0, 0, 10)
    change = RefactoringChange(
        file_path="test.py",
        range=range,
        old_text="old",
        new_text="new"
    )
    
    assert change.file_path == "test.py", "File path eşleşmeli"
    assert change.old_text == "old", "Old text eşleşmeli"
    assert change.new_text == "new", "New text eşleşmeli"
    
    print(f"  File path: {change.file_path}")
    print(f"  Old text: {change.old_text}")
    print(f"  New text: {change.new_text}")
    
    print("\n" + "=" * 70)
    print("PASS: RefactoringChange dataclass")
    print("=" * 70)


def test_refactoring_operation_dataclass():
    """
    Test: RefactoringOperation dataclass.
    """
    print("=" * 70)
    print("TEST: RefactoringOperation Dataclass")
    print("=" * 70)
    
    range = RefactoringRange(0, 0, 0, 10)
    change = RefactoringChange(
        file_path="test.py",
        range=range,
        old_text="old",
        new_text="new"
    )
    
    operation = RefactoringOperation(
        id="operation_1",
        type=RefactoringType.RENAME,
        scope=RefactoringScope.FILE,
        changes=[change]
    )
    
    assert operation.id == "operation_1", "ID eşleşmeli"
    assert operation.type == RefactoringType.RENAME, "Type eşleşmeli"
    assert operation.scope == RefactoringScope.FILE, "Scope eşleşmeli"
    
    print(f"  ID: {operation.id}")
    print(f"  Type: {operation.type.value}")
    print(f"  Scope: {operation.scope.value}")
    
    print("\n" + "=" * 70)
    print("PASS: RefactoringOperation dataclass")
    print("=" * 70)


def test_refactoring_config_dataclass():
    """
    Test: RefactoringConfig dataclass.
    """
    print("=" * 70)
    print("TEST: RefactoringConfig Dataclass")
    print("=" * 70)
    
    config = RefactoringConfig(
        enabled=True,
        scope=RefactoringScope.PROJECT
    )
    
    assert config.enabled == True, "Enabled eşleşmeli"
    assert config.scope == RefactoringScope.PROJECT, "Scope eşleşmeli"
    
    print(f"  Enabled: {config.enabled}")
    print(f"  Scope: {config.scope.value}")
    
    print("\n" + "=" * 70)
    print("PASS: RefactoringConfig dataclass")
    print("=" * 70)


def test_refactoring_result_dataclass():
    """
    Test: RefactoringResult dataclass.
    """
    print("=" * 70)
    print("TEST: RefactoringResult Dataclass")
    print("=" * 70)
    
    result = RefactoringResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.changes, list), "Changes list olmalı"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Changes: {len(result.changes)}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: RefactoringResult dataclass")
    print("=" * 70)


def test_refactoring_manager_initialization():
    """
    Test: RefactoringManager initialization.
    """
    print("=" * 70)
    print("TEST: RefactoringManager Initialization")
    print("=" * 70)
    
    config = RefactoringConfig()
    manager = RefactoringManager(config)
    
    assert manager.config == config, "Config eşleşmeli"
    assert len(manager.operations) == 0, "Operations boş olmalı"
    assert manager.undo_stack == [], "Undo stack boş olmalı"
    
    print(f"  Operations: {len(manager.operations)}")
    print(f"  Undo stack: {len(manager.undo_stack)}")
    
    print("\n" + "=" * 70)
    print("PASS: RefactoringManager initialization")
    print("=" * 70)


def test_add_operation():
    """
    Test: Add operation.
    """
    print("=" * 70)
    print("TEST: Add Operation")
    print("=" * 70)
    
    manager = RefactoringManager()
    
    range = RefactoringRange(0, 0, 0, 10)
    change = RefactoringChange(
        file_path="test.py",
        range=range,
        old_text="old",
        new_text="new"
    )
    
    operation = RefactoringOperation(
        id="",
        type=RefactoringType.RENAME,
        scope=RefactoringScope.FILE,
        changes=[change]
    )
    
    result = manager.add_operation(operation)
    
    assert result.success == True, "Ekleme başarılı olmalı"
    assert len(manager.operations) > 0, "Operation eklenmeli"
    
    print(f"  Operation added: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add operation")
    print("=" * 70)


def test_remove_operation():
    """
    Test: Remove operation.
    """
    print("=" * 70)
    print("TEST: Remove Operation")
    print("=" * 70)
    
    manager = RefactoringManager()
    
    range = RefactoringRange(0, 0, 0, 10)
    change = RefactoringChange(
        file_path="test.py",
        range=range,
        old_text="old",
        new_text="new"
    )
    
    operation = RefactoringOperation(
        id="",
        type=RefactoringType.RENAME,
        scope=RefactoringScope.FILE,
        changes=[change]
    )
    
    result = manager.add_operation(operation)
    operation_id = result.operation.id
    
    result = manager.remove_operation(operation_id)
    
    assert result.success == True, "Kaldırma başarılı olmalı"
    assert operation_id not in manager.operations, "Operation silinmeli"
    
    print(f"  Operation removed: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Remove operation")
    print("=" * 70)


def test_get_operation():
    """
    Test: Get operation.
    """
    print("=" * 70)
    print("TEST: Get Operation")
    print("=" * 70)
    
    manager = RefactoringManager()
    
    range = RefactoringRange(0, 0, 0, 10)
    change = RefactoringChange(
        file_path="test.py",
        range=range,
        old_text="old",
        new_text="new"
    )
    
    operation = RefactoringOperation(
        id="",
        type=RefactoringType.RENAME,
        scope=RefactoringScope.FILE,
        changes=[change]
    )
    
    result = manager.add_operation(operation)
    operation_id = result.operation.id
    
    retrieved_operation = manager.get_operation(operation_id)
    
    assert retrieved_operation is not None, "Operation bulunmalı"
    assert retrieved_operation.id == operation_id, "ID eşleşmeli"
    
    print(f"  Operation: {retrieved_operation.type.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Get operation")
    print("=" * 70)


def test_get_all_operations():
    """
    Test: Get all operations.
    """
    print("=" * 70)
    print("TEST: Get All Operations")
    print("=" * 70)
    
    manager = RefactoringManager()
    
    range = RefactoringRange(0, 0, 0, 10)
    change = RefactoringChange(
        file_path="test.py",
        range=range,
        old_text="old",
        new_text="new"
    )
    
    operation = RefactoringOperation(
        id="",
        type=RefactoringType.RENAME,
        scope=RefactoringScope.FILE,
        changes=[change]
    )
    
    manager.add_operation(operation)
    operations = manager.get_all_operations()
    
    assert len(operations) > 0, "Operations olmalı"
    
    print(f"  Total operations: {len(operations)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get all operations")
    print("=" * 70)


def test_get_operations_by_type():
    """
    Test: Get operations by type.
    """
    print("=" * 70)
    print("TEST: Get Operations by Type")
    print("=" * 70)
    
    manager = RefactoringManager()
    
    range = RefactoringRange(0, 0, 0, 10)
    change = RefactoringChange(
        file_path="test.py",
        range=range,
        old_text="old",
        new_text="new"
    )
    
    operation = RefactoringOperation(
        id="",
        type=RefactoringType.RENAME,
        scope=RefactoringScope.FILE,
        changes=[change]
    )
    
    manager.add_operation(operation)
    operations = manager.get_operations_by_type(RefactoringType.RENAME)
    
    assert len(operations) > 0, "Rename operations olmalı"
    
    print(f"  Rename operations: {len(operations)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get operations by type")
    print("=" * 70)


def test_create_rename_operation():
    """
    Test: Create rename operation.
    """
    print("=" * 70)
    print("TEST: Create Rename Operation")
    print("=" * 70)
    
    manager = RefactoringManager()
    
    range = RefactoringRange(0, 0, 0, 10)
    result = manager.create_rename_operation("test.py", range, "old_name", "new_name")
    
    assert result.success == True, "Rename operation başarılı olmalı"
    
    print(f"  Rename operation: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Create rename operation")
    print("=" * 70)


def test_create_extract_function_operation():
    """
    Test: Create extract function operation.
    """
    print("=" * 70)
    print("TEST: Create Extract Function Operation")
    print("=" * 70)
    
    manager = RefactoringManager()
    
    range = RefactoringRange(0, 0, 0, 10)
    result = manager.create_extract_function_operation("test.py", range, "new_function")
    
    assert result.success == True, "Extract function operation başarılı olmalı"
    
    print(f"  Extract function operation: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Create extract function operation")
    print("=" * 70)


def test_create_extract_variable_operation():
    """
    Test: Create extract variable operation.
    """
    print("=" * 70)
    print("TEST: Create Extract Variable Operation")
    print("=" * 70)
    
    manager = RefactoringManager()
    
    range = RefactoringRange(0, 0, 0, 10)
    result = manager.create_extract_variable_operation("test.py", range, "new_variable")
    
    assert result.success == True, "Extract variable operation başarılı olmalı"
    
    print(f"  Extract variable operation: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Create extract variable operation")
    print("=" * 70)


def test_create_inline_function_operation():
    """
    Test: Create inline function operation.
    """
    print("=" * 70)
    print("TEST: Create Inline Function Operation")
    print("=" * 70)
    
    manager = RefactoringManager()
    
    range = RefactoringRange(0, 0, 0, 10)
    result = manager.create_inline_function_operation("test.py", range)
    
    assert result.success == True, "Inline function operation başarılı olmalı"
    
    print(f"  Inline function operation: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Create inline function operation")
    print("=" * 70)


def test_create_inline_variable_operation():
    """
    Test: Create inline variable operation.
    """
    print("=" * 70)
    print("TEST: Create Inline Variable Operation")
    print("=" * 70)
    
    manager = RefactoringManager()
    
    range = RefactoringRange(0, 0, 0, 10)
    result = manager.create_inline_variable_operation("test.py", range)
    
    assert result.success == True, "Inline variable operation başarılı olmalı"
    
    print(f"  Inline variable operation: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Create inline variable operation")
    print("=" * 70)


def test_apply_operation():
    """
    Test: Apply operation.
    """
    print("=" * 70)
    print("TEST: Apply Operation")
    print("=" * 70)
    
    manager = RefactoringManager()
    
    range = RefactoringRange(0, 0, 0, 10)
    result = manager.create_rename_operation("test.py", range, "old_name", "new_name")
    operation_id = result.operation.id
    
    result = manager.apply_operation(operation_id)
    
    assert result.success == True, "Apply başarılı olmalı"
    
    print(f"  Apply operation: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Apply operation")
    print("=" * 70)


def test_undo_operation():
    """
    Test: Undo operation.
    """
    print("=" * 70)
    print("TEST: Undo Operation")
    print("=" * 70)
    
    manager = RefactoringManager()
    
    range = RefactoringRange(0, 0, 0, 10)
    result = manager.create_rename_operation("test.py", range, "old_name", "new_name")
    operation_id = result.operation.id
    
    manager.apply_operation(operation_id)
    result = manager.undo_operation()
    
    assert result.success == True, "Undo başarılı olmalı"
    
    print(f"  Undo operation: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Undo operation")
    print("=" * 70)


def test_clear_operations():
    """
    Test: Clear operations.
    """
    print("=" * 70)
    print("TEST: Clear Operations")
    print("=" * 70)
    
    manager = RefactoringManager()
    
    range = RefactoringRange(0, 0, 0, 10)
    result = manager.create_rename_operation("test.py", range, "old_name", "new_name")
    
    result = manager.clear_operations()
    
    assert result.success == True, "Clear başarılı olmalı"
    assert len(manager.operations) == 0, "Operations temizlenmeli"
    
    print(f"  Cleared: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear operations")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    manager = RefactoringManager()
    
    new_config = RefactoringConfig(max_changes=200)
    result = manager.update_config(new_config)
    
    assert result.success == True, "Update başarılı olmalı"
    assert manager.config.max_changes == 200, "Config güncellenmeli"
    
    print(f"  Max changes: {manager.config.max_changes}")
    
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
    
    config = RefactoringConfig(max_changes=200)
    manager = RefactoringManager(config)
    
    retrieved_config = manager.get_config()
    
    assert retrieved_config.max_changes == 200, "Config eşleşmeli"
    
    print(f"  Max changes: {retrieved_config.max_changes}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_refactoring_type_enum()
        test2 = test_refactoring_scope_enum()
        test3 = test_refactoring_range_dataclass()
        test4 = test_refactoring_change_dataclass()
        test5 = test_refactoring_operation_dataclass()
        test6 = test_refactoring_config_dataclass()
        test7 = test_refactoring_result_dataclass()
        test8 = test_refactoring_manager_initialization()
        test9 = test_add_operation()
        test10 = test_remove_operation()
        test11 = test_get_operation()
        test12 = test_get_all_operations()
        test13 = test_get_operations_by_type()
        test14 = test_create_rename_operation()
        test15 = test_create_extract_function_operation()
        test16 = test_create_extract_variable_operation()
        test17 = test_create_inline_function_operation()
        test18 = test_create_inline_variable_operation()
        test19 = test_apply_operation()
        test20 = test_undo_operation()
        test21 = test_clear_operations()
        test22 = test_update_config()
        test23 = test_get_config()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"RefactoringType Enum: {'PASS' if test1 else 'FAIL'}")
        print(f"RefactoringScope Enum: {'PASS' if test2 else 'FAIL'}")
        print(f"RefactoringRange Dataclass: {'PASS' if test3 else 'FAIL'}")
        print(f"RefactoringChange Dataclass: {'PASS' if test4 else 'FAIL'}")
        print(f"RefactoringOperation Dataclass: {'PASS' if test5 else 'FAIL'}")
        print(f"RefactoringConfig Dataclass: {'PASS' if test6 else 'FAIL'}")
        print(f"RefactoringResult Dataclass: {'PASS' if test7 else 'FAIL'}")
        print(f"RefactoringManager Initialization: {'PASS' if test8 else 'FAIL'}")
        print(f"Add Operation: {'PASS' if test9 else 'FAIL'}")
        print(f"Remove Operation: {'PASS' if test10 else 'FAIL'}")
        print(f"Get Operation: {'PASS' if test11 else 'FAIL'}")
        print(f"Get All Operations: {'PASS' if test12 else 'FAIL'}")
        print(f"Get Operations by Type: {'PASS' if test13 else 'FAIL'}")
        print(f"Create Rename Operation: {'PASS' if test14 else 'FAIL'}")
        print(f"Create Extract Function Operation: {'PASS' if test15 else 'FAIL'}")
        print(f"Create Extract Variable Operation: {'PASS' if test16 else 'FAIL'}")
        print(f"Create Inline Function Operation: {'PASS' if test17 else 'FAIL'}")
        print(f"Create Inline Variable Operation: {'PASS' if test18 else 'FAIL'}")
        print(f"Apply Operation: {'PASS' if test19 else 'FAIL'}")
        print(f"Undo Operation: {'PASS' if test20 else 'FAIL'}")
        print(f"Clear Operations: {'PASS' if test21 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test22 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test23 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14, test15, test16, test17, test18, test19, test20, test21, test22, test23])
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
