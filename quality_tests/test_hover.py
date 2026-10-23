"""
Quality Test: Hover
Hover system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.hover import (
    HoverContentKind,
    Position,
    Range,
    MarkedString,
    Hover,
    ParameterInfo,
    SignatureInfo,
    HoverConfig,
    HoverEngine
)


def test_hover_content_kind_enum():
    """
    Test: HoverContentKind enum.
    """
    print("=" * 70)
    print("TEST: HoverContentKind Enum")
    print("=" * 70)
    
    assert HoverContentKind.PLAIN_TEXT.value == "plaintext"
    assert HoverContentKind.MARKDOWN.value == "markdown"
    
    print(f"  All enum values verified")
    print(f"  Total kinds: {len(HoverContentKind)}")
    
    print("\n" + "=" * 70)
    print("PASS: HoverContentKind enum")
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


def test_marked_string_dataclass():
    """
    Test: MarkedString dataclass.
    """
    print("=" * 70)
    print("TEST: MarkedString Dataclass")
    print("=" * 70)
    
    marked_string = MarkedString(language="python", value="test")
    
    assert marked_string.language == "python", "Language eşleşmeli"
    assert marked_string.value == "test", "Value eşleşmeli"
    
    print(f"  Language: {marked_string.language}")
    print(f"  Value: {marked_string.value}")
    
    print("\n" + "=" * 70)
    print("PASS: MarkedString dataclass")
    print("=" * 70)


def test_hover_dataclass():
    """
    Test: Hover dataclass.
    """
    print("=" * 70)
    print("TEST: Hover Dataclass")
    print("=" * 70)
    
    hover = Hover(contents="Test hover")
    
    assert hover.contents == "Test hover", "Contents eşleşmeli"
    assert hover.range is None, "Range None olmalı"
    
    print(f"  Contents: {hover.contents}")
    
    print("\n" + "=" * 70)
    print("PASS: Hover dataclass")
    print("=" * 70)


def test_parameter_info_dataclass():
    """
    Test: ParameterInfo dataclass.
    """
    print("=" * 70)
    print("TEST: ParameterInfo Dataclass")
    print("=" * 70)
    
    param_info = ParameterInfo(label="param1", documentation="Test parameter")
    
    assert param_info.label == "param1", "Label eşleşmeli"
    assert param_info.documentation == "Test parameter", "Documentation eşleşmeli"
    
    print(f"  Label: {param_info.label}")
    print(f"  Documentation: {param_info.documentation}")
    
    print("\n" + "=" * 70)
    print("PASS: ParameterInfo dataclass")
    print("=" * 70)


def test_signature_info_dataclass():
    """
    Test: SignatureInfo dataclass.
    """
    print("=" * 70)
    print("TEST: SignatureInfo Dataclass")
    print("=" * 70)
    
    signature = SignatureInfo(
        label="func(param1, param2)",
        documentation="Test function"
    )
    
    assert signature.label == "func(param1, param2)", "Label eşleşmeli"
    assert signature.documentation == "Test function", "Documentation eşleşmeli"
    
    print(f"  Label: {signature.label}")
    print(f"  Documentation: {signature.documentation}")
    
    print("\n" + "=" * 70)
    print("PASS: SignatureInfo dataclass")
    print("=" * 70)


def test_hover_config_dataclass():
    """
    Test: HoverConfig dataclass.
    """
    print("=" * 70)
    print("TEST: HoverConfig Dataclass")
    print("=" * 70)
    
    config = HoverConfig(
        enable_documentation=True,
        enable_type_info=True,
        content_kind=HoverContentKind.MARKDOWN
    )
    
    assert config.enable_documentation == True, "Enable documentation eşleşmeli"
    assert config.content_kind == HoverContentKind.MARKDOWN, "Content kind eşleşmeli"
    
    print(f"  Enable documentation: {config.enable_documentation}")
    print(f"  Content kind: {config.content_kind.value}")
    
    print("\n" + "=" * 70)
    print("PASS: HoverConfig dataclass")
    print("=" * 70)


def test_hover_engine_initialization():
    """
    Test: HoverEngine initialization.
    """
    print("=" * 70)
    print("TEST: HoverEngine Initialization")
    print("=" * 70)
    
    config = HoverConfig()
    engine = HoverEngine(config)
    
    assert engine.config == config, "Config eşleşmeli"
    assert len(engine.symbol_docs) > 0, "Symbol docs olmalı"
    
    print(f"  Symbol docs: {len(engine.symbol_docs)}")
    print(f"  Cache: {len(engine.cache)}")
    
    print("\n" + "=" * 70)
    print("PASS: HoverEngine initialization")
    print("=" * 70)


def test_get_hover():
    """
    Test: Get hover.
    """
    print("=" * 70)
    print("TEST: Get Hover")
    print("=" * 70)
    
    engine = HoverEngine()
    
    text = "def hello():\n    print('Hello')"
    
    hover = engine.get_hover(text, 1, 8, "python")
    
    assert hover is not None, "Hover olmalı"
    assert isinstance(hover, Hover), "Hover nesnesi olmalı"
    
    print(f"  Hover: {hover.contents}")
    
    print("\n" + "=" * 70)
    print("PASS: Get hover")
    print("=" * 70)


def test_get_hover_no_word():
    """
    Test: Get hover with no word.
    """
    print("=" * 70)
    print("TEST: Get Hover No Word")
    print("=" * 70)
    
    engine = HoverEngine()
    
    text = "    "
    
    hover = engine.get_hover(text, 0, 2, "python")
    
    assert hover is None, "Hover None olmalı"
    
    print(f"  Hover: {hover}")
    
    print("\n" + "=" * 70)
    print("PASS: Get hover no word")
    print("=" * 70)


def test_get_hover_history():
    """
    Test: Get hover history.
    """
    print("=" * 70)
    print("TEST: Get Hover History")
    print("=" * 70)
    
    engine = HoverEngine()
    
    text = "def hello():\n    print('Hello')"
    
    engine.get_hover(text, 1, 8, "python")
    
    history = engine.get_hover_history()
    
    assert len(history) > 0, "History olmalı"
    
    print(f"  History: {len(history)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get hover history")
    print("=" * 70)


def test_clear_history():
    """
    Test: Clear history.
    """
    print("=" * 70)
    print("TEST: Clear History")
    print("=" * 70)
    
    engine = HoverEngine()
    
    text = "def hello():\n    print('Hello')"
    
    engine.get_hover(text, 1, 8, "python")
    engine.clear_history()
    
    history = engine.get_hover_history()
    
    assert len(history) == 0, "History temizlenmeli"
    
    print(f"  History: {len(history)}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear history")
    print("=" * 70)


def test_clear_cache():
    """
    Test: Clear cache.
    """
    print("=" * 70)
    print("TEST: Clear Cache")
    print("=" * 70)
    
    engine = HoverEngine()
    
    text = "def hello():\n    print('Hello')"
    
    engine.get_hover(text, 1, 8, "python")
    engine.clear_cache()
    
    assert len(engine.cache) == 0, "Cache temizlenmeli"
    
    print(f"  Cache: {len(engine.cache)}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear cache")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    engine = HoverEngine()
    
    new_config = HoverConfig(enable_documentation=False)
    engine.update_config(new_config)
    
    assert engine.config.enable_documentation == False, "Config güncellenmeli"
    
    print(f"  Enable documentation: {engine.config.enable_documentation}")
    
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
    
    config = HoverConfig(enable_documentation=False)
    engine = HoverEngine(config)
    
    retrieved_config = engine.get_config()
    
    assert retrieved_config.enable_documentation == False, "Config eşleşmeli"
    
    print(f"  Enable documentation: {retrieved_config.enable_documentation}")
    
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
    
    engine = HoverEngine()
    
    # Python
    python_hover = engine.get_hover("def ", 0, 3, "python")
    
    # JavaScript
    js_hover = engine.get_hover("function ", 0, 8, "javascript")
    
    # Go
    go_hover = engine.get_hover("func ", 0, 4, "go")
    
    # At least one should have hover
    total_hovers = sum(1 for h in [python_hover, js_hover, go_hover] if h is not None)
    assert total_hovers > 0, "En az bir dilde hover olmalı"
    
    print(f"  Python: {'Yes' if python_hover else 'No'}")
    print(f"  JavaScript: {'Yes' if js_hover else 'No'}")
    print(f"  Go: {'Yes' if go_hover else 'No'}")
    
    print("\n" + "=" * 70)
    print("PASS: Multi-language support")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_hover_content_kind_enum()
        test2 = test_position_dataclass()
        test3 = test_range_dataclass()
        test4 = test_marked_string_dataclass()
        test5 = test_hover_dataclass()
        test6 = test_parameter_info_dataclass()
        test7 = test_signature_info_dataclass()
        test8 = test_hover_config_dataclass()
        test9 = test_hover_engine_initialization()
        test10 = test_get_hover()
        test11 = test_get_hover_no_word()
        test12 = test_get_hover_history()
        test13 = test_clear_history()
        test14 = test_clear_cache()
        test15 = test_update_config()
        test16 = test_get_config()
        test17 = test_multi_language_support()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"HoverContentKind Enum: {'PASS' if test1 else 'FAIL'}")
        print(f"Position Dataclass: {'PASS' if test2 else 'FAIL'}")
        print(f"Range Dataclass: {'PASS' if test3 else 'FAIL'}")
        print(f"MarkedString Dataclass: {'PASS' if test4 else 'FAIL'}")
        print(f"Hover Dataclass: {'PASS' if test5 else 'FAIL'}")
        print(f"ParameterInfo Dataclass: {'PASS' if test6 else 'FAIL'}")
        print(f"SignatureInfo Dataclass: {'PASS' if test7 else 'FAIL'}")
        print(f"HoverConfig Dataclass: {'PASS' if test8 else 'FAIL'}")
        print(f"HoverEngine Initialization: {'PASS' if test9 else 'FAIL'}")
        print(f"Get Hover: {'PASS' if test10 else 'FAIL'}")
        print(f"Get Hover No Word: {'PASS' if test11 else 'FAIL'}")
        print(f"Get Hover History: {'PASS' if test12 else 'FAIL'}")
        print(f"Clear History: {'PASS' if test13 else 'FAIL'}")
        print(f"Clear Cache: {'PASS' if test14 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test15 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test16 else 'FAIL'}")
        print(f"Multi-Language Support: {'PASS' if test17 else 'FAIL'}")
        
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
