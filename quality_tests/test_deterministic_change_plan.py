"""
Deterministik değişiklik planı testleri - Phase 6.16
Fallback plan oluşturucunun açık string replacement talimatları için
deterministik çalışmasını doğrular.
"""

import pytest
from app.tools.change_planner import ChangePlanner
from pathlib import Path


class TestDeterministicChangePlan:
    """Deterministik fallback plan oluşturma testleri."""

    def test_fallback_plan_string_replacement_turkish(self, tmp_path, monkeypatch):
        """
        Türkçe 'X' yerine 'Y' formatında açık replacement talimatı
        için deterministik plan oluşturur.
        """
        # Test dosyası oluştur
        test_file = tmp_path / "test.py"
        test_file.write_text("# Test dosyası\ndef hello():\n    return 'world'\n")
        
        # PROJECT_ROOT'u test dizini yap
        monkeypatch.setattr("app.tools.file_reader.PROJECT_ROOT", tmp_path)
        monkeypatch.setattr("app.core.config.PROJECT_ROOT", tmp_path)
        
        planner = ChangePlanner()
        
        # Türkçe replacement talimatı
        problem = "hello fonksiyonunda 'world' yerine 'universe' döndür"
        
        plan = planner._create_fallback_plan(
            file_path="test.py",
            problem=problem,
            source_code=test_file.read_text()
        )
        
        # Plan doğrulaması
        assert plan["file"] == "test.py"
        assert plan["function"] == "hello"
        assert "'world'" in plan["old_code"]
        assert "'universe'" in plan["new_code"]
        assert plan["old_code"] != plan["new_code"]
        assert "return 'universe'" in plan["new_code"]

    def test_fallback_plan_string_replacement_english(self, tmp_path, monkeypatch):
        """
        İngilizce replace 'X' with 'Y' formatında açık replacement talimatı
        için deterministik plan oluşturur.
        """
        # Test dosyası oluştur
        test_file = tmp_path / "test.py"
        test_file.write_text("# Test dosyası\ndef hello():\n    return 'world'\n")
        
        # PROJECT_ROOT'u test dizini yap
        monkeypatch.setattr("app.tools.file_reader.PROJECT_ROOT", tmp_path)
        monkeypatch.setattr("app.core.config.PROJECT_ROOT", tmp_path)
        
        planner = ChangePlanner()
        
        # İngilizce replacement talimatı
        problem = "replace 'world' with 'universe' in hello function"
        
        plan = planner._create_fallback_plan(
            file_path="test.py",
            problem=problem,
            source_code=test_file.read_text()
        )
        
        # Plan doğrulaması
        assert plan["file"] == "test.py"
        assert "'world'" in plan["old_code"]
        assert "'universe'" in plan["new_code"]
        assert plan["old_code"] != plan["new_code"]

    def test_fallback_plan_target_not_found_safe(self, tmp_path, monkeypatch):
        """
        Hedef string kaynak kodda bulunmadığında güvenli olarak
        aynı kodu kullanır (değişiklik yapmaz).
        """
        # Test dosyası oluştur
        test_file = tmp_path / "test.py"
        test_file.write_text("# Test dosyası\ndef hello():\n    return 'world'\n")
        
        # PROJECT_ROOT'u test dizini yap
        monkeypatch.setattr("app.tools.file_reader.PROJECT_ROOT", tmp_path)
        monkeypatch.setattr("app.core.config.PROJECT_ROOT", tmp_path)
        
        planner = ChangePlanner()
        
        # Kaynak kodda bulunmayan string
        problem = "hello fonksiyonunda 'mars' yerine 'universe' döndür"
        
        plan = planner._create_fallback_plan(
            file_path="test.py",
            problem=problem,
            source_code=test_file.read_text()
        )
        
        # Plan doğrulaması - güvenli olarak aynı kod
        assert plan["old_code"] == plan["new_code"]
        assert plan["old_code"] == test_file.read_text()

    def test_fallback_plan_no_replacement_instruction(self, tmp_path, monkeypatch):
        """
        Açık replacement talimatı olmadığında güvenli olarak
        aynı kodu kullanır.
        """
        # Test dosyası oluştur
        test_file = tmp_path / "test.py"
        test_file.write_text("# Test dosyası\ndef hello():\n    return 'world'\n")
        
        # PROJECT_ROOT'u test dizini yap
        monkeypatch.setattr("app.tools.file_reader.PROJECT_ROOT", tmp_path)
        monkeypatch.setattr("app.core.config.PROJECT_ROOT", tmp_path)
        
        planner = ChangePlanner()
        
        # Açık replacement talimatı yok
        problem = "hello fonksiyonunu düzelt"
        
        plan = planner._create_fallback_plan(
            file_path="test.py",
            problem=problem,
            source_code=test_file.read_text()
        )
        
        # Plan doğrulaması - güvenli olarak aynı kod
        assert plan["old_code"] == plan["new_code"]
        assert plan["old_code"] == test_file.read_text()

    def test_fallback_plan_empty_file(self, tmp_path, monkeypatch):
        """
        Boş dosya için güvenli placeholder plan oluşturur.
        """
        # Test dosyası oluştur
        test_file = tmp_path / "test.py"
        test_file.write_text("")
        
        # PROJECT_ROOT'u test dizini yap
        monkeypatch.setattr("app.tools.file_reader.PROJECT_ROOT", tmp_path)
        monkeypatch.setattr("app.core.config.PROJECT_ROOT", tmp_path)
        
        planner = ChangePlanner()
        
        problem = "multiply fonksiyonu oluştur"
        
        plan = planner._create_fallback_plan(
            file_path="test.py",
            problem=problem,
            source_code=""
        )
        
        # Plan doğrulaması
        assert plan["old_code"] == ""
        assert "def multiply" in plan["new_code"] or "TODO" in plan["new_code"]

    def test_fallback_plan_preserves_whitespace(self, tmp_path, monkeypatch):
        """
        Whitespace'ı koruyarak doğru old_code oluşturur.
        """
        # Test dosyası oluştur
        test_file = tmp_path / "test.py"
        test_file.write_text("# Test dosyası\ndef hello():\n    return 'world'\n")
        
        # PROJECT_ROOT'u test dizini yap
        monkeypatch.setattr("app.tools.file_reader.PROJECT_ROOT", tmp_path)
        monkeypatch.setattr("app.core.config.PROJECT_ROOT", tmp_path)
        
        planner = ChangePlanner()
        
        problem = "hello fonksiyonunda 'world' yerine 'universe' döndür"
        
        plan = planner._create_fallback_plan(
            file_path="test.py",
            problem=problem,
            source_code=test_file.read_text()
        )
        
        # Whitespace koruma doğrulaması
        assert "    return 'world'" in plan["old_code"]
        assert "    return 'universe'" in plan["new_code"]
