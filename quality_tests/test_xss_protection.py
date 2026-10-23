"""
Quality Test: XSS Protection
XSS protection system testleri for security module.
"""

import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from app.security.xss_protection import (
    XSSAttackType,
    XSSSeverity,
    XSSContext,
    XSSPattern,
    XSSDetectionResult,
    XSSProtectionConfig,
    XSSSanitizationResult,
    XSSProtection
)


def test_xss_attack_type_enum():
    """
    Test: XSSAttackType enum.
    """
    print("=" * 70)
    print("TEST: XSSAttackType Enum")
    print("=" * 70)
    
    assert XSSAttackType.REFLECTED.value == "reflected"
    assert XSSAttackType.STORED.value == "stored"
    assert XSSAttackType.DOM_BASED.value == "dom_based"
    assert XSSAttackType.SELF.value == "self"
    assert XSSAttackType.CUSTOM.value == "custom"
    
    print(f"  All enum values verified")
    print(f"  Total types: {len(XSSAttackType)}")
    
    print("\n" + "=" * 70)
    print("PASS: XSSAttackType enum")
    print("=" * 70)


def test_xss_severity_enum():
    """
    Test: XSSSeverity enum.
    """
    print("=" * 70)
    print("TEST: XSSSeverity Enum")
    print("=" * 70)
    
    assert XSSSeverity.LOW.value == "low"
    assert XSSSeverity.MEDIUM.value == "medium"
    assert XSSSeverity.HIGH.value == "high"
    assert XSSSeverity.CRITICAL.value == "critical"
    
    print(f"  All enum values verified")
    print(f"  Total severities: {len(XSSSeverity)}")
    
    print("\n" + "=" * 70)
    print("PASS: XSSSeverity enum")
    print("=" * 70)


def test_xss_context_enum():
    """
    Test: XSSContext enum.
    """
    print("=" * 70)
    print("TEST: XSSContext Enum")
    print("=" * 70)
    
    assert XSSContext.HTML.value == "html"
    assert XSSContext.JAVASCRIPT.value == "javascript"
    assert XSSContext.CSS.value == "css"
    assert XSSContext.URL.value == "url"
    assert XSSContext.ATTRIBUTE.value == "attribute"
    assert XSSContext.CUSTOM.value == "custom"
    
    print(f"  All enum values verified")
    print(f"  Total contexts: {len(XSSContext)}")
    
    print("\n" + "=" * 70)
    print("PASS: XSSContext enum")
    print("=" * 70)


def test_xss_pattern_dataclass():
    """
    Test: XSSPattern dataclass.
    """
    print("=" * 70)
    print("TEST: XSSPattern Dataclass")
    print("=" * 70)
    
    pattern = XSSPattern(
        pattern_id="pattern_1",
        name="Test Pattern",
        pattern=r'<script>',
        description="Test description",
        severity=XSSSeverity.HIGH
    )
    
    assert pattern.pattern_id == "pattern_1", "Pattern ID eşleşmeli"
    assert pattern.name == "Test Pattern", "Name eşleşmeli"
    assert pattern.severity == XSSSeverity.HIGH, "Severity eşleşmeli"
    
    print(f"  Pattern ID: {pattern.pattern_id}")
    print(f"  Name: {pattern.name}")
    
    print("\n" + "=" * 70)
    print("PASS: XSSPattern dataclass")
    print("=" * 70)


def test_xss_detection_result_dataclass():
    """
    Test: XSSDetectionResult dataclass.
    """
    print("=" * 70)
    print("TEST: XSSDetectionResult Dataclass")
    print("=" * 70)
    
    result = XSSDetectionResult(is_detected=True)
    result.message = "Test message"
    
    assert result.is_detected == True, "Is detected eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Is detected: {result.is_detected}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: XSSDetectionResult dataclass")
    print("=" * 70)


