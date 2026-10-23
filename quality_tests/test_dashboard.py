"""
Quality Test: Dashboard
Dashboard system testleri for UI module.
"""

import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from app.ui.dashboard import (
    WidgetType,
    WidgetPosition,
    DashboardLayout,
    Widget,
    DashboardConfig,
    DashboardResult,
    DashboardManager
)


def test_widget_type_enum():
    """
    Test: WidgetType enum.
    """
    print("=" * 70)
    print("TEST: WidgetType Enum")
    print("=" * 70)
    
    assert WidgetType.PROJECT_OVERVIEW.value == "project_overview"
    assert WidgetType.RECENT_FILES.value == "recent_files"
    assert WidgetType.QUICK_ACTIONS.value == "quick_actions"
    assert WidgetType.STATISTICS.value == "statistics"
    assert WidgetType.ACTIVITY_FEED.value == "activity_feed"
    assert WidgetType.NOTIFICATIONS.value == "notifications"
    assert WidgetType.GIT_STATUS.value == "git_status"
    assert WidgetType.SYSTEM_INFO.value == "system_info"
    assert WidgetType.CUSTOM.value == "custom"
    
    print(f"  All enum values verified")
    print(f"  Total types: {len(WidgetType)}")
    
    print("\n" + "=" * 70)
    print("PASS: WidgetType enum")
    print("=" * 70)


def test_widget_position_enum():
    """
    Test: WidgetPosition enum.
    """
    print("=" * 70)
    print("TEST: WidgetPosition Enum")
    print("=" * 70)
    
    assert WidgetPosition.TOP_LEFT.value == "top_left"
    assert WidgetPosition.TOP_CENTER.value == "top_center"
    assert WidgetPosition.TOP_RIGHT.value == "top_right"
    assert WidgetPosition.MIDDLE_LEFT.value == "middle_left"
    assert WidgetPosition.MIDDLE_CENTER.value == "middle_center"
    assert WidgetPosition.MIDDLE_RIGHT.value == "middle_right"
    assert WidgetPosition.BOTTOM_LEFT.value == "bottom_left"
    assert WidgetPosition.BOTTOM_CENTER.value == "bottom_center"
    assert WidgetPosition.BOTTOM_RIGHT.value == "bottom_right"
    
    print(f"  All enum values verified")
    print(f"  Total positions: {len(WidgetPosition)}")
    
    print("\n" + "=" * 70)
    print("PASS: WidgetPosition enum")
    print("=" * 70)


def test_dashboard_layout_enum():
    """
    Test: DashboardLayout enum.
    """
    print("=" * 70)
    print("TEST: DashboardLayout Enum")
    print("=" * 70)
    
    assert DashboardLayout.GRID.value == "grid"
    assert DashboardLayout.LIST.value == "list"
    assert DashboardLayout.TABS.value == "tabs"
    assert DashboardLayout.CUSTOM.value == "custom"
    
    print(f"  All enum values verified")
    print(f"  Total layouts: {len(DashboardLayout)}")
    
    print("\n" + "=" * 70)
    print("PASS: DashboardLayout enum")
    print("=" * 70)


def test_widget_dataclass():
    """
    Test: Widget dataclass.
    """
    print("=" * 70)
    print("TEST: Widget Dataclass")
    print("=" * 70)
    
    widget = Widget(
        id="widget_1",
        type=WidgetType.PROJECT_OVERVIEW,
        position=WidgetPosition.TOP_LEFT,
        title="Project Overview",
        content={"project_name": "Test"}
    )
    
    assert widget.id == "widget_1", "ID eşleşmeli"
    assert widget.type == WidgetType.PROJECT_OVERVIEW, "Type eşleşmeli"
    assert widget.position == WidgetPosition.TOP_LEFT, "Position eşleşmeli"
    assert widget.title == "Project Overview", "Title eşleşmeli"
    
    print(f"  ID: {widget.id}")
    print(f"  Type: {widget.type.value}")
    print(f"  Position: {widget.position.value}")
    print(f"  Title: {widget.title}")
    
    print("\n" + "=" * 70)
    print("PASS: Widget dataclass")
    print("=" * 70)


