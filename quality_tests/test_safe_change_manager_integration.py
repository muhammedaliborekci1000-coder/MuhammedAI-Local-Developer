"""
Integration Test: SafeChangeManager
Amaç: Gerçek SafeChangeManager uygulamasını, dosya değişikliğini, test çalıştırmayı,
backup oluşturmayı ve rollback mekanizmasını doğrulamak.

Gerçek Kullanılan Sınıflar:
- SafeChangeManager - gerçek production kodu
- BackupManager - gerçek production kodu
- CodePatchApplier - gerçek production kodu
- RollbackManager - gerçek production kodu
- PythonRunner - gerçek production kodu

NOT: Bu testler gerçek dosya işlemleri yapar. Geçici çalışma alanı kullanılır.
"""

import pytest
import sys
import os
import shutil
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.tools.safe_change_manager import SafeChangeManager
from app.tools.backup_manager import BackupManager
from app.tools.code_patch_applier import CodePatchApplier
from app.tools.rollback_manager import RollbackManager
from app.tools.python_runner import PythonRunner
from app.core.config import PROJECT_ROOT


@pytest.fixture
def tmp_path():
    """Create and clean up temporary workspace."""
    tmp_dir = PROJECT_ROOT / "quality_tests" / "safe_change_workspace"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    yield tmp_dir
    if tmp_dir.exists():
        shutil.rmtree(tmp_dir)


def test_safe_change_success_and_backup(tmp_path):
    """
    TEST A — Başarılı Değişiklik ve Gerçek Backup
    
    Geçici çalışma alanında başlangıç dosyası oluştur.
    Gerçek değişiklik uygulama akışını çağır.
    Backup'ın gerçekten oluşturulduğunu ve diskte bulunduğunu doğrula.
    Dosyanın beklenen içerikle değiştiğini doğrula.
    Gerçek test çalıştırıcısının çalıştığını doğrula.
    Sonucun başarılı olduğunu doğrula.
    Backup içeriğinin ilk dosyayla aynı olduğunu doğrula.
    """
    print("\n" + "=" * 70)
    print("TEST A — Başarılı Değişiklik ve Gerçek Backup")
    print("=" * 70)
    
    # Setup dosyaları
    calculator_file = tmp_path / "calculator.py"
    original_code = 'def add(a, b):\n    return a - b\n'
    with open(calculator_file, 'w', encoding='utf-8') as f:
        f.write(original_code)
    
    test_file = tmp_path / "test_calculator.py"
    test_code = '''
def test_add():
    assert add(2, 3) == 5
'''
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(test_code)
    
    # SafeChangeManager oluştur (gerçek bileşenlerle)
    safe_manager = SafeChangeManager()
    
    # Bileşenlerin project_root'unu geçici alana ayarla
    safe_manager.backup.project_root = tmp_path
    safe_manager.patcher.project_root = tmp_path
    safe_manager.rollback.project_root = tmp_path
    safe_manager.runner.project_root = tmp_path
    
    # Dosya yollarını relative olarak belirle
    relative_calc = "calculator.py"
    relative_test = "test_calculator.py"
    
    # Değişikliği uygula
    result = safe_manager.apply_patch_and_test(
        file_path=relative_calc,
        old_code=original_code,
        new_code='def add(a, b):\n    return a + b\n',
        test_file=relative_test
    )
    
    print(f"\nSonuç:")
    print(f"Success: {result.get('success')}")
    print(f"Backup: {result.get('backup')}")
    print(f"Patch: {result.get('patch')}")
    print(f"Syntax: {result.get('syntax')}")
    print(f"Test: {result.get('test')}")
    print(f"Error: {result.get('error')}")
    
    # Zorunlu assertion'lar
    assert result.get("success") is True, "Sonuç başarısız"
    print("✓ Sonuç başarılı.")
    
    assert result.get("backup") is not None, "Backup oluşturulmadı"
    backup_path = Path(result.get("backup"))
    assert backup_path.exists(), "Backup dosyası diskte bulunamadı"
    print(f"✓ Backup oluşturuldu: {backup_path}")
    
    # Dosyanın değiştiğini doğrula
    with open(calculator_file, 'r', encoding='utf-8') as f:
        final_code = f.read()
    assert "return a + b" in final_code or "return a+b" in final_code, "Dosya değiştirilmedi"
    print("✓ Dosya değiştirildi.")
    
    # Test çalıştırıcısının çalıştığını doğrula
    test_result = result.get("test")
    assert test_result is not None, "Test sonucu yok"
    assert test_result.get("success") is True, "Test başarısız"
    print("✓ Test çalıştırıcısı çalıştı ve başarılı.")
    
    # Backup içeriğinin ilk dosyayla aynı olduğunu doğrula
    with open(backup_path, 'r', encoding='utf-8') as f:
        backup_content = f.read()
    assert backup_content == original_code, "Backup içeriği yanlış"
    print("✓ Backup içeriği doğru.")
    
    # Cleanup backup
    if backup_path.exists():
        # backup_path: .muhammedai_backups/timestamp/calculator.py
        backup_timestamp_dir = backup_path.parent  # .muhammedai_backups/timestamp
        if backup_timestamp_dir.exists():
            shutil.rmtree(backup_timestamp_dir)
    
    print("\n" + "=" * 70)
    print("TEST A: PASS")
    print("=" * 70)


