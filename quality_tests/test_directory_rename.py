"""
Quality Test: Directory Rename
Directory rename system testleri.
"""

import sys
import os
import tempfile
import shutil

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.directory_rename import (
    DirectoryRenameEngine,
    RenameMode,
    RenameConfig,
    RenameResult
)


def test_rename_directory():
    """
    Test: Rename directory.
    """
    print("=" * 70)
    print("TEST: Rename Directory")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp()
    old_dir = os.path.join(temp_dir, "old_dir")
    new_dir = os.path.join(temp_dir, "new_dir")
    os.makedirs(old_dir)
    
    try:
        engine = DirectoryRenameEngine()
        result = engine.rename_directory(old_dir, new_dir)
        
        assert result.success, "Yeniden adlandırma başarılı olmalı"
        assert not os.path.exists(old_dir), "Eski yol olmamalı"
        assert os.path.exists(new_dir), "Yeni yol olmalı"
        
        print(f"  Success: {result.success}")
        print(f"  Message: {result.message}")
        
        print("\n" + "=" * 70)
        print("PASS: Rename directory")
        print("=" * 70)
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def test_rename_force():
    """
    Test: Rename force.
    """
    print("=" * 70)
    print("TEST: Rename Force")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp()
    old_dir = os.path.join(temp_dir, "old_dir")
    new_dir = os.path.join(temp_dir, "new_dir")
    os.makedirs(old_dir)
    os.makedirs(new_dir)
    
    try:
        config = RenameConfig(mode=RenameMode.FORCE)
        engine = DirectoryRenameEngine(config)
        result = engine.rename_directory(old_dir, new_dir)
        
        assert result.success, "Yeniden adlandırma başarılı olmalı"
        assert not os.path.exists(old_dir), "Eski yol olmamalı"
        assert os.path.exists(new_dir), "Yeni yol olmalı"
        
        print(f"  Success: {result.success}")
        print(f"  Message: {result.message}")
        
        print("\n" + "=" * 70)
        print("PASS: Rename force")
        print("=" * 70)
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def test_rename_multiple():
    """
    Test: Rename multiple directories.
    """
    print("=" * 70)
    print("TEST: Rename Multiple Directories")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp()
    dir1 = os.path.join(temp_dir, "dir1")
    dir2 = os.path.join(temp_dir, "dir2")
    new_dir1 = os.path.join(temp_dir, "new_dir1")
    new_dir2 = os.path.join(temp_dir, "new_dir2")
    os.makedirs(dir1)
    os.makedirs(dir2)
    
    try:
        engine = DirectoryRenameEngine()
        result = engine.rename_multiple([(dir1, new_dir1), (dir2, new_dir2)])
        
        assert result.success, "Yeniden adlandırma başarılı olmalı"
        
        print(f"  Success: {result.success}")
        print(f"  Message: {result.message}")
        
        print("\n" + "=" * 70)
        print("PASS: Rename multiple directories")
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
    
    temp_dir = tempfile.mkdtemp()
    old_dir = os.path.join(temp_dir, "old_dir")
    new_dir = os.path.join(temp_dir, "new_dir")
    os.makedirs(old_dir)
    
    try:
        engine = DirectoryRenameEngine()
        can_rename = engine.can_rename(old_dir, new_dir)
        
        assert can_rename == True, "Yeniden adlandırılabilir olmalı"
        
        print(f"  Can rename: {can_rename}")
        
        print("\n" + "=" * 70)
        print("PASS: Can rename")
        print("=" * 70)
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def test_undo_rename():
    """
    Test: Undo rename.
    """
    print("=" * 70)
    print("TEST: Undo Rename")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp()
    old_dir = os.path.join(temp_dir, "old_dir")
    new_dir = os.path.join(temp_dir, "new_dir")
    os.makedirs(old_dir)
    
    try:
        engine = DirectoryRenameEngine()
        engine.rename_directory(old_dir, new_dir)
        
        result = engine.undo_rename(new_dir)
        
        assert result.success, "Geri alma başarılı olmalı"
        assert os.path.exists(old_dir), "Eski yol geri yüklenmeli"
        assert not os.path.exists(new_dir), "Yeni yol olmamalı"
        
        print(f"  Success: {result.success}")
        print(f"  Message: {result.message}")
        
        print("\n" + "=" * 70)
        print("PASS: Undo rename")
        print("=" * 70)
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def test_get_rename_history():
    """
    Test: Get rename history.
    """
    print("=" * 70)
    print("TEST: Get Rename History")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp()
    old_dir = os.path.join(temp_dir, "old_dir")
    new_dir = os.path.join(temp_dir, "new_dir")
    os.makedirs(old_dir)
    
    try:
        engine = DirectoryRenameEngine()
        engine.rename_directory(old_dir, new_dir)
        
        history = engine.get_rename_history()
        
        assert len(history) > 0, "Geçmiş olmalı"
        
        print(f"  History: {len(history)}")
        
        print("\n" + "=" * 70)
        print("PASS: Get rename history")
        print("=" * 70)
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def test_clear_history():
    """
    Test: Clear history.
    """
    print("=" * 70)
    print("TEST: Clear History")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp()
    old_dir = os.path.join(temp_dir, "old_dir")
    new_dir = os.path.join(temp_dir, "new_dir")
    os.makedirs(old_dir)
    
    try:
        engine = DirectoryRenameEngine()
        engine.rename_directory(old_dir, new_dir)
        
        result = engine.clear_history()
        
        assert result.success, "Temizleme başarılı olmalı"
        assert len(engine.get_rename_history()) == 0, "Geçmiş temizlenmeli"
        
        print(f"  Success: {result.success}")
        
        print("\n" + "=" * 70)
        print("PASS: Clear history")
        print("=" * 70)
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    engine = DirectoryRenameEngine()
    
    new_config = RenameConfig(mode=RenameMode.FORCE)
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
    
    engine = DirectoryRenameEngine()
    
    config = engine.get_config()
    
    assert config is not None, "Config olmalı"
    assert config.mode == RenameMode.SIMPLE, "Config eşleşmeli"
    
    print(f"  Mode: {config.mode.value}")
    print(f"  Update references: {config.update_references}")
    
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
    assert RenameMode.FORCE.value == "force"
    assert RenameMode.PRESERVE_STRUCTURE.value == "preserve_structure"
    
    print(f"  All enum values verified")
    print(f"  Total modes: {len(RenameMode)}")
    
    print("\n" + "=" * 70)
    print("PASS: RenameMode enum")
    print("=" * 70)


