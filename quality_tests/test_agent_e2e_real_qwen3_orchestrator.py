"""
TEST H — Gerçek Qwen3:4B E2E Test with ChangeOrchestrator
Tests real Qwen3 model with deterministic orchestration
"""
import sys
import os
import pytest
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.ai.agent_loop import AgentLoop, LoopConfig
from app.tools.tool_registry import ToolRegistry
from app.ai.ollama_client import OllamaClient
from app.core.config import PROJECT_ROOT


def setup_test_files():
    """Test dosyalarını oluştur"""
    workspace = PROJECT_ROOT / "quality_tests" / "test_workspace"
    workspace.mkdir(parents=True, exist_ok=True)

    agent_file = workspace / "agent_task.py"
    test_file = workspace / "test_agent_task.py"
    
    agent_file.write_text('def greet():\n    return "Merhaba"\n', encoding='utf-8')
    test_file.write_text('from agent_task import greet\n\ndef test_greet():\n    assert greet() == "Merhaba Muhammed"\n', encoding='utf-8')
    
    return agent_file, test_file


def cleanup_test_files():
    """Test dosyalarını temizle"""
    workspace = PROJECT_ROOT / "quality_tests" / "test_workspace"
    if workspace.exists():
        import shutil
        shutil.rmtree(workspace)


