"""
Quality Test: Secure Storage
Secure storage system testleri for security module.
"""

import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from app.security.secure_storage import (
    StorageType,
    EncryptionType,
    AccessLevel,
    StorageItem,
    SecureStorageConfig,
    SecureStorageResult,
    SecureStorage
)


def test_storage_type_enum():
    """
    Test: StorageType enum.
    """
    print("=" * 70)
    print("TEST: StorageType Enum")
    print("=" * 70)
    
    assert StorageType.MEMORY.value == "memory"
    assert StorageType.FILE.value == "file"
    assert StorageType.DATABASE.value == "database"
    assert StorageType.CUSTOM.value == "custom"
    
    print(f"  All enum values verified")
    print(f"  Total types: {len(StorageType)}")
    
    print("\n" + "=" * 70)
    print("PASS: StorageType enum")
    print("=" * 70)


def test_encryption_type_enum():
    """
    Test: EncryptionType enum.
    """
    print("=" * 70)
    print("TEST: EncryptionType Enum")
    print("=" * 70)
    
    assert EncryptionType.NONE.value == "none"
    assert EncryptionType.AES_256.value == "aes_256"
    assert EncryptionType.CUSTOM.value == "custom"
    
    print(f"  All enum values verified")
    print(f"  Total types: {len(EncryptionType)}")
    
    print("\n" + "=" * 70)
    print("PASS: EncryptionType enum")
    print("=" * 70)


def test_access_level_enum():
    """
    Test: AccessLevel enum.
    """
    print("=" * 70)
    print("TEST: AccessLevel Enum")
    print("=" * 70)
    
    assert AccessLevel.PUBLIC.value == "public"
    assert AccessLevel.PRIVATE.value == "private"
    assert AccessLevel.RESTRICTED.value == "restricted"
    assert AccessLevel.CONFIDENTIAL.value == "confidential"
    
    print(f"  All enum values verified")
    print(f"  Total levels: {len(AccessLevel)}")
    
    print("\n" + "=" * 70)
    print("PASS: AccessLevel enum")
    print("=" * 70)


def test_storage_item_dataclass():
    """
    Test: StorageItem dataclass.
    """
    print("=" * 70)
    print("TEST: StorageItem Dataclass")
    print("=" * 70)
    
    item = StorageItem(
        item_id="item_1",
        key="test_key",
        value="test_value",
        storage_type=StorageType.MEMORY,
        encryption_type=EncryptionType.NONE,
        access_level=AccessLevel.PRIVATE
    )
    
    assert item.item_id == "item_1", "Item ID eşleşmeli"
    assert item.key == "test_key", "Key eşleşmeli"
    assert item.storage_type == StorageType.MEMORY, "Storage type eşleşmeli"
    
    print(f"  Item ID: {item.item_id}")
    print(f"  Key: {item.key}")
    
    print("\n" + "=" * 70)
    print("PASS: StorageItem dataclass")
    print("=" * 70)


def test_secure_storage_config_dataclass():
    """
    Test: SecureStorageConfig dataclass.
    """
    print("=" * 70)
    print("TEST: SecureStorageConfig Dataclass")
    print("=" * 70)
    
    config = SecureStorageConfig(enable_encryption=True)
    
    assert config.enable_encryption == True, "Enable encryption eşleşmeli"
    
    print(f"  Enable encryption: {config.enable_encryption}")
    
    print("\n" + "=" * 70)
    print("PASS: SecureStorageConfig dataclass")
    print("=" * 70)


def test_secure_storage_result_dataclass():
    """
    Test: SecureStorageResult dataclass.
    """
    print("=" * 70)
    print("TEST: SecureStorageResult Dataclass")
    print("=" * 70)
    
    result = SecureStorageResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.items, list), "Items list olmalı"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: SecureStorageResult dataclass")
    print("=" * 70)


def test_secure_storage_initialization():
    """
    Test: SecureStorage initialization.
    """
    print("=" * 70)
    print("TEST: SecureStorage Initialization")
    print("=" * 70)
    
    config = SecureStorageConfig()
    storage = SecureStorage(config)
    
    assert storage.config == config, "Config eşleşmeli"
    assert len(storage.storage) == 0, "Storage boş olmalı"
    
    print(f"  Storage: {len(storage.storage)}")
    
    print("\n" + "=" * 70)
    print("PASS: SecureStorage initialization")
    print("=" * 70)


def test_store():
    """
    Test: Store.
    """
    print("=" * 70)
    print("TEST: Store")
    print("=" * 70)
    
    storage = SecureStorage()
    
    result = storage.store("api_key", "secret_key_123")
    
    assert result.success == True, "Store başarılı olmalı"
    assert len(storage.storage) > 0, "Item eklenmeli"
    
    print(f"  Stored: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Store")
    print("=" * 70)


def test_retrieve():
    """
    Test: Retrieve.
    """
    print("=" * 70)
    print("TEST: Retrieve")
    print("=" * 70)
    
    storage = SecureStorage()
    
    storage.store("api_key", "secret_key_123")
    result = storage.retrieve("api_key")
    
    assert result.success == True, "Retrieve başarılı olmalı"
    assert result.value == "secret_key_123", "Value eşleşmeli"
    
    print(f"  Retrieved: {result.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Retrieve")
    print("=" * 70)


def test_delete():
    """
    Test: Delete.
    """
    print("=" * 70)
    print("TEST: Delete")
    print("=" * 70)
    
    storage = SecureStorage()
    
    storage.store("api_key", "secret_key_123")
    result = storage.delete("api_key")
    
    assert result.success == True, "Silme başarılı olmalı"
    assert "api_key" not in storage.storage, "Item silinmeli"
    
    print(f"  Deleted: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Delete")
    print("=" * 70)


