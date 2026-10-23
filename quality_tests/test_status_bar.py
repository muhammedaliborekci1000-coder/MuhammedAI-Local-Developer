"""
Quality Test: Status Bar
Status bar system testleri.
"""

import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from app.editor.status_bar import (
    StatusItemPosition,
    StatusItemPriority,
    StatusItem,
    StatusBarConfig,
    StatusBarResult,
    StatusBarManager
)


def test_status_item_position_enum():
    """
    Test: StatusItemPosition enum.
    """
    print("=" * 70)
    print("TEST: StatusItemPosition Enum")
    print("=" * 70)
    
    assert StatusItemPosition.LEFT.value == "left"
    assert StatusItemPosition.CENTER.value == "center"
    assert StatusItemPosition.RIGHT.value == "right"
    
    print(f"  All enum values verified")
    print(f"  Total positions: {len(StatusItemPosition)}")
    
    print("\n" + "=" * 70)
    print("PASS: StatusItemPosition enum")
    print("=" * 70)


def test_status_item_priority_enum():
    """
    Test: StatusItemPriority enum.
    """
    print("=" * 70)
    print("TEST: StatusItemPriority Enum")
    print("=" * 70)
    
    assert StatusItemPriority.HIGH.value == "high"
    assert StatusItemPriority.MEDIUM.value == "medium"
    assert StatusItemPriority.LOW.value == "low"
    
    print(f"  All enum values verified")
    print(f"  Total priorities: {len(StatusItemPriority)}")
    
    print("\n" + "=" * 70)
    print("PASS: StatusItemPriority enum")
    print("=" * 70)


def test_status_item_dataclass():
    """
    Test: StatusItem dataclass.
    """
    print("=" * 70)
    print("TEST: StatusItem Dataclass")
    print("=" * 70)
    
    item = StatusItem(
        id="test_item",
        label="Test",
        position=StatusItemPosition.LEFT,
        priority=StatusItemPriority.HIGH
    )
    
    assert item.id == "test_item", "ID eşleşmeli"
    assert item.label == "Test", "Label eşleşmeli"
    assert item.position == StatusItemPosition.LEFT, "Position eşleşmeli"
    
    print(f"  ID: {item.id}")
    print(f"  Label: {item.label}")
    print(f"  Position: {item.position.value}")
    
    print("\n" + "=" * 70)
    print("PASS: StatusItem dataclass")
    print("=" * 70)


def test_status_bar_config_dataclass():
    """
    Test: StatusBarConfig dataclass.
    """
    print("=" * 70)
    print("TEST: StatusBarConfig Dataclass")
    print("=" * 70)
    
    config = StatusBarConfig(
        enabled=True,
        show_line_column=True,
        show_git_branch=True
    )
    
    assert config.enabled == True, "Enabled eşleşmeli"
    assert config.show_line_column == True, "Show line column eşleşmeli"
    assert config.show_git_branch == True, "Show git branch eşleşmeli"
    
    print(f"  Enabled: {config.enabled}")
    print(f"  Show line column: {config.show_line_column}")
    print(f"  Show git branch: {config.show_git_branch}")
    
    print("\n" + "=" * 70)
    print("PASS: StatusBarConfig dataclass")
    print("=" * 70)


def test_status_bar_result_dataclass():
    """
    Test: StatusBarResult dataclass.
    """
    print("=" * 70)
    print("TEST: StatusBarResult Dataclass")
    print("=" * 70)
    
    result = StatusBarResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.items, list), "Items list olmalı"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Items: {len(result.items)}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: StatusBarResult dataclass")
    print("=" * 70)


def test_status_bar_manager_initialization():
    """
    Test: StatusBarManager initialization.
    """
    print("=" * 70)
    print("TEST: StatusBarManager Initialization")
    print("=" * 70)
    
    config = StatusBarConfig()
    manager = StatusBarManager(config)
    
    assert manager.config == config, "Config eşleşmeli"
    assert len(manager.items) > 0, "Items olmalı"
    
    print(f"  Items: {len(manager.items)}")
    
    print("\n" + "=" * 70)
    print("PASS: StatusBarManager initialization")
    print("=" * 70)


