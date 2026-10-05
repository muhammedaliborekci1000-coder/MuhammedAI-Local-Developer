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
    ) -> str:
        try:
            options = {
                "temperature": 0.1,
                "top_p": 0.8,
                "num_predict": 2000,
                "repeat_penalty": 1.15,
            }

            kwargs = {
                "model": self.model,
                "messages": [
                    {
                        "role": "user",
                        "content": message,
                    }
                ],
                "options": options,
                "think": False,
            }

            if response_format is not None:
                kwargs["format"] = response_format

            response = self.client.chat(**kwargs)

            message_data = response.get(
                "message",
                {}
            )

            content = message_data.get(
                "content",
                ""
            )

            if content:
                content = content.strip()

                # Qwen3 bazı durumlarda düşünme metnini
                # content alanına koyabiliyor.
                # Gerçek cevap </think> sonrasındadır.
                if "</think>" in content:
                    content = content.split(
                        "</think>",
                        1
                    )[1].strip()

                if content:
                    return content

            thinking = message_data.get(
                "thinking",
                ""
            )

            if thinking:
                thinking = thinking.strip()

                if "</think>" in thinking:
                    thinking = thinking.split(
                        "</think>",
                        1
                    )[1].strip()

                if thinking:
                    return thinking

            return "[AI boş cevap döndürdü]"

        except Exception as exc:
            return f"[Ollama hatası: {exc}]"
