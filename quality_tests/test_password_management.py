"""
Quality Test: Password Management
Password management system testleri for security module.
"""

import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from app.security.password_management import (
    PasswordStrength,
    HashAlgorithm,
    PasswordPolicy,
    PasswordPolicyConfig,
    PasswordHash,
    PasswordValidationResult,
    PasswordManagementResult,
    PasswordManager
)


def test_password_strength_enum():
    """
    Test: PasswordStrength enum.
    """
    print("=" * 70)
    print("TEST: PasswordStrength Enum")
    print("=" * 70)
    
    assert PasswordStrength.VERY_WEAK.value == "very_weak"
    assert PasswordStrength.WEAK.value == "weak"
    assert PasswordStrength.MEDIUM.value == "medium"
    assert PasswordStrength.STRONG.value == "strong"
    assert PasswordStrength.VERY_STRONG.value == "very_strong"
    
    print(f"  All enum values verified")
    print(f"  Total strengths: {len(PasswordStrength)}")
    
    print("\n" + "=" * 70)
    print("PASS: PasswordStrength enum")
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
    assert HashAlgorithm.BCRYPT.value == "bcrypt"
    assert HashAlgorithm.ARGON2.value == "argon2"
    assert HashAlgorithm.CUSTOM.value == "custom"
    
    print(f"  All enum values verified")
    print(f"  Total algorithms: {len(HashAlgorithm)}")
    
    print("\n" + "=" * 70)
    print("PASS: HashAlgorithm enum")
    print("=" * 70)


def test_password_policy_enum():
    """
    Test: PasswordPolicy enum.
    """
    print("=" * 70)
    print("TEST: PasswordPolicy Enum")
    print("=" * 70)
    
    assert PasswordPolicy.MIN_LENGTH.value == "min_length"
    assert PasswordPolicy.MAX_LENGTH.value == "max_length"
    assert PasswordPolicy.REQUIRE_UPPERCASE.value == "require_uppercase"
    assert PasswordPolicy.REQUIRE_LOWERCASE.value == "require_lowercase"
    
    print(f"  All enum values verified")
    print(f"  Total policies: {len(PasswordPolicy)}")
    
    print("\n" + "=" * 70)
    print("PASS: PasswordPolicy enum")
    print("=" * 70)


def test_password_policy_config_dataclass():
    """
    Test: PasswordPolicyConfig dataclass.
    """
    print("=" * 70)
    print("TEST: PasswordPolicyConfig Dataclass")
    print("=" * 70)
    
    config = PasswordPolicyConfig(min_length=12)
    
    assert config.min_length == 12, "Min length eşleşmeli"
    
    print(f"  Min length: {config.min_length}")
    
    print("\n" + "=" * 70)
    print("PASS: PasswordPolicyConfig dataclass")
    print("=" * 70)


def test_password_hash_dataclass():
    """
    Test: PasswordHash dataclass.
    """
    print("=" * 70)
    print("TEST: PasswordHash Dataclass")
    print("=" * 70)
    
    password_hash = PasswordHash(
        hash_id="hash_1",
        password_hash="abc123",
        salt="salt123",
        algorithm=HashAlgorithm.SHA256,
        iterations=100000,
        created_at="2024-01-01"
    )
    
    assert password_hash.hash_id == "hash_1", "Hash ID eşleşmeli"
    assert password_hash.algorithm == HashAlgorithm.SHA256, "Algorithm eşleşmeli"
    
    print(f"  Hash ID: {password_hash.hash_id}")
    
    print("\n" + "=" * 70)
    print("PASS: PasswordHash dataclass")
    print("=" * 70)


def test_password_validation_result_dataclass():
    """
    Test: PasswordValidationResult dataclass.
    """
    print("=" * 70)
    print("TEST: PasswordValidationResult Dataclass")
    print("=" * 70)
    
    result = PasswordValidationResult(is_valid=True)
    
    assert result.is_valid == True, "Is valid eşleşmeli"
    assert isinstance(result.errors, list), "Errors list olmalı"
    assert isinstance(result.warnings, list), "Warnings list olmalı"
    
    print(f"  Is valid: {result.is_valid}")
    
    print("\n" + "=" * 70)
    print("PASS: PasswordValidationResult dataclass")
    print("=" * 70)


def test_password_management_result_dataclass():
    """
    Test: PasswordManagementResult dataclass.
    """
    print("=" * 70)
    print("TEST: PasswordManagementResult Dataclass")
    print("=" * 70)
    
    result = PasswordManagementResult(success=True)
    
    assert result.success == True, "Success eşleşmeli"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: PasswordManagementResult dataclass")
    print("=" * 70)


def test_password_manager_initialization():
    """
    Test: PasswordManager initialization.
    """
    print("=" * 70)
    print("TEST: PasswordManager Initialization")
    print("=" * 70)
    
    policy = PasswordPolicyConfig()
    manager = PasswordManager(policy)
    
    assert manager.policy == policy, "Policy eşleşmeli"
    
    print(f"  Manager initialized")
    
    print("\n" + "=" * 70)
    print("PASS: PasswordManager initialization")
    print("=" * 70)