def test_add_item():
    """
    Test: Add item.
    """
    print("=" * 70)
    print("TEST: Add Item")
    print("=" * 70)
    
    manager = StatusBarManager()
    
    item = StatusItem(
        id="custom_item",
        label="Custom",
        position=StatusItemPosition.LEFT
    )
    
    result = manager.add_item(item)
    
    assert result.success == True, "Ekleme başarılı olmalı"
    assert "custom_item" in manager.items, "Item eklenmeli"
    
    print(f"  Item added: {item.label}")
    
    print("\n" + "=" * 70)
    print("PASS: Add item")
    print("=" * 70)


def test_remove_item():
    """
    Test: Remove item.
    """
    print("=" * 70)
    print("TEST: Remove Item")
    print("=" * 70)
    
    manager = StatusBarManager()
    
    item = StatusItem(
        id="custom_item",
        label="Custom",
        position=StatusItemPosition.LEFT
    )
    
    manager.add_item(item)
    result = manager.remove_item("custom_item")
    
    assert result.success == True, "Kaldırma başarılı olmalı"
    assert "custom_item" not in manager.items, "Item silinmeli"
    
    print(f"  Item removed: {item.label}")
    
    print("\n" + "=" * 70)
    print("PASS: Remove item")
    print("=" * 70)


def test_get_item():
    """
    Test: Get item.
    """
    print("=" * 70)
    print("TEST: Get Item")
    print("=" * 70)
    
    manager = StatusBarManager()
    
    item = manager.get_item("line_column")
    
    assert item is not None, "Item bulunmalı"
    assert item.id == "line_column", "ID eşleşmeli"
    
    print(f"  Item: {item.label}")
    
    print("\n" + "=" * 70)
    print("PASS: Get item")
    print("=" * 70)


def test_get_items():
    """
    Test: Get items.
    """
    print("=" * 70)
    print("TEST: Get Items")
    print("=" * 70)
    
    manager = StatusBarManager()
    
    items = manager.get_items()
    
    assert len(items) > 0, "Items olmalı"
    
    print(f"  Items: {len(items)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get items")
    print("=" * 70)


def test_get_items_by_position():
    """
    Test: Get items by position.
    """
    print("=" * 70)
    print("TEST: Get Items by Position")
    print("=" * 70)
    
    manager = StatusBarManager()
    
    left_items = manager.get_items_by_position(StatusItemPosition.LEFT)
    
    assert len(left_items) > 0, "Left items olmalı"
    
    print(f"  Left items: {len(left_items)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get items by position")
    print("=" * 70)


def test_update_item():
    """
    Test: Update item.
    """
    print("=" * 70)
    print("TEST: Update Item")
    print("=" * 70)
    
    manager = StatusBarManager()
    
    result = manager.update_item("line_column", label="Ln 10, Col 5")
    
    assert result.success == True, "Update başarılı olmalı"
    
    print(f"  Item updated: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Update item")
    print("=" * 70)


def test_set_line_column():
    """
    Test: Set line column.
    """
    print("=" * 70)
    print("TEST: Set Line Column")
    print("=" * 70)
    
    manager = StatusBarManager()
    
    result = manager.set_line_column(10, 5)
    
    assert result.success == True, "Set başarılı olmalı"
    
    print(f"  Line column set: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set line column")
    print("=" * 70)


def test_set_file_encoding():
    """
    Test: Set file encoding.
    """
    print("=" * 70)
    print("TEST: Set File Encoding")
    print("=" * 70)
    
    manager = StatusBarManager()
    
    result = manager.set_file_encoding("UTF-8")
    
    assert result.success == True, "Set başarılı olmalı"
    
    print(f"  Encoding set: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set file encoding")
    print("=" * 70)


def test_set_file_type():
    """
    Test: Set file type.
    """
    print("=" * 70)
    print("TEST: Set File Type")
    print("=" * 70)
    
    manager = StatusBarManager()
    
    result = manager.set_file_type("Python")
    
    assert result.success == True, "Set başarılı olmalı"
    
    print(f"  File type set: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set file type")
    print("=" * 70)


