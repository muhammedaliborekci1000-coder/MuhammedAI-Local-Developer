from pathlib import Path

from app.tools.safe_change_manager import SafeChangeManager
from app.core.config import PROJECT_ROOT


TARGET_FILE = "test_file_security_target.py"

target_path = Path(PROJECT_ROOT) / TARGET_FILE

target_path.write_text(
    '''def hello():
    print("ESKI")
''',
    encoding="utf-8",
)

manager = SafeChangeManager()

print("=" * 60)
print("TEST FILE SECURITY TEST")
print("=" * 60)

result = manager.apply_patch_and_test(
    file_path=TARGET_FILE,
    old_code='print("ESKI")',
    new_code='print("YENI")',
    test_file="olmayan_test.py",
)

print("\nSONUC:")
print(result)

print("\nHEDEF DOSYA:")
print(target_path.read_text(encoding="utf-8"))

if target_path.exists():
    target_path.unlink()

print("\nTEST DOSYASI SILINDI.")

if result["success"]:
    print("\n[HATA] Olmayan test dosyasına rağmen değişiklik yapıldı!")
else:
    print("\n[OK] Olmayan test dosyası nedeniyle işlem engellendi.")

if result["backup"] is None:
    print("[OK] Backup oluşturulmadı.")
else:
    print("[HATA] Backup oluşturuldu!")
