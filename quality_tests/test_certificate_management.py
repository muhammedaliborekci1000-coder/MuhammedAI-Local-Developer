"""
Quality Test: Certificate Management
Certificate management system testleri for security module.
"""

import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from app.security.certificate_management import (
    CertificateType,
    CertificateStatus,
    CertificateAlgorithm,
    Certificate,
    CertificateConfig,
    CertificateResult,
    CertificateManager
)


def test_certificate_type_enum():
    """
    Test: CertificateType enum.
    """
    print("=" * 70)
    print("TEST: CertificateType Enum")
    print("=" * 70)
    
    assert CertificateType.SSL.value == "ssl"
    assert CertificateType.TLS.value == "tls"
    assert CertificateType.CLIENT.value == "client"
    assert CertificateType.SERVER.value == "server"
    
    print(f"  All enum values verified")
    print(f"  Total types: {len(CertificateType)}")
    
    print("\n" + "=" * 70)
    print("PASS: CertificateType enum")
    print("=" * 70)


def test_certificate_status_enum():
    """
    Test: CertificateStatus enum.
    """
    print("=" * 70)
    print("TEST: CertificateStatus Enum")
    print("=" * 70)
    
    assert CertificateStatus.ACTIVE.value == "active"
    assert CertificateStatus.EXPIRED.value == "expired"
    assert CertificateStatus.REVOKED.value == "revoked"
    assert CertificateStatus.PENDING.value == "pending"
    assert CertificateStatus.SUSPENDED.value == "suspended"
    
    print(f"  All enum values verified")
    print(f"  Total statuses: {len(CertificateStatus)}")
    
    print("\n" + "=" * 70)
    print("PASS: CertificateStatus enum")
    print("=" * 70)


def test_certificate_algorithm_enum():
    """
    Test: CertificateAlgorithm enum.
    """
    print("=" * 70)
    print("TEST: CertificateAlgorithm Enum")
    print("=" * 70)
    
    assert CertificateAlgorithm.RSA_2048.value == "rsa_2048"
    assert CertificateAlgorithm.RSA_4096.value == "rsa_4096"
    assert CertificateAlgorithm.ECDSA_P256.value == "ecdsa_p256"
    assert CertificateAlgorithm.ECDSA_P384.value == "ecdsa_p384"
    
    print(f"  All enum values verified")
    print(f"  Total algorithms: {len(CertificateAlgorithm)}")
    
    print("\n" + "=" * 70)
    print("PASS: CertificateAlgorithm enum")
    print("=" * 70)


def test_certificate_dataclass():
    """
    Test: Certificate dataclass.
    """
    print("=" * 70)
    print("TEST: Certificate Dataclass")
    print("=" * 70)
    
    certificate = Certificate(
        certificate_id="cert_1",
        certificate_type=CertificateType.SSL,
        algorithm=CertificateAlgorithm.RSA_2048,
        public_key="pub_key_123",
        private_key="priv_key_123",
        issuer="CN=MyCA",
        subject="CN=example.com",
        serial_number="serial_123",
        status=CertificateStatus.ACTIVE,
        issued_at="1234567890",
        expires_at="1234567890"
    )
    
    assert certificate.certificate_id == "cert_1", "Certificate ID eşleşmeli"
    assert certificate.certificate_type == CertificateType.SSL, "Type eşleşmeli"
    
    print(f"  Certificate ID: {certificate.certificate_id}")
    
    print("\n" + "=" * 70)
    print("PASS: Certificate dataclass")
    print("=" * 70)


def test_certificate_config_dataclass():
    """
    Test: CertificateConfig dataclass.
    """
    print("=" * 70)
    print("TEST: CertificateConfig Dataclass")
    print("=" * 70)
    
    config = CertificateConfig(enable_auto_renewal=True)
    
    assert config.enable_auto_renewal == True, "Enable auto renewal eşleşmeli"
    
    print(f"  Enable auto renewal: {config.enable_auto_renewal}")
    
    print("\n" + "=" * 70)
    print("PASS: CertificateConfig dataclass")
    print("=" * 70)


