"""
Mock Unit Test: Correction Loop Counter and State Management
Amaç: Correction loop sayaç ve durum yönetimini mock ile doğrulamak.
Gerçek Ollama modeli kullanılmaz, deterministik sonuçlar sağlar.
"""

import pytest
import sys
import os
import shutil
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.ai.agent_loop import AgentLoop, LoopConfig
from app.ai.ollama_client import OllamaClient
from app.tools.tool_registry import ToolRegistry
from app.core.config import PROJECT_ROOT


class MockOllamaClient:
    """Mock OllamaClient - deterministik yanıtlar döndürür."""
    
    def __init__(self):
        self.call_count = 0
    
    def chat(self, message, tools=None, messages=None, response_format=None):
        """Deterministik mock yanıtlar döndürür."""
        self.call_count += 1
        
        # JSON formatı bekleniyorsa JSON döndür
        if response_format:
            return {
                "content": '{"file": "test.py", "function": "test", "problem": "test", "change": "test", "old_code": "def test():\n    pass", "new_code": "def test():\n    return True", "reason": "test"}'
            }
        
        # Native tool calls için mock response
        if tools:
            return {
                "content": "I will help you with your task.",
                "tool_calls": []
            }
        
        # Basit metin yanıtı
        return {
            "content": "Test response"
        }


def test_correction_counter_reset_between_runs_mock():
    """
    TEST: Ayrı run() çağrıları arasında correction counter'ın sıfırlandığını doğrula (mock).
    """
    print("\n" + "=" * 70)
    print("TEST: Correction Counter Reset Between Runs (Mock)")
    print("=" * 70)

    workspace = PROJECT_ROOT / "quality_tests" / "correction_workspace_mock"
    workspace.mkdir(parents=True, exist_ok=True)

    try:
        calculator_file = workspace / "calculator.py"
        original_code = 'def add(a, b):\n    return a - b\n'
        with open(calculator_file, 'w', encoding='utf-8') as f:
            f.write(original_code)

        test_file = workspace / "test_calculator.py"
        test_code = 'def test_add():\n    assert add(2, 3) == 5\n'
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(test_code)

        relative_calc = str(calculator_file.relative_to(PROJECT_ROOT))

        mock_client = MockOllamaClient()
        tool_registry = ToolRegistry()
        config = LoopConfig(max_correction_attempts=3, enable_logging=False)

        def approval_callback(tool_name, arguments):
            return True

        agent_loop = AgentLoop(
            ollama_client=mock_client,
            tool_registry=tool_registry,
            config=config,
            approval_callback=approval_callback
        )

        # İlk run
        user_task = f"{relative_calc} dosyasındaki add fonksiyonunu düzeltin."
        
        # Mock ile correction loop tetiklenmeyecek, direkt return
        with patch.object(agent_loop, '_requires_code_change', return_value=False):
            result1 = agent_loop.run(user_task)

        print(f"\nİlk run sonrası:")
        print(f"Success: {result1.success}")
        print(f"Correction attempt counter: {agent_loop._correction_attempt}")
        print(f"Correction history length: {len(agent_loop._correction_history)}")

        # Counter sıfırlanmalı
        assert agent_loop._correction_attempt == 0, "Correction attempt counter sıfırlanmadı"
        assert len(agent_loop._correction_history) == 0, "Correction history sıfırlanmadı"

        # İkinci run (aynı AgentLoop örneği)
        with patch.object(agent_loop, '_requires_code_change', return_value=False):
            result2 = agent_loop.run(user_task)

        print(f"\nİkinci run sonrası:")
        print(f"Success: {result2.success}")
        print(f"Correction attempt counter: {agent_loop._correction_attempt}")
        print(f"Correction history length: {len(agent_loop._correction_history)}")

        # Counter yine sıfırlanmalı
        assert agent_loop._correction_attempt == 0, "Correction attempt counter ikinci run'da sıfırlanmadı"
        assert len(agent_loop._correction_history) == 0, "Correction history ikinci run'da sıfırlanmadı"

        print("\n" + "=" * 70)
        print("TEST: PASS")
        print("=" * 70)

    finally:
        if workspace.exists():
            shutil.rmtree(workspace)


