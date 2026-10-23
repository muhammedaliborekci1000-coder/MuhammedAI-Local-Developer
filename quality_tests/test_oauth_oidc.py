"""
Quality Test: OAuth/OIDC Integration
OAuth/OIDC integration system testleri for security module.
"""

import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from app.security.oauth_oidc import (
    OAuthProvider,
    OAuthGrantType,
    OAuthScope,
    OAuthClient,
    OAuthToken,
    OAuthConfig,
    OAuthResult,
    OAuthManager
)


def test_oauth_provider_enum():
    """
    Test: OAuthProvider enum.
    """
    print("=" * 70)
    print("TEST: OAuthProvider Enum")
    print("=" * 70)
    
    assert OAuthProvider.GOOGLE.value == "google"
    assert OAuthProvider.GITHUB.value == "github"
    assert OAuthProvider.FACEBOOK.value == "facebook"
    assert OAuthProvider.MICROSOFT.value == "microsoft"
    
    print(f"  All enum values verified")
    print(f"  Total providers: {len(OAuthProvider)}")
    
    print("\n" + "=" * 70)
    print("PASS: OAuthProvider enum")
    print("=" * 70)


def test_oauth_grant_type_enum():
    """
    Test: OAuthGrantType enum.
    """
    print("=" * 70)
    print("TEST: OAuthGrantType Enum")
    print("=" * 70)
    
    assert OAuthGrantType.AUTHORIZATION_CODE.value == "authorization_code"
    assert OAuthGrantType.IMPLICIT.value == "implicit"
    assert OAuthGrantType.PASSWORD.value == "password"
    assert OAuthGrantType.CLIENT_CREDENTIALS.value == "client_credentials"
    assert OAuthGrantType.REFRESH_TOKEN.value == "refresh_token"
    
    print(f"  All enum values verified")
    print(f"  Total grant types: {len(OAuthGrantType)}")
    
    print("\n" + "=" * 70)
    print("PASS: OAuthGrantType enum")
    print("=" * 70)


def test_oauth_scope_enum():
    """
    Test: OAuthScope enum.
    """
    print("=" * 70)
    print("TEST: OAuthScope Enum")
    print("=" * 70)
    
    assert OAuthScope.OPENID.value == "openid"
    assert OAuthScope.PROFILE.value == "profile"
    assert OAuthScope.EMAIL.value == "email"
    assert OAuthScope.OFFLINE_ACCESS.value == "offline_access"
    
    print(f"  All enum values verified")
    print(f"  Total scopes: {len(OAuthScope)}")
    
    print("\n" + "=" * 70)
    print("PASS: OAuthScope enum")
    print("=" * 70)


def test_oauth_client_dataclass():
    """
    Test: OAuthClient dataclass.
    """
    print("=" * 70)
    print("TEST: OAuthClient Dataclass")
    print("=" * 70)
    
    client = OAuthClient(
        client_id="client_1",
        client_secret="secret_123",
        provider=OAuthProvider.GOOGLE,
        redirect_uri="http://localhost:8080/callback",
        scopes=["openid", "profile"]
    )
    
    assert client.client_id == "client_1", "Client ID eşleşmeli"
    assert client.provider == OAuthProvider.GOOGLE, "Provider eşleşmeli"
    
    print(f"  Client ID: {client.client_id}")
    
    print("\n" + "=" * 70)
    print("PASS: OAuthClient dataclass")
    print("=" * 70)


def test_oauth_token_dataclass():
    """
    Test: OAuthToken dataclass.
    """
    print("=" * 70)
    print("TEST: OAuthToken Dataclass")
    print("=" * 70)
    
    token = OAuthToken(
        token_id="token_1",
        user_id="user_1",
        client_id="client_1",
        access_token="access_123",
        refresh_token="refresh_123",
        token_type="Bearer",
        expires_in=3600,
        scope="openid profile",
        created_at="1234567890",
        expires_at="1234571490"
    )
    
    assert token.token_id == "token_1", "Token ID eşleşmeli"
    assert token.token_type == "Bearer", "Token type eşleşmeli"
    
    print(f"  Token ID: {token.token_id}")
    
    print("\n" + "=" * 70)
    print("PASS: OAuthToken dataclass")
    print("=" * 70)


def test_oauth_config_dataclass():
    """
    Test: OAuthConfig dataclass.
    """
    print("=" * 70)
    print("TEST: OAuthConfig Dataclass")
    print("=" * 70)
    
    config = OAuthConfig(enable_oidc=True)
    
    assert config.enable_oidc == True, "Enable OIDC eşleşmeli"
    
    print(f"  Enable OIDC: {config.enable_oidc}")
    
    print("\n" + "=" * 70)
    print("PASS: OAuthConfig dataclass")
    print("=" * 70)