def test_update():
    """
    Test: Update.
    """
    print("=" * 70)
    print("TEST: Update")
    print("=" * 70)
    
    storage = SecureStorage()
    
    storage.store("api_key", "secret_key_123")
    result = storage.update("api_key", "new_secret_key")
    
    assert result.success == True, "Update başarılı olmalı"
    
    print(f"  Updated: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Update")
    print("=" * 70)


def test_exists():
    """
    Test: Exists.
    """
    print("=" * 70)
    print("TEST: Exists")
    print("=" * 70)
    
    storage = SecureStorage()
    
    storage.store("api_key", "secret_key_123")
    exists = storage.exists("api_key")
    
    assert exists == True, "Item bulunmalı"
    
    print(f"  Exists: {exists}")
    
    print("\n" + "=" * 70)
    print("PASS: Exists")
    print("=" * 70)


def test_get_all_keys():
    """
    Test: Get all keys.
    """
    print("=" * 70)
    print("TEST: Get All Keys")
    print("=" * 70)
    
    storage = SecureStorage()
    
    storage.store("api_key", "secret_key_123")
    storage.store("user_token", "token_456")
    
    keys = storage.get_all_keys()
    
    assert len(keys) == 2, "2 key olmalı"
    
    print(f"  Keys: {len(keys)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get all keys")
    print("=" * 70)


def test_get_all_items():
    """
    Test: Get all items.
    """
    print("=" * 70)
    print("TEST: Get All Items")
    print("=" * 70)
    
    storage = SecureStorage()
    
    storage.store("api_key", "secret_key_123")
    storage.store("user_token", "token_456")
    
    items = storage.get_all_items()
    
    assert len(items) == 2, "2 item olmalı"
    
    print(f"  Items: {len(items)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get all items")
    print("=" * 70)


def test_cleanup_expired():
    """
    Test: Cleanup expired.
    """
    print("=" * 70)
    print("TEST: Cleanup Expired")
    print("=" * 70)
    
    storage = SecureStorage()
    
    storage.store("api_key", "secret_key_123", ttl_seconds=-1)
    
    result = storage.cleanup_expired()
    
    assert result.success == True, "Cleanup başarılı olmalı"
    
    print(f"  Cleanup: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Cleanup expired")
    print("=" * 70)


def test_clear_all():
    """
    Test: Clear all.
    """
    print("=" * 70)
    print("TEST: Clear All")
    print("=" * 70)
    
    storage = SecureStorage()
    
    storage.store("api_key", "secret_key_123")
    result = storage.clear_all()
    
    assert result.success == True, "Clear başarılı olmalı"
    assert len(storage.storage) == 0, "Storage boş olmalı"
    
    print(f"  Clear: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear all")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    storage = SecureStorage()
    
    new_config = SecureStorageConfig(enable_encryption=False)
    result = storage.update_config(new_config)
    
    assert result.success == True, "Update başarılı olmalı"
    assert storage.config.enable_encryption == False, "Config güncellenmeli"
    
    print(f"  Enable encryption: {storage.config.enable_encryption}")
    
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
    
    config = SecureStorageConfig(enable_encryption=False)
    storage = SecureStorage(config)
    
    retrieved_config = storage.get_config()
    
    assert retrieved_config.enable_encryption == False, "Config eşleşmeli"
    
    print(f"  Enable encryption: {retrieved_config.enable_encryption}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_storage_type_enum()
        test2 = test_encryption_type_enum()
        test3 = test_access_level_enum()
        test4 = test_storage_item_dataclass()
        test5 = test_secure_storage_config_dataclass()
        test6 = test_secure_storage_result_dataclass()
        test7 = test_secure_storage_initialization()
        test8 = test_store()
        test9 = test_retrieve()
        test10 = test_delete()
        test11 = test_update()
        test12 = test_exists()
        test13 = test_get_all_keys()
        test14 = test_get_all_items()
        test15 = test_cleanup_expired()
        test16 = test_clear_all()
        test17 = test_update_config()
        test18 = test_get_config()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"StorageType Enum: {'PASS' if test1 else 'FAIL'}")
        print(f"EncryptionType Enum: {'PASS' if test2 else 'FAIL'}")
        print(f"AccessLevel Enum: {'PASS' if test3 else 'FAIL'}")
        print(f"StorageItem Dataclass: {'PASS' if test4 else 'FAIL'}")
        print(f"SecureStorageConfig Dataclass: {'PASS' if test5 else 'FAIL'}")
        print(f"SecureStorageResult Dataclass: {'PASS' if test6 else 'FAIL'}")
        print(f"SecureStorage Initialization: {'PASS' if test7 else 'FAIL'}")
        print(f"Store: {'PASS' if test8 else 'FAIL'}")
        print(f"Retrieve: {'PASS' if test9 else 'FAIL'}")
        print(f"Delete: {'PASS' if test10 else 'FAIL'}")
        print(f"Update: {'PASS' if test11 else 'FAIL'}")
        print(f"Exists: {'PASS' if test12 else 'FAIL'}")
        print(f"Get All Keys: {'PASS' if test13 else 'FAIL'}")
        print(f"Get All Items: {'PASS' if test14 else 'FAIL'}")
        print(f"Cleanup Expired: {'PASS' if test15 else 'FAIL'}")
        print(f"Clear All: {'PASS' if test16 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test17 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test18 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14, test15, test16, test17, test18])
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
