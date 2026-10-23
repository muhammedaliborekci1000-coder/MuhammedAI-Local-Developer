"""
Quality Test: Terminal Selection
Terminal selection system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.tools.terminal_selection import (
    TerminalSelectionEngine,
    SelectionMode,
    SelectionScope,
    SelectionAction,
    SelectionConfig,
    SelectionPosition,
    SelectionRange,
    SelectionEntry,
    SelectionResult
)


def test_create_selection():
    """
    Test: Create selection.
    """
    print("=" * 70)
    print("TEST: Create Selection")
    print("=" * 70)
    
    engine = TerminalSelectionEngine()
    result = engine.create_selection("Default")
    
    assert result.success, "Oluşturma başarılı olmalı"
    assert result.selection_name == "Default", "Seçim adı eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Selection ID: {result.selection_id}")
    print(f"  Selection name: {result.selection_name}")
    
    print("\n" + "=" * 70)
    print("PASS: Create selection")
    print("=" * 70)


def test_create_selection_with_options():
    """
    Test: Create selection with options.
    """
    print("=" * 70)
    print("TEST: Create Selection With Options")
    print("=" * 70)
    
    engine = TerminalSelectionEngine()
    
    result = engine.create_selection(
        "Custom",
        mode=SelectionMode.WORD,
        start_line=10,
        start_column=5,
        end_line=10,
        end_column=15,
        background_color="#00ff00",
        foreground_color="#000000"
    )
    
    assert result.success, "Oluşturma başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Selection ID: {result.selection_id}")
    
    print("\n" + "=" * 70)
    print("PASS: Create selection with options")
    print("=" * 70)


def test_update_selection():
    """
    Test: Update selection.
    """
    print("=" * 70)
    print("TEST: Update Selection")
    print("=" * 70)
    
    engine = TerminalSelectionEngine()
    result = engine.create_selection("Default")
    selection_id = result.selection_id
    
    result = engine.update_selection(selection_id, name="Updated", end_line=20)
    
    assert result.success, "Güncelleme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Update selection")
    print("=" * 70)


def test_delete_selection():
    """
    Test: Delete selection.
    """
    print("=" * 70)
    print("TEST: Delete Selection")
    print("=" * 70)
    
    engine = TerminalSelectionEngine()
    result = engine.create_selection("Default")
    selection_id = result.selection_id
    
    result = engine.delete_selection(selection_id)
    
    assert result.success, "Silme başarılı olmalı"
    assert selection_id not in engine.selections, "Seçim silinmiş olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Delete selection")
    print("=" * 70)


def test_get_selection():
    """
    Test: Get selection.
    """
    print("=" * 70)
    print("TEST: Get Selection")
    print("=" * 70)
    
    engine = TerminalSelectionEngine()
    result = engine.create_selection("Default")
    selection_id = result.selection_id
    
    result = engine.get_selection(selection_id)
    
    assert result.success, "Alma başarılı olmalı"
    assert result.selection_name == "Default", "Seçim adı eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Selection name: {result.selection_name}")
    
    print("\n" + "=" * 70)
    print("PASS: Get selection")
    print("=" * 70)


def test_list_selections():
    """
    Test: List selections.
    """
    print("=" * 70)
    print("TEST: List Selections")
    print("=" * 70)
    
    engine = TerminalSelectionEngine()
    engine.create_selection("Selection1")
    engine.create_selection("Selection2")
    
    result = engine.list_selections()
    
    assert result.success, "Listeleme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: List selections")
    print("=" * 70)


def test_list_selections_with_scope():
    """
    Test: List selections with scope.
    """
    print("=" * 70)
    print("TEST: List Selections With Scope")
    print("=" * 70)
    
    engine = TerminalSelectionEngine()
    engine.create_selection("Selection1", scope=SelectionScope.GLOBAL)
    engine.create_selection("Selection2", scope=SelectionScope.SESSION)
    
    result = engine.list_selections(scope=SelectionScope.GLOBAL)
    
    assert result.success, "Listeleme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: List selections with scope")
    print("=" * 70)


def test_activate_selection():
    """
    Test: Activate selection.
    """
    print("=" * 70)
    print("TEST: Activate Selection")
    print("=" * 70)
    
    engine = TerminalSelectionEngine()
    result = engine.create_selection("Default")
    selection_id = result.selection_id
    
    result = engine.activate_selection(selection_id)
    
    assert result.success, "Aktifleştirme başarılı olmalı"
    assert engine.selections[selection_id].is_active, "Seçim aktif olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Activate selection")
    print("=" * 70)


def test_clone_selection():
    """
    Test: Clone selection.
    """
    print("=" * 70)
    print("TEST: Clone Selection")
    print("=" * 70)
    
    engine = TerminalSelectionEngine()
    result = engine.create_selection("Default")
    selection_id = result.selection_id
    
    result = engine.clone_selection(selection_id, "Cloned")
    
    assert result.success, "Klonlama başarılı olmalı"
    assert result.selection_name == "Cloned", "Yeni ad eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  New selection ID: {result.selection_id}")
    print(f"  New selection name: {result.selection_name}")
    
    print("\n" + "=" * 70)
    print("PASS: Clone selection")
    print("=" * 70)


def test_export_selection():
    """
    Test: Export selection.
    """
    print("=" * 70)
    print("TEST: Export Selection")
    print("=" * 70)
    
    engine = TerminalSelectionEngine()
    result = engine.create_selection("Default")
    selection_id = result.selection_id
    
    result = engine.export_selection(selection_id, format="json")
    
    assert result.success, "Dışa aktarma başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Export selection")
    print("=" * 70)


def test_import_selection():
    """
    Test: Import selection.
    """
    print("=" * 70)
    print("TEST: Import Selection")
    print("=" * 70)
    
    engine = TerminalSelectionEngine()
    
    data = {
        "name": "Imported",
        "mode": "word",
        "range": {
            "start": {"line": 10, "column": 5},
            "end": {"line": 10, "column": 15}
        },
        "background_color": "#00ff00",
        "foreground_color": "#000000"
    }
    
    result = engine.import_selection(data)
    
    assert result.success, "İçe aktarma başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Import selection")
    print("=" * 70)


def test_set_default_selection():
    """
    Test: Set default selection.
    """
    print("=" * 70)
    print("TEST: Set Default Selection")
    print("=" * 70)
    
    engine = TerminalSelectionEngine()
    result = engine.create_selection("Default")
    selection_id = result.selection_id
    
    result = engine.set_default_selection(selection_id)
    
    assert result.success, "Ayarlama başarılı olmalı"
    assert engine.selections[selection_id].is_default, "Seçim varsayılan olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set default selection")
    print("=" * 70)


def test_select_all():
    """
    Test: Select all.
    """
    print("=" * 70)
    print("TEST: Select All")
    print("=" * 70)
    
    engine = TerminalSelectionEngine()
    
    result = engine.select_all()
    
    assert result.success, "Seçim başarılı olmalı"
    assert result.selection_name == "Select All", "Seçim adı eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Select all")
    print("=" * 70)


def test_select_word():
    """
    Test: Select word.
    """
    print("=" * 70)
    print("TEST: Select Word")
    print("=" * 70)
    
    engine = TerminalSelectionEngine()
    
    result = engine.select_word(10, 5)
    
    assert result.success, "Seçim başarılı olmalı"
    assert result.selection_name == "Select Word", "Seçim adı eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Select word")
    print("=" * 70)


def test_select_line():
    """
    Test: Select line.
    """
    print("=" * 70)
    print("TEST: Select Line")
    print("=" * 70)
    
    engine = TerminalSelectionEngine()
    
    result = engine.select_line(10)
    
    assert result.success, "Seçim başarılı olmalı"
    assert result.selection_name == "Select Line", "Seçim adı eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Select line")
    print("=" * 70)


def test_clear_selection():
    """
    Test: Clear selection.
    """
    print("=" * 70)
    print("TEST: Clear Selection")
    print("=" * 70)
    
    engine = TerminalSelectionEngine()
    result = engine.create_selection("Default")
    selection_id = result.selection_id
    engine.activate_selection(selection_id)
    
    result = engine.clear_selection()
    
    assert result.success, "Temizleme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear selection")
    print("=" * 70)


def test_copy_selection():
    """
    Test: Copy selection.
    """
    print("=" * 70)
    print("TEST: Copy Selection")
    print("=" * 70)
    
    engine = TerminalSelectionEngine()
    result = engine.create_selection("Default")
    selection_id = result.selection_id
    
    result = engine.copy_selection(selection_id)
    
    assert result.success, "Kopyalama başarılı olmalı"
    assert result.selected_text is not None, "Seçili metin olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Copy selection")
    print("=" * 70)


def test_reset_selection():
    """
    Test: Reset selection.
    """
    print("=" * 70)
    print("TEST: Reset Selection")
    print("=" * 70)
    
    engine = TerminalSelectionEngine()
    result = engine.create_selection("Default")
    selection_id = result.selection_id
    
    result = engine.reset_selection(selection_id)
    
    assert result.success, "Sıfırlama başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Reset selection")
    print("=" * 70)


def test_get_selection_history():
    """
    Test: Get selection history.
    """
    print("=" * 70)
    print("TEST: Get Selection History")
    print("=" * 70)
    
    engine = TerminalSelectionEngine()
    engine.create_selection("Default")
    
    history = engine.get_selection_history()
    
    assert len(history) > 0, "Geçmiş olmalı"
    
    print(f"  History: {len(history)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get selection history")
    print("=" * 70)


def test_clear_history():
    """
    Test: Clear history.
    """
    print("=" * 70)
    print("TEST: Clear History")
    print("=" * 70)
    
    engine = TerminalSelectionEngine()
    engine.create_selection("Default")
    
    result = engine.clear_history()
    
    assert result.success, "Temizleme başarılı olmalı"
    assert len(engine.get_selection_history()) == 0, "Geçmiş temizlenmeli"
    
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
    
    engine = TerminalSelectionEngine()
    
    new_config = SelectionConfig(persist_selections=False)
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
    
    engine = TerminalSelectionEngine()
    
    config = engine.get_config()
    
    assert config is not None, "Config olmalı"
    assert config.persist_selections == True, "Config eşleşmeli"
    
    print(f"  Persist selections: {config.persist_selections}")
    print(f"  Auto load selections: {config.auto_load_selections}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


def test_selection_mode_enum():
    """
    Test: SelectionMode enum.
    """
    print("=" * 70)
    print("TEST: SelectionMode Enum")
    print("=" * 70)
    
    assert SelectionMode.CHARACTER.value == "character"
    assert SelectionMode.WORD.value == "word"
    assert SelectionMode.LINE.value == "line"
    assert SelectionMode.BLOCK.value == "block"
    assert SelectionMode.SMART.value == "smart"
    assert SelectionMode.RECTANGULAR.value == "rectangular"
    
    print(f"  All enum values verified")
    print(f"  Total modes: {len(SelectionMode)}")
    
    print("\n" + "=" * 70)
    print("PASS: SelectionMode enum")
    print("=" * 70)


def test_selection_scope_enum():
    """
    Test: SelectionScope enum.
    """
    print("=" * 70)
    print("TEST: SelectionScope Enum")
    print("=" * 70)
    
    assert SelectionScope.SESSION.value == "session"
    assert SelectionScope.TERMINAL.value == "terminal"
    assert SelectionScope.GLOBAL.value == "global"
    
    print(f"  All enum values verified")
    print(f"  Total scopes: {len(SelectionScope)}")
    
    print("\n" + "=" * 70)
    print("PASS: SelectionScope enum")
    print("=" * 70)


def test_selection_action_enum():
    """
    Test: SelectionAction enum.
    """
    print("=" * 70)
    print("TEST: SelectionAction Enum")
    print("=" * 70)
    
    assert SelectionAction.CREATE.value == "create"
    assert SelectionAction.UPDATE.value == "update"
    assert SelectionAction.DELETE.value == "delete"
    assert SelectionAction.GET.value == "get"
    assert SelectionAction.LIST.value == "list"
    assert SelectionAction.ACTIVATE.value == "activate"
    assert SelectionAction.CLONE.value == "clone"
    assert SelectionAction.IMPORT.value == "import"
    assert SelectionAction.EXPORT.value == "export"
    assert SelectionAction.SET_DEFAULT.value == "set_default"
    assert SelectionAction.SELECT_ALL.value == "select_all"
    assert SelectionAction.SELECT_WORD.value == "select_word"
    assert SelectionAction.SELECT_LINE.value == "select_line"
    assert SelectionAction.CLEAR.value == "clear"
    assert SelectionAction.COPY.value == "copy"
    assert SelectionAction.RESET.value == "reset"
    
    print(f"  All enum values verified")
    print(f"  Total actions: {len(SelectionAction)}")
    
    print("\n" + "=" * 70)
    print("PASS: SelectionAction enum")
    print("=" * 70)


def test_selection_config_dataclass():
    """
    Test: SelectionConfig dataclass.
    """
    print("=" * 70)
    print("TEST: SelectionConfig Dataclass")
    print("=" * 70)
    
    config = SelectionConfig(
        persist_selections=False,
        auto_load_selections=False
    )
    
    assert config.persist_selections == False, "Persist eşleşmeli"
    assert config.auto_load_selections == False, "Auto load eşleşmeli"
    
    print(f"  Persist selections: {config.persist_selections}")
    print(f"  Auto load selections: {config.auto_load_selections}")
    
    print("\n" + "=" * 70)
    print("PASS: SelectionConfig dataclass")
    print("=" * 70)


def test_selection_position_dataclass():
    """
    Test: SelectionPosition dataclass.
    """
    print("=" * 70)
    print("TEST: SelectionPosition Dataclass")
    print("=" * 70)
    
    position = SelectionPosition(line=10, column=20)
    
    assert position.line == 10, "Satır eşleşmeli"
    assert position.column == 20, "Sütun eşleşmeli"
    
    print(f"  Line: {position.line}")
    print(f"  Column: {position.column}")
    
    print("\n" + "=" * 70)
    print("PASS: SelectionPosition dataclass")
    print("=" * 70)


def test_selection_range_dataclass():
    """
    Test: SelectionRange dataclass.
    """
    print("=" * 70)
    print("TEST: SelectionRange Dataclass")
    print("=" * 70)
    
    start = SelectionPosition(line=0, column=0)
    end = SelectionPosition(line=10, column=20)
    range_obj = SelectionRange(start=start, end=end)
    
    assert range_obj.start.line == 0, "Başlangıç satırı eşleşmeli"
    assert range_obj.end.line == 10, "Bitiş satırı eşleşmeli"
    
    print(f"  Start line: {range_obj.start.line}")
    print(f"  End line: {range_obj.end.line}")
    
    print("\n" + "=" * 70)
    print("PASS: SelectionRange dataclass")
    print("=" * 70)


def test_selection_entry_dataclass():
    """
    Test: SelectionEntry dataclass.
    """
    print("=" * 70)
    print("TEST: SelectionEntry Dataclass")
    print("=" * 70)
    
    start = SelectionPosition(line=0, column=0)
    end = SelectionPosition(line=10, column=20)
    range_obj = SelectionRange(start=start, end=end)
    
    entry = SelectionEntry(
        id="selection_1",
        name="Default",
        mode=SelectionMode.CHARACTER,
        range=range_obj,
        background_color="#ffffff",
        foreground_color="#000000",
        scope=SelectionScope.SESSION,
        timestamp="2024-01-01T00:00:00"
    )
    
    assert entry.id == "selection_1", "ID eşleşmeli"
    assert entry.name == "Default", "Ad eşleşmeli"
    
    print(f"  ID: {entry.id}")
    print(f"  Name: {entry.name}")
    
    print("\n" + "=" * 70)
    print("PASS: SelectionEntry dataclass")
    print("=" * 70)


def test_selection_result_dataclass():
    """
    Test: SelectionResult dataclass.
    """
    print("=" * 70)
    print("TEST: SelectionResult Dataclass")
    print("=" * 70)
    
    result = SelectionResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: SelectionResult dataclass")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_create_selection()
        test2 = test_create_selection_with_options()
        test3 = test_update_selection()
        test4 = test_delete_selection()
        test5 = test_get_selection()
        test6 = test_list_selections()
        test7 = test_list_selections_with_scope()
        test8 = test_activate_selection()
        test9 = test_clone_selection()
        test10 = test_export_selection()
        test11 = test_import_selection()
        test12 = test_set_default_selection()
        test13 = test_select_all()
        test14 = test_select_word()
        test15 = test_select_line()
        test16 = test_clear_selection()
        test17 = test_copy_selection()
        test18 = test_reset_selection()
        test19 = test_get_selection_history()
        test20 = test_clear_history()
        test21 = test_update_config()
        test22 = test_get_config()
        test23 = test_selection_mode_enum()
        test24 = test_selection_scope_enum()
        test25 = test_selection_action_enum()
        test26 = test_selection_config_dataclass()
        test27 = test_selection_position_dataclass()
        test28 = test_selection_range_dataclass()
        test29 = test_selection_entry_dataclass()
        test30 = test_selection_result_dataclass()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Create Selection: {'PASS' if test1 else 'FAIL'}")
        print(f"Create Selection With Options: {'PASS' if test2 else 'FAIL'}")
        print(f"Update Selection: {'PASS' if test3 else 'FAIL'}")
        print(f"Delete Selection: {'PASS' if test4 else 'FAIL'}")
        print(f"Get Selection: {'PASS' if test5 else 'FAIL'}")
        print(f"List Selections: {'PASS' if test6 else 'FAIL'}")
        print(f"List Selections With Scope: {'PASS' if test7 else 'FAIL'}")
        print(f"Activate Selection: {'PASS' if test8 else 'FAIL'}")
        print(f"Clone Selection: {'PASS' if test9 else 'FAIL'}")
        print(f"Export Selection: {'PASS' if test10 else 'FAIL'}")
        print(f"Import Selection: {'PASS' if test11 else 'FAIL'}")
        print(f"Set Default Selection: {'PASS' if test12 else 'FAIL'}")
        print(f"Select All: {'PASS' if test13 else 'FAIL'}")
        print(f"Select Word: {'PASS' if test14 else 'FAIL'}")
        print(f"Select Line: {'PASS' if test15 else 'FAIL'}")
        print(f"Clear Selection: {'PASS' if test16 else 'FAIL'}")
        print(f"Copy Selection: {'PASS' if test17 else 'FAIL'}")
        print(f"Reset Selection: {'PASS' if test18 else 'FAIL'}")
        print(f"Get Selection History: {'PASS' if test19 else 'FAIL'}")
        print(f"Clear History: {'PASS' if test20 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test21 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test22 else 'FAIL'}")
        print(f"SelectionMode Enum: {'PASS' if test23 else 'FAIL'}")
        print(f"SelectionScope Enum: {'PASS' if test24 else 'FAIL'}")
        print(f"SelectionAction Enum: {'PASS' if test25 else 'FAIL'}")
        print(f"SelectionConfig Dataclass: {'PASS' if test26 else 'FAIL'}")
        print(f"SelectionPosition Dataclass: {'PASS' if test27 else 'FAIL'}")
        print(f"SelectionRange Dataclass: {'PASS' if test28 else 'FAIL'}")
        print(f"SelectionEntry Dataclass: {'PASS' if test29 else 'FAIL'}")
        print(f"SelectionResult Dataclass: {'PASS' if test30 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14, test15, test16, test17, test18, test19, test20, test21, test22, test23, test24, test25, test26, test27, test28, test29, test30])
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
