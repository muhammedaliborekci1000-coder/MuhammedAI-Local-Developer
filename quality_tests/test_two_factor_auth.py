"""
Quality Test: Two-Factor Authentication
Two-factor authentication system testleri for security module.
"""

import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from app.security.two_factor_auth import (
    TwoFactorMethod,
    TwoFactorStatus,
    TwoFactorSecret,
    TwoFactorConfig,
    TwoFactorResult,
    TwoFactorAuth
)


def test_two_factor_method_enum():
    """
    Test: TwoFactorMethod enum.
    """
    print("=" * 70)
    print("TEST: TwoFactorMethod Enum")
    print("=" * 70)
    
    assert TwoFactorMethod.TOTP.value == "totp"
    assert TwoFactorMethod.SMS.value == "sms"
    assert TwoFactorMethod.EMAIL.value == "email"
    assert TwoFactorMethod.AUTHENTICATOR_APP.value == "authenticator_app"
    
    print(f"  All enum values verified")
    print(f"  Total methods: {len(TwoFactorMethod)}")
    
    print("\n" + "=" * 70)
    print("PASS: TwoFactorMethod enum")
    print("=" * 70)


def test_two_factor_status_enum():
    """
    Test: TwoFactorStatus enum.
    """
    print("=" * 70)
    print("TEST: TwoFactorStatus Enum")
    print("=" * 70)
    
    assert TwoFactorStatus.DISABLED.value == "disabled"
    assert TwoFactorStatus.ENABLED.value == "enabled"
    assert TwoFactorStatus.REQUIRED.value == "required"
    assert TwoFactorStatus.VERIFIED.value == "verified"
    assert TwoFactorStatus.LOCKED.value == "locked"
    
    print(f"  All enum values verified")
    print(f"  Total statuses: {len(TwoFactorStatus)}")
    
    print("\n" + "=" * 70)
    print("PASS: TwoFactorStatus enum")
    print("=" * 70)


def test_two_factor_secret_dataclass():
    """
    Test: TwoFactorSecret dataclass.
    """
    print("=" * 70)
    print("TEST: TwoFactorSecret Dataclass")
    print("=" * 70)
    
    secret = TwoFactorSecret(
        secret_id="secret_1",
        user_id="user_1",
        secret="abc123",
        method=TwoFactorMethod.TOTP,
        status=TwoFactorStatus.ENABLED,
        created_at="2024-01-01"
    )
    
    assert secret.secret_id == "secret_1", "Secret ID eşleşmeli"
    assert secret.method == TwoFactorMethod.TOTP, "Method eşleşmeli"
    
    print(f"  Secret ID: {secret.secret_id}")
    
    print("\n" + "=" * 70)
    print("PASS: TwoFactorSecret dataclass")
    print("=" * 70)


def test_two_factor_config_dataclass():
    """
    Test: TwoFactorConfig dataclass.
    """
    print("=" * 70)
    print("TEST: TwoFactorConfig Dataclass")
    print("=" * 70)
    
    config = TwoFactorConfig(require_2fa=True)
    
    assert config.require_2fa == True, "Require 2FA eşleşmeli"
    
    print(f"  Require 2FA: {config.require_2fa}")
    
    print("\n" + "=" * 70)
    print("PASS: TwoFactorConfig dataclass")
    print("=" * 70)


def test_two_factor_result_dataclass():
    """
    Test: TwoFactorResult dataclass.
    """
    print("=" * 70)
    print("TEST: TwoFactorResult Dataclass")
    print("=" * 70)
    
    result = TwoFactorResult(success=True)
    
    assert result.success == True, "Success eşleşmeli"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: TwoFactorResult dataclass")
    print("=" * 70)


def test_two_factor_auth_initialization():
    """
    Test: TwoFactorAuth initialization.
    """
    print("=" * 70)
    print("TEST: TwoFactorAuth Initialization")
    print("=" * 70)
    
    config = TwoFactorConfig()
    auth = TwoFactorAuth(config)
    
    assert auth.config == config, "Config eşleşmeli"
    
    print(f"  Auth initialized")
    
    print("\n" + "=" * 70)
    print("PASS: TwoFactorAuth initialization")
    print("=" * 70)


def test_generate_secret():
    """
    Test: Generate secret.
    """
    print("=" * 70)
    print("TEST: Generate Secret")
    print("=" * 70)
    
    auth = TwoFactorAuth()
    
    result = auth.generate_secret("user_1")
    
    assert result.success == True, "Generation başarılı olmalı"
    assert result.secret is not None, "Secret olmalı"
    
    print(f"  Secret generated: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Generate secret")
    print("=" * 70)


def test_generate_totp():
    """
    Test: Generate TOTP.
    """
    print("=" * 70)
    print("TEST: Generate TOTP")
    print("=" * 70)
    
    auth = TwoFactorAuth()
    
    result = auth.generate_secret("user_1")
    secret_id = result.secret.secret_id
    
    totp_result = auth.generate_totp(secret_id)
    
    assert totp_result.success == True, "TOTP generation başarılı olmalı"
    assert totp_result.code is not None, "Code olmalı"
    
    print(f"  TOTP: {totp_result.code}")
    
    print("\n" + "=" * 70)
    print("PASS: Generate TOTP")
    print("=" * 70)


