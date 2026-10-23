"""
Quality Test: Indentation Guides
Indentation guides system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.indentation_guides import (
    IndentationGuidesEngine,
    GuideStyle,
    GuideColor,
    IndentationLevel,
    IndentationGuide,
    IndentationConfig,
    IndentationResult
)


def test_calculate_indentation():
    """
    Test: Calculate indentation.
    """
    print("=" * 70)
    print("TEST: Calculate Indentation")
    print("=" * 70)
    
    config = IndentationConfig()
    engine = IndentationGuidesEngine(config)
    
    code = """def my_function():
    x = 10
    if x > 5:
        print("Hello")
"""
    
    result = engine.calculate_indentation(code, current_line=0)
    
    assert result.success, "Hesaplama başarılı olmalı"
    assert len(result.guides) > 0, "Guide'lar hesaplanmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Guides: {len(result.guides)}")
    print(f"  Levels: {len(result.levels)}")
    
    print("\n" + "=" * 70)
    print("PASS: Calculate indentation")
    print("=" * 70)


def test_get_guide_at_position():
    """
    Test: Get guide at position.
    """
    print("=" * 70)
    print("TEST: Get Guide At Position")
    print("=" * 70)
    
    config = IndentationConfig()
    engine = IndentationGuidesEngine(config)
    
    code = "    line1\n        line2"
    engine.calculate_indentation(code)
    
    guide = engine.get_guide_at_position(0, 4)
    
    assert guide is not None, "Guide bulunmalı"
    
    print(f"  Guide found: {guide.line}, {guide.column}")
    
    print("\n" + "=" * 70)
    print("PASS: Get guide at position")
    print("=" * 70)


def test_get_guides_for_line():
    """
    Test: Get guides for line.
    """
    print("=" * 70)
    print("TEST: Get Guides For Line")
    print("=" * 70)
    
    config = IndentationConfig()
    engine = IndentationGuidesEngine(config)
    
    code = "    line1\n        line2"
    engine.calculate_indentation(code)
    
    guides = engine.get_guides_for_line(0)
    
    assert len(guides) > 0, "Guide'lar bulunmalı"
    
    print(f"  Guides: {len(guides)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get guides for line")
    print("=" * 70)


def test_get_level_for_line():
    """
    Test: Get level for line.
    """
    print("=" * 70)
    print("TEST: Get Level For Line")
    print("=" * 70)
    
    config = IndentationConfig()
    engine = IndentationGuidesEngine(config)
    
    code = "    line1\n        line2"
    engine.calculate_indentation(code)
    
    level = engine.get_level_for_line(0)
    
    assert level >= 0, "Level 0 veya daha büyük olmalı"
    
    print(f"  Level: {level}")
    
    print("\n" + "=" * 70)
    print("PASS: Get level for line")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    config = IndentationConfig()
    engine = IndentationGuidesEngine(config)
    
    new_config = IndentationConfig(enabled=False)
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
    
    config = IndentationConfig()
    engine = IndentationGuidesEngine(config)
    
    retrieved_config = engine.get_config()
    
    assert retrieved_config is not None, "Config olmalı"
    assert retrieved_config.enabled == True, "Config eşleşmeli"
    
    print(f"  Enabled: {retrieved_config.enabled}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


def test_toggle_guides():
    """
    Test: Toggle guides.
    """
    print("=" * 70)
    print("TEST: Toggle Guides")
    print("=" * 70)
    
    config = IndentationConfig()
    engine = IndentationGuidesEngine(config)
    
    result = engine.toggle_guides()
    
    assert result.success, "Toggle başarılı olmalı"
    assert engine.config.show_guides == False, "Disabled olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Toggle guides")
    print("=" * 70)


def test_set_guide_style():
    """
    Test: Set guide style.
    """
    print("=" * 70)
    print("TEST: Set Guide Style")
    print("=" * 70)
    
    config = IndentationConfig()
    engine = IndentationGuidesEngine(config)
    
    result = engine.set_guide_style(GuideStyle.DASHED)
    
    assert result.success, "Ayar başarılı olmalı"
    assert engine.config.guide_style == GuideStyle.DASHED, "Style eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Style: {engine.config.guide_style.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Set guide style")
    print("=" * 70)


def test_set_guide_color():
    """
    Test: Set guide color.
    """
    print("=" * 70)
    print("TEST: Set Guide Color")
    print("=" * 70)
    
    config = IndentationConfig()
    engine = IndentationGuidesEngine(config)
    
    result = engine.set_guide_color(GuideColor.ACTIVE)
    
    assert result.success, "Ayar başarılı olmalı"
    assert engine.config.guide_color == GuideColor.ACTIVE, "Color eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Color: {engine.config.guide_color.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Set guide color")
    print("=" * 70)


def test_set_tab_size():
    """
    Test: Set tab size.
    """
    print("=" * 70)
    print("TEST: Set Tab Size")
    print("=" * 70)
    
    config = IndentationConfig()
    engine = IndentationGuidesEngine(config)
    
    result = engine.set_tab_size(8)
    
    assert result.success, "Ayar başarılı olmalı"
    assert engine.config.tab_size == 8, "Tab size eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Tab size: {engine.config.tab_size}")
    
    print("\n" + "=" * 70)
    print("PASS: Set tab size")
    print("=" * 70)


def test_set_use_tabs():
    """
    Test: Set use tabs.
    """
    print("=" * 70)
    print("TEST: Set Use Tabs")
    print("=" * 70)
    
    config = IndentationConfig()
    engine = IndentationGuidesEngine(config)
    
    result = engine.set_use_tabs(True)
    
    assert result.success, "Ayar başarılı olmalı"
    assert engine.config.use_tabs == True, "Use tabs eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Use tabs: {engine.config.use_tabs}")
    
    print("\n" + "=" * 70)
    print("PASS: Set use tabs")
    print("=" * 70)


def test_toggle_rainbow_indentation():
    """
    Test: Toggle rainbow indentation.
    """
    print("=" * 70)
    print("TEST: Toggle Rainbow Indentation")
    print("=" * 70)
    
    config = IndentationConfig()
    engine = IndentationGuidesEngine(config)
    
    result = engine.toggle_rainbow_indentation()
    
    assert result.success, "Toggle başarılı olmalı"
    assert engine.config.rainbow_indentation == True, "Enabled olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Toggle rainbow indentation")
    print("=" * 70)


def test_get_all_guides():
    """
    Test: Get all guides.
    """
    print("=" * 70)
    print("TEST: Get All Guides")
    print("=" * 70)
    
    config = IndentationConfig()
    engine = IndentationGuidesEngine(config)
    
    code = "    line1"
    engine.calculate_indentation(code)
    
    guides = engine.get_all_guides()
    
    assert len(guides) > 0, "Guide'lar olmalı"
    
    print(f"  Guides: {len(guides)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get all guides")
    print("=" * 70)


def test_get_all_levels():
    """
    Test: Get all levels.
    """
    print("=" * 70)
    print("TEST: Get All Levels")
    print("=" * 70)
    
    config = IndentationConfig()
    engine = IndentationGuidesEngine(config)
    
    code = "    line1"
    engine.calculate_indentation(code)
    
    levels = engine.get_all_levels()
    
    assert len(levels) > 0, "Level'lar olmalı"
    
    print(f"  Levels: {len(levels)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get all levels")
    print("=" * 70)


def test_guide_style_enum():
    """
    Test: GuideStyle enum.
    """
    print("=" * 70)
    print("TEST: GuideStyle Enum")
    print("=" * 70)
    
    assert GuideStyle.SOLID.value == "solid"
    assert GuideStyle.DASHED.value == "dashed"
    assert GuideStyle.DOTTED.value == "dotted"
    assert GuideStyle.NONE.value == "none"
    
    print(f"  All enum values verified")
    print(f"  Total styles: {len(GuideStyle)}")
    
    print("\n" + "=" * 70)
    print("PASS: GuideStyle enum")
    print("=" * 70)


def test_guide_color_enum():
    """
    Test: GuideColor enum.
    """
    print("=" * 70)
    print("TEST: GuideColor Enum")
    print("=" * 70)
    
    assert GuideColor.DEFAULT.value == "default"
    assert GuideColor.ACTIVE.value == "active"
    assert GuideColor.ERROR.value == "error"
    assert GuideColor.WARNING.value == "warning"
    
    print(f"  All enum values verified")
    print(f"  Total colors: {len(GuideColor)}")
    
    print("\n" + "=" * 70)
    print("PASS: GuideColor enum")
    print("=" * 70)


def test_indentation_level_dataclass():
    """
    Test: IndentationLevel dataclass.
    """
    print("=" * 70)
    print("TEST: IndentationLevel Dataclass")
    print("=" * 70)
    
    level = IndentationLevel(
        level=1,
        start_column=0,
        end_column=4,
        is_active=True
    )
    
    assert level.level == 1, "Level eşleşmeli"
    assert level.start_column == 0, "Start column eşleşmeli"
    assert level.end_column == 4, "End column eşleşmeli"
    
    print(f"  Level: {level.level}")
    print(f"  Start column: {level.start_column}")
    print(f"  End column: {level.end_column}")
    
    print("\n" + "=" * 70)
    print("PASS: IndentationLevel dataclass")
    print("=" * 70)


def test_indentation_guide_dataclass():
    """
    Test: IndentationGuide dataclass.
    """
    print("=" * 70)
    print("TEST: IndentationGuide Dataclass")
    print("=" * 70)
    
    guide = IndentationGuide(
        line=0,
        column=4,
        level=1,
        style=GuideStyle.SOLID,
        color=GuideColor.DEFAULT
    )
    
    assert guide.line == 0, "Line eşleşmeli"
    assert guide.column == 4, "Column eşleşmeli"
    assert guide.level == 1, "Level eşleşmeli"
    
    print(f"  Line: {guide.line}")
    print(f"  Column: {guide.column}")
    print(f"  Level: {guide.level}")
    
    print("\n" + "=" * 70)
    print("PASS: IndentationGuide dataclass")
    print("=" * 70)


def test_indentation_config_dataclass():
    """
    Test: IndentationConfig dataclass.
    """
    print("=" * 70)
    print("TEST: IndentationConfig Dataclass")
    print("=" * 70)
    
    config = IndentationConfig(
        enabled=True,
        show_guides=True,
        tab_size=4
    )
    
    assert config.enabled == True, "Enabled eşleşmeli"
    assert config.show_guides == True, "Show guides eşleşmeli"
    assert config.tab_size == 4, "Tab size eşleşmeli"
    
    print(f"  Enabled: {config.enabled}")
    print(f"  Show guides: {config.show_guides}")
    print(f"  Tab size: {config.tab_size}")
    
    print("\n" + "=" * 70)
    print("PASS: IndentationConfig dataclass")
    print("=" * 70)


def test_indentation_result_dataclass():
    """
    Test: IndentationResult dataclass.
    """
    print("=" * 70)
    print("TEST: IndentationResult Dataclass")
    print("=" * 70)
    
    result = IndentationResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.guides, list), "Guides list olmalı"
    assert isinstance(result.levels, list), "Levels list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Guides: {len(result.guides)}")
    print(f"  Levels: {len(result.levels)}")
    
    print("\n" + "=" * 70)
    print("PASS: IndentationResult dataclass")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_calculate_indentation()
        test2 = test_get_guide_at_position()
        test3 = test_get_guides_for_line()
        test4 = test_get_level_for_line()
        test5 = test_update_config()
        test6 = test_get_config()
        test7 = test_toggle_guides()
        test8 = test_set_guide_style()
        test9 = test_set_guide_color()
        test10 = test_set_tab_size()
        test11 = test_set_use_tabs()
        test12 = test_toggle_rainbow_indentation()
        test13 = test_get_all_guides()
        test14 = test_get_all_levels()
        test15 = test_guide_style_enum()
        test16 = test_guide_color_enum()
        test17 = test_indentation_level_dataclass()
        test18 = test_indentation_guide_dataclass()
        test19 = test_indentation_config_dataclass()
        test20 = test_indentation_result_dataclass()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Calculate Indentation: {'PASS' if test1 else 'FAIL'}")
        print(f"Get Guide At Position: {'PASS' if test2 else 'FAIL'}")
        print(f"Get Guides For Line: {'PASS' if test3 else 'FAIL'}")
        print(f"Get Level For Line: {'PASS' if test4 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test5 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test6 else 'FAIL'}")
        print(f"Toggle Guides: {'PASS' if test7 else 'FAIL'}")
        print(f"Set Guide Style: {'PASS' if test8 else 'FAIL'}")
        print(f"Set Guide Color: {'PASS' if test9 else 'FAIL'}")
        print(f"Set Tab Size: {'PASS' if test10 else 'FAIL'}")
        print(f"Set Use Tabs: {'PASS' if test11 else 'FAIL'}")
        print(f"Toggle Rainbow Indentation: {'PASS' if test12 else 'FAIL'}")
        print(f"Get All Guides: {'PASS' if test13 else 'FAIL'}")
        print(f"Get All Levels: {'PASS' if test14 else 'FAIL'}")
        print(f"GuideStyle Enum: {'PASS' if test15 else 'FAIL'}")
        print(f"GuideColor Enum: {'PASS' if test16 else 'FAIL'}")
        print(f"IndentationLevel Dataclass: {'PASS' if test17 else 'FAIL'}")
        print(f"IndentationGuide Dataclass: {'PASS' if test18 else 'FAIL'}")
        print(f"IndentationConfig Dataclass: {'PASS' if test19 else 'FAIL'}")
        print(f"IndentationResult Dataclass: {'PASS' if test20 else 'FAIL'}")
        
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
