"""
Quality Test: Semantic Search
Semantic search system testleri.
"""

import sys
import os
import tempfile
import shutil
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.ai.semantic_search import (
    SemanticSearchEngine,
    SearchType,
    SearchScope,
    SearchResult,
    SemanticSearchResult
)


def test_search():
    """
    Test: Semantic search.
    """
    print("=" * 70)
    print("TEST: Semantic Search")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp(prefix="muhammedai_test_")
    
    try:
        # Test dosyası oluştur
        test_file = Path(temp_dir) / "test_module.py"
        test_file.write_text("""
def my_function():
    return 42

class MyClass:
    def method(self):
        pass
""", encoding='utf-8')
        
        engine = SemanticSearchEngine(project_root=temp_dir)
        
        # Search
        result = engine.search("function")
        
        assert result.success, "Search başarılı olmalı"
        assert isinstance(result.results, list), "Results list olmalı"
        
        print(f"  Success: {result.success}")
        print(f"  Results: {len(result.results)}")
        print(f"  Message: {result.message}")
        
        print("\n" + "=" * 70)
        print("PASS: Semantic search")
        print("=" * 70)
        
    finally:
        shutil.rmtree(temp_dir)


def test_search_symbols():
    """
    Test: Search symbols.
    """
    print("=" * 70)
    print("TEST: Search Symbols")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp(prefix="muhammedai_test_")
    
    try:
        # Test dosyası oluştur
        test_file = Path(temp_dir) / "test_module.py"
        test_file.write_text("""
def my_function():
    pass

class MyClass:
    pass
""", encoding='utf-8')
        
        engine = SemanticSearchEngine(project_root=temp_dir)
        
        # Symbol search
        result = engine.search_symbols("my_function")
        
        assert result.success, "Search başarılı olmalı"
        assert isinstance(result.results, list), "Results list olmalı"
        
        print(f"  Success: {result.success}")
        print(f"  Results: {len(result.results)}")
        print(f"  Message: {result.message}")
        
        print("\n" + "=" * 70)
        print("PASS: Search symbols")
        print("=" * 70)
        
    finally:
        shutil.rmtree(temp_dir)


def test_search_files():
    """
    Test: Search files.
    """
    print("=" * 70)
    print("TEST: Search Files")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp(prefix="muhammedai_test_")
    
    try:
        # Test dosyası oluştur
        test_file = Path(temp_dir) / "test_module.py"
        test_file.write_text("pass", encoding='utf-8')
        
        engine = SemanticSearchEngine(project_root=temp_dir)
        
        # File search
        result = engine.search_files("test")
        
        assert result.success, "Search başarılı olmalı"
        assert isinstance(result.results, list), "Results list olmalı"
        
        print(f"  Success: {result.success}")
        print(f"  Results: {len(result.results)}")
        print(f"  Message: {result.message}")
        
        print("\n" + "=" * 70)
        print("PASS: Search files")
        print("=" * 70)
        
    finally:
        shutil.rmtree(temp_dir)


def test_search_type_enum():
    """
    Test: SearchType enum.
    """
    print("=" * 70)
    print("TEST: SearchType Enum")
    print("=" * 70)
    
    assert SearchType.CODE.value == "code"
    assert SearchType.SYMBOL.value == "symbol"
    assert SearchType.DOCUMENTATION.value == "documentation"
    assert SearchType.FILE.value == "file"
    
    print(f"  All enum values verified")
    print(f"  Total types: {len(SearchType)}")
    
    print("\n" + "=" * 70)
    print("PASS: SearchType enum")
    print("=" * 70)


def test_search_scope_enum():
    """
    Test: SearchScope enum.
    """
    print("=" * 70)
    print("TEST: SearchScope Enum")
    print("=" * 70)
    
    assert SearchScope.PROJECT.value == "project"
    assert SearchScope.FILE.value == "file"
    assert SearchScope.DIRECTORY.value == "directory"
    
    print(f"  All enum values verified")
    print(f"  Total scopes: {len(SearchScope)}")
    
    print("\n" + "=" * 70)
    print("PASS: SearchScope enum")
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
        line=10,
        column=5,
        score=0.9,
        content="test content",
        symbol_name="test",
        symbol_type="function"
    )
    
    assert result.file_path == "test.py", "File path eşleşmeli"
    assert result.score == 0.9, "Score eşleşmeli"
    assert result.symbol_name == "test", "Symbol name eşleşmeli"
    
    print(f"  File path: {result.file_path}")
    print(f"  Score: {result.score}")
    print(f"  Symbol name: {result.symbol_name}")
    
    print("\n" + "=" * 70)
    print("PASS: SearchResult dataclass")
    print("=" * 70)


