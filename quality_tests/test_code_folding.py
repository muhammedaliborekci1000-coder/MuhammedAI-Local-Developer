"""
Quality Test: Code Folding
Code folding system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.code_folding import (
    CodeFoldingEngine,
    FoldType,
    FoldState,
    FoldRegion,
    FoldResult
)


def test_detect_fold_regions():
    """
    Test: Detect fold regions.
    """
    print("=" * 70)
    print("TEST: Detect Fold Regions")
    print("=" * 70)
    
    engine = CodeFoldingEngine()
    
    code = """def my_function():
    x = 10
    y = 20
    return x + y

class MyClass:
    def __init__(self):
        self.value = 0
"""
    
    result = engine.detect_fold_regions(code, language="python")
    
    assert result.success, "Detection başarılı olmalı"
    assert len(result.fold_regions) > 0, "Region'lar bulunmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Regions detected: {len(result.fold_regions)}")
    print(f"  Message: {result.message}")
    
    for region in result.fold_regions:
        print(f"  - {region.fold_type.value}: {region.start_line}-{region.end_line}")
    
    print("\n" + "=" * 70)
    print("PASS: Detect fold regions")
    print("=" * 70)


def test_fold_region():
    """
    Test: Fold region.
    """
    print("=" * 70)
    print("TEST: Fold Region")
    print("=" * 70)
    
    engine = CodeFoldingEngine()
    
    code = """def my_function():
    x = 10
    y = 20
    return x + y
"""
    
    result = engine.fold_region(0, code, language="python")
    
    assert result.success, "Fold başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Fold region")
    print("=" * 70)


def test_unfold_region():
    """
    Test: Unfold region.
    """
    print("=" * 70)
    print("TEST: Unfold Region")
    print("=" * 70)
    
    engine = CodeFoldingEngine()
    
    code = """def my_function():
    x = 10
    y = 20
    return x + y
"""
    
    result = engine.unfold_region(0, code, language="python")
    
    assert result.success, "Unfold başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Unfold region")
    print("=" * 70)


def test_fold_all():
    """
    Test: Fold all.
    """
    print("=" * 70)
    print("TEST: Fold All")
    print("=" * 70)
    
    engine = CodeFoldingEngine()
    
    code = """def my_function():
    x = 10
    return x

class MyClass:
    def __init__(self):
        self.value = 0
"""
    
    result = engine.fold_all(code, language="python")
    
    assert result.success, "Fold all başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Fold all")
    print("=" * 70)


def test_unfold_all():
    """
    Test: Unfold all.
    """
    print("=" * 70)
    print("TEST: Unfold All")
    print("=" * 70)
    
    engine = CodeFoldingEngine()
    
    code = """def my_function():
    x = 10
    return x
"""
    
    result = engine.unfold_all(code, language="python")
    
    assert result.success, "Unfold all başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Unfold all")
    print("=" * 70)


def test_get_fold_regions():
    """
    Test: Get fold regions.
    """
    print("=" * 70)
    print("TEST: Get Fold Regions")
    print("=" * 70)
    
    engine = CodeFoldingEngine()
    
    code = """def my_function():
    x = 10
    return x
"""
    
    result = engine.get_fold_regions(code, language="python")
    
    assert result.success, "Get başarılı olmalı"
    assert len(result.fold_regions) > 0, "Region'lar olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Regions: {len(result.fold_regions)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get fold regions")
    print("=" * 70)


def test_get_fold_level():
    """
    Test: Get fold level.
    """
    print("=" * 70)
    print("TEST: Get Fold Level")
    print("=" * 70)
    
    engine = CodeFoldingEngine()
    
    code = """def my_function():
    x = 10
    return x
"""
    
    level = engine.get_fold_level(0, code, language="python")
    
    assert level >= 0, "Level 0 veya daha büyük olmalı"
    
    print(f"  Fold level: {level}")
    
    print("\n" + "=" * 70)
    print("PASS: Get fold level")
    print("=" * 70)


def test_toggle_fold():
    """
    Test: Toggle fold.
    """
    print("=" * 70)
    print("TEST: Toggle Fold")
    print("=" * 70)
    
    engine = CodeFoldingEngine()
    
    code = """def my_function():
    x = 10
    return x
