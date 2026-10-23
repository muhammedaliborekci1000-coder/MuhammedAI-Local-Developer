"""
Quality Test: Header UI
Header UI system testleri for UI module.
"""

import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from app.ui.header_ui import (
    HeaderAction,
    HeaderPosition,
    HeaderItem,
    HeaderConfig,
    HeaderResult,
    HeaderUIManager
)


def test_header_action_enum():
    """
    Test: HeaderAction enum.
    """
    print("=" * 70)
    print("TEST: HeaderAction Enum")
    print("=" * 70)
    
    assert HeaderAction.MENU.value == "menu"
    assert HeaderAction.BUTTON.value == "button"
    assert HeaderAction.DROPDOWN.value == "dropdown"
    assert HeaderAction.SEARCH.value == "search"
    assert HeaderAction.LINK.value == "link"
    assert HeaderAction.CUSTOM.value == "custom"
    
    print(f"  All enum values verified")
    print(f"  Total actions: {len(HeaderAction)}")
    
    print("\n" + "=" * 70)
    print("PASS: HeaderAction enum")
    print("=" * 70)


def test_header_position_enum():
    """
    Test: HeaderPosition enum.
    """
    print("=" * 70)
    print("TEST: HeaderPosition Enum")
    print("=" * 70)
    
    assert HeaderPosition.TOP.value == "top"
    assert HeaderPosition.BOTTOM.value == "bottom"
    assert HeaderPosition.LEFT.value == "left"
    assert HeaderPosition.RIGHT.value == "right"
    assert HeaderPosition.CENTER.value == "center"
    assert HeaderPosition.CUSTOM.value == "custom"
    
    print(f"  All enum values verified")
    print(f"  Total positions: {len(HeaderPosition)}")
    
    print("\n" + "=" * 70)
    print("PASS: HeaderPosition enum")
    print("=" * 70)


def test_header_item_dataclass():
    """
    Test: HeaderItem dataclass.
    """
    print("=" * 70)
    print("TEST: HeaderItem Dataclass")
    print("=" * 70)
    
    item = HeaderItem(
        id="item_1",
        action=HeaderAction.BUTTON,
        label="Save",
        icon="save"
    )
    
    assert item.id == "item_1", "ID eşleşmeli"
    assert item.action == HeaderAction.BUTTON, "Action eşleşmeli"
    assert item.label == "Save", "Label eşleşmeli"
    assert item.icon == "save", "Icon eşleşmeli"
    
    print(f"  ID: {item.id}")
    print(f"  Action: {item.action.value}")
    print(f"  Label: {item.label}")
    print(f"  Icon: {item.icon}")
    
    print("\n" + "=" * 70)
    print("PASS: HeaderItem dataclass")
    print("=" * 70)


def test_header_config_dataclass():
    """
    Test: HeaderConfig dataclass.
    """
    print("=" * 70)
    print("TEST: HeaderConfig Dataclass")
    print("=" * 70)
    
    config = HeaderConfig(
        enabled=True,
        show_title=True
    )
    
    assert config.enabled == True, "Enabled eşleşmeli"
    assert config.show_title == True, "Show title eşleşmeli"
    
    print(f"  Enabled: {config.enabled}")
    print(f"  Show title: {config.show_title}")
    
    print("\n" + "=" * 70)
    print("PASS: HeaderConfig dataclass")
    print("=" * 70)


def test_header_result_dataclass():
    """
    Test: HeaderResult dataclass.
    """
    print("=" * 70)
    print("TEST: HeaderResult Dataclass")
    print("=" * 70)
    
    result = HeaderResult(success=True)
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
    print("PASS: HeaderResult dataclass")
    print("=" * 70)


def test_header_ui_manager_initialization():
    """
    Test: HeaderUIManager initialization.
    """
    print("=" * 70)
    print("TEST: HeaderUIManager Initialization")
    print("=" * 70)
    
    config = HeaderConfig()
    manager = HeaderUIManager(config)
    
    assert manager.config == config, "Config eşleşmeli"
    assert len(manager.items) == 0, "Items boş olmalı"
    assert manager.active_item_id is None, "Active item None olmalı"
    
    print(f"  Items: {len(manager.items)}")
    print(f"  Active item: {manager.active_item_id}")
    
    print("\n" + "=" * 70)
    print("PASS: HeaderUIManager initialization")
    print("=" * 70)


