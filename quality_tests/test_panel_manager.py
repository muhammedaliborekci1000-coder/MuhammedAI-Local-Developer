"""
Quality Test: Panel Manager
Panel manager system testleri.
"""

import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from app.editor.panel_manager import (
    PanelType,
    PanelPosition,
    PanelState,
    Panel,
    PanelConfig,
    PanelResult,
    PanelManager
)


def test_panel_type_enum():
    """
    Test: PanelType enum.
    """
    print("=" * 70)
    print("TEST: PanelType Enum")
    print("=" * 70)
    
    assert PanelType.SIDEBAR.value == "sidebar"
    assert PanelType.BOTTOM_PANEL.value == "bottom_panel"
    assert PanelType.EXPLORER.value == "explorer"
    assert PanelType.SEARCH.value == "search"
    assert PanelType.GIT.value == "git"
    assert PanelType.DEBUG.value == "debug"
    assert PanelType.TERMINAL.value == "terminal"
    assert PanelType.OUTPUT.value == "output"
    assert PanelType.PROBLEMS.value == "problems"
    assert PanelType.EXTENSIONS.value == "extensions"
    assert PanelType.CUSTOM.value == "custom"
    
    print(f"  All enum values verified")
    print(f"  Total types: {len(PanelType)}")
    
    print("\n" + "=" * 70)
    print("PASS: PanelType enum")
    print("=" * 70)


def test_panel_position_enum():
    """
    Test: PanelPosition enum.
    """
    print("=" * 70)
    print("TEST: PanelPosition Enum")
    print("=" * 70)
    
    assert PanelPosition.LEFT.value == "left"
    assert PanelPosition.RIGHT.value == "right"
    assert PanelPosition.BOTTOM.value == "bottom"
    assert PanelPosition.TOP.value == "top"
    
    print(f"  All enum values verified")
    print(f"  Total positions: {len(PanelPosition)}")
    
    print("\n" + "=" * 70)
    print("PASS: PanelPosition enum")
    print("=" * 70)


def test_panel_state_enum():
    """
    Test: PanelState enum.
    """
    print("=" * 70)
    print("TEST: PanelState Enum")
    print("=" * 70)
    
    assert PanelState.VISIBLE.value == "visible"
    assert PanelState.HIDDEN.value == "hidden"
    assert PanelState.MINIMIZED.value == "minimized"
    assert PanelState.MAXIMIZED.value == "maximized"
    
    print(f"  All enum values verified")
    print(f"  Total states: {len(PanelState)}")
    
    print("\n" + "=" * 70)
    print("PASS: PanelState enum")
    print("=" * 70)


def test_panel_dataclass():
    """
    Test: Panel dataclass.
    """
    print("=" * 70)
    print("TEST: Panel Dataclass")
    print("=" * 70)
    
    panel = Panel(
        id="test_panel",
        name="Test Panel",
        type=PanelType.CUSTOM,
        position=PanelPosition.LEFT,
        state=PanelState.VISIBLE
    )
    
    assert panel.id == "test_panel", "ID eşleşmeli"
    assert panel.name == "Test Panel", "Name eşleşmeli"
    assert panel.type == PanelType.CUSTOM, "Type eşleşmeli"
    
    print(f"  ID: {panel.id}")
    print(f"  Name: {panel.name}")
    print(f"  Type: {panel.type.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Panel dataclass")
    print("=" * 70)


def test_panel_config_dataclass():
    """
    Test: PanelConfig dataclass.
    """
    print("=" * 70)
    print("TEST: PanelConfig Dataclass")
    print("=" * 70)
    
    config = PanelConfig(
        enable_animations=True,
        auto_hide=False
    )
    
    assert config.enable_animations == True, "Enable animations eşleşmeli"
    assert config.auto_hide == False, "Auto hide eşleşmeli"
    
    print(f"  Enable animations: {config.enable_animations}")
    print(f"  Auto hide: {config.auto_hide}")
    
    print("\n" + "=" * 70)
    print("PASS: PanelConfig dataclass")
    print("=" * 70)


