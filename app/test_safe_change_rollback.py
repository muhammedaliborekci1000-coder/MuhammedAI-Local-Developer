from pathlib import Path

from app.tools.safe_change_manager import SafeChangeManager
from app.core.config import PROJECT_ROOT


TEST_FILE = "safe_rollback_test.py"

test_path = Path(PROJECT_ROOT) / TEST_FILE

test_path.write_text(
    '''def hello():
    print("ESKI KOD")
''',
    encoding="utf-8",
)

manager = SafeChangeManager()

print("=" * 60)
print("SAFE CHANGE ROLLBACK TEST")
print("=" * 60)

result = manager.apply_patch_and_test(
    file_path=TEST_FILE,
    old_code='print("ESKI KOD")',
    new_code='print("BOZUK KOD"',
    test_file=TEST_FILE,
)

print("\nSONUC:")
print(result)

print("\nDOSYA ICERIGI ROLLBACK SONRASI:")
print(test_path.read_text(encoding="utf-8"))

if test_path.exists():
    test_path.unlink()

print("\nTEST DOSYASI SILINDI.")
