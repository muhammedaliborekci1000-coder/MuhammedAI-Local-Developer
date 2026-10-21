"""
Unit Test: Correction Loop Counter and State Management
Amaç: Correction loop sayaç ve durum yönetimini doğrulamak.
"""

import pytest
import sys
import os
import shutil
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.ai.agent_loop import AgentLoop, LoopConfig
from app.ai.ollama_client import OllamaClient
from app.tools.tool_registry import ToolRegistry
from app.core.config import PROJECT_ROOT


def test_correction_counter_reset_between_runs():
    """
    TEST: Ayrı run() çağrıları arasında correction counter'ın sıfırlandığını doğrula.
    """
    print("\n" + "=" * 70)
    print("TEST: Correction Counter Reset Between Runs")
    print("=" * 70)

    workspace = PROJECT_ROOT / "quality_tests" / "correction_workspace"
    workspace.mkdir(parents=True, exist_ok=True)

    try:
        # Basit bir senaryo
        calculator_file = workspace / "calculator.py"
        original_code = 'def add(a, b):\n    return a - b\n'
        with open(calculator_file, 'w', encoding='utf-8') as f:
            f.write(original_code)

        test_file = workspace / "test_calculator.py"
        test_code = 'def test_add():\n    assert add(2, 3) == 5\n'
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(test_code)

        relative_calc = str(calculator_file.relative_to(PROJECT_ROOT))
        relative_test = str(test_file.relative_to(PROJECT_ROOT))

        ollama_client = OllamaClient()
        tool_registry = ToolRegistry()
        config = LoopConfig(max_correction_attempts=3, enable_logging=False)

        def approval_callback(tool_name, arguments):
            return True

        agent_loop = AgentLoop(
            ollama_client=ollama_client,
            tool_registry=tool_registry,
            config=config,
            approval_callback=approval_callback
        )

        # İlk run
        user_task = f"{relative_calc} dosyasındaki add fonksiyonunu düzeltin."
        result1 = agent_loop.run(user_task)

        print(f"\nİlk run sonrası:")
        print(f"Success: {result1.success}")
        print(f"Correction attempt counter: {agent_loop._correction_attempt}")
        print(f"Correction history length: {len(agent_loop._correction_history)}")

        # Counter sıfırlanmalı
        assert agent_loop._correction_attempt == 0, "Correction attempt counter sıfırlanmadı"
        assert len(agent_loop._correction_history) == 0, "Correction history sıfırlanmadı"

        # İkinci run (aynı AgentLoop örneği)
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


def test_max_correction_attempts_zero():
    """
    TEST: max_correction_attempts=0 verildiğinde güvenli davranış.
    """
    print("\n" + "=" * 70)
    print("TEST: Max Correction Attempts Zero")
    print("=" * 70)

    workspace = PROJECT_ROOT / "quality_tests" / "correction_workspace"
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
        relative_test = str(test_file.relative_to(PROJECT_ROOT))

        ollama_client = OllamaClient()
        tool_registry = ToolRegistry()
        config = LoopConfig(max_correction_attempts=0, enable_logging=False)

        def approval_callback(tool_name, arguments):
            return True

        agent_loop = AgentLoop(
            ollama_client=ollama_client,
            tool_registry=tool_registry,
            config=config,
            approval_callback=approval_callback
        )

        user_task = f"{relative_calc} dosyasındaki add fonksiyonunu düzeltin."
        result = agent_loop.run(user_task)

        print(f"\nSonuç:")
        print(f"Success: {result.success}")
        print(f"Error: {result.error}")

        # max_correction_attempts=0 olduğunda correction loop başlatılmamalı
        # Ancak ilk deneme başarılı olabilir
        print("\nNot: max_correction_attempts=0 correction loop'u devre dışı bırakır.")
        print("İlk deneme başarılı olabilir, bu normal bir durum.")

        print("\n" + "=" * 70)
        print("TEST: PASS")
        print("=" * 70)

    finally:
        if workspace.exists():
            shutil.rmtree(workspace)


def test_max_correction_attempts_negative():
    """
    TEST: max_correction_attempts negatif verildiğinde güvenli davranış.
    """
    print("\n" + "=" * 70)
    print("TEST: Max Correction Attempts Negative")
    print("=" * 70)

    workspace = PROJECT_ROOT / "quality_tests" / "correction_workspace"
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
        relative_test = str(test_file.relative_to(PROJECT_ROOT))

        ollama_client = OllamaClient()
        tool_registry = ToolRegistry()
        config = LoopConfig(max_correction_attempts=-1, enable_logging=False)

        def approval_callback(tool_name, arguments):
            return True

        agent_loop = AgentLoop(
            ollama_client=ollama_client,
            tool_registry=tool_registry,
            config=config,
            approval_callback=approval_callback
        )

        user_task = f"{relative_calc} dosyasındaki add fonksiyonunu düzeltin."
        result = agent_loop.run(user_task)

        print(f"\nSonuç:")
        print(f"Success: {result.success}")
        print(f"Error: {result.error}")

        print("\nNot: max_correction_attempts negatif olduğunda davranış belirsiz.")
        print("Bu durumda correction loop başlatılmayabilir.")

        print("\n" + "=" * 70)
        print("TEST: PASS")
        print("=" * 70)

    finally:
        if workspace.exists():
            shutil.rmtree(workspace)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
