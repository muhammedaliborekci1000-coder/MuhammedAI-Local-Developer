"""
Quality Test: Search and Replace
Search and replace system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.search_replace import (
    SearchReplaceEngine,
    SearchMode,
    SearchAction,
    ReplaceMode,
    SearchMatch,
    SearchResult,
    ReplaceResult,
    SearchReplaceConfig
)


def test_search_normal():
    """
    Test: Search normal mode.
    """
    print("=" * 70)
    print("TEST: Search Normal Mode")
    print("=" * 70)
    
    text = "Hello world, hello Python, hello AI"
    engine = SearchReplaceEngine()
    result = engine.search(text, "hello", SearchMode.NORMAL)
    
    assert result.success, "Search başarılı olmalı"
    assert result.total_matches > 0, "Eşleşme bulunmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Total matches: {result.total_matches}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Search normal mode")
    print("=" * 70)


def test_search_case_sensitive():
    """
    Test: Search case-sensitive mode.
    """
    print("=" * 70)
    print("TEST: Search Case-Sensitive Mode")
    print("=" * 70)
    
    text = "Hello world, hello Python, HELLO AI"
    engine = SearchReplaceEngine()
    result = engine.search(text, "Hello", SearchMode.CASE_SENSITIVE)
    
    assert result.success, "Search başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Total matches: {result.total_matches}")
    
    print("\n" + "=" * 70)
    print("PASS: Search case-sensitive mode")
    print("=" * 70)


def test_search_case_insensitive():
    """
    Test: Search case-insensitive mode.
    """
    print("=" * 70)
    print("TEST: Search Case-Insensitive Mode")
    print("=" * 70)
    
    text = "Hello world, hello Python, HELLO AI"
    engine = SearchReplaceEngine()
    result = engine.search(text, "hello", SearchMode.CASE_INSENSITIVE)
    
    assert result.success, "Search başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Total matches: {result.total_matches}")
    
    print("\n" + "=" * 70)
    print("PASS: Search case-insensitive mode")
    print("=" * 70)


def test_search_regex():
    """
    Test: Search regex mode.
    """
    print("=" * 70)
    print("TEST: Search Regex Mode")
    print("=" * 70)
    
    text = "Hello123 world456 Python789"
    engine = SearchReplaceEngine()
    result = engine.search(text, r"\d+", SearchMode.REGEX)
    
    assert result.success, "Search başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Total matches: {result.total_matches}")
    
    print("\n" + "=" * 70)
    print("PASS: Search regex mode")
    print("=" * 70)


def test_search_whole_word():
    """
    Test: Search whole word mode.
    """
    print("=" * 70)
    print("TEST: Search Whole Word Mode")
    print("=" * 70)
    
    text = "Hello world, hello Python, helloAI"
    engine = SearchReplaceEngine()
    result = engine.search(text, "hello", SearchMode.WHOLE_WORD)
    
    assert result.success, "Search başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Total matches: {result.total_matches}")
    
    print("\n" + "=" * 70)
    print("PASS: Search whole word mode")
    print("=" * 70)


def test_replace_one():
    """
    Test: Replace one occurrence.
    """
    print("=" * 70)
    print("TEST: Replace One")
    print("=" * 70)
    
    text = "Hello world, hello Python, hello AI"
    engine = SearchReplaceEngine()
    result = engine.replace(text, "hello", "Hi", SearchMode.CASE_INSENSITIVE, ReplaceMode.REPLACE_ONE)
    
    assert result.success, "Replace başarılı olmalı"
    assert result.replacements_count == 1, "1 değişiklik olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Replacements: {result.replacements_count}")
    print(f"  Replaced text: {result.replaced_text}")
    
    print("\n" + "=" * 70)
    print("PASS: Replace one")
    print("=" * 70)


def test_replace_all():
    """
    Test: Replace all occurrences.
    """
    print("=" * 70)
    print("TEST: Replace All")
    print("=" * 70)
    
    text = "Hello world, hello Python, hello AI"
    engine = SearchReplaceEngine()
    result = engine.replace(text, "hello", "Hi", SearchMode.CASE_INSENSITIVE, ReplaceMode.REPLACE_ALL)
    
    assert result.success, "Replace başarılı olmalı"
    assert result.replacements_count > 1, "Birden fazla değişiklik olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Replacements: {result.replacements_count}")
    print(f"  Replaced text: {result.replaced_text}")
    
    print("\n" + "=" * 70)
    print("PASS: Replace all")
    print("=" * 70)


def test_replace_preview():
    """
    Test: Replace preview.
    """
    print("=" * 70)
    print("TEST: Replace Preview")
    print("=" * 70)
    
    text = "Hello world, hello Python, hello AI"
    engine = SearchReplaceEngine()
    result = engine.replace(text, "hello", "Hi", SearchMode.CASE_INSENSITIVE, ReplaceMode.PREVIEW)
    
    assert result.success, "Preview başarılı olmalı"
    assert result.replaced_text is None, "Text değiştirilmemeli"
    assert len(result.preview_matches) > 0, "Preview matches olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Preview matches: {len(result.preview_matches)}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Replace preview")
    print("=" * 70)


def test_replace_at_position():
    """
    Test: Replace at position.
    """
    print("=" * 70)
    print("TEST: Replace at Position")
    print("=" * 70)
    
    text = "Hello world, hello Python, hello AI"
    engine = SearchReplaceEngine()
    result = engine.replace_at_position(text, "hello", "Hi", 1, SearchMode.CASE_INSENSITIVE)
    
    assert result.success, "Replace başarılı olmalı"
    assert result.replacements_count == 1, "1 değişiklik olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Replacements: {result.replacements_count}")
    
    print("\n" + "=" * 70)
    print("PASS: Replace at position")
    print("=" * 70)


def test_get_next_match():
    """
    Test: Get next match.
    """
    print("=" * 70)
    print("TEST: Get Next Match")
    print("=" * 70)
    
    text = "Hello world, hello Python, hello AI"
    engine = SearchReplaceEngine()
    engine.search(text, "hello", SearchMode.CASE_INSENSITIVE)
    
    next_match = engine.get_next_match(0, "forward")
    
    assert next_match is not None, "Next match bulunmalı"
    
    print(f"  Next match found: {next_match is not None}")
    print(f"  Match text: {next_match.text if next_match else None}")
    
    print("\n" + "=" * 70)
    print("PASS: Get next match")
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
    assert SearchMode.WHOLE_WORD.value == "whole_word"
    assert SearchMode.FUZZY.value == "fuzzy"
    
    print(f"  All enum values verified")
    print(f"  Total modes: {len(SearchMode)}")
    
    print("\n" + "=" * 70)
    print("PASS: SearchMode enum")
    print("=" * 70)


def test_replace_mode_enum():
    """
    Test: ReplaceMode enum.
    """
    print("=" * 70)
    print("TEST: ReplaceMode Enum")
    print("=" * 70)
    
    assert ReplaceMode.REPLACE_ONE.value == "replace_one"
    assert ReplaceMode.REPLACE_ALL.value == "replace_all"
    assert ReplaceMode.PREVIEW.value == "preview"
    
    print(f"  All enum values verified")
    print(f"  Total modes: {len(ReplaceMode)}")
    
    print("\n" + "=" * 70)
    print("PASS: ReplaceMode enum")
    print("=" * 70)


def test_search_match_dataclass():
    """
    Test: SearchMatch dataclass.
    """
    print("=" * 70)
    print("TEST: SearchMatch Dataclass")
    print("=" * 70)
    
    match = SearchMatch(
        text="hello",
        start=0,
        end=5,
        line=1,
        column=0,
        line_text="hello world"
    )
    
    assert match.text == "hello", "Text eşleşmeli"
    assert match.line == 1, "Line eşleşmeli"
    
    print(f"  Text: {match.text}")
    print(f"  Line: {match.line}")
    print(f"  Column: {match.column}")
    
    print("\n" + "=" * 70)
    print("PASS: SearchMatch dataclass")
    print("=" * 70)


def test_search_result_dataclass():
    """
    Test: SearchResult dataclass.
    """
    print("=" * 70)
    print("TEST: SearchResult Dataclass")
    print("=" * 70)
    
    result = SearchResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.matches, list), "Matches list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Matches: {len(result.matches)}")
    
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
    
    result = ReplaceResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.preview_matches, list), "Preview matches list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Preview matches: {len(result.preview_matches)}")
    
    print("\n" + "=" * 70)
    print("PASS: ReplaceResult dataclass")
    print("=" * 70)


def test_search_fuzzy():
    """
    Test: Search fuzzy mode.
    """
    print("=" * 70)
    print("TEST: Search Fuzzy Mode")
    print("=" * 70)
    
    text = "Hello world, hello_function Python, helloAI"
    engine = SearchReplaceEngine()
    result = engine.search(text, "hello", SearchMode.FUZZY)
    
    assert result.success, "Search başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Total matches: {result.total_matches}")
    
    print("\n" + "=" * 70)
    print("PASS: Search fuzzy mode")
    print("=" * 70)


def test_find_next():
    """
    Test: Find next.
    """
    print("=" * 70)
    print("TEST: Find Next")
    print("=" * 70)
    
    text = "Hello world, hello Python, hello AI"
    engine = SearchReplaceEngine()
    engine.search(text, "hello", SearchMode.CASE_INSENSITIVE)
    
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
    
    text = "Hello world, hello Python, hello AI"
    engine = SearchReplaceEngine()
    engine.search(text, "hello", SearchMode.CASE_INSENSITIVE)
    
    result = engine.find_previous()
    
    assert result.success, "Find previous başarılı olmalı"
    assert result.action == SearchAction.FIND_PREVIOUS.value, "Action eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Find previous")
    print("=" * 70)


def test_undo():
    """
    Test: Undo.
    """
    print("=" * 70)
    print("TEST: Undo")
    print("=" * 70)
    
    text = "Hello world, hello Python, hello AI"
    engine = SearchReplaceEngine()
    engine.replace(text, "hello", "Hi", SearchMode.CASE_INSENSITIVE, ReplaceMode.REPLACE_ALL)
    
    result = engine.undo()
    
    assert result.success, "Undo başarılı olmalı"
    assert result.action == SearchAction.UNDO.value, "Action eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Undo")
    print("=" * 70)


def test_redo():
    """
    Test: Redo.
    """
    print("=" * 70)
    print("TEST: Redo")
    print("=" * 70)
    
    text = "Hello world, hello Python, hello AI"
    engine = SearchReplaceEngine()
    engine.replace(text, "hello", "Hi", SearchMode.CASE_INSENSITIVE, ReplaceMode.REPLACE_ALL)
    engine.undo()
    
    result = engine.redo()
    
    assert result.success, "Redo başarılı olmalı"
    assert result.action == SearchAction.REDO.value, "Action eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Redo")
    print("=" * 70)


def test_search_history():
    """
    Test: Search history.
    """
    print("=" * 70)
    print("TEST: Search History")
    print("=" * 70)
    
    text = "Hello world, hello Python, hello AI"
    engine = SearchReplaceEngine()
    engine.search(text, "hello", SearchMode.CASE_INSENSITIVE)
    
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
    
    text = "Hello world, hello Python, hello AI"
    engine = SearchReplaceEngine()
    engine.search(text, "hello", SearchMode.CASE_INSENSITIVE)
    
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
    
    text = "Hello world, hello Python, hello AI"
    engine = SearchReplaceEngine()
    engine.search(text, "hello", SearchMode.CASE_INSENSITIVE)
    
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
    
    engine = SearchReplaceEngine()
    
    new_config = SearchReplaceConfig(case_sensitive=True)
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
    
    engine = SearchReplaceEngine()
    
    config = engine.get_config()
    
    assert config is not None, "Config olmalı"
    assert config.mode == SearchMode.NORMAL, "Mode eşleşmeli"
    
    print(f"  Mode: {config.mode.value}")
    print(f"  Case sensitive: {config.case_sensitive}")
    
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
    assert SearchAction.PREVIEW.value == "preview"
    assert SearchAction.FIND_NEXT.value == "find_next"
    assert SearchAction.FIND_PREVIOUS.value == "find_previous"
    assert SearchAction.UNDO.value == "undo"
    assert SearchAction.REDO.value == "redo"
    
    print(f"  All enum values verified")
    print(f"  Total actions: {len(SearchAction)}")
    
    print("\n" + "=" * 70)
    print("PASS: SearchAction enum")
    print("=" * 70)


def test_search_replace_config_dataclass():
    """
    Test: SearchReplaceConfig dataclass.
    """
    print("=" * 70)
    print("TEST: SearchReplaceConfig Dataclass")
    print("=" * 70)
    
    config = SearchReplaceConfig(
        mode=SearchMode.REGEX,
        case_sensitive=True
    )
    
    assert config.mode == SearchMode.REGEX, "Mode eşleşmeli"
    assert config.case_sensitive == True, "Case sensitive eşleşmeli"
    
    print(f"  Mode: {config.mode.value}")
    print(f"  Case sensitive: {config.case_sensitive}")
    print(f"  Include context: {config.include_context}")
    
    print("\n" + "=" * 70)
    print("PASS: SearchReplaceConfig dataclass")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_search_normal()
        test2 = test_search_case_sensitive()
        test3 = test_search_case_insensitive()
        test4 = test_search_regex()
        test5 = test_search_whole_word()
        test6 = test_replace_one()
        test7 = test_replace_all()
        test8 = test_replace_preview()
        test9 = test_replace_at_position()
        test10 = test_get_next_match()
        test11 = test_search_mode_enum()
        test12 = test_replace_mode_enum()
        test13 = test_search_match_dataclass()
        test14 = test_search_result_dataclass()
        test15 = test_replace_result_dataclass()
        test16 = test_search_fuzzy()
        test17 = test_find_next()
        test18 = test_find_previous()
        test19 = test_undo()
        test20 = test_redo()
        test21 = test_search_history()
        test22 = test_clear_history()
        test23 = test_get_statistics()
        test24 = test_update_config()
        test25 = test_get_config()
        test26 = test_search_action_enum()
        test27 = test_search_replace_config_dataclass()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Search Normal: {'PASS' if test1 else 'FAIL'}")
        print(f"Search Case-Sensitive: {'PASS' if test2 else 'FAIL'}")
        print(f"Search Case-Insensitive: {'PASS' if test3 else 'FAIL'}")
        print(f"Search Regex: {'PASS' if test4 else 'FAIL'}")
        print(f"Search Whole Word: {'PASS' if test5 else 'FAIL'}")
        print(f"Replace One: {'PASS' if test6 else 'FAIL'}")
        print(f"Replace All: {'PASS' if test7 else 'FAIL'}")
        print(f"Replace Preview: {'PASS' if test8 else 'FAIL'}")
        print(f"Replace at Position: {'PASS' if test9 else 'FAIL'}")
        print(f"Get Next Match: {'PASS' if test10 else 'FAIL'}")
        print(f"SearchMode Enum: {'PASS' if test11 else 'FAIL'}")
        print(f"ReplaceMode Enum: {'PASS' if test12 else 'FAIL'}")
        print(f"SearchMatch Dataclass: {'PASS' if test13 else 'FAIL'}")
        print(f"SearchResult Dataclass: {'PASS' if test14 else 'FAIL'}")
        print(f"ReplaceResult Dataclass: {'PASS' if test15 else 'FAIL'}")
        print(f"Search Fuzzy: {'PASS' if test16 else 'FAIL'}")
        print(f"Find Next: {'PASS' if test17 else 'FAIL'}")
        print(f"Find Previous: {'PASS' if test18 else 'FAIL'}")
        print(f"Undo: {'PASS' if test19 else 'FAIL'}")
        print(f"Redo: {'PASS' if test20 else 'FAIL'}")
        print(f"Search History: {'PASS' if test21 else 'FAIL'}")
        print(f"Clear History: {'PASS' if test22 else 'FAIL'}")
        print(f"Get Statistics: {'PASS' if test23 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test24 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test25 else 'FAIL'}")
        print(f"SearchAction Enum: {'PASS' if test26 else 'FAIL'}")
        print(f"SearchReplaceConfig Dataclass: {'PASS' if test27 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14, test15, test16, test17, test18, test19, test20, test21, test22, test23, test24, test25, test26, test27])
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
