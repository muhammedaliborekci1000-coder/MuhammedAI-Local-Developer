"""
Quality Test: Code Explanation
Code explanation system testleri.
"""

import sys
import os
import tempfile
import shutil
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.ai.code_explanation import (
    CodeExplainer,
    ExplanationType,
    ExplanationDetail,
    CodeExplanation,
    ExplanationResult
)


def test_explain_function():
    """
    Test: Explain function.
    """
    print("=" * 70)
    print("TEST: Explain Function")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp(prefix="muhammedai_test_")
    
    try:
        # Test dosyası oluştur
        test_file = Path(temp_dir) / "test_module.py"
        test_file.write_text("""
def my_function(x, y):
    return x + y
""", encoding='utf-8')
        
        explainer = CodeExplainer()
        
        # Explain function
        result = explainer.explain_function("my_function", str(test_file))
        
        assert result.success, "Explanation başarılı olmalı"
        assert result.explanation is not None, "Explanation olmalı"
        assert result.explanation.type == ExplanationType.FUNCTION, "Function type olmalı"
        assert "my_function" in result.explanation.summary, "Function name içermeli"
        
        print(f"  Success: {result.success}")
        print(f"  Summary: {result.explanation.summary}")
        print(f"  Message: {result.message}")
        
        print("\n" + "=" * 70)
        print("PASS: Explain function")
        print("=" * 70)
        
    finally:
        shutil.rmtree(temp_dir)


def test_explain_class():
    """
    Test: Explain class.
    """
    print("=" * 70)
    print("TEST: Explain Class")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp(prefix="muhammedai_test_")
    
    try:
        # Test dosyası oluştur
        test_file = Path(temp_dir) / "test_module.py"
        test_file.write_text("""
class MyClass:
    def method(self):
        pass
""", encoding='utf-8')
        
        explainer = CodeExplainer()
        
        # Explain class
        result = explainer.explain_class("MyClass", str(test_file))
        
        assert result.success, "Explanation başarılı olmalı"
        assert result.explanation is not None, "Explanation olmalı"
        assert result.explanation.type == ExplanationType.CLASS, "Class type olmalı"
        
        print(f"  Success: {result.success}")
        print(f"  Summary: {result.explanation.summary}")
        print(f"  Message: {result.message}")
        
        print("\n" + "=" * 70)
        print("PASS: Explain class")
        print("=" * 70)
        
    finally:
        shutil.rmtree(temp_dir)


def test_explain_module():
    """
    Test: Explain module.
    """
    print("=" * 70)
    print("TEST: Explain Module")
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
        
        explainer = CodeExplainer()
        
        # Explain module
        result = explainer.explain_module(str(test_file))
        
        assert result.success, "Explanation başarılı olmalı"
        assert result.explanation is not None, "Explanation olmalı"
        assert result.explanation.type == ExplanationType.MODULE, "Module type olmalı"
        
        print(f"  Success: {result.success}")
        print(f"  Summary: {result.explanation.summary}")
        print(f"  Message: {result.message}")
        
        print("\n" + "=" * 70)
        print("PASS: Explain module")
        print("=" * 70)
        
    finally:
        shutil.rmtree(temp_dir)


def test_explain_line():
    """
    Test: Explain line.
    """
    print("=" * 70)
    print("TEST: Explain Line")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp(prefix="muhammedai_test_")
    
    try:
        # Test dosyası oluştur
        test_file = Path(temp_dir) / "test_module.py"
        test_file.write_text("""
def my_function():
    x = 10
    return x
""", encoding='utf-8')
        
        explainer = CodeExplainer()
        
        # Explain line
        result = explainer.explain_line(str(test_file), line=2)
        
        assert result.success, "Explanation başarılı olmalı"
        assert result.explanation is not None, "Explanation olmalı"
        assert result.explanation.type == ExplanationType.LINE, "Line type olmalı"
        
        print(f"  Success: {result.success}")
        print(f"  Summary: {result.explanation.summary}")
        print(f"  Message: {result.message}")
        
        print("\n" + "=" * 70)
        print("PASS: Explain line")
        print("=" * 70)
        
    finally:
        shutil.rmtree(temp_dir)


def test_explanation_type_enum():
    """
    Test: ExplanationType enum.
    """
    print("=" * 70)
    print("TEST: ExplanationType Enum")
    print("=" * 70)
    
    assert ExplanationType.FUNCTION.value == "function"
    assert ExplanationType.CLASS.value == "class"
    assert ExplanationType.MODULE.value == "module"
    assert ExplanationType.LINE.value == "line"
    assert ExplanationType.CONCEPT.value == "concept"
    
    print(f"  All enum values verified")
    print(f"  Total types: {len(ExplanationType)}")
    
    print("\n" + "=" * 70)
    print("PASS: ExplanationType enum")
    print("=" * 70)


