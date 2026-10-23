"""
Quality Test: Terminal Search
Terminal search system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.tools.terminal_search import (
    TerminalSearchEngine,
    SearchMode,
    SearchScope,
    SearchOption,
    SearchConfig,
    SearchResult,
    SearchOutput
)


def test_search():
    """
    Test: Search.
    """
    print("=" * 70)
    print("TEST: Search")
    print("=" * 70)
    
    engine = TerminalSearchEngine()
    content = ["Line 1", "Line 2", "Test line", "Another test"]
    
    result = engine.search("test", content)
    
    assert result.success, "Arama başarılı olmalı"
    assert result.count == 2, "2 sonuç bulunmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Count: {result.count}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Search")
    print("=" * 70)


def test_search_with_panel():
    """
    Test: Search with panel.
    """
    print("=" * 70)
    print("TEST: Search With Panel")
    print("=" * 70)
    
    engine = TerminalSearchEngine()
    content = ["Line 1", "Test line"]
    
    result = engine.search("test", content, panel_id="panel_1")
    
    assert result.success, "Arama başarılı olmalı"
    assert result.results[0].panel_id == "panel_1", "Panel ID eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Panel ID: {result.results[0].panel_id}")
    
    print("\n" + "=" * 70)
    print("PASS: Search with panel")
    print("=" * 70)


def test_search_with_options():
    """
    Test: Search with options.
    """
    print("=" * 70)
    print("TEST: Search With Options")
    print("=" * 70)
    
    engine = TerminalSearchEngine()
    content = ["TEST line", "test line"]
    
    result = engine.search("test", content, options=[SearchOption.CASE_SENSITIVE])
    
    assert result.success, "Arama başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Count: {result.count}")
    
    print("\n" + "=" * 70)
    print("PASS: Search with options")
    print("=" * 70)


def test_search_regex():
    """
    Test: Search regex.
    """
    print("=" * 70)
    print("TEST: Search Regex")
    print("=" * 70)
    
    engine = TerminalSearchEngine()
    content = ["Line 1", "Line 2", "Test 123", "Test 456"]
    
    result = engine.search_regex(r"Test \d+", content)
    
    assert result.success, "Regex arama başarılı olmalı"
    assert result.count == 2, "2 sonuç bulunmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Count: {result.count}")
    
    print("\n" + "=" * 70)
    print("PASS: Search regex")
    print("=" * 70)


def test_search_whole_word():
    """
    Test: Search whole word.
    """
    print("=" * 70)
    print("TEST: Search Whole Word")
    print("=" * 70)
    
    engine = TerminalSearchEngine()
    content = ["test", "testing", "test case"]
    
    result = engine.search_whole_word("test", content)
    
    assert result.success, "Tam kelime arama başarılı olmalı"
    assert result.count >= 1, "En az 1 sonuç bulunmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Count: {result.count}")
    
    print("\n" + "=" * 70)
    print("PASS: Search whole word")
    print("=" * 70)


def test_navigate_next():
    """
    Test: Navigate next.
    """
    print("=" * 70)
    print("TEST: Navigate Next")
    print("=" * 70)
    
    engine = TerminalSearchEngine()
    
    result = engine.navigate_next(0)
    
    # This is a placeholder for navigation
    print(f"  Navigate next called")
    
    print("\n" + "=" * 70)
    print("PASS: Navigate next")
    print("=" * 70)


def test_navigate_previous():
    """
    Test: Navigate previous.
    """
    print("=" * 70)
    print("TEST: Navigate Previous")
    print("=" * 70)
    
    engine = TerminalSearchEngine()
    
    result = engine.navigate_previous(0)
    
    # This is a placeholder for navigation
    print(f"  Navigate previous called")
    
    print("\n" + "=" * 70)
    print("PASS: Navigate previous")
    print("=" * 70)


def test_get_search_history():
    """
    Test: Get search history.
    """
    print("=" * 70)
    print("TEST: Get Search History")
    print("=" * 70)
    
    engine = TerminalSearchEngine()
    content = ["Test line"]
    engine.search("test", content)
    
    history = engine.get_search_history()
    
    assert len(history) > 0, "Geçmiş olmalı"
    
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
    
    engine = TerminalSearchEngine()
    content = ["Test line"]
    engine.search("test", content)
    
    result = engine.clear_history()
    
    assert result.success, "Temizleme başarılı olmalı"
    assert len(engine.get_search_history()) == 0, "Geçmiş temizlenmeli"
    
    print(f"  Success: {result.success}")
    
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
    
    engine = TerminalSearchEngine()
    
    new_config = SearchConfig(case_sensitive=True)
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
    
    engine = TerminalSearchEngine()
    
    config = engine.get_config()
    
    assert config is not None, "Config olmalı"
    assert config.mode == SearchMode.TEXT, "Config eşleşmeli"
    
    print(f"  Mode: {config.mode.value}")
    print(f"  Scope: {config.scope.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


def test_search_mode_enum():
    """
    Test: SearchMode enum.
    """
    print("=" * 70)
    print("TEST: SearchMode Enum")
    print("=" * 70)
    
    assert SearchMode.TEXT.value == "text"
    assert SearchMode.REGEX.value == "regex"
    assert SearchMode.FUZZY.value == "fuzzy"
    
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
    
    assert SearchScope.CURRENT.value == "current"
    assert SearchScope.ALL.value == "all"
    assert SearchScope.HISTORY.value == "history"
    assert SearchScope.SCROLLBACK.value == "scrollback"
    
    print(f"  All enum values verified")
    print(f"  Total scopes: {len(SearchScope)}")
    
    print("\n" + "=" * 70)
    print("PASS: SearchScope enum")
    print("=" * 70)


def test_search_option_enum():
    """
    Test: SearchOption enum.
    """
    print("=" * 70)
    print("TEST: SearchOption Enum")
    print("=" * 70)
    
    assert SearchOption.CASE_SENSITIVE.value == "case_sensitive"
    assert SearchOption.CASE_INSENSITIVE.value == "case_insensitive"
    assert SearchOption.WHOLE_WORD.value == "whole_word"
    assert SearchOption.MATCH_WORD.value == "match_word"
    assert SearchOption.HIGHLIGHT.value == "highlight"
    
    print(f"  All enum values verified")
    print(f"  Total options: {len(SearchOption)}")
    
    print("\n" + "=" * 70)
    print("PASS: SearchOption enum")
    print("=" * 70)


def test_search_config_dataclass():
    """
    Test: SearchConfig dataclass.
    """
    print("=" * 70)
    print("TEST: SearchConfig Dataclass")
    print("=" * 70)
    
    config = SearchConfig(
        mode=SearchMode.REGEX,
        case_sensitive=True
    )
    
    assert config.mode == SearchMode.REGEX, "Mode eşleşmeli"
    assert config.case_sensitive == True, "Case sensitive eşleşmeli"
    
    print(f"  Mode: {config.mode.value}")
    print(f"  Case sensitive: {config.case_sensitive}")
    
    print("\n" + "=" * 70)
    print("PASS: SearchConfig dataclass")
    print("=" * 70)


def test_search_result_dataclass():
    """
    Test: SearchResult dataclass.
    """
    print("=" * 70)
    print("TEST: SearchResult Dataclass")
    print("=" * 70)
    
    result = SearchResult(
        id="search_1",
        content="Test line",
        line_number=1,
        start_index=0,
        end_index=4
    )
    
    assert result.id == "search_1", "ID eşleşmeli"
    assert result.content == "Test line", "İçerik eşleşmeli"
    assert result.line_number == 1, "Line number eşleşmeli"
    
    print(f"  ID: {result.id}")
    print(f"  Content: {result.content}")
    print(f"  Line number: {result.line_number}")
    
    print("\n" + "=" * 70)
    print("PASS: SearchResult dataclass")
    print("=" * 70)


def test_search_output_dataclass():
    """
    Test: SearchOutput dataclass.
    """
    print("=" * 70)
    print("TEST: SearchOutput Dataclass")
    print("=" * 70)
    
    output = SearchOutput(success=True)
    output.message = "Test message"
    
    assert output.success == True, "Success eşleşmeli"
    assert output.message == "Test message", "Message eşleşmeli"
    assert isinstance(output.errors, list), "Errors list olmalı"
    
    print(f"  Success: {output.success}")
    print(f"  Message: {output.message}")
    print(f"  Errors: {len(output.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: SearchOutput dataclass")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_search()
        test2 = test_search_with_panel()
        test3 = test_search_with_options()
        test4 = test_search_regex()
        test5 = test_search_whole_word()
        test6 = test_navigate_next()
        test7 = test_navigate_previous()
        test8 = test_get_search_history()
        test9 = test_clear_history()
        test10 = test_update_config()
        test11 = test_get_config()
        test12 = test_search_mode_enum()
        test13 = test_search_scope_enum()
        test14 = test_search_option_enum()
        test15 = test_search_config_dataclass()
        test16 = test_search_result_dataclass()
        test17 = test_search_output_dataclass()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Search: {'PASS' if test1 else 'FAIL'}")
        print(f"Search With Panel: {'PASS' if test2 else 'FAIL'}")
        print(f"Search With Options: {'PASS' if test3 else 'FAIL'}")
        print(f"Search Regex: {'PASS' if test4 else 'FAIL'}")
        print(f"Search Whole Word: {'PASS' if test5 else 'FAIL'}")
        print(f"Navigate Next: {'PASS' if test6 else 'FAIL'}")
        print(f"Navigate Previous: {'PASS' if test7 else 'FAIL'}")
        print(f"Get Search History: {'PASS' if test8 else 'FAIL'}")
        print(f"Clear History: {'PASS' if test9 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test10 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test11 else 'FAIL'}")
        print(f"SearchMode Enum: {'PASS' if test12 else 'FAIL'}")
        print(f"SearchScope Enum: {'PASS' if test13 else 'FAIL'}")
        print(f"SearchOption Enum: {'PASS' if test14 else 'FAIL'}")
        print(f"SearchConfig Dataclass: {'PASS' if test15 else 'FAIL'}")
        print(f"SearchResult Dataclass: {'PASS' if test16 else 'FAIL'}")
        print(f"SearchOutput Dataclass: {'PASS' if test17 else 'FAIL'}")
        
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
