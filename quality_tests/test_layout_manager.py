"""
Quality Test: Layout Manager
Layout manager system testleri for UI module.
"""

import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from app.ui.layout_manager import (
    LayoutType,
    PanelType,
    ResizeDirection,
    Panel,
    Layout,
    LayoutConfig,
    LayoutResult,
    LayoutManager
)


def test_layout_type_enum():
    """
    Test: LayoutType enum.
    """
    print("=" * 70)
    print("TEST: LayoutType Enum")
    print("=" * 70)
    
    assert LayoutType.SINGLE.value == "single"
    assert LayoutType.SPLIT_VERTICAL.value == "split_vertical"
    assert LayoutType.SPLIT_HORIZONTAL.value == "split_horizontal"
    assert LayoutType.GRID.value == "grid"
    assert LayoutType.TABS.value == "tabs"
    assert LayoutType.CUSTOM.value == "custom"
    
    print(f"  All enum values verified")
    print(f"  Total types: {len(LayoutType)}")
    
    print("\n" + "=" * 70)
    print("PASS: LayoutType enum")
    print("=" * 70)


def test_panel_type_enum():
    """
    Test: PanelType enum.
    """
    print("=" * 70)
    print("TEST: PanelType Enum")
    print("=" * 70)
    
    assert PanelType.EDITOR.value == "editor"
    assert PanelType.SIDEBAR.value == "sidebar"
    assert PanelType.TERMINAL.value == "terminal"
    assert PanelType.OUTPUT.value == "output"
    assert PanelType.EXPLORER.value == "explorer"
    assert PanelType.SEARCH.value == "search"
    assert PanelType.DEBUG.value == "debug"
    assert PanelType.CUSTOM.value == "custom"
    
    print(f"  All enum values verified")
    print(f"  Total types: {len(PanelType)}")
    
    print("\n" + "=" * 70)
    print("PASS: PanelType enum")
    print("=" * 70)


def test_resize_direction_enum():
    """
    Test: ResizeDirection enum.
    """
    print("=" * 70)
    print("TEST: ResizeDirection Enum")
    print("=" * 70)
    
    assert ResizeDirection.HORIZONTAL.value == "horizontal"
    assert ResizeDirection.VERTICAL.value == "vertical"
    assert ResizeDirection.BOTH.value == "both"
    assert ResizeDirection.CUSTOM.value == "custom"
    
    print(f"  All enum values verified")
    print(f"  Total directions: {len(ResizeDirection)}")
    
    print("\n" + "=" * 70)
    print("PASS: ResizeDirection enum")
    print("=" * 70)


def test_panel_dataclass():
    """
    Test: Panel dataclass.
    """
    print("=" * 70)
    print("TEST: Panel Dataclass")
    print("=" * 70)
    
    panel = Panel(
        id="panel_1",
        type=PanelType.EDITOR,
        title="Editor"
    )
    
    assert panel.id == "panel_1", "ID eşleşmeli"
    assert panel.type == PanelType.EDITOR, "Type eşleşmeli"
    assert panel.title == "Editor", "Title eşleşmeli"
    
    print(f"  ID: {panel.id}")
    print(f"  Type: {panel.type.value}")
    print(f"  Title: {panel.title}")
    
    print("\n" + "=" * 70)
    print("PASS: Panel dataclass")
    print("=" * 70)


def test_layout_dataclass():
    """
    Test: Layout dataclass.
    """
    print("=" * 70)
    print("TEST: Layout Dataclass")
    print("=" * 70)
    
    layout = Layout(
        id="layout_1",
        name="Default",
        type=LayoutType.SINGLE
    )
    
    assert layout.id == "layout_1", "ID eşleşmeli"
    assert layout.name == "Default", "Name eşleşmeli"
    assert layout.type == LayoutType.SINGLE, "Type eşleşmeli"
    
    print(f"  ID: {layout.id}")
    print(f"  Name: {layout.name}")
    print(f"  Type: {layout.type.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Layout dataclass")
    print("=" * 70)


