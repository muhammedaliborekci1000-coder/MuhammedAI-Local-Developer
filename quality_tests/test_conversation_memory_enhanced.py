"""
Quality Test: Enhanced Conversation Memory
Conversation memory gelişmiş özellikleri testleri.
"""

import sys
import os
import tempfile
import shutil
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.ai.conversation_memory import (
    ConversationMemory,
    MessagePriority
)


def test_message_priority():
    """
    Test: Message priority.
    """
    print("=" * 70)
    print("TEST: Message Priority")
    print("=" * 70)
    
    memory = ConversationMemory()
    
    # Farklı priority'ler ile mesaj ekle
    memory.add_message("user", "Critical message", priority=MessagePriority.CRITICAL)
    memory.add_message("user", "Normal message", priority=MessagePriority.NORMAL)
    memory.add_message("user", "Low priority message", priority=MessagePriority.LOW)
    
    # Priority kontrolü
    assert len(memory.messages) == 3, "3 mesaj olmalı"
    assert memory.messages[0].priority == MessagePriority.CRITICAL, "İlk mesaj CRITICAL olmalı"
    assert memory.messages[1].priority == MessagePriority.NORMAL, "İkinci mesaj NORMAL olmalı"
    assert memory.messages[2].priority == MessagePriority.LOW, "Üçüncü mesaj LOW olmalı"
    
    print(f"  Messages: {len(memory.messages)}")
    print(f"  Priorities: {[m.priority.name for m in memory.messages]}")
    
    print("\n" + "=" * 70)
    print("PASS: Message priority")
    print("=" * 70)


def test_conversation_summarization():
    """
    Test: Conversation summarization.
    """
    print("=" * 70)
    print("TEST: Conversation Summarization")
    print("=" * 70)
    
    memory = ConversationMemory()
    
    # Mesajlar ekle
    memory.add_user_message("Merhaba, nasılsın?")
    memory.add_assistant_message("İyiyim, teşekkürler!")
    memory.add_user_message("Python öğrenmek istiyorum")
    memory.add_assistant_message("Harika, nereden başlamak istersin?")
    
    # Özet al
    summary = memory.summarize_conversation(max_length=200)
    
    assert summary != "No conversation", "Özet olmalı"
    assert len(summary) > 0, "Özet boş olmamalı"
    print(f"  Summary: {summary}")
    
    print("\n" + "=" * 70)
    print("PASS: Conversation summarization")
    print("=" * 70)


def test_importance_calculation():
    """
    Test: Importance calculation.
    """
    print("=" * 70)
    print("TEST: Importance Calculation")
    print("=" * 70)
    
    memory = ConversationMemory()
    
    # User mesajı ekle
    memory.add_user_message("Bu çok önemli bir mesaj")
    user_msg = memory.messages[-1]
    
    # Importance hesapla
    importance = memory.calculate_importance(user_msg)
    
    assert 0.0 <= importance <= 1.0, "Importance 0-1 arası olmalı"
    print(f"  User message importance: {importance}")
    
    # Assistant mesajı ekle
    memory.add_assistant_message("Cevap")
    assistant_msg = memory.messages[-1]
    
    importance2 = memory.calculate_importance(assistant_msg)
    print(f"  Assistant message importance: {importance2}")
    
    # Critical priority mesaj
    memory.add_message("user", "Critical", priority=MessagePriority.CRITICAL)
    critical_msg = memory.messages[-1]
    
    importance3 = memory.calculate_importance(critical_msg)
    assert importance3 > importance, "Critical mesaj daha önemli olmalı"
    print(f"  Critical message importance: {importance3}")
    
    print("\n" + "=" * 70)
    print("PASS: Importance calculation")
    print("=" * 70)


def test_message_filtering():
    """
    Test: Message filtering.
    """
    print("=" * 70)
    print("TEST: Message Filtering")
    print("=" * 70)
    
    memory = ConversationMemory()
    
    # Mesajlar ekle
    memory.add_user_message("User message 1")
    memory.add_assistant_message("Assistant message 1")
    memory.add_message("user", "User message 2", priority=MessagePriority.HIGH)
    memory.add_assistant_message("Assistant message 2")
    
    # Role filtresi
    user_messages = memory.filter_messages(role="user")
    assert len(user_messages) == 2, "2 user mesajı olmalı"
    print(f"  User messages: {len(user_messages)}")
    
    # Priority filtresi
    high_priority = memory.filter_messages(min_priority=MessagePriority.HIGH)
    assert len(high_priority) >= 1, "En az 1 HIGH priority mesaj olmalı"
    print(f"  High priority messages: {len(high_priority)}")
    
    print("\n" + "=" * 70)
    print("PASS: Message filtering")
    print("=" * 70)