def test_panel_result_dataclass():
    """
    Test: PanelResult dataclass.
    """
    print("=" * 70)
    print("TEST: PanelResult Dataclass")
    print("=" * 70)
    
    result = PanelResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.panels, list), "Panels list olmalı"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Panels: {len(result.panels)}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: PanelResult dataclass")
    print("=" * 70)


def test_panel_manager_initialization():
    """
    Test: PanelManager initialization.
    """
    print("=" * 70)
    print("TEST: PanelManager Initialization")
    print("=" * 70)
    
    config = PanelConfig()
    manager = PanelManager(config)
    
    assert manager.config == config, "Config eşleşmeli"
    assert len(manager.panels) > 0, "Panels olmalı"
    
    print(f"  Panels: {len(manager.panels)}")
    
    print("\n" + "=" * 70)
    print("PASS: PanelManager initialization")
    print("=" * 70)


def test_register_panel():
    """
    Test: Register panel.
    """
    print("=" * 70)
    print("TEST: Register Panel")
    print("=" * 70)
    
    manager = PanelManager()
    
    panel = Panel(
        id="custom_panel",
        name="Custom Panel",
        type=PanelType.CUSTOM,
        position=PanelPosition.RIGHT
    )
    
    result = manager.register_panel(panel)
    
    assert result.success == True, "Registration başarılı olmalı"
    assert "custom_panel" in manager.panels, "Panel kaydedilmeli"
    
    print(f"  Panel registered: {panel.name}")
    
    print("\n" + "=" * 70)
    print("PASS: Register panel")
    print("=" * 70)


def test_unregister_panel():
    """
    Test: Unregister panel.
    """
    print("=" * 70)
    print("TEST: Unregister Panel")
    print("=" * 70)
    
    manager = PanelManager()
    
    panel = Panel(
        id="custom_panel",
        name="Custom Panel",
        type=PanelType.CUSTOM
    )
    
    manager.register_panel(panel)
    result = manager.unregister_panel("custom_panel")
    
    assert result.success == True, "Unregistration başarılı olmalı"
    assert "custom_panel" not in manager.panels, "Panel silinmeli"
    
    print(f"  Panel unregistered: {panel.name}")
    
    print("\n" + "=" * 70)
    print("PASS: Unregister panel")
    print("=" * 70)


def test_get_panel():
    """
    Test: Get panel.
    """
    print("=" * 70)
    print("TEST: Get Panel")
    print("=" * 70)
    
    manager = PanelManager()
    
    panel = manager.get_panel("explorer")
    
    assert panel is not None, "Panel bulunmalı"
    assert panel.id == "explorer", "ID eşleşmeli"
    
    print(f"  Panel: {panel.name}")
    
    print("\n" + "=" * 70)
    print("PASS: Get panel")
    print("=" * 70)


def test_get_all_panels():
    """
    Test: Get all panels.
    """
    print("=" * 70)
    print("TEST: Get All Panels")
    print("=" * 70)
    
    manager = PanelManager()
    
    panels = manager.get_all_panels()
    
    assert len(panels) > 0, "Panels olmalı"
    
    print(f"  Total panels: {len(panels)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get all panels")
    print("=" * 70)


def test_get_panels_by_position():
    """
    Test: Get panels by position.
    """
    print("=" * 70)
    print("TEST: Get Panels by Position")
    print("=" * 70)
    
    manager = PanelManager()
    
    left_panels = manager.get_panels_by_position(PanelPosition.LEFT)
    
    assert len(left_panels) > 0, "Left panels olmalı"
    
    print(f"  Left panels: {len(left_panels)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get panels by position")
    print("=" * 70)


def test_get_panels_by_type():
    """
    Test: Get panels by type.
    """
    print("=" * 70)
    print("TEST: Get Panels by Type")
    print("=" * 70)
    
    manager = PanelManager()
    
    explorer_panels = manager.get_panels_by_type(PanelType.EXPLORER)
    
    assert len(explorer_panels) > 0, "Explorer panels olmalı"
    
    print(f"  Explorer panels: {len(explorer_panels)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get panels by type")
    print("=" * 70)


def test_show_panel():
    """
    Test: Show panel.
    """
    print("=" * 70)
    print("TEST: Show Panel")
    print("=" * 70)
    
    manager = PanelManager()
    
    result = manager.show_panel("explorer")
    
    assert result.success == True, "Show başarılı olmalı"
    assert result.panel.state == PanelState.VISIBLE, "State visible olmalı"
    
    print(f"  Panel shown: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Show panel")
    print("=" * 70)


