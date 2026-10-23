"""
Quality Test: Inline Variable
Inline variable system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.inline_variable import (
    InlineVariableEngine,
    InlineMode,
    InlineScope,
    VariableReference,
    InlineConfig,
    InlineResult
)


def test_inline_variable():
    """
    Test: Inline variable.
    """
    print("=" * 70)
    print("TEST: Inline Variable")
    print("=" * 70)
    
    engine = InlineVariableEngine()
    
    content = "x = 42\nprint(x)"
    result = engine.inline_variable(content, "x")
    
    assert result.success, "Inline başarılı olmalı"
    assert result.references_removed > 0, "Referans kaldırılmalı"
    
    print(f"  Success: {result.success}")
    print(f"  References removed: {result.references_removed}")
    
    print("\n" + "=" * 70)
    print("PASS: Inline variable")
    print("=" * 70)


def test_inline_with_line_number():
    """
    Test: Inline with line number.
    """
    print("=" * 70)
    print("TEST: Inline With Line Number")
    print("=" * 70)
    
    engine = InlineVariableEngine()
    
    content = "x = 42\nprint(x)"
    result = engine.inline_variable(content, "x", line_number=0)
    
    assert result.success, "Inline başarılı olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Inline with line number")
    print("=" * 70)


def test_inline_empty_variable_name():
    """
    Test: Inline empty variable name.
    """
    print("=" * 70)
    print("TEST: Inline Empty Variable Name")
    print("=" * 70)
    
    engine = InlineVariableEngine()
    
    content = "x = 42"
    result = engine.inline_variable(content, "")
    
    assert result.success == False, "Başarısız olmalı"
    assert len(result.errors) > 0, "Hata olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Errors: {result.errors}")
    
    print("\n" + "=" * 70)
    print("PASS: Inline empty variable name")
    print("=" * 70)


def test_inline_nonexistent_variable():
    """
    Test: Inline nonexistent variable.
    """
    print("=" * 70)
    print("TEST: Inline Nonexistent Variable")
    print("=" * 70)
    
    engine = InlineVariableEngine()
    
    content = "x = 42"
    result = engine.inline_variable(content, "y")
    
    assert result.success == False, "Başarısız olmalı"
    assert len(result.errors) > 0, "Hata olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Errors: {result.errors}")
    
    print("\n" + "=" * 70)
    print("PASS: Inline nonexistent variable")
    print("=" * 70)


def test_undo_inline():
    """
    Test: Undo inline.
    """
    print("=" * 70)
    print("TEST: Undo Inline")
    print("=" * 70)
    
    engine = InlineVariableEngine()
    
    content = "x = 42\nprint(x)"
    engine.inline_variable(content, "x")
    result = engine.undo_inline()
    
    assert result.success, "Geri alma başarılı olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Undo inline")
    print("=" * 70)


def test_get_inline_history():
    """
    Test: Get inline history.
    """
    print("=" * 70)
    print("TEST: Get Inline History")
    print("=" * 70)
    
    engine = InlineVariableEngine()
    
    engine.inline_variable("x = 42\nprint(x)", "x")
    history = engine.get_inline_history()
    
    assert len(history) > 0, "Geçmiş olmalı"
    
    print(f"  History: {len(history)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get inline history")
    print("=" * 70)


def test_clear_history():
    """
    Test: Clear history.
    """
    print("=" * 70)
    print("TEST: Clear History")
    print("=" * 70)
    
    engine = InlineVariableEngine()
    
    engine.inline_variable("x = 42\nprint(x)", "x")
    result = engine.clear_history()
    
    assert result.success, "Temizleme başarılı olmalı"
    assert len(engine.get_inline_history()) == 0, "Geçmiş temizlenmeli"
    
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
    
    engine = InlineVariableEngine()
    
    new_config = InlineConfig(inline_mode=InlineMode.ALL_OCCURRENCES)
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
    
    engine = InlineVariableEngine()
    
    config = engine.get_config()
    
    assert config is not None, "Config olmalı"
    assert config.inline_mode == InlineMode.SINGLE_OCCURRENCE, "Config eşleşmeli"
    
    print(f"  Inline mode: {config.inline_mode.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


def test_inline_mode_enum():
    """
    Test: InlineMode enum.
    """
    print("=" * 70)
    print("TEST: InlineMode Enum")
    print("=" * 70)
    
    assert InlineMode.SINGLE_OCCURRENCE.value == "single_occurrence"
    assert InlineMode.ALL_OCCURRENCES.value == "all_occurrences"
    assert InlineMode.SELECTED_OCCURRENCES.value == "selected_occurrences"
    
    print(f"  All enum values verified")
    print(f"  Total modes: {len(InlineMode)}")
    
    print("\n" + "=" * 70)
    print("PASS: InlineMode enum")
    print("=" * 70)


def test_inline_scope_enum():
    """
    Test: InlineScope enum.
    """
    print("=" * 70)
    print("TEST: InlineScope Enum")
    print("=" * 70)
    
    assert InlineScope.LOCAL.value == "local"
    assert InlineScope.FUNCTION.value == "function"
    assert InlineScope.BLOCK.value == "block"
    
    print(f"  All enum values verified")
    print(f"  Total scopes: {len(InlineScope)}")
    
    print("\n" + "=" * 70)
    print("PASS: InlineScope enum")
    print("=" * 70)


def test_variable_reference_dataclass():
    """
    Test: VariableReference dataclass.
    """
    print("=" * 70)
    print("TEST: VariableReference Dataclass")
    print("=" * 70)
    
    reference = VariableReference(
        variable_name="x",
        line_number=0,
        column=0,
        is_definition=True
    )
    
    assert reference.variable_name == "x", "Variable name eşleşmeli"
    assert reference.line_number == 0, "Line number eşleşmeli"
    assert reference.is_definition == True, "Is definition eşleşmeli"
    
    print(f"  Variable name: {reference.variable_name}")
    print(f"  Line number: {reference.line_number}")
    print(f"  Is definition: {reference.is_definition}")
    
    print("\n" + "=" * 70)
    print("PASS: VariableReference dataclass")
    print("=" * 70)


def test_inline_config_dataclass():
    """
    Test: InlineConfig dataclass.
    """
    print("=" * 70)
    print("TEST: InlineConfig Dataclass")
    print("=" * 70)
    
    config = InlineConfig(
        inline_mode=InlineMode.SINGLE_OCCURRENCE,
        remove_unused=True,
        preserve_formatting=True
    )
    
    assert config.inline_mode == InlineMode.SINGLE_OCCURRENCE, "Inline mode eşleşmeli"
    assert config.remove_unused == True, "Remove unused eşleşmeli"
    assert config.preserve_formatting == True, "Preserve formatting eşleşmeli"
    
    print(f"  Inline mode: {config.inline_mode.value}")
    print(f"  Remove unused: {config.remove_unused}")
    print(f"  Preserve formatting: {config.preserve_formatting}")
    
    print("\n" + "=" * 70)
    print("PASS: InlineConfig dataclass")
    print("=" * 70)


def test_inline_result_dataclass():
    """
    Test: InlineResult dataclass.
    """
    print("=" * 70)
    print("TEST: InlineResult Dataclass")
    print("=" * 70)
    
    result = InlineResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: InlineResult dataclass")
    print("=" * 70)


def test_find_variable_value():
    """
    Test: Find variable value.
    """
    print("=" * 70)
    print("TEST: Find Variable Value")
    print("=" * 70)
    
    engine = InlineVariableEngine()
    
    content = "x = 42"
    value = engine._find_variable_value(content, "x", 0)
    
    assert value == "42", "Değer eşleşmeli"
    
    print(f"  Value: {value}")
    
    print("\n" + "=" * 70)
    print("PASS: Find variable value")
    print("=" * 70)


def test_find_references():
    """
    Test: Find references.
    """
    print("=" * 70)
    print("TEST: Find References")
    print("=" * 70)
    
    engine = InlineVariableEngine()
    
    content = "x = 42\nprint(x)"
    references = engine._find_references(content, "x")
    
    assert len(references) > 0, "Referans olmalı"
    
    print(f"  References: {len(references)}")
    
    print("\n" + "=" * 70)
    print("PASS: Find references")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_inline_variable()
        test2 = test_inline_with_line_number()
        test3 = test_inline_empty_variable_name()
        test4 = test_inline_nonexistent_variable()
        test5 = test_undo_inline()
        test6 = test_get_inline_history()
        test7 = test_clear_history()
        test8 = test_update_config()
        test9 = test_get_config()
        test10 = test_inline_mode_enum()
        test11 = test_inline_scope_enum()
        test12 = test_variable_reference_dataclass()
        test13 = test_inline_config_dataclass()
        test14 = test_inline_result_dataclass()
        test15 = test_find_variable_value()
        test16 = test_find_references()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Inline Variable: {'PASS' if test1 else 'FAIL'}")
        print(f"Inline With Line Number: {'PASS' if test2 else 'FAIL'}")
        print(f"Inline Empty Variable Name: {'PASS' if test3 else 'FAIL'}")
        print(f"Inline Nonexistent Variable: {'PASS' if test4 else 'FAIL'}")
        print(f"Undo Inline: {'PASS' if test5 else 'FAIL'}")
        print(f"Get Inline History: {'PASS' if test6 else 'FAIL'}")
        print(f"Clear History: {'PASS' if test7 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test8 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test9 else 'FAIL'}")
        print(f"InlineMode Enum: {'PASS' if test10 else 'FAIL'}")
        print(f"InlineScope Enum: {'PASS' if test11 else 'FAIL'}")
        print(f"VariableReference Dataclass: {'PASS' if test12 else 'FAIL'}")
        print(f"InlineConfig Dataclass: {'PASS' if test13 else 'FAIL'}")
        print(f"InlineResult Dataclass: {'PASS' if test14 else 'FAIL'}")
        print(f"Find Variable Value: {'PASS' if test15 else 'FAIL'}")
        print(f"Find References: {'PASS' if test16 else 'FAIL'}")
        
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
