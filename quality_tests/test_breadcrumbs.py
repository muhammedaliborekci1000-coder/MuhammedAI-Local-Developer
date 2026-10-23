"""
Quality Test: Breadcrumbs
Breadcrumbs system testleri.
"""

import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from app.editor.breadcrumbs import (
    BreadcrumbType,
    BreadcrumbSeparator,
    BreadcrumbItem,
    BreadcrumbConfig,
    BreadcrumbResult,
    BreadcrumbManager
)


def test_breadcrumb_type_enum():
    """
    Test: BreadcrumbType enum.
    """
    print("=" * 70)
    print("TEST: BreadcrumbType Enum")
    print("=" * 70)
    
    assert BreadcrumbType.FILE.value == "file"
    assert BreadcrumbType.SYMBOL.value == "symbol"
    assert BreadcrumbType.DIRECTORY.value == "directory"
    assert BreadcrumbType.PROJECT.value == "project"
    
    print(f"  All enum values verified")
    print(f"  Total types: {len(BreadcrumbType)}")
    
    print("\n" + "=" * 70)
    print("PASS: BreadcrumbType enum")
    print("=" * 70)


def test_breadcrumb_separator_enum():
    """
    Test: BreadcrumbSeparator enum.
    """
    print("=" * 70)
    print("TEST: BreadcrumbSeparator Enum")
    print("=" * 70)
    
    assert BreadcrumbSeparator.ARROW.value == "arrow"
    assert BreadcrumbSeparator.SLASH.value == "slash"
    assert BreadcrumbSeparator.DOT.value == "dot"
    assert BreadcrumbSeparator.NONE.value == "none"
    
    print(f"  All enum values verified")
    print(f"  Total separators: {len(BreadcrumbSeparator)}")
    
    print("\n" + "=" * 70)
    print("PASS: BreadcrumbSeparator enum")
    print("=" * 70)


def test_breadcrumb_item_dataclass():
    """
    Test: BreadcrumbItem dataclass.
    """
    print("=" * 70)
    print("TEST: BreadcrumbItem Dataclass")
    print("=" * 70)
    
    item = BreadcrumbItem(
        id="breadcrumb_1",
        label="main.py",
        type=BreadcrumbType.FILE,
        path="src/main.py"
    )
    
    assert item.id == "breadcrumb_1", "ID eşleşmeli"
    assert item.label == "main.py", "Label eşleşmeli"
    assert item.type == BreadcrumbType.FILE, "Type eşleşmeli"
    
    print(f"  ID: {item.id}")
    print(f"  Label: {item.label}")
    print(f"  Type: {item.type.value}")
    
    print("\n" + "=" * 70)
    print("PASS: BreadcrumbItem dataclass")
    print("=" * 70)


def test_breadcrumb_config_dataclass():
    """
    Test: BreadcrumbConfig dataclass.
    """
    print("=" * 70)
    print("TEST: BreadcrumbConfig Dataclass")
    print("=" * 70)
    
    config = BreadcrumbConfig(
        enabled=True,
        show_file_breadcrumbs=True,
        separator=BreadcrumbSeparator.ARROW
    )
    
    assert config.enabled == True, "Enabled eşleşmeli"
    assert config.show_file_breadcrumbs == True, "Show file breadcrumbs eşleşmeli"
    assert config.separator == BreadcrumbSeparator.ARROW, "Separator eşleşmeli"
    
    print(f"  Enabled: {config.enabled}")
    print(f"  Show file breadcrumbs: {config.show_file_breadcrumbs}")
    print(f"  Separator: {config.separator.value}")
    
    print("\n" + "=" * 70)
    print("PASS: BreadcrumbConfig dataclass")
    print("=" * 70)


def test_breadcrumb_result_dataclass():
    """
    Test: BreadcrumbResult dataclass.
    """
    print("=" * 70)
    print("TEST: BreadcrumbResult Dataclass")
    print("=" * 70)
    
    result = BreadcrumbResult(success=True)
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
    print("PASS: BreadcrumbResult dataclass")
    print("=" * 70)


def test_breadcrumb_manager_initialization():
    """
    Test: BreadcrumbManager initialization.
    """
    print("=" * 70)
    print("TEST: BreadcrumbManager Initialization")
    print("=" * 70)
    
    config = BreadcrumbConfig()
    manager = BreadcrumbManager(config)
    
    assert manager.config == config, "Config eşleşmeli"
    assert len(manager.current_items) == 0, "Current items boş olmalı"
    
    print(f"  Current items: {len(manager.current_items)}")
    
    print("\n" + "=" * 70)
    print("PASS: BreadcrumbManager initialization")
    print("=" * 70)


def test_generate_file_breadcrumbs():
    """
    Test: Generate file breadcrumbs.
    """
    print("=" * 70)
    print("TEST: Generate File Breadcrumbs")
    print("=" * 70)
    
    manager = BreadcrumbManager()
    
    result = manager.generate_file_breadcrumbs("src/app/editor/main.py")
    
    assert result.success == True, "Generation başarılı olmalı"
    assert len(result.items) > 0, "Items oluşturulmalı"
    
    print(f"  Items: {len(result.items)}")
    
    print("\n" + "=" * 70)
    print("PASS: Generate file breadcrumbs")
    print("=" * 70)


