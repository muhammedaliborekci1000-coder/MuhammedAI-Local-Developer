"""
MuhammedAI Local Developer - Dashboard
Dashboard system for web UI.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum


class WidgetType(Enum):
    """Widget type."""
    PROJECT_OVERVIEW = "project_overview"
    RECENT_FILES = "recent_files"
    QUICK_ACTIONS = "quick_actions"
    STATISTICS = "statistics"
    ACTIVITY_FEED = "activity_feed"
    NOTIFICATIONS = "notifications"
    GIT_STATUS = "git_status"
    SYSTEM_INFO = "system_info"
    CUSTOM = "custom"


class WidgetPosition(Enum):
    """Widget position."""
    TOP_LEFT = "top_left"
    TOP_CENTER = "top_center"
    TOP_RIGHT = "top_right"
    MIDDLE_LEFT = "middle_left"
    MIDDLE_CENTER = "middle_center"
    MIDDLE_RIGHT = "middle_right"
    BOTTOM_LEFT = "bottom_left"
    BOTTOM_CENTER = "bottom_center"
    BOTTOM_RIGHT = "bottom_right"


class DashboardLayout(Enum):
    """Dashboard layout."""
    GRID = "grid"
    LIST = "list"
    TABS = "tabs"
    CUSTOM = "custom"


@dataclass
class Widget:
    """Dashboard widget."""
    id: str
    type: WidgetType
    position: WidgetPosition
    title: str
    content: Dict[str, Any]
    is_enabled: bool = True
    is_visible: bool = True
    is_collapsed: bool = False
    size: str = "medium"  # small, medium, large
    priority: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DashboardConfig:
    """Dashboard configuration."""
    enabled: bool = True
    layout: DashboardLayout = DashboardLayout.GRID
    show_widgets: bool = True
    show_header: bool = True
    show_footer: bool = True
    auto_refresh: bool = True
    refresh_interval: int = 30  # seconds
    enable_drag_drop: bool = True
    enable_customization: bool = True
    max_widgets: int = 12
    theme: str = "default"


@dataclass
class DashboardResult:
    """Dashboard result."""
    success: bool
    widget: Optional[Widget] = None
    widgets: List[Widget] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    message: Optional[str] = None


class DashboardManager:
    """
    Dashboard manager.
    
    Özellikler:
    - Project overview widget
    - Recent files widget
    - Quick actions widget
    - Statistics widget
    - Activity feed widget
    - Notifications widget
    - Git status widget
    - System info widget
    - Custom widgets
    - Widget positioning
    - Widget sizing
    - Layout management
    - Drag and drop
    - Customization
    - Auto refresh
    """
    
    def __init__(self, config: Optional[DashboardConfig] = None):
        """
        Initialize dashboard manager.
        
        Args:
            config: Dashboard configuration
        """
        self.config = config or DashboardConfig()
        self.widgets: Dict[str, Widget] = {}
        self.widget_id_counter = 0
        self._next_id()
    
    def _next_id(self) -> str:
        """
        Generate next widget ID.
        
        Returns:
            str: Widget ID
        """
        self.widget_id_counter += 1
        return f"widget_{self.widget_id_counter}"
    
    def add_widget(self, widget: Widget) -> DashboardResult:
        """
        Add a widget.
        
        Args:
            widget: Widget to add
            
        Returns:
            DashboardResult: Add result
        """
        result = DashboardResult(success=True)
        
        try:
            if not widget.id:
                widget.id = self._next_id()
            
            if len(self.widgets) >= self.config.max_widgets:
                result.errors.append("Maximum widgets reached")
                result.success = False
                return result
            
            self.widgets[widget.id] = widget
            result.widget = widget
            result.widgets = self.get_all_widgets()
            result.message = f"Widget '{widget.id}' added"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def remove_widget(self, widget_id: str) -> DashboardResult:
        """
        Remove a widget.
        
        Args:
            widget_id: Widget ID
            
        Returns:
            DashboardResult: Remove result
        """
        result = DashboardResult(success=False)
        
        try:
            if widget_id in self.widgets:
                del self.widgets[widget_id]
                result.success = True
                result.widgets = self.get_all_widgets()
                result.message = f"Widget '{widget_id}' removed"
            else:
                result.errors.append("Widget not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_widget(self, widget_id: str) -> Optional[Widget]:
        """
        Get widget by ID.
        
        Args:
            widget_id: Widget ID
            
        Returns:
            Optional[Widget]: Widget
        """
        return self.widgets.get(widget_id)
    
    def get_all_widgets(self) -> List[Widget]:
        """
        Get all widgets.
        
        Returns:
            List[Widget]: All widgets
        """
        return list(self.widgets.values())
    
    def get_widgets_by_type(self, widget_type: WidgetType) -> List[Widget]:
        """
        Get widgets by type.
        
        Args:
            widget_type: Widget type
            
        Returns:
            List[Widget]: Widgets
        """
        return [w for w in self.widgets.values() if w.type == widget_type]
    
    def get_widgets_by_position(self, position: WidgetPosition) -> List[Widget]:
        """
        Get widgets by position.
        
        Args:
            position: Widget position
            
        Returns:
            List[Widget]: Widgets
        """
        return [w for w in self.widgets.values() if w.position == position]
    
    def add_project_overview_widget(self, position: WidgetPosition, content: Dict[str, Any]) -> DashboardResult:
        """
        Add project overview widget.
        
        Args:
            position: Widget position
            content: Widget content
            
        Returns:
            DashboardResult: Add result
        """
        widget = Widget(
            id="",
            type=WidgetType.PROJECT_OVERVIEW,
            position=position,
            title="Project Overview",
            content=content
        )
        
        return self.add_widget(widget)
    
    def add_recent_files_widget(self, position: WidgetPosition, content: Dict[str, Any]) -> DashboardResult:
        """
        Add recent files widget.
        
        Args:
            position: Widget position
            content: Widget content
            
        Returns:
            DashboardResult: Add result
        """
        widget = Widget(
            id="",
            type=WidgetType.RECENT_FILES,
            position=position,
            title="Recent Files",
            content=content
        )
        
        return self.add_widget(widget)
    
    def add_quick_actions_widget(self, position: WidgetPosition, content: Dict[str, Any]) -> DashboardResult:
        """
        Add quick actions widget.
        
        Args:
            position: Widget position
            content: Widget content
            
        Returns:
            DashboardResult: Add result
        """
        widget = Widget(
            id="",
            type=WidgetType.QUICK_ACTIONS,
            position=position,
            title="Quick Actions",
            content=content
        )
        
        return self.add_widget(widget)
    
    def add_statistics_widget(self, position: WidgetPosition, content: Dict[str, Any]) -> DashboardResult:
        """
        Add statistics widget.
        
        Args:
            position: Widget position
            content: Widget content
            
        Returns:
            DashboardResult: Add result
        """
        widget = Widget(
            id="",
            type=WidgetType.STATISTICS,
            position=position,
            title="Statistics",
            content=content
        )
        
        return self.add_widget(widget)
    
    def add_activity_feed_widget(self, position: WidgetPosition, content: Dict[str, Any]) -> DashboardResult:
        """
        Add activity feed widget.
        
        Args:
            position: Widget position
            content: Widget content
            
        Returns:
            DashboardResult: Add result
        """
        widget = Widget(
            id="",
            type=WidgetType.ACTIVITY_FEED,
            position=position,
            title="Activity Feed",
            content=content
        )
        
        return self.add_widget(widget)
    
    def add_notifications_widget(self, position: WidgetPosition, content: Dict[str, Any]) -> DashboardResult:
        """
        Add notifications widget.
        
        Args:
            position: Widget position
            content: Widget content
            
        Returns:
            DashboardResult: Add result
        """
        widget = Widget(
            id="",
            type=WidgetType.NOTIFICATIONS,
            position=position,
            title="Notifications",
            content=content
        )
        
        return self.add_widget(widget)
    
    def add_git_status_widget(self, position: WidgetPosition, content: Dict[str, Any]) -> DashboardResult:
        """
        Add git status widget.
        
        Args:
            position: Widget position
            content: Widget content
            
        Returns:
            DashboardResult: Add result
        """
        widget = Widget(
            id="",
            type=WidgetType.GIT_STATUS,
            position=position,
            title="Git Status",
            content=content
        )
        
        return self.add_widget(widget)
    
    def add_system_info_widget(self, position: WidgetPosition, content: Dict[str, Any]) -> DashboardResult:
        """
        Add system info widget.
        
        Args:
            position: Widget position
            content: Widget content
            
        Returns:
            DashboardResult: Add result
        """
        widget = Widget(
            id="",
            type=WidgetType.SYSTEM_INFO,
            position=position,
            title="System Info",
            content=content
        )
        
        return self.add_widget(widget)
    
    def move_widget(self, widget_id: str, new_position: WidgetPosition) -> DashboardResult:
        """
        Move widget to new position.
        
        Args:
            widget_id: Widget ID
            new_position: New position
            
        Returns:
            DashboardResult: Move result
        """
        result = DashboardResult(success=False)
        
        try:
            widget = self.widgets.get(widget_id)
            if widget:
                widget.position = new_position
                result.success = True
                result.widget = widget
                result.message = f"Widget '{widget_id}' moved to {new_position.value}"
            else:
                result.errors.append("Widget not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def resize_widget(self, widget_id: str, new_size: str) -> DashboardResult:
        """
        Resize widget.
        
        Args:
            widget_id: Widget ID
            new_size: New size (small, medium, large)
            
        Returns:
            DashboardResult: Resize result
        """
        result = DashboardResult(success=False)
        
        try:
            widget = self.widgets.get(widget_id)
            if widget:
                widget.size = new_size
                result.success = True
                result.widget = widget
                result.message = f"Widget '{widget_id}' resized to {new_size}"
            else:
                result.errors.append("Widget not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def collapse_widget(self, widget_id: str, collapsed: bool) -> DashboardResult:
        """
        Collapse/expand widget.
        
        Args:
            widget_id: Widget ID
            collapsed: Collapsed state
            
        Returns:
            DashboardResult: Collapse result
        """
        result = DashboardResult(success=False)
        
        try:
            widget = self.widgets.get(widget_id)
            if widget:
                widget.is_collapsed = collapsed
                result.success = True
                result.widget = widget
                result.message = f"Widget '{widget_id}' {'collapsed' if collapsed else 'expanded'}"
            else:
                result.errors.append("Widget not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def clear_widgets(self) -> DashboardResult:
        """
        Clear all widgets.
        
        Returns:
            DashboardResult: Clear result
        """
        result = DashboardResult(success=True)
        
        try:
            self.widgets.clear()
            result.message = "All widgets cleared"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def set_widget_enabled(self, widget_id: str, enabled: bool) -> DashboardResult:
        """
        Set widget enabled state.
        
        Args:
            widget_id: Widget ID
            enabled: Enabled state
            
        Returns:
            DashboardResult: Set result
        """
        result = DashboardResult(success=False)
        
        try:
            widget = self.widgets.get(widget_id)
            if widget:
                widget.is_enabled = enabled
                result.success = True
                result.message = f"Widget '{widget_id}' {'enabled' if enabled else 'disabled'}"
            else:
                result.errors.append("Widget not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def set_widget_visible(self, widget_id: str, visible: bool) -> DashboardResult:
        """
        Set widget visible state.
        
        Args:
            widget_id: Widget ID
            visible: Visible state
            
        Returns:
            DashboardResult: Set result
        """
        result = DashboardResult(success=False)
        
        try:
            widget = self.widgets.get(widget_id)
            if widget:
                widget.is_visible = visible
                result.success = True
                result.message = f"Widget '{widget_id}' {'visible' if visible else 'hidden'}"
            else:
                result.errors.append("Widget not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def update_config(self, config: DashboardConfig) -> DashboardResult:
        """
        Update dashboard configuration.
        
        Args:
            config: New configuration
            
        Returns:
            DashboardResult: Update result
        """
        result = DashboardResult(success=True)
        
        try:
            self.config = config
            result.message = "Config updated"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def get_config(self) -> DashboardConfig:
        """
        Get dashboard configuration.
        
        Returns:
            DashboardConfig: Configuration
        """
        return self.config


if __name__ == "__main__":
    # Basit test
    config = DashboardConfig()
    manager = DashboardManager(config)
    
    # Widget ekle
    content = {"project_name": "Test Project", "files": 10}
    result = manager.add_project_overview_widget(WidgetPosition.TOP_LEFT, content)
    
    print(f"Widget added: {result.message}")
    
    # Tüm widget'ları al
    widgets = manager.get_all_widgets()
    
    print(f"Total widgets: {len(widgets)}")
