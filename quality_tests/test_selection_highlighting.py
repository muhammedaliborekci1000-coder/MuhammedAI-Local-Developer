"""
Quality Test: Selection Highlighting
Selection highlighting system testleri.
"""

import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from app.editor.selection_highlighting import (
    HighlightStyle,
    HighlightColor,
    SelectionRange,
    Highlight,
    SelectionHighlightConfig,
    SelectionHighlightResult,
    SelectionHighlightManager
)


def test_highlight_style_enum():
    """
    Test: HighlightStyle enum.
    """
    print("=" * 70)
    print("TEST: HighlightStyle Enum")
    print("=" * 70)
    
    assert HighlightStyle.BACKGROUND.value == "background"
    assert HighlightStyle.OUTLINE.value == "outline"
    assert HighlightStyle.UNDERLINE.value == "underline"
    assert HighlightStyle.GLOW.value == "glow"
    
    print(f"  All enum values verified")
    print(f"  Total styles: {len(HighlightStyle)}")
    
    print("\n" + "=" * 70)
    print("PASS: HighlightStyle enum")
    print("=" * 70)


def test_highlight_color_enum():
    """
    Test: HighlightColor enum.
    """
    print("=" * 70)
    print("TEST: HighlightColor Enum")
    print("=" * 70)
    
    assert HighlightColor.DEFAULT.value == "default"
    assert HighlightColor.BLUE.value == "blue"
    assert HighlightColor.GREEN.value == "green"
    assert HighlightColor.YELLOW.value == "yellow"
    assert HighlightColor.ORANGE.value == "orange"
    assert HighlightColor.RED.value == "red"
    assert HighlightColor.PURPLE.value == "purple"
    assert HighlightColor.CYAN.value == "cyan"
    assert HighlightColor.CUSTOM.value == "custom"
    
    print(f"  All enum values verified")
    print(f"  Total colors: {len(HighlightColor)}")
    
    print("\n" + "=" * 70)
    print("PASS: HighlightColor enum")
    print("=" * 70)


def test_selection_range_dataclass():
    """
    Test: SelectionRange dataclass.
    """
    print("=" * 70)
    print("TEST: SelectionRange Dataclass")
    print("=" * 70)
    
    range = SelectionRange(
        start_line=0,
        start_column=0,
        end_line=0,
        end_column=10
    )
    
    assert range.start_line == 0, "Start line eşleşmeli"
    assert range.start_column == 0, "Start column eşleşmeli"
    assert range.end_line == 0, "End line eşleşmeli"
    assert range.end_column == 10, "End column eşleşmeli"
    
    print(f"  Start: ({range.start_line}, {range.start_column})")
    print(f"  End: ({range.end_line}, {range.end_column})")
    
    print("\n" + "=" * 70)
    print("PASS: SelectionRange dataclass")
    print("=" * 70)


def test_highlight_dataclass():
    """
    Test: Highlight dataclass.
    """
    print("=" * 70)
    print("TEST: Highlight Dataclass")
    print("=" * 70)
    
    range = SelectionRange(0, 0, 0, 10)
    highlight = Highlight(
        id="highlight_1",
        range=range,
        style=HighlightStyle.BACKGROUND,
        color=HighlightColor.BLUE
    )
    
    assert highlight.id == "highlight_1", "ID eşleşmeli"
    assert highlight.style == HighlightStyle.BACKGROUND, "Style eşleşmeli"
    assert highlight.color == HighlightColor.BLUE, "Color eşleşmeli"
    
    print(f"  ID: {highlight.id}")
    print(f"  Style: {highlight.style.value}")
    print(f"  Color: {highlight.color.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Highlight dataclass")
    print("=" * 70)


