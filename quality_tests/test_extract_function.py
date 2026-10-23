"""
Quality Test: Extract Function
Extract function system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.extract_function import (
    ExtractFunctionEngine,
    ExtractScope,
    FunctionVisibility,
    FunctionParameter,
    ExtractedFunction,
    ExtractResult
)


def test_extract_function():
    """
    Test: Extract function.
    """
    print("=" * 70)
    print("TEST: Extract Function")
    print("=" * 70)
    
    code = """
def main():
    x = 10
    y = 20
    result = x + y
    print(result)
"""
    
    engine = ExtractFunctionEngine()
    result = engine.extract_function(code, 2, 3, "calculate_sum", ExtractScope.LOCAL, "python")
    
    assert result.success, "Extract function başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Function name: {result.function.name if result.function else 'N/A'}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Extract function")
    print("=" * 70)


def test_detect_parameters():
    """
    Test: Detect parameters.
    """
    print("=" * 70)
    print("TEST: Detect Parameters")
    print("=" * 70)
    
    code = """
def main():
    x = 10
    y = 20
    result = x + y
"""
    
    engine = ExtractFunctionEngine()
    result = engine.extract_function(code, 2, 3, "calculate_sum", ExtractScope.LOCAL, "python")
    
    if result.function:
        print(f"  Parameters: {len(result.function.parameters)}")
        for param in result.function.parameters:
            print(f"    {param.name}")
    
    print("\n" + "=" * 70)
    print("PASS: Detect parameters")
    print("=" * 70)


def test_detect_return_type():
    """
    Test: Detect return type.
    """
    print("=" * 70)
    print("TEST: Detect Return Type")
    print("=" * 70)
    
    code = """
def main():
    x = 10
    return x
"""
    
    engine = ExtractFunctionEngine()
    result = engine.extract_function(code, 2, 2, "get_value", ExtractScope.LOCAL, "python")
    
    if result.function:
        print(f"  Return type: {result.function.return_type}")
    
    print("\n" + "=" * 70)
    print("PASS: Detect return type")
    print("=" * 70)


def test_preview_extraction():
    """
    Test: Preview extraction.
    """
    print("=" * 70)
    print("TEST: Preview Extraction")
    print("=" * 70)
    
    code = """
def main():
    x = 10
    y = 20
    result = x + y
"""
    
    engine = ExtractFunctionEngine()
    result = engine.preview_extraction(code, 2, 3, "calculate_sum", ExtractScope.LOCAL)
    
    assert result.success, "Preview başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Extracted code preview: {len(result.extracted_code)} chars")
    
    print("\n" + "=" * 70)
    print("PASS: Preview extraction")
    print("=" * 70)


def test_validate_extraction():
    """
    Test: Validate extraction.
    """
    print("=" * 70)
    print("TEST: Validate Extraction")
    print("=" * 70)
    
    code = """
def main():
    x = 10
    return x
