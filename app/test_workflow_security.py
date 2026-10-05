from app.tools.change_workflow import ChangeWorkflow


workflow = ChangeWorkflow()

plan = {
    "file": "tests/run_all_tests.py",
    "function": "run_all_tests",
    "problem": "Test sonucu yanlış dönüyor.",
    "change": "Test sonucu dönüşünü düzelt.",
    "old_code": "GEÇERSİZ_TEST_KODU",
    "new_code": "return self.print_summary()",
    "reason": "Test sonucunun main fonksiyonuna aktarılması.",
}


print("=" * 60)
print("CHANGE WORKFLOW SECURITY TEST")
print("=" * 60)


print("\n[TEST 1] Geçersiz plan kontrolü")

validation = workflow.validator.validate(plan)

print(validation)


print("\n[TEST 2] Onaysız değişiklik")

result = workflow.apply_change(
    plan=plan,
    test_file="tests/run_all_tests.py",
    approved=False,
)

print(result)

print("\n[TEST 3] Geçersiz new_code ile güvenlik kontrolü")

invalid_plan = {
    "file": "tests/run_all_tests.py",
    "function": "run_all_tests",
    "problem": "Test amacıyla geçersiz kod.",
    "change": "Geçersiz Python kodu uygulanacak.",
    "old_code": "def run_all_tests(self):",
    "new_code": "def broken(",
    "reason": "Güvenlik testi.",
}

validation = workflow.validator.validate(invalid_plan)

print("VALIDATION:")
print(validation)

result = workflow.apply_change(
    plan=invalid_plan,
    test_file="tests/run_all_tests.py",
    approved=True,
)

print("APPLY RESULT:")
print(result)