def test_layout_config_dataclass():
    """
    Test: LayoutConfig dataclass.
    """
    print("=" * 70)
    print("TEST: LayoutConfig Dataclass")
    print("=" * 70)
    
    config = LayoutConfig(
        enabled=True,
        enable_resizing=True
    )
    
    assert config.enabled == True, "Enabled eşleşmeli"
    assert config.enable_resizing == True, "Enable resizing eşleşmeli"
    
    print(f"  Enabled: {config.enabled}")
    print(f"  Enable resizing: {config.enable_resizing}")
    
    print("\n" + "=" * 70)
    print("PASS: LayoutConfig dataclass")
    print("=" * 70)


def test_layout_result_dataclass():
    """
    Test: LayoutResult dataclass.
    """
    print("=" * 70)
    print("TEST: LayoutResult Dataclass")
    print("=" * 70)
    
    result = LayoutResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.layouts, list), "Layouts list olmalı"
    assert isinstance(result.panels, list), "Panels list olmalı"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Layouts: {len(result.layouts)}")
    print(f"  Panels: {len(result.panels)}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: LayoutResult dataclass")
    print("=" * 70)


def test_layout_manager_initialization():
    """
    Test: LayoutManager initialization.
    """
    print("=" * 70)
    print("TEST: LayoutManager Initialization")
    print("=" * 70)
    
    config = LayoutConfig()
    manager = LayoutManager(config)
    
    assert manager.config == config, "Config eşleşmeli"
    assert len(manager.layouts) == 0, "Layouts boş olmalı"
    assert len(manager.panels) == 0, "Panels boş olmalı"
    assert manager.active_layout_id is None, "Active layout None olmalı"
    
    print(f"  Layouts: {len(manager.layouts)}")
    print(f"  Panels: {len(manager.panels)}")
    print(f"  Active layout: {manager.active_layout_id}")
    
    print("\n" + "=" * 70)
    print("PASS: LayoutManager initialization")
    print("=" * 70)


def test_add_layout():
    """
    Test: Add layout.
    """
    print("=" * 70)
    print("TEST: Add Layout")
    print("=" * 70)
    
    manager = LayoutManager()
    
    layout = Layout(
        id="",
        name="Default",
        type=LayoutType.SINGLE
    )
    
    result = manager.add_layout(layout)
    
    assert result.success == True, "Ekleme başarılı olmalı"
    assert result.layout is not None, "Layout olmalı"
    assert len(manager.layouts) > 0, "Layout eklenmeli"
    
    print(f"  Layout added: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add layout")
    print("=" * 70)


def test_remove_layout():
    """
    Test: Remove layout.
    """
    print("=" * 70)
    print("TEST: Remove Layout")
    print("=" * 70)
    
    manager = LayoutManager()
    
    layout = Layout(
        id="",
        name="Default",
        type=LayoutType.SINGLE
    )
    
    result = manager.add_layout(layout)
    layout_id = result.layout.id
    
    result = manager.remove_layout(layout_id)
    
    assert result.success == True, "Silme başarılı olmalı"
    assert layout_id not in manager.layouts, "Layout silinmeli"
    
    print(f"  Layout removed: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Remove layout")
    print("=" * 70)


def test_get_layout():
    """
    Test: Get layout.
    """
    print("=" * 70)
    print("TEST: Get Layout")
    print("=" * 70)
    
    manager = LayoutManager()
    
    layout = Layout(
        id="",
        name="Default",
        type=LayoutType.SINGLE
    )
    
    result = manager.add_layout(layout)
    layout_id = result.layout.id
    
    retrieved_layout = manager.get_layout(layout_id)
    
    assert retrieved_layout is not None, "Layout bulunmalı"
    assert retrieved_layout.id == layout_id, "ID eşleşmeli"
    
    print(f"  Layout: {retrieved_layout.name}")
    
    print("\n" + "=" * 70)
    print("PASS: Get layout")
    print("=" * 70)


def test_get_all_layouts():
    """
    Test: Get all layouts.
    """
    print("=" * 70)
    print("TEST: Get All Layouts")
    print("=" * 70)
    
    manager = LayoutManager()
    
    layout = Layout(
        id="",
        name="Default",
        type=LayoutType.SINGLE
    )
    
    manager.add_layout(layout)
    layouts = manager.get_all_layouts()
    
    assert len(layouts) > 0, "Layouts olmalı"
    
    print(f"  Total layouts: {len(layouts)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get all layouts")
    print("=" * 70)


