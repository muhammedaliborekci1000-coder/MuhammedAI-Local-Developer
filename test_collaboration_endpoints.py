"""
Collaboration Endpoint Testleri
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000"


def test_create_collaboration_session():
    """Collaboration session oluşturma test."""
    print("\nTesting /api/editor/collaboration/session...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/editor/collaboration/session",
            json={"name": "Test Session", "owner_id": "user_1"}
        )
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Success: {result.get('success')}")
        print(f"Session ID: {result.get('session_id')}")
        print(f"Session Name: {result.get('session_name')}")
        print(f"Users count: {len(result.get('users', []))}")
        return response.status_code == 200 and result.get('success')
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_join_collaboration_session():
    """Collaboration session'a katılma test."""
    print("\nTesting /api/editor/collaboration/join...")
    try:
        # Önce session oluştur
        create_resp = requests.post(
            f"{BASE_URL}/api/editor/collaboration/session",
            json={"name": "Test Session", "owner_id": "user_1"}
        )
        session_id = create_resp.json().get("session_id")
        
        if session_id:
            response = requests.post(
                f"{BASE_URL}/api/editor/collaboration/join",
                json={"session_id": session_id, "user_id": "user_2", "user_name": "Alice"}
            )
            print(f"Status: {response.status_code}")
            result = response.json()
            print(f"Success: {result.get('success')}")
            print(f"Users count: {len(result.get('users', []))}")
            print(f"Message: {result.get('message')}")
            return response.status_code == 200 and result.get('success')
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_leave_collaboration_session():
    """Collaboration session'dan ayrılma test."""
    print("\nTesting /api/editor/collaboration/leave...")
    try:
        # Önce session oluştur ve katıl
        create_resp = requests.post(
            f"{BASE_URL}/api/editor/collaboration/session",
            json={"name": "Test Session", "owner_id": "user_1"}
        )
        session_id = create_resp.json().get("session_id")
        
        if session_id:
            response = requests.post(
                f"{BASE_URL}/api/editor/collaboration/leave",
                json={"session_id": session_id, "user_id": "user_1"}
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


def test_add_collaboration_comment():
    """Comment ekleme test."""
    print("\nTesting /api/editor/collaboration/comment...")
    try:
        # Önce session oluştur
        create_resp = requests.post(
            f"{BASE_URL}/api/editor/collaboration/session",
            json={"name": "Test Session", "owner_id": "user_1"}
        )
        session_id = create_resp.json().get("session_id")
        
        if session_id:
            response = requests.post(
                f"{BASE_URL}/api/editor/collaboration/comment",
                json={
                    "session_id": session_id,
                    "user_id": "user_1",
                    "user_name": "Bob",
                    "content": "This is a test comment",
                    "file_path": "test.py",
                    "line": 10
                }
            )
            print(f"Status: {response.status_code}")
            result = response.json()
            print(f"Success: {result.get('success')}")
            print(f"Comments count: {len(result.get('comments', []))}")
            print(f"Message: {result.get('message')}")
            return response.status_code == 200 and result.get('success')
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_get_collaboration_session():
    """Collaboration session bilgilerini alma test."""
    print("\nTesting GET /api/editor/collaboration/session...")
    try:
        # Önce session oluştur
        create_resp = requests.post(
            f"{BASE_URL}/api/editor/collaboration/session",
            json={"name": "Test Session", "owner_id": "user_1"}
        )
        
        response = requests.get(f"{BASE_URL}/api/editor/collaboration/session")
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Success: {result.get('success')}")
        print(f"Session ID: {result.get('session_id')}")
        print(f"Session Name: {result.get('session_name')}")
        print(f"Users count: {len(result.get('users', []))}")
        print(f"Comments count: {len(result.get('comments', []))}")
        return response.status_code == 200 and result.get('success')
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_update_collaboration_role():
    """Kullanıcı rolü güncelleme test."""
    print("\nTesting /api/editor/collaboration/role...")
    try:
        # Önce session oluştur
        create_resp = requests.post(
            f"{BASE_URL}/api/editor/collaboration/session",
            json={"name": "Test Session", "owner_id": "user_1"}
        )
        session_id = create_resp.json().get("session_id")
        
        if session_id:
            response = requests.post(
                f"{BASE_URL}/api/editor/collaboration/role",
                json={"session_id": session_id, "user_id": "user_1", "role": "editor"}
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
    print("Collaboration Endpoint Testleri")
    print("=" * 70)
    
    results = []
    results.append(("Create Session", test_create_collaboration_session()))
    results.append(("Join Session", test_join_collaboration_session()))
    results.append(("Leave Session", test_leave_collaboration_session()))
    results.append(("Add Comment", test_add_collaboration_comment()))
    results.append(("Get Session", test_get_collaboration_session()))
    results.append(("Update Role", test_update_collaboration_role()))
    
    print("\n" + "=" * 70)
    print("Test Sonuclari")
    print("=" * 70)
    for name, result in results:
        status = "BASARILI" if result else "BASARISIZ"
        print(f"{name}: {status}")
    
    total = len(results)
    passed = sum(1 for _, r in results if r)
    print(f"\nToplam: {passed}/{total} test basarili")
