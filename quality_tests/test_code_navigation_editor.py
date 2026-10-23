"""
Quality Test: Code Navigation (Editor)
Code navigation system testleri for editor module.
"""

import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from app.editor.code_navigation import (
    NavigationType,
    NavigationMode,
    NavigationLocation,
    NavigationTarget,
    NavigationHistory,
    NavigationConfig,
    NavigationResult,
    CodeNavigationManager
)


def test_navigation_type_enum():
    """
    Test: NavigationType enum.
    """
    print("=" * 70)
    print("TEST: NavigationType Enum")
    print("=" * 70)
    
    assert NavigationType.DEFINITION.value == "definition"
    assert NavigationType.REFERENCE.value == "reference"
    assert NavigationType.IMPLEMENTATION.value == "implementation"
    assert NavigationType.TYPE_DEFINITION.value == "type_definition"
    assert NavigationType.DECLARATION.value == "declaration"
    
    print(f"  All enum values verified")
    print(f"  Total types: {len(NavigationType)}")
    
    print("\n" + "=" * 70)
    print("PASS: NavigationType enum")
    print("=" * 70)


def test_navigation_mode_enum():
    """
    Test: NavigationMode enum.
    """
    print("=" * 70)
    print("TEST: NavigationMode Enum")
    print("=" * 70)
    
    assert NavigationMode.SINGLE_FILE.value == "single_file"
    assert NavigationMode.MULTI_FILE.value == "multi_file"
    assert NavigationMode.PROJECT_WIDE.value == "project_wide"
    
    print(f"  All enum values verified")
    print(f"  Total modes: {len(NavigationMode)}")
    
    print("\n" + "=" * 70)
    print("PASS: NavigationMode enum")
    print("=" * 70)


def test_navigation_location_dataclass():
    """
    Test: NavigationLocation dataclass.
    """
    print("=" * 70)
    print("TEST: NavigationLocation Dataclass")
    print("=" * 70)
    
    location = NavigationLocation(
        file_path="test.py",
        line=10,
        column=5,
        symbol_name="test_function"
    )
    
    assert location.file_path == "test.py", "File path eşleşmeli"
    assert location.line == 10, "Line eşleşmeli"
    assert location.column == 5, "Column eşleşmeli"
    assert location.symbol_name == "test_function", "Symbol name eşleşmeli"
    
    print(f"  File path: {location.file_path}")
    print(f"  Line: {location.line}")
    print(f"  Column: {location.column}")
    print(f"  Symbol: {location.symbol_name}")
    
    print("\n" + "=" * 70)
    print("PASS: NavigationLocation dataclass")
    print("=" * 70)


def test_navigation_target_dataclass():
    """
    Test: NavigationTarget dataclass.
    """
    print("=" * 70)
    print("TEST: NavigationTarget Dataclass")
    print("=" * 70)
    
    location = NavigationLocation(
        file_path="test.py",
        line=10,
        column=5
    )
    
    target = NavigationTarget(
        id="target_1",
        type=NavigationType.DEFINITION,
        location=location
    )
    
    assert target.id == "target_1", "ID eşleşmeli"
    assert target.type == NavigationType.DEFINITION, "Type eşleşmeli"
    assert target.location == location, "Location eşleşmeli"
    
    print(f"  ID: {target.id}")
    print(f"  Type: {target.type.value}")
    print(f"  Location: {target.location.file_path}")
    
    print("\n" + "=" * 70)
    print("PASS: NavigationTarget dataclass")
    print("=" * 70)


def test_navigation_history_dataclass():
    """
    Test: NavigationHistory dataclass.
    """
    print("=" * 70)
    print("TEST: NavigationHistory Dataclass")
    print("=" * 70)
    
    history = NavigationHistory()
    
    assert isinstance(history.locations, list), "Locations list olmalı"
    assert history.current_index == -1, "Current index -1 olmalı"
    assert history.max_history == 100, "Max history 100 olmalı"
    
    print(f"  Locations: {len(history.locations)}")
    print(f"  Current index: {history.current_index}")
    print(f"  Max history: {history.max_history}")
    
    print("\n" + "=" * 70)
    print("PASS: NavigationHistory dataclass")
    print("=" * 70)


