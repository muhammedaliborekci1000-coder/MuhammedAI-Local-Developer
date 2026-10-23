"""
Quality Test: Macros
Macros system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.macros import (
    MacrosEngine,
    MacroAction,
    MacroEventType,
    MacroEvent,
    Macro,
    MacroConfig,
    MacroResult
)


def test_start_recording():
    """
    Test: Start recording.
    """
    print("=" * 70)
    print("TEST: Start Recording")
    print("=" * 70)
    
    engine = MacrosEngine()
    
    result = engine.start_recording("test_macro", "Test macro")
    
    assert result.success, "Kayıt başarılı olmalı"
    assert engine.is_recording_active() == True, "Kayıt aktif olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Start recording")
    print("=" * 70)


def test_stop_recording():
    """
    Test: Stop recording.
    """
    print("=" * 70)
    print("TEST: Stop Recording")
    print("=" * 70)
    
    engine = MacrosEngine()
    
    engine.start_recording("test_macro", "Test macro")
    result = engine.stop_recording()
    
    assert result.success, "Durdurma başarılı olmalı"
    assert engine.is_recording_active() == False, "Kayıt durmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Stop recording")
    print("=" * 70)


def test_record_event():
    """
    Test: Record event.
    """
    print("=" * 70)
    print("TEST: Record Event")
    print("=" * 70)
    
    engine = MacrosEngine()
    
    engine.start_recording("test_macro", "Test macro")
    result = engine.record_event(MacroEventType.KEY_PRESS, {"key": "a"}, 0, 0)
    
    assert result.success, "Kayıt başarılı olmalı"
    assert result.events_count == 1, "1 olay olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Events count: {result.events_count}")
    
    print("\n" + "=" * 70)
    print("PASS: Record event")
    print("=" * 70)


def test_play_macro():
    """
    Test: Play macro.
    """
    print("=" * 70)
    print("TEST: Play Macro")
    print("=" * 70)
    
    engine = MacrosEngine()
    
    engine.start_recording("test_macro", "Test macro")
    engine.record_event(MacroEventType.KEY_PRESS, {"key": "a"}, 0, 0)
    engine.stop_recording()
    
    result = engine.play_macro("test_macro")
    
    assert result.success, "Oynatma başarılı olmalı"
    assert result.events_count == 1, "1 olay olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Play macro")
    print("=" * 70)


def test_edit_macro():
    """
    Test: Edit macro.
    """
    print("=" * 70)
    print("TEST: Edit Macro")
    print("=" * 70)
    
    engine = MacrosEngine()
    
    engine.start_recording("test_macro", "Test macro")
    engine.stop_recording()
    
    result = engine.edit_macro("test_macro", description="Updated description")
    
    assert result.success, "Düzenleme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Edit macro")
    print("=" * 70)


def test_delete_macro():
    """
    Test: Delete macro.
    """
    print("=" * 70)
    print("TEST: Delete Macro")
    print("=" * 70)
    
    engine = MacrosEngine()
    
    engine.start_recording("test_macro", "Test macro")
    engine.stop_recording()
    
    result = engine.delete_macro("test_macro")
    
    assert result.success, "Silme başarılı olmalı"
    assert engine.get_macro("test_macro") is None, "Macro silinmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Delete macro")
    print("=" * 70)


def test_get_macro():
    """
    Test: Get macro.
    """
    print("=" * 70)
    print("TEST: Get Macro")
    print("=" * 70)
    
    engine = MacrosEngine()
    
    engine.start_recording("test_macro", "Test macro")
    engine.stop_recording()
    
    macro = engine.get_macro("test_macro")
    
    assert macro is not None, "Macro olmalı"
    assert macro.name == "test_macro", "Macro adı eşleşmeli"
    
    print(f"  Macro name: {macro.name}")
    print(f"  Description: {macro.description}")
    
    print("\n" + "=" * 70)
    print("PASS: Get macro")
    print("=" * 70)


def test_get_all_macros():
    """
    Test: Get all macros.
    """
    print("=" * 70)
    print("TEST: Get All Macros")
    print("=" * 70)
    
    engine = MacrosEngine()
    
    engine.start_recording("test_macro1", "Test macro 1")
    engine.stop_recording()
    
    engine.start_recording("test_macro2", "Test macro 2")
    engine.stop_recording()
    
    macros = engine.get_all_macros()
    
    assert len(macros) == 2, "2 macro olmalı"
    
    print(f"  Total macros: {len(macros)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get all macros")
    print("=" * 70)


def test_enable_macro():
    """
    Test: Enable macro.
    """
    print("=" * 70)
    print("TEST: Enable Macro")
    print("=" * 70)
    
    engine = MacrosEngine()
    
    engine.start_recording("test_macro", "Test macro")
    engine.stop_recording()
    
    result = engine.enable_macro("test_macro")
    
    assert result.success, "Etkinleştirme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Enable macro")
    print("=" * 70)


def test_disable_macro():
    """
    Test: Disable macro.
    """
    print("=" * 70)
    print("TEST: Disable Macro")
    print("=" * 70)
    
    engine = MacrosEngine()
    
    engine.start_recording("test_macro", "Test macro")
    engine.stop_recording()
    
    result = engine.disable_macro("test_macro")
    
    assert result.success, "Devre dışı bırakma başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Disable macro")
    print("=" * 70)


def test_get_playback_history():
    """
    Test: Get playback history.
    """
    print("=" * 70)
    print("TEST: Get Playback History")
    print("=" * 70)
    
    engine = MacrosEngine()
    
    engine.start_recording("test_macro", "Test macro")
    engine.record_event(MacroEventType.KEY_PRESS, {"key": "a"}, 0, 0)
    engine.stop_recording()
    
    engine.play_macro("test_macro")
    history = engine.get_playback_history()
    
    assert len(history) > 0, "Geçmiş olmalı"
    
    print(f"  History: {len(history)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get playback history")
    print("=" * 70)


def test_clear_history():
    """
    Test: Clear history.
    """
    print("=" * 70)
    print("TEST: Clear History")
    print("=" * 70)
    
    engine = MacrosEngine()
    
    engine.start_recording("test_macro", "Test macro")
    engine.record_event(MacroEventType.KEY_PRESS, {"key": "a"}, 0, 0)
    engine.stop_recording()
    
    engine.play_macro("test_macro")
    result = engine.clear_history()
    
    assert result.success, "Temizleme başarılı olmalı"
    assert len(engine.get_playback_history()) == 0, "Geçmiş temizlenmeli"
    
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
    
    engine = MacrosEngine()
    
    new_config = MacroConfig(auto_save=False, max_events=500)
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
    
    engine = MacrosEngine()
    
    config = engine.get_config()
    
    assert config is not None, "Config olmalı"
    assert config.auto_save == True, "Config eşleşmeli"
    
    print(f"  Auto save: {config.auto_save}")
    print(f"  Max events: {config.max_events}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


def test_is_recording_active():
    """
    Test: Is recording active.
    """
    print("=" * 70)
    print("TEST: Is Recording Active")
    print("=" * 70)
    
    engine = MacrosEngine()
    
    assert engine.is_recording_active() == False, "Kayıt aktif olmamalı"
    
    engine.start_recording("test_macro", "Test macro")
    assert engine.is_recording_active() == True, "Kayıt aktif olmalı"
    
    engine.stop_recording()
    assert engine.is_recording_active() == False, "Kayıt aktif olmamalı"
    
    print(f"  Recording active check passed")
    
    print("\n" + "=" * 70)
    print("PASS: Is recording active")
    print("=" * 70)


def test_is_playing_active():
    """
    Test: Is playing active.
    """
    print("=" * 70)
    print("TEST: Is Playing Active")
    print("=" * 70)
    
    engine = MacrosEngine()
    
    assert engine.is_playing_active() == False, "Oynatma aktif olmamalı"
    
    engine.start_recording("test_macro", "Test macro")
    engine.record_event(MacroEventType.KEY_PRESS, {"key": "a"}, 0, 0)
    engine.stop_recording()
    
    engine.play_macro("test_macro")
    assert engine.is_playing_active() == False, "Oynatma tamamlandı"
    
    print(f"  Playing active check passed")
    
    print("\n" + "=" * 70)
    print("PASS: Is playing active")
    print("=" * 70)


def test_macro_action_enum():
    """
    Test: MacroAction enum.
    """
    print("=" * 70)
    print("TEST: MacroAction Enum")
    print("=" * 70)
    
    assert MacroAction.RECORD.value == "record"
    assert MacroAction.PLAY.value == "play"
    assert MacroAction.STOP.value == "stop"
    assert MacroAction.PAUSE.value == "pause"
    assert MacroAction.RESUME.value == "resume"
    
    print(f"  All enum values verified")
    print(f"  Total actions: {len(MacroAction)}")
    
    print("\n" + "=" * 70)
    print("PASS: MacroAction enum")
    print("=" * 70)


def test_macro_event_type_enum():
    """
    Test: MacroEventType enum.
    """
    print("=" * 70)
    print("TEST: MacroEventType Enum")
    print("=" * 70)
    
    assert MacroEventType.KEY_PRESS.value == "key_press"
    assert MacroEventType.MOUSE_CLICK.value == "mouse_click"
    assert MacroEventType.TEXT_INSERT.value == "text_insert"
    assert MacroEventType.TEXT_DELETE.value == "text_delete"
    assert MacroEventType.CURSOR_MOVE.value == "cursor_move"
    assert MacroEventType.SELECTION_CHANGE.value == "selection_change"
    
    print(f"  All enum values verified")
    print(f"  Total types: {len(MacroEventType)}")
    
    print("\n" + "=" * 70)
    print("PASS: MacroEventType enum")
    print("=" * 70)


def test_macro_event_dataclass():
    """
    Test: MacroEvent dataclass.
    """
    print("=" * 70)
    print("TEST: MacroEvent Dataclass")
    print("=" * 70)
    
    event = MacroEvent(
        event_type=MacroEventType.KEY_PRESS,
        timestamp=1234567890.0,
        data={"key": "a"},
        line=0,
        column=0
    )
    
    assert event.event_type == MacroEventType.KEY_PRESS, "Event type eşleşmeli"
    assert event.data == {"key": "a"}, "Data eşleşmeli"
    
    print(f"  Event type: {event.event_type.value}")
    print(f"  Data: {event.data}")
    
    print("\n" + "=" * 70)
    print("PASS: MacroEvent dataclass")
    print("=" * 70)


def test_macro_dataclass():
    """
    Test: Macro dataclass.
    """
    print("=" * 70)
    print("TEST: Macro Dataclass")
    print("=" * 70)
    
    macro = Macro(
        name="test_macro",
        description="Test macro",
        enabled=True
    )
    
    assert macro.name == "test_macro", "Name eşleşmeli"
    assert macro.description == "Test macro", "Description eşleşmeli"
    assert macro.enabled == True, "Enabled eşleşmeli"
    
    print(f"  Name: {macro.name}")
    print(f"  Description: {macro.description}")
    print(f"  Enabled: {macro.enabled}")
    
    print("\n" + "=" * 70)
    print("PASS: Macro dataclass")
    print("=" * 70)


def test_macro_config_dataclass():
    """
    Test: MacroConfig dataclass.
    """
    print("=" * 70)
    print("TEST: MacroConfig Dataclass")
    print("=" * 70)
    
    config = MacroConfig(
        auto_save=True,
        max_events=1000,
        enable_playback=True
    )
    
    assert config.auto_save == True, "Auto save eşleşmeli"
    assert config.max_events == 1000, "Max events eşleşmeli"
    assert config.enable_playback == True, "Enable playback eşleşmeli"
    
    print(f"  Auto save: {config.auto_save}")
    print(f"  Max events: {config.max_events}")
    print(f"  Enable playback: {config.enable_playback}")
    
    print("\n" + "=" * 70)
    print("PASS: MacroConfig dataclass")
    print("=" * 70)


def test_macro_result_dataclass():
    """
    Test: MacroResult dataclass.
    """
    print("=" * 70)
    print("TEST: MacroResult Dataclass")
    print("=" * 70)
    
    result = MacroResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: MacroResult dataclass")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_start_recording()
        test2 = test_stop_recording()
        test3 = test_record_event()
        test4 = test_play_macro()
        test5 = test_edit_macro()
        test6 = test_delete_macro()
        test7 = test_get_macro()
        test8 = test_get_all_macros()
        test9 = test_enable_macro()
        test10 = test_disable_macro()
        test11 = test_get_playback_history()
        test12 = test_clear_history()
        test13 = test_update_config()
        test14 = test_get_config()
        test15 = test_is_recording_active()
        test16 = test_is_playing_active()
        test17 = test_macro_action_enum()
        test18 = test_macro_event_type_enum()
        test19 = test_macro_event_dataclass()
        test20 = test_macro_dataclass()
        test21 = test_macro_config_dataclass()
        test22 = test_macro_result_dataclass()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Start Recording: {'PASS' if test1 else 'FAIL'}")
        print(f"Stop Recording: {'PASS' if test2 else 'FAIL'}")
        print(f"Record Event: {'PASS' if test3 else 'FAIL'}")
        print(f"Play Macro: {'PASS' if test4 else 'FAIL'}")
        print(f"Edit Macro: {'PASS' if test5 else 'FAIL'}")
        print(f"Delete Macro: {'PASS' if test6 else 'FAIL'}")
        print(f"Get Macro: {'PASS' if test7 else 'FAIL'}")
        print(f"Get All Macros: {'PASS' if test8 else 'FAIL'}")
        print(f"Enable Macro: {'PASS' if test9 else 'FAIL'}")
        print(f"Disable Macro: {'PASS' if test10 else 'FAIL'}")
        print(f"Get Playback History: {'PASS' if test11 else 'FAIL'}")
        print(f"Clear History: {'PASS' if test12 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test13 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test14 else 'FAIL'}")
        print(f"Is Recording Active: {'PASS' if test15 else 'FAIL'}")
        print(f"Is Playing Active: {'PASS' if test16 else 'FAIL'}")
        print(f"MacroAction Enum: {'PASS' if test17 else 'FAIL'}")
        print(f"MacroEventType Enum: {'PASS' if test18 else 'FAIL'}")
        print(f"MacroEvent Dataclass: {'PASS' if test19 else 'FAIL'}")
        print(f"Macro Dataclass: {'PASS' if test20 else 'FAIL'}")
        print(f"MacroConfig Dataclass: {'PASS' if test21 else 'FAIL'}")
        print(f"MacroResult Dataclass: {'PASS' if test22 else 'FAIL'}")
        
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
