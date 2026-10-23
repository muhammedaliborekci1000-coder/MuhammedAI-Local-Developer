"""
Quality Test: Terminal Clear
Terminal clear system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.tools.terminal_clear import (
    TerminalClearEngine,
    ClearMode,
    ClearScope,
    ClearAction,
    ClearConfig,
    ClearResult
)


def test_clear_screen():
    """
    Test: Clear screen.
    """
    print("=" * 70)
    print("TEST: Clear Screen")
    print("=" * 70)
    
    engine = TerminalClearEngine()
    engine.screen_content = ["Line 1", "Line 2"]
    
    result = engine.clear_screen()
    
    assert result.success, "Temizleme başarılı olmalı"
    assert result.cleared_count == 2, "2 satır temizlenmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Cleared count: {result.cleared_count}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear screen")
    print("=" * 70)


def test_clear_screen_with_panel():
    """
    Test: Clear screen with panel.
    """
    print("=" * 70)
    print("TEST: Clear Screen With Panel")
    print("=" * 70)
    
    engine = TerminalClearEngine()
    engine.screen_content = ["Line 1", "Line 2"]
    
    result = engine.clear_screen(panel_id="panel_1")
    
    assert result.success, "Temizleme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear screen with panel")
    print("=" * 70)


def test_clear_scrollback():
    """
    Test: Clear scrollback.
    """
    print("=" * 70)
    print("TEST: Clear Scrollback")
    print("=" * 70)
    
    engine = TerminalClearEngine()
    engine.scrollback = ["Line 1", "Line 2", "Line 3"]
    
    result = engine.clear_scrollback()
    
    assert result.success, "Temizleme başarılı olmalı"
    assert result.cleared_count == 3, "3 satır temizlenmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Cleared count: {result.cleared_count}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear scrollback")
    print("=" * 70)


def test_clear_history():
    """
    Test: Clear history.
    """
    print("=" * 70)
    print("TEST: Clear History")
    print("=" * 70)
    
    engine = TerminalClearEngine()
    engine.config.preserve_history = False
    engine.history = ["cmd1", "cmd2"]
    
    result = engine.clear_history()
    
    assert result.success, "Temizleme başarılı olmalı"
    assert result.cleared_count == 2, "2 girdi temizlenmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Cleared count: {result.cleared_count}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear history")
    print("=" * 70)


def test_clear_history_preserved():
    """
    Test: Clear history with preservation.
    """
    print("=" * 70)
    print("TEST: Clear History Preserved")
    print("=" * 70)
    
    engine = TerminalClearEngine()
    engine.config.preserve_history = True
    engine.history = ["cmd1", "cmd2"]
    
    result = engine.clear_history()
    
    assert not result.success, "Temizleme başarısız olmalı (koruma aktif)"
    
    print(f"  Success: {result.success}")
    print(f"  Errors: {result.errors}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear history preserved")
    print("=" * 70)


def test_clear_all():
    """
    Test: Clear all.
    """
    print("=" * 70)
    print("TEST: Clear All")
    print("=" * 70)
    
    engine = TerminalClearEngine()
    engine.config.preserve_history = False
    engine.screen_content = ["Line 1"]
    engine.scrollback = ["Line 2"]
    engine.history = ["cmd1"]
    
    result = engine.clear_all()
    
    assert result.success, "Temizleme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Cleared count: {result.cleared_count}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear all")
    print("=" * 70)


def test_clear_by_panel():
    """
    Test: Clear by panel.
    """
    print("=" * 70)
    print("TEST: Clear By Panel")
    print("=" * 70)
    
    engine = TerminalClearEngine()
    engine.screen_content = ["Line 1", "Line 2"]
    
    result = engine.clear_by_panel("panel_1")
    
    assert result.success, "Temizleme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear by panel")
    print("=" * 70)


def test_reset_terminal():
    """
    Test: Reset terminal.
    """
    print("=" * 70)
    print("TEST: Reset Terminal")
    print("=" * 70)
    
    engine = TerminalClearEngine()
    engine.screen_content = ["Line 1"]
    engine.scrollback = ["Line 2"]
    
    result = engine.reset_terminal()
    
    assert result.success, "Sıfırlama başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Reset terminal")
    print("=" * 70)


def test_flush_buffer():
    """
    Test: Flush buffer.
    """
    print("=" * 70)
    print("TEST: Flush Buffer")
    print("=" * 70)
    
    engine = TerminalClearEngine()
    engine.screen_content = ["Line 1", "Line 2"]
    
    result = engine.flush_buffer()
    
    assert result.success, "Temizleme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Flush buffer")
    print("=" * 70)


def test_purge_data():
    """
    Test: Purge data.
    """
    print("=" * 70)
    print("TEST: Purge Data")
    print("=" * 70)
    
    engine = TerminalClearEngine()
    engine.screen_content = ["Line 1"]
    engine.scrollback = ["Line 2"]
    engine.history = ["cmd1"]
    
    result = engine.purge_data()
    
    assert result.success, "Temizleme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Purge data")
    print("=" * 70)


def test_get_clear_history():
    """
    Test: Get clear history.
    """
    print("=" * 70)
    print("TEST: Get Clear History")
    print("=" * 70)
    
    engine = TerminalClearEngine()
    engine.clear_screen()
    
    history = engine.get_clear_history()
    
    assert len(history) > 0, "Geçmiş olmalı"
    
    print(f"  History: {len(history)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get clear history")
    print("=" * 70)


def test_clear_clear_history():
    """
    Test: Clear clear history.
    """
    print("=" * 70)
    print("TEST: Clear Clear History")
    print("=" * 70)
    
    engine = TerminalClearEngine()
    engine.clear_screen()
    
    result = engine.clear_clear_history()
    
    assert result.success, "Temizleme başarılı olmalı"
    assert len(engine.get_clear_history()) == 0, "Geçmiş temizlenmeli"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear clear history")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    engine = TerminalClearEngine()
    
    new_config = ClearConfig(preserve_history=False)
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
    
    engine = TerminalClearEngine()
    
    config = engine.get_config()
    
    assert config is not None, "Config olmalı"
    assert config.preserve_history == True, "Config eşleşmeli"
    
    print(f"  Preserve history: {config.preserve_history}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


def test_clear_mode_enum():
    """
    Test: ClearMode enum.
    """
    print("=" * 70)
    print("TEST: ClearMode Enum")
    print("=" * 70)
    
    assert ClearMode.SCREEN.value == "screen"
    assert ClearMode.SCROLLBACK.value == "scrollback"
    assert ClearMode.HISTORY.value == "history"
    assert ClearMode.ALL.value == "all"
    
    print(f"  All enum values verified")
    print(f"  Total modes: {len(ClearMode)}")
    
    print("\n" + "=" * 70)
    print("PASS: ClearMode enum")
    print("=" * 70)


def test_clear_scope_enum():
    """
    Test: ClearScope enum.
    """
    print("=" * 70)
    print("TEST: ClearScope Enum")
    print("=" * 70)
    
    assert ClearScope.CURRENT.value == "current"
    assert ClearScope.PANEL.value == "panel"
    assert ClearScope.SESSION.value == "session"
    assert ClearScope.GLOBAL.value == "global"
    
    print(f"  All enum values verified")
    print(f"  Total scopes: {len(ClearScope)}")
    
    print("\n" + "=" * 70)
    print("PASS: ClearScope enum")
    print("=" * 70)


def test_clear_action_enum():
    """
    Test: ClearAction enum.
    """
    print("=" * 70)
    print("TEST: ClearAction Enum")
    print("=" * 70)
    
    assert ClearAction.CLEAR.value == "clear"
    assert ClearAction.RESET.value == "reset"
    assert ClearAction.FLUSH.value == "flush"
    assert ClearAction.PURGE.value == "purge"
    
    print(f"  All enum values verified")
    print(f"  Total actions: {len(ClearAction)}")
    
    print("\n" + "=" * 70)
    print("PASS: ClearAction enum")
    print("=" * 70)


def test_clear_config_dataclass():
    """
    Test: ClearConfig dataclass.
    """
    print("=" * 70)
    print("TEST: ClearConfig Dataclass")
    print("=" * 70)
    
    config = ClearConfig(
        confirm_before_clear=True,
        preserve_history=False
    )
    
    assert config.confirm_before_clear == True, "Confirm eşleşmeli"
    assert config.preserve_history == False, "Preserve history eşleşmeli"
    
    print(f"  Confirm before clear: {config.confirm_before_clear}")
    print(f"  Preserve history: {config.preserve_history}")
    
    print("\n" + "=" * 70)
    print("PASS: ClearConfig dataclass")
    print("=" * 70)


def test_clear_result_dataclass():
    """
    Test: ClearResult dataclass.
    """
    print("=" * 70)
    print("TEST: ClearResult Dataclass")
    print("=" * 70)
    
    result = ClearResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: ClearResult dataclass")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_clear_screen()
        test2 = test_clear_screen_with_panel()
        test3 = test_clear_scrollback()
        test4 = test_clear_history()
        test5 = test_clear_history_preserved()
        test6 = test_clear_all()
        test7 = test_clear_by_panel()
        test8 = test_reset_terminal()
        test9 = test_flush_buffer()
        test10 = test_purge_data()
        test11 = test_get_clear_history()
        test12 = test_clear_clear_history()
        test13 = test_update_config()
        test14 = test_get_config()
        test15 = test_clear_mode_enum()
        test16 = test_clear_scope_enum()
        test17 = test_clear_action_enum()
        test18 = test_clear_config_dataclass()
        test19 = test_clear_result_dataclass()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Clear Screen: {'PASS' if test1 else 'FAIL'}")
        print(f"Clear Screen With Panel: {'PASS' if test2 else 'FAIL'}")
        print(f"Clear Scrollback: {'PASS' if test3 else 'FAIL'}")
        print(f"Clear History: {'PASS' if test4 else 'FAIL'}")
        print(f"Clear History Preserved: {'PASS' if test5 else 'FAIL'}")
        print(f"Clear All: {'PASS' if test6 else 'FAIL'}")
        print(f"Clear By Panel: {'PASS' if test7 else 'FAIL'}")
        print(f"Reset Terminal: {'PASS' if test8 else 'FAIL'}")
        print(f"Flush Buffer: {'PASS' if test9 else 'FAIL'}")
        print(f"Purge Data: {'PASS' if test10 else 'FAIL'}")
        print(f"Get Clear History: {'PASS' if test11 else 'FAIL'}")
        print(f"Clear Clear History: {'PASS' if test12 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test13 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test14 else 'FAIL'}")
        print(f"ClearMode Enum: {'PASS' if test15 else 'FAIL'}")
        print(f"ClearScope Enum: {'PASS' if test16 else 'FAIL'}")
        print(f"ClearAction Enum: {'PASS' if test17 else 'FAIL'}")
        print(f"ClearConfig Dataclass: {'PASS' if test18 else 'FAIL'}")
        print(f"ClearResult Dataclass: {'PASS' if test19 else 'FAIL'}")
        
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
