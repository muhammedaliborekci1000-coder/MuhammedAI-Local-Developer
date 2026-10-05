"""
Quality Test: AgentLoop Tool Retry Interaction
Amaç: Model geçerli bir tool çağrısı yaptığında no-tool retry mekanizmasının yanlışlıkla devreye girmediğini doğrula.
"""

import sys
import os
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

# Proje kök dizinini path'e ekle
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.ai.agent_loop import AgentLoop, LoopConfig, LoopResult
from app.ai.tool_parser import ToolCall, ParseResult
from app.tools.tool_registry import ToolRegistry, ToolDefinition


class MockOllamaClient:
    """Sahte OllamaClient - test için."""
    
    def __init__(self):
        self.call_count = 0
        self.responses = [
            # İlk çağrı: read_file tool çağrısı
            '{"tool": "read_file", "arguments": {"relative_path": "test_file.py"}}',
            # İkinci çağrı: normal final cevap
            "Dosya içeriği başarıyla okundu. Test tamamlandı."
        ]
    
    def chat(self, prompt: str) -> str:
        """Sahte chat metodu."""
        if self.call_count < len(self.responses):
            response = self.responses[self.call_count]
            self.call_count += 1
            return response
        else:
            # Fazla çağrı olursa hata fırlat
            raise RuntimeError(f"Beklenmeyen AI çağrısı: {self.call_count}")


class MockToolRegistry:
    """Sahte ToolRegistry - test için."""

    def __init__(self):
        self.tools: Dict[str, ToolDefinition] = {}
        # Mock workflow for AgentLoop initialization
        self.workflow = None
        # read_file için sahte handler kaydet
        self.register(
            name="read_file",
            description="Test için sahte read_file",
            handler=self._mock_read_file,
            requires_approval=False
        )
    
    def register(self, name: str, description: str, handler, requires_approval: bool = False, category: str = "general"):
        """Tool kaydetme."""
        self.tools[name] = ToolDefinition(
            name=name,
            description=description,
            handler=handler,
            requires_approval=requires_approval,
            category=category
        )
    
    def has(self, name: str) -> bool:
        """Tool var mı kontrolü."""
        return name in self.tools
    
    def get(self, name: str) -> Optional[ToolDefinition]:
        """Tool getir."""
        return self.tools.get(name)
    
    def get_tool_schema(self, name: str) -> Optional[Dict[str, Any]]:
        """Tool şeması."""
        if name == "read_file":
            return {
                "name": "read_file",
                "description": "Test için sahte read_file",
                "requires_approval": False,
                "parameters": [
                    {"name": "relative_path", "type": "str", "required": True, "description": "Dosya yolu"}
                ],
                "example_call": '{"tool": "read_file", "arguments": {"relative_path": "test.py"}}'
            }
        return None
    
    def get_tool_info(self, name: str) -> Optional[Dict[str, Any]]:
        """Tool bilgisi."""
        tool = self.get(name)
        if tool is None:
            return None
        return {
            "name": tool.name,
            "description": tool.description,
            "requires_approval": tool.requires_approval,
            "category": tool.category
        }
    
    def list_tools(self) -> List[str]:
        """Tool listesi."""
        return list(self.tools.keys())
    
    def execute(self, name: str, arguments: Optional[Dict[str, Any]] = None, approved: bool = False) -> Dict[str, Any]:
        """Tool çalıştırma."""
        tool = self.get(name)
        if tool is None:
            return {"success": False, "error": f"Tool bulunamadı: {name}"}
        
        if tool.requires_approval and not approved:
            return {"success": False, "error": "Onay gerekli"}
        
        try:
            result = tool.handler(**(arguments or {}))
            return {"success": True, "tool": name, "result": result}
        except Exception as exc:
            return {"success": False, "error": str(exc)}
    
    def get_tools_for_prompt(self) -> str:
        """Prompt için tool listesi."""
        return "- read_file: Test için sahte read_file"
    
    def get_detailed_tools_for_prompt(self) -> str:
        """Detaylı tool bilgisi."""
        return "read_file: Test için sahte read_file"
    
    def _mock_read_file(self, relative_path: str) -> str:
        """Sahte read_file handler."""
        return f"# Sahte dosya içeriği: {relative_path}\nprint('Hello, World!')"


