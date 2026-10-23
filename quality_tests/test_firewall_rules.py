"""
Quality Test: Firewall Rules
Firewall rules system testleri for security module.
"""

import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from app.security.firewall_rules import (
    FirewallProtocol,
    FirewallDirection,
    FirewallAction,
    FirewallRule,
    FirewallConfig,
    FirewallResult,
    FirewallManager
)


def test_firewall_protocol_enum():
    """
    Test: FirewallProtocol enum.
    """
    print("=" * 70)
    print("TEST: FirewallProtocol Enum")
    print("=" * 70)
    
    assert FirewallProtocol.TCP.value == "tcp"
    assert FirewallProtocol.UDP.value == "udp"
    assert FirewallProtocol.ICMP.value == "icmp"
    assert FirewallProtocol.ANY.value == "any"
    
    print(f"  All enum values verified")
    print(f"  Total protocols: {len(FirewallProtocol)}")
    
    print("\n" + "=" * 70)
    print("PASS: FirewallProtocol enum")
    print("=" * 70)


def test_firewall_direction_enum():
    """
    Test: FirewallDirection enum.
    """
    print("=" * 70)
    print("TEST: FirewallDirection Enum")
    print("=" * 70)
    
    assert FirewallDirection.INBOUND.value == "inbound"
    assert FirewallDirection.OUTBOUND.value == "outbound"
    assert FirewallDirection.BOTH.value == "both"
    
    print(f"  All enum values verified")
    print(f"  Total directions: {len(FirewallDirection)}")
    
    print("\n" + "=" * 70)
    print("PASS: FirewallDirection enum")
    print("=" * 70)


def test_firewall_action_enum():
    """
    Test: FirewallAction enum.
    """
    print("=" * 70)
    print("TEST: FirewallAction Enum")
    print("=" * 70)
    
    assert FirewallAction.ALLOW.value == "allow"
    assert FirewallAction.DENY.value == "deny"
    assert FirewallAction.DROP.value == "drop"
    assert FirewallAction.REJECT.value == "reject"
    assert FirewallAction.LOG.value == "log"
    
    print(f"  All enum values verified")
    print(f"  Total actions: {len(FirewallAction)}")
    
    print("\n" + "=" * 70)
    print("PASS: FirewallAction enum")
    print("=" * 70)


def test_firewall_rule_dataclass():
    """
    Test: FirewallRule dataclass.
    """
    print("=" * 70)
    print("TEST: FirewallRule Dataclass")
    print("=" * 70)
    
    rule = FirewallRule(
        rule_id="rule_1",
        protocol=FirewallProtocol.TCP,
        direction=FirewallDirection.INBOUND,
        action=FirewallAction.ALLOW
    )
    
    assert rule.rule_id == "rule_1", "Rule ID eşleşmeli"
    assert rule.protocol == FirewallProtocol.TCP, "Protocol eşleşmeli"
    
    print(f"  Rule ID: {rule.rule_id}")
    
    print("\n" + "=" * 70)
    print("PASS: FirewallRule dataclass")
    print("=" * 70)


def test_firewall_config_dataclass():
    """
    Test: FirewallConfig dataclass.
    """
    print("=" * 70)
    print("TEST: FirewallConfig Dataclass")
    print("=" * 70)
    
    config = FirewallConfig(enable_logging=True)
    
    assert config.enable_logging == True, "Enable logging eşleşmeli"
    
    print(f"  Enable logging: {config.enable_logging}")
    
    print("\n" + "=" * 70)
    print("PASS: FirewallConfig dataclass")
    print("=" * 70)


def test_firewall_result_dataclass():
    """
    Test: FirewallResult dataclass.
    """
    print("=" * 70)
    print("TEST: FirewallResult Dataclass")
    print("=" * 70)
    
    result = FirewallResult(success=True)
    
    assert result.success == True, "Success eşleşmeli"
    assert isinstance(result.rules, list), "Rules list olmalı"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: FirewallResult dataclass")
    print("=" * 70)


def test_firewall_manager_initialization():
    """
    Test: FirewallManager initialization.
    """
    print("=" * 70)
    print("TEST: FirewallManager Initialization")
    print("=" * 70)
    
    config = FirewallConfig()
    manager = FirewallManager(config)
    
    assert manager.config == config, "Config eşleşmeli"
    
    print(f"  Manager initialized")
    
    print("\n" + "=" * 70)
    print("PASS: FirewallManager initialization")
    print("=" * 70)


