"""
Quality Test: Replace UI
Replace UI system testleri.
"""

import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from app.editor.replace_ui import (
    ReplaceMode,
    ReplaceScope,
    MatchCase,
    ReplaceMatch,
    ReplaceQuery,
    ReplaceConfig,
    ReplaceResult,
    ReplaceUIManager
)


def test_replace_mode_enum():
    """
    Test: ReplaceMode enum.
    """
    print("=" * 70)
    print("TEST: ReplaceMode Enum")
    print("=" * 70)
    
    assert ReplaceMode.SINGLE.value == "single"
    assert ReplaceMode.ALL.value == "all"
    assert ReplaceMode.SELECTION.value == "selection"
    assert ReplaceMode.BUFFER.value == "buffer"
    
    print(f"  All enum values verified")
    print(f"  Total modes: {len(ReplaceMode)}")
    
    print("\n" + "=" * 70)
    print("PASS: ReplaceMode enum")
    print("=" * 70)


def test_replace_scope_enum():
    """
    Test: ReplaceScope enum.
    """
    print("=" * 70)
    print("TEST: ReplaceScope Enum")
    print("=" * 70)
    
    assert ReplaceScope.CURRENT_FILE.value == "current_file"
    assert ReplaceScope.OPEN_FILES.value == "open_files"
    assert ReplaceScope.PROJECT.value == "project"
    assert ReplaceScope.SELECTION.value == "selection"
    
    print(f"  All enum values verified")
    print(f"  Total scopes: {len(ReplaceScope)}")
    
    print("\n" + "=" * 70)
    print("PASS: ReplaceScope enum")
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


def test_replace_match_dataclass():
    """
    Test: ReplaceMatch dataclass.
    """
    print("=" * 70)
    print("TEST: ReplaceMatch Dataclass")
    print("=" * 70)
    
    match = ReplaceMatch(
        line_number=1,
        column=0,
        line_content="hello world",
        match_text="hello"
    )
    
    assert match.line_number == 1, "Line number eşleşmeli"
    assert match.column == 0, "Column eşleşmeli"
    assert match.match_text == "hello", "Match text eşleşmeli"
    
    print(f"  Line: {match.line_number}")
    print(f"  Column: {match.column}")
    print(f"  Match: {match.match_text}")
    
    print("\n" + "=" * 70)
    print("PASS: ReplaceMatch dataclass")
    print("=" * 70)


def test_replace_query_dataclass():
    """
    Test: ReplaceQuery dataclass.
    """
    print("=" * 70)
    print("TEST: ReplaceQuery Dataclass")
    print("=" * 70)
    
    query = ReplaceQuery(
        search_text="hello",
        replace_text="world",
        mode=ReplaceMode.SINGLE,
        scope=ReplaceScope.CURRENT_FILE
    )
    
    assert query.search_text == "hello", "Search text eşleşmeli"
    assert query.replace_text == "world", "Replace text eşleşmeli"
    assert query.mode == ReplaceMode.SINGLE, "Mode eşleşmeli"
    
    print(f"  Search: {query.search_text}")
    print(f"  Replace: {query.replace_text}")
    print(f"  Mode: {query.mode.value}")
    
    print("\n" + "=" * 70)
    print("PASS: ReplaceQuery dataclass")
    print("=" * 70)


def test_replace_config_dataclass():
    """
    Test: ReplaceConfig dataclass.
    """
    print("=" * 70)
    print("TEST: ReplaceConfig Dataclass")
    print("=" * 70)
    
    config = ReplaceConfig(
        show_preview=True,
        show_context=True
    )
    
    assert config.show_preview == True, "Show preview eşleşmeli"
    assert config.show_context == True, "Show context eşleşmeli"
    
    print(f"  Show preview: {config.show_preview}")
    print(f"  Show context: {config.show_context}")
    
    print("\n" + "=" * 70)
    print("PASS: ReplaceConfig dataclass")
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
    assert isinstance(result.matches, list), "Matches list olmalı"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Matches: {len(result.matches)}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: ReplaceResult dataclass")
    print("=" * 70)


