"""
Quality Test: CSRF Protection
CSRF protection system testleri for security module.
"""

import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from app.security.csrf_protection import (
    CSRFTokenType,
    CSRFValidationMode,
    CSRFToken,
    CSRFProtectionConfig,
    CSRFProtectionResult,
    CSRFProtection
)


def test_csrf_token_type_enum():
    """
    Test: CSRFTokenType enum.
    """
    print("=" * 70)
    print("TEST: CSRFTokenType Enum")
    print("=" * 70)
    
    assert CSRFTokenType.SESSION.value == "session"
    assert CSRFTokenType.COOKIE.value == "cookie"
    assert CSRFTokenType.HEADER.value == "header"
    assert CSRFTokenType.CUSTOM.value == "custom"
    
    print(f"  All enum values verified")
    print(f"  Total types: {len(CSRFTokenType)}")
    
    print("\n" + "=" * 70)
    print("PASS: CSRFTokenType enum")
    print("=" * 70)


def test_csrf_validation_mode_enum():
    """
    Test: CSRFValidationMode enum.
    """
    print("=" * 70)
    print("TEST: CSRFValidationMode Enum")
    print("=" * 70)
    
    assert CSRFValidationMode.STRICT.value == "strict"
    assert CSRFValidationMode.LENIENT.value == "lenient"
    assert CSRFValidationMode.CUSTOM.value == "custom"
    
    print(f"  All enum values verified")
    print(f"  Total modes: {len(CSRFValidationMode)}")
    
    print("\n" + "=" * 70)
    print("PASS: CSRFValidationMode enum")
    print("=" * 70)


def test_csrf_token_dataclass():
    """
    Test: CSRFToken dataclass.
    """
    print("=" * 70)
    print("TEST: CSRFToken Dataclass")
    print("=" * 70)
    
    token = CSRFToken(
        token_id="csrf_1",
        token_value="test_token_value",
        token_type=CSRFTokenType.SESSION
    )
    
    assert token.token_id == "csrf_1", "Token ID eşleşmeli"
    assert token.token_value == "test_token_value", "Token value eşleşmeli"
    assert token.token_type == CSRFTokenType.SESSION, "Token type eşleşmeli"
    
    print(f"  Token ID: {token.token_id}")
    print(f"  Token value: {token.token_value}")
    
    print("\n" + "=" * 70)
    print("PASS: CSRFToken dataclass")
    print("=" * 70)


def test_csrf_protection_config_dataclass():
    """
    Test: CSRFProtectionConfig dataclass.
    """
    print("=" * 70)
    print("TEST: CSRFProtectionConfig Dataclass")
    print("=" * 70)
    
    config = CSRFProtectionConfig(token_expiry_seconds=7200)
    
    assert config.token_expiry_seconds == 7200, "Token expiry seconds eşleşmeli"
    
    print(f"  Token expiry seconds: {config.token_expiry_seconds}")
    
    print("\n" + "=" * 70)
    print("PASS: CSRFProtectionConfig dataclass")
    print("=" * 70)


def test_csrf_protection_result_dataclass():
    """
    Test: CSRFProtectionResult dataclass.
    """
    print("=" * 70)
    print("TEST: CSRFProtectionResult Dataclass")
    print("=" * 70)
    
    result = CSRFProtectionResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.tokens, list), "Tokens list olmalı"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: CSRFProtectionResult dataclass")
    print("=" * 70)


def test_csrf_protection_initialization():
    """
    Test: CSRFProtection initialization.
    """
    print("=" * 70)
    print("TEST: CSRFProtection Initialization")
    print("=" * 70)
    
    config = CSRFProtectionConfig()
    protection = CSRFProtection(config)
    
    assert protection.config == config, "Config eşleşmeli"
    assert len(protection.tokens) == 0, "Tokens boş olmalı"
    
    print(f"  Tokens: {len(protection.tokens)}")
    
    print("\n" + "=" * 70)
    print("PASS: CSRFProtection initialization")
    print("=" * 70)


