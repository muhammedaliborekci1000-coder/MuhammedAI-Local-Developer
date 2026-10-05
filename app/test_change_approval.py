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
print("CHANGE APPROVAL TEST")
print("=" * 60)

result = workflow.apply_change(
    plan=plan,
    test_file="tests/run_all_tests.py",
    approved=False,
)

print(result)
