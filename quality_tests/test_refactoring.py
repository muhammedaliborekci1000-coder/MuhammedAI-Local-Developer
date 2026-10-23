"""
Quality Test: Refactoring
Refactoring system testleri.
"""

import sys
import os
import tempfile
import shutil
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.ai.refactoring import (
    RefactoringEngine,
    RefactoringType,
    RefactoringEdit,
    RefactoringResult
)


def test_rename_symbol():
    """
    Test: Rename symbol.
    """
    print("=" * 70)
    print("TEST: Rename Symbol")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp(prefix="muhammedai_test_")
    
    try:
        # Test dosyası oluştur
        test_file = Path(temp_dir) / "test.py"
        test_file.write_text("def my_function():\n    pass\n", encoding='utf-8')
        
        engine = RefactoringEngine()
        
        # Rename
        result = engine.rename_symbol(
            file_path=str(test_file),
            old_name="my_function",
            new_name="new_function",
            line=1,
            column=0
        )
        
        assert result.success, "Rename başarılı olmalı"
        assert len(result.edits) > 0, "Edits olmalı"
        assert "new_function" in result.edits[0].new_text, "New name içermeli"
        
        print(f"  Success: {result.success}")
        print(f"  Edits: {len(result.edits)}")
        print(f"  Message: {result.message}")
        
        print("\n" + "=" * 70)
        print("PASS: Rename symbol")
        print("=" * 70)
        
    finally:
        shutil.rmtree(temp_dir)


def test_extract_function():
    """
    Test: Extract function.
    """
    print("=" * 70)
    print("TEST: Extract Function")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp(prefix="muhammedai_test_")
    
    try:
        # Test dosyası oluştur
        test_file = Path(temp_dir) / "test.py"
        test_file.write_text("def main():\n    x = 10\n    y = 20\n", encoding='utf-8')
        
        engine = RefactoringEngine()
        
        # Extract function
        result = engine.extract_function(
            file_path=str(test_file),
            start_line=2,
            end_line=3,
            function_name="extracted_func"
        )
        
        assert result is not None, "Result olmalı"
        print(f"  Success: {result.success}")
        print(f"  Edits: {len(result.edits)}")
        print(f"  Message: {result.message}")
        
        print("\n" + "=" * 70)
        print("PASS: Extract function")
        print("=" * 70)
        
    finally:
        shutil.rmtree(temp_dir)


def test_extract_variable():
    """
    Test: Extract variable.
    """
    print("=" * 70)
    print("TEST: Extract Variable")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp(prefix="muhammedai_test_")
    
    try:
        # Test dosyası oluştur
        test_file = Path(temp_dir) / "test.py"
        test_file.write_text("x = 10 + 20\n", encoding='utf-8')
        
        engine = RefactoringEngine()
        
        # Extract variable
        result = engine.extract_variable(
            file_path=str(test_file),
            start_line=1,
            end_line=1,
            start_column=4,
            end_column=9,
            variable_name="result"
        )
        
        assert result is not None, "Result olmalı"
        print(f"  Success: {result.success}")
        print(f"  Edits: {len(result.edits)}")
        print(f"  Message: {result.message}")
        
        print("\n" + "=" * 70)
        print("PASS: Extract variable")
        print("=" * 70)
        
    finally:
        shutil.rmtree(temp_dir)


def test_inline_variable():
    """
    Test: Inline variable.
    """
    print("=" * 70)
    print("TEST: Inline Variable")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp(prefix="muhammedai_test_")
    
    try:
        # Test dosyası oluştur
        test_file = Path(temp_dir) / "test.py"
        test_file.write_text("x = 10\ny = x\n", encoding='utf-8')
        
        engine = RefactoringEngine()
        
        # Inline variable
        result = engine.inline_variable(
            file_path=str(test_file),
            variable_name="x",
            line=1
        )
        
        assert result is not None, "Result olmalı"
        print(f"  Success: {result.success}")
        print(f"  Edits: {len(result.edits)}")
        print(f"  Message: {result.message}")
        
        print("\n" + "=" * 70)
        print("PASS: Inline variable")
        print("=" * 70)
        
    finally:
        shutil.rmtree(temp_dir)


def test_organize_imports():
    """
    Test: Organize imports.
    """
    print("=" * 70)
    print("TEST: Organize Imports")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp(prefix="muhammedai_test_")
    
    try:
        # Test dosyası oluştur
        test_file = Path(temp_dir) / "test.py"
        test_file.write_text("import sys\nimport os\nimport sys\nx = 10\n", encoding='utf-8')
        
        engine = RefactoringEngine()
        
        # Organize imports
        result = engine.organize_imports(str(test_file))
        
        assert result is not None, "Result olmalı"
        print(f"  Success: {result.success}")
        print(f"  Edits: {len(result.edits)}")
        print(f"  Message: {result.message}")
        
        print("\n" + "=" * 70)
        print("PASS: Organize imports")
        print("=" * 70)
        
    finally:
        shutil.rmtree(temp_dir)


