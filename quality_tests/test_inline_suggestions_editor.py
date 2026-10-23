"""
Quality Test: Inline Suggestions (Editor)
Inline suggestions system testleri for editor module.
"""

import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from app.editor.inline_suggestions import (
    SuggestionType,
    SuggestionTrigger,
    SuggestionRange,
    InlineSuggestion,
    SuggestionsConfig,
    SuggestionsResult,
    InlineSuggestionsManager
)


def test_suggestion_type_enum():
    """
    Test: SuggestionType enum.
    """
    print("=" * 70)
    print("TEST: SuggestionType Enum")
    print("=" * 70)
    
    assert SuggestionType.COMPLETION.value == "completion"
    assert SuggestionType.PREDICTION.value == "prediction"
    assert SuggestionType.SNIPPET.value == "snippet"
    assert SuggestionType.FIX.value == "fix"
    assert SuggestionType.OPTIMIZATION.value == "optimization"
    assert SuggestionType.CUSTOM.value == "custom"
    
    print(f"  All enum values verified")
    print(f"  Total types: {len(SuggestionType)}")
    
    print("\n" + "=" * 70)
    print("PASS: SuggestionType enum")
    print("=" * 70)


def test_suggestion_trigger_enum():
    """
    Test: SuggestionTrigger enum.
    """
    print("=" * 70)
    print("TEST: SuggestionTrigger Enum")
    print("=" * 70)
    
    assert SuggestionTrigger.MANUAL.value == "manual"
    assert SuggestionTrigger.AUTOMATIC.value == "automatic"
    assert SuggestionTrigger.ON_TYPE.value == "on_type"
    assert SuggestionTrigger.ON_SAVE.value == "on_save"
    
    print(f"  All enum values verified")
    print(f"  Total triggers: {len(SuggestionTrigger)}")
    
    print("\n" + "=" * 70)
    print("PASS: SuggestionTrigger enum")
    print("=" * 70)


def test_suggestion_range_dataclass():
    """
    Test: SuggestionRange dataclass.
    """
    print("=" * 70)
    print("TEST: SuggestionRange Dataclass")
    print("=" * 70)
    
    range = SuggestionRange(
        start_line=0,
        start_column=0,
        end_line=10,
        end_column=20
    )
    
    assert range.start_line == 0, "Start line eşleşmeli"
    assert range.start_column == 0, "Start column eşleşmeli"
    assert range.end_line == 10, "End line eşleşmeli"
    assert range.end_column == 20, "End column eşleşmeli"
    
    print(f"  Start: ({range.start_line}, {range.start_column})")
    print(f"  End: ({range.end_line}, {range.end_column})")
    
    print("\n" + "=" * 70)
    print("PASS: SuggestionRange dataclass")
    print("=" * 70)


def test_inline_suggestion_dataclass():
    """
    Test: InlineSuggestion dataclass.
    """
    print("=" * 70)
    print("TEST: InlineSuggestion Dataclass")
    print("=" * 70)
    
    range = SuggestionRange(0, 0, 0, 10)
    suggestion = InlineSuggestion(
        id="suggestion_1",
        type=SuggestionType.COMPLETION,
        range=range,
        text="completion_text"
    )
    
    assert suggestion.id == "suggestion_1", "ID eşleşmeli"
    assert suggestion.type == SuggestionType.COMPLETION, "Type eşleşmeli"
    assert suggestion.text == "completion_text", "Text eşleşmeli"
    
    print(f"  ID: {suggestion.id}")
    print(f"  Type: {suggestion.type.value}")
    print(f"  Text: {suggestion.text}")
    
    print("\n" + "=" * 70)
    print("PASS: InlineSuggestion dataclass")
    print("=" * 70)


