"""
Quality Test: Decorations
Decorations system testleri.
"""

import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from app.editor.decorations import (
    DecorationType,
    DecorationPosition,
    DecorationRange,
    Decoration,
    DecorationsConfig,
    DecorationsResult,
    DecorationsManager
)


def test_decoration_type_enum():
    """
    Test: DecorationType enum.
    """
    print("=" * 70)
    print("TEST: DecorationType Enum")
    print("=" * 70)
    
    assert DecorationType.ERROR.value == "error"
    assert DecorationType.WARNING.value == "warning"
    assert DecorationType.INFO.value == "info"
    assert DecorationType.HINT.value == "hint"
    assert DecorationType.SUCCESS.value == "success"
    assert DecorationType.CUSTOM.value == "custom"
    
    print(f"  All enum values verified")
    print(f"  Total types: {len(DecorationType)}")
    
    print("\n" + "=" * 70)
    print("PASS: DecorationType enum")
    print("=" * 70)


def test_decoration_position_enum():
    """
    Test: DecorationPosition enum.
    """
    print("=" * 70)
    print("TEST: DecorationPosition Enum")
    print("=" * 70)
    
    assert DecorationPosition.INLINE.value == "inline"
    assert DecorationPosition.GUTTER.value == "gutter"
    assert DecorationPosition.OVERVIEW.value == "overview"
    assert DecorationPosition.MINIMAP.value == "minimap"
    
    print(f"  All enum values verified")
    print(f"  Total positions: {len(DecorationPosition)}")
    
    print("\n" + "=" * 70)
    print("PASS: DecorationPosition enum")
    print("=" * 70)


def test_decoration_range_dataclass():
    """
    Test: DecorationRange dataclass.
    """
    print("=" * 70)
    print("TEST: DecorationRange Dataclass")
    print("=" * 70)
    
    range = DecorationRange(
        start_line=0,
        start_column=0,
        end_line=0,
        end_column=10
    )
    
    assert range.start_line == 0, "Start line eşleşmeli"
    assert range.start_column == 0, "Start column eşleşmeli"
    assert range.end_line == 0, "End line eşleşmeli"
    assert range.end_column == 10, "End column eşleşmeli"
    
    print(f"  Start: ({range.start_line}, {range.start_column})")
    print(f"  End: ({range.end_line}, {range.end_column})")
    
    print("\n" + "=" * 70)
    print("PASS: DecorationRange dataclass")
    print("=" * 70)


def test_decoration_dataclass():
    """
    Test: Decoration dataclass.
    """
    print("=" * 70)
    print("TEST: Decoration Dataclass")
    print("=" * 70)
    
    range = DecorationRange(0, 0, 0, 10)
    decoration = Decoration(
        id="decoration_1",
        type=DecorationType.ERROR,
        range=range,
        message="Test error"
    )
    
    assert decoration.id == "decoration_1", "ID eşleşmeli"
    assert decoration.type == DecorationType.ERROR, "Type eşleşmeli"
    assert decoration.message == "Test error", "Message eşleşmeli"
    
    print(f"  ID: {decoration.id}")
    print(f"  Type: {decoration.type.value}")
    print(f"  Message: {decoration.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Decoration dataclass")
    print("=" * 70)


def test_decorations_config_dataclass():
    """
    Test: DecorationsConfig dataclass.
    """
    print("=" * 70)
    print("TEST: DecorationsConfig Dataclass")
    print("=" * 70)
    
    config = DecorationsConfig(
        enabled=True,
        show_errors=True
    )
    
    assert config.enabled == True, "Enabled eşleşmeli"
    assert config.show_errors == True, "Show errors eşleşmeli"
    
    print(f"  Enabled: {config.enabled}")
    print(f"  Show errors: {config.show_errors}")
    
    print("\n" + "=" * 70)
    print("PASS: DecorationsConfig dataclass")
    print("=" * 70)


def test_decorations_result_dataclass():
    """
    Test: DecorationsResult dataclass.
    """
    print("=" * 70)
    print("TEST: DecorationsResult Dataclass")
    print("=" * 70)
    
    result = DecorationsResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.decorations, list), "Decorations list olmalı"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Decorations: {len(result.decorations)}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: DecorationsResult dataclass")
    print("=" * 70)


