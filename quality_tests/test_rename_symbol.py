"""
Quality Test: Rename Symbol
Rename symbol system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.rename_symbol import (
    RenameSymbolEngine,
    RenameScope,
    SymbolKind,
    SymbolReference,
    RenameEdit,
    RenameResult
)


def test_prepare_rename():
    """
    Test: Prepare rename.
    """
    print("=" * 70)
    print("TEST: Prepare Rename")
    print("=" * 70)
    
    code = """
def my_function():
    x = 42
    return x
"""
    
    engine = RenameSymbolEngine()
    position = code.find("x")
    result = engine.prepare_rename(code, position, "test.py", "python")
    
    assert result.success, "Prepare rename başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Total references: {result.total_references}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Prepare rename")
    print("=" * 70)


def test_find_python_references():
    """
    Test: Find Python references.
    """
    print("=" * 70)
    print("TEST: Find Python References")
    print("=" * 70)
    
    code = """
def my_function():
    x = 42
    return x
"""
    
    engine = RenameSymbolEngine()
    position = code.find("x")
    result = engine.prepare_rename(code, position, "test.py", "python")
    
    assert result.success, "References bulunmalı"
    assert result.total_references > 0, "Referanslar olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  References: {result.total_references}")
    
    for ref in result.references:
        print(f"    Line {ref.line}: {ref.is_definition}")
    
    print("\n" + "=" * 70)
    print("PASS: Find Python references")
    print("=" * 70)


def test_apply_rename():
    """
    Test: Apply rename.
    """
    print("=" * 70)
    print("TEST: Apply Rename")
    print("=" * 70)
    
    code = """
def my_function():
    x = 42
    return x
"""
    
    engine = RenameSymbolEngine()
    position = code.find("x")
    prepare_result = engine.prepare_rename(code, position, "test.py", "python")
    
    if prepare_result.references:
        fixed_code, result = engine.apply_rename(
            code,
            "x",
            "y",
            prepare_result.references,
            "test.py"
        )
        
        assert result.success, "Rename uygulanmalı"
        assert "y" in fixed_code, "Yeni isim kodda olmalı"
        
        print(f"  Success: {result.success}")
        print(f"  Message: {result.message}")
        print(f"  Edits: {len(result.edits)}")
    
    print("\n" + "=" * 70)
    print("PASS: Apply rename")
    print("=" * 70)


def test_validate_rename():
    """
    Test: Validate rename.
    """
    print("=" * 70)
    print("TEST: Validate Rename")
    print("=" * 70)
    
    code = """
def my_function():
    x = 42
    return x
"""
    
    engine = RenameSymbolEngine()
    
    # Valid rename
    is_valid, errors = engine.validate_rename("x", "y", code)
    assert is_valid, "Valid rename olmalı"
    
    # Invalid rename (keyword)
    is_valid, errors = engine.validate_rename("x", "def", code)
    assert not is_valid, "Keyword rename invalid olmalı"
    
    print(f"  Valid rename: {is_valid}")
    print(f"  Keyword validation: {'PASS' if not is_valid else 'FAIL'}")
    
    print("\n" + "=" * 70)
    print("PASS: Validate rename")
    print("=" * 70)


def test_get_rename_preview():
    """
    Test: Get rename preview.
    """
    print("=" * 70)
    print("TEST: Get Rename Preview")
    print("=" * 70)
    
    code = """
def my_function():
    x = 42
    return x
