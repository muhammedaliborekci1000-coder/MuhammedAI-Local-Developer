"""
Quality Test: File Search
File search system testleri.
"""

import sys
import os
import tempfile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.file_search import (
    FileSearchEngine,
    SearchScope,
    SearchMode,
    SearchAction,
    FileMatch,
    FileSearchConfig,
    FileSearchResult
)


def test_search_by_filename():
    """
    Test: Search by filename.
    """
    print("=" * 70)
    print("TEST: Search by Filename")
    print("=" * 70)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Test dosyaları oluştur
        with open(os.path.join(tmpdir, "main.py"), "w") as f:
            f.write("def main():\n    pass")
        with open(os.path.join(tmpdir, "utils.py"), "w") as f:
            f.write("def helper():\n    pass")
        
        engine = FileSearchEngine(tmpdir)
        result = engine.search_files("main", SearchScope.FILE_NAME)
        
        assert result.success, "Search başarılı olmalı"
        assert result.total_files > 0, "Dosya bulunmalı"
        
        print(f"  Success: {result.success}")
        print(f"  Total files: {result.total_files}")
        print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Search by filename")
    print("=" * 70)


def test_search_by_content():
    """
    Test: Search by content.
    """
    print("=" * 70)
    print("TEST: Search by Content")
    print("=" * 70)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Test dosyası oluştur
        with open(os.path.join(tmpdir, "main.py"), "w") as f:
            f.write("def main():\n    pass")
        
        engine = FileSearchEngine(tmpdir)
        result = engine.search_files("def main", SearchScope.FILE_CONTENT)
        
        assert result.success, "Search başarılı olmalı"
        
        print(f"  Success: {result.success}")
        print(f"  Total files: {result.total_files}")
    
    print("\n" + "=" * 70)
    print("PASS: Search by content")
    print("=" * 70)


def test_search_both():
    """
    Test: Search both filename and content.
    """
    print("=" * 70)
    print("TEST: Search Both")
    print("=" * 70)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Test dosyaları oluştur
        with open(os.path.join(tmpdir, "main.py"), "w") as f:
            f.write("def main():\n    pass")
        
        engine = FileSearchEngine(tmpdir)
        result = engine.search_files("main", SearchScope.BOTH)
        
        assert result.success, "Search başarılı olmalı"
        
        print(f"  Success: {result.success}")
        print(f"  Total files: {result.total_files}")
    
    print("\n" + "=" * 70)
    print("PASS: Search both")
    print("=" * 70)


def test_case_sensitive_search():
    """
    Test: Case-sensitive search.
    """
    print("=" * 70)
    print("TEST: Case-Sensitive Search")
    print("=" * 70)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Test dosyası oluştur
        with open(os.path.join(tmpdir, "Main.py"), "w") as f:
            f.write("def main():\n    pass")
        
        engine = FileSearchEngine(tmpdir)
        result = engine.search_files("Main", SearchScope.FILE_NAME, SearchMode.CASE_SENSITIVE)
        
        assert result.success, "Search başarılı olmalı"
        
        print(f"  Success: {result.success}")
        print(f"  Total files: {result.total_files}")
    
    print("\n" + "=" * 70)
    print("PASS: Case-sensitive search")
    print("=" * 70)


def test_regex_search():
    """
    Test: Regex search.
    """
    print("=" * 70)
    print("TEST: Regex Search")
    print("=" * 70)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Test dosyaları oluştur
        with open(os.path.join(tmpdir, "main.py"), "w") as f:
            f.write("def main():\n    pass")
        with open(os.path.join(tmpdir, "test.py"), "w") as f:
            f.write("def test():\n    pass")
        
        engine = FileSearchEngine(tmpdir)
        result = engine.search_files(r"main|test", SearchScope.FILE_NAME, SearchMode.REGEX)
        
        assert result.success, "Search başarılı olmalı"
        
        print(f"  Success: {result.success}")
        print(f"  Total files: {result.total_files}")
    
    print("\n" + "=" * 70)
    print("PASS: Regex search")
    print("=" * 70)


