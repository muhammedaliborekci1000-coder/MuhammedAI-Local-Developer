"""
Quality Test: Terminal Focus
Terminal focus system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.tools.terminal_focus import (
    TerminalFocusEngine,
    FocusMode,
    FocusScope,
    FocusAction,
    FocusConfig,
    FocusEntry,
    FocusResult
)


def test_focus_terminal():
    """
    Test: Focus terminal.
    """
    print("=" * 70)
    print("TEST: Focus Terminal")
    print("=" * 70)
    
    engine = TerminalFocusEngine()
    result = engine.focus_terminal("terminal_1")
    
    assert result.success, "Odaklama başarılı olmalı"
    assert result.focused_terminal_id == "terminal_1", "Terminal ID eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Focused terminal ID: {result.focused_terminal_id}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Focus terminal")
    print("=" * 70)


def test_focus_terminal_with_details():
    """
    Test: Focus terminal with details.
    """
    print("=" * 70)
    print("TEST: Focus Terminal With Details")
    print("=" * 70)
    
    engine = TerminalFocusEngine()
    result = engine.focus_terminal("terminal_1", panel_id="panel_1", session_id="session_1")
    
    assert result.success, "Odaklama başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Panel ID: {engine.terminals['terminal_1'].panel_id}")
    
    print("\n" + "=" * 70)
    print("PASS: Focus terminal with details")
    print("=" * 70)


def test_unfocus_terminal():
    """
    Test: Unfocus terminal.
    """
    print("=" * 70)
    print("TEST: Unfocus Terminal")
    print("=" * 70)
    
    engine = TerminalFocusEngine()
    engine.focus_terminal("terminal_1")
    
    result = engine.unfocus_terminal("terminal_1")
    
    assert result.success, "Odak kaldırma başarılı olmalı"
    assert engine.focused_terminal is None, "Odaklı terminal olmamalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Unfocus terminal")
    print("=" * 70)


def test_toggle_focus():
    """
    Test: Toggle focus.
    """
    print("=" * 70)
    print("TEST: Toggle Focus")
    print("=" * 70)
    
    engine = TerminalFocusEngine()
    engine.focus_terminal("terminal_1")
    
    result = engine.toggle_focus("terminal_1")
    
    assert result.success, "Değiştirme başarılı olmalı"
    assert engine.focused_terminal is None, "Odak kaldırılmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Action: {result.action}")
    
    print("\n" + "=" * 70)
    print("PASS: Toggle focus")
    print("=" * 70)


def test_focus_next():
    """
    Test: Focus next.
    """
    print("=" * 70)
    print("TEST: Focus Next")
    print("=" * 70)
    
    engine = TerminalFocusEngine()
    engine.focus_terminal("terminal_1")
    engine.focus_terminal("terminal_2")
    
    result = engine.focus_next()
    
    assert result.success, "Sonrakine odaklama başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Action: {result.action}")
    
    print("\n" + "=" * 70)
    print("PASS: Focus next")
    print("=" * 70)


def test_focus_previous():
    """
    Test: Focus previous.
    """
    print("=" * 70)
    print("TEST: Focus Previous")
    print("=" * 70)
    
    engine = TerminalFocusEngine()
    engine.focus_terminal("terminal_1")
    engine.focus_terminal("terminal_2")
    
    result = engine.focus_previous()
    
    assert result.success, "Öncekine odaklama başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Action: {result.action}")
    
    print("\n" + "=" * 70)
    print("PASS: Focus previous")
    print("=" * 70)


def test_get_focused_terminal():
    """
    Test: Get focused terminal.
    """
    print("=" * 70)
    print("TEST: Get Focused Terminal")
    print("=" * 70)
    
    engine = TerminalFocusEngine()
    engine.focus_terminal("terminal_1")
    
    focused = engine.get_focused_terminal()
    
    assert focused is not None, "Odaklı terminal olmalı"
    assert focused.terminal_id == "terminal_1", "Terminal ID eşleşmeli"
    
    print(f"  Terminal ID: {focused.terminal_id}")
    print(f"  Is focused: {focused.is_focused}")
    
    print("\n" + "=" * 70)
    print("PASS: Get focused terminal")
    print("=" * 70)


def test_get_all_terminals():
    """
    Test: Get all terminals.
    """
    print("=" * 70)
    print("TEST: Get All Terminals")
    print("=" * 70)
    
    engine = TerminalFocusEngine()
    engine.focus_terminal("terminal_1")
    engine.focus_terminal("terminal_2")
    
    terminals = engine.get_all_terminals()
    
    assert len(terminals) == 2, "2 terminal bulunmalı"
    
    print(f"  Terminals: {len(terminals)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get all terminals")
    print("=" * 70)


def test_get_terminal():
    """
    Test: Get terminal.
    """
    print("=" * 70)
    print("TEST: Get Terminal")
    print("=" * 70)
    
    engine = TerminalFocusEngine()
    engine.focus_terminal("terminal_1")
    
    terminal = engine.get_terminal("terminal_1")
    
    assert terminal is not None, "Terminal bulunmalı"
    assert terminal.terminal_id == "terminal_1", "Terminal ID eşleşmeli"
    
    print(f"  Terminal ID: {terminal.terminal_id}")
    
    print("\n" + "=" * 70)
    print("PASS: Get terminal")
    print("=" * 70)


def test_get_focus_history():
    """
    Test: Get focus history.
    """
    print("=" * 70)
    print("TEST: Get Focus History")
    print("=" * 70)
    
    engine = TerminalFocusEngine()
    engine.focus_terminal("terminal_1")
    
    history = engine.get_focus_history()
    
    assert len(history) > 0, "Geçmiş olmalı"
    
    print(f"  History: {len(history)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get focus history")
    print("=" * 70)


def test_clear_history():
    """
    Test: Clear history.
    """
    print("=" * 70)
    print("TEST: Clear History")
    print("=" * 70)
    
    engine = TerminalFocusEngine()
    engine.focus_terminal("terminal_1")
    
    result = engine.clear_history()
    
    assert result.success, "Temizleme başarılı olmalı"
    assert len(engine.get_focus_history()) == 0, "Geçmiş temizlenmeli"
    
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
    
    engine = TerminalFocusEngine()
    
    new_config = FocusConfig(auto_focus_on_create=False)
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
    
    engine = TerminalFocusEngine()
    
    config = engine.get_config()
    
    assert config is not None, "Config olmalı"
    assert config.auto_focus_on_create == True, "Config eşleşmeli"
    
    print(f"  Auto focus on create: {config.auto_focus_on_create}")
    print(f"  Show focus indicator: {config.show_focus_indicator}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


def test_focus_mode_enum():
    """
    Test: FocusMode enum.
    """
    print("=" * 70)
    print("TEST: FocusMode Enum")
    print("=" * 70)
    
    assert FocusMode.SINGLE.value == "single"
    assert FocusMode.MULTI.value == "multi"
    assert FocusMode.AUTO.value == "auto"
    
    print(f"  All enum values verified")
    print(f"  Total modes: {len(FocusMode)}")
    
    print("\n" + "=" * 70)
    print("PASS: FocusMode enum")
    print("=" * 70)


def test_focus_scope_enum():
    """
    Test: FocusScope enum.
    """
    print("=" * 70)
    print("TEST: FocusScope Enum")
    print("=" * 70)
    
    assert FocusScope.TERMINAL.value == "terminal"
    assert FocusScope.PANEL.value == "panel"
    assert FocusScope.SESSION.value == "session"
    
    print(f"  All enum values verified")
    print(f"  Total scopes: {len(FocusScope)}")
    
    print("\n" + "=" * 70)
    print("PASS: FocusScope enum")
    print("=" * 70)


def test_focus_action_enum():
    """
    Test: FocusAction enum.
    """
    print("=" * 70)
    print("TEST: FocusAction Enum")
    print("=" * 70)
    
    assert FocusAction.FOCUS.value == "focus"
    assert FocusAction.UNFOCUS.value == "unfocus"
    assert FocusAction.TOGGLE.value == "toggle"
    assert FocusAction.NEXT.value == "next"
    assert FocusAction.PREVIOUS.value == "previous"
    
    print(f"  All enum values verified")
    print(f"  Total actions: {len(FocusAction)}")
    
    print("\n" + "=" * 70)
    print("PASS: FocusAction enum")
    print("=" * 70)


def test_focus_config_dataclass():
    """
    Test: FocusConfig dataclass.
    """
    print("=" * 70)
    print("TEST: FocusConfig Dataclass")
    print("=" * 70)
    
    config = FocusConfig(
        auto_focus_on_create=False,
        show_focus_indicator=False
    )
    
    assert config.auto_focus_on_create == False, "Auto focus eşleşmeli"
    assert config.show_focus_indicator == False, "Show indicator eşleşmeli"
    
    print(f"  Auto focus on create: {config.auto_focus_on_create}")
    print(f"  Show focus indicator: {config.show_focus_indicator}")
    
    print("\n" + "=" * 70)
    print("PASS: FocusConfig dataclass")
    print("=" * 70)


def test_focus_entry_dataclass():
    """
    Test: FocusEntry dataclass.
    """
    print("=" * 70)
    print("TEST: FocusEntry Dataclass")
    print("=" * 70)
    
    entry = FocusEntry(
        id="focus_1",
        terminal_id="terminal_1",
        timestamp="2024-01-01T00:00:00"
    )
    
    assert entry.id == "focus_1", "ID eşleşmeli"
    assert entry.terminal_id == "terminal_1", "Terminal ID eşleşmeli"
    
    print(f"  ID: {entry.id}")
    print(f"  Terminal ID: {entry.terminal_id}")
    
    print("\n" + "=" * 70)
    print("PASS: FocusEntry dataclass")
    print("=" * 70)


def test_focus_result_dataclass():
    """
    Test: FocusResult dataclass.
    """
    print("=" * 70)
    print("TEST: FocusResult Dataclass")
    print("=" * 70)
    
    result = FocusResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: FocusResult dataclass")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_focus_terminal()
        test2 = test_focus_terminal_with_details()
        test3 = test_unfocus_terminal()
        test4 = test_toggle_focus()
        test5 = test_focus_next()
        test6 = test_focus_previous()
        test7 = test_get_focused_terminal()
        test8 = test_get_all_terminals()
        test9 = test_get_terminal()
        test10 = test_get_focus_history()
        test11 = test_clear_history()
        test12 = test_update_config()
        test13 = test_get_config()
        test14 = test_focus_mode_enum()
        test15 = test_focus_scope_enum()
        test16 = test_focus_action_enum()
        test17 = test_focus_config_dataclass()
        test18 = test_focus_entry_dataclass()
        test19 = test_focus_result_dataclass()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Focus Terminal: {'PASS' if test1 else 'FAIL'}")
        print(f"Focus Terminal With Details: {'PASS' if test2 else 'FAIL'}")
        print(f"Unfocus Terminal: {'PASS' if test3 else 'FAIL'}")
        print(f"Toggle Focus: {'PASS' if test4 else 'FAIL'}")
        print(f"Focus Next: {'PASS' if test5 else 'FAIL'}")
        print(f"Focus Previous: {'PASS' if test6 else 'FAIL'}")
        print(f"Get Focused Terminal: {'PASS' if test7 else 'FAIL'}")
        print(f"Get All Terminals: {'PASS' if test8 else 'FAIL'}")
        print(f"Get Terminal: {'PASS' if test9 else 'FAIL'}")
        print(f"Get Focus History: {'PASS' if test10 else 'FAIL'}")
        print(f"Clear History: {'PASS' if test11 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test12 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test13 else 'FAIL'}")
        print(f"FocusMode Enum: {'PASS' if test14 else 'FAIL'}")
        print(f"FocusScope Enum: {'PASS' if test15 else 'FAIL'}")
        print(f"FocusAction Enum: {'PASS' if test16 else 'FAIL'}")
        print(f"FocusConfig Dataclass: {'PASS' if test17 else 'FAIL'}")
        print(f"FocusEntry Dataclass: {'PASS' if test18 else 'FAIL'}")
        print(f"FocusResult Dataclass: {'PASS' if test19 else 'FAIL'}")
        
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