def test_replace_ui_manager_initialization():
    """
    Test: ReplaceUIManager initialization.
    """
    print("=" * 70)
    print("TEST: ReplaceUIManager Initialization")
    print("=" * 70)
    
    config = ReplaceConfig()
    manager = ReplaceUIManager(config)
    
    assert manager.config == config, "Config eşleşmeli"
    assert len(manager.replace_history) == 0, "History boş olmalı"
    
    print(f"  History: {len(manager.replace_history)}")
    
    print("\n" + "=" * 70)
    print("PASS: ReplaceUIManager initialization")
    print("=" * 70)


def test_find_matches():
    """
    Test: Find matches.
    """
    print("=" * 70)
    print("TEST: Find Matches")
    print("=" * 70)
    
    manager = ReplaceUIManager()
    
    query = ReplaceQuery(search_text="hello")
    content = "hello world\nhello there"
    
    result = manager.find_matches(query, content)
    
    assert result.success == True, "Find başarılı olmalı"
    assert len(result.matches) > 0, "Matches bulunmalı"
    
    print(f"  Matches: {len(result.matches)}")
    
    print("\n" + "=" * 70)
    print("PASS: Find matches")
    print("=" * 70)


def test_replace():
    """
    Test: Replace.
    """
    print("=" * 70)
    print("TEST: Replace")
    print("=" * 70)
    
    manager = ReplaceUIManager()
    
    query = ReplaceQuery(search_text="hello", replace_text="world")
    content = "hello world"
    
    result = manager.replace(query, content)
    
    assert result.success == True, "Replace başarılı olmalı"
    assert result.replaced_count == 1, "1 değişiklik olmalı"
    
    print(f"  Replaced: {result.message}")
    
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
    
    manager = ReplaceUIManager()
    
    query = ReplaceQuery(search_text="hello", replace_text="world")
    content = "hello world\nhello there"
    
    result = manager.replace_all(query, content)
    
    assert result.success == True, "Replace all başarılı olmalı"
    assert result.replaced_count > 0, "Değişiklikler olmalı"
    
    print(f"  Replaced: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Replace all")
    print("=" * 70)


def test_preview_replace():
    """
    Test: Preview replace.
    """
    print("=" * 70)
    print("TEST: Preview Replace")
    print("=" * 70)
    
    manager = ReplaceUIManager()
    
    query = ReplaceQuery(search_text="hello", replace_text="world")
    content = "hello world"
    
    result = manager.preview_replace(query, content)
    
    assert result.success == True, "Preview başarılı olmalı"
    
    print(f"  Preview: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Preview replace")
    print("=" * 70)


def test_get_replace_history():
    """
    Test: Get replace history.
    """
    print("=" * 70)
    print("TEST: Get Replace History")
    print("=" * 70)
    
    manager = ReplaceUIManager()
    
    query = ReplaceQuery(search_text="hello", replace_text="world")
    manager.find_matches(query, "hello world")
    
    history = manager.get_replace_history()
    
    assert len(history) > 0, "History olmalı"
    
    print(f"  History: {len(history)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get replace history")
    print("=" * 70)


def test_clear_history():
    """
    Test: Clear history.
    """
    print("=" * 70)
    print("TEST: Clear History")
    print("=" * 70)
    
    manager = ReplaceUIManager()
    
    query = ReplaceQuery(search_text="hello", replace_text="world")
    manager.find_matches(query, "hello world")
    
    manager.clear_history()
    
    history = manager.get_replace_history()
    
    assert len(history) == 0, "History temizlenmeli"
    
    print(f"  History cleared")
    
    print("\n" + "=" * 70)
    print("PASS: Clear history")
    print("=" * 70)


def test_get_current_matches():
    """
    Test: Get current matches.
    """
    print("=" * 70)
    print("TEST: Get Current Matches")
    print("=" * 70)
    
    manager = ReplaceUIManager()
    
    query = ReplaceQuery(search_text="hello")
    manager.find_matches(query, "hello world")
    
    matches = manager.get_current_matches()
    
    assert len(matches) > 0, "Matches olmalı"
    
    print(f"  Matches: {len(matches)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get current matches")
    print("=" * 70)


