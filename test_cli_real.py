"""
Gerçek CLI Testleri
git status, python --version, dosya inceleme görevlerini test eder.
"""

import sys
import os
from pathlib import Path
import io

# UTF-8 output için stdout'u ayarla
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='ignore')

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
        safe_error = result.error.encode('utf-8', errors='ignore').decode('utf-8')
        print(f"  Hata: {safe_error}")
    
    print(f"\nYanit:")
    print("-" * 70)
    safe_response = result.final_response.encode('utf-8', errors='ignore').decode('utf-8')
    print(safe_response)
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
    
    # Conversation history'yi detaylı yazdır
    print(f"\nConversation history (son 5 mesaj):")
    try:
        history = agent_loop.memory.get_messages()
        print(f"Toplam mesaj sayısı: {len(history)}")
        for i, msg in enumerate(history[-5:]):
            role = msg.get('role', 'unknown')
            content_len = len(msg.get('content', ''))
            # tool_call_id sadece tool mesajları için geçerli
            tool_call_id = msg.get('tool_call_id', 'N/A') if role == 'tool' else 'N/A'
            print(f"  {i+1}. role={role}, content_len={content_len}, tool_call_id={tool_call_id}")
            if role == 'tool':
                content_preview = msg.get('content', '')[:500]
                print(f"     preview: {content_preview}")
        
        # Tüm conversation history'yi dosyaya yaz
        with open('test1_conversation_history.txt', 'w', encoding='utf-8') as f:
            for i, msg in enumerate(history):
                role = msg.get('role', 'unknown')
                content = msg.get('content', '')
                # tool_call_id sadece tool mesajları için geçerli
                tool_call_id = msg.get('tool_call_id', 'N/A') if role == 'tool' else 'N/A'
                f.write(f"Message {i+1}:\n")
                f.write(f"  role: {role}\n")
                f.write(f"  tool_call_id: {tool_call_id}\n")
                f.write(f"  content_len: {len(content)}\n")
                f.write(f"  content: {content[:1000]}\n")
                f.write("-" * 70 + "\n")
        print(f"Conversation history test1_conversation_history.txt dosyasına yazıldı.")
    except Exception as e:
        print(f"Hata: {e}")
    
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
        safe_error = result.error.encode('utf-8', errors='ignore').decode('utf-8')
        print(f"  Hata: {safe_error}")
    
    print(f"\nYanit:")
    print("-" * 70)
    safe_response = result.final_response.encode('utf-8', errors='ignore').decode('utf-8')
    print(safe_response)
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
        safe_error = result.error.encode('utf-8', errors='ignore').decode('utf-8')
        print(f"  Hata: {safe_error}")
    
    print(f"\nYanıt:")
    print("-" * 70)
    try:
        safe_response = result.final_response.encode('utf-8', errors='ignore').decode('utf-8')
        print(safe_response[:500])
    except Exception as e:
        print(f"[Yanıt yazdırılamadı: {e}]")
    print("-" * 70)
    
    print(f"\nTool çağrıları:")
    for i, call in enumerate(result.tool_calls):
        print(f"  {i+1}. Tool: {call.get('tool')}")
        print(f"     Argümanlar: {call.get('arguments')}")
        if call.get('tool') == 'read_file':
            tool_result = call.get('result', {})
            print(f"     Result keys: {list(tool_result.keys())}")
            # ToolRegistry.execute() result'ı 'result' key'i içinde döndürür
            actual_result = tool_result.get('result', {})
            print(f"     Actual result keys: {list(actual_result.keys())}")
            content = actual_result.get('content', '')
            print(f"     Dosya boyutu: {len(content)} karakter")
    
    file_read = any(call.get('tool') == 'read_file' for call in result.tool_calls)
    
    print(f"\nDosya okundu: {file_read}")
    
    # Conversation history kontrolü (dosya içeriği modele verildi mi?)
    print(f"\nOllama messages (ilk 1000 karakter):")
    ollama_messages = agent_loop.memory.get_messages()
    print(f"Message count: {len(ollama_messages)}")
    for i, msg in enumerate(ollama_messages[:3]):
        print(f"Message {i}: role={msg.get('role')}, content_len={len(msg.get('content', ''))}")
        print(f"Content preview: {msg.get('content', '')[:200]}")
    
    return {
        "task": user_task,
        "success": result.success,
        "iterations": result.iterations,
        "tool_calls_count": len(result.tool_calls),
        "file_read": file_read,
        "final_response": result.final_response
    }


