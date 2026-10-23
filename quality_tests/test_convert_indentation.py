"""
Quality Test: Convert Indentation
Convert indentation system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.convert_indentation import (
    ConvertIndentationEngine,
    IndentationType,
    ConvertScope,
    ConvertRange,
    ConvertConfig,
    ConvertResult
)


def test_convert_indentation():
    """
    Test: Convert indentation.
    """
    print("=" * 70)
    print("TEST: Convert Indentation")
    print("=" * 70)
    
    engine = ConvertIndentationEngine()
    
    content = "def test():\n\tpass\n\treturn"
    result = engine.convert_indentation(content)
    
    assert result.success, "Dönüştürme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Convert indentation")
    print("=" * 70)


def test_convert_tabs_to_spaces():
    """
    Test: Convert tabs to spaces.
    """
    print("=" * 70)
    print("TEST: Convert Tabs to Spaces")
    print("=" * 70)
    
    engine = ConvertIndentationEngine()
    
    content = "def test():\n\tpass\n\treturn"
    result = engine.convert_tabs_to_spaces(content)
    
    assert result.success, "Dönüştürme başarılı olmalı"
    assert result.tabs_converted > 0, "Tab'lar dönüştürülmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Tabs converted: {result.tabs_converted}")
    
    print("\n" + "=" * 70)
    print("PASS: Convert tabs to spaces")
    print("=" * 70)


def test_convert_spaces_to_tabs():
    """
    Test: Convert spaces to tabs.
    """
    print("=" * 70)
    print("TEST: Convert Spaces to Tabs")
    print("=" * 70)
    
    config = ConvertConfig(target_type=IndentationType.TABS)
    engine = ConvertIndentationEngine(config)
    
    content = "def test():\n    pass\n    return"
    result = engine.convert_spaces_to_tabs(content)
    
    assert result.success, "Dönüştürme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Convert spaces to tabs")
    print("=" * 70)


def test_convert_selection():
    """
    Test: Convert selection.
    """
    print("=" * 70)
    print("TEST: Convert Selection")
    print("=" * 70)
    
    config = ConvertConfig(scope=ConvertScope.SELECTION)
    engine = ConvertIndentationEngine(config)
    
    content = "def test():\n\tpass\n\treturn"
    convert_range = ConvertRange(start_line=1, end_line=2)
    result = engine.convert_indentation(content, convert_range)
    
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
    
    config = ConvertConfig(scope=ConvertScope.LINE)
    engine = ConvertIndentationEngine(config)
    
    content = "def test():\n\tpass\n\treturn"
    convert_range = ConvertRange(start_line=1, end_line=1)
    result = engine.convert_indentation(content, convert_range)
    
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
    
    config = ConvertConfig(scope=ConvertScope.DOCUMENT)
    engine = ConvertIndentationEngine(config)
    
    content = "def test():\n\tpass\n\treturn"
    result = engine.convert_indentation(content)
    
    assert result.success, "Dönüştürme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Convert document")
    print("=" * 70)


def test_set_tab_size():
    """
    Test: Set tab size.
    """
    print("=" * 70)
    print("TEST: Set Tab Size")
    print("=" * 70)
    
    engine = ConvertIndentationEngine()
    
    result = engine.set_tab_size(2)
    
    assert result.success, "Ayar başarılı olmalı"
    assert engine.config.tab_size == 2, "Tab size eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Tab size: {engine.config.tab_size}")
    
    print("\n" + "=" * 70)
    print("PASS: Set tab size")
    print("=" * 70)


def test_invalid_tab_size():
    """
    Test: Invalid tab size.
    """
    print("=" * 70)
    print("TEST: Invalid Tab Size")
    print("=" * 70)
    
    engine = ConvertIndentationEngine()
    
    result = engine.set_tab_size(0)
    
    assert result.success == False, "Başarısız olmalı"
    assert len(result.errors) > 0, "Hata olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Errors: {result.errors}")
    
    print("\n" + "=" * 70)
    print("PASS: Invalid tab size")
    print("=" * 70)


def test_undo_convert():
    """
    Test: Undo convert.
    """
    print("=" * 70)
    print("TEST: Undo Convert")
    print("=" * 70)
    
    engine = ConvertIndentationEngine()
    
    content = "def test():\n\tpass"
    engine.convert_tabs_to_spaces(content)
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
    
    engine = ConvertIndentationEngine()
    
    content = "def test():\n\tpass"
    engine.convert_tabs_to_spaces(content)
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
    
    engine = ConvertIndentationEngine()
    
    content = "def test():\n\tpass"
    engine.convert_tabs_to_spaces(content)
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
    
    engine = ConvertIndentationEngine()
    
    new_config = ConvertConfig(target_type=IndentationType.TABS, tab_size=2)
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
    
    engine = ConvertIndentationEngine()
    
    config = engine.get_config()
    
    assert config is not None, "Config olmalı"
    assert config.target_type == IndentationType.SPACES, "Config eşleşmeli"
    
    print(f"  Target type: {config.target_type.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


def test_indentation_type_enum():
    """
    Test: IndentationType enum.
    """
    print("=" * 70)
    print("TEST: IndentationType Enum")
    print("=" * 70)
    
    assert IndentationType.SPACES.value == "spaces"
    assert IndentationType.TABS.value == "tabs"
    
    print(f"  All enum values verified")
    print(f"  Total types: {len(IndentationType)}")
    
    print("\n" + "=" * 70)
    print("PASS: IndentationType enum")
    print("=" * 70)


def test_convert_scope_enum():
    """
    Test: ConvertScope enum.
    """
    print("=" * 70)
    print("TEST: ConvertScope Enum")
    print("=" * 70)
    
    assert ConvertScope.LINE.value == "line"
    assert ConvertScope.SELECTION.value == "selection"
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


def test_convert_config_dataclass():
    """
    Test: ConvertConfig dataclass.
    """
    print("=" * 70)
    print("TEST: ConvertConfig Dataclass")
    print("=" * 70)
    
    config = ConvertConfig(
        target_type=IndentationType.SPACES,
        tab_size=4,
        preserve_relative_indent=True
    )
    
    assert config.target_type == IndentationType.SPACES, "Target type eşleşmeli"
    assert config.tab_size == 4, "Tab size eşleşmeli"
    assert config.preserve_relative_indent == True, "Preserve relative indent eşleşmeli"
    
    print(f"  Target type: {config.target_type.value}")
    print(f"  Tab size: {config.tab_size}")
    print(f"  Preserve relative indent: {config.preserve_relative_indent}")
    
    print("\n" + "=" * 70)
    print("PASS: ConvertConfig dataclass")
    print("=" * 70)


def test_convert_result_dataclass():
    """
    Test: ConvertResult dataclass.
    """
    print("=" * 70)
    print("TEST: ConvertResult Dataclass")
    print("=" * 70)
    
    result = ConvertResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: ConvertResult dataclass")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_convert_indentation()
        test2 = test_convert_tabs_to_spaces()
        test3 = test_convert_spaces_to_tabs()
        test4 = test_convert_selection()
        test5 = test_convert_line()
        test6 = test_convert_document()
        test7 = test_set_tab_size()
        test8 = test_invalid_tab_size()
        test9 = test_undo_convert()
        test10 = test_get_convert_history()
        test11 = test_clear_history()
        test12 = test_update_config()
        test13 = test_get_config()
        test14 = test_indentation_type_enum()
        test15 = test_convert_scope_enum()
        test16 = test_convert_range_dataclass()
        test17 = test_convert_config_dataclass()
        test18 = test_convert_result_dataclass()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Convert Indentation: {'PASS' if test1 else 'FAIL'}")
        print(f"Convert Tabs to Spaces: {'PASS' if test2 else 'FAIL'}")
        print(f"Convert Spaces to Tabs: {'PASS' if test3 else 'FAIL'}")
        print(f"Convert Selection: {'PASS' if test4 else 'FAIL'}")
        print(f"Convert Line: {'PASS' if test5 else 'FAIL'}")
        print(f"Convert Document: {'PASS' if test6 else 'FAIL'}")
        print(f"Set Tab Size: {'PASS' if test7 else 'FAIL'}")
        print(f"Invalid Tab Size: {'PASS' if test8 else 'FAIL'}")
        print(f"Undo Convert: {'PASS' if test9 else 'FAIL'}")
        print(f"Get Convert History: {'PASS' if test10 else 'FAIL'}")
        print(f"Clear History: {'PASS' if test11 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test12 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test13 else 'FAIL'}")
        print(f"IndentationType Enum: {'PASS' if test14 else 'FAIL'}")
        print(f"ConvertScope Enum: {'PASS' if test15 else 'FAIL'}")
        print(f"ConvertRange Dataclass: {'PASS' if test16 else 'FAIL'}")
        print(f"ConvertConfig Dataclass: {'PASS' if test17 else 'FAIL'}")
        print(f"ConvertResult Dataclass: {'PASS' if test18 else 'FAIL'}")
        
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
