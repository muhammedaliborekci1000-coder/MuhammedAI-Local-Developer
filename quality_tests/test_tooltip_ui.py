"""
Quality Test: Tooltip UI
Tooltip UI system testleri for UI module.
"""

import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from app.ui.tooltip_ui import (
    TooltipPosition,
    TooltipTrigger,
    Tooltip,
    TooltipConfig,
    TooltipResult,
    TooltipUIManager
)


def test_tooltip_position_enum():
    """
    Test: TooltipPosition enum.
    """
    print("=" * 70)
    print("TEST: TooltipPosition Enum")
    print("=" * 70)
    
    assert TooltipPosition.TOP.value == "top"
    assert TooltipPosition.BOTTOM.value == "bottom"
    assert TooltipPosition.LEFT.value == "left"
    assert TooltipPosition.RIGHT.value == "right"
    assert TooltipPosition.TOP_LEFT.value == "top_left"
    assert TooltipPosition.TOP_RIGHT.value == "top_right"
    assert TooltipPosition.BOTTOM_LEFT.value == "bottom_left"
    assert TooltipPosition.BOTTOM_RIGHT.value == "bottom_right"
    assert TooltipPosition.AUTO.value == "auto"
    assert TooltipPosition.CUSTOM.value == "custom"
    
    print(f"  All enum values verified")
    print(f"  Total positions: {len(TooltipPosition)}")
    
    print("\n" + "=" * 70)
    print("PASS: TooltipPosition enum")
    print("=" * 70)


def test_tooltip_trigger_enum():
    """
    Test: TooltipTrigger enum.
    """
    print("=" * 70)
    print("TEST: TooltipTrigger Enum")
    print("=" * 70)
    
    assert TooltipTrigger.HOVER.value == "hover"
    assert TooltipTrigger.CLICK.value == "click"
    assert TooltipTrigger.FOCUS.value == "focus"
    assert TooltipTrigger.MANUAL.value == "manual"
    assert TooltipTrigger.CUSTOM.value == "custom"
    
    print(f"  All enum values verified")
    print(f"  Total triggers: {len(TooltipTrigger)}")
    
    print("\n" + "=" * 70)
    print("PASS: TooltipTrigger enum")
    print("=" * 70)


def test_tooltip_dataclass():
    """
    Test: Tooltip dataclass.
    """
    print("=" * 70)
    print("TEST: Tooltip Dataclass")
    print("=" * 70)
    
    tooltip = Tooltip(
        id="tooltip_1",
        content="This is a tooltip",
        target_id="button_1"
    )
    
    assert tooltip.id == "tooltip_1", "ID eşleşmeli"
    assert tooltip.content == "This is a tooltip", "Content eşleşmeli"
    assert tooltip.target_id == "button_1", "Target ID eşleşmeli"
    
    print(f"  ID: {tooltip.id}")
    print(f"  Content: {tooltip.content}")
    print(f"  Target ID: {tooltip.target_id}")
    
    print("\n" + "=" * 70)
    print("PASS: Tooltip dataclass")
    print("=" * 70)


def test_tooltip_config_dataclass():
    """
    Test: TooltipConfig dataclass.
    """
    print("=" * 70)
    print("TEST: TooltipConfig Dataclass")
    print("=" * 70)
    
    config = TooltipConfig(
        enabled=True,
        show_arrow=True
    )
    
    assert config.enabled == True, "Enabled eşleşmeli"
    assert config.show_arrow == True, "Show arrow eşleşmeli"
    
    print(f"  Enabled: {config.enabled}")
    print(f"  Show arrow: {config.show_arrow}")
    
    print("\n" + "=" * 70)
    print("PASS: TooltipConfig dataclass")
    print("=" * 70)


def test_tooltip_result_dataclass():
    """
    Test: TooltipResult dataclass.
    """
    print("=" * 70)
    print("TEST: TooltipResult Dataclass")
    print("=" * 70)
    
    result = TooltipResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.tooltips, list), "Tooltips list olmalı"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Tooltips: {len(result.tooltips)}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: TooltipResult dataclass")
    print("=" * 70)


def test_tooltip_ui_manager_initialization():
    """
    Test: TooltipUIManager initialization.
    """
    print("=" * 70)
    print("TEST: TooltipUIManager Initialization")
    print("=" * 70)
    
    config = TooltipConfig()
    manager = TooltipUIManager(config)
    
    assert manager.config == config, "Config eşleşmeli"
    assert len(manager.tooltips) == 0, "Tooltips boş olmalı"
    
    print(f"  Tooltips: {len(manager.tooltips)}")
    
    print("\n" + "=" * 70)
    print("PASS: TooltipUIManager initialization")
    print("=" * 70)


