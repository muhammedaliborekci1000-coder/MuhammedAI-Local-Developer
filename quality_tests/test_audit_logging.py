"""
Quality Test: Audit Logging
Audit logging system testleri for security module.
"""

import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from app.security.audit_logging import (
    AuditLogLevel,
    AuditLogCategory,
    AuditLogAction,
    AuditLogEntry,
    AuditLogConfig,
    AuditLogResult,
    AuditLogger
)


def test_audit_log_level_enum():
    """
    Test: AuditLogLevel enum.
    """
    print("=" * 70)
    print("TEST: AuditLogLevel Enum")
    print("=" * 70)
    
    assert AuditLogLevel.DEBUG.value == "debug"
    assert AuditLogLevel.INFO.value == "info"
    assert AuditLogLevel.WARNING.value == "warning"
    assert AuditLogLevel.ERROR.value == "error"
    assert AuditLogLevel.CRITICAL.value == "critical"
    
    print(f"  All enum values verified")
    print(f"  Total levels: {len(AuditLogLevel)}")
    
    print("\n" + "=" * 70)
    print("PASS: AuditLogLevel enum")
    print("=" * 70)


def test_audit_log_category_enum():
    """
    Test: AuditLogCategory enum.
    """
    print("=" * 70)
    print("TEST: AuditLogCategory Enum")
    print("=" * 70)
    
    assert AuditLogCategory.AUTHENTICATION.value == "authentication"
    assert AuditLogCategory.AUTHORIZATION.value == "authorization"
    assert AuditLogCategory.USER_MANAGEMENT.value == "user_management"
    assert AuditLogCategory.ROLE_MANAGEMENT.value == "role_management"
    assert AuditLogCategory.SESSION_MANAGEMENT.value == "session_management"
    assert AuditLogCategory.API_KEY_MANAGEMENT.value == "api_key_management"
    assert AuditLogCategory.ENCRYPTION.value == "encryption"
    assert AuditLogCategory.DATA_ACCESS.value == "data_access"
    assert AuditLogCategory.SYSTEM.value == "system"
    assert AuditLogCategory.CUSTOM.value == "custom"
    
    print(f"  All enum values verified")
    print(f"  Total categories: {len(AuditLogCategory)}")
    
    print("\n" + "=" * 70)
    print("PASS: AuditLogCategory enum")
    print("=" * 70)


def test_audit_log_action_enum():
    """
    Test: AuditLogAction enum.
    """
    print("=" * 70)
    print("TEST: AuditLogAction Enum")
    print("=" * 70)
    
    assert AuditLogAction.CREATE.value == "create"
    assert AuditLogAction.READ.value == "read"
    assert AuditLogAction.UPDATE.value == "update"
    assert AuditLogAction.DELETE.value == "delete"
    assert AuditLogAction.LOGIN.value == "login"
    assert AuditLogAction.LOGOUT.value == "logout"
    assert AuditLogAction.GRANT.value == "grant"
    assert AuditLogAction.REVOKE.value == "revoke"
    assert AuditLogAction.EXPORT.value == "export"
    assert AuditLogAction.IMPORT.value == "import"
    assert AuditLogAction.CUSTOM.value == "custom"
    
    print(f"  All enum values verified")
    print(f"  Total actions: {len(AuditLogAction)}")
    
    print("\n" + "=" * 70)
    print("PASS: AuditLogAction enum")
    print("=" * 70)


def test_audit_log_entry_dataclass():
    """
    Test: AuditLogEntry dataclass.
    """
    print("=" * 70)
    print("TEST: AuditLogEntry Dataclass")
    print("=" * 70)
    
    entry = AuditLogEntry(
        log_id="log_1",
        user_id="user_1",
        action=AuditLogAction.LOGIN,
        category=AuditLogCategory.AUTHENTICATION,
        level=AuditLogLevel.INFO,
        message="User logged in"
    )
    
    assert entry.log_id == "log_1", "Log ID eşleşmeli"
    assert entry.user_id == "user_1", "User ID eşleşmeli"
    assert entry.action == AuditLogAction.LOGIN, "Action eşleşmeli"
    
    print(f"  Log ID: {entry.log_id}")
    print(f"  Message: {entry.message}")
    
    print("\n" + "=" * 70)
    print("PASS: AuditLogEntry dataclass")
    print("=" * 70)


