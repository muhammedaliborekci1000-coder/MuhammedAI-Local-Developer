"""
FileReader offset/limit özellikleri için deterministik testler.
"""

import pytest
from pathlib import Path
from app.tools.file_reader import FileReader
from app.core.config import PROJECT_ROOT


class TestFileReader:
    """FileReader offset/limit özelliklerini test eder."""

    def test_backward_compatibility_default_params(self, monkeypatch, tmp_path):
        """
        Eski read(path) çağrısı geriye dönük uyumlu çalışıyor.
        offset=0, limit=None (varsayılan) durumunda string döndürür.
        """
        # Test dosyası oluştur
        test_file = tmp_path / "test.txt"
        test_file.write_text("line1\nline2\nline3\nline4\nline5")

        # FileReader'ı test diziniyle oluştur
        monkeypatch.setattr("app.tools.file_reader.PROJECT_ROOT", tmp_path)
        reader = FileReader(project_root=tmp_path)

        # Eski stil çağrı (sadece path)
        result = reader.read("test.txt")

        # String dönmeli (backward compatibility)
        assert isinstance(result, str)
        assert result == "line1\nline2\nline3\nline4\nline5"

    def test_offset_limit_returns_dict(self, monkeypatch, tmp_path):
        """
        offset veya limit belirtilmişse dict döndürür.
        """
        test_file = tmp_path / "test.txt"
        test_file.write_text("line1\nline2\nline3\nline4\nline5")

        monkeypatch.setattr("app.tools.file_reader.PROJECT_ROOT", tmp_path)
        reader = FileReader(project_root=tmp_path)

        # offset belirtilmiş
        result = reader.read("test.txt", offset=1)
        assert isinstance(result, dict)
        assert "content" in result
        assert "total_lines" in result
        assert "read_lines" in result
        assert "offset" in result
        assert "truncated" in result

        # limit belirtilmiş
        result = reader.read("test.txt", limit=3)
        assert isinstance(result, dict)
        assert result["read_lines"] == 3

    def test_offset_limit_first_three_lines(self, monkeypatch, tmp_path):
        """
        offset=0, limit=3 ilk üç satırı doğru döndürüyor.
        """
        test_file = tmp_path / "test.txt"
        test_file.write_text("line1\nline2\nline3\nline4\nline5")

        monkeypatch.setattr("app.tools.file_reader.PROJECT_ROOT", tmp_path)
        reader = FileReader(project_root=tmp_path)

        result = reader.read("test.txt", offset=0, limit=3)

        assert result["content"] == "line1\nline2\nline3"
        assert result["total_lines"] == 5
        assert result["read_lines"] == 3
        assert result["offset"] == 0
        assert result["truncated"] is True

    def test_offset_limit_next_lines(self, monkeypatch, tmp_path):
        """
        offset=3, limit=3 doğru sonraki satırları döndürüyor.
        """
        test_file = tmp_path / "test.txt"
        test_file.write_text("line1\nline2\nline3\nline4\nline5")

        monkeypatch.setattr("app.tools.file_reader.PROJECT_ROOT", tmp_path)
        reader = FileReader(project_root=tmp_path)

        result = reader.read("test.txt", offset=3, limit=3)

        assert result["content"] == "line4\nline5"
        assert result["total_lines"] == 5
        assert result["read_lines"] == 2
        assert result["offset"] == 3
        assert result["truncated"] is False

    def test_metadata_values_correct(self, monkeypatch, tmp_path):
        """
        total_lines, read_lines, offset ve truncated değerleri doğru.
        """
        test_file = tmp_path / "test.txt"
        test_file.write_text("line1\nline2\nline3\nline4\nline5\nline6\nline7\nline8\nline9\nline10")

        monkeypatch.setattr("app.tools.file_reader.PROJECT_ROOT", tmp_path)
        reader = FileReader(project_root=tmp_path)

        result = reader.read("test.txt", offset=2, limit=5)

        assert result["total_lines"] == 10
        assert result["read_lines"] == 5
        assert result["offset"] == 2
        assert result["truncated"] is True

    def test_offset_beyond_file_end(self, monkeypatch, tmp_path):
        """
        Dosyanın sonunu aşan offset boş sonuç döndürür.
        """
        test_file = tmp_path / "test.txt"
        test_file.write_text("line1\nline2\nline3")

        monkeypatch.setattr("app.tools.file_reader.PROJECT_ROOT", tmp_path)
        reader = FileReader(project_root=tmp_path)

        result = reader.read("test.txt", offset=10, limit=5)

        assert result["content"] == ""
        assert result["total_lines"] == 3
        assert result["read_lines"] == 0
        assert result["offset"] == 10
        assert result["truncated"] is False

    def test_empty_file(self, monkeypatch, tmp_path):
        """
        Boş dosya davranışı belirli ve tutarlı.
        """
        test_file = tmp_path / "test.txt"
        test_file.write_text("")

        monkeypatch.setattr("app.tools.file_reader.PROJECT_ROOT", tmp_path)
        reader = FileReader(project_root=tmp_path)

        # Varsayılan çağrı
        result = reader.read("test.txt")
        assert isinstance(result, str)
        assert result == ""

        # offset/limit çağrısı
        result = reader.read("test.txt", offset=0, limit=10)
        assert result["content"] == ""
        assert result["total_lines"] == 0
        assert result["read_lines"] == 0
        assert result["truncated"] is False

    def test_negative_offset(self, monkeypatch, tmp_path):
        """
        Negatif offset güvenli davranış göstermeli.
        Python slicing negatif offset'i desteklemez, boş sonuç döner.
        """
        test_file = tmp_path / "test.txt"
        test_file.write_text("line1\nline2\nline3")

        monkeypatch.setattr("app.tools.file_reader.PROJECT_ROOT", tmp_path)
        reader = FileReader(project_root=tmp_path)

        # Negatif offset - Python slicing boş sonuç döner
        result = reader.read("test.txt", offset=-1, limit=2)

        # Negatif offset ile slicing boş sonuç döner
        assert result["content"] == ""
        assert result["read_lines"] == 0

    def test_negative_limit(self, monkeypatch, tmp_path):
        """
        Negatif limit güvenli davranış göstermeli.
        Python slicing negatif limit'i destekler (sondan sayar).
        """
        test_file = tmp_path / "test.txt"
        test_file.write_text("line1\nline2\nline3\nline4\nline5")

        monkeypatch.setattr("app.tools.file_reader.PROJECT_ROOT", tmp_path)
        reader = FileReader(project_root=tmp_path)

        # Negatif limit - Python slicing sondan sayar
        result = reader.read("test.txt", offset=0, limit=-2)

        # Son 2 satır hariç
        assert result["content"] == "line1\nline2\nline3"
        assert result["read_lines"] == 3

    def test_tool_schema_compatibility(self, monkeypatch, tmp_path):
        """
        Mevcut read_file tool şeması ile gerçek uygulama aynı parametreleri destekliyor.
        Tool şemasında: relative_path (str), offset (int, default=0), limit (int, default=None)
        """
        test_file = tmp_path / "test.txt"
        test_file.write_text("line1\nline2\nline3")

        monkeypatch.setattr("app.tools.file_reader.PROJECT_ROOT", tmp_path)
        reader = FileReader(project_root=tmp_path)

        # relative_path zorunlu
        with pytest.raises(TypeError):
            reader.read()  # relative_path eksik

        # offset varsayılan 0
        result = reader.read("test.txt")
        assert isinstance(result, str)

        # limit varsayılan None
        result = reader.read("test.txt", offset=0)
        assert isinstance(result, str)

        # offset ve limit birlikte
        result = reader.read("test.txt", offset=0, limit=2)
        assert isinstance(result, dict)
        assert result["read_lines"] == 2

    def test_single_line_file(self, monkeypatch, tmp_path):
        """
        Tek satırlı dosya davranışı.
        """
        test_file = tmp_path / "test.txt"
        test_file.write_text("single line")

        monkeypatch.setattr("app.tools.file_reader.PROJECT_ROOT", tmp_path)
        reader = FileReader(project_root=tmp_path)

        result = reader.read("test.txt", offset=0, limit=10)

        assert result["content"] == "single line"
        assert result["total_lines"] == 1
        assert result["read_lines"] == 1
        assert result["truncated"] is False

    def test_limit_zero(self, monkeypatch, tmp_path):
        """
        limit=0 boş sonuç döndürür.
        """
        test_file = tmp_path / "test.txt"
        test_file.write_text("line1\nline2\nline3")

        monkeypatch.setattr("app.tools.file_reader.PROJECT_ROOT", tmp_path)
        reader = FileReader(project_root=tmp_path)

        result = reader.read("test.txt", offset=0, limit=0)

        assert result["content"] == ""
        assert result["read_lines"] == 0
        assert result["truncated"] is True
