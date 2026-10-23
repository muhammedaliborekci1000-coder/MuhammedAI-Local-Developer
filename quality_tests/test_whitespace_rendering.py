"""
Quality Test: Whitespace Rendering
Whitespace rendering system testleri.
"""

import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from app.editor.whitespace_rendering import (
    WhitespaceType,
    WhitespaceRenderMode,
    WhitespaceGlyph,
    WhitespaceConfig,
    WhitespaceRenderResult,
    WhitespaceRenderer
)


def test_whitespace_type_enum():
    """
    Test: WhitespaceType enum.
    """
    print("=" * 70)
    print("TEST: WhitespaceType Enum")
    print("=" * 70)
    
    assert WhitespaceType.SPACE.value == "space"
    assert WhitespaceType.TAB.value == "tab"
    assert WhitespaceType.NEWLINE.value == "newline"
    assert WhitespaceType.CARRIAGE_RETURN.value == "carriage_return"
    assert WhitespaceType.FORM_FEED.value == "form_feed"
    assert WhitespaceType.VERTICAL_TAB.value == "vertical_tab"
    
    print(f"  All enum values verified")
    print(f"  Total types: {len(WhitespaceType)}")
    
    print("\n" + "=" * 70)
    print("PASS: WhitespaceType enum")
    print("=" * 70)


def test_whitespace_render_mode_enum():
    """
    Test: WhitespaceRenderMode enum.
    """
    print("=" * 70)
    print("TEST: WhitespaceRenderMode Enum")
    print("=" * 70)
    
    assert WhitespaceRenderMode.NONE.value == "none"
    assert WhitespaceRenderMode.BOUNDARIES.value == "boundaries"
    assert WhitespaceRenderMode.ALL.value == "all"
    assert WhitespaceRenderMode.CUSTOM.value == "custom"
    
    print(f"  All enum values verified")
    print(f"  Total modes: {len(WhitespaceRenderMode)}")
    
    print("\n" + "=" * 70)
    print("PASS: WhitespaceRenderMode enum")
    print("=" * 70)


def test_whitespace_glyph_dataclass():
    """
    Test: WhitespaceGlyph dataclass.
    """
    print("=" * 70)
    print("TEST: WhitespaceGlyph Dataclass")
    print("=" * 70)
    
    glyph = WhitespaceGlyph(
        type=WhitespaceType.SPACE,
        glyph="·",
        color="#808080",
        size=12
    )
    
    assert glyph.type == WhitespaceType.SPACE, "Type eşleşmeli"
    assert glyph.glyph == "·", "Glyph eşleşmeli"
    assert glyph.color == "#808080", "Color eşleşmeli"
    
    print(f"  Type: {glyph.type.value}")
    print(f"  Glyph: {glyph.glyph}")
    print(f"  Color: {glyph.color}")
    
    print("\n" + "=" * 70)
    print("PASS: WhitespaceGlyph dataclass")
    print("=" * 70)


def test_whitespace_config_dataclass():
    """
    Test: WhitespaceConfig dataclass.
    """
    print("=" * 70)
    print("TEST: WhitespaceConfig Dataclass")
    print("=" * 70)
    
    config = WhitespaceConfig(
        render_mode=WhitespaceRenderMode.BOUNDARIES,
        show_spaces=True
    )
    
    assert config.render_mode == WhitespaceRenderMode.BOUNDARIES, "Render mode eşleşmeli"
    assert config.show_spaces == True, "Show spaces eşleşmeli"
    
    print(f"  Render mode: {config.render_mode.value}")
    print(f"  Show spaces: {config.show_spaces}")
    
    print("\n" + "=" * 70)
    print("PASS: WhitespaceConfig dataclass")
    print("=" * 70)


def test_whitespace_render_result_dataclass():
    """
    Test: WhitespaceRenderResult dataclass.
    """
    print("=" * 70)
    print("TEST: WhitespaceRenderResult Dataclass")
    print("=" * 70)
    
    result = WhitespaceRenderResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: WhitespaceRenderResult dataclass")
    print("=" * 70)


def test_whitespace_renderer_initialization():
    """
    Test: WhitespaceRenderer initialization.
    """
    print("=" * 70)
    print("TEST: WhitespaceRenderer Initialization")
    print("=" * 70)
    
    config = WhitespaceConfig()
    renderer = WhitespaceRenderer(config)
    
    assert renderer.config == config, "Config eşleşmeli"
    assert len(renderer.glyphs) > 0, "Glyphs olmalı"
    
    print(f"  Glyphs: {len(renderer.glyphs)}")
    
    print("\n" + "=" * 70)
    print("PASS: WhitespaceRenderer initialization")
    print("=" * 70)


