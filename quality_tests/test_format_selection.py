"""
Quality Test: Format Selection
Format selection system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.format_selection import (
    FormatSelectionEngine,
    FormatScope,
    FormatTrigger,
    SelectionRange,
    FormatSelectionConfig,
    FormatSelectionResult
)


def test_format_selection():
    """
    Test: Format selection.
    """
    print("=" * 70)
    print("TEST: Format Selection")
    print("=" * 70)
    
    engine = FormatSelectionEngine()
    
    content = "def test( x,y ):\n    result=x+y\n    return result"
    selection = SelectionRange(start_line=0, end_line=2)
    result = engine.format_selection(content, selection)
    
    assert result.success, "Formatlama başarılı olmalı"
    assert result.lines_formatted > 0, "Satır formatlanmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Lines formatted: {result.lines_formatted}")
    
    print("\n" + "=" * 70)
    print("PASS: Format selection")
    print("=" * 70)


def test_format_line():
    """
    Test: Format line.
    """
    print("=" * 70)
    print("TEST: Format Line")
    print("=" * 70)
    
    engine = FormatSelectionEngine()
    
    content = "def test( x,y ):\n    result=x+y"
    result = engine.format_line(content, 0)
    
    assert result.success, "Formatlama başarılı olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Format line")
    print("=" * 70)


def test_format_block():
    """
    Test: Format block.
    """
    print("=" * 70)
    print("TEST: Format Block")
    print("=" * 70)
    
    engine = FormatSelectionEngine()
    
    content = "def test( x,y ):\n    result=x+y\n    return result"
    result = engine.format_block(content, 0, 2)
    
    assert result.success, "Formatlama başarılı olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Format block")
    print("=" * 70)


def test_format_document():
    """
    Test: Format document.
    """
    print("=" * 70)
    print("TEST: Format Document")
    print("=" * 70)
    
    engine = FormatSelectionEngine()
    
    content = "def test( x,y ):\n    result=x+y\n    return result"
    result = engine.format_document(content)
    
    assert result.success, "Formatlama başarılı olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Format document")
    print("=" * 70)


def test_invalid_selection():
    """
    Test: Invalid selection.
    """
    print("=" * 70)
    print("TEST: Invalid Selection")
    print("=" * 70)
    
    engine = FormatSelectionEngine()
    
    content = "def test():\n    pass"
    selection = SelectionRange(start_line=10, end_line=20)
    result = engine.format_selection(content, selection)
    
    assert result.success == False, "Başarısız olmalı"
    assert len(result.errors) > 0, "Hata olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Errors: {result.errors}")
    
    print("\n" + "=" * 70)
    print("PASS: Invalid selection")
    print("=" * 70)


def test_normalize_whitespace():
    """
    Test: Normalize whitespace.
    """
    print("=" * 70)
    print("TEST: Normalize Whitespace")
    print("=" * 70)
    
    engine = FormatSelectionEngine()
    engine.config.normalize_whitespace = True
    
    line = "x  =  1  +  2"
    result = engine._normalize_whitespace(line)
    
    assert "  " not in result, "Multiple space olmamalı"
    
    print(f"  Original: '{line}'")
    print(f"  Normalized: '{result}'")
    
    print("\n" + "=" * 70)
    print("PASS: Normalize whitespace")
    print("=" * 70)


def test_fix_operator_spacing():
    """
    Test: Fix operator spacing.
    """
    print("=" * 70)
    print("TEST: Fix Operator Spacing")
    print("=" * 70)
    
    engine = FormatSelectionEngine()
    
    line = "x=1+2"
    result = engine._fix_operator_spacing(line)
    
    assert "= " in result or " =" in result, "Operator spacing düzeltilmeli"
    
    print(f"  Original: '{line}'")
    print(f"  Fixed: '{result}'")
    
    print("\n" + "=" * 70)
    print("PASS: Fix operator spacing")
    print("=" * 70)


def test_fix_comma_spacing():
    """
    Test: Fix comma spacing.
    """
    print("=" * 70)
    print("TEST: Fix Comma Spacing")
    print("=" * 70)
    
    engine = FormatSelectionEngine()
    
    line = "func(a,b,c)"
    result = engine._fix_comma_spacing(line)
    
    assert ", " in result, "Comma spacing düzeltilmeli"
    
    print(f"  Original: '{line}'")
    print(f"  Fixed: '{result}'")
    
    print("\n" + "=" * 70)
    print("PASS: Fix comma spacing")
    print("=" * 70)


def test_fix_paren_spacing():
    """
    Test: Fix paren spacing.
    """
    print("=" * 70)
    print("TEST: Fix Paren Spacing")
    print("=" * 70)
    
    engine = FormatSelectionEngine()
    
    line = "func (x)"
    result = engine._fix_paren_spacing(line)
    
    assert "( " not in result, "Space before paren kaldırılmalı"
    
    print(f"  Original: '{line}'")
    print(f"  Fixed: '{result}'")
    
    print("\n" + "=" * 70)
    print("PASS: Fix paren spacing")
    print("=" * 70)


def test_normalize_quotes():
    """
    Test: Normalize quotes.
    """
    print("=" * 70)
    print("TEST: Normalize Quotes")
    print("=" * 70)
    
    engine = FormatSelectionEngine()
    engine.config.normalize_quotes = True
    
    line = "text = 'hello'"
    result = engine._normalize_quotes(line)
    
    assert '"' in result, "Double quote olmalı"
    
    print(f"  Original: '{line}'")
    print(f"  Normalized: '{result}'")
    
    print("\n" + "=" * 70)
    print("PASS: Normalize quotes")
    print("=" * 70)


def test_trim_blank_lines():
    """
    Test: Trim blank lines.
    """
    print("=" * 70)
    print("TEST: Trim Blank Lines")
    print("=" * 70)
    
    engine = FormatSelectionEngine()
    
    lines = ["line1", "", "", "", "line2"]
    result = engine._trim_blank_lines(lines)
    
    assert len(result) < len(lines), "Blank line azalmalı"
    
    print(f"  Original: {len(lines)} lines")
    print(f"  Trimmed: {len(result)} lines")
    
    print("\n" + "=" * 70)
    print("PASS: Trim blank lines")
    print("=" * 70)


def test_undo_format():
    """
    Test: Undo format.
    """
    print("=" * 70)
    print("TEST: Undo Format")
    print("=" * 70)
    
    engine = FormatSelectionEngine()
    
    content = "def test( x,y ):\n    result=x+y"
    selection = SelectionRange(start_line=0, end_line=1)
    engine.format_selection(content, selection)
    result = engine.undo_format()
    
    assert result.success, "Geri alma başarılı olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Undo format")
    print("=" * 70)


def test_get_format_history():
    """
    Test: Get format history.
    """
    print("=" * 70)
    print("TEST: Get Format History")
    print("=" * 70)
    
    engine = FormatSelectionEngine()
    
    content = "def test( x,y ):\n    result=x+y"
    selection = SelectionRange(start_line=0, end_line=1)
    engine.format_selection(content, selection)
    history = engine.get_format_history()
    
    assert len(history) > 0, "Geçmiş olmalı"
    
    print(f"  History: {len(history)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get format history")
    print("=" * 70)


def test_clear_history():
    """
    Test: Clear history.
    """
    print("=" * 70)
    print("TEST: Clear History")
    print("=" * 70)
    
    engine = FormatSelectionEngine()
    
    content = "def test( x,y ):\n    result=x+y"
    selection = SelectionRange(start_line=0, end_line=1)
    engine.format_selection(content, selection)
    result = engine.clear_history()
    
    assert result.success, "Temizleme başarılı olmalı"
    assert len(engine.get_format_history()) == 0, "Geçmiş temizlenmeli"
    
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
    
    engine = FormatSelectionEngine()
    
    new_config = FormatSelectionConfig(preserve_indentation=False)
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
    
    engine = FormatSelectionEngine()
    
    config = engine.get_config()
    
    assert config is not None, "Config olmalı"
    assert config.preserve_indentation == True, "Config eşleşmeli"
    
    print(f"  Preserve indentation: {config.preserve_indentation}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


def test_format_scope_enum():
    """
    Test: FormatScope enum.
    """
    print("=" * 70)
    print("TEST: FormatScope Enum")
    print("=" * 70)
    
    assert FormatScope.SELECTION.value == "selection"
    assert FormatScope.LINE.value == "line"
    assert FormatScope.BLOCK.value == "block"
    assert FormatScope.FUNCTION.value == "function"
    assert FormatScope.DOCUMENT.value == "document"
    
    print(f"  All enum values verified")
    print(f"  Total scopes: {len(FormatScope)}")
    
    print("\n" + "=" * 70)
    print("PASS: FormatScope enum")
    print("=" * 70)


def test_format_trigger_enum():
    """
    Test: FormatTrigger enum.
    """
    print("=" * 70)
    print("TEST: FormatTrigger Enum")
    print("=" * 70)
    
    assert FormatTrigger.MANUAL.value == "manual"
    assert FormatTrigger.ON_SAVE.value == "on_save"
    assert FormatTrigger.ON_PASTE.value == "on_paste"
    assert FormatTrigger.ON_TYPE.value == "on_type"
    assert FormatTrigger.AUTO.value == "auto"
    
    print(f"  All enum values verified")
    print(f"  Total triggers: {len(FormatTrigger)}")
    
    print("\n" + "=" * 70)
    print("PASS: FormatTrigger enum")
    print("=" * 70)


def test_selection_range_dataclass():
    """
    Test: SelectionRange dataclass.
    """
    print("=" * 70)
    print("TEST: SelectionRange Dataclass")
    print("=" * 70)
    
    selection = SelectionRange(
        start_line=0,
        end_line=5,
        start_column=0,
        end_column=10
    )
    
    assert selection.start_line == 0, "Start line eşleşmeli"
    assert selection.end_line == 5, "End line eşleşmeli"
    
    print(f"  Start line: {selection.start_line}")
    print(f"  End line: {selection.end_line}")
    
    print("\n" + "=" * 70)
    print("PASS: SelectionRange dataclass")
    print("=" * 70)


def test_format_selection_config_dataclass():
    """
    Test: FormatSelectionConfig dataclass.
    """
    print("=" * 70)
    print("TEST: FormatSelectionConfig Dataclass")
    print("=" * 70)
    
    config = FormatSelectionConfig(
        format_scope=FormatScope.SELECTION,
        preserve_indentation=True,
        normalize_whitespace=True
    )
    
    assert config.format_scope == FormatScope.SELECTION, "Format scope eşleşmeli"
    assert config.preserve_indentation == True, "Preserve indentation eşleşmeli"
    assert config.normalize_whitespace == True, "Normalize whitespace eşleşmeli"
    
    print(f"  Format scope: {config.format_scope.value}")
    print(f"  Preserve indentation: {config.preserve_indentation}")
    print(f"  Normalize whitespace: {config.normalize_whitespace}")
    
    print("\n" + "=" * 70)
    print("PASS: FormatSelectionConfig dataclass")
    print("=" * 70)


def test_format_selection_result_dataclass():
    """
    Test: FormatSelectionResult dataclass.
    """
    print("=" * 70)
    print("TEST: FormatSelectionResult Dataclass")
    print("=" * 70)
    
    result = FormatSelectionResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: FormatSelectionResult dataclass")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_format_selection()
        test2 = test_format_line()
        test3 = test_format_block()
        test4 = test_format_document()
        test5 = test_invalid_selection()
        test6 = test_normalize_whitespace()
        test7 = test_fix_operator_spacing()
        test8 = test_fix_comma_spacing()
        test9 = test_fix_paren_spacing()
        test10 = test_normalize_quotes()
        test11 = test_trim_blank_lines()
        test12 = test_undo_format()
        test13 = test_get_format_history()
        test14 = test_clear_history()
        test15 = test_update_config()
        test16 = test_get_config()
        test17 = test_format_scope_enum()
        test18 = test_format_trigger_enum()
        test19 = test_selection_range_dataclass()
        test20 = test_format_selection_config_dataclass()
        test21 = test_format_selection_result_dataclass()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Format Selection: {'PASS' if test1 else 'FAIL'}")
        print(f"Format Line: {'PASS' if test2 else 'FAIL'}")
        print(f"Format Block: {'PASS' if test3 else 'FAIL'}")
        print(f"Format Document: {'PASS' if test4 else 'FAIL'}")
        print(f"Invalid Selection: {'PASS' if test5 else 'FAIL'}")
        print(f"Normalize Whitespace: {'PASS' if test6 else 'FAIL'}")
        print(f"Fix Operator Spacing: {'PASS' if test7 else 'FAIL'}")
        print(f"Fix Comma Spacing: {'PASS' if test8 else 'FAIL'}")
        print(f"Fix Paren Spacing: {'PASS' if test9 else 'FAIL'}")
        print(f"Normalize Quotes: {'PASS' if test10 else 'FAIL'}")
        print(f"Trim Blank Lines: {'PASS' if test11 else 'FAIL'}")
        print(f"Undo Format: {'PASS' if test12 else 'FAIL'}")
        print(f"Get Format History: {'PASS' if test13 else 'FAIL'}")
        print(f"Clear History: {'PASS' if test14 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test15 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test16 else 'FAIL'}")
        print(f"FormatScope Enum: {'PASS' if test17 else 'FAIL'}")
        print(f"FormatTrigger Enum: {'PASS' if test18 else 'FAIL'}")
        print(f"SelectionRange Dataclass: {'PASS' if test19 else 'FAIL'}")
        print(f"FormatSelectionConfig Dataclass: {'PASS' if test20 else 'FAIL'}")
        print(f"FormatSelectionResult Dataclass: {'PASS' if test21 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14, test15, test16, test17, test18, test19, test20, test21])
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
