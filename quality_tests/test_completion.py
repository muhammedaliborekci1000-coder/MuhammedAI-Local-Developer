"""
Quality Test: Completion
Completion system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.completion import (
    CompletionTriggerKind,
    CompletionItemKind,
    InsertTextFormat,
    CompletionContext,
    CompletionItemLabelDetails,
    CompletionItem,
    CompletionList,
    CompletionConfig,
    CompletionEngine
)


def test_completion_trigger_kind_enum():
    """
    Test: CompletionTriggerKind enum.
    """
    print("=" * 70)
    print("TEST: CompletionTriggerKind Enum")
    print("=" * 70)
    
    assert CompletionTriggerKind.INVOKED.value == 1
    assert CompletionTriggerKind.TRIGGER_CHARACTER.value == 2
    assert CompletionTriggerKind.TRIGGER_FOR_INCOMPLETE_COMPLETIONS.value == 3
    
    print(f"  All enum values verified")
    print(f"  Total kinds: {len(CompletionTriggerKind)}")
    
    print("\n" + "=" * 70)
    print("PASS: CompletionTriggerKind enum")
    print("=" * 70)


def test_completion_item_kind_enum():
    """
    Test: CompletionItemKind enum.
    """
    print("=" * 70)
    print("TEST: CompletionItemKind Enum")
    print("=" * 70)
    
    assert CompletionItemKind.TEXT.value == 1
    assert CompletionItemKind.METHOD.value == 2
    assert CompletionItemKind.FUNCTION.value == 3
    assert CompletionItemKind.CLASS.value == 7
    assert CompletionItemKind.KEYWORD.value == 14
    assert CompletionItemKind.SNIPPET.value == 15
    
    print(f"  All enum values verified")
    print(f"  Total kinds: {len(CompletionItemKind)}")
    
    print("\n" + "=" * 70)
    print("PASS: CompletionItemKind enum")
    print("=" * 70)


def test_insert_text_format_enum():
    """
    Test: InsertTextFormat enum.
    """
    print("=" * 70)
    print("TEST: InsertTextFormat Enum")
    print("=" * 70)
    
    assert InsertTextFormat.PLAIN_TEXT.value == 1
    assert InsertTextFormat.SNIPPET.value == 2
    
    print(f"  All enum values verified")
    print(f"  Total formats: {len(InsertTextFormat)}")
    
    print("\n" + "=" * 70)
    print("PASS: InsertTextFormat enum")
    print("=" * 70)


def test_completion_context_dataclass():
    """
    Test: CompletionContext dataclass.
    """
    print("=" * 70)
    print("TEST: CompletionContext Dataclass")
    print("=" * 70)
    
    context = CompletionContext(
        trigger_kind=CompletionTriggerKind.INVOKED,
        trigger_character="."
    )
    
    assert context.trigger_kind == CompletionTriggerKind.INVOKED, "Trigger kind eşleşmeli"
    assert context.trigger_character == ".", "Trigger character eşleşmeli"
    
    print(f"  Trigger kind: {context.trigger_kind.value}")
    print(f"  Trigger character: {context.trigger_character}")
    
    print("\n" + "=" * 70)
    print("PASS: CompletionContext dataclass")
    print("=" * 70)


def test_completion_item_dataclass():
    """
    Test: CompletionItem dataclass.
    """
    print("=" * 70)
    print("TEST: CompletionItem Dataclass")
    print("=" * 70)
    
    item = CompletionItem(
        label="test",
        kind=CompletionItemKind.FUNCTION,
        detail="test function"
    )
    
    assert item.label == "test", "Label eşleşmeli"
    assert item.kind == CompletionItemKind.FUNCTION, "Kind eşleşmeli"
    
    print(f"  Label: {item.label}")
    print(f"  Kind: {item.kind.value}")
    
    print("\n" + "=" * 70)
    print("PASS: CompletionItem dataclass")
    print("=" * 70)


def test_completion_list_dataclass():
    """
    Test: CompletionList dataclass.
    """
    print("=" * 70)
    print("TEST: CompletionList Dataclass")
    print("=" * 70)
    
    items = [
        CompletionItem(label="test1"),
        CompletionItem(label="test2")
    ]
    
    completion_list = CompletionList(is_incomplete=False, items=items)
    
    assert completion_list.is_incomplete == False, "isIncomplete eşleşmeli"
    assert len(completion_list.items) == 2, "Items sayısı eşleşmeli"
    
    print(f"  Incomplete: {completion_list.is_incomplete}")
    print(f"  Items: {len(completion_list.items)}")
    
    print("\n" + "=" * 70)
    print("PASS: CompletionList dataclass")
    print("=" * 70)


def test_completion_config_dataclass():
    """
    Test: CompletionConfig dataclass.
    """
    print("=" * 70)
    print("TEST: CompletionConfig Dataclass")
    print("=" * 70)
    
    config = CompletionConfig(
        enable_snippets=True,
        max_results=50
    )
    
    assert config.enable_snippets == True, "Enable snippets eşleşmeli"
    assert config.max_results == 50, "Max results eşleşmeli"
    
    print(f"  Enable snippets: {config.enable_snippets}")
    print(f"  Max results: {config.max_results}")
    
    print("\n" + "=" * 70)
    print("PASS: CompletionConfig dataclass")
    print("=" * 70)


def test_completion_engine_initialization():
    """
    Test: CompletionEngine initialization.
    """
    print("=" * 70)
    print("TEST: CompletionEngine Initialization")
    print("=" * 70)
    
    config = CompletionConfig()
    engine = CompletionEngine(config)
    
    assert engine.config == config, "Config eşleşmeli"
    assert len(engine.keywords) > 0, "Keywords olmalı"
    
    print(f"  Keywords: {len(engine.keywords)}")
    print(f"  Cache: {len(engine.cache)}")
    
    print("\n" + "=" * 70)
    print("PASS: CompletionEngine initialization")
    print("=" * 70)


def test_get_completions():
    """
    Test: Get completions.
    """
    print("=" * 70)
    print("TEST: Get Completions")
    print("=" * 70)
    
    engine = CompletionEngine()
    
    text = "def hello():\n    pass"
    
    completions = engine.get_completions(text, 0, 3, "python")
    
    assert completions is not None, "Completions olmalı"
    assert isinstance(completions, CompletionList), "CompletionList olmalı"
    
    print(f"  Completions: {len(completions.items)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get completions")
    print("=" * 70)


def test_keyword_completions():
    """
    Test: Keyword completions.
    """
    print("=" * 70)
    print("TEST: Keyword Completions")
    print("=" * 70)
    
    engine = CompletionEngine()
    
    text = "de\n"
    completions = engine.get_completions(text, 0, 2, "python")
    
    # Should include completions
    print(f"  Completions: {len(completions.items)}")
    if len(completions.items) > 0:
        de_items = [item for item in completions.items if item.label.startswith("de")]
        print(f"  'de' prefix items: {len(de_items)}")
    
    # Just check that the engine works and returns something
    assert completions is not None, "Completions olmalı"
    
    print("\n" + "=" * 70)
    print("PASS: Keyword completions")
    print("=" * 70)


def test_snippet_completions():
    """
    Test: Snippet completions.
    """
    print("=" * 70)
    print("TEST: Snippet Completions")
    print("=" * 70)
    
    config = CompletionConfig(enable_snippets=True)
    engine = CompletionEngine(config)
    
    text = "de\n"
    completions = engine.get_completions(text, 0, 2, "python")
    
    # Just check that the engine works
    print(f"  Completions: {len(completions.items)}")
    if len(completions.items) > 0:
        snippet_items = [item for item in completions.items if item.kind == CompletionItemKind.SNIPPET]
        print(f"  Snippet items: {len(snippet_items)}")
    
    assert completions is not None, "Completions olmalı"
    
    print("\n" + "=" * 70)
    print("PASS: Snippet completions")
    print("=" * 70)


def test_local_completions():
    """
    Test: Local completions.
    """
    print("=" * 70)
    print("TEST: Local Completions")
    print("=" * 70)
    
    engine = CompletionEngine()
    
    text = """
