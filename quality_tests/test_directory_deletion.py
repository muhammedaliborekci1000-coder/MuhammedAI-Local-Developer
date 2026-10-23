"""
Quality Test: Directory Deletion
Directory deletion system testleri.
"""

import sys
import os
import tempfile
import shutil

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.directory_deletion import (
    DirectoryDeletionEngine,
    DeleteMode,
    DeleteScope,
    DeleteConfig,
    DeleteResult
)


def test_delete_directory():
    """
    Test: Delete directory.
    """
    print("=" * 70)
    print("TEST: Delete Directory")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp()
    new_dir = os.path.join(temp_dir, "new_dir")
    os.makedirs(new_dir)
    
    try:
        engine = DirectoryDeletionEngine()
        result = engine.delete_directory(new_dir)
        
        assert result.success, "Silme başarılı olmalı"
        assert not os.path.exists(new_dir), "Dizin silinmeli"
        
        print(f"  Success: {result.success}")
        print(f"  Message: {result.message}")
        
        print("\n" + "=" * 70)
        print("PASS: Delete directory")
        print("=" * 70)
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def test_delete_recursive():
    """
    Test: Delete recursive.
    """
    print("=" * 70)
    print("TEST: Delete Recursive")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp()
    parent_dir = os.path.join(temp_dir, "parent")
    child_dir = os.path.join(parent_dir, "child")
    os.makedirs(child_dir)
    
    try:
        config = DeleteConfig(mode=DeleteMode.RECURSIVE)
        engine = DirectoryDeletionEngine(config)
        result = engine.delete_directory(parent_dir)
        
        assert result.success, "Silme başarılı olmalı"
        assert not os.path.exists(parent_dir), "Dizin silinmeli"
        
        print(f"  Success: {result.success}")
        print(f"  Message: {result.message}")
        
        print("\n" + "=" * 70)
        print("PASS: Delete recursive")
        print("=" * 70)
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def test_delete_contents_only():
    """
    Test: Delete contents only.
    """
    print("=" * 70)
    print("TEST: Delete Contents Only")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp()
    parent_dir = os.path.join(temp_dir, "parent")
    child_file = os.path.join(parent_dir, "file.txt")
    os.makedirs(parent_dir)
    with open(child_file, 'w') as f:
        f.write("test")
    
    try:
        config = DeleteConfig(scope=DeleteScope.CONTENTS_ONLY)
        engine = DirectoryDeletionEngine(config)
        result = engine.delete_directory(parent_dir)
        
        assert result.success, "Silme başarılı olmalı"
        assert os.path.exists(parent_dir), "Dizin kalmalı"
        assert len(os.listdir(parent_dir)) == 0, "İçerik silinmeli"
        
        print(f"  Success: {result.success}")
        print(f"  Message: {result.message}")
        
        print("\n" + "=" * 70)
        print("PASS: Delete contents only")
        print("=" * 70)
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def test_delete_force():
    """
    Test: Delete force.
    """
    print("=" * 70)
    print("TEST: Delete Force")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp()
    parent_dir = os.path.join(temp_dir, "parent")
    child_file = os.path.join(parent_dir, "file.txt")
    os.makedirs(parent_dir)
    with open(child_file, 'w') as f:
        f.write("test")
    
    try:
        config = DeleteConfig(mode=DeleteMode.FORCE, scope=DeleteScope.DIRECTORY_ONLY)
        engine = DirectoryDeletionEngine(config)
        result = engine.delete_directory(parent_dir)
        
        assert result.success, "Silme başarılı olmalı"
        assert not os.path.exists(parent_dir), "Dizin silinmeli"
        
        print(f"  Success: {result.success}")
        print(f"  Message: {result.message}")
        
        print("\n" + "=" * 70)
        print("PASS: Delete force")
        print("=" * 70)
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def test_delete_multiple():
    """
    Test: Delete multiple directories.
    """
    print("=" * 70)
    print("TEST: Delete Multiple Directories")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp()
    dir1 = os.path.join(temp_dir, "dir1")
    dir2 = os.path.join(temp_dir, "dir2")
    dir3 = os.path.join(temp_dir, "dir3")
    os.makedirs(dir1)
    os.makedirs(dir2)
    os.makedirs(dir3)
    
    try:
        engine = DirectoryDeletionEngine()
        result = engine.delete_multiple([dir1, dir2, dir3])
        
        assert result.success, "Silme başarılı olmalı"
        assert result.deleted_count == 3, "3 dizin silinmeli"
        
        print(f"  Success: {result.success}")
        print(f"  Deleted count: {result.deleted_count}")
        
        print("\n" + "=" * 70)
        print("PASS: Delete multiple directories")
        print("=" * 70)
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def test_can_delete():
    """
    Test: Can delete.
    """
    print("=" * 70)
    print("TEST: Can Delete")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp()
    new_dir = os.path.join(temp_dir, "new_dir")
    os.makedirs(new_dir)
    
    try:
        engine = DirectoryDeletionEngine()
        can_delete = engine.can_delete(new_dir)
        
        assert can_delete == True, "Silinebilir olmalı"
        
        print(f"  Can delete: {can_delete}")
        
        print("\n" + "=" * 70)
        print("PASS: Can delete")
        print("=" * 70)
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def test_undo_deletion():
    """
    Test: Undo deletion.
    """
    print("=" * 70)
    print("TEST: Undo Deletion")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp()
    new_dir = os.path.join(temp_dir, "new_dir")
    os.makedirs(new_dir)
    
    try:
        config = DeleteConfig(backup_before_delete=True)
        engine = DirectoryDeletionEngine(config)
        engine.delete_directory(new_dir)
        
        result = engine.undo_deletion(new_dir)
        
        assert result.success, "Geri alma başarılı olmalı"
        assert os.path.exists(new_dir), "Dizin geri yüklenmeli"
        
        print(f"  Success: {result.success}")
        print(f"  Message: {result.message}")
        
        print("\n" + "=" * 70)
        print("PASS: Undo deletion")
        print("=" * 70)
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def test_get_deletion_history():
    """
    Test: Get deletion history.
    """
    print("=" * 70)
    print("TEST: Get Deletion History")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp()
    new_dir = os.path.join(temp_dir, "new_dir")
    os.makedirs(new_dir)
    
    try:
        engine = DirectoryDeletionEngine()
        engine.delete_directory(new_dir)
        
        history = engine.get_deletion_history()
        
        assert len(history) > 0, "Geçmiş olmalı"
        
        print(f"  History: {len(history)}")
        
        print("\n" + "=" * 70)
        print("PASS: Get deletion history")
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
    new_dir = os.path.join(temp_dir, "new_dir")
    os.makedirs(new_dir)
    
    try:
        engine = DirectoryDeletionEngine()
        engine.delete_directory(new_dir)
        
        result = engine.clear_history()
        
        assert result.success, "Temizleme başarılı olmalı"
        assert len(engine.get_deletion_history()) == 0, "Geçmiş temizlenmeli"
        
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
    
    engine = DirectoryDeletionEngine()
    
    new_config = DeleteConfig(mode=DeleteMode.FORCE)
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
    
    engine = DirectoryDeletionEngine()
    
    config = engine.get_config()
    
    assert config is not None, "Config olmalı"
    assert config.mode == DeleteMode.RECURSIVE, "Config eşleşmeli"
    
    print(f"  Mode: {config.mode.value}")
    print(f"  Scope: {config.scope.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


def test_delete_mode_enum():
    """
    Test: DeleteMode enum.
    """
    print("=" * 70)
    print("TEST: DeleteMode Enum")
    print("=" * 70)
    
    assert DeleteMode.SINGLE.value == "single"
    assert DeleteMode.RECURSIVE.value == "recursive"
    assert DeleteMode.FORCE.value == "force"
    assert DeleteMode.SAFE.value == "safe"
    
    print(f"  All enum values verified")
    print(f"  Total modes: {len(DeleteMode)}")
    
    print("\n" + "=" * 70)
    print("PASS: DeleteMode enum")
    print("=" * 70)


def test_delete_scope_enum():
    """
    Test: DeleteScope enum.
    """
    print("=" * 70)
    print("TEST: DeleteScope Enum")
    print("=" * 70)
    
    assert DeleteScope.CONTENTS_ONLY.value == "contents_only"
    assert DeleteScope.DIRECTORY_ONLY.value == "directory_only"
    assert DeleteScope.ALL.value == "all"
    
    print(f"  All enum values verified")
    print(f"  Total scopes: {len(DeleteScope)}")
    
    print("\n" + "=" * 70)
    print("PASS: DeleteScope enum")
    print("=" * 70)


def test_delete_config_dataclass():
    """
    Test: DeleteConfig dataclass.
    """
    print("=" * 70)
    print("TEST: DeleteConfig Dataclass")
    print("=" * 70)
    
    config = DeleteConfig(
        mode=DeleteMode.FORCE,
        scope=DeleteScope.CONTENTS_ONLY
    )
    
    assert config.mode == DeleteMode.FORCE, "Mode eşleşmeli"
    assert config.scope == DeleteScope.CONTENTS_ONLY, "Scope eşleşmeli"
    
    print(f"  Mode: {config.mode.value}")
    print(f"  Scope: {config.scope.value}")
    
    print("\n" + "=" * 70)
    print("PASS: DeleteConfig dataclass")
    print("=" * 70)


def test_delete_result_dataclass():
    """
    Test: DeleteResult dataclass.
    """
    print("=" * 70)
    print("TEST: DeleteResult Dataclass")
    print("=" * 70)
    
    result = DeleteResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: DeleteResult dataclass")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_delete_directory()
        test2 = test_delete_recursive()
        test3 = test_delete_contents_only()
        test4 = test_delete_force()
        test5 = test_delete_multiple()
        test6 = test_can_delete()
        test7 = test_undo_deletion()
        test8 = test_get_deletion_history()
        test9 = test_clear_history()
        test10 = test_update_config()
        test11 = test_get_config()
        test12 = test_delete_mode_enum()
        test13 = test_delete_scope_enum()
        test14 = test_delete_config_dataclass()
        test15 = test_delete_result_dataclass()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Delete Directory: {'PASS' if test1 else 'FAIL'}")
        print(f"Delete Recursive: {'PASS' if test2 else 'FAIL'}")
        print(f"Delete Contents Only: {'PASS' if test3 else 'FAIL'}")
        print(f"Delete Force: {'PASS' if test4 else 'FAIL'}")
        print(f"Delete Multiple: {'PASS' if test5 else 'FAIL'}")
        print(f"Can Delete: {'PASS' if test6 else 'FAIL'}")
        print(f"Undo Deletion: {'PASS' if test7 else 'FAIL'}")
        print(f"Get Deletion History: {'PASS' if test8 else 'FAIL'}")
        print(f"Clear History: {'PASS' if test9 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test10 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test11 else 'FAIL'}")
        print(f"DeleteMode Enum: {'PASS' if test12 else 'FAIL'}")
        print(f"DeleteScope Enum: {'PASS' if test13 else 'FAIL'}")
        print(f"DeleteConfig Dataclass: {'PASS' if test14 else 'FAIL'}")
        print(f"DeleteResult Dataclass: {'PASS' if test15 else 'FAIL'}")
        
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
