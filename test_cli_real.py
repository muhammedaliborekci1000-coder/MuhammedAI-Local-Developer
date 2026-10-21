"""
Gerçek CLI Testleri
git status, python --version, dosya inceleme görevlerini test eder.
"""

import sys
import os
from pathlib import Path

# Proje kök dizinini path'e ekle
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from app.core.config import PROJECT_ROOT
from app.ai.agent_loop import AgentLoop, LoopConfig
from app.ai.ollama_client import OllamaClient
from app.tools.tool_registry import ToolRegistry


def test_git_status():
    """
    Git status terminal komutu testi
    """
    print("=" * 70)
    print("TEST 1: git status")
    print("=" * 70)
    
    ollama_client = OllamaClient()
    tool_registry = ToolRegistry()
    
    # Onay callback (her zaman onay ver)
    def approval_callback(tool_name: str, arguments: dict) -> bool:
        print(f"  Onay istendi: {tool_name}")
        print(f"  Argümanlar: {arguments}")
        return True
    
    config = LoopConfig(max_iterations=5)
    agent_loop = AgentLoop(
        ollama_client=ollama_client,
        tool_registry=tool_registry,
        config=config,
        approval_callback=approval_callback
    )
    
    user_task = "git status"
    
    print(f"\nGörev: {user_task}")
    result = agent_loop.run(user_task)
    
    print(f"\nSonuc:")
    print(f"  Success: {result.success}")
    print(f"  İterasyon: {result.iterations}")
    print(f"  Tool çağrısı sayısı: {len(result.tool_calls)}")
    
    if result.error:
        print(f"  Hata: {result.error}")
    
    print(f"\nYanıt:")
    print("-" * 70)
    print(result.final_response)
    print("-" * 70)
    
    print(f"\nTool çağrıları:")
    for i, call in enumerate(result.tool_calls):
        print(f"  {i+1}. Tool: {call.get('tool')}")
        print(f"     Argümanlar: {call.get('arguments')}")
        print(f"     Sonuç success: {call.get('result', {}).get('success')}")
    
    # Terminal aracı kullanıldı mı?
    terminal_used = any(call.get('tool') == 'execute_terminal_command' for call in result.tool_calls)
    
    print(f"\nTerminal aracı kullanıldı: {terminal_used}")
    
    if terminal_used:
        for call in result.tool_calls:
            if call.get('tool') == 'execute_terminal_command':
                tool_result = call.get('result', {})
                if 'result' in tool_result:
                    actual_result = tool_result['result']
                    stdout = actual_result.get('stdout', '')
                    print(f"Git status çıktısı (ilk 300 karakter):")
                    print(stdout[:300])
    
    return {
        "task": user_task,
        "success": result.success,
        "iterations": result.iterations,
        "tool_calls_count": len(result.tool_calls),
        "terminal_used": terminal_used,
        "final_response": result.final_response
    }


def test_python_version():
    """
    Python version terminal komutu testi
    """
    print("\n" + "=" * 70)
    print("TEST 2: python --version")
    print("=" * 70)
    
    ollama_client = OllamaClient()
    tool_registry = ToolRegistry()
    
    def approval_callback(tool_name: str, arguments: dict) -> bool:
        print(f"  Onay istendi: {tool_name}")
        print(f"  Argümanlar: {arguments}")
        return True
    
    config = LoopConfig(max_iterations=5)
    agent_loop = AgentLoop(
        ollama_client=ollama_client,
        tool_registry=tool_registry,
        config=config,
        approval_callback=approval_callback
    )
    
    user_task = "python --version"
    
    print(f"\nGörev: {user_task}")
    result = agent_loop.run(user_task)
    
    print(f"\nSonuc:")
    print(f"  Success: {result.success}")
    print(f"  İterasyon: {result.iterations}")
    print(f"  Tool çağrısı sayısı: {len(result.tool_calls)}")
    
    if result.error:
        print(f"  Hata: {result.error}")
    
    print(f"\nYanıt:")
    print("-" * 70)
    print(result.final_response)
    print("-" * 70)
    
    print(f"\nTool çağrıları:")
    for i, call in enumerate(result.tool_calls):
        print(f"  {i+1}. Tool: {call.get('tool')}")
        print(f"     Argümanlar: {call.get('arguments')}")
        print(f"     Sonuç success: {call.get('result', {}).get('success')}")
    
    terminal_used = any(call.get('tool') == 'execute_terminal_command' for call in result.tool_calls)
    
    print(f"\nTerminal aracı kullanıldı: {terminal_used}")
    
    if terminal_used:
        for call in result.tool_calls:
            if call.get('tool') == 'execute_terminal_command':
                tool_result = call.get('result', {})
                if 'result' in tool_result:
                    actual_result = tool_result['result']
                    stdout = actual_result.get('stdout', '')
                    print(f"Python version çıktısı:")
                    print(stdout)
    
    return {
        "task": user_task,
        "success": result.success,
        "iterations": result.iterations,
        "tool_calls_count": len(result.tool_calls),
        "terminal_used": terminal_used,
        "final_response": result.final_response
    }