def test_semantic_search_result_dataclass():
    """
    Test: SemanticSearchResult dataclass.
    """
    print("=" * 70)
    print("TEST: SemanticSearchResult Dataclass")
    print("=" * 70)
    
    result = SemanticSearchResult(success=True)
    result.message = "Test message"
    result.query = "test query"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert result.query == "test query", "Query eşleşmeli"
    assert isinstance(result.results, list), "Results list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Query: {result.query}")
    print(f"  Results: {len(result.results)}")
    
    print("\n" + "=" * 70)
    print("PASS: SemanticSearchResult dataclass")
    print("=" * 70)


def test_keyword_extraction():
    """
    Test: Keyword extraction.
    """
    print("=" * 70)
    print("TEST: Keyword Extraction")
    print("=" * 70)
    
    engine = SemanticSearchEngine()
    
    keywords = engine._extract_keywords("find function that returns value")
    
    assert isinstance(keywords, list), "Keywords list olmalı"
    assert len(keywords) > 0, "Keywords olmalı"
    
    print(f"  Keywords: {keywords}")
    
    print("\n" + "=" * 70)
    print("PASS: Keyword extraction")
    print("=" * 70)


def test_score_calculation():
    """
    Test: Score calculation.
    """
    print("=" * 70)
    print("TEST: Score Calculation")
    print("=" * 70)
    
    engine = SemanticSearchEngine()
    
    item = {
        "name": "my_function",
        "type": "function",
        "content": "def my_function():",
        "line": 1,
        "column": 0
    }
    
    keywords = ["function"]
    score = engine._calculate_score(keywords, item)
    
    assert score >= 0, "Score non-negative olmalı"
    
    print(f"  Score: {score}")
    
    print("\n" + "=" * 70)
    print("PASS: Score calculation")
    print("=" * 70)


def test_context_extraction():
    """
    Test: Context extraction.
    """
    print("=" * 70)
    print("TEST: Context Extraction")
    print("=" * 70)
    
    engine = SemanticSearchEngine()
    
    lines = ["line 1", "line 2", "line 3", "line 4", "line 5"]
    context = engine._get_context(lines, 3)
    
    assert context is not None, "Context olmalı"
    assert isinstance(context, str), "Context string olmalı"
    
    print(f"  Context: {context}")
    
    print("\n" + "=" * 70)
    print("PASS: Context extraction")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_search()
        test2 = test_search_symbols()
        test3 = test_search_files()
        test4 = test_search_type_enum()
        test5 = test_search_scope_enum()
        test6 = test_search_result_dataclass()
        test7 = test_semantic_search_result_dataclass()
        test8 = test_keyword_extraction()
        test9 = test_score_calculation()
        test10 = test_context_extraction()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Semantic Search: {'PASS' if test1 else 'FAIL'}")
        print(f"Search Symbols: {'PASS' if test2 else 'FAIL'}")
        print(f"Search Files: {'PASS' if test3 else 'FAIL'}")
        print(f"SearchType Enum: {'PASS' if test4 else 'FAIL'}")
        print(f"SearchScope Enum: {'PASS' if test5 else 'FAIL'}")
        print(f"SearchResult Dataclass: {'PASS' if test6 else 'FAIL'}")
        print(f"SemanticSearchResult Dataclass: {'PASS' if test7 else 'FAIL'}")
        print(f"Keyword Extraction: {'PASS' if test8 else 'FAIL'}")
        print(f"Score Calculation: {'PASS' if test9 else 'FAIL'}")
        print(f"Context Extraction: {'PASS' if test10 else 'FAIL'}")
        
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
