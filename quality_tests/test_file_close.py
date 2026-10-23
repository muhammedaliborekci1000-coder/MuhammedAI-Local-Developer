"""
Quality Test: File Close
File close system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.file_close import (
    FileCloseEngine,
    CloseMode,
    SavePrompt,
    FileState,
    CloseConfig,
    CloseResult
)


def test_close_file():
    """
    Test: Close file.
    """
    print("=" * 70)
    print("TEST: Close File")
    print("=" * 70)
    
    engine = FileCloseEngine()
    engine.open_file("test.txt", "Hello World")
    
    result = engine.close_file("test.txt", force=True)
    
    assert result.success, "Kapatma başarılı olmalı"
    assert result.closed_count == 1, "1 dosya kapatılmalı"
    assert "test.txt" not in engine.get_open_files(), "Dosya kapatılmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Close file")
    print("=" * 70)


def test_close_all():
    """
    Test: Close all.
    """
    print("=" * 70)
    print("TEST: Close All")
    print("=" * 70)
    
    engine = FileCloseEngine()
    engine.open_file("test1.txt", "Content 1")
    engine.open_file("test2.txt", "Content 2")
    engine.open_file("test3.txt", "Content 3")
    
    result = engine.close_all(force=True)
    
    assert result.success, "Kapatma başarılı olmalı"
    assert result.closed_count == 3, "3 dosya kapatılmalı"
    assert len(engine.get_open_files()) == 0, "Tüm dosyalar kapatılmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Close all")
    print("=" * 70)


def test_close_others():
    """
    Test: Close others.
    """
    print("=" * 70)
    print("TEST: Close Others")
    print("=" * 70)
    
    engine = FileCloseEngine()
    engine.open_file("test1.txt", "Content 1")
    engine.open_file("test2.txt", "Content 2")
    engine.open_file("test3.txt", "Content 3")
    
    result = engine.close_others("test2.txt", force=True)
    
    assert result.success, "Kapatma başarılı olmalı"
    assert result.closed_count == 2, "2 dosya kapatılmalı"
    assert "test2.txt" in engine.get_open_files(), "test2.txt açık kalmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Close others")
    print("=" * 70)


def test_close_to_right():
    """
    Test: Close to right.
    """
    print("=" * 70)
    print("TEST: Close to Right")
    print("=" * 70)
    
    engine = FileCloseEngine()
    engine.open_file("test1.txt", "Content 1")
    engine.open_file("test2.txt", "Content 2")
    engine.open_file("test3.txt", "Content 3")
    
    result = engine.close_to_right("test1.txt", force=True)
    
    assert result.success, "Kapatma başarılı olmalı"
    assert "test1.txt" in engine.get_open_files(), "test1.txt açık kalmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Close to right")
    print("=" * 70)


def test_close_to_left():
    """
    Test: Close to left.
    """
    print("=" * 70)
    print("TEST: Close to Left")
    print("=" * 70)
    
    engine = FileCloseEngine()
    engine.open_file("test1.txt", "Content 1")
    engine.open_file("test2.txt", "Content 2")
    engine.open_file("test3.txt", "Content 3")
    
    result = engine.close_to_left("test3.txt", force=True)
    
    assert result.success, "Kapatma başarılı olmalı"
    assert "test3.txt" in engine.get_open_files(), "test3.txt açık kalmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Close to left")
    print("=" * 70)


def test_has_unsaved_changes():
    """
    Test: Has unsaved changes.
    """
    print("=" * 70)
    print("TEST: Has Unsaved Changes")
    print("=" * 70)
    
    engine = FileCloseEngine()
    engine.open_file("test.txt", "Hello World")
    
    has_changes = engine.has_unsaved_changes("test.txt")
    assert has_changes == False, "Değişiklik olmamalı"
    
    engine.update_content("test.txt", "Hello World Updated")
    has_changes = engine.has_unsaved_changes("test.txt")
    assert has_changes == True, "Değişiklik olmalı"
    
    print(f"  Has unsaved changes: {has_changes}")
    
    print("\n" + "=" * 70)
    print("PASS: Has unsaved changes")
    print("=" * 70)


def test_get_open_files():
    """
    Test: Get open files.
    """
    print("=" * 70)
    print("TEST: Get Open Files")
    print("=" * 70)
    
    engine = FileCloseEngine()
    engine.open_file("test1.txt", "Content 1")
    engine.open_file("test2.txt", "Content 2")
    
    open_files = engine.get_open_files()
    
    assert len(open_files) == 2, "2 açık dosya olmalı"
    assert "test1.txt" in open_files, "test1.txt olmalı"
    assert "test2.txt" in open_files, "test2.txt olmalı"
    
    print(f"  Open files: {len(open_files)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get open files")
    print("=" * 70)


def test_get_file_state():
    """
    Test: Get file state.
    """
    print("=" * 70)
    print("TEST: Get File State")
    print("=" * 70)
    
    engine = FileCloseEngine()
    engine.open_file("test.txt", "Hello World")
    
    state = engine.get_file_state("test.txt")
    
    assert state is not None, "Durum olmalı"
    assert state.path == "test.txt", "Yol eşleşmeli"
    assert state.content == "Hello World", "İçerik eşleşmeli"
    
    print(f"  Path: {state.path}")
    print(f"  Modified: {state.modified}")
    
    print("\n" + "=" * 70)
    print("PASS: Get file state")
    print("=" * 70)


def test_reopen_file():
    """
    Test: Reopen file.
    """
    print("=" * 70)
    print("TEST: Reopen File")
    print("=" * 70)
    
    engine = FileCloseEngine()
    engine.open_file("test.txt", "Hello World")
    engine.close_file("test.txt", force=True)
    
    result = engine.reopen_file("test.txt")
    
    assert result.success, "Açma başarılı olmalı"
    assert "test.txt" in engine.get_open_files(), "Dosya açılmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Reopen file")
    print("=" * 70)


def test_get_close_history():
    """
    Test: Get close history.
    """
    print("=" * 70)
    print("TEST: Get Close History")
    print("=" * 70)
    
    engine = FileCloseEngine()
    engine.open_file("test.txt", "Hello World")
    engine.close_file("test.txt", force=True)
    
    history = engine.get_close_history()
    
    assert len(history) > 0, "Geçmiş olmalı"
    
    print(f"  History: {len(history)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get close history")
    print("=" * 70)


def test_clear_history():
    """
    Test: Clear history.
    """
    print("=" * 70)
    print("TEST: Clear History")
    print("=" * 70)
    
    engine = FileCloseEngine()
    engine.open_file("test.txt", "Hello World")
    engine.close_file("test.txt", force=True)
    
    result = engine.clear_history()
    
    assert result.success, "Temizleme başarılı olmalı"
    assert len(engine.get_close_history()) == 0, "Geçmiş temizlenmeli"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear history")
    print("=" * 70)


def test_get_recent_files():
    """
    Test: Get recent files.
    """
    print("=" * 70)
    print("TEST: Get Recent Files")
    print("=" * 70)
    
    engine = FileCloseEngine()
    engine.open_file("test1.txt", "Content 1")
    engine.open_file("test2.txt", "Content 2")
    
    recent_files = engine.get_recent_files()
    
    assert len(recent_files) > 0, "Son dosyalar olmalı"
    
    print(f"  Recent files: {len(recent_files)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get recent files")
    print("=" * 70)


def test_clear_recent_files():
    """
    Test: Clear recent files.
    """
    print("=" * 70)
    print("TEST: Clear Recent Files")
    print("=" * 70)
    
    engine = FileCloseEngine()
    engine.open_file("test.txt", "Hello World")
    
    result = engine.clear_recent_files()
    
    assert result.success, "Temizleme başarılı olmalı"
    assert len(engine.get_recent_files()) == 0, "Son dosyalar temizlenmeli"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear recent files")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    engine = FileCloseEngine()
    
    new_config = CloseConfig(mode=CloseMode.CLOSE_ALL, save_prompt=SavePrompt.NEVER)
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
    
    engine = FileCloseEngine()
    
    config = engine.get_config()
    
    assert config is not None, "Config olmalı"
    assert config.mode == CloseMode.CLOSE, "Config eşleşmeli"
    
    print(f"  Mode: {config.mode.value}")
    print(f"  Save prompt: {config.save_prompt.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


def test_close_mode_enum():
    """
    Test: CloseMode enum.
    """
    print("=" * 70)
    print("TEST: CloseMode Enum")
    print("=" * 70)
    
    assert CloseMode.CLOSE.value == "close"
    assert CloseMode.CLOSE_ALL.value == "close_all"
    assert CloseMode.CLOSE_OTHERS.value == "close_others"
    assert CloseMode.CLOSE_TO_RIGHT.value == "close_to_right"
    assert CloseMode.CLOSE_TO_LEFT.value == "close_to_left"
    
    print(f"  All enum values verified")
    print(f"  Total modes: {len(CloseMode)}")
    
    print("\n" + "=" * 70)
    print("PASS: CloseMode enum")
    print("=" * 70)


def test_save_prompt_enum():
    """
    Test: SavePrompt enum.
    """
    print("=" * 70)
    print("TEST: SavePrompt Enum")
    print("=" * 70)
    
    assert SavePrompt.ALWAYS.value == "always"
    assert SavePrompt.NEVER.value == "never"
    assert SavePrompt.PROMPT.value == "prompt"
    
    print(f"  All enum values verified")
    print(f"  Total prompts: {len(SavePrompt)}")
    
    print("\n" + "=" * 70)
    print("PASS: SavePrompt enum")
    print("=" * 70)


def test_file_state_dataclass():
    """
    Test: FileState dataclass.
    """
    print("=" * 70)
    print("TEST: FileState Dataclass")
    print("=" * 70)
    
    state = FileState(
        path="/test/file.txt",
        content="Hello World",
        modified=True
    )
    
    assert state.path == "/test/file.txt", "Path eşleşmeli"
    assert state.content == "Hello World", "Content eşleşmeli"
    assert state.modified == True, "Modified eşleşmeli"
    
    print(f"  Path: {state.path}")
    print(f"  Modified: {state.modified}")
    
    print("\n" + "=" * 70)
    print("PASS: FileState dataclass")
    print("=" * 70)


def test_close_config_dataclass():
    """
    Test: CloseConfig dataclass.
    """
    print("=" * 70)
    print("TEST: CloseConfig Dataclass")
    print("=" * 70)
    
    config = CloseConfig(
        mode=CloseMode.CLOSE_ALL,
        save_prompt=SavePrompt.NEVER,
        auto_save_before_close=True
    )
    
    assert config.mode == CloseMode.CLOSE_ALL, "Mode eşleşmeli"
    assert config.save_prompt == SavePrompt.NEVER, "Save prompt eşleşmeli"
    assert config.auto_save_before_close == True, "Auto save eşleşmeli"
    
    print(f"  Mode: {config.mode.value}")
    print(f"  Save prompt: {config.save_prompt.value}")
    print(f"  Auto save before close: {config.auto_save_before_close}")
    
    print("\n" + "=" * 70)
    print("PASS: CloseConfig dataclass")
    print("=" * 70)


def test_close_result_dataclass():
    """
    Test: CloseResult dataclass.
    """
    print("=" * 70)
    print("TEST: CloseResult Dataclass")
    print("=" * 70)
    
    result = CloseResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: CloseResult dataclass")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_close_file()
        test2 = test_close_all()
        test3 = test_close_others()
        test4 = test_close_to_right()
        test5 = test_close_to_left()
        test6 = test_has_unsaved_changes()
        test7 = test_get_open_files()
        test8 = test_get_file_state()
        test9 = test_reopen_file()
        test10 = test_get_close_history()
        test11 = test_clear_history()
        test12 = test_get_recent_files()
        test13 = test_clear_recent_files()
        test14 = test_update_config()
        test15 = test_get_config()
        test16 = test_close_mode_enum()
        test17 = test_save_prompt_enum()
        test18 = test_file_state_dataclass()
        test19 = test_close_config_dataclass()
        test20 = test_close_result_dataclass()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Close File: {'PASS' if test1 else 'FAIL'}")
        print(f"Close All: {'PASS' if test2 else 'FAIL'}")
        print(f"Close Others: {'PASS' if test3 else 'FAIL'}")
        print(f"Close to Right: {'PASS' if test4 else 'FAIL'}")
        print(f"Close to Left: {'PASS' if test5 else 'FAIL'}")
        print(f"Has Unsaved Changes: {'PASS' if test6 else 'FAIL'}")
        print(f"Get Open Files: {'PASS' if test7 else 'FAIL'}")
        print(f"Get File State: {'PASS' if test8 else 'FAIL'}")
        print(f"Reopen File: {'PASS' if test9 else 'FAIL'}")
        print(f"Get Close History: {'PASS' if test10 else 'FAIL'}")
        print(f"Clear History: {'PASS' if test11 else 'FAIL'}")
        print(f"Get Recent Files: {'PASS' if test12 else 'FAIL'}")
        print(f"Clear Recent Files: {'PASS' if test13 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test14 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test15 else 'FAIL'}")
        print(f"CloseMode Enum: {'PASS' if test16 else 'FAIL'}")
        print(f"SavePrompt Enum: {'PASS' if test17 else 'FAIL'}")
        print(f"FileState Dataclass: {'PASS' if test18 else 'FAIL'}")
        print(f"CloseConfig Dataclass: {'PASS' if test19 else 'FAIL'}")
        print(f"CloseResult Dataclass: {'PASS' if test20 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14, test15, test16, test17, test18, test19, test20])
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