def test_tool_call_does_not_trigger_no_tool_retry():
    """
    Test: Geçerli tool çağrısı yapıldığında no-tool retry mekanizması devreye girmemeli.
    """
    print("=" * 70)
    print("TEST: Tool çağrısı yapıldığında no-tool retry devreye girmez")
    print("=" * 70)
    
    # Mock bileşenleri oluştur
    mock_ai = MockOllamaClient()
    mock_registry = MockToolRegistry()
    
    # LoopConfig ile max_no_tool_retries=2
    config = LoopConfig(
        max_iterations=10,
        max_no_tool_retries=2,
        enable_logging=False
    )
    
    # AgentLoop oluştur
    agent_loop = AgentLoop(
        ollama_client=mock_ai,
        tool_registry=mock_registry,
        config=config,
        approval_callback=None
    )
    
    # Görevi çalıştır
    user_task = "test_file.py dosyasını oku"
    print(f"\nGörev: {user_task}")
    print("-" * 70)
    
    result = agent_loop.run(user_task)
    
    # Sonuçları raporla
    print("\nSONUÇLAR:")
    print("-" * 70)
    print(f"Başarı: {result.success}")
    print(f"Final Cevap: {result.final_response}")
    print(f"İterasyon: {result.iterations}")
    print(f"Tool Çağrıları: {len(result.tool_calls)}")
    
    if result.tool_calls:
        for i, call in enumerate(result.tool_calls, 1):
            print(f"  {i}. Tool: {call['tool']}, Args: {call['arguments']}")
    
    print(f"AI Çağrı Sayısı: {mock_ai.call_count}")
    print(f"Hata: {result.error}")
    
    # Doğrulamalar
    print("\nDOĞRULAMALAR:")
    print("-" * 70)
    
    passed = True
    
    # 1. Test başarıyla tamamlanmalı
    if not result.success:
        print("[X] FAIL: Test başarısız")
        passed = False
    else:
        print("[OK] PASS: Test başarılı")
    
    # 2. En az bir geçerli tool çağrısı gerçekleşmeli
    if len(result.tool_calls) < 1:
        print("[X] FAIL: Tool çağrısı yapılmadı")
        passed = False
    else:
        print(f"[OK] PASS: {len(result.tool_calls)} tool çağrısı yapıldı")
    
    # 3. read_file sahte registry üzerinden çalışmalı
    read_file_calls = [c for c in result.tool_calls if c['tool'] == 'read_file']
    if len(read_file_calls) < 1:
        print("[X] FAIL: read_file çağrısı yapılmadı")
        passed = False
    else:
        print("[OK] PASS: read_file çağrısı yapıldı")
    
    # 4. Gerçek run_python_file veya apply_change çalışmamalı
    dangerous_calls = [c for c in result.tool_calls if c['tool'] in ['run_python_file', 'apply_change']]
    if len(dangerous_calls) > 0:
        print(f"[X] FAIL: Tehlikeli tool çağrıları yapıldı: {dangerous_calls}")
        passed = False
    else:
        print("[OK] PASS: Tehlikeli tool çağrıları yapılmadı")
    
    # 5. Model çağrıları sonsuz döngüye girmemeli (max 3 bekleniyor: 1 tool, 1 final)
    if mock_ai.call_count > 3:
        print(f"[X] FAIL: Çok fazla AI çağrısı: {mock_ai.call_count}")
        passed = False
    else:
        print(f"[OK] PASS: AI çağrısı sayısı makul: {mock_ai.call_count}")
    
    # 6. max_no_tool_retries=2 olmasına rağmen geçerli tool çağrısından dolayı gereksiz retry oluşmamalı
    # Tool çağrısı yapıldığı için retry sayısı 0 olmalı
    # Bu, tool_call_log'un dolu olmasından anlaşılır
    if len(result.tool_calls) > 0 and result.iterations <= 2:
        print("[OK] PASS: Gereksiz retry oluşmadı")
    else:
        print(f"[X] FAIL: Gereksiz retry oluşmuş olabilir (iteration: {result.iterations})")
        passed = False
    
    # 7. Test sonunda final cevap alınmalı
    if not result.final_response or result.error:
        print("[X] FAIL: Final cevap alınamadı veya hata var")
        passed = False
    else:
        print("[OK] PASS: Final cevap alındı")
    
    print("\n" + "=" * 70)
    if passed:
        print("TEST SONUCU: PASS")
    else:
        print("TEST SONUCU: FAIL")
    print("=" * 70)
    
    return passed


if __name__ == "__main__":
    try:
        passed = test_tool_call_does_not_trigger_no_tool_retry()
        sys.exit(0 if passed else 1)
    except Exception as e:
        print(f"\nTEST HATASI:")
        print("-" * 70)
        import traceback
        traceback.print_exc()
        print("=" * 70)
        sys.exit(1)
