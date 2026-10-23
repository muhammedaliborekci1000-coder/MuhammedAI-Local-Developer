"""
Syntax Highlighting Endpoint Testleri
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000"


def test_syntax_highlight_python():
    """Python syntax highlighting test."""
    print("\nTesting /api/editor/syntax-highlight (Python)...")
    try:
        code = """def hello():
    print('world')
    x = 42
    return x"""
        
        response = requests.post(
            f"{BASE_URL}/api/editor/syntax-highlight",
            json={"code": code, "language": "python", "theme": "vs_code_dark"}
        )
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Success: {result.get('success')}")
        print(f"Lines count: {result.get('lines_count')}")
        print(f"Has HTML: {bool(result.get('html'))}")
        print(f"Errors: {result.get('errors')}")
        return response.status_code == 200 and result.get('success')
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_syntax_highlight_javascript():
    """JavaScript syntax highlighting test."""
    print("\nTesting /api/editor/syntax-highlight (JavaScript)...")
    try:
        code = """function hello() {
    console.log('world');
    const x = 42;
    return x;
}"""
        
        response = requests.post(
            f"{BASE_URL}/api/editor/syntax-highlight",
            json={"code": code, "language": "javascript", "theme": "monokai"}
        )
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Success: {result.get('success')}")
        print(f"Lines count: {result.get('lines_count')}")
        print(f"Errors: {result.get('errors')}")
        return response.status_code == 200 and result.get('success')
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_syntax_highlight_html():
    """HTML syntax highlighting test."""
    print("\nTesting /api/editor/syntax-highlight (HTML)...")
    try:
        code = """<html>
<body>
    <h1>Hello World</h1>
</body>
</html>"""
        
        response = requests.post(
            f"{BASE_URL}/api/editor/syntax-highlight",
            json={"code": code, "language": "html", "theme": "dracula"}
        )
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Success: {result.get('success')}")
        print(f"Lines count: {result.get('lines_count')}")
        print(f"Errors: {result.get('errors')}")
        return response.status_code == 200 and result.get('success')
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_syntax_highlight_css():
    """CSS syntax highlighting test."""
    print("\nTesting /api/editor/syntax-highlight (CSS)...")
    try:
        code = """.container {
    width: 100%;
    background-color: #fff;
}"""
        
        response = requests.post(
            f"{BASE_URL}/api/editor/syntax-highlight",
            json={"code": code, "language": "css", "theme": "github_light"}
        )
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Success: {result.get('success')}")
        print(f"Lines count: {result.get('lines_count')}")
        print(f"Errors: {result.get('errors')}")
        return response.status_code == 200 and result.get('success')
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_syntax_highlight_themes():
    """Different themes test."""
    print("\nTesting different themes...")
    themes = ["vs_code_dark", "monokai", "dracula", "github_light", "github_dark", "solarized_dark", "solarized_light"]
    code = "def test(): return 42"
    
    results = []
    for theme in themes:
        try:
            response = requests.post(
                f"{BASE_URL}/api/editor/syntax-highlight",
                json={"code": code, "language": "python", "theme": theme}
            )
            result = response.json()
            success = response.status_code == 200 and result.get('success')
            print(f"  {theme}: {'OK' if success else 'FAIL'}")
            results.append(success)
        except Exception as e:
            print(f"  {theme}: ERROR - {e}")
            results.append(False)
    
    return all(results)


def test_syntax_highlight_empty():
    """Empty code test."""
    print("\nTesting /api/editor/syntax-highlight (Empty)...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/editor/syntax-highlight",
            json={"code": "", "language": "python", "theme": "vs_code_dark"}
        )
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Success: {result.get('success')}")
        print(f"Lines count: {result.get('lines_count')}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_syntax_highlight_multiline():
    """Multiline code test."""
    print("\nTesting /api/editor/syntax-highlight (Multiline)...")
    try:
        code = """class MyClass:
    def __init__(self, value):
        self.value = value
    
    def get_value(self):
        return self.value
    
    def set_value(self, new_value):
        self.value = new_value

# Create instance
obj = MyClass(42)
print(obj.get_value())"""
        
        response = requests.post(
            f"{BASE_URL}/api/editor/syntax-highlight",
            json={"code": code, "language": "python", "theme": "vs_code_dark"}
        )
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Success: {result.get('success')}")
        print(f"Lines count: {result.get('lines_count')}")
        print(f"Errors: {result.get('errors')}")
        return response.status_code == 200 and result.get('success')
    except Exception as e:
        print(f"Error: {e}")
        return False


if __name__ == "__main__":
    print("=" * 70)
    print("Syntax Highlighting Endpoint Testleri")
    print("=" * 70)
    
    results = []
    results.append(("Python", test_syntax_highlight_python()))
    results.append(("JavaScript", test_syntax_highlight_javascript()))
    results.append(("HTML", test_syntax_highlight_html()))
    results.append(("CSS", test_syntax_highlight_css()))
    results.append(("Themes", test_syntax_highlight_themes()))
    results.append(("Empty Code", test_syntax_highlight_empty()))
    results.append(("Multiline", test_syntax_highlight_multiline()))
    
    print("\n" + "=" * 70)
    print("Test Sonuclari")
    print("=" * 70)
    for name, result in results:
        status = "BASARILI" if result else "BASARISIZ"
        print(f"{name}: {status}")
    
    total = len(results)
    passed = sum(1 for _, r in results if r)
    print(f"\nToplam: {passed}/{total} test basarili")