def test_render():
    """
    Test: Render whitespace.
    """
    print("=" * 70)
    print("TEST: Render Whitespace")
    print("=" * 70)
    
    renderer = WhitespaceRenderer()
    
    text = "hello world"
    result = renderer.render(text)
    
    assert result.success == True, "Render başarılı olmalı"
    assert "·" in result.rendered_text, "Space glyph olmalı"
    
    print(f"  Rendered: {result.message}")
    print(f"  Text: {result.rendered_text}")
    
    print("\n" + "=" * 70)
    print("PASS: Render whitespace")
    print("=" * 70)


def test_render_trailing():
    """
    Test: Render trailing whitespace.
    """
    print("=" * 70)
    print("TEST: Render Trailing Whitespace")
    print("=" * 70)
    
    renderer = WhitespaceRenderer()
    
    text = "hello   "
    result = renderer.render_trailing(text)
    
    assert result.success == True, "Render başarılı olmalı"
    
    print(f"  Rendered: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Render trailing whitespace")
    print("=" * 70)


def test_render_leading():
    """
    Test: Render leading whitespace.
    """
    print("=" * 70)
    print("TEST: Render Leading Whitespace")
    print("=" * 70)
    
    renderer = WhitespaceRenderer()
    
    text = "   hello"
    result = renderer.render_leading(text)
    
    assert result.success == True, "Render başarılı olmalı"
    
    print(f"  Rendered: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Render leading whitespace")
    print("=" * 70)


def test_set_glyph():
    """
    Test: Set glyph.
    """
    print("=" * 70)
    print("TEST: Set Glyph")
    print("=" * 70)
    
    renderer = WhitespaceRenderer()
    
    result = renderer.set_glyph(WhitespaceType.SPACE, "•")
    
    assert result.success == True, "Set başarılı olmalı"
    
    print(f"  Glyph set: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set glyph")
    print("=" * 70)


def test_set_glyph_color():
    """
    Test: Set glyph color.
    """
    print("=" * 70)
    print("TEST: Set Glyph Color")
    print("=" * 70)
    
    renderer = WhitespaceRenderer()
    
    result = renderer.set_glyph_color(WhitespaceType.SPACE, "#FF0000")
    
    assert result.success == True, "Set başarılı olmalı"
    
    print(f"  Color set: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set glyph color")
    print("=" * 70)


def test_get_glyph():
    """
    Test: Get glyph.
    """
    print("=" * 70)
    print("TEST: Get Glyph")
    print("=" * 70)
    
    renderer = WhitespaceRenderer()
    
    glyph = renderer.get_glyph(WhitespaceType.SPACE)
    
    assert glyph is not None, "Glyph bulunmalı"
    assert glyph.type == WhitespaceType.SPACE, "Type eşleşmeli"
    
    print(f"  Glyph: {glyph.glyph}")
    
    print("\n" + "=" * 70)
    print("PASS: Get glyph")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    renderer = WhitespaceRenderer()
    
    new_config = WhitespaceConfig(space_glyph="•")
    result = renderer.update_config(new_config)
    
    assert result.success == True, "Update başarılı olmalı"
    
    print(f"  Config updated: {result.message}")
    
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
    
    config = WhitespaceConfig(space_glyph="•")
    renderer = WhitespaceRenderer(config)
    
    retrieved_config = renderer.get_config()
    
    assert retrieved_config.space_glyph == "•", "Config eşleşmeli"
    
    print(f"  Space glyph: {retrieved_config.space_glyph}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_whitespace_type_enum()
        test2 = test_whitespace_render_mode_enum()
        test3 = test_whitespace_glyph_dataclass()
        test4 = test_whitespace_config_dataclass()
        test5 = test_whitespace_render_result_dataclass()
        test6 = test_whitespace_renderer_initialization()
        test7 = test_render()
        test8 = test_render_trailing()
        test9 = test_render_leading()
        test10 = test_set_glyph()
        test11 = test_set_glyph_color()
        test12 = test_get_glyph()
        test13 = test_update_config()
        test14 = test_get_config()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"WhitespaceType Enum: {'PASS' if test1 else 'FAIL'}")
        print(f"WhitespaceRenderMode Enum: {'PASS' if test2 else 'FAIL'}")
        print(f"WhitespaceGlyph Dataclass: {'PASS' if test3 else 'FAIL'}")
        print(f"WhitespaceConfig Dataclass: {'PASS' if test4 else 'FAIL'}")
        print(f"WhitespaceRenderResult Dataclass: {'PASS' if test5 else 'FAIL'}")
        print(f"WhitespaceRenderer Initialization: {'PASS' if test6 else 'FAIL'}")
        print(f"Render: {'PASS' if test7 else 'FAIL'}")
        print(f"Render Trailing: {'PASS' if test8 else 'FAIL'}")
        print(f"Render Leading: {'PASS' if test9 else 'FAIL'}")
        print(f"Set Glyph: {'PASS' if test10 else 'FAIL'}")
        print(f"Set Glyph Color: {'PASS' if test11 else 'FAIL'}")
        print(f"Get Glyph: {'PASS' if test12 else 'FAIL'}")
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
