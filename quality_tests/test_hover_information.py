"""
Quality Test: Hover Information
Hover information system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.hover_information import (
    HoverInformationEngine,
    HoverKind,
    HoverContent,
    HoverResult
)


def test_get_hover_info():
    """
    Test: Get hover info.
    """
    print("=" * 70)
    print("TEST: Get Hover Info")
    print("=" * 70)
    
    code = """
def my_function():
    return "Hello"
"""
    
    engine = HoverInformationEngine()
    position = code.find("my_function")
    result = engine.get_hover_info(code, position, "python")
    
    assert result.success, "Hover başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    if result.content:
        print(f"  Text: {result.content.text}")
        print(f"  Kind: {result.content.kind.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Get hover info")
    print("=" * 70)


def test_function_hover():
    """
    Test: Function hover.
    """
    print("=" * 70)
    print("TEST: Function Hover")
    print("=" * 70)
    
    code = """
def my_function(x, y):
    \"\"\"This is a docstring.\"\"\"
    return x + y
"""
    
    engine = HoverInformationEngine()
    position = code.find("my_function")
    result = engine.get_hover_info(code, position, "python")
    
    assert result.success, "Hover başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Kind: {result.content.kind.value if result.content else None}")
    print(f"  Documentation: {result.content.documentation if result.content else None}")
    
    print("\n" + "=" * 70)
    print("PASS: Function hover")
    print("=" * 70)


def test_class_hover():
    """
    Test: Class hover.
    """
    print("=" * 70)
    print("TEST: Class Hover")
    print("=" * 70)
    
    code = """
class MyClass:
    \"\"\"This is a class.\"\"\"
    pass
"""
    
    engine = HoverInformationEngine()
    position = code.find("MyClass")
    result = engine.get_hover_info(code, position, "python")
    
    assert result.success, "Hover başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Kind: {result.content.kind.value if result.content else None}")
    
    print("\n" + "=" * 70)
    print("PASS: Class hover")
    print("=" * 70)


def test_variable_hover():
    """
    Test: Variable hover.
    """
    print("=" * 70)
    print("TEST: Variable Hover")
    print("=" * 70)
    
    code = """
x = 42
print(x)
"""
    
    engine = HoverInformationEngine()
    position = code.find("x")
    result = engine.get_hover_info(code, position, "python")
    
    assert result.success, "Hover başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Kind: {result.content.kind.value if result.content else None}")
    
    print("\n" + "=" * 70)
    print("PASS: Variable hover")
    print("=" * 70)


def test_keyword_hover():
    """
    Test: Keyword hover.
    """
    print("=" * 70)
    print("TEST: Keyword Hover")
    print("=" * 70)
    
    code = """
def my_function():
    return "Hello"