def test_dashboard_config_dataclass():
    """
    Test: DashboardConfig dataclass.
    """
    print("=" * 70)
    print("TEST: DashboardConfig Dataclass")
    print("=" * 70)
    
    config = DashboardConfig(
        enabled=True,
        layout=DashboardLayout.GRID
    )
    
    assert config.enabled == True, "Enabled eşleşmeli"
    assert config.layout == DashboardLayout.GRID, "Layout eşleşmeli"
    
    print(f"  Enabled: {config.enabled}")
    print(f"  Layout: {config.layout.value}")
    
    print("\n" + "=" * 70)
    print("PASS: DashboardConfig dataclass")
    print("=" * 70)


def test_dashboard_result_dataclass():
    """
    Test: DashboardResult dataclass.
    """
    print("=" * 70)
    print("TEST: DashboardResult Dataclass")
    print("=" * 70)
    
    result = DashboardResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.widgets, list), "Widgets list olmalı"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Widgets: {len(result.widgets)}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: DashboardResult dataclass")
    print("=" * 70)


def test_dashboard_manager_initialization():
    """
    Test: DashboardManager initialization.
    """
    print("=" * 70)
    print("TEST: DashboardManager Initialization")
    print("=" * 70)
    
    config = DashboardConfig()
    manager = DashboardManager(config)
    
    assert manager.config == config, "Config eşleşmeli"
    assert len(manager.widgets) == 0, "Widgets boş olmalı"
    
    print(f"  Widgets: {len(manager.widgets)}")
    
    print("\n" + "=" * 70)
    print("PASS: DashboardManager initialization")
    print("=" * 70)


def test_add_widget():
    """
    Test: Add widget.
    """
    print("=" * 70)
    print("TEST: Add Widget")
    print("=" * 70)
    
    manager = DashboardManager()
    
    widget = Widget(
        id="",
        type=WidgetType.PROJECT_OVERVIEW,
        position=WidgetPosition.TOP_LEFT,
        title="Project Overview",
        content={"project_name": "Test"}
    )
    
    result = manager.add_widget(widget)
    
    assert result.success == True, "Ekleme başarılı olmalı"
    assert len(manager.widgets) > 0, "Widget eklenmeli"
    
    print(f"  Widget added: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add widget")
    print("=" * 70)


def test_remove_widget():
    """
    Test: Remove widget.
    """
    print("=" * 70)
    print("TEST: Remove Widget")
    print("=" * 70)
    
    manager = DashboardManager()
    
    widget = Widget(
        id="",
        type=WidgetType.PROJECT_OVERVIEW,
        position=WidgetPosition.TOP_LEFT,
        title="Project Overview",
        content={"project_name": "Test"}
    )
    
    result = manager.add_widget(widget)
    widget_id = result.widget.id
    
    result = manager.remove_widget(widget_id)
    
    assert result.success == True, "Kaldırma başarılı olmalı"
    assert widget_id not in manager.widgets, "Widget silinmeli"
    
    print(f"  Widget removed: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Remove widget")
    print("=" * 70)


def test_get_widget():
    """
    Test: Get widget.
    """
    print("=" * 70)
    print("TEST: Get Widget")
    print("=" * 70)
    
    manager = DashboardManager()
    
    widget = Widget(
        id="",
        type=WidgetType.PROJECT_OVERVIEW,
        position=WidgetPosition.TOP_LEFT,
        title="Project Overview",
        content={"project_name": "Test"}
    )
    
    result = manager.add_widget(widget)
    widget_id = result.widget.id
    
    retrieved_widget = manager.get_widget(widget_id)
    
    assert retrieved_widget is not None, "Widget bulunmalı"
    assert retrieved_widget.id == widget_id, "ID eşleşmeli"
    
    print(f"  Widget: {retrieved_widget.title}")
    
    print("\n" + "=" * 70)
    print("PASS: Get widget")
    print("=" * 70)


def test_get_all_widgets():
    """
    Test: Get all widgets.
    """
    print("=" * 70)
    print("TEST: Get All Widgets")
    print("=" * 70)
    
    manager = DashboardManager()
    
    widget = Widget(
        id="",
        type=WidgetType.PROJECT_OVERVIEW,
        position=WidgetPosition.TOP_LEFT,
        title="Project Overview",
        content={"project_name": "Test"}
    )
    
    manager.add_widget(widget)
    widgets = manager.get_all_widgets()
    
    assert len(widgets) > 0, "Widgets olmalı"
    
    print(f"  Total widgets: {len(widgets)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get all widgets")
    print("=" * 70)


