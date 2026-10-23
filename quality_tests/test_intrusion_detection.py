"""
Quality Test: Intrusion Detection
Intrusion detection system testleri for security module.
"""

import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from app.security.intrusion_detection import (
    IntrusionType,
    IntrusionSeverity,
    IntrusionStatus,
    IntrusionAlert,
    DetectionRule,
    IntrusionDetectionConfig,
    IntrusionDetectionResult,
    IntrusionDetectionManager
)


def test_intrusion_type_enum():
    """
    Test: IntrusionType enum.
    """
    print("=" * 70)
    print("TEST: IntrusionType Enum")
    print("=" * 70)
    
    assert IntrusionType.BRUTE_FORCE.value == "brute_force"
    assert IntrusionType.SQL_INJECTION.value == "sql_injection"
    assert IntrusionType.XSS_ATTACK.value == "xss_attack"
    assert IntrusionType.DDOS.value == "ddos"
    
    print(f"  All enum values verified")
    print(f"  Total types: {len(IntrusionType)}")
    
    print("\n" + "=" * 70)
    print("PASS: IntrusionType enum")
    print("=" * 70)


def test_intrusion_severity_enum():
    """
    Test: IntrusionSeverity enum.
    """
    print("=" * 70)
    print("TEST: IntrusionSeverity Enum")
    print("=" * 70)
    
    assert IntrusionSeverity.LOW.value == "low"
    assert IntrusionSeverity.MEDIUM.value == "medium"
    assert IntrusionSeverity.HIGH.value == "high"
    assert IntrusionSeverity.CRITICAL.value == "critical"
    
    print(f"  All enum values verified")
    print(f"  Total severities: {len(IntrusionSeverity)}")
    
    print("\n" + "=" * 70)
    print("PASS: IntrusionSeverity enum")
    print("=" * 70)


def test_intrusion_status_enum():
    """
    Test: IntrusionStatus enum.
    """
    print("=" * 70)
    print("TEST: IntrusionStatus Enum")
    print("=" * 70)
    
    assert IntrusionStatus.DETECTED.value == "detected"
    assert IntrusionStatus.INVESTIGATING.value == "investigating"
    assert IntrusionStatus.CONFIRMED.value == "confirmed"
    assert IntrusionStatus.FALSE_POSITIVE.value == "false_positive"
    assert IntrusionStatus.RESOLVED.value == "resolved"
    
    print(f"  All enum values verified")
    print(f"  Total statuses: {len(IntrusionStatus)}")
    
    print("\n" + "=" * 70)
    print("PASS: IntrusionStatus enum")
    print("=" * 70)


def test_intrusion_alert_dataclass():
    """
    Test: IntrusionAlert dataclass.
    """
    print("=" * 70)
    print("TEST: IntrusionAlert Dataclass")
    print("=" * 70)
    
    alert = IntrusionAlert(
        alert_id="alert_1",
        intrusion_type=IntrusionType.SQL_INJECTION,
        severity=IntrusionSeverity.HIGH,
        status=IntrusionStatus.DETECTED
    )
    
    assert alert.alert_id == "alert_1", "Alert ID eşleşmeli"
    assert alert.intrusion_type == IntrusionType.SQL_INJECTION, "Type eşleşmeli"
    
    print(f"  Alert ID: {alert.alert_id}")
    
    print("\n" + "=" * 70)
    print("PASS: IntrusionAlert dataclass")
    print("=" * 70)


def test_detection_rule_dataclass():
    """
    Test: DetectionRule dataclass.
    """
    print("=" * 70)
    print("TEST: DetectionRule Dataclass")
    print("=" * 70)
    
    rule = DetectionRule(
        rule_id="rule_1",
        name="SQL Injection",
        intrusion_type=IntrusionType.SQL_INJECTION,
        pattern=r"union.*select",
        severity=IntrusionSeverity.HIGH
    )
    
    assert rule.rule_id == "rule_1", "Rule ID eşleşmeli"
    assert rule.intrusion_type == IntrusionType.SQL_INJECTION, "Type eşleşmeli"
    
    print(f"  Rule ID: {rule.rule_id}")
    
    print("\n" + "=" * 70)
    print("PASS: DetectionRule dataclass")
    print("=" * 70)