def test_extension_filtering():
    """
    Test: Extension filtering.
    """
    print("=" * 70)
    print("TEST: Extension Filtering")
    print("=" * 70)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Test dosyaları oluştur
        with open(os.path.join(tmpdir, "main.py"), "w") as f:
            f.write("def main():\n    pass")
        with open(os.path.join(tmpdir, "README.md"), "w") as f:
            f.write("# README")
        
        engine = FileSearchEngine(tmpdir)
        result = engine.search_files("", SearchScope.FILE_NAME, extensions=[".py"])
        
        assert result.success, "Search başarılı olmalı"
        
        print(f"  Success: {result.success}")
        print(f"  Total files: {result.total_files}")
        print(f"  File names: {[m.file_name for m in result.matches]}")
    
    print("\n" + "=" * 70)
    print("PASS: Extension filtering")
    print("=" * 70)


def test_exclude_dirs():
    """
    Test: Exclude directories.
    """
    print("=" * 70)
    print("TEST: Exclude Directories")
    print("=" * 70)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Test dosyaları oluştur
        os.makedirs(os.path.join(tmpdir, ".git"))
        with open(os.path.join(tmpdir, ".git", "config"), "w") as f:
            f.write("[core]")
        
        with open(os.path.join(tmpdir, "main.py"), "w") as f:
            f.write("def main():\n    pass")
        
        engine = FileSearchEngine(tmpdir)
        result = engine.search_files("", SearchScope.FILE_NAME)
        
        assert result.success, "Search başarılı olmalı"
        
        print(f"  Success: {result.success}")
        print(f"  Total files: {result.total_files}")
        print(f"  File names: {[m.file_name for m in result.matches]}")
    
    print("\n" + "=" * 70)
    print("PASS: Exclude directories")
    print("=" * 70)


def test_search_by_extension():
    """
    Test: Search by extension.
    """
    print("=" * 70)
    print("TEST: Search by Extension")
    print("=" * 70)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Test dosyaları oluştur
        with open(os.path.join(tmpdir, "main.py"), "w") as f:
            f.write("def main():\n    pass")
        with open(os.path.join(tmpdir, "README.md"), "w") as f:
            f.write("# README")
        
        engine = FileSearchEngine(tmpdir)
        result = engine.search_by_extension([".py"])
        
        assert result.success, "Search başarılı olmalı"
        
        print(f"  Success: {result.success}")
        print(f"  Total files: {result.total_files}")
        print(f"  File names: {[m.file_name for m in result.matches]}")
    
    print("\n" + "=" * 70)
    print("PASS: Search by extension")
    print("=" * 70)


def test_search_scope_enum():
    """
    Test: SearchScope enum.
    """
    print("=" * 70)
    print("TEST: SearchScope Enum")
    print("=" * 70)
    
    assert SearchScope.FILE_NAME.value == "file_name"
    assert SearchScope.FILE_CONTENT.value == "file_content"
    assert SearchScope.BOTH.value == "both"
    
    print(f"  All enum values verified")
    print(f"  Total scopes: {len(SearchScope)}")
    
    print("\n" + "=" * 70)
    print("PASS: SearchScope enum")
    print("=" * 70)


def test_search_mode_enum():
    """
    Test: SearchMode enum.
    """
    print("=" * 70)
    print("TEST: SearchMode Enum")
    print("=" * 70)
    
    assert SearchMode.NORMAL.value == "normal"
    assert SearchMode.CASE_SENSITIVE.value == "case_sensitive"
    assert SearchMode.CASE_INSENSITIVE.value == "case_insensitive"
    assert SearchMode.REGEX.value == "regex"
    
    print(f"  All enum values verified")
    print(f"  Total modes: {len(SearchMode)}")
    
    print("\n" + "=" * 70)
    print("PASS: SearchMode enum")
    print("=" * 70)