def test_add_rule():
    """
    Test: Add rule.
    """
    print("=" * 70)
    print("TEST: Add Rule")
    print("=" * 70)
    
    manager = FirewallManager()
    
    result = manager.add_rule(
        protocol=FirewallProtocol.TCP,
        direction=FirewallDirection.INBOUND,
        action=FirewallAction.ALLOW
    )
    
    assert result.success == True, "Ekleme başarılı olmalı"
    
    print(f"  Rule added: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add rule")
    print("=" * 70)


def test_remove_rule():
    """
    Test: Remove rule.
    """
    print("=" * 70)
    print("TEST: Remove Rule")
    print("=" * 70)
    
    manager = FirewallManager()
    
    result = manager.add_rule(FirewallProtocol.TCP, FirewallDirection.INBOUND, FirewallAction.ALLOW)
    rule_id = result.rule.rule_id
    
    remove_result = manager.remove_rule(rule_id)
    
    assert remove_result.success == True, "Silme başarılı olmalı"
    
    print(f"  Rule removed: {remove_result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Remove rule")
    print("=" * 70)


def test_evaluate_packet():
    """
    Test: Evaluate packet.
    """
    print("=" * 70)
    print("TEST: Evaluate Packet")
    print("=" * 70)
    
    manager = FirewallManager()
    
    manager.add_rule(FirewallProtocol.TCP, FirewallDirection.INBOUND, FirewallAction.ALLOW, destination_port=80)
    
    result = manager.evaluate_packet(
        protocol=FirewallProtocol.TCP,
        direction=FirewallDirection.INBOUND,
        destination_port=80
    )
    
    assert result.action == FirewallAction.ALLOW, "Action ALLOW olmalı"
    
    print(f"  Action: {result.action.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Evaluate packet")
    print("=" * 70)


def test_get_rule():
    """
    Test: Get rule.
    """
    print("=" * 70)
    print("TEST: Get Rule")
    print("=" * 70)
    
    manager = FirewallManager()
    
    result = manager.add_rule(FirewallProtocol.TCP, FirewallDirection.INBOUND, FirewallAction.ALLOW)
    rule_id = result.rule.rule_id
    
    rule = manager.get_rule(rule_id)
    
    assert rule is not None, "Rule bulunmalı"
    
    print(f"  Rule found")
    
    print("\n" + "=" * 70)
    print("PASS: Get rule")
    print("=" * 70)


def test_get_rules_by_protocol():
    """
    Test: Get rules by protocol.
    """
    print("=" * 70)
    print("TEST: Get Rules by Protocol")
    print("=" * 70)
    
    manager = FirewallManager()
    
    manager.add_rule(FirewallProtocol.TCP, FirewallDirection.INBOUND, FirewallAction.ALLOW)
    manager.add_rule(FirewallProtocol.TCP, FirewallDirection.OUTBOUND, FirewallAction.ALLOW)
    manager.add_rule(FirewallProtocol.UDP, FirewallDirection.INBOUND, FirewallAction.ALLOW)
    
    rules = manager.get_rules_by_protocol(FirewallProtocol.TCP)
    
    assert len(rules) == 2, "2 TCP rule olmalı"
    
    print(f"  TCP rules: {len(rules)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get rules by protocol")
    print("=" * 70)


def test_get_rules_by_direction():
    """
    Test: Get rules by direction.
    """
    print("=" * 70)
    print("TEST: Get Rules by Direction")
    print("=" * 70)
    
    manager = FirewallManager()
    
    manager.add_rule(FirewallProtocol.TCP, FirewallDirection.INBOUND, FirewallAction.ALLOW)
    manager.add_rule(FirewallProtocol.TCP, FirewallDirection.INBOUND, FirewallAction.ALLOW)
    manager.add_rule(FirewallProtocol.UDP, FirewallDirection.OUTBOUND, FirewallAction.ALLOW)
    
    rules = manager.get_rules_by_direction(FirewallDirection.INBOUND)
    
    assert len(rules) == 2, "2 INBOUND rule olmalı"
    
    print(f"  INBOUND rules: {len(rules)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get rules by direction")
    print("=" * 70)


