"""
Quality Test: Rate Limiting
Rate limiting system testleri for security module.
"""

import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from app.security.rate_limiting import (
    RateLimitAlgorithm,
    RateLimitScope,
    RateLimitRule,
    RateLimitBucket,
    RateLimitConfig,
    RateLimitResult,
    RateLimiter
)


def test_rate_limit_algorithm_enum():
    """
    Test: RateLimitAlgorithm enum.
    """
    print("=" * 70)
    print("TEST: RateLimitAlgorithm Enum")
    print("=" * 70)
    
    assert RateLimitAlgorithm.TOKEN_BUCKET.value == "token_bucket"
    assert RateLimitAlgorithm.LEAKY_BUCKET.value == "leaky_bucket"
    assert RateLimitAlgorithm.FIXED_WINDOW.value == "fixed_window"
    assert RateLimitAlgorithm.SLIDING_WINDOW.value == "sliding_window"
    assert RateLimitAlgorithm.CUSTOM.value == "custom"
    
    print(f"  All enum values verified")
    print(f"  Total algorithms: {len(RateLimitAlgorithm)}")
    
    print("\n" + "=" * 70)
    print("PASS: RateLimitAlgorithm enum")
    print("=" * 70)


def test_rate_limit_scope_enum():
    """
    Test: RateLimitScope enum.
    """
    print("=" * 70)
    print("TEST: RateLimitScope Enum")
    print("=" * 70)
    
    assert RateLimitScope.GLOBAL.value == "global"
    assert RateLimitScope.USER.value == "user"
    assert RateLimitScope.IP.value == "ip"
    assert RateLimitScope.API_KEY.value == "api_key"
    assert RateLimitScope.ENDPOINT.value == "endpoint"
    assert RateLimitScope.CUSTOM.value == "custom"
    
    print(f"  All enum values verified")
    print(f"  Total scopes: {len(RateLimitScope)}")
    
    print("\n" + "=" * 70)
    print("PASS: RateLimitScope enum")
    print("=" * 70)


def test_rate_limit_rule_dataclass():
    """
    Test: RateLimitRule dataclass.
    """
    print("=" * 70)
    print("TEST: RateLimitRule Dataclass")
    print("=" * 70)
    
    rule = RateLimitRule(
        rule_id="rule_1",
        scope=RateLimitScope.USER,
        algorithm=RateLimitAlgorithm.TOKEN_BUCKET,
        rate=100,
        period=60
    )
    
    assert rule.rule_id == "rule_1", "Rule ID eşleşmeli"
    assert rule.scope == RateLimitScope.USER, "Scope eşleşmeli"
    assert rule.rate == 100, "Rate eşleşmeli"
    
    print(f"  Rule ID: {rule.rule_id}")
    print(f"  Rate: {rule.rate}")
    
    print("\n" + "=" * 70)
    print("PASS: RateLimitRule dataclass")
    print("=" * 70)


def test_rate_limit_bucket_dataclass():
    """
    Test: RateLimitBucket dataclass.
    """
    print("=" * 70)
    print("TEST: RateLimitBucket Dataclass")
    print("=" * 70)
    
    bucket = RateLimitBucket(
        bucket_id="bucket_1",
        rule_id="rule_1",
        tokens=10.0
    )
    
    assert bucket.bucket_id == "bucket_1", "Bucket ID eşleşmeli"
    assert bucket.rule_id == "rule_1", "Rule ID eşleşmeli"
    assert bucket.tokens == 10.0, "Tokens eşleşmeli"
    
    print(f"  Bucket ID: {bucket.bucket_id}")
    print(f"  Tokens: {bucket.tokens}")
    
    print("\n" + "=" * 70)
    print("PASS: RateLimitBucket dataclass")
    print("=" * 70)


def test_rate_limit_config_dataclass():
    """
    Test: RateLimitConfig dataclass.
    """
    print("=" * 70)
    print("TEST: RateLimitConfig Dataclass")
    print("=" * 70)
    
    config = RateLimitConfig(default_rate=200)
    
    assert config.default_rate == 200, "Default rate eşleşmeli"
    
    print(f"  Default rate: {config.default_rate}")
    
    print("\n" + "=" * 70)
    print("PASS: RateLimitConfig dataclass")
    print("=" * 70)


def test_rate_limit_result_dataclass():
    """
    Test: RateLimitResult dataclass.
    """
    print("=" * 70)
    print("TEST: RateLimitResult Dataclass")
    print("=" * 70)
    
    result = RateLimitResult(allowed=True)
    result.message = "Test message"
    
    assert result.allowed == True, "Allowed eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Allowed: {result.allowed}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: RateLimitResult dataclass")
    print("=" * 70)