def test_navigation_config_dataclass():
    """
    Test: NavigationConfig dataclass.
    """
    print("=" * 70)
    print("TEST: NavigationConfig Dataclass")
    print("=" * 70)
    
    config = NavigationConfig(
        enabled=True,
        mode=NavigationMode.PROJECT_WIDE
    )
    
    assert config.enabled == True, "Enabled eşleşmeli"
    assert config.mode == NavigationMode.PROJECT_WIDE, "Mode eşleşmeli"
    
    print(f"  Enabled: {config.enabled}")
    print(f"  Mode: {config.mode.value}")
    
    print("\n" + "=" * 70)
    print("PASS: NavigationConfig dataclass")
    print("=" * 70)


def test_navigation_result_dataclass():
    """
    Test: NavigationResult dataclass.
    """
    print("=" * 70)
    print("TEST: NavigationResult Dataclass")
    print("=" * 70)
    
    result = NavigationResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: NavigationResult dataclass")
    print("=" * 70)


def test_code_navigation_manager_initialization():
    """
    Test: CodeNavigationManager initialization.
    """
    print("=" * 70)
    print("TEST: CodeNavigationManager Initialization")
    print("=" * 70)
    
    config = NavigationConfig()
    manager = CodeNavigationManager(config)
    
    assert manager.config == config, "Config eşleşmeli"
    assert len(manager.targets) == 0, "Targets boş olmalı"
    assert manager.history is not None, "History olmalı"
    
    print(f"  Targets: {len(manager.targets)}")
    print(f"  History: {manager.history is not None}")
    
    print("\n" + "=" * 70)
    print("PASS: CodeNavigationManager initialization")
    print("=" * 70)


def test_add_target():
    """
    Test: Add target.
    """
    print("=" * 70)
    print("TEST: Add Target")
    print("=" * 70)
    
    manager = CodeNavigationManager()
    
    location = NavigationLocation(
        file_path="test.py",
        line=10,
        column=5
    )
    
    target = NavigationTarget(
        id="",
        type=NavigationType.DEFINITION,
        location=location
    )
    
    result = manager.add_target(target)
    
    assert result.success == True, "Ekleme başarılı olmalı"
    assert len(manager.targets) > 0, "Target eklenmeli"
    
    print(f"  Target added: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add target")
    print("=" * 70)


def test_remove_target():
    """
    Test: Remove target.
    """
    print("=" * 70)
    print("TEST: Remove Target")
    print("=" * 70)
    
    manager = CodeNavigationManager()
    
    location = NavigationLocation(
        file_path="test.py",
        line=10,
        column=5
    )
    
    target = NavigationTarget(
        id="",
        type=NavigationType.DEFINITION,
        location=location
    )
    
    result = manager.add_target(target)
    target_id = result.target.id
    
    result = manager.remove_target(target_id)
    
    assert result.success == True, "Kaldırma başarılı olmalı"
    assert target_id not in manager.targets, "Target silinmeli"
    
    print(f"  Target removed: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Remove target")
    print("=" * 70)


def test_get_target():
    """
    Test: Get target.
    """
    print("=" * 70)
    print("TEST: Get Target")
    print("=" * 70)
    
    manager = CodeNavigationManager()
    
    location = NavigationLocation(
        file_path="test.py",
        line=10,
        column=5
    )
    
    target = NavigationTarget(
        id="",
        type=NavigationType.DEFINITION,
        location=location
    )
    
    result = manager.add_target(target)
    target_id = result.target.id
    
    retrieved_target = manager.get_target(target_id)
    
    assert retrieved_target is not None, "Target bulunmalı"
    assert retrieved_target.id == target_id, "ID eşleşmeli"
    
    print(f"  Target: {retrieved_target.type.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Get target")
    print("=" * 70)


def test_get_all_targets():
    """
    Test: Get all targets.
    """
    print("=" * 70)
    print("TEST: Get All Targets")
    print("=" * 70)
    
    manager = CodeNavigationManager()
    
    location = NavigationLocation(
        file_path="test.py",
        line=10,
        column=5
    )
    
    target = NavigationTarget(
        id="",
        type=NavigationType.DEFINITION,
        location=location
    )
    
    manager.add_target(target)
    targets = manager.get_all_targets()
    
    assert len(targets) > 0, "Targets olmalı"
    
    print(f"  Total targets: {len(targets)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get all targets")
    print("=" * 70)