def test_safe_change_test_failure_rollback(tmp_path):
    """
    TEST B — Test Başarısızlığında Gerçek Rollback
    
    Başlangıç dosyasını oluştur ve içeriğini kaydet.
    Gerçek değişiklik uygulama akışını çalıştır.
    Kontrollü bir test hatası oluştur.
    Test başarısız olduğunda gerçek rollback mekanizmasının çağrıldığını doğrula.
    Dosyanın ilk içeriğine geri döndüğünü doğrula.
    Backup'ın varlığını ve test sonucunun başarısız olduğunu doğrula.
    """
    print("\n" + "=" * 70)
    print("TEST B — Test Başarısızlığında Gerçek Rollback")
    print("=" * 70)
    
    # Setup dosyaları
    calculator_file = tmp_path / "calculator.py"
    original_code = 'def add(a, b):\n    return a - b\n'
    with open(calculator_file, 'w', encoding='utf-8') as f:
        f.write(original_code)
    
    test_file = tmp_path / "test_calculator.py"
    test_code = '''
def test_add():
    assert add(2, 3) == 5  # Bu test başarısız olacak çünkü add a - b döndürüyor
'''
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(test_code)
    
    # SafeChangeManager oluştur
    safe_manager = SafeChangeManager()
    
    # Bileşenlerin project_root'unu geçici alana ayarla
    safe_manager.backup.project_root = tmp_path
    safe_manager.patcher.project_root = tmp_path
    safe_manager.rollback.project_root = tmp_path
    safe_manager.runner.project_root = tmp_path
    
    # Dosya yollarını relative olarak belirle
    relative_calc = "calculator.py"
    relative_test = "test_calculator.py"
    
    # Değişikliği uygula (syntax hatası içeren kod ile test başarısız olacak)
    result = safe_manager.apply_patch_and_test(
        file_path=relative_calc,
        old_code=original_code,
        new_code='def add(a, b):\n    return a + b\n    syntax error here',  # Syntax hatası
        test_file=relative_test
    )
    
    print(f"\nSonuç:")
    print(f"Success: {result.get('success')}")
    print(f"Backup: {result.get('backup')}")
    print(f"Patch: {result.get('patch')}")
    print(f"Syntax: {result.get('syntax')}")
    print(f"Test: {result.get('test')}")
    print(f"Error: {result.get('error')}")
    print(f"Rollback: {result.get('rollback')}")
    
    # Zorunlu assertion'lar
    assert result.get("success") is False, "Sonuç başarılı olmamalı"
    print("✓ Sonuç başarısız (beklenen).")
    
    assert result.get("backup") is not None, "Backup oluşturulmadı"
    backup_path = Path(result.get("backup"))
    assert backup_path.exists(), "Backup dosyası diskte bulunamadı"
    print(f"✓ Backup oluşturuldu: {backup_path}")
    
    # Syntax hatası olduğu için test çalıştırılmadı
    assert result.get("syntax") != "OK", "Syntax kontrolü başarısız olmalı"
    print("✓ Syntax kontrolü başarısız (beklenen).")
    
    # Rollback yapıldığını doğrula
    assert result.get("rollback") is not None, "Rollback yapılmadı"
    print("✓ Rollback yapıldı.")
    
    # Dosyanın ilk içeriğine geri döndüğünü doğrula
    with open(calculator_file, 'r', encoding='utf-8') as f:
        final_code = f.read()
    assert final_code == original_code, "Dosya rollback yapılmadı"
    print("✓ Dosya rollback yapıldı.")
    
    # Cleanup backup
    if backup_path.exists():
        backup_timestamp_dir = backup_path.parent
        if backup_timestamp_dir.exists():
            shutil.rmtree(backup_timestamp_dir)
    
    print("\n" + "=" * 70)
    print("TEST B: PASS")
    print("=" * 70)


