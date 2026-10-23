"""
Quality Test: Global Search
Global search system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.global_search import (
    GlobalSearchEngine,
    SearchScope,
    SearchMode,
    SearchAction,
    SearchContext,
    SearchResult,
    GlobalSearchConfig,
    GlobalSearchResult
)


def test_search():
    """
    Test: Search.
    """
    print("=" * 70)
    print("TEST: Search")
    print("=" * 70)
    
    engine = GlobalSearchEngine()
    
    files = {
        "test.py": "print('hello')\nprint('world')",
        "test2.py": "print('test')"
    }
    
    result = engine.search("print", files)
    
    assert result.success, "Arama başarılı olmalı"
    assert result.total_matches > 0, "Eşleşme bulunmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Total matches: {result.total_matches}")
    print(f"  Files searched: {result.files_searched}")
    
    print("\n" + "=" * 70)
    print("PASS: Search")
    print("=" * 70)


def test_replace():
    """
    Test: Replace.
    """
    print("=" * 70)
    print("TEST: Replace")
    print("=" * 70)
    
    engine = GlobalSearchEngine()
    
    files = {
        "test.py": "print('hello')\nprint('world')"
    }
    
    result = engine.replace("print", "console.log", files)
    
    assert result.success, "Değiştirme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Total replacements: {result.total_matches}")
    
    print("\n" + "=" * 70)
    print("PASS: Replace")
    print("=" * 70)


def test_filter_results():
    """
    Test: Filter results.
    """
    print("=" * 70)
    print("TEST: Filter Results")
    print("=" * 70)
    
    engine = GlobalSearchEngine()
    
    files = {
        "test.py": "print('hello')\nprint('world')",
        "test2.py": "print('test')"
    }
    
    engine.search("print", files)
    
    filtered = engine.filter_results("test.py")
    
    assert len(filtered) > 0, "Filtrelenmiş sonuçlar olmalı"
    
    print(f"  Filtered results: {len(filtered)}")
    
    print("\n" + "=" * 70)
    print("PASS: Filter results")
    print("=" * 70)


def test_get_result_count():
    """
    Test: Get result count.
    """
    print("=" * 70)
    print("TEST: Get Result Count")
    print("=" * 70)
    
    engine = GlobalSearchEngine()
    
    files = {
        "test.py": "print('hello')\nprint('world')"
    }
    
    engine.search("print", files)
    
    count = engine.get_result_count()
    
    assert count > 0, "Sonuç sayısı 0'dan büyük olmalı"
    
    print(f"  Result count: {count}")
    
    print("\n" + "=" * 70)
    print("PASS: Get result count")
    print("=" * 70)


def test_clear_results():
    """
    Test: Clear results.
    """
    print("=" * 70)
    print("TEST: Clear Results")
    print("=" * 70)
    
    engine = GlobalSearchEngine()
    
    files = {
        "test.py": "print('hello')"
    }
    
    engine.search("print", files)
    result = engine.clear_results()
    
    assert result.success, "Temizleme başarılı olmalı"
    assert engine.get_result_count() == 0, "Sonuçlar temizlenmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Result count: {engine.get_result_count()}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear results")
    print("=" * 70)


def test_get_search_history():
    """
    Test: Get search history.
    """
    print("=" * 70)
    print("TEST: Get Search History")
    print("=" * 70)
    
    engine = GlobalSearchEngine()
    
    files = {
        "test.py": "print('hello')"
    }
    
    engine.search("print", files)
    engine.search("hello", files)
    
    history = engine.get_search_history()
    
    assert len(history) > 0, "Geçmiş olmalı"
    
    print(f"  History: {history}")
    
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
    
    engine = GlobalSearchEngine()
    
    files = {
        "test.py": "print('hello')"
    }
    
    engine.search("print", files)
    result = engine.clear_history()
    
    assert result.success, "Temizleme başarılı olmalı"
    assert len(engine.get_search_history()) == 0, "Geçmiş temizlenmeli"
    
    print(f"  Success: {result.success}")
    print(f"  History: {len(engine.get_search_history())}")
    
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
    
    engine = GlobalSearchEngine()
    
    new_config = GlobalSearchConfig(scope=SearchScope.WORKSPACE)
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
    
    engine = GlobalSearchEngine()
    
    config = engine.get_config()
    
    assert config is not None, "Config olmalı"
    assert config.scope == SearchScope.PROJECT, "Config eşleşmeli"
    
    print(f"  Scope: {config.scope.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


def test_search_scope_enum():
    """
    Test: SearchScope enum.
    """
    print("=" * 70)
    print("TEST: SearchScope Enum")
    print("=" * 70)
    
    assert SearchScope.CURRENT_FILE.value == "current_file"
    assert SearchScope.OPEN_FILES.value == "open_files"
    assert SearchScope.PROJECT.value == "project"
    assert SearchScope.WORKSPACE.value == "workspace"
    
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
    
    assert SearchMode.PLAIN_TEXT.value == "plain_text"
    assert SearchMode.REGEX.value == "regex"
    assert SearchMode.CASE_SENSITIVE.value == "case_sensitive"
    assert SearchMode.CASE_INSENSITIVE.value == "case_insensitive"
    assert SearchMode.WHOLE_WORD.value == "whole_word"
    assert SearchMode.FUZZY.value == "fuzzy"
    
    print(f"  All enum values verified")
    print(f"  Total modes: {len(SearchMode)}")
    
    print("\n" + "=" * 70)
    print("PASS: SearchMode enum")
    print("=" * 70)


def test_search_context_enum():
    """
    Test: SearchContext enum.
    """
    print("=" * 70)
    print("TEST: SearchContext Enum")
    print("=" * 70)
    
    assert SearchContext.CODE.value == "code"
    assert SearchContext.COMMENTS.value == "comments"
    assert SearchContext.STRINGS.value == "strings"
    assert SearchContext.ALL.value == "all"
    
    print(f"  All enum values verified")
    print(f"  Total contexts: {len(SearchContext)}")
    
    print("\n" + "=" * 70)
    print("PASS: SearchContext enum")
    print("=" * 70)


def test_search_result_dataclass():
    """
    Test: SearchResult dataclass.
    """
    print("=" * 70)
    print("TEST: SearchResult Dataclass")
    print("=" * 70)
    
    result = SearchResult(
        file_path="test.py",
        line_number=5,
        column=10,
        match_text="print"
    )
    
    assert result.file_path == "test.py", "File path eşleşmeli"
    assert result.line_number == 5, "Line number eşleşmeli"
    assert result.column == 10, "Column eşleşmeli"
    
    print(f"  File path: {result.file_path}")
    print(f"  Line number: {result.line_number}")
    print(f"  Column: {result.column}")
    
    print("\n" + "=" * 70)
    print("PASS: SearchResult dataclass")
    print("=" * 70)


def test_global_search_config_dataclass():
    """
    Test: GlobalSearchConfig dataclass.
    """
    print("=" * 70)
    print("TEST: GlobalSearchConfig Dataclass")
    print("=" * 70)
    
    config = GlobalSearchConfig(
        scope=SearchScope.PROJECT,
        mode=SearchMode.PLAIN_TEXT,
        max_results=100
    )
    
    assert config.scope == SearchScope.PROJECT, "Scope eşleşmeli"
    assert config.mode == SearchMode.PLAIN_TEXT, "Mode eşleşmeli"
    assert config.max_results == 100, "Max results eşleşmeli"
    
    print(f"  Scope: {config.scope.value}")
    print(f"  Mode: {config.mode.value}")
    print(f"  Max results: {config.max_results}")
    
    print("\n" + "=" * 70)
    print("PASS: GlobalSearchConfig dataclass")
    print("=" * 70)


def test_global_search_result_dataclass():
    """
    Test: GlobalSearchResult dataclass.
    """
    print("=" * 70)
    print("TEST: GlobalSearchResult Dataclass")
    print("=" * 70)
    
    result = GlobalSearchResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.results, list), "Results list olmalı"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Results: {len(result.results)}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: GlobalSearchResult dataclass")
    print("=" * 70)


def test_search_with_empty_query():
    """
    Test: Search with empty query.
    """
    print("=" * 70)
    print("TEST: Search With Empty Query")
    print("=" * 70)
    
    engine = GlobalSearchEngine()
    
    files = {
        "test.py": "print('hello')"
    }
    
    result = engine.search("", files)
    
    assert result.success == False, "Başarısız olmalı"
    assert len(result.errors) > 0, "Hata olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Errors: {result.errors}")
    
    print("\n" + "=" * 70)
    print("PASS: Search with empty query")
    print("=" * 70)


def test_search_with_no_files():
    """
    Test: Search with no files.
    """
    print("=" * 70)
    print("TEST: Search With No Files")
    print("=" * 70)
    
    engine = GlobalSearchEngine()
    
    result = engine.search("print", None)
    
    assert result.success == False, "Başarısız olmalı"
    assert len(result.errors) > 0, "Hata olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Errors: {result.errors}")
    
    print("\n" + "=" * 70)
    print("PASS: Search with no files")
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
    assert SearchAction.FILTER.value == "filter"
    assert SearchAction.CLEAR.value == "clear"
    
    print(f"  All enum values verified")
    print(f"  Total actions: {len(SearchAction)}")
    
    print("\n" + "=" * 70)
    print("PASS: SearchAction enum")
    print("=" * 70)


def test_find_next():
    """
    Test: Find next.
    """
    print("=" * 70)
    print("TEST: Find Next")
    print("=" * 70)
    
    engine = GlobalSearchEngine()
    
    files = {
        "test.py": "print('hello')\nprint('world')",
        "test2.py": "print('test')"
    }
    
    engine.search("print", files)
    
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
    
    engine = GlobalSearchEngine()
    
    files = {
        "test.py": "print('hello')\nprint('world')",
        "test2.py": "print('test')"
    }
    
    engine.search("print", files)
    
    result = engine.find_previous()
    
    assert result.success, "Find previous başarılı olmalı"
    assert result.action == SearchAction.FIND_PREVIOUS.value, "Action eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Find previous")
    print("=" * 70)


def test_get_statistics():
    """
    Test: Get statistics.
    """
    print("=" * 70)
    print("TEST: Get Statistics")
    print("=" * 70)
    
    engine = GlobalSearchEngine()
    
    files = {
        "test.py": "print('hello')\nprint('world')"
    }
    
    engine.search("print", files)
    
    stats = engine.get_statistics()
    
    assert stats is not None, "İstatistikler olmalı"
    assert "total_matches" in stats, "Total matches olmalı"
    assert "current_index" in stats, "Current index olmalı"
    
    print(f"  Total matches: {stats['total_matches']}")
    print(f"  Current index: {stats['current_index']}")
    print(f"  Search history count: {stats['search_history_count']}")
    
    print("\n" + "=" * 70)
    print("PASS: Get statistics")
    print("=" * 70)


def test_set_file_filters():
    """
    Test: Set file filters.
    """
    print("=" * 70)
    print("TEST: Set File Filters")
    print("=" * 70)
    
    engine = GlobalSearchEngine()
    
    result = engine.set_file_filters(["test.py"])
    
    assert result.success, "Filtreleme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set file filters")
    print("=" * 70)


def test_set_extension_filters():
    """
    Test: Set extension filters.
    """
    print("=" * 70)
    print("TEST: Set Extension Filters")
    print("=" * 70)
    
    engine = GlobalSearchEngine()
    
    result = engine.set_extension_filters([".py"])
    
    assert result.success, "Filtreleme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set extension filters")
    print("=" * 70)


def test_set_directory_filters():
    """
    Test: Set directory filters.
    """
    print("=" * 70)
    print("TEST: Set Directory Filters")
    print("=" * 70)
    
    engine = GlobalSearchEngine()
    
    result = engine.set_directory_filters(["src"])
    
    assert result.success, "Filtreleme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set directory filters")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_search()
        test2 = test_replace()
        test3 = test_filter_results()
        test4 = test_get_result_count()
        test5 = test_clear_results()
        test6 = test_get_search_history()
        test7 = test_clear_history()
        test8 = test_update_config()
        test9 = test_get_config()
        test10 = test_search_scope_enum()
        test11 = test_search_mode_enum()
        test12 = test_search_context_enum()
        test13 = test_search_result_dataclass()
        test14 = test_global_search_config_dataclass()
        test15 = test_global_search_result_dataclass()
        test16 = test_search_with_empty_query()
        test17 = test_search_with_no_files()
        test18 = test_search_action_enum()
        test19 = test_find_next()
        test20 = test_find_previous()
        test21 = test_get_statistics()
        test22 = test_set_file_filters()
        test23 = test_set_extension_filters()
        test24 = test_set_directory_filters()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Search: {'PASS' if test1 else 'FAIL'}")
        print(f"Replace: {'PASS' if test2 else 'FAIL'}")
        print(f"Filter Results: {'PASS' if test3 else 'FAIL'}")
        print(f"Get Result Count: {'PASS' if test4 else 'FAIL'}")
        print(f"Clear Results: {'PASS' if test5 else 'FAIL'}")
        print(f"Get Search History: {'PASS' if test6 else 'FAIL'}")
        print(f"Clear History: {'PASS' if test7 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test8 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test9 else 'FAIL'}")
        print(f"SearchScope Enum: {'PASS' if test10 else 'FAIL'}")
        print(f"SearchMode Enum: {'PASS' if test11 else 'FAIL'}")
        print(f"SearchContext Enum: {'PASS' if test12 else 'FAIL'}")
        print(f"SearchResult Dataclass: {'PASS' if test13 else 'FAIL'}")
        print(f"GlobalSearchConfig Dataclass: {'PASS' if test14 else 'FAIL'}")
        print(f"GlobalSearchResult Dataclass: {'PASS' if test15 else 'FAIL'}")
        print(f"Search With Empty Query: {'PASS' if test16 else 'FAIL'}")
        print(f"Search With No Files: {'PASS' if test17 else 'FAIL'}")
        print(f"SearchAction Enum: {'PASS' if test18 else 'FAIL'}")
        print(f"Find Next: {'PASS' if test19 else 'FAIL'}")
        print(f"Find Previous: {'PASS' if test20 else 'FAIL'}")
        print(f"Get Statistics: {'PASS' if test21 else 'FAIL'}")
        print(f"Set File Filters: {'PASS' if test22 else 'FAIL'}")
        print(f"Set Extension Filters: {'PASS' if test23 else 'FAIL'}")
        print(f"Set Directory Filters: {'PASS' if test24 else 'FAIL'}")
        
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