def test_navigate_to_match():
    """
    Test: Navigate to match.
    """
    print("=" * 70)
    print("TEST: Navigate to Match")
    print("=" * 70)
    
    manager = ReplaceUIManager()
    
    query = ReplaceQuery(search_text="hello")
    manager.find_matches(query, "hello world")
    
    match = manager.navigate_to_match(0)
    
    assert match is not None, "Match bulunmalı"
    
    print(f"  Navigated to: line {match.line_number}")
    
    print("\n" + "=" * 70)
    print("PASS: Navigate to match")
    print("=" * 70)


def test_get_match_count():
    """
    Test: Get match count.
    """
    print("=" * 70)
    print("TEST: Get Match Count")
    print("=" * 70)
    
    manager = ReplaceUIManager()
    
    query = ReplaceQuery(search_text="hello")
    manager.find_matches(query, "hello world\nhello there")
    
    count = manager.get_match_count()
    
    assert count > 0, "Count > 0 olmalı"
    
    print(f"  Count: {count}")
    
    print("\n" + "=" * 70)
    print("PASS: Get match count")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    manager = ReplaceUIManager()
    
    new_config = ReplaceConfig(max_matches=500)
    manager.update_config(new_config)
    
    assert manager.config.max_matches == 500, "Config güncellenmeli"
    
    print(f"  Max matches: {manager.config.max_matches}")
    
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
    
    config = ReplaceConfig(max_matches=500)
    manager = ReplaceUIManager(config)
    
    retrieved_config = manager.get_config()
    
    assert retrieved_config.max_matches == 500, "Config eşleşmeli"
    
    print(f"  Max matches: {retrieved_config.max_matches}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_replace_mode_enum()
        test2 = test_replace_scope_enum()
        test3 = test_match_case_enum()
        test4 = test_replace_match_dataclass()
        test5 = test_replace_query_dataclass()
        test6 = test_replace_config_dataclass()
        test7 = test_replace_result_dataclass()
        test8 = test_replace_ui_manager_initialization()
        test9 = test_find_matches()
        test10 = test_replace()
        test11 = test_replace_all()
        test12 = test_preview_replace()
        test13 = test_get_replace_history()
        test14 = test_clear_history()
        test15 = test_get_current_matches()
        test16 = test_navigate_to_match()
        test17 = test_get_match_count()
        test18 = test_update_config()
        test19 = test_get_config()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"ReplaceMode Enum: {'PASS' if test1 else 'FAIL'}")
        print(f"ReplaceScope Enum: {'PASS' if test2 else 'FAIL'}")
        print(f"MatchCase Enum: {'PASS' if test3 else 'FAIL'}")
        print(f"ReplaceMatch Dataclass: {'PASS' if test4 else 'FAIL'}")
        print(f"ReplaceQuery Dataclass: {'PASS' if test5 else 'FAIL'}")
        print(f"ReplaceConfig Dataclass: {'PASS' if test6 else 'FAIL'}")
        print(f"ReplaceResult Dataclass: {'PASS' if test7 else 'FAIL'}")
        print(f"ReplaceUIManager Initialization: {'PASS' if test8 else 'FAIL'}")
        print(f"Find Matches: {'PASS' if test9 else 'FAIL'}")
        print(f"Replace: {'PASS' if test10 else 'FAIL'}")
        print(f"Replace All: {'PASS' if test11 else 'FAIL'}")
        print(f"Preview Replace: {'PASS' if test12 else 'FAIL'}")
        print(f"Get Replace History: {'PASS' if test13 else 'FAIL'}")
        print(f"Clear History: {'PASS' if test14 else 'FAIL'}")
        print(f"Get Current Matches: {'PASS' if test15 else 'FAIL'}")
        print(f"Navigate to Match: {'PASS' if test16 else 'FAIL'}")
        print(f"Get Match Count: {'PASS' if test17 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test18 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test19 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14, test15, test16, test17, test18, test19])
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