def test_generate_token():
    """
    Test: Generate token.
    """
    print("=" * 70)
    print("TEST: Generate Token")
    print("=" * 70)
    
    protection = CSRFProtection()
    
    result = protection.generate_token(user_id="user_1")
    
    assert result.success == True, "Generation başarılı olmalı"
    assert len(protection.tokens) > 0, "Token eklenmeli"
    assert result.token is not None, "Token olmalı"
    
    print(f"  Token generated: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Generate token")
    print("=" * 70)


def test_validate_token():
    """
    Test: Validate token.
    """
    print("=" * 70)
    print("TEST: Validate Token")
    print("=" * 70)
    
    protection = CSRFProtection()
    
    result = protection.generate_token(user_id="user_1")
    token_value = result.token.token_value
    
    validation = protection.validate_token(token_value, user_id="user_1")
    
    assert validation.success == True, "Validation başarılı olmalı"
    assert validation.is_valid == True, "Token valid olmalı"
    
    print(f"  Token valid: {validation.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Validate token")
    print("=" * 70)


def test_revoke_token():
    """
    Test: Revoke token.
    """
    print("=" * 70)
    print("TEST: Revoke Token")
    print("=" * 70)
    
    protection = CSRFProtection()
    
    result = protection.generate_token(user_id="user_1")
    token_id = result.token.token_id
    
    result = protection.revoke_token(token_id)
    
    assert result.success == True, "Revoke başarılı olmalı"
    assert result.token.is_valid == False, "Token invalid olmalı"
    
    print(f"  Token revoked: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Revoke token")
    print("=" * 70)


def test_rotate_token():
    """
    Test: Rotate token.
    """
    print("=" * 70)
    print("TEST: Rotate Token")
    print("=" * 70)
    
    config = CSRFProtectionConfig(enable_token_rotation=True)
    protection = CSRFProtection(config)
    
    result = protection.generate_token(user_id="user_1")
    token_id = result.token.token_id
    old_value = result.token.token_value
    
    result = protection.rotate_token(token_id)
    
    assert result.success == True, "Rotation başarılı olmalı"
    assert result.token.token_value != old_value, "Token value değişmeli"
    
    print(f"  Token rotated: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Rotate token")
    print("=" * 70)


def test_get_token():
    """
    Test: Get token.
    """
    print("=" * 70)
    print("TEST: Get Token")
    print("=" * 70)
    
    protection = CSRFProtection()
    
    result = protection.generate_token(user_id="user_1")
    token_id = result.token.token_id
    
    token = protection.get_token(token_id)
    
    assert token is not None, "Token bulunmalı"
    assert token.token_id == token_id, "Token ID eşleşmeli"
    
    print(f"  Token: {token.token_id}")
    
    print("\n" + "=" * 70)
    print("PASS: Get token")
    print("=" * 70)


def test_get_token_by_value():
    """
    Test: Get token by value.
    """
    print("=" * 70)
    print("TEST: Get Token by Value")
    print("=" * 70)
    
    protection = CSRFProtection()
    
    result = protection.generate_token(user_id="user_1")
    token_value = result.token.token_value
    
    token = protection.get_token_by_value(token_value)
    
    assert token is not None, "Token bulunmalı"
    
    print(f"  Token: {token.token_id}")
    
    print("\n" + "=" * 70)
    print("PASS: Get token by value")
    print("=" * 70)


def test_get_all_tokens():
    """
    Test: Get all tokens.
    """
    print("=" * 70)
    print("TEST: Get All Tokens")
    print("=" * 70)
    
    protection = CSRFProtection()
    
    protection.generate_token(user_id="user_1")
    protection.generate_token(user_id="user_2")
    
    tokens = protection.get_all_tokens()
    
    assert len(tokens) == 2, "2 token olmalı"
    
    print(f"  Total tokens: {len(tokens)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get all tokens")
    print("=" * 70)


def test_get_user_tokens():
    """
    Test: Get user tokens.
    """
    print("=" * 70)
    print("TEST: Get User Tokens")
    print("=" * 70)
    
    protection = CSRFProtection()
    
    protection.generate_token(user_id="user_1")
    protection.generate_token(user_id="user_1")
    
    tokens = protection.get_user_tokens("user_1")
    
    assert len(tokens) == 2, "2 token olmalı"
    
    print(f"  User tokens: {len(tokens)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get user tokens")
    print("=" * 70)


