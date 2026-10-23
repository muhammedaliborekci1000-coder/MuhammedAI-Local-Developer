"""
Quality Test: Search UI
Search UI system testleri.
"""

import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from app.editor.search_ui import (
    SearchMode,
    SearchScope,
    MatchCase,
    SearchResult,
    SearchQuery,
    SearchConfig,
    SearchUIResult,
    SearchUIManager
)


def test_search_mode_enum():
    """
    Test: SearchMode enum.
    """
    print("=" * 70)
    print("TEST: SearchMode Enum")
    print("=" * 70)
    
    assert SearchMode.FIND.value == "find"
    assert SearchMode.REPLACE.value == "replace"
    assert SearchMode.FIND_IN_FILES.value == "find_in_files"
    assert SearchMode.REPLACE_IN_FILES.value == "replace_in_files"
    
    print(f"  All enum values verified")
    print(f"  Total modes: {len(SearchMode)}")
    
    print("\n" + "=" * 70)
    print("PASS: SearchMode enum")
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
    assert SearchScope.SELECTION.value == "selection"
    
    print(f"  All enum values verified")
    print(f"  Total scopes: {len(SearchScope)}")
    
    print("\n" + "=" * 70)
    print("PASS: SearchScope enum")
    print("=" * 70)


def test_match_case_enum():
    """
    Test: MatchCase enum.
    """
    print("=" * 70)
    print("TEST: MatchCase Enum")
    print("=" * 70)
    
    assert MatchCase.SENSITIVE.value == "sensitive"
    assert MatchCase.INSENSITIVE.value == "insensitive"
    
    print(f"  All enum values verified")
    print(f"  Total cases: {len(MatchCase)}")
    
    print("\n" + "=" * 70)
    print("PASS: MatchCase enum")
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
        line_number=1,
        column=0,
        line_content="hello world",
        match_text="hello"
    )
    
    assert result.file_path == "test.py", "File path eşleşmeli"
    assert result.line_number == 1, "Line number eşleşmeli"
    assert result.match_text == "hello", "Match text eşleşmeli"
    
    print(f"  File: {result.file_path}")
    print(f"  Line: {result.line_number}")
    print(f"  Match: {result.match_text}")
    
    print("\n" + "=" * 70)
    print("PASS: SearchResult dataclass")
    print("=" * 70)


def test_search_query_dataclass():
    """
    Test: SearchQuery dataclass.
    """
    print("=" * 70)
    print("TEST: SearchQuery Dataclass")
    print("=" * 70)
    
    query = SearchQuery(
        search_text="hello",
        replace_text="world",
        mode=SearchMode.FIND,
        scope=SearchScope.CURRENT_FILE
    )
    
    assert query.search_text == "hello", "Search text eşleşmeli"
    assert query.replace_text == "world", "Replace text eşleşmeli"
    assert query.mode == SearchMode.FIND, "Mode eşleşmeli"
    
    print(f"  Search: {query.search_text}")
    print(f"  Replace: {query.replace_text}")
    print(f"  Mode: {query.mode.value}")
    
    print("\n" + "=" * 70)
    print("PASS: SearchQuery dataclass")
    print("=" * 70)


def test_search_config_dataclass():
    """
    Test: SearchConfig dataclass.
    """
    print("=" * 70)
    print("TEST: SearchConfig Dataclass")
    print("=" * 70)
    
    config = SearchConfig(
        max_results=100,
        show_context=True
    )
    
    assert config.max_results == 100, "Max results eşleşmeli"
    assert config.show_context == True, "Show context eşleşmeli"
    
    print(f"  Max results: {config.max_results}")
    print(f"  Show context: {config.show_context}")
    
    print("\n" + "=" * 70)
    print("PASS: SearchConfig dataclass")
    print("=" * 70)


def test_search_ui_result_dataclass():
    """
    Test: SearchUIResult dataclass.
    """
    print("=" * 70)
    print("TEST: SearchUIResult Dataclass")
    print("=" * 70)
    
    result = SearchUIResult(success=True)
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
    print("PASS: SearchUIResult dataclass")
    print("=" * 70)


def test_search_ui_manager_initialization():
    """
    Test: SearchUIManager initialization.
    """
    print("=" * 70)
    print("TEST: SearchUIManager Initialization")
    print("=" * 70)
    
    config = SearchConfig()
    manager = SearchUIManager(config)
    
    assert manager.config == config, "Config eşleşmeli"
    assert len(manager.search_history) == 0, "History boş olmalı"
    
    print(f"  History: {len(manager.search_history)}")
    
    print("\n" + "=" * 70)
    print("PASS: SearchUIManager initialization")
    print("=" * 70)


def test_search():
    """
    Test: Search.
    """
    print("=" * 70)
    print("TEST: Search")
    print("=" * 70)
    
    manager = SearchUIManager()
    
    query = SearchQuery(search_text="hello")
    content = "hello world\nhello there"
    
    result = manager.search(query, content, "test.py")
    
    assert result.success == True, "Search başarılı olmalı"
    assert result.total_matches > 0, "Matches bulunmalı"
    
    print(f"  Matches: {result.total_matches}")
    
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
    
    manager = SearchUIManager()
    
    query = SearchQuery(search_text="hello", replace_text="world")
    content = "hello world"
    
    result = manager.replace(query, content)
    
    assert result.success == True, "Replace başarılı olmalı"
    assert result.output is not None, "Output olmalı"
    
    print(f"  Replace result: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Replace")
    print("=" * 70)


