"""
Quality Test: Context Menu
Context menu system testleri.
"""

import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from app.editor.context_menu import (
    MenuItemType,
    MenuItem,
    ContextMenuConfig,
    ContextMenuResult,
    ContextMenuManager
)


def test_menu_item_type_enum():
    """
    Test: MenuItemType enum.
    """
    print("=" * 70)
    print("TEST: MenuItemType Enum")
    print("=" * 70)
    
    assert MenuItemType.ACTION.value == "action"
    assert MenuItemType.SUBMENU.value == "submenu"
    assert MenuItemType.SEPARATOR.value == "separator"
    assert MenuItemType.CHECKBOX.value == "checkbox"
    assert MenuItemType.RADIO.value == "radio"
    
    print(f"  All enum values verified")
    print(f"  Total types: {len(MenuItemType)}")
    
    print("\n" + "=" * 70)
    print("PASS: MenuItemType enum")
    print("=" * 70)


def test_menu_item_dataclass():
    """
    Test: MenuItem dataclass.
    """
    print("=" * 70)
    print("TEST: MenuItem Dataclass")
    print("=" * 70)
    
    item = MenuItem(
        id="item_1",
        label="Test Item",
        type=MenuItemType.ACTION,
        icon="test"
    )
    
    assert item.id == "item_1", "ID eşleşmeli"
    assert item.label == "Test Item", "Label eşleşmeli"
    assert item.type == MenuItemType.ACTION, "Type eşleşmeli"
    
    print(f"  ID: {item.id}")
    print(f"  Label: {item.label}")
    print(f"  Type: {item.type.value}")
    
    print("\n" + "=" * 70)
    print("PASS: MenuItem dataclass")
    print("=" * 70)


def test_context_menu_config_dataclass():
    """
    Test: ContextMenuConfig dataclass.
    """
    print("=" * 70)
    print("TEST: ContextMenuConfig Dataclass")
    print("=" * 70)
    
    config = ContextMenuConfig(
        show_icons=True,
        show_shortcuts=True
    )
    
    assert config.show_icons == True, "Show icons eşleşmeli"
    assert config.show_shortcuts == True, "Show shortcuts eşleşmeli"
    
    print(f"  Show icons: {config.show_icons}")
    print(f"  Show shortcuts: {config.show_shortcuts}")
    
    print("\n" + "=" * 70)
    print("PASS: ContextMenuConfig dataclass")
    print("=" * 70)


def test_context_menu_result_dataclass():
    """
    Test: ContextMenuResult dataclass.
    """
    print("=" * 70)
    print("TEST: ContextMenuResult Dataclass")
    print("=" * 70)
    
    result = ContextMenuResult(success=True)
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
    print("PASS: ContextMenuResult dataclass")
    print("=" * 70)


def test_context_menu_manager_initialization():
    """
    Test: ContextMenuManager initialization.
    """
    print("=" * 70)
    print("TEST: ContextMenuManager Initialization")
    print("=" * 70)
    
    config = ContextMenuConfig()
    manager = ContextMenuManager(config)
    
    assert manager.config == config, "Config eşleşmeli"
    assert len(manager.menu_items) > 0, "Menu items olmalı"
    
    print(f"  Menu items: {len(manager.menu_items)}")
    
    print("\n" + "=" * 70)
    print("PASS: ContextMenuManager initialization")
    print("=" * 70)


def test_add_menu_item():
    """
    Test: Add menu item.
    """
    print("=" * 70)
    print("TEST: Add Menu Item")
    print("=" * 70)
    
    manager = ContextMenuManager()
    
    item = MenuItem(
        id="custom",
        label="Custom",
        icon="custom"
    )
    
    result = manager.add_menu_item(item)
    
    assert result.success == True, "Ekleme başarılı olmalı"
    assert "custom" in manager.menu_items, "Item eklenmeli"
    
    print(f"  Menu item added: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add menu item")
    print("=" * 70)


def test_remove_menu_item():
    """
    Test: Remove menu item.
    """
    print("=" * 70)
    print("TEST: Remove Menu Item")
    print("=" * 70)
    
    manager = ContextMenuManager()
    
    item = MenuItem(
        id="custom",
        label="Custom"
    )
    
    manager.add_menu_item(item)
    result = manager.remove_menu_item("custom")
    
    assert result.success == True, "Kaldırma başarılı olmalı"
    assert "custom" not in manager.menu_items, "Item silinmeli"
    
    print(f"  Menu item removed: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Remove menu item")
    print("=" * 70)


