"""
MuhammedAI Local Developer - Multiple Tabs
Multiple tabs management for code editor.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime


class TabState(Enum):
    """Tab state."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    MODIFIED = "modified"
    READ_ONLY = "read_only"
    PINNED = "pinned"


class TabGroup(Enum):
    """Tab group."""
    UNGROUPED = "ungrouped"
    EDITORS = "editors"
    TERMINALS = "terminals"
    PREVIEW = "preview"
    DEBUG = "debug"


@dataclass
class Tab:
    """Tab."""
    id: str
    title: str
    content: str
    file_path: Optional[str] = None
    language: str = "python"
    state: TabState = TabState.INACTIVE
    group: TabGroup = TabGroup.UNGROUPED
    is_modified: bool = False
    is_pinned: bool = False
    is_read_only: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    last_accessed: datetime = field(default_factory=datetime.now)
    cursor_position: tuple = (0, 0)  # (line, column)
    scroll_position: int = 0


@dataclass
class TabsResult:
    """Tabs result."""
    success: bool
    tabs: List[Tab] = field(default_factory=list)
    active_tab: Optional[Tab] = None
    total_tabs: int = 0
    errors: List[str] = field(default_factory=list)
    message: Optional[str] = None


class TabManager:
    """
    Tab manager for multiple tabs.
    
    Özellikler:
    - Tab creation and deletion
    - Tab switching
    - Tab ordering
    - Tab grouping
    - Tab state management
    - Active tab tracking
    - Modified state tracking
    - Pinned tabs support
    - Read-only tabs support
    - Cursor and scroll position tracking
    - Tab search
    """
    
    def __init__(self):
        """Initialize tab manager."""
        self.tabs: Dict[str, Tab] = {}
        self.active_tab_id: Optional[str] = None
        self.tab_order: List[str] = []
        self._tab_counter = 0
    
    def create_tab(
        self,
        title: str,
        content: str = "",
        file_path: Optional[str] = None,
        language: str = "python",
        group: TabGroup = TabGroup.UNGROUPED
    ) -> TabsResult:
        """
        Yeni tab oluştur.
        
        Args:
            title: Tab başlığı
            content: Tab içeriği
            file_path: Dosya yolu
            language: Programlama dili
            group: Tab grubu
            
        Returns:
            TabsResult: Tab oluşturma sonucu
        """
        result = TabsResult(success=False)
        
        try:
            # Tab ID oluştur
            tab_id = f"tab_{self._tab_counter}"
            self._tab_counter += 1
            
            # Tab oluştur
            tab = Tab(
                id=tab_id,
                title=title,
                content=content,
                file_path=file_path,
                language=language,
                group=group
            )
            
            # Tab'ı ekle
            self.tabs[tab_id] = tab
            self.tab_order.append(tab_id)
            
            # İlk tab ise aktif yap
            if len(self.tabs) == 1:
                self.active_tab_id = tab_id
                tab.state = TabState.ACTIVE
            
            result.tabs = list(self.tabs.values())
            result.active_tab = self.get_active_tab()
            result.total_tabs = len(self.tabs)
            result.success = True
            result.message = f"Tab '{title}' created"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def close_tab(self, tab_id: str) -> TabsResult:
        """
        Tab kapat.
        
        Args:
            tab_id: Tab ID
            
        Returns:
            TabsResult: Tab kapatma sonucu
        """
        result = TabsResult(success=False)
        
        try:
            if tab_id not in self.tabs:
                result.errors.append(f"Tab {tab_id} not found")
                return result
            
            # Tab'ı kaldır
            del self.tabs[tab_id]
            self.tab_order.remove(tab_id)
            
            # Aktif tab ise yeni aktif tab seç
            if self.active_tab_id == tab_id:
                if self.tab_order:
                    self.active_tab_id = self.tab_order[-1]
                    if self.active_tab_id in self.tabs:
                        self.tabs[self.active_tab_id].state = TabState.ACTIVE
                else:
                    self.active_tab_id = None
            
            result.tabs = list(self.tabs.values())
            result.active_tab = self.get_active_tab()
            result.total_tabs = len(self.tabs)
            result.success = True
            result.message = f"Tab {tab_id} closed"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def switch_tab(self, tab_id: str) -> TabsResult:
        """
        Tab'a geç.
        
        Args:
            tab_id: Tab ID
            
        Returns:
            TabsResult: Tab değiştirme sonucu
        """
        result = TabsResult(success=False)
        
        try:
            if tab_id not in self.tabs:
                result.errors.append(f"Tab {tab_id} not found")
                return result
            
            # Önceki aktif tab'ı inactive yap
            if self.active_tab_id and self.active_tab_id in self.tabs:
                self.tabs[self.active_tab_id].state = TabState.INACTIVE
            
            # Yeni aktif tab'ı ayarla
            self.active_tab_id = tab_id
            self.tabs[tab_id].state = TabState.ACTIVE
            self.tabs[tab_id].last_accessed = datetime.now()
            
            # Tab'ı sıranın sonuna taşı
            self.tab_order.remove(tab_id)
            self.tab_order.append(tab_id)
            
            result.tabs = list(self.tabs.values())
            result.active_tab = self.tabs[tab_id]
            result.total_tabs = len(self.tabs)
            result.success = True
            result.message = f"Switched to tab '{self.tabs[tab_id].title}'"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_active_tab(self) -> Optional[Tab]:
        """Aktif tab'ı al."""
        if self.active_tab_id and self.active_tab_id in self.tabs:
            return self.tabs[self.active_tab_id]
        return None
    
    def get_tab(self, tab_id: str) -> Optional[Tab]:
        """Tab al."""
        return self.tabs.get(tab_id)
    
    def get_all_tabs(self) -> List[Tab]:
        """Tüm tab'ları al."""
        return [self.tabs[tab_id] for tab_id in self.tab_order]
    
    def get_tabs_by_group(self, group: TabGroup) -> List[Tab]:
        """Gruba göre tab'ları al."""
        return [tab for tab in self.tabs.values() if tab.group == group]
    
    def update_tab_content(
        self,
        tab_id: str,
        content: str
    ) -> TabsResult:
        """
        Tab içeriğini güncelle.
        
        Args:
            tab_id: Tab ID
            content: Yeni içerik
            
        Returns:
            TabsResult: Güncelleme sonucu
        """
        result = TabsResult(success=False)
        
        try:
            if tab_id not in self.tabs:
                result.errors.append(f"Tab {tab_id} not found")
                return result
            
            self.tabs[tab_id].content = content
            self.tabs[tab_id].is_modified = True
            self.tabs[tab_id].last_accessed = datetime.now()
            
            result.tabs = list(self.tabs.values())
            result.active_tab = self.get_active_tab()
            result.success = True
            result.message = f"Tab '{self.tabs[tab_id].title}' updated"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def pin_tab(self, tab_id: str) -> TabsResult:
        """
        Tab'ı sabitle.
        
        Args:
            tab_id: Tab ID
            
        Returns:
            TabsResult: Sabitleme sonucu
        """
        result = TabsResult(success=False)
        
        try:
            if tab_id not in self.tabs:
                result.errors.append(f"Tab {tab_id} not found")
                return result
            
            self.tabs[tab_id].is_pinned = True
            self.tabs[tab_id].state = TabState.PINNED
            
            result.tabs = list(self.tabs.values())
            result.active_tab = self.get_active_tab()
            result.success = True
            result.message = f"Tab '{self.tabs[tab_id].title}' pinned"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def unpin_tab(self, tab_id: str) -> TabsResult:
        """
        Tab sabitlemesini kaldır.
        
        Args:
            tab_id: Tab ID
            
        Returns:
            TabsResult: Sabitleme kaldırma sonucu
        """
        result = TabsResult(success=False)
        
        try:
            if tab_id not in self.tabs:
                result.errors.append(f"Tab {tab_id} not found")
                return result
            
            self.tabs[tab_id].is_pinned = False
            if self.tabs[tab_id].state == TabState.PINNED:
                self.tabs[tab_id].state = TabState.INACTIVE
            
            result.tabs = list(self.tabs.values())
            result.active_tab = self.get_active_tab()
            result.success = True
            result.message = f"Tab '{self.tabs[tab_id].title}' unpinned"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def set_read_only(self, tab_id: str, read_only: bool = True) -> TabsResult:
        """
        Tab'ı read-only yap.
        
        Args:
            tab_id: Tab ID
            read_only: Read-only durumu
            
        Returns:
            TabsResult: Read-only ayarlama sonucu
        """
        result = TabsResult(success=False)
        
        try:
            if tab_id not in self.tabs:
                result.errors.append(f"Tab {tab_id} not found")
                return result
            
            self.tabs[tab_id].is_read_only = read_only
            self.tabs[tab_id].state = TabState.READ_ONLY if read_only else TabState.INACTIVE
            
            result.tabs = list(self.tabs.values())
            result.active_tab = self.get_active_tab()
            result.success = True
            result.message = f"Tab '{self.tabs[tab_id].title}' read-only set to {read_only}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def update_cursor_position(
        self,
        tab_id: str,
        line: int,
        column: int
    ) -> TabsResult:
        """
        Cursor pozisyonunu güncelle.
        
        Args:
            tab_id: Tab ID
            line: Satır numarası
            column: Sütun numarası
            
        Returns:
            TabsResult: Güncelleme sonucu
        """
        result = TabsResult(success=False)
        
        try:
            if tab_id not in self.tabs:
                result.errors.append(f"Tab {tab_id} not found")
                return result
            
            self.tabs[tab_id].cursor_position = (line, column)
            self.tabs[tab_id].last_accessed = datetime.now()
            
            result.tabs = list(self.tabs.values())
            result.active_tab = self.get_active_tab()
            result.success = True
            result.message = f"Cursor position updated for tab '{self.tabs[tab_id].title}'"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def search_tabs(self, query: str) -> List[Tab]:
        """
        Tab'larda ara.
        
        Args:
            query: Arama sorgusu
            
        Returns:
            List[Tab]: Eşleşen tab'lar
        """
        query_lower = query.lower()
        matching_tabs = []
        
        for tab in self.tabs.values():
            if query_lower in tab.title.lower() or query_lower in tab.content.lower():
                matching_tabs.append(tab)
        
        return matching_tabs


if __name__ == "__main__":
    # Basit test
    manager = TabManager()
    
    # Tab'lar oluştur
    result1 = manager.create_tab("main.py", "def main():\n    pass")
    result2 = manager.create_tab("utils.py", "def helper():\n    pass")
    
    print(f"Created tabs: {result1.total_tabs}")
    print(f"Active tab: {result1.active_tab.title if result1.active_tab else None}")
    
    # Tab değiştir
    result3 = manager.switch_tab(result2.tabs[1].id)
    print(f"Switched to: {result3.active_tab.title if result3.active_tab else None}")