def test_decorations_manager_initialization():
    """
    Test: DecorationsManager initialization.
    """
    print("=" * 70)
    print("TEST: DecorationsManager Initialization")
    print("=" * 70)
    
    config = DecorationsConfig()
    manager = DecorationsManager(config)
    
    assert manager.config == config, "Config eşleşmeli"
    assert len(manager.decorations) == 0, "Decorations boş olmalı"
    
    print(f"  Decorations: {len(manager.decorations)}")
    
    print("\n" + "=" * 70)
    print("PASS: DecorationsManager initialization")
    print("=" * 70)


def test_add_decoration():
    """
    Test: Add decoration.
    """
    print("=" * 70)
    print("TEST: Add Decoration")
    print("=" * 70)
    
    manager = DecorationsManager()
    
    range = DecorationRange(0, 0, 0, 10)
    decoration = Decoration(
        id="",
        type=DecorationType.ERROR,
        range=range,
        message="Test error"
    )
    
    result = manager.add_decoration(decoration)
    
    assert result.success == True, "Ekleme başarılı olmalı"
    assert len(manager.decorations) > 0, "Decoration eklenmeli"
    
    print(f"  Decoration added: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add decoration")
    print("=" * 70)


def test_remove_decoration():
    """
    Test: Remove decoration.
    """
    print("=" * 70)
    print("TEST: Remove Decoration")
    print("=" * 70)
    
    manager = DecorationsManager()
    
    range = DecorationRange(0, 0, 0, 10)
    decoration = Decoration(
        id="",
        type=DecorationType.ERROR,
        range=range,
        message="Test error"
    )
    
    result = manager.add_decoration(decoration)
    decoration_id = result.decorations[0].id
    
    result = manager.remove_decoration(decoration_id)
    
    assert result.success == True, "Kaldırma başarılı olmalı"
    assert decoration_id not in manager.decorations, "Decoration silinmeli"
    
    print(f"  Decoration removed: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Remove decoration")
    print("=" * 70)


def test_get_decoration():
    """
    Test: Get decoration.
    """
    print("=" * 70)
    print("TEST: Get Decoration")
    print("=" * 70)
    
    manager = DecorationsManager()
    
    range = DecorationRange(0, 0, 0, 10)
    decoration = Decoration(
        id="",
        type=DecorationType.ERROR,
        range=range,
        message="Test error"
    )
    
    result = manager.add_decoration(decoration)
    decoration_id = result.decorations[0].id
    
    retrieved_decoration = manager.get_decoration(decoration_id)
    
    assert retrieved_decoration is not None, "Decoration bulunmalı"
    assert retrieved_decoration.id == decoration_id, "ID eşleşmeli"
    
    print(f"  Decoration: {retrieved_decoration.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Get decoration")
    print("=" * 70)


def test_get_all_decorations():
    """
    Test: Get all decorations.
    """
    print("=" * 70)
    print("TEST: Get All Decorations")
    print("=" * 70)
    
    manager = DecorationsManager()
    
    range = DecorationRange(0, 0, 0, 10)
    decoration = Decoration(
        id="",
        type=DecorationType.ERROR,
        range=range,
        message="Test error"
    )
    
    manager.add_decoration(decoration)
    decorations = manager.get_all_decorations()
    
    assert len(decorations) > 0, "Decorations olmalı"
    
    print(f"  Total decorations: {len(decorations)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get all decorations")
    print("=" * 70)


def test_get_decorations_by_type():
    """
    Test: Get decorations by type.
    """
    print("=" * 70)
    print("TEST: Get Decorations by Type")
    print("=" * 70)
    
    manager = DecorationsManager()
    
    range = DecorationRange(0, 0, 0, 10)
    decoration = Decoration(
        id="",
        type=DecorationType.ERROR,
        range=range,
        message="Test error"
    )
    
    manager.add_decoration(decoration)
    decorations = manager.get_decorations_by_type(DecorationType.ERROR)
    
    assert len(decorations) > 0, "Error decorations olmalı"
    
    print(f"  Error decorations: {len(decorations)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get decorations by type")
    print("=" * 70)


