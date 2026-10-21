"""
MuhammedAI Local Developer - Conversation Memory
AI ile kullanıcı arasındaki mesaj geçmişini yönetir.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime, UTC


@dataclass
class Message:
    """Tekil mesaj."""
    role: str  # "user", "assistant", "tool"
    content: str
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))
    metadata: Dict[str, Any] = field(default_factory=dict)


class ConversationMemory:
    """
    Mesaj geçmişini yönetir.

    Özellikler:
    - Mesaj ekleme
    - Token limitine göre kırpma
    - Context window yönetimi
    - Mesaj geçmişini alma
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
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Mesaj ekler.

        Args:
            role: Mesaj rolü ("user", "assistant", "tool")
            content: Mesaj içeriği
            metadata: Ek meta veriler
        """
        if not role or not isinstance(role, str):
            raise ValueError("Role geçerli bir string olmalıdır.")

        if not content or not isinstance(content, str):
            raise ValueError("Content geçerli bir string olmalıdır.")

        message = Message(
            role=role,
            content=content,
            metadata=metadata or {}
        )

        self.messages.append(message)

        # Limitleri uygula
        self._apply_limits()

    def add_user_message(self, content: str) -> None:
        """Kullanıcı mesajı ekler."""
        self.add_message("user", content)

    def add_assistant_message(self, content: str, tool_calls=None) -> None:
        """AI asistan mesajı ekler."""
        metadata = {}
        if tool_calls:
            metadata["tool_calls"] = tool_calls
        self.add_message("assistant", content, metadata=metadata)

    def add_tool_result(
        self,
        tool_name: str,
        result: Dict[str, Any],
        success: bool
    ) -> None:
        """
        Tool sonucunu mesaj olarak ekler.

        Args:
            tool_name: Çalıştırılan tool adı
            result: Tool sonucu
            success: Başarı durumu
        """
        content = f"Tool: {tool_name}\n"
        content += f"Success: {success}\n"
        content += f"Result: {str(result)}"

        self.add_message(
            "tool",
            content,
            metadata={
                "tool_name": tool_name,
                "success": success,
                "raw_result": result
            }
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
        return [
            {
                "role": msg.role,
                "content": msg.content
            }
            for msg in self.messages
        ]

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
