"""
Quality Test: Code Navigation
Code navigation system testleri.
"""

import sys
import os
import tempfile
import shutil
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.ai.code_navigation import (
    CodeNavigator,
    NavigationTarget,
    Reference,
    CallSite
)


def test_go_to_definition():
    """
    Test: Go to definition.
    """
    print("=" * 70)
    print("TEST: Go to Definition")
    print("=" * 70)
    
    navigator = CodeNavigator()
    
    # Codebase index olmadan test et
    result = navigator.go_to_definition(
        file_path="test.py",
        line=1,
        column=0,
        symbol_name="test_function"
    )
    
    # Codebase index olmadan None dönmeli
    assert result is None, "Codebase index olmadan None olmalı"
    print(f"  Result without codebase index: {result}")
    
    print("\n" + "=" * 70)
    print("PASS: Go to definition")
    print("=" * 70)


def test_find_references():
    """
    Test: Find references.
    """
    print("=" * 70)
    print("TEST: Find References")
    print("=" * 70)
    
    navigator = CodeNavigator()
    
    # Codebase index olmadan test et
    references = navigator.find_references(
        symbol_name="test_function",
        file_path=None
    )
    
    # Codebase index olmadan boş liste dönmeli
    assert isinstance(references, list), "List olmalı"
    print(f"  References without codebase index: {len(references)}")
    
    print("\n" + "=" * 70)
    print("PASS: Find references")
    print("=" * 70)


def test_go_to_implementation():
    """
    Test: Go to implementation.
    """
    print("=" * 70)
    print("TEST: Go to Implementation")
    print("=" * 70)
    
    navigator = CodeNavigator()
    
    # Codebase index olmadan test et
    result = navigator.go_to_implementation(symbol_name="test_function")
    
    # Codebase index olmadan None dönmeli
    assert result is None, "Codebase index olmadan None olmalı"
    print(f"  Result without codebase index: {result}")
    
    print("\n" + "=" * 70)
    print("PASS: Go to implementation")
    print("=" * 70)


def test_symbol_search():
    """
    Test: Symbol search.
    """
    print("=" * 70)
    print("TEST: Symbol Search")
    print("=" * 70)
    
    navigator = CodeNavigator()
    
    # Codebase index olmadan test et
    results = navigator.symbol_search(query="AgentLoop")
    
    # Codebase index olmadan boş liste dönmeli
    assert isinstance(results, list), "List olmalı"
    print(f"  Results without codebase index: {len(results)}")
    
    print("\n" + "=" * 70)
    print("PASS: Symbol search")
    print("=" * 70)


def test_file_outline():
    """
    Test: File outline.
    """
    print("=" * 70)
    print("TEST: File Outline")
    print("=" * 70)
    
    navigator = CodeNavigator()
    
    # Codebase index olmadan test et
    outline = navigator.get_file_outline(file_path="test.py")
    
    # Codebase index olmadan boş liste dönmeli
    assert isinstance(outline, list), "List olmalı"
    print(f"  Outline without codebase index: {len(outline)}")
    
    print("\n" + "=" * 70)
    print("PASS: File outline")
    print("=" * 70)


def test_call_hierarchy():
    """
    Test: Call hierarchy.
    """
    print("=" * 70)
    print("TEST: Call Hierarchy")
    print("=" * 70)
    
    navigator = CodeNavigator()
    
    # Callers
    callers = navigator.get_call_hierarchy(symbol_name="test_function", direction="callers")
    assert isinstance(callers, list), "List olmalı"
    print(f"  Callers without codebase index: {len(callers)}")
    
    # Callees
    callees = navigator.get_call_hierarchy(symbol_name="test_function", direction="callees")
    assert isinstance(callees, list), "List olmalı"
    print(f"  Callees without codebase index: {len(callees)}")
    
    print("\n" + "=" * 70)
    print("PASS: Call hierarchy")
    print("=" * 70)


def test_breadcrumbs():
    """
    Test: Breadcrumbs.
    """
    print("=" * 70)
    print("TEST: Breadcrumbs")
    print("=" * 70)
    
    navigator = CodeNavigator()
    
    # Codebase index olmadan test et
    breadcrumbs = navigator.get_breadcrumbs(file_path="test.py", line=10)
    
    # Codebase index olmadan boş liste dönmeli
    assert isinstance(breadcrumbs, list), "List olmalı"
    print(f"  Breadcrumbs without codebase index: {len(breadcrumbs)}")
    
    print("\n" + "=" * 70)
    print("PASS: Breadcrumbs")
    print("=" * 70)


