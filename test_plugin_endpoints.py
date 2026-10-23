"""
Plugin Sistemi Endpoint Testleri
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000"


def test_get_plugins():
    """Tüm plugin'leri alma test."""
    print("\nTesting /api/editor/plugins...")
    try:
        response = requests.get(f"{BASE_URL}/api/editor/plugins")
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Success: {result.get('success')}")
        print(f"Total: {result.get('total')}")
        print(f"Plugins: {[p['name'] for p in result.get('plugins', [])]}")
        return response.status_code == 200 and result.get('success')
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_install_plugin():
    """Plugin yükleme test."""
    print("\nTesting /api/editor/plugins/install...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/editor/plugins/install",
            json={
                "plugin_id": "test_plugin",
                "plugin_data": {
                    "name": "Test Plugin",
                    "version": "1.0.0",
                    "description": "A test plugin",
                    "author": "Test Author",
                    "type": "tool"
                }
            }
        )
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Success: {result.get('success')}")
        print(f"Message: {result.get('message')}")
        print(f"Plugin: {result.get('plugin')}")
        return response.status_code == 200 and result.get('success')
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_enable_plugin():
    """Plugin aktifleştirme test."""
    print("\nTesting /api/editor/plugins/enable...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/editor/plugins/enable",
            json={"plugin_id": "tool_formatter"}
        )
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Success: {result.get('success')}")
        print(f"Message: {result.get('message')}")
        return response.status_code == 200 and result.get('success')
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_disable_plugin():
    """Plugin devre dışı bırakma test."""
    print("\nTesting /api/editor/plugins/disable...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/editor/plugins/disable",
            json={"plugin_id": "language_python"}
        )
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Success: {result.get('success')}")
        print(f"Message: {result.get('message')}")
        return response.status_code == 200 and result.get('success')
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_configure_plugin():
    """Plugin yapılandırma test."""
    print("\nTesting /api/editor/plugins/configure...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/editor/plugins/configure",
            json={"plugin_id": "theme_dark_plus", "config": {"color": "#1e1e1e"}}
        )
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Success: {result.get('success')}")
        print(f"Message: {result.get('message')}")
        return response.status_code == 200 and result.get('success')
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_search_plugins():
    """Plugin arama test."""
    print("\nTesting /api/editor/plugins/search...")
    try:
        response = requests.get(f"{BASE_URL}/api/editor/plugins/search")
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Success: {result.get('success')}")
        print(f"Total: {result.get('total')}")
        return response.status_code == 200 and result.get('success')
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_get_plugin_status():
    """Plugin durumu alma test."""
    print("\nTesting /api/editor/plugins/{plugin_id}/status...")
    try:
        response = requests.get(f"{BASE_URL}/api/editor/plugins/theme_dark_plus/status")
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Success: {result.get('success')}")
        print(f"Status: {result.get('status')}")
        return response.status_code == 200 and result.get('success')
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_uninstall_plugin():
    """Plugin kaldırma test."""
    print("\nTesting DELETE /api/editor/plugins/uninstall...")
    try:
        response = requests.delete(
            f"{BASE_URL}/api/editor/plugins/uninstall",
            json={"plugin_id": "test_plugin"}
        )
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Success: {result.get('success')}")
        print(f"Message: {result.get('message')}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False


if __name__ == "__main__":
    print("=" * 70)
    print("Plugin Sistemi Endpoint Testleri")
    print("=" * 70)
    
    results = []
    results.append(("Get Plugins", test_get_plugins()))
    results.append(("Install Plugin", test_install_plugin()))
    results.append(("Enable Plugin", test_enable_plugin()))
    results.append(("Disable Plugin", test_disable_plugin()))
    results.append(("Configure Plugin", test_configure_plugin()))
    results.append(("Search Plugins", test_search_plugins()))
    results.append(("Get Plugin Status", test_get_plugin_status()))
    results.append(("Uninstall Plugin", test_uninstall_plugin()))
    
    print("\n" + "=" * 70)
    print("Test Sonuclari")
    print("=" * 70)
    for name, result in results:
        status = "BASARILI" if result else "BASARISIZ"
        print(f"{name}: {status}")
    
    total = len(results)
    passed = sum(1 for _, r in results if r)
    print(f"\nToplam: {passed}/{total} test basarili")