def test_selection_highlight_config_dataclass():
    """
    Test: SelectionHighlightConfig dataclass.
    """
    print("=" * 70)
    print("TEST: SelectionHighlightConfig Dataclass")
    print("=" * 70)
    
    config = SelectionHighlightConfig(
        highlight_current_selection=True,
        highlight_matching_words=True
    )
    
    assert config.highlight_current_selection == True, "Highlight current selection eşleşmeli"
    assert config.highlight_matching_words == True, "Highlight matching words eşleşmeli"
    
    print(f"  Highlight current selection: {config.highlight_current_selection}")
    print(f"  Highlight matching words: {config.highlight_matching_words}")
    
    print("\n" + "=" * 70)
    print("PASS: SelectionHighlightConfig dataclass")
    print("=" * 70)


def test_selection_highlight_result_dataclass():
    """
    Test: SelectionHighlightResult dataclass.
    """
    print("=" * 70)
    print("TEST: SelectionHighlightResult Dataclass")
    print("=" * 70)
    
    result = SelectionHighlightResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.highlights, list), "Highlights list olmalı"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Highlights: {len(result.highlights)}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: SelectionHighlightResult dataclass")
    print("=" * 70)


def test_selection_highlight_manager_initialization():
    """
    Test: SelectionHighlightManager initialization.
    """
    print("=" * 70)
    print("TEST: SelectionHighlightManager Initialization")
    print("=" * 70)
    
    config = SelectionHighlightConfig()
    manager = SelectionHighlightManager(config)
    
    assert manager.config == config, "Config eşleşmeli"
    assert len(manager.highlights) == 0, "Highlights boş olmalı"
    
    print(f"  Highlights: {len(manager.highlights)}")
    
    print("\n" + "=" * 70)
    print("PASS: SelectionHighlightManager initialization")
    print("=" * 70)


def test_add_highlight():
    """
    Test: Add highlight.
    """
    print("=" * 70)
    print("TEST: Add Highlight")
    print("=" * 70)
    
    manager = SelectionHighlightManager()
    
    range = SelectionRange(0, 0, 0, 10)
    highlight = Highlight(
        id="",
        range=range,
        style=HighlightStyle.BACKGROUND
    )
    
    result = manager.add_highlight(highlight)
    
    assert result.success == True, "Ekleme başarılı olmalı"
    assert len(manager.highlights) > 0, "Highlight eklenmeli"
    
    print(f"  Highlight added: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add highlight")
    print("=" * 70)


def test_remove_highlight():
    """
    Test: Remove highlight.
    """
    print("=" * 70)
    print("TEST: Remove Highlight")
    print("=" * 70)
    
    manager = SelectionHighlightManager()
    
    range = SelectionRange(0, 0, 0, 10)
    highlight = Highlight(
        id="",
        range=range
    )
    
    result = manager.add_highlight(highlight)
    highlight_id = result.highlights[0].id
    
    result = manager.remove_highlight(highlight_id)
    
    assert result.success == True, "Kaldırma başarılı olmalı"
    assert highlight_id not in manager.highlights, "Highlight silinmeli"
    
    print(f"  Highlight removed: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Remove highlight")
    print("=" * 70)


def test_get_highlight():
    """
    Test: Get highlight.
    """
    print("=" * 70)
    print("TEST: Get Highlight")
    print("=" * 70)
    
    manager = SelectionHighlightManager()
    
    range = SelectionRange(0, 0, 0, 10)
    highlight = Highlight(
        id="",
        range=range
    )
    
    result = manager.add_highlight(highlight)
    highlight_id = result.highlights[0].id
    
    retrieved_highlight = manager.get_highlight(highlight_id)
    
    assert retrieved_highlight is not None, "Highlight bulunmalı"
    assert retrieved_highlight.id == highlight_id, "ID eşleşmeli"
    
    print(f"  Highlight: {retrieved_highlight.id}")
    
    print("\n" + "=" * 70)
    print("PASS: Get highlight")
    print("=" * 70)