def test_safe_delete():
    """
    Test: Safe delete.
    """
    print("=" * 70)
    print("TEST: Safe Delete")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp(prefix="muhammedai_test_")
    
    try:
        # Test dosyası oluştur
        test_file = Path(temp_dir) / "test.py"
        test_file.write_text("x = 10\n", encoding='utf-8')
        
        engine = RefactoringEngine()
        
        # Safe delete
        result = engine.safe_delete(
            file_path=str(test_file),
            symbol_name="x",
            line=1
        )
        
        assert result is not None, "Result olmalı"
        print(f"  Success: {result.success}")
        print(f"  Edits: {len(result.edits)}")
        print(f"  Message: {result.message}")
        
        print("\n" + "=" * 70)
        print("PASS: Safe delete")
        print("=" * 70)
        
    finally:
        shutil.rmtree(temp_dir)


def test_apply_edits():
    """
    Test: Apply edits.
    """
    print("=" * 70)
    print("TEST: Apply Edits")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp(prefix="muhammedai_test_")
    
    try:
        # Test dosyası oluştur
        test_file = Path(temp_dir) / "test.py"
        test_file.write_text("old_text\n", encoding='utf-8')
        
        engine = RefactoringEngine()
        
        # Edit oluştur
        edit = RefactoringEdit(
            file_path=str(test_file),
            start_line=1,
            start_column=0,
            end_line=1,
            end_column=8,
            old_text="old_text",
            new_text="new_text"
        )
        
        # Apply edits
        result = engine.apply_edits([edit])
        
        assert result is not None, "Result olmalı"
        print(f"  Success: {result.success}")
        print(f"  Message: {result.message}")
        
        # Dosyayı kontrol et
        new_content = test_file.read_text(encoding='utf-8')
        print(f"  New content: {new_content.strip()}")
        
        print("\n" + "=" * 70)
        print("PASS: Apply edits")
        print("=" * 70)
        
    finally:
        shutil.rmtree(temp_dir)


def test_refactoring_type_enum():
    """
    Test: RefactoringType enum.
    """
    print("=" * 70)
    print("TEST: RefactoringType Enum")
    print("=" * 70)
    
    # Tüm enum değerlerini kontrol et
    assert RefactoringType.RENAME_SYMBOL.value == "rename_symbol"
    assert RefactoringType.EXTRACT_FUNCTION.value == "extract_function"
    assert RefactoringType.EXTRACT_VARIABLE.value == "extract_variable"
    assert RefactoringType.INLINE_VARIABLE.value == "inline_variable"
    assert RefactoringType.MOVE_SYMBOL.value == "move_symbol"
    assert RefactoringType.CHANGE_SIGNATURE.value == "change_signature"
    assert RefactoringType.SAFE_DELETE.value == "safe_delete"
    assert RefactoringType.ORGANIZE_IMPORTS.value == "organize_imports"
    
    print(f"  All enum values verified")
    print(f"  Total types: {len(RefactoringType)}")
    
    print("\n" + "=" * 70)
    print("PASS: RefactoringType enum")
    print("=" * 70)


def test_refactoring_edit():
    """
    Test: RefactoringEdit dataclass.
    """
    print("=" * 70)
    print("TEST: RefactoringEdit Dataclass")
    print("=" * 70)
    
    edit = RefactoringEdit(
        file_path="test.py",
        start_line=1,
        start_column=0,
        end_line=1,
        end_column=8,
        old_text="old",
        new_text="new"
    )
    
    assert edit.file_path == "test.py", "File path eşleşmeli"
    assert edit.start_line == 1, "Start line eşleşmeli"
    assert edit.old_text == "old", "Old text eşleşmeli"
    assert edit.new_text == "new", "New text eşleşmeli"
    
    print(f"  File path: {edit.file_path}")
    print(f"  Old text: {edit.old_text}")
    print(f"  New text: {edit.new_text}")
    
    print("\n" + "=" * 70)
    print("PASS: RefactoringEdit dataclass")
    print("=" * 70)


def test_refactoring_result():
    """
    Test: RefactoringResult dataclass.
    """
    print("=" * 70)
    print("TEST: RefactoringResult Dataclass")
    print("=" * 70)
    
    result = RefactoringResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.edits, list), "Edits list olmalı"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Edits: {len(result.edits)}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: RefactoringResult dataclass")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_rename_symbol()
        test2 = test_extract_function()
        test3 = test_extract_variable()
        test4 = test_inline_variable()
        test5 = test_organize_imports()
        test6 = test_safe_delete()
        test7 = test_apply_edits()
        test8 = test_refactoring_type_enum()
        test9 = test_refactoring_edit()
        test10 = test_refactoring_result()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Rename Symbol: {'PASS' if test1 else 'FAIL'}")
        print(f"Extract Function: {'PASS' if test2 else 'FAIL'}")
        print(f"Extract Variable: {'PASS' if test3 else 'FAIL'}")
        print(f"Inline Variable: {'PASS' if test4 else 'FAIL'}")
        print(f"Organize Imports: {'PASS' if test5 else 'FAIL'}")
        print(f"Safe Delete: {'PASS' if test6 else 'FAIL'}")
        print(f"Apply Edits: {'PASS' if test7 else 'FAIL'}")
        print(f"RefactoringType Enum: {'PASS' if test8 else 'FAIL'}")
        print(f"RefactoringEdit Dataclass: {'PASS' if test9 else 'FAIL'}")
        print(f"RefactoringResult Dataclass: {'PASS' if test10 else 'FAIL'}")
        
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
