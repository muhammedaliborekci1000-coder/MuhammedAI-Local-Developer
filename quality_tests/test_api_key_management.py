"""
Quality Test: API Key Management
API key management system testleri for security module.
"""

import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from app.security.api_key_management import (
    APIKeyType,
    APIKeyStatus,
    APIKeyScope,
    APIKey,
    APIKeyUsage,
    APIKeyManagementConfig,
    APIKeyManagementResult,
    APIKeyManager
)


def test_api_key_type_enum():
    """
    Test: APIKeyType enum.
    """
    print("=" * 70)
    print("TEST: APIKeyType Enum")
    print("=" * 70)
    
    assert APIKeyType.READ_ONLY.value == "read_only"
    assert APIKeyType.READ_WRITE.value == "read_write"
    assert APIKeyType.ADMIN.value == "admin"
    assert APIKeyType.CUSTOM.value == "custom"
    
    print(f"  All enum values verified")
    print(f"  Total types: {len(APIKeyType)}")
    
    print("\n" + "=" * 70)
    print("PASS: APIKeyType enum")
    print("=" * 70)


def test_api_key_status_enum():
    """
    Test: APIKeyStatus enum.
    """
    print("=" * 70)
    print("TEST: APIKeyStatus Enum")
    print("=" * 70)
    
    assert APIKeyStatus.ACTIVE.value == "active"
    assert APIKeyStatus.INACTIVE.value == "inactive"
    assert APIKeyStatus.REVOKED.value == "revoked"
    assert APIKeyStatus.EXPIRED.value == "expired"
    
    print(f"  All enum values verified")
    print(f"  Total statuses: {len(APIKeyStatus)}")
    
    print("\n" + "=" * 70)
    print("PASS: APIKeyStatus enum")
    print("=" * 70)


def test_api_key_scope_enum():
    """
    Test: APIKeyScope enum.
    """
    print("=" * 70)
    print("TEST: APIKeyScope Enum")
    print("=" * 70)
    
    assert APIKeyScope.GLOBAL.value == "global"
    assert APIKeyScope.PROJECT.value == "project"
    assert APIKeyScope.ORGANIZATION.value == "organization"
    assert APIKeyScope.USER.value == "user"
    assert APIKeyScope.CUSTOM.value == "custom"
    
    print(f"  All enum values verified")
    print(f"  Total scopes: {len(APIKeyScope)}")
    
    print("\n" + "=" * 70)
    print("PASS: APIKeyScope enum")
    print("=" * 70)


def test_api_key_dataclass():
    """
    Test: APIKey dataclass.
    """
    print("=" * 70)
    print("TEST: APIKey Dataclass")
    print("=" * 70)
    
    api_key = APIKey(
        key_id="key_1",
        user_id="user_1",
        name="Test Key",
        key_type=APIKeyType.READ_ONLY,
        scope=APIKeyScope.GLOBAL,
        key_hash="hashed_key"
    )
    
    assert api_key.key_id == "key_1", "Key ID eşleşmeli"
    assert api_key.user_id == "user_1", "User ID eşleşmeli"
    assert api_key.name == "Test Key", "Name eşleşmeli"
    
    print(f"  Key ID: {api_key.key_id}")
    print(f"  Name: {api_key.name}")
    
    print("\n" + "=" * 70)
    print("PASS: APIKey dataclass")
    print("=" * 70)


def test_api_key_usage_dataclass():
    """
    Test: APIKeyUsage dataclass.
    """
    print("=" * 70)
    print("TEST: APIKeyUsage Dataclass")
    print("=" * 70)
    
    usage = APIKeyUsage(
        usage_id="usage_1",
        key_id="key_1",
        endpoint="/api/test",
        method="GET"
    )
    
    assert usage.usage_id == "usage_1", "Usage ID eşleşmeli"
    assert usage.key_id == "key_1", "Key ID eşleşmeli"
    assert usage.endpoint == "/api/test", "Endpoint eşleşmeli"
    
    print(f"  Usage ID: {usage.usage_id}")
    print(f"  Endpoint: {usage.endpoint}")
    
    print("\n" + "=" * 70)
    print("PASS: APIKeyUsage dataclass")
    print("=" * 70)