def test_get_widgets_by_type():
    """
    Test: Get widgets by type.
    """
    print("=" * 70)
    print("TEST: Get Widgets by Type")
    print("=" * 70)
    
    manager = DashboardManager()
    
    widget = Widget(
        id="",
        type=WidgetType.PROJECT_OVERVIEW,
        position=WidgetPosition.TOP_LEFT,
        title="Project Overview",
        content={"project_name": "Test"}
    )
    
    manager.add_widget(widget)
    widgets = manager.get_widgets_by_type(WidgetType.PROJECT_OVERVIEW)
    
    assert len(widgets) > 0, "Project overview widgets olmalı"
    
    print(f"  Project overview widgets: {len(widgets)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get widgets by type")
    print("=" * 70)


def test_get_widgets_by_position():
    """
    Test: Get widgets by position.
    """
    print("=" * 70)
    print("TEST: Get Widgets by Position")
    print("=" * 70)
    
    manager = DashboardManager()
    
    widget = Widget(
        id="",
        type=WidgetType.PROJECT_OVERVIEW,
        position=WidgetPosition.TOP_LEFT,
        title="Project Overview",
        content={"project_name": "Test"}
    )
    
    manager.add_widget(widget)
    widgets = manager.get_widgets_by_position(WidgetPosition.TOP_LEFT)
    
    assert len(widgets) > 0, "Top left widgets olmalı"
    
    print(f"  Top left widgets: {len(widgets)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get widgets by position")
    print("=" * 70)


def test_add_project_overview_widget():
    """
    Test: Add project overview widget.
    """
    print("=" * 70)
    print("TEST: Add Project Overview Widget")
    print("=" * 70)
    
    manager = DashboardManager()
    
    content = {"project_name": "Test Project", "files": 10}
    result = manager.add_project_overview_widget(WidgetPosition.TOP_LEFT, content)
    
    assert result.success == True, "Project overview widget başarılı olmalı"
    
    print(f"  Project overview widget: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add project overview widget")
    print("=" * 70)


def test_add_recent_files_widget():
    """
    Test: Add recent files widget.
    """
    print("=" * 70)
    print("TEST: Add Recent Files Widget")
    print("=" * 70)
    
    manager = DashboardManager()
    
    content = {"files": ["file1.py", "file2.py"]}
    result = manager.add_recent_files_widget(WidgetPosition.TOP_RIGHT, content)
    
    assert result.success == True, "Recent files widget başarılı olmalı"
    
    print(f"  Recent files widget: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add recent files widget")
    print("=" * 70)


def test_add_quick_actions_widget():
    """
    Test: Add quick actions widget.
    """
    print("=" * 70)
    print("TEST: Add Quick Actions Widget")
    print("=" * 70)
    
    manager = DashboardManager()
    
    content = {"actions": ["New File", "Open File"]}
    result = manager.add_quick_actions_widget(WidgetPosition.MIDDLE_LEFT, content)
    
    assert result.success == True, "Quick actions widget başarılı olmalı"
    
    print(f"  Quick actions widget: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add quick actions widget")
    print("=" * 70)


def test_add_statistics_widget():
    """
    Test: Add statistics widget.
    """
    print("=" * 70)
    print("TEST: Add Statistics Widget")
    print("=" * 70)
    
    manager = DashboardManager()
    
    content = {"lines": 1000, "files": 50}
    result = manager.add_statistics_widget(WidgetPosition.MIDDLE_CENTER, content)
    
    assert result.success == True, "Statistics widget başarılı olmalı"
    
    print(f"  Statistics widget: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add statistics widget")
    print("=" * 70)


def test_add_activity_feed_widget():
    """
    Test: Add activity feed widget.
    """
    print("=" * 70)
    print("TEST: Add Activity Feed Widget")
    print("=" * 70)
    
    manager = DashboardManager()
    
    content = {"activities": ["Commit", "Push"]}
    result = manager.add_activity_feed_widget(WidgetPosition.BOTTOM_LEFT, content)
    
    assert result.success == True, "Activity feed widget başarılı olmalı"
    
    print(f"  Activity feed widget: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add activity feed widget")
    print("=" * 70)


def test_add_notifications_widget():
    """
    Test: Add notifications widget.
    """
    print("=" * 70)
    print("TEST: Add Notifications Widget")
    print("=" * 70)
    
    manager = DashboardManager()
    
    content = {"notifications": ["New message"]}
    result = manager.add_notifications_widget(WidgetPosition.BOTTOM_RIGHT, content)
    
    assert result.success == True, "Notifications widget başarılı olmalı"
    
    print(f"  Notifications widget: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add notifications widget")
    print("=" * 70)