"""
    
    result = engine.toggle_fold(0, code, language="python")
    
    assert result.success, "Toggle başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Toggle fold")
    print("=" * 70)


def test_fold_type_enum():
    """
    Test: FoldType enum.
    """
    print("=" * 70)
    print("TEST: FoldType Enum")
    print("=" * 70)
    
    assert FoldType.FUNCTION.value == "function"
    assert FoldType.CLASS.value == "class"
    assert FoldType.BLOCK.value == "block"
    assert FoldType.COMMENT.value == "comment"
    assert FoldType.REGION.value == "region"
    assert FoldType.IMPORT.value == "import"
    assert FoldType.IF_STATEMENT.value == "if_statement"
    assert FoldType.LOOP.value == "loop"
    assert FoldType.TRY_EXCEPT.value == "try_except"
    assert FoldType.WITH_STATEMENT.value == "with_statement"
    
    print(f"  All enum values verified")
    print(f"  Total types: {len(FoldType)}")
    
    print("\n" + "=" * 70)
    print("PASS: FoldType enum")
    print("=" * 70)


def test_fold_state_enum():
    """
    Test: FoldState enum.
    """
    print("=" * 70)
    print("TEST: FoldState Enum")
    print("=" * 70)
    
    assert FoldState.EXPANDED.value == "expanded"
    assert FoldState.COLLAPSED.value == "collapsed"
    
    print(f"  All enum values verified")
    print(f"  Total states: {len(FoldState)}")
    
    print("\n" + "=" * 70)
    print("PASS: FoldState enum")
    print("=" * 70)


def test_fold_region_dataclass():
    """
    Test: FoldRegion dataclass.
    """
    print("=" * 70)
    print("TEST: FoldRegion Dataclass")
    print("=" * 70)
    
    region = FoldRegion(
        start_line=0,
        end_line=5,
        fold_type=FoldType.FUNCTION,
        name="test_function",
        level=0
    )
    
    assert region.start_line == 0, "Start line eşleşmeli"
    assert region.end_line == 5, "End line eşleşmeli"
    assert region.fold_type == FoldType.FUNCTION, "Type eşleşmeli"
    
    print(f"  Start line: {region.start_line}")
    print(f"  End line: {region.end_line}")
    print(f"  Type: {region.fold_type.value}")
    print(f"  Name: {region.name}")
    
    print("\n" + "=" * 70)
    print("PASS: FoldRegion dataclass")
    print("=" * 70)


def test_fold_result_dataclass():
    """
    Test: FoldResult dataclass.
    """
    print("=" * 70)
    print("TEST: FoldResult Dataclass")
    print("=" * 70)
    
    result = FoldResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.fold_regions, list), "Fold regions list olmalı"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Fold regions: {len(result.fold_regions)}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: FoldResult dataclass")
    print("=" * 70)


def test_multiple_languages():
    """
    Test: Multiple languages.
    """
    print("=" * 70)
    print("TEST: Multiple Languages")
    print("=" * 70)
    
    engine = CodeFoldingEngine()
    
    # Python
    python_code = "def my_function():\n    pass"
    python_result = engine.detect_fold_regions(python_code, language="python")
    assert python_result.success, "Python detection başarılı olmalı"
    
    # JavaScript
    js_code = "function myFunction() {\n    pass\n}"
    js_result = engine.detect_fold_regions(js_code, language="javascript")
    assert js_result.success, "JavaScript detection başarılı olmalı"
    
    # HTML
    html_code = "<!-- comment -->"
    html_result = engine.detect_fold_regions(html_code, language="html")
    assert html_result.success, "HTML detection başarılı olmalı"
    
    print(f"  Python: {python_result.success}")
    print(f"  JavaScript: {js_result.success}")
    print(f"  HTML: {html_result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Multiple languages")
    print("=" * 70)


def test_nested_folding():
    """
    Test: Nested folding.
    """
    print("=" * 70)
    print("TEST: Nested Folding")
    print("=" * 70)
    
    engine = CodeFoldingEngine()
    
    code = """class MyClass:
    def __init__(self):
        self.value = 0
        
    def my_method(self):
        if True:
            pass
"""
    
    result = engine.detect_fold_regions(code, language="python")
    
    assert result.success, "Detection başarılı olmalı"
    
    # Check levels
    levels = [r.level for r in result.fold_regions]
    print(f"  Levels: {levels}")
    
    print("\n" + "=" * 70)
    print("PASS: Nested folding")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_detect_fold_regions()
        test2 = test_fold_region()
        test3 = test_unfold_region()
        test4 = test_fold_all()
        test5 = test_unfold_all()
        test6 = test_get_fold_regions()
        test7 = test_get_fold_level()
        test8 = test_toggle_fold()
        test9 = test_fold_type_enum()
        test10 = test_fold_state_enum()
        test11 = test_fold_region_dataclass()
        test12 = test_fold_result_dataclass()
        test13 = test_multiple_languages()
        test14 = test_nested_folding()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Detect Fold Regions: {'PASS' if test1 else 'FAIL'}")
        print(f"Fold Region: {'PASS' if test2 else 'FAIL'}")
        print(f"Unfold Region: {'PASS' if test3 else 'FAIL'}")
        print(f"Fold All: {'PASS' if test4 else 'FAIL'}")
        print(f"Unfold All: {'PASS' if test5 else 'FAIL'}")
        print(f"Get Fold Regions: {'PASS' if test6 else 'FAIL'}")
        print(f"Get Fold Level: {'PASS' if test7 else 'FAIL'}")
        print(f"Toggle Fold: {'PASS' if test8 else 'FAIL'}")
        print(f"FoldType Enum: {'PASS' if test9 else 'FAIL'}")
        print(f"FoldState Enum: {'PASS' if test10 else 'FAIL'}")
        print(f"FoldRegion Dataclass: {'PASS' if test11 else 'FAIL'}")
        print(f"FoldResult Dataclass: {'PASS' if test12 else 'FAIL'}")
        print(f"Multiple Languages: {'PASS' if test13 else 'FAIL'}")
        print(f"Nested Folding: {'PASS' if test14 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14])
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