def test_certificate_result_dataclass():
    """
    Test: CertificateResult dataclass.
    """
    print("=" * 70)
    print("TEST: CertificateResult Dataclass")
    print("=" * 70)
    
    result = CertificateResult(success=True)
    
    assert result.success == True, "Success eşleşmeli"
    assert isinstance(result.certificates, list), "Certificates list olmalı"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: CertificateResult dataclass")
    print("=" * 70)


def test_certificate_manager_initialization():
    """
    Test: CertificateManager initialization.
    """
    print("=" * 70)
    print("TEST: CertificateManager Initialization")
    print("=" * 70)
    
    config = CertificateConfig()
    manager = CertificateManager(config)
    
    assert manager.config == config, "Config eşleşmeli"
    
    print(f"  Manager initialized")
    
    print("\n" + "=" * 70)
    print("PASS: CertificateManager initialization")
    print("=" * 70)


def test_generate_certificate():
    """
    Test: Generate certificate.
    """
    print("=" * 70)
    print("TEST: Generate Certificate")
    print("=" * 70)
    
    manager = CertificateManager()
    
    result = manager.generate_certificate(
        certificate_type=CertificateType.SSL,
        subject="CN=example.com",
        issuer="CN=MyCA"
    )
    
    assert result.success == True, "Generation başarılı olmalı"
    assert result.certificate is not None, "Certificate olmalı"
    
    print(f"  Certificate generated: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Generate certificate")
    print("=" * 70)


def test_validate_certificate():
    """
    Test: Validate certificate.
    """
    print("=" * 70)
    print("TEST: Validate Certificate")
    print("=" * 70)
    
    manager = CertificateManager()
    
    result = manager.generate_certificate(
        certificate_type=CertificateType.SSL,
        subject="CN=example.com",
        issuer="CN=MyCA"
    )
    
    validation = manager.validate_certificate(result.certificate.certificate_id)
    
    assert validation.success == True, "Validation başarılı olmalı"
    
    print(f"  Valid: {validation.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Validate certificate")
    print("=" * 70)


def test_revoke_certificate():
    """
    Test: Revoke certificate.
    """
    print("=" * 70)
    print("TEST: Revoke Certificate")
    print("=" * 70)
    
    manager = CertificateManager()
    
    result = manager.generate_certificate(
        certificate_type=CertificateType.SSL,
        subject="CN=example.com",
        issuer="CN=MyCA"
    )
    
    revoke_result = manager.revoke_certificate(result.certificate.certificate_id)
    
    assert revoke_result.success == True, "Revoke başarılı olmalı"
    
    print(f"  Revoked: {revoke_result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Revoke certificate")
    print("=" * 70)


def test_renew_certificate():
    """
    Test: Renew certificate.
    """
    print("=" * 70)
    print("TEST: Renew Certificate")
    print("=" * 70)
    
    manager = CertificateManager()
    
    result = manager.generate_certificate(
        certificate_type=CertificateType.SSL,
        subject="CN=example.com",
        issuer="CN=MyCA"
    )
    
    renew_result = manager.renew_certificate(result.certificate.certificate_id)
    
    assert renew_result.success == True, "Renew başarılı olmalı"
    
    print(f"  Renewed: {renew_result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Renew certificate")
    print("=" * 70)


def test_get_certificate():
    """
    Test: Get certificate.
    """
    print("=" * 70)
    print("TEST: Get Certificate")
    print("=" * 70)
    
    manager = CertificateManager()
    
    result = manager.generate_certificate(
        certificate_type=CertificateType.SSL,
        subject="CN=example.com",
        issuer="CN=MyCA"
    )
    
    certificate = manager.get_certificate(result.certificate.certificate_id)
    
    assert certificate is not None, "Certificate bulunmalı"
    
    print(f"  Certificate found")
    
    print("\n" + "=" * 70)
    print("PASS: Get certificate")
    print("=" * 70)


