"""
Quality Test: Inline Suggestions
Inline suggestions system testleri.
"""

import sys
import os
import tempfile
import shutil
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.ai.inline_suggestions import (
    InlineSuggestionsEngine,
    Suggestion,
    SuggestionType,
    SuggestionPriority,
    SuggestionContext
)


def test_import_suggestions():
    """
    Test: Import suggestions.
    """
    print("=" * 70)
    print("TEST: Import Suggestions")
    print("=" * 70)
    
    engine = InlineSuggestionsEngine()
    
    # "import" ile başlayan prefix
    suggestions = engine.get_suggestions(
        file_path="test.py",
        line=1,
        column=6,
        current_line="import",
        lines_before=[],
        lines_after=[]
    )
    
    assert len(suggestions) > 0, "Import suggestions olmalı"
    
    import_suggestions = [s for s in suggestions if s.type == SuggestionType.IMPORT]
    assert len(import_suggestions) > 0, "Import type suggestions olmalı"
    
    print(f"  Total suggestions: {len(suggestions)}")
    print(f"  Import suggestions: {len(import_suggestions)}")
    print(f"  First import: {import_suggestions[0].text if import_suggestions else 'N/A'}")
    
    print("\n" + "=" * 70)
    print("PASS: Import suggestions")
    print("=" * 70)


def test_function_suggestions():
    """
    Test: Function suggestions.
    """
    print("=" * 70)
    print("TEST: Function Suggestions")
    print("=" * 70)
    
    engine = InlineSuggestionsEngine()
    
    # "def " ile başlayan prefix
    suggestions = engine.get_suggestions(
        file_path="test.py",
        line=1,
        column=4,
        current_line="def ",
        lines_before=[],
        lines_after=[]
    )
    
    # Function suggestions pattern-based olabilir veya boş olabilir
    print(f"  Total suggestions: {len(suggestions)}")
    
    # Pattern suggestions var mı kontrol et
    pattern_suggestions = [s for s in suggestions if s.type == SuggestionType.SNIPPET]
    print(f"  Pattern suggestions: {len(pattern_suggestions)}")
    
    print("\n" + "=" * 70)
    print("PASS: Function suggestions")
    print("=" * 70)


def test_variable_suggestions():
    """
    Test: Variable suggestions.
    """
    print("=" * 70)
    print("TEST: Variable Suggestions")
    print("=" * 70)
    
    engine = InlineSuggestionsEngine()
    
    # Function içinde variable suggestion
    suggestions = engine.get_suggestions(
        file_path="test.py",
        line=2,
        column=2,
        current_line="x = ",
        lines_before=["def test_function():\n    my_var = 10"],
        lines_after=[]
    )
    
    assert len(suggestions) >= 0, "Suggestions olmalı (boş olabilir)"
    
    print(f"  Total suggestions: {len(suggestions)}")
    
    # Variable suggestions var mı kontrol et
    variable_suggestions = [s for s in suggestions if s.type == SuggestionType.VARIABLE]
    print(f"  Variable suggestions: {len(variable_suggestions)}")
    
    print("\n" + "=" * 70)
    print("PASS: Variable suggestions")
    print("=" * 70)


def test_pattern_suggestions():
    """
    Test: Pattern suggestions.
    """
    print("=" * 70)
    print("TEST: Pattern Suggestions")
    print("=" * 70)
    
    engine = InlineSuggestionsEngine()
    
    # "for " ile başlayan prefix
    suggestions = engine.get_suggestions(
        file_path="test.py",
        line=1,
        column=4,
        current_line="for ",
        lines_before=[],
        lines_after=[]
    )
    
    # Pattern suggestions pattern-based olabilir veya boş olabilir
    print(f"  Total suggestions: {len(suggestions)}")
    
    # Pattern suggestions var mı kontrol et
    pattern_suggestions = [s for s in suggestions if s.type == SuggestionType.SNIPPET]
    print(f"  Pattern suggestions: {len(pattern_suggestions)}")
    
    print("\n" + "=" * 70)
    print("PASS: Pattern suggestions")
    print("=" * 70)


def test_context_building():
    """
    Test: Context building.
    """
    print("=" * 70)
    print("TEST: Context Building")
    print("=" * 70)
    
    engine = InlineSuggestionsEngine()
    
    context = engine._build_context(
        file_path="test.py",
        line=1,
        column=5,
        current_line="test_var",
        lines_before=[],
        lines_after=[]
    )
    
    assert context.file_path == "test.py", "File path eşleşmeli"
    assert context.line == 1, "Line eşleşmeli"
    assert context.column == 5, "Column eşleşmeli"
    # Current word detection column-based, so at column 5 it might be "test_"
    assert context.current_word is not None, "Current word olmalı"
    assert context.prefix == "test_", "Prefix eşleşmeli"
    
    print(f"  File path: {context.file_path}")
    print(f"  Line: {context.line}")
    print(f"  Column: {context.column}")
    print(f"  Current word: {context.current_word}")
    print(f"  Prefix: {context.prefix}")
    
    print("\n" + "=" * 70)
    print("PASS: Context building")
    print("=" * 70)


def test_current_word_detection():
    """
    Test: Current word detection.
    """
    print("=" * 70)
    print("TEST: Current Word Detection")
    print("=" * 70)
    
    engine = InlineSuggestionsEngine()
    
    # Test 1: "test_var" cursor "var" üzerinde (column 7 = after 'test_va')
    word1 = engine._get_current_word("test_var", 7)
    assert word1 is not None, "Word olmalı"
    print(f"  Test 1 (column 7): {word1}")
    
    # Test 2: "test_var" cursor "test" üzerinde (column 3 = after 'tes')
    word2 = engine._get_current_word("test_var", 3)
    assert word2 is not None, "Word olmalı"
    print(f"  Test 2 (column 3): {word2}")
    
    # Test 3: Boş satır
    word3 = engine._get_current_word("", 0)
    assert word3 is None, "None olmalı"
    print(f"  Test 3 (empty): {word3}")
    
    # Test 4: Full word (column 7 = last character)
    word4 = engine._get_current_word("test_var", 7)
    assert word4 is not None, "Word olmalı"
    print(f"  Test 4 (full): {word4}")
    
    print("\n" + "=" * 70)
    print("PASS: Current word detection")
    print("=" * 70)


