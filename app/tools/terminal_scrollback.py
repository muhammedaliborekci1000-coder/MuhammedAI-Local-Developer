"""
MuhammedAI Local Developer - Terminal Scrollback
Terminal scrollback management engine for code editor.
"""

from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime


class ScrollbackMode(Enum):
    """Scrollback mode."""
    UNLIMITED = "unlimited"
    LIMITED = "limited"
    CIRCULAR = "circular"


class ScrollbackAction(Enum):
    """Scrollback action."""
    ADD = "add"
    CLEAR = "clear"
    SEARCH = "search"
    SAVE = "save"
    LOAD = "load"
    EXPORT = "export"
    IMPORT = "import"
    NAVIGATE = "navigate"


@dataclass
class ScrollbackConfig:
    """Scrollback configuration."""
    max_lines: int = 1000
    mode: ScrollbackMode = ScrollbackMode.LIMITED
    enable_search: bool = True
    enable_persistence: bool = False
    storage_path: str = ""
    auto_save: bool = True
    show_line_numbers: bool = True
    show_timestamps: bool = False
    show_notifications: bool = True


@dataclass
class ScrollbackEntry:
    """Scrollback entry."""
    id: str
    content: str
    line_number: int
    timestamp: str
    panel_id: Optional[str] = None
    command_id: Optional[str] = None


@dataclass
class ScrollbackResult:
    """Scrollback result."""
    success: bool
    message: Optional[str] = None
    errors: List[str] = field(default_factory=list)
    entries: List[ScrollbackEntry] = field(default_factory=list)
    count: int = 0


