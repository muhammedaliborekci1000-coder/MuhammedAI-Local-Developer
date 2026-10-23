"""
Quality Test: Settings Panel
Settings panel system testleri for UI module.
"""

import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from app.ui.settings_panel import (
    SettingType,
    SettingCategory,
    SettingOption,
    Setting,
    SettingsPanelConfig,
    SettingsPanelResult,
    SettingsPanelManager
)


def test_setting_type_enum():
    """
    Test: SettingType enum.
    """
    print("=" * 70)
    print("TEST: SettingType Enum")
    print("=" * 70)
    
    assert SettingType.BOOLEAN.value == "boolean"
    assert SettingType.STRING.value == "string"
    assert SettingType.NUMBER.value == "number"
    assert SettingType.INTEGER.value == "integer"
    assert SettingType.SELECT.value == "select"
    assert SettingType.MULTI_SELECT.value == "multi_select"
    assert SettingType.COLOR.value == "color"
    assert SettingType.PATH.value == "path"
    assert SettingType.HOTKEY.value == "hotkey"
    assert SettingType.CUSTOM.value == "custom"
    
    print(f"  All enum values verified")
    print(f"  Total types: {len(SettingType)}")
    
    print("\n" + "=" * 70)
    print("PASS: SettingType enum")
    print("=" * 70)


def test_setting_category_enum():
    """
    Test: SettingCategory enum.
    """
    print("=" * 70)
    print("TEST: SettingCategory Enum")
    print("=" * 70)
    
    assert SettingCategory.GENERAL.value == "general"
    assert SettingCategory.EDITOR.value == "editor"
    assert SettingCategory.THEME.value == "theme"
    assert SettingCategory.KEYBINDINGS.value == "keybindings"
    assert SettingCategory.TERMINAL.value == "terminal"
    assert SettingCategory.GIT.value == "git"
    assert SettingCategory.AI.value == "ai"
    assert SettingCategory.SECURITY.value == "security"
    assert SettingCategory.ADVANCED.value == "advanced"
    assert SettingCategory.CUSTOM.value == "custom"
    
    print(f"  All enum values verified")
    print(f"  Total categories: {len(SettingCategory)}")
    
    print("\n" + "=" * 70)
    print("PASS: SettingCategory enum")
    print("=" * 70)


def test_setting_option_dataclass():
    """
    Test: SettingOption dataclass.
    """
    print("=" * 70)
    print("TEST: SettingOption Dataclass")
    print("=" * 70)
    
    option = SettingOption(
        value="option1",
        label="Option 1",
        description="First option"
    )
    
    assert option.value == "option1", "Value eşleşmeli"
    assert option.label == "Option 1", "Label eşleşmeli"
    
    print(f"  Value: {option.value}")
    print(f"  Label: {option.label}")
    
    print("\n" + "=" * 70)
    print("PASS: SettingOption dataclass")
    print("=" * 70)


def test_setting_dataclass():
    """
    Test: Setting dataclass.
    """
    print("=" * 70)
    print("TEST: Setting Dataclass")
    print("=" * 70)
    
    setting = Setting(
        id="setting_1",
        type=SettingType.BOOLEAN,
        category=SettingCategory.GENERAL,
        key="auto_save",
        label="Auto Save",
        default_value=True,
        current_value=True
    )
    
    assert setting.id == "setting_1", "ID eşleşmeli"
    assert setting.type == SettingType.BOOLEAN, "Type eşleşmeli"
    assert setting.key == "auto_save", "Key eşleşmeli"
    assert setting.label == "Auto Save", "Label eşleşmeli"
    
    print(f"  ID: {setting.id}")
    print(f"  Type: {setting.type.value}")
    print(f"  Key: {setting.key}")
    print(f"  Label: {setting.label}")
    
    print("\n" + "=" * 70)
    print("PASS: Setting dataclass")
    print("=" * 70)


def test_settings_panel_config_dataclass():
    """
    Test: SettingsPanelConfig dataclass.
    """
    print("=" * 70)
    print("TEST: SettingsPanelConfig Dataclass")
    print("=" * 70)
    
    config = SettingsPanelConfig(
        enabled=True,
        show_categories=True
    )
    
    assert config.enabled == True, "Enabled eşleşmeli"
    assert config.show_categories == True, "Show categories eşleşmeli"
    
    print(f"  Enabled: {config.enabled}")
    print(f"  Show categories: {config.show_categories}")
    
    print("\n" + "=" * 70)
    print("PASS: SettingsPanelConfig dataclass")
    print("=" * 70)


