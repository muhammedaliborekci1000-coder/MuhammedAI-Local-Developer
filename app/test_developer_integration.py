from app.ai.developer_agent import DeveloperAgent
from pathlib import Path
from app.core.config import PROJECT_ROOT
import pytest


@pytest.mark.slow
def test_developer_agent_integration():
    """DeveloperAgent integration testi"""
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
        agent = DeveloperAgent()

        print("=" * 60)
        print("DEVELOPER AGENT FULL INTEGRATION TEST")
        print("=" * 60)


        # ============================================================
        # TEST 1 - Dosya analizi
        # ============================================================

        print("\n[TEST 1] Dosya analizi")

        result = agent.analyze_file(
            str(test_file.relative_to(PROJECT_ROOT))
        )

        print(result)


        # ============================================================
        # TEST 2 - Syntax hata taraması
        # ============================================================

        print("\n[TEST 2] Syntax hata taraması")

        result = agent.detect_errors()

        print(result)


        # ============================================================
        # TEST 3 - Kod arama
        # ============================================================

        print("\n[TEST 3] Kod arama")

        result = agent.search_code(
            "run_all_tests"
        )

        print(result)


        # ============================================================
        # TEST 4 - Çalıştır ve analiz et
        # ============================================================

        print("\n[TEST 4] Program çalıştırma ve analiz")

        result = agent.run_and_analyze(
            str(test_file.relative_to(PROJECT_ROOT))
        )

        print(result)


        # ============================================================
        # TEST 5 - AI değişiklik planı
        # ============================================================

        print("\n[TEST 5] AI değişiklik planı")

        plan_result = agent.create_change_plan(
            str(test_file.relative_to(PROJECT_ROOT)),
            (
                "Test programı çalıştırıldığında tüm testler "
                "başarılı olmasına rağmen yanlış exit code "
                "döndürmesi problemi."
            ),
        )

        print(plan_result)


        # ============================================================
        # TEST 6 - Validator sonucu
        # ============================================================

        print("\n[TEST 6] Plan validator sonucu")

        validation = plan_result.get(
            "validation",
            {},
        )

        print(validation)


        # ============================================================
        # TEST 7 - ONAYSIZ uygulama
        # ============================================================

        print("\n[TEST 7] Onaysız değişiklik")

        plan = plan_result.get(
            "plan",
            {},
        )

        result = agent.apply_change(
            plan=plan,
            test_file=str(test_file.relative_to(PROJECT_ROOT)),
            approved=False,
        )

        print(result)


        print("\n" + "=" * 60)
        print("INTEGRATION TEST TAMAMLANDI")
        print("=" * 60)

    finally:
        # Temizlik
        if workspace.exists():
            shutil.rmtree(workspace)