def test_set_active_layout():
    """
    Test: Set active layout.
    """
    print("=" * 70)
    print("TEST: Set Active Layout")
    print("=" * 70)
    
    manager = LayoutManager()
    
    layout = Layout(
        id="",
        name="Default",
        type=LayoutType.SINGLE
    )
    
    result = manager.add_layout(layout)
    layout_id = result.layout.id
    
    result = manager.set_active_layout(layout_id)
    
    assert result.success == True, "Set başarılı olmalı"
    assert manager.active_layout_id == layout_id, "Active layout eşleşmeli"
    
    print(f"  Active layout set: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set active layout")
    print("=" * 70)


def test_add_panel():
    """
    Test: Add panel.
    """
    print("=" * 70)
    print("TEST: Add Panel")
    print("=" * 70)
    
    manager = LayoutManager()
    
    layout = Layout(id="", name="Default", type=LayoutType.SINGLE)
    manager.add_layout(layout)
    
    panel = Panel(
        id="",
        type=PanelType.EDITOR,
        title="Editor"
    )
    
    result = manager.add_panel(panel)
    
    assert result.success == True, "Ekleme başarılı olmalı"
    assert result.panel is not None, "Panel olmalı"
    assert len(manager.panels) > 0, "Panel eklenmeli"
    
    print(f"  Panel added: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add panel")
    print("=" * 70)


def test_remove_panel():
    """
    Test: Remove panel.
    """
    print("=" * 70)
    print("TEST: Remove Panel")
    print("=" * 70)
    
    manager = LayoutManager()
    
    layout = Layout(id="", name="Default", type=LayoutType.SINGLE)
    manager.add_layout(layout)
    
    panel = Panel(
        id="",
        type=PanelType.EDITOR,
        title="Editor"
    )
    
    result = manager.add_panel(panel)
    panel_id = result.panel.id
    
    result = manager.remove_panel(panel_id)
    
    assert result.success == True, "Silme başarılı olmalı"
    assert panel_id not in manager.panels, "Panel silinmeli"
    
    print(f"  Panel removed: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Remove panel")
    print("=" * 70)


def test_get_panel():
    """
    Test: Get panel.
    """
    print("=" * 70)
    print("TEST: Get Panel")
    print("=" * 70)
    
    manager = LayoutManager()
    
    layout = Layout(id="", name="Default", type=LayoutType.SINGLE)
    manager.add_layout(layout)
    
    panel = Panel(
        id="",
        type=PanelType.EDITOR,
        title="Editor"
    )
    
    result = manager.add_panel(panel)
    panel_id = result.panel.id
    
    retrieved_panel = manager.get_panel(panel_id)
    
    assert retrieved_panel is not None, "Panel bulunmalı"
    assert retrieved_panel.id == panel_id, "ID eşleşmeli"
    
    print(f"  Panel: {retrieved_panel.title}")
    
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
    
    manager = LayoutManager()
    
    layout = Layout(id="", name="Default", type=LayoutType.SINGLE)
    manager.add_layout(layout)
    
    panel = Panel(
        id="",
        type=PanelType.EDITOR,
        title="Editor"
    )
    
    manager.add_panel(panel)
    panels = manager.get_all_panels()
    
    assert len(panels) > 0, "Panels olmalı"
    
    print(f"  Total panels: {len(panels)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get all panels")
    print("=" * 70)


def test_get_panels_by_type():
    """
    Test: Get panels by type.
    """
    print("=" * 70)
    print("TEST: Get Panels by Type")
    print("=" * 70)
    
    manager = LayoutManager()
    
    layout = Layout(id="", name="Default", type=LayoutType.SINGLE)
    manager.add_layout(layout)
    
    panel = Panel(
        id="",
        type=PanelType.EDITOR,
        title="Editor"
    )
    
    manager.add_panel(panel)
    panels = manager.get_panels_by_type(PanelType.EDITOR)
    
    assert len(panels) > 0, "Editor panels olmalı"
    
    print(f"  Editor panels: {len(panels)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get panels by type")
    print("=" * 70)


