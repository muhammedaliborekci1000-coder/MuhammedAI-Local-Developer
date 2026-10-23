"""
Git Entegrasyonu Endpoint Testleri
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000"


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


def test_git_commit():
    """Git commit endpoint test."""
    print("\nTesting /api/editor/git/commit...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/editor/git/commit",
            json={"message": "Test commit"}
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_git_push():
    """Git push endpoint test."""
    print("\nTesting /api/editor/git/push...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/editor/git/push",
            json={"remote": "origin", "force": False}
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_git_pull():
    """Git pull endpoint test."""
    print("\nTesting /api/editor/git/pull...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/editor/git/pull",
            json={"remote": "origin", "rebase": False}
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_git_log():
    """Git log endpoint test."""
    print("\nTesting /api/editor/git/log...")
    try:
        response = requests.get(f"{BASE_URL}/api/editor/git/log")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_git_branch():
    """Git branch endpoint test."""
    print("\nTesting /api/editor/git/branch...")
    try:
        response = requests.get(f"{BASE_URL}/api/editor/git/branch")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_git_checkout():
    """Git checkout endpoint test."""
    print("\nTesting /api/editor/git/checkout...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/editor/git/checkout",
            json={"branch": "main"}
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_git_diff():
    """Git diff endpoint test."""
    print("\nTesting /api/editor/git/diff...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/editor/git/diff",
            json={"file_path": None, "staged": False}
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_git_stage():
    """Git stage endpoint test."""
    print("\nTesting /api/editor/git/stage...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/editor/git/stage",
            json={"file_path": "test.py"}
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_git_unstage():
    """Git unstage endpoint test."""
    print("\nTesting /api/editor/git/unstage...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/editor/git/unstage",
            json={"file_path": "test.py"}
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_git_stash():
    """Git stash endpoint test."""
    print("\nTesting /api/editor/git/stash...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/editor/git/stash",
            json={"message": "Test stash"}
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_git_stash_list():
    """Git stash list endpoint test."""
    print("\nTesting /api/editor/git/stash/list...")
    try:
        response = requests.get(f"{BASE_URL}/api/editor/git/stash/list")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False


if __name__ == "__main__":
    print("=" * 70)
    print("Git Entegrasyonu Endpoint Testleri")
    print("=" * 70)
    
    results = []
    results.append(("Git Status", test_git_status()))
    results.append(("Git Commit", test_git_commit()))
    results.append(("Git Push", test_git_push()))
    results.append(("Git Pull", test_git_pull()))
    results.append(("Git Log", test_git_log()))
    results.append(("Git Branch", test_git_branch()))
    results.append(("Git Checkout", test_git_checkout()))
    results.append(("Git Diff", test_git_diff()))
    results.append(("Git Stage", test_git_stage()))
    results.append(("Git Unstage", test_git_unstage()))
    results.append(("Git Stash", test_git_stash()))
    results.append(("Git Stash List", test_git_stash_list()))
    
    print("\n" + "=" * 70)
    print("Test Sonuclari")
    print("=" * 70)
    for name, result in results:
        status = "BASARILI" if result else "BASARISIZ"
        print(f"{name}: {status}")
    
    total = len(results)
    passed = sum(1 for _, r in results if r)
    print(f"\nToplam: {passed}/{total} test basarili")
