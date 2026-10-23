"""
Tab/Sekme Entegrasyonu Endpoint Testleri
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000"


def test_create_tab():
    """Tab oluşturma endpoint test."""
    print("\nTesting /api/editor/tabs/create...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/editor/tabs/create",
            json={"title": "test.py", "content": "print('hello')", "language": "python"}
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_get_tabs():
    """Tab listesi endpoint test."""
    print("\nTesting /api/editor/tabs...")
    try:
        response = requests.get(f"{BASE_URL}/api/editor/tabs")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_switch_tab():
    """Tab değiştirme endpoint test."""
    print("\nTesting /api/editor/tabs/switch...")
    try:
        # Önce bir tab oluştur
        create_resp = requests.post(
            f"{BASE_URL}/api/editor/tabs/create",
            json={"title": "switch_test.py", "content": "code", "language": "python"}
        )
        tab_id = create_resp.json().get("tab_id")
        
        if tab_id:
            response = requests.post(
                f"{BASE_URL}/api/editor/tabs/switch",
                json={"tab_id": tab_id}
            )
            print(f"Status: {response.status_code}")
            print(f"Response: {response.json()}")
            return response.status_code == 200
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_close_tab():
    """Tab kapatma endpoint test."""
    print("\nTesting /api/editor/tabs/close...")
    try:
        # Önce bir tab oluştur
        create_resp = requests.post(
            f"{BASE_URL}/api/editor/tabs/create",
            json={"title": "close_test.py", "content": "code", "language": "python"}
        )
        tab_id = create_resp.json().get("tab_id")
        
        if tab_id:
            response = requests.post(
                f"{BASE_URL}/api/editor/tabs/close",
                json={"tab_id": tab_id}
            )
            print(f"Status: {response.status_code}")
            print(f"Response: {response.json()}")
            return response.status_code == 200
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_update_tab():
    """Tab güncelleme endpoint test."""
    print("\nTesting /api/editor/tabs/update...")
    try:
        # Önce bir tab oluştur
        create_resp = requests.post(
            f"{BASE_URL}/api/editor/tabs/create",
            json={"title": "update_test.py", "content": "old code", "language": "python"}
        )
        tab_id = create_resp.json().get("tab_id")
        
        if tab_id:
            response = requests.post(
                f"{BASE_URL}/api/editor/tabs/update",
                json={"tab_id": tab_id, "content": "new code"}
            )
            print(f"Status: {response.status_code}")
            print(f"Response: {response.json()}")
            return response.status_code == 200
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_pin_tab():
    """Tab sabitleme endpoint test."""
    print("\nTesting /api/editor/tabs/pin...")
    try:
        # Önce bir tab oluştur
        create_resp = requests.post(
            f"{BASE_URL}/api/editor/tabs/create",
            json={"title": "pin_test.py", "content": "code", "language": "python"}
        )
        tab_id = create_resp.json().get("tab_id")
        
        if tab_id:
            response = requests.post(
                f"{BASE_URL}/api/editor/tabs/pin",
                json={"tab_id": tab_id}
            )
            print(f"Status: {response.status_code}")
            print(f"Response: {response.json()}")
            return response.status_code == 200
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_unpin_tab():
    """Tab sabitleme kaldırma endpoint test."""
    print("\nTesting /api/editor/tabs/unpin...")
    try:
        # Önce bir tab oluştur ve pinle
        create_resp = requests.post(
            f"{BASE_URL}/api/editor/tabs/create",
            json={"title": "unpin_test.py", "content": "code", "language": "python"}
        )
        tab_id = create_resp.json().get("tab_id")
        
        if tab_id:
            # Önce pinle
            requests.post(f"{BASE_URL}/api/editor/tabs/pin", json={"tab_id": tab_id})
            
            # Sonra unpin yap
            response = requests.post(
                f"{BASE_URL}/api/editor/tabs/unpin",
                json={"tab_id": tab_id}
            )
            print(f"Status: {response.status_code}")
            print(f"Response: {response.json()}")
            return response.status_code == 200
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_set_read_only():
    """Tab read-only ayarlama endpoint test."""
    print("\nTesting /api/editor/tabs/read-only...")
    try:
        # Önce bir tab oluştur
        create_resp = requests.post(
            f"{BASE_URL}/api/editor/tabs/create",
            json={"title": "readonly_test.py", "content": "code", "language": "python"}
        )
        tab_id = create_resp.json().get("tab_id")
        
        if tab_id:
            response = requests.post(
                f"{BASE_URL}/api/editor/tabs/read-only",
                json={"tab_id": tab_id, "read_only": True}
            )
            print(f"Status: {response.status_code}")
            print(f"Response: {response.json()}")
            return response.status_code == 200
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False


if __name__ == "__main__":
    print("=" * 70)
    print("Tab/Sekme Entegrasyonu Endpoint Testleri")
    print("=" * 70)
    
    results = []
    results.append(("Create Tab", test_create_tab()))
    results.append(("Get Tabs", test_get_tabs()))
    results.append(("Switch Tab", test_switch_tab()))
    results.append(("Close Tab", test_close_tab()))
    results.append(("Update Tab", test_update_tab()))
    results.append(("Pin Tab", test_pin_tab()))
    results.append(("Unpin Tab", test_unpin_tab()))
    results.append(("Set Read-Only", test_set_read_only()))
    
    print("\n" + "=" * 70)
    print("Test Sonuclari")
    print("=" * 70)
    for name, result in results:
        status = "BASARILI" if result else "BASARISIZ"
        print(f"{name}: {status}")
    
    total = len(results)
    passed = sum(1 for _, r in results if r)
    print(f"\nToplam: {passed}/{total} test basarili")