def test_add_tooltip():
    """
    Test: Add tooltip.
    """
    print("=" * 70)
    print("TEST: Add Tooltip")
    print("=" * 70)
    
    manager = TooltipUIManager()
    
    tooltip = Tooltip(
        id="",
        content="This is a tooltip",
        target_id="button_1"
    )
    
    result = manager.add_tooltip(tooltip)
    
    assert result.success == True, "Ekleme başarılı olmalı"
    assert result.tooltip is not None, "Tooltip olmalı"
    assert len(manager.tooltips) > 0, "Tooltip eklenmeli"
    
    print(f"  Tooltip added: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add tooltip")
    print("=" * 70)


def test_remove_tooltip():
    """
    Test: Remove tooltip.
    """
    print("=" * 70)
    print("TEST: Remove Tooltip")
    print("=" * 70)
    
    manager = TooltipUIManager()
    
    tooltip = Tooltip(
        id="",
        content="This is a tooltip",
        target_id="button_1"
    )
    
    result = manager.add_tooltip(tooltip)
    tooltip_id = result.tooltip.id
    
    result = manager.remove_tooltip(tooltip_id)
    
    assert result.success == True, "Silme başarılı olmalı"
    assert tooltip_id not in manager.tooltips, "Tooltip silinmeli"
    
    print(f"  Tooltip removed: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Remove tooltip")
    print("=" * 70)


def test_get_tooltip():
    """
    Test: Get tooltip.
    """
    print("=" * 70)
    print("TEST: Get Tooltip")
    print("=" * 70)
    
    manager = TooltipUIManager()
    
    tooltip = Tooltip(
        id="",
        content="This is a tooltip",
        target_id="button_1"
    )
    
    result = manager.add_tooltip(tooltip)
    tooltip_id = result.tooltip.id
    
    retrieved_tooltip = manager.get_tooltip(tooltip_id)
    
    assert retrieved_tooltip is not None, "Tooltip bulunmalı"
    assert retrieved_tooltip.id == tooltip_id, "ID eşleşmeli"
    
    print(f"  Tooltip: {retrieved_tooltip.content}")
    
    print("\n" + "=" * 70)
    print("PASS: Get tooltip")
    print("=" * 70)


def test_get_all_tooltips():
    """
    Test: Get all tooltips.
    """
    print("=" * 70)
    print("TEST: Get All Tooltips")
    print("=" * 70)
    
    manager = TooltipUIManager()
    
    tooltip = Tooltip(
        id="",
        content="This is a tooltip",
        target_id="button_1"
    )
    
    manager.add_tooltip(tooltip)
    tooltips = manager.get_all_tooltips()
    
    assert len(tooltips) > 0, "Tooltips olmalı"
    
    print(f"  Total tooltips: {len(tooltips)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get all tooltips")
    print("=" * 70)


def test_get_tooltip_by_target():
    """
    Test: Get tooltip by target.
    """
    print("=" * 70)
    print("TEST: Get Tooltip by Target")
    print("=" * 70)
    
    manager = TooltipUIManager()
    
    tooltip = Tooltip(
        id="",
        content="This is a tooltip",
        target_id="button_1"
    )
    
    manager.add_tooltip(tooltip)
    retrieved_tooltip = manager.get_tooltip_by_target("button_1")
    
    assert retrieved_tooltip is not None, "Tooltip bulunmalı"
    assert retrieved_tooltip.target_id == "button_1", "Target ID eşleşmeli"
    
    print(f"  Tooltip: {retrieved_tooltip.content}")
    
    print("\n" + "=" * 70)
    print("PASS: Get tooltip by target")
    print("=" * 70)


def test_show_tooltip():
    """
    Test: Show tooltip.
    """
    print("=" * 70)
    print("TEST: Show Tooltip")
    print("=" * 70)
    
    manager = TooltipUIManager()
    
    tooltip = Tooltip(
        id="",
        content="This is a tooltip",
        target_id="button_1"
    )
    
    result = manager.add_tooltip(tooltip)
    tooltip_id = result.tooltip.id
    
    result = manager.show_tooltip(tooltip_id)
    
    assert result.success == True, "Show başarılı olmalı"
    
    print(f"  Tooltip shown: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Show tooltip")
    print("=" * 70)