def test_set_git_branch():
    """
    Test: Set git branch.
    """
    print("=" * 70)
    print("TEST: Set Git Branch")
    print("=" * 70)
    
    manager = StatusBarManager()
    
    result = manager.set_git_branch("main")
    
    assert result.success == True, "Set başarılı olmalı"
    
    print(f"  Git branch set: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set git branch")
    print("=" * 70)


def test_set_indentation():
    """
    Test: Set indentation.
    """
    print("=" * 70)
    print("TEST: Set Indentation")
    print("=" * 70)
    
    manager = StatusBarManager()
    
    result = manager.set_indentation("Spaces", 4)
    
    assert result.success == True, "Set başarılı olmalı"
    
    print(f"  Indentation set: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set indentation")
    print("=" * 70)


def test_set_language():
    """
    Test: Set language.
    """
    print("=" * 70)
    print("TEST: Set Language")
    print("=" * 70)
    
    manager = StatusBarManager()
    
    result = manager.set_language("Python")
    
    assert result.success == True, "Set başarılı olmalı"
    
    print(f"  Language set: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set language")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    manager = StatusBarManager()
    
    new_config = StatusBarConfig(max_items_per_section=10)
    result = manager.update_config(new_config)
    
    assert result.success == True, "Update başarılı olmalı"
    assert manager.config.max_items_per_section == 10, "Config güncellenmeli"
    
    print(f"  Max items per section: {manager.config.max_items_per_section}")
    
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
    
    config = StatusBarConfig(max_items_per_section=10)
    manager = StatusBarManager(config)
    
    retrieved_config = manager.get_config()
    
    assert retrieved_config.max_items_per_section == 10, "Config eşleşmeli"
    
    print(f"  Max items per section: {retrieved_config.max_items_per_section}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_status_item_position_enum()
        test2 = test_status_item_priority_enum()
        test3 = test_status_item_dataclass()
        test4 = test_status_bar_config_dataclass()
        test5 = test_status_bar_result_dataclass()
        test6 = test_status_bar_manager_initialization()
        test7 = test_add_item()
        test8 = test_remove_item()
        test9 = test_get_item()
        test10 = test_get_items()
        test11 = test_get_items_by_position()
        test12 = test_update_item()
        test13 = test_set_line_column()
        test14 = test_set_file_encoding()
        test15 = test_set_file_type()
        test16 = test_set_git_branch()
        test17 = test_set_indentation()
        test18 = test_set_language()
        test19 = test_update_config()
        test20 = test_get_config()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"StatusItemPosition Enum: {'PASS' if test1 else 'FAIL'}")
        print(f"StatusItemPriority Enum: {'PASS' if test2 else 'FAIL'}")
        print(f"StatusItem Dataclass: {'PASS' if test3 else 'FAIL'}")
        print(f"StatusBarConfig Dataclass: {'PASS' if test4 else 'FAIL'}")
        print(f"StatusBarResult Dataclass: {'PASS' if test5 else 'FAIL'}")
        print(f"StatusBarManager Initialization: {'PASS' if test6 else 'FAIL'}")
        print(f"Add Item: {'PASS' if test7 else 'FAIL'}")
        print(f"Remove Item: {'PASS' if test8 else 'FAIL'}")
        print(f"Get Item: {'PASS' if test9 else 'FAIL'}")
        print(f"Get Items: {'PASS' if test10 else 'FAIL'}")
        print(f"Get Items by Position: {'PASS' if test11 else 'FAIL'}")
        print(f"Update Item: {'PASS' if test12 else 'FAIL'}")
        print(f"Set Line Column: {'PASS' if test13 else 'FAIL'}")
        print(f"Set File Encoding: {'PASS' if test14 else 'FAIL'}")
        print(f"Set File Type: {'PASS' if test15 else 'FAIL'}")
        print(f"Set Git Branch: {'PASS' if test16 else 'FAIL'}")
        print(f"Set Indentation: {'PASS' if test17 else 'FAIL'}")
        print(f"Set Language: {'PASS' if test18 else 'FAIL'}")
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
