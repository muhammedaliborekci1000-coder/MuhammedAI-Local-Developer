"""
TEST 2: AgentLoop with Fake Model
Tests AgentLoop's ability to transition from create_change_plan to apply_change
"""
import sys
import os
from pathlib import Path

# Proje kök dizinini path'e ekle
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.ai.agent_loop import AgentLoop, LoopConfig
from app.tools.tool_registry import ToolRegistry
from app.core.config import PROJECT_ROOT
from quality_tests.fake_ollama_client import FakeOllamaClient


def test_agent_loop_fake_model(approval_mode=True):
    """
    TEST 2A/B: AgentLoop with Fake Model
    """
    print("=" * 70)
    print(f"TEST 2: AgentLoop Fake Model (approval={approval_mode})")
    print("=" * 70)
    
    # Workspace
    workspace = PROJECT_ROOT / "quality_tests" / "e2e_workspace"
    workspace.mkdir(parents=True, exist_ok=True)
    
    agent_file = workspace / "agent_task.py"
    test_file = workspace / "test_agent_task.py"
    
    # Orijinal içerik
    original_content = 'def greet():\n    return "Merhaba"\n'
    
    # Dosyaları oluştur
    agent_file.write_text(original_content, encoding='utf-8')
    test_file.write_text('from agent_task import greet\n\ndef test_greet():\n    assert greet() == "Merhaba Muhammed"\n', encoding='utf-8')
    
    print(f"Test dosyası: {agent_file}")
    print(f"Orijinal içerik:\n{original_content}")
    
    # Approval callback
    approval_log = []
    
    def approval_callback(tool_name: str, arguments: dict) -> bool:
        print(f"  [APPROVAL] {tool_name} -> {'APPROVED' if approval_mode else 'REJECTED'}")
        approval_log.append((tool_name, arguments, approval_mode))
        return approval_mode
    
    # Fake model oluştur
    fake_client = FakeOllamaClient(approval_mode=approval_mode)
    
    # AgentLoop oluştur
    config = LoopConfig(
        max_iterations=10,
        max_no_tool_retries=2,
        enable_logging=True
    )
    
    tool_registry = ToolRegistry()
    
    agent_loop = AgentLoop(
        ollama_client=fake_client,
        tool_registry=tool_registry,
        config=config,
        approval_callback=approval_callback
    )
    
    # Görev
    user_task = "quality_tests/e2e_workspace/agent_task.py dosyasındaki greet fonksiyonunun döndürdü metni 'Merhaba Muhammed' olarak değiştir."
    
    print(f"\nGörev: {user_task}")
    print("-" * 70)
    
    # AgentLoop'u çalıştır
    try:
        result = agent_loop.run(user_task)
        print("\nAgentLoop sonucu:")
        print(result)
    except Exception as exc:
        print(f"\nAgentLoop hatası: {exc}")
        import traceback
        traceback.print_exc()
    
    # Sonuçları raporla
    print("\n" + "=" * 70)
    print("SONUÇLAR")
    print("=" * 70)
    
    print(f"\nFake model çağrı sayısı: {fake_client.agent_loop_call_count}")
    print(f"Approval log: {len(approval_log)} çağrı")
    
    for i, (tool_name, args, approved) in enumerate(approval_log, 1):
        print(f"  {i}. {tool_name} -> approved={approved}")
    
    # Dosya içeriği
    final_content = agent_file.read_text(encoding='utf-8')
    print(f"\nSon dosya içeriği:")
    print(final_content)
    
    # Beklenen içerik
    if approval_mode:
        expected = 'def greet():\n    return "Merhaba Muhammed"\n'
        print(f"Beklenen:\n{expected}")
        print(f"Eşleşiyor: {final_content == expected}")
    else:
        expected = original_content
        print(f"Beklenen (değişmemiş):\n{expected}")
        print(f"Eşleşiyor: {final_content == expected}")
    
    return {
        'call_count': fake_client.agent_loop_call_count,
        'approval_count': len(approval_log),
        'final_content': final_content,
        'expected_content': expected if approval_mode else original_content,
        'matches': final_content == (expected if approval_mode else original_content)
    }


if __name__ == "__main__":
    # TEST 2A: approval=True
    print("\n\n")
    result_a = test_agent_loop_fake_model(approval_mode=True)
    
    # TEST 2B: approval=False
    print("\n\n")
    result_b = test_agent_loop_fake_model(approval_mode=False)
    
    # Özet
    print("\n\n")
    print("=" * 70)
    print("GENEL ÖZET")
    print("=" * 70)
    print(f"\nTEST 2A (approval=True):")
    print(f"  Model çağrıları: {result_a['call_count']}")
    print(f"  Approval çağrıları: {result_a['approval_count']}")
    print(f"  Dosya eşleşiyor: {result_a['matches']}")
    
    print(f"\nTEST 2B (approval=False):")
    print(f"  Model çağrıları: {result_b['call_count']}")
    print(f"  Approval çağrıları: {result_b['approval_count']}")
    print(f"  Dosya değişmedi: {result_b['matches']}")