def test_xss_protection_config_dataclass():
    """
    Test: XSSProtectionConfig dataclass.
    """
    print("=" * 70)
    print("TEST: XSSProtectionConfig Dataclass")
    print("=" * 70)
    
    config = XSSProtectionConfig(strict_mode=True)
    
    assert config.strict_mode == True, "Strict mode eşleşmeli"
    
    print(f"  Strict mode: {config.strict_mode}")
    
    print("\n" + "=" * 70)
    print("PASS: XSSProtectionConfig dataclass")
    print("=" * 70)


def test_xss_sanitization_result_dataclass():
    """
    Test: XSSSanitizationResult dataclass.
    """
    print("=" * 70)
    print("TEST: XSSSanitizationResult Dataclass")
    print("=" * 70)
    
    result = XSSSanitizationResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.detections, list), "Detections list olmalı"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: XSSSanitizationResult dataclass")
    print("=" * 70)


def test_xss_protection_initialization():
    """
    Test: XSSProtection initialization.
    """
    print("=" * 70)
    print("TEST: XSSProtection Initialization")
    print("=" * 70)
    
    config = XSSProtectionConfig()
    protection = XSSProtection(config)
    
    assert protection.config == config, "Config eşleşmeli"
    assert len(protection.patterns) > 0, "Default patterns olmalı"
    
    print(f"  Patterns: {len(protection.patterns)}")
    
    print("\n" + "=" * 70)
    print("PASS: XSSProtection initialization")
    print("=" * 70)


def test_add_pattern():
    """
    Test: Add pattern.
    """
    print("=" * 70)
    print("TEST: Add Pattern")
    print("=" * 70)
    
    config = XSSProtectionConfig(enable_custom_patterns=True)
    protection = XSSProtection(config)
    
    result = protection.add_pattern(
        name="Test Pattern",
        pattern=r'test_pattern',
        description="Test description",
        severity=XSSSeverity.MEDIUM
    )
    
    assert result.pattern_id is not None, "Pattern ID olmalı"
    
    print(f"  Pattern added: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add pattern")
    print("=" * 70)


def test_remove_pattern():
    """
    Test: Remove pattern.
    """
    print("=" * 70)
    print("TEST: Remove Pattern")
    print("=" * 70)
    
    config = XSSProtectionConfig(enable_custom_patterns=True)
    protection = XSSProtection(config)
    
    result = protection.add_pattern("Test", r'test', "Test", XSSSeverity.MEDIUM)
    pattern_id = result.pattern_id
    
    result = protection.remove_pattern(pattern_id)
    
    assert result.message is not None, "Remove başarılı olmalı"
    
    print(f"  Pattern removed: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Remove pattern")
    print("=" * 70)


def test_detect_xss():
    """
    Test: Detect XSS.
    """
    print("=" * 70)
    print("TEST: Detect XSS")
    print("=" * 70)
    
    protection = XSSProtection()
    
    malicious = "<script>alert('XSS')</script>"
    detection = protection.detect_xss(malicious)
    
    assert detection.is_detected == True, "XSS tespit edilmeli"
    
    print(f"  XSS detected: {detection.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Detect XSS")
    print("=" * 70)


def test_sanitize():
    """
    Test: Sanitize.
    """
    print("=" * 70)
    print("TEST: Sanitize")
    print("=" * 70)
    
    protection = XSSProtection()
    
    malicious = "<script>alert('XSS')</script>"
    result = protection.sanitize(malicious)
    
    assert result.success == True, "Sanitization başarılı olmalı"
    assert result.sanitized_content != malicious, "Content değişmeli"
    
    print(f"  Sanitized: {result.sanitized_content}")
    
    print("\n" + "=" * 70)
    print("PASS: Sanitize")
    print("=" * 70)


