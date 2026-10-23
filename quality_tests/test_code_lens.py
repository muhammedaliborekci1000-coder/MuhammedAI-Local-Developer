"""
Quality Test: Code Lens
Code lens system testleri.
"""

import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from app.editor.code_lens import (
    LensType,
    LensPosition,
    LensAction,
    CodeLens,
    CodeLensConfig,
    CodeLensResult,
    CodeLensManager
)


def test_lens_type_enum():
    """
    Test: LensType enum.
    """
    print("=" * 70)
    print("TEST: LensType Enum")
    print("=" * 70)
    
    assert LensType.REFERENCE.value == "reference"
    assert LensType.IMPLEMENTATION.value == "implementation"
    assert LensType.DEFINITION.value == "definition"
    assert LensType.TEST.value == "test"
    assert LensType.DOCUMENTATION.value == "documentation"
    assert LensType.ERROR.value == "error"
    assert LensType.WARNING.value == "warning"
    assert LensType.INFO.value == "info"
    assert LensType.CUSTOM.value == "custom"
    
    print(f"  All enum values verified")
    print(f"  Total types: {len(LensType)}")
    
    print("\n" + "=" * 70)
    print("PASS: LensType enum")
    print("=" * 70)


def test_lens_position_dataclass():
    """
    Test: LensPosition dataclass.
    """
    print("=" * 70)
    print("TEST: LensPosition Dataclass")
    print("=" * 70)
    
    position = LensPosition(
        line=0,
        column=0
    )
    
    assert position.line == 0, "Line eşleşmeli"
    assert position.column == 0, "Column eşleşmeli"
    
    print(f"  Line: {position.line}")
    print(f"  Column: {position.column}")
    
    print("\n" + "=" * 70)
    print("PASS: LensPosition dataclass")
    print("=" * 70)


def test_lens_action_dataclass():
    """
    Test: LensAction dataclass.
    """
    print("=" * 70)
    print("TEST: LensAction Dataclass")
    print("=" * 70)
    
    action = LensAction(
        id="action_1",
        title="Test Action",
        command="test.command"
    )
    
    assert action.id == "action_1", "ID eşleşmeli"
    assert action.title == "Test Action", "Title eşleşmeli"
    assert action.command == "test.command", "Command eşleşmeli"
    
    print(f"  ID: {action.id}")
    print(f"  Title: {action.title}")
    print(f"  Command: {action.command}")
    
    print("\n" + "=" * 70)
    print("PASS: LensAction dataclass")
    print("=" * 70)


def test_code_lens_dataclass():
    """
    Test: CodeLens dataclass.
    """
    print("=" * 70)
    print("TEST: CodeLens Dataclass")
    print("=" * 70)
    
    position = LensPosition(0, 0)
    lens = CodeLens(
        id="lens_1",
        title="Test Lens",
        type=LensType.INFO,
        position=position
    )
    
    assert lens.id == "lens_1", "ID eşleşmeli"
    assert lens.title == "Test Lens", "Title eşleşmeli"
    assert lens.type == LensType.INFO, "Type eşleşmeli"
    
    print(f"  ID: {lens.id}")
    print(f"  Title: {lens.title}")
    print(f"  Type: {lens.type.value}")
    
    print("\n" + "=" * 70)
    print("PASS: CodeLens dataclass")
    print("=" * 70)


def test_code_lens_config_dataclass():
    """
    Test: CodeLensConfig dataclass.
    """
    print("=" * 70)
    print("TEST: CodeLensConfig Dataclass")
    print("=" * 70)
    
    config = CodeLensConfig(
        enabled=True,
        show_reference_lenses=True
    )
    
    assert config.enabled == True, "Enabled eşleşmeli"
    assert config.show_reference_lenses == True, "Show reference lenses eşleşmeli"
    
    print(f"  Enabled: {config.enabled}")
    print(f"  Show reference lenses: {config.show_reference_lenses}")
    
    print("\n" + "=" * 70)
    print("PASS: CodeLensConfig dataclass")
    print("=" * 70)


def test_code_lens_result_dataclass():
    """
    Test: CodeLensResult dataclass.
    """
    print("=" * 70)
    print("TEST: CodeLensResult Dataclass")
    print("=" * 70)
    
    result = CodeLensResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.lenses, list), "Lenses list olmalı"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Lenses: {len(result.lenses)}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: CodeLensResult dataclass")
    print("=" * 70)


def test_code_lens_manager_initialization():
    """
    Test: CodeLensManager initialization.
    """
    print("=" * 70)
    print("TEST: CodeLensManager Initialization")
    print("=" * 70)
    
    config = CodeLensConfig()
    manager = CodeLensManager(config)
    
    assert manager.config == config, "Config eşleşmeli"
    assert len(manager.lenses) == 0, "Lenses boş olmalı"
    
    print(f"  Lenses: {len(manager.lenses)}")
    
    print("\n" + "=" * 70)
    print("PASS: CodeLensManager initialization")
    print("=" * 70)


