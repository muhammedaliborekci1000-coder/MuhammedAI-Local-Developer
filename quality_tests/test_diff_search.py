"""
Quality Test: Diff Search
Diff search system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.diff_search import (
    DiffSearchEngine,
    SearchMode,
    SearchScope,
    SearchDirection,
    SearchAction,
    SearchResult,
    ReplaceResult,
    SearchConfig,
    SearchEngineResult
)


def test_search():
    """
    Test: Search.
    """
    print("=" * 70)
    print("TEST: Search")
    print("=" * 70)
    
    engine = DiffSearchEngine()
    lines = ["Line 1 with test", "Line 2 with test", "Line 3"]
    engine.set_content(lines, "test.txt")
    
    result = engine.search("test")
    
    assert result.success, "Arama başarılı olmalı"
    assert result.action == SearchAction.SEARCH.value, "Action eşleşmeli"
    assert result.total_matches > 0, "Eşleşme olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Total matches: {result.total_matches}")
    print(f"  Message: {result.message}")
    
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
    
    engine = DiffSearchEngine()
    lines = ["Line 1 with test", "Line 2 with test", "Line 3"]
    engine.set_content(lines, "test.txt")
    
    result = engine.replace("test", "demo")
    
    assert result.success, "Değiştirme başarılı olmalı"
    assert result.action == SearchAction.REPLACE.value, "Action eşleşmeli"
    assert result.total_replaced > 0, "Değiştirme olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Total replaced: {result.total_replaced}")
    print(f"  Message: {result.message}")
    
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
    
    engine = DiffSearchEngine()
    lines = ["Line 1 with test", "Line 2 with test", "Line 3"]
    engine.set_content(lines, "test.txt")
    
    result = engine.replace_all("test", "demo")
    
    assert result.success, "Değiştirme başarılı olmalı"
    assert result.action == SearchAction.REPLACE_ALL.value, "Action eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Total replaced: {result.total_replaced}")
    
    print("\n" + "=" * 70)
    print("PASS: Replace all")
    print("=" * 70)


def test_find_next():
    """
    Test: Find next.
    """
    print("=" * 70)
    print("TEST: Find Next")
    print("=" * 70)
    
    engine = DiffSearchEngine()
    lines = ["Line 1 with test", "Line 2 with test", "Line 3"]
    engine.set_content(lines, "test.txt")
    engine.search("test")
    
    result = engine.find_next()
    
    assert result.success, "Bulma başarılı olmalı"
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
    
    engine = DiffSearchEngine()
    lines = ["Line 1 with test", "Line 2 with test", "Line 3"]
    engine.set_content(lines, "test.txt")
    engine.search("test")
    
    result = engine.find_previous()
    
    assert result.success, "Bulma başarılı olmalı"
    assert result.action == SearchAction.FIND_PREVIOUS.value, "Action eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Find previous")
    print("=" * 70)


def test_clear_results():
    """
    Test: Clear results.
    """
    print("=" * 70)
    print("TEST: Clear Results")
    print("=" * 70)
    
    engine = DiffSearchEngine()
    lines = ["Line 1 with test", "Line 2 with test", "Line 3"]
    engine.set_content(lines, "test.txt")
    engine.search("test")
    
    result = engine.clear_results()
    
    assert result.success, "Temizleme başarılı olmalı"
    assert len(engine.get_results()) == 0, "Sonuçlar temizlenmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear results")
    print("=" * 70)


def test_get_results():
    """
    Test: Get results.
    """
    print("=" * 70)
    print("TEST: Get Results")
    print("=" * 70)
    
    engine = DiffSearchEngine()
    lines = ["Line 1 with test", "Line 2 with test", "Line 3"]
    engine.set_content(lines, "test.txt")
    engine.search("test")
    
    results = engine.get_results()
    
    assert len(results) > 0, "Sonuçlar olmalı"
    
    print(f"  Results: {len(results)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get results")
    print("=" * 70)


def test_get_current_match():
    """
    Test: Get current match.
    """
    print("=" * 70)
    print("TEST: Get Current Match")
    print("=" * 70)
    
    engine = DiffSearchEngine()
    lines = ["Line 1 with test", "Line 2 with test", "Line 3"]
    engine.set_content(lines, "test.txt")
    engine.search("test")
    
    match = engine.get_current_match()
    
    assert match is not None, "Eşleşme bulunmalı"
    
    print(f"  Line number: {match.line_number}")
    print(f"  Matched text: {match.matched_text}")
    
    print("\n" + "=" * 70)
    print("PASS: Get current match")
    print("=" * 70)


def test_get_search_history():
    """
    Test: Get search history.
    """
    print("=" * 70)
    print("TEST: Get Search History")
    print("=" * 70)
    
    engine = DiffSearchEngine()
    lines = ["Line 1 with test", "Line 2 with test", "Line 3"]
    engine.set_content(lines, "test.txt")
    engine.search("test")
    
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
    
    engine = DiffSearchEngine()
    lines = ["Line 1 with test", "Line 2 with test", "Line 3"]
    engine.set_content(lines, "test.txt")
    engine.search("test")
    
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
    
    engine = DiffSearchEngine()
    lines = ["Line 1 with test", "Line 2 with test", "Line 3"]
    engine.set_content(lines, "test.txt")
    engine.search("test")
    
    stats = engine.get_statistics()
    
    assert stats is not None, "İstatistikler olmalı"
    assert stats["total_matches"] > 0, "Toplam eşleşme olmalı"
    
    print(f"  Total matches: {stats['total_matches']}")
    print(f"  Total lines: {stats['total_lines']}")
    
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
    
    engine = DiffSearchEngine()
    
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
    
    engine = DiffSearchEngine()
    
    config = engine.get_config()
    
    assert config is not None, "Config olmalı"
    assert config.case_sensitive == False, "Config eşleşmeli"
    
    print(f"  Case sensitive: {config.case_sensitive}")
    print(f"  Whole word: {config.whole_word}")
    
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
    assert SearchMode.CASE_SENSITIVE.value == "case_sensitive"
    assert SearchMode.CASE_INSENSITIVE.value == "case_insensitive"
    assert SearchMode.WHOLE_WORD.value == "whole_word"
    
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
    assert SearchScope.ALL_FILES.value == "all_files"
    assert SearchScope.SELECTED_TEXT.value == "selected_text"
    assert SearchScope.VISIBLE_AREA.value == "visible_area"
    assert SearchScope.HUNKS_ONLY.value == "hunks_only"
    
    print(f"  All enum values verified")
    print(f"  Total scopes: {len(SearchScope)}")
    
    print("\n" + "=" * 70)
    print("PASS: SearchScope enum")
    print("=" * 70)


def test_search_direction_enum():
    """
    Test: SearchDirection enum.
    """
    print("=" * 70)
    print("TEST: SearchDirection Enum")
    print("=" * 70)
    
    assert SearchDirection.NEXT.value == "next"
    assert SearchDirection.PREVIOUS.value == "previous"
    assert SearchDirection.ALL.value == "all"
    assert SearchDirection.FIRST.value == "first"
    assert SearchDirection.LAST.value == "last"
    
    print(f"  All enum values verified")
    print(f"  Total directions: {len(SearchDirection)}")
    
    print("\n" + "=" * 70)
    print("PASS: SearchDirection enum")
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
    assert SearchAction.CLEAR.value == "clear"
    
    print(f"  All enum values verified")
    print(f"  Total actions: {len(SearchAction)}")
    
    print("\n" + "=" * 70)
    print("PASS: SearchAction enum")
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
        line_number=1,
        start_position=0,
        end_position=4,
        matched_text="test",
        file_path="test.txt"
    )
    
    assert result.line_number == 1, "Line number eşleşmeli"
    assert result.matched_text == "test", "Matched text eşleşmeli"
    
    print(f"  Line number: {result.line_number}")
    print(f"  Matched text: {result.matched_text}")
    
    print("\n" + "=" * 70)
    print("PASS: SearchResult dataclass")
    print("=" * 70)


def test_replace_result_dataclass():
    """
    Test: ReplaceResult dataclass.
    """
    print("=" * 70)
    print("TEST: ReplaceResult Dataclass")
    print("=" * 70)
    
    result = ReplaceResult(
        line_number=1,
        original_text="test",
        replaced_text="demo",
        file_path="test.txt"
    )
    
    assert result.line_number == 1, "Line number eşleşmeli"
    assert result.was_replaced == True, "Was replaced eşleşmeli"
    
    print(f"  Line number: {result.line_number}")
    print(f"  Was replaced: {result.was_replaced}")
    
    print("\n" + "=" * 70)
    print("PASS: ReplaceResult dataclass")
    print("=" * 70)


def test_search_engine_result_dataclass():
    """
    Test: SearchEngineResult dataclass.
    """
    print("=" * 70)
    print("TEST: SearchEngineResult Dataclass")
    print("=" * 70)
    
    result = SearchEngineResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: SearchEngineResult dataclass")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_search()
        test2 = test_replace()
        test3 = test_replace_all()
        test4 = test_find_next()
        test5 = test_find_previous()
        test6 = test_clear_results()
        test7 = test_get_results()
        test8 = test_get_current_match()
        test9 = test_get_search_history()
        test10 = test_clear_history()
        test11 = test_get_statistics()
        test12 = test_update_config()
        test13 = test_get_config()
        test14 = test_search_mode_enum()
        test15 = test_search_scope_enum()
        test16 = test_search_direction_enum()
        test17 = test_search_action_enum()
        test18 = test_search_config_dataclass()
        test19 = test_search_result_dataclass()
        test20 = test_replace_result_dataclass()
        test21 = test_search_engine_result_dataclass()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Search: {'PASS' if test1 else 'FAIL'}")
        print(f"Replace: {'PASS' if test2 else 'FAIL'}")
        print(f"Replace All: {'PASS' if test3 else 'FAIL'}")
        print(f"Find Next: {'PASS' if test4 else 'FAIL'}")
        print(f"Find Previous: {'PASS' if test5 else 'FAIL'}")
        print(f"Clear Results: {'PASS' if test6 else 'FAIL'}")
        print(f"Get Results: {'PASS' if test7 else 'FAIL'}")
        print(f"Get Current Match: {'PASS' if test8 else 'FAIL'}")
        print(f"Get Search History: {'PASS' if test9 else 'FAIL'}")
        print(f"Clear History: {'PASS' if test10 else 'FAIL'}")
        print(f"Get Statistics: {'PASS' if test11 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test12 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test13 else 'FAIL'}")
        print(f"SearchMode Enum: {'PASS' if test14 else 'FAIL'}")
        print(f"SearchScope Enum: {'PASS' if test15 else 'FAIL'}")
        print(f"SearchDirection Enum: {'PASS' if test16 else 'FAIL'}")
        print(f"SearchAction Enum: {'PASS' if test17 else 'FAIL'}")
        print(f"SearchConfig Dataclass: {'PASS' if test18 else 'FAIL'}")
        print(f"SearchResult Dataclass: {'PASS' if test19 else 'FAIL'}")
        print(f"ReplaceResult Dataclass: {'PASS' if test20 else 'FAIL'}")
        print(f"SearchEngineResult Dataclass: {'PASS' if test21 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14, test15, test16, test17, test18, test19, test20, test21])
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
