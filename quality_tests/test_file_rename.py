"""
Quality Test: File Rename
File rename system testleri.
"""

import sys
import os
import tempfile
import shutil

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.file_rename import (
    FileRenameEngine,
    RenameMode,
    RenameScope,
    RenameTarget,
    RenameConfig,
    RenameResult
)


def test_rename_file():
    """
    Test: Rename file.
    """
    print("=" * 70)
    print("TEST: Rename File")
    print("=" * 70)
    
    # Create temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as f:
        temp_file = f.name
        f.write(b"test content")
    
    temp_dir = os.path.dirname(temp_file)
    new_file = os.path.join(temp_dir, "renamed_file.txt")
    
    try:
        engine = FileRenameEngine()
        result = engine.rename_file(temp_file, new_file)
        
        assert result.success, "Yeniden adlandırma başarılı olmalı"
        assert not os.path.exists(temp_file), "Eski dosya olmamalı"
        assert os.path.exists(new_file), "Yeni dosya olmalı"
        
        print(f"  Success: {result.success}")
        print(f"  Message: {result.message}")
        
        print("\n" + "=" * 70)
        print("PASS: Rename file")
        print("=" * 70)
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)
        if os.path.exists(new_file):
            os.remove(new_file)


def test_rename_directory():
    """
    Test: Rename directory.
    """
    print("=" * 70)
    print("TEST: Rename Directory")
    print("=" * 70)
    
    # Create temp directory
    temp_dir = tempfile.mkdtemp()
    parent_dir = os.path.dirname(temp_dir)
    new_dir = os.path.join(parent_dir, "renamed_dir")
    
    try:
        engine = FileRenameEngine()
        result = engine.rename_directory(temp_dir, new_dir)
        
        assert result.success, "Yeniden adlandırma başarılı olmalı"
        assert not os.path.exists(temp_dir), "Eski dizin olmamalı"
        assert os.path.exists(new_dir), "Yeni dizin olmalı"
        
        print(f"  Success: {result.success}")
        print(f"  Message: {result.message}")
        
        print("\n" + "=" * 70)
        print("PASS: Rename directory")
        print("=" * 70)
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        if os.path.exists(new_dir):
            shutil.rmtree(new_dir)


def test_rename_multiple():
    """
    Test: Rename multiple.
    """
    print("=" * 70)
    print("TEST: Rename Multiple")
    print("=" * 70)
    
    # Create temp files
    temp_files = []
    new_files = []
    temp_dir = tempfile.mkdtemp()
    
    for i in range(3):
        temp_file = os.path.join(temp_dir, f"file{i}.txt")
        with open(temp_file, 'w') as f:
            f.write("test content")
        temp_files.append(temp_file)
        new_files.append(os.path.join(temp_dir, f"renamed{i}.txt"))
    
    try:
        engine = FileRenameEngine()
        targets = [RenameTarget(old_path=temp_files[i], new_path=new_files[i], is_directory=False) for i in range(3)]
        result = engine.rename_multiple(targets)
        
        assert result.success, "Yeniden adlandırma başarılı olmalı"
        assert result.renamed_count == 3, "3 dosya yeniden adlandırılmalı"
        
        print(f"  Success: {result.success}")
        print(f"  Renamed count: {result.renamed_count}")
        
        print("\n" + "=" * 70)
        print("PASS: Rename multiple")
        print("=" * 70)
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def test_can_rename():
    """
    Test: Can rename.
    """
    print("=" * 70)
    print("TEST: Can Rename")
    print("=" * 70)
    
    # Create temp file
    with tempfile.NamedTemporaryFile(delete=False) as f:
        temp_file = f.name
        f.write(b"test content")
    
    try:
        engine = FileRenameEngine()
        can_rename = engine.can_rename(temp_file)
        
        assert can_rename == True, "Yeniden adlandırılabilir olmalı"
        
        print(f"  Can rename: {can_rename}")
        
        print("\n" + "=" * 70)
        print("PASS: Can rename")
        print("=" * 70)
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)