def test_verify_code():
    """
    Test: Verify code.
    """
    print("=" * 70)
    print("TEST: Verify Code")
    print("=" * 70)
    
    auth = TwoFactorAuth()
    
    result = auth.generate_secret("user_1")
    secret_id = result.secret.secret_id
    
    totp_result = auth.generate_totp(secret_id)
    verify_result = auth.verify_code(secret_id, totp_result.code)
    
    assert verify_result.success == True, "Verification başarılı olmalı"
    assert verify_result.is_valid == True, "Code valid olmalı"
    
    print(f"  Verified: {verify_result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Verify code")
    print("=" * 70)


def test_generate_backup_codes():
    """
    Test: Generate backup codes.
    """
    print("=" * 70)
    print("TEST: Generate Backup Codes")
    print("=" * 70)
    
    auth = TwoFactorAuth()
    
    result = auth.generate_secret("user_1")
    secret_id = result.secret.secret_id
    
    backup_result = auth.generate_backup_codes(secret_id)
    
    assert backup_result.success == True, "Backup codes generation başarılı olmalı"
    
    print(f"  Backup codes: {backup_result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Generate backup codes")
    print("=" * 70)


def test_disable_2fa():
    """
    Test: Disable 2FA.
    """
    print("=" * 70)
    print("TEST: Disable 2FA")
    print("=" * 70)
    
    auth = TwoFactorAuth()
    
    result = auth.generate_secret("user_1")
    secret_id = result.secret.secret_id
    
    disable_result = auth.disable_2fa(secret_id)
    
    assert disable_result.success == True, "Disable başarılı olmalı"
    
    print(f"  Disabled: {disable_result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Disable 2FA")
    print("=" * 70)


def test_get_secret():
    """
    Test: Get secret.
    """
    print("=" * 70)
    print("TEST: Get Secret")
    print("=" * 70)
    
    auth = TwoFactorAuth()
    
    result = auth.generate_secret("user_1")
    secret_id = result.secret.secret_id
    
    secret = auth.get_secret(secret_id)
    
    assert secret is not None, "Secret bulunmalı"
    
    print(f"  Secret found")
    
    print("\n" + "=" * 70)
    print("PASS: Get secret")
    print("=" * 70)


def test_get_user_secrets():
    """
    Test: Get user secrets.
    """
    print("=" * 70)
    print("TEST: Get User Secrets")
    print("=" * 70)
    
    auth = TwoFactorAuth()
    
    auth.generate_secret("user_1")
    auth.generate_secret("user_1")
    
    secrets = auth.get_user_secrets("user_1")
    
    assert len(secrets) == 2, "2 secret olmalı"
    
    print(f"  User secrets: {len(secrets)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get user secrets")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    auth = TwoFactorAuth()
    
    new_config = TwoFactorConfig(require_2fa=True)
    result = auth.update_config(new_config)
    
    assert result.success == True, "Update başarılı olmalı"
    assert auth.config.require_2fa == True, "Config güncellenmeli"
    
    print(f"  Require 2FA: {auth.config.require_2fa}")
    
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
    
    config = TwoFactorConfig(require_2fa=True)
    auth = TwoFactorAuth(config)
    
    retrieved_config = auth.get_config()
    
    assert retrieved_config.require_2fa == True, "Config eşleşmeli"
    
    print(f"  Require 2FA: {retrieved_config.require_2fa}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_two_factor_method_enum()
        test2 = test_two_factor_status_enum()
        test3 = test_two_factor_secret_dataclass()
        test4 = test_two_factor_config_dataclass()
        test5 = test_two_factor_result_dataclass()
        test6 = test_two_factor_auth_initialization()
        test7 = test_generate_secret()
        test8 = test_generate_totp()
        test9 = test_verify_code()
        test10 = test_generate_backup_codes()
        test11 = test_disable_2fa()
        test12 = test_get_secret()
        test13 = test_get_user_secrets()
        test14 = test_update_config()
        test15 = test_get_config()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"TwoFactorMethod Enum: {'PASS' if test1 else 'FAIL'}")
        print(f"TwoFactorStatus Enum: {'PASS' if test2 else 'FAIL'}")
        print(f"TwoFactorSecret Dataclass: {'PASS' if test3 else 'FAIL'}")
        print(f"TwoFactorConfig Dataclass: {'PASS' if test4 else 'FAIL'}")
        print(f"TwoFactorResult Dataclass: {'PASS' if test5 else 'FAIL'}")
        print(f"TwoFactorAuth Initialization: {'PASS' if test6 else 'FAIL'}")
        print(f"Generate Secret: {'PASS' if test7 else 'FAIL'}")
        print(f"Generate TOTP: {'PASS' if test8 else 'FAIL'}")
        print(f"Verify Code: {'PASS' if test9 else 'FAIL'}")
        print(f"Generate Backup Codes: {'PASS' if test10 else 'FAIL'}")
        print(f"Disable 2FA: {'PASS' if test11 else 'FAIL'}")
        print(f"Get Secret: {'PASS' if test12 else 'FAIL'}")
        print(f"Get User Secrets: {'PASS' if test13 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test14 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test15 else 'FAIL'}")
        
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