def test_get_all_rules():
    """
    Test: Get all rules.
    """
    print("=" * 70)
    print("TEST: Get All Rules")
    print("=" * 70)
    
    manager = FirewallManager()
    
    manager.add_rule(FirewallProtocol.TCP, FirewallDirection.INBOUND, FirewallAction.ALLOW)
    manager.add_rule(FirewallProtocol.UDP, FirewallDirection.INBOUND, FirewallAction.ALLOW)
    
    rules = manager.get_all_rules()
    
    assert len(rules) == 2, "2 rule olmalı"
    
    print(f"  Rules: {len(rules)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get all rules")
    print("=" * 70)


def test_enable_rule():
    """
    Test: Enable rule.
    """
    print("=" * 70)
    print("TEST: Enable Rule")
    print("=" * 70)
    
    manager = FirewallManager()
    
    result = manager.add_rule(FirewallProtocol.TCP, FirewallDirection.INBOUND, FirewallAction.ALLOW)
    rule_id = result.rule.rule_id
    
    enable_result = manager.enable_rule(rule_id)
    
    assert enable_result.success == True, "Enable başarılı olmalı"
    
    print(f"  Rule enabled: {enable_result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Enable rule")
    print("=" * 70)


def test_disable_rule():
    """
    Test: Disable rule.
    """
    print("=" * 70)
    print("TEST: Disable Rule")
    print("=" * 70)
    
    manager = FirewallManager()
    
    result = manager.add_rule(FirewallProtocol.TCP, FirewallDirection.INBOUND, FirewallAction.ALLOW)
    rule_id = result.rule.rule_id
    
    disable_result = manager.disable_rule(rule_id)
    
    assert disable_result.success == True, "Disable başarılı olmalı"
    
    print(f"  Rule disabled: {disable_result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Disable rule")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    manager = FirewallManager()
    
    new_config = FirewallConfig(default_action=FirewallAction.ALLOW)
    result = manager.update_config(new_config)
    
    assert result.success == True, "Update başarılı olmalı"
    assert manager.config.default_action == FirewallAction.ALLOW, "Config güncellenmeli"
    
    print(f"  Default action: {manager.config.default_action.value}")
    
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
    
    config = FirewallConfig(default_action=FirewallAction.ALLOW)
    manager = FirewallManager(config)
    
    retrieved_config = manager.get_config()
    
    assert retrieved_config.default_action == FirewallAction.ALLOW, "Config eşleşmeli"
    
    print(f"  Default action: {retrieved_config.default_action.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_firewall_protocol_enum()
        test2 = test_firewall_direction_enum()
        test3 = test_firewall_action_enum()
        test4 = test_firewall_rule_dataclass()
        test5 = test_firewall_config_dataclass()
        test6 = test_firewall_result_dataclass()
        test7 = test_firewall_manager_initialization()
        test8 = test_add_rule()
        test9 = test_remove_rule()
        test10 = test_evaluate_packet()
        test11 = test_get_rule()
        test12 = test_get_rules_by_protocol()
        test13 = test_get_rules_by_direction()
        test14 = test_get_all_rules()
        test15 = test_enable_rule()
        test16 = test_disable_rule()
        test17 = test_update_config()
        test18 = test_get_config()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"FirewallProtocol Enum: {'PASS' if test1 else 'FAIL'}")
        print(f"FirewallDirection Enum: {'PASS' if test2 else 'FAIL'}")
        print(f"FirewallAction Enum: {'PASS' if test3 else 'FAIL'}")
        print(f"FirewallRule Dataclass: {'PASS' if test4 else 'FAIL'}")
        print(f"FirewallConfig Dataclass: {'PASS' if test5 else 'FAIL'}")
        print(f"FirewallResult Dataclass: {'PASS' if test6 else 'FAIL'}")
        print(f"FirewallManager Initialization: {'PASS' if test7 else 'FAIL'}")
        print(f"Add Rule: {'PASS' if test8 else 'FAIL'}")
        print(f"Remove Rule: {'PASS' if test9 else 'FAIL'}")
        print(f"Evaluate Packet: {'PASS' if test10 else 'FAIL'}")
        print(f"Get Rule: {'PASS' if test11 else 'FAIL'}")
        print(f"Get Rules by Protocol: {'PASS' if test12 else 'FAIL'}")
        print(f"Get Rules by Direction: {'PASS' if test13 else 'FAIL'}")
        print(f"Get All Rules: {'PASS' if test14 else 'FAIL'}")
        print(f"Enable Rule: {'PASS' if test15 else 'FAIL'}")
        print(f"Disable Rule: {'PASS' if test16 else 'FAIL'}")
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
