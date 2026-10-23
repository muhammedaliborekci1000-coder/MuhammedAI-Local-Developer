"""
Quality Test: Current Line Highlighting
Current line highlighting system testleri.
"""

import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from app.editor.current_line_highlighting import (
    HighlightStyle,
    CurrentLineHighlight,
    CurrentLineHighlightConfig,
    CurrentLineHighlightResult,
    CurrentLineHighlightManager
)


def test_highlight_style_enum():
    """
    Test: HighlightStyle enum.
    """
    print("=" * 70)
    print("TEST: HighlightStyle Enum")
    print("=" * 70)
    
    assert HighlightStyle.BACKGROUND.value == "background"
    assert HighlightStyle.BORDER.value == "border"
    assert HighlightStyle.UNDERLINE.value == "underline"
    assert HighlightStyle.GLOW.value == "glow"
    
    print(f"  All enum values verified")
    print(f"  Total styles: {len(HighlightStyle)}")
    
    print("\n" + "=" * 70)
    print("PASS: HighlightStyle enum")
    print("=" * 70)


def test_current_line_highlight_dataclass():
    """
    Test: CurrentLineHighlight dataclass.
    """
    print("=" * 70)
    print("TEST: CurrentLineHighlight Dataclass")
    print("=" * 70)
    
    highlight = CurrentLineHighlight(
        line=10,
        style=HighlightStyle.BACKGROUND,
        color="#FFFF00",
        opacity=0.3
    )
    
    assert highlight.line == 10, "Line eşleşmeli"
    assert highlight.style == HighlightStyle.BACKGROUND, "Style eşleşmeli"
    assert highlight.color == "#FFFF00", "Color eşleşmeli"
    assert highlight.opacity == 0.3, "Opacity eşleşmeli"
    
    print(f"  Line: {highlight.line}")
    print(f"  Style: {highlight.style.value}")
    print(f"  Color: {highlight.color}")
    print(f"  Opacity: {highlight.opacity}")
    
    print("\n" + "=" * 70)
    print("PASS: CurrentLineHighlight dataclass")
    print("=" * 70)


def test_current_line_highlight_config_dataclass():
    """
    Test: CurrentLineHighlightConfig dataclass.
    """
    print("=" * 70)
    print("TEST: CurrentLineHighlightConfig Dataclass")
    print("=" * 70)
    
    config = CurrentLineHighlightConfig(
        enabled=True,
        style=HighlightStyle.BACKGROUND
    )
    
    assert config.enabled == True, "Enabled eşleşmeli"
    assert config.style == HighlightStyle.BACKGROUND, "Style eşleşmeli"
    
    print(f"  Enabled: {config.enabled}")
    print(f"  Style: {config.style.value}")
    
    print("\n" + "=" * 70)
    print("PASS: CurrentLineHighlightConfig dataclass")
    print("=" * 70)


def test_current_line_highlight_result_dataclass():
    """
    Test: CurrentLineHighlightResult dataclass.
    """
    print("=" * 70)
    print("TEST: CurrentLineHighlightResult Dataclass")
    print("=" * 70)
    
    result = CurrentLineHighlightResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: CurrentLineHighlightResult dataclass")
    print("=" * 70)


def test_current_line_highlight_manager_initialization():
    """
    Test: CurrentLineHighlightManager initialization.
    """
    print("=" * 70)
    print("TEST: CurrentLineHighlightManager Initialization")
    print("=" * 70)
    
    config = CurrentLineHighlightConfig()
    manager = CurrentLineHighlightManager(config)
    
    assert manager.config == config, "Config eşleşmeli"
    assert manager.current_line == 0, "Current line 0 olmalı"
    assert manager.highlight is None, "Highlight None olmalı"
    
    print(f"  Current line: {manager.current_line}")
    
    print("\n" + "=" * 70)
    print("PASS: CurrentLineHighlightManager initialization")
    print("=" * 70)


def test_set_current_line():
    """
    Test: Set current line.
    """
    print("=" * 70)
    print("TEST: Set Current Line")
    print("=" * 70)
    
    manager = CurrentLineHighlightManager()
    
    result = manager.set_current_line(10)
    
    assert result.success == True, "Set başarılı olmalı"
    assert manager.current_line == 10, "Current line eşleşmeli"
    
    print(f"  Current line set: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set current line")
    print("=" * 70)


def test_get_current_line():
    """
    Test: Get current line.
    """
    print("=" * 70)
    print("TEST: Get Current Line")
    print("=" * 70)
    
    manager = CurrentLineHighlightManager()
    manager.set_current_line(10)
    
    current_line = manager.get_current_line()
    
    assert current_line == 10, "Current line eşleşmeli"
    
    print(f"  Current line: {current_line}")
    
    print("\n" + "=" * 70)
    print("PASS: Get current line")
    print("=" * 70)


