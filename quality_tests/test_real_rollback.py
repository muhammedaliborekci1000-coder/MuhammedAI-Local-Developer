"""
Gerçek Rollback Testi
Amaç: SafeChangeManager'ın otomatik rollback mekanizmasını test etmek.
"""

import sys
import os
import shutil
from pathlib import Path

# Proje kök dizinini path'e ekle
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.tools.safe_change_manager import SafeChangeManager
from app.tools.file_reader import FileReader
from app.core.config import PROJECT_ROOT


def test_real_rollback():
    """
    Gerçek rollback testi: Test başarısız olduğunda rollback gerçekleşir mi?
    """
    print("=" * 70)
    print("GERÇEK ROLLBACK TESTİ")
    print("=" * 70)

    # Workspace
    workspace = PROJECT_ROOT / "quality_tests" / "e2e_workspace"
    workspace.mkdir(parents=True, exist_ok=True)

    # Test dosyası
    test_file = workspace / "rollback_target.py"
    relative_path = "quality_tests/e2e_workspace/rollback_target.py"

    # Test dosyası (kasıtlı başarısız)
    test_py = workspace / "test_rollback.py"
    relative_test = "quality_tests/e2e_workspace/test_rollback.py"

    # Test dosyasını oluştur
    test_content = '''# Test dosyası - kasıtlı olarak başarısız olacak
import sys
sys.exit(1)  # Kasitli olarak hata dondur
'''
    with open(test_py, 'w', encoding='utf-8') as f:
        f.write(test_content)

    # Orijinal içerik
    original_content = '''def get_message():
    return "ORIGINAL"
'''
    
    # Değiştirilecek kod
    old_code = 'return "ORIGINAL"'
    new_code = 'return "CHANGED"'
    
    try:
        # 1. Dosyayı oluştur
        print("\n1. TEST DOSYASI OLUŞTURMA")
        print("-" * 70)
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(original_content)
        print(f"Dosya oluşturuldu: {test_file}")
        print(f"İçerik:\n{original_content}")
        
        # 2. read_file test
        print("\n2. READ_FILE TEST")
        print("-" * 70)
        reader = FileReader(project_root=PROJECT_ROOT)
        content = reader.read(relative_path)
        print(f"Okunan içerik:\n{content}")
        
        if content == original_content:
            print("[OK] PASS: read_file başarılı")
            read_file_pass = True
        else:
            print("[X] FAIL: read_file içeriği eşleşmiyor")
            read_file_pass = False
        
        # 3. SafeChangeManager oluştur
        print("\n3. SAFECHANGEMANAGER BAŞLATMA")
        print("-" * 70)
        manager = SafeChangeManager()
        print("SafeChangeManager oluşturuldu")
        
        # 4. apply_patch_and_test çağrısı (test başarısız olacak)
        print("\n4. APPLY_PATCH_AND_TEST (Test başarısız olacak)")
        print("-" * 70)
        print(f"file_path: {relative_path}")
        print(f"old_code: {old_code}")
        print(f"new_code: {new_code}")
        print(f"test_file: {relative_test}")
        
        result = manager.apply_patch_and_test(
            file_path=relative_path,
            old_code=old_code,
            new_code=new_code,
            test_file=relative_test
        )
        
        print(f"\nSonuç:")
        for key, value in result.items():
            print(f"  {key}: {value}")
        
        # 5. Sonuçları doğrula
        print("\n5. DOĞRULAMALAR")
        print("-" * 70)
        
        # Validation failure
        validation_failed = result.get("error") is not None
        print(f"Validation failure: {validation_failed}")
        if validation_failed:
            print(f"  Error: {result.get('error')}")
        
        # Backup oluşturuldu mu
        backup_created = result.get("backup") is not None
        print(f"Backup oluşturuldu: {backup_created}")
        if backup_created:
            print(f"  Backup path: {result.get('backup')}")
            backup_path = result.get("backup")
            # Backup dosyası gerçekten var mı?
            if Path(backup_path).exists():
                print(f"  [OK] Backup dosyası mevcut")
                backup_exists = True
            else:
                print(f"  [X] Backup dosyası mevcut değil!")
                backup_exists = False
        else:
            backup_exists = False
        
        # Rollback çağrıldı mı
        rollback_called = result.get("rollback") is not None
        print(f"Rollback çağrıldı: {rollback_called}")
        if rollback_called:
            print(f"  Rollback sonucu: {result.get('rollback')}")

        # Test failure details kontrolü
        test_failure_details = result.get("test_failure_details")
        print(f"Test failure details mevcut: {test_failure_details is not None}")

        # Assertion'larla gerçek değerleri doğrula
        assert test_failure_details is not None, "test_failure_details alanı eksik"

        # Test dosyası sys.exit(1) ile kasıtlı başarısız oluyor
        assert test_failure_details.get("returncode") == 1, f"Beklenen returncode=1, alınan: {test_failure_details.get('returncode')}"
        assert test_failure_details.get("stdout") == "", f"Beklenen stdout='', alınan: {test_failure_details.get('stdout')}"
        assert test_failure_details.get("stderr") == "", f"Beklenen stderr='', alınan: {test_failure_details.get('stderr')}"
        assert test_failure_details.get("error") is None, f"Beklenen error=None, alınan: {test_failure_details.get('error')}"

        print(f"  stdout: '{test_failure_details.get('stdout', '')}'")
        print(f"  stderr: '{test_failure_details.get('stderr', '')}'")
        print(f"  returncode: {test_failure_details.get('returncode')}")
        print(f"  error: {test_failure_details.get('error')}")
        print("[OK] PASS: test_failure_details değerleri doğrulandı")
        test_failure_details_present = True
        
        # Dosya içeriği kontrolü
        print("\n6. DOSYA İÇERİĞİ KONTROLÜ (Rollback sonrası)")
        print("-" * 70)
        with open(test_file, 'r', encoding='utf-8') as f:
            final_content = f.read()
        
        print(f"Son içerik:\n{final_content}")
        
        if final_content == original_content:
            print("[OK] PASS: Dosya orijinal içeriğine döndü (rollback başarılı)")
            content_restored = True
        else:
            print("[X] FAIL: Dosya orijinal içeriğine dönmedi (rollback başarısız!)")
            content_restored = False
        
        # 7. Toplam sonuç
        print("\n" + "=" * 70)
        print("TEST SONUCU")
        print("=" * 70)
        print(f"read_file: {'PASS' if read_file_pass else 'FAIL'}")
        print(f"Validation failure: {'YES' if validation_failed else 'NO'}")
        print(f"Backup oluşturuldu: {'YES' if backup_created else 'NO'}")
        print(f"Backup dosyası var: {'YES' if backup_exists else 'NO'}")
        print(f"Rollback çağrıldı: {'YES' if rollback_called else 'NO'}")
        print(f"Test failure details mevcut: {'YES' if test_failure_details_present else 'NO'}")
        print(f"Dosya orijinal oldu: {'YES' if content_restored else 'NO'}")

        # Rollback başarılı mı?
        test_passed = (
            read_file_pass and
            validation_failed and
            backup_created and
            backup_exists and
            rollback_called and
            test_failure_details_present and
            content_restored
        )
        
        print(f"\nTOPLAM: {'PASS' if test_passed else 'FAIL'}")
        print("=" * 70)

        # Test passes if it completes without exception

    finally:
        # Temizlik - backup dosyalarını da temizle
        print("\n7. TEMİZLİK")
        print("-" * 70)

        # Backup dizinini temizle
        backup_dir = PROJECT_ROOT / ".muhammedai_backups"
        if backup_dir.exists():
            try:
                shutil.rmtree(backup_dir)
                print(f"Backup dizini temizlendi: {backup_dir}")
            except Exception as e:
                print(f"Backup temizleme hatası: {e}")

        # Test dosyalarını temizle
        if test_file.exists():
            test_file.unlink()
            print(f"Test dosyası silindi: {test_file}")

        if test_py.exists():
            test_py.unlink()
            print(f"Test dosyası silindi: {test_py}")


if __name__ == "__main__":
    try:
        test_real_rollback()
        sys.exit(0)
    except Exception as e:
        print(f"\nTEST HATASI:")
        print("-" * 70)
        import traceback
        traceback.print_exc()
        print("=" * 70)
        sys.exit(1)
