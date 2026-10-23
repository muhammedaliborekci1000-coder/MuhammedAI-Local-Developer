"""
Quality Test: Glyph Margin
Glyph margin system testleri.
"""

import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from app.editor.glyph_margin import (
    GlyphType,
    GlyphPosition,
    Glyph,
    GlyphMarginConfig,
    GlyphMarginResult,
    GlyphMarginManager
)


def test_glyph_type_enum():
    """
    Test: GlyphType enum.
    """
    print("=" * 70)
    print("TEST: GlyphType Enum")
    print("=" * 70)
    
    assert GlyphType.BREAKPOINT.value == "breakpoint"
    assert GlyphType.ERROR.value == "error"
    assert GlyphType.WARNING.value == "warning"
    assert GlyphType.INFO.value == "info"
    assert GlyphType.SUCCESS.value == "success"
    assert GlyphType.BOOKMARK.value == "bookmark"
    assert GlyphType.FOLDED.value == "folded"
    assert GlyphType.UNFOLDED.value == "unfolded"
    assert GlyphType.CUSTOM.value == "custom"
    
    print(f"  All enum values verified")
    print(f"  Total types: {len(GlyphType)}")
    
    print("\n" + "=" * 70)
    print("PASS: GlyphType enum")
    print("=" * 70)


def test_glyph_position_enum():
    """
    Test: GlyphPosition enum.
    """
    print("=" * 70)
    print("TEST: GlyphPosition Enum")
    print("=" * 70)
    
    assert GlyphPosition.LEFT.value == "left"
    assert GlyphPosition.RIGHT.value == "right"
    assert GlyphPosition.CENTER.value == "center"
    
    print(f"  All enum values verified")
    print(f"  Total positions: {len(GlyphPosition)}")
    
    print("\n" + "=" * 70)
    print("PASS: GlyphPosition enum")
    print("=" * 70)


def test_glyph_dataclass():
    """
    Test: Glyph dataclass.
    """
    print("=" * 70)
    print("TEST: Glyph Dataclass")
    print("=" * 70)
    
    glyph = Glyph(
        id="glyph_1",
        type=GlyphType.BREAKPOINT,
        line=10,
        icon="●"
    )
    
    assert glyph.id == "glyph_1", "ID eşleşmeli"
    assert glyph.type == GlyphType.BREAKPOINT, "Type eşleşmeli"
    assert glyph.line == 10, "Line eşleşmeli"
    assert glyph.icon == "●", "Icon eşleşmeli"
    
    print(f"  ID: {glyph.id}")
    print(f"  Type: {glyph.type.value}")
    print(f"  Line: {glyph.line}")
    print(f"  Icon: {glyph.icon}")
    
    print("\n" + "=" * 70)
    print("PASS: Glyph dataclass")
    print("=" * 70)


def test_glyph_margin_config_dataclass():
    """
    Test: GlyphMarginConfig dataclass.
    """
    print("=" * 70)
    print("TEST: GlyphMarginConfig Dataclass")
    print("=" * 70)
    
    config = GlyphMarginConfig(
        enabled=True,
        position=GlyphPosition.LEFT
    )
    
    assert config.enabled == True, "Enabled eşleşmeli"
    assert config.position == GlyphPosition.LEFT, "Position eşleşmeli"
    
    print(f"  Enabled: {config.enabled}")
    print(f"  Position: {config.position.value}")
    
    print("\n" + "=" * 70)
    print("PASS: GlyphMarginConfig dataclass")
    print("=" * 70)


def test_glyph_margin_result_dataclass():
    """
    Test: GlyphMarginResult dataclass.
    """
    print("=" * 70)
    print("TEST: GlyphMarginResult Dataclass")
    print("=" * 70)
    
    result = GlyphMarginResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.glyphs, list), "Glyphs list olmalı"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Glyphs: {len(result.glyphs)}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: GlyphMarginResult dataclass")
    print("=" * 70)


def test_glyph_margin_manager_initialization():
    """
    Test: GlyphMarginManager initialization.
    """
    print("=" * 70)
    print("TEST: GlyphMarginManager Initialization")
    print("=" * 70)
    
    config = GlyphMarginConfig()
    manager = GlyphMarginManager(config)
    
    assert manager.config == config, "Config eşleşmeli"
    assert len(manager.glyphs) == 0, "Glyphs boş olmalı"
    
    print(f"  Glyphs: {len(manager.glyphs)}")
    
    print("\n" + "=" * 70)
    print("PASS: GlyphMarginManager initialization")
    print("=" * 70)


