"""
Quality Test: Terminal Sessions
Terminal sessions system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.tools.terminal_sessions import (
    TerminalSessionsEngine,
    SessionState,
    SessionAction,
    SessionConfig,
    Session,
    SessionResult
)


def test_create_session():
    """
    Test: Create session.
    """
    print("=" * 70)
    print("TEST: Create Session")
    print("=" * 70)
    
    engine = TerminalSessionsEngine()
    result = engine.create_session("Test Session")
    
    assert result.success, "Oluşturma başarılı olmalı"
    assert result.session is not None, "Session olmalı"
    assert result.session.name == "Test Session", "İsim eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Session ID: {result.session_id}")
    print(f"  Session name: {result.session.name}")
    
    print("\n" + "=" * 70)
    print("PASS: Create session")
    print("=" * 70)


def test_create_session_with_details():
    """
    Test: Create session with details.
    """
    print("=" * 70)
    print("TEST: Create Session With Details")
    print("=" * 70)
    
    engine = TerminalSessionsEngine()
    result = engine.create_session(
        "Test Session",
        shell="cmd",
        working_directory="/path/to/project",
        environment={"VAR1": "value1"}
    )
    
    assert result.success, "Oluşturma başarılı olmalı"
    assert result.session.shell == "cmd", "Shell eşleşmeli"
    assert result.session.working_directory == "/path/to/project", "Working directory eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Shell: {result.session.shell}")
    print(f"  Working directory: {result.session.working_directory}")
    
    print("\n" + "=" * 70)
    print("PASS: Create session with details")
    print("=" * 70)


def test_save_session():
    """
    Test: Save session.
    """
    print("=" * 70)
    print("TEST: Save Session")
    print("=" * 70)
    
    engine = TerminalSessionsEngine()
    create_result = engine.create_session("Test Session")
    
    result = engine.save_session(create_result.session_id)
    
    assert result.success, "Kaydetme başarılı olmalı"
    assert result.session.state == SessionState.SAVED, "Durum saved olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  State: {result.session.state.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Save session")
    print("=" * 70)


def test_load_session():
    """
    Test: Load session.
    """
    print("=" * 70)
    print("TEST: Load Session")
    print("=" * 70)
    
    engine = TerminalSessionsEngine()
    create_result = engine.create_session("Test Session")
    
    result = engine.load_session(create_result.session_id)
    
    assert result.success, "Yükleme başarılı olmalı"
    assert result.session.state == SessionState.LOADED, "Durum loaded olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  State: {result.session.state.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Load session")
    print("=" * 70)


def test_delete_session():
    """
    Test: Delete session.
    """
    print("=" * 70)
    print("TEST: Delete Session")
    print("=" * 70)
    
    engine = TerminalSessionsEngine()
    create_result = engine.create_session("Test Session")
    
    result = engine.delete_session(create_result.session_id)
    
    assert result.success, "Silme başarılı olmalı"
    assert engine.get_session(create_result.session_id) is None, "Session silinmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Delete session")
    print("=" * 70)


def test_rename_session():
    """
    Test: Rename session.
    """
    print("=" * 70)
    print("TEST: Rename Session")
    print("=" * 70)
    
    engine = TerminalSessionsEngine()
    create_result = engine.create_session("Test Session")
    
    result = engine.rename_session(create_result.session_id, "Renamed Session")
    
    assert result.success, "Yeniden adlandırma başarılı olmalı"
    assert result.session.name == "Renamed Session", "İsim değişmeli"
    
    print(f"  Success: {result.success}")
    print(f"  New name: {result.session.name}")
    
    print("\n" + "=" * 70)
    print("PASS: Rename session")
    print("=" * 70)


def test_export_session():
    """
    Test: Export session.
    """
    print("=" * 70)
    print("TEST: Export Session")
    print("=" * 70)
    
    engine = TerminalSessionsEngine()
    create_result = engine.create_session("Test Session")
    
    result = engine.export_session(create_result.session_id, format="json")
    
    assert result.success, "Dışa aktarma başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Export session")
    print("=" * 70)


def test_import_session():
    """
    Test: Import session.
    """
    print("=" * 70)
    print("TEST: Import Session")
    print("=" * 70)
    
    engine = TerminalSessionsEngine()
    
    data = {
        "name": "Imported Session",
        "shell": "cmd",
        "working_directory": "/path/to/project",
        "environment": {"VAR1": "value1"}
    }
    
    result = engine.import_session(data)
    
    assert result.success, "İçe aktarma başarılı olmalı"
    assert result.session.name == "Imported Session", "İsim eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Session name: {result.session.name}")
    
    print("\n" + "=" * 70)
    print("PASS: Import session")
    print("=" * 70)


def test_get_session():
    """
    Test: Get session.
    """
    print("=" * 70)
    print("TEST: Get Session")
    print("=" * 70)
    
    engine = TerminalSessionsEngine()
    create_result = engine.create_session("Test Session")
    
    session = engine.get_session(create_result.session_id)
    
    assert session is not None, "Session olmalı"
    assert session.name == "Test Session", "İsim eşleşmeli"
    
    print(f"  Session: {session.name}")
    print(f"  State: {session.state.value}")
    
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
    
    engine = TerminalSessionsEngine()
    engine.create_session("Session 1")
    engine.create_session("Session 2")
    
    sessions = engine.get_all_sessions()
    
    assert len(sessions) == 2, "2 session olmalı"
    
    print(f"  Session count: {len(sessions)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get all sessions")
    print("=" * 70)


def test_get_active_session():
    """
    Test: Get active session.
    """
    print("=" * 70)
    print("TEST: Get Active Session")
    print("=" * 70)
    
    engine = TerminalSessionsEngine()
    create_result = engine.create_session("Test Session")
    
    active_session = engine.get_active_session()
    
    assert active_session is not None, "Aktif session olmalı"
    assert active_session.id == create_result.session_id, "ID eşleşmeli"
    
    print(f"  Active session: {active_session.name}")
    
    print("\n" + "=" * 70)
    print("PASS: Get active session")
    print("=" * 70)


def test_get_session_history():
    """
    Test: Get session history.
    """
    print("=" * 70)
    print("TEST: Get Session History")
    print("=" * 70)
    
    engine = TerminalSessionsEngine()
    engine.create_session("Test Session")
    
    history = engine.get_session_history()
    
    assert len(history) > 0, "Geçmiş olmalı"
    
    print(f"  History: {len(history)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get session history")
    print("=" * 70)


def test_clear_history():
    """
    Test: Clear history.
    """
    print("=" * 70)
    print("TEST: Clear History")
    print("=" * 70)
    
    engine = TerminalSessionsEngine()
    engine.create_session("Test Session")
    
    result = engine.clear_history()
    
    assert result.success, "Temizleme başarılı olmalı"
    assert len(engine.get_session_history()) == 0, "Geçmiş temizlenmeli"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear history")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    engine = TerminalSessionsEngine()
    
    new_config = SessionConfig(shell="cmd")
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
    
    engine = TerminalSessionsEngine()
    
    config = engine.get_config()
    
    assert config is not None, "Config olmalı"
    assert config.shell == "powershell", "Config eşleşmeli"
    
    print(f"  Shell: {config.shell}")
    print(f"  Font size: {config.font_size}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


def test_session_state_enum():
    """
    Test: SessionState enum.
    """
    print("=" * 70)
    print("TEST: SessionState Enum")
    print("=" * 70)
    
    assert SessionState.ACTIVE.value == "active"
    assert SessionState.INACTIVE.value == "inactive"
    assert SessionState.SAVED.value == "saved"
    assert SessionState.LOADED.value == "loaded"
    
    print(f"  All enum values verified")
    print(f"  Total states: {len(SessionState)}")
    
    print("\n" + "=" * 70)
    print("PASS: SessionState enum")
    print("=" * 70)


def test_session_action_enum():
    """
    Test: SessionAction enum.
    """
    print("=" * 70)
    print("TEST: SessionAction Enum")
    print("=" * 70)
    
    assert SessionAction.CREATE.value == "create"
    assert SessionAction.SAVE.value == "save"
    assert SessionAction.LOAD.value == "load"
    assert SessionAction.DELETE.value == "delete"
    assert SessionAction.RENAME.value == "rename"
    
    print(f"  All enum values verified")
    print(f"  Total actions: {len(SessionAction)}")
    
    print("\n" + "=" * 70)
    print("PASS: SessionAction enum")
    print("=" * 70)


def test_session_config_dataclass():
    """
    Test: SessionConfig dataclass.
    """
    print("=" * 70)
    print("TEST: SessionConfig Dataclass")
    print("=" * 70)
    
    config = SessionConfig(
        shell="cmd",
        font_size=16
    )
    
    assert config.shell == "cmd", "Shell eşleşmeli"
    assert config.font_size == 16, "Font size eşleşmeli"
    
    print(f"  Shell: {config.shell}")
    print(f"  Font size: {config.font_size}")
    
    print("\n" + "=" * 70)
    print("PASS: SessionConfig dataclass")
    print("=" * 70)


def test_session_dataclass():
    """
    Test: Session dataclass.
    """
    print("=" * 70)
    print("TEST: Session Dataclass")
    print("=" * 70)
    
    session = Session(
        id="session_1",
        name="Test Session",
        state=SessionState.ACTIVE,
        shell="powershell",
        working_directory="/path/to/project",
        environment={},
        theme="default",
        font_family="Consolas",
        font_size=14,
        created_at="2024-01-01T00:00:00",
        last_modified="2024-01-01T00:00:00"
    )
    
    assert session.id == "session_1", "ID eşleşmeli"
    assert session.name == "Test Session", "İsim eşleşmeli"
    assert session.state == SessionState.ACTIVE, "Durum eşleşmeli"
    
    print(f"  ID: {session.id}")
    print(f"  Name: {session.name}")
    print(f"  State: {session.state.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Session dataclass")
    print("=" * 70)


def test_session_result_dataclass():
    """
    Test: SessionResult dataclass.
    """
    print("=" * 70)
    print("TEST: SessionResult Dataclass")
    print("=" * 70)
    
    result = SessionResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: SessionResult dataclass")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_create_session()
        test2 = test_create_session_with_details()
        test3 = test_save_session()
        test4 = test_load_session()
        test5 = test_delete_session()
        test6 = test_rename_session()
        test7 = test_export_session()
        test8 = test_import_session()
        test9 = test_get_session()
        test10 = test_get_all_sessions()
        test11 = test_get_active_session()
        test12 = test_get_session_history()
        test13 = test_clear_history()
        test14 = test_update_config()
        test15 = test_get_config()
        test16 = test_session_state_enum()
        test17 = test_session_action_enum()
        test18 = test_session_config_dataclass()
        test19 = test_session_dataclass()
        test20 = test_session_result_dataclass()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Create Session: {'PASS' if test1 else 'FAIL'}")
        print(f"Create Session With Details: {'PASS' if test2 else 'FAIL'}")
        print(f"Save Session: {'PASS' if test3 else 'FAIL'}")
        print(f"Load Session: {'PASS' if test4 else 'FAIL'}")
        print(f"Delete Session: {'PASS' if test5 else 'FAIL'}")
        print(f"Rename Session: {'PASS' if test6 else 'FAIL'}")
        print(f"Export Session: {'PASS' if test7 else 'FAIL'}")
        print(f"Import Session: {'PASS' if test8 else 'FAIL'}")
        print(f"Get Session: {'PASS' if test9 else 'FAIL'}")
        print(f"Get All Sessions: {'PASS' if test10 else 'FAIL'}")
        print(f"Get Active Session: {'PASS' if test11 else 'FAIL'}")
        print(f"Get Session History: {'PASS' if test12 else 'FAIL'}")
        print(f"Clear History: {'PASS' if test13 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test14 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test15 else 'FAIL'}")
        print(f"SessionState Enum: {'PASS' if test16 else 'FAIL'}")
        print(f"SessionAction Enum: {'PASS' if test17 else 'FAIL'}")
        print(f"SessionConfig Dataclass: {'PASS' if test18 else 'FAIL'}")
        print(f"Session Dataclass: {'PASS' if test19 else 'FAIL'}")
        print(f"SessionResult Dataclass: {'PASS' if test20 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14, test15, test16, test17, test18, test19, test20])
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
