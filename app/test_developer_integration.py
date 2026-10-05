from app.ai.developer_agent import DeveloperAgent


agent = DeveloperAgent()

print("=" * 60)
print("DEVELOPER AGENT FULL INTEGRATION TEST")
print("=" * 60)


# ============================================================
# TEST 1 - Dosya analizi
# ============================================================

print("\n[TEST 1] Dosya analizi")

result = agent.analyze_file(
    "tests/run_all_tests.py"
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
    "tests/run_all_tests.py"
)

print(result)


# ============================================================
# TEST 5 - AI değişiklik planı
# ============================================================

print("\n[TEST 5] AI değişiklik planı")

plan_result = agent.create_change_plan(
    "tests/run_all_tests.py",
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
    test_file="tests/run_all_tests.py",
    approved=False,
)

print(result)


print("\n" + "=" * 60)
print("INTEGRATION TEST TAMAMLANDI")
print("=" * 60)
