"""
Quality Test: Case Conversion
Case conversion system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.case_conversion import (
    CaseConversionEngine,
    CaseType,
    ConvertScope,
    ConvertRange,
    CaseConfig,
    CaseResult
)


def test_to_upper():
    """
    Test: To upper.
    """
    print("=" * 70)
    print("TEST: To Upper")
    print("=" * 70)
    
    engine = CaseConversionEngine()
    
    content = "Hello World"
    result = engine.to_upper(content)
    
    assert result.success, "Dönüştürme başarılı olmalı"
    assert result.modified_content == "HELLO WORLD", "Upper case olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Modified: {result.modified_content}")
    
    print("\n" + "=" * 70)
    print("PASS: To upper")
    print("=" * 70)


def test_to_lower():
    """
    Test: To lower.
    """
    print("=" * 70)
    print("TEST: To Lower")
    print("=" * 70)
    
    engine = CaseConversionEngine()
    
    content = "HELLO WORLD"
    result = engine.to_lower(content)
    
    assert result.success, "Dönüştürme başarılı olmalı"
    assert result.modified_content == "hello world", "Lower case olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Modified: {result.modified_content}")
    
    print("\n" + "=" * 70)
    print("PASS: To lower")
    print("=" * 70)


def test_to_title():
    """
    Test: To title.
    """
    print("=" * 70)
    print("TEST: To Title")
    print("=" * 70)
    
    engine = CaseConversionEngine()
    
    content = "hello world"
    result = engine.to_title(content)
    
    assert result.success, "Dönüştürme başarılı olmalı"
    assert result.modified_content == "Hello World", "Title case olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Modified: {result.modified_content}")
    
    print("\n" + "=" * 70)
    print("PASS: To title")
    print("=" * 70)


def test_to_sentence():
    """
    Test: To sentence.
    """
    print("=" * 70)
    print("TEST: To Sentence")
    print("=" * 70)
    
    engine = CaseConversionEngine()
    
    content = "hello world. this is a test"
    result = engine.to_sentence(content)
    
    assert result.success, "Dönüştürme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Modified: {result.modified_content}")
    
    print("\n" + "=" * 70)
    print("PASS: To sentence")
    print("=" * 70)


def test_to_reverse():
    """
    Test: To reverse.
    """
    print("=" * 70)
    print("TEST: To Reverse")
    print("=" * 70)
    
    engine = CaseConversionEngine()
    
    content = "Hello World"
    result = engine.to_reverse(content)
    
    assert result.success, "Dönüştürme başarılı olmalı"
    assert result.modified_content == "hELLO wORLD", "Reverse case olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Modified: {result.modified_content}")
    
    print("\n" + "=" * 70)
    print("PASS: To reverse")
    print("=" * 70)


def test_to_camel():
    """
    Test: To camel.
    """
    print("=" * 70)
    print("TEST: To Camel")
    print("=" * 70)
    
    engine = CaseConversionEngine()
    
    content = "hello_world"
    result = engine.to_camel(content)
    
    assert result.success, "Dönüştürme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Modified: {result.modified_content}")
    
    print("\n" + "=" * 70)
    print("PASS: To camel")
    print("=" * 70)


def test_to_snake():
    """
    Test: To snake.
    """
    print("=" * 70)
    print("TEST: To Snake")
    print("=" * 70)
    
    engine = CaseConversionEngine()
    
    content = "HelloWorld"
    result = engine.to_snake(content)
    
    assert result.success, "Dönüştürme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Modified: {result.modified_content}")
    
    print("\n" + "=" * 70)
    print("PASS: To snake")
    print("=" * 70)


def test_to_pascal():
    """
    Test: To pascal.
    """
    print("=" * 70)
    print("TEST: To Pascal")
    print("=" * 70)
    
    engine = CaseConversionEngine()
    
    content = "hello_world"
    result = engine.to_pascal(content)
    
    assert result.success, "Dönüştürme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Modified: {result.modified_content}")
    
    print("\n" + "=" * 70)
    print("PASS: To pascal")
    print("=" * 70)


def test_to_kebab():
    """
    Test: To kebab.
    """
    print("=" * 70)
    print("TEST: To Kebab")
    print("=" * 70)
    
    engine = CaseConversionEngine()
    
    content = "HelloWorld"
    result = engine.to_kebab(content)
    
    assert result.success, "Dönüştürme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Modified: {result.modified_content}")
    
    print("\n" + "=" * 70)
    print("PASS: To kebab")
    print("=" * 70)


def test_convert_selection():
    """
    Test: Convert selection.
    """
    print("=" * 70)
    print("TEST: Convert Selection")
    print("=" * 70)
    
    config = CaseConfig(scope=ConvertScope.SELECTION)
    engine = CaseConversionEngine(config)
    
    content = "Hello\nWorld\nTest"
    convert_range = ConvertRange(start_line=0, end_line=1)
    result = engine.convert_case(content, CaseType.UPPER, convert_range)
    
    assert result.success, "Dönüştürme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Convert selection")
    print("=" * 70)


def test_convert_line():
    """
    Test: Convert line.
    """
    print("=" * 70)
    print("TEST: Convert Line")
    print("=" * 70)
    
    config = CaseConfig(scope=ConvertScope.LINE)
    engine = CaseConversionEngine(config)
    
    content = "Hello\nWorld\nTest"
    convert_range = ConvertRange(start_line=1, end_line=1)
    result = engine.convert_case(content, CaseType.UPPER, convert_range)
    
    assert result.success, "Dönüştürme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Convert line")
    print("=" * 70)


def test_convert_document():
    """
    Test: Convert document.
    """
    print("=" * 70)
    print("TEST: Convert Document")
    print("=" * 70)
    
    config = CaseConfig(scope=ConvertScope.DOCUMENT)
    engine = CaseConversionEngine(config)
    
    content = "Hello\nWorld\nTest"
    result = engine.convert_case(content, CaseType.UPPER)
    
    assert result.success, "Dönüştürme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Convert document")
    print("=" * 70)


def test_convert_word():
    """
    Test: Convert word.
    """
    print("=" * 70)
    print("TEST: Convert Word")
    print("=" * 70)
    
    config = CaseConfig(scope=ConvertScope.WORD)
    engine = CaseConversionEngine(config)
    
    content = "Hello World Test"
    convert_range = ConvertRange(start_line=0, end_line=0, start_column=6, end_column=10)
    result = engine.convert_case(content, CaseType.UPPER, convert_range)
    
    assert result.success, "Dönüştürme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Convert word")
    print("=" * 70)


def test_undo_convert():
    """
    Test: Undo convert.
    """
    print("=" * 70)
    print("TEST: Undo Convert")
    print("=" * 70)
    
    engine = CaseConversionEngine()
    
    content = "Hello World"
    engine.to_upper(content)
    result = engine.undo_convert()
    
    assert result.success, "Geri alma başarılı olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Undo convert")
    print("=" * 70)


def test_get_convert_history():
    """
    Test: Get convert history.
    """
    print("=" * 70)
    print("TEST: Get Convert History")
    print("=" * 70)
    
    engine = CaseConversionEngine()
    
    content = "Hello World"
    engine.to_upper(content)
    history = engine.get_convert_history()
    
    assert len(history) > 0, "Geçmiş olmalı"
    
    print(f"  History: {len(history)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get convert history")
    print("=" * 70)


def test_clear_history():
    """
    Test: Clear history.
    """
    print("=" * 70)
    print("TEST: Clear History")
    print("=" * 70)
    
    engine = CaseConversionEngine()
    
    content = "Hello World"
    engine.to_upper(content)
    result = engine.clear_history()
    
    assert result.success, "Temizleme başarılı olmalı"
    assert len(engine.get_convert_history()) == 0, "Geçmiş temizlenmeli"
    
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
    
    engine = CaseConversionEngine()
    
    new_config = CaseConfig(scope=ConvertScope.DOCUMENT)
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
    
    engine = CaseConversionEngine()
    
    config = engine.get_config()
    
    assert config is not None, "Config olmalı"
    assert config.scope == ConvertScope.SELECTION, "Config eşleşmeli"
    
    print(f"  Scope: {config.scope.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


def test_case_type_enum():
    """
    Test: CaseType enum.
    """
    print("=" * 70)
    print("TEST: CaseType Enum")
    print("=" * 70)
    
    assert CaseType.UPPER.value == "upper"
    assert CaseType.LOWER.value == "lower"
    assert CaseType.TITLE.value == "title"
    assert CaseType.CAMEL.value == "camel"
    assert CaseType.SNAKE.value == "snake"
    assert CaseType.PASCAL.value == "pascal"
    assert CaseType.KEBAB.value == "kebab"
    assert CaseType.SENTENCE.value == "sentence"
    
    print(f"  All enum values verified")
    print(f"  Total types: {len(CaseType)}")
    
    print("\n" + "=" * 70)
    print("PASS: CaseType enum")
    print("=" * 70)


def test_convert_scope_enum():
    """
    Test: ConvertScope enum.
    """
    print("=" * 70)
    print("TEST: ConvertScope Enum")
    print("=" * 70)
    
    assert ConvertScope.WORD.value == "word"
    assert ConvertScope.SELECTION.value == "selection"
    assert ConvertScope.LINE.value == "line"
    assert ConvertScope.DOCUMENT.value == "document"
    
    print(f"  All enum values verified")
    print(f"  Total scopes: {len(ConvertScope)}")
    
    print("\n" + "=" * 70)
    print("PASS: ConvertScope enum")
    print("=" * 70)


def test_convert_range_dataclass():
    """
    Test: ConvertRange dataclass.
    """
    print("=" * 70)
    print("TEST: ConvertRange Dataclass")
    print("=" * 70)
    
    convert_range = ConvertRange(
        start_line=0,
        end_line=5,
        start_column=0,
        end_column=10
    )
    
    assert convert_range.start_line == 0, "Start line eşleşmeli"
    assert convert_range.end_line == 5, "End line eşleşmeli"
    
    print(f"  Start line: {convert_range.start_line}")
    print(f"  End line: {convert_range.end_line}")
    
    print("\n" + "=" * 70)
    print("PASS: ConvertRange dataclass")
    print("=" * 70)


def test_case_config_dataclass():
    """
    Test: CaseConfig dataclass.
    """
    print("=" * 70)
    print("TEST: CaseConfig Dataclass")
    print("=" * 70)
    
    config = CaseConfig(
        scope=ConvertScope.SELECTION,
        preserve_formatting=True,
        skip_keywords=True
    )
    
    assert config.scope == ConvertScope.SELECTION, "Scope eşleşmeli"
    assert config.preserve_formatting == True, "Preserve formatting eşleşmeli"
    assert config.skip_keywords == True, "Skip keywords eşleşmeli"
    
    print(f"  Scope: {config.scope.value}")
    print(f"  Preserve formatting: {config.preserve_formatting}")
    print(f"  Skip keywords: {config.skip_keywords}")
    
    print("\n" + "=" * 70)
    print("PASS: CaseConfig dataclass")
    print("=" * 70)


def test_case_result_dataclass():
    """
    Test: CaseResult dataclass.
    """
    print("=" * 70)
    print("TEST: CaseResult Dataclass")
    print("=" * 70)
    
    result = CaseResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: CaseResult dataclass")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_to_upper()
        test2 = test_to_lower()
        test3 = test_to_title()
        test4 = test_to_sentence()
        test5 = test_to_reverse()
        test6 = test_to_camel()
        test7 = test_to_snake()
        test8 = test_to_pascal()
        test9 = test_to_kebab()
        test10 = test_convert_selection()
        test11 = test_convert_line()
        test12 = test_convert_document()
        test13 = test_convert_word()
        test14 = test_undo_convert()
        test15 = test_get_convert_history()
        test16 = test_clear_history()
        test17 = test_update_config()
        test18 = test_get_config()
        test19 = test_case_type_enum()
        test20 = test_convert_scope_enum()
        test21 = test_convert_range_dataclass()
        test22 = test_case_config_dataclass()
        test23 = test_case_result_dataclass()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"To Upper: {'PASS' if test1 else 'FAIL'}")
        print(f"To Lower: {'PASS' if test2 else 'FAIL'}")
        print(f"To Title: {'PASS' if test3 else 'FAIL'}")
        print(f"To Sentence: {'PASS' if test4 else 'FAIL'}")
        print(f"To Reverse: {'PASS' if test5 else 'FAIL'}")
        print(f"To Camel: {'PASS' if test6 else 'FAIL'}")
        print(f"To Snake: {'PASS' if test7 else 'FAIL'}")
        print(f"To Pascal: {'PASS' if test8 else 'FAIL'}")
        print(f"To Kebab: {'PASS' if test9 else 'FAIL'}")
        print(f"Convert Selection: {'PASS' if test10 else 'FAIL'}")
        print(f"Convert Line: {'PASS' if test11 else 'FAIL'}")
        print(f"Convert Document: {'PASS' if test12 else 'FAIL'}")
        print(f"Convert Word: {'PASS' if test13 else 'FAIL'}")
        print(f"Undo Convert: {'PASS' if test14 else 'FAIL'}")
        print(f"Get Convert History: {'PASS' if test15 else 'FAIL'}")
        print(f"Clear History: {'PASS' if test16 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test17 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test18 else 'FAIL'}")
        print(f"CaseType Enum: {'PASS' if test19 else 'FAIL'}")
        print(f"ConvertScope Enum: {'PASS' if test20 else 'FAIL'}")
        print(f"ConvertRange Dataclass: {'PASS' if test21 else 'FAIL'}")
        print(f"CaseConfig Dataclass: {'PASS' if test22 else 'FAIL'}")
        print(f"CaseResult Dataclass: {'PASS' if test23 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14, test15, test16, test17, test18, test19, test20, test21, test22, test23])
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
