"""
IntelliSense (Auto-Completion) Endpoint Testleri
"""

import requests
import json
from pathlib import Path

BASE_URL = "http://127.0.0.1:8000"


def test_auto_completion():
    """Auto completion endpoint test."""
    print("\nTesting /api/editor/completion...")
    try:
        # Test dosyası oluştur
        test_file = Path("test_completion.py")
        test_file.write_text("""def hello():
    print('world')
    x = 42
    return x

hello()
""")
        
        response = requests.post(
            f"{BASE_URL}/api/editor/completion",
            json={
                "file_path": str(test_file),
                "line": 5,
                "column": 0,
                "prefix": "h"
            }
        )
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Success: {result.get('success')}")
        print(f"Context: {result.get('context')}")
        print(f"Items count: {len(result.get('items', []))}")
        print(f"Errors: {result.get('errors')}")
        
        # Temizle
        test_file.unlink()
        
        return response.status_code == 200 and result.get('success')
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_auto_completion_keywords():
    """Keywords completion test."""
    print("\nTesting /api/editor/completion (Keywords)...")
    try:
        test_file = Path("test_completion.py")
        test_file.write_text("if ")
        
        response = requests.post(
            f"{BASE_URL}/api/editor/completion",
            json={
                "file_path": str(test_file),
                "line": 0,
                "column": 3,
                "prefix": "i"
            }
        )
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Success: {result.get('success')}")
        print(f"Items count: {len(result.get('items', []))}")
        
        test_file.unlink()
        
        return response.status_code == 200 and result.get('success')
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_auto_completion_builtins():
    """Builtins completion test."""
    print("\nTesting /api/editor/completion (Builtins)...")
    try:
        test_file = Path("test_completion.py")
        test_file.write_text("pri")
        
        response = requests.post(
            f"{BASE_URL}/api/editor/completion",
            json={
                "file_path": str(test_file),
                "line": 0,
                "column": 3,
                "prefix": "pri"
            }
        )
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Success: {result.get('success')}")
        print(f"Items count: {len(result.get('items', []))}")
        
        test_file.unlink()
        
        return response.status_code == 200 and result.get('success')
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_auto_completion_empty_prefix():
    """Empty prefix test."""
    print("\nTesting /api/editor/completion (Empty prefix)...")
    try:
        test_file = Path("test_completion.py")
        test_file.write_text("def test(): pass")
        
        response = requests.post(
            f"{BASE_URL}/api/editor/completion",
            json={
                "file_path": str(test_file),
                "line": 0,
                "column": 0,
                "prefix": ""
            }
        )
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Success: {result.get('success')}")
        print(f"Items count: {len(result.get('items', []))}")
        
        test_file.unlink()
        
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_auto_completion_invalid_file():
    """Invalid file test."""
    print("\nTesting /api/editor/completion (Invalid file)...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/editor/completion",
            json={
                "file_path": "nonexistent.py",
                "line": 0,
                "column": 0,
                "prefix": ""
            }
        )
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Success: {result.get('success')}")
        print(f"Errors: {result.get('errors')}")
        
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False


if __name__ == "__main__":
    print("=" * 70)
    print("IntelliSense (Auto-Completion) Endpoint Testleri")
    print("=" * 70)
    
    results = []
    results.append(("Auto Completion", test_auto_completion()))
    results.append(("Keywords", test_auto_completion_keywords()))
    results.append(("Builtins", test_auto_completion_builtins()))
    results.append(("Empty Prefix", test_auto_completion_empty_prefix()))
    results.append(("Invalid File", test_auto_completion_invalid_file()))
    
    print("\n" + "=" * 70)
    print("Test Sonuclari")
    print("=" * 70)
    for name, result in results:
        status = "BASARILI" if result else "BASARISIZ"
        print(f"{name}: {status}")
    
    total = len(results)
    passed = sum(1 for _, r in results if r)
    print(f"\nToplam: {passed}/{total} test basarili")
