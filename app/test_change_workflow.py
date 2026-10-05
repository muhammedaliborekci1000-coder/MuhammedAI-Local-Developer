from app.tools.change_workflow import ChangeWorkflow


workflow = ChangeWorkflow()

problem = """
tests/run_all_tests.py dosyasında bütün 12 test başarılı
olmasına rağmen program [FAIL] Some tests failed diyerek
sonlanıyordu.

Sorunun nedeni run_all_tests() fonksiyonunun
self.print_summary() sonucunu return etmemesiydi.
"""

print("AI DEĞİŞİKLİK PLANI OLUŞTURUYOR...")
print("=" * 60)

plan = workflow.analyze_problem(
    "tests/run_all_tests.py",
    problem,
)

print(plan)
