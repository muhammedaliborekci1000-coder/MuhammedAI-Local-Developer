"""
MuhammedAI Local Developer - Tab Manager
Tab management system for code editor.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum


class TabState(Enum):
    """Tab state."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    MODIFIED = "modified"
    PINNED = "pinned"


class TabGroup(Enum):
    """Tab group."""
    UNGROUPED = "ungrouped"
    GROUP_1 = "group_1"
    GROUP_2 = "group_2"
    GROUP_3 = "group_3"


@dataclass
class Tab:
    """Tab information."""
    id: str
    uri: str
    title: str
    state: TabState = TabState.INACTIVE
    group: TabGroup = TabGroup.UNGROUPED
    is_pinned: bool = False
    is_preview: bool = False
    language: Optional[str] = None
    cursor_position: Optional[tuple] = None
    scroll_position: Optional[int] = None


@dataclass
class TabConfig:
    """Tab configuration."""
    max_tabs: int = 100
    enable_preview: bool = True
    preview_delay: int = 500
    enable_pinning: bool = True
    enable_grouping: bool = True
    enable_reordering: bool = True
    close_on_last: bool = False
    show_modified_indicator: bool = True
    show_language_indicator: bool = True


class TabManager:
    """
    Tab manager.
    
    Özellikler:
    - Tab management
    - Tab switching
    - Tab grouping
    - Tab pinning
    - Tab reorder
    - Tab preview
    - Tab persistence
    - Tab history
    - Modified state tracking
    - Language detection
    - Cursor position tracking
    - Scroll position tracking
    - Tab closing
    - Tab duplication
    - Tab splitting
    """
    
    def __init__(self, config: Optional[TabConfig] = None):
        """
        Initialize tab manager.
        
        Args:
            config: Tab configuration
        """
        self.config = config or TabConfig()
        self.tabs: List[Tab] = []
        self.active_tab_id: Optional[str] = None
        self._next_tab_id = 1
        self.tab_history: List[str] = []
    
    def add_tab(
        self,
        uri: str,
        title: str,
        language: Optional[str] = None,
        activate: bool = True
    ) -> Tab:
        """
        Add tab.
        
        Args:
            uri: Document URI
            title: Tab title
            language: Language identifier
            activate: Whether to activate tab
            
        Returns:
            Tab: Created tab
        """
        tab_id = f"tab_{self._next_tab_id}"
        self._next_tab_id += 1
        
        tab = Tab(
            id=tab_id,
            uri=uri,
            title=title,
            state=TabState.INACTIVE,
            language=language
        )
        
        # Check if tab already exists
        existing_tab = self.get_tab_by_uri(uri)
        if existing_tab:
            if activate:
                self.activate_tab(existing_tab.id)
            return existing_tab
        
        # Add tab
        self.tabs.append(tab)
        
        if activate:
            self.activate_tab(tab_id)
        
        return tab
    
    def close_tab(self, tab_id: str) -> bool:
        """
        Close tab.
        
        Args:
            tab_id: Tab ID
            
        Returns:
            bool: Success
        """
        tab = self.get_tab(tab_id)
        if not tab:
            return False
        
        # Cannot close pinned tabs
        if tab.is_pinned:
            return False
        
        # Remove tab
        self.tabs = [t for t in self.tabs if t.id != tab_id]
        
        # If closing active tab, activate another
        if self.active_tab_id == tab_id:
            if self.tabs:
                self.activate_tab(self.tabs[-1].id)
            else:
                self.active_tab_id = None
        
        return True
    
    def activate_tab(self, tab_id: str) -> bool:
        """
        Activate tab.
        
        Args:
            tab_id: Tab ID
            
        Returns:
            bool: Success
        """
        tab = self.get_tab(tab_id)
        if not tab:
            return False
        
        # Deactivate current active tab
        if self.active_tab_id:
            current_tab = self.get_tab(self.active_tab_id)
            if current_tab:
                current_tab.state = TabState.INACTIVE
        
        # Activate new tab
        self.active_tab_id = tab_id
        tab.state = TabState.ACTIVE
        
        # Add to history
        if tab_id not in self.tab_history:
            self.tab_history.append(tab_id)
        
        return True
    
    def get_tab(self, tab_id: str) -> Optional[Tab]:
        """
        Get tab by ID.
        
        Args:
            tab_id: Tab ID
            
        Returns:
            Optional[Tab]: Tab
        """
        for tab in self.tabs:
            if tab.id == tab_id:
                return tab
        return None
    
    def get_tab_by_uri(self, uri: str) -> Optional[Tab]:
        """
        Get tab by URI.
        
        Args:
            uri: Document URI
            
        Returns:
            Optional[Tab]: Tab
        """
        for tab in self.tabs:
            if tab.uri == uri:
                return tab
        return None
    
    def get_active_tab(self) -> Optional[Tab]:
        """
        Get active tab.
        
        Returns:
            Optional[Tab]: Active tab
        """
        return self.get_tab(self.active_tab_id) if self.active_tab_id else None
    
    def get_all_tabs(self) -> List[Tab]:
        """
        Get all tabs.
        
        Returns:
            List[Tab]: All tabs
        """
        return self.tabs
    
    def get_tabs_by_group(self, group: TabGroup) -> List[Tab]:
        """
        Get tabs by group.
        
        Args:
            group: Tab group
            
        Returns:
            List[Tab]: Tabs
        """
        return [tab for tab in self.tabs if tab.group == group]
    
    def pin_tab(self, tab_id: str) -> bool:
        """
        Pin tab.
        
        Args:
            tab_id: Tab ID
            
        Returns:
            bool: Success
        """
        tab = self.get_tab(tab_id)
        if tab:
            tab.is_pinned = True
            tab.state = TabState.PINNED
            return True
        return False
    
    def unpin_tab(self, tab_id: str) -> bool:
        """
        Unpin tab.
        
        Args:
            tab_id: Tab ID
            
        Returns:
            bool: Success
        """
        tab = self.get_tab(tab_id)
        if tab:
            tab.is_pinned = False
            tab.state = TabState.INACTIVE
            return True
        return False
    
    def toggle_pin(self, tab_id: str) -> bool:
        """
        Toggle pin state.
        
        Args:
            tab_id: Tab ID
            
        Returns:
            bool: Success
        """
        tab = self.get_tab(tab_id)
        if tab:
            if tab.is_pinned:
                return self.unpin_tab(tab_id)
            else:
                return self.pin_tab(tab_id)
        return False
    
    def set_tab_group(self, tab_id: str, group: TabGroup) -> bool:
        """
        Set tab group.
        
        Args:
            tab_id: Tab ID
            group: Tab group
            
        Returns:
            bool: Success
        """
        tab = self.get_tab(tab_id)
        if tab:
            tab.group = group
            return True
        return False
    
    def move_tab(self, tab_id: str, new_index: int) -> bool:
        """
        Move tab to new position.
        
        Args:
            tab_id: Tab ID
            new_index: New index
            
        Returns:
            bool: Success
        """
        tab = self.get_tab(tab_id)
        if not tab:
            return False
        
        try:
            old_index = self.tabs.index(tab)
            self.tabs.pop(old_index)
            self.tabs.insert(new_index, tab)
            return True
        except (ValueError, IndexError):
            return False
    
    def duplicate_tab(self, tab_id: str) -> Optional[Tab]:
        """
        Duplicate tab.
        
        Args:
            tab_id: Tab ID
            
        Returns:
            Optional[Tab]: Duplicated tab
        """
        tab = self.get_tab(tab_id)
        if not tab:
            return None
        
        # Create unique URI for duplicate
        duplicate_uri = f"{tab.uri}?duplicate={self._next_tab_id}"
        
        new_tab = self.add_tab(
            uri=duplicate_uri,
            title=f"{tab.title} (Copy)",
            language=tab.language,
            activate=True
        )
        
        return new_tab
    
    def mark_modified(self, tab_id: str) -> bool:
        """
        Mark tab as modified.
        
        Args:
            tab_id: Tab ID
            
        Returns:
            bool: Success
        """
        tab = self.get_tab(tab_id)
        if tab:
            tab.state = TabState.MODIFIED
            return True
        return False
    
    def mark_saved(self, tab_id: str) -> bool:
        """
        Mark tab as saved.
        
        Args:
            tab_id: Tab ID
            
        Returns:
            bool: Success
        """
        tab = self.get_tab(tab_id)
        if tab:
            if not tab.is_pinned:
                tab.state = TabState.INACTIVE
            return True
        return False
    
    def set_cursor_position(self, tab_id: str, line: int, character: int) -> bool:
        """
        Set cursor position.
        
        Args:
            tab_id: Tab ID
            line: Line number
            character: Character offset
            
        Returns:
            bool: Success
        """
        tab = self.get_tab(tab_id)
        if tab:
            tab.cursor_position = (line, character)
            return True
        return False
    
    def set_scroll_position(self, tab_id: str, position: int) -> bool:
        """
        Set scroll position.
        
        Args:
            tab_id: Tab ID
            position: Scroll position
            
        Returns:
            bool: Success
        """
        tab = self.get_tab(tab_id)
        if tab:
            tab.scroll_position = position
            return True
        return False
    
    def get_tab_history(self) -> List[str]:
        """
        Get tab history.
        
        Returns:
            List[str]: Tab history
        """
        return self.tab_history
    
    def clear_history(self) -> None:
        """Clear tab history."""
        self.tab_history.clear()
    
    def close_all_tabs(self) -> None:
        """Close all tabs except pinned."""
        self.tabs = [tab for tab in self.tabs if tab.is_pinned]
        if self.tabs:
            self.activate_tab(self.tabs[0].id)
        else:
            self.active_tab_id = None
    
    def close_other_tabs(self, tab_id: str) -> bool:
        """
        Close all tabs except the specified one and pinned tabs.
        
        Args:
            tab_id: Tab ID to keep
            
        Returns:
            bool: Success
        """
        tab = self.get_tab(tab_id)
        if not tab:
            return False
        
        self.tabs = [t for t in self.tabs if t.id == tab_id or t.is_pinned]
        self.activate_tab(tab_id)
        return True
    
    def close_tabs_to_right(self, tab_id: str) -> bool:
        """
        Close all tabs to the right of the specified tab.
        
        Args:
            tab_id: Tab ID
            
        Returns:
            bool: Success
        """
        tab = self.get_tab(tab_id)
        if not tab:
            return False
        
        try:
            index = self.tabs.index(tab)
            self.tabs = self.tabs[:index + 1]
            return True
        except ValueError:
            return False
    
    def close_tabs_to_left(self, tab_id: str) -> bool:
        """
        Close all tabs to the left of the specified tab.
        
        Args:
            tab_id: Tab ID
            
        Returns:
            bool: Success
        """
        tab = self.get_tab(tab_id)
        if not tab:
            return False
        
        try:
            index = self.tabs.index(tab)
            self.tabs = self.tabs[index:]
            self.activate_tab(tab_id)
            return True
        except ValueError:
            return False
    
    def update_config(self, config: TabConfig) -> None:
        """
        Update tab configuration.
        
        Args:
            config: New configuration
        """
        self.config = config
    
    def get_config(self) -> TabConfig:
        """
        Get tab configuration.
        
        Returns:
            TabConfig: Configuration
        """
        return self.config


if __name__ == "__main__":
    # Basit test
    config = TabConfig()
    manager = TabManager(config)
    
    # Add tabs
    tab1 = manager.add_tab("file:///test1.py", "test1.py", "python")
    tab2 = manager.add_tab("file:///test2.py", "test2.py", "python")
    
    print(f"Active tab: {manager.get_active_tab().title}")
    print(f"Total tabs: {len(manager.get_all_tabs())}")
    
    # Pin tab
    manager.pin_tab(tab1.id)
    print(f"Tab 1 pinned: {tab1.is_pinned}")
