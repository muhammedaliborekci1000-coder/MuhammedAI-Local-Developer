"""
Quality Test: Quick Open
Quick open system testleri.
"""

import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from app.editor.quick_open import (
    QuickOpenMode,
    QuickOpenFilter,
    QuickOpenItem,
    QuickOpenConfig,
    QuickOpenResult,
    QuickOpenManager
)


def test_quick_open_mode_enum():
    """
    Test: QuickOpenMode enum.
    """
    print("=" * 70)
    print("TEST: QuickOpenMode Enum")
    print("=" * 70)
    
    assert QuickOpenMode.FILES.value == "files"
    assert QuickOpenMode.SYMBOLS.value == "symbols"
    assert QuickOpenMode.COMMANDS.value == "commands"
    assert QuickOpenMode.RECENT.value == "recent"
    
    print(f"  All enum values verified")
    print(f"  Total modes: {len(QuickOpenMode)}")
    
    print("\n" + "=" * 70)
    print("PASS: QuickOpenMode enum")
    print("=" * 70)


def test_quick_open_filter_enum():
    """
    Test: QuickOpenFilter enum.
    """
    print("=" * 70)
    print("TEST: QuickOpenFilter Enum")
    print("=" * 70)
    
    assert QuickOpenFilter.ALL.value == "all"
    assert QuickOpenFilter.FILES_ONLY.value == "files_only"
    assert QuickOpenFilter.DIRECTORIES_ONLY.value == "directories_only"
    assert QuickOpenFilter.OPEN_FILES.value == "open_files"
    
    print(f"  All enum values verified")
    print(f"  Total filters: {len(QuickOpenFilter)}")
    
    print("\n" + "=" * 70)
    print("PASS: QuickOpenFilter enum")
    print("=" * 70)


def test_quick_open_item_dataclass():
    """
    Test: QuickOpenItem dataclass.
    """
    print("=" * 70)
    print("TEST: QuickOpenItem Dataclass")
    print("=" * 70)
    
    item = QuickOpenItem(
        path="src/main.py",
        name="main.py",
        file_type="python",
        is_open=True,
        language="python"
    )
    
    assert item.path == "src/main.py", "Path eşleşmeli"
    assert item.name == "main.py", "Name eşleşmeli"
    assert item.file_type == "python", "File type eşleşmeli"
    
    print(f"  Path: {item.path}")
    print(f"  Name: {item.name}")
    print(f"  Type: {item.file_type}")
    
    print("\n" + "=" * 70)
    print("PASS: QuickOpenItem dataclass")
    print("=" * 70)


def test_quick_open_config_dataclass():
    """
    Test: QuickOpenConfig dataclass.
    """
    print("=" * 70)
    print("TEST: QuickOpenConfig Dataclass")
    print("=" * 70)
    
    config = QuickOpenConfig(
        max_results=20,
        fuzzy_search=True
    )
    
    assert config.max_results == 20, "Max results eşleşmeli"
    assert config.fuzzy_search == True, "Fuzzy search eşleşmeli"
    
    print(f"  Max results: {config.max_results}")
    print(f"  Fuzzy search: {config.fuzzy_search}")
    
    print("\n" + "=" * 70)
    print("PASS: QuickOpenConfig dataclass")
    print("=" * 70)


def test_quick_open_result_dataclass():
    """
    Test: QuickOpenResult dataclass.
    """
    print("=" * 70)
    print("TEST: QuickOpenResult Dataclass")
    print("=" * 70)
    
    result = QuickOpenResult(success=True)
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
    print("PASS: QuickOpenResult dataclass")
    print("=" * 70)


def test_quick_open_manager_initialization():
    """
    Test: QuickOpenManager initialization.
    """
    print("=" * 70)
    print("TEST: QuickOpenManager Initialization")
    print("=" * 70)
    
    config = QuickOpenConfig()
    manager = QuickOpenManager(config)
    
    assert manager.config == config, "Config eşleşmeli"
    assert len(manager.files) > 0, "Files olmalı"
    
    print(f"  Files: {len(manager.files)}")
    
    print("\n" + "=" * 70)
    print("PASS: QuickOpenManager initialization")
    print("=" * 70)


def test_register_file():
    """
    Test: Register file.
    """
    print("=" * 70)
    print("TEST: Register File")
    print("=" * 70)
    
    manager = QuickOpenManager()
    
    item = QuickOpenItem(
        path="test.py",
        name="test.py",
        file_type="python"
    )
    
    result = manager.register_file(item)
    
    assert result == True, "Registration başarılı olmalı"
    assert "test.py" in manager.files, "File kaydedilmeli"
    
    print(f"  File registered: {item.name}")
    
    print("\n" + "=" * 70)
    print("PASS: Register file")
    print("=" * 70)


def test_unregister_file():
    """
    Test: Unregister file.
    """
    print("=" * 70)
    print("TEST: Unregister File")
    print("=" * 70)
    
    manager = QuickOpenManager()
    
    item = QuickOpenItem(
        path="test.py",
        name="test.py",
        file_type="python"
    )
    
    manager.register_file(item)
    result = manager.unregister_file("test.py")
    
    assert result == True, "Unregistration başarılı olmalı"
    assert "test.py" not in manager.files, "File silinmeli"
    
    print(f"  File unregistered: {item.name}")
    
    print("\n" + "=" * 70)
    print("PASS: Unregister file")
    print("=" * 70)