def test_get_decorations_by_position():
    """
    Test: Get decorations by position.
    """
    print("=" * 70)
    print("TEST: Get Decorations by Position")
    print("=" * 70)
    
    manager = DecorationsManager()
    
    range = DecorationRange(0, 0, 0, 10)
    decoration = Decoration(
        id="",
        type=DecorationType.ERROR,
        range=range,
        message="Test error",
        position=DecorationPosition.INLINE
    )
    
    manager.add_decoration(decoration)
    decorations = manager.get_decorations_by_position(DecorationPosition.INLINE)
    
    assert len(decorations) > 0, "Inline decorations olmalı"
    
    print(f"  Inline decorations: {len(decorations)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get decorations by position")
    print("=" * 70)


def test_add_error():
    """
    Test: Add error.
    """
    print("=" * 70)
    print("TEST: Add Error")
    print("=" * 70)
    
    manager = DecorationsManager()
    
    range = DecorationRange(0, 0, 0, 10)
    result = manager.add_error(range, "Test error")
    
    assert result.success == True, "Error başarılı olmalı"
    
    print(f"  Error added: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add error")
    print("=" * 70)


def test_add_warning():
    """
    Test: Add warning.
    """
    print("=" * 70)
    print("TEST: Add Warning")
    print("=" * 70)
    
    manager = DecorationsManager()
    
    range = DecorationRange(0, 0, 0, 10)
    result = manager.add_warning(range, "Test warning")
    
    assert result.success == True, "Warning başarılı olmalı"
    
    print(f"  Warning added: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add warning")
    print("=" * 70)


def test_add_info():
    """
    Test: Add info.
    """
    print("=" * 70)
    print("TEST: Add Info")
    print("=" * 70)
    
    manager = DecorationsManager()
    
    range = DecorationRange(0, 0, 0, 10)
    result = manager.add_info(range, "Test info")
    
    assert result.success == True, "Info başarılı olmalı"
    
    print(f"  Info added: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add info")
    print("=" * 70)


def test_add_hint():
    """
    Test: Add hint.
    """
    print("=" * 70)
    print("TEST: Add Hint")
    print("=" * 70)
    
    manager = DecorationsManager()
    
    range = DecorationRange(0, 0, 0, 10)
    result = manager.add_hint(range, "Test hint")
    
    assert result.success == True, "Hint başarılı olmalı"
    
    print(f"  Hint added: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add hint")
    print("=" * 70)


def test_clear_decorations():
    """
    Test: Clear decorations.
    """
    print("=" * 70)
    print("TEST: Clear Decorations")
    print("=" * 70)
    
    manager = DecorationsManager()
    
    range = DecorationRange(0, 0, 0, 10)
    decoration = Decoration(
        id="",
        type=DecorationType.ERROR,
        range=range,
        message="Test error"
    )
    
    manager.add_decoration(decoration)
    result = manager.clear_decorations()
    
    assert result.success == True, "Clear başarılı olmalı"
    assert len(manager.decorations) == 0, "Decorations temizlenmeli"
    
    print(f"  Cleared: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear decorations")
    print("=" * 70)


def test_clear_decorations_by_type():
    """
    Test: Clear decorations by type.
    """
    print("=" * 70)
    print("TEST: Clear Decorations by Type")
    print("=" * 70)
    
    manager = DecorationsManager()
    
    range = DecorationRange(0, 0, 0, 10)
    decoration = Decoration(
        id="",
        type=DecorationType.ERROR,
        range=range,
        message="Test error"
    )
    
    manager.add_decoration(decoration)
    result = manager.clear_decorations_by_type(DecorationType.ERROR)
    
    assert result.success == True, "Clear başarılı olmalı"
    
    print(f"  Cleared by type: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear decorations by type")
    print("=" * 70)


def test_set_decoration_enabled():
    """
    Test: Set decoration enabled.
    """
    print("=" * 70)
    print("TEST: Set Decoration Enabled")
    print("=" * 70)
    
    manager = DecorationsManager()
    
    range = DecorationRange(0, 0, 0, 10)
    decoration = Decoration(
        id="",
        type=DecorationType.ERROR,
        range=range,
        message="Test error"
    )
    
    result = manager.add_decoration(decoration)
    decoration_id = result.decorations[0].id
    
    result = manager.set_decoration_enabled(decoration_id, False)
    
    assert result.success == True, "Set başarılı olmalı"
    
    print(f"  Decoration enabled state: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set decoration enabled")
    print("=" * 70)