def test_hide_tooltip():
    """
    Test: Hide tooltip.
    """
    print("=" * 70)
    print("TEST: Hide Tooltip")
    print("=" * 70)
    
    manager = TooltipUIManager()
    
    tooltip = Tooltip(
        id="",
        content="This is a tooltip",
        target_id="button_1"
    )
    
    result = manager.add_tooltip(tooltip)
    tooltip_id = result.tooltip.id
    
    manager.show_tooltip(tooltip_id)
    result = manager.hide_tooltip(tooltip_id)
    
    assert result.success == True, "Hide başarılı olmalı"
    
    print(f"  Tooltip hidden: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Hide tooltip")
    print("=" * 70)


def test_set_tooltip_position():
    """
    Test: Set tooltip position.
    """
    print("=" * 70)
    print("TEST: Set Tooltip Position")
    print("=" * 70)
    
    manager = TooltipUIManager()
    
    tooltip = Tooltip(
        id="",
        content="This is a tooltip",
        target_id="button_1"
    )
    
    result = manager.add_tooltip(tooltip)
    tooltip_id = result.tooltip.id
    
    result = manager.set_tooltip_position(tooltip_id, TooltipPosition.BOTTOM)
    
    assert result.success == True, "Set başarılı olmalı"
    
    print(f"  Tooltip position set: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set tooltip position")
    print("=" * 70)


def test_set_tooltip_content():
    """
    Test: Set tooltip content.
    """
    print("=" * 70)
    print("TEST: Set Tooltip Content")
    print("=" * 70)
    
    manager = TooltipUIManager()
    
    tooltip = Tooltip(
        id="",
        content="This is a tooltip",
        target_id="button_1"
    )
    
    result = manager.add_tooltip(tooltip)
    tooltip_id = result.tooltip.id
    
    result = manager.set_tooltip_content(tooltip_id, "New content")
    
    assert result.success == True, "Set başarılı olmalı"
    
    print(f"  Tooltip content updated: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set tooltip content")
    print("=" * 70)


def test_set_tooltip_enabled():
    """
    Test: Set tooltip enabled.
    """
    print("=" * 70)
    print("TEST: Set Tooltip Enabled")
    print("=" * 70)
    
    manager = TooltipUIManager()
    
    tooltip = Tooltip(
        id="",
        content="This is a tooltip",
        target_id="button_1"
    )
    
    result = manager.add_tooltip(tooltip)
    tooltip_id = result.tooltip.id
    
    result = manager.set_tooltip_enabled(tooltip_id, False)
    
    assert result.success == True, "Set başarılı olmalı"
    
    print(f"  Tooltip enabled state: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set tooltip enabled")
    print("=" * 70)


def test_set_tooltip_delay():
    """
    Test: Set tooltip delay.
    """
    print("=" * 70)
    print("TEST: Set Tooltip Delay")
    print("=" * 70)
    
    manager = TooltipUIManager()
    
    tooltip = Tooltip(
        id="",
        content="This is a tooltip",
        target_id="button_1"
    )
    
    result = manager.add_tooltip(tooltip)
    tooltip_id = result.tooltip.id
    
    result = manager.set_tooltip_delay(tooltip_id, 500)
    
    assert result.success == True, "Set başarılı olmalı"
    
    print(f"  Tooltip delay set: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set tooltip delay")
    print("=" * 70)


def test_set_tooltip_duration():
    """
    Test: Set tooltip duration.
    """
    print("=" * 70)
    print("TEST: Set Tooltip Duration")
    print("=" * 70)
    
    manager = TooltipUIManager()
    
    tooltip = Tooltip(
        id="",
        content="This is a tooltip",
        target_id="button_1"
    )
    
    result = manager.add_tooltip(tooltip)
    tooltip_id = result.tooltip.id
    
    result = manager.set_tooltip_duration(tooltip_id, 2000)
    
    assert result.success == True, "Set başarılı olmalı"
    
    print(f"  Tooltip duration set: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set tooltip duration")
    print("=" * 70)


def test_hide_all_tooltips():
    """
    Test: Hide all tooltips.
    """
    print("=" * 70)
    print("TEST: Hide All Tooltips")
    print("=" * 70)
    
    manager = TooltipUIManager()
    
    tooltip = Tooltip(
        id="",
        content="This is a tooltip",
        target_id="button_1"
    )
    
    result = manager.add_tooltip(tooltip)
    manager.show_tooltip(result.tooltip.id)
    
    result = manager.hide_all_tooltips()
    
    assert result.success == True, "Hide başarılı olmalı"
    
    visible_tooltips = [t for t in manager.tooltips.values() if t.is_visible]
    assert len(visible_tooltips) == 0, "Tüm tooltip'lar gizlenmeli"
    
    print(f"  All tooltips hidden: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Hide all tooltips")
    print("=" * 70)


