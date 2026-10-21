"""
Phase 6.9 — Inspection-Only Görev Doğrulama Testleri
Inspection-only görevlerin doğru sınıflandırıldığını ve dosyaların değiştirilmediğini doğrular.
"""

import pytest
from unittest.mock import MagicMock, patch
from app.ai.agent_loop import AgentLoop, LoopConfig
from app.ai.ollama_client import OllamaClient
from app.tools.tool_registry import ToolRegistry


def test_inspection_task_classification():
    """Inspection-only görev doğru sınıflandırılmalı."""
    from app.ai.agent_loop import AgentLoop
    
    loop = AgentLoop(
        ollama_client=MagicMock(),
        tool_registry=MagicMock()
    )
    
    # Inspection-only görev
    task = "Projede bir Python dosyasını incele. Henüz hiçbir dosyayı değiştirme."
    
    assert loop._is_inspection_only_task(task) is True
    assert loop._requires_code_change(task) is False
    assert loop._is_test_only_task(task) is False


def test_inspection_task_no_change_workflow():
    """Inspection-only görevde ChangeWorkflow çağrılmamalı."""
    from app.ai.agent_loop import AgentLoop, LoopConfig
    from app.ai.ollama_client import OllamaClient
    from app.tools.tool_registry import ToolRegistry
    from unittest.mock import patch
    from app.ai.tool_parser import ToolCall, ParseResult

    # Mock registry
    registry = MagicMock(spec=ToolRegistry)
    registry.workflow = MagicMock()
    registry.execute.return_value = {
        "success": True,
        "content": "Dosya içeriği okundu"
    }

    # Mock AI client - dosyayı okur (tool çağrısı yapar)
    ai_client = MagicMock(spec=OllamaClient)
    ai_client.chat.return_value = {
        "content": "read_file aracını kullanıyorum",
        "tool_calls": None
    }

    loop = AgentLoop(
        ollama_client=ai_client,
        tool_registry=registry,
        config=LoopConfig(max_iterations=3)
    )

    # Parser mock - tool çağrısı döndür
    with patch.object(loop.parser, 'parse') as mock_parse:
        mock_parse.return_value = ParseResult(
            success=True,
            tool_calls=[ToolCall(name="read_file", arguments={"relative_path": "app/core/config.py"}, raw_text="")],
            raw_response=""
        )

        # Inspection-only görev
        result = loop.run("app/core/config.py dosyasını incele, değiştirme")

    # Sonuç başarılı olmalı (hedef dosya okundu)
    assert result.success is True

    # ChangeWorkflow.create_plan çağrılmamalı
    registry.workflow.create_plan.assert_not_called()

    # Dosya değiştirilmemiş olmalı (apply_change çağrılmamalı)
    if hasattr(registry.workflow, 'apply_change'):
        registry.workflow.apply_change.assert_not_called()


def test_inspection_task_with_file_read():
    """Inspection-only görevde read_file tool'u kullanılabilir."""
    from app.ai.agent_loop import AgentLoop, LoopConfig
    from app.ai.ollama_client import OllamaClient
    from app.tools.tool_registry import ToolRegistry
    from app.ai.tool_parser import ToolCall, ParseResult
    from unittest.mock import patch
    
    # Mock registry
    registry = MagicMock(spec=ToolRegistry)
    registry.workflow = MagicMock()
    
    registry.execute.return_value = {
        "success": True,
        "content": "Dosya içeriği"
    }
    
    # Mock AI client - tool çağrısı yapar (read_file)
    ai_client = MagicMock(spec=OllamaClient)
    ai_client.chat.return_value = {
        "content": "read_file aracını kullanıyorum",
        "tool_calls": None
    }
    
    loop = AgentLoop(
        ollama_client=ai_client,
        tool_registry=registry,
        config=LoopConfig(max_iterations=3)
    )
    
    # Parser mock - tool çağrısı döndür
    with patch.object(loop.parser, 'parse') as mock_parse:
        mock_parse.return_value = ParseResult(
            success=True,
            tool_calls=[ToolCall(name="read_file", arguments={"relative_path": "app/core/config.py"}, raw_text="")],
            raw_response=""
        )
        
        # Inspection-only görev
        result = loop.run("app/core/config.py dosyasını incele")
    
    # Sonuç başarılı olmalı (hedef dosya okundu)
    assert result.success is True
    
    # ChangeWorkflow çağrılmamalı
    registry.workflow.create_plan.assert_not_called()