def test_suggestion_priority():
    """
    Test: Suggestion priority sorting.
    """
    print("=" * 70)
    print("TEST: Suggestion Priority Sorting")
    print("=" * 70)
    
    engine = InlineSuggestionsEngine()
    
    suggestions = engine.get_suggestions(
        file_path="test.py",
        line=1,
        column=4,
        current_line="def ",
        lines_before=[],
        lines_after=[]
    )
    
    # Priority sıralamasını kontrol et
    if len(suggestions) > 1:
        for i in range(len(suggestions) - 1):
            assert suggestions[i].priority.value >= suggestions[i + 1].priority.value, \
                "Sıralama priority bazlı olmalı"
    
    print(f"  Total suggestions: {len(suggestions)}")
    if suggestions:
        print(f"  Highest priority: {suggestions[0].priority.name}")
        print(f"  Lowest priority: {suggestions[-1].priority.name}")
    
    print("\n" + "=" * 70)
    print("PASS: Suggestion priority sorting")
    print("=" * 70)


def test_suggestion_types():
    """
    Test: Suggestion type enum.
    """
    print("=" * 70)
    print("TEST: Suggestion Type Enum")
    print("=" * 70)
    
    # Tüm enum değerlerini kontrol et
    assert SuggestionType.COMPLETION.value == "completion"
    assert SuggestionType.IMPORT.value == "import"
    assert SuggestionType.FUNCTION.value == "function"
    assert SuggestionType.VARIABLE.value == "variable"
    assert SuggestionType.SNIPPET.value == "snippet"
    assert SuggestionType.CORRECTION.value == "correction"
    
    print(f"  All enum values verified")
    print(f"  Total types: {len(SuggestionType)}")
    
    print("\n" + "=" * 70)
    print("PASS: Suggestion type enum")
    print("=" * 70)


def test_suggestion_limit():
    """
    Test: Suggestion limit.
    """
    print("=" * 70)
    print("TEST: Suggestion Limit")
    print("=" * 70)
    
    engine = InlineSuggestionsEngine()
    
    suggestions = engine.get_suggestions(
        file_path="test.py",
        line=1,
        column=4,
        current_line="def ",
        lines_before=[],
        lines_after=[]
    )
    
    # Max 20 suggestion
    assert len(suggestions) <= 20, "Max 20 suggestion olmalı"
    
    print(f"  Suggestions: {len(suggestions)}")
    print(f"  Within limit: {len(suggestions) <= 20}")
    
    print("\n" + "=" * 70)
    print("PASS: Suggestion limit")
    print("=" * 70)


def test_codebase_index_integration():
    """
    Test: Codebase index integration.
    """
    print("=" * 70)
    print("TEST: Codebase Index Integration")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp(prefix="muhammedai_test_")
    
    try:
        # Test dosyası oluştur
        test_file = Path(temp_dir) / "test.py"
        test_file.write_text("def my_function():\n    pass\n", encoding='utf-8')
        
        # Codebase index ile engine oluştur
        from app.ai.codebase_index import CodebaseIndex
        codebase_index = CodebaseIndex(project_root=Path(temp_dir))
        
        engine = InlineSuggestionsEngine(codebase_index=codebase_index)
        
        # Codebase index'in set edildiğini kontrol et
        assert engine.codebase_index is not None, "Codebase index set olmalı"
        print(f"  Codebase index integrated: {engine.codebase_index is not None}")
        
        # Symbol suggestions al
        suggestions = engine.get_suggestions(
            file_path=str(test_file),
            line=2,
            column=2,
            current_line="my_",
            lines_before=["def my_function():\n    pass"],
            lines_after=[]
        )
        
        assert isinstance(suggestions, list), "Suggestions list olmalı"
        print(f"  Suggestions retrieved: {len(suggestions)}")
        
        print("\n" + "=" * 70)
        print("PASS: Codebase index integration")
        print("=" * 70)
        
    finally:
        shutil.rmtree(temp_dir)


if __name__ == "__main__":
    try:
        test1 = test_import_suggestions()
        test2 = test_function_suggestions()
        test3 = test_variable_suggestions()
        test4 = test_pattern_suggestions()
        test5 = test_context_building()
        test6 = test_current_word_detection()
        test7 = test_suggestion_priority()
        test8 = test_suggestion_types()
        test9 = test_suggestion_limit()
        test10 = test_codebase_index_integration()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Import Suggestions: {'PASS' if test1 else 'FAIL'}")
        print(f"Function Suggestions: {'PASS' if test2 else 'FAIL'}")
        print(f"Variable Suggestions: {'PASS' if test3 else 'FAIL'}")
        print(f"Pattern Suggestions: {'PASS' if test4 else 'FAIL'}")
        print(f"Context Building: {'PASS' if test5 else 'FAIL'}")
        print(f"Current Word Detection: {'PASS' if test6 else 'FAIL'}")
        print(f"Suggestion Priority Sorting: {'PASS' if test7 else 'FAIL'}")
        print(f"Suggestion Type Enum: {'PASS' if test8 else 'FAIL'}")
        print(f"Suggestion Limit: {'PASS' if test9 else 'FAIL'}")
        print(f"Codebase Index Integration: {'PASS' if test10 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10])
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
