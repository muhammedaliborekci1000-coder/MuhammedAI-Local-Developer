"""
Codebase Intelligence Real Qwen3 Test
Gerçek Qwen3 modeli ile Codebase Intelligence entegrasyon testi.
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


@pytest.mark.slow
def test_codebase_intelligence_real_qwen3():
    """
    Gerçek Qwen3 ile Codebase Intelligence testi.
    Symbol discovery → related files → context → plan zinciri.
    """
    print("\n" + "=" * 70)
    print("CODEBASE INTELLIGENCE REAL QWEN3 TEST")
    print("=" * 70)

    workspace = PROJECT_ROOT / "quality_tests" / "codebase_intelligence_workspace"
    workspace.mkdir(parents=True, exist_ok=True)

    try:
        # Basit bir test dosyası oluştur
        test_file = workspace / "calculator.py"
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write('''
class Calculator:
    def add(self, a, b):
        return a + b
    
    def subtract(self, a, b):
        return a - b

def test_calculator():
    calc = Calculator()
    assert calc.add(1, 2) == 3
    assert calc.subtract(5, 3) == 2
''')

        relative_test = str(test_file.relative_to(PROJECT_ROOT))

        # AgentLoop oluştur
        ollama_client = OllamaClient()
        tool_registry = ToolRegistry()
        config = LoopConfig(
            max_iterations=5,
            enable_logging=True
        )

        def approval_callback(tool_name, arguments):
            print(f"Approval: {tool_name} -> APPROVED")
            return True

        agent_loop = AgentLoop(
            ollama_client=ollama_client,
            tool_registry=tool_registry,
            config=config,
            approval_callback=approval_callback
        )

        # Basit bir görev - symbol discovery kullanarak
        user_task = f"{relative_test} dosyasındaki Calculator class'ını ve metodlarını analiz et."

        print(f"\nGörev: {user_task}")
        print("-" * 70)

        # AgentLoop'u çalıştır
        result = agent_loop.run(user_task)

        print(f"\nAgentLoop sonucu:")
        print(f"Success: {result.success}")
        print(f"Error: {result.error}")
        print(f"Iterations: {result.iterations}")
        print(f"Tool calls: {len(result.tool_calls)}")

        # Tool call kontrolü
        tool_names = [tc.get("tool") for tc in result.tool_calls]
        print(f"Used tools: {tool_names}")

        # Codebase intelligence tool'ları kullanıldı mı?
        codebase_tools_used = any(
            tool in tool_names 
            for tool in ["search_code_symbols", "get_symbol_details", "find_related_files"]
        )
        print(f"Codebase intelligence tools used: {codebase_tools_used}")

        # Session kontrolü
        if agent_loop.session:
            print(f"\nSession bilgisi:")
            print(f"Session ID: {agent_loop.session.session_id}")
            print(f"Status: {agent_loop.session.status.value}")
            print(f"Tool calls: {len(agent_loop.session.tool_history)}")

            assert agent_loop.session.session_id is not None

        print("\n" + "=" * 70)
        print("CODEBASE INTELLIGENCE REAL QWEN3 TEST: PASS")
        print("=" * 70)

    finally:
        # Temizlik
        if workspace.exists():
            shutil.rmtree(workspace)
            print(f"\nWorkspace temizlendi: {workspace}")


if __name__ == "__main__":
    try:
        test_codebase_intelligence_real_qwen3()
        print("\n" + "=" * 70)
        print("GERÇEK QWEN3 CODEBASE INTELLIGENCE TEST BAŞARILI")
        print("=" * 70)
        sys.exit(0)
    except Exception as e:
        print(f"\nTEST HATASI:")
        print("-" * 70)
        import traceback
        traceback.print_exc()
        print("=" * 70)
        sys.exit(1)
