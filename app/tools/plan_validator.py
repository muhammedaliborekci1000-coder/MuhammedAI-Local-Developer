import ast

from app.tools.file_reader import FileReader


class PlanValidator:

    REQUIRED_FIELDS = [
        "file",
        "function",
        "problem",
        "change",
        "old_code",
        "new_code",
        "reason",
    ]

    def __init__(self):
        self.reader = FileReader()

    def validate(self, plan: dict) -> dict:

        result = {
            "valid": False,
            "errors": [],
        }

        # 1. Plan formatı
        if not isinstance(plan, dict):
            result["errors"].append(
                "Plan dictionary formatında değil."
            )
            return result

        # 2. AI hata döndürmüş mü?
        if "error" in plan:
            result["errors"].append(
                plan.get(
                    "error",
                    "AI plan hatası.",
                )
            )
            return result

        # 3. Zorunlu alanlar
        missing_fields = [
            field
            for field in self.REQUIRED_FIELDS
            if field not in plan
        ]

        if missing_fields:
            result["errors"].append(
                "Eksik alanlar: "
                + ", ".join(missing_fields)
            )
            return result

        # 4. Alan tipleri ve boşluk kontrolü
        for field in self.REQUIRED_FIELDS:

            value = plan.get(field)

            if not isinstance(value, str):
                result["errors"].append(
                    f"{field} alanı metin olmalı."
                )
                continue

            if not value.strip():
                result["errors"].append(
                    f"{field} alanı boş olamaz."
                )

        if result["errors"]:
            return result

        # 5. Hedef dosyayı oku
        file_path = plan["file"]

        try:
            source_code = self.reader.read(
                file_path
            )

        except Exception as exc:
            result["errors"].append(
                f"Hedef dosya okunamadı: {exc}"
            )
            return result

        # 6. old_code kontrolü
        old_code = plan["old_code"]

        occurrences = source_code.count(
            old_code
        )

        if occurrences == 0:
            result["errors"].append(
                "old_code hedef dosyada bulunamadı."
            )

        elif occurrences > 1:
            result["errors"].append(
                f"old_code hedef dosyada "
                f"{occurrences} kez bulundu. "
                "Değişiklik belirsiz."
            )

        if result["errors"]:
            return result

        # 7. Aynı kod kontrolü
        new_code = plan["new_code"]

        if old_code == new_code:
            result["errors"].append(
                "old_code ve new_code aynı. "
                "Gerçek bir değişiklik bulunmuyor."
            )
            return result

        # 8. Gerçek dosya üzerinde aday değişiklik oluştur
        candidate_source = source_code.replace(
            old_code,
            new_code,
            1,
        )

        # UTF-8 BOM varsa syntax kontrolünden önce kaldır.
        candidate_source = candidate_source.lstrip("\ufeff")

        # 9. Aday dosyanın tamamını syntax kontrol et
        try:
            ast.parse(
                candidate_source,
                filename=file_path,
            )

        except SyntaxError as exc:
            result["errors"].append(
                "Değişiklik sonrası oluşacak dosyada "
                "Python syntax hatası var: "
                f"{exc.msg} "
                f"(satır {exc.lineno})"
            )

            return result

        # 10. Başarılı
        result["valid"] = True

        return result