def test_generate_salt():
    """
    Test: Generate salt.
    """
    print("=" * 70)
    print("TEST: Generate Salt")
    print("=" * 70)
    
    manager = PasswordManager()
    
    salt = manager.generate_salt()
    
    assert len(salt) > 0, "Salt oluşturulmalı"
    
    print(f"  Salt length: {len(salt)}")
    
    print("\n" + "=" * 70)
    print("PASS: Generate salt")
    print("=" * 70)


def test_hash_password():
    """
    Test: Hash password.
    """
    print("=" * 70)
    print("TEST: Hash Password")
    print("=" * 70)
    
    manager = PasswordManager()
    
    result = manager.hash_password("MyPassword123!")
    
    assert result.success == True, "Hash başarılı olmalı"
    assert result.password_hash is not None, "Hash olmalı"
    
    print(f"  Hashed: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Hash password")
    print("=" * 70)


def test_verify_password():
    """
    Test: Verify password.
    """
    print("=" * 70)
    print("TEST: Verify Password")
    print("=" * 70)
    
    manager = PasswordManager()
    
    result = manager.hash_password("MyPassword123!")
    password_hash = result.password_hash
    
    is_valid = manager.verify_password("MyPassword123!", password_hash)
    
    assert is_valid == True, "Password valid olmalı"
    
    print(f"  Valid: {is_valid}")
    
    print("\n" + "=" * 70)
    print("PASS: Verify password")
    print("=" * 70)


def test_validate_password():
    """
    Test: Validate password.
    """
    print("=" * 70)
    print("TEST: Validate Password")
    print("=" * 70)
    
    manager = PasswordManager()
    
    result = manager.validate_password("SecurePass123!")
    
    assert result.is_valid == True, "Password valid olmalı"
    assert result.strength is not None, "Strength olmalı"
    
    print(f"  Valid: {result.is_valid}")
    print(f"  Strength: {result.strength.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Validate password")
    print("=" * 70)


def test_generate_password():
    """
    Test: Generate password.
    """
    print("=" * 70)
    print("TEST: Generate Password")
    print("=" * 70)
    
    manager = PasswordManager()
    
    password = manager.generate_password(16)
    
    assert len(password) == 16, "Password length eşleşmeli"
    
    print(f"  Generated: {password}")
    
    print("\n" + "=" * 70)
    print("PASS: Generate password")
    print("=" * 70)


def test_update_policy():
    """
    Test: Update policy.
    """
    print("=" * 70)
    print("TEST: Update Policy")
    print("=" * 70)
    
    manager = PasswordManager()
    
    new_policy = PasswordPolicyConfig(min_length=16)
    result = manager.update_policy(new_policy)
    
    assert result.success == True, "Update başarılı olmalı"
    assert manager.policy.min_length == 16, "Policy güncellenmeli"
    
    print(f"  Min length: {manager.policy.min_length}")
    
    print("\n" + "=" * 70)
    print("PASS: Update policy")
    print("=" * 70)


def test_get_policy():
    """
    Test: Get policy.
    """
    print("=" * 70)
    print("TEST: Get Policy")
    print("=" * 70)
    
    policy = PasswordPolicyConfig(min_length=16)
    manager = PasswordManager(policy)
    
    retrieved_policy = manager.get_policy()
    
    assert retrieved_policy.min_length == 16, "Policy eşleşmeli"
    
    print(f"  Min length: {retrieved_policy.min_length}")
    
    print("\n" + "=" * 70)
    print("PASS: Get policy")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_password_strength_enum()
        test2 = test_hash_algorithm_enum()
        test3 = test_password_policy_enum()
        test4 = test_password_policy_config_dataclass()
        test5 = test_password_hash_dataclass()
        test6 = test_password_validation_result_dataclass()
        test7 = test_password_management_result_dataclass()
        test8 = test_password_manager_initialization()
        test9 = test_generate_salt()
        test10 = test_hash_password()
        test11 = test_verify_password()
        test12 = test_validate_password()
        test13 = test_generate_password()
        test14 = test_update_policy()
        test15 = test_get_policy()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"PasswordStrength Enum: {'PASS' if test1 else 'FAIL'}")
        print(f"HashAlgorithm Enum: {'PASS' if test2 else 'FAIL'}")
        print(f"PasswordPolicy Enum: {'PASS' if test3 else 'FAIL'}")
        print(f"PasswordPolicyConfig Dataclass: {'PASS' if test4 else 'FAIL'}")
        print(f"PasswordHash Dataclass: {'PASS' if test5 else 'FAIL'}")
        print(f"PasswordValidationResult Dataclass: {'PASS' if test6 else 'FAIL'}")
        print(f"PasswordManagementResult Dataclass: {'PASS' if test7 else 'FAIL'}")
        print(f"PasswordManager Initialization: {'PASS' if test8 else 'FAIL'}")
        print(f"Generate Salt: {'PASS' if test9 else 'FAIL'}")
        print(f"Hash Password: {'PASS' if test10 else 'FAIL'}")
        print(f"Verify Password: {'PASS' if test11 else 'FAIL'}")
        print(f"Validate Password: {'PASS' if test12 else 'FAIL'}")
        print(f"Generate Password: {'PASS' if test13 else 'FAIL'}")
        print(f"Update Policy: {'PASS' if test14 else 'FAIL'}")
        print(f"Get Policy: {'PASS' if test15 else 'FAIL'}")
        
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