def test_message_search():
    """
    Test: Message search.
    """
    print("=" * 70)
    print("TEST: Message Search")
    print("=" * 70)
    
    memory = ConversationMemory()
    
    # Mesajlar ekle
    memory.add_user_message("Python öğrenmek istiyorum")
    memory.add_assistant_message("Python harika bir dil")
    memory.add_user_message("JavaScript de öğrenmek istiyorum")
    memory.add_assistant_message("JavaScript de önemli")
    
    # Arama
    results = memory.search_messages("Python")
    assert len(results) > 0, "Python araması sonuç döndürmeli"
    print(f"  'Python' search results: {len(results)}")
    
    # Role ile arama
    user_results = memory.search_messages("öğrenmek", role="user")
    assert len(user_results) > 0, "User araması sonuç döndürmeli"
    print(f"  User 'öğrenmek' search results: {len(user_results)}")
    
    print("\n" + "=" * 70)
    print("PASS: Message search")
    print("=" * 70)


def test_export_import():
    """
    Test: Export/import conversation.
    """
    print("=" * 70)
    print("TEST: Export/Import Conversation")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp(prefix="muhammedai_test_")
    
    try:
        # Memory oluştur ve mesaj ekle
        memory1 = ConversationMemory()
        memory1.add_user_message("Test message 1")
        memory1.add_assistant_message("Test response 1")
        memory1.add_message("user", "Test message 2", priority=MessagePriority.HIGH)
        
        # Export
        export_path = Path(temp_dir) / "conversation.json"
        json_str = memory1.export_conversation(export_path)
        
        assert export_path.exists(), "Export dosyası oluşturulmalı"
        print(f"  Export path: {export_path}")
        print(f"  Export size: {len(json_str)}")
        
        # Yeni memory oluştur
        memory2 = ConversationMemory()
        
        # Import
        imported = memory2.import_conversation(export_path)
        
        assert imported > 0, "Import başarılı olmalı"
        assert len(memory2.messages) > 0, "Mesajlar yüklenmeli"
        print(f"  Imported messages: {imported}")
        print(f"  Total messages after import: {len(memory2.messages)}")
        
        # İçerik kontrolü
        assert memory2.messages[0].content == "Test message 1", "İçerik eşleşmeli"
        assert memory2.messages[2].priority == MessagePriority.HIGH, "Priority yüklenmeli"
        
        print("\n" + "=" * 70)
        print("PASS: Export/import conversation")
        print("=" * 70)
        
    finally:
        shutil.rmtree(temp_dir)


def test_enhanced_stats():
    """
    Test: Enhanced statistics.
    """
    print("=" * 70)
    print("TEST: Enhanced Statistics")
    print("=" * 70)
    
    memory = ConversationMemory()
    
    # Mesajlar ekle
    memory.add_user_message("User 1")
    memory.add_assistant_message("Assistant 1")
    memory.add_message("user", "User 2", priority=MessagePriority.HIGH)
    memory.add_tool_result("test_tool", {"result": "ok"}, True)
    
    # Stats al
    stats = memory.get_stats()
    
    assert stats["message_count"] == 4, "4 mesaj olmalı"
    assert stats["by_role"]["user"] == 2, "2 user mesajı olmalı"
    assert stats["by_role"]["assistant"] == 1, "1 assistant mesajı olmalı"
    assert stats["by_role"]["tool"] == 1, "1 tool mesajı olmalı"
    
    print(f"  Message count: {stats['message_count']}")
    print(f"  By role: {stats['by_role']}")
    print(f"  Total characters: {stats['total_characters']}")
    
    print("\n" + "=" * 70)
    print("PASS: Enhanced statistics")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_message_priority()
        test2 = test_conversation_summarization()
        test3 = test_importance_calculation()
        test4 = test_message_filtering()
        test5 = test_message_search()
        test6 = test_export_import()
        test7 = test_enhanced_stats()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Message Priority: {'PASS' if test1 else 'FAIL'}")
        print(f"Conversation Summarization: {'PASS' if test2 else 'FAIL'}")
        print(f"Importance Calculation: {'PASS' if test3 else 'FAIL'}")
        print(f"Message Filtering: {'PASS' if test4 else 'FAIL'}")
        print(f"Message Search: {'PASS' if test5 else 'FAIL'}")
        print(f"Export/Import: {'PASS' if test6 else 'FAIL'}")
        print(f"Enhanced Statistics: {'PASS' if test7 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7])
        print(f"\nTOPLAM: {'PASS' if all_passed else 'FAIL'}")
        print("=" * 70)
        
        sys.exit(0 if all_passed else 1)
    except Exception as e:
        print(f"\nTEST HATASI:")
        print("-" * 70)
        import traceback
        traceback.print_exc()
        print("=" * 70)
        sys.exit(1)
