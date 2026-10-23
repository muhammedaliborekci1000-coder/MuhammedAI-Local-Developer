"""
Quality Test: Font Size Control
Font size control system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.font_size_control import (
    FontSizeControlEngine,
    FontSizePreset,
    FontFamily,
    FontSettings,
    FontSizeResult
)


def test_increase_font_size():
    """
    Test: Increase font size.
    """
    print("=" * 70)
    print("TEST: Increase Font Size")
    print("=" * 70)
    
    engine = FontSizeControlEngine()
    
    result = engine.increase_font_size()
    
    assert result.success, "Artırma başarılı olmalı"
    assert result.font_size == 16, "Font size 16 olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Font size: {result.font_size}")
    
    print("\n" + "=" * 70)
    print("PASS: Increase font size")
    print("=" * 70)


def test_decrease_font_size():
    """
    Test: Decrease font size.
    """
    print("=" * 70)
    print("TEST: Decrease Font Size")
    print("=" * 70)
    
    engine = FontSizeControlEngine()
    
    result = engine.decrease_font_size()
    
    assert result.success, "Azaltma başarılı olmalı"
    assert result.font_size == 12, "Font size 12 olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Font size: {result.font_size}")
    
    print("\n" + "=" * 70)
    print("PASS: Decrease font size")
    print("=" * 70)


def test_set_font_size():
    """
    Test: Set font size.
    """
    print("=" * 70)
    print("TEST: Set Font Size")
    print("=" * 70)
    
    engine = FontSizeControlEngine()
    
    result = engine.set_font_size(18)
    
    assert result.success, "Ayar başarılı olmalı"
    assert result.font_size == 18, "Font size 18 olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Font size: {result.font_size}")
    
    print("\n" + "=" * 70)
    print("PASS: Set font size")
    print("=" * 70)


def test_get_font_size():
    """
    Test: Get font size.
    """
    print("=" * 70)
    print("TEST: Get Font Size")
    print("=" * 70)
    
    engine = FontSizeControlEngine()
    
    result = engine.get_font_size()
    
    assert result.success, "Alma başarılı olmalı"
    assert result.font_size == 14, "Font size 14 olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Font size: {result.font_size}")
    
    print("\n" + "=" * 70)
    print("PASS: Get font size")
    print("=" * 70)


def test_reset_font_size():
    """
    Test: Reset font size.
    """
    print("=" * 70)
    print("TEST: Reset Font Size")
    print("=" * 70)
    
    engine = FontSizeControlEngine()
    engine.set_font_size(20)
    
    result = engine.reset_font_size()
    
    assert result.success, "Sıfırlama başarılı olmalı"
    assert result.font_size == 14, "Font size 14 olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Font size: {result.font_size}")
    
    print("\n" + "=" * 70)
    print("PASS: Reset font size")
    print("=" * 70)


def test_set_preset():
    """
    Test: Set preset.
    """
    print("=" * 70)
    print("TEST: Set Preset")
    print("=" * 70)
    
    engine = FontSizeControlEngine()
    
    result = engine.set_preset(FontSizePreset.LARGE)
    
    assert result.success, "Preset ayar başarılı olmalı"
    assert result.font_size == 14, "Font size 14 olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Font size: {result.font_size}")
    
    print("\n" + "=" * 70)
    print("PASS: Set preset")
    print("=" * 70)


def test_zoom_in():
    """
    Test: Zoom in.
    """
    print("=" * 70)
    print("TEST: Zoom In")
    print("=" * 70)
    
    engine = FontSizeControlEngine()
    
    result = engine.zoom_in()
    
    assert result.success, "Zoom in başarılı olmalı"
    assert result.font_size == 16, "Font size 16 olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Font size: {result.font_size}")
    
    print("\n" + "=" * 70)
    print("PASS: Zoom in")
    print("=" * 70)


def test_zoom_out():
    """
    Test: Zoom out.
    """
    print("=" * 70)
    print("TEST: Zoom Out")
    print("=" * 70)
    
    engine = FontSizeControlEngine()
    
    result = engine.zoom_out()
    
    assert result.success, "Zoom out başarılı olmalı"
    assert result.font_size == 12, "Font size 12 olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Font size: {result.font_size}")
    
    print("\n" + "=" * 70)
    print("PASS: Zoom out")
    print("=" * 70)


def test_set_line_height():
    """
    Test: Set line height.
    """
    print("=" * 70)
    print("TEST: Set Line Height")
    print("=" * 70)
    
    engine = FontSizeControlEngine()
    
    result = engine.set_line_height(2.0)
    
    assert result.success, "Ayar başarılı olmalı"
    assert engine.settings.line_height == 2.0, "Line height 2.0 olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Line height: {engine.settings.line_height}")
    
    print("\n" + "=" * 70)
    print("PASS: Set line height")
    print("=" * 70)


def test_set_font_family():
    """
    Test: Set font family.
    """
    print("=" * 70)
    print("TEST: Set Font Family")
    print("=" * 70)
    
    engine = FontSizeControlEngine()
    
    result = engine.set_font_family(FontFamily.SANS_SERIF)
    
    assert result.success, "Ayar başarılı olmalı"
    assert engine.settings.font_family == FontFamily.SANS_SERIF, "Font family eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Font family: {engine.settings.font_family.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Set font family")
    print("=" * 70)


def test_set_custom_font_family():
    """
    Test: Set custom font family.
    """
    print("=" * 70)
    print("TEST: Set Custom Font Family")
    print("=" * 70)
    
    engine = FontSizeControlEngine()
    
    result = engine.set_custom_font_family("Fira Code")
    
    assert result.success, "Ayar başarılı olmalı"
    assert engine.settings.custom_font_family == "Fira Code", "Custom font eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Custom font: {engine.settings.custom_font_family}")
    
    print("\n" + "=" * 70)
    print("PASS: Set custom font family")
    print("=" * 70)


def test_set_ui_font_size():
    """
    Test: Set UI font size.
    """
    print("=" * 70)
    print("TEST: Set UI Font Size")
    print("=" * 70)
    
    engine = FontSizeControlEngine()
    
    result = engine.set_ui_font_size(14)
    
    assert result.success, "Ayar başarılı olmalı"
    assert engine.settings.ui_font_size == 14, "UI font size 14 olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  UI font size: {engine.settings.ui_font_size}")
    
    print("\n" + "=" * 70)
    print("PASS: Set UI font size")
    print("=" * 70)


def test_set_letter_spacing():
    """
    Test: Set letter spacing.
    """
    print("=" * 70)
    print("TEST: Set Letter Spacing")
    print("=" * 70)
    
    engine = FontSizeControlEngine()
    
    result = engine.set_letter_spacing(1.0)
    
    assert result.success, "Ayar başarılı olmalı"
    assert engine.settings.letter_spacing == 1.0, "Letter spacing 1.0 olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Letter spacing: {engine.settings.letter_spacing}")
    
    print("\n" + "=" * 70)
    print("PASS: Set letter spacing")
    print("=" * 70)


def test_set_word_spacing():
    """
    Test: Set word spacing.
    """
    print("=" * 70)
    print("TEST: Set Word Spacing")
    print("=" * 70)
    
    engine = FontSizeControlEngine()
    
    result = engine.set_word_spacing(1.0)
    
    assert result.success, "Ayar başarılı olmalı"
    assert engine.settings.word_spacing == 1.0, "Word spacing 1.0 olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Word spacing: {engine.settings.word_spacing}")
    
    print("\n" + "=" * 70)
    print("PASS: Set word spacing")
    print("=" * 70)


def test_set_min_font_size():
    """
    Test: Set min font size.
    """
    print("=" * 70)
    print("TEST: Set Min Font Size")
    print("=" * 70)
    
    engine = FontSizeControlEngine()
    
    result = engine.set_min_font_size(10)
    
    assert result.success, "Ayar başarılı olmalı"
    assert engine.settings.min_font_size == 10, "Min font size 10 olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Min font size: {engine.settings.min_font_size}")
    
    print("\n" + "=" * 70)
    print("PASS: Set min font size")
    print("=" * 70)


def test_set_max_font_size():
    """
    Test: Set max font size.
    """
    print("=" * 70)
    print("TEST: Set Max Font Size")
    print("=" * 70)
    
    engine = FontSizeControlEngine()
    
    result = engine.set_max_font_size(48)
    
    assert result.success, "Ayar başarılı olmalı"
    assert engine.settings.max_font_size == 48, "Max font size 48 olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Max font size: {engine.settings.max_font_size}")
    
    print("\n" + "=" * 70)
    print("PASS: Set max font size")
    print("=" * 70)


def test_get_settings():
    """
    Test: Get settings.
    """
    print("=" * 70)
    print("TEST: Get Settings")
    print("=" * 70)
    
    engine = FontSizeControlEngine()
    
    settings = engine.get_settings()
    
    assert settings is not None, "Ayarlar olmalı"
    assert settings.editor_font_size == 14, "Editor font size 14 olmalı"
    
    print(f"  Editor font size: {settings.editor_font_size}")
    
    print("\n" + "=" * 70)
    print("PASS: Get settings")
    print("=" * 70)


def test_update_settings():
    """
    Test: Update settings.
    """
    print("=" * 70)
    print("TEST: Update Settings")
    print("=" * 70)
    
    engine = FontSizeControlEngine()
    
    new_settings = FontSettings(editor_font_size=16)
    result = engine.update_settings(new_settings)
    
    assert result.success, "Güncelleme başarılı olmalı"
    assert engine.settings.editor_font_size == 16, "Editor font size 16 olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Editor font size: {engine.settings.editor_font_size}")
    
    print("\n" + "=" * 70)
    print("PASS: Update settings")
    print("=" * 70)


def test_font_size_preset_enum():
    """
    Test: FontSizePreset enum.
    """
    print("=" * 70)
    print("TEST: FontSizePreset Enum")
    print("=" * 70)
    
    assert FontSizePreset.EXTRA_SMALL.value == 8
    assert FontSizePreset.SMALL.value == 10
    assert FontSizePreset.MEDIUM.value == 12
    assert FontSizePreset.LARGE.value == 14
    assert FontSizePreset.EXTRA_LARGE.value == 16
    assert FontSizePreset.HUGE.value == 18
    assert FontSizePreset.EXTRA_HUGE.value == 20
    
    print(f"  All enum values verified")
    print(f"  Total presets: {len(FontSizePreset)}")
    
    print("\n" + "=" * 70)
    print("PASS: FontSizePreset enum")
    print("=" * 70)


def test_font_family_enum():
    """
    Test: FontFamily enum.
    """
    print("=" * 70)
    print("TEST: FontFamily Enum")
    print("=" * 70)
    
    assert FontFamily.MONOSPACE.value == "monospace"
    assert FontFamily.SANS_SERIF.value == "sans-serif"
    assert FontFamily.SERIF.value == "serif"
    assert FontFamily.CUSTOM.value == "custom"
    
    print(f"  All enum values verified")
    print(f"  Total families: {len(FontFamily)}")
    
    print("\n" + "=" * 70)
    print("PASS: FontFamily enum")
    print("=" * 70)


def test_font_settings_dataclass():
    """
    Test: FontSettings dataclass.
    """
    print("=" * 70)
    print("TEST: FontSettings Dataclass")
    print("=" * 70)
    
    settings = FontSettings(
        editor_font_size=16,
        ui_font_size=14,
        line_height=1.5
    )
    
    assert settings.editor_font_size == 16, "Editor font size eşleşmeli"
    assert settings.ui_font_size == 14, "UI font size eşleşmeli"
    assert settings.line_height == 1.5, "Line height eşleşmeli"
    
    print(f"  Editor font size: {settings.editor_font_size}")
    print(f"  UI font size: {settings.ui_font_size}")
    print(f"  Line height: {settings.line_height}")
    
    print("\n" + "=" * 70)
    print("PASS: FontSettings dataclass")
    print("=" * 70)


def test_font_size_result_dataclass():
    """
    Test: FontSizeResult dataclass.
    """
    print("=" * 70)
    print("TEST: FontSizeResult Dataclass")
    print("=" * 70)
    
    result = FontSizeResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: FontSizeResult dataclass")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_increase_font_size()
        test2 = test_decrease_font_size()
        test3 = test_set_font_size()
        test4 = test_get_font_size()
        test5 = test_reset_font_size()
        test6 = test_set_preset()
        test7 = test_zoom_in()
        test8 = test_zoom_out()
        test9 = test_set_line_height()
        test10 = test_set_font_family()
        test11 = test_set_custom_font_family()
        test12 = test_set_ui_font_size()
        test13 = test_set_letter_spacing()
        test14 = test_set_word_spacing()
        test15 = test_set_min_font_size()
        test16 = test_set_max_font_size()
        test17 = test_get_settings()
        test18 = test_update_settings()
        test19 = test_font_size_preset_enum()
        test20 = test_font_family_enum()
        test21 = test_font_settings_dataclass()
        test22 = test_font_size_result_dataclass()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Increase Font Size: {'PASS' if test1 else 'FAIL'}")
        print(f"Decrease Font Size: {'PASS' if test2 else 'FAIL'}")
        print(f"Set Font Size: {'PASS' if test3 else 'FAIL'}")
        print(f"Get Font Size: {'PASS' if test4 else 'FAIL'}")
        print(f"Reset Font Size: {'PASS' if test5 else 'FAIL'}")
        print(f"Set Preset: {'PASS' if test6 else 'FAIL'}")
        print(f"Zoom In: {'PASS' if test7 else 'FAIL'}")
        print(f"Zoom Out: {'PASS' if test8 else 'FAIL'}")
        print(f"Set Line Height: {'PASS' if test9 else 'FAIL'}")
        print(f"Set Font Family: {'PASS' if test10 else 'FAIL'}")
        print(f"Set Custom Font Family: {'PASS' if test11 else 'FAIL'}")
        print(f"Set UI Font Size: {'PASS' if test12 else 'FAIL'}")
        print(f"Set Letter Spacing: {'PASS' if test13 else 'FAIL'}")
        print(f"Set Word Spacing: {'PASS' if test14 else 'FAIL'}")
        print(f"Set Min Font Size: {'PASS' if test15 else 'FAIL'}")
        print(f"Set Max Font Size: {'PASS' if test16 else 'FAIL'}")
        print(f"Get Settings: {'PASS' if test17 else 'FAIL'}")
        print(f"Update Settings: {'PASS' if test18 else 'FAIL'}")
        print(f"FontSizePreset Enum: {'PASS' if test19 else 'FAIL'}")
        print(f"FontFamily Enum: {'PASS' if test20 else 'FAIL'}")
        print(f"FontSettings Dataclass: {'PASS' if test21 else 'FAIL'}")
        print(f"FontSizeResult Dataclass: {'PASS' if test22 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14, test15, test16, test17, test18, test19, test20, test21, test22])
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
