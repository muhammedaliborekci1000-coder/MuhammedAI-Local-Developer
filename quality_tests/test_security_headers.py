"""
Quality Test: Security Headers
Security headers system testleri for security module.
"""

import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from app.security.security_headers import (
    SecurityHeaderType,
    SecurityHeader,
    SecurityHeadersConfig,
    SecurityHeadersResult,
    SecurityHeadersManager
)


def test_security_header_type_enum():
    """
    Test: SecurityHeaderType enum.
    """
    print("=" * 70)
    print("TEST: SecurityHeaderType Enum")
    print("=" * 70)
    
    assert SecurityHeaderType.HSTS.value == "Strict-Transport-Security"
    assert SecurityHeaderType.X_FRAME_OPTIONS.value == "X-Frame-Options"
    assert SecurityHeaderType.X_CONTENT_TYPE_OPTIONS.value == "X-Content-Type-Options"
    assert SecurityHeaderType.X_XSS_PROTECTION.value == "X-XSS-Protection"
    
    print(f"  All enum values verified")
    print(f"  Total types: {len(SecurityHeaderType)}")
    
    print("\n" + "=" * 70)
    print("PASS: SecurityHeaderType enum")
    print("=" * 70)


def test_security_header_dataclass():
    """
    Test: SecurityHeader dataclass.
    """
    print("=" * 70)
    print("TEST: SecurityHeader Dataclass")
    print("=" * 70)
    
    header = SecurityHeader(
        header_id="header_1",
        header_type=SecurityHeaderType.HSTS,
        value="max-age=31536000"
    )
    
    assert header.header_id == "header_1", "Header ID eşleşmeli"
    assert header.header_type == SecurityHeaderType.HSTS, "Header type eşleşmeli"
    
    print(f"  Header ID: {header.header_id}")
    
    print("\n" + "=" * 70)
    print("PASS: SecurityHeader dataclass")
    print("=" * 70)


def test_security_headers_config_dataclass():
    """
    Test: SecurityHeadersConfig dataclass.
    """
    print("=" * 70)
    print("TEST: SecurityHeadersConfig Dataclass")
    print("=" * 70)
    
    config = SecurityHeadersConfig(enable_hsts=True)
    
    assert config.enable_hsts == True, "Enable HSTS eşleşmeli"
    
    print(f"  Enable HSTS: {config.enable_hsts}")
    
    print("\n" + "=" * 70)
    print("PASS: SecurityHeadersConfig dataclass")
    print("=" * 70)


def test_security_headers_result_dataclass():
    """
    Test: SecurityHeadersResult dataclass.
    """
    print("=" * 70)
    print("TEST: SecurityHeadersResult Dataclass")
    print("=" * 70)
    
    result = SecurityHeadersResult(success=True)
    
    assert result.success == True, "Success eşleşmeli"
    assert isinstance(result.headers, dict), "Headers dict olmalı"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: SecurityHeadersResult dataclass")
    print("=" * 70)


def test_security_headers_manager_initialization():
    """
    Test: SecurityHeadersManager initialization.
    """
    print("=" * 70)
    print("TEST: SecurityHeadersManager Initialization")
    print("=" * 70)
    
    config = SecurityHeadersConfig()
    manager = SecurityHeadersManager(config)
    
    assert manager.config == config, "Config eşleşmeli"
    
    print(f"  Manager initialized")
    
    print("\n" + "=" * 70)
    print("PASS: SecurityHeadersManager initialization")
    print("=" * 70)


def test_add_header():
    """
    Test: Add header.
    """
    print("=" * 70)
    print("TEST: Add Header")
    print("=" * 70)
    
    manager = SecurityHeadersManager()
    
    result = manager.add_header(
        header_type=SecurityHeaderType.HSTS,
        value="max-age=31536000"
    )
    
    assert result.success == True, "Ekleme başarılı olmalı"
    
    print(f"  Header added: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add header")
    print("=" * 70)


