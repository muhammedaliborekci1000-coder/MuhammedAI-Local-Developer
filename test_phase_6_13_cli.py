"""
Phase 6.13 - Gerçek CLI inceleme testi
Deterministik dosya okuma
"""

import sys
import io
from app.ai.agent_loop import AgentLoop, LoopConfig
from app.ai.ollama_client import OllamaClient
from app.tools.tool_registry import ToolRegistry
from app.core.config import DEFAULT_MODEL, PROJECT_ROOT

# UTF-8 stdout
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def test_real_inspection_cli():
    """Gerçek CLI inceleme testi - Phase 6.13"""
    
    print("=" * 60)
    print("Phase 6.13 - Gerçek CLI İnceleme Testi")
    print("=" * 60)
    
    # Ollama bağlantısı kontrolü
    print("\n1. Ollama bağlantısı kontrol ediliyor...")
    try:
        ollama_client = OllamaClient(model=DEFAULT_MODEL)
        print(f"   ✓ Ollama bağlantısı başarılı: {DEFAULT_MODEL}")
    except Exception as e:
        print(f"   ✗ Ollama bağlantı hatası: {e}")
        return
    
    # ToolRegistry oluştur
    print("\n2. ToolRegistry oluşturuluyor...")
    try:
        tool_registry = ToolRegistry()
        print("   ✓ ToolRegistry oluşturuldu")
    except Exception as e:
        print(f"   ✗ ToolRegistry hatası: {e}")
        return
    
    # AgentLoop oluştur
    print("\n3. AgentLoop oluşturuluyor...")
    config = LoopConfig(max_iterations=5)
    agent_loop = AgentLoop(
        ollama_client=ollama_client,
        tool_registry=tool_registry,
        config=config,
        approval_callback=None
    )
    print("   ✓ AgentLoop oluşturuldu")
    
    # İnceleme görevi
    user_task = "app/ai/agent_loop.py dosyasını incele. Hiçbir dosyayı değiştirme. Olası bir mantık hatasını gerçek kod kanıtıyla açıkla ve düzeltme öner. Hata tespit edemezsen bunu açıkça söyle."
    
    print(f"\n4. Görev çalıştırılıyor:")
    print(f"   Görev: {user_task}")
    print()
    
    # Görevi çalıştır
    result = agent_loop.run(user_task)
    
    # Sonuçları yazdır
    print("\n" + "=" * 60)
    print("SONUÇLAR")
    print("=" * 60)
    print(f"\nBaşarı: {result.success}")
    print(f"İterasyon: {result.iterations}")
    print(f"Tool çağrısı sayısı: {len(result.tool_calls)}")
    
    if result.error:
        print(f"Hata: {result.error}")
    
    print("\nTool çağrı logu:")
    for i, call in enumerate(result.tool_calls, 1):
        print(f"  {i}. Tool: {call.get('tool')}")
        print(f"     Arguments: {call.get('arguments')}")
        print(f"     Success: {call.get('result', {}).get('success')}")
    
    print("\nFinal Response:")
    print("-" * 60)
    print(result.final_response)
    print("-" * 60)
    
    # Hedef dosya doğrulaması
    print("\n" + "=" * 60)
    print("HEDEF DOSYA DOĞRULAMASI")
    print("=" * 60)
    
    target_file = "app/ai/agent_loop.py"
    
    # Dosya değişikliği kontrolü
    print("\nDosya değişikliği kontrolü:")
    file_modified = any(
        call.get("tool") in ["write_file", "edit_file", "create_file", "delete_file"]
        for call in result.tool_calls
    )
    if file_modified:
        print("✗ Dosya değişikliği yapıldı (beklenmeyen)")
    else:
        print("✓ Dosya değişikliği yapılmadı (beklenen)")
    
    # İlgisiz araç kontrolü
    print("\nİlgisiz araç kontrolü:")
    irrelevant_tools = ["start_web_preview", "stop_web_preview", "run_python_file"]
    used_irrelevant = []
    for call in result.tool_calls:
        tool = call.get("tool")
        if tool in irrelevant_tools:
            used_irrelevant.append(tool)
    
    if used_irrelevant:
        print(f"✗ İlgisiz araçlar kullanıldı: {used_irrelevant}")
    else:
        print("✓ İlgisiz araçlar kullanılmadı (beklenen)")
    
    # Ön okuma başarısı
    print("\nÖn okuma başarısı:")
    if result.success:
        print("✓ Hedef dosya ön okuma başarılı")
    else:
        print("✗ Hedef dosya ön okuma başarısız")
    
    print("\n" + "=" * 60)
    print("TEST TAMAMLANDI")
    print("=" * 60)

if __name__ == "__main__":
    test_real_inspection_cli()
