"""
Quality Test: Terminal Panels
Terminal panels system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.tools.terminal_panels import (
    TerminalPanelsEngine,
    PanelState,
    SplitDirection,
    PanelAction,
    PanelConfig,
    Panel,
    PanelResult
)


def test_create_panel():
    """
    Test: Create panel.
    """
    print("=" * 70)
    print("TEST: Create Panel")
    print("=" * 70)
    
    engine = TerminalPanelsEngine()
    result = engine.create_panel("Test Panel")
    
    assert result.success, "Oluşturma başarılı olmalı"
    assert result.panel is not None, "Panel olmalı"
    assert result.panel.name == "Test Panel", "İsim eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Panel ID: {result.panel_id}")
    print(f"  Panel name: {result.panel.name}")
    
    print("\n" + "=" * 70)
    print("PASS: Create panel")
    print("=" * 70)


def test_close_panel():
    """
    Test: Close panel.
    """
    print("=" * 70)
    print("TEST: Close Panel")
    print("=" * 70)
    
    engine = TerminalPanelsEngine()
    create_result = engine.create_panel("Test Panel")
    
    result = engine.close_panel(create_result.panel_id)
    
    assert result.success, "Kapatma başarılı olmalı"
    assert engine.get_panel(create_result.panel_id) is None, "Panel silinmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Close panel")
    print("=" * 70)


def test_rename_panel():
    """
    Test: Rename panel.
    """
    print("=" * 70)
    print("TEST: Rename Panel")
    print("=" * 70)
    
    engine = TerminalPanelsEngine()
    create_result = engine.create_panel("Test Panel")
    
    result = engine.rename_panel(create_result.panel_id, "Renamed Panel")
    
    assert result.success, "Yeniden adlandırma başarılı olmalı"
    assert result.panel.name == "Renamed Panel", "İsim değişmeli"
    
    print(f"  Success: {result.success}")
    print(f"  New name: {result.panel.name}")
    
    print("\n" + "=" * 70)
    print("PASS: Rename panel")
    print("=" * 70)


def test_focus_panel():
    """
    Test: Focus panel.
    """
    print("=" * 70)
    print("TEST: Focus Panel")
    print("=" * 70)
    
    engine = TerminalPanelsEngine()
    create_result = engine.create_panel("Test Panel")
    
    result = engine.focus_panel(create_result.panel_id)
    
    assert result.success, "Odaklama başarılı olmalı"
    assert result.panel.is_focused == True, "Odaklanmış olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Is focused: {result.panel.is_focused}")
    
    print("\n" + "=" * 70)
    print("PASS: Focus panel")
    print("=" * 70)


def test_split_panel():
    """
    Test: Split panel.
    """
    print("=" * 70)
    print("TEST: Split Panel")
    print("=" * 70)
    
    engine = TerminalPanelsEngine()
    create_result = engine.create_panel("Test Panel")
    
    result = engine.split_panel(create_result.panel_id, SplitDirection.HORIZONTAL)
    
    assert result.success, "Bölme başarılı olmalı"
    assert result.panel is not None, "Yeni panel olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  New panel ID: {result.panel_id}")
    
    print("\n" + "=" * 70)
    print("PASS: Split panel")
    print("=" * 70)


def test_resize_panel():
    """
    Test: Resize panel.
    """
    print("=" * 70)
    print("TEST: Resize Panel")
    print("=" * 70)
    
    engine = TerminalPanelsEngine()
    create_result = engine.create_panel("Test Panel")
    
    result = engine.resize_panel(create_result.panel_id, 800, 600)
    
    assert result.success, "Yeniden boyutlandırma başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Resize panel")
    print("=" * 70)


def test_clear_panel():
    """
    Test: Clear panel.
    """
    print("=" * 70)
    print("TEST: Clear Panel")
    print("=" * 70)
    
    engine = TerminalPanelsEngine()
    create_result = engine.create_panel("Test Panel")
    
    result = engine.clear_panel(create_result.panel_id)
    
    assert result.success, "Temizleme başarılı olmalı"
    assert result.panel.command_count == 0, "Komut sayısı sıfırlanmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Command count: {result.panel.command_count}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear panel")
    print("=" * 70)


def test_restart_panel():
    """
    Test: Restart panel.
    """
    print("=" * 70)
    print("TEST: Restart Panel")
    print("=" * 70)
    
    engine = TerminalPanelsEngine()
    create_result = engine.create_panel("Test Panel")
    
    result = engine.restart_panel(create_result.panel_id)
    
    assert result.success, "Yeniden başlatma başarılı olmalı"
    assert result.panel.state == PanelState.INACTIVE, "Durum inactive olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  State: {result.panel.state.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Restart panel")
    print("=" * 70)


def test_kill_panel():
    """
    Test: Kill panel.
    """
    print("=" * 70)
    print("TEST: Kill Panel")
    print("=" * 70)
    
    engine = TerminalPanelsEngine()
    create_result = engine.create_panel("Test Panel")
    
    result = engine.kill_panel(create_result.panel_id)
    
    assert result.success, "Durdurma başarılı olmalı"
    assert result.panel.state == PanelState.ERROR, "Durum error olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  State: {result.panel.state.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Kill panel")
    print("=" * 70)


def test_get_panel():
    """
    Test: Get panel.
    """
    print("=" * 70)
    print("TEST: Get Panel")
    print("=" * 70)
    
    engine = TerminalPanelsEngine()
    create_result = engine.create_panel("Test Panel")
    
    panel = engine.get_panel(create_result.panel_id)
    
    assert panel is not None, "Panel olmalı"
    assert panel.name == "Test Panel", "İsim eşleşmeli"
    
    print(f"  Panel: {panel.name}")
    print(f"  State: {panel.state.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Get panel")
    print("=" * 70)


def test_get_all_panels():
    """
    Test: Get all panels.
    """
    print("=" * 70)
    print("TEST: Get All Panels")
    print("=" * 70)
    
    engine = TerminalPanelsEngine()
    engine.create_panel("Panel 1")
    engine.create_panel("Panel 2")
    
    panels = engine.get_all_panels()
    
    assert len(panels) == 2, "2 panel olmalı"
    
    print(f"  Panel count: {len(panels)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get all panels")
    print("=" * 70)


def test_get_active_panel():
    """
    Test: Get active panel.
    """
    print("=" * 70)
    print("TEST: Get Active Panel")
    print("=" * 70)
    
    engine = TerminalPanelsEngine()
    create_result = engine.create_panel("Test Panel")
    
    active_panel = engine.get_active_panel()
    
    assert active_panel is not None, "Aktif panel olmalı"
    assert active_panel.id == create_result.panel_id, "ID eşleşmeli"
    
    print(f"  Active panel: {active_panel.name}")
    
    print("\n" + "=" * 70)
    print("PASS: Get active panel")
    print("=" * 70)


def test_get_panel_history():
    """
    Test: Get panel history.
    """
    print("=" * 70)
    print("TEST: Get Panel History")
    print("=" * 70)
    
    engine = TerminalPanelsEngine()
    engine.create_panel("Test Panel")
    
    history = engine.get_panel_history()
    
    assert len(history) > 0, "Geçmiş olmalı"
    
    print(f"  History: {len(history)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get panel history")
    print("=" * 70)


def test_clear_history():
    """
    Test: Clear history.
    """
    print("=" * 70)
    print("TEST: Clear History")
    print("=" * 70)
    
    engine = TerminalPanelsEngine()
    engine.create_panel("Test Panel")
    
    result = engine.clear_history()
    
    assert result.success, "Temizleme başarılı olmalı"
    assert len(engine.get_panel_history()) == 0, "Geçmiş temizlenmeli"
    
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
    
    engine = TerminalPanelsEngine()
    
    new_config = PanelConfig(shell="cmd")
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
    
    engine = TerminalPanelsEngine()
    
    config = engine.get_config()
    
    assert config is not None, "Config olmalı"
    assert config.shell == "powershell", "Config eşleşmeli"
    
    print(f"  Shell: {config.shell}")
    print(f"  Font size: {config.font_size}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


def test_panel_state_enum():
    """
    Test: PanelState enum.
    """
    print("=" * 70)
    print("TEST: PanelState Enum")
    print("=" * 70)
    
    assert PanelState.ACTIVE.value == "active"
    assert PanelState.INACTIVE.value == "inactive"
    assert PanelState.BUSY.value == "busy"
    assert PanelState.ERROR.value == "error"
    
    print(f"  All enum values verified")
    print(f"  Total states: {len(PanelState)}")
    
    print("\n" + "=" * 70)
    print("PASS: PanelState enum")
    print("=" * 70)


def test_split_direction_enum():
    """
    Test: SplitDirection enum.
    """
    print("=" * 70)
    print("TEST: SplitDirection Enum")
    print("=" * 70)
    
    assert SplitDirection.HORIZONTAL.value == "horizontal"
    assert SplitDirection.VERTICAL.value == "vertical"
    
    print(f"  All enum values verified")
    print(f"  Total directions: {len(SplitDirection)}")
    
    print("\n" + "=" * 70)
    print("PASS: SplitDirection enum")
    print("=" * 70)


def test_panel_action_enum():
    """
    Test: PanelAction enum.
    """
    print("=" * 70)
    print("TEST: PanelAction Enum")
    print("=" * 70)
    
    assert PanelAction.CREATE.value == "create"
    assert PanelAction.CLOSE.value == "close"
    assert PanelAction.RENAME.value == "rename"
    assert PanelAction.FOCUS.value == "focus"
    
    print(f"  All enum values verified")
    print(f"  Total actions: {len(PanelAction)}")
    
    print("\n" + "=" * 70)
    print("PASS: PanelAction enum")
    print("=" * 70)


def test_panel_config_dataclass():
    """
    Test: PanelConfig dataclass.
    """
    print("=" * 70)
    print("TEST: PanelConfig Dataclass")
    print("=" * 70)
    
    config = PanelConfig(
        shell="cmd",
        font_size=16
    )
    
    assert config.shell == "cmd", "Shell eşleşmeli"
    assert config.font_size == 16, "Font size eşleşmeli"
    
    print(f"  Shell: {config.shell}")
    print(f"  Font size: {config.font_size}")
    
    print("\n" + "=" * 70)
    print("PASS: PanelConfig dataclass")
    print("=" * 70)


def test_panel_dataclass():
    """
    Test: Panel dataclass.
    """
    print("=" * 70)
    print("TEST: Panel Dataclass")
    print("=" * 70)
    
    panel = Panel(
        id="panel_1",
        name="Test Panel",
        state=PanelState.ACTIVE
    )
    
    assert panel.id == "panel_1", "ID eşleşmeli"
    assert panel.name == "Test Panel", "İsim eşleşmeli"
    assert panel.state == PanelState.ACTIVE, "Durum eşleşmeli"
    
    print(f"  ID: {panel.id}")
    print(f"  Name: {panel.name}")
    print(f"  State: {panel.state.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Panel dataclass")
    print("=" * 70)


def test_panel_result_dataclass():
    """
    Test: PanelResult dataclass.
    """
    print("=" * 70)
    print("TEST: PanelResult Dataclass")
    print("=" * 70)
    
    result = PanelResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: PanelResult dataclass")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_create_panel()
        test2 = test_close_panel()
        test3 = test_rename_panel()
        test4 = test_focus_panel()
        test5 = test_split_panel()
        test6 = test_resize_panel()
        test7 = test_clear_panel()
        test8 = test_restart_panel()
        test9 = test_kill_panel()
        test10 = test_get_panel()
        test11 = test_get_all_panels()
        test12 = test_get_active_panel()
        test13 = test_get_panel_history()
        test14 = test_clear_history()
        test15 = test_update_config()
        test16 = test_get_config()
        test17 = test_panel_state_enum()
        test18 = test_split_direction_enum()
        test19 = test_panel_action_enum()
        test20 = test_panel_config_dataclass()
        test21 = test_panel_dataclass()
        test22 = test_panel_result_dataclass()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Create Panel: {'PASS' if test1 else 'FAIL'}")
        print(f"Close Panel: {'PASS' if test2 else 'FAIL'}")
        print(f"Rename Panel: {'PASS' if test3 else 'FAIL'}")
        print(f"Focus Panel: {'PASS' if test4 else 'FAIL'}")
        print(f"Split Panel: {'PASS' if test5 else 'FAIL'}")
        print(f"Resize Panel: {'PASS' if test6 else 'FAIL'}")
        print(f"Clear Panel: {'PASS' if test7 else 'FAIL'}")
        print(f"Restart Panel: {'PASS' if test8 else 'FAIL'}")
        print(f"Kill Panel: {'PASS' if test9 else 'FAIL'}")
        print(f"Get Panel: {'PASS' if test10 else 'FAIL'}")
        print(f"Get All Panels: {'PASS' if test11 else 'FAIL'}")
        print(f"Get Active Panel: {'PASS' if test12 else 'FAIL'}")
        print(f"Get Panel History: {'PASS' if test13 else 'FAIL'}")
        print(f"Clear History: {'PASS' if test14 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test15 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test16 else 'FAIL'}")
        print(f"PanelState Enum: {'PASS' if test17 else 'FAIL'}")
        print(f"SplitDirection Enum: {'PASS' if test18 else 'FAIL'}")
        print(f"PanelAction Enum: {'PASS' if test19 else 'FAIL'}")
        print(f"PanelConfig Dataclass: {'PASS' if test20 else 'FAIL'}")
        print(f"Panel Dataclass: {'PASS' if test21 else 'FAIL'}")
        print(f"PanelResult Dataclass: {'PASS' if test22 else 'FAIL'}")
        
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
