"""
Quality Test: Encryption
Encryption system testleri for security module.
"""

import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from app.security.encryption import (
    EncryptionAlgorithm,
    EncryptionMode,
    HashAlgorithm,
    KeyType,
    EncryptionKey,
    EncryptionConfig,
    EncryptionResult,
    EncryptionManager
)


def test_encryption_algorithm_enum():
    """
    Test: EncryptionAlgorithm enum.
    """
    print("=" * 70)
    print("TEST: EncryptionAlgorithm Enum")
    print("=" * 70)
    
    assert EncryptionAlgorithm.AES_256.value == "aes_256"
    assert EncryptionAlgorithm.AES_128.value == "aes_128"
    assert EncryptionAlgorithm.RSA_4096.value == "rsa_4096"
    assert EncryptionAlgorithm.RSA_2048.value == "rsa_2048"
    assert EncryptionAlgorithm.CUSTOM.value == "custom"
    
    print(f"  All enum values verified")
    print(f"  Total algorithms: {len(EncryptionAlgorithm)}")
    
    print("\n" + "=" * 70)
    print("PASS: EncryptionAlgorithm enum")
    print("=" * 70)


def test_encryption_mode_enum():
    """
    Test: EncryptionMode enum.
    """
    print("=" * 70)
    print("TEST: EncryptionMode Enum")
    print("=" * 70)
    
    assert EncryptionMode.ECB.value == "ecb"
    assert EncryptionMode.CBC.value == "cbc"
    assert EncryptionMode.GCM.value == "gcm"
    assert EncryptionMode.CTR.value == "ctr"
    assert EncryptionMode.CUSTOM.value == "custom"
    
    print(f"  All enum values verified")
    print(f"  Total modes: {len(EncryptionMode)}")
    
    print("\n" + "=" * 70)
    print("PASS: EncryptionMode enum")
    print("=" * 70)


def test_hash_algorithm_enum():
    """
    Test: HashAlgorithm enum.
    """
    print("=" * 70)
    print("TEST: HashAlgorithm Enum")
    print("=" * 70)
    
    assert HashAlgorithm.SHA256.value == "sha256"
    assert HashAlgorithm.SHA512.value == "sha512"
    assert HashAlgorithm.MD5.value == "md5"
    assert HashAlgorithm.SHA1.value == "sha1"
    assert HashAlgorithm.CUSTOM.value == "custom"
    
    print(f"  All enum values verified")
    print(f"  Total algorithms: {len(HashAlgorithm)}")
    
    print("\n" + "=" * 70)
    print("PASS: HashAlgorithm enum")
    print("=" * 70)


def test_key_type_enum():
    """
    Test: KeyType enum.
    """
    print("=" * 70)
    print("TEST: KeyType Enum")
    print("=" * 70)
    
    assert KeyType.SYMMETRIC.value == "symmetric"
    assert KeyType.ASYMMETRIC.value == "asymmetric"
    assert KeyType.HASH.value == "hash"
    assert KeyType.CUSTOM.value == "custom"
    
    print(f"  All enum values verified")
    print(f"  Total types: {len(KeyType)}")
    
    print("\n" + "=" * 70)
    print("PASS: KeyType enum")
    print("=" * 70)


def test_encryption_key_dataclass():
    """
    Test: EncryptionKey dataclass.
    """
    print("=" * 70)
    print("TEST: EncryptionKey Dataclass")
    print("=" * 70)
    
    key = EncryptionKey(
        key_id="key_1",
        key_type=KeyType.SYMMETRIC,
        algorithm=EncryptionAlgorithm.AES_256,
        key_data="encoded_key_data"
    )
    
    assert key.key_id == "key_1", "Key ID eşleşmeli"
    assert key.key_type == KeyType.SYMMETRIC, "Key type eşleşmeli"
    assert key.algorithm == EncryptionAlgorithm.AES_256, "Algorithm eşleşmeli"
    
    print(f"  Key ID: {key.key_id}")
    print(f"  Key type: {key.key_type.value}")
    
    print("\n" + "=" * 70)
    print("PASS: EncryptionKey dataclass")
    print("=" * 70)


def test_encryption_config_dataclass():
    """
    Test: EncryptionConfig dataclass.
    """
    print("=" * 70)
    print("TEST: EncryptionConfig Dataclass")
    print("=" * 70)
    
    config = EncryptionConfig(key_rotation_days=180)
    
    assert config.key_rotation_days == 180, "Key rotation days eşleşmeli"
    
    print(f"  Key rotation days: {config.key_rotation_days}")
    
    print("\n" + "=" * 70)
    print("PASS: EncryptionConfig dataclass")
    print("=" * 70)


