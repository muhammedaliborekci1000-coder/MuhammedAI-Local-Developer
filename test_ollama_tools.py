"""
Minimal Ollama Tool Calling Testi
Kod değişikliği olmadan Ollama API'sinin tool_calls döndürüp döndürmediğini test eder.
"""
import ollama
import json

# Ollama client
client = ollama.Client(host="http://127.0.0.1:11434")

# Test için basit bir tool tanımı
tools = [
    {
        "type": "function",
        "function": {
            "name": "test_tool",
            "description": "Test aracı",
            "parameters": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "Test mesajı"
                    }
                },
                "required": ["message"]
            }
        }
    }
]

# İstek
request = {
    "model": "qwen3:4b",
    "messages": [
        {
            "role": "user",
            "content": "Test mesajı gönder: Merhaba"
        }
    ],
    "tools": tools,
    "options": {
        "temperature": 0.1
    }
}

print("Ollama API Tool Calling Testi")
print("=" * 70)
print(f"Model: {request['model']}")
print(f"Tools gönderiliyor: {len(tools)}")
print(f"Tool adı: {tools[0]['function']['name']}")
print("-" * 70)

try:
    response = client.chat(**request)
    
    print("\nYanıt tipi:", type(response))
    print("Yanıt özellikleri:", dir(response))
    
    # ChatResponse objesinden dict'e çevir
    response_dict = {
        "model": response.model,
        "message": {
            "role": response.message.role,
            "content": response.message.content,
        }
    }
    
    # tool_calls var mı kontrol et
    if hasattr(response.message, 'tool_calls'):
        response_dict["message"]["tool_calls"] = response.message.tool_calls
    else:
        response_dict["message"]["tool_calls"] = []
    
    print("\nYanıt yapısı:")
    print(json.dumps(response_dict, indent=2, ensure_ascii=False))
    
    print("\n" + "=" * 70)
    print("TOOL CALLS ANALİZİ")
    print("=" * 70)
    
    tool_calls = response_dict["message"]["tool_calls"]
    
    if tool_calls:
        print(f"[OK] Tool calls bulundu: {len(tool_calls)}")
        for i, tc in enumerate(tool_calls, 1):
            print(f"  {i}. {json.dumps(tc, indent=4, ensure_ascii=False)}")
    else:
        print("[FAIL] Tool calls YOK")
        print(f"Content: {response_dict['message']['content'][:200]}")
        
except Exception as e:
    print(f"[ERROR] Hata: {e}")
    import traceback
    traceback.print_exc()