def test_suggestions_config_dataclass():
    """
    Test: SuggestionsConfig dataclass.
    """
    print("=" * 70)
    print("TEST: SuggestionsConfig Dataclass")
    print("=" * 70)
    
    config = SuggestionsConfig(
        enabled=True,
        trigger_mode=SuggestionTrigger.AUTOMATIC
    )
    
    assert config.enabled == True, "Enabled eşleşmeli"
    assert config.trigger_mode == SuggestionTrigger.AUTOMATIC, "Trigger mode eşleşmeli"
    
    print(f"  Enabled: {config.enabled}")
    print(f"  Trigger mode: {config.trigger_mode.value}")
    
    print("\n" + "=" * 70)
    print("PASS: SuggestionsConfig dataclass")
    print("=" * 70)


def test_suggestions_result_dataclass():
    """
    Test: SuggestionsResult dataclass.
    """
    print("=" * 70)
    print("TEST: SuggestionsResult Dataclass")
    print("=" * 70)
    
    result = SuggestionsResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.suggestions, list), "Suggestions list olmalı"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Suggestions: {len(result.suggestions)}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: SuggestionsResult dataclass")
    print("=" * 70)


def test_inline_suggestions_manager_initialization():
    """
    Test: InlineSuggestionsManager initialization.
    """
    print("=" * 70)
    print("TEST: InlineSuggestionsManager Initialization")
    print("=" * 70)
    
    config = SuggestionsConfig()
    manager = InlineSuggestionsManager(config)
    
    assert manager.config == config, "Config eşleşmeli"
    assert len(manager.suggestions) == 0, "Suggestions boş olmalı"
    
    print(f"  Suggestions: {len(manager.suggestions)}")
    
    print("\n" + "=" * 70)
    print("PASS: InlineSuggestionsManager initialization")
    print("=" * 70)


def test_add_suggestion():
    """
    Test: Add suggestion.
    """
    print("=" * 70)
    print("TEST: Add Suggestion")
    print("=" * 70)
    
    manager = InlineSuggestionsManager()
    
    range = SuggestionRange(0, 0, 0, 10)
    suggestion = InlineSuggestion(
        id="",
        type=SuggestionType.COMPLETION,
        range=range,
        text="completion_text"
    )
    
    result = manager.add_suggestion(suggestion)
    
    assert result.success == True, "Ekleme başarılı olmalı"
    assert len(manager.suggestions) > 0, "Suggestion eklenmeli"
    
    print(f"  Suggestion added: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add suggestion")
    print("=" * 70)


def test_remove_suggestion():
    """
    Test: Remove suggestion.
    """
    print("=" * 70)
    print("TEST: Remove Suggestion")
    print("=" * 70)
    
    manager = InlineSuggestionsManager()
    
    range = SuggestionRange(0, 0, 0, 10)
    suggestion = InlineSuggestion(
        id="",
        type=SuggestionType.COMPLETION,
        range=range,
        text="completion_text"
    )
    
    result = manager.add_suggestion(suggestion)
    suggestion_id = result.suggestions[0].id
    
    result = manager.remove_suggestion(suggestion_id)
    
    assert result.success == True, "Kaldırma başarılı olmalı"
    assert suggestion_id not in manager.suggestions, "Suggestion silinmeli"
    
    print(f"  Suggestion removed: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Remove suggestion")
    print("=" * 70)


def test_get_suggestion():
    """
    Test: Get suggestion.
    """
    print("=" * 70)
    print("TEST: Get Suggestion")
    print("=" * 70)
    
    manager = InlineSuggestionsManager()
    
    range = SuggestionRange(0, 0, 0, 10)
    suggestion = InlineSuggestion(
        id="",
        type=SuggestionType.COMPLETION,
        range=range,
        text="completion_text"
    )
    
    result = manager.add_suggestion(suggestion)
    suggestion_id = result.suggestions[0].id
    
    retrieved_suggestion = manager.get_suggestion(suggestion_id)
    
    assert retrieved_suggestion is not None, "Suggestion bulunmalı"
    assert retrieved_suggestion.id == suggestion_id, "ID eşleşmeli"
    
    print(f"  Suggestion: {retrieved_suggestion.text}")
    
    print("\n" + "=" * 70)
    print("PASS: Get suggestion")
    print("=" * 70)