def test_empty_response():
    """
    Boş model yanıtı testi - modelin çok kısa/belirsiz içerik döndürdüğü durum
    """
    print("\n" + "=" * 70)
    print("TEST 4: Belirsiz model yanıtı")
    print("=" * 70)
    
    ollama_client = OllamaClient()
    tool_registry = ToolRegistry()
    
    def approval_callback(tool_name: str, arguments: dict) -> bool:
        return True
    
    config = LoopConfig(max_iterations=3)
    agent_loop = AgentLoop(
        ollama_client=ollama_client,
        tool_registry=tool_registry,
        config=config,
        approval_callback=approval_callback
    )
    
    # Çok kısa ve belirsiz bir görev
    user_task = "x"
    
    print(f"\nGörev: '{user_task}' (belirsiz görev)")
    result = agent_loop.run(user_task)
    
    print(f"\nSonuc:")
    print(f"  Success: {result.success}")
    print(f"  İterasyon: {result.iterations}")
    print(f"  Tool çağrısı sayısı: {len(result.tool_calls)}")
    
    if result.error:
        print(f"  Hata: {result.error}")
    
    if result.final_response:
        print(f"  Final response: {result.final_response[:200]}")
    
    # Belirsiz görev için güvenli davranış: hata veya kısa yanıt
    assert result is not None, "Result None olmamalı"
    print(f"  ✓ Result None değil - güvenli davranış")
    
    return {
        "task": user_task,
        "success": result.success,
        "iterations": result.iterations,
        "tool_calls_count": len(result.tool_calls),
        "final_response": result.final_response,
        "error": result.error
    }


def test_max_iterations():
    """
    Maksimum iterasyon testi - modelin sürekli tool call yaparak iterasyon sınırına ulaşması
    """
    print("\n" + "=" * 70)
    print("TEST 5: Maksimum iterasyon")
    print("=" * 70)
    
    ollama_client = OllamaClient()
    tool_registry = ToolRegistry()
    
    def approval_callback(tool_name: str, arguments: dict) -> bool:
        return True
    
    # Düşük max_iterations ile test et
    config = LoopConfig(max_iterations=2)
    agent_loop = AgentLoop(
        ollama_client=ollama_client,
        tool_registry=tool_registry,
        config=config,
        approval_callback=approval_callback
    )
    
    # Modelin sürekli farklı dosyaları okumasını isteyen bir görev
    user_task = "app/ai/agent_loop.py dosyasını oku, sonra app/ai/conversation_memory.py dosyasını oku, sonra app/ai/ollama_client.py dosyasını oku, sonra app/tools/terminal_executor.py dosyasını oku"
    
    print(f"\nGörev: {user_task}")
    result = agent_loop.run(user_task)
    
    print(f"\nSonuc:")
    print(f"  Success: {result.success}")
    print(f"  İterasyon: {result.iterations}")
    print(f"  Tool çağrısı sayısı: {len(result.tool_calls)}")
    print(f"  Maksimum iterasyon: {config.max_iterations}")
    
    # Maksimum iterasyon aşıldıysa success False olmalı
    if result.iterations >= config.max_iterations:
        print(f"  Maksimum iterasyon aşıldı: {result.iterations} >= {config.max_iterations}")
        if not result.success:
            print(f"  ✓ Success doğru şekilde False olarak ayarlandı")
        else:
            print(f"  ✗ Success False olmalıydı ancak True - görev tamamlanmadı")
    else:
        print(f"  Maksimum iterasyon aşılmadı: {result.iterations} < {config.max_iterations}")
        print(f"  Model görevi erken tamamladı")
    
    return {
        "task": user_task,
        "success": result.success,
        "iterations": result.iterations,
        "tool_calls_count": len(result.tool_calls),
        "final_response": result.final_response,
        "max_iterations": config.max_iterations
    }


def test_tool_error():
    """
    Tool hatası testi
    """
    print("\n" + "=" * 70)
    print("TEST 6: Tool hatası")
    print("=" * 70)
    
    ollama_client = OllamaClient()
    tool_registry = ToolRegistry()
    
    def approval_callback(tool_name: str, arguments: dict) -> bool:
        return True
    
    config = LoopConfig(max_iterations=3)
    agent_loop = AgentLoop(
        ollama_client=ollama_client,
        tool_registry=tool_registry,
        config=config,
        approval_callback=approval_callback
    )
    
    user_task = "var_olmayan_bir_dosya_12345.txt dosyasını oku"
    
    print(f"\nGörev: {user_task}")
    result = agent_loop.run(user_task)
    
    print(f"\nSonuc:")
    print(f"  Success: {result.success}")
    print(f"  İterasyon: {result.iterations}")
    print(f"  Tool çağrısı sayısı: {len(result.tool_calls)}")
    
    if result.error:
        print(f"  Hata: {result.error}")
    
    return {
        "task": user_task,
        "success": result.success,
        "iterations": result.iterations,
        "tool_calls_count": len(result.tool_calls),
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
    
    # Test 4: boş model yanıtı
    try:
        result4 = test_empty_response()
        results.append(result4)
    except Exception as e:
        print(f"\nTEST 4 HATASI: {e}")
        import traceback
        traceback.print_exc()
        results.append({"task": "boş model yanıtı", "error": str(e)})
    
    # Test 5: maksimum iterasyon
    try:
        result5 = test_max_iterations()
        results.append(result5)
    except Exception as e:
        print(f"\nTEST 5 HATASI: {e}")
        import traceback
        traceback.print_exc()
        results.append({"task": "maksimum iterasyon", "error": str(e)})
    
    # Test 6: tool hatası
    try:
        result6 = test_tool_error()
        results.append(result6)
    except Exception as e:
        print(f"\nTEST 6 HATASI: {e}")
        import traceback
        traceback.print_exc()
        results.append({"task": "tool hatası", "error": str(e)})
    
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
