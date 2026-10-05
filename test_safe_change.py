from app.tools.safe_change_manager import SafeChangeManager


manager = SafeChangeManager()

result = manager.apply_and_test(
    "safe_test.py",
    'print("BOZUK"',
    "safe_test.py",
)

print("SONUÇ:")
print(result)
