"""
MuhammedAI Local Developer - Terminal Focus
Terminal focus management engine for code editor.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime


class FocusMode(Enum):
    """Focus mode."""
    SINGLE = "single"
    MULTI = "multi"
    AUTO = "auto"


class FocusScope(Enum):
    """Focus scope."""
    TERMINAL = "terminal"
    PANEL = "panel"
    SESSION = "session"


class FocusAction(Enum):
    """Focus action."""
    FOCUS = "focus"
    UNFOCUS = "unfocus"
    TOGGLE = "toggle"
    NEXT = "next"
    PREVIOUS = "previous"


@dataclass
class FocusConfig:
    """Focus configuration."""
    auto_focus_on_create: bool = True
    auto_focus_on_click: bool = True
    focus_on_command: bool = True
    show_focus_indicator: bool = True
    show_notifications: bool = True
    log_focus_changes: bool = True


@dataclass
class FocusEntry:
    """Focus entry."""
    id: str
    terminal_id: str
    panel_id: Optional[str] = None
    session_id: Optional[str] = None
    timestamp: str = ""
    is_focused: bool = False


@dataclass
class FocusResult:
    """Focus result."""
    success: bool
    message: Optional[str] = None
    errors: List[str] = field(default_factory=list)
    focused_terminal_id: Optional[str] = None
    previous_terminal_id: Optional[str] = None
    action: Optional[str] = None


class TerminalFocusEngine:
    """
    Terminal focus management engine.
    
    Özellikler:
    - Focus terminal
    - Unfocus terminal
    - Toggle focus
    - Focus next
    - Focus previous
    - Get focused terminal
    - Get all terminals
    - Focus history
    - Focus indicators
    - Auto focus
    - Focus validation
    """
    
    def __init__(self, config: Optional[FocusConfig] = None):
        """Initialize terminal focus engine."""
        self.config = config or FocusConfig()
        self.focused_terminal: Optional[str] = None
        self.terminals: Dict[str, FocusEntry] = {}
        self.focus_history: List[Dict[str, Any]] = []
        self._entry_counter = 0
    
    def focus_terminal(
        self,
        terminal_id: str,
        panel_id: Optional[str] = None,
        session_id: Optional[str] = None
    ) -> FocusResult:
        """
