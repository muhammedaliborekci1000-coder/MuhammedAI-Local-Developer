"""
Quality Test: Content Security Policy
Content security policy system testleri for security module.
"""

import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from app.security.content_security_policy import (
    CSPDirective,
    CSPSource,
    CSPRule,
    CSPConfig,
    CSPResult,
    CSPManager
)


def test_csp_directive_enum():
    """
    Test: CSPDirective enum.
    """
    print("=" * 70)
    print("TEST: CSPDirective Enum")
    print("=" * 70)
    
    assert CSPDirective.DEFAULT_SRC.value == "default-src"
    assert CSPDirective.SCRIPT_SRC.value == "script-src"
    assert CSPDirective.STYLE_SRC.value == "style-src"
    assert CSPDirective.IMG_SRC.value == "img-src"
    assert CSPDirective.CONNECT_SRC.value == "connect-src"
    
    print(f"  All enum values verified")
    print(f"  Total directives: {len(CSPDirective)}")
    
    print("\n" + "=" * 70)
    print("PASS: CSPDirective enum")
    print("=" * 70)


def test_csp_source_enum():
    """
    Test: CSPSource enum.
    """
    print("=" * 70)
    print("TEST: CSPSource Enum")
    print("=" * 70)
    
    assert CSPSource.SELF.value == "'self'"
    assert CSPSource.NONE.value == "'none'"
    assert CSPSource.UNSAFE_INLINE.value == "'unsafe-inline'"
    assert CSPSource.UNSAFE_EVAL.value == "'unsafe-eval'"
    assert CSPSource.HTTPS.value == "https:"
    
    print(f"  All enum values verified")
    print(f"  Total sources: {len(CSPSource)}")
    
    print("\n" + "=" * 70)
    print("PASS: CSPSource enum")
    print("=" * 70)


def test_csp_rule_dataclass():
    """
    Test: CSPRule dataclass.
    """
    print("=" * 70)
    print("TEST: CSPRule Dataclass")
    print("=" * 70)
    
    rule = CSPRule(
        rule_id="rule_1",
        directive=CSPDirective.SCRIPT_SRC,
        sources=["'self'"]
    )
    
    assert rule.rule_id == "rule_1", "Rule ID eşleşmeli"
    assert rule.directive == CSPDirective.SCRIPT_SRC, "Directive eşleşmeli"
    assert rule.sources == ["'self'"], "Sources eşleşmeli"
    
    print(f"  Rule ID: {rule.rule_id}")
    print(f"  Directive: {rule.directive.value}")
    
    print("\n" + "=" * 70)
    print("PASS: CSPRule dataclass")
    print("=" * 70)


def test_csp_config_dataclass():
    """
    Test: CSPConfig dataclass.
    """
    print("=" * 70)
    print("TEST: CSPConfig Dataclass")
    print("=" * 70)
    
    config = CSPConfig(strict_mode=True)
    
    assert config.strict_mode == True, "Strict mode eşleşmeli"
    
    print(f"  Strict mode: {config.strict_mode}")
    
    print("\n" + "=" * 70)
    print("PASS: CSPConfig dataclass")
    print("=" * 70)


def test_csp_result_dataclass():
    """
    Test: CSPResult dataclass.
    """
    print("=" * 70)
    print("TEST: CSPResult Dataclass")
    print("=" * 70)
    
    result = CSPResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.rules, list), "Rules list olmalı"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: CSPResult dataclass")
    print("=" * 70)


def test_csp_manager_initialization():
    """
    Test: CSPManager initialization.
    """
    print("=" * 70)
    print("TEST: CSPManager Initialization")
    print("=" * 70)
    
    config = CSPConfig()
    manager = CSPManager(config)
    
    assert manager.config == config, "Config eşleşmeli"
    assert len(manager.rules) > 0, "Default rules olmalı"
    
    print(f"  Rules: {len(manager.rules)}")
    
    print("\n" + "=" * 70)
    print("PASS: CSPManager initialization")
    print("=" * 70)