def test_set_decoration_visible():
    """
    Test: Set decoration visible.
    """
    print("=" * 70)
    print("TEST: Set Decoration Visible")
    print("=" * 70)
    
    manager = DecorationsManager()
    
    range = DecorationRange(0, 0, 0, 10)
    decoration = Decoration(
        id="",
        type=DecorationType.ERROR,
        range=range,
        message="Test error"
    )
    
    result = manager.add_decoration(decoration)
    decoration_id = result.decorations[0].id
    
    result = manager.set_decoration_visible(decoration_id, False)
    
    assert result.success == True, "Set başarılı olmalı"
    
    print(f"  Decoration visible state: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set decoration visible")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    manager = DecorationsManager()
    
    new_config = DecorationsConfig(max_decorations=200)
    result = manager.update_config(new_config)
    
    assert result.success == True, "Update başarılı olmalı"
    assert manager.config.max_decorations == 200, "Config güncellenmeli"
    
    print(f"  Max decorations: {manager.config.max_decorations}")
    
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
    
    config = DecorationsConfig(max_decorations=200)
    manager = DecorationsManager(config)
    
    retrieved_config = manager.get_config()
    
    assert retrieved_config.max_decorations == 200, "Config eşleşmeli"
    
    print(f"  Max decorations: {retrieved_config.max_decorations}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_decoration_type_enum()
        test2 = test_decoration_position_enum()
        test3 = test_decoration_range_dataclass()
        test4 = test_decoration_dataclass()
        test5 = test_decorations_config_dataclass()
        test6 = test_decorations_result_dataclass()
        test7 = test_decorations_manager_initialization()
        test8 = test_add_decoration()
        test9 = test_remove_decoration()
        test10 = test_get_decoration()
        test11 = test_get_all_decorations()
        test12 = test_get_decorations_by_type()
        test13 = test_get_decorations_by_position()
        test14 = test_add_error()
        test15 = test_add_warning()
        test16 = test_add_info()
        test17 = test_add_hint()
        test18 = test_clear_decorations()
        test19 = test_clear_decorations_by_type()
        test20 = test_set_decoration_enabled()
        test21 = test_set_decoration_visible()
        test22 = test_update_config()
        test23 = test_get_config()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"DecorationType Enum: {'PASS' if test1 else 'FAIL'}")
        print(f"DecorationPosition Enum: {'PASS' if test2 else 'FAIL'}")
        print(f"DecorationRange Dataclass: {'PASS' if test3 else 'FAIL'}")
        print(f"Decoration Dataclass: {'PASS' if test4 else 'FAIL'}")
        print(f"DecorationsConfig Dataclass: {'PASS' if test5 else 'FAIL'}")
        print(f"DecorationsResult Dataclass: {'PASS' if test6 else 'FAIL'}")
        print(f"DecorationsManager Initialization: {'PASS' if test7 else 'FAIL'}")
        print(f"Add Decoration: {'PASS' if test8 else 'FAIL'}")
        print(f"Remove Decoration: {'PASS' if test9 else 'FAIL'}")
        print(f"Get Decoration: {'PASS' if test10 else 'FAIL'}")
        print(f"Get All Decorations: {'PASS' if test11 else 'FAIL'}")
        print(f"Get Decorations by Type: {'PASS' if test12 else 'FAIL'}")
        print(f"Get Decorations by Position: {'PASS' if test13 else 'FAIL'}")
        print(f"Add Error: {'PASS' if test14 else 'FAIL'}")
        print(f"Add Warning: {'PASS' if test15 else 'FAIL'}")
        print(f"Add Info: {'PASS' if test16 else 'FAIL'}")
        print(f"Add Hint: {'PASS' if test17 else 'FAIL'}")
        print(f"Clear Decorations: {'PASS' if test18 else 'FAIL'}")
        print(f"Clear Decorations by Type: {'PASS' if test19 else 'FAIL'}")
        print(f"Set Decoration Enabled: {'PASS' if test20 else 'FAIL'}")
        print(f"Set Decoration Visible: {'PASS' if test21 else 'FAIL'}")
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
