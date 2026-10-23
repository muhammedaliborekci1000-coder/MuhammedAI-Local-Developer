"""
MuhammedAI Local Developer - Terminal Tabs
Terminal tabs management engine for code editor.
"""

from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime


class TabState(Enum):
    """Tab state."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    BUSY = "busy"
    ERROR = "error"


class TabAction(Enum):
    """Tab action."""
    CREATE = "create"
    CLOSE = "close"
    RENAME = "rename"
    FOCUS = "focus"
    MOVE = "move"
    PIN = "pin"
    UNPIN = "unpin"
    DUPLICATE = "duplicate"


@dataclass
class TabConfig:
    """Tab configuration."""
    shell: str = "powershell"
    working_directory: Optional[str] = None
    theme: str = "default"
    font_family: str = "Consolas"
    font_size: int = 14
    show_close_button: bool = True
    show_notifications: bool = True


@dataclass
class Tab:
    """Terminal tab."""
    id: str
    name: str
    state: TabState
    shell: str
    working_directory: Optional[str]
    theme: str
    font_family: str
    font_size: int
    is_pinned: bool
    created_at: str
    last_activity: str
    command_count: int = 0


@dataclass
class TabResult:
    """Tab result."""
    success: bool
    message: Optional[str] = None
    errors: List[str] = field(default_factory=list)
    tab: Optional[Tab] = None
    tab_id: Optional[str] = None


class TerminalTabsEngine:
    """
    Terminal tabs management engine.
    
    Özellikler:
    - Create tab
    - Close tab
    - Rename tab
    - Focus tab
    - Move tab
    - Pin tab
    - Unpin tab
    - Duplicate tab
    - Get tab
    - Get all tabs
    - Get active tab
    - Get pinned tabs
    - Tab history
    - Tab state tracking
    - Tab ordering
    - Tab persistence
    """
    
    def __init__(self, config: Optional[TabConfig] = None):
        """Initialize terminal tabs engine."""
        self.config = config or TabConfig()
        self.tabs: List[Tab] = []
        self.tab_history: List[Dict[str, Any]] = []
        self.active_tab_id: Optional[str] = None
        self._tab_counter = 0
    
    def create_tab(
        self,
        name: str,
        shell: Optional[str] = None,
        working_directory: Optional[str] = None
    ) -> TabResult:
        """
        Tab oluştur.
        
        Args:
            name: Tab adı
            shell: Shell tipi
            working_directory: Çalışma dizini
            
        Returns:
            TabResult: Oluşturma sonucu
        """
        result = TabResult(success=False)
        
        try:
            # Generate tab ID
            tab_id = f"tab_{self._tab_counter}"
            self._tab_counter += 1
            
            # Create tab
            tab = Tab(
                id=tab_id,
                name=name,
                state=TabState.INACTIVE,
                shell=shell or self.config.shell,
                working_directory=working_directory or self.config.working_directory,
                theme=self.config.theme,
                font_family=self.config.font_family,
                font_size=self.config.font_size,
                is_pinned=False,
                created_at=self._get_timestamp(),
                last_activity=self._get_timestamp()
            )
            
            # Add to tabs
            self.tabs.append(tab)
            
            # Set as active if first tab
            if not self.active_tab_id:
                self.active_tab_id = tab_id
                tab.state = TabState.ACTIVE
            
            # Add to history
            self.tab_history.append({
                "action": "create",
                "tab_id": tab_id,
                "name": name,
                "timestamp": self._get_timestamp()
            })
            
            result.success = True
            result.tab = tab
            result.tab_id = tab_id
            result.message = f"Tab created: {name}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def close_tab(self, tab_id: str) -> TabResult:
        """
        Tab kapat.
        
        Args:
            tab_id: Tab ID
            
        Returns:
            TabResult: Kapatma sonucu
        """
        result = TabResult(success=False)
        result.tab_id = tab_id
        
        try:
            # Find tab
            tab_index = -1
            for i, tab in enumerate(self.tabs):
                if tab.id == tab_id:
                    tab_index = i
                    break
            
            if tab_index == -1:
                result.errors.append(f"Tab not found: {tab_id}")
                return result
            
            # Check if pinned
            if self.tabs[tab_index].is_pinned:
                result.errors.append(f"Cannot close pinned tab: {tab_id}")
                return result
            
            # Remove tab
            removed_tab = self.tabs.pop(tab_index)
            
            # Update active tab
            if self.active_tab_id == tab_id:
                if self.tabs:
                    self.active_tab_id = self.tabs[0].id
                    self.tabs[0].state = TabState.ACTIVE
                else:
                    self.active_tab_id = None
            
            # Add to history
            self.tab_history.append({
                "action": "close",
                "tab_id": tab_id,
                "timestamp": self._get_timestamp()
            })
            
            result.success = True
            result.message = f"Tab closed: {tab_id}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def rename_tab(self, tab_id: str, new_name: str) -> TabResult:
        """
        Tabi yeniden adlandır.
        
        Args:
            tab_id: Tab ID
            new_name: Yeni ad
            
        Returns:
            TabResult: Yeniden adlandırma sonucu
        """
        result = TabResult(success=False)
        result.tab_id = tab_id
        
        try:
            tab = self._get_tab_by_id(tab_id)
            if not tab:
                result.errors.append(f"Tab not found: {tab_id}")
                return result
            
            # Rename tab
            tab.name = new_name
            tab.last_activity = self._get_timestamp()
            
            # Add to history
            self.tab_history.append({
                "action": "rename",
                "tab_id": tab_id,
                "new_name": new_name,
                "timestamp": self._get_timestamp()
            })
            
            result.success = True
            result.tab = tab
            result.message = f"Tab renamed: {new_name}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def focus_tab(self, tab_id: str) -> TabResult:
        """
        Taba odakla.
        
        Args:
            tab_id: Tab ID
            
        Returns:
            TabResult: Odaklama sonucu
        """
        result = TabResult(success=False)
        result.tab_id = tab_id
        
        try:
            tab = self._get_tab_by_id(tab_id)
            if not tab:
                result.errors.append(f"Tab not found: {tab_id}")
                return result
            
            # Update focus
            for t in self.tabs:
                t.state = TabState.INACTIVE
            
            tab.state = TabState.ACTIVE
            tab.last_activity = self._get_timestamp()
            self.active_tab_id = tab_id
            
            # Add to history
            self.tab_history.append({
                "action": "focus",
                "tab_id": tab_id,
                "timestamp": self._get_timestamp()
            })
            
            result.success = True
            result.tab = tab
            result.message = f"Tab focused: {tab_id}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def move_tab(self, tab_id: str, new_index: int) -> TabResult:
        """
        Tabi taşı.
        
        Args:
            tab_id: Tab ID
            new_index: Yeni indeks
            
        Returns:
            TabResult: Taşıma sonucu
        """
        result = TabResult(success=False)
        result.tab_id = tab_id
        
        try:
            # Find tab
            tab_index = -1
            for i, tab in enumerate(self.tabs):
                if tab.id == tab_id:
                    tab_index = i
                    break
            
            if tab_index == -1:
                result.errors.append(f"Tab not found: {tab_id}")
                return result
            
            if new_index < 0 or new_index >= len(self.tabs):
                result.errors.append(f"Invalid index: {new_index}")
                return result
            
            # Move tab
            tab = self.tabs.pop(tab_index)
            self.tabs.insert(new_index, tab)
            
            # Add to history
            self.tab_history.append({
                "action": "move",
                "tab_id": tab_id,
                "old_index": tab_index,
                "new_index": new_index,
                "timestamp": self._get_timestamp()
            })
            
            result.success = True
            result.tab = tab
            result.message = f"Tab moved to index {new_index}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def pin_tab(self, tab_id: str) -> TabResult:
        """
        Tabi sabitle.
        
        Args:
            tab_id: Tab ID
            
        Returns:
            TabResult: Sabitleme sonucu
        """
        result = TabResult(success=False)
        result.tab_id = tab_id
        
        try:
            tab = self._get_tab_by_id(tab_id)
            if not tab:
                result.errors.append(f"Tab not found: {tab_id}")
                return result
            
            # Pin tab
            tab.is_pinned = True
            tab.last_activity = self._get_timestamp()
            
            # Move to front if not already
            if not self.tabs[0].is_pinned:
                tab_index = self.tabs.index(tab)
                self.tabs.pop(tab_index)
                self.tabs.insert(0, tab)
            
            # Add to history
            self.tab_history.append({
                "action": "pin",
                "tab_id": tab_id,
                "timestamp": self._get_timestamp()
            })
            
            result.success = True
            result.tab = tab
            result.message = f"Tab pinned: {tab_id}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def unpin_tab(self, tab_id: str) -> TabResult:
        """
        Tab sabitlemesini kaldır.
        
        Args:
            tab_id: Tab ID
            
        Returns:
            TabResult: Sabitleme kaldırma sonucu
        """
        result = TabResult(success=False)
        result.tab_id = tab_id
        
        try:
            tab = self._get_tab_by_id(tab_id)
            if not tab:
                result.errors.append(f"Tab not found: {tab_id}")
                return result
            
            # Unpin tab
            tab.is_pinned = False
            tab.last_activity = self._get_timestamp()
            
            # Add to history
            self.tab_history.append({
                "action": "unpin",
                "tab_id": tab_id,
                "timestamp": self._get_timestamp()
            })
            
            result.success = True
            result.tab = tab
            result.message = f"Tab unpinned: {tab_id}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def duplicate_tab(self, tab_id: str) -> TabResult:
        """
        Tabi kopyala.
        
        Args:
            tab_id: Tab ID
            
        Returns:
            TabResult: Kopyalama sonucu
        """
        result = TabResult(success=False)
        result.tab_id = tab_id
        
        try:
            original_tab = self._get_tab_by_id(tab_id)
            if not original_tab:
                result.errors.append(f"Tab not found: {tab_id}")
                return result
            
            # Create duplicate
            duplicate_result = self.create_tab(
                f"{original_tab.name} (copy)",
                original_tab.shell,
                original_tab.working_directory
            )
            
            if duplicate_result.success:
                # Add to history
                self.tab_history.append({
                    "action": "duplicate",
                    "tab_id": tab_id,
                    "new_tab_id": duplicate_result.tab_id,
                    "timestamp": self._get_timestamp()
                })
                
                result.success = True
                result.tab = duplicate_result.tab
                result.tab_id = duplicate_result.tab_id
                result.message = f"Tab duplicated: {duplicate_result.tab_id}"
            else:
                result.errors.extend(duplicate_result.errors)
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_tab(self, tab_id: str) -> Optional[Tab]:
        """
        Tab al.
        
        Args:
            tab_id: Tab ID
            
        Returns:
            Optional[Tab]: Tab
        """
        return self._get_tab_by_id(tab_id)
    
    def get_all_tabs(self) -> List[Tab]:
        """
        Tüm tabları al.
        
        Returns:
            List[Tab]: Tabs
        """
        return self.tabs.copy()
    
    def get_active_tab(self) -> Optional[Tab]:
        """
        Aktif tabı al.
        
        Returns:
            Optional[Tab]: Aktif tab
        """
        return self._get_tab_by_id(self.active_tab_id) if self.active_tab_id else None
    
    def get_pinned_tabs(self) -> List[Tab]:
        """
        Sabitlenmiş tabları al.
        
        Returns:
            List[Tab]: Sabitlenmiş tablar
        """
        return [tab for tab in self.tabs if tab.is_pinned]
    
    def get_tab_history(self) -> List[Dict[str, Any]]:
        """
        Tab geçmişini al.
        
        Returns:
            List[Dict[str, Any]]: Geçmiş
        """
        return self.tab_history
    
    def clear_history(self) -> TabResult:
        """
        Geçmişi temizle.
        
        Returns:
            TabResult: Temizleme sonucu
        """
        result = TabResult(success=False)
        
        try:
            self.tab_history.clear()
            result.success = True
            result.message = "Tab history cleared"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def update_config(self, config: TabConfig) -> TabResult:
        """
        Konfigürasyon güncelle.
        
        Args:
            config: Yeni konfigürasyon
            
        Returns:
            TabResult: Güncelleme sonucu
        """
        result = TabResult(success=False)
        
        try:
            self.config = config
            result.success = True
            result.message = "Config updated"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_config(self) -> TabConfig:
        """
        Konfigürasyon al.
        
        Returns:
            TabConfig: Konfigürasyon
        """
        return self.config
    
    def _get_tab_by_id(self, tab_id: str) -> Optional[Tab]:
        """
        ID'ye göre tab al.
        
        Args:
            tab_id: Tab ID
            
        Returns:
            Optional[Tab]: Tab
        """
        for tab in self.tabs:
            if tab.id == tab_id:
                return tab
        return None
    
    def _get_timestamp(self) -> str:
        """
        Zaman damgası al.
        
        Returns:
            str: ISO format zaman damgası
        """
        return datetime.now().isoformat()


if __name__ == "__main__":
    # Basit test
    engine = TerminalTabsEngine()
    
    print("Terminal Tabs Engine initialized")
    print(f"Shell: {engine.config.shell}")
