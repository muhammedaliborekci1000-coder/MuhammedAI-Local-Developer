import pytest
from app.tools.change_workflow import ChangeWorkflow
from pathlib import Path
from app.core.config import PROJECT_ROOT


@pytest.mark.slow
def test_change_workflow_analysis():
    """ChangeWorkflow analyze_problem testi"""
    import tempfile
    import shutil

    # Geçici workspace oluştur
    workspace = PROJECT_ROOT / "quality_tests" / "temp_test_workspace"
    workspace.mkdir(parents=True, exist_ok=True)

    # Örnek test dosyası oluştur
    test_file = workspace / "run_all_tests.py"
    test_content = '''
class TestRunner:
    def __init__(self):
        self.tests_passed = 0
        self.tests_failed = 0

    def run_all_tests(self):
        """Tüm testleri çalıştır"""
        self.tests_passed = 12
        self.tests_failed = 0
        self.print_summary()
        # BUG: return etmiyor!

    def print_summary(self):
        """Sonuç özeti yazdır"""
        if self.tests_failed == 0:
            print("[FAIL] Some tests failed")  # BUG: Yanlış mesaj
        else:
            print("[PASS] All tests passed")

if __name__ == "__main__":
    runner = TestRunner()
    runner.run_all_tests()
'''
    test_file.write_text(test_content, encoding='utf-8')

    try:
        workflow = ChangeWorkflow()

        problem = """
run_all_tests.py dosyasında bütün 12 test başarılı
olmasına rağmen program [FAIL] Some tests failed diyerek
sonlanıyordu.

Sorunun nedeni run_all_tests() fonksiyonunun
self.print_summary() sonucunu return etmemesiydi.
"""

        print("AI DEĞİŞİKLİK PLANI OLUŞTURUYOR...")
        print("=" * 60)

        plan = workflow.analyze_problem(
            str(test_file.relative_to(PROJECT_ROOT)),
            problem,
        )

        print(plan)

    finally:
        # Temizlik
        if workspace.exists():
            shutil.rmtree(workspace)
