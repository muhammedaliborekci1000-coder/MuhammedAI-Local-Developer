"""
Quality Test: Toolbar
Toolbar system testleri.
"""

import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from app.editor.toolbar import (
    ToolbarItemPosition,
    ToolbarItemType,
    ToolbarItem,
    ToolbarConfig,
    ToolbarResult,
    ToolbarManager
)


def test_toolbar_item_position_enum():
    """
    Test: ToolbarItemPosition enum.
    """
    print("=" * 70)
    print("TEST: ToolbarItemPosition Enum")
    print("=" * 70)
    
    assert ToolbarItemPosition.LEFT.value == "left"
    assert ToolbarItemPosition.CENTER.value == "center"
    assert ToolbarItemPosition.RIGHT.value == "right"
    
    print(f"  All enum values verified")
    print(f"  Total positions: {len(ToolbarItemPosition)}")
    
    print("\n" + "=" * 70)
    print("PASS: ToolbarItemPosition enum")
    print("=" * 70)


def test_toolbar_item_type_enum():
    """
    Test: ToolbarItemType enum.
    """
    print("=" * 70)
    print("TEST: ToolbarItemType Enum")
    print("=" * 70)
    
    assert ToolbarItemType.BUTTON.value == "button"
    assert ToolbarItemType.SEPARATOR.value == "separator"
    assert ToolbarItemType.DROPDOWN.value == "dropdown"
    assert ToolbarItemType.TOGGLE.value == "toggle"
    assert ToolbarItemType.INPUT.value == "input"
    
    print(f"  All enum values verified")
    print(f"  Total types: {len(ToolbarItemType)}")
    
    print("\n" + "=" * 70)
    print("PASS: ToolbarItemType enum")
    print("=" * 70)


def test_toolbar_item_dataclass():
    """
    Test: ToolbarItem dataclass.
    """
    print("=" * 70)
    print("TEST: ToolbarItem Dataclass")
    print("=" * 70)
    
    item = ToolbarItem(
        id="item_1",
        title="Test Item",
        type=ToolbarItemType.BUTTON,
        icon="test"
    )
    
    assert item.id == "item_1", "ID eşleşmeli"
    assert item.title == "Test Item", "Title eşleşmeli"
    assert item.type == ToolbarItemType.BUTTON, "Type eşleşmeli"
    
    print(f"  ID: {item.id}")
    print(f"  Title: {item.title}")
    print(f"  Type: {item.type.value}")
    
    print("\n" + "=" * 70)
    print("PASS: ToolbarItem dataclass")
    print("=" * 70)


def test_toolbar_config_dataclass():
    """
    Test: ToolbarConfig dataclass.
    """
    print("=" * 70)
    print("TEST: ToolbarConfig Dataclass")
    print("=" * 70)
    
    config = ToolbarConfig(
        show_icons=True,
        show_shortcuts=True
    )
    
    assert config.show_icons == True, "Show icons eşleşmeli"
    assert config.show_shortcuts == True, "Show shortcuts eşleşmeli"
    
    print(f"  Show icons: {config.show_icons}")
    print(f"  Show shortcuts: {config.show_shortcuts}")
    
    print("\n" + "=" * 70)
    print("PASS: ToolbarConfig dataclass")
    print("=" * 70)


def test_toolbar_result_dataclass():
    """
    Test: ToolbarResult dataclass.
    """
    print("=" * 70)
    print("TEST: ToolbarResult Dataclass")
    print("=" * 70)
    
    result = ToolbarResult(success=True)
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
    print("PASS: ToolbarResult dataclass")
    print("=" * 70)


def test_toolbar_manager_initialization():
    """
    Test: ToolbarManager initialization.
    """
    print("=" * 70)
    print("TEST: ToolbarManager Initialization")
    print("=" * 70)
    
    config = ToolbarConfig()
    manager = ToolbarManager(config)
    
    assert manager.config == config, "Config eşleşmeli"
    assert len(manager.toolbar_items) > 0, "Toolbar items olmalı"
    
    print(f"  Toolbar items: {len(manager.toolbar_items)}")
    
    print("\n" + "=" * 70)
    print("PASS: ToolbarManager initialization")
    print("=" * 70)