def test_get_all_suggestions():
    """
    Test: Get all suggestions.
    """
    print("=" * 70)
    print("TEST: Get All Suggestions")
    print("=" * 70)
    
    manager = InlineSuggestionsManager()
    
    range = SuggestionRange(0, 0, 0, 10)
    suggestion = InlineSuggestion(
        id="",
        type=SuggestionType.COMPLETION,
        range=range,
        text="completion_text"
    )
    
    manager.add_suggestion(suggestion)
    suggestions = manager.get_all_suggestions()
    
    assert len(suggestions) > 0, "Suggestions olmalı"
    
    print(f"  Total suggestions: {len(suggestions)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get all suggestions")
    print("=" * 70)


def test_get_suggestions_by_type():
    """
    Test: Get suggestions by type.
    """
    print("=" * 70)
    print("TEST: Get Suggestions by Type")
    print("=" * 70)
    
    manager = InlineSuggestionsManager()
    
    range = SuggestionRange(0, 0, 0, 10)
    suggestion = InlineSuggestion(
        id="",
        type=SuggestionType.COMPLETION,
        range=range,
        text="completion_text"
    )
    
    manager.add_suggestion(suggestion)
    suggestions = manager.get_suggestions_by_type(SuggestionType.COMPLETION)
    
    assert len(suggestions) > 0, "Completion suggestions olmalı"
    
    print(f"  Completion suggestions: {len(suggestions)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get suggestions by type")
    print("=" * 70)


def test_add_completion_suggestion():
    """
    Test: Add completion suggestion.
    """
    print("=" * 70)
    print("TEST: Add Completion Suggestion")
    print("=" * 70)
    
    manager = InlineSuggestionsManager()
    
    range = SuggestionRange(0, 0, 0, 10)
    result = manager.add_completion_suggestion(range, "completion_text", 0.8)
    
    assert result.success == True, "Completion suggestion başarılı olmalı"
    
    print(f"  Completion suggestion: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add completion suggestion")
    print("=" * 70)


def test_add_prediction_suggestion():
    """
    Test: Add prediction suggestion.
    """
    print("=" * 70)
    print("TEST: Add Prediction Suggestion")
    print("=" * 70)
    
    manager = InlineSuggestionsManager()
    
    range = SuggestionRange(0, 0, 0, 10)
    result = manager.add_prediction_suggestion(range, "prediction_text", 0.7)
    
    assert result.success == True, "Prediction suggestion başarılı olmalı"
    
    print(f"  Prediction suggestion: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add prediction suggestion")
    print("=" * 70)


def test_add_snippet_suggestion():
    """
    Test: Add snippet suggestion.
    """
    print("=" * 70)
    print("TEST: Add Snippet Suggestion")
    print("=" * 70)
    
    manager = InlineSuggestionsManager()
    
    range = SuggestionRange(0, 0, 0, 10)
    result = manager.add_snippet_suggestion(range, "snippet_text", "Test snippet")
    
    assert result.success == True, "Snippet suggestion başarılı olmalı"
    
    print(f"  Snippet suggestion: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add snippet suggestion")
    print("=" * 70)


def test_add_fix_suggestion():
    """
    Test: Add fix suggestion.
    """
    print("=" * 70)
    print("TEST: Add Fix Suggestion")
    print("=" * 70)
    
    manager = InlineSuggestionsManager()
    
    range = SuggestionRange(0, 0, 0, 10)
    result = manager.add_fix_suggestion(range, "fix_text", "Test fix")
    
    assert result.success == True, "Fix suggestion başarılı olmalı"
    
    print(f"  Fix suggestion: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add fix suggestion")
    print("=" * 70)


def test_add_optimization_suggestion():
    """
    Test: Add optimization suggestion.
    """
    print("=" * 70)
    print("TEST: Add Optimization Suggestion")
    print("=" * 70)
    
    manager = InlineSuggestionsManager()
    
    range = SuggestionRange(0, 0, 0, 10)
    result = manager.add_optimization_suggestion(range, "optimization_text", "Test optimization")
    
    assert result.success == True, "Optimization suggestion başarılı olmalı"
    
    print(f"  Optimization suggestion: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add optimization suggestion")
    print("=" * 70)


