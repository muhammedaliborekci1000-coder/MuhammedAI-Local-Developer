"""
Quality Test: Session Management
Session management system testleri for security module.
"""

import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from app.security.session_management import (
    SessionStatus,
    SessionType,
    SessionData,
    Session,
    SessionManagementConfig,
    SessionManagementResult,
    SessionManager
)


def test_session_status_enum():
    """
    Test: SessionStatus enum.
    """
    print("=" * 70)
    print("TEST: SessionStatus Enum")
    print("=" * 70)
    
    assert SessionStatus.ACTIVE.value == "active"
    assert SessionStatus.INACTIVE.value == "inactive"
    assert SessionStatus.EXPIRED.value == "expired"
    assert SessionStatus.REVOKED.value == "revoked"
    assert SessionStatus.TERMINATED.value == "terminated"
    
    print(f"  All enum values verified")
    print(f"  Total statuses: {len(SessionStatus)}")
    
    print("\n" + "=" * 70)
    print("PASS: SessionStatus enum")
    print("=" * 70)


def test_session_type_enum():
    """
    Test: SessionType enum.
    """
    print("=" * 70)
    print("TEST: SessionType Enum")
    print("=" * 70)
    
    assert SessionType.WEB.value == "web"
    assert SessionType.API.value == "api"
    assert SessionType.DESKTOP.value == "desktop"
    assert SessionType.MOBILE.value == "mobile"
    assert SessionType.CUSTOM.value == "custom"
    
    print(f"  All enum values verified")
    print(f"  Total types: {len(SessionType)}")
    
    print("\n" + "=" * 70)
    print("PASS: SessionType enum")
    print("=" * 70)


def test_session_data_dataclass():
    """
    Test: SessionData dataclass.
    """
    print("=" * 70)
    print("TEST: SessionData Dataclass")
    print("=" * 70)
    
    data = SessionData(key="test_key", value="test_value")
    
    assert data.key == "test_key", "Key eşleşmeli"
    assert data.value == "test_value", "Value eşleşmeli"
    
    print(f"  Key: {data.key}")
    print(f"  Value: {data.value}")
    
    print("\n" + "=" * 70)
    print("PASS: SessionData dataclass")
    print("=" * 70)


def test_session_dataclass():
    """
    Test: Session dataclass.
    """
    print("=" * 70)
    print("TEST: Session Dataclass")
    print("=" * 70)
    
    session = Session(
        session_id="session_1",
        user_id="user_1",
        session_type=SessionType.WEB,
        token="token_123"
    )
    
    assert session.session_id == "session_1", "Session ID eşleşmeli"
    assert session.user_id == "user_1", "User ID eşleşmeli"
    assert session.session_type == SessionType.WEB, "Session type eşleşmeli"
    
    print(f"  Session ID: {session.session_id}")
    print(f"  User ID: {session.user_id}")
    
    print("\n" + "=" * 70)
    print("PASS: Session dataclass")
    print("=" * 70)


def test_session_management_config_dataclass():
    """
    Test: SessionManagementConfig dataclass.
    """
    print("=" * 70)
    print("TEST: SessionManagementConfig Dataclass")
    print("=" * 70)
    
    config = SessionManagementConfig(session_timeout=3600)
    
    assert config.session_timeout == 3600, "Session timeout eşleşmeli"
    
    print(f"  Session timeout: {config.session_timeout}")
    
    print("\n" + "=" * 70)
    print("PASS: SessionManagementConfig dataclass")
    print("=" * 70)


def test_session_management_result_dataclass():
    """
    Test: SessionManagementResult dataclass.
    """
    print("=" * 70)
    print("TEST: SessionManagementResult Dataclass")
    print("=" * 70)
    
    result = SessionManagementResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.sessions, list), "Sessions list olmalı"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: SessionManagementResult dataclass")
    print("=" * 70)