def test_rename_config_dataclass():
    """
    Test: RenameConfig dataclass.
    """
    print("=" * 70)
    print("TEST: RenameConfig Dataclass")
    print("=" * 70)
    
    config = RenameConfig(
        mode=RenameMode.FORCE,
        update_references=False
    )
    
    assert config.mode == RenameMode.FORCE, "Mode eşleşmeli"
    assert config.update_references == False, "Update references eşleşmeli"
    
    print(f"  Mode: {config.mode.value}")
    print(f"  Update references: {config.update_references}")
    
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
        test1 = test_rename_directory()
        test2 = test_rename_force()
        test3 = test_rename_multiple()
        test4 = test_can_rename()
        test5 = test_undo_rename()
        test6 = test_get_rename_history()
        test7 = test_clear_history()
        test8 = test_update_config()
        test9 = test_get_config()
        test10 = test_rename_mode_enum()
        test11 = test_rename_config_dataclass()
        test12 = test_rename_result_dataclass()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Rename Directory: {'PASS' if test1 else 'FAIL'}")
        print(f"Rename Force: {'PASS' if test2 else 'FAIL'}")
        print(f"Rename Multiple: {'PASS' if test3 else 'FAIL'}")
        print(f"Can Rename: {'PASS' if test4 else 'FAIL'}")
        print(f"Undo Rename: {'PASS' if test5 else 'FAIL'}")
        print(f"Get Rename History: {'PASS' if test6 else 'FAIL'}")
        print(f"Clear History: {'PASS' if test7 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test8 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test9 else 'FAIL'}")
        print(f"RenameMode Enum: {'PASS' if test10 else 'FAIL'}")
        print(f"RenameConfig Dataclass: {'PASS' if test11 else 'FAIL'}")
        print(f"RenameResult Dataclass: {'PASS' if test12 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12])
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