def test_intrusion_detection_config_dataclass():
    """
    Test: IntrusionDetectionConfig dataclass.
    """
    print("=" * 70)
    print("TEST: IntrusionDetectionConfig Dataclass")
    print("=" * 70)
    
    config = IntrusionDetectionConfig(enable_auto_blocking=True)
    
    assert config.enable_auto_blocking == True, "Enable auto blocking eşleşmeli"
    
    print(f"  Enable auto blocking: {config.enable_auto_blocking}")
    
    print("\n" + "=" * 70)
    print("PASS: IntrusionDetectionConfig dataclass")
    print("=" * 70)


def test_intrusion_detection_result_dataclass():
    """
    Test: IntrusionDetectionResult dataclass.
    """
    print("=" * 70)
    print("TEST: IntrusionDetectionResult Dataclass")
    print("=" * 70)
    
    result = IntrusionDetectionResult(success=True)
    
    assert result.success == True, "Success eşleşmeli"
    assert isinstance(result.alerts, list), "Alerts list olmalı"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: IntrusionDetectionResult dataclass")
    print("=" * 70)


def test_intrusion_detection_manager_initialization():
    """
    Test: IntrusionDetectionManager initialization.
    """
    print("=" * 70)
    print("TEST: IntrusionDetectionManager Initialization")
    print("=" * 70)
    
    config = IntrusionDetectionConfig()
    manager = IntrusionDetectionManager(config)
    
    assert manager.config == config, "Config eşleşmeli"
    
    print(f"  Manager initialized")
    
    print("\n" + "=" * 70)
    print("PASS: IntrusionDetectionManager initialization")
    print("=" * 70)


def test_add_rule():
    """
    Test: Add rule.
    """
    print("=" * 70)
    print("TEST: Add Rule")
    print("=" * 70)
    
    manager = IntrusionDetectionManager()
    
    result = manager.add_rule(
        name="Custom Rule",
        intrusion_type=IntrusionType.ANOMALY,
        pattern=r"anomaly",
        severity=IntrusionSeverity.MEDIUM
    )
    
    assert result.success == True, "Ekleme başarılı olmalı"
    
    print(f"  Rule added: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add rule")
    print("=" * 70)


def test_detect_intrusion():
    """
    Test: Detect intrusion.
    """
    print("=" * 70)
    print("TEST: Detect Intrusion")
    print("=" * 70)
    
    manager = IntrusionDetectionManager()
    
    result = manager.detect_intrusion("SELECT * FROM users WHERE 1=1", source_ip="192.168.1.1")
    
    assert result.is_intrusion == True, "Intrusion tespit edilmeli"
    
    print(f"  Detected: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Detect intrusion")
    print("=" * 70)


def test_update_alert_status():
    """
    Test: Update alert status.
    """
    print("=" * 70)
    print("TEST: Update Alert Status")
    print("=" * 70)
    
    manager = IntrusionDetectionManager()
    
    result = manager.detect_intrusion("SELECT * FROM users WHERE 1=1")
    alert_id = result.alert.alert_id
    
    update_result = manager.update_alert_status(alert_id, IntrusionStatus.INVESTIGATING)
    
    assert update_result.success == True, "Update başarılı olmalı"
    
    print(f"  Status updated: {update_result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Update alert status")
    print("=" * 70)


def test_get_alert():
    """
    Test: Get alert.
    """
    print("=" * 70)
    print("TEST: Get Alert")
    print("=" * 70)
    
    manager = IntrusionDetectionManager()
    
    result = manager.detect_intrusion("SELECT * FROM users WHERE 1=1")
    alert_id = result.alert.alert_id
    
    alert = manager.get_alert(alert_id)
    
    assert alert is not None, "Alert bulunmalı"
    
    print(f"  Alert found")
    
    print("\n" + "=" * 70)
    print("PASS: Get alert")
    print("=" * 70)


def test_get_alerts_by_type():
    """
    Test: Get alerts by type.
    """
    print("=" * 70)
    print("TEST: Get Alerts by Type")
    print("=" * 70)
    
    manager = IntrusionDetectionManager()
    
    manager.detect_intrusion("SELECT * FROM users WHERE 1=1")
    manager.detect_intrusion("UNION SELECT * FROM users")
    
    alerts = manager.get_alerts_by_type(IntrusionType.SQL_INJECTION)
    
    assert len(alerts) >= 1, "SQL injection alert olmalı"
    
    print(f"  SQL injection alerts: {len(alerts)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get alerts by type")
    print("=" * 70)