def test_add_toolbar_item():
    """
    Test: Add toolbar item.
    """
    print("=" * 70)
    print("TEST: Add Toolbar Item")
    print("=" * 70)
    
    manager = ToolbarManager()
    
    item = ToolbarItem(
        id="custom",
        title="Custom",
        icon="custom"
    )
    
    result = manager.add_toolbar_item(item)
    
    assert result.success == True, "Ekleme başarılı olmalı"
    assert "custom" in manager.toolbar_items, "Item eklenmeli"
    
    print(f"  Toolbar item added: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add toolbar item")
    print("=" * 70)


def test_remove_toolbar_item():
    """
    Test: Remove toolbar item.
    """
    print("=" * 70)
    print("TEST: Remove Toolbar Item")
    print("=" * 70)
    
    manager = ToolbarManager()
    
    item = ToolbarItem(
        id="custom",
        title="Custom"
    )
    
    manager.add_toolbar_item(item)
    result = manager.remove_toolbar_item("custom")
    
    assert result.success == True, "Kaldırma başarılı olmalı"
    assert "custom" not in manager.toolbar_items, "Item silinmeli"
    
    print(f"  Toolbar item removed: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Remove toolbar item")
    print("=" * 70)


def test_get_toolbar_item():
    """
    Test: Get toolbar item.
    """
    print("=" * 70)
    print("TEST: Get Toolbar Item")
    print("=" * 70)
    
    manager = ToolbarManager()
    
    item = manager.get_toolbar_item("save")
    
    assert item is not None, "Item bulunmalı"
    assert item.id == "save", "ID eşleşmeli"
    
    print(f"  Item: {item.title}")
    
    print("\n" + "=" * 70)
    print("PASS: Get toolbar item")
    print("=" * 70)


def test_get_all_items():
    """
    Test: Get all items.
    """
    print("=" * 70)
    print("TEST: Get All Items")
    print("=" * 70)
    
    manager = ToolbarManager()
    
    items = manager.get_all_items()
    
    assert len(items) > 0, "Items olmalı"
    
    print(f"  Total items: {len(items)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get all items")
    print("=" * 70)


def test_get_items_by_type():
    """
    Test: Get items by type.
    """
    print("=" * 70)
    print("TEST: Get Items by Type")
    print("=" * 70)
    
    manager = ToolbarManager()
    
    items = manager.get_items_by_type(ToolbarItemType.BUTTON)
    
    assert len(items) > 0, "Button items olmalı"
    
    print(f"  Button items: {len(items)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get items by type")
    print("=" * 70)


def test_get_items_by_position():
    """
    Test: Get items by position.
    """
    print("=" * 70)
    print("TEST: Get Items by Position")
    print("=" * 70)
    
    manager = ToolbarManager()
    
    items = manager.get_items_by_position(ToolbarItemPosition.LEFT)
    
    assert len(items) > 0, "Left position items olmalı"
    
    print(f"  Left position items: {len(items)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get items by position")
    print("=" * 70)


def test_execute_action():
    """
    Test: Execute action.
    """
    print("=" * 70)
    print("TEST: Execute Action")
    print("=" * 70)
    
    manager = ToolbarManager()
    
    # Action tanımla
    def test_action():
        pass
    
    item = ToolbarItem(
        id="test_action",
        title="Test Action",
        action=test_action
    )
    
    manager.add_toolbar_item(item)
    result = manager.execute_action("test_action")
    
    assert result.success == True, "Execution başarılı olmalı"
    
    print(f"  Action executed: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Execute action")
    print("=" * 70)


def test_set_item_enabled():
    """
    Test: Set item enabled.
    """
    print("=" * 70)
    print("TEST: Set Item Enabled")
    print("=" * 70)
    
    manager = ToolbarManager()
    
    result = manager.set_item_enabled("save", False)
    
    assert result.success == True, "Set başarılı olmalı"
    
    print(f"  Item enabled state: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set item enabled")
    print("=" * 70)


def test_set_item_visible():
    """
    Test: Set item visible.
    """
    print("=" * 70)
    print("TEST: Set Item Visible")
    print("=" * 70)
    
    manager = ToolbarManager()
    
    result = manager.set_item_visible("save", False)
    
    assert result.success == True, "Set başarılı olmalı"
    
    print(f"  Item visible state: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set item visible")
    print("=" * 70)


