"""
Quality Test: Path Traversal Protection
Amaç: Web API'de path traversal saldırılarına karşı korumayı doğrulamak.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from app.ui.web_app import app
from app.core.config import PROJECT_ROOT


def test_path_traversal_blocked():
    """
    Test: Proje dışı path erişimi engellenmeli.
    """
    print("=" * 70)
    print("TEST: Path Traversal Blocked")
    print("=" * 70)
    
    client = TestClient(app)
    
    # Path traversal denemeleri
    traversal_paths = [
        "../../../etc/passwd",
        "..\\..\\..\\windows\\system32",
        "/etc/passwd",
        "C:/Windows/System32",
        "../../.git/config",
        "..\\..\\.git\\config"
    ]
    
    passed = True
    
    for path in traversal_paths:
        response = client.get(f"/api/project/files?path={path}")
        
        # 403 veya hata dönmeli
        if response.status_code == 200:
            print(f"[FAIL] Path traversal engellenmedi: {path}")
            passed = False
        else:
            print(f"[OK] Path engellendi: {path} (status: {response.status_code})")
    
    print(f"{'PASS' if passed else 'FAIL'}: Path traversal koruması")
    print("=" * 70)
    
    assert passed


def test_valid_path_allowed():
    """
    Test: Geçerli proje içi path erişilebilmeli.
    """
    print("=" * 70)
    print("TEST: Valid Path Allowed")
    print("=" * 70)
    
    client = TestClient(app)
    
    # Geçerli path
    response = client.get("/api/project/files?path=app")
    
    passed = response.status_code == 200
    
    if passed:
        print(f"[OK] Geçerli path erişilebildi: app")
    else:
        print(f"[FAIL] Geçerli path erişilemedi: app")
    
    print(f"{'PASS' if passed else 'FAIL'}: Geçerli path erişimi")
    print("=" * 70)
    
    assert passed


if __name__ == "__main__":
    try:
        test1 = test_path_traversal_blocked()
        test2 = test_valid_path_allowed()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Path Traversal Blocked: {'PASS' if test1 else 'FAIL'}")
        print(f"Valid Path Allowed: {'PASS' if test2 else 'FAIL'}")
        
        all_passed = test1 and test2
        print(f"\nTOPLAM: {'PASS' if all_passed else 'FAIL'}")
        print("=" * 70)
        
        sys.exit(0 if all_passed else 1)
    except Exception as e:
        print(f"\nTEST HATASI:")
        print("-" * 70)
        import traceback
        traceback.print_exc()
        print("=" * 70)
        sys.exit(1)