def test_oauth_result_dataclass():
    """
    Test: OAuthResult dataclass.
    """
    print("=" * 70)
    print("TEST: OAuthResult Dataclass")
    print("=" * 70)
    
    result = OAuthResult(success=True)
    
    assert result.success == True, "Success eşleşmeli"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: OAuthResult dataclass")
    print("=" * 70)


def test_oauth_manager_initialization():
    """
    Test: OAuthManager initialization.
    """
    print("=" * 70)
    print("TEST: OAuthManager Initialization")
    print("=" * 70)
    
    config = OAuthConfig()
    manager = OAuthManager(config)
    
    assert manager.config == config, "Config eşleşmeli"
    
    print(f"  Manager initialized")
    
    print("\n" + "=" * 70)
    print("PASS: OAuthManager initialization")
    print("=" * 70)


def test_register_client():
    """
    Test: Register client.
    """
    print("=" * 70)
    print("TEST: Register Client")
    print("=" * 70)
    
    manager = OAuthManager()
    
    result = manager.register_client(
        client_id="client_1",
        client_secret="secret_123",
        provider=OAuthProvider.GOOGLE,
        redirect_uri="http://localhost:8080/callback",
        scopes=["openid", "profile"]
    )
    
    assert result.success == True, "Registration başarılı olmalı"
    
    print(f"  Client registered: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Register client")
    print("=" * 70)


def test_generate_auth_url():
    """
    Test: Generate auth URL.
    """
    print("=" * 70)
    print("TEST: Generate Auth URL")
    print("=" * 70)
    
    manager = OAuthManager()
    
    manager.register_client(
        client_id="client_1",
        client_secret="secret_123",
        provider=OAuthProvider.GOOGLE,
        redirect_uri="http://localhost:8080/callback",
        scopes=["openid", "profile"]
    )
    
    result = manager.generate_auth_url("client_1")
    
    assert result.success == True, "Auth URL generation başarılı olmalı"
    assert result.auth_url is not None, "Auth URL olmalı"
    
    print(f"  Auth URL: {result.auth_url}")
    
    print("\n" + "=" * 70)
    print("PASS: Generate auth URL")
    print("=" * 70)


def test_exchange_code_for_token():
    """
    Test: Exchange code for token.
    """
    print("=" * 70)
    print("TEST: Exchange Code for Token")
    print("=" * 70)
    
    manager = OAuthManager()
    
    manager.register_client(
        client_id="client_1",
        client_secret="secret_123",
        provider=OAuthProvider.GOOGLE,
        redirect_uri="http://localhost:8080/callback",
        scopes=["openid", "profile"]
    )
    
    result = manager.exchange_code_for_token("client_1", "auth_code_123", user_id="user_1")
    
    assert result.success == True, "Token exchange başarılı olmalı"
    assert result.token is not None, "Token olmalı"
    
    print(f"  Token exchanged: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Exchange code for token")
    print("=" * 70)


def test_refresh_token():
    """
    Test: Refresh token.
    """
    print("=" * 70)
    print("TEST: Refresh Token")
    print("=" * 70)
    
    manager = OAuthManager()
    
    manager.register_client(
        client_id="client_1",
        client_secret="secret_123",
        provider=OAuthProvider.GOOGLE,
        redirect_uri="http://localhost:8080/callback",
        scopes=["openid", "profile"]
    )
    
    exchange_result = manager.exchange_code_for_token("client_1", "auth_code_123", user_id="user_1")
    refresh_token = exchange_result.token.refresh_token
    
    result = manager.refresh_token(refresh_token)
    
    assert result.success == True, "Refresh başarılı olmalı"
    
    print(f"  Token refreshed: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Refresh token")
    print("=" * 70)


def test_validate_token():
    """
    Test: Validate token.
    """
    print("=" * 70)
    print("TEST: Validate Token")
    print("=" * 70)
    
    manager = OAuthManager()
    
    manager.register_client(
        client_id="client_1",
        client_secret="secret_123",
        provider=OAuthProvider.GOOGLE,
        redirect_uri="http://localhost:8080/callback",
        scopes=["openid", "profile"]
    )
    
    exchange_result = manager.exchange_code_for_token("client_1", "auth_code_123", user_id="user_1")
    access_token = exchange_result.token.access_token
    
    is_valid = manager.validate_token(access_token)
    
    assert is_valid == True, "Token valid olmalı"
    
    print(f"  Valid: {is_valid}")
    
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
    
    manager = OAuthManager()
    
    manager.register_client(
        client_id="client_1",
        client_secret="secret_123",
        provider=OAuthProvider.GOOGLE,
        redirect_uri="http://localhost:8080/callback",
        scopes=["openid", "profile"]
    )
    
    exchange_result = manager.exchange_code_for_token("client_1", "auth_code_123", user_id="user_1")
    token_id = exchange_result.token.token_id
    
    result = manager.revoke_token(token_id)
    
    assert result.success == True, "Revoke başarılı olmalı"
    
    print(f"  Token revoked: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Revoke token")
    print("=" * 70)


