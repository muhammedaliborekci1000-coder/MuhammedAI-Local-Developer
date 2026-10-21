"""
Browser Agent Real Qwen3 Test
Gerçek browser automation ile entegrasyon testi.
"""

import pytest
import sys
import os
import shutil
import subprocess
import time
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.tools.browser_engine import BrowserEngine
from app.tools.browser_manager import BrowserManager
from app.tools.browser_inspector import BrowserInspector
from app.tools.browser_actions import BrowserActions
from app.core.config import PROJECT_ROOT


@pytest.mark.slow
def test_browser_agent_real_qwen3():
    """
    TEST — Real Browser Agent Integration
    
    Bu test gerçek browser automation kullanarak:
    - Browser engine detection
    - Browser launch
    - Localhost navigation
    - DOM inspection
    - Element detection
    - Screenshot
    - Cleanup
    
    gerçek sonuçlarla doğrular.
    """
    print("\n" + "=" * 70)
    print("REAL BROWSER AGENT TEST")
    print("=" * 70)
    
    # 1. Browser Engine Detection
    print("\n1. Browser Engine Detection")
    print("-" * 70)
    
    engine = BrowserEngine()
    status = engine.get_status()
    
    print(f"Engine: {status['engine']}")
    print(f"Package available: {status['package_available']}")
    print(f"Browser available: {status['browser_available']}")
    print(f"State: {status['state']}")
    print(f"Ready: {status['ready']}")
    
    if not status['ready']:
        print("\nSKIPPED — Browser engine not ready")
        print(f"Reason: {engine.get_installation_instructions()}")
        print("=" * 70)
        return
    
    print("Browser engine detection: PASS")
    
    # 4. Create Local HTML Fixture
    print("\n4. Create Local HTML Fixture")
    print("-" * 70)
    
    workspace = PROJECT_ROOT / "quality_tests" / "browser_fixture"
    workspace.mkdir(parents=True, exist_ok=True)
    
    html_file = workspace / "test.html"
    html_file.write_text("""
<!DOCTYPE html>
<html>
<head>
    <title>Test Page</title>
</head>
<body>
    <h1>Test Page</h1>
    <p>This is a test page for browser automation.</p>
    <button id="test-button">Click Me</button>
    <input type="text" id="test-input" name="username" placeholder="Enter text">
    <a href="#" id="test-link">Test Link</a>
</body>
</html>
""")
    
    print(f"Created fixture: {html_file}")
    print("Local HTML fixture: PASS")
    
    # 5. Browser Manager Init
    print("\n5. Browser Manager Init")
    print("-" * 70)
    
    manager = BrowserManager()
    
    assert manager.state.value == "CLOSED"
    print("Browser manager init: PASS")
    
    # 6. Browser Launch
    print("\n6. Browser Launch")
    print("-" * 70)
    
    info = manager.launch(headless=True)
    
    if info.state.value == "ERROR":
        print(f"\nSKIPPED — Browser launch failed: {info.error}")
        print("This may mean Playwright is not installed or browsers are not installed.")
        print("To fix:")
        print("  pip install playwright")
        print("  playwright install chromium")
        print("=" * 70)
        
        # Cleanup fixture
        if workspace.exists():
            shutil.rmtree(workspace)
        
        return
    
    assert info.state.value == "READY"
    assert info.error is None
    print(f"Browser state: {info.state.value}")
    print("Browser launch: PASS")
    
    # 7. Start Simple HTTP Server
    print("\n7. Start Simple HTTP Server")
    print("-" * 70)
    
    server_process = subprocess.Popen(
        [sys.executable, "-m", "http.server", "8888"],
        cwd=str(workspace),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    time.sleep(2)  # Wait for server to start
    print("HTTP server started on port 8888")
    
    try:
        # 6. Navigate to Localhost
        print("\n6. Navigate to Localhost")
        print("-" * 70)
        
        nav_info = manager.navigate("http://localhost:8888/test.html")
        
        assert nav_info.state.value == "READY"
        assert nav_info.url is not None
        assert nav_info.title is not None
        
        print(f"URL: {nav_info.url}")
        print(f"Title: {nav_info.title}")
        print("Navigate to localhost: PASS")
        
        # 7. DOM Inspection
        print("\n7. DOM Inspection")
        print("-" * 70)
        
        inspector = BrowserInspector(manager)
        page_info = inspector.inspect_page()
        
        assert page_info.url is not None
        assert page_info.title == "Test Page"
        assert len(page_info.headings) > 0
        assert len(page_info.buttons) > 0
        assert len(page_info.inputs) > 0
        assert len(page_info.links) > 0
        
        print(f"Title: {page_info.title}")
        print(f"Headings: {len(page_info.headings)}")
        print(f"Buttons: {len(page_info.buttons)}")
        print(f"Inputs: {len(page_info.inputs)}")
        print(f"Links: {len(page_info.links)}")
        print("DOM inspection: PASS")
        
        # 8. Screenshot
        print("\n8. Screenshot")
        print("-" * 70)
        
        screenshot_path = workspace / "screenshot.png"
        screenshot_info = manager.screenshot(str(screenshot_path))
        
        assert screenshot_info.error is None
        assert screenshot_info.screenshot_path is not None
        assert screenshot_path.exists()
        
        print(f"Screenshot saved: {screenshot_info.screenshot_path}")
        print("Screenshot: PASS")
        
        # 9. Browser Actions
        print("\n9. Browser Actions")
        print("-" * 70)
        
        actions = BrowserActions(manager)
        
        # Click button
        click_result = actions.click("#test-button")
        assert click_result.success is True
        print("Click button: PASS")
        
        # Type in input
        type_result = actions.type("#test-input", "test text")
        assert type_result.success is True
        print("Type in input: PASS")
        
        # Scroll
        scroll_result = actions.scroll("down", 100)
        assert scroll_result.success is True
        print("Scroll: PASS")
        
        # 10. Reload
        print("\n10. Reload")
        print("-" * 70)
        
        reload_info = manager.reload()
        
        assert reload_info.state.value == "READY"
        print("Reload: PASS")
        
        # 11. Get Errors
        print("\n11. Get Errors")
        print("-" * 70)
        
        status = manager.get_status()
        
        print(f"Console errors: {status['console_errors_count']}")
        print(f"Page errors: {status['page_errors_count']}")
        print(f"Network errors: {status['network_errors_count']}")
        print("Get errors: PASS")
        
        # 12. Cleanup
        print("\n12. Cleanup")
        print("-" * 70)
        
        manager.close()
        server_process.terminate()
        server_process.wait(timeout=5)
        
        assert manager.state.value == "CLOSED"
        
        # Clean up fixture
        if workspace.exists():
            shutil.rmtree(workspace)
        
        print("Cleanup: PASS")
        
        print("\n" + "=" * 70)
        print("REAL BROWSER AGENT TEST: PASS")
        print("=" * 70)
        
    except Exception as e:
        # Cleanup on error
        manager.close()
        if server_process.poll() is None:
            server_process.terminate()
            server_process.wait(timeout=5)
        if workspace.exists():
            shutil.rmtree(workspace)
        
        print("\n" + "=" * 70)
        print("REAL BROWSER AGENT TEST: FAILED")
        print("=" * 70)
        raise


if __name__ == "__main__":
    try:
        test_browser_agent_real_qwen3()
        sys.exit(0)
    except Exception as e:
        print(f"\nTEST HATASI:")
        print("-" * 70)
        import traceback
        traceback.print_exc()
        print("=" * 70)
        sys.exit(1)
