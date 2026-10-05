from app.tools.plan_validator import PlanValidator


validator = PlanValidator()


print("=" * 60)
print("PLAN VALIDATOR TEST")
print("=" * 60)


# TEST 1 — Eksik alan
print("\n[TEST 1] Eksik alan kontrolü")

plan = {
    "file": "tests/run_all_tests.py",
    "function": "run_all_tests",
}

result = validator.validate(plan)

print(result)


# TEST 2 — Olmayan old_code
print("\n[TEST 2] Yanlış old_code kontrolü")

plan = {
    "file": "tests/run_all_tests.py",
    "function": "run_all_tests",
    "problem": "Test sonucu yanlış dönüyor.",
    "change": "return eklenmesi gerekiyor.",
    "old_code": "BU KOD DOSYADA YOK",
    "new_code": "return self.print_summary()",
    "reason": "Sonucu main fonksiyonuna aktarmak."
}

result = validator.validate(plan)

print(result)


# TEST 3 — Aynı old_code/new_code
print("\n[TEST 3] Aynı kod kontrolü")

plan = {
    "file": "tests/run_all_tests.py",
    "function": "run_all_tests",
    "problem": "Test sonucu yanlış dönüyor.",
    "change": "Kodun düzeltilmesi gerekiyor.",
    "old_code": "return self.print_summary()",
    "new_code": "return self.print_summary()",
    "reason": "Test sonucunun doğru dönmesi."
}

result = validator.validate(plan)

print(result)


# TEST 4 — Gerçek mevcut kod
print("\n[TEST 4] Geçerli plan kontrolü")

plan = {
    "file": "tests/run_all_tests.py",
    "function": "run_all_tests",
    "problem": "Test sonucu yanlış dönüyor.",
    "change": "Mevcut kod üzerinde gerekli değişiklik yapılacak.",
    "old_code": "return self.print_summary()",
    "new_code": "return self.print_summary()\n",
    "reason": "Test sonucunun doğru şekilde döndürülmesi."
}

result = validator.validate(plan)

print(result)

print("\n[TEST 5] Geçersiz new_code syntax kontrolü")

invalid_syntax_plan = {
    "file": "tests/run_all_tests.py",
    "function": "run_all_tests",
    "problem": "Test sonucu problemi.",
    "change": "Kod değiştirilecek.",
    "old_code": "def run_all_tests(self):",
    "new_code": "def broken(",
    "reason": "Test amacıyla geçersiz Python kodu.",
}

result = validator.validate(invalid_syntax_plan)

print(result)