def test_add_git_status_widget():
    """
    Test: Add git status widget.
    """
    print("=" * 70)
    print("TEST: Add Git Status Widget")
    print("=" * 70)
    
    manager = DashboardManager()
    
    content = {"branch": "main", "status": "clean"}
    result = manager.add_git_status_widget(WidgetPosition.TOP_CENTER, content)
    
    assert result.success == True, "Git status widget başarılı olmalı"
    
    print(f"  Git status widget: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add git status widget")
    print("=" * 70)


def test_add_system_info_widget():
    """
    Test: Add system info widget.
    """
    print("=" * 70)
    print("TEST: Add System Info Widget")
    print("=" * 70)
    
    manager = DashboardManager()
    
    content = {"cpu": "Intel", "memory": "16GB"}
    result = manager.add_system_info_widget(WidgetPosition.BOTTOM_CENTER, content)
    
    assert result.success == True, "System info widget başarılı olmalı"
    
    print(f"  System info widget: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add system info widget")
    print("=" * 70)


def test_move_widget():
    """
    Test: Move widget.
    """
    print("=" * 70)
    print("TEST: Move Widget")
    print("=" * 70)
    
    manager = DashboardManager()
    
    content = {"project_name": "Test"}
    result = manager.add_project_overview_widget(WidgetPosition.TOP_LEFT, content)
    widget_id = result.widget.id
    
    result = manager.move_widget(widget_id, WidgetPosition.TOP_RIGHT)
    
    assert result.success == True, "Move başarılı olmalı"
    
    print(f"  Widget moved: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Move widget")
    print("=" * 70)


def test_resize_widget():
    """
    Test: Resize widget.
    """
    print("=" * 70)
    print("TEST: Resize Widget")
    print("=" * 70)
    
    manager = DashboardManager()
    
    content = {"project_name": "Test"}
    result = manager.add_project_overview_widget(WidgetPosition.TOP_LEFT, content)
    widget_id = result.widget.id
    
    result = manager.resize_widget(widget_id, "large")
    
    assert result.success == True, "Resize başarılı olmalı"
    
    print(f"  Widget resized: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Resize widget")
    print("=" * 70)


def test_collapse_widget():
    """
    Test: Collapse widget.
    """
    print("=" * 70)
    print("TEST: Collapse Widget")
    print("=" * 70)
    
    manager = DashboardManager()
    
    content = {"project_name": "Test"}
    result = manager.add_project_overview_widget(WidgetPosition.TOP_LEFT, content)
    widget_id = result.widget.id
    
    result = manager.collapse_widget(widget_id, True)
    
    assert result.success == True, "Collapse başarılı olmalı"
    
    print(f"  Widget collapsed: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Collapse widget")
    print("=" * 70)


def test_clear_widgets():
    """
    Test: Clear widgets.
    """
    print("=" * 70)
    print("TEST: Clear Widgets")
    print("=" * 70)
    
    manager = DashboardManager()
    
    content = {"project_name": "Test"}
    manager.add_project_overview_widget(WidgetPosition.TOP_LEFT, content)
    
    result = manager.clear_widgets()
    
    assert result.success == True, "Clear başarılı olmalı"
    assert len(manager.widgets) == 0, "Widgets temizlenmeli"
    
    print(f"  Cleared: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear widgets")
    print("=" * 70)


def test_set_widget_enabled():
    """
    Test: Set widget enabled.
    """
    print("=" * 70)
    print("TEST: Set Widget Enabled")
    print("=" * 70)
    
    manager = DashboardManager()
    
    content = {"project_name": "Test"}
    result = manager.add_project_overview_widget(WidgetPosition.TOP_LEFT, content)
    widget_id = result.widget.id
    
    result = manager.set_widget_enabled(widget_id, False)
    
    assert result.success == True, "Set başarılı olmalı"
    
    print(f"  Widget enabled state: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set widget enabled")
    print("=" * 70)


