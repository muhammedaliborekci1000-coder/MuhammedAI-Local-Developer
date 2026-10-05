from pathlib import Path

from app.tools.safe_change_manager import SafeChangeManager
from app.core.config import PROJECT_ROOT


TARGET_FILE = "workflow_success_test.py"

target_path = Path(PROJECT_ROOT) / TARGET_FILE

target_path.write_text(
    '''def hello():
    print("ESKI")
    
if __name__ == "__main__":
    hello()
''',
    encoding="utf-8",
)

manager = SafeChangeManager()

print("=" * 60)
print("SUCCESSFUL CHANGE WORKFLOW TEST")
print("=" * 60)

result = manager.apply_patch_and_test(
    file_path=TARGET_FILE,
    old_code='print("ESKI")',
    new_code='print("YENI")',
    test_file=TARGET_FILE,
)

print("\nSONUC:")
print(result)

print("\nDOSYA:")
print(target_path.read_text(encoding="utf-8"))

if target_path.exists():
    target_path.unlink()

print("\nTEST DOSYASI SILINDI.")