def test_resize_panel():
    """
    Test: Resize panel.
    """
    print("=" * 70)
    print("TEST: Resize Panel")
    print("=" * 70)
    
    manager = LayoutManager()
    
    layout = Layout(id="", name="Default", type=LayoutType.SINGLE)
    manager.add_layout(layout)
    
    panel = Panel(
        id="",
        type=PanelType.EDITOR,
        title="Editor"
    )
    
    result = manager.add_panel(panel)
    panel_id = result.panel.id
    
    result = manager.resize_panel(panel_id, width=200, height=150)
    
    assert result.success == True, "Resize başarılı olmalı"
    
    print(f"  Panel resized: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Resize panel")
    print("=" * 70)


def test_move_panel():
    """
    Test: Move panel.
    """
    print("=" * 70)
    print("TEST: Move Panel")
    print("=" * 70)
    
    manager = LayoutManager()
    
    layout = Layout(id="", name="Default", type=LayoutType.SINGLE)
    manager.add_layout(layout)
    
    panel = Panel(
        id="",
        type=PanelType.EDITOR,
        title="Editor"
    )
    
    result = manager.add_panel(panel)
    panel_id = result.panel.id
    
    result = manager.move_panel(panel_id, 10, 20)
    
    assert result.success == True, "Move başarılı olmalı"
    
    print(f"  Panel moved: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Move panel")
    print("=" * 70)


def test_collapse_panel():
    """
    Test: Collapse panel.
    """
    print("=" * 70)
    print("TEST: Collapse Panel")
    print("=" * 70)
    
    manager = LayoutManager()
    
    layout = Layout(id="", name="Default", type=LayoutType.SINGLE)
    manager.add_layout(layout)
    
    panel = Panel(
        id="",
        type=PanelType.EDITOR,
        title="Editor"
    )
    
    result = manager.add_panel(panel)
    panel_id = result.panel.id
    
    result = manager.collapse_panel(panel_id)
    
    assert result.success == True, "Collapse başarılı olmalı"
    
    print(f"  Panel collapsed: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Collapse panel")
    print("=" * 70)


def test_expand_panel():
    """
    Test: Expand panel.
    """
    print("=" * 70)
    print("TEST: Expand Panel")
    print("=" * 70)
    
    manager = LayoutManager()
    
    layout = Layout(id="", name="Default", type=LayoutType.SINGLE)
    manager.add_layout(layout)
    
    panel = Panel(
        id="",
        type=PanelType.EDITOR,
        title="Editor"
    )
    
    result = manager.add_panel(panel)
    panel_id = result.panel.id
    
    manager.collapse_panel(panel_id)
    result = manager.expand_panel(panel_id)
    
    assert result.success == True, "Expand başarılı olmalı"
    
    print(f"  Panel expanded: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Expand panel")
    print("=" * 70)


def test_set_panel_visible():
    """
    Test: Set panel visible.
    """
    print("=" * 70)
    print("TEST: Set Panel Visible")
    print("=" * 70)
    
    manager = LayoutManager()
    
    layout = Layout(id="", name="Default", type=LayoutType.SINGLE)
    manager.add_layout(layout)
    
    panel = Panel(
        id="",
        type=PanelType.EDITOR,
        title="Editor"
    )
    
    result = manager.add_panel(panel)
    panel_id = result.panel.id
    
    result = manager.set_panel_visible(panel_id, False)
    
    assert result.success == True, "Set başarılı olmalı"
    
    print(f"  Panel visible state: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set panel visible")
    print("=" * 70)


def test_clear_all_panels():
    """
    Test: Clear all panels.
    """
    print("=" * 70)
    print("TEST: Clear All Panels")
    print("=" * 70)
    
    manager = LayoutManager()
    
    layout = Layout(id="", name="Default", type=LayoutType.SINGLE)
    manager.add_layout(layout)
    
    panel = Panel(
        id="",
        type=PanelType.EDITOR,
        title="Editor"
    )
    
    manager.add_panel(panel)
    result = manager.clear_all_panels()
    
    assert result.success == True, "Clear başarılı olmalı"
    assert len(manager.panels) == 0, "Panels temizlenmeli"
    
    print(f"  All panels cleared: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear all panels")
    print("=" * 70)