def test_settings_panel_result_dataclass():
    """
    Test: SettingsPanelResult dataclass.
    """
    print("=" * 70)
    print("TEST: SettingsPanelResult Dataclass")
    print("=" * 70)
    
    result = SettingsPanelResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.settings, list), "Settings list olmalı"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Settings: {len(result.settings)}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: SettingsPanelResult dataclass")
    print("=" * 70)


def test_settings_panel_manager_initialization():
    """
    Test: SettingsPanelManager initialization.
    """
    print("=" * 70)
    print("TEST: SettingsPanelManager Initialization")
    print("=" * 70)
    
    config = SettingsPanelConfig()
    manager = SettingsPanelManager(config)
    
    assert manager.config == config, "Config eşleşmeli"
    assert len(manager.settings) == 0, "Settings boş olmalı"
    
    print(f"  Settings: {len(manager.settings)}")
    
    print("\n" + "=" * 70)
    print("PASS: SettingsPanelManager initialization")
    print("=" * 70)


def test_add_setting():
    """
    Test: Add setting.
    """
    print("=" * 70)
    print("TEST: Add Setting")
    print("=" * 70)
    
    manager = SettingsPanelManager()
    
    setting = Setting(
        id="",
        type=SettingType.BOOLEAN,
        category=SettingCategory.GENERAL,
        key="auto_save",
        label="Auto Save",
        default_value=True,
        current_value=True
    )
    
    result = manager.add_setting(setting)
    
    assert result.success == True, "Ekleme başarılı olmalı"
    assert len(manager.settings) > 0, "Setting eklenmeli"
    
    print(f"  Setting added: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add setting")
    print("=" * 70)


def test_remove_setting():
    """
    Test: Remove setting.
    """
    print("=" * 70)
    print("TEST: Remove Setting")
    print("=" * 70)
    
    manager = SettingsPanelManager()
    
    setting = Setting(
        id="",
        type=SettingType.BOOLEAN,
        category=SettingCategory.GENERAL,
        key="auto_save",
        label="Auto Save",
        default_value=True,
        current_value=True
    )
    
    result = manager.add_setting(setting)
    setting_id = result.setting.id
    
    result = manager.remove_setting(setting_id)
    
    assert result.success == True, "Kaldırma başarılı olmalı"
    assert setting_id not in manager.settings, "Setting silinmeli"
    
    print(f"  Setting removed: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Remove setting")
    print("=" * 70)


def test_get_setting():
    """
    Test: Get setting.
    """
    print("=" * 70)
    print("TEST: Get Setting")
    print("=" * 70)
    
    manager = SettingsPanelManager()
    
    setting = Setting(
        id="",
        type=SettingType.BOOLEAN,
        category=SettingCategory.GENERAL,
        key="auto_save",
        label="Auto Save",
        default_value=True,
        current_value=True
    )
    
    result = manager.add_setting(setting)
    setting_id = result.setting.id
    
    retrieved_setting = manager.get_setting(setting_id)
    
    assert retrieved_setting is not None, "Setting bulunmalı"
    assert retrieved_setting.id == setting_id, "ID eşleşmeli"
    
    print(f"  Setting: {retrieved_setting.label}")
    
    print("\n" + "=" * 70)
    print("PASS: Get setting")
    print("=" * 70)


def test_get_all_settings():
    """
    Test: Get all settings.
    """
    print("=" * 70)
    print("TEST: Get All Settings")
    print("=" * 70)
    
    manager = SettingsPanelManager()
    
    setting = Setting(
        id="",
        type=SettingType.BOOLEAN,
        category=SettingCategory.GENERAL,
        key="auto_save",
        label="Auto Save",
        default_value=True,
        current_value=True
    )
    
    manager.add_setting(setting)
    settings = manager.get_all_settings()
    
    assert len(settings) > 0, "Settings olmalı"
    
    print(f"  Total settings: {len(settings)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get all settings")
    print("=" * 70)


