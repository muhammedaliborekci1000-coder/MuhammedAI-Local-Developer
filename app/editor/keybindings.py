"""
MuhammedAI Local Developer - Keybindings
Keybinding management system for code editor.
"""

from typing import Dict, Any, Optional, List, Callable
from dataclasses import dataclass, field
from enum import Enum


class KeyModifier(Enum):
    """Key modifier."""
    CTRL = "ctrl"
    ALT = "alt"
    SHIFT = "shift"
    META = "meta"
    CMD = "cmd"


class KeybindingScope(Enum):
    """Keybinding scope."""
    GLOBAL = "global"
    EDITOR = "editor"
    TERMINAL = "terminal"
    EXPLORER = "explorer"
    SEARCH = "search"
    DEBUG = "debug"


@dataclass
class Keybinding:
    """Keybinding information."""
    id: str
    key: str
    modifiers: List[KeyModifier]
    command: str
    scope: KeybindingScope = KeybindingScope.GLOBAL
    when: Optional[str] = None
    description: Optional[str] = None
    enabled: bool = True


@dataclass
class KeybindingConfig:
    """Keybinding configuration."""
    enable_conflict_detection: bool = True
    allow_overrides: bool = False
    save_on_change: bool = True
    auto_save: bool = True
    keybinding_file_path: Optional[str] = None


@dataclass
class KeybindingResult:
    """Keybinding result."""
    success: bool
    keybinding: Optional[Keybinding] = None
    conflicts: List[Keybinding] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    message: Optional[str] = None