def test_file_match_dataclass():
    """
    Test: FileMatch dataclass.
    """
    print("=" * 70)
    print("TEST: FileMatch Dataclass")
    print("=" * 70)
    
    match = FileMatch(
        file_path="/path/to/file.py",
        file_name="file.py",
        directory="/path/to",
        size=1024,
        modified_time=None
    )
    
    assert match.file_path == "/path/to/file.py", "File path eşleşmeli"
    assert match.file_name == "file.py", "File name eşleşmeli"
    
    print(f"  File path: {match.file_path}")
    print(f"  File name: {match.file_name}")
    print(f"  Size: {match.size}")
    
    print("\n" + "=" * 70)
    print("PASS: FileMatch dataclass")
    print("=" * 70)


def test_file_search_result_dataclass():
    """
    Test: FileSearchResult dataclass.
    """
    print("=" * 70)
    print("TEST: FileSearchResult Dataclass")
    print("=" * 70)
    
    result = FileSearchResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.matches, list), "Matches list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Matches: {len(result.matches)}")
    
    print("\n" + "=" * 70)
    print("PASS: FileSearchResult dataclass")
    print("=" * 70)


def test_whole_word_search():
    """
    Test: Whole word search.
    """
    print("=" * 70)
    print("TEST: Whole Word Search")
    print("=" * 70)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Test dosyası oluştur
        with open(os.path.join(tmpdir, "test.py"), "w") as f:
            f.write("def main():\n    pass\n    main()")
        
        engine = FileSearchEngine(tmpdir)
        result = engine.search_files("main", SearchScope.FILE_CONTENT, SearchMode.WHOLE_WORD)
        
        assert result.success, "Search başarılı olmalı"
        
        print(f"  Success: {result.success}")
        print(f"  Total files: {result.total_files}")
    
    print("\n" + "=" * 70)
    print("PASS: Whole word search")
    print("=" * 70)


def test_fuzzy_search():
    """
    Test: Fuzzy search.
    """
    print("=" * 70)
    print("TEST: Fuzzy Search")
    print("=" * 70)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Test dosyası oluştur
        with open(os.path.join(tmpdir, "test.py"), "w") as f:
            f.write("def main_function():\n    pass")
        
        engine = FileSearchEngine(tmpdir)
        result = engine.search_files("main", SearchScope.FILE_CONTENT, SearchMode.FUZZY)
        
        assert result.success, "Search başarılı olmalı"
        
        print(f"  Success: {result.success}")
        print(f"  Total files: {result.total_files}")
    
    print("\n" + "=" * 70)
    print("PASS: Fuzzy search")
    print("=" * 70)


def test_replace():
    """
    Test: Replace.
    """
    print("=" * 70)
    print("TEST: Replace")
    print("=" * 70)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Test dosyası oluştur
        test_file = os.path.join(tmpdir, "test.py")
        with open(test_file, "w") as f:
            f.write("def main():\n    pass")
        
        engine = FileSearchEngine(tmpdir)
        result = engine.replace("main", "test", test_file)
        
        assert result.success, "Replace başarılı olmalı"
        assert result.action == SearchAction.REPLACE.value, "Action eşleşmeli"
        
        print(f"  Success: {result.success}")
        print(f"  Total matches: {result.total_matches}")
    
    print("\n" + "=" * 70)
    print("PASS: Replace")
    print("=" * 70)


def test_find_next():
    """
    Test: Find next.
    """
    print("=" * 70)
    print("TEST: Find Next")
    print("=" * 70)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Test dosyaları oluştur
        with open(os.path.join(tmpdir, "main.py"), "w") as f:
            f.write("def main():\n    pass")
        
        engine = FileSearchEngine(tmpdir)
        engine.search_files("main", SearchScope.FILE_NAME)
        
        result = engine.find_next()
        
        assert result.success, "Find next başarılı olmalı"
        assert result.action == SearchAction.FIND_NEXT.value, "Action eşleşmeli"
        
        print(f"  Success: {result.success}")
        print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Find next")
    print("=" * 70)