def test_navigation_target():
    """
    Test: NavigationTarget dataclass.
    """
    print("=" * 70)
    print("TEST: NavigationTarget Dataclass")
    print("=" * 70)
    
    target = NavigationTarget(
        file_path="test.py",
        line=10,
        column=5,
        symbol_name="test_function",
        symbol_type="function",
        description="def test_function():"
    )
    
    assert target.file_path == "test.py", "File path eşleşmeli"
    assert target.line == 10, "Line eşleşmeli"
    assert target.column == 5, "Column eşleşmeli"
    assert target.symbol_name == "test_function", "Symbol name eşleşmeli"
    assert target.symbol_type == "function", "Symbol type eşleşmeli"
    
    print(f"  File path: {target.file_path}")
    print(f"  Line: {target.line}")
    print(f"  Symbol: {target.symbol_name}")
    
    print("\n" + "=" * 70)
    print("PASS: NavigationTarget dataclass")
    print("=" * 70)


def test_reference():
    """
    Test: Reference dataclass.
    """
    print("=" * 70)
    print("TEST: Reference Dataclass")
    print("=" * 70)
    
    ref = Reference(
        file_path="test.py",
        line=15,
        column=10,
        context="test_function()"
    )
    
    assert ref.file_path == "test.py", "File path eşleşmeli"
    assert ref.line == 15, "Line eşleşmeli"
    assert ref.column == 10, "Column eşleşmeli"
    assert ref.context == "test_function()", "Context eşleşmeli"
    
    print(f"  File path: {ref.file_path}")
    print(f"  Line: {ref.line}")
    print(f"  Context: {ref.context}")
    
    print("\n" + "=" * 70)
    print("PASS: Reference dataclass")
    print("=" * 70)


def test_call_site():
    """
    Test: CallSite dataclass.
    """
    print("=" * 70)
    print("TEST: CallSite Dataclass")
    print("=" * 70)
    
    call_site = CallSite(
        file_path="test.py",
        line=20,
        column=5,
        caller_function="main",
        callee_symbol="test_function"
    )
    
    assert call_site.file_path == "test.py", "File path eşleşmeli"
    assert call_site.line == 20, "Line eşleşmeli"
    assert call_site.caller_function == "main", "Caller function eşleşmeli"
    assert call_site.callee_symbol == "test_function", "Callee symbol eşleşmeli"
    
    print(f"  File path: {call_site.file_path}")
    print(f"  Caller: {call_site.caller_function}")
    print(f"  Callee: {call_site.callee_symbol}")
    
    print("\n" + "=" * 70)
    print("PASS: CallSite dataclass")
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
        
        # Codebase index ile navigator oluştur
        from app.ai.codebase_index import CodebaseIndex
        codebase_index = CodebaseIndex(project_root=Path(temp_dir))
        
        navigator = CodeNavigator(codebase_index=codebase_index)
        
        # Codebase index'in set edildiğini kontrol et
        assert navigator.codebase_index is not None, "Codebase index set olmalı"
        print(f"  Codebase index integrated: {navigator.codebase_index is not None}")
        
        # Symbol search dene
        results = navigator.symbol_search(query="my_function")
        assert isinstance(results, list), "Results list olmalı"
        print(f"  Symbol search results: {len(results)}")
        
        print("\n" + "=" * 70)
        print("PASS: Codebase index integration")
        print("=" * 70)
        
    finally:
        shutil.rmtree(temp_dir)


if __name__ == "__main__":
    try:
        test1 = test_go_to_definition()
        test2 = test_find_references()
        test3 = test_go_to_implementation()
        test4 = test_symbol_search()
        test5 = test_file_outline()
        test6 = test_call_hierarchy()
        test7 = test_breadcrumbs()
        test8 = test_navigation_target()
        test9 = test_reference()
        test10 = test_call_site()
        test11 = test_codebase_index_integration()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Go to Definition: {'PASS' if test1 else 'FAIL'}")
        print(f"Find References: {'PASS' if test2 else 'FAIL'}")
        print(f"Go to Implementation: {'PASS' if test3 else 'FAIL'}")
        print(f"Symbol Search: {'PASS' if test4 else 'FAIL'}")
        print(f"File Outline: {'PASS' if test5 else 'FAIL'}")
        print(f"Call Hierarchy: {'PASS' if test6 else 'FAIL'}")
        print(f"Breadcrumbs: {'PASS' if test7 else 'FAIL'}")
        print(f"NavigationTarget Dataclass: {'PASS' if test8 else 'FAIL'}")
        print(f"Reference Dataclass: {'PASS' if test9 else 'FAIL'}")
        print(f"CallSite Dataclass: {'PASS' if test10 else 'FAIL'}")
        print(f"Codebase Index Integration: {'PASS' if test11 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11])
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