def test_session_manager_initialization():
    """
    Test: SessionManager initialization.
    """
    print("=" * 70)
    print("TEST: SessionManager Initialization")
    print("=" * 70)
    
    config = SessionManagementConfig()
    manager = SessionManager(config)
    
    assert manager.config == config, "Config eşleşmeli"
    assert len(manager.sessions) == 0, "Sessions boş olmalı"
    
    print(f"  Sessions: {len(manager.sessions)}")
    
    print("\n" + "=" * 70)
    print("PASS: SessionManager initialization")
    print("=" * 70)


def test_create_session():
    """
    Test: Create session.
    """
    print("=" * 70)
    print("TEST: Create Session")
    print("=" * 70)
    
    manager = SessionManager()
    
    result = manager.create_session("user_1", SessionType.WEB)
    
    assert result.success == True, "Ekleme başarılı olmalı"
    assert len(manager.sessions) > 0, "Session eklenmeli"
    
    print(f"  Session created: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Create session")
    print("=" * 70)


def test_delete_session():
    """
    Test: Delete session.
    """
    print("=" * 70)
    print("TEST: Delete Session")
    print("=" * 70)
    
    manager = SessionManager()
    
    result = manager.create_session("user_1", SessionType.WEB)
    session_id = result.session.session_id
    
    result = manager.delete_session(session_id)
    
    assert result.success == True, "Silme başarılı olmalı"
    assert session_id not in manager.sessions, "Session silinmeli"
    
    print(f"  Session deleted: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Delete session")
    print("=" * 70)


def test_update_session():
    """
    Test: Update session.
    """
    print("=" * 70)
    print("TEST: Update Session")
    print("=" * 70)
    
    manager = SessionManager()
    
    result = manager.create_session("user_1", SessionType.WEB)
    session_id = result.session.session_id
    
    result = manager.update_session(session_id, ip_address="192.168.1.1")
    
    assert result.success == True, "Update başarılı olmalı"
    
    print(f"  Session updated: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Update session")
    print("=" * 70)


def test_get_session():
    """
    Test: Get session.
    """
    print("=" * 70)
    print("TEST: Get Session")
    print("=" * 70)
    
    manager = SessionManager()
    
    result = manager.create_session("user_1", SessionType.WEB)
    session_id = result.session.session_id
    
    session = manager.get_session(session_id)
    
    assert session is not None, "Session bulunmalı"
    assert session.user_id == "user_1", "User ID eşleşmeli"
    
    print(f"  Session: {session.session_id}")
    
    print("\n" + "=" * 70)
    print("PASS: Get session")
    print("=" * 70)


def test_get_session_by_token():
    """
    Test: Get session by token.
    """
    print("=" * 70)
    print("TEST: Get Session by Token")
    print("=" * 70)
    
    manager = SessionManager()
    
    result = manager.create_session("user_1", SessionType.WEB)
    token = result.token
    
    session = manager.get_session_by_token(token)
    
    assert session is not None, "Session bulunmalı"
    
    print(f"  Session: {session.session_id}")
    
    print("\n" + "=" * 70)
    print("PASS: Get session by token")
    print("=" * 70)


def test_get_all_sessions():
    """
    Test: Get all sessions.
    """
    print("=" * 70)
    print("TEST: Get All Sessions")
    print("=" * 70)
    
    manager = SessionManager()
    
    manager.create_session("user_1", SessionType.WEB)
    manager.create_session("user_2", SessionType.API)
    
    sessions = manager.get_all_sessions()
    
    assert len(sessions) == 2, "2 session olmalı"
    
    print(f"  Total sessions: {len(sessions)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get all sessions")
    print("=" * 70)


def test_get_user_sessions():
    """
    Test: Get user sessions.
    """
    print("=" * 70)
    print("TEST: Get User Sessions")
    print("=" * 70)
    
    manager = SessionManager()
    
    manager.create_session("user_1", SessionType.WEB)
    manager.create_session("user_1", SessionType.API)
    
    sessions = manager.get_user_sessions("user_1")
    
    assert len(sessions) == 2, "2 session olmalı"
    
    print(f"  User sessions: {len(sessions)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get user sessions")
    print("=" * 70)