def test_encode():
    """
    Test: Encode.
    """
    print("=" * 70)
    print("TEST: Encode")
    print("=" * 70)
    
    protection = XSSProtection()
    
    content = "<script>alert('test')</script>"
    result = protection.encode(content, XSSContext.HTML)
    
    assert result.success == True, "Encoding başarılı olmalı"
    assert "&lt;" in result.sanitized_content, "Encoded olmalı"
    
    print(f"  Encoded: {result.sanitized_content}")
    
    print("\n" + "=" * 70)
    print("PASS: Encode")
    print("=" * 70)


def test_get_pattern():
    """
    Test: Get pattern.
    """
    print("=" * 70)
    print("TEST: Get Pattern")
    print("=" * 70)
    
    protection = XSSProtection()
    
    patterns = protection.get_all_patterns()
    if patterns:
        pattern_id = patterns[0].pattern_id
        pattern = protection.get_pattern(pattern_id)
        
        assert pattern is not None, "Pattern bulunmalı"
    
    print(f"  Pattern found")
    
    print("\n" + "=" * 70)
    print("PASS: Get pattern")
    print("=" * 70)


def test_get_all_patterns():
    """
    Test: Get all patterns.
    """
    print("=" * 70)
    print("TEST: Get All Patterns")
    print("=" * 70)
    
    protection = XSSProtection()
    
    patterns = protection.get_all_patterns()
    
    assert len(patterns) > 0, "Pattern olmalı"
    
    print(f"  Total patterns: {len(patterns)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get all patterns")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    protection = XSSProtection()
    
    new_config = XSSProtectionConfig(strict_mode=True)
    result = protection.update_config(new_config)
    
    assert result.success == True, "Update başarılı olmalı"
    assert protection.config.strict_mode == True, "Config güncellenmeli"
    
    print(f"  Strict mode: {protection.config.strict_mode}")
    
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
    
    config = XSSProtectionConfig(strict_mode=True)
    protection = XSSProtection(config)
    
    retrieved_config = protection.get_config()
    
    assert retrieved_config.strict_mode == True, "Config eşleşmeli"
    
    print(f"  Strict mode: {retrieved_config.strict_mode}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_xss_attack_type_enum()
        test2 = test_xss_severity_enum()
        test3 = test_xss_context_enum()
        test4 = test_xss_pattern_dataclass()
        test5 = test_xss_detection_result_dataclass()
        test6 = test_xss_protection_config_dataclass()
        test7 = test_xss_sanitization_result_dataclass()
        test8 = test_xss_protection_initialization()
        test9 = test_add_pattern()
        test10 = test_remove_pattern()
        test11 = test_detect_xss()
        test12 = test_sanitize()
        test13 = test_encode()
        test14 = test_get_pattern()
        test15 = test_get_all_patterns()
        test16 = test_update_config()
        test17 = test_get_config()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"XSSAttackType Enum: {'PASS' if test1 else 'FAIL'}")
        print(f"XSSSeverity Enum: {'PASS' if test2 else 'FAIL'}")
        print(f"XSSContext Enum: {'PASS' if test3 else 'FAIL'}")
        print(f"XSSPattern Dataclass: {'PASS' if test4 else 'FAIL'}")
        print(f"XSSDetectionResult Dataclass: {'PASS' if test5 else 'FAIL'}")
        print(f"XSSProtectionConfig Dataclass: {'PASS' if test6 else 'FAIL'}")
        print(f"XSSSanitizationResult Dataclass: {'PASS' if test7 else 'FAIL'}")
        print(f"XSSProtection Initialization: {'PASS' if test8 else 'FAIL'}")
        print(f"Add Pattern: {'PASS' if test9 else 'FAIL'}")
        print(f"Remove Pattern: {'PASS' if test10 else 'FAIL'}")
        print(f"Detect XSS: {'PASS' if test11 else 'FAIL'}")
        print(f"Sanitize: {'PASS' if test12 else 'FAIL'}")
        print(f"Encode: {'PASS' if test13 else 'FAIL'}")
        print(f"Get Pattern: {'PASS' if test14 else 'FAIL'}")
        print(f"Get All Patterns: {'PASS' if test15 else 'FAIL'}")
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