def test_get_session_tokens():
    """
    Test: Get session tokens.
    """
    print("=" * 70)
    print("TEST: Get Session Tokens")
    print("=" * 70)
    
    protection = CSRFProtection()
    
    protection.generate_token(user_id="user_1", session_id="session_1")
    protection.generate_token(user_id="user_2", session_id="session_1")
    
    tokens = protection.get_session_tokens("session_1")
    
    assert len(tokens) == 2, "2 token olmalı"
    
    print(f"  Session tokens: {len(tokens)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get session tokens")
    print("=" * 70)


def test_cleanup_expired_tokens():
    """
    Test: Cleanup expired tokens.
    """
    print("=" * 70)
    print("TEST: Cleanup Expired Tokens")
    print("=" * 70)
    
    protection = CSRFProtection()
    
    protection.generate_token(user_id="user_1", expires_in_seconds=-1)
    
    result = protection.cleanup_expired_tokens()
    
    assert result.success == True, "Cleanup başarılı olmalı"
    
    print(f"  Cleanup: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Cleanup expired tokens")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    protection = CSRFProtection()
    
    new_config = CSRFProtectionConfig(token_expiry_seconds=7200)
    result = protection.update_config(new_config)
    
    assert result.success == True, "Update başarılı olmalı"
    assert protection.config.token_expiry_seconds == 7200, "Config güncellenmeli"
    
    print(f"  Token expiry seconds: {protection.config.token_expiry_seconds}")
    
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
    
    config = CSRFProtectionConfig(token_expiry_seconds=7200)
    protection = CSRFProtection(config)
    
    retrieved_config = protection.get_config()
    
    assert retrieved_config.token_expiry_seconds == 7200, "Config eşleşmeli"
    
    print(f"  Token expiry seconds: {retrieved_config.token_expiry_seconds}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_csrf_token_type_enum()
        test2 = test_csrf_validation_mode_enum()
        test3 = test_csrf_token_dataclass()
        test4 = test_csrf_protection_config_dataclass()
        test5 = test_csrf_protection_result_dataclass()
        test6 = test_csrf_protection_initialization()
        test7 = test_generate_token()
        test8 = test_validate_token()
        test9 = test_revoke_token()
        test10 = test_rotate_token()
        test11 = test_get_token()
        test12 = test_get_token_by_value()
        test13 = test_get_all_tokens()
        test14 = test_get_user_tokens()
        test15 = test_get_session_tokens()
        test16 = test_cleanup_expired_tokens()
        test17 = test_update_config()
        test18 = test_get_config()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"CSRFTokenType Enum: {'PASS' if test1 else 'FAIL'}")
        print(f"CSRFValidationMode Enum: {'PASS' if test2 else 'FAIL'}")
        print(f"CSRFToken Dataclass: {'PASS' if test3 else 'FAIL'}")
        print(f"CSRFProtectionConfig Dataclass: {'PASS' if test4 else 'FAIL'}")
        print(f"CSRFProtectionResult Dataclass: {'PASS' if test5 else 'FAIL'}")
        print(f"CSRFProtection Initialization: {'PASS' if test6 else 'FAIL'}")
        print(f"Generate Token: {'PASS' if test7 else 'FAIL'}")
        print(f"Validate Token: {'PASS' if test8 else 'FAIL'}")
        print(f"Revoke Token: {'PASS' if test9 else 'FAIL'}")
        print(f"Rotate Token: {'PASS' if test10 else 'FAIL'}")
        print(f"Get Token: {'PASS' if test11 else 'FAIL'}")
        print(f"Get Token by Value: {'PASS' if test12 else 'FAIL'}")
        print(f"Get All Tokens: {'PASS' if test13 else 'FAIL'}")
        print(f"Get User Tokens: {'PASS' if test14 else 'FAIL'}")
        print(f"Get Session Tokens: {'PASS' if test15 else 'FAIL'}")
        print(f"Cleanup Expired Tokens: {'PASS' if test16 else 'FAIL'}")
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