def test_encryption_result_dataclass():
    """
    Test: EncryptionResult dataclass.
    """
    print("=" * 70)
    print("TEST: EncryptionResult Dataclass")
    print("=" * 70)
    
    result = EncryptionResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: EncryptionResult dataclass")
    print("=" * 70)


def test_encryption_manager_initialization():
    """
    Test: EncryptionManager initialization.
    """
    print("=" * 70)
    print("TEST: EncryptionManager Initialization")
    print("=" * 70)
    
    config = EncryptionConfig()
    manager = EncryptionManager(config)
    
    assert manager.config == config, "Config eşleşmeli"
    assert len(manager.keys) == 0, "Keys boş olmalı"
    
    print(f"  Keys: {len(manager.keys)}")
    
    print("\n" + "=" * 70)
    print("PASS: EncryptionManager initialization")
    print("=" * 70)


def test_generate_key():
    """
    Test: Generate key.
    """
    print("=" * 70)
    print("TEST: Generate Key")
    print("=" * 70)
    
    manager = EncryptionManager()
    
    result = manager.generate_key(KeyType.SYMMETRIC, EncryptionAlgorithm.AES_256)
    
    assert result.success == True, "Generation başarılı olmalı"
    assert len(manager.keys) > 0, "Key eklenmeli"
    
    print(f"  Key generated: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Generate key")
    print("=" * 70)


def test_encrypt():
    """
    Test: Encrypt.
    """
    print("=" * 70)
    print("TEST: Encrypt")
    print("=" * 70)
    
    manager = EncryptionManager()
    
    key_result = manager.generate_key(KeyType.SYMMETRIC, EncryptionAlgorithm.AES_256)
    encrypt_result = manager.encrypt("Hello, World!", key_result.key.key_id)
    
    assert encrypt_result.success == True, "Encryption başarılı olmalı"
    assert encrypt_result.encrypted_data is not None, "Encrypted data olmalı"
    
    print(f"  Encrypted: {encrypt_result.encrypted_data[:50]}...")
    
    print("\n" + "=" * 70)
    print("PASS: Encrypt")
    print("=" * 70)


def test_decrypt():
    """
    Test: Decrypt.
    """
    print("=" * 70)
    print("TEST: Decrypt")
    print("=" * 70)
    
    manager = EncryptionManager()
    
    key_result = manager.generate_key(KeyType.SYMMETRIC, EncryptionAlgorithm.AES_256)
    encrypt_result = manager.encrypt("Hello, World!", key_result.key.key_id)
    
    decrypt_result = manager.decrypt(encrypt_result.encrypted_data, key_result.key.key_id)
    
    assert decrypt_result.success == True, "Decryption başarılı olmalı"
    assert decrypt_result.decrypted_data == "Hello, World!", "Decrypted data eşleşmeli"
    
    print(f"  Decrypted: {decrypt_result.decrypted_data}")
    
    print("\n" + "=" * 70)
    print("PASS: Decrypt")
    print("=" * 70)


def test_hash():
    """
    Test: Hash.
    """
    print("=" * 70)
    print("TEST: Hash")
    print("=" * 70)
    
    manager = EncryptionManager()
    
    result = manager.hash("Hello, World!")
    
    assert result.success == True, "Hashing başarılı olmalı"
    assert result.hash is not None, "Hash olmalı"
    assert len(result.hash) == 64, "SHA-256 hash 64 karakter olmalı"
    
    print(f"  Hash: {result.hash[:32]}...")
    
    print("\n" + "=" * 70)
    print("PASS: Hash")
    print("=" * 70)


def test_verify_hash():
    """
    Test: Verify hash.
    """
    print("=" * 70)
    print("TEST: Verify Hash")
    print("=" * 70)
    
    manager = EncryptionManager()
    
    hash_result = manager.hash("Hello, World!")
    verify_result = manager.verify_hash("Hello, World!", hash_result.hash)
    
    assert verify_result.success == True, "Verification başarılı olmalı"
    
    print(f"  Hash verified: {verify_result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Verify hash")
    print("=" * 70)


def test_get_key():
    """
    Test: Get key.
    """
    print("=" * 70)
    print("TEST: Get Key")
    print("=" * 70)
    
    manager = EncryptionManager()
    
    result = manager.generate_key(KeyType.SYMMETRIC, EncryptionAlgorithm.AES_256)
    key_id = result.key.key_id
    
    key = manager.get_key(key_id)
    
    assert key is not None, "Key bulunmalı"
    assert key.key_id == key_id, "Key ID eşleşmeli"
    
    print(f"  Key: {key.key_id}")
    
    print("\n" + "=" * 70)
    print("PASS: Get key")
    print("=" * 70)


