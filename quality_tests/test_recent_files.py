"""
Quality Test: Recent Files
Recent files system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.recent_files import (
    RecentFilesEngine,
    SortMode,
    FilterMode,
    RecentFile,
    RecentFilesConfig,
    RecentFilesResult
)


def test_add_file():
    """
    Test: Add file.
    """
    print("=" * 70)
    print("TEST: Add File")
    print("=" * 70)
    
    engine = RecentFilesEngine()
    
    result = engine.add_file("/path/to/file.txt")
    
    assert result.success, "Ekleme başarılı olmalı"
    assert result.count == 1, "1 dosya olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Count: {result.count}")
    
    print("\n" + "=" * 70)
    print("PASS: Add file")
    print("=" * 70)


def test_remove_file():
    """
    Test: Remove file.
    """
    print("=" * 70)
    print("TEST: Remove File")
    print("=" * 70)
    
    engine = RecentFilesEngine()
    engine.add_file("/path/to/file.txt")
    
    result = engine.remove_file("/path/to/file.txt")
    
    assert result.success, "Kaldırma başarılı olmalı"
    assert result.count == 0, "0 dosya olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Remove file")
    print("=" * 70)


def test_pin_file():
    """
    Test: Pin file.
    """
    print("=" * 70)
    print("TEST: Pin File")
    print("=" * 70)
    
    engine = RecentFilesEngine()
    engine.add_file("/path/to/file.txt")
    
    result = engine.pin_file("/path/to/file.txt")
    
    assert result.success, "Sabitleme başarılı olmalı"
    assert result.files[0].pinned == True, "Dosya sabitlenmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Pin file")
    print("=" * 70)


def test_unpin_file():
    """
    Test: Unpin file.
    """
    print("=" * 70)
    print("TEST: Unpin File")
    print("=" * 70)
    
    engine = RecentFilesEngine()
    engine.add_file("/path/to/file.txt")
    engine.pin_file("/path/to/file.txt")
    
    result = engine.unpin_file("/path/to/file.txt")
    
    assert result.success, "Sabitleme kaldırma başarılı olmalı"
    assert result.files[0].pinned == False, "Dosya sabitlenmemeli"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Unpin file")
    print("=" * 70)


def test_get_recent_files():
    """
    Test: Get recent files.
    """
    print("=" * 70)
    print("TEST: Get Recent Files")
    print("=" * 70)
    
    config = RecentFilesConfig(persist_to_disk=False)
    engine = RecentFilesEngine(config)
    engine.add_file("/path/to/file1.txt")
    engine.add_file("/path/to/file2.txt")
    
    result = engine.get_recent_files()
    
    assert result.success, "Alma başarılı olmalı"
    assert result.count == 2, "2 dosya olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Count: {result.count}")
    
    print("\n" + "=" * 70)
    print("PASS: Get recent files")
    print("=" * 70)


def test_search_files():
    """
    Test: Search files.
    """
    print("=" * 70)
    print("TEST: Search Files")
    print("=" * 70)
    
    config = RecentFilesConfig(persist_to_disk=False)
    engine = RecentFilesEngine(config)
    engine.add_file("/path/to/file.txt")
    engine.add_file("/path/to/file2.txt")
    engine.add_file("/path/to/image.png")
    
    result = engine.search_files("file")
    
    assert result.success, "Arama başarılı olmalı"
    assert result.count == 2, "2 dosya bulunmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Count: {result.count}")
    
    print("\n" + "=" * 70)
    print("PASS: Search files")
    print("=" * 70)


def test_filter_by_extension():
    """
    Test: Filter by extension.
    """
    print("=" * 70)
    print("TEST: Filter By Extension")
    print("=" * 70)
    
    config = RecentFilesConfig(persist_to_disk=False)
    engine = RecentFilesEngine(config)
    engine.add_file("/path/to/file.txt")
    engine.add_file("/path/to/document.txt")
    engine.add_file("/path/to/image.png")
    
    result = engine.filter_by_extension("txt")
    
    assert result.success, "Filtreleme başarılı olmalı"
    assert result.count == 2, "2 txt dosyası olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Count: {result.count}")
    
    print("\n" + "=" * 70)
    print("PASS: Filter by extension")
    print("=" * 70)


def test_filter_by_project():
    """
    Test: Filter by project.
    """
    print("=" * 70)
    print("TEST: Filter By Project")
    print("=" * 70)
    
    engine = RecentFilesEngine()
    engine.add_file("/path/to/file1.txt", project="project1")
    engine.add_file("/path/to/file2.txt", project="project1")
    engine.add_file("/path/to/file3.txt", project="project2")
    
    result = engine.filter_by_project("project1")
    
    assert result.success, "Filtreleme başarılı olmalı"
    assert result.count == 2, "2 proje1 dosyası olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Count: {result.count}")
    
    print("\n" + "=" * 70)
    print("PASS: Filter by project")
    print("=" * 70)


def test_get_pinned_files():
    """
    Test: Get pinned files.
    """
    print("=" * 70)
    print("TEST: Get Pinned Files")
    print("=" * 70)
    
    engine = RecentFilesEngine()
    engine.add_file("/path/to/file1.txt")
    engine.add_file("/path/to/file2.txt")
    engine.pin_file("/path/to/file1.txt")
    
    result = engine.get_pinned_files()
    
    assert result.success, "Alma başarılı olmalı"
    assert result.count == 1, "1 sabitlenmiş dosya olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Count: {result.count}")
    
    print("\n" + "=" * 70)
    print("PASS: Get pinned files")
    print("=" * 70)


def test_clear_recent_files():
    """
    Test: Clear recent files.
    """
    print("=" * 70)
    print("TEST: Clear Recent Files")
    print("=" * 70)
    
    engine = RecentFilesEngine()
    engine.add_file("/path/to/file.txt")
    
    result = engine.clear_recent_files()
    
    assert result.success, "Temizleme başarılı olmalı"
    assert result.count == 0, "0 dosya olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear recent files")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    engine = RecentFilesEngine()
    
    new_config = RecentFilesConfig(max_files=100, sort_mode=SortMode.FREQUENCY)
    result = engine.update_config(new_config)
    
    assert result.success, "Güncelleme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    
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
    
    engine = RecentFilesEngine()
    
    config = engine.get_config()
    
    assert config is not None, "Config olmalı"
    assert config.max_files == 50, "Config eşleşmeli"
    
    print(f"  Max files: {config.max_files}")
    print(f"  Sort mode: {config.sort_mode.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


def test_sort_mode_enum():
    """
    Test: SortMode enum.
    """
    print("=" * 70)
    print("TEST: SortMode Enum")
    print("=" * 70)
    
    assert SortMode.DATE_DESC.value == "date_desc"
    assert SortMode.DATE_ASC.value == "date_asc"
    assert SortMode.NAME_ASC.value == "name_asc"
    assert SortMode.FREQUENCY.value == "frequency"
    
    print(f"  All enum values verified")
    print(f"  Total modes: {len(SortMode)}")
    
    print("\n" + "=" * 70)
    print("PASS: SortMode enum")
    print("=" * 70)


def test_filter_mode_enum():
    """
    Test: FilterMode enum.
    """
    print("=" * 70)
    print("TEST: FilterMode Enum")
    print("=" * 70)
    
    assert FilterMode.ALL.value == "all"
    assert FilterMode.PINNED.value == "pinned"
    assert FilterMode.UNPINNED.value == "unpinned"
    assert FilterMode.BY_EXTENSION.value == "by_extension"
    
    print(f"  All enum values verified")
    print(f"  Total modes: {len(FilterMode)}")
    
    print("\n" + "=" * 70)
    print("PASS: FilterMode enum")
    print("=" * 70)


def test_recent_file_dataclass():
    """
    Test: RecentFile dataclass.
    """
    print("=" * 70)
    print("TEST: RecentFile Dataclass")
    print("=" * 70)
    
    file = RecentFile(
        path="/test/file.txt",
        opened_at="2023-01-01T00:00:00",
        last_accessed="2023-01-01T00:00:00",
        access_count=5,
        pinned=True,
        project="test_project"
    )
    
    assert file.path == "/test/file.txt", "Path eşleşmeli"
    assert file.access_count == 5, "Access count eşleşmeli"
    assert file.pinned == True, "Pinned eşleşmeli"
    
    print(f"  Path: {file.path}")
    print(f"  Access count: {file.access_count}")
    print(f"  Pinned: {file.pinned}")
    
    print("\n" + "=" * 70)
    print("PASS: RecentFile dataclass")
    print("=" * 70)


def test_recent_files_config_dataclass():
    """
    Test: RecentFilesConfig dataclass.
    """
    print("=" * 70)
    print("TEST: RecentFilesConfig Dataclass")
    print("=" * 70)
    
    config = RecentFilesConfig(
        max_files=100,
        max_pinned=20,
        sort_mode=SortMode.FREQUENCY
    )
    
    assert config.max_files == 100, "Max files eşleşmeli"
    assert config.max_pinned == 20, "Max pinned eşleşmeli"
    assert config.sort_mode == SortMode.FREQUENCY, "Sort mode eşleşmeli"
    
    print(f"  Max files: {config.max_files}")
    print(f"  Max pinned: {config.max_pinned}")
    print(f"  Sort mode: {config.sort_mode.value}")
    
    print("\n" + "=" * 70)
    print("PASS: RecentFilesConfig dataclass")
    print("=" * 70)


def test_recent_files_result_dataclass():
    """
    Test: RecentFilesResult dataclass.
    """
    print("=" * 70)
    print("TEST: RecentFilesResult Dataclass")
    print("=" * 70)
    
    result = RecentFilesResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: RecentFilesResult dataclass")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_add_file()
        test2 = test_remove_file()
        test3 = test_pin_file()
        test4 = test_unpin_file()
        test5 = test_get_recent_files()
        test6 = test_search_files()
        test7 = test_filter_by_extension()
        test8 = test_filter_by_project()
        test9 = test_get_pinned_files()
        test10 = test_clear_recent_files()
        test11 = test_update_config()
        test12 = test_get_config()
        test13 = test_sort_mode_enum()
        test14 = test_filter_mode_enum()
        test15 = test_recent_file_dataclass()
        test16 = test_recent_files_config_dataclass()
        test17 = test_recent_files_result_dataclass()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Add File: {'PASS' if test1 else 'FAIL'}")
        print(f"Remove File: {'PASS' if test2 else 'FAIL'}")
        print(f"Pin File: {'PASS' if test3 else 'FAIL'}")
        print(f"Unpin File: {'PASS' if test4 else 'FAIL'}")
        print(f"Get Recent Files: {'PASS' if test5 else 'FAIL'}")
        print(f"Search Files: {'PASS' if test6 else 'FAIL'}")
        print(f"Filter By Extension: {'PASS' if test7 else 'FAIL'}")
        print(f"Filter By Project: {'PASS' if test8 else 'FAIL'}")
        print(f"Get Pinned Files: {'PASS' if test9 else 'FAIL'}")
        print(f"Clear Recent Files: {'PASS' if test10 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test11 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test12 else 'FAIL'}")
        print(f"SortMode Enum: {'PASS' if test13 else 'FAIL'}")
        print(f"FilterMode Enum: {'PASS' if test14 else 'FAIL'}")
        print(f"RecentFile Dataclass: {'PASS' if test15 else 'FAIL'}")
        print(f"RecentFilesConfig Dataclass: {'PASS' if test16 else 'FAIL'}")
        print(f"RecentFilesResult Dataclass: {'PASS' if test17 else 'FAIL'}")
        
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