@pytest.mark.slow
def test_h_real_qwen3_approval_true():
    """
    TEST H — Gerçek Qwen3:4B (approval=True)
    Beklenen:
    - Model plan oluşturabilmeli
    - Doğal dilde onay istese bile sistem güvenli biçimde approval aşamasına geçebilmeli
    - Gerçek callback True olduğunda değişiklik tamamlanmalı
    """
    print("=" * 70)
    print("TEST H — Gerçek Qwen3:4B (approval=True)")
    print("=" * 70)
    
    agent_file, test_file = setup_test_files()
    original_content = agent_file.read_text(encoding='utf-8')
    
    print(f"Test dosyası: {agent_file}")
    print(f"Orijinal içerik:\n{original_content}")
    
    try:
        # Approval callback
        approval_log = []
        
        def approval_callback(tool_name: str, arguments: dict) -> bool:
            print(f"  [APPROVAL] {tool_name} -> APPROVED")
            approval_log.append((tool_name, arguments, True))
            return True
        
        # Gerçek Ollama client
        ollama_client = OllamaClient(model="qwen3:4b")
        
        # AgentLoop oluştur
        config = LoopConfig(
            max_iterations=10,
            max_no_tool_retries=2,
            enable_logging=True
        )
        
        tool_registry = ToolRegistry()
        
        agent_loop = AgentLoop(
            ollama_client=ollama_client,
            tool_registry=tool_registry,
            config=config,
            approval_callback=approval_callback
        )
        
        # Görev
        user_task = "Dosya: quality_tests/test_workspace/agent_task.py. Bu dosyadaki greet fonksiyonunun döndürdü metni 'Merhaba Muhammed' olarak değiştir. Dosya yolu: quality_tests/test_workspace/agent_task.py"
        
        print(f"\nGörev: {user_task}")
        print("-" * 70)
        
        # AgentLoop'u çalıştır
        result = agent_loop.run(user_task)
        
        print("\nAgentLoop sonucu:")
        print(f"  Success: {result.success}")
        print(f"  Iterations: {result.iterations}")
        print(f"  Final response: {result.final_response.encode('cp1254', errors='ignore').decode('cp1254')}")
        print(f"  Error: {result.error}")
        
        # Tool call log
        print(f"\nTool call log ({len(result.tool_calls)} çağrı):")
        for i, call in enumerate(result.tool_calls, 1):
            print(f"  {i}. {call['tool']}")
            if call.get('result'):
                success = call['result'].get('success')
                print(f"     Success: {success}")
        
        # Approval log
        print(f"\nApproval log ({len(approval_log)} çağrı):")
        for i, (tool_name, args, approved) in enumerate(approval_log, 1):
            print(f"  {i}. {tool_name} -> approved={approved}")
        
        # Dosya içeriği
        final_content = agent_file.read_text(encoding='utf-8')
        print(f"\nSon dosya içeriği:")
        print(final_content)
        
        # Değerlendirme
        print("\n" + "=" * 70)
        print("DEĞERLENDİRME")
        print("=" * 70)
        
        # Orkestratör kullanıldı mı?
        orchestrator_used = any(
            call['tool'] == 'create_change_plan' and 
            call.get('result', {}).get('success')
            for call in result.tool_calls
        )
        print(f"Orkestratör kullanıldı: {orchestrator_used}")
        
        # Approval çağrıldı mı?
        approval_called = len(approval_log) > 0
        print(f"Approval çağrıldı: {approval_called}")
        
        # Dosya değişti mi?
        file_changed = final_content != original_content
        print(f"Dosya değişti: {file_changed}")
        
        # Backup oluştu mu?
        backup_created = any(
            call.get('result', {}).get('backup')
            for call in result.tool_calls
        )
        print(f"Backup oluştu: {backup_created}")
        
        # Test başarılı mı?
        success = (
            orchestrator_used and
            approval_called and
            file_changed and
            backup_created
        )

        print(f"\nTEST H: {'PASS' if success else 'FAIL'}")
        assert success, "Qwen3 değişiklik akışı beklenen şekilde tamamlanmadı."
        
    except Exception as exc:
        print(f"\nTEST H HATASI: {exc}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        cleanup_test_files()


@pytest.mark.slow
def test_h_real_qwen3_approval_false():
    """
    TEST H — Gerçek Qwen3:4B (approval=False)
    Beklenen:
    - Model plan oluşturabilmeli
    - Callback False olduğunda dosya değişmemeli
    """
    print("\n\n")
    print("=" * 70)
    print("TEST H — Gerçek Qwen3:4B (approval=False)")
    print("=" * 70)
    
    agent_file, test_file = setup_test_files()
    original_content = agent_file.read_text(encoding='utf-8')
    
    print(f"Test dosyası: {agent_file}")
    print(f"Orijinal içerik:\n{original_content}")
    
    try:
        # Approval callback (reddet)
        approval_log = []
        
        def approval_callback(tool_name: str, arguments: dict) -> bool:
            print(f"  [APPROVAL] {tool_name} -> REJECTED")
            approval_log.append((tool_name, arguments, False))
            return False
        
        # Gerçek Ollama client
        ollama_client = OllamaClient(model="qwen3:4b")
        
        # AgentLoop oluştur
        config = LoopConfig(
            max_iterations=10,
            max_no_tool_retries=2,
            enable_logging=True
        )
        
        tool_registry = ToolRegistry()
        
        agent_loop = AgentLoop(
            ollama_client=ollama_client,
            tool_registry=tool_registry,
            config=config,
            approval_callback=approval_callback
        )
        
        # Görev
        user_task = "Dosya: quality_tests/test_workspace/agent_task.py. Bu dosyadaki greet fonksiyonunun döndürdü metni 'Merhaba Muhammed' olarak değiştir. Dosya yolu: quality_tests/test_workspace/agent_task.py"
        
        print(f"\nGörev: {user_task}")
        print("-" * 70)
        
        # AgentLoop'u çalıştır
        result = agent_loop.run(user_task)
        
        print("\nAgentLoop sonucu:")
        print(f"  Success: {result.success}")
        print(f"  Iterations: {result.iterations}")
        print(f"  Final response: {result.final_response.encode('cp1254', errors='ignore').decode('cp1254')}")
        print(f"  Error: {result.error}")
        
        # Tool call log
        print(f"\nTool call log ({len(result.tool_calls)} çağrı):")
        for i, call in enumerate(result.tool_calls, 1):
            print(f"  {i}. {call['tool']}")
            if call.get('result'):
                success = call['result'].get('success')
                print(f"     Success: {success}")
        
        # Approval log
        print(f"\nApproval log ({len(approval_log)} çağrı):")
        for i, (tool_name, args, approved) in enumerate(approval_log, 1):
            print(f"  {i}. {tool_name} -> approved={approved}")
        
        # Dosya içeriği
        final_content = agent_file.read_text(encoding='utf-8')
        print(f"\nSon dosya içeriği:")
        print(final_content)
        
        # Değerlendirme
        print("\n" + "=" * 70)
        print("DEĞERLENDİRME")
        print("=" * 70)
        
        # Dosya değişmedi mi?
        file_unchanged = final_content == original_content
        print(f"Dosya değişmedi: {file_unchanged}")
        
        # Approval çağrıldı mı?
        approval_called = len(approval_log) > 0
        print(f"Approval çağrıldı: {approval_called}")
        
        # Test başarılı mı?
        success = (
            approval_called and
            file_unchanged
        )

        print(f"\nTEST H (approval=False): {'PASS' if success else 'FAIL'}")
        assert success, "Onay reddedildiğinde değişiklik engellenmeliydi."
        
    except Exception as exc:
        print(f"\nTEST H (approval=False) HATASI: {exc}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        cleanup_test_files()


if __name__ == "__main__":
    # TEST H (approval=True)
    test_h_real_qwen3_approval_true()
    
    # TEST H (approval=False)
    test_h_real_qwen3_approval_false()
    
    # Özet
    print("\n\n")
    print("=" * 70)
    print("GENEL ÖZET")
    print("=" * 70)
    print("Tüm testler PASS")
    print("=" * 70)