def test_get_all_keys():
    """
    Test: Get all keys.
    """
    print("=" * 70)
    print("TEST: Get All Keys")
    print("=" * 70)
    
    manager = EncryptionManager()
    
    manager.generate_key(KeyType.SYMMETRIC, EncryptionAlgorithm.AES_256)
    manager.generate_key(KeyType.SYMMETRIC, EncryptionAlgorithm.AES_128)
    
    keys = manager.get_all_keys()
    
    assert len(keys) == 2, "2 key olmalı"
    
    print(f"  Total keys: {len(keys)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get all keys")
    print("=" * 70)


def test_delete_key():
    """
    Test: Delete key.
    """
    print("=" * 70)
    print("TEST: Delete Key")
    print("=" * 70)
    
    manager = EncryptionManager()
    
    result = manager.generate_key(KeyType.SYMMETRIC, EncryptionAlgorithm.AES_256)
    key_id = result.key.key_id
    
    result = manager.delete_key(key_id)
    
    assert result.success == True, "Silme başarılı olmalı"
    assert key_id not in manager.keys, "Key silinmeli"
    
    print(f"  Key deleted: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Delete key")
    print("=" * 70)


def test_rotate_key():
    """
    Test: Rotate key.
    """
    print("=" * 70)
    print("TEST: Rotate Key")
    print("=" * 70)
    
    manager = EncryptionManager()
    
    result = manager.generate_key(KeyType.SYMMETRIC, EncryptionAlgorithm.AES_256)
    key_id = result.key.key_id
    old_key_data = result.key.key_data
    
    result = manager.rotate_key(key_id)
    
    assert result.success == True, "Rotation başarılı olmalı"
    assert result.key.key_data != old_key_data, "Key data değişmeli"
    
    print(f"  Key rotated: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Rotate key")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    manager = EncryptionManager()
    
    new_config = EncryptionConfig(key_rotation_days=180)
    result = manager.update_config(new_config)
    
    assert result.success == True, "Update başarılı olmalı"
    assert manager.config.key_rotation_days == 180, "Config güncellenmeli"
    
    print(f"  Key rotation days: {manager.config.key_rotation_days}")
    
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
    
    config = EncryptionConfig(key_rotation_days=180)
    manager = EncryptionManager(config)
    
    retrieved_config = manager.get_config()
    
    assert retrieved_config.key_rotation_days == 180, "Config eşleşmeli"
    
    print(f"  Key rotation days: {retrieved_config.key_rotation_days}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_encryption_algorithm_enum()
        test2 = test_encryption_mode_enum()
        test3 = test_hash_algorithm_enum()
        test4 = test_key_type_enum()
        test5 = test_encryption_key_dataclass()
        test6 = test_encryption_config_dataclass()
        test7 = test_encryption_result_dataclass()
        test8 = test_encryption_manager_initialization()
        test9 = test_generate_key()
        test10 = test_encrypt()
        test11 = test_decrypt()
        test12 = test_hash()
        test13 = test_verify_hash()
        test14 = test_get_key()
        test15 = test_get_all_keys()
        test16 = test_delete_key()
        test17 = test_rotate_key()
        test18 = test_update_config()
        test19 = test_get_config()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"EncryptionAlgorithm Enum: {'PASS' if test1 else 'FAIL'}")
        print(f"EncryptionMode Enum: {'PASS' if test2 else 'FAIL'}")
        print(f"HashAlgorithm Enum: {'PASS' if test3 else 'FAIL'}")
        print(f"KeyType Enum: {'PASS' if test4 else 'FAIL'}")
        print(f"EncryptionKey Dataclass: {'PASS' if test5 else 'FAIL'}")
        print(f"EncryptionConfig Dataclass: {'PASS' if test6 else 'FAIL'}")
        print(f"EncryptionResult Dataclass: {'PASS' if test7 else 'FAIL'}")
        print(f"EncryptionManager Initialization: {'PASS' if test8 else 'FAIL'}")
        print(f"Generate Key: {'PASS' if test9 else 'FAIL'}")
        print(f"Encrypt: {'PASS' if test10 else 'FAIL'}")
        print(f"Decrypt: {'PASS' if test11 else 'FAIL'}")
        print(f"Hash: {'PASS' if test12 else 'FAIL'}")
        print(f"Verify Hash: {'PASS' if test13 else 'FAIL'}")
        print(f"Get Key: {'PASS' if test14 else 'FAIL'}")
        print(f"Get All Keys: {'PASS' if test15 else 'FAIL'}")
        print(f"Delete Key: {'PASS' if test16 else 'FAIL'}")
        print(f"Rotate Key: {'PASS' if test17 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test18 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test19 else 'FAIL'}")
        
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