def test_get_menu_item():
    """
    Test: Get menu item.
    """
    print("=" * 70)
    print("TEST: Get Menu Item")
    print("=" * 70)
    
    manager = ContextMenuManager()
    
    item = manager.get_menu_item("cut")
    
    assert item is not None, "Item bulunmalı"
    assert item.id == "cut", "ID eşleşmeli"
    
    print(f"  Item: {item.label}")
    
    print("\n" + "=" * 70)
    print("PASS: Get menu item")
    print("=" * 70)


def test_get_all_items():
    """
    Test: Get all items.
    """
    print("=" * 70)
    print("TEST: Get All Items")
    print("=" * 70)
    
    manager = ContextMenuManager()
    
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
    
    manager = ContextMenuManager()
    
    items = manager.get_items_by_type(MenuItemType.ACTION)
    
    assert len(items) > 0, "Action items olmalı"
    
    print(f"  Action items: {len(items)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get items by type")
    print("=" * 70)


def test_execute_action():
    """
    Test: Execute action.
    """
    print("=" * 70)
    print("TEST: Execute Action")
    print("=" * 70)
    
    manager = ContextMenuManager()
    
    # Action tanımla
    def test_action():
        pass
    
    item = MenuItem(
        id="test_action",
        label="Test Action",
        action=test_action
    )
    
    manager.add_menu_item(item)
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
    
    manager = ContextMenuManager()
    
    result = manager.set_item_enabled("cut", False)
    
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
    
    manager = ContextMenuManager()
    
    result = manager.set_item_visible("cut", False)
    
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
    
    manager = ContextMenuManager()
    
    result = manager.set_item_checked("cut", True)
    
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
    
    manager = ContextMenuManager()
    
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
    
    manager = ContextMenuManager()
    
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
    
    manager = ContextMenuManager()
    
    new_config = ContextMenuConfig(max_menu_items=30)
    result = manager.update_config(new_config)
    
    assert result.success == True, "Update başarılı olmalı"
    assert manager.config.max_menu_items == 30, "Config güncellenmeli"
    
    print(f"  Max menu items: {manager.config.max_menu_items}")
    
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
    
    config = ContextMenuConfig(max_menu_items=30)
    manager = ContextMenuManager(config)
    
    retrieved_config = manager.get_config()
    
    assert retrieved_config.max_menu_items == 30, "Config eşleşmeli"
    
    print(f"  Max menu items: {retrieved_config.max_menu_items}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_menu_item_type_enum()
        test2 = test_menu_item_dataclass()
        test3 = test_context_menu_config_dataclass()
        test4 = test_context_menu_result_dataclass()
        test5 = test_context_menu_manager_initialization()
        test6 = test_add_menu_item()
        test7 = test_remove_menu_item()
        test8 = test_get_menu_item()
        test9 = test_get_all_items()
        test10 = test_get_items_by_type()
        test11 = test_execute_action()
        test12 = test_set_item_enabled()
        test13 = test_set_item_visible()
        test14 = test_set_item_checked()
        test15 = test_get_visible_items()
        test16 = test_get_enabled_items()
        test17 = test_update_config()
        test18 = test_get_config()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"MenuItemType Enum: {'PASS' if test1 else 'FAIL'}")
        print(f"MenuItem Dataclass: {'PASS' if test2 else 'FAIL'}")
        print(f"ContextMenuConfig Dataclass: {'PASS' if test3 else 'FAIL'}")
        print(f"ContextMenuResult Dataclass: {'PASS' if test4 else 'FAIL'}")
        print(f"ContextMenuManager Initialization: {'PASS' if test5 else 'FAIL'}")
        print(f"Add Menu Item: {'PASS' if test6 else 'FAIL'}")
        print(f"Remove Menu Item: {'PASS' if test7 else 'FAIL'}")
        print(f"Get Menu Item: {'PASS' if test8 else 'FAIL'}")
        print(f"Get All Items: {'PASS' if test9 else 'FAIL'}")
        print(f"Get Items by Type: {'PASS' if test10 else 'FAIL'}")
        print(f"Execute Action: {'PASS' if test11 else 'FAIL'}")
        print(f"Set Item Enabled: {'PASS' if test12 else 'FAIL'}")
        print(f"Set Item Visible: {'PASS' if test13 else 'FAIL'}")
        print(f"Set Item Checked: {'PASS' if test14 else 'FAIL'}")
        print(f"Get Visible Items: {'PASS' if test15 else 'FAIL'}")
        print(f"Get Enabled Items: {'PASS' if test16 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test17 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test18 else 'FAIL'}")
        
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