def test_remove_header():
    """
    Test: Remove header.
    """
    print("=" * 70)
    print("TEST: Remove Header")
    print("=" * 70)
    
    manager = SecurityHeadersManager()
    
    # First add a custom header
    manager.add_header(SecurityHeaderType.CROSS_ORIGIN_OPENER_POLICY, "same-origin")
    
    result = manager.remove_header(SecurityHeaderType.CROSS_ORIGIN_OPENER_POLICY)
    
    assert result.success == True, "Silme başarılı olmalı"
    
    print(f"  Header removed: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Remove header")
    print("=" * 70)


def test_generate_headers():
    """
    Test: Generate headers.
    """
    print("=" * 70)
    print("TEST: Generate Headers")
    print("=" * 70)
    
    manager = SecurityHeadersManager()
    
    result = manager.generate_headers()
    
    assert result.success == True, "Generation başarılı olmalı"
    assert len(result.headers) > 0, "Headers olmalı"
    
    print(f"  Headers generated: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Generate headers")
    print("=" * 70)


def test_get_header():
    """
    Test: Get header.
    """
    print("=" * 70)
    print("TEST: Get Header")
    print("=" * 70)
    
    manager = SecurityHeadersManager()
    
    # Add a custom header first
    manager.add_header(SecurityHeaderType.CROSS_ORIGIN_OPENER_POLICY, "same-origin")
    
    header = manager.get_header(SecurityHeaderType.CROSS_ORIGIN_OPENER_POLICY)
    
    assert header is not None, "Header bulunmalı"
    
    print(f"  Header found")
    
    print("\n" + "=" * 70)
    print("PASS: Get header")
    print("=" * 70)


def test_get_all_headers():
    """
    Test: Get all headers.
    """
    print("=" * 70)
    print("TEST: Get All Headers")
    print("=" * 70)
    
    manager = SecurityHeadersManager()
    
    headers = manager.get_all_headers()
    
    assert len(headers) > 0, "Headers olmalı"
    
    print(f"  Headers: {len(headers)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get all headers")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    manager = SecurityHeadersManager()
    
    new_config = SecurityHeadersConfig(enable_hsts=False)
    result = manager.update_config(new_config)
    
    assert result.success == True, "Update başarılı olmalı"
    assert manager.config.enable_hsts == False, "Config güncellenmeli"
    
    print(f"  Enable HSTS: {manager.config.enable_hsts}")
    
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
    
    config = SecurityHeadersConfig(enable_hsts=False)
    manager = SecurityHeadersManager(config)
    
    retrieved_config = manager.get_config()
    
    assert retrieved_config.enable_hsts == False, "Config eşleşmeli"
    
    print(f"  Enable HSTS: {retrieved_config.enable_hsts}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_security_header_type_enum()
        test2 = test_security_header_dataclass()
        test3 = test_security_headers_config_dataclass()
        test4 = test_security_headers_result_dataclass()
        test5 = test_security_headers_manager_initialization()
        test6 = test_add_header()
        test7 = test_remove_header()
        test8 = test_generate_headers()
        test9 = test_get_header()
        test10 = test_get_all_headers()
        test11 = test_update_config()
        test12 = test_get_config()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"SecurityHeaderType Enum: {'PASS' if test1 else 'FAIL'}")
        print(f"SecurityHeader Dataclass: {'PASS' if test2 else 'FAIL'}")
        print(f"SecurityHeadersConfig Dataclass: {'PASS' if test3 else 'FAIL'}")
        print(f"SecurityHeadersResult Dataclass: {'PASS' if test4 else 'FAIL'}")
        print(f"SecurityHeadersManager Initialization: {'PASS' if test5 else 'FAIL'}")
        print(f"Add Header: {'PASS' if test6 else 'FAIL'}")
        print(f"Remove Header: {'PASS' if test7 else 'FAIL'}")
        print(f"Generate Headers: {'PASS' if test8 else 'FAIL'}")
        print(f"Get Header: {'PASS' if test9 else 'FAIL'}")
        print(f"Get All Headers: {'PASS' if test10 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test11 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test12 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12])
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