def test_add_lens():
    """
    Test: Add lens.
    """
    print("=" * 70)
    print("TEST: Add Lens")
    print("=" * 70)
    
    manager = CodeLensManager()
    
    position = LensPosition(0, 0)
    lens = CodeLens(
        id="",
        title="Test Lens",
        position=position
    )
    
    result = manager.add_lens(lens)
    
    assert result.success == True, "Ekleme başarılı olmalı"
    assert len(manager.lenses) > 0, "Lens eklenmeli"
    
    print(f"  Lens added: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add lens")
    print("=" * 70)


def test_remove_lens():
    """
    Test: Remove lens.
    """
    print("=" * 70)
    print("TEST: Remove Lens")
    print("=" * 70)
    
    manager = CodeLensManager()
    
    position = LensPosition(0, 0)
    lens = CodeLens(
        id="",
        title="Test Lens",
        position=position
    )
    
    result = manager.add_lens(lens)
    lens_id = result.lenses[0].id
    
    result = manager.remove_lens(lens_id)
    
    assert result.success == True, "Kaldırma başarılı olmalı"
    assert lens_id not in manager.lenses, "Lens silinmeli"
    
    print(f"  Lens removed: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Remove lens")
    print("=" * 70)


def test_get_lens():
    """
    Test: Get lens.
    """
    print("=" * 70)
    print("TEST: Get Lens")
    print("=" * 70)
    
    manager = CodeLensManager()
    
    position = LensPosition(0, 0)
    lens = CodeLens(
        id="",
        title="Test Lens",
        position=position
    )
    
    result = manager.add_lens(lens)
    lens_id = result.lenses[0].id
    
    retrieved_lens = manager.get_lens(lens_id)
    
    assert retrieved_lens is not None, "Lens bulunmalı"
    assert retrieved_lens.id == lens_id, "ID eşleşmeli"
    
    print(f"  Lens: {retrieved_lens.title}")
    
    print("\n" + "=" * 70)
    print("PASS: Get lens")
    print("=" * 70)


def test_get_all_lenses():
    """
    Test: Get all lenses.
    """
    print("=" * 70)
    print("TEST: Get All Lenses")
    print("=" * 70)
    
    manager = CodeLensManager()
    
    position = LensPosition(0, 0)
    lens = CodeLens(
        id="",
        title="Test Lens",
        position=position
    )
    
    manager.add_lens(lens)
    lenses = manager.get_all_lenses()
    
    assert len(lenses) > 0, "Lenses olmalı"
    
    print(f"  Total lenses: {len(lenses)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get all lenses")
    print("=" * 70)


def test_get_lenses_by_type():
    """
    Test: Get lenses by type.
    """
    print("=" * 70)
    print("TEST: Get Lenses by Type")
    print("=" * 70)
    
    manager = CodeLensManager()
    
    position = LensPosition(0, 0)
    lens = CodeLens(
        id="",
        title="Test Lens",
        type=LensType.REFERENCE,
        position=position
    )
    
    manager.add_lens(lens)
    lenses = manager.get_lenses_by_type(LensType.REFERENCE)
    
    assert len(lenses) > 0, "Reference lenses olmalı"
    
    print(f"  Reference lenses: {len(lenses)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get lenses by type")
    print("=" * 70)


def test_get_lenses_at_line():
    """
    Test: Get lenses at line.
    """
    print("=" * 70)
    print("TEST: Get Lenses at Line")
    print("=" * 70)
    
    manager = CodeLensManager()
    
    position = LensPosition(0, 0)
    lens = CodeLens(
        id="",
        title="Test Lens",
        position=position
    )
    
    manager.add_lens(lens)
    lenses = manager.get_lenses_at_line(0)
    
    assert len(lenses) > 0, "Line 0 lenses olmalı"
    
    print(f"  Line 0 lenses: {len(lenses)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get lenses at line")
    print("=" * 70)


def test_add_reference_lens():
    """
    Test: Add reference lens.
    """
    print("=" * 70)
    print("TEST: Add Reference Lens")
    print("=" * 70)
    
    manager = CodeLensManager()
    
    position = LensPosition(0, 0)
    result = manager.add_reference_lens("my_function", position, 5)
    
    assert result.success == True, "Reference lens başarılı olmalı"
    
    print(f"  Reference lens: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add reference lens")
    print("=" * 70)


def test_add_implementation_lens():
    """
    Test: Add implementation lens.
    """
    print("=" * 70)
    print("TEST: Add Implementation Lens")
    print("=" * 70)
    
    manager = CodeLensManager()
    
    position = LensPosition(0, 0)
    result = manager.add_implementation_lens("MyInterface", position, 3)
    
    assert result.success == True, "Implementation lens başarılı olmalı"
    
    print(f"  Implementation lens: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add implementation lens")
    print("=" * 70)


def test_add_definition_lens():
    """
    Test: Add definition lens.
    """
    print("=" * 70)
    print("TEST: Add Definition Lens")
    print("=" * 70)
    
    manager = CodeLensManager()
    
    position = LensPosition(0, 0)
    result = manager.add_definition_lens("my_function", position)
    
    assert result.success == True, "Definition lens başarılı olmalı"
    
    print(f"  Definition lens: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add definition lens")
    print("=" * 70)