def test_get_targets_by_type():
    """
    Test: Get targets by type.
    """
    print("=" * 70)
    print("TEST: Get Targets by Type")
    print("=" * 70)
    
    manager = CodeNavigationManager()
    
    location = NavigationLocation(
        file_path="test.py",
        line=10,
        column=5
    )
    
    target = NavigationTarget(
        id="",
        type=NavigationType.DEFINITION,
        location=location
    )
    
    manager.add_target(target)
    targets = manager.get_targets_by_type(NavigationType.DEFINITION)
    
    assert len(targets) > 0, "Definition targets olmalı"
    
    print(f"  Definition targets: {len(targets)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get targets by type")
    print("=" * 70)


def test_navigate_to():
    """
    Test: Navigate to location.
    """
    print("=" * 70)
    print("TEST: Navigate To Location")
    print("=" * 70)
    
    manager = CodeNavigationManager()
    
    location = NavigationLocation(
        file_path="test.py",
        line=10,
        column=5
    )
    
    result = manager.navigate_to(location)
    
    assert result.success == True, "Navigation başarılı olmalı"
    
    print(f"  Navigation: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Navigate to location")
    print("=" * 70)


def test_go_to_definition():
    """
    Test: Go to definition.
    """
    print("=" * 70)
    print("TEST: Go to Definition")
    print("=" * 70)
    
    manager = CodeNavigationManager()
    
    location = NavigationLocation(
        file_path="test.py",
        line=10,
        column=5
    )
    
    result = manager.go_to_definition(location)
    
    assert result.success == True, "Go to definition başarılı olmalı"
    
    print(f"  Go to definition: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Go to definition")
    print("=" * 70)


def test_go_to_reference():
    """
    Test: Go to reference.
    """
    print("=" * 70)
    print("TEST: Go to Reference")
    print("=" * 70)
    
    manager = CodeNavigationManager()
    
    location = NavigationLocation(
        file_path="test.py",
        line=10,
        column=5
    )
    
    result = manager.go_to_reference(location)
    
    assert result.success == True, "Go to reference başarılı olmalı"
    
    print(f"  Go to reference: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Go to reference")
    print("=" * 70)


def test_go_to_implementation():
    """
    Test: Go to implementation.
    """
    print("=" * 70)
    print("TEST: Go to Implementation")
    print("=" * 70)
    
    manager = CodeNavigationManager()
    
    location = NavigationLocation(
        file_path="test.py",
        line=10,
        column=5
    )
    
    result = manager.go_to_implementation(location)
    
    assert result.success == True, "Go to implementation başarılı olmalı"
    
    print(f"  Go to implementation: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Go to implementation")
    print("=" * 70)


def test_go_to_type_definition():
    """
    Test: Go to type definition.
    """
    print("=" * 70)
    print("TEST: Go to Type Definition")
    print("=" * 70)
    
    manager = CodeNavigationManager()
    
    location = NavigationLocation(
        file_path="test.py",
        line=10,
        column=5
    )
    
    result = manager.go_to_type_definition(location)
    
    assert result.success == True, "Go to type definition başarılı olmalı"
    
    print(f"  Go to type definition: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Go to type definition")
    print("=" * 70)


def test_go_back():
    """
    Test: Go back in history.
    """
    print("=" * 70)
    print("TEST: Go Back")
    print("=" * 70)
    
    manager = CodeNavigationManager()
    
    location1 = NavigationLocation(
        file_path="test.py",
        line=10,
        column=5
    )
    
    location2 = NavigationLocation(
        file_path="test.py",
        line=20,
        column=5
    )
    
    manager.navigate_to(location1)
    manager.navigate_to(location2)
    result = manager.go_back()
    
    assert result.success == True, "Go back başarılı olmalı"
    
    print(f"  Go back: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Go back")
    print("=" * 70)


def test_go_forward():
    """
    Test: Go forward in history.
    """
    print("=" * 70)
    print("TEST: Go Forward")
    print("=" * 70)
    
    manager = CodeNavigationManager()
    
    location1 = NavigationLocation(
        file_path="test.py",
        line=10,
        column=5
    )
    
    location2 = NavigationLocation(
        file_path="test.py",
        line=20,
        column=5
    )
    
    location3 = NavigationLocation(
        file_path="test.py",
        line=30,
        column=5
    )
    
    manager.navigate_to(location1)
    manager.navigate_to(location2)
    manager.navigate_to(location3)
    manager.go_back()
    manager.go_back()
    result = manager.go_forward()
    
    assert result.success == True, "Go forward başarılı olmalı"
    
    print(f"  Go forward: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Go forward")
    print("=" * 70)