def test_filter_by_confidence():
    """
    Test: Filter by confidence.
    """
    print("=" * 70)
    print("TEST: Filter by Confidence")
    print("=" * 70)
    
    manager = InlineSuggestionsManager()
    
    range = SuggestionRange(0, 0, 0, 10)
    manager.add_completion_suggestion(range, "text1", 0.9)
    manager.add_completion_suggestion(range, "text2", 0.5)
    
    filtered = manager.filter_by_confidence(0.7)
    
    assert len(filtered) > 0, "Filtered suggestions olmalı"
    
    print(f"  Filtered suggestions: {len(filtered)}")
    
    print("\n" + "=" * 70)
    print("PASS: Filter by confidence")
    print("=" * 70)


def test_get_top_suggestions():
    """
    Test: Get top suggestions.
    """
    print("=" * 70)
    print("TEST: Get Top Suggestions")
    print("=" * 70)
    
    manager = InlineSuggestionsManager()
    
    range = SuggestionRange(0, 0, 0, 10)
    manager.add_completion_suggestion(range, "text1", 0.9)
    manager.add_completion_suggestion(range, "text2", 0.7)
    
    top = manager.get_top_suggestions(1)
    
    assert len(top) > 0, "Top suggestions olmalı"
    
    print(f"  Top suggestions: {len(top)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get top suggestions")
    print("=" * 70)


def test_clear_suggestions():
    """
    Test: Clear suggestions.
    """
    print("=" * 70)
    print("TEST: Clear Suggestions")
    print("=" * 70)
    
    manager = InlineSuggestionsManager()
    
    range = SuggestionRange(0, 0, 0, 10)
    manager.add_completion_suggestion(range, "text", 0.8)
    
    result = manager.clear_suggestions()
    
    assert result.success == True, "Clear başarılı olmalı"
    assert len(manager.suggestions) == 0, "Suggestions temizlenmeli"
    
    print(f"  Cleared: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear suggestions")
    print("=" * 70)


def test_clear_suggestions_by_type():
    """
    Test: Clear suggestions by type.
    """
    print("=" * 70)
    print("TEST: Clear Suggestions by Type")
    print("=" * 70)
    
    manager = InlineSuggestionsManager()
    
    range = SuggestionRange(0, 0, 0, 10)
    manager.add_completion_suggestion(range, "text", 0.8)
    
    result = manager.clear_suggestions_by_type(SuggestionType.COMPLETION)
    
    assert result.success == True, "Clear başarılı olmalı"
    
    print(f"  Cleared by type: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear suggestions by type")
    print("=" * 70)


def test_set_suggestion_enabled():
    """
    Test: Set suggestion enabled.
    """
    print("=" * 70)
    print("TEST: Set Suggestion Enabled")
    print("=" * 70)
    
    manager = InlineSuggestionsManager()
    
    range = SuggestionRange(0, 0, 0, 10)
    result = manager.add_completion_suggestion(range, "text", 0.8)
    suggestion_id = result.suggestions[0].id
    
    result = manager.set_suggestion_enabled(suggestion_id, False)
    
    assert result.success == True, "Set başarılı olmalı"
    
    print(f"  Suggestion enabled state: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set suggestion enabled")
    print("=" * 70)