def test_add_item():
    """
    Test: Add item.
    """
    print("=" * 70)
    print("TEST: Add Item")
    print("=" * 70)
    
    manager = HeaderUIManager()
    
    item = HeaderItem(
        id="",
        action=HeaderAction.BUTTON,
        label="Save",
        icon="save"
    )
    
    result = manager.add_item(item)
    
    assert result.success == True, "Ekleme başarılı olmalı"
    assert result.item is not None, "Item olmalı"
    assert len(manager.items) > 0, "Item eklenmeli"
    
    print(f"  Item added: {result.message}")
    
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
    
    manager = HeaderUIManager()
    
    item = HeaderItem(
        id="",
        action=HeaderAction.BUTTON,
        label="Save",
        icon="save"
    )
    
    result = manager.add_item(item)
    item_id = result.item.id
    
    result = manager.remove_item(item_id)
    
    assert result.success == True, "Silme başarılı olmalı"
    assert item_id not in manager.items, "Item silinmeli"
    
    print(f"  Item removed: {result.message}")
    
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
    
    manager = HeaderUIManager()
    
    item = HeaderItem(
        id="",
        action=HeaderAction.BUTTON,
        label="Save",
        icon="save"
    )
    
    result = manager.add_item(item)
    item_id = result.item.id
    
    retrieved_item = manager.get_item(item_id)
    
    assert retrieved_item is not None, "Item bulunmalı"
    assert retrieved_item.id == item_id, "ID eşleşmeli"
    
    print(f"  Item: {retrieved_item.label}")
    
    print("\n" + "=" * 70)
    print("PASS: Get item")
    print("=" * 70)


def test_get_all_items():
    """
    Test: Get all items.
    """
    print("=" * 70)
    print("TEST: Get All Items")
    print("=" * 70)
    
    manager = HeaderUIManager()
    
    item = HeaderItem(
        id="",
        action=HeaderAction.BUTTON,
        label="Save",
        icon="save"
    )
    
    manager.add_item(item)
    items = manager.get_all_items()
    
    assert len(items) > 0, "Items olmalı"
    
    print(f"  Total items: {len(items)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get all items")
    print("=" * 70)


def test_get_items_by_action():
    """
    Test: Get items by action.
    """
    print("=" * 70)
    print("TEST: Get Items by Action")
    print("=" * 70)
    
    manager = HeaderUIManager()
    
    item = HeaderItem(
        id="",
        action=HeaderAction.BUTTON,
        label="Save",
        icon="save"
    )
    
    manager.add_item(item)
    items = manager.get_items_by_action(HeaderAction.BUTTON)
    
    assert len(items) > 0, "Button items olmalı"
    
    print(f"  Button items: {len(items)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get items by action")
    print("=" * 70)


def test_set_active_item():
    """
    Test: Set active item.
    """
    print("=" * 70)
    print("TEST: Set Active Item")
    print("=" * 70)
    
    manager = HeaderUIManager()
    
    item = HeaderItem(
        id="",
        action=HeaderAction.BUTTON,
        label="Save",
        icon="save"
    )
    
    result = manager.add_item(item)
    item_id = result.item.id
    
    result = manager.set_active_item(item_id)
    
    assert result.success == True, "Set başarılı olmalı"
    assert manager.active_item_id == item_id, "Active item eşleşmeli"
    
    print(f"  Active item set: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set active item")
    print("=" * 70)


def test_set_item_enabled():
    """
    Test: Set item enabled.
    """
    print("=" * 70)
    print("TEST: Set Item Enabled")
    print("=" * 70)
    
    manager = HeaderUIManager()
    
    item = HeaderItem(
        id="",
        action=HeaderAction.BUTTON,
        label="Save",
        icon="save"
    )
    
    result = manager.add_item(item)
    item_id = result.item.id
    
    result = manager.set_item_enabled(item_id, False)
    
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
    
    manager = HeaderUIManager()
    
    item = HeaderItem(
        id="",
        action=HeaderAction.BUTTON,
        label="Save",
        icon="save"
    )
    
    result = manager.add_item(item)
    item_id = result.item.id
    
    result = manager.set_item_visible(item_id, False)
    
    assert result.success == True, "Set başarılı olmalı"
    
    print(f"  Item visible state: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set item visible")
    print("=" * 70)


def test_set_item_badge():
    """
    Test: Set item badge.
    """
    print("=" * 70)
    print("TEST: Set Item Badge")
    print("=" * 70)
    
    manager = HeaderUIManager()
    
    item = HeaderItem(
        id="",
        action=HeaderAction.BUTTON,
        label="Save",
        icon="save"
    )
    
    result = manager.add_item(item)
    item_id = result.item.id
    
    result = manager.set_item_badge(item_id, "3")
    
    assert result.success == True, "Set başarılı olmalı"
    
    print(f"  Item badge set: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set item badge")
    print("=" * 70)


