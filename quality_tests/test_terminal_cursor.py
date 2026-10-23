"""
Quality Test: Terminal Cursor
Terminal cursor system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.tools.terminal_cursor import (
    TerminalCursorEngine,
    CursorStyle,
    CursorScope,
    CursorAction,
    CursorConfig,
    CursorEntry,
    CursorPosition,
    CursorResult
)


def test_create_cursor():
    """
    Test: Create cursor.
    """
    print("=" * 70)
    print("TEST: Create Cursor")
    print("=" * 70)
    
    engine = TerminalCursorEngine()
    result = engine.create_cursor("Default")
    
    assert result.success, "Oluşturma başarılı olmalı"
    assert result.cursor_name == "Default", "Cursor adı eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Cursor ID: {result.cursor_id}")
    print(f"  Cursor name: {result.cursor_name}")
    
    print("\n" + "=" * 70)
    print("PASS: Create cursor")
    print("=" * 70)


def test_create_cursor_with_options():
    """
    Test: Create cursor with options.
    """
    print("=" * 70)
    print("TEST: Create Cursor With Options")
    print("=" * 70)
    
    engine = TerminalCursorEngine()
    
    result = engine.create_cursor(
        "Custom",
        style=CursorStyle.BAR,
        color="#00ff00",
        size=2,
        blink=True,
        blink_interval=0.3,
        blink_enabled=True
    )
    
    assert result.success, "Oluşturma başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Cursor ID: {result.cursor_id}")
    
    print("\n" + "=" * 70)
    print("PASS: Create cursor with options")
    print("=" * 70)


def test_update_cursor():
    """
    Test: Update cursor.
    """
    print("=" * 70)
    print("TEST: Update Cursor")
    print("=" * 70)
    
    engine = TerminalCursorEngine()
    result = engine.create_cursor("Default")
    cursor_id = result.cursor_id
    
    result = engine.update_cursor(cursor_id, name="Updated", color="#ff0000")
    
    assert result.success, "Güncelleme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Update cursor")
    print("=" * 70)


def test_delete_cursor():
    """
    Test: Delete cursor.
    """
    print("=" * 70)
    print("TEST: Delete Cursor")
    print("=" * 70)
    
    engine = TerminalCursorEngine()
    result = engine.create_cursor("Default")
    cursor_id = result.cursor_id
    
    result = engine.delete_cursor(cursor_id)
    
    assert result.success, "Silme başarılı olmalı"
    assert cursor_id not in engine.cursors, "Cursor ayarı silinmiş olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Delete cursor")
    print("=" * 70)


def test_get_cursor():
    """
    Test: Get cursor.
    """
    print("=" * 70)
    print("TEST: Get Cursor")
    print("=" * 70)
    
    engine = TerminalCursorEngine()
    result = engine.create_cursor("Default")
    cursor_id = result.cursor_id
    
    result = engine.get_cursor(cursor_id)
    
    assert result.success, "Alma başarılı olmalı"
    assert result.cursor_name == "Default", "Cursor adı eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Cursor name: {result.cursor_name}")
    
    print("\n" + "=" * 70)
    print("PASS: Get cursor")
    print("=" * 70)


def test_list_cursors():
    """
    Test: List cursors.
    """
    print("=" * 70)
    print("TEST: List Cursors")
    print("=" * 70)
    
    engine = TerminalCursorEngine()
    engine.create_cursor("Cursor1")
    engine.create_cursor("Cursor2")
    
    result = engine.list_cursors()
    
    assert result.success, "Listeleme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: List cursors")
    print("=" * 70)


def test_list_cursors_with_scope():
    """
    Test: List cursors with scope.
    """
    print("=" * 70)
    print("TEST: List Cursors With Scope")
    print("=" * 70)
    
    engine = TerminalCursorEngine()
    engine.create_cursor("Cursor1", scope=CursorScope.GLOBAL)
    engine.create_cursor("Cursor2", scope=CursorScope.SESSION)
    
    result = engine.list_cursors(scope=CursorScope.GLOBAL)
    
    assert result.success, "Listeleme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: List cursors with scope")
    print("=" * 70)


def test_activate_cursor():
    """
    Test: Activate cursor.
    """
    print("=" * 70)
    print("TEST: Activate Cursor")
    print("=" * 70)
    
    engine = TerminalCursorEngine()
    result = engine.create_cursor("Default")
    cursor_id = result.cursor_id
    
    result = engine.activate_cursor(cursor_id)
    
    assert result.success, "Aktifleştirme başarılı olmalı"
    assert engine.cursors[cursor_id].is_active, "Cursor ayarı aktif olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Activate cursor")
    print("=" * 70)


def test_clone_cursor():
    """
    Test: Clone cursor.
    """
    print("=" * 70)
    print("TEST: Clone Cursor")
    print("=" * 70)
    
    engine = TerminalCursorEngine()
    result = engine.create_cursor("Default")
    cursor_id = result.cursor_id
    
    result = engine.clone_cursor(cursor_id, "Cloned")
    
    assert result.success, "Klonlama başarılı olmalı"
    assert result.cursor_name == "Cloned", "Yeni ad eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  New cursor ID: {result.cursor_id}")
    print(f"  New cursor name: {result.cursor_name}")
    
    print("\n" + "=" * 70)
    print("PASS: Clone cursor")
    print("=" * 70)


def test_export_cursor():
    """
    Test: Export cursor.
    """
    print("=" * 70)
    print("TEST: Export Cursor")
    print("=" * 70)
    
    engine = TerminalCursorEngine()
    result = engine.create_cursor("Default")
    cursor_id = result.cursor_id
    
    result = engine.export_cursor(cursor_id, format="json")
    
    assert result.success, "Dışa aktarma başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Export cursor")
    print("=" * 70)


def test_import_cursor():
    """
    Test: Import cursor.
    """
    print("=" * 70)
    print("TEST: Import Cursor")
    print("=" * 70)
    
    engine = TerminalCursorEngine()
    
    data = {
        "name": "Imported",
        "style": "bar",
        "color": "#00ff00",
        "size": 2,
        "blink": True,
        "blink_interval": 0.3,
        "blink_enabled": True
    }
    
    result = engine.import_cursor(data)
    
    assert result.success, "İçe aktarma başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Import cursor")
    print("=" * 70)


def test_set_default_cursor():
    """
    Test: Set default cursor.
    """
    print("=" * 70)
    print("TEST: Set Default Cursor")
    print("=" * 70)
    
    engine = TerminalCursorEngine()
    result = engine.create_cursor("Default")
    cursor_id = result.cursor_id
    
    result = engine.set_default_cursor(cursor_id)
    
    assert result.success, "Ayarlama başarılı olmalı"
    assert engine.cursors[cursor_id].is_default, "Cursor ayarı varsayılan olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set default cursor")
    print("=" * 70)


def test_move_cursor():
    """
    Test: Move cursor.
    """
    print("=" * 70)
    print("TEST: Move Cursor")
    print("=" * 70)
    
    engine = TerminalCursorEngine()
    
    result = engine.move_cursor(10, 20)
    
    assert result.success, "Hareket başarılı olmalı"
    assert result.position is not None, "Pozisyon olmalı"
    assert result.position.line == 10, "Satır eşleşmeli"
    assert result.position.column == 20, "Sütun eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Position: line {result.position.line}, column {result.position.column}")
    
    print("\n" + "=" * 70)
    print("PASS: Move cursor")
    print("=" * 70)


def test_get_cursor_position():
    """
    Test: Get cursor position.
    """
    print("=" * 70)
    print("TEST: Get Cursor Position")
    print("=" * 70)
    
    engine = TerminalCursorEngine()
    engine.move_cursor(10, 20)
    
    position = engine.get_cursor_position()
    
    assert position is not None, "Pozisyon olmalı"
    assert position.line == 10, "Satır eşleşmeli"
    assert position.column == 20, "Sütun eşleşmeli"
    
    print(f"  Position: line {position.line}, column {position.column}")
    
    print("\n" + "=" * 70)
    print("PASS: Get cursor position")
    print("=" * 70)


def test_reset_cursor():
    """
    Test: Reset cursor.
    """
    print("=" * 70)
    print("TEST: Reset Cursor")
    print("=" * 70)
    
    engine = TerminalCursorEngine()
    result = engine.create_cursor("Default")
    cursor_id = result.cursor_id
    
    result = engine.reset_cursor(cursor_id)
    
    assert result.success, "Sıfırlama başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Reset cursor")
    print("=" * 70)


def test_get_cursor_history():
    """
    Test: Get cursor history.
    """
    print("=" * 70)
    print("TEST: Get Cursor History")
    print("=" * 70)
    
    engine = TerminalCursorEngine()
    engine.create_cursor("Default")
    
    history = engine.get_cursor_history()
    
    assert len(history) > 0, "Geçmiş olmalı"
    
    print(f"  History: {len(history)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get cursor history")
    print("=" * 70)


def test_clear_history():
    """
    Test: Clear history.
    """
    print("=" * 70)
    print("TEST: Clear History")
    print("=" * 70)
    
    engine = TerminalCursorEngine()
    engine.create_cursor("Default")
    
    result = engine.clear_history()
    
    assert result.success, "Temizleme başarılı olmalı"
    assert len(engine.get_cursor_history()) == 0, "Geçmiş temizlenmeli"
    
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
    
    engine = TerminalCursorEngine()
    
    new_config = CursorConfig(persist_cursors=False)
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
    
    engine = TerminalCursorEngine()
    
    config = engine.get_config()
    
    assert config is not None, "Config olmalı"
    assert config.persist_cursors == True, "Config eşleşmeli"
    
    print(f"  Persist cursors: {config.persist_cursors}")
    print(f"  Auto load cursors: {config.auto_load_cursors}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


def test_cursor_style_enum():
    """
    Test: CursorStyle enum.
    """
    print("=" * 70)
    print("TEST: CursorStyle Enum")
    print("=" * 70)
    
    assert CursorStyle.BLOCK.value == "block"
    assert CursorStyle.UNDERLINE.value == "underline"
    assert CursorStyle.BAR.value == "bar"
    assert CursorStyle.BEAM.value == "beam"
    assert CursorStyle.HOLLOW.value == "hollow"
    
    print(f"  All enum values verified")
    print(f"  Total styles: {len(CursorStyle)}")
    
    print("\n" + "=" * 70)
    print("PASS: CursorStyle enum")
    print("=" * 70)


def test_cursor_scope_enum():
    """
    Test: CursorScope enum.
    """
    print("=" * 70)
    print("TEST: CursorScope Enum")
    print("=" * 70)
    
    assert CursorScope.SESSION.value == "session"
    assert CursorScope.TERMINAL.value == "terminal"
    assert CursorScope.GLOBAL.value == "global"
    
    print(f"  All enum values verified")
    print(f"  Total scopes: {len(CursorScope)}")
    
    print("\n" + "=" * 70)
    print("PASS: CursorScope enum")
    print("=" * 70)


def test_cursor_action_enum():
    """
    Test: CursorAction enum.
    """
    print("=" * 70)
    print("TEST: CursorAction Enum")
    print("=" * 70)
    
    assert CursorAction.CREATE.value == "create"
    assert CursorAction.UPDATE.value == "update"
    assert CursorAction.DELETE.value == "delete"
    assert CursorAction.GET.value == "get"
    assert CursorAction.LIST.value == "list"
    assert CursorAction.ACTIVATE.value == "activate"
    assert CursorAction.CLONE.value == "clone"
    assert CursorAction.IMPORT.value == "import"
    assert CursorAction.EXPORT.value == "export"
    assert CursorAction.SET_DEFAULT.value == "set_default"
    assert CursorAction.MOVE.value == "move"
    assert CursorAction.RESET.value == "reset"
    
    print(f"  All enum values verified")
    print(f"  Total actions: {len(CursorAction)}")
    
    print("\n" + "=" * 70)
    print("PASS: CursorAction enum")
    print("=" * 70)


def test_cursor_config_dataclass():
    """
    Test: CursorConfig dataclass.
    """
    print("=" * 70)
    print("TEST: CursorConfig Dataclass")
    print("=" * 70)
    
    config = CursorConfig(
        persist_cursors=False,
        auto_load_cursors=False
    )
    
    assert config.persist_cursors == False, "Persist eşleşmeli"
    assert config.auto_load_cursors == False, "Auto load eşleşmeli"
    
    print(f"  Persist cursors: {config.persist_cursors}")
    print(f"  Auto load cursors: {config.auto_load_cursors}")
    
    print("\n" + "=" * 70)
    print("PASS: CursorConfig dataclass")
    print("=" * 70)


def test_cursor_entry_dataclass():
    """
    Test: CursorEntry dataclass.
    """
    print("=" * 70)
    print("TEST: CursorEntry Dataclass")
    print("=" * 70)
    
    entry = CursorEntry(
        id="cursor_1",
        name="Default",
        style=CursorStyle.BLOCK,
        color="#ffffff",
        size=1,
        blink=True,
        blink_interval=0.5,
        blink_enabled=True,
        scope=CursorScope.SESSION,
        timestamp="2024-01-01T00:00:00"
    )
    
    assert entry.id == "cursor_1", "ID eşleşmeli"
    assert entry.name == "Default", "Ad eşleşmeli"
    
    print(f"  ID: {entry.id}")
    print(f"  Name: {entry.name}")
    
    print("\n" + "=" * 70)
    print("PASS: CursorEntry dataclass")
    print("=" * 70)


def test_cursor_position_dataclass():
    """
    Test: CursorPosition dataclass.
    """
    print("=" * 70)
    print("TEST: CursorPosition Dataclass")
    print("=" * 70)
    
    position = CursorPosition(line=10, column=20)
    
    assert position.line == 10, "Satır eşleşmeli"
    assert position.column == 20, "Sütun eşleşmeli"
    
    print(f"  Line: {position.line}")
    print(f"  Column: {position.column}")
    
    print("\n" + "=" * 70)
    print("PASS: CursorPosition dataclass")
    print("=" * 70)


def test_cursor_result_dataclass():
    """
    Test: CursorResult dataclass.
    """
    print("=" * 70)
    print("TEST: CursorResult Dataclass")
    print("=" * 70)
    
    result = CursorResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: CursorResult dataclass")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_create_cursor()
        test2 = test_create_cursor_with_options()
        test3 = test_update_cursor()
        test4 = test_delete_cursor()
        test5 = test_get_cursor()
        test6 = test_list_cursors()
        test7 = test_list_cursors_with_scope()
        test8 = test_activate_cursor()
        test9 = test_clone_cursor()
        test10 = test_export_cursor()
        test11 = test_import_cursor()
        test12 = test_set_default_cursor()
        test13 = test_move_cursor()
        test14 = test_get_cursor_position()
        test15 = test_reset_cursor()
        test16 = test_get_cursor_history()
        test17 = test_clear_history()
        test18 = test_update_config()
        test19 = test_get_config()
        test20 = test_cursor_style_enum()
        test21 = test_cursor_scope_enum()
        test22 = test_cursor_action_enum()
        test23 = test_cursor_config_dataclass()
        test24 = test_cursor_entry_dataclass()
        test25 = test_cursor_position_dataclass()
        test26 = test_cursor_result_dataclass()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Create Cursor: {'PASS' if test1 else 'FAIL'}")
        print(f"Create Cursor With Options: {'PASS' if test2 else 'FAIL'}")
        print(f"Update Cursor: {'PASS' if test3 else 'FAIL'}")
        print(f"Delete Cursor: {'PASS' if test4 else 'FAIL'}")
        print(f"Get Cursor: {'PASS' if test5 else 'FAIL'}")
        print(f"List Cursors: {'PASS' if test6 else 'FAIL'}")
        print(f"List Cursors With Scope: {'PASS' if test7 else 'FAIL'}")
        print(f"Activate Cursor: {'PASS' if test8 else 'FAIL'}")
        print(f"Clone Cursor: {'PASS' if test9 else 'FAIL'}")
        print(f"Export Cursor: {'PASS' if test10 else 'FAIL'}")
        print(f"Import Cursor: {'PASS' if test11 else 'FAIL'}")
        print(f"Set Default Cursor: {'PASS' if test12 else 'FAIL'}")
        print(f"Move Cursor: {'PASS' if test13 else 'FAIL'}")
        print(f"Get Cursor Position: {'PASS' if test14 else 'FAIL'}")
        print(f"Reset Cursor: {'PASS' if test15 else 'FAIL'}")
        print(f"Get Cursor History: {'PASS' if test16 else 'FAIL'}")
        print(f"Clear History: {'PASS' if test17 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test18 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test19 else 'FAIL'}")
        print(f"CursorStyle Enum: {'PASS' if test20 else 'FAIL'}")
        print(f"CursorScope Enum: {'PASS' if test21 else 'FAIL'}")
        print(f"CursorAction Enum: {'PASS' if test22 else 'FAIL'}")
        print(f"CursorConfig Dataclass: {'PASS' if test23 else 'FAIL'}")
        print(f"CursorEntry Dataclass: {'PASS' if test24 else 'FAIL'}")
        print(f"CursorPosition Dataclass: {'PASS' if test25 else 'FAIL'}")
        print(f"CursorResult Dataclass: {'PASS' if test26 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14, test15, test16, test17, test18, test19, test20, test21, test22, test23, test24, test25, test26])
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
