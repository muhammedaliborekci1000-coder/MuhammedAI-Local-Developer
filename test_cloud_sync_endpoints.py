"""
Cloud Sync Endpoint Testleri
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000"


def test_configure_cloud_provider():
    """Cloud provider yapılandırma test."""
    print("\nTesting /api/editor/cloud-sync/configure...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/editor/cloud-sync/configure",
            json={"provider": "github", "config": {"token": "test"}}
        )
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Success: {result.get('success')}")
        print(f"Message: {result.get('message')}")
        return response.status_code == 200 and result.get('success')
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_add_cloud_sync_file():
    """Dosyayı sync'e ekleme test."""
    print("\nTesting /api/editor/cloud-sync/file...")
    try:
        # Önce provider yapılandır
        requests.post(
            f"{BASE_URL}/api/editor/cloud-sync/configure",
            json={"provider": "github"}
        )
        
        response = requests.post(
            f"{BASE_URL}/api/editor/cloud-sync/file",
            json={"path": "test.py", "local_hash": "abc123"}
        )
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Success: {result.get('success')}")
        print(f"Path: {result.get('path')}")
        print(f"Status: {result.get('status')}")
        return response.status_code == 200 and result.get('success')
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_get_cloud_sync_files():
    """Sync dosyalarını alma test."""
    print("\nTesting /api/editor/cloud-sync/files...")
    try:
        response = requests.get(f"{BASE_URL}/api/editor/cloud-sync/files")
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Success: {result.get('success')}")
        print(f"Total: {result.get('total')}")
        print(f"Files: {result.get('files')}")
        return response.status_code == 200 and result.get('success')
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_cloud_sync():
    """Cloud sync test."""
    print("\nTesting /api/editor/cloud-sync/sync...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/editor/cloud-sync/sync",
            json={"direction": "bidirectional"}
        )
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Success: {result.get('success')}")
        print(f"Files synced: {result.get('files_synced')}")
        print(f"Message: {result.get('message')}")
        print(f"Errors: {result.get('errors')}")
        return response.status_code == 200 and result.get('success')
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_get_cloud_sync_status():
    """Cloud sync durumunu alma test."""
    print("\nTesting /api/editor/cloud-sync/status...")
    try:
        response = requests.get(f"{BASE_URL}/api/editor/cloud-sync/status")
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Success: {result.get('success')}")
        print(f"Provider: {result.get('status', {}).get('provider')}")
        print(f"Is syncing: {result.get('status', {}).get('is_syncing')}")
        print(f"Total files: {result.get('status', {}).get('total_files')}")
        return response.status_code == 200 and result.get('success')
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_remove_cloud_sync_file():
    """Dosyayı sync'ten kaldırma test."""
    print("\nTesting DELETE /api/editor/cloud-sync/file...")
    try:
        response = requests.delete(
            f"{BASE_URL}/api/editor/cloud-sync/file",
            json={"path": "test.py"}
        )
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Success: {result.get('success')}")
        print(f"Message: {result.get('message')}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_resolve_cloud_sync_conflict():
    """Conflict çözme test."""
    print("\nTesting /api/editor/cloud-sync/resolve...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/editor/cloud-sync/resolve",
            json={"path": "test.py", "resolution": "local"}
        )
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Success: {result.get('success')}")
        print(f"Message: {result.get('message')}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_get_cloud_sync_history():
    """Sync geçmişini alma test."""
    print("\nTesting /api/editor/cloud-sync/history...")
    try:
        response = requests.get(f"{BASE_URL}/api/editor/cloud-sync/history")
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Success: {result.get('success')}")
        print(f"Total: {result.get('total')}")
        print(f"History: {result.get('history')}")
        return response.status_code == 200 and result.get('success')
    except Exception as e:
        print(f"Error: {e}")
        return False


if __name__ == "__main__":
    print("=" * 70)
    print("Cloud Sync Endpoint Testleri")
    print("=" * 70)
    
    results = []
    results.append(("Configure Provider", test_configure_cloud_provider()))
    results.append(("Add File", test_add_cloud_sync_file()))
    results.append(("Get Files", test_get_cloud_sync_files()))
    results.append(("Sync", test_cloud_sync()))
    results.append(("Get Status", test_get_cloud_sync_status()))
    results.append(("Remove File", test_remove_cloud_sync_file()))
    results.append(("Resolve Conflict", test_resolve_cloud_sync_conflict()))
    results.append(("Get History", test_get_cloud_sync_history()))
    
    print("\n" + "=" * 70)
    print("Test Sonuclari")
    print("=" * 70)
    for name, result in results:
        status = "BASARILI" if result else "BASARISIZ"
        print(f"{name}: {status}")
    
    total = len(results)
    passed = sum(1 for _, r in results if r)
    print(f"\nToplam: {passed}/{total} test basarili")
