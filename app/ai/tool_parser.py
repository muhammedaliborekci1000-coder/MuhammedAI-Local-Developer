"""
MuhammedAI Local Developer - Tool Parser
AI'dan gelen tool çağrılarını güvenli şekilde parse eder.
"""

import json
import re
from typing import Dict, Any, Optional, List
from dataclasses import dataclass


@dataclass
class ToolCall:
    """Parse edilmiş tool çağrısı."""
    name: str
    arguments: Dict[str, Any]
    raw_text: str


@dataclass
class ParseResult:
    """Parse sonucu."""
    success: bool
    tool_calls: List[ToolCall]
    error: Optional[str] = None
    raw_response: Optional[str] = None


class ToolParser:
    """
    AI'dan gelen tool çağrılarını parse eder.

    Qwen3 bazen düz metin içinde JSON döndürebilir.
    Parser toleranslıdır ancak belirsiz durumlarda güvenli davranır.
    """

    # Regex ile tool çağrısı adaylarını bulmak için desenler
    # Bu desenler sadece JSON bloğunu tespit eder, ayrıştırma json.loads ile yapılır
    TOOL_CALL_PATTERNS = [
        # Format: {"tool": "name", "arguments": {...}}
        r'\{["\']tool["\']\s*:\s*["\']([^"\']+)["\']\s*,\s*["\']arguments["\']\s*:\s*\{[^}]*\}\}',
        # Format: {"name": "tool_name", "params": {...}}
        r'\{["\']name["\']\s*:\s*["\']([^"\']+)["\']\s*,\s*["\']params["\']\s*:\s*\{[^}]*\}\}',
        # Format: {"tool_name": "...", "arguments": {...}}
        r'\{["\']tool_name["\']\s*:\s*["\']([^"\']+)["\']\s*,\s*["\']arguments["\']\s*:\s*\{[^}]*\}\}',
        # Format: {"function": "...", "parameters": {...}}
        r'\{["\']function["\']\s*:\s*["\']([^"\']+)["\']\s*,\s*["\']parameters["\']\s*:\s*\{[^}]*\}\}',
    ]

    def __init__(self):
        # Tüm desenleri derle
        self.compiled_patterns = [
            re.compile(pattern, re.DOTALL)
            for pattern in self.TOOL_CALL_PATTERNS
        ]

    def _extract_json_blocks(self, text: str) -> List[str]:
        """
        Metinden JSON bloklarını çıkarır.

        Regex ile JSON adaylarını bulur, sonra json.loads ile doğrular.
        """
        json_blocks = []

        # Önce tam JSON nesnelerini bulmaya çalış
        try:
            # Tüm metin tek bir JSON ise
            json.loads(text.strip())
            json_blocks.append(text.strip())
            return json_blocks
        except (json.JSONDecodeError, ValueError):
            pass

        # Regex ile JSON adaylarını bul
        for pattern in self.compiled_patterns:
            matches = pattern.finditer(text)
            for match in matches:
                candidate = match.group(0)
                json_blocks.append(candidate)

        # Ek olarak, {...} formatındaki blokları da dene
        brace_pattern = re.compile(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', re.DOTALL)
        for match in brace_pattern.finditer(text):
            candidate = match.group(0)
            if candidate not in json_blocks:
                json_blocks.append(candidate)

        return json_blocks

    def _parse_json_tool_call(self, json_str: str) -> Optional[ToolCall]:
        """
        JSON stringinden tool çağrısını parse eder.

        Güvenli: Geçersiz JSON veya eksik alanlar durumunda None döner.
        """
        try:
            data = json.loads(json_str)
        except (json.JSONDecodeError, ValueError):
            return None

        if not isinstance(data, dict):
            return None

        # Farklı olası alan adlarını destekle
        tool_name = None
        arguments = {}

        # Tool adı için olası alanlar
        for key in ["tool", "name", "tool_name", "function"]:
            if key in data and isinstance(data[key], str):
                tool_name = data[key]
                break

        if not tool_name:
            return None

        # Argümanlar için olası alanlar
        for key in ["arguments", "params", "parameters"]:
            if key in data and isinstance(data[key], dict):
                arguments = data[key]
                break

        # Tool adı ve argümanları doğrula
        if not isinstance(tool_name, str) or not tool_name.strip():
            return None

        if not isinstance(arguments, dict):
            return None

        return ToolCall(
            name=tool_name.strip(),
            arguments=arguments,
            raw_text=json_str
        )

    def parse(self, ai_response: str) -> ParseResult:
        """
        AI yanıtını parse eder ve tool çağrılarını çıkarır.

        Args:
            ai_response: AI'dan gelen metin yanıtı
        
        Returns:
            ParseResult: Başarı durumunu ve tool çağrılarını içerir
        """
        if not ai_response or not ai_response.strip():
            return ParseResult(
                success=True,
                tool_calls=[],
                raw_response=ai_response
            )

        # JSON bloklarını çıkar
        json_blocks = self._extract_json_blocks(ai_response)

        tool_calls = []
        parse_errors = []

        for json_block in json_blocks:
            tool_call = self._parse_json_tool_call(json_block)
            if tool_call:
                tool_calls.append(tool_call)
            else:
                # JSON bloğu var ama geçerli tool çağrısı değil
                # Bu normal olabilir (sadece bilgi içeren JSON)
                pass

        if not tool_calls:
            # Tool çağrısı bulunamadı, bu bir hata değil
            # AI sadece düz metin döndürmüş olabilir
            return ParseResult(
                success=True,
                tool_calls=[],
                raw_response=ai_response
            )

        return ParseResult(
            success=True,
            tool_calls=tool_calls,
            raw_response=ai_response
        )

    def validate_tool_call(self, tool_call: ToolCall, available_tools: set) -> bool:
        """
        Tool çağrısının geçerli olup olmadığını kontrol eder.

        Args:
            tool_call: Doğrulanacak tool çağrısı
            available_tools: Mevcut tool adları set'i
        
        Returns:
            bool: Tool çağrısı geçerliyse True
        """
        if not tool_call.name or not tool_call.name.strip():
            return False

        if tool_call.name not in available_tools:
            return False

        # Argümanların güvenli olduğunu kontrol et
        # Şimdilik sadece dict olduğunu kontrol ediyoruz
        if not isinstance(tool_call.arguments, dict):
            return False

        return True


if __name__ == "__main__":
    # Basit test
    parser = ToolParser()

    # Test 1: Düz metin
    result = parser.parse("Bu sadece bir metin.")
    print(f"Test 1: {result.success}, tool_calls: {len(result.tool_calls)}")

    # Test 2: JSON tool çağrısı
    result = parser.parse('{"tool": "read_file", "arguments": {"file": "test.py"}}')
    print(f"Test 2: {result.success}, tool_calls: {len(result.tool_calls)}")
    if result.tool_calls:
        print(f"  Tool: {result.tool_calls[0].name}")

    # Test 3: Metin içinde JSON
    result = parser.parse('Lütfen dosyayı oku: {"tool": "search_code", "arguments": {"query": "test"}}')
    print(f"Test 3: {result.success}, tool_calls: {len(result.tool_calls)}")
    if result.tool_calls:
        print(f"  Tool: {result.tool_calls[0].name}")

    print("ToolParser basit testleri tamamlandı.")
