"""
MuhammedAI Local Developer - CLI Başlatıcı
AI Developer Agent için terminal arayüzü.
"""

import sys
import ollama
from app.ai.ollama_client import OllamaClient
from app.ai.agent_loop import AgentLoop, LoopConfig
from app.tools.tool_registry import ToolRegistry
from app.core.config import OLLAMA_HOST, DEFAULT_MODEL


def check_ollama_connection(host: str = OLLAMA_HOST) -> bool:
    """Ollama bağlantısını kontrol et."""
    try:
        client = ollama.Client(host=host)
        client.list()
        return True
    except Exception as e:
        return False


def check_model(host: str = OLLAMA_HOST, model: str = DEFAULT_MODEL) -> bool:
    """Modelin mevcut olup olmadığını kontrol et."""
    try:
        client = ollama.Client(host=host)
        response = client.list()
        # response.models bir Model objeleri listesi, her Model'in 'model' attribute'u var
        model_names = [m.model.split(':')[0] for m in response.models]
        return model in model_names or model.split(':')[0] in model_names
    except Exception as e:
        return False


def approval_callback(tool_name: str, arguments: dict) -> bool:
    """
    CLI üzerinden kullanıcı onayı ister.
    
    Args:
        tool_name: Tool adı
        arguments: Tool argümanları
    
    Returns:
        bool: Kullanıcı onay verdiyse True
    """
    print("\n" + "=" * 60)
    print(f"ONAY İSTENİYOR: {tool_name}")
    print("=" * 60)
    
    # Eğer plan varsa detayları göster
    if 'plan' in arguments:
        plan = arguments['plan']
        print(f"  Dosya: {plan.get('file', 'Belirtilmemiş')}")
        print(f"  Fonksiyon: {plan.get('function', 'Belirtilmemiş')}")
        print(f"  Problem: {plan.get('problem', 'Belirtilmemiş')}")
        print(f"  Değişiklik: {plan.get('change', 'Belirtilmemiş')}")
        print(f"  Sebep: {plan.get('reason', 'Belirtilmemiş')}")
        print("\n  Eski kod:")
        print("  " + "-" * 56)
        for line in plan.get('old_code', '').split('\n'):
            print(f"  {line}")
        print("  " + "-" * 56)
        print("\n  Yeni kod:")
        print("  " + "-" * 56)
        for line in plan.get('new_code', '').split('\n'):
            print(f"  {line}")
        print("  " + "-" * 56)
    else:
        print("Argümanlar:")
        for key, value in arguments.items():
            print(f"  {key}: {value}")
    
    print("=" * 60)

    while True:
        response = input("Bu işlemi onaylıyor musunuz? (y/n): ").strip().lower()
        if response in ['y', 'yes', 'evet', 'e']:
            return True
        elif response in ['n', 'no', 'hayır', 'h']:
            return False
        else:
            print("Lütfen 'y' (evet) veya 'n' (hayır) girin.")


def main():
    print("=" * 70)
    print("MUHAMMEDAI LOCAL DEVELOPER - CLI")
    print("=" * 70)
    
    # Ollama bağlantısını kontrol et
    print(f"\nOllama bağlantısı kontrol ediliyor: {OLLAMA_HOST}")
    if not check_ollama_connection():
        print(f"HATA: Ollama sunucusuna bağlanılamadı.")
        print(f"Lütfen Ollama'nın çalıştığından emin olun: {OLLAMA_HOST}")
        print(f"Ollama kurulumu için: https://ollama.ai")
        sys.exit(1)
    print("✓ Ollama bağlantısı başarılı")
    
    # Model kontrolü
    print(f"\nModel kontrol ediliyor: {DEFAULT_MODEL}")
    if not check_model():
        print(f"HATA: Model bulunamadı: {DEFAULT_MODEL}")
        print(f"Mevcut modelleri görmek için: ollama list")
        print(f"Model indirmek için: ollama pull {DEFAULT_MODEL}")
        sys.exit(1)
    print(f"✓ Model mevcut: {DEFAULT_MODEL}")
    
    # AgentLoop'u başlat
    print("\nAgent başlatılıyor...")
    ollama_client = OllamaClient(host=OLLAMA_HOST, model=DEFAULT_MODEL)
    tool_registry = ToolRegistry()
    config = LoopConfig(max_iterations=10, enable_logging=True)
    
    # Onay callback - kullanıcı onayı isteniyor
    agent_loop = AgentLoop(
        ollama_client=ollama_client,
        tool_registry=tool_registry,
        config=config,
        approval_callback=approval_callback
    )
    
    print("✓ Agent başlatıldı")
    print(f"✓ Mevcut araçlar: {len(tool_registry.list_tools())}")
    print()
    
    # Ana döngü
    while True:
        try:
            # Kullanıcıdan görev al
            task = input("Görev (veya 'exit'/'quit' ile çıkış): ").strip()
            
            if task.lower() in ['exit', 'quit', 'çıkış']:
                print("\nÇıkılıyor...")
                break
            
            if not task:
                continue
            
            print("\nGörev çalıştırılıyor...")
            print("-" * 70)
            
            # Görevi çalıştır
            result = agent_loop.run(task)
            
            # Sonuçları göster
            print("\n" + "=" * 70)
            print("SONUÇ")
            print("=" * 70)
            print(f"Başarı: {result.success}")
            print(f"İterasyon: {result.iterations}")
            print(f"Tool çağrısı sayısı: {len(result.tool_calls)}")
            
            if result.error:
                print(f"Hata: {result.error}")
            
            print("\nYanıt:")
            print("-" * 70)
            print(result.final_response)
            print("-" * 70)
            
        except KeyboardInterrupt:
            print("\n\nKullanıcı tarafından iptal edildi.")
            break
        except Exception as e:
            print(f"\nHata: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    main()
