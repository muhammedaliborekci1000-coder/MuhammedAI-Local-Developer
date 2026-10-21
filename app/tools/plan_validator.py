import ast
import re

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

    def _normalize_whitespace(self, text: str) -> str:
        """
        Normalize whitespace for fuzzy matching.
        - Strip trailing whitespace
        - Normalize leading indentation to single space for comparison
        - Collapse multiple spaces to single space
        """
        # Strip trailing whitespace
        normalized = text.rstrip()
        # Replace tabs with spaces
        normalized = normalized.replace('\t', ' ')
        # Collapse multiple spaces to single space
        normalized = re.sub(r' +', ' ', normalized)
        # Strip leading whitespace for content comparison
        # (but we'll preserve the original for the actual replacement)
        return normalized.lstrip()

    def _find_normalized_match(self, old_code: str, source_code: str) -> dict:
        """
        Try to find old_code in source_code using normalized whitespace matching.

        Returns:
            dict with keys:
            - found: bool
            - corrected_old_code: str (if found)
            - match_count: int
            - error: str (if not found or ambiguous)
        """
        import logging
        logger = logging.getLogger(__name__)

        old_normalized = self._normalize_whitespace(old_code)
        logger.info(f"Old code normalized: {repr(old_normalized)}")

        # Try multi-line matching first
        source_lines = source_code.split('\n')
        old_lines = old_code.split('\n')

        # If old_code is multi-line, try to find the exact sequence
        if len(old_lines) > 1:
            old_lines_normalized = [self._normalize_whitespace(line) for line in old_lines]
            logger.info(f"Multi-line old_code: {len(old_lines)} lines, normalized: {old_lines_normalized}")

            # Search for the sequence in source
            for i in range(len(source_lines) - len(old_lines) + 1):
                source_window = source_lines[i:i+len(old_lines)]
                source_window_normalized = [self._normalize_whitespace(line) for line in source_window]

                if source_window_normalized == old_lines_normalized:
                    # Found exact sequence match
                    corrected_old_code = '\n'.join(source_window)
                    logger.info(f"Multi-line match found at line {i}: {repr(corrected_old_code)}")
                    return {
                        "found": True,
                        "corrected_old_code": corrected_old_code,
                        "match_count": 1,
                        "error": None
                    }

            # Multi-line match not found
            logger.warning("Multi-line match not found")
            return {
                "found": False,
                "match_count": 0,
                "error": "old_code normalized match bulunamadı (multi-line)"
            }

        # Single-line matching
        candidates = []
        for i, line in enumerate(source_lines):
            line_normalized = self._normalize_whitespace(line)
            logger.debug(f"Line {i}: {repr(line)} -> normalized: {repr(line_normalized)}")
            if line_normalized == old_normalized:
                candidates.append(line)
                logger.info(f"Match found at line {i}: {repr(line)}")

        if len(candidates) == 0:
            logger.warning(f"No single-line matches found. Looking for: {repr(old_normalized)}")
            return {
                "found": False,
                "match_count": 0,
                "error": "old_code normalized match bulunamadı"
            }
        elif len(candidates) == 1:
            logger.info(f"Single unique match found: {repr(candidates[0])}")
            return {
                "found": True,
                "corrected_old_code": candidates[0],
                "match_count": 1,
                "error": None
            }
        else:
            logger.warning(f"Ambiguous match: {len(candidates)} candidates found")
            return {
                "found": False,
                "match_count": len(candidates),
                "error": f"old_code normalized eşleşmesi belirsiz: {len(candidates)} aday bulundu"
            }

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
            # Exact match failed, try normalized matching
            import logging
            logger = logging.getLogger(__name__)
            logger.info(f"Exact match failed for old_code, trying normalized matching...")

            normalized_result = self._find_normalized_match(old_code, source_code)

            if normalized_result["found"]:
                # Found unique normalized match - use corrected old_code
                corrected_old_code = normalized_result["corrected_old_code"]
                plan["old_code"] = corrected_old_code  # Update plan with corrected version
                plan["_old_code_corrected"] = True  # Mark as corrected
                logger.info(f"Normalized match found, corrected old_code to: {repr(corrected_old_code[:50])}...")
                # Verify the corrected version actually exists
                occurrences = source_code.count(corrected_old_code)
                if occurrences != 1:
                    result["errors"].append(
                        f"Corrected old_code beklenmedik şekilde {occurrences} kez bulundu."
                    )
                    return result
                # No unique normalized match found
                result["errors"].append(
                    f"old_code hedef dosyada bulunamadı. Expected: {repr(old_code[:100])}... "
                    f"({normalized_result['error']})"
                )
                return result

        elif occurrences > 1:
            result["errors"].append(
                f"old_code hedef dosyada "
                f"{occurrences} kez bulundu. "
                "Değişiklik belirsiz."
            )
            return result

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