def test_get_all_highlights():
    """
    Test: Get all highlights.
    """
    print("=" * 70)
    print("TEST: Get All Highlights")
    print("=" * 70)
    
    manager = SelectionHighlightManager()
    
    range = SelectionRange(0, 0, 0, 10)
    highlight = Highlight(
        id="",
        range=range
    )
    
    manager.add_highlight(highlight)
    highlights = manager.get_all_highlights()
    
    assert len(highlights) > 0, "Highlights olmalı"
    
    print(f"  Total highlights: {len(highlights)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get all highlights")
    print("=" * 70)


def test_get_highlights_by_style():
    """
    Test: Get highlights by style.
    """
    print("=" * 70)
    print("TEST: Get Highlights by Style")
    print("=" * 70)
    
    manager = SelectionHighlightManager()
    
    range = SelectionRange(0, 0, 0, 10)
    highlight = Highlight(
        id="",
        range=range,
        style=HighlightStyle.BACKGROUND
    )
    
    manager.add_highlight(highlight)
    highlights = manager.get_highlights_by_style(HighlightStyle.BACKGROUND)
    
    assert len(highlights) > 0, "Background highlights olmalı"
    
    print(f"  Background highlights: {len(highlights)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get highlights by style")
    print("=" * 70)


def test_get_highlights_by_color():
    """
    Test: Get highlights by color.
    """
    print("=" * 70)
    print("TEST: Get Highlights by Color")
    print("=" * 70)
    
    manager = SelectionHighlightManager()
    
    range = SelectionRange(0, 0, 0, 10)
    highlight = Highlight(
        id="",
        range=range,
        color=HighlightColor.BLUE
    )
    
    manager.add_highlight(highlight)
    highlights = manager.get_highlights_by_color(HighlightColor.BLUE)
    
    assert len(highlights) > 0, "Blue highlights olmalı"
    
    print(f"  Blue highlights: {len(highlights)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get highlights by color")
    print("=" * 70)


def test_highlight_selection():
    """
    Test: Highlight selection.
    """
    print("=" * 70)
    print("TEST: Highlight Selection")
    print("=" * 70)
    
    manager = SelectionHighlightManager()
    
    range = SelectionRange(0, 0, 0, 10)
    result = manager.highlight_selection(range)
    
    assert result.success == True, "Highlight başarılı olmalı"
    
    print(f"  Selection highlighted: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Highlight selection")
    print("=" * 70)


def test_highlight_matching_words():
    """
    Test: Highlight matching words.
    """
    print("=" * 70)
    print("TEST: Highlight Matching Words")
    print("=" * 70)
    
    manager = SelectionHighlightManager()
    
    text = "hello world hello"
    selection = SelectionRange(0, 0, 0, 5)
    
    result = manager.highlight_matching_words(text, selection)
    
    assert result.success == True, "Highlight başarılı olmalı"
    
    print(f"  Matching words highlighted: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Highlight matching words")
    print("=" * 70)


def test_highlight_matching_brackets():
    """
    Test: Highlight matching brackets.
    """
    print("=" * 70)
    print("TEST: Highlight Matching Brackets")
    print("=" * 70)
    
    manager = SelectionHighlightManager()
    
    text = "(hello)"
    position = (0, 0)
    
    result = manager.highlight_matching_brackets(text, position)
    
    assert result.success == True, "Highlight başarılı olmalı"
    
    print(f"  Brackets highlighted: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Highlight matching brackets")
    print("=" * 70)


def test_clear_highlights():
    """
    Test: Clear highlights.
    """
    print("=" * 70)
    print("TEST: Clear Highlights")
    print("=" * 70)
    
    manager = SelectionHighlightManager()
    
    range = SelectionRange(0, 0, 0, 10)
    highlight = Highlight(
        id="",
        range=range
    )
    
    manager.add_highlight(highlight)
    result = manager.clear_highlights()
    
    assert result.success == True, "Clear başarılı olmalı"
    assert len(manager.highlights) == 0, "Highlights temizlenmeli"
    
    print(f"  Cleared: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear highlights")
    print("=" * 70)