def test_add_test_lens():
    """
    Test: Add test lens.
    """
    print("=" * 70)
    print("TEST: Add Test Lens")
    print("=" * 70)
    
    manager = CodeLensManager()
    
    position = LensPosition(0, 0)
    result = manager.add_test_lens("test_my_function", position, "passed")
    
    assert result.success == True, "Test lens başarılı olmalı"
    
    print(f"  Test lens: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add test lens")
    print("=" * 70)


def test_execute_lens_action():
    """
    Test: Execute lens action.
    """
    print("=" * 70)
    print("TEST: Execute Lens Action")
    print("=" * 70)
    
    manager = CodeLensManager()
    
    position = LensPosition(0, 0)
    
    def test_callback():
        pass
    
    action = LensAction(
        id="action_1",
        title="Test Action",
        callback=test_callback
    )
    
    lens = CodeLens(
        id="",
        title="Test Lens",
        position=position,
        actions=[action]
    )
    
    result = manager.add_lens(lens)
    lens_id = result.lenses[0].id
    
    result = manager.execute_lens_action(lens_id, "action_1")
    
    assert result.success == True, "Action execution başarılı olmalı"
    
    print(f"  Action executed: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Execute lens action")
    print("=" * 70)


def test_clear_lenses():
    """
    Test: Clear lenses.
    """
    print("=" * 70)
    print("TEST: Clear Lenses")
    print("=" * 70)
    
    manager = CodeLensManager()
    
    position = LensPosition(0, 0)
    lens = CodeLens(
        id="",
        title="Test Lens",
        position=position
    )
    
    manager.add_lens(lens)
    result = manager.clear_lenses()
    
    assert result.success == True, "Clear başarılı olmalı"
    assert len(manager.lenses) == 0, "Lenses temizlenmeli"
    
    print(f"  Cleared: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear lenses")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    manager = CodeLensManager()
    
    new_config = CodeLensConfig(max_lenses_per_line=10)
    result = manager.update_config(new_config)
    
    assert result.success == True, "Update başarılı olmalı"
    assert manager.config.max_lenses_per_line == 10, "Config güncellenmeli"
    
    print(f"  Max lenses per line: {manager.config.max_lenses_per_line}")
    
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
    
    config = CodeLensConfig(max_lenses_per_line=10)
    manager = CodeLensManager(config)
    
    retrieved_config = manager.get_config()
    
    assert retrieved_config.max_lenses_per_line == 10, "Config eşleşmeli"
    
    print(f"  Max lenses per line: {retrieved_config.max_lenses_per_line}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_lens_type_enum()
        test2 = test_lens_position_dataclass()
        test3 = test_lens_action_dataclass()
        test4 = test_code_lens_dataclass()
        test5 = test_code_lens_config_dataclass()
        test6 = test_code_lens_result_dataclass()
        test7 = test_code_lens_manager_initialization()
        test8 = test_add_lens()
        test9 = test_remove_lens()
        test10 = test_get_lens()
        test11 = test_get_all_lenses()
        test12 = test_get_lenses_by_type()
        test13 = test_get_lenses_at_line()
        test14 = test_add_reference_lens()
        test15 = test_add_implementation_lens()
        test16 = test_add_definition_lens()
        test17 = test_add_test_lens()
        test18 = test_execute_lens_action()
        test19 = test_clear_lenses()
        test20 = test_update_config()
        test21 = test_get_config()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"LensType Enum: {'PASS' if test1 else 'FAIL'}")
        print(f"LensPosition Dataclass: {'PASS' if test2 else 'FAIL'}")
        print(f"LensAction Dataclass: {'PASS' if test3 else 'FAIL'}")
        print(f"CodeLens Dataclass: {'PASS' if test4 else 'FAIL'}")
        print(f"CodeLensConfig Dataclass: {'PASS' if test5 else 'FAIL'}")
        print(f"CodeLensResult Dataclass: {'PASS' if test6 else 'FAIL'}")
        print(f"CodeLensManager Initialization: {'PASS' if test7 else 'FAIL'}")
        print(f"Add Lens: {'PASS' if test8 else 'FAIL'}")
        print(f"Remove Lens: {'PASS' if test9 else 'FAIL'}")
        print(f"Get Lens: {'PASS' if test10 else 'FAIL'}")
        print(f"Get All Lenses: {'PASS' if test11 else 'FAIL'}")
        print(f"Get Lenses by Type: {'PASS' if test12 else 'FAIL'}")
        print(f"Get Lenses at Line: {'PASS' if test13 else 'FAIL'}")
        print(f"Add Reference Lens: {'PASS' if test14 else 'FAIL'}")
        print(f"Add Implementation Lens: {'PASS' if test15 else 'FAIL'}")
        print(f"Add Definition Lens: {'PASS' if test16 else 'FAIL'}")
        print(f"Add Test Lens: {'PASS' if test17 else 'FAIL'}")
        print(f"Execute Lens Action: {'PASS' if test18 else 'FAIL'}")
        print(f"Clear Lenses: {'PASS' if test19 else 'FAIL'}")
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