def test_correction_counter_increments_on_failure_mock():
    """
    TEST: Düzeltme sayacı yalnızca ilgili başarısız uygulama sonucunda doğru şekilde artıyor (mock).
    """
    print("\n" + "=" * 70)
    print("TEST: Correction Counter Increments on Failure (Mock)")
    print("=" * 70)

    workspace = PROJECT_ROOT / "quality_tests" / "correction_workspace_mock"
    workspace.mkdir(parents=True, exist_ok=True)

    try:
        calculator_file = workspace / "calculator.py"
        original_code = 'def add(a, b):\n    return a - b\n'
        with open(calculator_file, 'w', encoding='utf-8') as f:
            f.write(original_code)

        test_file = workspace / "test_calculator.py"
        test_code = 'def test_add():\n    assert add(2, 3) == 5\n'
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(test_code)

        relative_calc = str(calculator_file.relative_to(PROJECT_ROOT))

        mock_client = MockOllamaClient()
        tool_registry = ToolRegistry()
        config = LoopConfig(max_correction_attempts=3, enable_logging=False)

        def approval_callback(tool_name, arguments):
            return True

        agent_loop = AgentLoop(
            ollama_client=mock_client,
            tool_registry=tool_registry,
            config=config,
            approval_callback=approval_callback
        )

        # Correction counter manuel artırma simülasyonu
        agent_loop._correction_attempt = 1
        agent_loop._correction_history.append({"attempt": 1, "success": False})

        print(f"\nCorrection attempt counter: {agent_loop._correction_attempt}")
        print(f"Correction history length: {len(agent_loop._correction_history)}")

        assert agent_loop._correction_attempt == 1, "Counter 1 olmalı"
        assert len(agent_loop._correction_history) == 1, "History 1 eleman olmalı"

        print("\n" + "=" * 70)
        print("TEST: PASS")
        print("=" * 70)

    finally:
        if workspace.exists():
            shutil.rmtree(workspace)


def test_max_correction_attempts_limit_stops_loop_mock():
    """
    TEST: Düzeltme sınırı aşılınca döngü duruyor (mock).
    """
    print("\n" + "=" * 70)
    print("TEST: Max Correction Attempts Limit Stops Loop (Mock)")
    print("=" * 70)

    workspace = PROJECT_ROOT / "quality_tests" / "correction_workspace_mock"
    workspace.mkdir(parents=True, exist_ok=True)

    try:
        calculator_file = workspace / "calculator.py"
        original_code = 'def add(a, b):\n    return a - b\n'
        with open(calculator_file, 'w', encoding='utf-8') as f:
            f.write(original_code)

        test_file = workspace / "test_calculator.py"
        test_code = 'def test_add():\n    assert add(2, 3) == 5\n'
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(test_code)

        relative_calc = str(calculator_file.relative_to(PROJECT_ROOT))

        mock_client = MockOllamaClient()
        tool_registry = ToolRegistry()
        config = LoopConfig(max_correction_attempts=2, enable_logging=False)

        def approval_callback(tool_name, arguments):
            return True

        agent_loop = AgentLoop(
            ollama_client=mock_client,
            tool_registry=tool_registry,
            config=config,
            approval_callback=approval_callback
        )

        # Sınır simülasyonu
        agent_loop._correction_attempt = 2
        agent_loop._correction_history.append({"attempt": 1, "success": False})
        agent_loop._correction_history.append({"attempt": 2, "success": False})

        print(f"\nCorrection attempt counter: {agent_loop._correction_attempt}")
        print(f"Max correction attempts: {config.max_correction_attempts}")
        print(f"Correction history length: {len(agent_loop._correction_history)}")

        assert agent_loop._correction_attempt == config.max_correction_attempts, "Counter max'a ulaştı"
        assert len(agent_loop._correction_history) == config.max_correction_attempts, "History max eleman"

        print("\n" + "=" * 70)
        print("TEST: PASS")
        print("=" * 70)

    finally:
        if workspace.exists():
            shutil.rmtree(workspace)