def test_audit_log_config_dataclass():
    """
    Test: AuditLogConfig dataclass.
    """
    print("=" * 70)
    print("TEST: AuditLogConfig Dataclass")
    print("=" * 70)
    
    config = AuditLogConfig(retention_days=180)
    
    assert config.retention_days == 180, "Retention days eşleşmeli"
    
    print(f"  Retention days: {config.retention_days}")
    
    print("\n" + "=" * 70)
    print("PASS: AuditLogConfig dataclass")
    print("=" * 70)


def test_audit_log_result_dataclass():
    """
    Test: AuditLogResult dataclass.
    """
    print("=" * 70)
    print("TEST: AuditLogResult Dataclass")
    print("=" * 70)
    
    result = AuditLogResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.log_entries, list), "Log entries list olmalı"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: AuditLogResult dataclass")
    print("=" * 70)


def test_audit_logger_initialization():
    """
    Test: AuditLogger initialization.
    """
    print("=" * 70)
    print("TEST: AuditLogger Initialization")
    print("=" * 70)
    
    config = AuditLogConfig()
    logger = AuditLogger(config)
    
    assert logger.config == config, "Config eşleşmeli"
    assert len(logger.logs) == 0, "Logs boş olmalı"
    
    print(f"  Logs: {len(logger.logs)}")
    
    print("\n" + "=" * 70)
    print("PASS: AuditLogger initialization")
    print("=" * 70)


def test_log():
    """
    Test: Log.
    """
    print("=" * 70)
    print("TEST: Log")
    print("=" * 70)
    
    logger = AuditLogger()
    
    result = logger.log(
        user_id="user_1",
        action=AuditLogAction.LOGIN,
        category=AuditLogCategory.AUTHENTICATION,
        message="User logged in",
        level=AuditLogLevel.INFO
    )
    
    assert result.success == True, "Log başarılı olmalı"
    assert len(logger.logs) > 0, "Log eklenmeli"
    
    print(f"  Log entry created: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Log")
    print("=" * 70)


def test_get_log():
    """
    Test: Get log.
    """
    print("=" * 70)
    print("TEST: Get Log")
    print("=" * 70)
    
    logger = AuditLogger()
    
    result = logger.log(
        user_id="user_1",
        action=AuditLogAction.LOGIN,
        category=AuditLogCategory.AUTHENTICATION,
        message="User logged in",
        level=AuditLogLevel.INFO
    )
    log_id = result.log_entry.log_id
    
    log = logger.get_log(log_id)
    
    assert log is not None, "Log bulunmalı"
    assert log.log_id == log_id, "Log ID eşleşmeli"
    
    print(f"  Log: {log.log_id}")
    
    print("\n" + "=" * 70)
    print("PASS: Get log")
    print("=" * 70)


def test_get_all_logs():
    """
    Test: Get all logs.
    """
    print("=" * 70)
    print("TEST: Get All Logs")
    print("=" * 70)
    
    logger = AuditLogger()
    
    logger.log("user_1", AuditLogAction.LOGIN, AuditLogCategory.AUTHENTICATION, "User logged in")
    logger.log("user_2", AuditLogAction.LOGOUT, AuditLogCategory.AUTHENTICATION, "User logged out")
    
    logs = logger.get_all_logs()
    
    assert len(logs) == 2, "2 log olmalı"
    
    print(f"  Total logs: {len(logs)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get all logs")
    print("=" * 70)