def test_inspection_task_no_file_modification():
    """Inspection-only görevde hiçbir dosya değiştirilmemeli."""
    from app.ai.agent_loop import AgentLoop, LoopConfig
    from app.ai.ollama_client import OllamaClient
    from app.tools.tool_registry import ToolRegistry
    from app.ai.tool_parser import ToolCall, ParseResult
    from unittest.mock import patch
    
    # Mock registry
    registry = MagicMock(spec=ToolRegistry)
    registry.workflow = MagicMock()
    
    # Dosya yazma tool'ları çağrılmamalı
    def mock_execute(name, arguments, approved=False):
        if name in ["write_file", "edit_file", "create_file"]:
            raise AssertionError(f"Dosya yazma tool'u çağrılmamalı: {name}")
        return {"success": True, "content": "OK"}
    
    registry.execute.side_effect = mock_execute
    
    # Mock AI client - tool çağrısı yapar (read_file)
    ai_client = MagicMock(spec=OllamaClient)
    ai_client.chat.return_value = {
        "content": "Dosya incelendi. Hata bulunamadı.",
        "tool_calls": None
    }
    
    loop = AgentLoop(
        ollama_client=ai_client,
        tool_registry=registry,
        config=LoopConfig(max_iterations=3)
    )
    
    # Parser mock - tool çağrısı döndür
    with patch.object(loop.parser, 'parse') as mock_parse:
        mock_parse.return_value = ParseResult(
            success=True,
            tool_calls=[ToolCall(name="read_file", arguments={"relative_path": "app/core/config.py"}, raw_text="")],
            raw_response=""
        )
        
        # Inspection-only görev
        result = loop.run("app/core/config.py dosyasını incele")
    
    # Sonuç başarılı olmalı (hedef dosya okundu)
    assert result.success is True


def test_inspection_task_with_negation():
    """Negasyon içeren görevler inspection-only olarak tespit edilmeli."""
    from app.ai.agent_loop import AgentLoop
    
    loop = AgentLoop(
        ollama_client=MagicMock(),
        tool_registry=MagicMock()
    )
    
    tasks_with_negation = [
        "Dosyayı incele, değiştirme",
        "Henüz değişiklik yapma, sadece kontrol et",
        "Kodu review et, don't change",
        "Analyze without modifying"
    ]
    
    for task in tasks_with_negation:
        assert loop._is_inspection_only_task(task) is True, f"Negasyon içeren görev tespit edilemedi: {task}"
        assert loop._requires_code_change(task) is False, f"Negasyon içeren görev kod değişikliği gerektiriyor: {task}"


def test_inspection_vs_code_change_distinction():
    """Inspection ve kod değişikliği görevleri ayrılmalı."""
    from app.ai.agent_loop import AgentLoop
    
    loop = AgentLoop(
        ollama_client=MagicMock(),
        tool_registry=MagicMock()
    )
    
    inspection_task = "Dosyayı incele, değiştirme"
    code_change_task = "Dosyayı değiştir ve güncelle"
    
    # Inspection task
    assert loop._is_inspection_only_task(inspection_task) is True
    assert loop._requires_code_change(inspection_task) is False
    
    # Code change task
    assert loop._is_inspection_only_task(code_change_task) is False
    assert loop._requires_code_change(code_change_task) is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