def test_get_file_info():
    """
    Test: Get file info.
    """
    print("=" * 70)
    print("TEST: Get File Info")
    print("=" * 70)
    
    # Create temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as f:
        temp_file = f.name
        f.write(b"test content")
    
    try:
        engine = FileRenameEngine()
        info = engine.get_file_info(temp_file)
        
        assert info is not None, "Bilgi olmalı"
        assert info["name"] == os.path.basename(temp_file), "İsim eşleşmeli"
        assert info["is_directory"] == False, "Dosya olmalı"
        
        print(f"  Name: {info['name']}")
        print(f"  Is directory: {info['is_directory']}")
        print(f"  Size: {info['size']}")
        
        print("\n" + "=" * 70)
        print("PASS: Get file info")
        print("=" * 70)
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)


def test_undo_rename():
    """
    Test: Undo rename.
    """
    print("=" * 70)
    print("TEST: Undo Rename")
    print("=" * 70)
    
    # Create temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as f:
        temp_file = f.name
        f.write(b"test content")
    
    temp_dir = os.path.dirname(temp_file)
    new_file = os.path.join(temp_dir, "renamed_file.txt")
    
    try:
        engine = FileRenameEngine()
        engine.rename_file(temp_file, new_file)
        
        result = engine.undo_rename(new_file)
        
        assert result.success, "Geri alma başarılı olmalı"
        
        print(f"  Success: {result.success}")
        print(f"  Message: {result.message}")
        
        print("\n" + "=" * 70)
        print("PASS: Undo rename")
        print("=" * 70)
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)
        if os.path.exists(new_file):
            os.remove(new_file)


def test_get_rename_history():
    """
    Test: Get rename history.
    """
    print("=" * 70)
    print("TEST: Get Rename History")
    print("=" * 70)
    
    # Create temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as f:
        temp_file = f.name
        f.write(b"test content")
    
    temp_dir = os.path.dirname(temp_file)
    new_file = os.path.join(temp_dir, "renamed_file.txt")
    
    try:
        engine = FileRenameEngine()
        engine.rename_file(temp_file, new_file)
        
        history = engine.get_rename_history()
        
        assert len(history) > 0, "Geçmiş olmalı"
        
        print(f"  History: {len(history)}")
        
        print("\n" + "=" * 70)
        print("PASS: Get rename history")
        print("=" * 70)
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)
        if os.path.exists(new_file):
            os.remove(new_file)


