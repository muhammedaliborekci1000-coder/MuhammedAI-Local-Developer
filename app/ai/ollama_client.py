import ollama

from app.core.config import OLLAMA_HOST, DEFAULT_MODEL


class OllamaClient:

    def __init__(
        self,
        host: str = OLLAMA_HOST,
        model: str = DEFAULT_MODEL,
    ):
        self.host = host
        self.model = model
        self.client = ollama.Client(host=self.host)

    def chat(
        self,
        message: str,
        response_format=None,
        tools=None,
        messages=None,
    ) -> dict:
        """
        Ollama chat isteği yapar.
        
        Args:
            message: Kullanıcı mesajı (messages verilmezse kullanılır)
            response_format: JSON format şeması (opsiyonel)
            tools: Araç tanımları listesi (opsiyonel)
            messages: Mesaj listesi (opsiyonel, verilirse message kullanılmaz)
            
        Returns:
            dict: Yanıt içeren content ve tool_calls alanları
        """
        try:
            options = {
                "temperature": 0.1,
                "top_p": 0.8,
                "num_predict": 2000,
                "repeat_penalty": 1.15,
                "think": False,
            }

            # Messages listesi verilmişse kullan, yoksa tek message oluştur
            if messages:
                chat_messages = messages
            else:
                chat_messages = [
                    {
                        "role": "user",
                        "content": message,
                    }
                ]

            kwargs = {
                "model": self.model,
                "messages": chat_messages,
                "options": options,
            }

            if response_format is not None:
                kwargs["format"] = response_format
            
            if tools is not None:
                kwargs["tools"] = tools

            response = self.client.chat(**kwargs)

            # ChatResponse objesinden gerekli alanları al
            result = {
                "content": "",
                "tool_calls": None,
                "raw_response": response
            }
            
            # Content
            if hasattr(response.message, 'content') and response.message.content:
                content = response.message.content.strip()
                
                # Qwen3 bazı durumlarda düşünme metnini
                # content alanına koyabiliyor.
                # Gerçek cevap  sonrasındadır.
                if "</think>" in content:
                    content = content.split("</think>", 1)[1].strip()
                
                result["content"] = content
            
            # Tool calls
            if hasattr(response.message, 'tool_calls') and response.message.tool_calls:
                result["tool_calls"] = response.message.tool_calls
            
            # Thinking (fallback)
            if not result["content"] and hasattr(response.message, 'thinking') and response.message.thinking:
                thinking = response.message.thinking.strip()
                if "</think>" in thinking:
                    thinking = thinking.split("</think>", 1)[1].strip()
                result["content"] = thinking

            if not result["content"] and not result["tool_calls"]:
                result["content"] = "[AI boş cevap döndürdü]"

            return result

        except Exception as exc:
            return {
                "content": f"[Ollama hatası: {exc}]",
                "tool_calls": None,
                "error": str(exc)
            }
