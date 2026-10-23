"""
Quality Test: Theme Manager
Theme manager system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.theme_manager import (
    ThemeType,
    ThemeCategory,
    ThemeColors,
    ThemeSettings,
    Theme,
    ThemeConfig,
    ThemeManager
)


def test_theme_type_enum():
    """
    Test: ThemeType enum.
    """
    print("=" * 70)
    print("TEST: ThemeType Enum")
    print("=" * 70)
    
    assert ThemeType.DARK.value == "dark"
    assert ThemeType.LIGHT.value == "light"
    assert ThemeType.CUSTOM.value == "custom"
    
    print(f"  All enum values verified")
    print(f"  Total types: {len(ThemeType)}")
    
    print("\n" + "=" * 70)
    print("PASS: ThemeType enum")
    print("=" * 70)


def test_theme_category_enum():
    """
    Test: ThemeCategory enum.
    """
    print("=" * 70)
    print("TEST: ThemeCategory Enum")
    print("=" * 70)
    
    assert ThemeCategory.BUILT_IN.value == "built_in"
    assert ThemeCategory.USER_INSTALLED.value == "user_installed"
    assert ThemeCategory.COMMUNITY.value == "community"
    
    print(f"  All enum values verified")
    print(f"  Total categories: {len(ThemeCategory)}")
    
    print("\n" + "=" * 70)
    print("PASS: ThemeCategory enum")
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


def test_theme_settings_dataclass():
    """
    Test: ThemeSettings dataclass.
    """
    print("=" * 70)
    print("TEST: ThemeSettings Dataclass")
    print("=" * 70)
    
    settings = ThemeSettings(
        font_family="Consolas",
        font_size=14
    )
    
    assert settings.font_family == "Consolas", "Font family eşleşmeli"
    assert settings.font_size == 14, "Font size eşleşmeli"
    
    print(f"  Font family: {settings.font_family}")
    print(f"  Font size: {settings.font_size}")
    
    print("\n" + "=" * 70)
    print("PASS: ThemeSettings dataclass")
    print("=" * 70)


def test_theme_dataclass():
    """
    Test: Theme dataclass.
    """
    print("=" * 70)
    print("TEST: Theme Dataclass")
    print("=" * 70)
    
    theme = Theme(
        id="test_theme",
        name="Test Theme",
        type=ThemeType.DARK,
        category=ThemeCategory.BUILT_IN
    )
    
    assert theme.id == "test_theme", "ID eşleşmeli"
    assert theme.name == "Test Theme", "Name eşleşmeli"
    
    print(f"  ID: {theme.id}")
    print(f"  Name: {theme.name}")
    
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
        current_theme_id="default_dark",
        auto_switch=False
    )
    
    assert config.current_theme_id == "default_dark", "Current theme ID eşleşmeli"
    assert config.auto_switch == False, "Auto switch eşleşmeli"
    
    print(f"  Current theme ID: {config.current_theme_id}")
    print(f"  Auto switch: {config.auto_switch}")
    
    print("\n" + "=" * 70)
    print("PASS: ThemeConfig dataclass")
    print("=" * 70)


def test_theme_manager_initialization():
    """
    Test: ThemeManager initialization.
    """
    print("=" * 70)
    print("TEST: ThemeManager Initialization")
    print("=" * 70)
    
    config = ThemeConfig()
    manager = ThemeManager(config)
    
    assert manager.config == config, "Config eşleşmeli"
    assert len(manager.themes) > 0, "Themes olmalı"
    
    print(f"  Themes: {len(manager.themes)}")
    
    print("\n" + "=" * 70)
    print("PASS: ThemeManager initialization")
    print("=" * 70)


def test_get_theme():
    """
    Test: Get theme.
    """
    print("=" * 70)
    print("TEST: Get Theme")
    print("=" * 70)
    
    manager = ThemeManager()
    
    theme = manager.get_theme("default_dark")
    
    assert theme is not None, "Theme olmalı"
    assert theme.id == "default_dark", "Theme ID eşleşmeli"
    
    print(f"  Theme: {theme.name}")
    
    print("\n" + "=" * 70)
    print("PASS: Get theme")
    print("=" * 70)


def test_get_current_theme():
    """
    Test: Get current theme.
    """
    print("=" * 70)
    print("TEST: Get Current Theme")
    print("=" * 70)
    
    manager = ThemeManager()
    
    current_theme = manager.get_current_theme()
    
    assert current_theme is not None, "Current theme olmalı"
    
    print(f"  Current theme: {current_theme.name}")
    
    print("\n" + "=" * 70)
    print("PASS: Get current theme")
    print("=" * 70)


def test_set_theme():
    """
    Test: Set theme.
    """
    print("=" * 70)
    print("TEST: Set Theme")
    print("=" * 70)
    
    manager = ThemeManager()
    
    result = manager.set_theme("default_light")
    
    assert result == True, "Set başarılı olmalı"
    assert manager.config.current_theme_id == "default_light", "Theme değişmeli"
    
    print(f"  Current theme: {manager.config.current_theme_id}")
    
    print("\n" + "=" * 70)
    print("PASS: Set theme")
    print("=" * 70)


def test_switch_theme_type():
    """
    Test: Switch theme type.
    """
    print("=" * 70)
    print("TEST: Switch Theme Type")
    print("=" * 70)
    
    manager = ThemeManager()
    
    result = manager.switch_theme_type(ThemeType.LIGHT)
    
    assert result == True, "Switch başarılı olmalı"
    
    current_theme = manager.get_current_theme()
    assert current_theme.type == ThemeType.LIGHT, "Theme type LIGHT olmalı"
    
    print(f"  Theme type: {current_theme.type.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Switch theme type")
    print("=" * 70)


def test_toggle_dark_light():
    """
    Test: Toggle dark/light.
    """
    print("=" * 70)
    print("TEST: Toggle Dark/Light")
    print("=" * 70)
    
    manager = ThemeManager()
    
    initial_type = manager.get_current_theme().type
    manager.toggle_dark_light()
    new_type = manager.get_current_theme().type
    
    assert initial_type != new_type, "Theme type değişmeli"
    
    print(f"  Initial type: {initial_type.value}")
    print(f"  New type: {new_type.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Toggle dark/light")
    print("=" * 70)


def test_add_custom_theme():
    """
    Test: Add custom theme.
    """
    print("=" * 70)
    print("TEST: Add Custom Theme")
    print("=" * 70)
    
    manager = ThemeManager()
    
    custom_theme = Theme(
        id="custom_test",
        name="Custom Test",
        type=ThemeType.CUSTOM,
        category=ThemeCategory.USER_INSTALLED
    )
    
    result = manager.add_custom_theme(custom_theme)
    
    assert result == True, "Add başarılı olmalı"
    assert manager.get_theme("custom_test") is not None, "Theme eklenmeli"
    
    print(f"  Custom theme added: {custom_theme.name}")
    
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
    
    manager = ThemeManager()
    
    custom_theme = Theme(
        id="custom_test",
        name="Custom Test",
        type=ThemeType.CUSTOM,
        category=ThemeCategory.USER_INSTALLED
    )
    
    manager.add_custom_theme(custom_theme)
    result = manager.remove_theme("custom_test")
    
    assert result == True, "Remove başarılı olmalı"
    assert manager.get_theme("custom_test") is None, "Theme silinmeli"
    
    print(f"  Custom theme removed: {custom_theme.name}")
    
    print("\n" + "=" * 70)
    print("PASS: Remove theme")
    print("=" * 70)


def test_get_all_themes():
    """
    Test: Get all themes.
    """
    print("=" * 70)
    print("TEST: Get All Themes")
    print("=" * 70)
    
    manager = ThemeManager()
    
    all_themes = manager.get_all_themes()
    
    assert len(all_themes) > 0, "Themes olmalı"
    
    print(f"  Total themes: {len(all_themes)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get all themes")
    print("=" * 70)


def test_get_themes_by_type():
    """
    Test: Get themes by type.
    """
    print("=" * 70)
    print("TEST: Get Themes by Type")
    print("=" * 70)
    
    manager = ThemeManager()
    
    dark_themes = manager.get_themes_by_type(ThemeType.DARK)
    
    assert len(dark_themes) > 0, "Dark themes olmalı"
    
    print(f"  Dark themes: {len(dark_themes)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get themes by type")
    print("=" * 70)


def test_get_themes_by_category():
    """
    Test: Get themes by category.
    """
    print("=" * 70)
    print("TEST: Get Themes by Category")
    print("=" * 70)
    
    manager = ThemeManager()
    
    builtin_themes = manager.get_themes_by_category(ThemeCategory.BUILT_IN)
    
    assert len(builtin_themes) > 0, "Built-in themes olmalı"
    
    print(f"  Built-in themes: {len(builtin_themes)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get themes by category")
    print("=" * 70)


def test_create_custom_theme():
    """
    Test: Create custom theme.
    """
    print("=" * 70)
    print("TEST: Create Custom Theme")
    print("=" * 70)
    
    manager = ThemeManager()
    
    custom_theme = manager.create_custom_theme(
        name="My Custom Theme",
        description="My custom theme"
    )
    
    assert custom_theme is not None, "Theme oluşturulmalı"
    assert custom_theme.name == "My Custom Theme", "Name eşleşmeli"
    
    print(f"  Custom theme created: {custom_theme.name}")
    
    print("\n" + "=" * 70)
    print("PASS: Create custom theme")
    print("=" * 70)


def test_update_theme_colors():
    """
    Test: Update theme colors.
    """
    print("=" * 70)
    print("TEST: Update Theme Colors")
    print("=" * 70)
    
    manager = ThemeManager()
    
    new_colors = ThemeColors(background="#000000")
    result = manager.update_theme_colors("default_dark", new_colors)
    
    assert result == True, "Update başarılı olmalı"
    
    theme = manager.get_theme("default_dark")
    assert theme.colors.background == "#000000", "Background güncellenmeli"
    
    print(f"  Background updated: {theme.colors.background}")
    
    print("\n" + "=" * 70)
    print("PASS: Update theme colors")
    print("=" * 70)


def test_update_theme_settings():
    """
    Test: Update theme settings.
    """
    print("=" * 70)
    print("TEST: Update Theme Settings")
    print("=" * 70)
    
    manager = ThemeManager()
    
    new_settings = ThemeSettings(font_size=16)
    result = manager.update_theme_settings("default_dark", new_settings)
    
    assert result == True, "Update başarılı olmalı"
    
    theme = manager.get_theme("default_dark")
    assert theme.settings.font_size == 16, "Font size güncellenmeli"
    
    print(f"  Font size updated: {theme.settings.font_size}")
    
    print("\n" + "=" * 70)
    print("PASS: Update theme settings")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    manager = ThemeManager()
    
    new_config = ThemeConfig(auto_switch=True)
    manager.update_config(new_config)
    
    assert manager.config.auto_switch == True, "Config güncellenmeli"
    
    print(f"  Auto switch: {manager.config.auto_switch}")
    
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
    
    config = ThemeConfig(auto_switch=True)
    manager = ThemeManager(config)
    
    retrieved_config = manager.get_config()
    
    assert retrieved_config.auto_switch == True, "Config eşleşmeli"
    
    print(f"  Auto switch: {retrieved_config.auto_switch}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_theme_type_enum()
        test2 = test_theme_category_enum()
        test3 = test_theme_colors_dataclass()
        test4 = test_theme_settings_dataclass()
        test5 = test_theme_dataclass()
        test6 = test_theme_config_dataclass()
        test7 = test_theme_manager_initialization()
        test8 = test_get_theme()
        test9 = test_get_current_theme()
        test10 = test_set_theme()
        test11 = test_switch_theme_type()
        test12 = test_toggle_dark_light()
        test13 = test_add_custom_theme()
        test14 = test_remove_theme()
        test15 = test_get_all_themes()
        test16 = test_get_themes_by_type()
        test17 = test_get_themes_by_category()
        test18 = test_create_custom_theme()
        test19 = test_update_theme_colors()
        test20 = test_update_theme_settings()
        test21 = test_update_config()
        test22 = test_get_config()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"ThemeType Enum: {'PASS' if test1 else 'FAIL'}")
        print(f"ThemeCategory Enum: {'PASS' if test2 else 'FAIL'}")
        print(f"ThemeColors Dataclass: {'PASS' if test3 else 'FAIL'}")
        print(f"ThemeSettings Dataclass: {'PASS' if test4 else 'FAIL'}")
        print(f"Theme Dataclass: {'PASS' if test5 else 'FAIL'}")
        print(f"ThemeConfig Dataclass: {'PASS' if test6 else 'FAIL'}")
        print(f"ThemeManager Initialization: {'PASS' if test7 else 'FAIL'}")
        print(f"Get Theme: {'PASS' if test8 else 'FAIL'}")
        print(f"Get Current Theme: {'PASS' if test9 else 'FAIL'}")
        print(f"Set Theme: {'PASS' if test10 else 'FAIL'}")
        print(f"Switch Theme Type: {'PASS' if test11 else 'FAIL'}")
        print(f"Toggle Dark/Light: {'PASS' if test12 else 'FAIL'}")
        print(f"Add Custom Theme: {'PASS' if test13 else 'FAIL'}")
        print(f"Remove Theme: {'PASS' if test14 else 'FAIL'}")
        print(f"Get All Themes: {'PASS' if test15 else 'FAIL'}")
        print(f"Get Themes by Type: {'PASS' if test16 else 'FAIL'}")
        print(f"Get Themes by Category: {'PASS' if test17 else 'FAIL'}")
        print(f"Create Custom Theme: {'PASS' if test18 else 'FAIL'}")
        print(f"Update Theme Colors: {'PASS' if test19 else 'FAIL'}")
        print(f"Update Theme Settings: {'PASS' if test20 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test21 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test22 else 'FAIL'}")
        
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
