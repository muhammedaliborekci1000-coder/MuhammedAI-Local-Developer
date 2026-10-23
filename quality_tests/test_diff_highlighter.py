"""
Quality Test: Diff Highlighter
Diff highlighter system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.diff_highlighter import (
    DiffHighlighterEngine,
    HighlightType,
    HighlightStyle,
    HighlightScope,
    ColorScheme,
    HighlightRange,
    HighlightedLine,
    HighlighterConfig,
    HighlighterResult
)


def test_highlight_line():
    """
    Test: Highlight line.
    """
    print("=" * 70)
    print("TEST: Highlight Line")
    print("=" * 70)
    
    engine = DiffHighlighterEngine()
    line = "def hello_world():"
    result = engine.highlight_line(line, 1, "added")
    
    assert result.success, "Highlight başarılı olmalı"
    assert result.total_lines == 1, "1 satır olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Total lines: {result.total_lines}")
    print(f"  Total highlights: {result.total_highlights}")
    
    print("\n" + "=" * 70)
    print("PASS: Highlight line")
    print("=" * 70)


def test_highlight_lines():
    """
    Test: Highlight lines.
    """
    print("=" * 70)
    print("TEST: Highlight Lines")
    print("=" * 70)
    
    engine = DiffHighlighterEngine()
    lines = ["Line 1", "Line 2", "Line 3"]
    line_types = ["added", "removed", "unchanged"]
    
    result = engine.highlight_lines(lines, line_types)
    
    assert result.success, "Highlight başarılı olmalı"
    assert result.total_lines == 3, "3 satır olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Total lines: {result.total_lines}")
    
    print("\n" + "=" * 70)
    print("PASS: Highlight lines")
    print("=" * 70)


def test_highlight_word():
    """
    Test: Highlight word.
    """
    print("=" * 70)
    print("TEST: Highlight Word")
    print("=" * 70)
    
    engine = DiffHighlighterEngine()
    line = "This is a test line with test word"
    result = engine.highlight_word(line, "test", 1)
    
    assert result.success, "Highlight başarılı olmalı"
    assert result.total_highlights > 0, "Highlight olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Total highlights: {result.total_highlights}")
    
    print("\n" + "=" * 70)
    print("PASS: Highlight word")
    print("=" * 70)


def test_highlight_changes():
    """
    Test: Highlight changes.
    """
    print("=" * 70)
    print("TEST: Highlight Changes")
    print("=" * 70)
    
    engine = DiffHighlighterEngine()
    old_line = "This is old line"
    new_line = "This is new line"
    
    result = engine.highlight_changes(old_line, new_line, 1)
    
    assert result.success, "Highlight başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Total highlights: {result.total_highlights}")
    
    print("\n" + "=" * 70)
    print("PASS: Highlight changes")
    print("=" * 70)


def test_set_color_scheme():
    """
    Test: Set color scheme.
    """
    print("=" * 70)
    print("TEST: Set Color Scheme")
    print("=" * 70)
    
    engine = DiffHighlighterEngine()
    scheme = ColorScheme(added_bg="#ff0000")
    
    result = engine.set_color_scheme(scheme)
    
    assert result.success, "Renk şeması ayarlama başarılı olmalı"
    assert engine.config.color_scheme.added_bg == "#ff0000", "Renk eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set color scheme")
    print("=" * 70)


def test_get_highlighted_lines():
    """
    Test: Get highlighted lines.
    """
    print("=" * 70)
    print("TEST: Get Highlighted Lines")
    print("=" * 70)
    
    engine = DiffHighlighterEngine()
    engine.highlight_line("Line 1", 1, "added")
    engine.highlight_line("Line 2", 2, "removed")
    
    lines = engine.get_highlighted_lines()
    
    assert len(lines) == 2, "2 satır olmalı"
    
    print(f"  Highlighted lines: {len(lines)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get highlighted lines")
    print("=" * 70)


def test_get_line_highlights():
    """
    Test: Get line highlights.
    """
    print("=" * 70)
    print("TEST: Get Line Highlights")
    print("=" * 70)
    
    engine = DiffHighlighterEngine()
    engine.highlight_line("Line 1", 1, "added")
    
    line_highlights = engine.get_line_highlights(1)
    
    assert line_highlights is not None, "Highlight bulunmalı"
    assert line_highlights.line_number == 1, "Satır numarası eşleşmeli"
    
    print(f"  Line number: {line_highlights.line_number}")
    print(f"  Highlights: {len(line_highlights.highlights)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get line highlights")
    print("=" * 70)


def test_get_highlighter_history():
    """
    Test: Get highlighter history.
    """
    print("=" * 70)
    print("TEST: Get Highlighter History")
    print("=" * 70)
    
    engine = DiffHighlighterEngine()
    engine.highlight_line("Line 1", 1, "added")
    
    history = engine.get_highlighter_history()
    
    assert len(history) > 0, "Geçmiş olmalı"
    
    print(f"  History: {len(history)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get highlighter history")
    print("=" * 70)


def test_clear_history():
    """
    Test: Clear history.
    """
    print("=" * 70)
    print("TEST: Clear History")
    print("=" * 70)
    
    engine = DiffHighlighterEngine()
    engine.highlight_line("Line 1", 1, "added")
    
    result = engine.clear_history()
    
    assert result.success, "Temizleme başarılı olmalı"
    assert len(engine.get_highlighter_history()) == 0, "Geçmiş temizlenmeli"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear history")
    print("=" * 70)


def test_get_statistics():
    """
    Test: Get statistics.
    """
    print("=" * 70)
    print("TEST: Get Statistics")
    print("=" * 70)
    
    engine = DiffHighlighterEngine()
    engine.highlight_line("Line 1", 1, "added")
    engine.highlight_line("Line 2", 2, "removed")
    
    stats = engine.get_statistics()
    
    assert stats is not None, "İstatistikler olmalı"
    assert stats["total_lines"] == 2, "Toplam satır 2 olmalı"
    
    print(f"  Total lines: {stats['total_lines']}")
    print(f"  Total highlights: {stats['total_highlights']}")
    
    print("\n" + "=" * 70)
    print("PASS: Get statistics")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    engine = DiffHighlighterEngine()
    
    new_config = HighlighterConfig(enable_syntax_highlighting=False)
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
    
    engine = DiffHighlighterEngine()
    
    config = engine.get_config()
    
    assert config is not None, "Config olmalı"
    assert config.enable_syntax_highlighting == True, "Config eşleşmeli"
    
    print(f"  Enable syntax highlighting: {config.enable_syntax_highlighting}")
    print(f"  Enable diff coloring: {config.enable_diff_coloring}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


def test_highlight_type_enum():
    """
    Test: HighlightType enum.
    """
    print("=" * 70)
    print("TEST: HighlightType Enum")
    print("=" * 70)
    
    assert HighlightType.ADDED.value == "added"
    assert HighlightType.REMOVED.value == "removed"
    assert HighlightType.MODIFIED.value == "modified"
    assert HighlightType.UNCHANGED.value == "unchanged"
    assert HighlightType.CONTEXT.value == "context"
    assert HighlightType.HEADER.value == "header"
    assert HighlightType.KEYWORD.value == "keyword"
    assert HighlightType.STRING.value == "string"
    assert HighlightType.COMMENT.value == "comment"
    assert HighlightType.FUNCTION.value == "function"
    assert HighlightType.VARIABLE.value == "variable"
    assert HighlightType.NUMBER.value == "number"
    assert HighlightType.OPERATOR.value == "operator"
    
    print(f"  All enum values verified")
    print(f"  Total types: {len(HighlightType)}")
    
    print("\n" + "=" * 70)
    print("PASS: HighlightType enum")
    print("=" * 70)


def test_highlight_style_enum():
    """
    Test: HighlightStyle enum.
    """
    print("=" * 70)
    print("TEST: HighlightStyle Enum")
    print("=" * 70)
    
    assert HighlightStyle.BACKGROUND.value == "background"
    assert HighlightStyle.FOREGROUND.value == "foreground"
    assert HighlightStyle.BORDER.value == "border"
    assert HighlightStyle.UNDERLINE.value == "underline"
    assert HighlightStyle.BOLD.value == "bold"
    assert HighlightStyle.ITALIC.value == "italic"
    
    print(f"  All enum values verified")
    print(f"  Total styles: {len(HighlightStyle)}")
    
    print("\n" + "=" * 70)
    print("PASS: HighlightStyle enum")
    print("=" * 70)


def test_highlight_scope_enum():
    """
    Test: HighlightScope enum.
    """
    print("=" * 70)
    print("TEST: HighlightScope Enum")
    print("=" * 70)
    
    assert HighlightScope.LINE.value == "line"
    assert HighlightScope.WORD.value == "word"
    assert HighlightScope.CHARACTER.value == "character"
    assert HighlightScope.BLOCK.value == "block"
    
    print(f"  All enum values verified")
    print(f"  Total scopes: {len(HighlightScope)}")
    
    print("\n" + "=" * 70)
    print("PASS: HighlightScope enum")
    print("=" * 70)


def test_color_scheme_dataclass():
    """
    Test: ColorScheme dataclass.
    """
    print("=" * 70)
    print("TEST: ColorScheme Dataclass")
    print("=" * 70)
    
    scheme = ColorScheme(
        added_bg="#ff0000",
        added_fg="#00ff00"
    )
    
    assert scheme.added_bg == "#ff0000", "Added bg eşleşmeli"
    assert scheme.added_fg == "#00ff00", "Added fg eşleşmeli"
    
    print(f"  Added bg: {scheme.added_bg}")
    print(f"  Added fg: {scheme.added_fg}")
    
    print("\n" + "=" * 70)
    print("PASS: ColorScheme dataclass")
    print("=" * 70)


def test_highlight_range_dataclass():
    """
    Test: HighlightRange dataclass.
    """
    print("=" * 70)
    print("TEST: HighlightRange Dataclass")
    print("=" * 70)
    
    range_obj = HighlightRange(
        start=0,
        end=10,
        highlight_type=HighlightType.ADDED,
        style=HighlightStyle.BACKGROUND
    )
    
    assert range_obj.start == 0, "Start eşleşmeli"
    assert range_obj.end == 10, "End eşleşmeli"
    
    print(f"  Start: {range_obj.start}")
    print(f"  End: {range_obj.end}")
    
    print("\n" + "=" * 70)
    print("PASS: HighlightRange dataclass")
    print("=" * 70)


def test_highlighted_line_dataclass():
    """
    Test: HighlightedLine dataclass.
    """
    print("=" * 70)
    print("TEST: HighlightedLine Dataclass")
    print("=" * 70)
    
    line = HighlightedLine(
        line_number=1,
        content="Line content",
        line_type="added"
    )
    
    assert line.line_number == 1, "Line number eşleşmeli"
    assert line.content == "Line content", "Content eşleşmeli"
    
    print(f"  Line number: {line.line_number}")
    print(f"  Content: {line.content}")
    
    print("\n" + "=" * 70)
    print("PASS: HighlightedLine dataclass")
    print("=" * 70)


def test_highlighter_config_dataclass():
    """
    Test: HighlighterConfig dataclass.
    """
    print("=" * 70)
    print("TEST: HighlighterConfig Dataclass")
    print("=" * 70)
    
    config = HighlighterConfig(
        enable_syntax_highlighting=False,
        enable_diff_coloring=False
    )
    
    assert config.enable_syntax_highlighting == False, "Syntax highlighting eşleşmeli"
    assert config.enable_diff_coloring == False, "Diff coloring eşleşmeli"
    
    print(f"  Enable syntax highlighting: {config.enable_syntax_highlighting}")
    print(f"  Enable diff coloring: {config.enable_diff_coloring}")
    
    print("\n" + "=" * 70)
    print("PASS: HighlighterConfig dataclass")
    print("=" * 70)


def test_highlighter_result_dataclass():
    """
    Test: HighlighterResult dataclass.
    """
    print("=" * 70)
    print("TEST: HighlighterResult Dataclass")
    print("=" * 70)
    
    result = HighlighterResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: HighlighterResult dataclass")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_highlight_line()
        test2 = test_highlight_lines()
        test3 = test_highlight_word()
        test4 = test_highlight_changes()
        test5 = test_set_color_scheme()
        test6 = test_get_highlighted_lines()
        test7 = test_get_line_highlights()
        test8 = test_get_highlighter_history()
        test9 = test_clear_history()
        test10 = test_get_statistics()
        test11 = test_update_config()
        test12 = test_get_config()
        test13 = test_highlight_type_enum()
        test14 = test_highlight_style_enum()
        test15 = test_highlight_scope_enum()
        test16 = test_color_scheme_dataclass()
        test17 = test_highlight_range_dataclass()
        test18 = test_highlighted_line_dataclass()
        test19 = test_highlighter_config_dataclass()
        test20 = test_highlighter_result_dataclass()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Highlight Line: {'PASS' if test1 else 'FAIL'}")
        print(f"Highlight Lines: {'PASS' if test2 else 'FAIL'}")
        print(f"Highlight Word: {'PASS' if test3 else 'FAIL'}")
        print(f"Highlight Changes: {'PASS' if test4 else 'FAIL'}")
        print(f"Set Color Scheme: {'PASS' if test5 else 'FAIL'}")
        print(f"Get Highlighted Lines: {'PASS' if test6 else 'FAIL'}")
        print(f"Get Line Highlights: {'PASS' if test7 else 'FAIL'}")
        print(f"Get Highlighter History: {'PASS' if test8 else 'FAIL'}")
        print(f"Clear History: {'PASS' if test9 else 'FAIL'}")
        print(f"Get Statistics: {'PASS' if test10 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test11 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test12 else 'FAIL'}")
        print(f"HighlightType Enum: {'PASS' if test13 else 'FAIL'}")
        print(f"HighlightStyle Enum: {'PASS' if test14 else 'FAIL'}")
        print(f"HighlightScope Enum: {'PASS' if test15 else 'FAIL'}")
        print(f"ColorScheme Dataclass: {'PASS' if test16 else 'FAIL'}")
        print(f"HighlightRange Dataclass: {'PASS' if test17 else 'FAIL'}")
        print(f"HighlightedLine Dataclass: {'PASS' if test18 else 'FAIL'}")
        print(f"HighlighterConfig Dataclass: {'PASS' if test19 else 'FAIL'}")
        print(f"HighlighterResult Dataclass: {'PASS' if test20 else 'FAIL'}")
        
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