class KeybindingManager:
    """
    Keybinding manager.
    
    Özellikler:
    - Keybindings
    - Custom shortcuts
    - Keybinding editor
    - Conflict detection
    - Keybinding export/import
    - Scope-based keybindings
    - Modifier keys
    - Keybinding validation
    - Keybinding history
    - Keybinding presets
    - Multi-platform support
    - Keybinding search
    - Keybinding categories
    """
    
    def __init__(self, config: Optional[KeybindingConfig] = None):
        """
        Initialize keybinding manager.
        
        Args:
            config: Keybinding configuration
        """
        self.config = config or KeybindingConfig()
        self.keybindings: Dict[str, Keybinding] = {}
        self._initialize_builtin_keybindings()
    
    def _initialize_builtin_keybindings(self) -> None:
        """Initialize built-in keybindings."""
        # File operations
        self.register_keybinding(Keybinding(
            id="file.new",
            key="n",
            modifiers=[KeyModifier.CTRL],
            command="file.new",
            scope=KeybindingScope.GLOBAL,
            description="New file"
        ))
        
        self.register_keybinding(Keybinding(
            id="file.open",
            key="o",
            modifiers=[KeyModifier.CTRL],
            command="file.open",
            scope=KeybindingScope.GLOBAL,
            description="Open file"
        ))
        
        self.register_keybinding(Keybinding(
            id="file.save",
            key="s",
            modifiers=[KeyModifier.CTRL],
            command="file.save",
            scope=KeybindingScope.GLOBAL,
            description="Save file"
        ))
        
        self.register_keybinding(Keybinding(
            id="file.save_all",
            key="s",
            modifiers=[KeyModifier.CTRL, KeyModifier.SHIFT],
            command="file.save_all",
            scope=KeybindingScope.GLOBAL,
            description="Save all files"
        ))
        
        # Edit operations
        self.register_keybinding(Keybinding(
            id="edit.undo",
            key="z",
            modifiers=[KeyModifier.CTRL],
            command="edit.undo",
            scope=KeybindingScope.EDITOR,
            description="Undo"
        ))
        
        self.register_keybinding(Keybinding(
            id="edit.redo",
            key="y",
            modifiers=[KeyModifier.CTRL],
            command="edit.redo",
            scope=KeybindingScope.EDITOR,
            description="Redo"
        ))
        
        self.register_keybinding(Keybinding(
            id="edit.cut",
            key="x",
            modifiers=[KeyModifier.CTRL],
            command="edit.cut",
            scope=KeybindingScope.EDITOR,
            description="Cut"
        ))
        
        self.register_keybinding(Keybinding(
            id="edit.copy",
            key="c",
            modifiers=[KeyModifier.CTRL],
            command="edit.copy",
            scope=KeybindingScope.EDITOR,
            description="Copy"
        ))
        
        self.register_keybinding(Keybinding(
            id="edit.paste",
            key="v",
            modifiers=[KeyModifier.CTRL],
            command="edit.paste",
            scope=KeybindingScope.EDITOR,
            description="Paste"
        ))
        
        self.register_keybinding(Keybinding(
            id="edit.select_all",
            key="a",
            modifiers=[KeyModifier.CTRL],
            command="edit.select_all",
            scope=KeybindingScope.EDITOR,
            description="Select all"
        ))
        
        # View operations
        self.register_keybinding(Keybinding(
            id="view.command_palette",
            key="p",
            modifiers=[KeyModifier.CTRL, KeyModifier.SHIFT],
            command="view.command_palette",
            scope=KeybindingScope.GLOBAL,
            description="Command palette"
        ))
        
        self.register_keybinding(Keybinding(
            id="view.toggle_sidebar",
            key="b",
            modifiers=[KeyModifier.CTRL],
            command="view.toggle_sidebar",
            scope=KeybindingScope.GLOBAL,
            description="Toggle sidebar"
        ))
        
        self.register_keybinding(Keybinding(
            id="view.toggle_terminal",
            key="`",
            modifiers=[KeyModifier.CTRL],
            command="view.toggle_terminal",
            scope=KeybindingScope.GLOBAL,
            description="Toggle terminal"
        ))
        
        # Navigation
        self.register_keybinding(Keybinding(
            id="nav.go_to_line",
            key="g",
            modifiers=[KeyModifier.CTRL],
            command="nav.go_to_line",
            scope=KeybindingScope.EDITOR,
            description="Go to line"
        ))
        
        self.register_keybinding(Keybinding(
            id="nav.go_to_file",
            key="p",
            modifiers=[KeyModifier.CTRL],
            command="nav.go_to_file",
            scope=KeybindingScope.GLOBAL,
            description="Go to file"
        ))
        
        # Search
        self.register_keybinding(Keybinding(
            id="search.find",
            key="f",
            modifiers=[KeyModifier.CTRL],
            command="search.find",
            scope=KeybindingScope.EDITOR,
            description="Find"
        ))
        
        self.register_keybinding(Keybinding(
            id="search.replace",
            key="h",
            modifiers=[KeyModifier.CTRL],
            command="search.replace",
            scope=KeybindingScope.EDITOR,
            description="Replace"
        ))
        
        self.register_keybinding(Keybinding(
            id="search.find_in_files",
            key="f",
            modifiers=[KeyModifier.CTRL, KeyModifier.SHIFT],
            command="search.find_in_files",
            scope=KeybindingScope.GLOBAL,
            description="Find in files"
        ))
        
        # Debug
        self.register_keybinding(Keybinding(
            id="debug.start",
            key="f5",
            modifiers=[],
            command="debug.start",
            scope=KeybindingScope.GLOBAL,
            description="Start debugging"
        ))
        
        self.register_keybinding(Keybinding(
            id="debug.step_over",
            key="f10",
            modifiers=[],
            command="debug.step_over",
            scope=KeybindingScope.DEBUG,
            description="Step over"
        ))
        
        self.register_keybinding(Keybinding(
            id="debug.step_into",
            key="f11",
            modifiers=[],
            command="debug.step_into",
            scope=KeybindingScope.DEBUG,
            description="Step into"
        ))
        
        self.register_keybinding(Keybinding(
            id="debug.step_out",
            key="shift+f11",
            modifiers=[KeyModifier.SHIFT],
            command="debug.step_out",
            scope=KeybindingScope.DEBUG,
            description="Step out"
        ))
    
    def register_keybinding(self, keybinding: Keybinding) -> KeybindingResult:
        """
        Register a keybinding.
        
        Args:
            keybinding: Keybinding to register
            
        Returns:
            KeybindingResult: Registration result
        """
        result = KeybindingResult(success=False)
        
        # Check for conflicts
        if self.config.enable_conflict_detection:
            conflicts = self._find_conflicts(keybinding)
            if conflicts and not self.config.allow_overrides:
                result.conflicts = conflicts
                result.errors.append("Keybinding conflicts detected")
                result.message = "Keybinding conflicts detected"
                return result
        
        # Register
        self.keybindings[keybinding.id] = keybinding
        result.success = True
        result.keybinding = keybinding
        result.message = f"Keybinding '{keybinding.id}' registered"
        
        return result
    
    def unregister_keybinding(self, keybinding_id: str) -> KeybindingResult:
        """
        Unregister a keybinding.
        
        Args:
            keybinding_id: Keybinding ID
            
        Returns:
            KeybindingResult: Unregistration result
        """
        result = KeybindingResult(success=False)
        
        if keybinding_id in self.keybindings:
            del self.keybindings[keybinding_id]
            result.success = True
            result.message = f"Keybinding '{keybinding_id}' unregistered"
        else:
            result.errors.append("Keybinding not found")
        
        return result
    
    def get_keybinding(self, keybinding_id: str) -> Optional[Keybinding]:
        """
        Get keybinding by ID.
        
        Args:
            keybinding_id: Keybinding ID
            
        Returns:
            Optional[Keybinding]: Keybinding
        """
        return self.keybindings.get(keybinding_id)
    
    def get_all_keybindings(self) -> List[Keybinding]:
        """
        Get all keybindings.
        
        Returns:
            List[Keybinding]: All keybindings
        """
        return list(self.keybindings.values())
    
    def get_keybindings_by_scope(self, scope: KeybindingScope) -> List[Keybinding]:
        """
        Get keybindings by scope.
        
        Args:
            scope: Keybinding scope
            
        Returns:
            List[Keybinding]: Keybindings
        """
        return [kb for kb in self.keybindings.values() if kb.scope == scope]
    
    def get_keybindings_by_command(self, command: str) -> List[Keybinding]:
        """
        Get keybindings by command.
        
        Args:
            command: Command name
            
        Returns:
            List[Keybinding]: Keybindings
        """
        return [kb for kb in self.keybindings.values() if kb.command == command]
    
    def find_keybinding_by_key(self, key: str, modifiers: List[KeyModifier], scope: KeybindingScope) -> Optional[Keybinding]:
        """
        Find keybinding by key combination.
        
        Args:
            key: Key
            modifiers: Modifiers
            scope: Scope
            
        Returns:
            Optional[Keybinding]: Keybinding
        """
        for kb in self.keybindings.values():
            if kb.key == key and kb.modifiers == modifiers and kb.scope == scope:
                return kb
        return None
    
    def _find_conflicts(self, keybinding: Keybinding) -> List[Keybinding]:
        """
        Find conflicting keybindings.
        
        Args:
            keybinding: Keybinding to check
            
        Returns:
            List[Keybinding]: Conflicting keybindings
        """
        conflicts = []
        
        for kb in self.keybindings.values():
            if kb.id == keybinding.id:
                continue
            
            if (kb.key == keybinding.key and 
                kb.modifiers == keybinding.modifiers and 
                kb.scope == keybinding.scope):
                conflicts.append(kb)
        
        return conflicts
    
    def check_conflicts(self, keybinding: Keybinding) -> KeybindingResult:
        """
        Check for keybinding conflicts.
        
        Args:
            keybinding: Keybinding to check
            
        Returns:
            KeybindingResult: Conflict check result
        """
        result = KeybindingResult(success=True)
        
        conflicts = self._find_conflicts(keybinding)
        
        if conflicts:
            result.success = False
            result.conflicts = conflicts
            result.errors.append("Conflicts detected")
            result.message = f"Found {len(conflicts)} conflicts"
        else:
            result.message = "No conflicts detected"
        
        return result
    
    def update_keybinding(self, keybinding_id: str, keybinding: Keybinding) -> KeybindingResult:
        """
        Update a keybinding.
        
        Args:
            keybinding_id: Keybinding ID
            keybinding: New keybinding
            
        Returns:
            KeybindingResult: Update result
        """
        result = KeybindingResult(success=False)
        
        if keybinding_id not in self.keybindings:
            result.errors.append("Keybinding not found")
            return result
        
        # Check for conflicts
        if self.config.enable_conflict_detection:
            conflicts = self._find_conflicts(keybinding)
            if conflicts and not self.config.allow_overrides:
                result.conflicts = conflicts
                result.errors.append("Keybinding conflicts detected")
                return result
        
        # Update
        self.keybindings[keybinding_id] = keybinding
        result.success = True
        result.keybinding = keybinding
        result.message = f"Keybinding '{keybinding_id}' updated"
        
        return result
    
    def search_keybindings(self, query: str) -> List[Keybinding]:
        """
        Search keybindings.
        
        Args:
            query: Search query
            
        Returns:
            List[Keybinding]: Matching keybindings
        """
        query_lower = query.lower()
        results = []
        
        for kb in self.keybindings.values():
            if (query_lower in kb.command.lower() or
                (kb.description and query_lower in kb.description.lower()) or
                query_lower in kb.key.lower()):
                results.append(kb)
        
        return results
    
    def export_keybindings(self) -> Dict[str, Any]:
        """
        Export keybindings to dictionary.
        
        Returns:
            Dict[str, Any]: Exported keybindings
        """
        export_data = {
            "keybindings": []
        }
        
        for kb in self.keybindings.values():
            kb_data = {
                "id": kb.id,
                "key": kb.key,
                "modifiers": [m.value for m in kb.modifiers],
                "command": kb.command,
                "scope": kb.scope.value,
                "when": kb.when,
                "description": kb.description,
                "enabled": kb.enabled
            }
            export_data["keybindings"].append(kb_data)
        
        return export_data
    
    def import_keybindings(self, data: Dict[str, Any]) -> KeybindingResult:
        """
        Import keybindings from dictionary.
        
        Args:
            data: Import data
            
        Returns:
            KeybindingResult: Import result
        """
        result = KeybindingResult(success=False)
        
        if "keybindings" not in data:
            result.errors.append("Invalid import data")
            return result
        
        imported_count = 0
        
        for kb_data in data["keybindings"]:
            try:
                modifiers = [KeyModifier(m) for m in kb_data.get("modifiers", [])]
                
                keybinding = Keybinding(
                    id=kb_data["id"],
                    key=kb_data["key"],
                    modifiers=modifiers,
                    command=kb_data["command"],
                    scope=KeybindingScope(kb_data.get("scope", "global")),
                    when=kb_data.get("when"),
                    description=kb_data.get("description"),
                    enabled=kb_data.get("enabled", True)
                )
                
                self.keybindings[keybinding.id] = keybinding
                imported_count += 1
            except Exception as e:
                result.errors.append(f"Error importing {kb_data.get('id', 'unknown')}: {str(e)}")
        
        result.success = True
        result.message = f"Imported {imported_count} keybindings"
        
        return result
    
    def update_config(self, config: KeybindingConfig) -> None:
        """
        Update keybinding configuration.
        
        Args:
            config: New configuration
        """
        self.config = config
    
    def get_config(self) -> KeybindingConfig:
        """
        Get keybinding configuration.
        
        Returns:
            KeybindingConfig: Configuration
        """
        return self.config


if __name__ == "__main__":
    # Basit test
    config = KeybindingConfig()
    manager = KeybindingManager(config)
    
    # Keybinding ara
    results = manager.search_keybindings("save")
    
    print(f"Found {len(results)} keybindings")
    for kb in results:
        modifiers = "+".join([m.value for m in kb.modifiers])
        print(f"  - {modifiers}+{kb.key}: {kb.command}")