def test_hide_panel():
    """
    Test: Hide panel.
    """
    print("=" * 70)
    print("TEST: Hide Panel")
    print("=" * 70)
    
    manager = PanelManager()
    
    result = manager.hide_panel("explorer")
    
    assert result.success == True, "Hide başarılı olmalı"
    assert result.panel.state == PanelState.HIDDEN, "State hidden olmalı"
    
    print(f"  Panel hidden: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Hide panel")
    print("=" * 70)


def test_toggle_panel():
    """
    Test: Toggle panel.
    """
    print("=" * 70)
    print("TEST: Toggle Panel")
    print("=" * 70)
    
    manager = PanelManager()
    
    result = manager.toggle_panel("explorer")
    
    assert result.success == True, "Toggle başarılı olmalı"
    
    print(f"  Panel toggled: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Toggle panel")
    print("=" * 70)


def test_minimize_panel():
    """
    Test: Minimize panel.
    """
    print("=" * 70)
    print("TEST: Minimize Panel")
    print("=" * 70)
    
    manager = PanelManager()
    
    result = manager.minimize_panel("explorer")
    
    assert result.success == True, "Minimize başarılı olmalı"
    assert result.panel.state == PanelState.MINIMIZED, "State minimized olmalı"
    
    print(f"  Panel minimized: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Minimize panel")
    print("=" * 70)


def test_maximize_panel():
    """
    Test: Maximize panel.
    """
    print("=" * 70)
    print("TEST: Maximize Panel")
    print("=" * 70)
    
    manager = PanelManager()
    
    result = manager.maximize_panel("explorer")
    
    assert result.success == True, "Maximize başarılı olmalı"
    assert result.panel.state == PanelState.MAXIMIZED, "State maximized olmalı"
    
    print(f"  Panel maximized: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Maximize panel")
    print("=" * 70)


def test_set_active_panel():
    """
    Test: Set active panel.
    """
    print("=" * 70)
    print("TEST: Set Active Panel")
    print("=" * 70)
    
    manager = PanelManager()
    
    result = manager.set_active_panel("explorer")
    
    assert result.success == True, "Set başarılı olmalı"
    assert manager.active_panel_id == "explorer", "Active ID eşleşmeli"
    
    print(f"  Active panel set: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set active panel")
    print("=" * 70)


def test_get_active_panel():
    """
    Test: Get active panel.
    """
    print("=" * 70)
    print("TEST: Get Active Panel")
    print("=" * 70)
    
    manager = PanelManager()
    
    manager.set_active_panel("explorer")
    active_panel = manager.get_active_panel()
    
    assert active_panel is not None, "Active panel olmalı"
    assert active_panel.id == "explorer", "ID eşleşmeli"
    
    print(f"  Active panel: {active_panel.name}")
    
    print("\n" + "=" * 70)
    print("PASS: Get active panel")
    print("=" * 70)


def test_pin_panel():
    """
    Test: Pin panel.
    """
    print("=" * 70)
    print("TEST: Pin Panel")
    print("=" * 70)
    
    manager = PanelManager()
    
    result = manager.pin_panel("explorer")
    
    assert result.success == True, "Pin başarılı olmalı"
    assert result.panel.is_pinned == True, "Pinned olmalı"
    
    print(f"  Panel pinned: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Pin panel")
    print("=" * 70)


def test_unpin_panel():
    """
    Test: Unpin panel.
    """
    print("=" * 70)
    print("TEST: Unpin Panel")
    print("=" * 70)
    
    manager = PanelManager()
    
    manager.pin_panel("explorer")
    result = manager.unpin_panel("explorer")
    
    assert result.success == True, "Unpin başarılı olmalı"
    assert result.panel.is_pinned == False, "Unpinned olmalı"
    
    print(f"  Panel unpinned: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Unpin panel")
    print("=" * 70)