def test_get_client():
    """
    Test: Get client.
    """
    print("=" * 70)
    print("TEST: Get Client")
    print("=" * 70)
    
    manager = OAuthManager()
    
    manager.register_client(
        client_id="client_1",
        client_secret="secret_123",
        provider=OAuthProvider.GOOGLE,
        redirect_uri="http://localhost:8080/callback",
        scopes=["openid", "profile"]
    )
    
    client = manager.get_client("client_1")
    
    assert client is not None, "Client bulunmalı"
    
    print(f"  Client found")
    
    print("\n" + "=" * 70)
    print("PASS: Get client")
    print("=" * 70)


def test_get_token():
    """
    Test: Get token.
    """
    print("=" * 70)
    print("TEST: Get Token")
    print("=" * 70)
    
    manager = OAuthManager()
    
    manager.register_client(
        client_id="client_1",
        client_secret="secret_123",
        provider=OAuthProvider.GOOGLE,
        redirect_uri="http://localhost:8080/callback",
        scopes=["openid", "profile"]
    )
    
    exchange_result = manager.exchange_code_for_token("client_1", "auth_code_123", user_id="user_1")
    token_id = exchange_result.token.token_id
    
    token = manager.get_token(token_id)
    
    assert token is not None, "Token bulunmalı"
    
    print(f"  Token found")
    
    print("\n" + "=" * 70)
    print("PASS: Get token")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    manager = OAuthManager()
    
    new_config = OAuthConfig(enable_oidc=False)
    result = manager.update_config(new_config)
    
    assert result.success == True, "Update başarılı olmalı"
    assert manager.config.enable_oidc == False, "Config güncellenmeli"
    
    print(f"  Enable OIDC: {manager.config.enable_oidc}")
    
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
    
    config = OAuthConfig(enable_oidc=False)
    manager = OAuthManager(config)
    
    retrieved_config = manager.get_config()
    
    assert retrieved_config.enable_oidc == False, "Config eşleşmeli"
    
    print(f"  Enable OIDC: {retrieved_config.enable_oidc}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_oauth_provider_enum()
        test2 = test_oauth_grant_type_enum()
        test3 = test_oauth_scope_enum()
        test4 = test_oauth_client_dataclass()
        test5 = test_oauth_token_dataclass()
        test6 = test_oauth_config_dataclass()
        test7 = test_oauth_result_dataclass()
        test8 = test_oauth_manager_initialization()
        test9 = test_register_client()
        test10 = test_generate_auth_url()
        test11 = test_exchange_code_for_token()
        test12 = test_refresh_token()
        test13 = test_validate_token()
        test14 = test_revoke_token()
        test15 = test_get_client()
        test16 = test_get_token()
        test17 = test_update_config()
        test18 = test_get_config()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"OAuthProvider Enum: {'PASS' if test1 else 'FAIL'}")
        print(f"OAuthGrantType Enum: {'PASS' if test2 else 'FAIL'}")
        print(f"OAuthScope Enum: {'PASS' if test3 else 'FAIL'}")
        print(f"OAuthClient Dataclass: {'PASS' if test4 else 'FAIL'}")
        print(f"OAuthToken Dataclass: {'PASS' if test5 else 'FAIL'}")
        print(f"OAuthConfig Dataclass: {'PASS' if test6 else 'FAIL'}")
        print(f"OAuthResult Dataclass: {'PASS' if test7 else 'FAIL'}")
        print(f"OAuthManager Initialization: {'PASS' if test8 else 'FAIL'}")
        print(f"Register Client: {'PASS' if test9 else 'FAIL'}")
        print(f"Generate Auth URL: {'PASS' if test10 else 'FAIL'}")
        print(f"Exchange Code for Token: {'PASS' if test11 else 'FAIL'}")
        print(f"Refresh Token: {'PASS' if test12 else 'FAIL'}")
        print(f"Validate Token: {'PASS' if test13 else 'FAIL'}")
        print(f"Revoke Token: {'PASS' if test14 else 'FAIL'}")
        print(f"Get Client: {'PASS' if test15 else 'FAIL'}")
        print(f"Get Token: {'PASS' if test16 else 'FAIL'}")
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