def test_find_previous():
    """
    Test: Find previous.
    """
    print("=" * 70)
    print("TEST: Find Previous")
    print("=" * 70)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Test dosyaları oluştur
        with open(os.path.join(tmpdir, "main.py"), "w") as f:
            f.write("def main():\n    pass")
        
        engine = FileSearchEngine(tmpdir)
        engine.search_files("main", SearchScope.FILE_NAME)
        
        result = engine.find_previous()
        
        assert result.success, "Find previous başarılı olmalı"
        assert result.action == SearchAction.FIND_PREVIOUS.value, "Action eşleşmeli"
        
        print(f"  Success: {result.success}")
        print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Find previous")
    print("=" * 70)


def test_search_history():
    """
    Test: Search history.
    """
    print("=" * 70)
    print("TEST: Search History")
    print("=" * 70)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Test dosyası oluştur
        with open(os.path.join(tmpdir, "main.py"), "w") as f:
            f.write("def main():\n    pass")
        
        engine = FileSearchEngine(tmpdir)
        engine.search_files("main", SearchScope.FILE_NAME)
        
        history = engine.get_search_history()
        
        assert len(history) > 0, "Geçmiş olmalı"
        
        print(f"  History: {len(history)}")
    
    print("\n" + "=" * 70)
    print("PASS: Search history")
    print("=" * 70)


def test_clear_history():
    """
    Test: Clear history.
    """
    print("=" * 70)
    print("TEST: Clear History")
    print("=" * 70)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Test dosyası oluştur
        with open(os.path.join(tmpdir, "main.py"), "w") as f:
            f.write("def main():\n    pass")
        
        engine = FileSearchEngine(tmpdir)
        engine.search_files("main", SearchScope.FILE_NAME)
        
        result = engine.clear_history()
        
        assert result.success, "Temizleme başarılı olmalı"
        assert len(engine.get_search_history()) == 0, "Geçmiş temizlenmeli"
        
        print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear history")
    print("=" * 70)


