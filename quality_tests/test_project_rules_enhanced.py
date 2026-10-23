"""
Quality Test: Enhanced Project Rules
Project rules gelişmiş özellikleri testleri.
"""

import sys
import os
import tempfile
import shutil
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.ai.project_rules import (
    ProjectRules,
    Rule,
    RulePriority,
    RuleSeverity
)


def test_severity_levels():
    """
    Test: Rule severity levels.
    """
    print("=" * 70)
    print("TEST: Rule Severity Levels")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp(prefix="muhammedai_test_")
    
    try:
        # Rules dizini oluştur
        rules_dir = Path(temp_dir) / ".muhammedai" / "rules"
        rules_dir.mkdir(parents=True, exist_ok=True)
        
        # Security rule dosyası oluştur
        security_file = rules_dir / "security.md"
        security_file.write_text("- Never use eval() in production code\n- Must validate all user input", encoding='utf-8')
        
        # Coding rule dosyası oluştur
        coding_file = rules_dir / "coding.md"
        coding_file.write_text("- Recommend using type hints\n- Should add docstrings", encoding='utf-8')
        
        # Project rules oluştur
        rules = ProjectRules(project_root=Path(temp_dir))
        
        # Severity kontrolü
        security_rules = [r for r in rules.rules.values() if "security" in r.file_path]
        assert len(security_rules) > 0, "Security rules olmalı"
        
        for rule in security_rules:
            assert rule.severity == RuleSeverity.ERROR, "Security rules ERROR severity olmalı"
            print(f"  Security rule: {rule.content} - Severity: {rule.severity.value}")
        
        coding_rules = [r for r in rules.rules.values() if "coding" in r.file_path]
        for rule in coding_rules:
            assert rule.severity in [RuleSeverity.WARNING, RuleSeverity.SUGGESTION], "Coding rules WARNING veya SUGGESTION olmalı"
            print(f"  Coding rule: {rule.content} - Severity: {rule.severity.value}")
        
        print("\n" + "=" * 70)
        print("PASS: Rule severity levels")
        print("=" * 70)
        
    finally:
        shutil.rmtree(temp_dir)


def test_rule_validation():
    """
    Test: Rule validation.
    """
    print("=" * 70)
    print("TEST: Rule Validation")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp(prefix="muhammedai_test_")
    
    try:
        # Project rules oluştur
        rules = ProjectRules(project_root=Path(temp_dir))
        
        # Geçerli rule
        valid_rule = Rule(
            content="Use type hints",
            file_path="coding.md",
            priority=RulePriority.PROJECT_ARCHITECTURE,
            pattern=r"def\s+\w+\([^)]*\):"
        )
        
        validation = rules.validate_rule(valid_rule)
        assert validation["valid"], "Rule geçerli olmalı"
        print(f"  Valid rule validation: {validation}")
        
        # Geçersiz rule (boş content)
        invalid_rule = Rule(
            content="",
            file_path="coding.md",
            priority=RulePriority.PROJECT_ARCHITECTURE
        )
        
        validation = rules.validate_rule(invalid_rule)
        assert not validation["valid"], "Boş content geçersiz olmalı"
        assert len(validation["errors"]) > 0, "Error olmalı"
        print(f"  Invalid rule validation: {validation}")
        
        # Geçersiz regex
        invalid_regex_rule = Rule(
            content="Test rule",
            file_path="coding.md",
            priority=RulePriority.PROJECT_ARCHITECTURE,
            pattern="[invalid(regex"
        )
        
        validation = rules.validate_rule(invalid_regex_rule)
        assert not validation["valid"], "Geçersiz regex olmalı"
        print(f"  Invalid regex validation: {validation}")
        
        print("\n" + "=" * 70)
        print("PASS: Rule validation")
        print("=" * 70)
        
    finally:
        shutil.rmtree(temp_dir)