def test_get_history():
    """
    Test: Get history.
    """
    print("=" * 70)
    print("TEST: Get History")
    print("=" * 70)
    
    manager = CodeNavigationManager()
    
    history = manager.get_history()
    
    assert history is not None, "History bulunmalı"
    
    print(f"  History: {history is not None}")
    
    print("\n" + "=" * 70)
    print("PASS: Get history")
    print("=" * 70)


def test_clear_history():
    """
    Test: Clear history.
    """
    print("=" * 70)
    print("TEST: Clear History")
    print("=" * 70)
    
    manager = CodeNavigationManager()
    
    location = NavigationLocation(
        file_path="test.py",
        line=10,
        column=5
    )
    
    manager.navigate_to(location)
    result = manager.clear_history()
    
    assert result.success == True, "Clear başarılı olmalı"
    assert len(manager.history.locations) == 0, "History temizlenmeli"
    
    print(f"  Cleared: {result.message}")
    
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
    
    manager = CodeNavigationManager()
    
    new_config = NavigationConfig(max_history=200)
    result = manager.update_config(new_config)
    
    assert result.success == True, "Update başarılı olmalı"
    assert manager.config.max_history == 200, "Config güncellenmeli"
    
    print(f"  Max history: {manager.config.max_history}")
    
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
    
    config = NavigationConfig(max_history=200)
    manager = CodeNavigationManager(config)
    
    retrieved_config = manager.get_config()
    
    assert retrieved_config.max_history == 200, "Config eşleşmeli"
    
    print(f"  Max history: {retrieved_config.max_history}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_navigation_type_enum()
        test2 = test_navigation_mode_enum()
        test3 = test_navigation_location_dataclass()
        test4 = test_navigation_target_dataclass()
        test5 = test_navigation_history_dataclass()
        test6 = test_navigation_config_dataclass()
        test7 = test_navigation_result_dataclass()
        test8 = test_code_navigation_manager_initialization()
        test9 = test_add_target()
        test10 = test_remove_target()
        test11 = test_get_target()
        test12 = test_get_all_targets()
        test13 = test_get_targets_by_type()
        test14 = test_navigate_to()
        test15 = test_go_to_definition()
        test16 = test_go_to_reference()
        test17 = test_go_to_implementation()
        test18 = test_go_to_type_definition()
        test19 = test_go_back()
        test20 = test_go_forward()
        test21 = test_get_history()
        test22 = test_clear_history()
        test23 = test_update_config()
        test24 = test_get_config()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"NavigationType Enum: {'PASS' if test1 else 'FAIL'}")
        print(f"NavigationMode Enum: {'PASS' if test2 else 'FAIL'}")
        print(f"NavigationLocation Dataclass: {'PASS' if test3 else 'FAIL'}")
        print(f"NavigationTarget Dataclass: {'PASS' if test4 else 'FAIL'}")
        print(f"NavigationHistory Dataclass: {'PASS' if test5 else 'FAIL'}")
        print(f"NavigationConfig Dataclass: {'PASS' if test6 else 'FAIL'}")
        print(f"NavigationResult Dataclass: {'PASS' if test7 else 'FAIL'}")
        print(f"CodeNavigationManager Initialization: {'PASS' if test8 else 'FAIL'}")
        print(f"Add Target: {'PASS' if test9 else 'FAIL'}")
        print(f"Remove Target: {'PASS' if test10 else 'FAIL'}")
        print(f"Get Target: {'PASS' if test11 else 'FAIL'}")
        print(f"Get All Targets: {'PASS' if test12 else 'FAIL'}")
        print(f"Get Targets by Type: {'PASS' if test13 else 'FAIL'}")
        print(f"Navigate To: {'PASS' if test14 else 'FAIL'}")
        print(f"Go to Definition: {'PASS' if test15 else 'FAIL'}")
        print(f"Go to Reference: {'PASS' if test16 else 'FAIL'}")
        print(f"Go to Implementation: {'PASS' if test17 else 'FAIL'}")
        print(f"Go to Type Definition: {'PASS' if test18 else 'FAIL'}")
        print(f"Go Back: {'PASS' if test19 else 'FAIL'}")
        print(f"Go Forward: {'PASS' if test20 else 'FAIL'}")
        print(f"Get History: {'PASS' if test21 else 'FAIL'}")
        print(f"Clear History: {'PASS' if test22 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test23 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test24 else 'FAIL'}")
        
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