def test_safe_change_invalid_patch(tmp_path):
    """
    TEST C — Geçersiz Patch veya Uygulama Hatası
    
    Mevcut kodla eşleşmeyen bir patch kullan.
    Uygulamanın hatayı doğru raporladığını doğrula.
    Dosyanın bozulmadığını ve başlangıç içeriğinin korunduğunu doğrula.
    """
    print("\n" + "=" * 70)
    print("TEST C — Geçersiz Patch veya Uygulama Hatası")
    print("=" * 70)
    
    # Setup dosyaları
    calculator_file = tmp_path / "calculator.py"
    original_code = 'def add(a, b):\n    return a - b\n'
    with open(calculator_file, 'w', encoding='utf-8') as f:
        f.write(original_code)
    
    test_file = tmp_path / "test_calculator.py"
    test_code = '''
def test_add():
    assert add(2, 3) == 5
'''
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(test_code)
    
    # SafeChangeManager oluştur
    safe_manager = SafeChangeManager()
    
    # Bileşenlerin project_root'unu geçici alana ayarla
    safe_manager.backup.project_root = tmp_path
    safe_manager.patcher.project_root = tmp_path
    safe_manager.rollback.project_root = tmp_path
    safe_manager.runner.project_root = tmp_path
    
    # Dosya yollarını relative olarak belirle
    relative_calc = "calculator.py"
    relative_test = "test_calculator.py"
    
    # Mevcut kodla eşleşmeyen bir patch kullan
    invalid_old_code = 'def add(a, b):\n    return a * b\n'  # Bu kod dosyada yok
    
    # Değişikliği uygula
    result = safe_manager.apply_patch_and_test(
        file_path=relative_calc,
        old_code=invalid_old_code,
        new_code='def add(a, b):\n    return a + b\n',
        test_file=relative_test
    )
    
    print(f"\nSonuç:")
    print(f"Success: {result.get('success')}")
    print(f"Backup: {result.get('backup')}")
    print(f"Patch: {result.get('patch')}")
    print(f"Error: {result.get('error')}")
    
    # Zorunlu assertion'lar
    assert result.get("success") is False, "Sonuç başarılı olmamalı"
    print("✓ Sonuç başarısız (beklenen).")
    
    # Hata mesajının doğru olduğunu doğrula
    assert result.get("error") is not None, "Hata mesajı yok"
    error_msg = result.get("error")
    assert "old_code" in error_msg.lower() or "bulunamadı" in error_msg.lower(), "Hata mesajı yanlış"
    print(f"✓ Hata mesajı doğru: {error_msg}")
    
    # Dosyanın bozulmadığını doğrula
    with open(calculator_file, 'r', encoding='utf-8') as f:
        final_code = f.read()
    assert final_code == original_code, "Dosya bozuldu"
    print("✓ Dosya bozulmadı.")
    
    # Backup oluşturulmamış olmalı (patch başarısız olduğu için)
    # Not: Mevcut uygulamada backup patch'ten önce oluşturuluyor
    # Bu durumda backup oluşturulmuş olabilir ama rollback yapılmamalı
    if result.get("backup") is not None:
        backup_path = Path(result.get("backup"))
        if backup_path.exists():
            backup_timestamp_dir = backup_path.parent
            if backup_timestamp_dir.exists():
                shutil.rmtree(backup_timestamp_dir)
        print("Not: Backup oluşturuldu (patch öncesi).")
    else:
        print("Not: Backup oluşturulmadı.")
    
    print("\n" + "=" * 70)
    print("TEST C: PASS")
    print("=" * 70)


