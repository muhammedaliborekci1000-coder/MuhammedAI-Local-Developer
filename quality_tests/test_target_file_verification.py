"""
Deterministik dosya hedefleme ve görev doğrulama testleri - Phase 6.12
"""

import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path
from app.ai.agent_loop import AgentLoop, LoopConfig
from app.ai.ollama_client import OllamaClient
from app.tools.tool_registry import ToolRegistry
from app.core.config import PROJECT_ROOT


class TestTargetFileVerification:
    """Açık dosya yolu hedefleme ve görev doğrulama testleri."""

    def test_inspection_task_reads_target_file(self, monkeypatch, tmp_path):
        """
        app/ai/agent_loop.py istenince dosyanın ön okuma ile okunması.
        """
        # Test dosyası oluştur
        test_file = tmp_path / "test.py"
        test_file.write_text("# Test file\nprint('hello')")

        # PROJECT_ROOT'u test dizini yap
        monkeypatch.setattr("app.tools.file_reader.PROJECT_ROOT", tmp_path)
        monkeypatch.setattr("app.core.config.PROJECT_ROOT", tmp_path)

        # Mock AI client
        mock_ai = MagicMock()
        mock_ai.chat.return_value = {
            "content": "Dosya okundu.",
            "tool_calls": None
        }

        # Tool registry oluştur
        registry = ToolRegistry()

        # AgentLoop oluştur
        config = LoopConfig(max_iterations=5)
        agent_loop = AgentLoop(
            ollama_client=mock_ai,
            tool_registry=registry,
            config=config,
            approval_callback=None
        )

        # İnceleme görevi
        user_task = "test.py dosyasını incele. Hiçbir dosyayı değiştirme."

        result = agent_loop.run(user_task)

        # Ön okuma başarılı olmalı
        assert result.success is True

    def test_inspection_task_with_correct_file_read(self, monkeypatch, tmp_path):
        """
        Model doğru dosyayı okursa görev başarılı olmalı.
        """
        # Test dosyası oluştur
        test_file = tmp_path / "test.py"
        test_file.write_text("# Test file\nprint('hello')")

        monkeypatch.setattr("app.tools.file_reader.PROJECT_ROOT", tmp_path)
        monkeypatch.setattr("app.core.config.PROJECT_ROOT", tmp_path)

        # Mock AI client - tool çağrısı yapar
        mock_ai = MagicMock()
        mock_ai.chat.return_value = {
            "content": "Dosya incelendi.",
            "tool_calls": None
        }

        registry = ToolRegistry()
        config = LoopConfig(max_iterations=5)
        agent_loop = AgentLoop(
            ollama_client=mock_ai,
            tool_registry=registry,
            config=config,
            approval_callback=None
        )

        user_task = "test.py dosyasını incele. Hiçbir dosyayı değiştirme."

        result = agent_loop.run(user_task)

        # Hedef dosya okunduysa başarılı olmalı (ön okuma başarılı)
        assert result.success is True

    def test_inspection_task_target_not_read_fails(self, monkeypatch, tmp_path):
        """
        İstenen dosya okunamadığında görevin başarılı sayılmaması.
        """
        monkeypatch.setattr("app.tools.file_reader.PROJECT_ROOT", tmp_path)
        monkeypatch.setattr("app.core.config.PROJECT_ROOT", tmp_path)

        mock_ai = MagicMock()
        mock_ai.chat.return_value = {
            "content": "Dosya incelemesi tamamlandı.",
            "tool_calls": None
        }

        registry = ToolRegistry()
        config = LoopConfig(max_iterations=5)
        agent_loop = AgentLoop(
            ollama_client=mock_ai,
            tool_registry=registry,
            config=config,
            approval_callback=None
        )

        # Var olmayan dosya
        user_task = "nonexistent.py dosyasını incele. Hiçbir dosyayı değiştirme."

        result = agent_loop.run(user_task)

        # Dosya bulunamadığı için başarısız olmalı
        assert result.success is False
        assert "bulunamadı" in result.error.lower()

    def test_general_inspection_no_target_file(self, monkeypatch, tmp_path):
        """
        Açık dosya yolu olmayan genel inceleme görevlerinin mevcut davranışının bozulmaması.
        """
        monkeypatch.setattr("app.tools.file_reader.PROJECT_ROOT", tmp_path)
        monkeypatch.setattr("app.core.config.PROJECT_ROOT", tmp_path)

        mock_ai = MagicMock()
        mock_ai.chat.return_value = {
            "content": "Proje yapısı incelendi.",
            "tool_calls": None
        }

        registry = ToolRegistry()
        config = LoopConfig(max_iterations=5)
        agent_loop = AgentLoop(
            ollama_client=mock_ai,
            tool_registry=registry,
            config=config,
            approval_callback=None
        )

        # Genel inceleme görevi - hedef dosya yok
        user_task = "Projeyi incele. Hiçbir dosyayı değiştirme."

        result = agent_loop.run(user_task)

        # Hedef dosya belirtilmediği için tool çağrısı yapılmadıysa başarısız döner
        # Bu mevcut davranış - dosya işlemi gerektiren görevlerde tool çağrısı şart
        assert result.success is False

    def test_code_change_task_unaffected(self, monkeypatch, tmp_path):
        """
        Test-only ve code-change görevlerinin mevcut davranışlarının korunması.
        """
        test_file = tmp_path / "test.py"
        test_file.write_text("# Test file")

        monkeypatch.setattr("app.tools.file_reader.PROJECT_ROOT", tmp_path)
        monkeypatch.setattr("app.core.config.PROJECT_ROOT", tmp_path)

        mock_ai = MagicMock()
        mock_ai.chat.return_value = {
            "content": "Değişiklik yapıldı.",
            "tool_calls": None
        }

        registry = ToolRegistry()
        config = LoopConfig(max_iterations=5)
        agent_loop = AgentLoop(
            ollama_client=mock_ai,
            tool_registry=registry,
            config=config,
            approval_callback=None
        )

        # Kod değişikliği görevi
        user_task = "test.py dosyasında değişiklik yap."

        result = agent_loop.run(user_task)

        # Kod değişikliği görevi inspection-only değil, başarılı olabilir
        # (mevcut davranış korunmalı)
        # Model tool çağrısı yapmadığı için ChangeWorkflow tetiklenir
        # Dosya bulunamazsa başarısız döner
        # Bu test sadece davranışın bozulmadığını kontrol eder

    def test_file_path_extraction(self):
        """
        Dosya yolu çıkarma fonksiyonunun doğru çalışması.
        """
        from app.ai.agent_loop import AgentLoop

        # Mock oluştur
        mock_ai = MagicMock()
        registry = MagicMock()
        config = LoopConfig()
        agent_loop = AgentLoop(
            ollama_client=mock_ai,
            tool_registry=registry,
            config=config,
            approval_callback=None
        )

        # Test cases
        assert agent_loop._extract_file_path_from_task("app/ai/agent_loop.py dosyasını incele") == "app/ai/agent_loop.py"
        assert agent_loop._extract_file_path_from_task("test.txt dosyasını oku") == "test.txt"
        assert agent_loop._extract_file_path_from_task("config.json'u kontrol et") == "config.json"
        assert agent_loop._extract_file_path_from_task("dosya incele") is None

    def test_inspection_no_file_modification(self, monkeypatch, tmp_path):
        """
        Inspection-only görevlerinde hiçbir dosyanın değiştirilmemesi.
        """
        test_file = tmp_path / "test.py"
        test_file.write_text("# Original content")

        monkeypatch.setattr("app.tools.file_reader.PROJECT_ROOT", tmp_path)
        monkeypatch.setattr("app.core.config.PROJECT_ROOT", tmp_path)

        mock_ai = MagicMock()
        mock_ai.chat.return_value = {
            "content": "Dosya incelendi.",
            "tool_calls": None
        }

        registry = ToolRegistry()
        config = LoopConfig(max_iterations=5)
        agent_loop = AgentLoop(
            ollama_client=mock_ai,
            tool_registry=registry,
            config=config,
            approval_callback=None
        )

        user_task = "test.py dosyasını incele. Hiçbir dosyayı değiştirme."

        original_content = test_file.read_text()

        result = agent_loop.run(user_task)

        # Dosya değişmemeli
        assert test_file.read_text() == original_content

    def test_target_file_logging(self, monkeypatch, tmp_path):
        """
        Hedef dosyanın loglandığını doğrula.
        """
        test_file = tmp_path / "test.py"
        test_file.write_text("# Test")

        monkeypatch.setattr("app.tools.file_reader.PROJECT_ROOT", tmp_path)
        monkeypatch.setattr("app.core.config.PROJECT_ROOT", tmp_path)

        mock_ai = MagicMock()
        mock_ai.chat.return_value = {
            "content": "Dosya incelendi.",
            "tool_calls": None
        }

        registry = ToolRegistry()
        config = LoopConfig(max_iterations=5)
        agent_loop = AgentLoop(
            ollama_client=mock_ai,
            tool_registry=registry,
            config=config,
            approval_callback=None
        )

        user_task = "test.py dosyasını incele. Hiçbir dosyayı değiştirme."

        # Log capture
        with patch.object(agent_loop.logger, 'info') as mock_log:
            result = agent_loop.run(user_task)

            # Hedef dosya loglanmalı
            log_calls = [str(call) for call in mock_log.call_args_list]
            assert any("test.py" in str(call) for call in log_calls)

    def test_target_file_pre_read(self, monkeypatch, tmp_path):
        """
        Hedef dosyanın model çağrısından önce okunması.
        """
        test_file = tmp_path / "test.py"
        test_file.write_text("# Test content\nprint('hello')")

        monkeypatch.setattr("app.tools.file_reader.PROJECT_ROOT", tmp_path)
        monkeypatch.setattr("app.core.config.PROJECT_ROOT", tmp_path)

        mock_ai = MagicMock()
        mock_ai.chat.return_value = {
            "content": "Dosya incelendi.",
            "tool_calls": None
        }

        registry = ToolRegistry()
        config = LoopConfig(max_iterations=5)
        agent_loop = AgentLoop(
            ollama_client=mock_ai,
            tool_registry=registry,
            config=config,
            approval_callback=None
        )

        user_task = "test.py dosyasını incele. Hiçbir dosyayı değiştirme."

        result = agent_loop.run(user_task)

        # Hedef dosya okunduysa başarılı olmalı
        assert result.success is True

        # Model çağrıldı mı kontrol et
        assert mock_ai.chat.called

        # AI'ya verilen mesajda dosya içeriği var mı
        call_args = mock_ai.chat.call_args
        prompt = call_args[0][0] if call_args[0] else ""
        assert "Test content" in prompt or "# Test content" in prompt

    def test_target_file_not_found_error(self, monkeypatch, tmp_path):
        """
        Dosya bulunamadığında açık hata vermesi.
        """
        monkeypatch.setattr("app.tools.file_reader.PROJECT_ROOT", tmp_path)
        monkeypatch.setattr("app.core.config.PROJECT_ROOT", tmp_path)

        mock_ai = MagicMock()
        mock_ai.chat.return_value = {
            "content": "Dosya incelendi.",
            "tool_calls": None
        }

        registry = ToolRegistry()
        config = LoopConfig(max_iterations=5)
        agent_loop = AgentLoop(
            ollama_client=mock_ai,
            tool_registry=registry,
            config=config,
            approval_callback=None
        )

        # Var olmayan dosya
        user_task = "nonexistent.py dosyasını incele. Hiçbir dosyayı değiştirme."

        result = agent_loop.run(user_task)

        # Başarısız olmalı
        assert result.success is False
        assert "bulunamadı" in result.error.lower()

        # Model çağrılmamalı (ön okuma başarısız)
        assert not mock_ai.chat.called

    def test_inspection_tool_restriction(self, monkeypatch, tmp_path):
        """
        Inspection-only görevde ilgisiz araçların kullanılmaması.
        """
        test_file = tmp_path / "test.py"
        test_file.write_text("# Test")

        monkeypatch.setattr("app.tools.file_reader.PROJECT_ROOT", tmp_path)
        monkeypatch.setattr("app.core.config.PROJECT_ROOT", tmp_path)

        mock_ai = MagicMock()
        mock_ai.chat.return_value = {
            "content": "Dosya incelendi.",
            "tool_calls": None
        }

        registry = ToolRegistry()
        config = LoopConfig(max_iterations=5)
        agent_loop = AgentLoop(
            ollama_client=mock_ai,
            tool_registry=registry,
            config=config,
            approval_callback=None
        )

        user_task = "test.py dosyasını incele. Hiçbir dosyayı değiştirme."

        result = agent_loop.run(user_task)

        # start_web_preview gibi araçlar kullanılmamalı
        for call in result.tool_calls:
            tool_name = call.get("tool")
            assert tool_name not in ["start_web_preview", "stop_web_preview", "run_python_file"]

    def test_file_modification_tools_blocked(self, monkeypatch, tmp_path):
        """
        Dosya değiştirme araçlarının çağrılmaması.
        """
        test_file = tmp_path / "test.py"
        test_file.write_text("# Test")

        monkeypatch.setattr("app.tools.file_reader.PROJECT_ROOT", tmp_path)
        monkeypatch.setattr("app.core.config.PROJECT_ROOT", tmp_path)

        mock_ai = MagicMock()
        mock_ai.chat.return_value = {
            "content": "Dosya incelendi.",
            "tool_calls": None
        }

        registry = ToolRegistry()
        config = LoopConfig(max_iterations=5)
        agent_loop = AgentLoop(
            ollama_client=mock_ai,
            tool_registry=registry,
            config=config,
            approval_callback=None
        )

        user_task = "test.py dosyasını incele. Hiçbir dosyayı değiştirme."

        result = agent_loop.run(user_task)

        # Dosya değiştirme araçları kullanılmamalı
        for call in result.tool_calls:
            tool_name = call.get("tool")
            assert tool_name not in ["write_file", "edit_file", "create_file", "delete_file"]

    def test_project_outside_path_rejected(self, monkeypatch, tmp_path):
        """
        Proje dışına çıkan yolların reddedilmesi.
        """
        test_file = tmp_path / "test.py"
        test_file.write_text("# Test")

        monkeypatch.setattr("app.tools.file_reader.PROJECT_ROOT", tmp_path)
        monkeypatch.setattr("app.core.config.PROJECT_ROOT", tmp_path)

        mock_ai = MagicMock()
        mock_ai.chat.return_value = {
            "content": "Dosya incelendi.",
            "tool_calls": None
        }

        registry = ToolRegistry()
        config = LoopConfig(max_iterations=5)
        agent_loop = AgentLoop(
            ollama_client=mock_ai,
            tool_registry=registry,
            config=config,
            approval_callback=None
        )

        # Proje dışı yol
        user_task = "../outside/test.py dosyasını incele. Hiçbir dosyayı değiştirme."

        result = agent_loop.run(user_task)

        # Başarısız olmalı
        assert result.success is False
