"""
Quality Test: Terminal Hyperlinks
Terminal hyperlinks system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.tools.terminal_hyperlinks import (
    TerminalHyperlinksEngine,
    HyperlinkType,
    HyperlinkScope,
    HyperlinkAction,
    HyperlinkConfig,
    HyperlinkEntry,
    HyperlinkResult
)


def test_create_hyperlink():
    """
    Test: Create hyperlink.
    """
    print("=" * 70)
    print("TEST: Create Hyperlink")
    print("=" * 70)
    
    engine = TerminalHyperlinksEngine()
    result = engine.create_hyperlink("Default", url="https://example.com")
    
    assert result.success, "Oluşturma başarılı olmalı"
    assert result.hyperlink_name == "Default", "Hyperlink adı eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Hyperlink ID: {result.hyperlink_id}")
    print(f"  Hyperlink name: {result.hyperlink_name}")
    
    print("\n" + "=" * 70)
    print("PASS: Create hyperlink")
    print("=" * 70)


def test_create_hyperlink_with_options():
    """
    Test: Create hyperlink with options.
    """
    print("=" * 70)
    print("TEST: Create Hyperlink With Options")
    print("=" * 70)
    
    engine = TerminalHyperlinksEngine()
    
    result = engine.create_hyperlink(
        "Custom",
        link_type=HyperlinkType.URL,
        url="https://example.com",
        text="Click here",
        color="#00ff00",
        underline=True,
        hover_color="#ff0000",
        hover_underline=False,
        click_action="open"
    )
    
    assert result.success, "Oluşturma başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Hyperlink ID: {result.hyperlink_id}")
    
    print("\n" + "=" * 70)
    print("PASS: Create hyperlink with options")
    print("=" * 70)


def test_update_hyperlink():
    """
    Test: Update hyperlink.
    """
    print("=" * 70)
    print("TEST: Update Hyperlink")
    print("=" * 70)
    
    engine = TerminalHyperlinksEngine()
    result = engine.create_hyperlink("Default", url="https://example.com")
    hyperlink_id = result.hyperlink_id
    
    result = engine.update_hyperlink(hyperlink_id, name="Updated", url="https://updated.com")
    
    assert result.success, "Güncelleme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Update hyperlink")
    print("=" * 70)


def test_delete_hyperlink():
    """
    Test: Delete hyperlink.
    """
    print("=" * 70)
    print("TEST: Delete Hyperlink")
    print("=" * 70)
    
    engine = TerminalHyperlinksEngine()
    result = engine.create_hyperlink("Default", url="https://example.com")
    hyperlink_id = result.hyperlink_id
    
    result = engine.delete_hyperlink(hyperlink_id)
    
    assert result.success, "Silme başarılı olmalı"
    assert hyperlink_id not in engine.hyperlinks, "Hyperlink silinmiş olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Delete hyperlink")
    print("=" * 70)


def test_get_hyperlink():
    """
    Test: Get hyperlink.
    """
    print("=" * 70)
    print("TEST: Get Hyperlink")
    print("=" * 70)
    
    engine = TerminalHyperlinksEngine()
    result = engine.create_hyperlink("Default", url="https://example.com")
    hyperlink_id = result.hyperlink_id
    
    result = engine.get_hyperlink(hyperlink_id)
    
    assert result.success, "Alma başarılı olmalı"
    assert result.hyperlink_name == "Default", "Hyperlink adı eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Hyperlink name: {result.hyperlink_name}")
    
    print("\n" + "=" * 70)
    print("PASS: Get hyperlink")
    print("=" * 70)


def test_list_hyperlinks():
    """
    Test: List hyperlinks.
    """
    print("=" * 70)
    print("TEST: List Hyperlinks")
    print("=" * 70)
    
    engine = TerminalHyperlinksEngine()
    engine.create_hyperlink("Hyperlink1", url="https://example1.com")
    engine.create_hyperlink("Hyperlink2", url="https://example2.com")
    
    result = engine.list_hyperlinks()
    
    assert result.success, "Listeleme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: List hyperlinks")
    print("=" * 70)


def test_list_hyperlinks_with_scope():
    """
    Test: List hyperlinks with scope.
    """
    print("=" * 70)
    print("TEST: List Hyperlinks With Scope")
    print("=" * 70)
    
    engine = TerminalHyperlinksEngine()
    engine.create_hyperlink("Hyperlink1", url="https://example1.com", scope=HyperlinkScope.GLOBAL)
    engine.create_hyperlink("Hyperlink2", url="https://example2.com", scope=HyperlinkScope.SESSION)
    
    result = engine.list_hyperlinks(scope=HyperlinkScope.GLOBAL)
    
    assert result.success, "Listeleme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: List hyperlinks with scope")
    print("=" * 70)


def test_activate_hyperlink():
    """
    Test: Activate hyperlink.
    """
    print("=" * 70)
    print("TEST: Activate Hyperlink")
    print("=" * 70)
    
    engine = TerminalHyperlinksEngine()
    result = engine.create_hyperlink("Default", url="https://example.com")
    hyperlink_id = result.hyperlink_id
    
    result = engine.activate_hyperlink(hyperlink_id)
    
    assert result.success, "Aktifleştirme başarılı olmalı"
    assert engine.hyperlinks[hyperlink_id].is_active, "Hyperlink aktif olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Activate hyperlink")
    print("=" * 70)


def test_clone_hyperlink():
    """
    Test: Clone hyperlink.
    """
    print("=" * 70)
    print("TEST: Clone Hyperlink")
    print("=" * 70)
    
    engine = TerminalHyperlinksEngine()
    result = engine.create_hyperlink("Default", url="https://example.com")
    hyperlink_id = result.hyperlink_id
    
    result = engine.clone_hyperlink(hyperlink_id, "Cloned")
    
    assert result.success, "Klonlama başarılı olmalı"
    assert result.hyperlink_name == "Cloned", "Yeni ad eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  New hyperlink ID: {result.hyperlink_id}")
    print(f"  New hyperlink name: {result.hyperlink_name}")
    
    print("\n" + "=" * 70)
    print("PASS: Clone hyperlink")
    print("=" * 70)


def test_export_hyperlink():
    """
    Test: Export hyperlink.
    """
    print("=" * 70)
    print("TEST: Export Hyperlink")
    print("=" * 70)
    
    engine = TerminalHyperlinksEngine()
    result = engine.create_hyperlink("Default", url="https://example.com")
    hyperlink_id = result.hyperlink_id
    
    result = engine.export_hyperlink(hyperlink_id, format="json")
    
    assert result.success, "Dışa aktarma başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Export hyperlink")
    print("=" * 70)


def test_import_hyperlink():
    """
    Test: Import hyperlink.
    """
    print("=" * 70)
    print("TEST: Import Hyperlink")
    print("=" * 70)
    
    engine = TerminalHyperlinksEngine()
    
    data = {
        "name": "Imported",
        "link_type": "url",
        "url": "https://example.com",
        "text": "Click here",
        "color": "#00ff00",
        "underline": True,
        "hover_color": "#ff0000",
        "hover_underline": False,
        "click_action": "open"
    }
    
    result = engine.import_hyperlink(data)
    
    assert result.success, "İçe aktarma başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Import hyperlink")
    print("=" * 70)


def test_set_default_hyperlink():
    """
    Test: Set default hyperlink.
    """
    print("=" * 70)
    print("TEST: Set Default Hyperlink")
    print("=" * 70)
    
    engine = TerminalHyperlinksEngine()
    result = engine.create_hyperlink("Default", url="https://example.com")
    hyperlink_id = result.hyperlink_id
    
    result = engine.set_default_hyperlink(hyperlink_id)
    
    assert result.success, "Ayarlama başarılı olmalı"
    assert engine.hyperlinks[hyperlink_id].is_default, "Hyperlink varsayılan olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set default hyperlink")
    print("=" * 70)


def test_click_hyperlink():
    """
    Test: Click hyperlink.
    """
    print("=" * 70)
    print("TEST: Click Hyperlink")
    print("=" * 70)
    
    engine = TerminalHyperlinksEngine()
    result = engine.create_hyperlink("Default", url="https://example.com")
    hyperlink_id = result.hyperlink_id
    
    result = engine.click_hyperlink(hyperlink_id)
    
    assert result.success, "Tıklama başarılı olmalı"
    assert result.url == "https://example.com", "URL eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  URL: {result.url}")
    
    print("\n" + "=" * 70)
    print("PASS: Click hyperlink")
    print("=" * 70)


def test_hover_hyperlink():
    """
    Test: Hover hyperlink.
    """
    print("=" * 70)
    print("TEST: Hover Hyperlink")
    print("=" * 70)
    
    engine = TerminalHyperlinksEngine()
    result = engine.create_hyperlink("Default", url="https://example.com")
    hyperlink_id = result.hyperlink_id
    
    result = engine.hover_hyperlink(hyperlink_id)
    
    assert result.success, "Hover başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Hover hyperlink")
    print("=" * 70)


def test_reset_hyperlink():
    """
    Test: Reset hyperlink.
    """
    print("=" * 70)
    print("TEST: Reset Hyperlink")
    print("=" * 70)
    
    engine = TerminalHyperlinksEngine()
    result = engine.create_hyperlink("Default", url="https://example.com")
    hyperlink_id = result.hyperlink_id
    
    result = engine.reset_hyperlink(hyperlink_id)
    
    assert result.success, "Sıfırlama başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Reset hyperlink")
    print("=" * 70)


def test_get_hyperlink_history():
    """
    Test: Get hyperlink history.
    """
    print("=" * 70)
    print("TEST: Get Hyperlink History")
    print("=" * 70)
    
    engine = TerminalHyperlinksEngine()
    engine.create_hyperlink("Default", url="https://example.com")
    
    history = engine.get_hyperlink_history()
    
    assert len(history) > 0, "Geçmiş olmalı"
    
    print(f"  History: {len(history)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get hyperlink history")
    print("=" * 70)


def test_clear_history():
    """
    Test: Clear history.
    """
    print("=" * 70)
    print("TEST: Clear History")
    print("=" * 70)
    
    engine = TerminalHyperlinksEngine()
    engine.create_hyperlink("Default", url="https://example.com")
    
    result = engine.clear_history()
    
    assert result.success, "Temizleme başarılı olmalı"
    assert len(engine.get_hyperlink_history()) == 0, "Geçmiş temizlenmeli"
    
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
    
    engine = TerminalHyperlinksEngine()
    
    new_config = HyperlinkConfig(persist_hyperlinks=False)
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
    
    engine = TerminalHyperlinksEngine()
    
    config = engine.get_config()
    
    assert config is not None, "Config olmalı"
    assert config.persist_hyperlinks == True, "Config eşleşmeli"
    
    print(f"  Persist hyperlinks: {config.persist_hyperlinks}")
    print(f"  Auto load hyperlinks: {config.auto_load_hyperlinks}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


def test_hyperlink_type_enum():
    """
    Test: HyperlinkType enum.
    """
    print("=" * 70)
    print("TEST: HyperlinkType Enum")
    print("=" * 70)
    
    assert HyperlinkType.URL.value == "url"
    assert HyperlinkType.FILE.value == "file"
    assert HyperlinkType.EMAIL.value == "email"
    assert HyperlinkType.COMMAND.value == "command"
    assert HyperlinkType.DIRECTORY.value == "directory"
    assert HyperlinkType.CUSTOM.value == "custom"
    
    print(f"  All enum values verified")
    print(f"  Total types: {len(HyperlinkType)}")
    
    print("\n" + "=" * 70)
    print("PASS: HyperlinkType enum")
    print("=" * 70)


def test_hyperlink_scope_enum():
    """
    Test: HyperlinkScope enum.
    """
    print("=" * 70)
    print("TEST: HyperlinkScope Enum")
    print("=" * 70)
    
    assert HyperlinkScope.SESSION.value == "session"
    assert HyperlinkScope.TERMINAL.value == "terminal"
    assert HyperlinkScope.GLOBAL.value == "global"
    
    print(f"  All enum values verified")
    print(f"  Total scopes: {len(HyperlinkScope)}")
    
    print("\n" + "=" * 70)
    print("PASS: HyperlinkScope enum")
    print("=" * 70)


def test_hyperlink_action_enum():
    """
    Test: HyperlinkAction enum.
    """
    print("=" * 70)
    print("TEST: HyperlinkAction Enum")
    print("=" * 70)
    
    assert HyperlinkAction.CREATE.value == "create"
    assert HyperlinkAction.UPDATE.value == "update"
    assert HyperlinkAction.DELETE.value == "delete"
    assert HyperlinkAction.GET.value == "get"
    assert HyperlinkAction.LIST.value == "list"
    assert HyperlinkAction.ACTIVATE.value == "activate"
    assert HyperlinkAction.CLONE.value == "clone"
    assert HyperlinkAction.IMPORT.value == "import"
    assert HyperlinkAction.EXPORT.value == "export"
    assert HyperlinkAction.SET_DEFAULT.value == "set_default"
    assert HyperlinkAction.CLICK.value == "click"
    assert HyperlinkAction.HOVER.value == "hover"
    assert HyperlinkAction.RESET.value == "reset"
    
    print(f"  All enum values verified")
    print(f"  Total actions: {len(HyperlinkAction)}")
    
    print("\n" + "=" * 70)
    print("PASS: HyperlinkAction enum")
    print("=" * 70)


def test_hyperlink_config_dataclass():
    """
    Test: HyperlinkConfig dataclass.
    """
    print("=" * 70)
    print("TEST: HyperlinkConfig Dataclass")
    print("=" * 70)
    
    config = HyperlinkConfig(
        persist_hyperlinks=False,
        auto_load_hyperlinks=False
    )
    
    assert config.persist_hyperlinks == False, "Persist eşleşmeli"
    assert config.auto_load_hyperlinks == False, "Auto load eşleşmeli"
    
    print(f"  Persist hyperlinks: {config.persist_hyperlinks}")
    print(f"  Auto load hyperlinks: {config.auto_load_hyperlinks}")
    
    print("\n" + "=" * 70)
    print("PASS: HyperlinkConfig dataclass")
    print("=" * 70)


def test_hyperlink_entry_dataclass():
    """
    Test: HyperlinkEntry dataclass.
    """
    print("=" * 70)
    print("TEST: HyperlinkEntry Dataclass")
    print("=" * 70)
    
    entry = HyperlinkEntry(
        id="hyperlink_1",
        name="Default",
        link_type=HyperlinkType.URL,
        url="https://example.com",
        text="Click here",
        color="#00ff00",
        underline=True,
        scope=HyperlinkScope.SESSION,
        timestamp="2024-01-01T00:00:00"
    )
    
    assert entry.id == "hyperlink_1", "ID eşleşmeli"
    assert entry.name == "Default", "Ad eşleşmeli"
    
    print(f"  ID: {entry.id}")
    print(f"  Name: {entry.name}")
    
    print("\n" + "=" * 70)
    print("PASS: HyperlinkEntry dataclass")
    print("=" * 70)


def test_hyperlink_result_dataclass():
    """
    Test: HyperlinkResult dataclass.
    """
    print("=" * 70)
    print("TEST: HyperlinkResult Dataclass")
    print("=" * 70)
    
    result = HyperlinkResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: HyperlinkResult dataclass")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_create_hyperlink()
        test2 = test_create_hyperlink_with_options()
        test3 = test_update_hyperlink()
        test4 = test_delete_hyperlink()
        test5 = test_get_hyperlink()
        test6 = test_list_hyperlinks()
        test7 = test_list_hyperlinks_with_scope()
        test8 = test_activate_hyperlink()
        test9 = test_clone_hyperlink()
        test10 = test_export_hyperlink()
        test11 = test_import_hyperlink()
        test12 = test_set_default_hyperlink()
        test13 = test_click_hyperlink()
        test14 = test_hover_hyperlink()
        test15 = test_reset_hyperlink()
        test16 = test_get_hyperlink_history()
        test17 = test_clear_history()
        test18 = test_update_config()
        test19 = test_get_config()
        test20 = test_hyperlink_type_enum()
        test21 = test_hyperlink_scope_enum()
        test22 = test_hyperlink_action_enum()
        test23 = test_hyperlink_config_dataclass()
        test24 = test_hyperlink_entry_dataclass()
        test25 = test_hyperlink_result_dataclass()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Create Hyperlink: {'PASS' if test1 else 'FAIL'}")
        print(f"Create Hyperlink With Options: {'PASS' if test2 else 'FAIL'}")
        print(f"Update Hyperlink: {'PASS' if test3 else 'FAIL'}")
        print(f"Delete Hyperlink: {'PASS' if test4 else 'FAIL'}")
        print(f"Get Hyperlink: {'PASS' if test5 else 'FAIL'}")
        print(f"List Hyperlinks: {'PASS' if test6 else 'FAIL'}")
        print(f"List Hyperlinks With Scope: {'PASS' if test7 else 'FAIL'}")
        print(f"Activate Hyperlink: {'PASS' if test8 else 'FAIL'}")
        print(f"Clone Hyperlink: {'PASS' if test9 else 'FAIL'}")
        print(f"Export Hyperlink: {'PASS' if test10 else 'FAIL'}")
        print(f"Import Hyperlink: {'PASS' if test11 else 'FAIL'}")
        print(f"Set Default Hyperlink: {'PASS' if test12 else 'FAIL'}")
        print(f"Click Hyperlink: {'PASS' if test13 else 'FAIL'}")
        print(f"Hover Hyperlink: {'PASS' if test14 else 'FAIL'}")
        print(f"Reset Hyperlink: {'PASS' if test15 else 'FAIL'}")
        print(f"Get Hyperlink History: {'PASS' if test16 else 'FAIL'}")
        print(f"Clear History: {'PASS' if test17 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test18 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test19 else 'FAIL'}")
        print(f"HyperlinkType Enum: {'PASS' if test20 else 'FAIL'}")
        print(f"HyperlinkScope Enum: {'PASS' if test21 else 'FAIL'}")
        print(f"HyperlinkAction Enum: {'PASS' if test22 else 'FAIL'}")
        print(f"HyperlinkConfig Dataclass: {'PASS' if test23 else 'FAIL'}")
        print(f"HyperlinkEntry Dataclass: {'PASS' if test24 else 'FAIL'}")
        print(f"HyperlinkResult Dataclass: {'PASS' if test25 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14, test15, test16, test17, test18, test19, test20, test21, test22, test23, test24, test25])
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