def test_api_key_management_config_dataclass():
    """
    Test: APIKeyManagementConfig dataclass.
    """
    print("=" * 70)
    print("TEST: APIKeyManagementConfig Dataclass")
    print("=" * 70)
    
    config = APIKeyManagementConfig(max_keys_per_user=5)
    
    assert config.max_keys_per_user == 5, "Max keys per user eşleşmeli"
    
    print(f"  Max keys per user: {config.max_keys_per_user}")
    
    print("\n" + "=" * 70)
    print("PASS: APIKeyManagementConfig dataclass")
    print("=" * 70)


def test_api_key_management_result_dataclass():
    """
    Test: APIKeyManagementResult dataclass.
    """
    print("=" * 70)
    print("TEST: APIKeyManagementResult Dataclass")
    print("=" * 70)
    
    result = APIKeyManagementResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.api_keys, list), "API keys list olmalı"
    assert isinstance(result.usages, list), "Usages list olmalı"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: APIKeyManagementResult dataclass")
    print("=" * 70)


def test_api_key_manager_initialization():
    """
    Test: APIKeyManager initialization.
    """
    print("=" * 70)
    print("TEST: APIKeyManager Initialization")
    print("=" * 70)
    
    config = APIKeyManagementConfig()
    manager = APIKeyManager(config)
    
    assert manager.config == config, "Config eşleşmeli"
    assert len(manager.api_keys) == 0, "API keys boş olmalı"
    
    print(f"  API keys: {len(manager.api_keys)}")
    
    print("\n" + "=" * 70)
    print("PASS: APIKeyManager initialization")
    print("=" * 70)


def test_create_api_key():
    """
    Test: Create API key.
    """
    print("=" * 70)
    print("TEST: Create API Key")
    print("=" * 70)
    
    manager = APIKeyManager()
    
    result = manager.create_api_key("user_1", "Test Key", APIKeyType.READ_ONLY, APIKeyScope.GLOBAL)
    
    assert result.success == True, "Ekleme başarılı olmalı"
    assert len(manager.api_keys) > 0, "API key eklenmeli"
    assert result.raw_key is not None, "Raw key olmalı"
    
    print(f"  API key created: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Create API key")
    print("=" * 70)


def test_delete_api_key():
    """
    Test: Delete API key.
    """
    print("=" * 70)
    print("TEST: Delete API Key")
    print("=" * 70)
    
    manager = APIKeyManager()
    
    result = manager.create_api_key("user_1", "Test Key", APIKeyType.READ_ONLY, APIKeyScope.GLOBAL)
    key_id = result.api_key.key_id
    
    result = manager.delete_api_key(key_id)
    
    assert result.success == True, "Silme başarılı olmalı"
    assert key_id not in manager.api_keys, "API key silinmeli"
    
    print(f"  API key deleted: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Delete API key")
    print("=" * 70)


def test_update_api_key():
    """
    Test: Update API key.
    """
    print("=" * 70)
    print("TEST: Update API Key")
    print("=" * 70)
    
    manager = APIKeyManager()
    
    result = manager.create_api_key("user_1", "Test Key", APIKeyType.READ_ONLY, APIKeyScope.GLOBAL)
    key_id = result.api_key.key_id
    
    result = manager.update_api_key(key_id, description="Updated description")
    
    assert result.success == True, "Update başarılı olmalı"
    
    print(f"  API key updated: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Update API key")
    print("=" * 70)


def test_get_api_key():
    """
    Test: Get API key.
    """
    print("=" * 70)
    print("TEST: Get API Key")
    print("=" * 70)
    
    manager = APIKeyManager()
    
    result = manager.create_api_key("user_1", "Test Key", APIKeyType.READ_ONLY, APIKeyScope.GLOBAL)
    key_id = result.api_key.key_id
    
    api_key = manager.get_api_key(key_id)
    
    assert api_key is not None, "API key bulunmalı"
    assert api_key.name == "Test Key", "Name eşleşmeli"
    
    print(f"  API key: {api_key.name}")
    
    print("\n" + "=" * 70)
    print("PASS: Get API key")
    print("=" * 70)


def test_get_api_key_by_hash():
    """
    Test: Get API key by hash.
    """
    print("=" * 70)
    print("TEST: Get API Key by Hash")
    print("=" * 70)
    
    manager = APIKeyManager()
    
    result = manager.create_api_key("user_1", "Test Key", APIKeyType.READ_ONLY, APIKeyScope.GLOBAL)
    key_hash = result.api_key.key_hash
    
    api_key = manager.get_api_key_by_hash(key_hash)
    
    assert api_key is not None, "API key bulunmalı"
    
    print(f"  API key: {api_key.name}")
    
    print("\n" + "=" * 70)
    print("PASS: Get API key by hash")
    print("=" * 70)


