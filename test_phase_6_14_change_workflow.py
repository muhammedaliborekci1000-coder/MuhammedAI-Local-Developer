"""
Phase 6.14 - Kod değiştirme iş akışı doğrulama testi
Geçici test çalışma alanında güvenli kod değişikliği
"""

import sys
import io
import os
from pathlib import Path
from app.ai.agent_loop import AgentLoop, LoopConfig
from app.ai.ollama_client import OllamaClient
from app.tools.tool_registry import ToolRegistry
from app.core.config import DEFAULT_MODEL, PROJECT_ROOT

# UTF-8 stdout
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def test_change_workflow():
    """Kod değiştirme iş akışı doğrulama - Phase 6.14"""
    
    print("=" * 60)
    print("Phase 6.14 - Kod Değiştirme İş Akışı Doğrulama")
    print("=" * 60)
    
    # Geçici test çalışma alanı oluştur
    test_workspace = Path(PROJECT_ROOT) / "temp_test_workspace"
    test_workspace.mkdir(exist_ok=True)
    
    test_file = test_workspace / "test_target.py"
    test_file.write_text("# Test dosyası\ndef hello():\n    return 'world'\n")
    
    print(f"\n1. Geçici test çalışma alanı oluşturuldu: {test_file}")
    
    # Ollama bağlantısı kontrolü
    print("\n2. Ollama bağlantısı kontrol ediliyor...")
    try:
        ollama_client = OllamaClient(model=DEFAULT_MODEL)
        print(f"   ✓ Ollama bağlantısı başarılı: {DEFAULT_MODEL}")
    except Exception as e:
        print(f"   ✗ Ollama bağlantı hatası: {e}")
        # Temizle
        test_file.unlink(missing_ok=True)
        test_workspace.rmdir()
        return
    
    # ToolRegistry oluştur
    print("\n3. ToolRegistry oluşturuluyor...")
    try:
        tool_registry = ToolRegistry()
        print("   ✓ ToolRegistry oluşturuldu")
    except Exception as e:
        print(f"   ✗ ToolRegistry hatası: {e}")
        # Temizle
        test_file.unlink(missing_ok=True)
        test_workspace.rmdir()
        return
    
    # AgentLoop oluştur
    print("\n4. AgentLoop oluşturuluyor...")
    config = LoopConfig(max_iterations=5)
    
    # Açık onay callback'i - her zaman True döndürür
    def approval_callback(tool_name: str, arguments: dict) -> bool:
        print(f"   Onay istendi: {tool_name}")
        print(f"   Onay veriliyor...")
        return True
    
    agent_loop = AgentLoop(
        ollama_client=ollama_client,
        tool_registry=tool_registry,
        config=config,
        approval_callback=approval_callback  # Açık onay mekanizması
    )
    print("   ✓ AgentLoop oluşturuldu")
    
    # Kod değiştirme görevi
    user_task = f"temp_test_workspace/test_target.py dosyasındaki hello fonksiyonunu değiştir. 'world' yerine 'universe' döndürsün."
    
    print(f"\n5. Görev çalıştırılıyor:")
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
    
    # Dosya değişikliği kontrolü
    print("\n" + "=" * 60)
    print("DOSYA DEĞİŞİKLİĞİ DOĞRULAMASI")
    print("=" * 60)
    
    # Dosyanın değişip değişmediğini kontrol et
    current_content = test_file.read_text()
    original_content = "# Test dosyası\ndef hello():\n    return 'world'\n"
    
    print("\nOrijinal içerik:")
    print(original_content)
    print("\nGüncel içerik:")
    print(current_content)
    
    if current_content != original_content:
        print("✓ Dosya değişikliği yapıldı")
    else:
        print("✗ Dosya değişikliği yapılmadı")
    
    # Yedek dosyası kontrolü
    print("\nYedek dosyası kontrolü:")
    backup_dir = Path(PROJECT_ROOT) / ".muhammedai_backups"
    if backup_dir.exists():
        backup_files = list(backup_dir.rglob("test_target.py"))
        if backup_files:
            print(f"✓ Yedek dosyaları bulundu: {backup_files}")
        else:
            print("✗ Yedek dosyası bulunamadı")
    else:
        print("✗ Yedek dizini bulunamadı")
    
    # Temizle
    print("\n" + "=" * 60)
    print("TEMİZLEME")
    print("=" * 60)
    
    test_file.unlink(missing_ok=True)
    
    # Yedek dosyalarını temizle
    backup_dir = Path(PROJECT_ROOT) / ".muhammedai_backups"
    if backup_dir.exists():
        for backup in backup_dir.rglob("test_target.py"):
            backup.unlink(missing_ok=True)
    
    # Tüm dosyaları temizle
    for item in test_workspace.iterdir():
        if item.is_file():
            item.unlink(missing_ok=True)
    
    try:
        test_workspace.rmdir()
        print("✓ Geçici dosyalar temizlendi")
    except OSError as e:
        print(f"⚠ Dizin temizlenemedi: {e}")
        print("  Manuel temizleme gerekebilir.")
    
    print("\n" + "=" * 60)
    print("TEST TAMAMLANDI")
    print("=" * 60)

if __name__ == "__main__":
    test_change_workflow()