def test_get_settings_by_category():
    """
    Test: Get settings by category.
    """
    print("=" * 70)
    print("TEST: Get Settings by Category")
    print("=" * 70)
    
    manager = SettingsPanelManager()
    
    setting = Setting(
        id="",
        type=SettingType.BOOLEAN,
        category=SettingCategory.GENERAL,
        key="auto_save",
        label="Auto Save",
        default_value=True,
        current_value=True
    )
    
    manager.add_setting(setting)
    settings = manager.get_settings_by_category(SettingCategory.GENERAL)
    
    assert len(settings) > 0, "General settings olmalı"
    
    print(f"  General settings: {len(settings)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get settings by category")
    print("=" * 70)


def test_get_settings_by_type():
    """
    Test: Get settings by type.
    """
    print("=" * 70)
    print("TEST: Get Settings by Type")
    print("=" * 70)
    
    manager = SettingsPanelManager()
    
    setting = Setting(
        id="",
        type=SettingType.BOOLEAN,
        category=SettingCategory.GENERAL,
        key="auto_save",
        label="Auto Save",
        default_value=True,
        current_value=True
    )
    
    manager.add_setting(setting)
    settings = manager.get_settings_by_type(SettingType.BOOLEAN)
    
    assert len(settings) > 0, "Boolean settings olmalı"
    
    print(f"  Boolean settings: {len(settings)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get settings by type")
    print("=" * 70)


def test_update_setting_value():
    """
    Test: Update setting value.
    """
    print("=" * 70)
    print("TEST: Update Setting Value")
    print("=" * 70)
    
    manager = SettingsPanelManager()
    
    result = manager.add_boolean_setting(SettingCategory.GENERAL, "auto_save", "Auto Save", True)
    setting_id = result.setting.id
    
    result = manager.update_setting_value(setting_id, False)
    
    assert result.success == True, "Update başarılı olmalı"
    
    print(f"  Setting updated: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Update setting value")
    print("=" * 70)


def test_reset_setting_to_default():
    """
    Test: Reset setting to default.
    """
    print("=" * 70)
    print("TEST: Reset Setting to Default")
    print("=" * 70)
    
    manager = SettingsPanelManager()
    
    result = manager.add_boolean_setting(SettingCategory.GENERAL, "auto_save", "Auto Save", True)
    setting_id = result.setting.id
    
    manager.update_setting_value(setting_id, False)
    result = manager.reset_setting_to_default(setting_id)
    
    assert result.success == True, "Reset başarılı olmalı"
    
    print(f"  Setting reset: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Reset setting to default")
    print("=" * 70)


def test_reset_all_to_defaults():
    """
    Test: Reset all to defaults.
    """
    print("=" * 70)
    print("TEST: Reset All to Defaults")
    print("=" * 70)
    
    manager = SettingsPanelManager()
    
    manager.add_boolean_setting(SettingCategory.GENERAL, "auto_save", "Auto Save", True)
    
    result = manager.reset_all_to_defaults()
    
    assert result.success == True, "Reset başarılı olmalı"
    
    print(f"  All reset: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Reset all to defaults")
    print("=" * 70)


def test_add_boolean_setting():
    """
    Test: Add boolean setting.
    """
    print("=" * 70)
    print("TEST: Add Boolean Setting")
    print("=" * 70)
    
    manager = SettingsPanelManager()
    
    result = manager.add_boolean_setting(SettingCategory.GENERAL, "auto_save", "Auto Save", True, "Auto save files")
    
    assert result.success == True, "Boolean setting başarılı olmalı"
    
    print(f"  Boolean setting: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add boolean setting")
    print("=" * 70)


def test_add_string_setting():
    """
    Test: Add string setting.
    """
    print("=" * 70)
    print("TEST: Add String Setting")
    print("=" * 70)
    
    manager = SettingsPanelManager()
    
    result = manager.add_string_setting(SettingCategory.EDITOR, "font_family", "Font Family", "Arial", "Editor font")
    
    assert result.success == True, "String setting başarılı olmalı"
    
    print(f"  String setting: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add string setting")
    print("=" * 70)


def test_add_number_setting():
    """
    Test: Add number setting.
    """
    print("=" * 70)
    print("TEST: Add Number Setting")
    print("=" * 70)
    
    manager = SettingsPanelManager()
    
    result = manager.add_number_setting(SettingCategory.EDITOR, "font_size", "Font Size", 14.0, 8.0, 72.0, "Editor font size")
    
    assert result.success == True, "Number setting başarılı olmalı"
    
    print(f"  Number setting: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add number setting")
    print("=" * 70)