def test_validate_session():
    """
    Test: Validate session.
    """
    print("=" * 70)
    print("TEST: Validate Session")
    print("=" * 70)
    
    manager = SessionManager()
    
    result = manager.create_session("user_1", SessionType.WEB)
    session_id = result.session.session_id
    
    result = manager.validate_session(session_id)
    
    assert result.success == True, "Validation başarılı olmalı"
    
    print(f"  Session valid: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Validate session")
    print("=" * 70)


def test_refresh_session():
    """
    Test: Refresh session.
    """
    print("=" * 70)
    print("TEST: Refresh Session")
    print("=" * 70)
    
    manager = SessionManager()
    
    result = manager.create_session("user_1", SessionType.WEB)
    session_id = result.session.session_id
    
    result = manager.refresh_session(session_id)
    
    assert result.success == True, "Refresh başarılı olmalı"
    
    print(f"  Session refreshed: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Refresh session")
    print("=" * 70)


def test_terminate_session():
    """
    Test: Terminate session.
    """
    print("=" * 70)
    print("TEST: Terminate Session")
    print("=" * 70)
    
    manager = SessionManager()
    
    result = manager.create_session("user_1", SessionType.WEB)
    session_id = result.session.session_id
    
    result = manager.terminate_session(session_id)
    
    assert result.success == True, "Terminate başarılı olmalı"
    
    print(f"  Session terminated: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Terminate session")
    print("=" * 70)


def test_revoke_session():
    """
    Test: Revoke session.
    """
    print("=" * 70)
    print("TEST: Revoke Session")
    print("=" * 70)
    
    manager = SessionManager()
    
    result = manager.create_session("user_1", SessionType.WEB)
    session_id = result.session.session_id
    
    result = manager.revoke_session(session_id)
    
    assert result.success == True, "Revoke başarılı olmalı"
    
    print(f"  Session revoked: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Revoke session")
    print("=" * 70)


def test_set_session_data():
    """
    Test: Set session data.
    """
    print("=" * 70)
    print("TEST: Set Session Data")
    print("=" * 70)
    
    manager = SessionManager()
    
    result = manager.create_session("user_1", SessionType.WEB)
    session_id = result.session.session_id
    
    result = manager.set_session_data(session_id, "test_key", "test_value")
    
    assert result.success == True, "Set başarılı olmalı"
    
    print(f"  Session data set: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set session data")
    print("=" * 70)


def test_get_session_data():
    """
    Test: Get session data.
    """
    print("=" * 70)
    print("TEST: Get Session Data")
    print("=" * 70)
    
    manager = SessionManager()
    
    result = manager.create_session("user_1", SessionType.WEB)
    session_id = result.session.session_id
    
    manager.set_session_data(session_id, "test_key", "test_value")
    value = manager.get_session_data(session_id, "test_key")
    
    assert value == "test_value", "Value eşleşmeli"
    
    print(f"  Session data: {value}")
    
    print("\n" + "=" * 70)
    print("PASS: Get session data")
    print("=" * 70)


def test_remove_session_data():
    """
    Test: Remove session data.
    """
    print("=" * 70)
    print("TEST: Remove Session Data")
    print("=" * 70)
    
    manager = SessionManager()
    
    result = manager.create_session("user_1", SessionType.WEB)
    session_id = result.session.session_id
    
    manager.set_session_data(session_id, "test_key", "test_value")
    result = manager.remove_session_data(session_id, "test_key")
    
    assert result.success == True, "Remove başarılı olmalı"
    
    print(f"  Session data removed: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Remove session data")
    print("=" * 70)


