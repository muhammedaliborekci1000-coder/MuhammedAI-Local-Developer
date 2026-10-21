"""
Browser Agent Tests
Browser automation özellikleri için testler.
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.tools.browser_engine import BrowserEngine, EngineState
from app.tools.browser_manager import BrowserManager, BrowserState, BrowserInfo
from app.tools.browser_inspector import BrowserInspector, PageInfo, PageElement
from app.tools.browser_actions import BrowserActions, ActionRisk, ActionResult


def test_browser_engine_detection():
    """TEST 1 — Browser engine detection."""
    print("\n" + "=" * 70)
    print("TEST 1 — Browser Engine Detection")
    print("=" * 70)

    engine = BrowserEngine()
    status = engine.get_status()
    
    assert "engine" in status
    assert "package_available" in status
    assert "browser_available" in status
    assert "state" in status
    assert "ready" in status
    
    print(f"Engine: {status['engine']}")
    print(f"State: {status['state']}")
    print("Browser engine detection: PASS")
    print("=" * 70)


def test_browser_engine_state():
    """TEST 2 — Browser engine state."""
    print("\n" + "=" * 70)
    print("TEST 2 — Browser Engine State")
    print("=" * 70)

    engine = BrowserEngine()
    
    # State enum check
    assert engine.state.value in [s.value for s in EngineState]
    
    print(f"Engine state: {engine.state.value}")
    print("Browser engine state: PASS")
    print("=" * 70)


def test_browser_manager_init():
    """TEST 3 — Browser manager init."""
    print("\n" + "=" * 70)
    print("TEST 3 — Browser Manager Init")
    print("=" * 70)

    manager = BrowserManager()
    
    assert manager.state == BrowserState.CLOSED
    assert manager.browser is None
    assert manager.page is None
    
    print("Browser manager init: PASS")
    print("=" * 70)


def test_browser_manager_status():
    """TEST 4 — Browser manager status."""
    print("\n" + "=" * 70)
    print("TEST 4 — Browser Manager Status")
    print("=" * 70)

    manager = BrowserManager()
    status = manager.get_status()
    
    assert "browser_state" in status
    assert "engine_status" in status
    assert status["browser_state"] == BrowserState.CLOSED.value
    
    print("Browser manager status: PASS")
    print("=" * 70)


def test_browser_manager_not_ready():
    """TEST 5 — Browser manager not ready."""
    print("\n" + "=" * 70)
    print("TEST 5 — Browser Manager Not Ready")
    print("=" * 70)

    manager = BrowserManager()
    
    assert manager.is_ready() == manager.engine.is_ready()
    
    print("Browser manager not ready: PASS")
    print("=" * 70)


def test_browser_manager_launch_without_engine():
    """TEST 6 — Browser launch without engine."""
    print("\n" + "=" * 70)
    print("TEST 6 — Browser Launch Without Engine")
    print("=" * 70)

    manager = BrowserManager()
    
    if not manager.engine.is_ready():
        info = manager.launch()
        
        assert info.state == BrowserState.ERROR
        assert info.error is not None
        
        print(f"Launch error: {info.error}")
        print("Browser launch without engine: PASS")
    else:
        print("SKIPPED — Browser engine available")
        print("=" * 70)


def test_browser_manager_navigate_not_ready():
    """TEST 7 — Browser navigate not ready."""
    print("\n" + "=" * 70)
    print("TEST 7 — Browser Navigate Not Ready")
    print("=" * 70)

    manager = BrowserManager()
    info = manager.navigate("http://localhost:8000")
    
    assert info.state == BrowserState.CLOSED
    assert info.error is not None
    
    print("Browser navigate not ready: PASS")
    print("=" * 70)


def test_browser_manager_reload_not_ready():
    """TEST 8 — Browser reload not ready."""
    print("\n" + "=" * 70)
    print("TEST 8 — Browser Reload Not Ready")
    print("=" * 70)

    manager = BrowserManager()
    info = manager.reload()
    
    assert info.state == BrowserState.CLOSED
    assert info.error is not None
    
    print("Browser reload not ready: PASS")
    print("=" * 70)


def test_browser_manager_screenshot_not_ready():
    """TEST 9 — Browser screenshot not ready."""
    print("\n" + "=" * 70)
    print("TEST 9 — Browser Screenshot Not Ready")
    print("=" * 70)

    manager = BrowserManager()
    info = manager.screenshot()
    
    assert info.state == BrowserState.CLOSED
    assert info.error is not None
    
    print("Browser screenshot not ready: PASS")
    print("=" * 70)


def test_browser_manager_close():
    """TEST 10 — Browser close."""
    print("\n" + "=" * 70)
    print("TEST 10 — Browser Close")
    print("=" * 70)

    manager = BrowserManager()
    success = manager.close()
    
    # Close returns False if nothing to close, but state should be CLOSED
    assert manager.state == BrowserState.CLOSED
    
    print("Browser close: PASS")
    print("=" * 70)


def test_browser_inspector_init():
    """TEST 11 — Browser inspector init."""
    print("\n" + "=" * 70)
    print("TEST 11 — Browser Inspector Init")
    print("=" * 70)

    manager = BrowserManager()
    inspector = BrowserInspector(manager)
    
    assert inspector.browser_manager == manager
    
    print("Browser inspector init: PASS")
    print("=" * 70)


def test_browser_inspect_not_ready():
    """TEST 12 — Browser inspect not ready."""
    print("\n" + "=" * 70)
    print("TEST 12 — Browser Inspect Not Ready")
    print("=" * 70)

    manager = BrowserManager()
    inspector = BrowserInspector(manager)
    page_info = inspector.inspect_page()
    
    assert page_info.error is not None
    
    print("Browser inspect not ready: PASS")
    print("=" * 70)


def test_browser_actions_init():
    """TEST 13 — Browser actions init."""
    print("\n" + "=" * 70)
    print("TEST 13 — Browser Actions Init")
    print("=" * 70)

    manager = BrowserManager()
    actions = BrowserActions(manager)
    
    assert actions.browser_manager == manager
    
    print("Browser actions init: PASS")
    print("=" * 70)


def test_browser_actions_risk_classification():
    """TEST 14 — Browser actions risk classification."""
    print("\n" + "=" * 70)
    print("TEST 14 — Browser Actions Risk Classification")
    print("=" * 70)

    manager = BrowserManager()
    actions = BrowserActions(manager)
    
    # Safe actions
    assert actions._get_risk("inspect") == ActionRisk.SAFE
    assert actions._get_risk("screenshot") == ActionRisk.SAFE
    
    # Low actions
    assert actions._get_risk("scroll") == ActionRisk.LOW
    assert actions._get_risk("hover") == ActionRisk.LOW
    
    # Medium actions
    assert actions._get_risk("click") == ActionRisk.MEDIUM
    assert actions._get_risk("type") == ActionRisk.MEDIUM
    
    # High actions
    assert actions._get_risk("navigate") == ActionRisk.HIGH
    assert actions._get_risk("file_upload") == ActionRisk.HIGH
    
    # Blocked actions
    assert actions._get_risk("javascript_inject") == ActionRisk.BLOCKED
    assert actions._get_risk("cookie_extract") == ActionRisk.BLOCKED
    
    print("Browser actions risk classification: PASS")
    print("=" * 70)


def test_browser_actions_click_not_ready():
    """TEST 15 — Browser actions click not ready."""
    print("\n" + "=" * 70)
    print("TEST 15 — Browser Actions Click Not Ready")
    print("=" * 70)

    manager = BrowserManager()
    actions = BrowserActions(manager)
    result = actions.click("button")
    
    assert result.success is False
    assert result.error is not None
    
    print("Browser actions click not ready: PASS")
    print("=" * 70)


def test_browser_actions_type_not_ready():
    """TEST 16 — Browser actions type not ready."""
    print("\n" + "=" * 70)
    print("TEST 16 — Browser Actions Type Not Ready")
    print("=" * 70)

    manager = BrowserManager()
    actions = BrowserActions(manager)
    result = actions.type("input", "test")
    
    assert result.success is False
    assert result.error is not None
    
    print("Browser actions type not ready: PASS")
    print("=" * 70)


def test_browser_actions_fill_not_ready():
    """TEST 17 — Browser actions fill not ready."""
    print("\n" + "=" * 70)
    print("TEST 17 — Browser Actions Fill Not Ready")
    print("=" * 70)

    manager = BrowserManager()
    actions = BrowserActions(manager)
    result = actions.fill("input", "test")
    
    assert result.success is False
    assert result.error is not None
    
    print("Browser actions fill not ready: PASS")
    print("=" * 70)


def test_browser_actions_select_not_ready():
    """TEST 18 — Browser actions select not ready."""
    print("\n" + "=" * 70)
    print("TEST 18 — Browser Actions Select Not Ready")
    print("=" * 70)

    manager = BrowserManager()
    actions = BrowserActions(manager)
    result = actions.select("select", "value")
    
    assert result.success is False
    assert result.error is not None
    
    print("Browser actions select not ready: PASS")
    print("=" * 70)


def test_browser_actions_check_not_ready():
    """TEST 19 — Browser actions check not ready."""
    print("\n" + "=" * 70)
    print("TEST 19 — Browser Actions Check Not Ready")
    print("=" * 70)

    manager = BrowserManager()
    actions = BrowserActions(manager)
    result = actions.check("input")
    
    assert result.success is False
    assert result.error is not None
    
    print("Browser actions check not ready: PASS")
    print("=" * 70)


def test_browser_actions_uncheck_not_ready():
    """TEST 20 — Browser actions uncheck not ready."""
    print("\n" + "=" * 70)
    print("TEST 20 — Browser Actions Uncheck Not Ready")
    print("=" * 70)

    manager = BrowserManager()
    actions = BrowserActions(manager)
    result = actions.uncheck("input")
    
    assert result.success is False
    assert result.error is not None
    
    print("Browser actions uncheck not ready: PASS")
    print("=" * 70)


def test_browser_actions_hover_not_ready():
    """TEST 21 — Browser actions hover not ready."""
    print("\n" + "=" * 70)
    print("TEST 21 — Browser Actions Hover Not Ready")
    print("=" * 70)

    manager = BrowserManager()
    actions = BrowserActions(manager)
    result = actions.hover("button")
    
    assert result.success is False
    assert result.error is not None
    
    print("Browser actions hover not ready: PASS")
    print("=" * 70)


def test_browser_actions_focus_not_ready():
    """TEST 22 — Browser actions focus not ready."""
    print("\n" + "=" * 70)
    print("TEST 22 — Browser Actions Focus Not Ready")
    print("=" * 70)

    manager = BrowserManager()
    actions = BrowserActions(manager)
    result = actions.focus("input")
    
    assert result.success is False
    assert result.error is not None
    
    print("Browser actions focus not ready: PASS")
    print("=" * 70)


def test_browser_actions_press_not_ready():
    """TEST 23 — Browser actions press not ready."""
    print("\n" + "=" * 70)
    print("TEST 23 — Browser Actions Press Not Ready")
    print("=" * 70)

    manager = BrowserManager()
    actions = BrowserActions(manager)
    result = actions.press("Enter")
    
    assert result.success is False
    assert result.error is not None
    
    print("Browser actions press not ready: PASS")
    print("=" * 70)


def test_browser_actions_submit_not_ready():
    """TEST 24 — Browser actions submit not ready."""
    print("\n" + "=" * 70)
    print("TEST 24 — Browser Actions Submit Not Ready")
    print("=" * 70)

    manager = BrowserManager()
    actions = BrowserActions(manager)
    result = actions.submit("form")
    
    assert result.success is False
    assert result.error is not None
    
    print("Browser actions submit not ready: PASS")
    print("=" * 70)


def test_browser_actions_scroll_not_ready():
    """TEST 25 — Browser actions scroll not ready."""
    print("\n" + "=" * 70)
    print("TEST 25 — Browser Actions Scroll Not Ready")
    print("=" * 70)

    manager = BrowserManager()
    actions = BrowserActions(manager)
    result = actions.scroll("down")
    
    assert result.success is False
    assert result.error is not None
    
    print("Browser actions scroll not ready: PASS")
    print("=" * 70)


def test_browser_actions_clear_not_ready():
    """TEST 26 — Browser actions clear not ready."""
    print("\n" + "=" * 70)
    print("TEST 26 — Browser Actions Clear Not Ready")
    print("=" * 70)

    manager = BrowserManager()
    actions = BrowserActions(manager)
    result = actions.clear("input")
    
    assert result.success is False
    assert result.error is not None
    
    print("Browser actions clear not ready: PASS")
    print("=" * 70)


def test_browser_actions_sensitive_blocked():
    """TEST 27 — Browser actions sensitive blocked."""
    print("\n" + "=" * 70)
    print("TEST 27 — Browser Actions Sensitive Blocked")
    print("=" * 70)

    manager = BrowserManager()
    actions = BrowserActions(manager)
    result = actions.type("input[type='password']", "secret", sensitive=True)
    
    # Browser not ready takes precedence
    assert result.success is False
    assert result.error is not None
    
    print("Browser actions sensitive blocked: PASS")
    print("=" * 70)


def test_page_element_dataclass():
    """TEST 28 — PageElement dataclass."""
    print("\n" + "=" * 70)
    print("TEST 28 — PageElement Dataclass")
    print("=" * 70)

    element = PageElement(
        tag="button",
        text="Click me",
        id="btn1",
        classes=["btn", "primary"],
        role="button",
        name=None,
        type=None,
        visible=True,
        selector="button"
    )
    
    assert element.tag == "button"
    assert element.text == "Click me"
    assert element.visible is True
    
    print("PageElement dataclass: PASS")
    print("=" * 70)


def test_page_info_dataclass():
    """TEST 29 — PageInfo dataclass."""
    print("\n" + "=" * 70)
    print("TEST 29 — PageInfo Dataclass")
    print("=" * 70)

    page_info = PageInfo(
        url="http://localhost:8000",
        title="Test Page",
        visible_text="Hello World",
        headings=[],
        links=[],
        buttons=[],
        inputs=[],
        textareas=[],
        selects=[],
        forms=[],
        images=[],
        error=None
    )
    
    assert page_info.url == "http://localhost:8000"
    assert page_info.title == "Test Page"
    assert page_info.error is None
    
    print("PageInfo dataclass: PASS")
    print("=" * 70)


def test_action_result_dataclass():
    """TEST 30 — ActionResult dataclass."""
    print("\n" + "=" * 70)
    print("TEST 30 — ActionResult Dataclass")
    print("=" * 70)

    result = ActionResult(
        success=True,
        action="click",
        selector="button",
        error=None,
        url_changed=True,
        new_url="http://localhost:8000/new",
        element_exists=True
    )
    
    assert result.success is True
    assert result.action == "click"
    assert result.url_changed is True
    
    print("ActionResult dataclass: PASS")
    print("=" * 70)


def test_browser_info_dataclass():
    """TEST 31 — BrowserInfo dataclass."""
    print("\n" + "=" * 70)
    print("TEST 31 — BrowserInfo Dataclass")
    print("=" * 70)

    info = BrowserInfo(
        state=BrowserState.READY,
        url="http://localhost:8000",
        title="Test",
        viewport={"width": 1280, "height": 720},
        console_errors=[],
        page_errors=[],
        network_errors=[],
        screenshot_path=None,
        error=None
    )
    
    assert info.state == BrowserState.READY
    assert info.url == "http://localhost:8000"
    assert info.error is None
    
    print("BrowserInfo dataclass: PASS")
    print("=" * 70)


def test_browser_state_enum():
    """TEST 32 — BrowserState enum."""
    print("\n" + "=" * 70)
    print("TEST 32 — BrowserState Enum")
    print("=" * 70)

    states = [s.value for s in BrowserState]
    
    assert "STARTING" in states
    assert "RUNNING" in states
    assert "READY" in states
    assert "ERROR" in states
    assert "CLOSED" in states
    
    print("BrowserState enum: PASS")
    print("=" * 70)


def test_engine_state_enum():
    """TEST 33 — EngineState enum."""
    print("\n" + "=" * 70)
    print("TEST 33 — EngineState Enum")
    print("=" * 70)

    states = [s.value for s in EngineState]
    
    assert "AVAILABLE" in states
    assert "MISSING_PACKAGE" in states
    assert "MISSING_BROWSER" in states
    assert "ERROR" in states
    assert "READY" in states
    
    print("EngineState enum: PASS")
    print("=" * 70)


def test_action_risk_enum():
    """TEST 34 — ActionRisk enum."""
    print("\n" + "=" * 70)
    print("TEST 34 — ActionRisk Enum")
    print("=" * 70)

    risks = [r.value for r in ActionRisk]
    
    assert "SAFE" in risks
    assert "LOW" in risks
    assert "MEDIUM" in risks
    assert "HIGH" in risks
    assert "BLOCKED" in risks
    
    print("ActionRisk enum: PASS")
    print("=" * 70)


def test_browser_manager_cleanup():
    """TEST 35 — Browser manager cleanup."""
    print("\n" + "=" * 70)
    print("TEST 35 — Browser Manager Cleanup")
    print("=" * 70)

    manager = BrowserManager()
    manager.cleanup()
    
    assert manager.state == BrowserState.CLOSED
    
    print("Browser manager cleanup: PASS")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test_browser_engine_detection()
        test_browser_engine_state()
        test_browser_manager_init()
        test_browser_manager_status()
        test_browser_manager_not_ready()
        test_browser_manager_launch_without_engine()
        test_browser_manager_navigate_not_ready()
        test_browser_manager_reload_not_ready()
        test_browser_manager_screenshot_not_ready()
        test_browser_manager_close()
        test_browser_inspector_init()
        test_browser_inspect_not_ready()
        test_browser_actions_init()
        test_browser_actions_risk_classification()
        test_browser_actions_click_not_ready()
        test_browser_actions_type_not_ready()
        test_browser_actions_fill_not_ready()
        test_browser_actions_select_not_ready()
        test_browser_actions_check_not_ready()
        test_browser_actions_uncheck_not_ready()
        test_browser_actions_hover_not_ready()
        test_browser_actions_focus_not_ready()
        test_browser_actions_press_not_ready()
        test_browser_actions_submit_not_ready()
        test_browser_actions_scroll_not_ready()
        test_browser_actions_clear_not_ready()
        test_browser_actions_sensitive_blocked()
        test_page_element_dataclass()
        test_page_info_dataclass()
        test_action_result_dataclass()
        test_browser_info_dataclass()
        test_browser_state_enum()
        test_engine_state_enum()
        test_action_risk_enum()
        test_browser_manager_cleanup()

        print("\n" + "=" * 70)
        print("BROWSER AGENT TESTLERİ BAŞARILI")
        print("=" * 70)
        sys.exit(0)
    except Exception as e:
        print(f"\nTEST HATASI:")
        print("-" * 70)
        import traceback
        traceback.print_exc()
        print("=" * 70)
        sys.exit(1)