def test_add_glyph():
    """
    Test: Add glyph.
    """
    print("=" * 70)
    print("TEST: Add Glyph")
    print("=" * 70)
    
    manager = GlyphMarginManager()
    
    glyph = Glyph(
        id="",
        type=GlyphType.BREAKPOINT,
        line=10,
        icon="●"
    )
    
    result = manager.add_glyph(glyph)
    
    assert result.success == True, "Ekleme başarılı olmalı"
    assert len(manager.glyphs) > 0, "Glyph eklenmeli"
    
    print(f"  Glyph added: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add glyph")
    print("=" * 70)


def test_remove_glyph():
    """
    Test: Remove glyph.
    """
    print("=" * 70)
    print("TEST: Remove Glyph")
    print("=" * 70)
    
    manager = GlyphMarginManager()
    
    glyph = Glyph(
        id="",
        type=GlyphType.BREAKPOINT,
        line=10,
        icon="●"
    )
    
    result = manager.add_glyph(glyph)
    glyph_id = result.glyphs[0].id
    
    result = manager.remove_glyph(glyph_id)
    
    assert result.success == True, "Kaldırma başarılı olmalı"
    assert glyph_id not in manager.glyphs, "Glyph silinmeli"
    
    print(f"  Glyph removed: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Remove glyph")
    print("=" * 70)


def test_get_glyph():
    """
    Test: Get glyph.
    """
    print("=" * 70)
    print("TEST: Get Glyph")
    print("=" * 70)
    
    manager = GlyphMarginManager()
    
    glyph = Glyph(
        id="",
        type=GlyphType.BREAKPOINT,
        line=10,
        icon="●"
    )
    
    result = manager.add_glyph(glyph)
    glyph_id = result.glyphs[0].id
    
    retrieved_glyph = manager.get_glyph(glyph_id)
    
    assert retrieved_glyph is not None, "Glyph bulunmalı"
    assert retrieved_glyph.id == glyph_id, "ID eşleşmeli"
    
    print(f"  Glyph: {retrieved_glyph.icon}")
    
    print("\n" + "=" * 70)
    print("PASS: Get glyph")
    print("=" * 70)


def test_get_all_glyphs():
    """
    Test: Get all glyphs.
    """
    print("=" * 70)
    print("TEST: Get All Glyphs")
    print("=" * 70)
    
    manager = GlyphMarginManager()
    
    glyph = Glyph(
        id="",
        type=GlyphType.BREAKPOINT,
        line=10,
        icon="●"
    )
    
    manager.add_glyph(glyph)
    glyphs = manager.get_all_glyphs()
    
    assert len(glyphs) > 0, "Glyphs olmalı"
    
    print(f"  Total glyphs: {len(glyphs)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get all glyphs")
    print("=" * 70)


def test_get_glyphs_by_type():
    """
    Test: Get glyphs by type.
    """
    print("=" * 70)
    print("TEST: Get Glyphs by Type")
    print("=" * 70)
    
    manager = GlyphMarginManager()
    
    glyph = Glyph(
        id="",
        type=GlyphType.BREAKPOINT,
        line=10,
        icon="●"
    )
    
    manager.add_glyph(glyph)
    glyphs = manager.get_glyphs_by_type(GlyphType.BREAKPOINT)
    
    assert len(glyphs) > 0, "Breakpoint glyphs olmalı"
    
    print(f"  Breakpoint glyphs: {len(glyphs)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get glyphs by type")
    print("=" * 70)


def test_get_glyphs_at_line():
    """
    Test: Get glyphs at line.
    """
    print("=" * 70)
    print("TEST: Get Glyphs at Line")
    print("=" * 70)
    
    manager = GlyphMarginManager()
    
    glyph = Glyph(
        id="",
        type=GlyphType.BREAKPOINT,
        line=10,
        icon="●"
    )
    
    manager.add_glyph(glyph)
    glyphs = manager.get_glyphs_at_line(10)
    
    assert len(glyphs) > 0, "Line 10 glyphs olmalı"
    
    print(f"  Line 10 glyphs: {len(glyphs)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get glyphs at line")
    print("=" * 70)


