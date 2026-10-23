"""
Quality Test: Auto Completion
Auto completion system testleri.
"""

import sys
import os
import tempfile
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.auto_completion import (
    AutoCompleter,
    CompletionType,
    CompletionContext,
    CompletionItem,
    AutoCompletionResult
)


def test_complete():
    """
    Test: Auto completion.
    """
    print("=" * 70)
    print("TEST: Auto Completion")
    print("=" * 70)
    
    # Test dosyası oluştur
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write("def my_function():\n    pass\n")
        test_file = f.name
    
    try:
        completer = AutoCompleter()
        
        result = completer.complete(test_file, line=1, column=4, prefix="def")
        
        assert result.success, "Completion başarılı olmalı"
        assert isinstance(result.items, list), "Items list olmalı"
        
        print(f"  Success: {result.success}")
        print(f"  Items: {len(result.items)}")
        print(f"  Context: {result.context.value if result.context else None}")
        print(f"  Message: {result.message}")
        
        print("\n" + "=" * 70)
        print("PASS: Auto completion")
        print("=" * 70)
    
    finally:
        Path(test_file).unlink()


def test_keyword_completion():
    """
    Test: Keyword completion.
    """
    print("=" * 70)
    print("TEST: Keyword Completion")
    print("=" * 70)
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write("def my_function():\n    pass\n")
        test_file = f.name
    
    try:
        completer = AutoCompleter()
        
        result = completer.complete(test_file, line=1, column=2, prefix="de")
        
        assert result.success, "Completion başarılı olmalı"
        
        keyword_items = [item for item in result.items if item.type == CompletionType.KEYWORD]
        print(f"  Keyword items: {len(keyword_items)}")
        
        print("\n" + "=" * 70)
        print("PASS: Keyword completion")
        print("=" * 70)
    
    finally:
        Path(test_file).unlink()


def test_builtin_completion():
    """
    Test: Built-in completion.
    """
    print("=" * 70)
    print("TEST: Built-in Completion")
    print("=" * 70)
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write("x = len()\n")
        test_file = f.name
    
    try:
        completer = AutoCompleter()
        
        result = completer.complete(test_file, line=1, column=6, prefix="le")
        
        assert result.success, "Completion başarılı olmalı"
        
        builtin_items = [item for item in result.items if item.type == CompletionType.BUILTIN]
        print(f"  Built-in items: {len(builtin_items)}")
        
        print("\n" + "=" * 70)
        print("PASS: Built-in completion")
        print("=" * 70)
    
    finally:
        Path(test_file).unlink()


def test_local_variable_completion():
    """
    Test: Local variable completion.
    """
    print("=" * 70)
    print("TEST: Local Variable Completion")
    print("=" * 70)
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write("my_var = 10\nx = my_\n")
        test_file = f.name
    
    try:
        completer = AutoCompleter()
        
        result = completer.complete(test_file, line=2, column=6, prefix="my_")
        
        assert result.success, "Completion başarılı olmalı"
        
        var_items = [item for item in result.items if item.type == CompletionType.VARIABLE]
        print(f"  Variable items: {len(var_items)}")
        
        print("\n" + "=" * 70)
        print("PASS: Local variable completion")
        print("=" * 70)
    
    finally:
        Path(test_file).unlink()


def test_snippet_completion():
    """
    Test: Snippet completion.
    """
    print("=" * 70)
    print("TEST: Snippet Completion")
    print("=" * 70)
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write("def\n")
        test_file = f.name
    
    try:
        completer = AutoCompleter()
        
        result = completer.complete(test_file, line=1, column=3, prefix="def")
        
        assert result.success, "Completion başarılı olmalı"
        
        snippet_items = [item for item in result.items if item.type == CompletionType.SNIPPET]
        print(f"  Snippet items: {len(snippet_items)}")
        
        print("\n" + "=" * 70)
        print("PASS: Snippet completion")
        print("=" * 70)
    
    finally:
        Path(test_file).unlink()


def test_import_completion():
    """
    Test: Import completion.
    """
    print("=" * 70)
    print("TEST: Import Completion")
    print("=" * 70)
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write("import os\n")
        test_file = f.name
    
    try:
        completer = AutoCompleter()
        
        result = completer.complete(test_file, line=1, column=8, prefix="o")
        
        assert result.success, "Completion başarılı olmalı"
        
        import_items = [item for item in result.items if item.type == CompletionType.IMPORT]
        print(f"  Import items: {len(import_items)}")
        
        print("\n" + "=" * 70)
        print("PASS: Import completion")
        print("=" * 70)
    
    finally:
        Path(test_file).unlink()


def test_completion_type_enum():
    """
    Test: CompletionType enum.
    """
    print("=" * 70)
    print("TEST: CompletionType Enum")
    print("=" * 70)
    
    assert CompletionType.KEYWORD.value == "keyword"
    assert CompletionType.BUILTIN.value == "builtin"
    assert CompletionType.VARIABLE.value == "variable"
    assert CompletionType.FUNCTION.value == "function"
    assert CompletionType.CLASS.value == "class"
    assert CompletionType.METHOD.value == "method"
    assert CompletionType.ATTRIBUTE.value == "attribute"
    assert CompletionType.IMPORT.value == "import"
    assert CompletionType.SNIPPET.value == "snippet"
    assert CompletionType.PATH.value == "path"
    assert CompletionType.FILE.value == "file"
    
    print(f"  All enum values verified")
    print(f"  Total types: {len(CompletionType)}")
    
    print("\n" + "=" * 70)
    print("PASS: CompletionType enum")
    print("=" * 70)


