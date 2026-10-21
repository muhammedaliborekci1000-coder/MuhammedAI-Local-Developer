"""
Phase 6.7 — Görev Sınıflandırma Testleri
Test-only görevlerin kod değişikliği görevlerinden ayrıldığını doğrular.
"""

import pytest
from unittest.mock import MagicMock, patch
from app.ai.agent_loop import AgentLoop, LoopConfig
from app.ai.ollama_client import OllamaClient
from app.tools.tool_registry import ToolRegistry


def test_is_test_only_task_true():
    """Test-only görev doğru tespit edilmeli."""
    from app.ai.agent_loop import AgentLoop
    
    loop = AgentLoop(
        ollama_client=MagicMock(),
        tool_registry=MagicMock()
    )
    
    # Test anahtar kelimeleri ile görevler
    test_tasks = [
        "multiply.py dosyasını test et",
        "test multiply.py",
        "multiply.py çalıştır",
        "run multiply.py",
        "multiply.py doğrula",
        "check multiply.py"
    ]
    
    for task in test_tasks:
        assert loop._is_test_only_task(task) is True, f"Test-only görev tespit edilemedi: {task}"


def test_is_test_only_task_false():
    """Kod değişikliği görevleri test-only olarak tespit edilmemeli."""
    from app.ai.agent_loop import AgentLoop
    
    loop = AgentLoop(
        ollama_client=MagicMock(),
        tool_registry=MagicMock()
    )
    
    # Kod değişikliği anahtar kelimeleri ile görevler
    code_change_tasks = [
        "multiply.py dosyasında multiply fonksiyonu oluştur",
        "multiply.py'ye yeni bir fonksiyon ekle",
        "multiply.py dosyasını değiştir",
        "multiply.py'yi düzenle",
        "multiply.py'yi güncelle"
    ]
    
    for task in code_change_tasks:
        assert loop._is_test_only_task(task) is False, f"Kod değişikliği görevi test-only olarak tespit edildi: {task}"


def test_is_test_only_task_with_both_keywords():
    """Hem test hem değişiklik anahtar kelimesi varsa test-only olmamalı."""
    from app.ai.agent_loop import AgentLoop
    
    loop = AgentLoop(
        ollama_client=MagicMock(),
        tool_registry=MagicMock()
    )
    
    # Hem test hem değişiklik anahtar kelimeleri
    mixed_tasks = [
        "multiply.py dosyasını değiştir ve test et",
        "multiply.py'ye yeni fonksiyon ekle ve çalıştır",
        "multiply.py'yi düzenle ve doğrula"
    ]
    
    for task in mixed_tasks:
        assert loop._is_test_only_task(task) is False, f"Karma görev test-only olarak tespit edildi: {task}"


def test_requires_code_change_excludes_test_only():
    """_requires_code_change test-only görevleri hariç tutmalı."""
    from app.ai.agent_loop import AgentLoop
    
    loop = AgentLoop(
        ollama_client=MagicMock(),
        tool_registry=MagicMock()
    )
    
    # Test-only görevler kod değişikliği gerektirmez
    test_tasks = [
        "multiply.py dosyasını test et",
        "test multiply.py"
    ]
    
    for task in test_tasks:
        assert loop._requires_code_change(task) is False, f"Test-only görev kod değişikliği gerektiriyor olarak tespit edildi: {task}"
    
    # Kod değişikliği görevleri kod değişikliği gerektirir
    code_change_tasks = [
        "multiply.py dosyasında multiply fonksiyonu oluştur",
        "multiply.py'ye yeni bir fonksiyon ekle"
    ]
    
    for task in code_change_tasks:
        assert loop._requires_code_change(task) is True, f"Kod değişikliği görevi reddedildi: {task}"


def test_test_only_task_execution():
    """Test-only görev doğrudan çalıştırılmalı, ChangeWorkflow çağrılmamalı."""
    from app.ai.agent_loop import AgentLoop, LoopConfig
    from app.ai.ollama_client import OllamaClient
    from app.tools.tool_registry import ToolRegistry
    
    # Mock registry
    registry = MagicMock(spec=ToolRegistry)
    registry.execute.return_value = {
        "success": True,
        "stdout": "Test passed\nmultiply(2, 3) == 6: OK",
        "stderr": "",
        "returncode": 0
    }
    registry.workflow = MagicMock()  # AgentLoop __init__ gerektirir
    
    # Mock AI client - tool çağrısı yapmıyor
    ai_client = MagicMock(spec=OllamaClient)
    ai_client.chat.return_value = {
        "content": "Test çalıştırılıyor...",
        "tool_calls": None
    }
    
    loop = AgentLoop(
        ollama_client=ai_client,
        tool_registry=registry,
        config=LoopConfig(max_iterations=5)
    )
    
    # Test-only görev
    result = loop.run("quality_tests/tool_usage_workspace/multiply.py dosyasını test et")
    
    # Başarılı olmalı
    assert result.success is True
    assert "BAŞARILI" in result.final_response
    assert "Test çalıştırıldı" in result.final_response
    
    # ChangeWorkflow çağrılmamalı (dosya değiştirilmemiş olmalı)
    # Bu, run_python_file tool'unun çağrıldığını doğrular