def test_file_inspection():
    """
    Dosya inceleme görevi testi
    """
    print("\n" + "=" * 70)
    print("TEST 3: app/ai/agent_loop.py dosyasını incele ve içeriğini özetle")
    print("=" * 70)
    
    ollama_client = OllamaClient()
    tool_registry = ToolRegistry()
    
    def approval_callback(tool_name: str, arguments: dict) -> bool:
        print(f"  Onay istendi: {tool_name}")
        print(f"  Argümanlar: {arguments}")
        return True
    
    config = LoopConfig(max_iterations=5)
    agent_loop = AgentLoop(
        ollama_client=ollama_client,
        tool_registry=tool_registry,
        config=config,
        approval_callback=approval_callback
    )
    
    user_task = "app/ai/agent_loop.py dosyasını incele ve içeriğini özetle"
    
    print(f"\nGörev: {user_task}")
    result = agent_loop.run(user_task)
    
    print(f"\nSonuc:")
    print(f"  Success: {result.success}")
    print(f"  İterasyon: {result.iterations}")
    print(f"  Tool çağrısı sayısı: {len(result.tool_calls)}")
    
    if result.error:
        print(f"  Hata: {result.error}")
    
    print(f"\nYanıt:")
    print("-" * 70)
    try:
        print(result.final_response)
    except Exception as e:
        print(f"[Yanıt yazdırılamadı: {e}]")
        safe_response = result.final_response.encode('utf-8', errors='ignore').decode('utf-8')
        print(safe_response[:500])
    print("-" * 70)
    
    print(f"\nTool çağrıları:")
    for i, call in enumerate(result.tool_calls):
        print(f"  {i+1}. Tool: {call.get('tool')}")
        print(f"     Argümanlar: {call.get('arguments')}")
        if call.get('tool') == 'read_file':
            tool_result = call.get('result', {})
            content = tool_result.get('content', '')
            print(f"     Dosya boyutu: {len(content)} karakter")
    
    file_read = any(call.get('tool') == 'read_file' for call in result.tool_calls)
    
    print(f"\nDosya okundu: {file_read}")
    
    # Conversation history kontrolü (dosya içeriği modele verildi mi?)
    print(f"\nConversation history (ilk 500 karakter):")
    conversation = agent_loop.memory.get_conversation_text()
    try:
        print(conversation[:500])
    except Exception as e:
        print(f"[Conversation yazdırılamadı: {e}]")
        safe_conv = conversation.encode('utf-8', errors='ignore').decode('utf-8')
        print(safe_conv[:500])
    
    return {
        "task": user_task,
        "success": result.success,
        "iterations": result.iterations,
        "tool_calls_count": len(result.tool_calls),
        "file_read": file_read,
        "final_response": result.final_response
    }


def main():
    print("=" * 70)
    print("GERÇEK CLI TESTLERİ")
    print("=" * 70)
    
    results = []
    
    # Test 1: git status
    try:
        result1 = test_git_status()
        results.append(result1)
    except Exception as e:
        print(f"\nTEST 1 HATASI: {e}")
        import traceback
        traceback.print_exc()
        results.append({"task": "git status", "error": str(e)})
    
    # Test 2: python --version
    try:
        result2 = test_python_version()
        results.append(result2)
    except Exception as e:
        print(f"\nTEST 2 HATASI: {e}")
        import traceback
        traceback.print_exc()
        results.append({"task": "python --version", "error": str(e)})
    
    # Test 3: dosya inceleme
    try:
        result3 = test_file_inspection()
        results.append(result3)
    except Exception as e:
        print(f"\nTEST 3 HATASI: {e}")
        import traceback
        traceback.print_exc()
        results.append({"task": "dosya inceleme", "error": str(e)})
    
    # Özet rapor
    print("\n" + "=" * 70)
    print("ÖZET RAPOR")
    print("=" * 70)
    
    for i, result in enumerate(results, 1):
        print(f"\nTEST {i}: {result.get('task', 'Bilinmiyor')}")
        print(f"  Success: {result.get('success', 'N/A')}")
        print(f"  İterasyon: {result.get('iterations', 'N/A')}")
        print(f"  Tool çağrısı sayısı: {result.get('tool_calls_count', 'N/A')}")
        print(f"  Terminal kullanıldı: {result.get('terminal_used', 'N/A')}")
        print(f"  Dosya okundu: {result.get('file_read', 'N/A')}")
        if 'error' in result:
            print(f"  Hata: {result['error']}")
    
    print("\n" + "=" * 70)
    
    return results


if __name__ == "__main__":
    try:
        results = main()
        sys.exit(0)
    except Exception as e:
        print(f"\nGENEL HATA:")
        print("-" * 70)
        import traceback
        traceback.print_exc()
        print("=" * 70)
        sys.exit(1)