def test_add_rule():
    """
    Test: Add rule.
    """
    print("=" * 70)
    print("TEST: Add Rule")
    print("=" * 70)
    
    manager = CSPManager()
    
    result = manager.add_rule(
        directive=CSPDirective.FONT_SRC,
        sources=["'self'", "https://fonts.googleapis.com"]
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
    
    manager = CSPManager()
    
    result = manager.add_rule(CSPDirective.FONT_SRC, ["'self'"])
    rule_id = result.rule.rule_id
    
    result = manager.remove_rule(rule_id)
    
    assert result.success == True, "Silme başarılı olmalı"
    
    print(f"  Rule removed: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Remove rule")
    print("=" * 70)


def test_update_rule():
    """
    Test: Update rule.
    """
    print("=" * 70)
    print("TEST: Update Rule")
    print("=" * 70)
    
    manager = CSPManager()
    
    result = manager.add_rule(CSPDirective.FONT_SRC, ["'self'"])
    rule_id = result.rule.rule_id
    
    result = manager.update_rule(rule_id, sources=["'self'", "https://example.com"])
    
    assert result.success == True, "Update başarılı olmalı"
    
    print(f"  Rule updated: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Update rule")
    print("=" * 70)


def test_get_rule():
    """
    Test: Get rule.
    """
    print("=" * 70)
    print("TEST: Get Rule")
    print("=" * 70)
    
    manager = CSPManager()
    
    result = manager.add_rule(CSPDirective.FONT_SRC, ["'self'"])
    rule_id = result.rule.rule_id
    
    rule = manager.get_rule(rule_id)
    
    assert rule is not None, "Rule bulunmalı"
    assert rule.rule_id == rule_id, "Rule ID eşleşmeli"
    
    print(f"  Rule: {rule.rule_id}")
    
    print("\n" + "=" * 70)
    print("PASS: Get rule")
    print("=" * 70)


def test_get_rule_by_directive():
    """
    Test: Get rule by directive.
    """
    print("=" * 70)
    print("TEST: Get Rule by Directive")
    print("=" * 70)
    
    manager = CSPManager()
    
    rule = manager.get_rule_by_directive(CSPDirective.SCRIPT_SRC)
    
    assert rule is not None, "Rule bulunmalı"
    
    print(f"  Rule: {rule.directive.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Get rule by directive")
    print("=" * 70)


def test_get_all_rules():
    """
    Test: Get all rules.
    """
    print("=" * 70)
    print("TEST: Get All Rules")
    print("=" * 70)
    
    manager = CSPManager()
    
    rules = manager.get_all_rules()
    
    assert len(rules) > 0, "Rule olmalı"
    
    print(f"  Total rules: {len(rules)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get all rules")
    print("=" * 70)


def test_generate_policy():
    """
    Test: Generate policy.
    """
    print("=" * 70)
    print("TEST: Generate Policy")
    print("=" * 70)
    
    manager = CSPManager()
    
    result = manager.generate_policy()
    
    assert result.success == True, "Generation başarılı olmalı"
    assert result.policy is not None, "Policy olmalı"
    
    print(f"  Policy: {result.policy}")
    
    print("\n" + "=" * 70)
    print("PASS: Generate policy")
    print("=" * 70)


def test_generate_header():
    """
    Test: Generate header.
    """
    print("=" * 70)
    print("TEST: Generate Header")
    print("=" * 70)
    
    manager = CSPManager()
    
    result = manager.generate_header()
    
    assert result.success == True, "Generation başarılı olmalı"
    
    print(f"  Header: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Generate header")
    print("=" * 70)


def test_enable_strict_mode():
    """
    Test: Enable strict mode.
    """
    print("=" * 70)
    print("TEST: Enable Strict Mode")
    print("=" * 70)
    
    manager = CSPManager()
    
    result = manager.enable_strict_mode()
    
    assert result.success == True, "Enable başarılı olmalı"
    assert manager.config.strict_mode == True, "Strict mode enabled olmalı"
    
    print(f"  Strict mode: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Enable strict mode")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    manager = CSPManager()
    
    new_config = CSPConfig(strict_mode=True)
    result = manager.update_config(new_config)
    
    assert result.success == True, "Update başarılı olmalı"
    assert manager.config.strict_mode == True, "Config güncellenmeli"
    
    print(f"  Strict mode: {manager.config.strict_mode}")
    
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
    
    config = CSPConfig(strict_mode=True)
    manager = CSPManager(config)
    
    retrieved_config = manager.get_config()
    
    assert retrieved_config.strict_mode == True, "Config eşleşmeli"
    
    print(f"  Strict mode: {retrieved_config.strict_mode}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_csp_directive_enum()
        test2 = test_csp_source_enum()
        test3 = test_csp_rule_dataclass()
        test4 = test_csp_config_dataclass()
        test5 = test_csp_result_dataclass()
        test6 = test_csp_manager_initialization()
        test7 = test_add_rule()
        test8 = test_remove_rule()
        test9 = test_update_rule()
        test10 = test_get_rule()
        test11 = test_get_rule_by_directive()
        test12 = test_get_all_rules()
        test13 = test_generate_policy()
        test14 = test_generate_header()
        test15 = test_enable_strict_mode()
        test16 = test_update_config()
        test17 = test_get_config()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"CSPDirective Enum: {'PASS' if test1 else 'FAIL'}")
        print(f"CSPSource Enum: {'PASS' if test2 else 'FAIL'}")
        print(f"CSPRule Dataclass: {'PASS' if test3 else 'FAIL'}")
        print(f"CSPConfig Dataclass: {'PASS' if test4 else 'FAIL'}")
        print(f"CSPResult Dataclass: {'PASS' if test5 else 'FAIL'}")
        print(f"CSPManager Initialization: {'PASS' if test6 else 'FAIL'}")
        print(f"Add Rule: {'PASS' if test7 else 'FAIL'}")
        print(f"Remove Rule: {'PASS' if test8 else 'FAIL'}")
        print(f"Update Rule: {'PASS' if test9 else 'FAIL'}")
        print(f"Get Rule: {'PASS' if test10 else 'FAIL'}")
        print(f"Get Rule by Directive: {'PASS' if test11 else 'FAIL'}")
        print(f"Get All Rules: {'PASS' if test12 else 'FAIL'}")
        print(f"Generate Policy: {'PASS' if test13 else 'FAIL'}")
        print(f"Generate Header: {'PASS' if test14 else 'FAIL'}")
        print(f"Enable Strict Mode: {'PASS' if test15 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test16 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test17 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14, test15, test16, test17])
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