def test_conflict_detection():
    """
    Test: Rule conflict detection.
    """
    print("=" * 70)
    print("TEST: Conflict Detection")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp(prefix="muhammedai_test_")
    
    try:
        # Project rules oluştur
        rules = ProjectRules(project_root=Path(temp_dir))
        
        # İki conflict rule ekle
        rule1 = Rule(
            content="Never use eval()",
            file_path="security.md",
            priority=RulePriority.PROJECT_SECURITY,
            severity=RuleSeverity.ERROR,
            tags={"security"}
        )
        
        rule2 = Rule(
            content="Consider eval() for dynamic code",
            file_path="coding.md",
            priority=RulePriority.PROJECT_ARCHITECTURE,
            severity=RuleSeverity.SUGGESTION,
            tags={"security"}
        )
        
        rules.rules["rule1"] = rule1
        rules.rules["rule2"] = rule2
        
        # Conflict detection
        conflicts = rules.detect_conflicts()
        
        assert len(conflicts) > 0, "Conflict tespit edilmeli"
        print(f"  Conflicts: {len(conflicts)}")
        for conflict in conflicts:
            print(f"    {conflict['reason']}")
        
        print("\n" + "=" * 70)
        print("PASS: Conflict detection")
        print("=" * 70)
        
    finally:
        shutil.rmtree(temp_dir)


def test_rule_enforcement():
    """
    Test: Rule enforcement.
    """
    print("=" * 70)
    print("TEST: Rule Enforcement")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp(prefix="muhammedai_test_")
    
    try:
        # Project rules oluştur
        rules = ProjectRules(project_root=Path(temp_dir))
        
        # Pattern içeren rule ekle
        rule = Rule(
            content="Avoid using eval()",
            file_path="security.md",
            priority=RulePriority.PROJECT_SECURITY,
            severity=RuleSeverity.ERROR,
            pattern=r"eval\s*\("
        )
        
        rules.rules["rule1"] = rule
        
        # Violation içeren content
        content_with_violation = "x = eval(user_input)"
        violations = rules.enforce_rules(content_with_violation, "test.py")
        
        assert len(violations) > 0, "Violation tespit edilmeli"
        assert violations[0]["severity"] == "error", "ERROR severity olmalı"
        print(f"  Violations: {len(violations)}")
        print(f"  Violation message: {violations[0]['message']}")
        
        # Violation içermeyen content
        content_without_violation = "x = int(user_input)"
        violations = rules.enforce_rules(content_without_violation, "test.py")
        
        assert len(violations) == 0, "Violation olmamalı"
        print(f"  No violations: {len(violations)}")
        
        print("\n" + "=" * 70)
        print("PASS: Rule enforcement")
        print("=" * 70)
        
    finally:
        shutil.rmtree(temp_dir)


def test_rule_analytics():
    """
    Test: Rule analytics.
    """
    print("=" * 70)
    print("TEST: Rule Analytics")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp(prefix="muhammedai_test_")
    
    try:
        # Project rules oluştur
        rules = ProjectRules(project_root=Path(temp_dir))
        
        # Çeşitli rules ekle
        rules.rules["rule1"] = Rule(
            content="Rule 1",
            file_path="security.md",
            priority=RulePriority.PROJECT_SECURITY,
            severity=RuleSeverity.ERROR,
            tags={"security"},
            enabled=True,
            violation_count=5
        )
        
        rules.rules["rule2"] = Rule(
            content="Rule 2",
            file_path="coding.md",
            priority=RulePriority.PROJECT_ARCHITECTURE,
            severity=RuleSeverity.WARNING,
            tags={"coding"},
            enabled=True,
            violation_count=2
        )
        
        rules.rules["rule3"] = Rule(
            content="Rule 3",
            file_path="testing.md",
            priority=RulePriority.DIRECTORY,
            severity=RuleSeverity.INFO,
            tags={"testing"},
            enabled=False,
            violation_count=0
        )
        
        # Analytics al
        analytics = rules.get_analytics()
        
        assert analytics["total_rules"] == 3, "3 rule olmalı"
        assert analytics["enabled_rules"] == 2, "2 enabled rule olmalı"
        assert analytics["disabled_rules"] == 1, "1 disabled rule olmalı"
        assert analytics["total_violations"] == 7, "7 violation olmalı"
        assert "error" in analytics["severity_counts"], "ERROR severity olmalı"
        assert "security" in analytics["tag_counts"], "security tag olmalı"
        
        print(f"  Total rules: {analytics['total_rules']}")
        print(f"  Enabled rules: {analytics['enabled_rules']}")
        print(f"  Disabled rules: {analytics['disabled_rules']}")
        print(f"  Severity counts: {analytics['severity_counts']}")
        print(f"  Tag counts: {analytics['tag_counts']}")
        print(f"  Total violations: {analytics['total_violations']}")
        
        print("\n" + "=" * 70)
        print("PASS: Rule analytics")
        print("=" * 70)
        
    finally:
        shutil.rmtree(temp_dir)