def test_rate_limiter_initialization():
    """
    Test: RateLimiter initialization.
    """
    print("=" * 70)
    print("TEST: RateLimiter Initialization")
    print("=" * 70)
    
    config = RateLimitConfig()
    limiter = RateLimiter(config)
    
    assert limiter.config == config, "Config eşleşmeli"
    assert len(limiter.rules) == 0, "Rules boş olmalı"
    assert len(limiter.buckets) == 0, "Buckets boş olmalı"
    
    print(f"  Rules: {len(limiter.rules)}")
    print(f"  Buckets: {len(limiter.buckets)}")
    
    print("\n" + "=" * 70)
    print("PASS: RateLimiter initialization")
    print("=" * 70)


def test_add_rule():
    """
    Test: Add rule.
    """
    print("=" * 70)
    print("TEST: Add Rule")
    print("=" * 70)
    
    limiter = RateLimiter()
    
    result = limiter.add_rule(
        scope=RateLimitScope.USER,
        algorithm=RateLimitAlgorithm.TOKEN_BUCKET,
        rate=100,
        period=60
    )
    
    assert result.allowed == True, "Ekleme başarılı olmalı"
    assert len(limiter.rules) > 0, "Rule eklenmeli"
    
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
    
    limiter = RateLimiter()
    
    result = limiter.add_rule(
        scope=RateLimitScope.USER,
        algorithm=RateLimitAlgorithm.TOKEN_BUCKET,
        rate=100,
        period=60
    )
    rule_id = result.rule_id
    
    result = limiter.remove_rule(rule_id)
    
    assert result.allowed == True, "Silme başarılı olmalı"
    assert rule_id not in limiter.rules, "Rule silinmeli"
    
    print(f"  Rule removed: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Remove rule")
    print("=" * 70)


def test_get_rule():
    """
    Test: Get rule.
    """
    print("=" * 70)
    print("TEST: Get Rule")
    print("=" * 70)
    
    limiter = RateLimiter()
    
    result = limiter.add_rule(
        scope=RateLimitScope.USER,
        algorithm=RateLimitAlgorithm.TOKEN_BUCKET,
        rate=100,
        period=60
    )
    rule_id = result.rule_id
    
    rule = limiter.get_rule(rule_id)
    
    assert rule is not None, "Rule bulunmalı"
    assert rule.rule_id == rule_id, "Rule ID eşleşmeli"
    
    print(f"  Rule: {rule.rule_id}")
    
    print("\n" + "=" * 70)
    print("PASS: Get rule")
    print("=" * 70)


def test_get_all_rules():
    """
    Test: Get all rules.
    """
    print("=" * 70)
    print("TEST: Get All Rules")
    print("=" * 70)
    
    limiter = RateLimiter()
    
    limiter.add_rule(RateLimitScope.USER, RateLimitAlgorithm.TOKEN_BUCKET, 100, 60)
    limiter.add_rule(RateLimitScope.IP, RateLimitAlgorithm.LEAKY_BUCKET, 50, 60)
    
    rules = limiter.get_all_rules()
    
    assert len(rules) == 2, "2 rule olmalı"
    
    print(f"  Total rules: {len(rules)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get all rules")
    print("=" * 70)


def test_check_rate_limit():
    """
    Test: Check rate limit.
    """
    print("=" * 70)
    print("TEST: Check Rate Limit")
    print("=" * 70)
    
    limiter = RateLimiter()
    
    result = limiter.add_rule(
        scope=RateLimitScope.USER,
        algorithm=RateLimitAlgorithm.TOKEN_BUCKET,
        rate=10,
        period=60,
        burst=5
    )
    
    check_result = limiter.check_rate_limit("user_1", result.rule_id)
    
    assert check_result.allowed == True, "İzin verilmeli"
    
    print(f"  Rate limit check: {check_result.message}")
    print(f"  Allowed: {check_result.allowed}")
    
    print("\n" + "=" * 70)
    print("PASS: Check rate limit")
    print("=" * 70)


def test_add_to_whitelist():
    """
    Test: Add to whitelist.
    """
    print("=" * 70)
    print("TEST: Add to Whitelist")
    print("=" * 70)
    
    limiter = RateLimiter()
    
    result = limiter.add_to_whitelist("user_1")
    
    assert result.allowed == True, "Ekleme başarılı olmalı"
    assert "user_1" in limiter.whitelist, "Whitelist'e eklenmeli"
    
    print(f"  Whitelist add: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add to whitelist")
    print("=" * 70)


def test_remove_from_whitelist():
    """
    Test: Remove from whitelist.
    """
    print("=" * 70)
    print("TEST: Remove from Whitelist")
    print("=" * 70)
    
    limiter = RateLimiter()
    
    limiter.add_to_whitelist("user_1")
    result = limiter.remove_from_whitelist("user_1")
    
    assert result.allowed == True, "Kaldırma başarılı olmalı"
    assert "user_1" not in limiter.whitelist, "Whitelist'ten kaldırılmalı"
    
    print(f"  Whitelist remove: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Remove from whitelist")
    print("=" * 70)