def test_get_certificates_by_type():
    """
    Test: Get certificates by type.
    """
    print("=" * 70)
    print("TEST: Get Certificates by Type")
    print("=" * 70)
    
    manager = CertificateManager()
    
    manager.generate_certificate(CertificateType.SSL, "CN=example.com", "CN=MyCA")
    manager.generate_certificate(CertificateType.SSL, "CN=test.com", "CN=MyCA")
    
    certificates = manager.get_certificates_by_type(CertificateType.SSL)
    
    assert len(certificates) == 2, "2 certificate olmalı"
    
    print(f"  Certificates: {len(certificates)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get certificates by type")
    print("=" * 70)


def test_get_all_certificates():
    """
    Test: Get all certificates.
    """
    print("=" * 70)
    print("TEST: Get All Certificates")
    print("=" * 70)
    
    manager = CertificateManager()
    
    manager.generate_certificate(CertificateType.SSL, "CN=example.com", "CN=MyCA")
    manager.generate_certificate(CertificateType.TLS, "CN=test.com", "CN=MyCA")
    
    certificates = manager.get_all_certificates()
    
    assert len(certificates) == 2, "2 certificate olmalı"
    
    print(f"  Certificates: {len(certificates)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get all certificates")
    print("=" * 70)


def test_check_expiry():
    """
    Test: Check expiry.
    """
    print("=" * 70)
    print("TEST: Check Expiry")
    print("=" * 70)
    
    manager = CertificateManager()
    
    result = manager.check_expiry()
    
    assert result.success == True, "Check başarılı olmalı"
    
    print(f"  Expiry check: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Check expiry")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    manager = CertificateManager()
    
    new_config = CertificateConfig(enable_auto_renewal=False)
    result = manager.update_config(new_config)
    
    assert result.success == True, "Update başarılı olmalı"
    assert manager.config.enable_auto_renewal == False, "Config güncellenmeli"
    
    print(f"  Enable auto renewal: {manager.config.enable_auto_renewal}")
    
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
    
    config = CertificateConfig(enable_auto_renewal=False)
    manager = CertificateManager(config)
    
    retrieved_config = manager.get_config()
    
    assert retrieved_config.enable_auto_renewal == False, "Config eşleşmeli"
    
    print(f"  Enable auto renewal: {retrieved_config.enable_auto_renewal}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_certificate_type_enum()
        test2 = test_certificate_status_enum()
        test3 = test_certificate_algorithm_enum()
        test4 = test_certificate_dataclass()
        test5 = test_certificate_config_dataclass()
        test6 = test_certificate_result_dataclass()
        test7 = test_certificate_manager_initialization()
        test8 = test_generate_certificate()
        test9 = test_validate_certificate()
        test10 = test_revoke_certificate()
        test11 = test_renew_certificate()
        test12 = test_get_certificate()
        test13 = test_get_certificates_by_type()
        test14 = test_get_all_certificates()
        test15 = test_check_expiry()
        test16 = test_update_config()
        test17 = test_get_config()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"CertificateType Enum: {'PASS' if test1 else 'FAIL'}")
        print(f"CertificateStatus Enum: {'PASS' if test2 else 'FAIL'}")
        print(f"CertificateAlgorithm Enum: {'PASS' if test3 else 'FAIL'}")
        print(f"Certificate Dataclass: {'PASS' if test4 else 'FAIL'}")
        print(f"CertificateConfig Dataclass: {'PASS' if test5 else 'FAIL'}")
        print(f"CertificateResult Dataclass: {'PASS' if test6 else 'FAIL'}")
        print(f"CertificateManager Initialization: {'PASS' if test7 else 'FAIL'}")
        print(f"Generate Certificate: {'PASS' if test8 else 'FAIL'}")
        print(f"Validate Certificate: {'PASS' if test9 else 'FAIL'}")
        print(f"Revoke Certificate: {'PASS' if test10 else 'FAIL'}")
        print(f"Renew Certificate: {'PASS' if test11 else 'FAIL'}")
        print(f"Get Certificate: {'PASS' if test12 else 'FAIL'}")
        print(f"Get Certificates by Type: {'PASS' if test13 else 'FAIL'}")
        print(f"Get All Certificates: {'PASS' if test14 else 'FAIL'}")
        print(f"Check Expiry: {'PASS' if test15 else 'FAIL'}")
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