def test_set_widget_visible():
    """
    Test: Set widget visible.
    """
    print("=" * 70)
    print("TEST: Set Widget Visible")
    print("=" * 70)
    
    manager = DashboardManager()
    
    content = {"project_name": "Test"}
    result = manager.add_project_overview_widget(WidgetPosition.TOP_LEFT, content)
    widget_id = result.widget.id
    
    result = manager.set_widget_visible(widget_id, False)
    
    assert result.success == True, "Set başarılı olmalı"
    
    print(f"  Widget visible state: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set widget visible")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    manager = DashboardManager()
    
    new_config = DashboardConfig(max_widgets=20)
    result = manager.update_config(new_config)
    
    assert result.success == True, "Update başarılı olmalı"
    assert manager.config.max_widgets == 20, "Config güncellenmeli"
    
    print(f"  Max widgets: {manager.config.max_widgets}")
    
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
    
    config = DashboardConfig(max_widgets=20)
    manager = DashboardManager(config)
    
    retrieved_config = manager.get_config()
    
    assert retrieved_config.max_widgets == 20, "Config eşleşmeli"
    
    print(f"  Max widgets: {retrieved_config.max_widgets}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_widget_type_enum()
        test2 = test_widget_position_enum()
        test3 = test_dashboard_layout_enum()
        test4 = test_widget_dataclass()
        test5 = test_dashboard_config_dataclass()
        test6 = test_dashboard_result_dataclass()
        test7 = test_dashboard_manager_initialization()
        test8 = test_add_widget()
        test9 = test_remove_widget()
        test10 = test_get_widget()
        test11 = test_get_all_widgets()
        test12 = test_get_widgets_by_type()
        test13 = test_get_widgets_by_position()
        test14 = test_add_project_overview_widget()
        test15 = test_add_recent_files_widget()
        test16 = test_add_quick_actions_widget()
        test17 = test_add_statistics_widget()
        test18 = test_add_activity_feed_widget()
        test19 = test_add_notifications_widget()
        test20 = test_add_git_status_widget()
        test21 = test_add_system_info_widget()
        test22 = test_move_widget()
        test23 = test_resize_widget()
        test24 = test_collapse_widget()
        test25 = test_clear_widgets()
        test26 = test_set_widget_enabled()
        test27 = test_set_widget_visible()
        test28 = test_update_config()
        test29 = test_get_config()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"WidgetType Enum: {'PASS' if test1 else 'FAIL'}")
        print(f"WidgetPosition Enum: {'PASS' if test2 else 'FAIL'}")
        print(f"DashboardLayout Enum: {'PASS' if test3 else 'FAIL'}")
        print(f"Widget Dataclass: {'PASS' if test4 else 'FAIL'}")
        print(f"DashboardConfig Dataclass: {'PASS' if test5 else 'FAIL'}")
        print(f"DashboardResult Dataclass: {'PASS' if test6 else 'FAIL'}")
        print(f"DashboardManager Initialization: {'PASS' if test7 else 'FAIL'}")
        print(f"Add Widget: {'PASS' if test8 else 'FAIL'}")
        print(f"Remove Widget: {'PASS' if test9 else 'FAIL'}")
        print(f"Get Widget: {'PASS' if test10 else 'FAIL'}")
        print(f"Get All Widgets: {'PASS' if test11 else 'FAIL'}")
        print(f"Get Widgets by Type: {'PASS' if test12 else 'FAIL'}")
        print(f"Get Widgets by Position: {'PASS' if test13 else 'FAIL'}")
        print(f"Add Project Overview Widget: {'PASS' if test14 else 'FAIL'}")
        print(f"Add Recent Files Widget: {'PASS' if test15 else 'FAIL'}")
        print(f"Add Quick Actions Widget: {'PASS' if test16 else 'FAIL'}")
        print(f"Add Statistics Widget: {'PASS' if test17 else 'FAIL'}")
        print(f"Add Activity Feed Widget: {'PASS' if test18 else 'FAIL'}")
        print(f"Add Notifications Widget: {'PASS' if test19 else 'FAIL'}")
        print(f"Add Git Status Widget: {'PASS' if test20 else 'FAIL'}")
        print(f"Add System Info Widget: {'PASS' if test21 else 'FAIL'}")
        print(f"Move Widget: {'PASS' if test22 else 'FAIL'}")
        print(f"Resize Widget: {'PASS' if test23 else 'FAIL'}")
        print(f"Collapse Widget: {'PASS' if test24 else 'FAIL'}")
        print(f"Clear Widgets: {'PASS' if test25 else 'FAIL'}")
        print(f"Set Widget Enabled: {'PASS' if test26 else 'FAIL'}")
        print(f"Set Widget Visible: {'PASS' if test27 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test28 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test29 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14, test15, test16, test17, test18, test19, test20, test21, test22, test23, test24, test25, test26, test27, test28, test29])
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