def test_generate_symbol_breadcrumbs():
    """
    Test: Generate symbol breadcrumbs.
    """
    print("=" * 70)
    print("TEST: Generate Symbol Breadcrumbs")
    print("=" * 70)
    
    manager = BreadcrumbManager()
    
    code = """class MyClass:
    def __init__(self):
        pass
    
    def my_method(self):
        pass
"""
    
    result = manager.generate_symbol_breadcrumbs(code, 0)
    
    assert result.success == True, "Generation başarılı olmalı"
    
    print(f"  Items: {len(result.items)}")
    
    print("\n" + "=" * 70)
    print("PASS: Generate symbol breadcrumbs")
    print("=" * 70)


def test_navigate_to_breadcrumb():
    """
    Test: Navigate to breadcrumb.
    """
    print("=" * 70)
    print("TEST: Navigate to Breadcrumb")
    print("=" * 70)
    
    manager = BreadcrumbManager()
    
    manager.generate_file_breadcrumbs("src/app/editor/main.py")
    
    if manager.current_items:
        result = manager.navigate_to_breadcrumb(manager.current_items[0].id)
        
        assert result.success == True, "Navigation başarılı olmalı"
        
        print(f"  Navigated: {result.message}")
    else:
        print("  No items to navigate")
    
    print("\n" + "=" * 70)
    print("PASS: Navigate to breadcrumb")
    print("=" * 70)


def test_get_navigation_history():
    """
    Test: Get navigation history.
    """
    print("=" * 70)
    print("TEST: Get Navigation History")
    print("=" * 70)
    
    manager = BreadcrumbManager()
    
    manager.generate_file_breadcrumbs("src/app/editor/main.py")
    
    if manager.current_items:
        manager.navigate_to_breadcrumb(manager.current_items[0].id)
    
    history = manager.get_navigation_history()
    
    print(f"  History: {len(history)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get navigation history")
    print("=" * 70)


def test_clear_history():
    """
    Test: Clear history.
    """
    print("=" * 70)
    print("TEST: Clear History")
    print("=" * 70)
    
    manager = BreadcrumbManager()
    
    manager.generate_file_breadcrumbs("src/app/editor/main.py")
    
    if manager.current_items:
        manager.navigate_to_breadcrumb(manager.current_items[0].id)
    
    manager.clear_history()
    
    history = manager.get_navigation_history()
    
    assert len(history) == 0, "History temizlenmeli"
    
    print(f"  History cleared")
    
    print("\n" + "=" * 70)
    print("PASS: Clear history")
    print("=" * 70)


def test_get_current_items():
    """
    Test: Get current items.
    """
    print("=" * 70)
    print("TEST: Get Current Items")
    print("=" * 70)
    
    manager = BreadcrumbManager()
    
    manager.generate_file_breadcrumbs("src/app/editor/main.py")
    
    items = manager.get_current_items()
    
    assert len(items) > 0, "Items olmalı"
    
    print(f"  Items: {len(items)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get current items")
    print("=" * 70)


def test_set_separator():
    """
    Test: Set separator.
    """
    print("=" * 70)
    print("TEST: Set Separator")
    print("=" * 70)
    
    manager = BreadcrumbManager()
    
    result = manager.set_separator(BreadcrumbSeparator.SLASH)
    
    assert result.success == True, "Set başarılı olmalı"
    assert manager.config.separator == BreadcrumbSeparator.SLASH, "Separator eşleşmeli"
    
    print(f"  Separator: {manager.config.separator.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Set separator")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    manager = BreadcrumbManager()
    
    new_config = BreadcrumbConfig(max_items=20)
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
    
    config = BreadcrumbConfig(max_items=20)
    manager = BreadcrumbManager(config)
    
    retrieved_config = manager.get_config()
    
    assert retrieved_config.max_items == 20, "Config eşleşmeli"
    
    print(f"  Max items: {retrieved_config.max_items}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_breadcrumb_type_enum()
        test2 = test_breadcrumb_separator_enum()
        test3 = test_breadcrumb_item_dataclass()
        test4 = test_breadcrumb_config_dataclass()
        test5 = test_breadcrumb_result_dataclass()
        test6 = test_breadcrumb_manager_initialization()
        test7 = test_generate_file_breadcrumbs()
        test8 = test_generate_symbol_breadcrumbs()
        test9 = test_navigate_to_breadcrumb()
        test10 = test_get_navigation_history()
        test11 = test_clear_history()
        test12 = test_get_current_items()
        test13 = test_set_separator()
        test14 = test_update_config()
        test15 = test_get_config()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"BreadcrumbType Enum: {'PASS' if test1 else 'FAIL'}")
        print(f"BreadcrumbSeparator Enum: {'PASS' if test2 else 'FAIL'}")
        print(f"BreadcrumbItem Dataclass: {'PASS' if test3 else 'FAIL'}")
        print(f"BreadcrumbConfig Dataclass: {'PASS' if test4 else 'FAIL'}")
        print(f"BreadcrumbResult Dataclass: {'PASS' if test5 else 'FAIL'}")
        print(f"BreadcrumbManager Initialization: {'PASS' if test6 else 'FAIL'}")
        print(f"Generate File Breadcrumbs: {'PASS' if test7 else 'FAIL'}")
        print(f"Generate Symbol Breadcrumbs: {'PASS' if test8 else 'FAIL'}")
        print(f"Navigate to Breadcrumb: {'PASS' if test9 else 'FAIL'}")
        print(f"Get Navigation History: {'PASS' if test10 else 'FAIL'}")
        print(f"Clear History: {'PASS' if test11 else 'FAIL'}")
        print(f"Get Current Items: {'PASS' if test12 else 'FAIL'}")
        print(f"Set Separator: {'PASS' if test13 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test14 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test15 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14, test15])
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