def test_cleanup_expired_sessions():
    """
    Test: Cleanup expired sessions.
    """
    print("=" * 70)
    print("TEST: Cleanup Expired Sessions")
    print("=" * 70)
    
    manager = SessionManager()
    
    result = manager.create_session("user_1", SessionType.WEB)
    
    result = manager.cleanup_expired_sessions()
    
    assert result.success == True, "Cleanup başarılı olmalı"
    
    print(f"  Cleanup: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Cleanup expired sessions")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    manager = SessionManager()
    
    new_config = SessionManagementConfig(session_timeout=7200)
    result = manager.update_config(new_config)
    
    assert result.success == True, "Update başarılı olmalı"
    assert manager.config.session_timeout == 7200, "Config güncellenmeli"
    
    print(f"  Session timeout: {manager.config.session_timeout}")
    
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
    
    config = SessionManagementConfig(session_timeout=7200)
    manager = SessionManager(config)
    
    retrieved_config = manager.get_config()
    
    assert retrieved_config.session_timeout == 7200, "Config eşleşmeli"
    
    print(f"  Session timeout: {retrieved_config.session_timeout}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_session_status_enum()
        test2 = test_session_type_enum()
        test3 = test_session_data_dataclass()
        test4 = test_session_dataclass()
        test5 = test_session_management_config_dataclass()
        test6 = test_session_management_result_dataclass()
        test7 = test_session_manager_initialization()
        test8 = test_create_session()
        test9 = test_delete_session()
        test10 = test_update_session()
        test11 = test_get_session()
        test12 = test_get_session_by_token()
        test13 = test_get_all_sessions()
        test14 = test_get_user_sessions()
        test15 = test_validate_session()
        test16 = test_refresh_session()
        test17 = test_terminate_session()
        test18 = test_revoke_session()
        test19 = test_set_session_data()
        test20 = test_get_session_data()
        test21 = test_remove_session_data()
        test22 = test_cleanup_expired_sessions()
        test23 = test_update_config()
        test24 = test_get_config()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"SessionStatus Enum: {'PASS' if test1 else 'FAIL'}")
        print(f"SessionType Enum: {'PASS' if test2 else 'FAIL'}")
        print(f"SessionData Dataclass: {'PASS' if test3 else 'FAIL'}")
        print(f"Session Dataclass: {'PASS' if test4 else 'FAIL'}")
        print(f"SessionManagementConfig Dataclass: {'PASS' if test5 else 'FAIL'}")
        print(f"SessionManagementResult Dataclass: {'PASS' if test6 else 'FAIL'}")
        print(f"SessionManager Initialization: {'PASS' if test7 else 'FAIL'}")
        print(f"Create Session: {'PASS' if test8 else 'FAIL'}")
        print(f"Delete Session: {'PASS' if test9 else 'FAIL'}")
        print(f"Update Session: {'PASS' if test10 else 'FAIL'}")
        print(f"Get Session: {'PASS' if test11 else 'FAIL'}")
        print(f"Get Session by Token: {'PASS' if test12 else 'FAIL'}")
        print(f"Get All Sessions: {'PASS' if test13 else 'FAIL'}")
        print(f"Get User Sessions: {'PASS' if test14 else 'FAIL'}")
        print(f"Validate Session: {'PASS' if test15 else 'FAIL'}")
        print(f"Refresh Session: {'PASS' if test16 else 'FAIL'}")
        print(f"Terminate Session: {'PASS' if test17 else 'FAIL'}")
        print(f"Revoke Session: {'PASS' if test18 else 'FAIL'}")
        print(f"Set Session Data: {'PASS' if test19 else 'FAIL'}")
        print(f"Get Session Data: {'PASS' if test20 else 'FAIL'}")
        print(f"Remove Session Data: {'PASS' if test21 else 'FAIL'}")
        print(f"Cleanup Expired Sessions: {'PASS' if test22 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test23 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test24 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14, test15, test16, test17, test18, test19, test20, test21, test22, test23, test24])
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