def test_add_select_setting():
    """
    Test: Add select setting.
    """
    print("=" * 70)
    print("TEST: Add Select Setting")
    print("=" * 70)
    
    manager = SettingsPanelManager()
    
    options = [SettingOption("light", "Light"), SettingOption("dark", "Dark")]
    result = manager.add_select_setting(SettingCategory.THEME, "theme", "Theme", "light", options, "Editor theme")
    
    assert result.success == True, "Select setting başarılı olmalı"
    
    print(f"  Select setting: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add select setting")
    print("=" * 70)


def test_add_color_setting():
    """
    Test: Add color setting.
    """
    print("=" * 70)
    print("TEST: Add Color Setting")
    print("=" * 70)
    
    manager = SettingsPanelManager()
    
    result = manager.add_color_setting(SettingCategory.THEME, "accent_color", "Accent Color", "#007acc", "Accent color")
    
    assert result.success == True, "Color setting başarılı olmalı"
    
    print(f"  Color setting: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add color setting")
    print("=" * 70)


def test_add_hotkey_setting():
    """
    Test: Add hotkey setting.
    """
    print("=" * 70)
    print("TEST: Add Hotkey Setting")
    print("=" * 70)
    
    manager = SettingsPanelManager()
    
    result = manager.add_hotkey_setting(SettingCategory.KEYBINDINGS, "save", "Save", "Ctrl+S", "Save file")
    
    assert result.success == True, "Hotkey setting başarılı olmalı"
    
    print(f"  Hotkey setting: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add hotkey setting")
    print("=" * 70)


def test_export_settings():
    """
    Test: Export settings.
    """
    print("=" * 70)
    print("TEST: Export Settings")
    print("=" * 70)
    
    manager = SettingsPanelManager()
    
    manager.add_boolean_setting(SettingCategory.GENERAL, "auto_save", "Auto Save", True)
    
    settings_dict = manager.export_settings()
    
    assert isinstance(settings_dict, dict), "Dictionary olmalı"
    assert "auto_save" in settings_dict, "auto_save olmalı"
    
    print(f"  Exported: {len(settings_dict)} settings")
    
    print("\n" + "=" * 70)
    print("PASS: Export settings")
    print("=" * 70)


def test_import_settings():
    """
    Test: Import settings.
    """
    print("=" * 70)
    print("TEST: Import Settings")
    print("=" * 70)
    
    manager = SettingsPanelManager()
    
    manager.add_boolean_setting(SettingCategory.GENERAL, "auto_save", "Auto Save", True)
    
    settings_dict = {"auto_save": False}
    result = manager.import_settings(settings_dict)
    
    assert result.success == True, "Import başarılı olmalı"
    
    print(f"  Imported: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Import settings")
    print("=" * 70)


def test_clear_settings():
    """
    Test: Clear settings.
    """
    print("=" * 70)
    print("TEST: Clear Settings")
    print("=" * 70)
    
    manager = SettingsPanelManager()
    
    manager.add_boolean_setting(SettingCategory.GENERAL, "auto_save", "Auto Save", True)
    
    result = manager.clear_settings()
    
    assert result.success == True, "Clear başarılı olmalı"
    assert len(manager.settings) == 0, "Settings temizlenmeli"
    
    print(f"  Cleared: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear settings")
    print("=" * 70)


def test_set_setting_enabled():
    """
    Test: Set setting enabled.
    """
    print("=" * 70)
    print("TEST: Set Setting Enabled")
    print("=" * 70)
    
    manager = SettingsPanelManager()
    
    result = manager.add_boolean_setting(SettingCategory.GENERAL, "auto_save", "Auto Save", True)
    setting_id = result.setting.id
    
    result = manager.set_setting_enabled(setting_id, False)
    
    assert result.success == True, "Set başarılı olmalı"
    
    print(f"  Setting enabled state: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set setting enabled")
    print("=" * 70)


