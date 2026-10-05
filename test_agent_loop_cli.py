"""
MuhammedAI Local Developer - AgentLoop CLI Test Script
AgentLoop'u CLI üzerinden test etmek için basit arayüz.
"""

from app.ai.developer_agent import DeveloperAgent


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
    print("Argümanlar:")
    for key, value in arguments.items():
        print(f"  {key}: {value}")
    print("=" * 60)

    while True:
        response = input("Bu işlemi onaylıyor musunuz? (y/n): ").strip().lower()
        if response in ['y', 'yes', 'evet']:
            return True
        elif response in ['n', 'no', 'hayır']:
            return False
        else:
            print("Lütfen 'y' (evet) veya 'n' (hayır) girin.")


def main():
    print("=" * 70)
    print("MUHAMMEDAI LOCAL DEVELOPER - AGENT LOOP CLI TEST")
    print("=" * 70)

    # Agent'ı onay callback ile başlat
    agent = DeveloperAgent(approval_callback=approval_callback)

    print("\nAgent başlatıldı.")
    print("Mevcut araçlar:", agent.registry.list_tools())
    print()

    # Kullanıcıdan görev al
    task = input("Görevinizi girin (veya 'çıkış' yazın): ").strip()

    if task.lower() in ['çıkış', 'exit', 'quit']:
        print("Çıkılıyor...")
        return

    print("\nGörev çalıştırılıyor...")
    print("-" * 70)

    # Görevi çalıştır
    result = agent.run_task(task)

    # Sonuçları göster
    print("\n" + "=" * 70)
    print("SONUÇ")
    print("=" * 70)
    print(f"Başarı: {result.success}")
    print(f"İterasyon: {result.iterations}")
    print(f"Tool çağrısı sayısı: {len(result.tool_calls)}")

    if result.error:
        print(f"Hata: {result.error}")

    print("\nFinal Cevap:")
    print("-" * 70)
    print(result.final_response)
    print("-" * 70)

    # Tool çağrı logunu göster
    if result.tool_calls:
        print("\nTool Çağrı Logu:")
        print("-" * 70)
        for i, log in enumerate(result.tool_calls, 1):
            print(f"{i}. Tool: {log['tool']}")
            print(f"   Iteration: {log['iteration']}")
            print(f"   Arguments: {log['arguments']}")
            print(f"   Result: {log['result']}")
            print()

    # Konuşma geçmişini göster
    print("\nKonuşma Geçmişi:")
    print("-" * 70)
    history = agent.get_conversation_history()
    for msg in history:
        print(f"[{msg['role'].upper()}]")
        print(msg['content'][:200] + "..." if len(msg['content']) > 200 else msg['content'])
        print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nKullanıcı tarafından iptal edildi.")
    except Exception as e:
        print(f"\nHata: {e}")
        import traceback
        traceback.print_exc()
