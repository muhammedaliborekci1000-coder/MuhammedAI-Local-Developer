"""
Debugging Endpoint Testleri
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000"


def test_debug_start():
    """Debug session başlatma test."""
    print("\nTesting /api/editor/debug/start...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/editor/debug/start",
            json={"uri": "file:///test.py"}
        )
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Success: {result.get('success')}")
        print(f"Session ID: {result.get('session_id')}")
        print(f"State: {result.get('state')}")
        return response.status_code == 200 and result.get('success')
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_debug_add_breakpoint():
    """Breakpoint ekleme test."""
    print("\nTesting /api/editor/debug/breakpoint...")
    try:
        # Önce session başlat
        start_resp = requests.post(
            f"{BASE_URL}/api/editor/debug/start",
            json={"uri": "file:///test.py"}
        )
        
        response = requests.post(
            f"{BASE_URL}/api/editor/debug/breakpoint",
            json={"uri": "file:///test.py", "line": 10, "kind": "line"}
        )
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Success: {result.get('success')}")
        print(f"Breakpoint ID: {result.get('breakpoint_id')}")
        print(f"Line: {result.get('line')}")
        return response.status_code == 200 and result.get('success')
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_debug_get_breakpoints():
    """Breakpoint listesi test."""
    print("\nTesting /api/editor/debug/breakpoints...")
    try:
        response = requests.get(f"{BASE_URL}/api/editor/debug/breakpoints")
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Success: {result.get('success')}")
        print(f"Total: {result.get('total')}")
        print(f"Breakpoints: {result.get('breakpoints')}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_debug_remove_breakpoint():
    """Breakpoint kaldırma test."""
    print("\nTesting DELETE /api/editor/debug/breakpoint...")
    try:
        # Önce breakpoint ekle
        add_resp = requests.post(
            f"{BASE_URL}/api/editor/debug/breakpoint",
            json={"uri": "file:///test.py", "line": 20}
        )
        bp_id = add_resp.json().get("breakpoint_id")
        
        if bp_id:
            response = requests.delete(
                f"{BASE_URL}/api/editor/debug/breakpoint",
                json={"breakpoint_id": bp_id}
            )
            print(f"Status: {response.status_code}")
            result = response.json()
            print(f"Success: {result.get('success')}")
            print(f"Message: {result.get('message')}")
            return response.status_code == 200 and result.get('success')
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_debug_step():
    """Step test."""
    print("\nTesting /api/editor/debug/step...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/editor/debug/step",
            json={"kind": "over"}
        )
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Success: {result.get('success')}")
        print(f"Message: {result.get('message')}")
        print(f"State: {result.get('state')}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_debug_get_variables():
    """Değişkenleri alma test."""
    print("\nTesting /api/editor/debug/variables...")
    try:
        response = requests.get(f"{BASE_URL}/api/editor/debug/variables")
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Success: {result.get('success')}")
        print(f"Total: {result.get('total')}")
        print(f"Variables: {result.get('variables')}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_debug_get_stack():
    """Call stack alma test."""
    print("\nTesting /api/editor/debug/stack...")
    try:
        response = requests.get(f"{BASE_URL}/api/editor/debug/stack")
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Success: {result.get('success')}")
        print(f"Total: {result.get('total')}")
        print(f"Stack frames: {result.get('stack_frames')}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_debug_stop():
    """Debug session durdurma test."""
    print("\nTesting /api/editor/debug/stop...")
    try:
        # Önce session başlat
        start_resp = requests.post(
            f"{BASE_URL}/api/editor/debug/start",
            json={"uri": "file:///test.py"}
        )
        session_id = start_resp.json().get("session_id")
        
        if session_id:
            response = requests.post(
                f"{BASE_URL}/api/editor/debug/stop",
                json={"session_id": session_id}
            )
            print(f"Status: {response.status_code}")
            result = response.json()
            print(f"Success: {result.get('success')}")
            print(f"Message: {result.get('message')}")
            return response.status_code == 200 and result.get('success')
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False


if __name__ == "__main__":
    print("=" * 70)
    print("Debugging Endpoint Testleri")
    print("=" * 70)
    
    results = []
    results.append(("Debug Start", test_debug_start()))
    results.append(("Add Breakpoint", test_debug_add_breakpoint()))
    results.append(("Get Breakpoints", test_debug_get_breakpoints()))
    results.append(("Remove Breakpoint", test_debug_remove_breakpoint()))
    results.append(("Debug Step", test_debug_step()))
    results.append(("Get Variables", test_debug_get_variables()))
    results.append(("Get Stack", test_debug_get_stack()))
    results.append(("Debug Stop", test_debug_stop()))
    
    print("\n" + "=" * 70)
    print("Test Sonuclari")
    print("=" * 70)
    for name, result in results:
        status = "BASARILI" if result else "BASARISIZ"
        print(f"{name}: {status}")
    
    total = len(results)
    passed = sum(1 for _, r in results if r)
    print(f"\nToplam: {passed}/{total} test basarili")
