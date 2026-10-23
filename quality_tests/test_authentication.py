"""
Quality Test: Authentication
Authentication system testleri for security module.
"""

import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from app.security.authentication import (
    AuthMethod,
    AuthStatus,
    TokenType,
    UserCredentials,
    AuthSession,
    AuthConfig,
    AuthResult,
    AuthenticationManager
)


def test_auth_method_enum():
    """
    Test: AuthMethod enum.
    """
    print("=" * 70)
    print("TEST: AuthMethod Enum")
    print("=" * 70)
    
    assert AuthMethod.PASSWORD.value == "password"
    assert AuthMethod.TOKEN.value == "token"
    assert AuthMethod.OAUTH.value == "oauth"
    assert AuthMethod.SSO.value == "sso"
    assert AuthMethod.BIOMETRIC.value == "biometric"
    assert AuthMethod.TWO_FACTOR.value == "two_factor"
    assert AuthMethod.CUSTOM.value == "custom"
    
    print(f"  All enum values verified")
    print(f"  Total methods: {len(AuthMethod)}")
    
    print("\n" + "=" * 70)
    print("PASS: AuthMethod enum")
    print("=" * 70)


def test_auth_status_enum():
    """
    Test: AuthStatus enum.
    """
    print("=" * 70)
    print("TEST: AuthStatus Enum")
    print("=" * 70)
    
    assert AuthStatus.PENDING.value == "pending"
    assert AuthStatus.SUCCESS.value == "success"
    assert AuthStatus.FAILED.value == "failed"
    assert AuthStatus.EXPIRED.value == "expired"
    assert AuthStatus.REVOKED.value == "revoked"
    assert AuthStatus.LOCKED.value == "locked"
    
    print(f"  All enum values verified")
    print(f"  Total statuses: {len(AuthStatus)}")
    
    print("\n" + "=" * 70)
    print("PASS: AuthStatus enum")
    print("=" * 70)


def test_token_type_enum():
    """
    Test: TokenType enum.
    """
    print("=" * 70)
    print("TEST: TokenType Enum")
    print("=" * 70)
    
    assert TokenType.ACCESS.value == "access"
    assert TokenType.REFRESH.value == "refresh"
    assert TokenType.RESET.value == "reset"
    assert TokenType.VERIFICATION.value == "verification"
    assert TokenType.API_KEY.value == "api_key"
    assert TokenType.CUSTOM.value == "custom"
    
    print(f"  All enum values verified")
    print(f"  Total types: {len(TokenType)}")
    
    print("\n" + "=" * 70)
    print("PASS: TokenType enum")
    print("=" * 70)


def test_user_credentials_dataclass():
    """
    Test: UserCredentials dataclass.
    """
    print("=" * 70)
    print("TEST: UserCredentials Dataclass")
    print("=" * 70)
    
    user = UserCredentials(
        user_id="user_1",
        username="testuser",
        password_hash="hashed_password"
    )
    
    assert user.user_id == "user_1", "User ID eşleşmeli"
    assert user.username == "testuser", "Username eşleşmeli"
    assert user.password_hash == "hashed_password", "Password hash eşleşmeli"
    
    print(f"  User ID: {user.user_id}")
    print(f"  Username: {user.username}")
    
    print("\n" + "=" * 70)
    print("PASS: UserCredentials dataclass")
    print("=" * 70)


def test_auth_session_dataclass():
    """
    Test: AuthSession dataclass.
    """
    print("=" * 70)
    print("TEST: AuthSession Dataclass")
    print("=" * 70)
    
    session = AuthSession(
        session_id="session_1",
        user_id="user_1",
        auth_method=AuthMethod.PASSWORD,
        token="token_123"
    )
    
    assert session.session_id == "session_1", "Session ID eşleşmeli"
    assert session.user_id == "user_1", "User ID eşleşmeli"
    assert session.auth_method == AuthMethod.PASSWORD, "Auth method eşleşmeli"
    
    print(f"  Session ID: {session.session_id}")
    print(f"  User ID: {session.user_id}")
    
    print("\n" + "=" * 70)
    print("PASS: AuthSession dataclass")
    print("=" * 70)