def test_get_user_logs():
    """
    Test: Get user logs.
    """
    print("=" * 70)
    print("TEST: Get User Logs")
    print("=" * 70)
    
    logger = AuditLogger()
    
    logger.log("user_1", AuditLogAction.LOGIN, AuditLogCategory.AUTHENTICATION, "User logged in")
    logger.log("user_1", AuditLogAction.LOGOUT, AuditLogCategory.AUTHENTICATION, "User logged out")
    
    logs = logger.get_user_logs("user_1")
    
    assert len(logs) == 2, "2 log olmalı"
    
    print(f"  User logs: {len(logs)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get user logs")
    print("=" * 70)


def test_get_logs_by_category():
    """
    Test: Get logs by category.
    """
    print("=" * 70)
    print("TEST: Get Logs by Category")
    print("=" * 70)
    
    logger = AuditLogger()
    
    logger.log("user_1", AuditLogAction.LOGIN, AuditLogCategory.AUTHENTICATION, "User logged in")
    logger.log("user_1", AuditLogAction.CREATE, AuditLogCategory.USER_MANAGEMENT, "User created")
    
    logs = logger.get_logs_by_category(AuditLogCategory.AUTHENTICATION)
    
    assert len(logs) == 1, "1 log olmalı"
    
    print(f"  Category logs: {len(logs)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get logs by category")
    print("=" * 70)


def test_get_logs_by_action():
    """
    Test: Get logs by action.
    """
    print("=" * 70)
    print("TEST: Get Logs by Action")
    print("=" * 70)
    
    logger = AuditLogger()
    
    logger.log("user_1", AuditLogAction.LOGIN, AuditLogCategory.AUTHENTICATION, "User logged in")
    logger.log("user_2", AuditLogAction.LOGIN, AuditLogCategory.AUTHENTICATION, "User logged in")
    
    logs = logger.get_logs_by_action(AuditLogAction.LOGIN)
    
    assert len(logs) == 2, "2 log olmalı"
    
    print(f"  Action logs: {len(logs)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get logs by action")
    print("=" * 70)


def test_get_logs_by_level():
    """
    Test: Get logs by level.
    """
    print("=" * 70)
    print("TEST: Get Logs by Level")
    print("=" * 70)
    
    logger = AuditLogger()
    
    logger.log("user_1", AuditLogAction.LOGIN, AuditLogCategory.AUTHENTICATION, "User logged in", level=AuditLogLevel.INFO)
    logger.log("user_1", AuditLogAction.DELETE, AuditLogCategory.USER_MANAGEMENT, "User deleted", level=AuditLogLevel.ERROR)
    
    logs = logger.get_logs_by_level(AuditLogLevel.INFO)
    
    assert len(logs) == 1, "1 log olmalı"
    
    print(f"  Level logs: {len(logs)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get logs by level")
    print("=" * 70)


def test_search_logs():
    """
    Test: Search logs.
    """
    print("=" * 70)
    print("TEST: Search Logs")
    print("=" * 70)
    
    logger = AuditLogger()
    
    logger.log("user_1", AuditLogAction.LOGIN, AuditLogCategory.AUTHENTICATION, "User logged in")
    logger.log("user_1", AuditLogAction.CREATE, AuditLogCategory.USER_MANAGEMENT, "User created")
    
    logs = logger.search_logs("logged")
    
    assert len(logs) == 1, "1 log olmalı"
    
    print(f"  Search results: {len(logs)}")
    
    print("\n" + "=" * 70)
    print("PASS: Search logs")
    print("=" * 70)


def test_filter_logs():
    """
    Test: Filter logs.
    """
    print("=" * 70)
    print("TEST: Filter Logs")
    print("=" * 70)
    
    logger = AuditLogger()
    
    logger.log("user_1", AuditLogAction.LOGIN, AuditLogCategory.AUTHENTICATION, "User logged in")
    logger.log("user_1", AuditLogAction.CREATE, AuditLogCategory.USER_MANAGEMENT, "User created")
    
    logs = logger.filter_logs(user_id="user_1", category=AuditLogCategory.AUTHENTICATION)
    
    assert len(logs) == 1, "1 log olmalı"
    
    print(f"  Filtered logs: {len(logs)}")
    
    print("\n" + "=" * 70)
    print("PASS: Filter logs")
    print("=" * 70)