def test_get_all_api_keys():
    """
    Test: Get all API keys.
    """
    print("=" * 70)
    print("TEST: Get All API Keys")
    print("=" * 70)
    
    manager = APIKeyManager()
    
    manager.create_api_key("user_1", "Test Key 1", APIKeyType.READ_ONLY, APIKeyScope.GLOBAL)
    manager.create_api_key("user_2", "Test Key 2", APIKeyType.READ_WRITE, APIKeyScope.GLOBAL)
    
    api_keys = manager.get_all_api_keys()
    
    assert len(api_keys) == 2, "2 API key olmalı"
    
    print(f"  Total API keys: {len(api_keys)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get all API keys")
    print("=" * 70)


def test_get_user_api_keys():
    """
    Test: Get user API keys.
    """
    print("=" * 70)
    print("TEST: Get User API Keys")
    print("=" * 70)
    
    manager = APIKeyManager()
    
    manager.create_api_key("user_1", "Test Key 1", APIKeyType.READ_ONLY, APIKeyScope.GLOBAL)
    manager.create_api_key("user_1", "Test Key 2", APIKeyType.READ_WRITE, APIKeyScope.GLOBAL)
    
    api_keys = manager.get_user_api_keys("user_1")
    
    assert len(api_keys) == 2, "2 API key olmalı"
    
    print(f"  User API keys: {len(api_keys)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get user API keys")
    print("=" * 70)


def test_validate_api_key():
    """
    Test: Validate API key.
    """
    print("=" * 70)
    print("TEST: Validate API Key")
    print("=" * 70)
    
    manager = APIKeyManager()
    
    result = manager.create_api_key("user_1", "Test Key", APIKeyType.READ_ONLY, APIKeyScope.GLOBAL)
    raw_key = result.raw_key
    
    result = manager.validate_api_key(raw_key)
    
    assert result.success == True, "Validation başarılı olmalı"
    
    print(f"  API key valid: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Validate API key")
    print("=" * 70)


def test_revoke_api_key():
    """
    Test: Revoke API key.
    """
    print("=" * 70)
    print("TEST: Revoke API Key")
    print("=" * 70)
    
    manager = APIKeyManager()
    
    result = manager.create_api_key("user_1", "Test Key", APIKeyType.READ_ONLY, APIKeyScope.GLOBAL)
    key_id = result.api_key.key_id
    
    result = manager.revoke_api_key(key_id)
    
    assert result.success == True, "Revoke başarılı olmalı"
    
    print(f"  API key revoked: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Revoke API key")
    print("=" * 70)


def test_rotate_api_key():
    """
    Test: Rotate API key.
    """
    print("=" * 70)
    print("TEST: Rotate API Key")
    print("=" * 70)
    
    manager = APIKeyManager()
    
    result = manager.create_api_key("user_1", "Test Key", APIKeyType.READ_ONLY, APIKeyScope.GLOBAL)
    key_id = result.api_key.key_id
    
    result = manager.rotate_api_key(key_id)
    
    assert result.success == True, "Rotate başarılı olmalı"
    assert result.raw_key is not None, "New raw key olmalı"
    
    print(f"  API key rotated: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Rotate API key")
    print("=" * 70)


def test_get_key_usage():
    """
    Test: Get key usage.
    """
    print("=" * 70)
    print("TEST: Get Key Usage")
    print("=" * 70)
    
    manager = APIKeyManager()
    
    result = manager.create_api_key("user_1", "Test Key", APIKeyType.READ_ONLY, APIKeyScope.GLOBAL)
    key_id = result.api_key.key_id
    
    manager.validate_api_key(result.raw_key)
    usages = manager.get_key_usage(key_id)
    
    assert len(usages) > 0, "Usage olmalı"
    
    print(f"  Key usage: {len(usages)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get key usage")
    print("=" * 70)


def test_get_all_usage():
    """
    Test: Get all usage.
    """
    print("=" * 70)
    print("TEST: Get All Usage")
    print("=" * 70)
    
    manager = APIKeyManager()
    
    result = manager.create_api_key("user_1", "Test Key", APIKeyType.READ_ONLY, APIKeyScope.GLOBAL)
    manager.validate_api_key(result.raw_key)
    
    usages = manager.get_all_usage()
    
    assert len(usages) > 0, "Usage olmalı"
    
    print(f"  Total usage: {len(usages)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get all usage")
    print("=" * 70)