def test_enable_disable_rules():
    """
    Test: Enable/disable rules.
    """
    print("=" * 70)
    print("TEST: Enable/Disable Rules")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp(prefix="muhammedai_test_")
    
    try:
        # Project rules oluştur
        rules = ProjectRules(project_root=Path(temp_dir))
        
        # Rule ekle
        rules.rules["rule1"] = Rule(
            content="Test rule",
            file_path="coding.md",
            priority=RulePriority.PROJECT_ARCHITECTURE,
            enabled=True
        )
        
        # Disable
        result = rules.disable_rule("rule1")
        assert result == True, "Disable başarılı olmalı"
        assert not rules.rules["rule1"].enabled, "Rule disabled olmalı"
        print(f"  Disabled: {not rules.rules['rule1'].enabled}")
        
        # Enable
        result = rules.enable_rule("rule1")
        assert result == True, "Enable başarılı olmalı"
        assert rules.rules["rule1"].enabled, "Rule enabled olmalı"
        print(f"  Enabled: {rules.rules['rule1'].enabled}")
        
        # Non-existent rule
        result = rules.disable_rule("nonexistent")
        assert result == False, "Non-existent rule başarısız olmalı"
        print(f"  Non-existent rule: {result}")
        
        print("\n" + "=" * 70)
        print("PASS: Enable/disable rules")
        print("=" * 70)
        
    finally:
        shutil.rmtree(temp_dir)


def test_pattern_extraction():
    """
    Test: Pattern extraction from rule content.
    """
    print("=" * 70)
    print("TEST: Pattern Extraction")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp(prefix="muhammedai_test_")
    
    try:
        # Rules dizini oluştur
        rules_dir = Path(temp_dir) / ".muhammedai" / "rules"
        rules_dir.mkdir(parents=True, exist_ok=True)
        
        # Pattern içeren rule dosyası oluştur
        pattern_file = rules_dir / "patterns.md"
        pattern_file.write_text("- Avoid /eval\\s*\\(/ patterns", encoding='utf-8')
        
        # Project rules oluştur
        rules = ProjectRules(project_root=Path(temp_dir))
        
        # Pattern kontrolü
        pattern_rules = [r for r in rules.rules.values() if r.pattern]
        assert len(pattern_rules) > 0, "Pattern içeren rule olmalı"
        
        for rule in pattern_rules:
            print(f"  Rule: {rule.content}")
            print(f"  Pattern: {rule.pattern}")
            assert rule.pattern is not None, "Pattern olmalı"
        
        print("\n" + "=" * 70)
        print("PASS: Pattern extraction")
        print("=" * 70)
        
    finally:
        shutil.rmtree(temp_dir)


if __name__ == "__main__":
    try:
        test1 = test_severity_levels()
        test2 = test_rule_validation()
        test3 = test_conflict_detection()
        test4 = test_rule_enforcement()
        test5 = test_rule_analytics()
        test6 = test_enable_disable_rules()
        test7 = test_pattern_extraction()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Severity Levels: {'PASS' if test1 else 'FAIL'}")
        print(f"Rule Validation: {'PASS' if test2 else 'FAIL'}")
        print(f"Conflict Detection: {'PASS' if test3 else 'FAIL'}")
        print(f"Rule Enforcement: {'PASS' if test4 else 'FAIL'}")
        print(f"Rule Analytics: {'PASS' if test5 else 'FAIL'}")
        print(f"Enable/Disable Rules: {'PASS' if test6 else 'FAIL'}")
        print(f"Pattern Extraction: {'PASS' if test7 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7])
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
