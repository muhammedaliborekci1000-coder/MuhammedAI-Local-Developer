"""
VS Code Entegrasyonu Endpoint Testleri
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_syntax_highlight():
    """Syntax highlighting endpoint test."""
    print("Testing /api/editor/syntax-highlight...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/editor/syntax-highlight",
            json={
                "code": "def hello():\n    print('world')",
                "language": "python",
                "theme": "vs_code_dark"
            }
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_tabs():
    """Tabs endpoint test."""
    print("\nTesting /api/editor/tabs/create...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/editor/tabs/create",
            json={
                "title": "test.py",
                "content": "print('test')",
                "language": "python"
            }
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_get_tabs():
    """Get tabs endpoint test."""
    print("\nTesting /api/editor/tabs...")
    try:
        response = requests.get(f"{BASE_URL}/api/editor/tabs")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_terminal():
    """Terminal endpoint test."""
    print("\nTesting /api/editor/terminal/create...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/editor/terminal/create",
            json={
                "name": "Test Terminal",
                "type": "command"
            }
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_lsp_start():
    """LSP start endpoint test."""
    print("\nTesting /api/editor/lsp/start...")
    try:
        response = requests.post(f"{BASE_URL}/api/editor/lsp/start")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_lsp_document_open():
    """LSP document open endpoint test."""
    print("\nTesting /api/editor/lsp/document/open...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/editor/lsp/document/open",
            json={
                "uri": "file:///test.py",
                "language_id": "python",
                "text": "def hello():\n    print('world')"
            }
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_lsp_completion():
    """LSP completion endpoint test."""
    print("\nTesting /api/editor/lsp/completion...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/editor/lsp/completion",
            json={
                "uri": "file:///test.py",
                "line": 0,
                "character": 4
            }
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_git_status():
    """Git status endpoint test."""
    print("\nTesting /api/editor/git/status...")
    try:
        response = requests.get(f"{BASE_URL}/api/editor/git/status")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 70)
    print("VS Code Entegrasyonu Endpoint Testleri")
    print("=" * 70)
    
    results = []
    results.append(("Syntax Highlight", test_syntax_highlight()))
    results.append(("Tabs Create", test_tabs()))
    results.append(("Get Tabs", test_get_tabs()))
    results.append(("Terminal Create", test_terminal()))
    results.append(("LSP Start", test_lsp_start()))
    results.append(("LSP Document Open", test_lsp_document_open()))
    results.append(("LSP Completion", test_lsp_completion()))
    results.append(("Git Status", test_git_status()))
    
    print("\n" + "=" * 70)
    print("Test Sonuçları")
    print("=" * 70)
    for name, result in results:
        status = "BASARILI" if result else "BASARISIZ"
        print(f"{name}: {status}")
    
    total = len(results)
    passed = sum(1 for _, r in results if r)
    print(f"\nToplam: {passed}/{total} test başarılı")