def test_export_logs():
    """
    Test: Export logs.
    """
    print("=" * 70)
    print("TEST: Export Logs")
    print("=" * 70)
    
    logger = AuditLogger()
    
    logger.log("user_1", AuditLogAction.LOGIN, AuditLogCategory.AUTHENTICATION, "User logged in")
    
    result = logger.export_logs(format="json")
    
    assert result.success == True, "Export başarılı olmalı"
    
    print(f"  Export: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Export logs")
    print("=" * 70)


def test_clear_logs():
    """
    Test: Clear logs.
    """
    print("=" * 70)
    print("TEST: Clear Logs")
    print("=" * 70)
    
    logger = AuditLogger()
    
    logger.log("user_1", AuditLogAction.LOGIN, AuditLogCategory.AUTHENTICATION, "User logged in")
    
    result = logger.clear_logs()
    
    assert result.success == True, "Clear başarılı olmalı"
    assert len(logger.logs) == 0, "Logs boş olmalı"
    
    print(f"  Clear: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear logs")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    logger = AuditLogger()
    
    new_config = AuditLogConfig(retention_days=180)
    result = logger.update_config(new_config)
    
    assert result.success == True, "Update başarılı olmalı"
    assert logger.config.retention_days == 180, "Config güncellenmeli"
    
    print(f"  Retention days: {logger.config.retention_days}")
    
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
    
    config = AuditLogConfig(retention_days=180)
    logger = AuditLogger(config)
    
    retrieved_config = logger.get_config()
    
    assert retrieved_config.retention_days == 180, "Config eşleşmeli"
    
    print(f"  Retention days: {retrieved_config.retention_days}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_audit_log_level_enum()
        test2 = test_audit_log_category_enum()
        test3 = test_audit_log_action_enum()
        test4 = test_audit_log_entry_dataclass()
        test5 = test_audit_log_config_dataclass()
        test6 = test_audit_log_result_dataclass()
        test7 = test_audit_logger_initialization()
        test8 = test_log()
        test9 = test_get_log()
        test10 = test_get_all_logs()
        test11 = test_get_user_logs()
        test12 = test_get_logs_by_category()
        test13 = test_get_logs_by_action()
        test14 = test_get_logs_by_level()
        test15 = test_search_logs()
        test16 = test_filter_logs()
        test17 = test_export_logs()
        test18 = test_clear_logs()
        test19 = test_update_config()
        test20 = test_get_config()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"AuditLogLevel Enum: {'PASS' if test1 else 'FAIL'}")
        print(f"AuditLogCategory Enum: {'PASS' if test2 else 'FAIL'}")
        print(f"AuditLogAction Enum: {'PASS' if test3 else 'FAIL'}")
        print(f"AuditLogEntry Dataclass: {'PASS' if test4 else 'FAIL'}")
        print(f"AuditLogConfig Dataclass: {'PASS' if test5 else 'FAIL'}")
        print(f"AuditLogResult Dataclass: {'PASS' if test6 else 'FAIL'}")
        print(f"AuditLogger Initialization: {'PASS' if test7 else 'FAIL'}")
        print(f"Log: {'PASS' if test8 else 'FAIL'}")
        print(f"Get Log: {'PASS' if test9 else 'FAIL'}")
        print(f"Get All Logs: {'PASS' if test10 else 'FAIL'}")
        print(f"Get User Logs: {'PASS' if test11 else 'FAIL'}")
        print(f"Get Logs by Category: {'PASS' if test12 else 'FAIL'}")
        print(f"Get Logs by Action: {'PASS' if test13 else 'FAIL'}")
        print(f"Get Logs by Level: {'PASS' if test14 else 'FAIL'}")
        print(f"Search Logs: {'PASS' if test15 else 'FAIL'}")
        print(f"Filter Logs: {'PASS' if test16 else 'FAIL'}")
        print(f"Export Logs: {'PASS' if test17 else 'FAIL'}")
        print(f"Clear Logs: {'PASS' if test18 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test19 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test20 else 'FAIL'}")
        
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