def test_get_highlight():
    """
    Test: Get highlight.
    """
    print("=" * 70)
    print("TEST: Get Highlight")
    print("=" * 70)
    
    manager = CurrentLineHighlightManager()
    manager.set_current_line(10)
    
    highlight = manager.get_highlight()
    
    assert highlight is not None, "Highlight bulunmalı"
    assert highlight.line == 10, "Line eşleşmeli"
    
    print(f"  Highlight: line {highlight.line}")
    
    print("\n" + "=" * 70)
    print("PASS: Get highlight")
    print("=" * 70)


def test_set_highlight_style():
    """
    Test: Set highlight style.
    """
    print("=" * 70)
    print("TEST: Set Highlight Style")
    print("=" * 70)
    
    manager = CurrentLineHighlightManager()
    
    result = manager.set_highlight_style(HighlightStyle.BORDER)
    
    assert result.success == True, "Set başarılı olmalı"
    
    print(f"  Style set: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set highlight style")
    print("=" * 70)


def test_set_highlight_color():
    """
    Test: Set highlight color.
    """
    print("=" * 70)
    print("TEST: Set Highlight Color")
    print("=" * 70)
    
    manager = CurrentLineHighlightManager()
    
    result = manager.set_highlight_color("#FF0000")
    
    assert result.success == True, "Set başarılı olmalı"
    
    print(f"  Color set: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set highlight color")
    print("=" * 70)


def test_set_opacity():
    """
    Test: Set opacity.
    """
    print("=" * 70)
    print("TEST: Set Opacity")
    print("=" * 70)
    
    manager = CurrentLineHighlightManager()
    
    result = manager.set_opacity(0.5)
    
    assert result.success == True, "Set başarılı olmalı"
    
    print(f"  Opacity set: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set opacity")
    print("=" * 70)


def test_set_enabled():
    """
    Test: Set enabled.
    """
    print("=" * 70)
    print("TEST: Set Enabled")
    print("=" * 70)
    
    manager = CurrentLineHighlightManager()
    
    result = manager.set_enabled(False)
    
    assert result.success == True, "Set başarılı olmalı"
    
    print(f"  Enabled state: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set enabled")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    manager = CurrentLineHighlightManager()
    
    new_config = CurrentLineHighlightConfig(opacity=0.5)
    result = manager.update_config(new_config)
    
    assert result.success == True, "Update başarılı olmalı"
    assert manager.config.opacity == 0.5, "Config güncellenmeli"
    
    print(f"  Opacity: {manager.config.opacity}")
    
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
    
    config = CurrentLineHighlightConfig(opacity=0.5)
    manager = CurrentLineHighlightManager(config)
    
    retrieved_config = manager.get_config()
    
    assert retrieved_config.opacity == 0.5, "Config eşleşmeli"
    
    print(f"  Opacity: {retrieved_config.opacity}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_highlight_style_enum()
        test2 = test_current_line_highlight_dataclass()
        test3 = test_current_line_highlight_config_dataclass()
        test4 = test_current_line_highlight_result_dataclass()
        test5 = test_current_line_highlight_manager_initialization()
        test6 = test_set_current_line()
        test7 = test_get_current_line()
        test8 = test_get_highlight()
        test9 = test_set_highlight_style()
        test10 = test_set_highlight_color()
        test11 = test_set_opacity()
        test12 = test_set_enabled()
        test13 = test_update_config()
        test14 = test_get_config()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"HighlightStyle Enum: {'PASS' if test1 else 'FAIL'}")
        print(f"CurrentLineHighlight Dataclass: {'PASS' if test2 else 'FAIL'}")
        print(f"CurrentLineHighlightConfig Dataclass: {'PASS' if test3 else 'FAIL'}")
        print(f"CurrentLineHighlightResult Dataclass: {'PASS' if test4 else 'FAIL'}")
        print(f"CurrentLineHighlightManager Initialization: {'PASS' if test5 else 'FAIL'}")
        print(f"Set Current Line: {'PASS' if test6 else 'FAIL'}")
        print(f"Get Current Line: {'PASS' if test7 else 'FAIL'}")
        print(f"Get Highlight: {'PASS' if test8 else 'FAIL'}")
        print(f"Set Highlight Style: {'PASS' if test9 else 'FAIL'}")
        print(f"Set Highlight Color: {'PASS' if test10 else 'FAIL'}")
        print(f"Set Opacity: {'PASS' if test11 else 'FAIL'}")
        print(f"Set Enabled: {'PASS' if test12 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test13 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test14 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14])
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