def test_clear_history():
    """
    Test: Clear history.
    """
    print("=" * 70)
    print("TEST: Clear History")
    print("=" * 70)
    
    # Create temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as f:
        temp_file = f.name
        f.write(b"test content")
    
    temp_dir = os.path.dirname(temp_file)
    new_file = os.path.join(temp_dir, "renamed_file.txt")
    
    try:
        engine = FileRenameEngine()
        engine.rename_file(temp_file, new_file)
        
        result = engine.clear_history()
        
        assert result.success, "Temizleme başarılı olmalı"
        assert len(engine.get_rename_history()) == 0, "Geçmiş temizlenmeli"
        
        print(f"  Success: {result.success}")
        
        print("\n" + "=" * 70)
        print("PASS: Clear history")
        print("=" * 70)
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)
        if os.path.exists(new_file):
            os.remove(new_file)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    engine = FileRenameEngine()
    
    new_config = RenameConfig(mode=RenameMode.CASE_CHANGE)
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
    
    engine = FileRenameEngine()
    
    config = engine.get_config()
    
    assert config is not None, "Config olmalı"
    assert config.mode == RenameMode.SIMPLE, "Config eşleşmeli"
    
    print(f"  Mode: {config.mode.value}")
    print(f"  Require confirmation: {config.require_confirmation}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


def test_rename_mode_enum():
    """
    Test: RenameMode enum.
    """
    print("=" * 70)
    print("TEST: RenameMode Enum")
    print("=" * 70)
    
    assert RenameMode.SIMPLE.value == "simple"
    assert RenameMode.CASE_CHANGE.value == "case_change"
    assert RenameMode.PREFIX_SUFFIX.value == "prefix_suffix"
    assert RenameMode.PATTERN.value == "pattern"
    
    print(f"  All enum values verified")
    print(f"  Total modes: {len(RenameMode)}")
    
    print("\n" + "=" * 70)
    print("PASS: RenameMode enum")
    print("=" * 70)


def test_rename_scope_enum():
    """
    Test: RenameScope enum.
    """
    print("=" * 70)
    print("TEST: RenameScope Enum")
    print("=" * 70)
    
    assert RenameScope.FILE.value == "file"
    assert RenameScope.DIRECTORY.value == "directory"
    assert RenameScope.MULTIPLE.value == "multiple"
    
    print(f"  All enum values verified")
    print(f"  Total scopes: {len(RenameScope)}")
    
    print("\n" + "=" * 70)
    print("PASS: RenameScope enum")
    print("=" * 70)


def test_rename_target_dataclass():
    """
    Test: RenameTarget dataclass.
    """
    print("=" * 70)
    print("TEST: RenameTarget Dataclass")
    print("=" * 70)
    
    target = RenameTarget(
        old_path="/test/old.txt",
        new_path="/test/new.txt",
        is_directory=False
    )
    
    assert target.old_path == "/test/old.txt", "Old path eşleşmeli"
    assert target.new_path == "/test/new.txt", "New path eşleşmeli"
    assert target.is_directory == False, "Is directory eşleşmeli"
    
    print(f"  Old path: {target.old_path}")
    print(f"  New path: {target.new_path}")
    print(f"  Is directory: {target.is_directory}")
    
    print("\n" + "=" * 70)
    print("PASS: RenameTarget dataclass")
    print("=" * 70)


def test_rename_config_dataclass():
    """
    Test: RenameConfig dataclass.
    """
    print("=" * 70)
    print("TEST: RenameConfig Dataclass")
    print("=" * 70)
    
    config = RenameConfig(
        mode=RenameMode.CASE_CHANGE,
        require_confirmation=True,
        show_notification=True
    )
    
    assert config.mode == RenameMode.CASE_CHANGE, "Mode eşleşmeli"
    assert config.require_confirmation == True, "Require confirmation eşleşmeli"
    assert config.show_notification == True, "Show notification eşleşmeli"
    
    print(f"  Mode: {config.mode.value}")
    print(f"  Require confirmation: {config.require_confirmation}")
    print(f"  Show notification: {config.show_notification}")
    
    print("\n" + "=" * 70)
    print("PASS: RenameConfig dataclass")
    print("=" * 70)


def test_rename_result_dataclass():
    """
    Test: RenameResult dataclass.
    """
    print("=" * 70)
    print("TEST: RenameResult Dataclass")
    print("=" * 70)
    
    result = RenameResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: RenameResult dataclass")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_rename_file()
        test2 = test_rename_directory()
        test3 = test_rename_multiple()
        test4 = test_can_rename()
        test5 = test_get_file_info()
        test6 = test_undo_rename()
        test7 = test_get_rename_history()
        test8 = test_clear_history()
        test9 = test_update_config()
        test10 = test_get_config()
        test11 = test_rename_mode_enum()
        test12 = test_rename_scope_enum()
        test13 = test_rename_target_dataclass()
        test14 = test_rename_config_dataclass()
        test15 = test_rename_result_dataclass()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Rename File: {'PASS' if test1 else 'FAIL'}")
        print(f"Rename Directory: {'PASS' if test2 else 'FAIL'}")
        print(f"Rename Multiple: {'PASS' if test3 else 'FAIL'}")
        print(f"Can Rename: {'PASS' if test4 else 'FAIL'}")
        print(f"Get File Info: {'PASS' if test5 else 'FAIL'}")
        print(f"Undo Rename: {'PASS' if test6 else 'FAIL'}")
        print(f"Get Rename History: {'PASS' if test7 else 'FAIL'}")
        print(f"Clear History: {'PASS' if test8 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test9 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test10 else 'FAIL'}")
        print(f"RenameMode Enum: {'PASS' if test11 else 'FAIL'}")
        print(f"RenameScope Enum: {'PASS' if test12 else 'FAIL'}")
        print(f"RenameTarget Dataclass: {'PASS' if test13 else 'FAIL'}")
        print(f"RenameConfig Dataclass: {'PASS' if test14 else 'FAIL'}")
        print(f"RenameResult Dataclass: {'PASS' if test15 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14, test15])
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