def test_safe_change_runtime_test_failure_rollback(tmp_path):
    """
    TEST D — Runtime Test Failure ve Gerçek Rollback
    
    tmp_path altında gerçek bir Python dosyası oluştur.
    Başlangıç dosyasının içeriğini kaydet.
    Gerçek SafeChangeManager üzerinden geçerli bir patch uygula.
    Patch sonrasında Python dosyası sözdizimi açısından geçerli olsun.
    Gerçek PythonRunner.run_file() çalışsın.
    Test dosyası gerçekten çalışsın ve başarısız çıksın.
    Test sürecinin başlatıldığını ve sıfırdan farklı exit code ile sonlandığını doğrula.
    Gerçek RollbackManager üzerinden rollback gerçekleşsin.
    Hedef dosyanın içeriğinin başlangıç içeriğine döndüğünü doğrula.
    Backup dosyasının fiziksel olarak mevcut olduğunu ve başlangıç içeriğini taşıdığını doğrula.
    Production sonucunun başarısızlığı doğru raporladığını doğrula.
    """
    print("\n" + "=" * 70)
    print("TEST D — Runtime Test Failure ve Gerçek Rollback")
    print("=" * 70)
    
    # Setup dosyaları
    calculator_file = tmp_path / "calculator.py"
    original_code = 'def add(a, b):\n    return a - b\n'
    with open(calculator_file, 'w', encoding='utf-8') as f:
        f.write(original_code)
    
    test_file = tmp_path / "test_calculator.py"
    test_code = '''
import sys
sys.path.insert(0, '.')
from calculator import add

def test_add():
    assert False  # Bu test her zaman başarısız olacak

if __name__ == "__main__":
    test_add()
'''
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(test_code)
    
    # SafeChangeManager oluştur
    safe_manager = SafeChangeManager()
    
    # Bileşenlerin project_root'unu geçici alana ayarla
    safe_manager.backup.project_root = tmp_path
    safe_manager.patcher.project_root = tmp_path
    safe_manager.rollback.project_root = tmp_path
    safe_manager.runner.project_root = tmp_path
    
    # Dosya yollarını relative olarak belirle
    relative_calc = "calculator.py"
    relative_test = "test_calculator.py"
    
    # Değişikliği uygula (geçerli patch, ancak test başarısız olacak)
    result = safe_manager.apply_patch_and_test(
        file_path=relative_calc,
        old_code=original_code,
        new_code='def add(a, b):\n    return a + b\n',  # Geçerli syntax
        test_file=relative_test
    )
    
    print(f"\nSonuç:")
    print(f"Success: {result.get('success')}")
    print(f"Backup: {result.get('backup')}")
    print(f"Patch: {result.get('patch')}")
    print(f"Syntax: {result.get('syntax')}")
    print(f"Test: {result.get('test')}")
    print(f"Error: {result.get('error')}")
    print(f"Rollback: {result.get('rollback')}")
    
    # Zorunlu assertion'lar
    assert result.get("success") is False, "Sonuç başarılı olmamalı"
    print("✓ Sonuç başarısız (beklenen).")
    
    assert result.get("backup") is not None, "Backup oluşturulmadı"
    backup_path = Path(result.get("backup"))
    assert backup_path.exists(), "Backup dosyası diskte bulunamadı"
    print(f"✓ Backup oluşturuldu: {backup_path}")
    
    # Patch başarılı olduğunu doğrula
    patch_result = result.get("patch")
    assert patch_result is not None, "Patch sonucu yok"
    assert patch_result.get("success") is True, "Patch başarısız olmamalı"
    print("✓ Patch başarılı.")
    
    # Syntax kontrolü başarılı olduğunu doğrula
    assert result.get("syntax") == "OK", "Syntax kontrolü başarısız olmamalı"
    print("✓ Syntax kontrolü başarılı.")
    
    # Test çalıştırıldığını doğrula
    test_result = result.get("test")
    assert test_result is not None, "Test sonucu yok"
    print("✓ Test çalıştırıldı.")
    
    # Test başarısız olduğunu doğrula
    assert test_result.get("success") is False, "Test başarılı olmamalı"
    print("✓ Test başarısız (beklenen).")
    
    # Exit code sıfırdan farklı olduğunu doğrula
    returncode = test_result.get("returncode")
    assert returncode is not None, "Returncode yok"
    assert returncode != 0, "Returncode sıfır olmamalı"
    print(f"✓ Exit code sıfırdan farklı: {returncode}")
    
    # Rollback yapıldığını doğrula
    assert result.get("rollback") is not None, "Rollback yapılmadı"
    print("✓ Rollback yapıldı.")
    
    # Dosyanın ilk içeriğine geri döndüğünü doğrula
    with open(calculator_file, 'r', encoding='utf-8') as f:
        final_code = f.read()
    assert final_code == original_code, "Dosya rollback yapılmadı"
    print("✓ Dosya rollback yapıldı.")
    
    # Backup içeriğinin başlangıç içeriğini taşıdığını doğrula
    with open(backup_path, 'r', encoding='utf-8') as f:
        backup_content = f.read()
    assert backup_content == original_code, "Backup içeriği yanlış"
    print("✓ Backup içeriği doğru.")
    
    # Hata ayrıntılarının kaydedildiğini doğrula
    assert result.get("test_failure_details") is not None, "Hata ayrıntıları kaydedilmedi"
    test_failure_details = result.get("test_failure_details")
    assert "stdout" in test_failure_details, "stdout kaydedilmedi"
    assert "stderr" in test_failure_details, "stderr kaydedilmedi"
    assert "returncode" in test_failure_details, "returncode kaydedilmedi"
    print("✓ Hata ayrıntıları kaydedildi.")
    
    # Cleanup backup
    if backup_path.exists():
        backup_timestamp_dir = backup_path.parent
        if backup_timestamp_dir.exists():
            shutil.rmtree(backup_timestamp_dir)
    
    print("\n" + "=" * 70)
    print("TEST D: PASS")
    print("=" * 70)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