def test_get_alerts_by_severity():
    """
    Test: Get alerts by severity.
    """
    print("=" * 70)
    print("TEST: Get Alerts by Severity")
    print("=" * 70)
    
    manager = IntrusionDetectionManager()
    
    manager.detect_intrusion("SELECT * FROM users WHERE 1=1")
    manager.detect_intrusion("<script>alert('xss')</script>")
    
    alerts = manager.get_alerts_by_severity(IntrusionSeverity.HIGH)
    
    assert len(alerts) >= 1, "HIGH severity alert olmalı"
    
    print(f"  HIGH severity alerts: {len(alerts)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get alerts by severity")
    print("=" * 70)


def test_get_all_alerts():
    """
    Test: Get all alerts.
    """
    print("=" * 70)
    print("TEST: Get All Alerts")
    print("=" * 70)
    
    manager = IntrusionDetectionManager()
    
    manager.detect_intrusion("SELECT * FROM users WHERE 1=1")
    manager.detect_intrusion("<script>alert('xss')</script>")
    
    alerts = manager.get_all_alerts()
    
    assert len(alerts) >= 1, "Alert olmalı"
    
    print(f"  Alerts: {len(alerts)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get all alerts")
    print("=" * 70)


def test_cleanup_old_alerts():
    """
    Test: Cleanup old alerts.
    """
    print("=" * 70)
    print("TEST: Cleanup Old Alerts")
    print("=" * 70)
    
    manager = IntrusionDetectionManager()
    
    result = manager.cleanup_old_alerts()
    
    assert result.success == True, "Cleanup başarılı olmalı"
    
    print(f"  Cleanup: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Cleanup old alerts")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    manager = IntrusionDetectionManager()
    
    new_config = IntrusionDetectionConfig(enable_auto_blocking=True)
    result = manager.update_config(new_config)
    
    assert result.success == True, "Update başarılı olmalı"
    assert manager.config.enable_auto_blocking == True, "Config güncellenmeli"
    
    print(f"  Enable auto blocking: {manager.config.enable_auto_blocking}")
    
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
    
    config = IntrusionDetectionConfig(enable_auto_blocking=True)
    manager = IntrusionDetectionManager(config)
    
    retrieved_config = manager.get_config()
    
    assert retrieved_config.enable_auto_blocking == True, "Config eşleşmeli"
    
    print(f"  Enable auto blocking: {retrieved_config.enable_auto_blocking}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_intrusion_type_enum()
        test2 = test_intrusion_severity_enum()
        test3 = test_intrusion_status_enum()
        test4 = test_intrusion_alert_dataclass()
        test5 = test_detection_rule_dataclass()
        test6 = test_intrusion_detection_config_dataclass()
        test7 = test_intrusion_detection_result_dataclass()
        test8 = test_intrusion_detection_manager_initialization()
        test9 = test_add_rule()
        test10 = test_detect_intrusion()
        test11 = test_update_alert_status()
        test12 = test_get_alert()
        test13 = test_get_alerts_by_type()
        test14 = test_get_alerts_by_severity()
        test15 = test_get_all_alerts()
        test16 = test_cleanup_old_alerts()
        test17 = test_update_config()
        test18 = test_get_config()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"IntrusionType Enum: {'PASS' if test1 else 'FAIL'}")
        print(f"IntrusionSeverity Enum: {'PASS' if test2 else 'FAIL'}")
        print(f"IntrusionStatus Enum: {'PASS' if test3 else 'FAIL'}")
        print(f"IntrusionAlert Dataclass: {'PASS' if test4 else 'FAIL'}")
        print(f"DetectionRule Dataclass: {'PASS' if test5 else 'FAIL'}")
        print(f"IntrusionDetectionConfig Dataclass: {'PASS' if test6 else 'FAIL'}")
        print(f"IntrusionDetectionResult Dataclass: {'PASS' if test7 else 'FAIL'}")
        print(f"IntrusionDetectionManager Initialization: {'PASS' if test8 else 'FAIL'}")
        print(f"Add Rule: {'PASS' if test9 else 'FAIL'}")
        print(f"Detect Intrusion: {'PASS' if test10 else 'FAIL'}")
        print(f"Update Alert Status: {'PASS' if test11 else 'FAIL'}")
        print(f"Get Alert: {'PASS' if test12 else 'FAIL'}")
        print(f"Get Alerts by Type: {'PASS' if test13 else 'FAIL'}")
        print(f"Get Alerts by Severity: {'PASS' if test14 else 'FAIL'}")
        print(f"Get All Alerts: {'PASS' if test15 else 'FAIL'}")
        print(f"Cleanup Old Alerts: {'PASS' if test16 else 'FAIL'}")
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
