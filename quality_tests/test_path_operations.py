"""
Quality Test: Path Operations
Path operations system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.path_operations import (
    PathOperationsEngine,
    PathSeparator,
    PathOperation,
    PathConfig,
    PathResult
)


def test_join_paths():
    """
    Test: Join paths.
    """
    print("=" * 70)
    print("TEST: Join Paths")
    print("=" * 70)
    
    engine = PathOperationsEngine()
    result = engine.join_paths("path", "to", "file.txt")
    
    assert result.success, "Birleştirme başarılı olmalı"
    assert result.result is not None, "Sonuç olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Result: {result.result}")
    
    print("\n" + "=" * 70)
    print("PASS: Join paths")
    print("=" * 70)


def test_normalize_path():
    """
    Test: Normalize path.
    """
    print("=" * 70)
    print("TEST: Normalize Path")
    print("=" * 70)
    
    engine = PathOperationsEngine()
    result = engine.normalize_path("path/to/../to/file.txt")
    
    assert result.success, "Normalizasyon başarılı olmalı"
    assert result.result is not None, "Sonuç olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Result: {result.result}")
    
    print("\n" + "=" * 70)
    print("PASS: Normalize path")
    print("=" * 70)


def test_get_absolute_path():
    """
    Test: Get absolute path.
    """
    print("=" * 70)
    print("TEST: Get Absolute Path")
    print("=" * 70)
    
    engine = PathOperationsEngine()
    result = engine.get_absolute_path("file.txt")
    
    assert result.success, "Mutlak yol alma başarılı olmalı"
    assert result.result is not None, "Sonuç olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Result: {result.result}")
    
    print("\n" + "=" * 70)
    print("PASS: Get absolute path")
    print("=" * 70)


def test_get_relative_path():
    """
    Test: Get relative path.
    """
    print("=" * 70)
    print("TEST: Get Relative Path")
    print("=" * 70)
    
    engine = PathOperationsEngine()
    result = engine.get_relative_path("/path/to/file.txt", "/path")
    
    assert result.success, "Göreli yol alma başarılı olmalı"
    assert result.result is not None, "Sonuç olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Result: {result.result}")
    
    print("\n" + "=" * 70)
    print("PASS: Get relative path")
    print("=" * 70)


def test_get_basename():
    """
    Test: Get basename.
    """
    print("=" * 70)
    print("TEST: Get Basename")
    print("=" * 70)
    
    engine = PathOperationsEngine()
    result = engine.get_basename("/path/to/file.txt")
    
    assert result.success, "Dosya adı alma başarılı olmalı"
    assert result.result == "file.txt", "Dosya adı eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Result: {result.result}")
    
    print("\n" + "=" * 70)
    print("PASS: Get basename")
    print("=" * 70)


def test_get_dirname():
    """
    Test: Get dirname.
    """
    print("=" * 70)
    print("TEST: Get Dirname")
    print("=" * 70)
    
    engine = PathOperationsEngine()
    result = engine.get_dirname("/path/to/file.txt")
    
    assert result.success, "Dizin adı alma başarılı olmalı"
    assert result.result is not None, "Sonuç olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Result: {result.result}")
    
    print("\n" + "=" * 70)
    print("PASS: Get dirname")
    print("=" * 70)


def test_get_extension():
    """
    Test: Get extension.
    """
    print("=" * 70)
    print("TEST: Get Extension")
    print("=" * 70)
    
    engine = PathOperationsEngine()
    result = engine.get_extension("/path/to/file.txt")
    
    assert result.success, "Uzantı alma başarılı olmalı"
    assert result.result == ".txt", "Uzantı eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Result: {result.result}")
    
    print("\n" + "=" * 70)
    print("PASS: Get extension")
    print("=" * 70)


def test_split_path():
    """
    Test: Split path.
    """
    print("=" * 70)
    print("TEST: Split Path")
    print("=" * 70)
    
    engine = PathOperationsEngine()
    result = engine.split_path("/path/to/file.txt")
    
    assert result.success, "Bölme başarılı olmalı"
    assert result.result is not None, "Sonuç olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Result: {result.result}")
    
    print("\n" + "=" * 70)
    print("PASS: Split path")
    print("=" * 70)


def test_validate_path():
    """
    Test: Validate path.
    """
    print("=" * 70)
    print("TEST: Validate Path")
    print("=" * 70)
    
    engine = PathOperationsEngine()
    result = engine.validate_path("/path/to/file.txt")
    
    assert result.success, "Doğrulama başarılı olmalı"
    assert result.result is not None, "Sonuç olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Result: {result.result}")
    
    print("\n" + "=" * 70)
    print("PASS: Validate path")
    print("=" * 70)


def test_convert_separator():
    """
    Test: Convert separator.
    """
    print("=" * 70)
    print("TEST: Convert Separator")
    print("=" * 70)
    
    engine = PathOperationsEngine()
    result = engine.convert_separator("path/to/file.txt", PathSeparator.BACKWARD)
    
    assert result.success, "Dönüştürme başarılı olmalı"
    assert result.result is not None, "Sonuç olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Result: {result.result}")
    
    print("\n" + "=" * 70)
    print("PASS: Convert separator")
    print("=" * 70)


def test_get_operation_history():
    """
    Test: Get operation history.
    """
    print("=" * 70)
    print("TEST: Get Operation History")
    print("=" * 70)
    
    engine = PathOperationsEngine()
    engine.join_paths("path", "to", "file.txt")
    
    history = engine.get_operation_history()
    
    assert len(history) > 0, "Geçmiş olmalı"
    
    print(f"  History: {len(history)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get operation history")
    print("=" * 70)


def test_clear_history():
    """
    Test: Clear history.
    """
    print("=" * 70)
    print("TEST: Clear History")
    print("=" * 70)
    
    engine = PathOperationsEngine()
    engine.join_paths("path", "to", "file.txt")
    
    result = engine.clear_history()
    
    assert result.success, "Temizleme başarılı olmalı"
    assert len(engine.get_operation_history()) == 0, "Geçmiş temizlenmeli"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear history")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    engine = PathOperationsEngine()
    
    new_config = PathConfig(separator=PathSeparator.FORWARD)
    result = engine.update_config(new_config)
    
    assert result.success, "Güncelleme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Update config")
    print("=" * 70)


def test_get_config():
    """
    Test: Get config.
    """
    print("=" * 70)
    print("TEST: Get Config")
    print("=" * 70)
    
    engine = PathOperationsEngine()
    
    config = engine.get_config()
    
    assert config is not None, "Config olmalı"
    assert config.separator == PathSeparator.AUTO, "Config eşleşmeli"
    
    print(f"  Separator: {config.separator.value}")
    print(f"  Normalize: {config.normalize}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


def test_path_separator_enum():
    """
    Test: PathSeparator enum.
    """
    print("=" * 70)
    print("TEST: PathSeparator Enum")
    print("=" * 70)
    
    assert PathSeparator.FORWARD.value == "/"
    assert PathSeparator.BACKWARD.value == "\\"
    assert PathSeparator.AUTO.value == "auto"
    
    print(f"  All enum values verified")
    print(f"  Total separators: {len(PathSeparator)}")
    
    print("\n" + "=" * 70)
    print("PASS: PathSeparator enum")
    print("=" * 70)


def test_path_operation_enum():
    """
    Test: PathOperation enum.
    """
    print("=" * 70)
    print("TEST: PathOperation Enum")
    print("=" * 70)
    
    assert PathOperation.JOIN.value == "join"
    assert PathOperation.NORMALIZE.value == "normalize"
    assert PathOperation.ABSOLUTE.value == "absolute"
    assert PathOperation.RELATIVE.value == "relative"
    
    print(f"  All enum values verified")
    print(f"  Total operations: {len(PathOperation)}")
    
    print("\n" + "=" * 70)
    print("PASS: PathOperation enum")
    print("=" * 70)


def test_path_config_dataclass():
    """
    Test: PathConfig dataclass.
    """
    print("=" * 70)
    print("TEST: PathConfig Dataclass")
    print("=" * 70)
    
    config = PathConfig(
        separator=PathSeparator.FORWARD,
        normalize=False
    )
    
    assert config.separator == PathSeparator.FORWARD, "Separator eşleşmeli"
    assert config.normalize == False, "Normalize eşleşmeli"
    
    print(f"  Separator: {config.separator.value}")
    print(f"  Normalize: {config.normalize}")
    
    print("\n" + "=" * 70)
    print("PASS: PathConfig dataclass")
    print("=" * 70)


def test_path_result_dataclass():
    """
    Test: PathResult dataclass.
    """
    print("=" * 70)
    print("TEST: PathResult Dataclass")
    print("=" * 70)
    
    result = PathResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: PathResult dataclass")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_join_paths()
        test2 = test_normalize_path()
        test3 = test_get_absolute_path()
        test4 = test_get_relative_path()
        test5 = test_get_basename()
        test6 = test_get_dirname()
        test7 = test_get_extension()
        test8 = test_split_path()
        test9 = test_validate_path()
        test10 = test_convert_separator()
        test11 = test_get_operation_history()
        test12 = test_clear_history()
        test13 = test_update_config()
        test14 = test_get_config()
        test15 = test_path_separator_enum()
        test16 = test_path_operation_enum()
        test17 = test_path_config_dataclass()
        test18 = test_path_result_dataclass()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Join Paths: {'PASS' if test1 else 'FAIL'}")
        print(f"Normalize Path: {'PASS' if test2 else 'FAIL'}")
        print(f"Get Absolute Path: {'PASS' if test3 else 'FAIL'}")
        print(f"Get Relative Path: {'PASS' if test4 else 'FAIL'}")
        print(f"Get Basename: {'PASS' if test5 else 'FAIL'}")
        print(f"Get Dirname: {'PASS' if test6 else 'FAIL'}")
        print(f"Get Extension: {'PASS' if test7 else 'FAIL'}")
        print(f"Split Path: {'PASS' if test8 else 'FAIL'}")
        print(f"Validate Path: {'PASS' if test9 else 'FAIL'}")
        print(f"Convert Separator: {'PASS' if test10 else 'FAIL'}")
        print(f"Get Operation History: {'PASS' if test11 else 'FAIL'}")
        print(f"Clear History: {'PASS' if test12 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test13 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test14 else 'FAIL'}")
        print(f"PathSeparator Enum: {'PASS' if test15 else 'FAIL'}")
        print(f"PathOperation Enum: {'PASS' if test16 else 'FAIL'}")
        print(f"PathConfig Dataclass: {'PASS' if test17 else 'FAIL'}")
        print(f"PathResult Dataclass: {'PASS' if test18 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14, test15, test16, test17, test18])
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