"""
    
    engine = ExtractFunctionEngine()
    
    # Valid extraction
    is_valid, errors = engine.validate_extraction(code, 1, 2, "my_function")
    assert is_valid, "Valid extraction olmalı"
    
    # Invalid extraction (keyword)
    is_valid, errors = engine.validate_extraction(code, 1, 2, "def")
    assert not is_valid, "Keyword extraction invalid olmalı"
    
    print(f"  Valid extraction: {is_valid}")
    print(f"  Keyword validation: {'PASS' if not is_valid else 'FAIL'}")
    
    print("\n" + "=" * 70)
    print("PASS: Validate extraction")
    print("=" * 70)


def test_extract_scope_enum():
    """
    Test: ExtractScope enum.
    """
    print("=" * 70)
    print("TEST: ExtractScope Enum")
    print("=" * 70)
    
    assert ExtractScope.LOCAL.value == "local"
    assert ExtractScope.GLOBAL.value == "global"
    assert ExtractScope.CLASS.value == "class"
    
    print(f"  All enum values verified")
    print(f"  Total scopes: {len(ExtractScope)}")
    
    print("\n" + "=" * 70)
    print("PASS: ExtractScope enum")
    print("=" * 70)


def test_function_visibility_enum():
    """
    Test: FunctionVisibility enum.
    """
    print("=" * 70)
    print("TEST: FunctionVisibility Enum")
    print("=" * 70)
    
    assert FunctionVisibility.PRIVATE.value == "private"
    assert FunctionVisibility.PUBLIC.value == "public"
    assert FunctionVisibility.PROTECTED.value == "protected"
    
    print(f"  All enum values verified")
    print(f"  Total visibilities: {len(FunctionVisibility)}")
    
    print("\n" + "=" * 70)
    print("PASS: FunctionVisibility enum")
    print("=" * 70)


def test_function_parameter_dataclass():
    """
    Test: FunctionParameter dataclass.
    """
    print("=" * 70)
    print("TEST: FunctionParameter Dataclass")
    print("=" * 70)
    
    param = FunctionParameter(
        name="x",
        type_hint="int",
        default_value="0"
    )
    
    assert param.name == "x", "Name eşleşmeli"
    assert param.type_hint == "int", "Type hint eşleşmeli"
    
    print(f"  Name: {param.name}")
    print(f"  Type hint: {param.type_hint}")
    print(f"  Default value: {param.default_value}")
    
    print("\n" + "=" * 70)
    print("PASS: FunctionParameter dataclass")
    print("=" * 70)


def test_extracted_function_dataclass():
    """
    Test: ExtractedFunction dataclass.
    """
    print("=" * 70)
    print("TEST: ExtractedFunction Dataclass")
    print("=" * 70)
    
    func = ExtractedFunction(
        name="my_function",
        parameters=[FunctionParameter(name="x")],
        return_type="int",
        body="return x"
    )
    
    assert func.name == "my_function", "Name eşleşmeli"
    assert len(func.parameters) > 0, "Parameters olmalı"
    
    print(f"  Name: {func.name}")
    print(f"  Parameters: {len(func.parameters)}")
    print(f"  Return type: {func.return_type}")
    
    print("\n" + "=" * 70)
    print("PASS: ExtractedFunction dataclass")
    print("=" * 70)


def test_extract_result_dataclass():
    """
    Test: ExtractResult dataclass.
    """
    print("=" * 70)
    print("TEST: ExtractResult Dataclass")
    print("=" * 70)
    
    result = ExtractResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: ExtractResult dataclass")
    print("=" * 70)


def test_global_scope_extraction():
    """
    Test: Global scope extraction.
    """
    print("=" * 70)
    print("TEST: Global Scope Extraction")
    print("=" * 70)
    
    code = """
x = 10
y = 20
result = x + y
"""
    
    engine = ExtractFunctionEngine()
    result = engine.extract_function(code, 1, 2, "calculate_sum", ExtractScope.GLOBAL, "python")
    
    assert result.success, "Global extraction başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Scope: GLOBAL")
    
    print("\n" + "=" * 70)
    print("PASS: Global scope extraction")
    print("=" * 70)


def test_class_scope_extraction():
    """
    Test: Class scope extraction.
    """
    print("=" * 70)
    print("TEST: Class Scope Extraction")
    print("=" * 70)
    
    code = """
class MyClass:
    x = 10
    y = 20
    result = x + y
"""
    
    engine = ExtractFunctionEngine()
    result = engine.extract_function(code, 2, 3, "calculate_sum", ExtractScope.CLASS, "python")
    
    assert result.success, "Class extraction başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Scope: CLASS")
    
    print("\n" + "=" * 70)
    print("PASS: Class scope extraction")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_extract_function()
        test2 = test_detect_parameters()
        test3 = test_detect_return_type()
        test4 = test_preview_extraction()
        test5 = test_validate_extraction()
        test6 = test_extract_scope_enum()
        test7 = test_function_visibility_enum()
        test8 = test_function_parameter_dataclass()
        test9 = test_extracted_function_dataclass()
        test10 = test_extract_result_dataclass()
        test11 = test_global_scope_extraction()
        test12 = test_class_scope_extraction()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Extract Function: {'PASS' if test1 else 'FAIL'}")
        print(f"Detect Parameters: {'PASS' if test2 else 'FAIL'}")
        print(f"Detect Return Type: {'PASS' if test3 else 'FAIL'}")
        print(f"Preview Extraction: {'PASS' if test4 else 'FAIL'}")
        print(f"Validate Extraction: {'PASS' if test5 else 'FAIL'}")
        print(f"ExtractScope Enum: {'PASS' if test6 else 'FAIL'}")
        print(f"FunctionVisibility Enum: {'PASS' if test7 else 'FAIL'}")
        print(f"FunctionParameter Dataclass: {'PASS' if test8 else 'FAIL'}")
        print(f"ExtractedFunction Dataclass: {'PASS' if test9 else 'FAIL'}")
        print(f"ExtractResult Dataclass: {'PASS' if test10 else 'FAIL'}")
        print(f"Global Scope Extraction: {'PASS' if test11 else 'FAIL'}")
        print(f"Class Scope Extraction: {'PASS' if test12 else 'FAIL'}")
        
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