def test_set_setting_visible():
    """
    Test: Set setting visible.
    """
    print("=" * 70)
    print("TEST: Set Setting Visible")
    print("=" * 70)
    
    manager = SettingsPanelManager()
    
    result = manager.add_boolean_setting(SettingCategory.GENERAL, "auto_save", "Auto Save", True)
    setting_id = result.setting.id
    
    result = manager.set_setting_visible(setting_id, False)
    
    assert result.success == True, "Set başarılı olmalı"
    
    print(f"  Setting visible state: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set setting visible")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    manager = SettingsPanelManager()
    
    new_config = SettingsPanelConfig(max_settings_per_category=100)
    result = manager.update_config(new_config)
    
    assert result.success == True, "Update başarılı olmalı"
    assert manager.config.max_settings_per_category == 100, "Config güncellenmeli"
    
    print(f"  Max settings per category: {manager.config.max_settings_per_category}")
    
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
    
    config = SettingsPanelConfig(max_settings_per_category=100)
    manager = SettingsPanelManager(config)
    
    retrieved_config = manager.get_config()
    
    assert retrieved_config.max_settings_per_category == 100, "Config eşleşmeli"
    
    print(f"  Max settings per category: {retrieved_config.max_settings_per_category}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_setting_type_enum()
        test2 = test_setting_category_enum()
        test3 = test_setting_option_dataclass()
        test4 = test_setting_dataclass()
        test5 = test_settings_panel_config_dataclass()
        test6 = test_settings_panel_result_dataclass()
        test7 = test_settings_panel_manager_initialization()
        test8 = test_add_setting()
        test9 = test_remove_setting()
        test10 = test_get_setting()
        test11 = test_get_all_settings()
        test12 = test_get_settings_by_category()
        test13 = test_get_settings_by_type()
        test14 = test_update_setting_value()
        test15 = test_reset_setting_to_default()
        test16 = test_reset_all_to_defaults()
        test17 = test_add_boolean_setting()
        test18 = test_add_string_setting()
        test19 = test_add_number_setting()
        test20 = test_add_select_setting()
        test21 = test_add_color_setting()
        test22 = test_add_hotkey_setting()
        test23 = test_export_settings()
        test24 = test_import_settings()
        test25 = test_clear_settings()
        test26 = test_set_setting_enabled()
        test27 = test_set_setting_visible()
        test28 = test_update_config()
        test29 = test_get_config()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"SettingType Enum: {'PASS' if test1 else 'FAIL'}")
        print(f"SettingCategory Enum: {'PASS' if test2 else 'FAIL'}")
        print(f"SettingOption Dataclass: {'PASS' if test3 else 'FAIL'}")
        print(f"Setting Dataclass: {'PASS' if test4 else 'FAIL'}")
        print(f"SettingsPanelConfig Dataclass: {'PASS' if test5 else 'FAIL'}")
        print(f"SettingsPanelResult Dataclass: {'PASS' if test6 else 'FAIL'}")
        print(f"SettingsPanelManager Initialization: {'PASS' if test7 else 'FAIL'}")
        print(f"Add Setting: {'PASS' if test8 else 'FAIL'}")
        print(f"Remove Setting: {'PASS' if test9 else 'FAIL'}")
        print(f"Get Setting: {'PASS' if test10 else 'FAIL'}")
        print(f"Get All Settings: {'PASS' if test11 else 'FAIL'}")
        print(f"Get Settings by Category: {'PASS' if test12 else 'FAIL'}")
        print(f"Get Settings by Type: {'PASS' if test13 else 'FAIL'}")
        print(f"Update Setting Value: {'PASS' if test14 else 'FAIL'}")
        print(f"Reset Setting to Default: {'PASS' if test15 else 'FAIL'}")
        print(f"Reset All to Defaults: {'PASS' if test16 else 'FAIL'}")
        print(f"Add Boolean Setting: {'PASS' if test17 else 'FAIL'}")
        print(f"Add String Setting: {'PASS' if test18 else 'FAIL'}")
        print(f"Add Number Setting: {'PASS' if test19 else 'FAIL'}")
        print(f"Add Select Setting: {'PASS' if test20 else 'FAIL'}")
        print(f"Add Color Setting: {'PASS' if test21 else 'FAIL'}")
        print(f"Add Hotkey Setting: {'PASS' if test22 else 'FAIL'}")
        print(f"Export Settings: {'PASS' if test23 else 'FAIL'}")
        print(f"Import Settings: {'PASS' if test24 else 'FAIL'}")
        print(f"Clear Settings: {'PASS' if test25 else 'FAIL'}")
        print(f"Set Setting Enabled: {'PASS' if test26 else 'FAIL'}")
        print(f"Set Setting Visible: {'PASS' if test27 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test28 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test29 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14, test15, test16, test17, test18, test19, test20, test21, test22, test23, test24, test25, test26, test27, test28, test29])
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