def test_auth_config_dataclass():
    """
    Test: AuthConfig dataclass.
    """
    print("=" * 70)
    print("TEST: AuthConfig Dataclass")
    print("=" * 70)
    
    config = AuthConfig(
        password_min_length=8,
        enable_two_factor=False
    )
    
    assert config.password_min_length == 8, "Password min length eşleşmeli"
    assert config.enable_two_factor == False, "Enable two factor eşleşmeli"
    
    print(f"  Password min length: {config.password_min_length}")
    print(f"  Enable two factor: {config.enable_two_factor}")
    
    print("\n" + "=" * 70)
    print("PASS: AuthConfig dataclass")
    print("=" * 70)


def test_auth_result_dataclass():
    """
    Test: AuthResult dataclass.
    """
    print("=" * 70)
    print("TEST: AuthResult Dataclass")
    print("=" * 70)
    
    result = AuthResult(success=True, status=AuthStatus.SUCCESS)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.status == AuthStatus.SUCCESS, "Status eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Status: {result.status.value}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: AuthResult dataclass")
    print("=" * 70)


def test_authentication_manager_initialization():
    """
    Test: AuthenticationManager initialization.
    """
    print("=" * 70)
    print("TEST: AuthenticationManager Initialization")
    print("=" * 70)
    
    config = AuthConfig()
    manager = AuthenticationManager(config)
    
    assert manager.config == config, "Config eşleşmeli"
    assert len(manager.users) == 0, "Users boş olmalı"
    assert len(manager.sessions) == 0, "Sessions boş olmalı"
    
    print(f"  Users: {len(manager.users)}")
    print(f"  Sessions: {len(manager.sessions)}")
    
    print("\n" + "=" * 70)
    print("PASS: AuthenticationManager initialization")
    print("=" * 70)


def test_hash_password():
    """
    Test: Hash password.
    """
    print("=" * 70)
    print("TEST: Hash Password")
    print("=" * 70)
    
    manager = AuthenticationManager()
    
    password = "TestPass123!"
    hashed = manager.hash_password(password)
    
    assert hashed != password, "Hash farklı olmalı"
    assert len(hashed) == 64, "SHA-256 hash 64 karakter olmalı"
    
    print(f"  Password hashed successfully")
    
    print("\n" + "=" * 70)
    print("PASS: Hash password")
    print("=" * 70)


def test_validate_password():
    """
    Test: Validate password.
    """
    print("=" * 70)
    print("TEST: Validate Password")
    print("=" * 70)
    
    manager = AuthenticationManager()
    
    # Valid password
    valid = manager.validate_password("TestPass123!")
    assert valid == True, "Valid password geçmeli"
    
    # Invalid password (too short)
    invalid = manager.validate_password("Test1!")
    assert invalid == False, "Invalid password geçmemeli"
    
    print(f"  Password validation working")
    
    print("\n" + "=" * 70)
    print("PASS: Validate password")
    print("=" * 70)


def test_register_user():
    """
    Test: Register user.
    """
    print("=" * 70)
    print("TEST: Register User")
    print("=" * 70)
    
    manager = AuthenticationManager()
    
    result = manager.register_user("testuser", "TestPass123!", "test@example.com")
    
    assert result.success == True, "Kayıt başarılı olmalı"
    assert len(manager.users) > 0, "User eklenmeli"
    
    print(f"  User registered: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Register user")
    print("=" * 70)


def test_authenticate():
    """
    Test: Authenticate.
    """
    print("=" * 70)
    print("TEST: Authenticate")
    print("=" * 70)
    
    manager = AuthenticationManager()
    
    # Register user
    manager.register_user("testuser", "TestPass123!", "test@example.com")
    
    # Authenticate
    result = manager.authenticate("testuser", "TestPass123!")
    
    assert result.success == True, "Authentication başarılı olmalı"
    assert result.token is not None, "Token olmalı"
    
    print(f"  Authentication: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Authenticate")
    print("=" * 70)


