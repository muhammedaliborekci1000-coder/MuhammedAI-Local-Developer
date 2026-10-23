"""
Quality Test: File Permissions
File permissions system testleri.
"""

import sys
import os
import tempfile
import shutil

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.file_permissions import (
    FilePermissionsEngine,
    PermissionType,
    PermissionAction,
    PermissionInfo,
    PermissionConfig,
    PermissionResult
)


def test_check_permissions():
    """
    Test: Check permissions.
    """
    print("=" * 70)
    print("TEST: Check Permissions")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp()
    temp_file = os.path.join(temp_dir, "test.txt")
    
    with open(temp_file, 'w') as f:
        f.write("Hello World")
    
    try:
        engine = FilePermissionsEngine()
        result = engine.check_permissions(temp_file)
        
        assert result.success, "Kontrol başarılı olmalı"
        assert result.permission_info is not None, "Permission info olmalı"
        assert result.permission_info.readable == True, "Okunabilir olmalı"
        
        print(f"  Success: {result.success}")
        print(f"  Readable: {result.permission_info.readable}")
        print(f"  Writable: {result.permission_info.writable}")
        
        print("\n" + "=" * 70)
        print("PASS: Check permissions")
        print("=" * 70)
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def test_grant_permission():
    """
    Test: Grant permission.
    """
    print("=" * 70)
    print("TEST: Grant Permission")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp()
    temp_file = os.path.join(temp_dir, "test.txt")
    
    with open(temp_file, 'w') as f:
        f.write("Hello World")
    
    try:
        engine = FilePermissionsEngine()
        result = engine.grant_permission(temp_file, PermissionType.READ)
        
        assert result.success, "İzin verme başarılı olmalı"
        assert result.permission_info is not None, "Permission info olmalı"
        
        print(f"  Success: {result.success}")
        print(f"  Message: {result.message}")
        
        print("\n" + "=" * 70)
        print("PASS: Grant permission")
        print("=" * 70)
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def test_revoke_permission():
    """
    Test: Revoke permission.
    """
    print("=" * 70)
    print("TEST: Revoke Permission")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp()
    temp_file = os.path.join(temp_dir, "test.txt")
    
    with open(temp_file, 'w') as f:
        f.write("Hello World")
    
    try:
        engine = FilePermissionsEngine()
        result = engine.revoke_permission(temp_file, PermissionType.WRITE)
        
        assert result.success, "İzin kaldırma başarılı olmalı"
        
        print(f"  Success: {result.success}")
        print(f"  Message: {result.message}")
        
        # Restore write permission for cleanup
        engine.grant_permission(temp_file, PermissionType.WRITE)
        
        print("\n" + "=" * 70)
        print("PASS: Revoke permission")
        print("=" * 70)
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def test_modify_permissions():
    """
    Test: Modify permissions.
    """
    print("=" * 70)
    print("TEST: Modify Permissions")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp()
    temp_file = os.path.join(temp_dir, "test.txt")
    
    with open(temp_file, 'w') as f:
        f.write("Hello World")
    
    try:
        engine = FilePermissionsEngine()
        result = engine.modify_permissions(temp_file, read=True, write=True, execute=False)
        
        assert result.success, "Değiştirme başarılı olmalı"
        
        print(f"  Success: {result.success}")
        print(f"  Message: {result.message}")
        
        print("\n" + "=" * 70)
        print("PASS: Modify permissions")
        print("=" * 70)
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def test_get_permission_history():
    """
    Test: Get permission history.
    """
    print("=" * 70)
    print("TEST: Get Permission History")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp()
    temp_file = os.path.join(temp_dir, "test.txt")
    
    with open(temp_file, 'w') as f:
        f.write("Hello World")
    
    try:
        engine = FilePermissionsEngine()
        engine.check_permissions(temp_file)
        
        history = engine.get_permission_history()
        
        assert len(history) > 0, "Geçmiş olmalı"
        
        print(f"  History: {len(history)}")
        
        print("\n" + "=" * 70)
        print("PASS: Get permission history")
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
    temp_file = os.path.join(temp_dir, "test.txt")
    
    with open(temp_file, 'w') as f:
        f.write("Hello World")
    
    try:
        engine = FilePermissionsEngine()
        engine.check_permissions(temp_file)
        
        result = engine.clear_history()
        
        assert result.success, "Temizleme başarılı olmalı"
        assert len(engine.get_permission_history()) == 0, "Geçmiş temizlenmeli"
        
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
    
    engine = FilePermissionsEngine()
    
    new_config = PermissionConfig(auto_check=False)
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
    
    engine = FilePermissionsEngine()
    
    config = engine.get_config()
    
    assert config is not None, "Config olmalı"
    assert config.auto_check == True, "Config eşleşmeli"
    
    print(f"  Auto check: {config.auto_check}")
    print(f"  Show notification: {config.show_notification}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


def test_permission_type_enum():
    """
    Test: PermissionType enum.
    """
    print("=" * 70)
    print("TEST: PermissionType Enum")
    print("=" * 70)
    
    assert PermissionType.READ.value == "read"
    assert PermissionType.WRITE.value == "write"
    assert PermissionType.EXECUTE.value == "execute"
    assert PermissionType.ALL.value == "all"
    
    print(f"  All enum values verified")
    print(f"  Total types: {len(PermissionType)}")
    
    print("\n" + "=" * 70)
    print("PASS: PermissionType enum")
    print("=" * 70)


def test_permission_action_enum():
    """
    Test: PermissionAction enum.
    """
    print("=" * 70)
    print("TEST: PermissionAction Enum")
    print("=" * 70)
    
    assert PermissionAction.CHECK.value == "check"
    assert PermissionAction.GRANT.value == "grant"
    assert PermissionAction.REVOKE.value == "revoke"
    assert PermissionAction.MODIFY.value == "modify"
    
    print(f"  All enum values verified")
    print(f"  Total actions: {len(PermissionAction)}")
    
    print("\n" + "=" * 70)
    print("PASS: PermissionAction enum")
    print("=" * 70)


def test_permission_info_dataclass():
    """
    Test: PermissionInfo dataclass.
    """
    print("=" * 70)
    print("TEST: PermissionInfo Dataclass")
    print("=" * 70)
    
    info = PermissionInfo(
        path="/test/file.txt",
        readable=True,
        writable=True,
        executable=False
    )
    
    assert info.path == "/test/file.txt", "Path eşleşmeli"
    assert info.readable == True, "Readable eşleşmeli"
    assert info.writable == True, "Writable eşleşmeli"
    
    print(f"  Path: {info.path}")
    print(f"  Readable: {info.readable}")
    print(f"  Writable: {info.writable}")
    
    print("\n" + "=" * 70)
    print("PASS: PermissionInfo dataclass")
    print("=" * 70)


def test_permission_config_dataclass():
    """
    Test: PermissionConfig dataclass.
    """
    print("=" * 70)
    print("TEST: PermissionConfig Dataclass")
    print("=" * 70)
    
    config = PermissionConfig(
        auto_check=False,
        show_notification=False
    )
    
    assert config.auto_check == False, "Auto check eşleşmeli"
    assert config.show_notification == False, "Show notification eşleşmeli"
    
    print(f"  Auto check: {config.auto_check}")
    print(f"  Show notification: {config.show_notification}")
    
    print("\n" + "=" * 70)
    print("PASS: PermissionConfig dataclass")
    print("=" * 70)


def test_permission_result_dataclass():
    """
    Test: PermissionResult dataclass.
    """
    print("=" * 70)
    print("TEST: PermissionResult Dataclass")
    print("=" * 70)
    
    result = PermissionResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: PermissionResult dataclass")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_check_permissions()
        test2 = test_grant_permission()
        test3 = test_revoke_permission()
        test4 = test_modify_permissions()
        test5 = test_get_permission_history()
        test6 = test_clear_history()
        test7 = test_update_config()
        test8 = test_get_config()
        test9 = test_permission_type_enum()
        test10 = test_permission_action_enum()
        test11 = test_permission_info_dataclass()
        test12 = test_permission_config_dataclass()
        test13 = test_permission_result_dataclass()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Check Permissions: {'PASS' if test1 else 'FAIL'}")
        print(f"Grant Permission: {'PASS' if test2 else 'FAIL'}")
        print(f"Revoke Permission: {'PASS' if test3 else 'FAIL'}")
        print(f"Modify Permissions: {'PASS' if test4 else 'FAIL'}")
        print(f"Get Permission History: {'PASS' if test5 else 'FAIL'}")
        print(f"Clear History: {'PASS' if test6 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test7 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test8 else 'FAIL'}")
        print(f"PermissionType Enum: {'PASS' if test9 else 'FAIL'}")
        print(f"PermissionAction Enum: {'PASS' if test10 else 'FAIL'}")
        print(f"PermissionInfo Dataclass: {'PASS' if test11 else 'FAIL'}")
        print(f"PermissionConfig Dataclass: {'PASS' if test12 else 'FAIL'}")
        print(f"PermissionResult Dataclass: {'PASS' if test13 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13])
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
