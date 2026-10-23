"""
Quality Test: Formatting
Formatting system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.formatting import (
    FormattingMode,
    FormattingTriggerKind,
    Position,
    Range,
    TextEdit,
    FormattingOptions,
    DocumentFormattingParams,
    FormattingConfig,
    FormattingEngine
)


def test_formatting_mode_enum():
    """
    Test: FormattingMode enum.
    """
    print("=" * 70)
    print("TEST: FormattingMode Enum")
    print("=" * 70)
    
    assert FormattingMode.FULL.value == "full"
    assert FormattingMode.RANGE.value == "range"
    assert FormattingMode.ON_TYPE.value == "on_type"
    
    print(f"  All enum values verified")
    print(f"  Total modes: {len(FormattingMode)}")
    
    print("\n" + "=" * 70)
    print("PASS: FormattingMode enum")
    print("=" * 70)


def test_formatting_trigger_kind_enum():
    """
    Test: FormattingTriggerKind enum.
    """
    print("=" * 70)
    print("TEST: FormattingTriggerKind Enum")
    print("=" * 70)
    
    assert FormattingTriggerKind.ON_SAVE.value == "on_save"
    assert FormattingTriggerKind.ON_TYPE.value == "on_type"
    assert FormattingTriggerKind.MANUAL.value == "manual"
    
    print(f"  All enum values verified")
    print(f"  Total kinds: {len(FormattingTriggerKind)}")
    
    print("\n" + "=" * 70)
    print("PASS: FormattingTriggerKind enum")
    print("=" * 70)


def test_position_dataclass():
    """
    Test: Position dataclass.
    """
    print("=" * 70)
    print("TEST: Position Dataclass")
    print("=" * 70)
    
    position = Position(line=1, character=0)
    
    assert position.line == 1, "Line eşleşmeli"
    assert position.character == 0, "Character eşleşmeli"
    
    print(f"  Line: {position.line}")
    print(f"  Character: {position.character}")
    
    print("\n" + "=" * 70)
    print("PASS: Position dataclass")
    print("=" * 70)


def test_range_dataclass():
    """
    Test: Range dataclass.
    """
    print("=" * 70)
    print("TEST: Range Dataclass")
    print("=" * 70)
    
    range_obj = Range(
        start=Position(line=1, character=0),
        end=Position(line=2, character=10)
    )
    
    assert range_obj.start.line == 1, "Start line eşleşmeli"
    assert range_obj.end.line == 2, "End line eşleşmeli"
    
    print(f"  Start line: {range_obj.start.line}")
    print(f"  End line: {range_obj.end.line}")
    
    print("\n" + "=" * 70)
    print("PASS: Range dataclass")
    print("=" * 70)


def test_text_edit_dataclass():
    """
    Test: TextEdit dataclass.
    """
    print("=" * 70)
    print("TEST: TextEdit Dataclass")
    print("=" * 70)
    
    text_edit = TextEdit(
        range=Range(
            start=Position(line=0, character=0),
            end=Position(line=1, character=0)
        ),
        newText="test"
    )
    
    assert text_edit.newText == "test", "New text eşleşmeli"
    
    print(f"  New text: {text_edit.newText}")
    
    print("\n" + "=" * 70)
    print("PASS: TextEdit dataclass")
    print("=" * 70)


def test_formatting_options_dataclass():
    """
    Test: FormattingOptions dataclass.
    """
    print("=" * 70)
    print("TEST: FormattingOptions Dataclass")
    print("=" * 70)
    
    options = FormattingOptions(
        tab_size=4,
        insert_spaces=True
    )
    
    assert options.tab_size == 4, "Tab size eşleşmeli"
    assert options.insert_spaces == True, "Insert spaces eşleşmeli"
    
    print(f"  Tab size: {options.tab_size}")
    print(f"  Insert spaces: {options.insert_spaces}")
    
    print("\n" + "=" * 70)
    print("PASS: FormattingOptions dataclass")
    print("=" * 70)


def test_document_formatting_params_dataclass():
    """
    Test: DocumentFormattingParams dataclass.
    """
    print("=" * 70)
    print("TEST: DocumentFormattingParams Dataclass")
    print("=" * 70)
    
    params = DocumentFormattingParams(
        options=FormattingOptions()
    )
    
    assert params.options is not None, "Options olmalı"
    
    print(f"  Options: {params.options}")
    
    print("\n" + "=" * 70)
    print("PASS: DocumentFormattingParams dataclass")
    print("=" * 70)


def test_formatting_config_dataclass():
    """
    Test: FormattingConfig dataclass.
    """
    print("=" * 70)
    print("TEST: FormattingConfig Dataclass")
    print("=" * 70)
    
    config = FormattingConfig(
        mode=FormattingMode.FULL,
        auto_format=False
    )
    
    assert config.mode == FormattingMode.FULL, "Mode eşleşmeli"
    assert config.auto_format == False, "Auto format eşleşmeli"
    
    print(f"  Mode: {config.mode.value}")
    print(f"  Auto format: {config.auto_format}")
    
    print("\n" + "=" * 70)
    print("PASS: FormattingConfig dataclass")
    print("=" * 70)


def test_formatting_engine_initialization():
    """
    Test: FormattingEngine initialization.
    """
    print("=" * 70)
    print("TEST: FormattingEngine Initialization")
    print("=" * 70)
    
    config = FormattingConfig()
    engine = FormattingEngine(config)
    
    assert engine.config == config, "Config eşleşmeli"
    assert len(engine.rules) > 0, "Rules olmalı"
    
    print(f"  Rules: {len(engine.rules)}")
    
    print("\n" + "=" * 70)
    print("PASS: FormattingEngine initialization")
    print("=" * 70)


def test_format_document():
    """
    Test: Format document.
    """
    print("=" * 70)
    print("TEST: Format Document")
    print("=" * 70)
    
    engine = FormattingEngine()
    
    text = "def hello():\n    pass    "
    
    params = DocumentFormattingParams(options=FormattingOptions(trim_trailing_whitespace=True))
    edits = engine.format_document(text, "python", params)
    
    assert edits is not None, "Edits olmalı"
    assert isinstance(edits, list), "List olmalı"
    
    print(f"  Edits: {len(edits)}")
    
    print("\n" + "=" * 70)
    print("PASS: Format document")
    print("=" * 70)


def test_format_range():
    """
    Test: Format range.
    """
    print("=" * 70)
    print("TEST: Format Range")
    print("=" * 70)
    
    engine = FormattingEngine()
    
    text = "def hello():\n    pass    "
    range_obj = Range(
        start=Position(line=0, character=0),
        end=Position(line=1, character=10)
    )
    
    edits = engine.format_range(text, range_obj, "python")
    
    assert edits is not None, "Edits olmalı"
    assert isinstance(edits, list), "List olmalı"
    
    print(f"  Edits: {len(edits)}")
    
    print("\n" + "=" * 70)
    print("PASS: Format range")
    print("=" * 70)


def test_trim_trailing_whitespace():
    """
    Test: Trim trailing whitespace.
    """
    print("=" * 70)
    print("TEST: Trim Trailing Whitespace")
    print("=" * 70)
    
    engine = FormattingEngine()
    
    text = "def hello():    \n    pass    "
    result = engine._trim_trailing_whitespace(text)
    
    assert result == "def hello():\n    pass", "Whitespace temizlenmeli"
    
    print(f"  Result: {repr(result)}")
    
    print("\n" + "=" * 70)
    print("PASS: Trim trailing whitespace")
    print("=" * 70)


def test_insert_final_newline():
    """
    Test: Insert final newline.
    """
    print("=" * 70)
    print("TEST: Insert Final Newline")
    print("=" * 70)
    
    engine = FormattingEngine()
    
    text = "def hello():\n    pass"
    result = engine._insert_final_newline(text)
    
    assert result.endswith('\n'), "Newline eklenmeli"
    
    print(f"  Result: {repr(result)}")
    
    print("\n" + "=" * 70)
    print("PASS: Insert final newline")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    engine = FormattingEngine()
    
    new_config = FormattingConfig(max_line_length=100)
    engine.update_config(new_config)
    
    assert engine.config.max_line_length == 100, "Config güncellenmeli"
    
    print(f"  Max line length: {engine.config.max_line_length}")
    
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
    
    config = FormattingConfig(max_line_length=100)
    engine = FormattingEngine(config)
    
    retrieved_config = engine.get_config()
    
    assert retrieved_config.max_line_length == 100, "Config eşleşmeli"
    
    print(f"  Max line length: {retrieved_config.max_line_length}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


def test_multi_language_support():
    """
    Test: Multi-language support.
    """
    print("=" * 70)
    print("TEST: Multi-Language Support")
    print("=" * 70)
    
    engine = FormattingEngine()
    
    # Python
    python_text = "def hello():\n    pass    "
    python_edits = engine.format_document(python_text, "python")
    
    # JavaScript
    js_text = "function hello() {\n    pass    }"
    js_edits = engine.format_document(js_text, "javascript")
    
    # At least one should have edits
    total_edits = sum(1 for edits in [python_edits, js_edits] if len(edits) > 0)
    assert total_edits > 0, "En az bir dilde edits olmalı"
    
    print(f"  Python: {len(python_edits)}")
    print(f"  JavaScript: {len(js_edits)}")
    
    print("\n" + "=" * 70)
    print("PASS: Multi-language support")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_formatting_mode_enum()
        test2 = test_formatting_trigger_kind_enum()
        test3 = test_position_dataclass()
        test4 = test_range_dataclass()
        test5 = test_text_edit_dataclass()
        test6 = test_formatting_options_dataclass()
        test7 = test_document_formatting_params_dataclass()
        test8 = test_formatting_config_dataclass()
        test9 = test_formatting_engine_initialization()
        test10 = test_format_document()
        test11 = test_format_range()
        test12 = test_trim_trailing_whitespace()
        test13 = test_insert_final_newline()
        test14 = test_update_config()
        test15 = test_get_config()
        test16 = test_multi_language_support()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"FormattingMode Enum: {'PASS' if test1 else 'FAIL'}")
        print(f"FormattingTriggerKind Enum: {'PASS' if test2 else 'FAIL'}")
        print(f"Position Dataclass: {'PASS' if test3 else 'FAIL'}")
        print(f"Range Dataclass: {'PASS' if test4 else 'FAIL'}")
        print(f"TextEdit Dataclass: {'PASS' if test5 else 'FAIL'}")
        print(f"FormattingOptions Dataclass: {'PASS' if test6 else 'FAIL'}")
        print(f"DocumentFormattingParams Dataclass: {'PASS' if test7 else 'FAIL'}")
        print(f"FormattingConfig Dataclass: {'PASS' if test8 else 'FAIL'}")
        print(f"FormattingEngine Initialization: {'PASS' if test9 else 'FAIL'}")
        print(f"Format Document: {'PASS' if test10 else 'FAIL'}")
        print(f"Format Range: {'PASS' if test11 else 'FAIL'}")
        print(f"Trim Trailing Whitespace: {'PASS' if test12 else 'FAIL'}")
        print(f"Insert Final Newline: {'PASS' if test13 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test14 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test15 else 'FAIL'}")
        print(f"Multi-Language Support: {'PASS' if test16 else 'FAIL'}")
        
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