def test_explanation_detail_enum():
    """
    Test: ExplanationDetail enum.
    """
    print("=" * 70)
    print("TEST: ExplanationDetail Enum")
    print("=" * 70)
    
    assert ExplanationDetail.SIMPLE.value == "simple"
    assert ExplanationDetail.DETAILED.value == "detailed"
    assert ExplanationDetail.TECHNICAL.value == "technical"
    
    print(f"  All enum values verified")
    print(f"  Total details: {len(ExplanationDetail)}")
    
    print("\n" + "=" * 70)
    print("PASS: ExplanationDetail enum")
    print("=" * 70)


def test_code_explanation_dataclass():
    """
    Test: CodeExplanation dataclass.
    """
    print("=" * 70)
    print("TEST: CodeExplanation Dataclass")
    print("=" * 70)
    
    explanation = CodeExplanation(
        type=ExplanationType.FUNCTION,
        detail=ExplanationDetail.DETAILED,
        summary="Test summary",
        description="Test description"
    )
    
    assert explanation.type == ExplanationType.FUNCTION, "Type eşleşmeli"
    assert explanation.detail == ExplanationDetail.DETAILED, "Detail eşleşmeli"
    assert explanation.summary == "Test summary", "Summary eşleşmeli"
    
    print(f"  Type: {explanation.type.value}")
    print(f"  Detail: {explanation.detail.value}")
    print(f"  Summary: {explanation.summary}")
    
    print("\n" + "=" * 70)
    print("PASS: CodeExplanation dataclass")
    print("=" * 70)


def test_explanation_result_dataclass():
    """
    Test: ExplanationResult dataclass.
    """
    print("=" * 70)
    print("TEST: ExplanationResult Dataclass")
    print("=" * 70)
    
    result = ExplanationResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: ExplanationResult dataclass")
    print("=" * 70)


def test_complexity_calculation():
    """
    Test: Complexity calculation.
    """
    print("=" * 70)
    print("TEST: Complexity Calculation")
    print("=" * 70)
    
    import ast
    code = """
def my_function(x):
    if x > 0:
        for i in range(10):
            if i % 2 == 0:
                return i
    return 0
"""
    tree = ast.parse(code)
    func_node = tree.body[0]
    
    explainer = CodeExplainer()
    complexity = explainer._calculate_complexity(func_node)
    
    assert complexity in ["Low", "Medium", "High"], "Valid complexity olmalı"
    print(f"  Complexity: {complexity}")
    
    print("\n" + "=" * 70)
    print("PASS: Complexity calculation")
    print("=" * 70)


def test_data_flow_analysis():
    """
    Test: Data flow analysis.
    """
    print("=" * 70)
    print("TEST: Data Flow Analysis")
    print("=" * 70)
    
    import ast
    code = "def my_function(x, y):\n    return x + y\n"
    tree = ast.parse(code)
    func_node = tree.body[0]
    
    explainer = CodeExplainer()
    data_flow = explainer._analyze_data_flow(func_node)
    
    assert data_flow is not None, "Data flow olmalı"
    assert "Input" in data_flow, "Input içermeli"
    print(f"  Data flow: {data_flow}")
    
    print("\n" + "=" * 70)
    print("PASS: Data flow analysis")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_explain_function()
        test2 = test_explain_class()
        test3 = test_explain_module()
        test4 = test_explain_line()
        test5 = test_explanation_type_enum()
        test6 = test_explanation_detail_enum()
        test7 = test_code_explanation_dataclass()
        test8 = test_explanation_result_dataclass()
        test9 = test_complexity_calculation()
        test10 = test_data_flow_analysis()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Explain Function: {'PASS' if test1 else 'FAIL'}")
        print(f"Explain Class: {'PASS' if test2 else 'FAIL'}")
        print(f"Explain Module: {'PASS' if test3 else 'FAIL'}")
        print(f"Explain Line: {'PASS' if test4 else 'FAIL'}")
        print(f"ExplanationType Enum: {'PASS' if test5 else 'FAIL'}")
        print(f"ExplanationDetail Enum: {'PASS' if test6 else 'FAIL'}")
        print(f"CodeExplanation Dataclass: {'PASS' if test7 else 'FAIL'}")
        print(f"ExplanationResult Dataclass: {'PASS' if test8 else 'FAIL'}")
        print(f"Complexity Calculation: {'PASS' if test9 else 'FAIL'}")
        print(f"Data Flow Analysis: {'PASS' if test10 else 'FAIL'}")
        
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