def test_get_statistics():
    """
    Test: Get statistics.
    """
    print("=" * 70)
    print("TEST: Get Statistics")
    print("=" * 70)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Test dosyası oluştur
        with open(os.path.join(tmpdir, "main.py"), "w") as f:
            f.write("def main():\n    pass")
        
        engine = FileSearchEngine(tmpdir)
        engine.search_files("main", SearchScope.FILE_NAME)
        
        stats = engine.get_statistics()
        
        assert stats is not None, "İstatistikler olmalı"
        assert "total_matches" in stats, "Total matches olmalı"
        
        print(f"  Total matches: {stats['total_matches']}")
        print(f"  Current index: {stats['current_index']}")
    
    print("\n" + "=" * 70)
    print("PASS: Get statistics")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        engine = FileSearchEngine(tmpdir)
        
        new_config = FileSearchConfig(case_sensitive=True)
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
    
    with tempfile.TemporaryDirectory() as tmpdir:
        engine = FileSearchEngine(tmpdir)
        
        config = engine.get_config()
        
        assert config is not None, "Config olmalı"
        assert config.scope == SearchScope.FILE_NAME, "Scope eşleşmeli"
        
        print(f"  Scope: {config.scope.value}")
        print(f"  Mode: {config.mode.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


def test_search_action_enum():
    """
    Test: SearchAction enum.
    """
    print("=" * 70)
    print("TEST: SearchAction Enum")
    print("=" * 70)
    
    assert SearchAction.SEARCH.value == "search"
    assert SearchAction.REPLACE.value == "replace"
    assert SearchAction.REPLACE_ALL.value == "replace_all"
    assert SearchAction.FIND_NEXT.value == "find_next"
    assert SearchAction.FIND_PREVIOUS.value == "find_previous"
    
    print(f"  All enum values verified")
    print(f"  Total actions: {len(SearchAction)}")
    
    print("\n" + "=" * 70)
    print("PASS: SearchAction enum")
    print("=" * 70)


def test_file_search_config_dataclass():
    """
    Test: FileSearchConfig dataclass.
    """
    print("=" * 70)
    print("TEST: FileSearchConfig Dataclass")
    print("=" * 70)
    
    config = FileSearchConfig(
        scope=SearchScope.FILE_CONTENT,
        mode=SearchMode.REGEX
    )
    
    assert config.scope == SearchScope.FILE_CONTENT, "Scope eşleşmeli"
    assert config.mode == SearchMode.REGEX, "Mode eşleşmeli"
    
    print(f"  Scope: {config.scope.value}")
    print(f"  Mode: {config.mode.value}")
    print(f"  Include context: {config.include_context}")
    
    print("\n" + "=" * 70)
    print("PASS: FileSearchConfig dataclass")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_search_by_filename()
        test2 = test_search_by_content()
        test3 = test_search_both()
        test4 = test_case_sensitive_search()
        test5 = test_regex_search()
        test6 = test_extension_filtering()
        test7 = test_exclude_dirs()
        test8 = test_search_by_extension()
        test9 = test_search_scope_enum()
        test10 = test_search_mode_enum()
        test11 = test_file_match_dataclass()
        test12 = test_file_search_result_dataclass()
        test13 = test_whole_word_search()
        test14 = test_fuzzy_search()
        test15 = test_replace()
        test16 = test_find_next()
        test17 = test_find_previous()
        test18 = test_search_history()
        test19 = test_clear_history()
        test20 = test_get_statistics()
        test21 = test_update_config()
        test22 = test_get_config()
        test23 = test_search_action_enum()
        test24 = test_file_search_config_dataclass()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Search by Filename: {'PASS' if test1 else 'FAIL'}")
        print(f"Search by Content: {'PASS' if test2 else 'FAIL'}")
        print(f"Search Both: {'PASS' if test3 else 'FAIL'}")
        print(f"Case-Sensitive Search: {'PASS' if test4 else 'FAIL'}")
        print(f"Regex Search: {'PASS' if test5 else 'FAIL'}")
        print(f"Extension Filtering: {'PASS' if test6 else 'FAIL'}")
        print(f"Exclude Directories: {'PASS' if test7 else 'FAIL'}")
        print(f"Search by Extension: {'PASS' if test8 else 'FAIL'}")
        print(f"SearchScope Enum: {'PASS' if test9 else 'FAIL'}")
        print(f"SearchMode Enum: {'PASS' if test10 else 'FAIL'}")
        print(f"FileMatch Dataclass: {'PASS' if test11 else 'FAIL'}")
        print(f"FileSearchResult Dataclass: {'PASS' if test12 else 'FAIL'}")
        print(f"Whole Word Search: {'PASS' if test13 else 'FAIL'}")
        print(f"Fuzzy Search: {'PASS' if test14 else 'FAIL'}")
        print(f"Replace: {'PASS' if test15 else 'FAIL'}")
        print(f"Find Next: {'PASS' if test16 else 'FAIL'}")
        print(f"Find Previous: {'PASS' if test17 else 'FAIL'}")
        print(f"Search History: {'PASS' if test18 else 'FAIL'}")
        print(f"Clear History: {'PASS' if test19 else 'FAIL'}")
        print(f"Get Statistics: {'PASS' if test20 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test21 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test22 else 'FAIL'}")
        print(f"SearchAction Enum: {'PASS' if test23 else 'FAIL'}")
        print(f"FileSearchConfig Dataclass: {'PASS' if test24 else 'FAIL'}")
        
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