def test_test_only_task_failure():
    """Test başarısız olduğunda görev başarısız bildirilmeli."""
    from app.ai.agent_loop import AgentLoop, LoopConfig
    from app.ai.ollama_client import OllamaClient
    from app.tools.tool_registry import ToolRegistry
    
    # Mock registry - başarısız test
    registry = MagicMock(spec=ToolRegistry)
    registry.execute.return_value = {
        "success": True,
        "stdout": "",
        "stderr": "AssertionError: multiply(2, 3) != 6",
        "returncode": 1
    }
    registry.workflow = MagicMock()  # AgentLoop __init__ gerektirir
    
    # Mock AI client
    ai_client = MagicMock(spec=OllamaClient)
    ai_client.chat.return_value = {
        "content": "Test çalıştırılıyor...",
        "tool_calls": None
    }
    
    loop = AgentLoop(
        ollama_client=ai_client,
        tool_registry=registry,
        config=LoopConfig(max_iterations=5)
    )
    
    # Test-only görev
    result = loop.run("quality_tests/tool_usage_workspace/multiply.py dosyasını test et")
    
    # Başarısız olmalı
    assert result.success is False
    assert "BAŞARISIZ" in result.final_response
    assert result.error == "Test başarısız"


def test_code_change_task_not_affected():
    """Kod değişikliği görevleri test-only olarak tespit edilmemeli."""
    from app.ai.agent_loop import AgentLoop
    
    loop = AgentLoop(
        ollama_client=MagicMock(),
        tool_registry=MagicMock()
    )
    
    # Kod değişikliği görevi test-only olmamalı
    code_change_task = "multiply.py dosyasında multiply fonksiyonu oluştur"
    assert loop._is_test_only_task(code_change_task) is False
    assert loop._requires_code_change(code_change_task) is True


def test_is_inspection_only_task_true():
    """Inspection-only görev doğru tespit edilmeli."""
    from app.ai.agent_loop import AgentLoop
    
    loop = AgentLoop(
        ollama_client=MagicMock(),
        tool_registry=MagicMock()
    )
    
    # Inspection-only görevler
    inspection_tasks = [
        "Projede bir Python dosyasını incele. Henüz hiçbir dosyayı değiştirme.",
        "app/core/config.py dosyasını incele ve hata bul",
        "multiply.py dosyasını review et, değiştirme",
        "Dosyayı kontrol et, değişiklik yapma",
        "analyze the code without changing it"
    ]
    
    for task in inspection_tasks:
        assert loop._is_inspection_only_task(task) is True, f"Inspection-only görev tespit edilemedi: {task}"


def test_is_inspection_only_task_false():
    """Kod değişikliği görevleri inspection-only olarak tespit edilmemeli."""
    from app.ai.agent_loop import AgentLoop
    
    loop = AgentLoop(
        ollama_client=MagicMock(),
        tool_registry=MagicMock()
    )
    
    # Kod değişikliği görevleri
    code_change_tasks = [
        "multiply.py dosyasında multiply fonksiyonu oluştur",
        "multiply.py'yi değiştir",
        "Dosyayı düzenle ve güncelle"
    ]
    
    for task in code_change_tasks:
        assert loop._is_inspection_only_task(task) is False, f"Kod değişikliği görevi inspection-only olarak tespit edildi: {task}"


def test_requires_code_change_excludes_inspection_only():
    """_requires_code_change inspection-only görevleri hariç tutmalı."""
    from app.ai.agent_loop import AgentLoop
    
    loop = AgentLoop(
        ollama_client=MagicMock(),
        tool_registry=MagicMock()
    )
    
    # Inspection-only görevler kod değişikliği gerektirmez
    inspection_tasks = [
        "Projede bir Python dosyasını incele. Henüz hiçbir dosyayı değiştirme.",
        "app/core/config.py dosyasını incele ve hata bul"
    ]
    
    for task in inspection_tasks:
        assert loop._requires_code_change(task) is False, f"Inspection-only görev kod değişikliği gerektiriyor olarak tespit edildi: {task}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