def test_add_to_blacklist():
    """
    Test: Add to blacklist.
    """
    print("=" * 70)
    print("TEST: Add to Blacklist")
    print("=" * 70)
    
    limiter = RateLimiter()
    
    result = limiter.add_to_blacklist("user_1")
    
    assert result.allowed == True, "Ekleme başarılı olmalı"
    assert "user_1" in limiter.blacklist, "Blacklist'e eklenmeli"
    
    print(f"  Blacklist add: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add to blacklist")
    print("=" * 70)


def test_remove_from_blacklist():
    """
    Test: Remove from blacklist.
    """
    print("=" * 70)
    print("TEST: Remove from Blacklist")
    print("=" * 70)
    
    limiter = RateLimiter()
    
    limiter.add_to_blacklist("user_1")
    result = limiter.remove_from_blacklist("user_1")
    
    assert result.allowed == True, "Kaldırma başarılı olmalı"
    assert "user_1" not in limiter.blacklist, "Blacklist'ten kaldırılmalı"
    
    print(f"  Blacklist remove: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Remove from blacklist")
    print("=" * 70)


def test_cleanup_buckets():
    """
    Test: Cleanup buckets.
    """
    print("=" * 70)
    print("TEST: Cleanup Buckets")
    print("=" * 70)
    
    limiter = RateLimiter()
    
    result = limiter.add_rule(RateLimitScope.USER, RateLimitAlgorithm.TOKEN_BUCKET, 10, 60)
    limiter.check_rate_limit("user_1", result.rule_id)
    
    result = limiter.cleanup_buckets()
    
    assert result.allowed == True, "Cleanup başarılı olmalı"
    
    print(f"  Cleanup: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Cleanup buckets")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    limiter = RateLimiter()
    
    new_config = RateLimitConfig(default_rate=200)
    result = limiter.update_config(new_config)
    
    assert result.allowed == True, "Update başarılı olmalı"
    assert limiter.config.default_rate == 200, "Config güncellenmeli"
    
    print(f"  Default rate: {limiter.config.default_rate}")
    
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
    
    config = RateLimitConfig(default_rate=200)
    limiter = RateLimiter(config)
    
    retrieved_config = limiter.get_config()
    
    assert retrieved_config.default_rate == 200, "Config eşleşmeli"
    
    print(f"  Default rate: {retrieved_config.default_rate}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_rate_limit_algorithm_enum()
        test2 = test_rate_limit_scope_enum()
        test3 = test_rate_limit_rule_dataclass()
        test4 = test_rate_limit_bucket_dataclass()
        test5 = test_rate_limit_config_dataclass()
        test6 = test_rate_limit_result_dataclass()
        test7 = test_rate_limiter_initialization()
        test8 = test_add_rule()
        test9 = test_remove_rule()
        test10 = test_get_rule()
        test11 = test_get_all_rules()
        test12 = test_check_rate_limit()
        test13 = test_add_to_whitelist()
        test14 = test_remove_from_whitelist()
        test15 = test_add_to_blacklist()
        test16 = test_remove_from_blacklist()
        test17 = test_cleanup_buckets()
        test18 = test_update_config()
        test19 = test_get_config()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"RateLimitAlgorithm Enum: {'PASS' if test1 else 'FAIL'}")
        print(f"RateLimitScope Enum: {'PASS' if test2 else 'FAIL'}")
        print(f"RateLimitRule Dataclass: {'PASS' if test3 else 'FAIL'}")
        print(f"RateLimitBucket Dataclass: {'PASS' if test4 else 'FAIL'}")
        print(f"RateLimitConfig Dataclass: {'PASS' if test5 else 'FAIL'}")
        print(f"RateLimitResult Dataclass: {'PASS' if test6 else 'FAIL'}")
        print(f"RateLimiter Initialization: {'PASS' if test7 else 'FAIL'}")
        print(f"Add Rule: {'PASS' if test8 else 'FAIL'}")
        print(f"Remove Rule: {'PASS' if test9 else 'FAIL'}")
        print(f"Get Rule: {'PASS' if test10 else 'FAIL'}")
        print(f"Get All Rules: {'PASS' if test11 else 'FAIL'}")
        print(f"Check Rate Limit: {'PASS' if test12 else 'FAIL'}")
        print(f"Add to Whitelist: {'PASS' if test13 else 'FAIL'}")
        print(f"Remove from Whitelist: {'PASS' if test14 else 'FAIL'}")
        print(f"Add to Blacklist: {'PASS' if test15 else 'FAIL'}")
        print(f"Remove from Blacklist: {'PASS' if test16 else 'FAIL'}")
        print(f"Cleanup Buckets: {'PASS' if test17 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test18 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test19 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14, test15, test16, test17, test18, test19])
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