"""
    
    engine = HoverInformationEngine()
    position = code.find("def")
    result = engine.get_hover_info(code, position, "python")
    
    assert result.success, "Hover başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Kind: {result.content.kind.value if result.content else None}")
    
    print("\n" + "=" * 70)
    print("PASS: Keyword hover")
    print("=" * 70)


def test_get_hover_for_symbol():
    """
    Test: Get hover for symbol.
    """
    print("=" * 70)
    print("TEST: Get Hover for Symbol")
    print("=" * 70)
    
    engine = HoverInformationEngine()
    
    content = engine.get_hover_for_symbol(
        symbol="my_function",
        symbol_type=HoverKind.FUNCTION,
        documentation="This is a function",
        type_info="def my_function() -> None"
    )
    
    assert content is not None, "Content oluşturulmalı"
    assert content.text == "my_function", "Text eşleşmeli"
    
    print(f"  Text: {content.text}")
    print(f"  Kind: {content.kind.value}")
    print(f"  Documentation: {content.documentation}")
    
    print("\n" + "=" * 70)
    print("PASS: Get hover for symbol")
    print("=" * 70)


def test_hover_kind_enum():
    """
    Test: HoverKind enum.
    """
    print("=" * 70)
    print("TEST: HoverKind Enum")
    print("=" * 70)
    
    assert HoverKind.VARIABLE.value == "variable"
    assert HoverKind.FUNCTION.value == "function"
    assert HoverKind.CLASS.value == "class"
    assert HoverKind.METHOD.value == "method"
    assert HoverKind.PARAMETER.value == "parameter"
    assert HoverKind.MODULE.value == "module"
    assert HoverKind.IMPORT.value == "import"
    assert HoverKind.KEYWORD.value == "keyword"
    assert HoverKind.STRING.value == "string"
    assert HoverKind.NUMBER.value == "number"
    assert HoverKind.COMMENT.value == "comment"
    
    print(f"  All enum values verified")
    print(f"  Total kinds: {len(HoverKind)}")
    
    print("\n" + "=" * 70)
    print("PASS: HoverKind enum")
    print("=" * 70)


def test_hover_content_dataclass():
    """
    Test: HoverContent dataclass.
    """
    print("=" * 70)
    print("TEST: HoverContent Dataclass")
    print("=" * 70)
    
    content = HoverContent(
        text="my_function",
        kind=HoverKind.FUNCTION,
        documentation="This is a function",
        type_info="def my_function() -> None"
    )
    
    assert content.text == "my_function", "Text eşleşmeli"
    assert content.kind == HoverKind.FUNCTION, "Kind eşleşmeli"
    
    print(f"  Text: {content.text}")
    print(f"  Kind: {content.kind.value}")
    print(f"  Documentation: {content.documentation}")
    
    print("\n" + "=" * 70)
    print("PASS: HoverContent dataclass")
    print("=" * 70)


def test_hover_result_dataclass():
    """
    Test: HoverResult dataclass.
    """
    print("=" * 70)
    print("TEST: HoverResult Dataclass")
    print("=" * 70)
    
    result = HoverResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: HoverResult dataclass")
    print("=" * 70)


def test_type_info_extraction():
    """
    Test: Type info extraction.
    """
    print("=" * 70)
    print("TEST: Type Info Extraction")
    print("=" * 70)
    
    code = """
def my_function(x: int, y: str) -> bool:
    return True
"""
    
    engine = HoverInformationEngine()
    position = code.find("my_function")
    result = engine.get_hover_info(code, position, "python")
    
    assert result.success, "Hover başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Type info: {result.content.type_info if result.content else None}")
    
    print("\n" + "=" * 70)
    print("PASS: Type info extraction")
    print("=" * 70)


def test_documentation_extraction():
    """
    Test: Documentation extraction.
    """
    print("=" * 70)
    print("TEST: Documentation Extraction")
    print("=" * 70)
    
    code = """
def my_function():
    \"\"\"This is a docstring.\"\"\"
    pass
"""
    
    engine = HoverInformationEngine()
    position = code.find("my_function")
    result = engine.get_hover_info(code, position, "python")
    
    assert result.success, "Hover başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Documentation: {result.content.documentation if result.content else None}")
    
    print("\n" + "=" * 70)
    print("PASS: Documentation extraction")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_get_hover_info()
        test2 = test_function_hover()
        test3 = test_class_hover()
        test4 = test_variable_hover()
        test5 = test_keyword_hover()
        test6 = test_get_hover_for_symbol()
        test7 = test_hover_kind_enum()
        test8 = test_hover_content_dataclass()
        test9 = test_hover_result_dataclass()
        test10 = test_type_info_extraction()
        test11 = test_documentation_extraction()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Get Hover Info: {'PASS' if test1 else 'FAIL'}")
        print(f"Function Hover: {'PASS' if test2 else 'FAIL'}")
        print(f"Class Hover: {'PASS' if test3 else 'FAIL'}")
        print(f"Variable Hover: {'PASS' if test4 else 'FAIL'}")
        print(f"Keyword Hover: {'PASS' if test5 else 'FAIL'}")
        print(f"Get Hover for Symbol: {'PASS' if test6 else 'FAIL'}")
        print(f"HoverKind Enum: {'PASS' if test7 else 'FAIL'}")
        print(f"HoverContent Dataclass: {'PASS' if test8 else 'FAIL'}")
        print(f"HoverResult Dataclass: {'PASS' if test9 else 'FAIL'}")
        print(f"Type Info Extraction: {'PASS' if test10 else 'FAIL'}")
        print(f"Documentation Extraction: {'PASS' if test11 else 'FAIL'}")
        
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
