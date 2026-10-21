from app.tools.safe_change_manager import SafeChangeManager


def test_safe_change():
    """SafeChangeManager testi"""
    manager = SafeChangeManager()

    result = manager.apply_patch_and_test(
        file_path="safe_test.py",
        old_code='print("BOZUK"',
        new_code="safe_test.py",
        test_file="safe_test.py",
    )

    print("SONUÇ:")
    print(result)
