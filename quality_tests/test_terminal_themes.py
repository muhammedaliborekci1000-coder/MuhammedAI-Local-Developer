"""
Quality Test: Terminal Themes
Terminal themes system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.tools.terminal_themes import (
    TerminalThemesEngine,
    ThemeType,
    ThemeScope,
    ThemeAction,
    ThemeConfig,
    ColorPalette,
    ThemeEntry,
    ThemeResult
)


def create_default_palette():
    """Create default color palette for testing."""
    return ColorPalette(
        background="#000000",
        foreground="#ffffff",
        cursor="#ffffff",
        selection="#ffffff",
        black="#000000",
        red="#ff0000",
        green="#00ff00",
        yellow="#ffff00",
        blue="#0000ff",
        magenta="#ff00ff",
        cyan="#00ffff",
        white="#ffffff",
        bright_black="#000000",
        bright_red="#ff0000",
        bright_green="#00ff00",
        bright_yellow="#ffff00",
        bright_blue="#0000ff",
        bright_magenta="#ff00ff",
        bright_cyan="#00ffff",
        bright_white="#ffffff"
    )


def test_create_theme():
    """
    Test: Create theme.
    """
    print("=" * 70)
    print("TEST: Create Theme")
    print("=" * 70)
    
    engine = TerminalThemesEngine()
    palette = create_default_palette()
    result = engine.create_theme("Dark", ThemeType.DARK, palette)
    
    assert result.success, "Oluşturma başarılı olmalı"
    assert result.theme_name == "Dark", "Tema adı eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Theme ID: {result.theme_id}")
    print(f"  Theme name: {result.theme_name}")
    
    print("\n" + "=" * 70)
    print("PASS: Create theme")
    print("=" * 70)


def test_create_theme_with_options():
    """
    Test: Create theme with options.
    """
    print("=" * 70)
    print("TEST: Create Theme With Options")
    print("=" * 70)
    
    engine = TerminalThemesEngine()
    palette = create_default_palette()
    
    result = engine.create_theme(
        "Custom",
        ThemeType.CUSTOM,
        palette,
        font_family="monospace",
        font_size=14,
        font_weight="bold",
        line_height=1.5,
        letter_spacing=0.5,
        cursor_style="block",
        cursor_blink=True,
        transparency=0.9,
        blur=10.0
    )
    
    assert result.success, "Oluşturma başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Theme ID: {result.theme_id}")
    
    print("\n" + "=" * 70)
    print("PASS: Create theme with options")
    print("=" * 70)


def test_update_theme():
    """
    Test: Update theme.
    """
    print("=" * 70)
    print("TEST: Update Theme")
    print("=" * 70)
    
    engine = TerminalThemesEngine()
    palette = create_default_palette()
    result = engine.create_theme("Dark", ThemeType.DARK, palette)
    theme_id = result.theme_id
    
    result = engine.update_theme(theme_id, name="Updated", font_size=16)
    
    assert result.success, "Güncelleme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Update theme")
    print("=" * 70)


def test_delete_theme():
    """
    Test: Delete theme.
    """
    print("=" * 70)
    print("TEST: Delete Theme")
    print("=" * 70)
    
    engine = TerminalThemesEngine()
    palette = create_default_palette()
    result = engine.create_theme("Dark", ThemeType.DARK, palette)
    theme_id = result.theme_id
    
    result = engine.delete_theme(theme_id)
    
    assert result.success, "Silme başarılı olmalı"
    assert theme_id not in engine.themes, "Tema silinmiş olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Delete theme")
    print("=" * 70)


def test_get_theme():
    """
    Test: Get theme.
    """
    print("=" * 70)
    print("TEST: Get Theme")
    print("=" * 70)
    
    engine = TerminalThemesEngine()
    palette = create_default_palette()
    result = engine.create_theme("Dark", ThemeType.DARK, palette)
    theme_id = result.theme_id
    
    result = engine.get_theme(theme_id)
    
    assert result.success, "Alma başarılı olmalı"
    assert result.theme_name == "Dark", "Tema adı eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Theme name: {result.theme_name}")
    
    print("\n" + "=" * 70)
    print("PASS: Get theme")
    print("=" * 70)


def test_list_themes():
    """
    Test: List themes.
    """
    print("=" * 70)
    print("TEST: List Themes")
    print("=" * 70)
    
    engine = TerminalThemesEngine()
    palette = create_default_palette()
    engine.create_theme("Theme1", ThemeType.DARK, palette)
    engine.create_theme("Theme2", ThemeType.LIGHT, palette)
    
    result = engine.list_themes()
    
    assert result.success, "Listeleme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: List themes")
    print("=" * 70)


def test_list_themes_with_scope():
    """
    Test: List themes with scope.
    """
    print("=" * 70)
    print("TEST: List Themes With Scope")
    print("=" * 70)
    
    engine = TerminalThemesEngine()
    palette = create_default_palette()
    engine.create_theme("Theme1", ThemeType.DARK, palette, scope=ThemeScope.GLOBAL)
    engine.create_theme("Theme2", ThemeType.LIGHT, palette, scope=ThemeScope.SESSION)
    
    result = engine.list_themes(scope=ThemeScope.GLOBAL)
    
    assert result.success, "Listeleme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: List themes with scope")
    print("=" * 70)


def test_activate_theme():
    """
    Test: Activate theme.
    """
    print("=" * 70)
    print("TEST: Activate Theme")
    print("=" * 70)
    
    engine = TerminalThemesEngine()
    palette = create_default_palette()
    result = engine.create_theme("Dark", ThemeType.DARK, palette)
    theme_id = result.theme_id
    
    result = engine.activate_theme(theme_id)
    
    assert result.success, "Aktifleştirme başarılı olmalı"
    assert engine.themes[theme_id].is_active, "Tema aktif olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Activate theme")
    print("=" * 70)


def test_clone_theme():
    """
    Test: Clone theme.
    """
    print("=" * 70)
    print("TEST: Clone Theme")
    print("=" * 70)
    
    engine = TerminalThemesEngine()
    palette = create_default_palette()
    result = engine.create_theme("Dark", ThemeType.DARK, palette)
    theme_id = result.theme_id
    
    result = engine.clone_theme(theme_id, "Cloned")
    
    assert result.success, "Klonlama başarılı olmalı"
    assert result.theme_name == "Cloned", "Yeni ad eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  New theme ID: {result.theme_id}")
    print(f"  New theme name: {result.theme_name}")
    
    print("\n" + "=" * 70)
    print("PASS: Clone theme")
    print("=" * 70)


def test_export_theme():
    """
    Test: Export theme.
    """
    print("=" * 70)
    print("TEST: Export Theme")
    print("=" * 70)
    
    engine = TerminalThemesEngine()
    palette = create_default_palette()
    result = engine.create_theme("Dark", ThemeType.DARK, palette)
    theme_id = result.theme_id
    
    result = engine.export_theme(theme_id, format="json")
    
    assert result.success, "Dışa aktarma başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Export theme")
    print("=" * 70)


def test_import_theme():
    """
    Test: Import theme.
    """
    print("=" * 70)
    print("TEST: Import Theme")
    print("=" * 70)
    
    engine = TerminalThemesEngine()
    
    data = {
        "name": "Imported",
        "theme_type": "dark",
        "color_palette": {
            "background": "#000000",
            "foreground": "#ffffff",
            "cursor": "#ffffff",
            "selection": "#ffffff",
            "black": "#000000",
            "red": "#ff0000",
            "green": "#00ff00",
            "yellow": "#ffff00",
            "blue": "#0000ff",
            "magenta": "#ff00ff",
            "cyan": "#00ffff",
            "white": "#ffffff",
            "bright_black": "#000000",
            "bright_red": "#ff0000",
            "bright_green": "#00ff00",
            "bright_yellow": "#ffff00",
            "bright_blue": "#0000ff",
            "bright_magenta": "#ff00ff",
            "bright_cyan": "#00ffff",
            "bright_white": "#ffffff"
        },
        "font_family": "monospace",
        "font_size": 14
    }
    
    result = engine.import_theme(data)
    
    assert result.success, "İçe aktarma başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Import theme")
    print("=" * 70)


def test_set_default_theme():
    """
    Test: Set default theme.
    """
    print("=" * 70)
    print("TEST: Set Default Theme")
    print("=" * 70)
    
    engine = TerminalThemesEngine()
    palette = create_default_palette()
    result = engine.create_theme("Dark", ThemeType.DARK, palette)
    theme_id = result.theme_id
    
    result = engine.set_default_theme(theme_id)
    
    assert result.success, "Ayarlama başarılı olmalı"
    assert engine.themes[theme_id].is_default, "Tema varsayılan olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set default theme")
    print("=" * 70)


def test_get_theme_history():
    """
    Test: Get theme history.
    """
    print("=" * 70)
    print("TEST: Get Theme History")
    print("=" * 70)
    
    engine = TerminalThemesEngine()
    palette = create_default_palette()
    engine.create_theme("Dark", ThemeType.DARK, palette)
    
    history = engine.get_theme_history()
    
    assert len(history) > 0, "Geçmiş olmalı"
    
    print(f"  History: {len(history)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get theme history")
    print("=" * 70)


def test_clear_history():
    """
    Test: Clear history.
    """
    print("=" * 70)
    print("TEST: Clear History")
    print("=" * 70)
    
    engine = TerminalThemesEngine()
    palette = create_default_palette()
    engine.create_theme("Dark", ThemeType.DARK, palette)
    
    result = engine.clear_history()
    
    assert result.success, "Temizleme başarılı olmalı"
    assert len(engine.get_theme_history()) == 0, "Geçmiş temizlenmeli"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear history")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    engine = TerminalThemesEngine()
    
    new_config = ThemeConfig(persist_themes=False)
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
    
    engine = TerminalThemesEngine()
    
    config = engine.get_config()
    
    assert config is not None, "Config olmalı"
    assert config.persist_themes == True, "Config eşleşmeli"
    
    print(f"  Persist themes: {config.persist_themes}")
    print(f"  Auto load themes: {config.auto_load_themes}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


def test_theme_type_enum():
    """
    Test: ThemeType enum.
    """
    print("=" * 70)
    print("TEST: ThemeType Enum")
    print("=" * 70)
    
    assert ThemeType.DARK.value == "dark"
    assert ThemeType.LIGHT.value == "light"
    assert ThemeType.HIGH_CONTRAST.value == "high_contrast"
    assert ThemeType.CUSTOM.value == "custom"
    
    print(f"  All enum values verified")
    print(f"  Total theme types: {len(ThemeType)}")
    
    print("\n" + "=" * 70)
    print("PASS: ThemeType enum")
    print("=" * 70)


def test_theme_scope_enum():
    """
    Test: ThemeScope enum.
    """
    print("=" * 70)
    print("TEST: ThemeScope Enum")
    print("=" * 70)
    
    assert ThemeScope.SESSION.value == "session"
    assert ThemeScope.TERMINAL.value == "terminal"
    assert ThemeScope.GLOBAL.value == "global"
    
    print(f"  All enum values verified")
    print(f"  Total scopes: {len(ThemeScope)}")
    
    print("\n" + "=" * 70)
    print("PASS: ThemeScope enum")
    print("=" * 70)


def test_theme_action_enum():
    """
    Test: ThemeAction enum.
    """
    print("=" * 70)
    print("TEST: ThemeAction Enum")
    print("=" * 70)
    
    assert ThemeAction.CREATE.value == "create"
    assert ThemeAction.UPDATE.value == "update"
    assert ThemeAction.DELETE.value == "delete"
    assert ThemeAction.GET.value == "get"
    assert ThemeAction.LIST.value == "list"
    assert ThemeAction.ACTIVATE.value == "activate"
    assert ThemeAction.CLONE.value == "clone"
    assert ThemeAction.IMPORT.value == "import"
    assert ThemeAction.EXPORT.value == "export"
    assert ThemeAction.SET_DEFAULT.value == "set_default"
    
    print(f"  All enum values verified")
    print(f"  Total actions: {len(ThemeAction)}")
    
    print("\n" + "=" * 70)
    print("PASS: ThemeAction enum")
    print("=" * 70)


def test_theme_config_dataclass():
    """
    Test: ThemeConfig dataclass.
    """
    print("=" * 70)
    print("TEST: ThemeConfig Dataclass")
    print("=" * 70)
    
    config = ThemeConfig(
        persist_themes=False,
        auto_load_themes=False
    )
    
    assert config.persist_themes == False, "Persist eşleşmeli"
    assert config.auto_load_themes == False, "Auto load eşleşmeli"
    
    print(f"  Persist themes: {config.persist_themes}")
    print(f"  Auto load themes: {config.auto_load_themes}")
    
    print("\n" + "=" * 70)
    print("PASS: ThemeConfig dataclass")
    print("=" * 70)


def test_color_palette_dataclass():
    """
    Test: ColorPalette dataclass.
    """
    print("=" * 70)
    print("TEST: ColorPalette Dataclass")
    print("=" * 70)
    
    palette = ColorPalette(
        background="#000000",
        foreground="#ffffff",
        cursor="#ffffff",
        selection="#ffffff",
        black="#000000",
        red="#ff0000",
        green="#00ff00",
        yellow="#ffff00",
        blue="#0000ff",
        magenta="#ff00ff",
        cyan="#00ffff",
        white="#ffffff",
        bright_black="#000000",
        bright_red="#ff0000",
        bright_green="#00ff00",
        bright_yellow="#ffff00",
        bright_blue="#0000ff",
        bright_magenta="#ff00ff",
        bright_cyan="#00ffff",
        bright_white="#ffffff"
    )
    
    assert palette.background == "#000000", "Background eşleşmeli"
    assert palette.foreground == "#ffffff", "Foreground eşleşmeli"
    
    print(f"  Background: {palette.background}")
    print(f"  Foreground: {palette.foreground}")
    
    print("\n" + "=" * 70)
    print("PASS: ColorPalette dataclass")
    print("=" * 70)


def test_theme_entry_dataclass():
    """
    Test: ThemeEntry dataclass.
    """
    print("=" * 70)
    print("TEST: ThemeEntry Dataclass")
    print("=" * 70)
    
    palette = create_default_palette()
    
    entry = ThemeEntry(
        id="theme_1",
        name="Dark",
        theme_type=ThemeType.DARK,
        color_palette=palette,
        timestamp="2024-01-01T00:00:00"
    )
    
    assert entry.id == "theme_1", "ID eşleşmeli"
    assert entry.name == "Dark", "Ad eşleşmeli"
    
    print(f"  ID: {entry.id}")
    print(f"  Name: {entry.name}")
    
    print("\n" + "=" * 70)
    print("PASS: ThemeEntry dataclass")
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
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: ThemeResult dataclass")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_create_theme()
        test2 = test_create_theme_with_options()
        test3 = test_update_theme()
        test4 = test_delete_theme()
        test5 = test_get_theme()
        test6 = test_list_themes()
        test7 = test_list_themes_with_scope()
        test8 = test_activate_theme()
        test9 = test_clone_theme()
        test10 = test_export_theme()
        test11 = test_import_theme()
        test12 = test_set_default_theme()
        test13 = test_get_theme_history()
        test14 = test_clear_history()
        test15 = test_update_config()
        test16 = test_get_config()
        test17 = test_theme_type_enum()
        test18 = test_theme_scope_enum()
        test19 = test_theme_action_enum()
        test20 = test_theme_config_dataclass()
        test21 = test_color_palette_dataclass()
        test22 = test_theme_entry_dataclass()
        test23 = test_theme_result_dataclass()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Create Theme: {'PASS' if test1 else 'FAIL'}")
        print(f"Create Theme With Options: {'PASS' if test2 else 'FAIL'}")
        print(f"Update Theme: {'PASS' if test3 else 'FAIL'}")
        print(f"Delete Theme: {'PASS' if test4 else 'FAIL'}")
        print(f"Get Theme: {'PASS' if test5 else 'FAIL'}")
        print(f"List Themes: {'PASS' if test6 else 'FAIL'}")
        print(f"List Themes With Scope: {'PASS' if test7 else 'FAIL'}")
        print(f"Activate Theme: {'PASS' if test8 else 'FAIL'}")
        print(f"Clone Theme: {'PASS' if test9 else 'FAIL'}")
        print(f"Export Theme: {'PASS' if test10 else 'FAIL'}")
        print(f"Import Theme: {'PASS' if test11 else 'FAIL'}")
        print(f"Set Default Theme: {'PASS' if test12 else 'FAIL'}")
        print(f"Get Theme History: {'PASS' if test13 else 'FAIL'}")
        print(f"Clear History: {'PASS' if test14 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test15 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test16 else 'FAIL'}")
        print(f"ThemeType Enum: {'PASS' if test17 else 'FAIL'}")
        print(f"ThemeScope Enum: {'PASS' if test18 else 'FAIL'}")
        print(f"ThemeAction Enum: {'PASS' if test19 else 'FAIL'}")
        print(f"ThemeConfig Dataclass: {'PASS' if test20 else 'FAIL'}")
        print(f"ColorPalette Dataclass: {'PASS' if test21 else 'FAIL'}")
        print(f"ThemeEntry Dataclass: {'PASS' if test22 else 'FAIL'}")
        print(f"ThemeResult Dataclass: {'PASS' if test23 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14, test15, test16, test17, test18, test19, test20, test21, test22, test23])
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
