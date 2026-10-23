"""
Quality Test: Sidebar UI
Sidebar UI system testleri for UI module.
"""

import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from app.ui.sidebar_ui import (
    SidebarPosition,
    SidebarPanel,
    SidebarItem,
    SidebarConfig,
    SidebarResult,
    SidebarUIManager
)


def test_sidebar_position_enum():
    """
    Test: SidebarPosition enum.
    """
    print("=" * 70)
    print("TEST: SidebarPosition Enum")
    print("=" * 70)
    
    assert SidebarPosition.LEFT.value == "left"
    assert SidebarPosition.RIGHT.value == "right"
    assert SidebarPosition.CUSTOM.value == "custom"
    
    print(f"  All enum values verified")
    print(f"  Total positions: {len(SidebarPosition)}")
    
    print("\n" + "=" * 70)
    print("PASS: SidebarPosition enum")
    print("=" * 70)


def test_sidebar_panel_enum():
    """
    Test: SidebarPanel enum.
    """
    print("=" * 70)
    print("TEST: SidebarPanel Enum")
    print("=" * 70)
    
    assert SidebarPanel.FILE_EXPLORER.value == "file_explorer"
    assert SidebarPanel.SEARCH.value == "search"
    assert SidebarPanel.GIT.value == "git"
    assert SidebarPanel.DEBUG.value == "debug"
    assert SidebarPanel.EXTENSIONS.value == "extensions"
    assert SidebarPanel.OUTLINE.value == "outline"
    assert SidebarPanel.PROBLEMS.value == "problems"
    assert SidebarPanel.OUTPUT.value == "output"
    assert SidebarPanel.TERMINAL.value == "terminal"
    assert SidebarPanel.CUSTOM.value == "custom"
    
    print(f"  All enum values verified")
    print(f"  Total panels: {len(SidebarPanel)}")
    
    print("\n" + "=" * 70)
    print("PASS: SidebarPanel enum")
    print("=" * 70)


def test_sidebar_item_dataclass():
    """
    Test: SidebarItem dataclass.
    """
    print("=" * 70)
    print("TEST: SidebarItem Dataclass")
    print("=" * 70)
    
    item = SidebarItem(
        id="item_1",
        panel=SidebarPanel.FILE_EXPLORER,
        title="File Explorer",
        icon="folder"
    )
    
    assert item.id == "item_1", "ID eşleşmeli"
    assert item.panel == SidebarPanel.FILE_EXPLORER, "Panel eşleşmeli"
    assert item.title == "File Explorer", "Title eşleşmeli"
    assert item.icon == "folder", "Icon eşleşmeli"
    
    print(f"  ID: {item.id}")
    print(f"  Panel: {item.panel.value}")
    print(f"  Title: {item.title}")
    print(f"  Icon: {item.icon}")
    
    print("\n" + "=" * 70)
    print("PASS: SidebarItem dataclass")
    print("=" * 70)


def test_sidebar_config_dataclass():
    """
    Test: SidebarConfig dataclass.
    """
    print("=" * 70)
    print("TEST: SidebarConfig Dataclass")
    print("=" * 70)
    
    config = SidebarConfig(
        enabled=True,
        position=SidebarPosition.LEFT
    )
    
    assert config.enabled == True, "Enabled eşleşmeli"
    assert config.position == SidebarPosition.LEFT, "Position eşleşmeli"
    
    print(f"  Enabled: {config.enabled}")
    print(f"  Position: {config.position.value}")
    
    print("\n" + "=" * 70)
    print("PASS: SidebarConfig dataclass")
    print("=" * 70)


def test_sidebar_result_dataclass():
    """
    Test: SidebarResult dataclass.
    """
    print("=" * 70)
    print("TEST: SidebarResult Dataclass")
    print("=" * 70)
    
    result = SidebarResult(success=True)
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
    print("PASS: SidebarResult dataclass")
    print("=" * 70)


def test_sidebar_ui_manager_initialization():
    """
    Test: SidebarUIManager initialization.
    """
    print("=" * 70)
    print("TEST: SidebarUIManager Initialization")
    print("=" * 70)
    
    config = SidebarConfig()
    manager = SidebarUIManager(config)
    
    assert manager.config == config, "Config eşleşmeli"
    assert len(manager.items) == 0, "Items boş olmalı"
    assert manager.active_item_id is None, "Active item None olmalı"
    
    print(f"  Items: {len(manager.items)}")
    print(f"  Active item: {manager.active_item_id}")
    
    print("\n" + "=" * 70)
    print("PASS: SidebarUIManager initialization")
    print("=" * 70)