def test_resize_panel():
    """
    Test: Resize panel.
    """
    print("=" * 70)
    print("TEST: Resize Panel")
    print("=" * 70)
    
    manager = PanelManager()
    
    result = manager.resize_panel("explorer", width=300, height=400)
    
    assert result.success == True, "Resize başarılı olmalı"
    assert result.panel.width == 300, "Width eşleşmeli"
    assert result.panel.height == 400, "Height eşleşmeli"
    
    print(f"  Panel resized: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Resize panel")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    manager = PanelManager()
    
    new_config = PanelConfig(max_panels_per_side=10)
    result = manager.update_config(new_config)
    
    assert result.success == True, "Update başarılı olmalı"
    assert manager.config.max_panels_per_side == 10, "Config güncellenmeli"
    
    print(f"  Max panels per side: {manager.config.max_panels_per_side}")
    
    print("\n" + "=" * 70)
    print("PASS: Update config")
    print("=" * 70)


def test_get_config():
    """
    Test: Get config.
    """
    print("=" * 70)
    print("TEST: Get Config")
    print("=" * 70)
    
    config = PanelConfig(max_panels_per_side=10)
    manager = PanelManager(config)
    
    retrieved_config = manager.get_config()
    
    assert retrieved_config.max_panels_per_side == 10, "Config eşleşmeli"
    
    print(f"  Max panels per side: {retrieved_config.max_panels_per_side}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_panel_type_enum()
        test2 = test_panel_position_enum()
        test3 = test_panel_state_enum()
        test4 = test_panel_dataclass()
        test5 = test_panel_config_dataclass()
        test6 = test_panel_result_dataclass()
        test7 = test_panel_manager_initialization()
        test8 = test_register_panel()
        test9 = test_unregister_panel()
        test10 = test_get_panel()
        test11 = test_get_all_panels()
        test12 = test_get_panels_by_position()
        test13 = test_get_panels_by_type()
        test14 = test_show_panel()
        test15 = test_hide_panel()
        test16 = test_toggle_panel()
        test17 = test_minimize_panel()
        test18 = test_maximize_panel()
        test19 = test_set_active_panel()
        test20 = test_get_active_panel()
        test21 = test_pin_panel()
        test22 = test_unpin_panel()
        test23 = test_resize_panel()
        test24 = test_update_config()
        test25 = test_get_config()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"PanelType Enum: {'PASS' if test1 else 'FAIL'}")
        print(f"PanelPosition Enum: {'PASS' if test2 else 'FAIL'}")
        print(f"PanelState Enum: {'PASS' if test3 else 'FAIL'}")
        print(f"Panel Dataclass: {'PASS' if test4 else 'FAIL'}")
        print(f"PanelConfig Dataclass: {'PASS' if test5 else 'FAIL'}")
        print(f"PanelResult Dataclass: {'PASS' if test6 else 'FAIL'}")
        print(f"PanelManager Initialization: {'PASS' if test7 else 'FAIL'}")
        print(f"Register Panel: {'PASS' if test8 else 'FAIL'}")
        print(f"Unregister Panel: {'PASS' if test9 else 'FAIL'}")
        print(f"Get Panel: {'PASS' if test10 else 'FAIL'}")
        print(f"Get All Panels: {'PASS' if test11 else 'FAIL'}")
        print(f"Get Panels by Position: {'PASS' if test12 else 'FAIL'}")
        print(f"Get Panels by Type: {'PASS' if test13 else 'FAIL'}")
        print(f"Show Panel: {'PASS' if test14 else 'FAIL'}")
        print(f"Hide Panel: {'PASS' if test15 else 'FAIL'}")
        print(f"Toggle Panel: {'PASS' if test16 else 'FAIL'}")
        print(f"Minimize Panel: {'PASS' if test17 else 'FAIL'}")
        print(f"Maximize Panel: {'PASS' if test18 else 'FAIL'}")
        print(f"Set Active Panel: {'PASS' if test19 else 'FAIL'}")
        print(f"Get Active Panel: {'PASS' if test20 else 'FAIL'}")
        print(f"Pin Panel: {'PASS' if test21 else 'FAIL'}")
        print(f"Unpin Panel: {'PASS' if test22 else 'FAIL'}")
        print(f"Resize Panel: {'PASS' if test23 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test24 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test25 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14, test15, test16, test17, test18, test19, test20, test21, test22, test23, test24, test25])
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
