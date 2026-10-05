import json

from app.ai.ollama_client import OllamaClient
from app.tools.file_reader import FileReader


class ChangePlanner:

    def __init__(self):
        self.ai = OllamaClient()
        self.reader = FileReader()

    def create_plan(
        self,
        file_path: str,
        problem: str,
    ) -> dict:

        source_code = self.reader.read(file_path)

        schema = {
            "type": "object",
            "properties": {
                "file": {"type": "string"},
                "function": {"type": "string"},
                "problem": {"type": "string"},
                "change": {"type": "string"},
                "old_code": {"type": "string"},
                "new_code": {"type": "string"},
                "reason": {"type": "string"}
            },
            "required": [
                "file",
                "function",
                "problem",
                "change",
                "old_code",
                "new_code",
                "reason"
            ]
        }

        prompt = (
            "Sen MuhammedAI Local Developer'sın.\n\n"
            "Python kodunda güvenli ve minimal bir "
            "değişiklik planı hazırla.\n\n"

            f"DOSYA: {file_path}\n\n"

            "MEVCUT KOD:\n"
            "```python\n"
            f"{source_code}\n"
            "```\n\n"

            "TESPİT EDİLEN PROBLEM:\n"
            f"{problem}\n\n"

            "ÇOK ÖNEMLİ KURALLAR:\n"
            "1. Dosyayı değiştirme.\n"
            "2. Sadece problemi çözmek için gereken "
            "en küçük kod parçasını değiştir.\n"
            "3. old_code dosyada birebir bulunan gerçek "
            "kod olmalıdır.\n"
            "4. old_code sadece değiştirilecek küçük "
            "kod parçasını içermelidir.\n"
            "5. new_code old_code ile aynı kapsamda "
            "olmalıdır.\n"
            "6. Dosyanın geri kalanını old_code içine "
            "alma.\n"
            "7. new_code içinde değişiklikle ilgisi olmayan "
            "kodları tekrar etme.\n"
            "8. Mevcut kodu değiştirmeden önce verilen "
            "kaynak koddan birebir kontrol et.\n"
            "9. Tahmin yapma.\n"
            "10. Sadece JSON nesnesi döndür.\n\n"

            "ÖRNEK:\n"
            "Eğer gerçek kod:\n"
            "return a - b\n"
            "ise ve problem toplama yapılmasıysa:\n"
            "old_code = return a - b\n"
            "new_code = return a + b\n\n"

            "Bu örneği yalnızca format göstermek için "
            "kullan. Gerçek old_code değerini verilen "
            "dosyadan al."
        )

        response = self.ai.chat(
            prompt,
            response_format=schema,
        )

        try:
            plan = json.loads(response)

        except json.JSONDecodeError:
            return {
                "error": "AI geçerli JSON döndürmedi.",
                "raw_response": response,
            }

        required_fields = [
            "file",
            "function",
            "problem",
            "change",
            "old_code",
            "new_code",
            "reason",
        ]

        missing = [
            field
            for field in required_fields
            if field not in plan
        ]

        if missing:
            return {
                "error": "JSON planında zorunlu alanlar eksik.",
                "missing_fields": missing,
                "plan": plan,
            }

        return plan
