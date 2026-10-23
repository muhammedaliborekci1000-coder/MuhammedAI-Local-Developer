"""
Quality Test: Terminal Copy/Paste
Terminal copy/paste system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.tools.terminal_copy_paste import (
    TerminalCopyPasteEngine,
    CopyMode,
    PasteMode,
    ClipboardAction,
    ClipboardConfig,
    ClipboardEntry,
    CopyPasteResult
)


def test_copy():
    """
    Test: Copy.
    """
    print("=" * 70)
    print("TEST: Copy")
    print("=" * 70)
    
    engine = TerminalCopyPasteEngine()
    result = engine.copy("Test content")
    
    assert result.success, "Kopyalama başarılı olmalı"
    assert result.content == "Test content", "İçerik eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Content: {result.content}")
    print(f"  Count: {result.count}")
    
    print("\n" + "=" * 70)
    print("PASS: Copy")
    print("=" * 70)


def test_copy_with_details():
    """
    Test: Copy with details.
    """
    print("=" * 70)
    print("TEST: Copy With Details")
    print("=" * 70)
    
    engine = TerminalCopyPasteEngine()
    result = engine.copy(
        "Test content",
        mode=CopyMode.SELECTION,
        source="selection",
        line_number=1,
        panel_id="panel_1"
    )
    
    assert result.success, "Kopyalama başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Entry ID: {result.entry_id}")
    
    print("\n" + "=" * 70)
    print("PASS: Copy with details")
    print("=" * 70)


def test_copy_line():
    """
    Test: Copy line.
    """
    print("=" * 70)
    print("TEST: Copy Line")
    print("=" * 70)
    
    engine = TerminalCopyPasteEngine()
    result = engine.copy_line("Test line", 1, panel_id="panel_1")
    
    assert result.success, "Satır kopyalama başarılı olmalı"
    assert result.content == "Test line", "İçerik eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Content: {result.content}")
    
    print("\n" + "=" * 70)
    print("PASS: Copy line")
    print("=" * 70)


def test_copy_block():
    """
    Test: Copy block.
    """
    print("=" * 70)
    print("TEST: Copy Block")
    print("=" * 70)
    
    engine = TerminalCopyPasteEngine()
    lines = ["Line 1", "Line 2", "Line 3"]
    
    result = engine.copy_block(lines, 1, panel_id="panel_1")
    
    assert result.success, "Blok kopyalama başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Content: {result.content}")
    
    print("\n" + "=" * 70)
    print("PASS: Copy block")
    print("=" * 70)


def test_copy_all():
    """
    Test: Copy all.
    """
    print("=" * 70)
    print("TEST: Copy All")
    print("=" * 70)
    
    engine = TerminalCopyPasteEngine()
    result = engine.copy_all("All content", panel_id="panel_1")
    
    assert result.success, "Tümünü kopyalama başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Content: {result.content}")
    
    print("\n" + "=" * 70)
    print("PASS: Copy all")
    print("=" * 70)


def test_paste():
    """
    Test: Paste.
    """
    print("=" * 70)
    print("TEST: Paste")
    print("=" * 70)
    
    engine = TerminalCopyPasteEngine()
    engine.copy("Test content")
    
    result = engine.paste()
    
    assert result.success, "Yapıştırma başarılı olmalı"
    assert result.content == "Test content", "İçerik eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Content: {result.content}")
    
    print("\n" + "=" * 70)
    print("PASS: Paste")
    print("=" * 70)


def test_paste_insert():
    """
    Test: Paste insert.
    """
    print("=" * 70)
    print("TEST: Paste Insert")
    print("=" * 70)
    
    engine = TerminalCopyPasteEngine()
    engine.copy("Test content")
    
    result = engine.paste_insert()
    
    assert result.success, "Ekleme yapıştırma başarılı olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Paste insert")
    print("=" * 70)


def test_paste_overwrite():
    """
    Test: Paste overwrite.
    """
    print("=" * 70)
    print("TEST: Paste Overwrite")
    print("=" * 70)
    
    engine = TerminalCopyPasteEngine()
    engine.copy("Test content")
    
    result = engine.paste_overwrite()
    
    assert result.success, "Üzerine yazma yapıştırma başarılı olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Paste overwrite")
    print("=" * 70)


def test_paste_append():
    """
    Test: Paste append.
    """
    print("=" * 70)
    print("TEST: Paste Append")
    print("=" * 70)
    
    engine = TerminalCopyPasteEngine()
    engine.copy("Test content")
    
    result = engine.paste_append()
    
    assert result.success, "Ekleme yapıştırma başarılı olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Paste append")
    print("=" * 70)


def test_cut():
    """
    Test: Cut.
    """
    print("=" * 70)
    print("TEST: Cut")
    print("=" * 70)
    
    engine = TerminalCopyPasteEngine()
    result = engine.cut("Test content")
    
    assert result.success, "Kesme başarılı olmalı"
    assert result.content == "Test content", "İçerik eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Content: {result.content}")
    
    print("\n" + "=" * 70)
    print("PASS: Cut")
    print("=" * 70)


def test_clear_clipboard():
    """
    Test: Clear clipboard.
    """
    print("=" * 70)
    print("TEST: Clear Clipboard")
    print("=" * 70)
    
    engine = TerminalCopyPasteEngine()
    engine.copy("Test content")
    
    result = engine.clear_clipboard()
    
    assert result.success, "Temizleme başarılı olmalı"
    assert engine.get_clipboard() is None, "Pano boş olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear clipboard")
    print("=" * 70)


def test_get_clipboard():
    """
    Test: Get clipboard.
    """
    print("=" * 70)
    print("TEST: Get Clipboard")
    print("=" * 70)
    
    engine = TerminalCopyPasteEngine()
    engine.copy("Test content")
    
    clipboard = engine.get_clipboard()
    
    assert clipboard is not None, "Pano olmalı"
    assert clipboard.content == "Test content", "İçerik eşleşmeli"
    
    print(f"  Content: {clipboard.content}")
    
    print("\n" + "=" * 70)
    print("PASS: Get clipboard")
    print("=" * 70)


def test_get_clipboard_history():
    """
    Test: Get clipboard history.
    """
    print("=" * 70)
    print("TEST: Get Clipboard History")
    print("=" * 70)
    
    engine = TerminalCopyPasteEngine()
    engine.copy("Content 1")
    engine.copy("Content 2")
    
    history = engine.get_clipboard_history()
    
    assert len(history) == 2, "2 girdi olmalı"
    
    print(f"  History: {len(history)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get clipboard history")
    print("=" * 70)


def test_restore_from_history():
    """
    Test: Restore from history.
    """
    print("=" * 70)
    print("TEST: Restore From History")
    print("=" * 70)
    
    engine = TerminalCopyPasteEngine()
    engine.copy("Content 1")
    result1 = engine.copy("Content 2")
    
    result = engine.restore_from_history(result1.entry_id)
    
    assert result.success, "Geri yükleme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Restore from history")
    print("=" * 70)


def test_clear_history():
    """
    Test: Clear history.
    """
    print("=" * 70)
    print("TEST: Clear History")
    print("=" * 70)
    
    engine = TerminalCopyPasteEngine()
    engine.copy("Content 1")
    
    result = engine.clear_history()
    
    assert result.success, "Temizleme başarılı olmalı"
    assert len(engine.get_clipboard_history()) == 0, "Geçmiş temizlenmeli"
    
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
    
    engine = TerminalCopyPasteEngine()
    
    new_config = ClipboardConfig(max_history=100)
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
    
    engine = TerminalCopyPasteEngine()
    
    config = engine.get_config()
    
    assert config is not None, "Config olmalı"
    assert config.max_history == 50, "Config eşleşmeli"
    
    print(f"  Max history: {config.max_history}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


def test_copy_mode_enum():
    """
    Test: CopyMode enum.
    """
    print("=" * 70)
    print("TEST: CopyMode Enum")
    print("=" * 70)
    
    assert CopyMode.SELECTION.value == "selection"
    assert CopyMode.LINE.value == "line"
    assert CopyMode.BLOCK.value == "block"
    assert CopyMode.ALL.value == "all"
    
    print(f"  All enum values verified")
    print(f"  Total modes: {len(CopyMode)}")
    
    print("\n" + "=" * 70)
    print("PASS: CopyMode enum")
    print("=" * 70)


def test_paste_mode_enum():
    """
    Test: PasteMode enum.
    """
    print("=" * 70)
    print("TEST: PasteMode Enum")
    print("=" * 70)
    
    assert PasteMode.INSERT.value == "insert"
    assert PasteMode.OVERWRITE.value == "overwrite"
    assert PasteMode.APPEND.value == "append"
    
    print(f"  All enum values verified")
    print(f"  Total modes: {len(PasteMode)}")
    
    print("\n" + "=" * 70)
    print("PASS: PasteMode enum")
    print("=" * 70)


def test_clipboard_action_enum():
    """
    Test: ClipboardAction enum.
    """
    print("=" * 70)
    print("TEST: ClipboardAction Enum")
    print("=" * 70)
    
    assert ClipboardAction.COPY.value == "copy"
    assert ClipboardAction.CUT.value == "cut"
    assert ClipboardAction.PASTE.value == "paste"
    assert ClipboardAction.CLEAR.value == "clear"
    
    print(f"  All enum values verified")
    print(f"  Total actions: {len(ClipboardAction)}")
    
    print("\n" + "=" * 70)
    print("PASS: ClipboardAction enum")
    print("=" * 70)


def test_clipboard_config_dataclass():
    """
    Test: ClipboardConfig dataclass.
    """
    print("=" * 70)
    print("TEST: ClipboardConfig Dataclass")
    print("=" * 70)
    
    config = ClipboardConfig(
        max_history=100,
        enable_history=False
    )
    
    assert config.max_history == 100, "Max history eşleşmeli"
    assert config.enable_history == False, "Enable history eşleşmeli"
    
    print(f"  Max history: {config.max_history}")
    print(f"  Enable history: {config.enable_history}")
    
    print("\n" + "=" * 70)
    print("PASS: ClipboardConfig dataclass")
    print("=" * 70)


def test_clipboard_entry_dataclass():
    """
    Test: ClipboardEntry dataclass.
    """
    print("=" * 70)
    print("TEST: ClipboardEntry Dataclass")
    print("=" * 70)
    
    entry = ClipboardEntry(
        id="clipboard_1",
        content="Test content",
        timestamp="2024-01-01T00:00:00"
    )
    
    assert entry.id == "clipboard_1", "ID eşleşmeli"
    assert entry.content == "Test content", "İçerik eşleşmeli"
    
    print(f"  ID: {entry.id}")
    print(f"  Content: {entry.content}")
    
    print("\n" + "=" * 70)
    print("PASS: ClipboardEntry dataclass")
    print("=" * 70)


def test_copy_paste_result_dataclass():
    """
    Test: CopyPasteResult dataclass.
    """
    print("=" * 70)
    print("TEST: CopyPasteResult Dataclass")
    print("=" * 70)
    
    result = CopyPasteResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: CopyPasteResult dataclass")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_copy()
        test2 = test_copy_with_details()
        test3 = test_copy_line()
        test4 = test_copy_block()
        test5 = test_copy_all()
        test6 = test_paste()
        test7 = test_paste_insert()
        test8 = test_paste_overwrite()
        test9 = test_paste_append()
        test10 = test_cut()
        test11 = test_clear_clipboard()
        test12 = test_get_clipboard()
        test13 = test_get_clipboard_history()
        test14 = test_restore_from_history()
        test15 = test_clear_history()
        test16 = test_update_config()
        test17 = test_get_config()
        test18 = test_copy_mode_enum()
        test19 = test_paste_mode_enum()
        test20 = test_clipboard_action_enum()
        test21 = test_clipboard_config_dataclass()
        test22 = test_clipboard_entry_dataclass()
        test23 = test_copy_paste_result_dataclass()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Copy: {'PASS' if test1 else 'FAIL'}")
        print(f"Copy With Details: {'PASS' if test2 else 'FAIL'}")
        print(f"Copy Line: {'PASS' if test3 else 'FAIL'}")
        print(f"Copy Block: {'PASS' if test4 else 'FAIL'}")
        print(f"Copy All: {'PASS' if test5 else 'FAIL'}")
        print(f"Paste: {'PASS' if test6 else 'FAIL'}")
        print(f"Paste Insert: {'PASS' if test7 else 'FAIL'}")
        print(f"Paste Overwrite: {'PASS' if test8 else 'FAIL'}")
        print(f"Paste Append: {'PASS' if test9 else 'FAIL'}")
        print(f"Cut: {'PASS' if test10 else 'FAIL'}")
        print(f"Clear Clipboard: {'PASS' if test11 else 'FAIL'}")
        print(f"Get Clipboard: {'PASS' if test12 else 'FAIL'}")
        print(f"Get Clipboard History: {'PASS' if test13 else 'FAIL'}")
        print(f"Restore From History: {'PASS' if test14 else 'FAIL'}")
        print(f"Clear History: {'PASS' if test15 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test16 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test17 else 'FAIL'}")
        print(f"CopyMode Enum: {'PASS' if test18 else 'FAIL'}")
        print(f"PasteMode Enum: {'PASS' if test19 else 'FAIL'}")
        print(f"ClipboardAction Enum: {'PASS' if test20 else 'FAIL'}")
        print(f"ClipboardConfig Dataclass: {'PASS' if test21 else 'FAIL'}")
        print(f"ClipboardEntry Dataclass: {'PASS' if test22 else 'FAIL'}")
        print(f"CopyPasteResult Dataclass: {'PASS' if test23 else 'FAIL'}")
        
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
