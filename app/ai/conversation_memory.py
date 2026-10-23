"""
MuhammedAI Local Developer - Conversation Memory
AI ile kullanıcı arasındaki mesaj geçmişini yönetir.
"""
import json
import re
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime, UTC
from enum import Enum


class MessagePriority(Enum):
    """Mesaj öncelik seviyeleri."""
    CRITICAL = 3
    HIGH = 2
    NORMAL = 1
    LOW = 0


@dataclass
class Message:
    """Tekil mesaj."""
    role: str  # "user", "assistant", "tool"
    content: str
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))
    metadata: Dict[str, Any] = field(default_factory=dict)
    priority: MessagePriority = MessagePriority.NORMAL
    importance: float = 1.0  # 0-1 arası importance score
    summary: Optional[str] = None  # Mesaj özeti (summarization için)


class ConversationMemory:
    """
    Mesaj geçmişini yönetir.

    Özellikler:
    - Mesaj ekleme
    - Token limitine göre kırpma
    - Context window yönetimi
    - Mesaj geçmişini alma
    - Conversation summarization
    - Message importance/priority
    - Export/import
    - Search/filter
    """

    def __init__(self, max_messages: int = 50, max_tokens: int = 8000):
        """
        Args:
            max_messages: Maksimum mesaj sayısı
            max_tokens: Tahmini token limiti (karakter bazlı yaklaşım)
        """
        self.max_messages = max_messages
        self.max_tokens = max_tokens
        self.messages: List[Message] = []

    def add_message(
        self,
        role: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None,
        priority: MessagePriority = MessagePriority.NORMAL
    ) -> None:
        """
        Mesaj ekler.

        Args:
            role: Mesaj rolü ("user", "assistant", "tool")
            content: Mesaj içeriği
            metadata: Ek meta veriler
            priority: Mesaj öncelik seviyesi
        """
        if not role or not isinstance(role, str):
            raise ValueError("Role geçerli bir string olmalıdır.")

        if not content or not isinstance(content, str):
            raise ValueError("Content geçerli bir string olmalıdır.")

        message = Message(
            role=role,
            content=content,
            metadata=metadata or {},
            priority=priority
        )

        self.messages.append(message)

        # Limitleri uygula
        self._apply_limits()

    def add_user_message(self, content: str) -> None:
        """Kullanıcı mesajı ekler."""
        self.add_message("user", content)

    def add_assistant_message(self, content: str, tool_calls=None, tool_call_ids=None) -> None:
        """AI asistan mesajı ekler."""
        metadata = {}
        if tool_calls:
            # Native tool_calls varsa, tool_call_id'leri sakla
            # tool_call_ids dışarıdan sağlanırsa kullan, yoksa oluştur
            if tool_call_ids is None:
                import uuid
                tool_call_ids = [f"call_{uuid.uuid4().hex[:8]}" for _ in tool_calls]
            
            metadata["tool_calls"] = tool_calls
            metadata["tool_call_ids"] = tool_call_ids
            metadata["has_native_tool_calls"] = True
        self.add_message("assistant", content, metadata=metadata)

    def add_tool_result(
        self,
        tool_name: str,
        result: Dict[str, Any],
        success: bool,
        tool_call_id: Optional[str] = None
    ) -> None:
        """
        Tool sonucunu mesaj olarak ekler.

        Args:
            tool_name: Çalıştırılan tool adı
            result: Tool sonucu
            success: Başarı durumu
            tool_call_id: Native tool call ID (varsa)
        """
        # Native tool calls için tool_call_id ile eşleşen format
        if tool_call_id:
            # Ollama formatında tool result - JSON formatında
            content = json.dumps(result, ensure_ascii=False)
        else:
            # Legacy format (metin tabanlı tool calls için)
            content = f"Tool: {tool_name}\n"
            content += f"Success: {success}\n"
            content += f"Result: {str(result)}"

        metadata = {
            "tool_name": tool_name,
            "success": success,
            "raw_result": result,
            "skip_limits": True  # Tool sonuçları silinmemeli
        }
        if tool_call_id:
            metadata["tool_call_id"] = tool_call_id

        self.add_message(
            "tool",
            content,
            metadata=metadata
        )

    def add_system_message(self, content: str) -> None:
        """Sistem mesajı ekler. System mesajları limit dışında tutulur."""
        if not content or not isinstance(content, str):
            raise ValueError("Content geçerli bir string olmalıdır.")
        
        message = Message(
            role="system",
            content=content,
            metadata={"skip_limits": True}  # System mesajları limit dışında
        )
        
        # System mesajları en başa ekle (öncelikli)
        self.messages.insert(0, message)

    def get_messages(self) -> List[Dict[str, str]]:
        """
        Mesajları Ollama formatında döndürür.

        Returns:
            List[Dict]: [{"role": "...", "content": "..."}]
        """
        ollama_messages = []
        last_assistant_had_tool_calls = False
        last_tool_call_ids = []

        for msg in self.messages:
            # System mesajları
            if msg.role == "system":
                ollama_messages.append({
                    "role": msg.role,
                    "content": msg.content
                })
            # Assistant mesajları
            elif msg.role == "assistant":
                ollama_msg = {
                    "role": msg.role,
                    "content": msg.content
                }
                # Native tool_calls varsa metadata'dan al
                if msg.metadata.get("has_native_tool_calls"):
                    tool_calls = msg.metadata.get("tool_calls", [])
                    tool_call_ids = msg.metadata.get("tool_call_ids", [])
                    if tool_calls:
                        ollama_msg["tool_calls"] = tool_calls
                        last_assistant_had_tool_calls = True
                        # Metadata'daki ID'leri kullan
                        last_tool_call_ids = tool_call_ids if tool_call_ids else []
                    else:
                        last_assistant_had_tool_calls = False
                        last_tool_call_ids = []
                else:
                    last_assistant_had_tool_calls = False
                    last_tool_call_ids = []
                ollama_messages.append(ollama_msg)
            # Tool mesajları
            elif msg.role == "tool":
                # Native tool_calls için tool_call_id ile eşleşen format
                tool_call_id = msg.metadata.get("tool_call_id")
                if tool_call_id:
                    # Ollama formatında tool result
                    ollama_messages.append({
                        "role": "tool",
                        "content": msg.content,
                        "tool_call_id": tool_call_id
                    })
                    # ID kullanıldı, listeden kaldır
                    if tool_call_id in last_tool_call_ids:
                        last_tool_call_ids.remove(tool_call_id)
                else:
                    # Legacy format (metin tabanlı)
                    ollama_messages.append({
                        "role": msg.role,
                        "content": msg.content
                    })
            else:
                # User mesajları vb.
                ollama_messages.append({
                    "role": msg.role,
                    "content": msg.content
                })

        return ollama_messages

    def get_conversation_text(self) -> str:
        """
        Tüm konuşmayı tek metin olarak döndürür.

        Returns:
            str: Konuşma metni
        """
        lines = []
        for msg in self.messages:
            lines.append(f"[{msg.role.upper()}]")
            lines.append(msg.content)
            lines.append("")

        return "\n".join(lines)

    def clear(self) -> None:
        """Mesaj geçmişini temizler."""
        self.messages.clear()

    def _apply_limits(self) -> None:
        """Mesaj limitlerini uygular. System mesajları limit dışında tutulur."""
        # System mesajlarını hariç tutarak mesaj sayısı limiti
        non_system_messages = [msg for msg in self.messages if not msg.metadata.get("skip_limits")]
        if len(non_system_messages) > self.max_messages:
            # En eski non-system mesajları sil
            system_messages = [msg for msg in self.messages if msg.metadata.get("skip_limits")]
            non_system_messages = non_system_messages[-self.max_messages:]
            self.messages = system_messages + non_system_messages

        # Token/karakter limiti (yaklaşık) - system mesajları hariç
        non_system_chars = sum(len(msg.content) for msg in self.messages if not msg.metadata.get("skip_limits"))
        if non_system_chars > self.max_tokens:
            # En eski non-system mesajlardan başlayarak sil
            system_messages = [msg for msg in self.messages if msg.metadata.get("skip_limits")]
            non_system_messages = [msg for msg in self.messages if not msg.metadata.get("skip_limits")]
            
            # Karakter limitini aşmayan kadar mesaj tut
            total = 0
            kept_messages = []
            for msg in reversed(non_system_messages):
                if total + len(msg.content) <= self.max_tokens:
                    kept_messages.insert(0, msg)
                    total += len(msg.content)
                else:
                    break
            
            self.messages = system_messages + kept_messages

    def get_stats(self) -> Dict[str, Any]:
        """
        İstatistikleri döndürür.

        Returns:
            Dict: Mesaj sayısı, toplam karakter vb.
        """
        return {
            "message_count": len(self.messages),
            "total_characters": sum(len(msg.content) for msg in self.messages),
            "by_role": {
                "user": sum(1 for msg in self.messages if msg.role == "user"),
                "assistant": sum(1 for msg in self.messages if msg.role == "assistant"),
                "tool": sum(1 for msg in self.messages if msg.role == "tool"),
            }
        }

    def trim_to_last_n(self, n: int) -> None:
        """
        Son n mesajı tutar, diğerlerini siler.

        Args:
            n: Tutulacak mesaj sayısı
        """
        if n < 1:
            self.clear()
        elif len(self.messages) > n:
            self.messages = self.messages[-n:]
    
    def summarize_conversation(self, max_length: int = 200) -> str:
        """
        Konuşmayı özetler.
        
        Args:
            max_length: Maksimum özet uzunluğu
            
        Returns:
            str: Konuşma özeti
        """
        if not self.messages:
            return "No conversation"
        
        # Basit özet: son 5 mesajın içeriğini birleştir
        recent_messages = self.messages[-5:]
        summary_parts = []
        
        for msg in recent_messages:
            role = msg.role.upper()
            content = msg.content[:50] + "..." if len(msg.content) > 50 else msg.content
            summary_parts.append(f"{role}: {content}")
        
        summary = " | ".join(summary_parts)
        
        if len(summary) > max_length:
            summary = summary[:max_length] + "..."
        
        return summary
    
    def calculate_importance(self, message: Message) -> float:
        """
        Mesaj importance hesaplar.
        
        Args:
            message: Mesaj
            
        Returns:
            float: Importance score (0-1)
        """
        importance = 0.5  # Base importance
        
        # Role bazlı importance
        if message.role == "user":
            importance += 0.3
        elif message.role == "assistant":
            importance += 0.2
        
        # Priority bazlı importance
        if message.priority == MessagePriority.CRITICAL:
            importance += 0.4
        elif message.priority == MessagePriority.HIGH:
            importance += 0.2
        elif message.priority == MessagePriority.LOW:
            importance -= 0.2
        
        # Content uzunluğu (uzun mesajlar daha önemli olabilir)
        if len(message.content) > 100:
            importance += 0.1
        
        return min(1.0, max(0.0, importance))
    
    def filter_messages(
        self,
        role: Optional[str] = None,
        min_priority: Optional[MessagePriority] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> List[Message]:
        """
        Mesajları filtreler.
        
        Args:
            role: Rol filtresi
            min_priority: Minimum priority
            start_time: Başlangıç zamanı
            end_time: Bitiş zamanı
            
        Returns:
            List[Message]: Filtrelenmiş mesajlar
        """
        filtered = self.messages
        
        if role:
            filtered = [m for m in filtered if m.role == role]
        
        if min_priority:
            filtered = [m for m in filtered if m.priority.value >= min_priority.value]
        
        if start_time:
            filtered = [m for m in filtered if m.timestamp >= start_time]
        
        if end_time:
            filtered = [m for m in filtered if m.timestamp <= end_time]
        
        return filtered
    
    def search_messages(self, query: str, role: Optional[str] = None) -> List[Message]:
        """
        Mesajlarda arama yapar.
        
        Args:
            query: Arama sorgusu
            role: Rol filtresi
            
        Returns:
            List[Message]: Eşleşen mesajlar
        """
        query_lower = query.lower()
        results = []
        
        for msg in self.messages:
            if role and msg.role != role:
                continue
            
            if query_lower in msg.content.lower():
                results.append(msg)
        
        return results
    
    def export_conversation(self, output_path: Optional[Path] = None) -> str:
        """
        Konuşmayı dışa aktar.
        
        Args:
            output_path: Çıktı dosyası yolu
            
        Returns:
            str: JSON string
        """
        data = {
            "exported_at": datetime.now(UTC).isoformat(),
            "message_count": len(self.messages),
            "messages": [
                {
                    "role": msg.role,
                    "content": msg.content,
                    "timestamp": msg.timestamp.isoformat(),
                    "metadata": msg.metadata,
                    "priority": msg.priority.name,
                    "importance": msg.importance,
                    "summary": msg.summary
                }
                for msg in self.messages
            ]
        }
        
        json_str = json.dumps(data, indent=2, ensure_ascii=False)
        
        if output_path:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(json_str)
        
        return json_str
    
    def import_conversation(self, input_path: Path) -> int:
        """
        Konuşmayı içe aktar.
        
        Args:
            input_path: Girdi dosyası yolu
            
        Returns:
            int: İçe aktarılan mesaj sayısı
        """
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        imported_count = 0
        
        for msg_data in data.get("messages", []):
            message = Message(
                role=msg_data["role"],
                content=msg_data["content"],
                timestamp=datetime.fromisoformat(msg_data["timestamp"]),
                metadata=msg_data.get("metadata", {}),
                priority=MessagePriority[msg_data.get("priority", "NORMAL")],
                importance=msg_data.get("importance", 1.0),
                summary=msg_data.get("summary")
            )
            self.messages.append(message)
            imported_count += 1
        
        return imported_count


if __name__ == "__main__":
    # Basit test
    memory = ConversationMemory(max_messages=10, max_tokens=1000)

    memory.add_user_message("Merhaba")
    memory.add_assistant_message("Selam, size nasıl yardımcı olabilirim?")
    memory.add_tool_result("test_tool", {"status": "ok"}, True)

    print("Mesaj sayısı:", len(memory.messages))
    print("İstatistikler:", memory.get_stats())
    print("\nKonuşma:")
    print(memory.get_conversation_text())

    print("\nConversationMemory basit testleri tamamlandı.")
