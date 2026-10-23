"""
Quality Test: Word Wrap
Word wrap system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.word_wrap import (
    WordWrapEngine,
    WrapMode,
    WrapColumn,
    WrappedLine,
    WordWrapConfig,
    WordWrapResult
)


def test_wrap_text():
    """
    Test: Wrap text.
    """
    print("=" * 70)
    print("TEST: Wrap Text")
    print("=" * 70)
    
    config = WordWrapConfig()
    engine = WordWrapEngine(config)
    
    text = "This is a very long line that should be wrapped at column 20 for better readability."
    result = engine.wrap_text(text, column=20)
    
    assert result.success, "Wrap başarılı olmalı"
    assert result.wrapped_code is not None, "Kod wrap edilmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Wrapped lines: {len(result.wrapped_lines)}")
    print(f"  Result: {result.wrapped_code}")
    
    print("\n" + "=" * 70)
    print("PASS: Wrap text")
    print("=" * 70)


def test_unwrap_text():
    """
    Test: Unwrap text.
    """
    print("=" * 70)
    print("TEST: Unwrap Text")
    print("=" * 70)
    
    config = WordWrapConfig()
    engine = WordWrapEngine(config)
    
    text = "line1↵\nline2"
    result = engine.unwrap_text(text)
    
    assert result.success, "Unwrap başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Unwrapped: {result.wrapped_code}")
    
    print("\n" + "=" * 70)
    print("PASS: Unwrap text")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    config = WordWrapConfig()
    engine = WordWrapEngine(config)
    
    new_config = WordWrapConfig(enabled=False)
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
    
    config = WordWrapConfig()
    engine = WordWrapEngine(config)
    
    retrieved_config = engine.get_config()
    
    assert retrieved_config is not None, "Config olmalı"
    assert retrieved_config.enabled == True, "Config eşleşmeli"
    
    print(f"  Enabled: {retrieved_config.enabled}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


def test_toggle_wrap():
    """
    Test: Toggle wrap.
    """
    print("=" * 70)
    print("TEST: Toggle Wrap")
    print("=" * 70)
    
    config = WordWrapConfig()
    engine = WordWrapEngine(config)
    
    result = engine.toggle_wrap()
    
    assert result.success, "Toggle başarılı olmalı"
    assert engine.config.enabled == False, "Disabled olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Toggle wrap")
    print("=" * 70)


def test_set_wrap_mode():
    """
    Test: Set wrap mode.
    """
    print("=" * 70)
    print("TEST: Set Wrap Mode")
    print("=" * 70)
    
    config = WordWrapConfig()
    engine = WordWrapEngine(config)
    
    result = engine.set_wrap_mode(WrapMode.CHARACTER)
    
    assert result.success, "Ayar başarılı olmalı"
    assert engine.config.wrap_mode == WrapMode.CHARACTER, "Mode eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Mode: {engine.config.wrap_mode.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Set wrap mode")
    print("=" * 70)


def test_set_wrap_column():
    """
    Test: Set wrap column.
    """
    print("=" * 70)
    print("TEST: Set Wrap Column")
    print("=" * 70)
    
    config = WordWrapConfig()
    engine = WordWrapEngine(config)
    
    result = engine.set_wrap_column(WrapColumn.COLUMN_120)
    
    assert result.success, "Ayar başarılı olmalı"
    assert engine.config.wrap_column == WrapColumn.COLUMN_120, "Column eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Column: {engine.config.wrap_column.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Set wrap column")
    print("=" * 70)


def test_set_custom_column():
    """
    Test: Set custom column.
    """
    print("=" * 70)
    print("TEST: Set Custom Column")
    print("=" * 70)
    
    config = WordWrapConfig()
    engine = WordWrapEngine(config)
    
    result = engine.set_custom_column(100)
    
    assert result.success, "Ayar başarılı olmalı"
    assert engine.config.custom_column == 100, "Custom column eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Custom column: {engine.config.custom_column}")
    
    print("\n" + "=" * 70)
    print("PASS: Set custom column")
    print("=" * 70)


def test_get_wrapped_lines():
    """
    Test: Get wrapped lines.
    """
    print("=" * 70)
    print("TEST: Get Wrapped Lines")
    print("=" * 70)
    
    config = WordWrapConfig()
    engine = WordWrapEngine(config)
    
    text = "This is a long line"
    engine.wrap_text(text, column=10)
    
    wrapped_lines = engine.get_wrapped_lines()
    
    assert len(wrapped_lines) > 0, "Wrap edilmiş satırlar olmalı"
    
    print(f"  Wrapped lines: {len(wrapped_lines)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get wrapped lines")
    print("=" * 70)


def test_wrap_mode_enum():
    """
    Test: WrapMode enum.
    """
    print("=" * 70)
    print("TEST: WrapMode Enum")
    print("=" * 70)
    
    assert WrapMode.NONE.value == "none"
    assert WrapMode.WORD.value == "word"
    assert WrapMode.CHARACTER.value == "character"
    assert WrapMode.BOUNDARY.value == "boundary"
    
    print(f"  All enum values verified")
    print(f"  Total modes: {len(WrapMode)}")
    
    print("\n" + "=" * 70)
    print("PASS: WrapMode enum")
    print("=" * 70)


def test_wrap_column_enum():
    """
    Test: WrapColumn enum.
    """
    print("=" * 70)
    print("TEST: WrapColumn Enum")
    print("=" * 70)
    
    assert WrapColumn.COLUMN_80.value == 80
    assert WrapColumn.COLUMN_100.value == 100
    assert WrapColumn.COLUMN_120.value == 120
    assert WrapColumn.CUSTOM.value == "custom"
    
    print(f"  All enum values verified")
    print(f"  Total columns: {len(WrapColumn)}")
    
    print("\n" + "=" * 70)
    print("PASS: WrapColumn enum")
    print("=" * 70)


def test_wrapped_line_dataclass():
    """
    Test: WrappedLine dataclass.
    """
    print("=" * 70)
    print("TEST: WrappedLine Dataclass")
    print("=" * 70)
    
    wrapped_line = WrappedLine(
        original_line=0,
        wrapped_lines=["line1", "line2"],
        wrap_positions=[0, 10]
    )
    
    assert wrapped_line.original_line == 0, "Original line eşleşmeli"
    assert len(wrapped_line.wrapped_lines) == 2, "Wrapped lines eşleşmeli"
    
    print(f"  Original line: {wrapped_line.original_line}")
    print(f"  Wrapped lines: {len(wrapped_line.wrapped_lines)}")
    
    print("\n" + "=" * 70)
    print("PASS: WrappedLine dataclass")
    print("=" * 70)


def test_word_wrap_config_dataclass():
    """
    Test: WordWrapConfig dataclass.
    """
    print("=" * 70)
    print("TEST: WordWrapConfig Dataclass")
    print("=" * 70)
    
    config = WordWrapConfig(
        enabled=True,
        wrap_mode=WrapMode.WORD,
        wrap_column=WrapColumn.COLUMN_80
    )
    
    assert config.enabled == True, "Enabled eşleşmeli"
    assert config.wrap_mode == WrapMode.WORD, "Mode eşleşmeli"
    assert config.wrap_column == WrapColumn.COLUMN_80, "Column eşleşmeli"
    
    print(f"  Enabled: {config.enabled}")
    print(f"  Mode: {config.wrap_mode.value}")
    print(f"  Column: {config.wrap_column.value}")
    
    print("\n" + "=" * 70)
    print("PASS: WordWrapConfig dataclass")
    print("=" * 70)


def test_word_wrap_result_dataclass():
    """
    Test: WordWrapResult dataclass.
    """
    print("=" * 70)
    print("TEST: WordWrapResult Dataclass")
    print("=" * 70)
    
    result = WordWrapResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.wrapped_lines, list), "Wrapped lines list olmalı"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Wrapped lines: {len(result.wrapped_lines)}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: WordWrapResult dataclass")
    print("=" * 70)


def test_word_wrap_mode():
    """
    Test: Word wrap mode.
    """
    print("=" * 70)
    print("TEST: Word Wrap Mode")
    print("=" * 70)
    
    config = WordWrapConfig(wrap_mode=WrapMode.WORD)
    engine = WordWrapEngine(config)
    
    text = "This is a test line with multiple words"
    result = engine.wrap_text(text, column=15)
    
    assert result.success, "Word wrap başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Mode: {config.wrap_mode.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Word wrap mode")
    print("=" * 70)


def test_character_wrap_mode():
    """
    Test: Character wrap mode.
    """
    print("=" * 70)
    print("TEST: Character Wrap Mode")
    print("=" * 70)
    
    config = WordWrapConfig(wrap_mode=WrapMode.CHARACTER)
    engine = WordWrapEngine(config)
    
    text = "Thisisalongword"
    result = engine.wrap_text(text, column=5)
    
    assert result.success, "Character wrap başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Mode: {config.wrap_mode.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Character wrap mode")
    print("=" * 70)


def test_boundary_wrap_mode():
    """
    Test: Boundary wrap mode.
    """
    print("=" * 70)
    print("TEST: Boundary Wrap Mode")
    print("=" * 70)
    
    config = WordWrapConfig(wrap_mode=WrapMode.BOUNDARY)
    engine = WordWrapEngine(config)
    
    text = "This is a test line"
    result = engine.wrap_text(text, column=10)
    
    assert result.success, "Boundary wrap başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Mode: {config.wrap_mode.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Boundary wrap mode")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_wrap_text()
        test2 = test_unwrap_text()
        test3 = test_update_config()
        test4 = test_get_config()
        test5 = test_toggle_wrap()
        test6 = test_set_wrap_mode()
        test7 = test_set_wrap_column()
        test8 = test_set_custom_column()
        test9 = test_get_wrapped_lines()
        test10 = test_wrap_mode_enum()
        test11 = test_wrap_column_enum()
        test12 = test_wrapped_line_dataclass()
        test13 = test_word_wrap_config_dataclass()
        test14 = test_word_wrap_result_dataclass()
        test15 = test_word_wrap_mode()
        test16 = test_character_wrap_mode()
        test17 = test_boundary_wrap_mode()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Wrap Text: {'PASS' if test1 else 'FAIL'}")
        print(f"Unwrap Text: {'PASS' if test2 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test3 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test4 else 'FAIL'}")
        print(f"Toggle Wrap: {'PASS' if test5 else 'FAIL'}")
        print(f"Set Wrap Mode: {'PASS' if test6 else 'FAIL'}")
        print(f"Set Wrap Column: {'PASS' if test7 else 'FAIL'}")
        print(f"Set Custom Column: {'PASS' if test8 else 'FAIL'}")
        print(f"Get Wrapped Lines: {'PASS' if test9 else 'FAIL'}")
        print(f"WrapMode Enum: {'PASS' if test10 else 'FAIL'}")
        print(f"WrapColumn Enum: {'PASS' if test11 else 'FAIL'}")
        print(f"WrappedLine Dataclass: {'PASS' if test12 else 'FAIL'}")
        print(f"WordWrapConfig Dataclass: {'PASS' if test13 else 'FAIL'}")
        print(f"WordWrapResult Dataclass: {'PASS' if test14 else 'FAIL'}")
        print(f"Word Wrap Mode: {'PASS' if test15 else 'FAIL'}")
        print(f"Character Wrap Mode: {'PASS' if test16 else 'FAIL'}")
        print(f"Boundary Wrap Mode: {'PASS' if test17 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14, test15, test16, test17])
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
