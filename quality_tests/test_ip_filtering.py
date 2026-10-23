"""
Quality Test: IP Filtering
IP filtering system testleri for security module.
"""

import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from app.security.ip_filtering import (
    IPFilterType,
    IPFilterAction,
    IPFilter,
    IPFilterConfig,
    IPFilterResult,
    IPFilterManager
)


def test_ip_filter_type_enum():
    """
    Test: IPFilterType enum.
    """
    print("=" * 70)
    print("TEST: IPFilterType Enum")
    print("=" * 70)
    
    assert IPFilterType.WHITELIST.value == "whitelist"
    assert IPFilterType.BLACKLIST.value == "blacklist"
    assert IPFilterType.CUSTOM.value == "custom"
    
    print(f"  All enum values verified")
    print(f"  Total types: {len(IPFilterType)}")
    
    print("\n" + "=" * 70)
    print("PASS: IPFilterType enum")
    print("=" * 70)


def test_ip_filter_action_enum():
    """
    Test: IPFilterAction enum.
    """
    print("=" * 70)
    print("TEST: IPFilterAction Enum")
    print("=" * 70)
    
    assert IPFilterAction.ALLOW.value == "allow"
    assert IPFilterAction.DENY.value == "deny"
    assert IPFilterAction.RATE_LIMIT.value == "rate_limit"
    assert IPFilterAction.LOG.value == "log"
    
    print(f"  All enum values verified")
    print(f"  Total actions: {len(IPFilterAction)}")
    
    print("\n" + "=" * 70)
    print("PASS: IPFilterAction enum")
    print("=" * 70)


def test_ip_filter_dataclass():
    """
    Test: IPFilter dataclass.
    """
    print("=" * 70)
    print("TEST: IPFilter Dataclass")
    print("=" * 70)
    
    ip_filter = IPFilter(
        filter_id="filter_1",
        ip_address="192.168.1.1",
        filter_type=IPFilterType.WHITELIST,
        action=IPFilterAction.ALLOW
    )
    
    assert ip_filter.filter_id == "filter_1", "Filter ID eşleşmeli"
    assert ip_filter.filter_type == IPFilterType.WHITELIST, "Filter type eşleşmeli"
    
    print(f"  Filter ID: {ip_filter.filter_id}")
    
    print("\n" + "=" * 70)
    print("PASS: IPFilter dataclass")
    print("=" * 70)


def test_ip_filter_config_dataclass():
    """
    Test: IPFilterConfig dataclass.
    """
    print("=" * 70)
    print("TEST: IPFilterConfig Dataclass")
    print("=" * 70)
    
    config = IPFilterConfig(enable_ipv6=True)
    
    assert config.enable_ipv6 == True, "Enable IPv6 eşleşmeli"
    
    print(f"  Enable IPv6: {config.enable_ipv6}")
    
    print("\n" + "=" * 70)
    print("PASS: IPFilterConfig dataclass")
    print("=" * 70)


def test_ip_filter_result_dataclass():
    """
    Test: IPFilterResult dataclass.
    """
    print("=" * 70)
    print("TEST: IPFilterResult Dataclass")
    print("=" * 70)
    
    result = IPFilterResult(success=True)
    
    assert result.success == True, "Success eşleşmeli"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: IPFilterResult dataclass")
    print("=" * 70)


def test_ip_filter_manager_initialization():
    """
    Test: IPFilterManager initialization.
    """
    print("=" * 70)
    print("TEST: IPFilterManager Initialization")
    print("=" * 70)
    
    config = IPFilterConfig()
    manager = IPFilterManager(config)
    
    assert manager.config == config, "Config eşleşmeli"
    
    print(f"  Manager initialized")
    
    print("\n" + "=" * 70)
    print("PASS: IPFilterManager initialization")
    print("=" * 70)


def test_add_filter():
    """
    Test: Add filter.
    """
    print("=" * 70)
    print("TEST: Add Filter")
    print("=" * 70)
    
    manager = IPFilterManager()
    
    result = manager.add_filter(
        ip_address="192.168.1.1",
        filter_type=IPFilterType.WHITELIST,
        action=IPFilterAction.ALLOW
    )
    
    assert result.success == True, "Ekleme başarılı olmalı"
    
    print(f"  Filter added: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add filter")
    print("=" * 70)


def test_remove_filter():
    """
    Test: Remove filter.
    """
    print("=" * 70)
    print("TEST: Remove Filter")
    print("=" * 70)
    
    manager = IPFilterManager()
    
    result = manager.add_filter("192.168.1.1", IPFilterType.WHITELIST, IPFilterAction.ALLOW)
    filter_id = result.filter.filter_id
    
    remove_result = manager.remove_filter(filter_id)
    
    assert remove_result.success == True, "Silme başarılı olmalı"
    
    print(f"  Filter removed: {remove_result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Remove filter")
    print("=" * 70)