def test_cleanup_expired_keys():
    """
    Test: Cleanup expired keys.
    """
    print("=" * 70)
    print("TEST: Cleanup Expired Keys")
    print("=" * 70)
    
    manager = APIKeyManager()
    
    result = manager.create_api_key("user_1", "Test Key", APIKeyType.READ_ONLY, APIKeyScope.GLOBAL, expires_in_days=-1)
    
    result = manager.cleanup_expired_keys()
    
    assert result.success == True, "Cleanup başarılı olmalı"
    
    print(f"  Cleanup: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Cleanup expired keys")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    manager = APIKeyManager()
    
    new_config = APIKeyManagementConfig(max_keys_per_user=20)
    result = manager.update_config(new_config)
    
    assert result.success == True, "Update başarılı olmalı"
    assert manager.config.max_keys_per_user == 20, "Config güncellenmeli"
    
    print(f"  Max keys per user: {manager.config.max_keys_per_user}")
    
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
    
    config = APIKeyManagementConfig(max_keys_per_user=20)
    manager = APIKeyManager(config)
    
    retrieved_config = manager.get_config()
    
    assert retrieved_config.max_keys_per_user == 20, "Config eşleşmeli"
    
    print(f"  Max keys per user: {retrieved_config.max_keys_per_user}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_api_key_type_enum()
        test2 = test_api_key_status_enum()
        test3 = test_api_key_scope_enum()
        test4 = test_api_key_dataclass()
        test5 = test_api_key_usage_dataclass()
        test6 = test_api_key_management_config_dataclass()
        test7 = test_api_key_management_result_dataclass()
        test8 = test_api_key_manager_initialization()
        test9 = test_create_api_key()
        test10 = test_delete_api_key()
        test11 = test_update_api_key()
        test12 = test_get_api_key()
        test13 = test_get_api_key_by_hash()
        test14 = test_get_all_api_keys()
        test15 = test_get_user_api_keys()
        test16 = test_validate_api_key()
        test17 = test_revoke_api_key()
        test18 = test_rotate_api_key()
        test19 = test_get_key_usage()
        test20 = test_get_all_usage()
        test21 = test_cleanup_expired_keys()
        test22 = test_update_config()
        test23 = test_get_config()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"APIKeyType Enum: {'PASS' if test1 else 'FAIL'}")
        print(f"APIKeyStatus Enum: {'PASS' if test2 else 'FAIL'}")
        print(f"APIKeyScope Enum: {'PASS' if test3 else 'FAIL'}")
        print(f"APIKey Dataclass: {'PASS' if test4 else 'FAIL'}")
        print(f"APIKeyUsage Dataclass: {'PASS' if test5 else 'FAIL'}")
        print(f"APIKeyManagementConfig Dataclass: {'PASS' if test6 else 'FAIL'}")
        print(f"APIKeyManagementResult Dataclass: {'PASS' if test7 else 'FAIL'}")
        print(f"APIKeyManager Initialization: {'PASS' if test8 else 'FAIL'}")
        print(f"Create API Key: {'PASS' if test9 else 'FAIL'}")
        print(f"Delete API Key: {'PASS' if test10 else 'FAIL'}")
        print(f"Update API Key: {'PASS' if test11 else 'FAIL'}")
        print(f"Get API Key: {'PASS' if test12 else 'FAIL'}")
        print(f"Get API Key by Hash: {'PASS' if test13 else 'FAIL'}")
        print(f"Get All API Keys: {'PASS' if test14 else 'FAIL'}")
        print(f"Get User API Keys: {'PASS' if test15 else 'FAIL'}")
        print(f"Validate API Key: {'PASS' if test16 else 'FAIL'}")
        print(f"Revoke API Key: {'PASS' if test17 else 'FAIL'}")
        print(f"Rotate API Key: {'PASS' if test18 else 'FAIL'}")
        print(f"Get Key Usage: {'PASS' if test19 else 'FAIL'}")
        print(f"Get All Usage: {'PASS' if test20 else 'FAIL'}")
        print(f"Cleanup Expired Keys: {'PASS' if test21 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test22 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test23 else 'FAIL'}")
        
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