def test_search():
    """
    Test: Search.
    """
    print("=" * 70)
    print("TEST: Search")
    print("=" * 70)
    
    manager = QuickOpenManager()
    
    result = manager.search("main")
    
    assert result.success == True, "Search başarılı olmalı"
    assert len(result.items) > 0, "Items bulunmalı"
    
    print(f"  Items found: {len(result.items)}")
    
    print("\n" + "=" * 70)
    print("PASS: Search")
    print("=" * 70)


def test_open_file():
    """
    Test: Open file.
    """
    print("=" * 70)
    print("TEST: Open File")
    print("=" * 70)
    
    manager = QuickOpenManager()
    
    result = manager.open_file("src/main.py")
    
    assert result.success == True, "Open başarılı olmalı"
    assert result.selected_item is not None, "Selected item olmalı"
    
    print(f"  File opened: {result.selected_item.name}")
    
    print("\n" + "=" * 70)
    print("PASS: Open file")
    print("=" * 70)


def test_close_file():
    """
    Test: Close file.
    """
    print("=" * 70)
    print("TEST: Close File")
    print("=" * 70)
    
    manager = QuickOpenManager()
    
    manager.open_file("src/main.py")
    result = manager.close_file("src/main.py")
    
    assert result.success == True, "Close başarılı olmalı"
    
    print(f"  File closed: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Close file")
    print("=" * 70)


def test_get_recent_files():
    """
    Test: Get recent files.
    """
    print("=" * 70)
    print("TEST: Get Recent Files")
    print("=" * 70)
    
    manager = QuickOpenManager()
    
    manager.open_file("src/main.py")
    manager.open_file("src/utils.py")
    
    recent = manager.get_recent_files()
    
    assert len(recent) > 0, "Recent files olmalı"
    
    print(f"  Recent files: {len(recent)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get recent files")
    print("=" * 70)


def test_get_open_files():
    """
    Test: Get open files.
    """
    print("=" * 70)
    print("TEST: Get Open Files")
    print("=" * 70)
    
    manager = QuickOpenManager()
    
    manager.open_file("src/main.py")
    manager.open_file("src/utils.py")
    
    open_files = manager.get_open_files()
    
    assert len(open_files) > 0, "Open files olmalı"
    
    print(f"  Open files: {len(open_files)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get open files")
    print("=" * 70)


def test_get_search_history():
    """
    Test: Get search history.
    """
    print("=" * 70)
    print("TEST: Get Search History")
    print("=" * 70)
    
    manager = QuickOpenManager()
    
    manager.search("main")
    manager.search("utils")
    
    history = manager.get_search_history()
    
    assert len(history) > 0, "History olmalı"
    
    print(f"  History: {len(history)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get search history")
    print("=" * 70)


def test_clear_history():
    """
    Test: Clear history.
    """
    print("=" * 70)
    print("TEST: Clear History")
    print("=" * 70)
    
    manager = QuickOpenManager()
    
    manager.search("main")
    manager.clear_history()
    
    history = manager.get_search_history()
    
    assert len(history) == 0, "History temizlenmeli"
    
    print(f"  History cleared")
    
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
    
    manager = QuickOpenManager()
    
    new_config = QuickOpenConfig(max_results=50)
    manager.update_config(new_config)
    
    assert manager.config.max_results == 50, "Config güncellenmeli"
    
    print(f"  Max results: {manager.config.max_results}")
    
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
    
    config = QuickOpenConfig(max_results=50)
    manager = QuickOpenManager(config)
    
    retrieved_config = manager.get_config()
    
    assert retrieved_config.max_results == 50, "Config eşleşmeli"
    
    print(f"  Max results: {retrieved_config.max_results}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_quick_open_mode_enum()
        test2 = test_quick_open_filter_enum()
        test3 = test_quick_open_item_dataclass()
        test4 = test_quick_open_config_dataclass()
        test5 = test_quick_open_result_dataclass()
        test6 = test_quick_open_manager_initialization()
        test7 = test_register_file()
        test8 = test_unregister_file()
        test9 = test_search()
        test10 = test_open_file()
        test11 = test_close_file()
        test12 = test_get_recent_files()
        test13 = test_get_open_files()
        test14 = test_get_search_history()
        test15 = test_clear_history()
        test16 = test_update_config()
        test17 = test_get_config()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"QuickOpenMode Enum: {'PASS' if test1 else 'FAIL'}")
        print(f"QuickOpenFilter Enum: {'PASS' if test2 else 'FAIL'}")
        print(f"QuickOpenItem Dataclass: {'PASS' if test3 else 'FAIL'}")
        print(f"QuickOpenConfig Dataclass: {'PASS' if test4 else 'FAIL'}")
        print(f"QuickOpenResult Dataclass: {'PASS' if test5 else 'FAIL'}")
        print(f"QuickOpenManager Initialization: {'PASS' if test6 else 'FAIL'}")
        print(f"Register File: {'PASS' if test7 else 'FAIL'}")
        print(f"Unregister File: {'PASS' if test8 else 'FAIL'}")
        print(f"Search: {'PASS' if test9 else 'FAIL'}")
        print(f"Open File: {'PASS' if test10 else 'FAIL'}")
        print(f"Close File: {'PASS' if test11 else 'FAIL'}")
        print(f"Get Recent Files: {'PASS' if test12 else 'FAIL'}")
        print(f"Get Open Files: {'PASS' if test13 else 'FAIL'}")
        print(f"Get Search History: {'PASS' if test14 else 'FAIL'}")
        print(f"Clear History: {'PASS' if test15 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test16 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test17 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14, test15, test16, test17])
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