def test_add_breakpoint():
    """
    Test: Add breakpoint.
    """
    print("=" * 70)
    print("TEST: Add Breakpoint")
    print("=" * 70)
    
    manager = GlyphMarginManager()
    
    result = manager.add_breakpoint(10)
    
    assert result.success == True, "Breakpoint başarılı olmalı"
    
    print(f"  Breakpoint added: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add breakpoint")
    print("=" * 70)


def test_add_error():
    """
    Test: Add error.
    """
    print("=" * 70)
    print("TEST: Add Error")
    print("=" * 70)
    
    manager = GlyphMarginManager()
    
    result = manager.add_error(10, "✗", "Test error")
    
    assert result.success == True, "Error başarılı olmalı"
    
    print(f"  Error added: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add error")
    print("=" * 70)


def test_add_warning():
    """
    Test: Add warning.
    """
    print("=" * 70)
    print("TEST: Add Warning")
    print("=" * 70)
    
    manager = GlyphMarginManager()
    
    result = manager.add_warning(10, "!", "Test warning")
    
    assert result.success == True, "Warning başarılı olmalı"
    
    print(f"  Warning added: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add warning")
    print("=" * 70)


def test_add_info():
    """
    Test: Add info.
    """
    print("=" * 70)
    print("TEST: Add Info")
    print("=" * 70)
    
    manager = GlyphMarginManager()
    
    result = manager.add_info(10, "i", "Test info")
    
    assert result.success == True, "Info başarılı olmalı"
    
    print(f"  Info added: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add error")
    print("=" * 70)


def test_add_bookmark():
    """
    Test: Add bookmark.
    """
    print("=" * 70)
    print("TEST: Add Bookmark")
    print("=" * 70)
    
    manager = GlyphMarginManager()
    
    result = manager.add_bookmark(10)
    
    assert result.success == True, "Bookmark başarılı olmalı"
    
    print(f"  Bookmark added: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add bookmark")
    print("=" * 70)


def test_toggle_fold():
    """
    Test: Toggle fold.
    """
    print("=" * 70)
    print("TEST: Toggle Fold")
    print("=" * 70)
    
    manager = GlyphMarginManager()
    
    result = manager.toggle_fold(10, True)
    
    assert result.success == True, "Fold başarılı olmalı"
    
    print(f"  Fold toggled: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Toggle fold")
    print("=" * 70)


def test_clear_glyphs():
    """
    Test: Clear glyphs.
    """
    print("=" * 70)
    print("TEST: Clear Glyphs")
    print("=" * 70)
    
    manager = GlyphMarginManager()
    
    glyph = Glyph(
        id="",
        type=GlyphType.BREAKPOINT,
        line=10,
        icon="●"
    )
    
    manager.add_glyph(glyph)
    result = manager.clear_glyphs()
    
    assert result.success == True, "Clear başarılı olmalı"
    assert len(manager.glyphs) == 0, "Glyphs temizlenmeli"
    
    print(f"  Cleared: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear glyphs")
    print("=" * 70)


def test_clear_glyphs_by_type():
    """
    Test: Clear glyphs by type.
    """
    print("=" * 70)
    print("TEST: Clear Glyphs by Type")
    print("=" * 70)
    
    manager = GlyphMarginManager()
    
    glyph = Glyph(
        id="",
        type=GlyphType.BREAKPOINT,
        line=10,
        icon="●"
    )
    
    manager.add_glyph(glyph)
    result = manager.clear_glyphs_by_type(GlyphType.BREAKPOINT)
    
    assert result.success == True, "Clear başarılı olmalı"
    
    print(f"  Cleared by type: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear glyphs by type")
    print("=" * 70)


def test_set_glyph_enabled():
    """
    Test: Set glyph enabled.
    """
    print("=" * 70)
    print("TEST: Set Glyph Enabled")
    print("=" * 70)
    
    manager = GlyphMarginManager()
    
    glyph = Glyph(
        id="",
        type=GlyphType.BREAKPOINT,
        line=10,
        icon="●"
    )
    
    result = manager.add_glyph(glyph)
    glyph_id = result.glyphs[0].id
    
    result = manager.set_glyph_enabled(glyph_id, False)
    
    assert result.success == True, "Set başarılı olmalı"
    
    print(f"  Glyph enabled state: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set glyph enabled")
    print("=" * 70)