def test_verify_token():
    """
    Test: Verify token.
    """
    print("=" * 70)
    print("TEST: Verify Token")
    print("=" * 70)
    
    manager = AuthenticationManager()
    
    # Register and authenticate
    manager.register_user("testuser", "TestPass123!", "test@example.com")
    auth_result = manager.authenticate("testuser", "TestPass123!")
    
    # Verify token
    result = manager.verify_token(auth_result.token)
    
    assert result.success == True, "Token doğrulama başarılı olmalı"
    
    print(f"  Token verification: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Verify token")
    print("=" * 70)


def test_refresh_token():
    """
    Test: Refresh token.
    """
    print("=" * 70)
    print("TEST: Refresh Token")
    print("=" * 70)
    
    manager = AuthenticationManager()
    
    # Register and authenticate
    manager.register_user("testuser", "TestPass123!", "test@example.com")
    auth_result = manager.authenticate("testuser", "TestPass123!")
    
    # Get refresh token
    session = manager.get_session(auth_result.session.session_id)
    refresh_token = session.refresh_token
    
    # Refresh token
    result = manager.refresh_token(refresh_token)
    
    assert result.success == True, "Token refresh başarılı olmalı"
    
    print(f"  Token refresh: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Refresh token")
    print("=" * 70)


def test_logout():
    """
    Test: Logout.
    """
    print("=" * 70)
    print("TEST: Logout")
    print("=" * 70)
    
    manager = AuthenticationManager()
    
    # Register and authenticate
    manager.register_user("testuser", "TestPass123!", "test@example.com")
    auth_result = manager.authenticate("testuser", "TestPass123!")
    
    # Logout
    result = manager.logout(auth_result.session.session_id)
    
    assert result.success == True, "Logout başarılı olmalı"
    
    print(f"  Logout: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Logout")
    print("=" * 70)


def test_revoke_token():
    """
    Test: Revoke token.
    """
    print("=" * 70)
    print("TEST: Revoke Token")
    print("=" * 70)
    
    manager = AuthenticationManager()
    
    # Register and authenticate
    manager.register_user("testuser", "TestPass123!", "test@example.com")
    auth_result = manager.authenticate("testuser", "TestPass123!")
    
    # Revoke token
    result = manager.revoke_token(auth_result.token)
    
    assert result.success == True, "Token revocation başarılı olmalı"
    
    print(f"  Token revocation: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Revoke token")
    print("=" * 70)


def test_change_password():
    """
    Test: Change password.
    """
    print("=" * 70)
    print("TEST: Change Password")
    print("=" * 70)
    
    manager = AuthenticationManager()
    
    # Register user
    result = manager.register_user("testuser", "TestPass123!", "test@example.com")
    user_id = list(manager.users.keys())[0]
    
    # Change password
    result = manager.change_password(user_id, "TestPass123!", "NewPass456!")
    
    assert result.success == True, "Password değişimi başarılı olmalı"
    
    print(f"  Password change: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Change password")
    print("=" * 70)


def test_get_user():
    """
    Test: Get user.
    """
    print("=" * 70)
    print("TEST: Get User")
    print("=" * 70)
    
    manager = AuthenticationManager()
    
    # Register user
    result = manager.register_user("testuser", "TestPass123!", "test@example.com")
    user_id = list(manager.users.keys())[0]
    
    # Get user
    user = manager.get_user(user_id)
    
    assert user is not None, "User bulunmalı"
    assert user.username == "testuser", "Username eşleşmeli"
    
    print(f"  User: {user.username}")
    
    print("\n" + "=" * 70)
    print("PASS: Get user")
    print("=" * 70)


def test_get_all_users():
    """
    Test: Get all users.
    """
    print("=" * 70)
    print("TEST: Get All Users")
    print("=" * 70)
    
    manager = AuthenticationManager()
    
    # Register users
    manager.register_user("testuser1", "TestPass123!", "test1@example.com")
    manager.register_user("testuser2", "TestPass123!", "test2@example.com")
    
    # Get all users
    users = manager.get_all_users()
    
    assert len(users) == 2, "2 user olmalı"
    
    print(f"  Total users: {len(users)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get all users")
    print("=" * 70)