- Terminate odakla.
        
        Args:
            terminal_id: Terminal ID
            panel_id: Panel ID
            session_id: Oturum ID
            
        Returns:
            FocusResult: Odaklama sonucu
        """
        result = FocusResult(success=False)
        result.action = FocusAction.FOCUS.value
        
        try:
            previous_terminal_id = self.focused_terminal
            
            # Unfocus previous
            if previous_terminal_id and previous_terminal_id in self.terminals:
                self.terminals[previous_terminal_id].is_focused = False
            
            # Create or update entry
            if terminal_id not in self.terminals:
                entry = FocusEntry(
                    id=f"focus_{self._entry_counter}",
                    terminal_id=terminal_id,
                    panel_id=panel_id,
                    session_id=session_id,
                    timestamp=self._get_timestamp(),
                    is_focused=True
                )
                self._entry_counter += 1
                self.terminals[terminal_id] = entry
            else:
                self.terminals[terminal_id].is_focused = True
                self.terminals[terminal_id].timestamp = self._get_timestamp()
            
            # Set as focused
            self.focused_terminal = terminal_id
            
            # Add to history
            if self.config.log_focus_changes:
                self.focus_history.append({
                    "action": "focus",
                    "terminal_id": terminal_id,
                    "previous_terminal_id": previous_terminal_id,
                    "timestamp": self._get_timestamp()
                })
            
            result.success = True
            result.focused_terminal_id = terminal_id
            result.previous_terminal_id = previous_terminal_id
            result.message = f"Focused terminal {terminal_id}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def unfocus_terminal(self, terminal_id: str) -> FocusResult:
        """
        Terminalden odak kaldır.
        
        Args:
            terminal_id: Terminal ID
            
        Returns:
            FocusResult: Odak kaldırma sonucu
        """
        result = FocusResult(success=False)
        result.action = FocusAction.UNFOCUS.value
        
        try:
            if terminal_id not in self.terminals:
                result.errors.append(f"Terminal not found: {terminal_id}")
                return result
            
            self.terminals[terminal_id].is_focused = False
            
            if self.focused_terminal == terminal_id:
                self.focused_terminal = None
            
            # Add to history
            if self.config.log_focus_changes:
                self.focus_history.append({
                    "action": "unfocus",
                    "terminal_id": terminal_id,
                    "timestamp": self._get_timestamp()
                })
            
            result.success = True
            result.message = f"Unfocused terminal {terminal_id}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def toggle_focus(self, terminal_id: str) -> FocusResult:
        """
        Odak değiştir.
        
        Args:
            terminal_id: Terminal ID
            
        Returns:
            FocusResult: Odak değiştirme sonucu
        """
        result = FocusResult(success=False)
        result.action = FocusAction.TOGGLE.value
        
        try:
            if terminal_id not in self.terminals:
                result.errors.append(f"Terminal not found: {terminal_id}")
                return result
            
            entry = self.terminals[terminal_id]
            
            if entry.is_focused:
                return self.unfocus_terminal(terminal_id)
            else:
                return self.focus_terminal(terminal_id)
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def focus_next(self) -> FocusResult:
        """
        Sonrakine odakla.
        
        Returns:
            FocusResult: Odaklama sonucu
        """
        result = FocusResult(success=False)
        result.action = FocusAction.NEXT.value
        
        try:
            terminal_ids = list(self.terminals.keys())
            
            if not terminal_ids:
                result.errors.append("No terminals available")
                return result
            
            if self.focused_terminal is None:
                # Focus first
                return self.focus_terminal(terminal_ids[0])
            
            current_index = terminal_ids.index(self.focused_terminal)
            next_index = (current_index + 1) % len(terminal_ids)
            next_terminal_id = terminal_ids[next_index]
            
            return self.focus_terminal(next_terminal_id)
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def focus_previous(self) -> FocusResult:
        """
        Öncekine odakla.
        
        Returns:
            FocusResult: Odaklama sonucu
        """
        result = FocusResult(success=False)
        result.action = FocusAction.PREVIOUS.value
        
        try:
            terminal_ids = list(self.terminals.keys())
            
            if not terminal_ids:
                result.errors.append("No terminals available")
                return result
            
            if self.focused_terminal is None:
                # Focus last
                return self.focus_terminal(terminal_ids[-1])
            
            current_index = terminal_ids.index(self.focused_terminal)
            prev_index = (current_index - 1) % len(terminal_ids)
            prev_terminal_id = terminal_ids[prev_index]
            
            return self.focus_terminal(prev_terminal_id)
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_focused_terminal(self) -> Optional[FocusEntry]:
        """
        Odaklı terminali al.
        
        Returns:
            Optional[FocusEntry]: Odaklı terminal
        """
        if self.focused_terminal and self.focused_terminal in self.terminals:
            return self.terminals[self.focused_terminal]
        return None
    
    def get_all_terminals(self) -> List[FocusEntry]:
        """
        Tüm terminalleri al.
        
        Returns:
            List[FocusEntry]: Terminal listesi
        """
        return list(self.terminals.values())
    
    def get_terminal(self, terminal_id: str) -> Optional[FocusEntry]:
        """
        Terminal al.
        
        Args:
            terminal_id: Terminal ID
            
        Returns:
            Optional[FocusEntry]: Terminal
        """
        return self.terminals.get(terminal_id)
    
    def get_focus_history(self) -> List[Dict[str, Any]]:
        """
        Odak geçmişini al.
        
        Returns:
            List[Dict[str, Any]]: Geçmiş
        """
        return self.focus_history
    
    def clear_history(self) -> FocusResult:
        """
        Geçmişi temizle.
        
        Returns:
            FocusResult: Temizleme sonucu
        """
        result = FocusResult(success=False)
        
        try:
            self.focus_history.clear()
            result.success = True
            result.message = "Focus history cleared"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def update_config(self, config: FocusConfig) -> FocusResult:
        """
        Konfigürasyon güncelle.
        
        Args:
            config: Yeni konfigürasyon
            
        Returns:
            FocusResult: Güncelleme sonucu
        """
        result = FocusResult(success=False)
        
        try:
            self.config = config
            result.success = True
            result.message = "Config updated"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_config(self) -> FocusConfig:
        """
        Konfigürasyon al.
        
        Returns:
            FocusConfig: Konfigürasyon
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
    engine = TerminalFocusEngine()
    
    print("Terminal Focus Engine initialized")
    print(f"Auto focus on create: {engine.config.auto_focus_on_create}")