def test_add_item():
    """
    Test: Add item.
    """
    print("=" * 70)
    print("TEST: Add Item")
    print("=" * 70)
    
    manager = SidebarUIManager()
    
    item = SidebarItem(
        id="",
        panel=SidebarPanel.FILE_EXPLORER,
        title="File Explorer",
        icon="folder"
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
    
    manager = SidebarUIManager()
    
    item = SidebarItem(
        id="",
        panel=SidebarPanel.FILE_EXPLORER,
        title="File Explorer",
        icon="folder"
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
    
    manager = SidebarUIManager()
    
    item = SidebarItem(
        id="",
        panel=SidebarPanel.FILE_EXPLORER,
        title="File Explorer",
        icon="folder"
    )
    
    result = manager.add_item(item)
    item_id = result.item.id
    
    retrieved_item = manager.get_item(item_id)
    
    assert retrieved_item is not None, "Item bulunmalı"
    assert retrieved_item.id == item_id, "ID eşleşmeli"
    
    print(f"  Item: {retrieved_item.title}")
    
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
    
    manager = SidebarUIManager()
    
    item = SidebarItem(
        id="",
        panel=SidebarPanel.FILE_EXPLORER,
        title="File Explorer",
        icon="folder"
    )
    
    manager.add_item(item)
    items = manager.get_all_items()
    
    assert len(items) > 0, "Items olmalı"
    
    print(f"  Total items: {len(items)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get all items")
    print("=" * 70)


def test_get_items_by_panel():
    """
    Test: Get items by panel.
    """
    print("=" * 70)
    print("TEST: Get Items by Panel")
    print("=" * 70)
    
    manager = SidebarUIManager()
    
    item = SidebarItem(
        id="",
        panel=SidebarPanel.FILE_EXPLORER,
        title="File Explorer",
        icon="folder"
    )
    
    manager.add_item(item)
    items = manager.get_items_by_panel(SidebarPanel.FILE_EXPLORER)
    
    assert len(items) > 0, "File explorer items olmalı"
    
    print(f"  File explorer items: {len(items)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get items by panel")
    print("=" * 70)


def test_set_active_item():
    """
    Test: Set active item.
    """
    print("=" * 70)
    print("TEST: Set Active Item")
    print("=" * 70)
    
    manager = SidebarUIManager()
    
    item = SidebarItem(
        id="",
        panel=SidebarPanel.FILE_EXPLORER,
        title="File Explorer",
        icon="folder"
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


def test_collapse_item():
    """
    Test: Collapse item.
    """
    print("=" * 70)
    print("TEST: Collapse Item")
    print("=" * 70)
    
    manager = SidebarUIManager()
    
    item = SidebarItem(
        id="",
        panel=SidebarPanel.FILE_EXPLORER,
        title="File Explorer",
        icon="folder"
    )
    
    result = manager.add_item(item)
    item_id = result.item.id
    
    result = manager.collapse_item(item_id)
    
    assert result.success == True, "Collapse başarılı olmalı"
    
    print(f"  Item collapsed: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Collapse item")
    print("=" * 70)


def test_expand_item():
    """
    Test: Expand item.
    """
    print("=" * 70)
    print("TEST: Expand Item")
    print("=" * 70)
    
    manager = SidebarUIManager()
    
    item = SidebarItem(
        id="",
        panel=SidebarPanel.FILE_EXPLORER,
        title="File Explorer",
        icon="folder"
    )
    
    result = manager.add_item(item)
    item_id = result.item.id
    
    manager.collapse_item(item_id)
    result = manager.expand_item(item_id)
    
    assert result.success == True, "Expand başarılı olmalı"
    
    print(f"  Item expanded: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Expand item")
    print("=" * 70)


def test_set_item_enabled():
    """
    Test: Set item enabled.
    """
    print("=" * 70)
    print("TEST: Set Item Enabled")
    print("=" * 70)
    
    manager = SidebarUIManager()
    
    item = SidebarItem(
        id="",
        panel=SidebarPanel.FILE_EXPLORER,
        title="File Explorer",
        icon="folder"
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
    
    manager = SidebarUIManager()
    
    item = SidebarItem(
        id="",
        panel=SidebarPanel.FILE_EXPLORER,
        title="File Explorer",
        icon="folder"
    )
    
    result = manager.add_item(item)
    item_id = result.item.id
    
    result = manager.set_item_visible(item_id, False)
    
    assert result.success == True, "Set başarılı olmalı"
    
    print(f"  Item visible state: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set item visible")
    print("=" * 70)


def test_reorder_item():
    """
    Test: Reorder item.
    """
    print("=" * 70)
    print("TEST: Reorder Item")
    print("=" * 70)
    
    manager = SidebarUIManager()
    
    item = SidebarItem(
        id="",
        panel=SidebarPanel.FILE_EXPLORER,
        title="File Explorer",
        icon="folder"
    )
    
    result = manager.add_item(item)
    item_id = result.item.id
    
    result = manager.reorder_item(item_id, 5)
    
    assert result.success == True, "Reorder başarılı olmalı"
    
    print(f"  Item reordered: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Reorder item")
    print("=" * 70)


def test_set_position():
    """
    Test: Set position.
    """
    print("=" * 70)
    print("TEST: Set Position")
    print("=" * 70)
    
    manager = SidebarUIManager()
    
    result = manager.set_position(SidebarPosition.RIGHT)
    
    assert result.success == True, "Set başarılı olmalı"
    assert manager.config.position == SidebarPosition.RIGHT, "Position eşleşmeli"
    
    print(f"  Position set: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set position")
    print("=" * 70)


def test_set_width():
    """
    Test: Set width.
    """
    print("=" * 70)
    print("TEST: Set Width")
    print("=" * 70)
    
    manager = SidebarUIManager()
    
    result = manager.set_width(400)
    
    assert result.success == True, "Set başarılı olmalı"
    assert manager.config.width == 400, "Width eşleşmeli"
    
    print(f"  Width set: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set width")
    print("=" * 70)


def test_clear_all_items():
    """
    Test: Clear all items.
    """
    print("=" * 70)
    print("TEST: Clear All Items")
    print("=" * 70)
    
    manager = SidebarUIManager()
    
    item = SidebarItem(
        id="",
        panel=SidebarPanel.FILE_EXPLORER,
        title="File Explorer",
        icon="folder"
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
    
    manager = SidebarUIManager()
    
    new_config = SidebarConfig(width=400)
    result = manager.update_config(new_config)
    
    assert result.success == True, "Update başarılı olmalı"
    assert manager.config.width == 400, "Config güncellenmeli"
    
    print(f"  Width: {manager.config.width}")
    
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
    
    config = SidebarConfig(width=400)
    manager = SidebarUIManager(config)
    
    retrieved_config = manager.get_config()
    
    assert retrieved_config.width == 400, "Config eşleşmeli"
    
    print(f"  Width: {retrieved_config.width}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_sidebar_position_enum()
        test2 = test_sidebar_panel_enum()
        test3 = test_sidebar_item_dataclass()
        test4 = test_sidebar_config_dataclass()
        test5 = test_sidebar_result_dataclass()
        test6 = test_sidebar_ui_manager_initialization()
        test7 = test_add_item()
        test8 = test_remove_item()
        test9 = test_get_item()
        test10 = test_get_all_items()
        test11 = test_get_items_by_panel()
        test12 = test_set_active_item()
        test13 = test_collapse_item()
        test14 = test_expand_item()
        test15 = test_set_item_enabled()
        test16 = test_set_item_visible()
        test17 = test_reorder_item()
        test18 = test_set_position()
        test19 = test_set_width()
        test20 = test_clear_all_items()
        test21 = test_update_config()
        test22 = test_get_config()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"SidebarPosition Enum: {'PASS' if test1 else 'FAIL'}")
        print(f"SidebarPanel Enum: {'PASS' if test2 else 'FAIL'}")
        print(f"SidebarItem Dataclass: {'PASS' if test3 else 'FAIL'}")
        print(f"SidebarConfig Dataclass: {'PASS' if test4 else 'FAIL'}")
        print(f"SidebarResult Dataclass: {'PASS' if test5 else 'FAIL'}")
        print(f"SidebarUIManager Initialization: {'PASS' if test6 else 'FAIL'}")
        print(f"Add Item: {'PASS' if test7 else 'FAIL'}")
        print(f"Remove Item: {'PASS' if test8 else 'FAIL'}")
        print(f"Get Item: {'PASS' if test9 else 'FAIL'}")
        print(f"Get All Items: {'PASS' if test10 else 'FAIL'}")
        print(f"Get Items by Panel: {'PASS' if test11 else 'FAIL'}")
        print(f"Set Active Item: {'PASS' if test12 else 'FAIL'}")
        print(f"Collapse Item: {'PASS' if test13 else 'FAIL'}")
        print(f"Expand Item: {'PASS' if test14 else 'FAIL'}")
        print(f"Set Item Enabled: {'PASS' if test15 else 'FAIL'}")
        print(f"Set Item Visible: {'PASS' if test16 else 'FAIL'}")
        print(f"Reorder Item: {'PASS' if test17 else 'FAIL'}")
        print(f"Set Position: {'PASS' if test18 else 'FAIL'}")
        print(f"Set Width: {'PASS' if test19 else 'FAIL'}")
        print(f"Clear All Items: {'PASS' if test20 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test21 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test22 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14, test15, test16, test17, test18, test19, test20, test21, test22])
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
