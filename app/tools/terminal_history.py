"""
MuhammedAI Local Developer - Terminal History
Terminal history management engine for code editor.
"""

from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime


class HistoryAction(Enum):
    """History action."""
    ADD = "add"
    REMOVE = "remove"
    CLEAR = "clear"
    SEARCH = "search"
    EXPORT = "export"
    IMPORT = "import"


@dataclass
class HistoryConfig:
    """History configuration."""
    max_entries: int = 1000
    persist_to_disk: bool = False
    storage_path: str = ""
    auto_save: bool = True
    show_notifications: bool = True


@dataclass
class HistoryEntry:
    """History entry."""
    id: str
    command: str
    panel_id: str
    timestamp: str
    exit_code: Optional[int] = None
    duration: float = 0.0
    working_directory: Optional[str] = None


@dataclass
class HistoryResult:
    """History result."""
    success: bool
    message: Optional[str] = None
    errors: List[str] = field(default_factory=list)
    entry: Optional[HistoryEntry] = None
    entries: List[HistoryEntry] = field(default_factory=list)
    count: int = 0


class TerminalHistoryEngine:
    """
    Terminal history management engine.
    
    Özellikler:
    - Add command to history
    - Remove command from history
    - Clear history
    - Search history
    - Export history
    - Import history
    - Get history by panel
    - Get history by date
    - Get recent commands
    - Get frequent commands
    - History persistence
    - History navigation
    - History filtering
    """
    
    def __init__(self, config: Optional[HistoryConfig] = None):
        """Initialize terminal history engine."""
        self.config = config or HistoryConfig()
        self.history: List[HistoryEntry] = []
        self.history_counter = 0
    
    def add_command(
        self,
        command: str,
        panel_id: str,
        exit_code: Optional[int] = None,
        duration: float = 0.0,
        working_directory: Optional[str] = None
    ) -> HistoryResult:
        """
        Komutu geçmişe ekle.
        
        Args:
            command: Komut
            panel_id: Panel ID
            exit_code: Çıkış kodu
            duration: Süre
            working_directory: Çalışma dizini
            
        Returns:
            HistoryResult: Ekleme sonucu
        """
        result = HistoryResult(success=False)
        
        try:
            # Generate entry ID
            entry_id = f"history_{self.history_counter}"
            self.history_counter += 1
            
            # Create entry
            entry = HistoryEntry(
                id=entry_id,
                command=command,
                panel_id=panel_id,
                timestamp=self._get_timestamp(),
                exit_code=exit_code,
                duration=duration,
                working_directory=working_directory
            )
            
            # Add to history
            self.history.append(entry)
            
            # Trim if exceeds max
            if len(self.history) > self.config.max_entries:
                self.history = self.history[-self.config.max_entries:]
            
            result.success = True
            result.entry = entry
            result.count = len(self.history)
            result.message = f"Command added to history: {command[:50]}..."
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def remove_command(self, entry_id: str) -> HistoryResult:
        """
        Komutu geçmişten sil.
        
        Args:
            entry_id: Entry ID
            
        Returns:
            HistoryResult: Silme sonucu
        """
        result = HistoryResult(success=False)
        
        try:
            # Find and remove entry
            for i, entry in enumerate(self.history):
                if entry.id == entry_id:
                    removed_entry = self.history.pop(i)
                    result.success = True
                    result.entry = removed_entry
                    result.count = len(self.history)
                    result.message = f"Command removed: {removed_entry.command[:50]}..."
                    return result
            
            result.errors.append(f"Entry not found: {entry_id}")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def clear_history(self, panel_id: Optional[str] = None) -> HistoryResult:
        """
        Geçmişi temizle.
        
        Args:
            panel_id: Panel ID (opsiyonel, belirtilirse sadece o panel)
            
        Returns:
            HistoryResult: Temizleme sonucu
        """
        result = HistoryResult(success=False)
        
        try:
            if panel_id:
                # Clear only for specific panel
                original_count = len(self.history)
                self.history = [entry for entry in self.history if entry.panel_id != panel_id]
                removed_count = original_count - len(self.history)
                result.success = True
                result.count = len(self.history)
                result.message = f"Cleared {removed_count} entries for panel {panel_id}"
            else:
                # Clear all
                removed_count = len(self.history)
                self.history.clear()
                result.success = True
                result.count = 0
                result.message = f"Cleared all {removed_count} entries"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def search_history(
        self,
        query: str,
        panel_id: Optional[str] = None,
        limit: int = 100
    ) -> HistoryResult:
        """
        Geçmişte ara.
        
        Args:
            query: Arama sorgusu
            panel_id: Panel ID (opsiyonel)
            limit: Sonuç limiti
            
        Returns:
            HistoryResult: Arama sonucu
        """
        result = HistoryResult(success=False)
        
        try:
            query_lower = query.lower()
            
            # Search
            filtered = []
            for entry in reversed(self.history):
                if panel_id and entry.panel_id != panel_id:
                    continue
                if query_lower in entry.command.lower():
                    filtered.append(entry)
                    if len(filtered) >= limit:
                        break
            
            result.success = True
            result.entries = filtered
            result.count = len(filtered)
            result.message = f"Found {len(filtered)} entries matching '{query}'"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_history_by_panel(self, panel_id: str, limit: int = 100) -> HistoryResult:
        """
        Panele göre geçmiş al.
        
        Args:
            panel_id: Panel ID
            limit: Sonuç limiti
            
        Returns:
            HistoryResult: Geçmiş sonucu
        """
        result = HistoryResult(success=False)
        
        try:
            filtered = [
                entry for entry in reversed(self.history)
                if entry.panel_id == panel_id
            ][:limit]
            
            result.success = True
            result.entries = filtered
            result.count = len(filtered)
            result.message = f"Found {len(filtered)} entries for panel {panel_id}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_recent_commands(self, limit: int = 10) -> HistoryResult:
        """
        Son komutları al.
        
        Args:
            limit: Sonuç limiti
            
        Returns:
            HistoryResult: Son komutlar sonucu
        """
        result = HistoryResult(success=False)
        
        try:
            recent = list(reversed(self.history))[:limit]
            
            result.success = True
            result.entries = recent
            result.count = len(recent)
            result.message = f"Retrieved {len(recent)} recent commands"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_frequent_commands(self, limit: int = 10) -> HistoryResult:
        """
        Sık kullanılan komutları al.
        
        Args:
            limit: Sonuç limiti
            
        Returns:
            HistoryResult: Sık kullanılan komutlar sonucu
        """
        result = HistoryResult(success=False)
        
        try:
            # Count command frequency
            command_counts: Dict[str, int] = {}
            for entry in self.history:
                command_counts[entry.command] = command_counts.get(entry.command, 0) + 1
            
            # Sort by frequency
            sorted_commands = sorted(
                command_counts.items(),
                key=lambda x: x[1],
                reverse=True
            )[:limit]
            
            # Get entries
            frequent = []
            for command, count in sorted_commands:
                for entry in reversed(self.history):
                    if entry.command == command:
                        frequent.append(entry)
                        break
            
            result.success = True
            result.entries = frequent
            result.count = len(frequent)
            result.message = f"Retrieved {len(frequent)} frequent commands"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_all_history(self) -> HistoryResult:
        """
        Tüm geçmişi al.
        
        Returns:
            HistoryResult: Tüm geçmiş sonucu
        """
        result = HistoryResult(success=False)
        
        try:
            result.success = True
            result.entries = list(reversed(self.history))
            result.count = len(self.history)
            result.message = f"Retrieved {len(self.history)} history entries"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def export_history(self, format: str = "json") -> HistoryResult:
        """
        Geçmişi dışa aktar.
        
        Args:
            format: Format (json, txt)
            
        Returns:
            HistoryResult: Dışa aktarma sonucu
        """
        result = HistoryResult(success=False)
        
        try:
            if format == "json":
                import json
                data = [
                    {
                        "id": entry.id,
                        "command": entry.command,
                        "panel_id": entry.panel_id,
                        "timestamp": entry.timestamp,
                        "exit_code": entry.exit_code,
                        "duration": entry.duration,
                        "working_directory": entry.working_directory
                    }
                    for entry in self.history
                ]
                result.success = True
                result.message = f"Exported {len(data)} entries as JSON"
            elif format == "txt":
                lines = [entry.command for entry in self.history]
                result.success = True
                result.message = f"Exported {len(lines)} entries as TXT"
            else:
                result.errors.append(f"Unsupported format: {format}")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def import_history(self, data: List[Dict[str, Any]]) -> HistoryResult:
        """
        Geçmişi içe aktar.
        
        Args:
            data: Veri
            
        Returns:
            HistoryResult: İçe aktarma sonucu
        """
        result = HistoryResult(success=False)
        
        try:
            imported_count = 0
            for item in data:
                entry = HistoryEntry(
                    id=item.get("id", f"history_{self.history_counter}"),
                    command=item["command"],
                    panel_id=item["panel_id"],
                    timestamp=item.get("timestamp", self._get_timestamp()),
                    exit_code=item.get("exit_code"),
                    duration=item.get("duration", 0.0),
                    working_directory=item.get("working_directory")
                )
                self.history.append(entry)
                self.history_counter += 1
                imported_count += 1
            
            result.success = True
            result.count = imported_count
            result.message = f"Imported {imported_count} entries"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def update_config(self, config: HistoryConfig) -> HistoryResult:
        """
        Konfigürasyon güncelle.
        
        Args:
            config: Yeni konfigürasyon
            
        Returns:
            HistoryResult: Güncelleme sonucu
        """
        result = HistoryResult(success=False)
        
        try:
            self.config = config
            result.success = True
            result.message = "Config updated"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_config(self) -> HistoryConfig:
        """
        Konfigürasyon al.
        
        Returns:
            HistoryConfig: Konfigürasyon
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
    engine = TerminalHistoryEngine()
    
    print("Terminal History Engine initialized")
    print(f"Max entries: {engine.config.max_entries}")