def test_set_suggestion_visible():
    """
    Test: Set suggestion visible.
    """
    print("=" * 70)
    print("TEST: Set Suggestion Visible")
    print("=" * 70)
    
    manager = InlineSuggestionsManager()
    
    range = SuggestionRange(0, 0, 0, 10)
    result = manager.add_completion_suggestion(range, "text", 0.8)
    suggestion_id = result.suggestions[0].id
    
    result = manager.set_suggestion_visible(suggestion_id, False)
    
    assert result.success == True, "Set başarılı olmalı"
    
    print(f"  Suggestion visible state: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set suggestion visible")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    manager = InlineSuggestionsManager()
    
    new_config = SuggestionsConfig(max_suggestions=10)
    result = manager.update_config(new_config)
    
    assert result.success == True, "Update başarılı olmalı"
    assert manager.config.max_suggestions == 10, "Config güncellenmeli"
    
    print(f"  Max suggestions: {manager.config.max_suggestions}")
    
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
    
    config = SuggestionsConfig(max_suggestions=10)
    manager = InlineSuggestionsManager(config)
    
    retrieved_config = manager.get_config()
    
    assert retrieved_config.max_suggestions == 10, "Config eşleşmeli"
    
    print(f"  Max suggestions: {retrieved_config.max_suggestions}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_suggestion_type_enum()
        test2 = test_suggestion_trigger_enum()
        test3 = test_suggestion_range_dataclass()
        test4 = test_inline_suggestion_dataclass()
        test5 = test_suggestions_config_dataclass()
        test6 = test_suggestions_result_dataclass()
        test7 = test_inline_suggestions_manager_initialization()
        test8 = test_add_suggestion()
        test9 = test_remove_suggestion()
        test10 = test_get_suggestion()
        test11 = test_get_all_suggestions()
        test12 = test_get_suggestions_by_type()
        test13 = test_add_completion_suggestion()
        test14 = test_add_prediction_suggestion()
        test15 = test_add_snippet_suggestion()
        test16 = test_add_fix_suggestion()
        test17 = test_add_optimization_suggestion()
        test18 = test_filter_by_confidence()
        test19 = test_get_top_suggestions()
        test20 = test_clear_suggestions()
        test21 = test_clear_suggestions_by_type()
        test22 = test_set_suggestion_enabled()
        test23 = test_set_suggestion_visible()
        test24 = test_update_config()
        test25 = test_get_config()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"SuggestionType Enum: {'PASS' if test1 else 'FAIL'}")
        print(f"SuggestionTrigger Enum: {'PASS' if test2 else 'FAIL'}")
        print(f"SuggestionRange Dataclass: {'PASS' if test3 else 'FAIL'}")
        print(f"InlineSuggestion Dataclass: {'PASS' if test4 else 'FAIL'}")
        print(f"SuggestionsConfig Dataclass: {'PASS' if test5 else 'FAIL'}")
        print(f"SuggestionsResult Dataclass: {'PASS' if test6 else 'FAIL'}")
        print(f"InlineSuggestionsManager Initialization: {'PASS' if test7 else 'FAIL'}")
        print(f"Add Suggestion: {'PASS' if test8 else 'FAIL'}")
        print(f"Remove Suggestion: {'PASS' if test9 else 'FAIL'}")
        print(f"Get Suggestion: {'PASS' if test10 else 'FAIL'}")
        print(f"Get All Suggestions: {'PASS' if test11 else 'FAIL'}")
        print(f"Get Suggestions by Type: {'PASS' if test12 else 'FAIL'}")
        print(f"Add Completion Suggestion: {'PASS' if test13 else 'FAIL'}")
        print(f"Add Prediction Suggestion: {'PASS' if test14 else 'FAIL'}")
        print(f"Add Snippet Suggestion: {'PASS' if test15 else 'FAIL'}")
        print(f"Add Fix Suggestion: {'PASS' if test16 else 'FAIL'}")
        print(f"Add Optimization Suggestion: {'PASS' if test17 else 'FAIL'}")
        print(f"Filter by Confidence: {'PASS' if test18 else 'FAIL'}")
        print(f"Get Top Suggestions: {'PASS' if test19 else 'FAIL'}")
        print(f"Clear Suggestions: {'PASS' if test20 else 'FAIL'}")
        print(f"Clear Suggestions by Type: {'PASS' if test21 else 'FAIL'}")
        print(f"Set Suggestion Enabled: {'PASS' if test22 else 'FAIL'}")
        print(f"Set Suggestion Visible: {'PASS' if test23 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test24 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test25 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14, test15, test16, test17, test18, test19, test20, test21, test22, test23, test24, test25])
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
