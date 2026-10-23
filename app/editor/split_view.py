"""
MuhammedAI Local Developer - Split View
Split view engine for code editor.
"""

from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from enum import Enum


class SplitDirection(Enum):
    """Split direction."""
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"


class SplitMode(Enum):
    """Split mode."""
    SPLIT = "split"
    UNSPLIT = "unsplit"
    FOCUS = "focus"


@dataclass
class ViewPane:
    """View pane."""
    pane_id: str
    file_path: str
    content: str
    cursor_line: int = 0
    cursor_column: int = 0
    is_active: bool = False
    scroll_position: int = 0


@dataclass
class SplitViewConfig:
    """Split view configuration."""
    enabled: bool = True
    direction: SplitDirection = SplitDirection.HORIZONTAL
    split_ratio: float = 0.5
    sync_scrolling: bool = True
    sync_cursor: bool = False
    show_divider: bool = True
    divider_size: int = 4
    max_panes: int = 4


@dataclass
class SplitViewResult:
    """Split view result."""
    success: bool
    panes: List[ViewPane] = field(default_factory=list)
    active_pane_id: Optional[str] = None
    errors: List[str] = field(default_factory=list)
    message: Optional[str] = None


class SplitViewEngine:
    """
    Split view engine.
    
    Özellikler:
    - Split view creation
    - Horizontal/vertical splitting
    - Pane management
    - Active pane tracking
    - Scroll synchronization
    - Cursor synchronization
    - Split ratio control
    - Pane focusing
    - Pane closing
    - Multi-pane support
    - Divider customization
    - View switching
    - Content synchronization
    - Layout management
    """
    
    def __init__(self, config: Optional[SplitViewConfig] = None):
        """Initialize split view engine."""
        self.config = config or SplitViewConfig()
        self.panes: List[ViewPane] = []
        self.active_pane_id: Optional[str] = None
        self.pane_counter = 0
    
    def split_view(
        self,
        direction: SplitDirection,
        file_path: str,
        content: str
    ) -> SplitViewResult:
        """
        View'ı split et.
        
        Args:
            direction: Split yönü
            file_path: Dosya yolu
            content: İçerik
            
        Returns:
            SplitViewResult: Split sonucu
        """
        result = SplitViewResult(success=False)
        
        try:
            if not self.config.enabled:
                result.message = "Split view disabled"
                return result
            
            if len(self.panes) >= self.config.max_panes:
                result.errors.append("Maximum panes reached")
                return result
            
            # Pane oluştur
            pane_id = f"pane_{self.pane_counter}"
            self.pane_counter += 1
            
            pane = ViewPane(
                pane_id=pane_id,
                file_path=file_path,
                content=content,
                is_active=True
            )
            
            # Mevcut active'ı kaldır
            for p in self.panes:
                p.is_active = False
            
            self.panes.append(pane)
            self.active_pane_id = pane_id
            
            # Direction güncelle
            self.config.direction = direction
            
            result.success = True
            result.panes = self.panes
            result.active_pane_id = self.active_pane_id
            result.message = f"Split view created with direction {direction.value}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def unsplit_view(self, pane_id: Optional[str] = None) -> SplitViewResult:
        """
        View'ı unsplit et.
        
        Args:
            pane_id: Pane ID (None ise tümünü kapat)
            
        Returns:
            SplitViewResult: Unsplit sonucu
        """
        result = SplitViewResult(success=False)
        
        try:
            if pane_id is None:
                # Tümünü kapat, sadece bir pane tut
                if self.panes:
                    self.panes = [self.panes[0]]
                    self.panes[0].is_active = True
                    self.active_pane_id = self.panes[0].pane_id
                    result.success = True
                    result.panes = self.panes
                    result.message = "View unsplit"
                else:
                    result.errors.append("No panes to unsplit")
            else:
                # Belirli pane'ı kapat
                pane_to_remove = None
                for p in self.panes:
                    if p.pane_id == pane_id:
                        pane_to_remove = p
                        break
                
                if pane_to_remove:
                    if len(self.panes) > 1:
                        self.panes.remove(pane_to_remove)
                        # Yeni active ata
                        if self.active_pane_id == pane_id:
                            self.panes[0].is_active = True
                            self.active_pane_id = self.panes[0].pane_id
                        result.success = True
                        result.panes = self.panes
                        result.message = f"Pane {pane_id} removed"
                    else:
                        result.errors.append("Cannot remove last pane")
                else:
                    result.errors.append("Pane not found")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def focus_pane(self, pane_id: str) -> SplitViewResult:
        """
        Pane'a focus yap.
        
        Args:
            pane_id: Pane ID
            
        Returns:
            SplitViewResult: Focus sonucu
        """
        result = SplitViewResult(success=False)
        
        try:
            pane_found = False
            for p in self.panes:
                if p.pane_id == pane_id:
                    p.is_active = True
                    pane_found = True
                else:
                    p.is_active = False
            
            if pane_found:
                self.active_pane_id = pane_id
                result.success = True
                result.panes = self.panes
                result.active_pane_id = self.active_pane_id
                result.message = f"Focused on pane {pane_id}"
            else:
                result.errors.append("Pane not found")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_active_pane(self) -> Optional[ViewPane]:
        """
        Aktif pane'ı al.
        
        Returns:
            Optional[ViewPane]: Aktif pane
        """
        for pane in self.panes:
            if pane.is_active:
                return pane
        return None
    
    def get_pane_by_id(self, pane_id: str) -> Optional[ViewPane]:
        """
        ID ile pane al.
        
        Args:
            pane_id: Pane ID
            
        Returns:
            Optional[ViewPane]: Pane
        """
        for pane in self.panes:
            if pane.pane_id == pane_id:
                return pane
        return None
    
    def update_pane_content(
        self,
        pane_id: str,
        content: str
    ) -> SplitViewResult:
        """
        Pane içeriğini güncelle.
        
        Args:
            pane_id: Pane ID
            content: Yeni içerik
            
        Returns:
            SplitViewResult: Güncelleme sonucu
        """
        result = SplitViewResult(success=False)
        
        try:
            pane = self.get_pane_by_id(pane_id)
            if pane:
                pane.content = content
                result.success = True
                result.panes = self.panes
                result.message = f"Pane {pane_id} content updated"
            else:
                result.errors.append("Pane not found")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def update_pane_cursor(
        self,
        pane_id: str,
        line: int,
        column: int
    ) -> SplitViewResult:
        """
        Pane cursor'ını güncelle.
        
        Args:
            pane_id: Pane ID
            line: Satır
            column: Sütun
            
        Returns:
            SplitViewResult: Güncelleme sonucu
        """
        result = SplitViewResult(success=False)
        
        try:
            pane = self.get_pane_by_id(pane_id)
            if pane:
                pane.cursor_line = line
                pane.cursor_column = column
                
                # Sync cursor
                if self.config.sync_cursor:
                    for p in self.panes:
                        if p.pane_id != pane_id:
                            p.cursor_line = line
                            p.cursor_column = column
                
                result.success = True
                result.panes = self.panes
                result.message = f"Pane {pane_id} cursor updated"
            else:
                result.errors.append("Pane not found")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def update_pane_scroll(
        self,
        pane_id: str,
        scroll_position: int
    ) -> SplitViewResult:
        """
        Pane scroll pozisyonunu güncelle.
        
        Args:
            pane_id: Pane ID
            scroll_position: Scroll pozisyonu
            
        Returns:
            SplitViewResult: Güncelleme sonucu
        """
        result = SplitViewResult(success=False)
        
        try:
            pane = self.get_pane_by_id(pane_id)
            if pane:
                pane.scroll_position = scroll_position
                
                # Sync scroll
                if self.config.sync_scrolling:
                    for p in self.panes:
                        if p.pane_id != pane_id:
                            p.scroll_position = scroll_position
                
                result.success = True
                result.panes = self.panes
                result.message = f"Pane {pane_id} scroll updated"
            else:
                result.errors.append("Pane not found")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def set_split_direction(self, direction: SplitDirection) -> SplitViewResult:
        """
        Split yönünü ayarla.
        
        Args:
            direction: Split yönü
            
        Returns:
            SplitViewResult: Ayarlama sonucu
        """
        result = SplitViewResult(success=False)
        
        try:
            self.config.direction = direction
            result.success = True
            result.message = f"Split direction set to {direction.value}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def set_split_ratio(self, ratio: float) -> SplitViewResult:
        """
        Split oranını ayarla.
        
        Args:
            ratio: Split oranı (0.0 - 1.0)
            
        Returns:
            SplitViewResult: Ayarlama sonucu
        """
        result = SplitViewResult(success=False)
        
        try:
            if 0.0 <= ratio <= 1.0:
                self.config.split_ratio = ratio
                result.success = True
                result.message = f"Split ratio set to {ratio}"
            else:
                result.errors.append("Ratio must be between 0.0 and 1.0")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def toggle_sync_scrolling(self) -> SplitViewResult:
        """
        Sync scrolling'ı aç/kapat.
        
        Returns:
            SplitViewResult: Toggle sonucu
        """
        result = SplitViewResult(success=False)
        
        try:
            self.config.sync_scrolling = not self.config.sync_scrolling
            result.success = True
            result.message = f"Sync scrolling {'enabled' if self.config.sync_scrolling else 'disabled'}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def toggle_sync_cursor(self) -> SplitViewResult:
        """
        Sync cursor'ı aç/kapat.
        
        Returns:
            SplitViewResult: Toggle sonucu
        """
        result = SplitViewResult(success=False)
        
        try:
            self.config.sync_cursor = not self.config.sync_cursor
            result.success = True
            result.message = f"Sync cursor {'enabled' if self.config.sync_cursor else 'disabled'}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_all_panes(self) -> List[ViewPane]:
        """
        Tüm pane'ları al.
        
        Returns:
            List[ViewPane]: Pane listesi
        """
        return self.panes
    
    def get_pane_count(self) -> int:
        """
        Pane sayısını al.
        
        Returns:
            int: Pane sayısı
        """
        return len(self.panes)
    
    def update_config(self, config: SplitViewConfig) -> SplitViewResult:
        """
        Konfigürasyon güncelle.
        
        Args:
            config: Yeni konfigürasyon
            
        Returns:
            SplitViewResult: Güncelleme sonucu
        """
        result = SplitViewResult(success=False)
        
        try:
            self.config = config
            result.success = True
            result.message = "Config updated"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_config(self) -> SplitViewConfig:
        """
        Konfigürasyon al.
        
        Returns:
            SplitViewConfig: Konfigürasyon
        """
        return self.config


if __name__ == "__main__":
    # Basit test
    config = SplitViewConfig()
    engine = SplitViewEngine(config)
    
    # Split et
    result = engine.split_view(SplitDirection.HORIZONTAL, "test.py", "print('hello')")
    print(f"Split: {result.success}")
    
    # İkinci pane ekle
    result = engine.split_view(SplitDirection.HORIZONTAL, "test2.py", "print('world')")
    print(f"Second pane: {result.success}")