def test_get_session():
    """
    Test: Get session.
    """
    print("=" * 70)
    print("TEST: Get Session")
    print("=" * 70)
    
    manager = AuthenticationManager()
    
    # Register and authenticate
    manager.register_user("testuser", "TestPass123!", "test@example.com")
    auth_result = manager.authenticate("testuser", "TestPass123!")
    
    # Get session
    session = manager.get_session(auth_result.session.session_id)
    
    assert session is not None, "Session bulunmalı"
    
    print(f"  Session: {session.session_id}")
    
    print("\n" + "=" * 70)
    print("PASS: Get session")
    print("=" * 70)


def test_get_all_sessions():
    """
    Test: Get all sessions.
    """
    print("=" * 70)
    print("TEST: Get All Sessions")
    print("=" * 70)
    
    manager = AuthenticationManager()
    
    # Register and authenticate
    manager.register_user("testuser", "TestPass123!", "test@example.com")
    manager.authenticate("testuser", "TestPass123!")
    
    # Get all sessions
    sessions = manager.get_all_sessions()
    
    assert len(sessions) > 0, "Session olmalı"
    
    print(f"  Total sessions: {len(sessions)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get all sessions")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    manager = AuthenticationManager()
    
    new_config = AuthConfig(password_min_length=12)
    result = manager.update_config(new_config)
    
    assert result.success == True, "Update başarılı olmalı"
    assert manager.config.password_min_length == 12, "Config güncellenmeli"
    
    print(f"  Password min length: {manager.config.password_min_length}")
    
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
    
    config = AuthConfig(password_min_length=12)
    manager = AuthenticationManager(config)
    
    retrieved_config = manager.get_config()
    
    assert retrieved_config.password_min_length == 12, "Config eşleşmeli"
    
    print(f"  Password min length: {retrieved_config.password_min_length}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_auth_method_enum()
        test2 = test_auth_status_enum()
        test3 = test_token_type_enum()
        test4 = test_user_credentials_dataclass()
        test5 = test_auth_session_dataclass()
        test6 = test_auth_config_dataclass()
        test7 = test_auth_result_dataclass()
        test8 = test_authentication_manager_initialization()
        test9 = test_hash_password()
        test10 = test_validate_password()
        test11 = test_register_user()
        test12 = test_authenticate()
        test13 = test_verify_token()
        test14 = test_refresh_token()
        test15 = test_logout()
        test16 = test_revoke_token()
        test17 = test_change_password()
        test18 = test_get_user()
        test19 = test_get_all_users()
        test20 = test_get_session()
        test21 = test_get_all_sessions()
        test22 = test_update_config()
        test23 = test_get_config()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"AuthMethod Enum: {'PASS' if test1 else 'FAIL'}")
        print(f"AuthStatus Enum: {'PASS' if test2 else 'FAIL'}")
        print(f"TokenType Enum: {'PASS' if test3 else 'FAIL'}")
        print(f"UserCredentials Dataclass: {'PASS' if test4 else 'FAIL'}")
        print(f"AuthSession Dataclass: {'PASS' if test5 else 'FAIL'}")
        print(f"AuthConfig Dataclass: {'PASS' if test6 else 'FAIL'}")
        print(f"AuthResult Dataclass: {'PASS' if test7 else 'FAIL'}")
        print(f"AuthenticationManager Initialization: {'PASS' if test8 else 'FAIL'}")
        print(f"Hash Password: {'PASS' if test9 else 'FAIL'}")
        print(f"Validate Password: {'PASS' if test10 else 'FAIL'}")
        print(f"Register User: {'PASS' if test11 else 'FAIL'}")
        print(f"Authenticate: {'PASS' if test12 else 'FAIL'}")
        print(f"Verify Token: {'PASS' if test13 else 'FAIL'}")
        print(f"Refresh Token: {'PASS' if test14 else 'FAIL'}")
        print(f"Logout: {'PASS' if test15 else 'FAIL'}")
        print(f"Revoke Token: {'PASS' if test16 else 'FAIL'}")
        print(f"Change Password: {'PASS' if test17 else 'FAIL'}")
        print(f"Get User: {'PASS' if test18 else 'FAIL'}")
        print(f"Get All Users: {'PASS' if test19 else 'FAIL'}")
        print(f"Get Session: {'PASS' if test20 else 'FAIL'}")
        print(f"Get All Sessions: {'PASS' if test21 else 'FAIL'}")
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