def test_check_ip():
    """
    Test: Check IP.
    """
    print("=" * 70)
    print("TEST: Check IP")
    print("=" * 70)
    
    manager = IPFilterManager()
    
    manager.add_filter("192.168.1.1", IPFilterType.WHITELIST, IPFilterAction.ALLOW)
    
    result = manager.check_ip("192.168.1.1")
    
    assert result.is_allowed == True, "IP izinli olmalı"
    
    print(f"  Allowed: {result.is_allowed}")
    
    print("\n" + "=" * 70)
    print("PASS: Check IP")
    print("=" * 70)


def test_get_whitelist():
    """
    Test: Get whitelist.
    """
    print("=" * 70)
    print("TEST: Get Whitelist")
    print("=" * 70)
    
    manager = IPFilterManager()
    
    manager.add_filter("192.168.1.1", IPFilterType.WHITELIST, IPFilterAction.ALLOW)
    manager.add_filter("192.168.1.2", IPFilterType.WHITELIST, IPFilterAction.ALLOW)
    
    whitelist = manager.get_whitelist()
    
    assert len(whitelist) == 2, "2 whitelist item olmalı"
    
    print(f"  Whitelist: {len(whitelist)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get whitelist")
    print("=" * 70)


def test_get_blacklist():
    """
    Test: Get blacklist.
    """
    print("=" * 70)
    print("TEST: Get Blacklist")
    print("=" * 70)
    
    manager = IPFilterManager()
    
    manager.add_filter("192.168.1.1", IPFilterType.BLACKLIST, IPFilterAction.DENY)
    manager.add_filter("192.168.1.2", IPFilterType.BLACKLIST, IPFilterAction.DENY)
    
    blacklist = manager.get_blacklist()
    
    assert len(blacklist) == 2, "2 blacklist item olmalı"
    
    print(f"  Blacklist: {len(blacklist)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get blacklist")
    print("=" * 70)


def test_get_all_filters():
    """
    Test: Get all filters.
    """
    print("=" * 70)
    print("TEST: Get All Filters")
    print("=" * 70)
    
    manager = IPFilterManager()
    
    manager.add_filter("192.168.1.1", IPFilterType.WHITELIST, IPFilterAction.ALLOW)
    manager.add_filter("192.168.1.2", IPFilterType.BLACKLIST, IPFilterAction.DENY)
    
    filters = manager.get_all_filters()
    
    assert len(filters) == 2, "2 filter olmalı"
    
    print(f"  Filters: {len(filters)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get all filters")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    manager = IPFilterManager()
    
    new_config = IPFilterConfig(default_action=IPFilterAction.DENY)
    result = manager.update_config(new_config)
    
    assert result.success == True, "Update başarılı olmalı"
    assert manager.config.default_action == IPFilterAction.DENY, "Config güncellenmeli"
    
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
    
    config = IPFilterConfig(default_action=IPFilterAction.DENY)
    manager = IPFilterManager(config)
    
    retrieved_config = manager.get_config()
    
    assert retrieved_config.default_action == IPFilterAction.DENY, "Config eşleşmeli"
    
    print(f"  Default action: {retrieved_config.default_action.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_ip_filter_type_enum()
        test2 = test_ip_filter_action_enum()
        test3 = test_ip_filter_dataclass()
        test4 = test_ip_filter_config_dataclass()
        test5 = test_ip_filter_result_dataclass()
        test6 = test_ip_filter_manager_initialization()
        test7 = test_add_filter()
        test8 = test_remove_filter()
        test9 = test_check_ip()
        test10 = test_get_whitelist()
        test11 = test_get_blacklist()
        test12 = test_get_all_filters()
        test13 = test_update_config()
        test14 = test_get_config()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"IPFilterType Enum: {'PASS' if test1 else 'FAIL'}")
        print(f"IPFilterAction Enum: {'PASS' if test2 else 'FAIL'}")
        print(f"IPFilter Dataclass: {'PASS' if test3 else 'FAIL'}")
        print(f"IPFilterConfig Dataclass: {'PASS' if test4 else 'FAIL'}")
        print(f"IPFilterResult Dataclass: {'PASS' if test5 else 'FAIL'}")
        print(f"IPFilterManager Initialization: {'PASS' if test6 else 'FAIL'}")
        print(f"Add Filter: {'PASS' if test7 else 'FAIL'}")
        print(f"Remove Filter: {'PASS' if test8 else 'FAIL'}")
        print(f"Check IP: {'PASS' if test9 else 'FAIL'}")
        print(f"Get Whitelist: {'PASS' if test10 else 'FAIL'}")
        print(f"Get Blacklist: {'PASS' if test11 else 'FAIL'}")
        print(f"Get All Filters: {'PASS' if test12 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test13 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test14 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14])
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