def test_replace_all():
    """
    Test: Replace all.
    """
    print("=" * 70)
    print("TEST: Replace All")
    print("=" * 70)
    
    manager = SearchUIManager()
    
    query = SearchQuery(search_text="hello", replace_text="world")
    content = "hello world\nhello there"
    
    result = manager.replace_all(query, content)
    
    assert result.success == True, "Replace all başarılı olmalı"
    assert result.output is not None, "Output olmalı"
    
    print(f"  Replace all result: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Replace all")
    print("=" * 70)


def test_get_search_history():
    """
    Test: Get search history.
    """
    print("=" * 70)
    print("TEST: Get Search History")
    print("=" * 70)
    
    manager = SearchUIManager()
    
    query = SearchQuery(search_text="hello")
    manager.search(query, "hello world", "test.py")
    
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
    
    manager = SearchUIManager()
    
    query = SearchQuery(search_text="hello")
    manager.search(query, "hello world", "test.py")
    
    manager.clear_history()
    
    history = manager.get_search_history()
    
    assert len(history) == 0, "History temizlenmeli"
    
    print(f"  History cleared")
    
    print("\n" + "=" * 70)
    print("PASS: Clear history")
    print("=" * 70)


def test_get_current_results():
    """
    Test: Get current results.
    """
    print("=" * 70)
    print("TEST: Get Current Results")
    print("=" * 70)
    
    manager = SearchUIManager()
    
    query = SearchQuery(search_text="hello")
    manager.search(query, "hello world", "test.py")
    
    results = manager.get_current_results()
    
    assert len(results) > 0, "Results olmalı"
    
    print(f"  Results: {len(results)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get current results")
    print("=" * 70)


def test_navigate_to_result():
    """
    Test: Navigate to result.
    """
    print("=" * 70)
    print("TEST: Navigate to Result")
    print("=" * 70)
    
    manager = SearchUIManager()
    
    query = SearchQuery(search_text="hello")
    manager.search(query, "hello world", "test.py")
    
    result = manager.navigate_to_result(0)
    
    assert result is not None, "Result bulunmalı"
    
    print(f"  Navigated to: line {result.line_number}")
    
    print("\n" + "=" * 70)
    print("PASS: Navigate to result")
    print("=" * 70)


def test_get_result_count():
    """
    Test: Get result count.
    """
    print("=" * 70)
    print("TEST: Get Result Count")
    print("=" * 70)
    
    manager = SearchUIManager()
    
    query = SearchQuery(search_text="hello")
    manager.search(query, "hello world\nhello there", "test.py")
    
    count = manager.get_result_count()
    
    assert count > 0, "Count > 0 olmalı"
    
    print(f"  Count: {count}")
    
    print("\n" + "=" * 70)
    print("PASS: Get result count")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    manager = SearchUIManager()
    
    new_config = SearchConfig(max_results=50)
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
    
    config = SearchConfig(max_results=50)
    manager = SearchUIManager(config)
    
    retrieved_config = manager.get_config()
    
    assert retrieved_config.max_results == 50, "Config eşleşmeli"
    
    print(f"  Max results: {retrieved_config.max_results}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_search_mode_enum()
        test2 = test_search_scope_enum()
        test3 = test_match_case_enum()
        test4 = test_search_result_dataclass()
        test5 = test_search_query_dataclass()
        test6 = test_search_config_dataclass()
        test7 = test_search_ui_result_dataclass()
        test8 = test_search_ui_manager_initialization()
        test9 = test_search()
        test10 = test_replace()
        test11 = test_replace_all()
        test12 = test_get_search_history()
        test13 = test_clear_history()
        test14 = test_get_current_results()
        test15 = test_navigate_to_result()
        test16 = test_get_result_count()
        test17 = test_update_config()
        test18 = test_get_config()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"SearchMode Enum: {'PASS' if test1 else 'FAIL'}")
        print(f"SearchScope Enum: {'PASS' if test2 else 'FAIL'}")
        print(f"MatchCase Enum: {'PASS' if test3 else 'FAIL'}")
        print(f"SearchResult Dataclass: {'PASS' if test4 else 'FAIL'}")
        print(f"SearchQuery Dataclass: {'PASS' if test5 else 'FAIL'}")
        print(f"SearchConfig Dataclass: {'PASS' if test6 else 'FAIL'}")
        print(f"SearchUIResult Dataclass: {'PASS' if test7 else 'FAIL'}")
        print(f"SearchUIManager Initialization: {'PASS' if test8 else 'FAIL'}")
        print(f"Search: {'PASS' if test9 else 'FAIL'}")
        print(f"Replace: {'PASS' if test10 else 'FAIL'}")
        print(f"Replace All: {'PASS' if test11 else 'FAIL'}")
        print(f"Get Search History: {'PASS' if test12 else 'FAIL'}")
        print(f"Clear History: {'PASS' if test13 else 'FAIL'}")
        print(f"Get Current Results: {'PASS' if test14 else 'FAIL'}")
        print(f"Navigate to Result: {'PASS' if test15 else 'FAIL'}")
        print(f"Get Result Count: {'PASS' if test16 else 'FAIL'}")
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
