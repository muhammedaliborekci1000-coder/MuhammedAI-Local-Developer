"""
Native Tool Calling Testleri
OllamaClient ve AgentLoop'un native tool_calls desteğini doğrular.
"""
import json
from app.ai.ollama_client import OllamaClient
from app.tools.tool_registry import ToolRegistry

print("=" * 70)
print("TEST 1: ToolRegistry Ollama Formatı")
print("=" * 70)

registry = ToolRegistry()
ollama_tools = registry.get_ollama_tools()

print(f"Toplam araç: {len(ollama_tools)}")
print(f"İlk araç: {json.dumps(ollama_tools[0], indent=2, ensure_ascii=False) if ollama_tools else 'Yok'}")

print("\n" + "=" * 70)
print("TEST 2: OllamaClient Tools Gönderimi")
print("=" * 70)

client = OllamaClient(model="qwen3:4b")
test_tools = [
    {
        "type": "function",
        "function": {
            "name": "test_echo",
            "description": "Test aracı",
            "parameters": {
                "type": "object",
                "properties": {
                    "message": {"type": "string", "description": "Mesaj"}
                },
                "required": ["message"]
            }
        }
    }
]

response = client.chat("Test mesajı", tools=test_tools)
print(f"Yanıt tipi: {type(response)}")
print(f"Content: {response.get('content', '')[:100]}")
print(f"Tool calls: {response.get('tool_calls')}")

print("\n" + "=" * 70)
print("TEST 3: Tools Olmadan Geriye Dönük Uyumluluk")
print("=" * 70)

response_no_tools = client.chat("Test mesajı")
print(f"Yanıt tipi: {type(response_no_tools)}")
print(f"Content: {response_no_tools.get('content', '')[:100]}")
print(f"Tool calls: {response_no_tools.get('tool_calls')}")

print("\n" + "=" * 70)
print("TAMAMLANDI")
print("=" * 70)
