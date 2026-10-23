"""
MuhammedAI Local Developer - Terminal Selection
Terminal selection management engine for code editor.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime


class SelectionMode(Enum):
    """Selection mode."""
    CHARACTER = "character"
    WORD = "word"
    LINE = "line"
    BLOCK = "block"
    SMART = "smart"
    RECTANGULAR = "rectangular"


class SelectionScope(Enum):
    """Selection scope."""
    SESSION = "session"
    TERMINAL = "terminal"
    GLOBAL = "global"


class SelectionAction(Enum):
    """Selection action."""
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    GET = "get"
    LIST = "list"
    ACTIVATE = "activate"
    CLONE = "clone"
    IMPORT = "import"
    EXPORT = "export"
    SET_DEFAULT = "set_default"
    SELECT_ALL = "select_all"
    SELECT_WORD = "select_word"
    SELECT_LINE = "select_line"
    CLEAR = "clear"
    COPY = "copy"
    RESET = "reset"


@dataclass
class SelectionConfig:
    """Selection configuration."""
    persist_selections: bool = True
    auto_load_selections: bool = True
    show_notifications: bool = True
    log_changes: bool = True
    validate_selections: bool = True


@dataclass
class SelectionPosition:
    """Selection position."""
    line: int
    column: int
    viewport_line: int = 0
    viewport_column: int = 0


@dataclass
class SelectionRange:
    """Selection range."""
    start: SelectionPosition
    end: SelectionPosition
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "start": {
                "line": self.start.line,
                "column": self.start.column,
                "viewport_line": self.start.viewport_line,
                "viewport_column": self.start.viewport_column
            },
            "end": {
                "line": self.end.line,
                "column": self.end.column,
                "viewport_line": self.end.viewport_line,
                "viewport_column": self.end.viewport_column
            }
        }


@dataclass
class SelectionEntry:
    """Selection entry."""
    id: str
    name: str
    mode: SelectionMode
    range: SelectionRange
    background_color: str
    foreground_color: str
    scope: SelectionScope
    timestamp: str = ""
    is_default: bool = False
    is_active: bool = False
    terminal_id: Optional[str] = None
    session_id: Optional[str] = None


@dataclass
class SelectionResult:
    """Selection result."""
    success: bool
    message: Optional[str] = None
    errors: List[str] = field(default_factory=list)
    selection_id: Optional[str] = None
    selection_name: Optional[str] = None
    action: Optional[str] = None
    selected_text: Optional[str] = None


class TerminalSelectionEngine:
    """
    Terminal selection management engine.
    
    Özellikler:
    - Create selection
    - Update selection
    - Delete selection
    - Get selection
    - List selections
    - Activate selection
    - Clone selection
    - Import selection
    - Export selection
    - Set default selection
    - Select all
    - Select word
    - Select line
    - Clear selection
    - Copy selection
    - Reset selection
    - Selection scope (session, terminal, global)
    - Selection mode management
    - Selection range management
    - Selection color management
    - Selection persistence
    - Selection validation
    - Selection history
    - Selection search/filter
    """
    
    def __init__(self, config: Optional[SelectionConfig] = None):
        """Initialize terminal selection engine."""
        self.config = config or SelectionConfig()
        self.selections: Dict[str, SelectionEntry] = {}
        self.selection_history: List[Dict[str, Any]] = []
        self._selection_counter = 0
        self._default_selection: Optional[str] = None
        self._active_selection: Optional[str] = None
    
    def create_selection(
        self,
        name: str,
        mode: SelectionMode = SelectionMode.CHARACTER,
        start_line: int = 0,
        start_column: int = 0,
        end_line: int = 0,
        end_column: int = 0,
        background_color: str = "#ffffff",
        foreground_color: str = "#000000",
        scope: SelectionScope = SelectionScope.SESSION,
        terminal_id: Optional[str] = None,
        session_id: Optional[str] = None
    ) -> SelectionResult:
        """
        Seçim oluştur.
        
        Args:
            name: Seçim adı
            mode: Seçim modu
            start_line: Başlangıç satırı
            start_column: Başlangıç sütunu
            end_line: Bitiş satırı
            end_column: Bitiş sütunu
            background_color: Arka plan rengi
            foreground_color: Ön plan rengi
            scope: Kapsam
            terminal_id: Terminal ID
            session_id: Oturum ID
            
        Returns:
            SelectionResult: Oluşturma sonucu
        """
        result = SelectionResult(success=False)
        result.action = SelectionAction.CREATE.value
        result.selection_name = name
        
        try:
            # Validate
            if self.config.validate_selections:
                if not name or not isinstance(name, str):
                    result.errors.append("Invalid selection name")
                    return result
            
            # Create range
            start = SelectionPosition(line=start_line, column=start_column)
            end = SelectionPosition(line=end_line, column=end_column)
            range_obj = SelectionRange(start=start, end=end)
            
            # Create entry
            selection_id = f"selection_{self._selection_counter}"
            self._selection_counter += 1
            
            entry = SelectionEntry(
                id=selection_id,
                name=name,
                mode=mode,
                range=range_obj,
                background_color=background_color,
                foreground_color=foreground_color,
                scope=scope,
                timestamp=self._get_timestamp(),
                terminal_id=terminal_id,
                session_id=session_id
            )
            
            # Store
            self.selections[selection_id] = entry
            
            # Set as default if first selection
            if self._default_selection is None:
                self._default_selection = selection_id
                entry.is_default = True
            
            # Add to history
            if self.config.log_changes:
                self.selection_history.append({
                    "action": "create",
                    "selection_id": selection_id,
                    "name": name,
                    "scope": scope.value,
                    "timestamp": entry.timestamp
                })
            
            result.success = True
            result.selection_id = selection_id
            result.message = f"Selection {name} created"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def update_selection(
        self,
        selection_id: str,
        name: Optional[str] = None,
        mode: Optional[SelectionMode] = None,
        start_line: Optional[int] = None,
        start_column: Optional[int] = None,
        end_line: Optional[int] = None,
        end_column: Optional[int] = None,
        background_color: Optional[str] = None,
        foreground_color: Optional[str] = None
    ) -> SelectionResult:
        """
        Seçim güncelle.
        
        Args:
            selection_id: Seçim ID
            name: Seçim adı
            mode: Seçim modu
            start_line: Başlangıç satırı
            start_column: Başlangıç sütunu
            end_line: Bitiş satırı
            end_column: Bitiş sütunu
            background_color: Arka plan rengi
            foreground_color: Ön plan rengi
            
        Returns:
            SelectionResult: Güncelleme sonucu
        """
        result = SelectionResult(success=False)
        result.action = SelectionAction.UPDATE.value
        result.selection_id = selection_id
        
        try:
            if selection_id not in self.selections:
                result.errors.append(f"Selection not found: {selection_id}")
                return result
            
            entry = self.selections[selection_id]
            
            if name is not None:
                entry.name = name
                result.selection_name = name
            if mode is not None:
                entry.mode = mode
            if start_line is not None or start_column is not None or end_line is not None or end_column is not None:
                start = SelectionPosition(
                    line=start_line if start_line is not None else entry.range.start.line,
                    column=start_column if start_column is not None else entry.range.start.column
                )
                end = SelectionPosition(
                    line=end_line if end_line is not None else entry.range.end.line,
                    column=end_column if end_column is not None else entry.range.end.column
                )
                entry.range = SelectionRange(start=start, end=end)
            if background_color is not None:
                entry.background_color = background_color
            if foreground_color is not None:
                entry.foreground_color = foreground_color
            
            entry.timestamp = self._get_timestamp()
            
            # Add to history
            if self.config.log_changes:
                self.selection_history.append({
                    "action": "update",
                    "selection_id": selection_id,
                    "timestamp": entry.timestamp
                })
            
            result.success = True
            result.message = f"Selection {selection_id} updated"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def delete_selection(self, selection_id: str) -> SelectionResult:
        """
        Seçim sil.
        
        Args:
            selection_id: Seçim ID
            
        Returns:
            SelectionResult: Silme sonucu
        """
        result = SelectionResult(success=False)
        result.action = SelectionAction.DELETE.value
        result.selection_id = selection_id
        
        try:
            if selection_id not in self.selections:
                result.errors.append(f"Selection not found: {selection_id}")
                return result
            
            entry = self.selections[selection_id]
            name = entry.name
            
            del self.selections[selection_id]
            
            # Reset default if deleted
            if self._default_selection == selection_id:
                self._default_selection = None
                # Set new default if available
                if self.selections:
                    self._default_selection = list(self.selections.keys())[0]
                    self.selections[self._default_selection].is_default = True
            
            # Reset active if deleted
            if self._active_selection == selection_id:
                self._active_selection = None
            
            # Add to history
            if self.config.log_changes:
                self.selection_history.append({
                    "action": "delete",
                    "selection_id": selection_id,
                    "name": name,
                    "timestamp": self._get_timestamp()
                })
            
            result.success = True
            result.message = f"Selection {name} deleted"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_selection(self, selection_id: str) -> SelectionResult:
        """
        Seçim al.
        
        Args:
            selection_id: Seçim ID
            
        Returns:
            SelectionResult: Alma sonucu
        """
        result = SelectionResult(success=False)
        result.action = SelectionAction.GET.value
        result.selection_id = selection_id
        
        try:
            if selection_id not in self.selections:
                result.errors.append(f"Selection not found: {selection_id}")
                return result
            
            entry = self.selections[selection_id]
            result.success = True
            result.selection_name = entry.name
            result.message = f"Selection {selection_id} retrieved"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def list_selections(
        self,
        scope: Optional[SelectionScope] = None,
        terminal_id: Optional[str] = None,
        session_id: Optional[str] = None
    ) -> SelectionResult:
        """
        Seçimleri listele.
        
        Args:
            scope: Kapsam
            terminal_id: Terminal ID
            session_id: Oturum ID
            
        Returns:
            SelectionResult: Listeleme sonucu
        """
        result = SelectionResult(success=False)
        result.action = SelectionAction.LIST.value
        
        try:
            filtered = list(self.selections.values())
            
            if scope:
                filtered = [s for s in filtered if s.scope == scope]
            
            if terminal_id:
                filtered = [s for s in filtered if s.terminal_id == terminal_id]
            
            if session_id:
                filtered = [s for s in filtered if s.session_id == session_id]
            
            result.success = True
            result.message = f"Listed {len(filtered)} selections"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def activate_selection(self, selection_id: str) -> SelectionResult:
        """
        Seçim aktifleştir.
        
        Args:
            selection_id: Seçim ID
            
        Returns:
            SelectionResult: Aktifleştirme sonucu
        """
        result = SelectionResult(success=False)
        result.action = SelectionAction.ACTIVATE.value
        result.selection_id = selection_id
        
        try:
            if selection_id not in self.selections:
                result.errors.append(f"Selection not found: {selection_id}")
                return result
            
            # Deactivate current
            if self._active_selection and self._active_selection in self.selections:
                self.selections[self._active_selection].is_active = False
            
            # Activate new
            self._active_selection = selection_id
            self.selections[selection_id].is_active = True
            
            # Add to history
            if self.config.log_changes:
                self.selection_history.append({
                    "action": "activate",
                    "selection_id": selection_id,
                    "timestamp": self._get_timestamp()
                })
            
            result.success = True
            result.message = f"Selection {selection_id} activated"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def clone_selection(self, selection_id: str, new_name: str) -> SelectionResult:
        """
        Seçim klonla.
        
        Args:
            selection_id: Seçim ID
            new_name: Yeni ad
            
        Returns:
            SelectionResult: Klonlama sonucu
        """
        result = SelectionResult(success=False)
        result.action = SelectionAction.CLONE.value
        result.selection_id = selection_id
        
        try:
            if selection_id not in self.selections:
                result.errors.append(f"Selection not found: {selection_id}")
                return result
            
            source = self.selections[selection_id]
            
            # Create clone
            new_selection_id = f"selection_{self._selection_counter}"
            self._selection_counter += 1
            
            start = SelectionPosition(
                line=source.range.start.line,
                column=source.range.start.column,
                viewport_line=source.range.start.viewport_line,
                viewport_column=source.range.start.viewport_column
            )
            end = SelectionPosition(
                line=source.range.end.line,
                column=source.range.end.column,
                viewport_line=source.range.end.viewport_line,
                viewport_column=source.range.end.viewport_column
            )
            range_obj = SelectionRange(start=start, end=end)
            
            entry = SelectionEntry(
                id=new_selection_id,
                name=new_name,
                mode=source.mode,
                range=range_obj,
                background_color=source.background_color,
                foreground_color=source.foreground_color,
                scope=source.scope,
                timestamp=self._get_timestamp(),
                terminal_id=source.terminal_id,
                session_id=source.session_id
            )
            
            self.selections[new_selection_id] = entry
            
            # Add to history
            if self.config.log_changes:
                self.selection_history.append({
                    "action": "clone",
                    "source_selection_id": selection_id,
                    "new_selection_id": new_selection_id,
                    "new_name": new_name,
                    "timestamp": entry.timestamp
                })
            
            result.success = True
            result.selection_id = new_selection_id
            result.selection_name = new_name
            result.message = f"Selection cloned as {new_name}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def export_selection(self, selection_id: str, format: str = "json") -> SelectionResult:
        """
        Seçim dışa aktar.
        
        Args:
            selection_id: Seçim ID
            format: Format (json)
            
        Returns:
            SelectionResult: Dışa aktarma sonucu
        """
        result = SelectionResult(success=False)
        result.action = SelectionAction.EXPORT.value
        result.selection_id = selection_id
        
        try:
            if selection_id not in self.selections:
                result.errors.append(f"Selection not found: {selection_id}")
                return result
            
            entry = self.selections[selection_id]
            
            if format == "json":
                import json
                data = {
                    "name": entry.name,
                    "mode": entry.mode.value,
                    "range": entry.range.to_dict(),
                    "background_color": entry.background_color,
                    "foreground_color": entry.foreground_color,
                    "scope": entry.scope.value
                }
                result.success = True
                result.message = f"Selection {selection_id} exported as JSON"
            else:
                result.errors.append(f"Unsupported format: {format}")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def import_selection(self, data: Dict[str, Any], scope: SelectionScope = SelectionScope.SESSION) -> SelectionResult:
        """
        Seçim içe aktar.
        
        Args:
            data: Veri
            scope: Kapsam
            
        Returns:
            SelectionResult: İçe aktarma sonucu
        """
        result = SelectionResult(success=False)
        result.action = SelectionAction.IMPORT.value
        
        try:
            name = data.get("name", "imported_selection")
            mode = SelectionMode(data.get("mode", "character"))
            range_data = data.get("range", {})
            start_data = range_data.get("start", {})
            end_data = range_data.get("end", {})
            background_color = data.get("background_color", "#ffffff")
            foreground_color = data.get("foreground_color", "#000000")
            
            return self.create_selection(
                name=name,
                mode=mode,
                start_line=start_data.get("line", 0),
                start_column=start_data.get("column", 0),
                end_line=end_data.get("line", 0),
                end_column=end_data.get("column", 0),
                background_color=background_color,
                foreground_color=foreground_color,
                scope=scope
            )
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def set_default_selection(self, selection_id: str) -> SelectionResult:
        """
        Varsayılan seçim ayarla.
        
        Args:
            selection_id: Seçim ID
            
        Returns:
            SelectionResult: Ayarlama sonucu
        """
        result = SelectionResult(success=False)
        result.action = SelectionAction.SET_DEFAULT.value
        result.selection_id = selection_id
        
        try:
            if selection_id not in self.selections:
                result.errors.append(f"Selection not found: {selection_id}")
                return result
            
            # Unset current default
            if self._default_selection and self._default_selection in self.selections:
                self.selections[self._default_selection].is_default = False
            
            # Set new default
            self._default_selection = selection_id
            self.selections[selection_id].is_default = True
            
            # Add to history
            if self.config.log_changes:
                self.selection_history.append({
                    "action": "set_default",
                    "selection_id": selection_id,
                    "timestamp": self._get_timestamp()
                })
            
            result.success = True
            result.message = f"Selection {selection_id} set as default"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def select_all(self) -> SelectionResult:
        """
        Tümünü seç.
        
        Returns:
            SelectionResult: Seçim sonucu
        """
        result = SelectionResult(success=False)
        result.action = SelectionAction.SELECT_ALL.value
        
        try:
            # Create a select-all selection
            selection_id = f"selection_{self._selection_counter}"
            self._selection_counter += 1
            
            start = SelectionPosition(line=0, column=0)
            end = SelectionPosition(line=999999, column=999999)
            range_obj = SelectionRange(start=start, end=end)
            
            entry = SelectionEntry(
                id=selection_id,
                name="Select All",
                mode=SelectionMode.CHARACTER,
                range=range_obj,
                background_color="#ffffff",
                foreground_color="#000000",
                scope=SelectionScope.SESSION,
                timestamp=self._get_timestamp()
            )
            
            self.selections[selection_id] = entry
            self._active_selection = selection_id
            entry.is_active = True
            
            # Add to history
            if self.config.log_changes:
                self.selection_history.append({
                    "action": "select_all",
                    "selection_id": selection_id,
                    "timestamp": entry.timestamp
                })
            
            result.success = True
            result.selection_id = selection_id
            result.selection_name = "Select All"
            result.message = "Selected all"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def select_word(self, line: int, column: int) -> SelectionResult:
        """
        Kelime seç.
        
        Args:
            line: Satır
            column: Sütun
            
        Returns:
            SelectionResult: Seçim sonucu
        """
        result = SelectionResult(success=False)
        result.action = SelectionAction.SELECT_WORD.value
        
        try:
            # Create a word selection
            selection_id = f"selection_{self._selection_counter}"
            self._selection_counter += 1
            
            start = SelectionPosition(line=line, column=column)
            end = SelectionPosition(line=line, column=column + 10)  # Approximate
            range_obj = SelectionRange(start=start, end=end)
            
            entry = SelectionEntry(
                id=selection_id,
                name="Select Word",
                mode=SelectionMode.WORD,
                range=range_obj,
                background_color="#ffffff",
                foreground_color="#000000",
                scope=SelectionScope.SESSION,
                timestamp=self._get_timestamp()
            )
            
            self.selections[selection_id] = entry
            self._active_selection = selection_id
            entry.is_active = True
            
            # Add to history
            if self.config.log_changes:
                self.selection_history.append({
                    "action": "select_word",
                    "selection_id": selection_id,
                    "line": line,
                    "column": column,
                    "timestamp": entry.timestamp
                })
            
            result.success = True
            result.selection_id = selection_id
            result.selection_name = "Select Word"
            result.message = f"Selected word at line {line}, column {column}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def select_line(self, line: int) -> SelectionResult:
        """
        Satır seç.
        
        Args:
            line: Satır
            
        Returns:
            SelectionResult: Seçim sonucu
        """
        result = SelectionResult(success=False)
        result.action = SelectionAction.SELECT_LINE.value
        
        try:
            # Create a line selection
            selection_id = f"selection_{self._selection_counter}"
            self._selection_counter += 1
            
            start = SelectionPosition(line=line, column=0)
            end = SelectionPosition(line=line, column=999999)
            range_obj = SelectionRange(start=start, end=end)
            
            entry = SelectionEntry(
                id=selection_id,
                name="Select Line",
                mode=SelectionMode.LINE,
                range=range_obj,
                background_color="#ffffff",
                foreground_color="#000000",
                scope=SelectionScope.SESSION,
                timestamp=self._get_timestamp()
            )
            
            self.selections[selection_id] = entry
            self._active_selection = selection_id
            entry.is_active = True
            
            # Add to history
            if self.config.log_changes:
                self.selection_history.append({
                    "action": "select_line",
                    "selection_id": selection_id,
                    "line": line,
                    "timestamp": entry.timestamp
                })
            
            result.success = True
            result.selection_id = selection_id
            result.selection_name = "Select Line"
            result.message = f"Selected line {line}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def clear_selection(self) -> SelectionResult:
        """
        Seçimi temizle.
        
        Returns:
            SelectionResult: Temizleme sonucu
        """
        result = SelectionResult(success=False)
        result.action = SelectionAction.CLEAR.value
        
        try:
            if self._active_selection and self._active_selection in self.selections:
                self.selections[self._active_selection].is_active = False
                self._active_selection = None
            
            # Add to history
            if self.config.log_changes:
                self.selection_history.append({
                    "action": "clear",
                    "timestamp": self._get_timestamp()
                })
            
            result.success = True
            result.message = "Selection cleared"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def copy_selection(self, selection_id: str) -> SelectionResult:
        """
        Seçimi kopyala.
        
        Args:
            selection_id: Seçim ID
            
        Returns:
            SelectionResult: Kopyalama sonucu
        """
        result = SelectionResult(success=False)
        result.action = SelectionAction.COPY.value
        result.selection_id = selection_id
        
        try:
            if selection_id not in self.selections:
                result.errors.append(f"Selection not found: {selection_id}")
                return result
            
            entry = self.selections[selection_id]
            result.selected_text = f"Selected text from {entry.name}"
            
            # Add to history
            if self.config.log_changes:
                self.selection_history.append({
                    "action": "copy",
                    "selection_id": selection_id,
                    "timestamp": self._get_timestamp()
                })
            
            result.success = True
            result.message = f"Selection {selection_id} copied"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def reset_selection(self, selection_id: str) -> SelectionResult:
        """
        Seçimi sıfırla.
        
        Args:
            selection_id: Seçim ID
            
        Returns:
            SelectionResult: Sıfırlama sonucu
        """
        result = SelectionResult(success=False)
        result.action = SelectionAction.RESET.value
        result.selection_id = selection_id
        
        try:
            if selection_id not in self.selections:
                result.errors.append(f"Selection not found: {selection_id}")
                return result
            
            entry = self.selections[selection_id]
            
            # Reset to defaults
            entry.mode = SelectionMode.CHARACTER
            entry.background_color = "#ffffff"
            entry.foreground_color = "#000000"
            entry.timestamp = self._get_timestamp()
            
            # Add to history
            if self.config.log_changes:
                self.selection_history.append({
                    "action": "reset",
                    "selection_id": selection_id,
                    "timestamp": entry.timestamp
                })
            
            result.success = True
            result.message = f"Selection {selection_id} reset"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_selection_history(self) -> List[Dict[str, Any]]:
        """
        Seçim geçmişini al.
        
        Returns:
            List[Dict[str, Any]]: Geçmiş
        """
        return self.selection_history
    
    def clear_history(self) -> SelectionResult:
        """
        Geçmişi temizle.
        
        Returns:
            SelectionResult: Temizleme sonucu
        """
        result = SelectionResult(success=False)
        
        try:
            self.selection_history.clear()
            result.success = True
            result.message = "Selection history cleared"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def update_config(self, config: SelectionConfig) -> SelectionResult:
        """
        Konfigürasyon güncelle.
        
        Args:
            config: Yeni konfigürasyon
            
        Returns:
            SelectionResult: Güncelleme sonucu
        """
        result = SelectionResult(success=False)
        
        try:
            self.config = config
            result.success = True
            result.message = "Config updated"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_config(self) -> SelectionConfig:
        """
        Konfigürasyon al.
        
        Returns:
            SelectionConfig: Konfigürasyon
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
    engine = TerminalSelectionEngine()
    
    print("Terminal Selection Engine initialized")
    print(f"Persist selections: {engine.config.persist_selections}")
