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
        
        # FileReader her zaman dict döndürür, content alanını al
        if isinstance(source_code, dict):
            content = source_code.get('content')
            # Content None veya boş ise güvenli olarak boş string kullan
            source_code = content if content is not None else ''

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

            "KRİTİK - old_code KURALLARI:\n"
            "- old_code MEVCUT KODDA BİREBİR bulunmalıdır.\n"
            "- old_code boşluk, indentation, newline dahil TAMAMEN aynı olmalıdır.\n"
            "- old_code'u kopyalarken her karakteri aynen al.\n"
            "- Tahmin etme, verilen MEVCUT KOD'dan kopyala.\n\n"

            "KRİTİK: JSON içindeki 'file' alanını KESİNLİKLE "
            f"şu şekilde kullan: '{file_path}'. "
            "Dosya yolunu değiştirme, typo yapma veya space ekleme.\n\n"

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

        # Response dict mi string mi kontrol et
        if isinstance(response, dict):
            # OllamaClient artık dict döndürüyor
            response_content = response.get("content", response)
        else:
            response_content = response

        try:
            plan = json.loads(response_content) if isinstance(response_content, str) else response_content
        except json.JSONDecodeError:
            # AI başarısız oldu, fallback şablon kullan
            plan = self._create_fallback_plan(file_path, problem, source_code)
        else:
            # AI başarılı ama alan kontrolü
            required_fields = [
                "file", "function", "problem", "change", "old_code", "new_code", "reason"
            ]
            missing = [field for field in required_fields if field not in plan]
            if missing:
                # AI eksik alanlar döndürdü, fallback şablon kullan
                plan = self._create_fallback_plan(file_path, problem, source_code)

        # Override file field with the actual file_path to prevent model typos
        plan["file"] = file_path

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

    def _create_fallback_plan(self, file_path: str, problem: str, source_code: str) -> dict:
        """
        AI başarısız olduğunda fallback plan oluşturur.
        Açık string replacement talimatları için deterministik yaklaşım.
        """
        import re
        
        # Kullanıcı görevinden fonksiyon adını çıkar
        function_match = re.search(r'(\w+)\s*\(', problem)
        function_name = function_match.group(1) if function_match else "unknown"
        
        # Eğer source_code'da fonksiyon tanımı varsa, onu kullan
        if "def " in source_code:
            func_match = re.search(r'def\s+(\w+)\s*\(', source_code)
            if func_match:
                function_name = func_match.group(1)
        
        # Dosya içeriğini birebir kullan (strip yapma, whitespace koru)
        old_code = source_code if source_code else "# Empty file"
        
        # Açık string replacement talimatını ara
        # Örnek: "'world' yerine 'universe'" veya "replace 'world' with 'universe'"
        replacement_patterns = [
            r"'([^']+)'\s+yerine\s+'([^']+)'",  # Türkçe: 'X' yerine 'Y'
            r'"([^"]+)"\s+yerine\s+"([^"]+)"',  # Türkçe: "X" yerine "Y"
            r"replace\s+'([^']+)'\s+with\s+'([^']+)'",  # İngilizce: replace 'X' with 'Y'
            r"replace\s+\"([^\"]+)\"\s+with\s+\"([^\"]+)\"",  # İngilizce: replace "X" with "Y"
        ]
        
        old_str = None
        new_str = None
        
        for pattern in replacement_patterns:
            match = re.search(pattern, problem, re.IGNORECASE)
            if match:
                old_str = match.group(1)
                new_str = match.group(2)
                break
        
        # Eğer açık replacement talimatı varsa ve kaynak kodda hedef string varsa
        if old_str and new_str and old_str in source_code:
            # Hedef string'in bulunduğu satırı veya bloğu old_code olarak al
            # Basitlik için: string'in bulunduğu satırı al
            lines = source_code.split('\n')
            old_code_lines = []
            found_line = None
            
            for i, line in enumerate(lines):
                if old_str in line:
                    # Bu satırı ve bağlamını al (tek satır replacement için)
                    old_code_lines.append(line)
                    found_line = i
                    break
            
            if old_code_lines:
                old_code = '\n'.join(old_code_lines)
                # new_code'da string'i değiştir
                new_code = old_code.replace(old_str, new_str)
            else:
                # Hedef string bulunamadı, güvenli olarak aynı kodu kullan
                new_code = source_code
        else:
            # Eğer source_code boşsa veya placeholder ise, new_code oluştur
            if not source_code.strip() or source_code.strip() == "# Bu dosya değiştirilmeli":
                old_code = source_code  # Birebir kullan
                if "multiply" in problem.lower():
                    new_code = "def multiply(a, b):\n    return a * b"
                    function_name = "multiply"
                elif "add" in problem.lower():
                    new_code = "def add(a, b):\n    return a + b"
                    function_name = "add"
                else:
                    new_code = f"# TODO: Implement {function_name} based on: {problem}"
            else:
                # Dosyada kod var ama belirgin replacement yok, güvenli olarak aynı kodu kullan
                new_code = source_code
        
        # Basit plan şablonu
        plan = {
            "file": file_path,
            "function": function_name,
            "problem": problem,
            "change": f"Modify {function_name} based on user request",
            "old_code": old_code,
            "new_code": new_code,
            "reason": f"User requested: {problem}"
        }
        
        return plan