def test_set_item_tooltip():
    """
    Test: Set item tooltip.
    """
    print("=" * 70)
    print("TEST: Set Item Tooltip")
    print("=" * 70)
    
    manager = HeaderUIManager()
    
    item = HeaderItem(
        id="",
        action=HeaderAction.BUTTON,
        label="Save",
        icon="save"
    )
    
    result = manager.add_item(item)
    item_id = result.item.id
    
    result = manager.set_item_tooltip(item_id, "Save file")
    
    assert result.success == True, "Set başarılı olmalı"
    
    print(f"  Item tooltip set: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set item tooltip")
    print("=" * 70)


def test_reorder_item():
    """
    Test: Reorder item.
    """
    print("=" * 70)
    print("TEST: Reorder Item")
    print("=" * 70)
    
    manager = HeaderUIManager()
    
    item = HeaderItem(
        id="",
        action=HeaderAction.BUTTON,
        label="Save",
        icon="save"
    )
    
    result = manager.add_item(item)
    item_id = result.item.id
    
    result = manager.reorder_item(item_id, 5)
    
    assert result.success == True, "Reorder başarılı olmalı"
    
    print(f"  Item reordered: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Reorder item")
    print("=" * 70)


def test_clear_all_items():
    """
    Test: Clear all items.
    """
    print("=" * 70)
    print("TEST: Clear All Items")
    print("=" * 70)
    
    manager = HeaderUIManager()
    
    item = HeaderItem(
        id="",
        action=HeaderAction.BUTTON,
        label="Save",
        icon="save"
    )
    
    manager.add_item(item)
    result = manager.clear_all_items()
    
    assert result.success == True, "Clear başarılı olmalı"
    assert len(manager.items) == 0, "Items temizlenmeli"
    
    print(f"  Items cleared: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear all items")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    manager = HeaderUIManager()
    
    new_config = HeaderConfig(max_items=20)
    result = manager.update_config(new_config)
    
    assert result.success == True, "Update başarılı olmalı"
    assert manager.config.max_items == 20, "Config güncellenmeli"
    
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
    
    config = HeaderConfig(max_items=20)
    manager = HeaderUIManager(config)
    
    retrieved_config = manager.get_config()
    
    assert retrieved_config.max_items == 20, "Config eşleşmeli"
    
    print(f"  Max items: {retrieved_config.max_items}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_header_action_enum()
        test2 = test_header_position_enum()
        test3 = test_header_item_dataclass()
        test4 = test_header_config_dataclass()
        test5 = test_header_result_dataclass()
        test6 = test_header_ui_manager_initialization()
        test7 = test_add_item()
        test8 = test_remove_item()
        test9 = test_get_item()
        test10 = test_get_all_items()
        test11 = test_get_items_by_action()
        test12 = test_set_active_item()
        test13 = test_set_item_enabled()
        test14 = test_set_item_visible()
        test15 = test_set_item_badge()
        test16 = test_set_item_tooltip()
        test17 = test_reorder_item()
        test18 = test_clear_all_items()
        test19 = test_update_config()
        test20 = test_get_config()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"HeaderAction Enum: {'PASS' if test1 else 'FAIL'}")
        print(f"HeaderPosition Enum: {'PASS' if test2 else 'FAIL'}")
        print(f"HeaderItem Dataclass: {'PASS' if test3 else 'FAIL'}")
        print(f"HeaderConfig Dataclass: {'PASS' if test4 else 'FAIL'}")
        print(f"HeaderResult Dataclass: {'PASS' if test5 else 'FAIL'}")
        print(f"HeaderUIManager Initialization: {'PASS' if test6 else 'FAIL'}")
        print(f"Add Item: {'PASS' if test7 else 'FAIL'}")
        print(f"Remove Item: {'PASS' if test8 else 'FAIL'}")
        print(f"Get Item: {'PASS' if test9 else 'FAIL'}")
        print(f"Get All Items: {'PASS' if test10 else 'FAIL'}")
        print(f"Get Items by Action: {'PASS' if test11 else 'FAIL'}")
        print(f"Set Active Item: {'PASS' if test12 else 'FAIL'}")
        print(f"Set Item Enabled: {'PASS' if test13 else 'FAIL'}")
        print(f"Set Item Visible: {'PASS' if test14 else 'FAIL'}")
        print(f"Set Item Badge: {'PASS' if test15 else 'FAIL'}")
        print(f"Set Item Tooltip: {'PASS' if test16 else 'FAIL'}")
        print(f"Reorder Item: {'PASS' if test17 else 'FAIL'}")
        print(f"Clear All Items: {'PASS' if test18 else 'FAIL'}")
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
