"""
PlanValidator whitespace-tolerant matching testleri.
Qwen3 modelinin old_code'u yanlış whitespace ile üretmesi durumunda
güvenli şekilde correction yapabilme yeteneğini test eder.
"""

import pytest
from app.tools.plan_validator import PlanValidator


class TestPlanValidatorWhitespaceMatching:
    """PlanValidator whitespace-tolerant matching testleri."""

    def test_exact_match_succeeds(self):
        """Exact match başarılı olmalı."""
        validator = PlanValidator()
        
        source_code = '''def greet():
    return "Merhaba"
'''
        
        plan = {
            "file": "test.py",
            "function": "greet",
            "problem": "Change greeting",
            "change": "Update return value",
            "old_code": '    return "Merhaba"',
            "new_code": '    return "Merhaba Muhammed"',
            "reason": "Update greeting"
        }
        
        # Mock the reader to return our source code
        validator.reader.read = lambda x: source_code
        
        result = validator.validate(plan)
        
        assert result["valid"] is True
        assert len(result["errors"]) == 0

    def test_indentation_difference_corrected(self):
        """Sadece indentation farkı varsa düzeltilmeli (trailing whitespace normalization)."""
        validator = PlanValidator()
        
        source_code = '''def greet():
    return "Merhaba"
'''
        
        # Model trailing space ekledi (normalization ile düzeltilebilir)
        plan = {
            "file": "test.py",
            "function": "greet",
            "problem": "Change greeting",
            "change": "Update return value",
            "old_code": '    return "Merhaba" ',  # Trailing space
            "new_code": '    return "Merhaba Muhammed"',
            "reason": "Update greeting"
        }
        
        validator.reader.read = lambda x: source_code
        
        result = validator.validate(plan)
        
        assert result["valid"] is True
        assert len(result["errors"]) == 0
        # old_code düzeltilmiş olmalı
        assert plan["old_code"] == '    return "Merhaba"'

    def test_multiple_spaces_normalized(self):
        """Trailing whitespace normalize edilmeli."""
        validator = PlanValidator()
        
        source_code = '''def greet():
    return "Merhaba"
'''
        
        # Model trailing space ekledi
        plan = {
            "file": "test.py",
            "function": "greet",
            "problem": "Change greeting",
            "change": "Update return value",
            "old_code": '    return "Merhaba"  ',  # Trailing spaces
            "new_code": '    return "Merhaba Muhammed"',
            "reason": "Update greeting"
        }
        
        validator.reader.read = lambda x: source_code
        
        result = validator.validate(plan)
        
        assert result["valid"] is True
        assert len(result["errors"]) == 0

    def test_no_match_rejected(self):
        """Hiç eşleşme yoksa reddedilmeli."""
        validator = PlanValidator()
        
        source_code = '''def greet():
    return "Merhaba"
'''
        
        plan = {
            "file": "test.py",
            "function": "greet",
            "problem": "Change greeting",
            "change": "Update return value",
            "old_code": '    return "Hello"',  # Yanlış içerik
            "new_code": '    return "Hello World"',
            "reason": "Update greeting"
        }
        
        validator.reader.read = lambda x: source_code
        
        result = validator.validate(plan)
        
        assert result["valid"] is False
        assert len(result["errors"]) > 0
        assert "bulunamadı" in result["errors"][0]

    def test_multiple_matches_rejected(self):
        """Birden fazla benzer eşleşme varsa reddedilmeli."""
        validator = PlanValidator()
        
        source_code = '''def greet():
    return "Merhaba"
def hello():
    return "Merhaba"
'''
        
        # Normalized match 2 kez bulunuyor
        plan = {
            "file": "test.py",
            "function": "greet",
            "problem": "Change greeting",
            "change": "Update return value",
            "old_code": 'return "Merhaba"',  # Indentation olmadan
            "new_code": 'return "Merhaba Muhammed"',
            "reason": "Update greeting"
        }
        
        validator.reader.read = lambda x: source_code
        
        result = validator.validate(plan)
        
        assert result["valid"] is False
        assert len(result["errors"]) > 0
        assert "belirsiz" in result["errors"][0] or "aday" in result["errors"][0]

    def test_exact_multiple_occurrences_rejected(self):
        """Exact match birden fazla kez varsa reddedilmeli."""
        validator = PlanValidator()
        
        source_code = '''def greet():
    return "Merhaba"
def hello():
    return "Merhaba"
'''
        
        # Exact match 2 kez var
        plan = {
            "file": "test.py",
            "function": "greet",
            "problem": "Change greeting",
            "change": "Update return value",
            "old_code": '    return "Merhaba"',
            "new_code": '    return "Merhaba Muhammed"',
            "reason": "Update greeting"
        }
        
        validator.reader.read = lambda x: source_code
        
        result = validator.validate(plan)
        
        assert result["valid"] is False
        assert len(result["errors"]) > 0
        assert "kez bulundu" in result["errors"][0]

    def test_syntax_check_after_correction(self):
        """
        Normalized correction sonrası syntax kontrolü yapılmalı.
        Değişiklik sonrası oluşan kod geçerli Python syntax'ına sahip olmalı.
        """
        validator = PlanValidator()
        
        source_code = '''def greet():
    return "Merhaba"
'''
        
        plan = {
            "file": "test.py",
            "function": "greet",
            "problem": "Change greeting",
            "change": "Update return value",
            "old_code": '  return "Merhaba"',  # Yanlış indentation
            "new_code": '  return "Merhaba Muhammed"',
            "reason": "Update greeting"
        }
        
        validator.reader.read = lambda x: source_code
        
        result = validator.validate(plan)
        
        assert result["valid"] is True
        # Syntax check passed (no syntax error in errors)

    def test_invalid_syntax_after_change_rejected(self):
        """
        Değişiklik sonrası syntax hatası varsa reddedilmeli.
        """
        validator = PlanValidator()
        
        source_code = '''def greet():
    return "Merhaba"
'''
        
        plan = {
            "file": "test.py",
            "function": "greet",
            "problem": "Change greeting",
            "change": "Update return value",
            "old_code": '    return "Merhaba"',
            "new_code": '    return "Merhaba Muhammed',  # Syntax hatası: missing quote
            "reason": "Update greeting"
        }
        
        validator.reader.read = lambda x: source_code
        
        result = validator.validate(plan)
        
        assert result["valid"] is False
        assert len(result["errors"]) > 0
        assert "syntax" in result["errors"][0].lower()

    def test_same_old_and_new_code_rejected(self):
        """
        old_code ve new_code aynıysa reddedilmeli.
        """
        validator = PlanValidator()
        
        source_code = '''def greet():
    return "Merhaba"
'''
        
        plan = {
            "file": "test.py",
            "function": "greet",
            "problem": "Change greeting",
            "change": "Update return value",
            "old_code": '    return "Merhaba"',
            "new_code": '    return "Merhaba"',  # Aynı
            "reason": "Update greeting"
        }
        
        validator.reader.read = lambda x: source_code
        
        result = validator.validate(plan)
        
        assert result["valid"] is False
        assert len(result["errors"]) > 0
        assert "aynı" in result["errors"][0].lower()

    def test_normalize_whitespace_method(self):
        """
        _normalize_whitespace method'un doğru çalıştığını test et.
        """
        validator = PlanValidator()
        
        # Test 1: Trailing whitespace stripped
        assert validator._normalize_whitespace("hello world  ") == "hello world"
        
        # Test 2: No trailing whitespace
        assert validator._normalize_whitespace("hello world") == "hello world"
        
        # Test 3: Leading whitespace stripped for comparison
        assert validator._normalize_whitespace("    hello world") == "hello world"
        
        # Test 4: Trailing tabs stripped
        assert validator._normalize_whitespace("hello world\t\t") == "hello world"
        
        # Test 5: Multiple spaces collapsed
        assert validator._normalize_whitespace("hello    world") == "hello world"