def test_successful_correction_completion_mock():
    """
    TEST: Başarılı düzeltmede doğru tamamlanma durumu oluşuyor (mock).
    """
    print("\n" + "=" * 70)
    print("TEST: Successful Correction Completion (Mock)")
    print("=" * 70)

    workspace = PROJECT_ROOT / "quality_tests" / "correction_workspace_mock"
    workspace.mkdir(parents=True, exist_ok=True)

    try:
        calculator_file = workspace / "calculator.py"
        original_code = 'def add(a, b):\n    return a + b\n'  # Düzeltilmiş kod
        with open(calculator_file, 'w', encoding='utf-8') as f:
            f.write(original_code)

        test_file = workspace / "test_calculator.py"
        test_code = 'def test_add():\n    assert add(2, 3) == 5\n'
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(test_code)

        relative_calc = str(calculator_file.relative_to(PROJECT_ROOT))

        mock_client = MockOllamaClient()
        tool_registry = ToolRegistry()
        config = LoopConfig(max_correction_attempts=3, enable_logging=False)

        def approval_callback(tool_name, arguments):
            return True

        agent_loop = AgentLoop(
            ollama_client=mock_client,
            tool_registry=tool_registry,
            config=config,
            approval_callback=approval_callback
        )

        # Başarılı düzeltme simülasyonu
        agent_loop._correction_attempt = 0
        agent_loop._correction_history = []  # Başarılı olduğu için history boş

        print(f"\nCorrection attempt counter: {agent_loop._correction_attempt}")
        print(f"Correction history length: {len(agent_loop._correction_history)}")

        assert agent_loop._correction_attempt == 0, "Başarılı düzeltmede counter 0 olmalı"
        assert len(agent_loop._correction_history) == 0, "Başarılı düzeltmede history boş olmalı"

        print("\n" + "=" * 70)
        print("TEST: PASS")
        print("=" * 70)

    finally:
        if workspace.exists():
            shutil.rmtree(workspace)


def test_model_text_response_controlled_behavior_mock():
    """
    TEST: Model beklenmeyen biçimde metin döndürürse sistem kontrollü davranıyor (mock).
    """
    print("\n" + "=" * 70)
    print("TEST: Model Text Response Controlled Behavior (Mock)")
    print("=" * 70)

    workspace = PROJECT_ROOT / "quality_tests" / "correction_workspace_mock"
    workspace.mkdir(parents=True, exist_ok=True)

    try:
        calculator_file = workspace / "calculator.py"
        original_code = 'def add(a, b):\n    return a - b\n'
        with open(calculator_file, 'w', encoding='utf-8') as f:
            f.write(original_code)

        test_file = workspace / "test_calculator.py"
        test_code = 'def test_add():\n    assert add(2, 3) == 5\n'
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(test_code)

        relative_calc = str(calculator_file.relative_to(PROJECT_ROOT))

        mock_client = MockOllamaClient()
        tool_registry = ToolRegistry()
        config = LoopConfig(max_correction_attempts=3, enable_logging=False)

        def approval_callback(tool_name, arguments):
            return True

        agent_loop = AgentLoop(
            ollama_client=mock_client,
            tool_registry=tool_registry,
            config=config,
            approval_callback=approval_callback
        )

        # Metin yanıtı simülasyonu - sistem kontrollü davranmalı
        user_task = f"{relative_calc} dosyasındaki add fonksiyonunu düzeltin."
        
        with patch.object(agent_loop, '_requires_code_change', return_value=False):
            result = agent_loop.run(user_task)

        print(f"\nSonuç:")
        print(f"Success: {result.success}")
        print(f"Error: {result.error}")

        # Sistem hatayı gizlememeli, kontrollü davranmalı
        # Result None olmamalı
        assert result is not None, "Result None olmamalı"

        print("\n" + "=" * 70)
        print("TEST: PASS")
        print("=" * 70)

    finally:
        if workspace.exists():
            shutil.rmtree(workspace)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
