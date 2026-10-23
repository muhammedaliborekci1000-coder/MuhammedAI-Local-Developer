"""
Quality Test: Extract Variable
Extract variable system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.extract_variable import (
    ExtractVariableEngine,
    VariableScope,
    ExtractionMode,
    VariableInfo,
    ExtractConfig,
    ExtractResult
)


def test_extract_variable():
    """
    Test: Extract variable.
    """
    print("=" * 70)
    print("TEST: Extract Variable")
    print("=" * 70)
    
    engine = ExtractVariableEngine()
    
    content = "x = 42 + 42"
    result = engine.extract_variable(content, "42")
    
    assert result.success, "Çıkarma başarılı olmalı"
    assert result.variable_info is not None, "Değişken bilgisi olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Variable name: {result.variable_info.name}")
    
    print("\n" + "=" * 70)
    print("PASS: Extract variable")
    print("=" * 70)


def test_extract_with_suggested_name():
    """
    Test: Extract with suggested name.
    """
    print("=" * 70)
    print("TEST: Extract With Suggested Name")
    print("=" * 70)
    
    engine = ExtractVariableEngine()
    
    content = "x = 42"
    result = engine.extract_variable(content, "42", suggested_name="my_number")
    
    assert result.success, "Çıkarma başarılı olmalı"
    assert result.variable_info.name == "my_number", "İsim eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Variable name: {result.variable_info.name}")
    
    print("\n" + "=" * 70)
    print("PASS: Extract with suggested name")
    print("=" * 70)


def test_extract_string():
    """
    Test: Extract string.
    """
    print("=" * 70)
    print("TEST: Extract String")
    print("=" * 70)
    
    engine = ExtractVariableEngine()
    
    content = 'print("hello")'
    result = engine.extract_variable(content, '"hello"')
    
    assert result.success, "Çıkarma başarılı olmalı"
    assert result.variable_info.variable_type == "str", "Tip str olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Variable type: {result.variable_info.variable_type}")
    
    print("\n" + "=" * 70)
    print("PASS: Extract string")
    print("=" * 70)


def test_extract_number():
    """
    Test: Extract number.
    """
    print("=" * 70)
    print("TEST: Extract Number")
    print("=" * 70)
    
    engine = ExtractVariableEngine()
    
    content = "x = 42"
    result = engine.extract_variable(content, "42")
    
    assert result.success, "Çıkarma başarılı olmalı"
    assert result.variable_info.variable_type == "int", "Tip int olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Variable type: {result.variable_info.variable_type}")
    
    print("\n" + "=" * 70)
    print("PASS: Extract number")
    print("=" * 70)


def test_extract_boolean():
    """
    Test: Extract boolean.
    """
    print("=" * 70)
    print("TEST: Extract Boolean")
    print("=" * 70)
    
    engine = ExtractVariableEngine()
    
    content = "x = True"
    result = engine.extract_variable(content, "True")
    
    assert result.success, "Çıkarma başarılı olmalı"
    assert result.variable_info.variable_type == "bool", "Tip bool olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Variable type: {result.variable_info.variable_type}")
    
    print("\n" + "=" * 70)
    print("PASS: Extract boolean")
    print("=" * 70)


def test_undo_extraction():
    """
    Test: Undo extraction.
    """
    print("=" * 70)
    print("TEST: Undo Extraction")
    print("=" * 70)
    
    engine = ExtractVariableEngine()
    
    content = "x = 42"
    engine.extract_variable(content, "42")
    result = engine.undo_extraction()
    
    assert result.success, "Geri alma başarılı olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Undo extraction")
    print("=" * 70)


def test_get_extraction_history():
    """
    Test: Get extraction history.
    """
    print("=" * 70)
    print("TEST: Get Extraction History")
    print("=" * 70)
    
    engine = ExtractVariableEngine()
    
    engine.extract_variable("x = 42", "42")
    history = engine.get_extraction_history()
    
    assert len(history) > 0, "Geçmiş olmalı"
    
    print(f"  History: {len(history)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get extraction history")
    print("=" * 70)


def test_clear_history():
    """
    Test: Clear history.
    """
    print("=" * 70)
    print("TEST: Clear History")
    print("=" * 70)
    
    engine = ExtractVariableEngine()
    
    engine.extract_variable("x = 42", "42")
    result = engine.clear_history()
    
    assert result.success, "Temizleme başarılı olmalı"
    assert len(engine.get_extraction_history()) == 0, "Geçmiş temizlenmeli"
    
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
    
    engine = ExtractVariableEngine()
    
    new_config = ExtractConfig(auto_infer_type=False)
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
    
    engine = ExtractVariableEngine()
    
    config = engine.get_config()
    
    assert config is not None, "Config olmalı"
    assert config.auto_infer_type == True, "Config eşleşmeli"
    
    print(f"  Auto infer type: {config.auto_infer_type}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


def test_variable_scope_enum():
    """
    Test: VariableScope enum.
    """
    print("=" * 70)
    print("TEST: VariableScope Enum")
    print("=" * 70)
    
    assert VariableScope.LOCAL.value == "local"
    assert VariableScope.FUNCTION.value == "function"
    assert VariableScope.CLASS.value == "class"
    assert VariableScope.MODULE.value == "module"
    assert VariableScope.GLOBAL.value == "global"
    
    print(f"  All enum values verified")
    print(f"  Total scopes: {len(VariableScope)}")
    
    print("\n" + "=" * 70)
    print("PASS: VariableScope enum")
    print("=" * 70)


def test_extraction_mode_enum():
    """
    Test: ExtractionMode enum.
    """
    print("=" * 70)
    print("TEST: ExtractionMode Enum")
    print("=" * 70)
    
    assert ExtractionMode.SELECTION.value == "selection"
    assert ExtractionMode.EXPRESSION.value == "expression"
    assert ExtractionMode.REPEATED_VALUE.value == "repeated_value"
    assert ExtractionMode.COMPLEX_EXPRESSION.value == "complex_expression"
    
    print(f"  All enum values verified")
    print(f"  Total modes: {len(ExtractionMode)}")
    
    print("\n" + "=" * 70)
    print("PASS: ExtractionMode enum")
    print("=" * 70)


def test_variable_info_dataclass():
    """
    Test: VariableInfo dataclass.
    """
    print("=" * 70)
    print("TEST: VariableInfo Dataclass")
    print("=" * 70)
    
    variable_info = VariableInfo(
        name="my_var",
        value="42",
        variable_type="int"
    )
    
    assert variable_info.name == "my_var", "Name eşleşmeli"
    assert variable_info.value == "42", "Value eşleşmeli"
    assert variable_info.variable_type == "int", "Type eşleşmeli"
    
    print(f"  Name: {variable_info.name}")
    print(f"  Value: {variable_info.value}")
    print(f"  Type: {variable_info.variable_type}")
    
    print("\n" + "=" * 70)
    print("PASS: VariableInfo dataclass")
    print("=" * 70)


def test_extract_config_dataclass():
    """
    Test: ExtractConfig dataclass.
    """
    print("=" * 70)
    print("TEST: ExtractConfig Dataclass")
    print("=" * 70)
    
    config = ExtractConfig(
        auto_infer_type=True,
        suggest_names=True,
        replace_all_occurrences=False
    )
    
    assert config.auto_infer_type == True, "Auto infer type eşleşmeli"
    assert config.suggest_names == True, "Suggest names eşleşmeli"
    assert config.replace_all_occurrences == False, "Replace all occurrences eşleşmeli"
    
    print(f"  Auto infer type: {config.auto_infer_type}")
    print(f"  Suggest names: {config.suggest_names}")
    print(f"  Replace all occurrences: {config.replace_all_occurrences}")
    
    print("\n" + "=" * 70)
    print("PASS: ExtractConfig dataclass")
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


def test_extract_empty_selection():
    """
    Test: Extract empty selection.
    """
    print("=" * 70)
    print("TEST: Extract Empty Selection")
    print("=" * 70)
    
    engine = ExtractVariableEngine()
    
    result = engine.extract_variable("x = 42", "")
    
    assert result.success == False, "Başarısız olmalı"
    assert len(result.errors) > 0, "Hata olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Errors: {result.errors}")
    
    print("\n" + "=" * 70)
    print("PASS: Extract empty selection")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_extract_variable()
        test2 = test_extract_with_suggested_name()
        test3 = test_extract_string()
        test4 = test_extract_number()
        test5 = test_extract_boolean()
        test6 = test_undo_extraction()
        test7 = test_get_extraction_history()
        test8 = test_clear_history()
        test9 = test_update_config()
        test10 = test_get_config()
        test11 = test_variable_scope_enum()
        test12 = test_extraction_mode_enum()
        test13 = test_variable_info_dataclass()
        test14 = test_extract_config_dataclass()
        test15 = test_extract_result_dataclass()
        test16 = test_extract_empty_selection()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Extract Variable: {'PASS' if test1 else 'FAIL'}")
        print(f"Extract With Suggested Name: {'PASS' if test2 else 'FAIL'}")
        print(f"Extract String: {'PASS' if test3 else 'FAIL'}")
        print(f"Extract Number: {'PASS' if test4 else 'FAIL'}")
        print(f"Extract Boolean: {'PASS' if test5 else 'FAIL'}")
        print(f"Undo Extraction: {'PASS' if test6 else 'FAIL'}")
        print(f"Get Extraction History: {'PASS' if test7 else 'FAIL'}")
        print(f"Clear History: {'PASS' if test8 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test9 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test10 else 'FAIL'}")
        print(f"VariableScope Enum: {'PASS' if test11 else 'FAIL'}")
        print(f"ExtractionMode Enum: {'PASS' if test12 else 'FAIL'}")
        print(f"VariableInfo Dataclass: {'PASS' if test13 else 'FAIL'}")
        print(f"ExtractConfig Dataclass: {'PASS' if test14 else 'FAIL'}")
        print(f"ExtractResult Dataclass: {'PASS' if test15 else 'FAIL'}")
        print(f"Extract Empty Selection: {'PASS' if test16 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14, test15, test16])
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
