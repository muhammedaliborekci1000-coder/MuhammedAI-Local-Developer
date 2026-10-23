"""
Quality Test: Terminal Font Settings
Terminal font settings system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.tools.terminal_font_settings import (
    TerminalFontSettingsEngine,
    FontWeight,
    FontStyle,
    FontScope,
    FontAction,
    FontConfig,
    FontEntry,
    FontResult
)


def test_create_font_setting():
    """
    Test: Create font setting.
    """
    print("=" * 70)
    print("TEST: Create Font Setting")
    print("=" * 70)
    
    engine = TerminalFontSettingsEngine()
    result = engine.create_font_setting("Default", "monospace", 12)
    
    assert result.success, "Oluşturma başarılı olmalı"
    assert result.font_name == "Default", "Font adı eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Font ID: {result.font_id}")
    print(f"  Font name: {result.font_name}")
    
    print("\n" + "=" * 70)
    print("PASS: Create font setting")
    print("=" * 70)


def test_create_font_setting_with_options():
    """
    Test: Create font setting with options.
    """
    print("=" * 70)
    print("TEST: Create Font Setting With Options")
    print("=" * 70)
    
    engine = TerminalFontSettingsEngine()
    
    result = engine.create_font_setting(
        "Custom",
        "Fira Code",
        14,
        weight=FontWeight.BOLD,
        style=FontStyle.ITALIC,
        line_height=1.5,
        letter_spacing=0.5,
        word_spacing=0.2,
        font_smoothing="grayscale",
        antialiasing=True,
        ligatures=True,
        fallback_fonts=["Consolas", "Courier New"]
    )
    
    assert result.success, "Oluşturma başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Font ID: {result.font_id}")
    
    print("\n" + "=" * 70)
    print("PASS: Create font setting with options")
    print("=" * 70)


def test_update_font_setting():
    """
    Test: Update font setting.
    """
    print("=" * 70)
    print("TEST: Update Font Setting")
    print("=" * 70)
    
    engine = TerminalFontSettingsEngine()
    result = engine.create_font_setting("Default", "monospace", 12)
    font_id = result.font_id
    
    result = engine.update_font_setting(font_id, name="Updated", size=14)
    
    assert result.success, "Güncelleme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Update font setting")
    print("=" * 70)


def test_delete_font_setting():
    """
    Test: Delete font setting.
    """
    print("=" * 70)
    print("TEST: Delete Font Setting")
    print("=" * 70)
    
    engine = TerminalFontSettingsEngine()
    result = engine.create_font_setting("Default", "monospace", 12)
    font_id = result.font_id
    
    result = engine.delete_font_setting(font_id)
    
    assert result.success, "Silme başarılı olmalı"
    assert font_id not in engine.fonts, "Font ayarı silinmiş olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Delete font setting")
    print("=" * 70)


def test_get_font_setting():
    """
    Test: Get font setting.
    """
    print("=" * 70)
    print("TEST: Get Font Setting")
    print("=" * 70)
    
    engine = TerminalFontSettingsEngine()
    result = engine.create_font_setting("Default", "monospace", 12)
    font_id = result.font_id
    
    result = engine.get_font_setting(font_id)
    
    assert result.success, "Alma başarılı olmalı"
    assert result.font_name == "Default", "Font adı eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Font name: {result.font_name}")
    
    print("\n" + "=" * 70)
    print("PASS: Get font setting")
    print("=" * 70)


def test_list_font_settings():
    """
    Test: List font settings.
    """
    print("=" * 70)
    print("TEST: List Font Settings")
    print("=" * 70)
    
    engine = TerminalFontSettingsEngine()
    engine.create_font_setting("Font1", "monospace", 12)
    engine.create_font_setting("Font2", "consolas", 14)
    
    result = engine.list_font_settings()
    
    assert result.success, "Listeleme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: List font settings")
    print("=" * 70)


def test_list_font_settings_with_scope():
    """
    Test: List font settings with scope.
    """
    print("=" * 70)
    print("TEST: List Font Settings With Scope")
    print("=" * 70)
    
    engine = TerminalFontSettingsEngine()
    engine.create_font_setting("Font1", "monospace", 12, scope=FontScope.GLOBAL)
    engine.create_font_setting("Font2", "consolas", 14, scope=FontScope.SESSION)
    
    result = engine.list_font_settings(scope=FontScope.GLOBAL)
    
    assert result.success, "Listeleme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: List font settings with scope")
    print("=" * 70)


def test_activate_font_setting():
    """
    Test: Activate font setting.
    """
    print("=" * 70)
    print("TEST: Activate Font Setting")
    print("=" * 70)
    
    engine = TerminalFontSettingsEngine()
    result = engine.create_font_setting("Default", "monospace", 12)
    font_id = result.font_id
    
    result = engine.activate_font_setting(font_id)
    
    assert result.success, "Aktifleştirme başarılı olmalı"
    assert engine.fonts[font_id].is_active, "Font ayarı aktif olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Activate font setting")
    print("=" * 70)


def test_clone_font_setting():
    """
    Test: Clone font setting.
    """
    print("=" * 70)
    print("TEST: Clone Font Setting")
    print("=" * 70)
    
    engine = TerminalFontSettingsEngine()
    result = engine.create_font_setting("Default", "monospace", 12)
    font_id = result.font_id
    
    result = engine.clone_font_setting(font_id, "Cloned")
    
    assert result.success, "Klonlama başarılı olmalı"
    assert result.font_name == "Cloned", "Yeni ad eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  New font ID: {result.font_id}")
    print(f"  New font name: {result.font_name}")
    
    print("\n" + "=" * 70)
    print("PASS: Clone font setting")
    print("=" * 70)


def test_export_font_setting():
    """
    Test: Export font setting.
    """
    print("=" * 70)
    print("TEST: Export Font Setting")
    print("=" * 70)
    
    engine = TerminalFontSettingsEngine()
    result = engine.create_font_setting("Default", "monospace", 12)
    font_id = result.font_id
    
    result = engine.export_font_setting(font_id, format="json")
    
    assert result.success, "Dışa aktarma başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Export font setting")
    print("=" * 70)


def test_import_font_setting():
    """
    Test: Import font setting.
    """
    print("=" * 70)
    print("TEST: Import Font Setting")
    print("=" * 70)
    
    engine = TerminalFontSettingsEngine()
    
    data = {
        "name": "Imported",
        "family": "Fira Code",
        "size": 14,
        "weight": "bold",
        "style": "italic",
        "line_height": 1.5,
        "letter_spacing": 0.5,
        "word_spacing": 0.2,
        "font_smoothing": "grayscale",
        "antialiasing": True,
        "ligatures": True,
        "fallback_fonts": ["Consolas", "Courier New"]
    }
    
    result = engine.import_font_setting(data)
    
    assert result.success, "İçe aktarma başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Import font setting")
    print("=" * 70)


def test_set_default_font_setting():
    """
    Test: Set default font setting.
    """
    print("=" * 70)
    print("TEST: Set Default Font Setting")
    print("=" * 70)
    
    engine = TerminalFontSettingsEngine()
    result = engine.create_font_setting("Default", "monospace", 12)
    font_id = result.font_id
    
    result = engine.set_default_font_setting(font_id)
    
    assert result.success, "Ayarlama başarılı olmalı"
    assert engine.fonts[font_id].is_default, "Font ayarı varsayılan olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set default font setting")
    print("=" * 70)


def test_reset_font_setting():
    """
    Test: Reset font setting.
    """
    print("=" * 70)
    print("TEST: Reset Font Setting")
    print("=" * 70)
    
    engine = TerminalFontSettingsEngine()
    result = engine.create_font_setting("Default", "monospace", 12)
    font_id = result.font_id
    
    result = engine.reset_font_setting(font_id)
    
    assert result.success, "Sıfırlama başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Reset font setting")
    print("=" * 70)


def test_get_font_history():
    """
    Test: Get font history.
    """
    print("=" * 70)
    print("TEST: Get Font History")
    print("=" * 70)
    
    engine = TerminalFontSettingsEngine()
    engine.create_font_setting("Default", "monospace", 12)
    
    history = engine.get_font_history()
    
    assert len(history) > 0, "Geçmiş olmalı"
    
    print(f"  History: {len(history)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get font history")
    print("=" * 70)


def test_clear_history():
    """
    Test: Clear history.
    """
    print("=" * 70)
    print("TEST: Clear History")
    print("=" * 70)
    
    engine = TerminalFontSettingsEngine()
    engine.create_font_setting("Default", "monospace", 12)
    
    result = engine.clear_history()
    
    assert result.success, "Temizleme başarılı olmalı"
    assert len(engine.get_font_history()) == 0, "Geçmiş temizlenmeli"
    
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
    
    engine = TerminalFontSettingsEngine()
    
    new_config = FontConfig(persist_fonts=False)
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
    
    engine = TerminalFontSettingsEngine()
    
    config = engine.get_config()
    
    assert config is not None, "Config olmalı"
    assert config.persist_fonts == True, "Config eşleşmeli"
    
    print(f"  Persist fonts: {config.persist_fonts}")
    print(f"  Auto load fonts: {config.auto_load_fonts}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


def test_font_weight_enum():
    """
    Test: FontWeight enum.
    """
    print("=" * 70)
    print("TEST: FontWeight Enum")
    print("=" * 70)
    
    assert FontWeight.THIN.value == "thin"
    assert FontWeight.EXTRA_LIGHT.value == "extra_light"
    assert FontWeight.LIGHT.value == "light"
    assert FontWeight.NORMAL.value == "normal"
    assert FontWeight.MEDIUM.value == "medium"
    assert FontWeight.SEMI_BOLD.value == "semi_bold"
    assert FontWeight.BOLD.value == "bold"
    assert FontWeight.EXTRA_BOLD.value == "extra_bold"
    assert FontWeight.BLACK.value == "black"
    
    print(f"  All enum values verified")
    print(f"  Total weights: {len(FontWeight)}")
    
    print("\n" + "=" * 70)
    print("PASS: FontWeight enum")
    print("=" * 70)


def test_font_style_enum():
    """
    Test: FontStyle enum.
    """
    print("=" * 70)
    print("TEST: FontStyle Enum")
    print("=" * 70)
    
    assert FontStyle.NORMAL.value == "normal"
    assert FontStyle.ITALIC.value == "italic"
    assert FontStyle.OBLIQUE.value == "oblique"
    
    print(f"  All enum values verified")
    print(f"  Total styles: {len(FontStyle)}")
    
    print("\n" + "=" * 70)
    print("PASS: FontStyle enum")
    print("=" * 70)


def test_font_scope_enum():
    """
    Test: FontScope enum.
    """
    print("=" * 70)
    print("TEST: FontScope Enum")
    print("=" * 70)
    
    assert FontScope.SESSION.value == "session"
    assert FontScope.TERMINAL.value == "terminal"
    assert FontScope.GLOBAL.value == "global"
    
    print(f"  All enum values verified")
    print(f"  Total scopes: {len(FontScope)}")
    
    print("\n" + "=" * 70)
    print("PASS: FontScope enum")
    print("=" * 70)


def test_font_action_enum():
    """
    Test: FontAction enum.
    """
    print("=" * 70)
    print("TEST: FontAction Enum")
    print("=" * 70)
    
    assert FontAction.CREATE.value == "create"
    assert FontAction.UPDATE.value == "update"
    assert FontAction.DELETE.value == "delete"
    assert FontAction.GET.value == "get"
    assert FontAction.LIST.value == "list"
    assert FontAction.ACTIVATE.value == "activate"
    assert FontAction.CLONE.value == "clone"
    assert FontAction.IMPORT.value == "import"
    assert FontAction.EXPORT.value == "export"
    assert FontAction.SET_DEFAULT.value == "set_default"
    assert FontAction.RESET.value == "reset"
    
    print(f"  All enum values verified")
    print(f"  Total actions: {len(FontAction)}")
    
    print("\n" + "=" * 70)
    print("PASS: FontAction enum")
    print("=" * 70)


def test_font_config_dataclass():
    """
    Test: FontConfig dataclass.
    """
    print("=" * 70)
    print("TEST: FontConfig Dataclass")
    print("=" * 70)
    
    config = FontConfig(
        persist_fonts=False,
        auto_load_fonts=False
    )
    
    assert config.persist_fonts == False, "Persist eşleşmeli"
    assert config.auto_load_fonts == False, "Auto load eşleşmeli"
    
    print(f"  Persist fonts: {config.persist_fonts}")
    print(f"  Auto load fonts: {config.auto_load_fonts}")
    
    print("\n" + "=" * 70)
    print("PASS: FontConfig dataclass")
    print("=" * 70)


def test_font_entry_dataclass():
    """
    Test: FontEntry dataclass.
    """
    print("=" * 70)
    print("TEST: FontEntry Dataclass")
    print("=" * 70)
    
    entry = FontEntry(
        id="font_1",
        name="Default",
        family="monospace",
        size=12,
        weight=FontWeight.NORMAL,
        style=FontStyle.NORMAL,
        line_height=1.0,
        letter_spacing=0.0,
        word_spacing=0.0,
        timestamp="2024-01-01T00:00:00"
    )
    
    assert entry.id == "font_1", "ID eşleşmeli"
    assert entry.name == "Default", "Ad eşleşmeli"
    
    print(f"  ID: {entry.id}")
    print(f"  Name: {entry.name}")
    
    print("\n" + "=" * 70)
    print("PASS: FontEntry dataclass")
    print("=" * 70)


def test_font_result_dataclass():
    """
    Test: FontResult dataclass.
    """
    print("=" * 70)
    print("TEST: FontResult Dataclass")
    print("=" * 70)
    
    result = FontResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: FontResult dataclass")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_create_font_setting()
        test2 = test_create_font_setting_with_options()
        test3 = test_update_font_setting()
        test4 = test_delete_font_setting()
        test5 = test_get_font_setting()
        test6 = test_list_font_settings()
        test7 = test_list_font_settings_with_scope()
        test8 = test_activate_font_setting()
        test9 = test_clone_font_setting()
        test10 = test_export_font_setting()
        test11 = test_import_font_setting()
        test12 = test_set_default_font_setting()
        test13 = test_reset_font_setting()
        test14 = test_get_font_history()
        test15 = test_clear_history()
        test16 = test_update_config()
        test17 = test_get_config()
        test18 = test_font_weight_enum()
        test19 = test_font_style_enum()
        test20 = test_font_scope_enum()
        test21 = test_font_action_enum()
        test22 = test_font_config_dataclass()
        test23 = test_font_entry_dataclass()
        test24 = test_font_result_dataclass()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Create Font Setting: {'PASS' if test1 else 'FAIL'}")
        print(f"Create Font Setting With Options: {'PASS' if test2 else 'FAIL'}")
        print(f"Update Font Setting: {'PASS' if test3 else 'FAIL'}")
        print(f"Delete Font Setting: {'PASS' if test4 else 'FAIL'}")
        print(f"Get Font Setting: {'PASS' if test5 else 'FAIL'}")
        print(f"List Font Settings: {'PASS' if test6 else 'FAIL'}")
        print(f"List Font Settings With Scope: {'PASS' if test7 else 'FAIL'}")
        print(f"Activate Font Setting: {'PASS' if test8 else 'FAIL'}")
        print(f"Clone Font Setting: {'PASS' if test9 else 'FAIL'}")
        print(f"Export Font Setting: {'PASS' if test10 else 'FAIL'}")
        print(f"Import Font Setting: {'PASS' if test11 else 'FAIL'}")
        print(f"Set Default Font Setting: {'PASS' if test12 else 'FAIL'}")
        print(f"Reset Font Setting: {'PASS' if test13 else 'FAIL'}")
        print(f"Get Font History: {'PASS' if test14 else 'FAIL'}")
        print(f"Clear History: {'PASS' if test15 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test16 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test17 else 'FAIL'}")
        print(f"FontWeight Enum: {'PASS' if test18 else 'FAIL'}")
        print(f"FontStyle Enum: {'PASS' if test19 else 'FAIL'}")
        print(f"FontScope Enum: {'PASS' if test20 else 'FAIL'}")
        print(f"FontAction Enum: {'PASS' if test21 else 'FAIL'}")
        print(f"FontConfig Dataclass: {'PASS' if test22 else 'FAIL'}")
        print(f"FontEntry Dataclass: {'PASS' if test23 else 'FAIL'}")
        print(f"FontResult Dataclass: {'PASS' if test24 else 'FAIL'}")
        
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