def test_completion_context_enum():
    """
    Test: CompletionContext enum.
    """
    print("=" * 70)
    print("TEST: CompletionContext Enum")
    print("=" * 70)
    
    assert CompletionContext.TOP_LEVEL.value == "top_level"
    assert CompletionContext.FUNCTION_BODY.value == "function_body"
    assert CompletionContext.CLASS_BODY.value == "class_body"
    assert CompletionContext.IMPORT_STATEMENT.value == "import_statement"
    assert CompletionContext.ATTRIBUTE_ACCESS.value == "attribute_access"
    assert CompletionContext.FUNCTION_CALL.value == "function_call"
    
    print(f"  All enum values verified")
    print(f"  Total contexts: {len(CompletionContext)}")
    
    print("\n" + "=" * 70)
    print("PASS: CompletionContext enum")
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
        type=CompletionType.KEYWORD,
        detail="Test detail",
        documentation="Test doc",
        insert_text="test",
        score=1.0
    )
    
    assert item.label == "test", "Label eşleşmeli"
    assert item.type == CompletionType.KEYWORD, "Type eşleşmeli"
    assert item.score == 1.0, "Score eşleşmeli"
    
    print(f"  Label: {item.label}")
    print(f"  Type: {item.type.value}")
    print(f"  Score: {item.score}")
    
    print("\n" + "=" * 70)
    print("PASS: CompletionItem dataclass")
    print("=" * 70)


def test_auto_completion_result_dataclass():
    """
    Test: AutoCompletionResult dataclass.
    """
    print("=" * 70)
    print("TEST: AutoCompletionResult Dataclass")
    print("=" * 70)
    
    result = AutoCompletionResult(success=True)
    result.message = "Test message"
    result.context = CompletionContext.TOP_LEVEL
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert result.context == CompletionContext.TOP_LEVEL, "Context eşleşmeli"
    assert isinstance(result.items, list), "Items list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Context: {result.context.value}")
    print(f"  Items: {len(result.items)}")
    
    print("\n" + "=" * 70)
    print("PASS: AutoCompletionResult dataclass")
    print("=" * 70)


def test_context_determination():
    """
    Test: Context determination.
    """
    print("=" * 70)
    print("TEST: Context Determination")
    print("=" * 70)
    
    completer = AutoCompleter()
    
    lines = ["def my_function():", "    pass"]
    context = completer._determine_context(lines, 1, 5)
    
    assert context is not None, "Context olmalı"
    print(f"  Context: {context.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Context determination")
    print("=" * 70)


def test_scoring_and_sorting():
    """
    Test: Scoring and sorting.
    """
    print("=" * 70)
    print("TEST: Scoring and Sorting")
    print("=" * 70)
    
    completer = AutoCompleter()
    
    items = [
        CompletionItem(label="def", type=CompletionType.KEYWORD, score=0.5),
        CompletionItem(label="define", type=CompletionType.KEYWORD, score=0.3),
        CompletionItem(label="default", type=CompletionType.KEYWORD, score=0.7)
    ]
    
    sorted_items = completer._score_and_sort(items, "de")
    
    assert len(sorted_items) == 3, "3 item olmalı"
    assert sorted_items[0].score >= sorted_items[1].score, "Sıralı olmalı"
    
    print(f"  Sorted items: {len(sorted_items)}")
    print(f"  First item: {sorted_items[0].label} (score: {sorted_items[0].score})")
    
    print("\n" + "=" * 70)
    print("PASS: Scoring and sorting")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_complete()
        test2 = test_keyword_completion()
        test3 = test_builtin_completion()
        test4 = test_local_variable_completion()
        test5 = test_snippet_completion()
        test6 = test_import_completion()
        test7 = test_completion_type_enum()
        test8 = test_completion_context_enum()
        test9 = test_completion_item_dataclass()
        test10 = test_auto_completion_result_dataclass()
        test11 = test_context_determination()
        test12 = test_scoring_and_sorting()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Auto Completion: {'PASS' if test1 else 'FAIL'}")
        print(f"Keyword Completion: {'PASS' if test2 else 'FAIL'}")
        print(f"Built-in Completion: {'PASS' if test3 else 'FAIL'}")
        print(f"Local Variable Completion: {'PASS' if test4 else 'FAIL'}")
        print(f"Snippet Completion: {'PASS' if test5 else 'FAIL'}")
        print(f"Import Completion: {'PASS' if test6 else 'FAIL'}")
        print(f"CompletionType Enum: {'PASS' if test7 else 'FAIL'}")
        print(f"CompletionContext Enum: {'PASS' if test8 else 'FAIL'}")
        print(f"CompletionItem Dataclass: {'PASS' if test9 else 'FAIL'}")
        print(f"AutoCompletionResult Dataclass: {'PASS' if test10 else 'FAIL'}")
        print(f"Context Determination: {'PASS' if test11 else 'FAIL'}")
        print(f"Scoring and Sorting: {'PASS' if test12 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12])
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