def test_set_glyph_visible():
    """
    Test: Set glyph visible.
    """
    print("=" * 70)
    print("TEST: Set Glyph Visible")
    print("=" * 70)
    
    manager = GlyphMarginManager()
    
    glyph = Glyph(
        id="",
        type=GlyphType.BREAKPOINT,
        line=10,
        icon="●"
    )
    
    result = manager.add_glyph(glyph)
    glyph_id = result.glyphs[0].id
    
    result = manager.set_glyph_visible(glyph_id, False)
    
    assert result.success == True, "Set başarılı olmalı"
    
    print(f"  Glyph visible state: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set glyph visible")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    manager = GlyphMarginManager()
    
    new_config = GlyphMarginConfig(width=30)
    result = manager.update_config(new_config)
    
    assert result.success == True, "Update başarılı olmalı"
    assert manager.config.width == 30, "Config güncellenmeli"
    
    print(f"  Width: {manager.config.width}")
    
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
    
    config = GlyphMarginConfig(width=30)
    manager = GlyphMarginManager(config)
    
    retrieved_config = manager.get_config()
    
    assert retrieved_config.width == 30, "Config eşleşmeli"
    
    print(f"  Width: {retrieved_config.width}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_glyph_type_enum()
        test2 = test_glyph_position_enum()
        test3 = test_glyph_dataclass()
        test4 = test_glyph_margin_config_dataclass()
        test5 = test_glyph_margin_result_dataclass()
        test6 = test_glyph_margin_manager_initialization()
        test7 = test_add_glyph()
        test8 = test_remove_glyph()
        test9 = test_get_glyph()
        test10 = test_get_all_glyphs()
        test11 = test_get_glyphs_by_type()
        test12 = test_get_glyphs_at_line()
        test13 = test_add_breakpoint()
        test14 = test_add_error()
        test15 = test_add_warning()
        test16 = test_add_info()
        test17 = test_add_bookmark()
        test18 = test_toggle_fold()
        test19 = test_clear_glyphs()
        test20 = test_clear_glyphs_by_type()
        test21 = test_set_glyph_enabled()
        test22 = test_set_glyph_visible()
        test23 = test_update_config()
        test24 = test_get_config()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"GlyphType Enum: {'PASS' if test1 else 'FAIL'}")
        print(f"GlyphPosition Enum: {'PASS' if test2 else 'FAIL'}")
        print(f"Glyph Dataclass: {'PASS' if test3 else 'FAIL'}")
        print(f"GlyphMarginConfig Dataclass: {'PASS' if test4 else 'FAIL'}")
        print(f"GlyphMarginResult Dataclass: {'PASS' if test5 else 'FAIL'}")
        print(f"GlyphMarginManager Initialization: {'PASS' if test6 else 'FAIL'}")
        print(f"Add Glyph: {'PASS' if test7 else 'FAIL'}")
        print(f"Remove Glyph: {'PASS' if test8 else 'FAIL'}")
        print(f"Get Glyph: {'PASS' if test9 else 'FAIL'}")
        print(f"Get All Glyphs: {'PASS' if test10 else 'FAIL'}")
        print(f"Get Glyphs by Type: {'PASS' if test11 else 'FAIL'}")
        print(f"Get Glyphs at Line: {'PASS' if test12 else 'FAIL'}")
        print(f"Add Breakpoint: {'PASS' if test13 else 'FAIL'}")
        print(f"Add Error: {'PASS' if test14 else 'FAIL'}")
        print(f"Add Warning: {'PASS' if test15 else 'FAIL'}")
        print(f"Add Info: {'PASS' if test16 else 'FAIL'}")
        print(f"Add Bookmark: {'PASS' if test17 else 'FAIL'}")
        print(f"Toggle Fold: {'PASS' if test18 else 'FAIL'}")
        print(f"Clear Glyphs: {'PASS' if test19 else 'FAIL'}")
        print(f"Clear Glyphs by Type: {'PASS' if test20 else 'FAIL'}")
        print(f"Set Glyph Enabled: {'PASS' if test21 else 'FAIL'}")
        print(f"Set Glyph Visible: {'PASS' if test22 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test23 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test24 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14, test15, test16, test17, test18, test19, test20, test21, test22, test23, test24])
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