def test_set_item_checked():
    """
    Test: Set item checked.
    """
    print("=" * 70)
    print("TEST: Set Item Checked")
    print("=" * 70)
    
    manager = ToolbarManager()
    
    result = manager.set_item_checked("save", True)
    
    assert result.success == True, "Set başarılı olmalı"
    
    print(f"  Item checked state: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set item checked")
    print("=" * 70)


def test_get_visible_items():
    """
    Test: Get visible items.
    """
    print("=" * 70)
    print("TEST: Get Visible Items")
    print("=" * 70)
    
    manager = ToolbarManager()
    
    visible_items = manager.get_visible_items()
    
    assert len(visible_items) > 0, "Visible items olmalı"
    
    print(f"  Visible items: {len(visible_items)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get visible items")
    print("=" * 70)


def test_get_enabled_items():
    """
    Test: Get enabled items.
    """
    print("=" * 70)
    print("TEST: Get Enabled Items")
    print("=" * 70)
    
    manager = ToolbarManager()
    
    enabled_items = manager.get_enabled_items()
    
    assert len(enabled_items) > 0, "Enabled items olmalı"
    
    print(f"  Enabled items: {len(enabled_items)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get enabled items")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    manager = ToolbarManager()
    
    new_config = ToolbarConfig(max_items=30)
    result = manager.update_config(new_config)
    
    assert result.success == True, "Update başarılı olmalı"
    assert manager.config.max_items == 30, "Config güncellenmeli"
    
    print(f"  Max items: {manager.config.max_items}")
    
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
    
    config = ToolbarConfig(max_items=30)
    manager = ToolbarManager(config)
    
    retrieved_config = manager.get_config()
    
    assert retrieved_config.max_items == 30, "Config eşleşmeli"
    
    print(f"  Max items: {retrieved_config.max_items}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_toolbar_item_position_enum()
        test2 = test_toolbar_item_type_enum()
        test3 = test_toolbar_item_dataclass()
        test4 = test_toolbar_config_dataclass()
        test5 = test_toolbar_result_dataclass()
        test6 = test_toolbar_manager_initialization()
        test7 = test_add_toolbar_item()
        test8 = test_remove_toolbar_item()
        test9 = test_get_toolbar_item()
        test10 = test_get_all_items()
        test11 = test_get_items_by_type()
        test12 = test_get_items_by_position()
        test13 = test_execute_action()
        test14 = test_set_item_enabled()
        test15 = test_set_item_visible()
        test16 = test_set_item_checked()
        test17 = test_get_visible_items()
        test18 = test_get_enabled_items()
        test19 = test_update_config()
        test20 = test_get_config()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"ToolbarItemPosition Enum: {'PASS' if test1 else 'FAIL'}")
        print(f"ToolbarItemType Enum: {'PASS' if test2 else 'FAIL'}")
        print(f"ToolbarItem Dataclass: {'PASS' if test3 else 'FAIL'}")
        print(f"ToolbarConfig Dataclass: {'PASS' if test4 else 'FAIL'}")
        print(f"ToolbarResult Dataclass: {'PASS' if test5 else 'FAIL'}")
        print(f"ToolbarManager Initialization: {'PASS' if test6 else 'FAIL'}")
        print(f"Add Toolbar Item: {'PASS' if test7 else 'FAIL'}")
        print(f"Remove Toolbar Item: {'PASS' if test8 else 'FAIL'}")
        print(f"Get Toolbar Item: {'PASS' if test9 else 'FAIL'}")
        print(f"Get All Items: {'PASS' if test10 else 'FAIL'}")
        print(f"Get Items by Type: {'PASS' if test11 else 'FAIL'}")
        print(f"Get Items by Position: {'PASS' if test12 else 'FAIL'}")
        print(f"Execute Action: {'PASS' if test13 else 'FAIL'}")
        print(f"Set Item Enabled: {'PASS' if test14 else 'FAIL'}")
        print(f"Set Item Visible: {'PASS' if test15 else 'FAIL'}")
        print(f"Set Item Checked: {'PASS' if test16 else 'FAIL'}")
        print(f"Get Visible Items: {'PASS' if test17 else 'FAIL'}")
        print(f"Get Enabled Items: {'PASS' if test18 else 'FAIL'}")
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
