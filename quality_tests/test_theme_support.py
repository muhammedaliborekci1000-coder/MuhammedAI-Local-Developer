"""
Quality Test: Theme Support
Theme support system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.theme_support import (
    ThemeSupportEngine,
    ThemeType,
    ColorScheme,
    ThemeColors,
    Theme,
    ThemeConfig,
    ThemeResult
)


def test_get_theme():
    """
    Test: Get theme.
    """
    print("=" * 70)
    print("TEST: Get Theme")
    print("=" * 70)
    
    engine = ThemeSupportEngine()
    
    result = engine.get_theme("Monokai")
    
    assert result.success, "Tema bulunmalı"
    assert result.theme is not None, "Theme olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Theme: {result.theme.name}")
    
    print("\n" + "=" * 70)
    print("PASS: Get theme")
    print("=" * 70)


def test_get_all_themes():
    """
    Test: Get all themes.
    """
    print("=" * 70)
    print("TEST: Get All Themes")
    print("=" * 70)
    
    engine = ThemeSupportEngine()
    
    result = engine.get_all_themes()
    
    assert result.success, "Tüm temalar alınmalı"
    assert len(result.themes) > 0, "Temalar olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Themes: {len(result.themes)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get all themes")
    print("=" * 70)


def test_get_active_theme():
    """
    Test: Get active theme.
    """
    print("=" * 70)
    print("TEST: Get Active Theme")
    print("=" * 70)
    
    engine = ThemeSupportEngine()
    
    result = engine.get_active_theme()
    
    assert result.success, "Aktif tema bulunmalı"
    assert result.theme is not None, "Theme olmalı"
    assert result.theme.is_active == True, "Aktif olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Active theme: {result.theme.name}")
    
    print("\n" + "=" * 70)
    print("PASS: Get active theme")
    print("=" * 70)


def test_set_theme():
    """
    Test: Set theme.
    """
    print("=" * 70)
    print("TEST: Set Theme")
    print("=" * 70)
    
    engine = ThemeSupportEngine()
    
    result = engine.set_theme("Dracula")
    
    assert result.success, "Tema ayarlanmalı"
    assert result.theme is not None, "Theme olmalı"
    assert result.theme.name == "Dracula", "Tema eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Theme: {result.theme.name}")
    
    print("\n" + "=" * 70)
    print("PASS: Set theme")
    print("=" * 70)


def test_add_custom_theme():
    """
    Test: Add custom theme.
    """
    print("=" * 70)
    print("TEST: Add Custom Theme")
    print("=" * 70)
    
    engine = ThemeSupportEngine()
    
    colors = ThemeColors(background="#000000", foreground="#ffffff")
    custom_theme = Theme(
        name="Custom Dark",
        theme_type=ThemeType.DARK,
        color_scheme=ColorScheme.CUSTOM,
        colors=colors
    )
    
    result = engine.add_custom_theme(custom_theme)
    
    assert result.success, "Özel tema eklenmeli"
    assert result.theme is not None, "Theme olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Theme: {result.theme.name}")
    
    print("\n" + "=" * 70)
    print("PASS: Add custom theme")
    print("=" * 70)


def test_remove_theme():
    """
    Test: Remove theme.
    """
    print("=" * 70)
    print("TEST: Remove Theme")
    print("=" * 70)
    
    engine = ThemeSupportEngine()
    
    # Özel tema ekle
    colors = ThemeColors(background="#000000", foreground="#ffffff")
    custom_theme = Theme(
        name="Temp Theme",
        theme_type=ThemeType.DARK,
        color_scheme=ColorScheme.CUSTOM,
        colors=colors
    )
    engine.add_custom_theme(custom_theme)
    
    # Kaldır
    result = engine.remove_theme("Temp Theme")
    
    assert result.success, "Tema kaldırılmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Remove theme")
    print("=" * 70)


def test_get_themes_by_type():
    """
    Test: Get themes by type.
    """
    print("=" * 70)
    print("TEST: Get Themes By Type")
    print("=" * 70)
    
    engine = ThemeSupportEngine()
    
    result = engine.get_themes_by_type(ThemeType.DARK)
    
    assert result.success, "Temalar alınmalı"
    assert len(result.themes) > 0, "Dark temalar olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Themes: {len(result.themes)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get themes by type")
    print("=" * 70)


def test_get_builtin_themes():
    """
    Test: Get builtin themes.
    """
    print("=" * 70)
    print("TEST: Get Builtin Themes")
    print("=" * 70)
    
    engine = ThemeSupportEngine()
    
    result = engine.get_builtin_themes()
    
    assert result.success, "Builtin temalar alınmalı"
    assert len(result.themes) > 0, "Builtin temalar olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Builtin themes: {len(result.themes)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get builtin themes")
    print("=" * 70)


def test_get_custom_themes():
    """
    Test: Get custom themes.
    """
    print("=" * 70)
    print("TEST: Get Custom Themes")
    print("=" * 70)
    
    engine = ThemeSupportEngine()
    
    result = engine.get_custom_themes()
    
    assert result.success, "Özel temalar alınmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Custom themes: {len(result.themes)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get custom themes")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    engine = ThemeSupportEngine()
    
    new_config = ThemeConfig(current_theme="Monokai")
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
    
    engine = ThemeSupportEngine()
    
    config = engine.get_config()
    
    assert config is not None, "Config olmalı"
    assert config.current_theme is not None, "Current theme olmalı"
    
    print(f"  Current theme: {config.current_theme}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


def test_toggle_auto_switch():
    """
    Test: Toggle auto switch.
    """
    print("=" * 70)
    print("TEST: Toggle Auto Switch")
    print("=" * 70)
    
    engine = ThemeSupportEngine()
    
    result = engine.toggle_auto_switch()
    
    assert result.success, "Toggle başarılı olmalı"
    assert engine.config.auto_switch == True, "Enabled olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Auto switch: {engine.config.auto_switch}")
    
    print("\n" + "=" * 70)
    print("PASS: Toggle auto switch")
    print("=" * 70)


def test_toggle_follow_system():
    """
    Test: Toggle follow system.
    """
    print("=" * 70)
    print("TEST: Toggle Follow System")
    print("=" * 70)
    
    engine = ThemeSupportEngine()
    
    result = engine.toggle_follow_system()
    
    assert result.success, "Toggle başarılı olmalı"
    assert engine.config.follow_system == False, "Disabled olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Follow system: {engine.config.follow_system}")
    
    print("\n" + "=" * 70)
    print("PASS: Toggle follow system")
    print("=" * 70)


def test_theme_type_enum():
    """
    Test: ThemeType enum.
    """
    print("=" * 70)
    print("TEST: ThemeType Enum")
    print("=" * 70)
    
    assert ThemeType.LIGHT.value == "light"
    assert ThemeType.DARK.value == "dark"
    assert ThemeType.HIGH_CONTRAST.value == "high_contrast"
    assert ThemeType.CUSTOM.value == "custom"
    
    print(f"  All enum values verified")
    print(f"  Total types: {len(ThemeType)}")
    
    print("\n" + "=" * 70)
    print("PASS: ThemeType enum")
    print("=" * 70)


def test_color_scheme_enum():
    """
    Test: ColorScheme enum.
    """
    print("=" * 70)
    print("TEST: ColorScheme Enum")
    print("=" * 70)
    
    assert ColorScheme.MONOKAI.value == "monokai"
    assert ColorScheme.DRACULA.value == "dracula"
    assert ColorScheme.SOLARIZED.value == "solarized"
    assert ColorScheme.GITHUB.value == "github"
    assert ColorScheme.NORD.value == "nord"
    assert ColorScheme.ONE_DARK.value == "one_dark"
    assert ColorScheme.VS_CODE.value == "vs_code"
    assert ColorScheme.CUSTOM.value == "custom"
    
    print(f"  All enum values verified")
    print(f"  Total schemes: {len(ColorScheme)}")
    
    print("\n" + "=" * 70)
    print("PASS: ColorScheme enum")
    print("=" * 70)


def test_theme_colors_dataclass():
    """
    Test: ThemeColors dataclass.
    """
    print("=" * 70)
    print("TEST: ThemeColors Dataclass")
    print("=" * 70)
    
    colors = ThemeColors(
        background="#1e1e1e",
        foreground="#d4d4d4"
    )
    
    assert colors.background == "#1e1e1e", "Background eşleşmeli"
    assert colors.foreground == "#d4d4d4", "Foreground eşleşmeli"
    
    print(f"  Background: {colors.background}")
    print(f"  Foreground: {colors.foreground}")
    
    print("\n" + "=" * 70)
    print("PASS: ThemeColors dataclass")
    print("=" * 70)


def test_theme_dataclass():
    """
    Test: Theme dataclass.
    """
    print("=" * 70)
    print("TEST: Theme Dataclass")
    print("=" * 70)
    
    colors = ThemeColors()
    theme = Theme(
        name="Test Theme",
        theme_type=ThemeType.DARK,
        color_scheme=ColorScheme.CUSTOM,
        colors=colors,
        is_builtin=True
    )
    
    assert theme.name == "Test Theme", "Name eşleşmeli"
    assert theme.theme_type == ThemeType.DARK, "Type eşleşmeli"
    assert theme.is_builtin == True, "Builtin eşleşmeli"
    
    print(f"  Name: {theme.name}")
    print(f"  Type: {theme.theme_type.value}")
    print(f"  Builtin: {theme.is_builtin}")
    
    print("\n" + "=" * 70)
    print("PASS: Theme dataclass")
    print("=" * 70)


def test_theme_config_dataclass():
    """
    Test: ThemeConfig dataclass.
    """
    print("=" * 70)
    print("TEST: ThemeConfig Dataclass")
    print("=" * 70)
    
    config = ThemeConfig(
        current_theme="Monokai",
        auto_switch=True,
        follow_system=True
    )
    
    assert config.current_theme == "Monokai", "Current theme eşleşmeli"
    assert config.auto_switch == True, "Auto switch eşleşmeli"
    assert config.follow_system == True, "Follow system eşleşmeli"
    
    print(f"  Current theme: {config.current_theme}")
    print(f"  Auto switch: {config.auto_switch}")
    print(f"  Follow system: {config.follow_system}")
    
    print("\n" + "=" * 70)
    print("PASS: ThemeConfig dataclass")
    print("=" * 70)


def test_theme_result_dataclass():
    """
    Test: ThemeResult dataclass.
    """
    print("=" * 70)
    print("TEST: ThemeResult Dataclass")
    print("=" * 70)
    
    result = ThemeResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.themes, list), "Themes list olmalı"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Themes: {len(result.themes)}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: ThemeResult dataclass")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_get_theme()
        test2 = test_get_all_themes()
        test3 = test_get_active_theme()
        test4 = test_set_theme()
        test5 = test_add_custom_theme()
        test6 = test_remove_theme()
        test7 = test_get_themes_by_type()
        test8 = test_get_builtin_themes()
        test9 = test_get_custom_themes()
        test10 = test_update_config()
        test11 = test_get_config()
        test12 = test_toggle_auto_switch()
        test13 = test_toggle_follow_system()
        test14 = test_theme_type_enum()
        test15 = test_color_scheme_enum()
        test16 = test_theme_colors_dataclass()
        test17 = test_theme_dataclass()
        test18 = test_theme_config_dataclass()
        test19 = test_theme_result_dataclass()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Get Theme: {'PASS' if test1 else 'FAIL'}")
        print(f"Get All Themes: {'PASS' if test2 else 'FAIL'}")
        print(f"Get Active Theme: {'PASS' if test3 else 'FAIL'}")
        print(f"Set Theme: {'PASS' if test4 else 'FAIL'}")
        print(f"Add Custom Theme: {'PASS' if test5 else 'FAIL'}")
        print(f"Remove Theme: {'PASS' if test6 else 'FAIL'}")
        print(f"Get Themes By Type: {'PASS' if test7 else 'FAIL'}")
        print(f"Get Builtin Themes: {'PASS' if test8 else 'FAIL'}")
        print(f"Get Custom Themes: {'PASS' if test9 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test10 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test11 else 'FAIL'}")
        print(f"Toggle Auto Switch: {'PASS' if test12 else 'FAIL'}")
        print(f"Toggle Follow System: {'PASS' if test13 else 'FAIL'}")
        print(f"ThemeType Enum: {'PASS' if test14 else 'FAIL'}")
        print(f"ColorScheme Enum: {'PASS' if test15 else 'FAIL'}")
        print(f"ThemeColors Dataclass: {'PASS' if test16 else 'FAIL'}")
        print(f"Theme Dataclass: {'PASS' if test17 else 'FAIL'}")
        print(f"ThemeConfig Dataclass: {'PASS' if test18 else 'FAIL'}")
        print(f"ThemeResult Dataclass: {'PASS' if test19 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14, test15, test16, test17, test18, test19])
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