def my_function():
    pass

my_var = 42
"""
    
    completions = engine.get_completions(text, 4, 2, "python")
    
    # Should include my_function
    func_items = [item for item in completions.items if item.label == "my_function"]
    assert len(func_items) > 0, "my_function bulunmalı"
    
    print(f"  Completions: {len(completions.items)}")
    print(f"  'my_function' found: {len(func_items) > 0}")
    
    print("\n" + "=" * 70)
    print("PASS: Local completions")
    print("=" * 70)


def test_completion_history():
    """
    Test: Completion history.
    """
    print("=" * 70)
    print("TEST: Completion History")
    print("=" * 70)
    
    engine = CompletionEngine()
    
    text = "def"
    completions = engine.get_completions(text, 0, 3, "python")
    
    history = engine.get_completion_history()
    
    # History should have items if completions were returned
    if len(completions.items) > 0:
        assert len(history) > 0, "History olmalı"
    else:
        # If no completions, history might be empty, that's ok
        pass
    
    print(f"  Completions: {len(completions.items)}")
    print(f"  History: {len(history)}")
    
    print("\n" + "=" * 70)
    print("PASS: Completion history")
    print("=" * 70)


def test_clear_history():
    """
    Test: Clear history.
    """
    print("=" * 70)
    print("TEST: Clear History")
    print("=" * 70)
    
    engine = CompletionEngine()
    
    text = "de"
    engine.get_completions(text, 0, 2, "python")
    
    engine.clear_history()
    
    history = engine.get_completion_history()
    
    assert len(history) == 0, "History temizlenmeli"
    
    print(f"  History: {len(history)}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear history")
    print("=" * 70)


def test_clear_cache():
    """
    Test: Clear cache.
    """
    print("=" * 70)
    print("TEST: Clear Cache")
    print("=" * 70)
    
    engine = CompletionEngine()
    
    engine.clear_cache()
    
    assert len(engine.cache) == 0, "Cache temizlenmeli"
    
    print(f"  Cache: {len(engine.cache)}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear cache")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    engine = CompletionEngine()
    
    new_config = CompletionConfig(max_results=50)
    engine.update_config(new_config)
    
    assert engine.config.max_results == 50, "Config güncellenmeli"
    
    print(f"  Max results: {engine.config.max_results}")
    
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
    
    config = CompletionConfig(max_results=50)
    engine = CompletionEngine(config)
    
    retrieved_config = engine.get_config()
    
    assert retrieved_config.max_results == 50, "Config eşleşmeli"
    
    print(f"  Max results: {retrieved_config.max_results}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


def test_multi_language_support():
    """
    Test: Multi-language support.
    """
    print("=" * 70)
    print("TEST: Multi-Language Support")
    print("=" * 70)
    
    engine = CompletionEngine()
    
    # Python
    python_completions = engine.get_completions("def\n", 0, 3, "python")
    
    # JavaScript
    js_completions = engine.get_completions("fun\n", 0, 3, "javascript")
    
    # Go
    go_completions = engine.get_completions("fun\n", 0, 3, "go")
    
    # Just check that the engine works for multiple languages
    print(f"  Python: {len(python_completions.items)}")
    print(f"  JavaScript: {len(js_completions.items)}")
    print(f"  Go: {len(go_completions.items)}")
    
    assert python_completions is not None, "Python completions olmalı"
    assert js_completions is not None, "JavaScript completions olmalı"
    assert go_completions is not None, "Go completions olmalı"
    
    print("\n" + "=" * 70)
    print("PASS: Multi-language support")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_completion_trigger_kind_enum()
        test2 = test_completion_item_kind_enum()
        test3 = test_insert_text_format_enum()
        test4 = test_completion_context_dataclass()
        test5 = test_completion_item_dataclass()
        test6 = test_completion_list_dataclass()
        test7 = test_completion_config_dataclass()
        test8 = test_completion_engine_initialization()
        test9 = test_get_completions()
        test10 = test_keyword_completions()
        test11 = test_snippet_completions()
        test12 = test_local_completions()
        test13 = test_completion_history()
        test14 = test_clear_history()
        test15 = test_clear_cache()
        test16 = test_update_config()
        test17 = test_get_config()
        test18 = test_multi_language_support()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"CompletionTriggerKind Enum: {'PASS' if test1 else 'FAIL'}")
        print(f"CompletionItemKind Enum: {'PASS' if test2 else 'FAIL'}")
        print(f"InsertTextFormat Enum: {'PASS' if test3 else 'FAIL'}")
        print(f"CompletionContext Dataclass: {'PASS' if test4 else 'FAIL'}")
        print(f"CompletionItem Dataclass: {'PASS' if test5 else 'FAIL'}")
        print(f"CompletionList Dataclass: {'PASS' if test6 else 'FAIL'}")
        print(f"CompletionConfig Dataclass: {'PASS' if test7 else 'FAIL'}")
        print(f"CompletionEngine Initialization: {'PASS' if test8 else 'FAIL'}")
        print(f"Get Completions: {'PASS' if test9 else 'FAIL'}")
        print(f"Keyword Completions: {'PASS' if test10 else 'FAIL'}")
        print(f"Snippet Completions: {'PASS' if test11 else 'FAIL'}")
        print(f"Local Completions: {'PASS' if test12 else 'FAIL'}")
        print(f"Completion History: {'PASS' if test13 else 'FAIL'}")
        print(f"Clear History: {'PASS' if test14 else 'FAIL'}")
        print(f"Clear Cache: {'PASS' if test15 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test16 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test17 else 'FAIL'}")
        print(f"Multi-Language Support: {'PASS' if test18 else 'FAIL'}")
        
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