def test_clear_all_tooltips():
    """
    Test: Clear all tooltips.
    """
    print("=" * 70)
    print("TEST: Clear All Tooltips")
    print("=" * 70)
    
    manager = TooltipUIManager()
    
    tooltip = Tooltip(
        id="",
        content="This is a tooltip",
        target_id="button_1"
    )
    
    manager.add_tooltip(tooltip)
    result = manager.clear_all_tooltips()
    
    assert result.success == True, "Clear başarılı olmalı"
    assert len(manager.tooltips) == 0, "Tooltips temizlenmeli"
    
    print(f"  All tooltips cleared: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear all tooltips")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    manager = TooltipUIManager()
    
    new_config = TooltipConfig(max_tooltips=100)
    result = manager.update_config(new_config)
    
    assert result.success == True, "Update başarılı olmalı"
    assert manager.config.max_tooltips == 100, "Config güncellenmeli"
    
    print(f"  Max tooltips: {manager.config.max_tooltips}")
    
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
    
    config = TooltipConfig(max_tooltips=100)
    manager = TooltipUIManager(config)
    
    retrieved_config = manager.get_config()
    
    assert retrieved_config.max_tooltips == 100, "Config eşleşmeli"
    
    print(f"  Max tooltips: {retrieved_config.max_tooltips}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_tooltip_position_enum()
        test2 = test_tooltip_trigger_enum()
        test3 = test_tooltip_dataclass()
        test4 = test_tooltip_config_dataclass()
        test5 = test_tooltip_result_dataclass()
        test6 = test_tooltip_ui_manager_initialization()
        test7 = test_add_tooltip()
        test8 = test_remove_tooltip()
        test9 = test_get_tooltip()
        test10 = test_get_all_tooltips()
        test11 = test_get_tooltip_by_target()
        test12 = test_show_tooltip()
        test13 = test_hide_tooltip()
        test14 = test_set_tooltip_position()
        test15 = test_set_tooltip_content()
        test16 = test_set_tooltip_enabled()
        test17 = test_set_tooltip_delay()
        test18 = test_set_tooltip_duration()
        test19 = test_hide_all_tooltips()
        test20 = test_clear_all_tooltips()
        test21 = test_update_config()
        test22 = test_get_config()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"TooltipPosition Enum: {'PASS' if test1 else 'FAIL'}")
        print(f"TooltipTrigger Enum: {'PASS' if test2 else 'FAIL'}")
        print(f"Tooltip Dataclass: {'PASS' if test3 else 'FAIL'}")
        print(f"TooltipConfig Dataclass: {'PASS' if test4 else 'FAIL'}")
        print(f"TooltipResult Dataclass: {'PASS' if test5 else 'FAIL'}")
        print(f"TooltipUIManager Initialization: {'PASS' if test6 else 'FAIL'}")
        print(f"Add Tooltip: {'PASS' if test7 else 'FAIL'}")
        print(f"Remove Tooltip: {'PASS' if test8 else 'FAIL'}")
        print(f"Get Tooltip: {'PASS' if test9 else 'FAIL'}")
        print(f"Get All Tooltips: {'PASS' if test10 else 'FAIL'}")
        print(f"Get Tooltip by Target: {'PASS' if test11 else 'FAIL'}")
        print(f"Show Tooltip: {'PASS' if test12 else 'FAIL'}")
        print(f"Hide Tooltip: {'PASS' if test13 else 'FAIL'}")
        print(f"Set Tooltip Position: {'PASS' if test14 else 'FAIL'}")
        print(f"Set Tooltip Content: {'PASS' if test15 else 'FAIL'}")
        print(f"Set Tooltip Enabled: {'PASS' if test16 else 'FAIL'}")
        print(f"Set Tooltip Delay: {'PASS' if test17 else 'FAIL'}")
        print(f"Set Tooltip Duration: {'PASS' if test18 else 'FAIL'}")
        print(f"Hide All Tooltips: {'PASS' if test19 else 'FAIL'}")
        print(f"Clear All Tooltips: {'PASS' if test20 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test21 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test22 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14, test15, test16, test17, test18, test19, test20, test21, test22])
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
