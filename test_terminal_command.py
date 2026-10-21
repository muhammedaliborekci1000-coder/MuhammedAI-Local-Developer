"""
Terminal Komut Testi
execute_terminal_command aracının doğru çalıştığını doğrular.
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


def test_terminal_command():
    """
    Terminal komutu testi - git status
    """
    print("=" * 60)
    print("Terminal Komut Testi - git status")
    print("=" * 60)
    
    # Ollama bağlantısı kontrol et
    try:
        ollama_client = OllamaClient()
        ollama_client.chat("test")
        print("1. [OK] Ollama baglantisi basarili")
    except Exception as e:
        print(f"1. [FAIL] Ollama baglanti hatasi: {e}")
        return False
    
    # ToolRegistry oluştur
    try:
        tool_registry = ToolRegistry()
        print("2. [OK] ToolRegistry olusturuldu")
    except Exception as e:
        print(f"2. [FAIL] ToolRegistry hatasi: {e}")
        return False
    
    # Terminal aracı kayıtlı mı kontrol et
    if "execute_terminal_command" in tool_registry.tools:
        print("3. [OK] execute_terminal_command aracı kayıtlı")
    else:
        print("3. [FAIL] execute_terminal_command aracı kayıtlı değil")
        return False
    
    # Onay callback'i (her zaman onay ver)
    def approval_callback_approve(tool_name: str, arguments: dict) -> bool:
        print(f"  Onay istendi: {tool_name}")
        print(f"  Argümanlar: {arguments}")
        return True
    
    config = LoopConfig(max_iterations=5)
    agent_loop = AgentLoop(
        ollama_client=ollama_client,
        tool_registry=tool_registry,
        config=config,
        approval_callback=approval_callback_approve
    )
    
    user_task = "git status komutunu çalıştır ve sonucu göster."
    
    print(f"\n4. Görev çalıştırılıyor: {user_task}")
    result = agent_loop.run(user_task)
    
    print(f"\nSonuc: success={result.success}")
    print(f"İterasyon: {result.iterations}")
    print(f"Tool çağrısı sayısı: {len(result.tool_calls)}")
    
    if result.error:
        print(f"Hata: {result.error}")
    
    print(f"\nYanıt:")
    print("-" * 60)
    print(result.final_response)
    print("-" * 60)
    
    # Tool çağrısı yapıldı mı kontrol et
    if len(result.tool_calls) > 0:
        print(f"\n[OK] Tool çağrısı yapıldı: {len(result.tool_calls)}")
        
        # Git status çıktısı var mı kontrol et
        for call in result.tool_calls:
            if call.get('tool') == 'execute_terminal_command':
                tool_result = call.get('result', {})
                print(f"  Tool result success: {tool_result.get('success')}")
                
                # Tool result içindeki gerçek terminal sonucunu kontrol et
                if 'result' in tool_result:
                    actual_result = tool_result['result']
                    if actual_result.get('success'):
                        stdout = actual_result.get('stdout', '')
                        if 'git' in stdout.lower() or 'branch' in stdout.lower():
                            print("\n[OK] Git status çıktısı alındı")
                            print("Çıktı (ilk 500 karakter):")
                            print(stdout[:500])
                            return True
                        else:
                            print("\n[FAIL] Git status çıktısı beklenen formatta değil")
                            return False
                    else:
                        print(f"\n[FAIL] Terminal komutu başarısız: {actual_result.get('error')}")
                        return False
                else:
                    print("\n[FAIL] Tool result içinde 'result' alanı yok")
                    return False
        
        print("\n[FAIL] execute_terminal_command çağrısı bulunamadı")
        return False
    else:
        print("\n[FAIL] Tool çağrısı yapılmadı")
        return False


def test_terminal_command_direct():
    """
    Terminal aracını doğrudan test et
    """
    print("\n" + "=" * 60)
    print("Terminal Aracı Doğrudan Test")
    print("=" * 60)
    
    try:
        tool_registry = ToolRegistry()
        result = tool_registry._execute_terminal_command("git status")
        
        print(f"Komut: {result.get('command')}")
        print(f"Exit code: {result.get('exit_code')}")
        print(f"Success: {result.get('success')}")
        print(f"Stdout: {result.get('stdout')}")
        print(f"Stderr: {result.get('stderr')}")
        
        if result.get('success') and 'git' in result.get('stdout', '').lower():
            print("\n[OK] Doğrudan terminal aracı testi başarılı")
            return True
        else:
            print("\n[FAIL] Doğrudan terminal aracı testi başarısız")
            return False
    except Exception as e:
        print(f"\n[FAIL] Hata: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    print("=" * 60)
    print("Terminal Komut Testi")
    print("=" * 60)
    
    test1_pass = test_terminal_command_direct()
    test2_pass = test_terminal_command()
    
    print("\n" + "=" * 60)
    print("SONUCLAR")
    print("=" * 60)
    print(f"TEST 1 (Doğrudan): {'PASS' if test1_pass else 'FAIL'}")
    print(f"TEST 2 (AgentLoop): {'PASS' if test2_pass else 'FAIL'}")
    
    all_pass = test1_pass and test2_pass
    print(f"\nTOPLAM: {'PASS' if all_pass else 'FAIL'}")
    print("=" * 60)
    
    return all_pass


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\nTEST HATASI:")
        print("-" * 60)
        import traceback
        traceback.print_exc()
        print("=" * 60)
        sys.exit(1)