"""
    
    engine = RenameSymbolEngine()
    position = code.find("x")
    prepare_result = engine.prepare_rename(code, position, "test.py", "python")
    
    if prepare_result.references:
        preview = engine.get_rename_preview(
            code,
            "x",
            "y",
            prepare_result.references
        )
        
        assert len(preview) > 0, "Preview olmalı"
        
        print(f"  Preview items: {len(preview)}")
        for line, old_line, new_line in preview:
            print(f"    Line {line}: '{old_line}' -> '{new_line}'")
    
    print("\n" + "=" * 70)
    print("PASS: Get rename preview")
    print("=" * 70)


def test_rename_scope_enum():
    """
    Test: RenameScope enum.
    """
    print("=" * 70)
    print("TEST: RenameScope Enum")
    print("=" * 70)
    
    assert RenameScope.LOCAL.value == "local"
    assert RenameScope.FILE.value == "file"
    assert RenameScope.PROJECT.value == "project"
    
    print(f"  All enum values verified")
    print(f"  Total scopes: {len(RenameScope)}")
    
    print("\n" + "=" * 70)
    print("PASS: RenameScope enum")
    print("=" * 70)


def test_symbol_kind_enum():
    """
    Test: SymbolKind enum.
    """
    print("=" * 70)
    print("TEST: SymbolKind Enum")
    print("=" * 70)
    
    assert SymbolKind.VARIABLE.value == "variable"
    assert SymbolKind.FUNCTION.value == "function"
    assert SymbolKind.CLASS.value == "class"
    assert SymbolKind.METHOD.value == "method"
    assert SymbolKind.PARAMETER.value == "parameter"
    assert SymbolKind.ATTRIBUTE.value == "attribute"
    assert SymbolKind.IMPORT.value == "import"
    
    print(f"  All enum values verified")
    print(f"  Total kinds: {len(SymbolKind)}")
    
    print("\n" + "=" * 70)
    print("PASS: SymbolKind enum")
    print("=" * 70)


def test_symbol_reference_dataclass():
    """
    Test: SymbolReference dataclass.
    """
    print("=" * 70)
    print("TEST: SymbolReference Dataclass")
    print("=" * 70)
    
    ref = SymbolReference(
        file_path="test.py",
        line=1,
        column=0,
        end_line=1,
        end_column=5,
        is_definition=True
    )
    
    assert ref.file_path == "test.py", "File path eşleşmeli"
    assert ref.is_definition == True, "Is definition eşleşmeli"
    
    print(f"  File path: {ref.file_path}")
    print(f"  Line: {ref.line}")
    print(f"  Is definition: {ref.is_definition}")
    
    print("\n" + "=" * 70)
    print("PASS: SymbolReference dataclass")
    print("=" * 70)


def test_rename_edit_dataclass():
    """
    Test: RenameEdit dataclass.
    """
    print("=" * 70)
    print("TEST: RenameEdit Dataclass")
    print("=" * 70)
    
    edit = RenameEdit(
        file_path="test.py",
        start_line=1,
        start_column=0,
        end_line=1,
        end_column=5,
        old_name="x",
        new_name="y"
    )
    
    assert edit.old_name == "x", "Old name eşleşmeli"
    assert edit.new_name == "y", "New name eşleşmeli"
    
    print(f"  Old name: {edit.old_name}")
    print(f"  New name: {edit.new_name}")
    print(f"  File path: {edit.file_path}")
    
    print("\n" + "=" * 70)
    print("PASS: RenameEdit dataclass")
    print("=" * 70)


def test_rename_result_dataclass():
    """
    Test: RenameResult dataclass.
    """
    print("=" * 70)
    print("TEST: RenameResult Dataclass")
    print("=" * 70)
    
    result = RenameResult(success=True)
    result.old_name = "x"
    result.new_name = "y"
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.old_name == "x", "Old name eşleşmeli"
    assert result.new_name == "y", "New name eşleşmeli"
    assert isinstance(result.references, list), "References list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Old name: {result.old_name}")
    print(f"  New name: {result.new_name}")
    print(f"  References: {len(result.references)}")
    
    print("\n" + "=" * 70)
    print("PASS: RenameResult dataclass")
    print("=" * 70)


def test_function_rename():
    """
    Test: Function rename.
    """
    print("=" * 70)
    print("TEST: Function Rename")
    print("=" * 70)
    
    code = """
def my_function():
    return "Hello"

result = my_function()
"""
    
    engine = RenameSymbolEngine()
    position = code.find("my_function")
    result = engine.prepare_rename(code, position, "test.py", "python")
    
    assert result.success, "Prepare rename başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Total references: {result.total_references}")
    
    print("\n" + "=" * 70)
    print("PASS: Function rename")
    print("=" * 70)


def test_class_rename():
    """
    Test: Class rename.
    """
    print("=" * 70)
    print("TEST: Class Rename")
    print("=" * 70)
    
    code = """
class MyClass:
    pass

obj = MyClass()
"""
    
    engine = RenameSymbolEngine()
    position = code.find("MyClass")
    result = engine.prepare_rename(code, position, "test.py", "python")
    
    assert result.success, "Prepare rename başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Total references: {result.total_references}")
    
    print("\n" + "=" * 70)
    print("PASS: Class rename")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_prepare_rename()
        test2 = test_find_python_references()
        test3 = test_apply_rename()
        test4 = test_validate_rename()
        test5 = test_get_rename_preview()
        test6 = test_rename_scope_enum()
        test7 = test_symbol_kind_enum()
        test8 = test_symbol_reference_dataclass()
        test9 = test_rename_edit_dataclass()
        test10 = test_rename_result_dataclass()
        test11 = test_function_rename()
        test12 = test_class_rename()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Prepare Rename: {'PASS' if test1 else 'FAIL'}")
        print(f"Find Python References: {'PASS' if test2 else 'FAIL'}")
        print(f"Apply Rename: {'PASS' if test3 else 'FAIL'}")
        print(f"Validate Rename: {'PASS' if test4 else 'FAIL'}")
        print(f"Get Rename Preview: {'PASS' if test5 else 'FAIL'}")
        print(f"RenameScope Enum: {'PASS' if test6 else 'FAIL'}")
        print(f"SymbolKind Enum: {'PASS' if test7 else 'FAIL'}")
        print(f"SymbolReference Dataclass: {'PASS' if test8 else 'FAIL'}")
        print(f"RenameEdit Dataclass: {'PASS' if test9 else 'FAIL'}")
        print(f"RenameResult Dataclass: {'PASS' if test10 else 'FAIL'}")
        print(f"Function Rename: {'PASS' if test11 else 'FAIL'}")
        print(f"Class Rename: {'PASS' if test12 else 'FAIL'}")
        
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