def test_clear_non_persistent_highlights():
    """
    Test: Clear non-persistent highlights.
    """
    print("=" * 70)
    print("TEST: Clear Non-Persistent Highlights")
    print("=" * 70)
    
    manager = SelectionHighlightManager()
    
    range = SelectionRange(0, 0, 0, 10)
    highlight = Highlight(
        id="",
        range=range,
        is_persistent=False
    )
    
    manager.add_highlight(highlight)
    result = manager.clear_non_persistent_highlights()
    
    assert result.success == True, "Clear başarılı olmalı"
    
    print(f"  Non-persistent cleared: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear non-persistent highlights")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    manager = SelectionHighlightManager()
    
    new_config = SelectionHighlightConfig(max_highlights=200)
    result = manager.update_config(new_config)
    
    assert result.success == True, "Update başarılı olmalı"
    assert manager.config.max_highlights == 200, "Config güncellenmeli"
    
    print(f"  Max highlights: {manager.config.max_highlights}")
    
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
    
    config = SelectionHighlightConfig(max_highlights=200)
    manager = SelectionHighlightManager(config)
    
    retrieved_config = manager.get_config()
    
    assert retrieved_config.max_highlights == 200, "Config eşleşmeli"
    
    print(f"  Max highlights: {retrieved_config.max_highlights}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_highlight_style_enum()
        test2 = test_highlight_color_enum()
        test3 = test_selection_range_dataclass()
        test4 = test_highlight_dataclass()
        test5 = test_selection_highlight_config_dataclass()
        test6 = test_selection_highlight_result_dataclass()
        test7 = test_selection_highlight_manager_initialization()
        test8 = test_add_highlight()
        test9 = test_remove_highlight()
        test10 = test_get_highlight()
        test11 = test_get_all_highlights()
        test12 = test_get_highlights_by_style()
        test13 = test_get_highlights_by_color()
        test14 = test_highlight_selection()
        test15 = test_highlight_matching_words()
        test16 = test_highlight_matching_brackets()
        test17 = test_clear_highlights()
        test18 = test_clear_non_persistent_highlights()
        test19 = test_update_config()
        test20 = test_get_config()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"HighlightStyle Enum: {'PASS' if test1 else 'FAIL'}")
        print(f"HighlightColor Enum: {'PASS' if test2 else 'FAIL'}")
        print(f"SelectionRange Dataclass: {'PASS' if test3 else 'FAIL'}")
        print(f"Highlight Dataclass: {'PASS' if test4 else 'FAIL'}")
        print(f"SelectionHighlightConfig Dataclass: {'PASS' if test5 else 'FAIL'}")
        print(f"SelectionHighlightResult Dataclass: {'PASS' if test6 else 'FAIL'}")
        print(f"SelectionHighlightManager Initialization: {'PASS' if test7 else 'FAIL'}")
        print(f"Add Highlight: {'PASS' if test8 else 'FAIL'}")
        print(f"Remove Highlight: {'PASS' if test9 else 'FAIL'}")
        print(f"Get Highlight: {'PASS' if test10 else 'FAIL'}")
        print(f"Get All Highlights: {'PASS' if test11 else 'FAIL'}")
        print(f"Get Highlights by Style: {'PASS' if test12 else 'FAIL'}")
        print(f"Get Highlights by Color: {'PASS' if test13 else 'FAIL'}")
        print(f"Highlight Selection: {'PASS' if test14 else 'FAIL'}")
        print(f"Highlight Matching Words: {'PASS' if test15 else 'FAIL'}")
        print(f"Highlight Matching Brackets: {'PASS' if test16 else 'FAIL'}")
        print(f"Clear Highlights: {'PASS' if test17 else 'FAIL'}")
        print(f"Clear Non-Persistent Highlights: {'PASS' if test18 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test19 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test20 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14, test15, test16, test17, test18, test19, test20])
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