def test_clear_all_layouts():
    """
    Test: Clear all layouts.
    """
    print("=" * 70)
    print("TEST: Clear All Layouts")
    print("=" * 70)
    
    manager = LayoutManager()
    
    layout = Layout(id="", name="Default", type=LayoutType.SINGLE)
    manager.add_layout(layout)
    
    result = manager.clear_all_layouts()
    
    assert result.success == True, "Clear başarılı olmalı"
    assert len(manager.layouts) == 0, "Layouts temizlenmeli"
    
    print(f"  All layouts cleared: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear all layouts")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    manager = LayoutManager()
    
    new_config = LayoutConfig(max_panels=30)
    result = manager.update_config(new_config)
    
    assert result.success == True, "Update başarılı olmalı"
    assert manager.config.max_panels == 30, "Config güncellenmeli"
    
    print(f"  Max panels: {manager.config.max_panels}")
    
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
    
    config = LayoutConfig(max_panels=30)
    manager = LayoutManager(config)
    
    retrieved_config = manager.get_config()
    
    assert retrieved_config.max_panels == 30, "Config eşleşmeli"
    
    print(f"  Max panels: {retrieved_config.max_panels}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_layout_type_enum()
        test2 = test_panel_type_enum()
        test3 = test_resize_direction_enum()
        test4 = test_panel_dataclass()
        test5 = test_layout_dataclass()
        test6 = test_layout_config_dataclass()
        test7 = test_layout_result_dataclass()
        test8 = test_layout_manager_initialization()
        test9 = test_add_layout()
        test10 = test_remove_layout()
        test11 = test_get_layout()
        test12 = test_get_all_layouts()
        test13 = test_set_active_layout()
        test14 = test_add_panel()
        test15 = test_remove_panel()
        test16 = test_get_panel()
        test17 = test_get_all_panels()
        test18 = test_get_panels_by_type()
        test19 = test_resize_panel()
        test20 = test_move_panel()
        test21 = test_collapse_panel()
        test22 = test_expand_panel()
        test23 = test_set_panel_visible()
        test24 = test_clear_all_panels()
        test25 = test_clear_all_layouts()
        test26 = test_update_config()
        test27 = test_get_config()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"LayoutType Enum: {'PASS' if test1 else 'FAIL'}")
        print(f"PanelType Enum: {'PASS' if test2 else 'FAIL'}")
        print(f"ResizeDirection Enum: {'PASS' if test3 else 'FAIL'}")
        print(f"Panel Dataclass: {'PASS' if test4 else 'FAIL'}")
        print(f"Layout Dataclass: {'PASS' if test5 else 'FAIL'}")
        print(f"LayoutConfig Dataclass: {'PASS' if test6 else 'FAIL'}")
        print(f"LayoutResult Dataclass: {'PASS' if test7 else 'FAIL'}")
        print(f"LayoutManager Initialization: {'PASS' if test8 else 'FAIL'}")
        print(f"Add Layout: {'PASS' if test9 else 'FAIL'}")
        print(f"Remove Layout: {'PASS' if test10 else 'FAIL'}")
        print(f"Get Layout: {'PASS' if test11 else 'FAIL'}")
        print(f"Get All Layouts: {'PASS' if test12 else 'FAIL'}")
        print(f"Set Active Layout: {'PASS' if test13 else 'FAIL'}")
        print(f"Add Panel: {'PASS' if test14 else 'FAIL'}")
        print(f"Remove Panel: {'PASS' if test15 else 'FAIL'}")
        print(f"Get Panel: {'PASS' if test16 else 'FAIL'}")
        print(f"Get All Panels: {'PASS' if test17 else 'FAIL'}")
        print(f"Get Panels by Type: {'PASS' if test18 else 'FAIL'}")
        print(f"Resize Panel: {'PASS' if test19 else 'FAIL'}")
        print(f"Move Panel: {'PASS' if test20 else 'FAIL'}")
        print(f"Collapse Panel: {'PASS' if test21 else 'FAIL'}")
        print(f"Expand Panel: {'PASS' if test22 else 'FAIL'}")
        print(f"Set Panel Visible: {'PASS' if test23 else 'FAIL'}")
        print(f"Clear All Panels: {'PASS' if test24 else 'FAIL'}")
        print(f"Clear All Layouts: {'PASS' if test25 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test26 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test27 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14, test15, test16, test17, test18, test19, test20, test21, test22, test23, test24, test25, test26, test27])
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