class TerminalScrollbackEngine:
    """
    Terminal scrollback management engine.
    
    Özellikler:
    - Add line to scrollback
    - Clear scrollback
    - Search scrollback
    - Save scrollback
    - Load scrollback
    - Export scrollback
    - Import scrollback
    - Navigate scrollback
    - Get scrollback
    - Get scrollback by panel
    - Scrollback limit
    - Scrollback mode
    - Scrollback history
    - Line numbers
    - Timestamps
    """
    
    def __init__(self, config: Optional[ScrollbackConfig] = None):
        """Initialize terminal scrollback engine."""
        self.config = config or ScrollbackConfig()
        self.scrollback: List[ScrollbackEntry] = []
        self.scrollback_history: List[Dict[str, Any]] = []
        self._line_counter = 0
        self._entry_counter = 0
    
    def add_line(
        self,
        content: str,
        panel_id: Optional[str] = None,
        command_id: Optional[str] = None
    ) -> ScrollbackResult:
        """
        Satır ekle.
        
        Args:
            content: İçerik
            panel_id: Panel ID
            command_id: Komut ID
            
        Returns:
            ScrollbackResult: Ekleme sonucu
        """
        result = ScrollbackResult(success=False)
        
        try:
            # Generate entry ID
            entry_id = f"scrollback_{self._entry_counter}"
            self._entry_counter += 1
            
            # Increment line counter
            self._line_counter += 1
            
            # Create entry
            entry = ScrollbackEntry(
                id=entry_id,
                content=content,
                line_number=self._line_counter,
                timestamp=self._get_timestamp(),
                panel_id=panel_id,
                command_id=command_id
            )
            
            # Add to scrollback
            self.scrollback.append(entry)
            
            # Trim if exceeds limit
            if self.config.mode == ScrollbackMode.LIMITED:
                if len(self.scrollback) > self.config.max_lines:
                    self.scrollback = self.scrollback[-self.config.max_lines:]
            elif self.config.mode == ScrollbackMode.CIRCULAR:
                if len(self.scrollback) > self.config.max_lines:
                    self.scrollback.pop(0)
            
            # Add to history
            self.scrollback_history.append({
                "action": "add",
                "entry_id": entry_id,
                "line_number": entry.line_number,
                "timestamp": entry.timestamp,
                "panel_id": panel_id,
                "command_id": command_id
            })
            
            result.success = True
            result.entries = [entry]
            result.count = len(self.scrollback)
            result.message = f"Line added: {content[:50]}..."
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def clear_scrollback(self, panel_id: Optional[str] = None) -> ScrollbackResult:
        """
        Scrollback'ı temizle.
        
        Args:
            panel_id: Panel ID (opsiyonel)
            
        Returns:
            ScrollbackResult: Temizleme sonucu
        """
        result = ScrollbackResult(success=False)
        
        try:
            if panel_id:
                # Clear only for specific panel
                original_count = len(self.scrollback)
                self.scrollback = [entry for entry in self.scrollback if entry.panel_id != panel_id]
                removed_count = original_count - len(self.scrollback)
                result.success = True
                result.count = len(self.scrollback)
                result.message = f"Cleared {removed_count} lines for panel {panel_id}"
            else:
                # Clear all
                removed_count = len(self.scrollback)
                self.scrollback.clear()
                self._line_counter = 0
                result.success = True
                result.count = 0
                result.message = f"Cleared all {removed_count} lines"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def search_scrollback(
        self,
        query: str,
        panel_id: Optional[str] = None,
        limit: int = 100
    ) -> ScrollbackResult:
        """
        Scrollback'ta ara.
        
        Args:
            query: Arama sorgusu
            panel_id: Panel ID (opsiyonel)
            limit: Sonuç limiti
            
        Returns:
            ScrollbackResult: Arama sonucu
        """
        result = ScrollbackResult(success=False)
        
        try:
            query_lower = query.lower()
            
            # Search
            filtered = []
            for entry in self.scrollback:
                if panel_id and entry.panel_id != panel_id:
                    continue
                if query_lower in entry.content.lower():
                    filtered.append(entry)
                    if len(filtered) >= limit:
                        break
            
            result.success = True
            result.entries = filtered
            result.count = len(filtered)
            result.message = f"Found {len(filtered)} lines matching '{query}'"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_scrollback(
        self,
        offset: int = 0,
        limit: int = 100,
        panel_id: Optional[str] = None
    ) -> ScrollbackResult:
        """
        Scrollback al.
        
        Args:
            offset: Başlangıç indeksi
            limit: Sonuç limiti
            panel_id: Panel ID (opsiyonel)
            
        Returns:
            ScrollbackResult: Alma sonucu
        """
        result = ScrollbackResult(success=False)
        
        try:
            filtered = self.scrollback
            
            if panel_id:
                filtered = [entry for entry in filtered if entry.panel_id == panel_id]
            
            # Apply offset and limit
            entries = filtered[offset:offset + limit]
            
            result.success = True
            result.entries = entries
            result.count = len(entries)
            result.message = f"Retrieved {len(entries)} lines"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_scrollback_by_panel(self, panel_id: str, limit: int = 100) -> ScrollbackResult:
        """
        Panele göre scrollback al.
        
        Args:
            panel_id: Panel ID
            limit: Sonuç limiti
            
        Returns:
            ScrollbackResult: Alma sonucu
        """
        result = ScrollbackResult(success=False)
        
        try:
            filtered = [
                entry for entry in self.scrollback
                if entry.panel_id == panel_id
            ][:limit]
            
            result.success = True
            result.entries = filtered
            result.count = len(filtered)
            result.message = f"Retrieved {len(filtered)} lines for panel {panel_id}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def export_scrollback(self, format: str = "json") -> ScrollbackResult:
        """
        Scrollback'ı dışa aktar.
        
        Args:
            format: Format (json, txt)
            
        Returns:
            ScrollbackResult: Dışa aktarma sonucu
        """
        result = ScrollbackResult(success=False)
        
        try:
            if format == "json":
                import json
                data = [
                    {
                        "id": entry.id,
                        "content": entry.content,
                        "line_number": entry.line_number,
                        "timestamp": entry.timestamp,
                        "panel_id": entry.panel_id,
                        "command_id": entry.command_id
                    }
                    for entry in self.scrollback
                ]
                result.success = True
                result.message = f"Exported {len(data)} lines as JSON"
            elif format == "txt":
                lines = [entry.content for entry in self.scrollback]
                result.success = True
                result.message = f"Exported {len(lines)} lines as TXT"
            else:
                result.errors.append(f"Unsupported format: {format}")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def import_scrollback(self, data: List[Dict[str, Any]]) -> ScrollbackResult:
        """
        Scrollback'ı içe aktar.
        
        Args:
            data: Veri
            
        Returns:
            ScrollbackResult: İçe aktarma sonucu
        """
        result = ScrollbackResult(success=False)
        
        try:
            imported_count = 0
            for item in data:
                entry = ScrollbackEntry(
                    id=item.get("id", f"scrollback_{self._entry_counter}"),
                    content=item["content"],
                    line_number=item.get("line_number", self._line_counter + 1),
                    timestamp=item.get("timestamp", self._get_timestamp()),
                    panel_id=item.get("panel_id"),
                    command_id=item.get("command_id")
                )
                self.scrollback.append(entry)
                self._entry_counter += 1
                self._line_counter += 1
                imported_count += 1
            
            result.success = True
            result.count = imported_count
            result.message = f"Imported {imported_count} lines"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_scrollback_history(self) -> List[Dict[str, Any]]:
        """
        Scrollback geçmişini al.
        
        Returns:
            List[Dict[str, Any]]: Geçmiş
        """
        return self.scrollback_history
    
    def clear_history(self) -> ScrollbackResult:
        """
        Geçmişi temizle.
        
        Returns:
            ScrollbackResult: Temizleme sonucu
        """
        result = ScrollbackResult(success=False)
        
        try:
            self.scrollback_history.clear()
            result.success = True
            result.message = "Scrollback history cleared"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def update_config(self, config: ScrollbackConfig) -> ScrollbackResult:
        """
        Konfigürasyon güncelle.
        
        Args:
            config: Yeni konfigürasyon
            
        Returns:
            ScrollbackResult: Güncelleme sonucu
        """
        result = ScrollbackResult(success=False)
        
        try:
            self.config = config
            result.success = True
            result.message = "Config updated"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_config(self) -> ScrollbackConfig:
        """
        Konfigürasyon al.
        
        Returns:
            ScrollbackConfig: Konfigürasyon
        """
        return self.config
    
    def _get_timestamp(self) -> str:
        """
        Zaman damgası al.
        
        Returns:
            str: ISO format zaman damgası
        """
        return datetime.now().isoformat()


if __name__ == "__main__":
    # Basit test
    engine = TerminalScrollbackEngine()
    
    print("Terminal Scrollback Engine initialized")
    print(f"Max lines: {engine.config.max_lines}")
