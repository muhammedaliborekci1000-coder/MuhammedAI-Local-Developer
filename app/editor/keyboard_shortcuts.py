"""
MuhammedAI Local Developer - Keyboard Shortcuts
Keyboard shortcuts engine for code editor.
"""

from typing import Dict, Any, Optional, List, Tuple, Callable
from dataclasses import dataclass, field
from enum import Enum


class ModifierKey(Enum):
    """Modifier key."""
    CTRL = "ctrl"
    ALT = "alt"
    SHIFT = "shift"
    META = "meta"
    CMD = "cmd"


class KeyCategory(Enum):
    """Key category."""
    EDITING = "editing"
    NAVIGATION = "navigation"
    SELECTION = "selection"
    VIEW = "view"
    SEARCH = "search"
    TERMINAL = "terminal"
    DEBUG = "debug"
    GIT = "git"
    CUSTOM = "custom"


@dataclass
class KeyBinding:
    """Key binding."""
    key: str
    modifiers: List[ModifierKey] = field(default_factory=list)
    action: str = ""
    description: str = ""
    category: KeyCategory = KeyCategory.EDITING
    when: str = ""  # Context condition
    is_builtin: bool = False


@dataclass
class ShortcutConflict:
    """Shortcut conflict."""
    existing_binding: KeyBinding
    new_binding: KeyBinding
    conflict_type: str = "duplicate"


@dataclass
class KeyBindingResult:
    """Key binding result."""
    success: bool
    action: Optional[str] = None
    binding: Optional[KeyBinding] = None
    conflicts: List[ShortcutConflict] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    message: Optional[str] = None


class KeyboardShortcutsEngine:
    """
    Keyboard shortcuts engine.
    
    Özellikler:
    - Key binding registration
    - Key binding lookup
    - Shortcut conflict detection
    - Custom shortcuts
    - Builtin shortcuts
    - Category filtering
    - Context-aware shortcuts
    - Shortcut validation
    - Shortcut export/import
    - Key combination parsing
    - Modifier key handling
    """
    
    def __init__(self):
        """Initialize keyboard shortcuts engine."""
        self.key_bindings: Dict[str, KeyBinding] = {}
        self._init_builtin_shortcuts()
    
    def _init_builtin_shortcuts(self):
        """Initialize builtin shortcuts."""
        # Editing shortcuts
        editing_shortcuts = [
            KeyBinding(key="s", modifiers=[ModifierKey.CTRL], action="save", description="Save file", category=KeyCategory.EDITING, is_builtin=True),
            KeyBinding(key="z", modifiers=[ModifierKey.CTRL], action="undo", description="Undo", category=KeyCategory.EDITING, is_builtin=True),
            KeyBinding(key="y", modifiers=[ModifierKey.CTRL], action="redo", description="Redo", category=KeyCategory.EDITING, is_builtin=True),
            KeyBinding(key="x", modifiers=[ModifierKey.CTRL], action="cut", description="Cut", category=KeyCategory.EDITING, is_builtin=True),
            KeyBinding(key="c", modifiers=[ModifierKey.CTRL], action="copy", description="Copy", category=KeyCategory.EDITING, is_builtin=True),
            KeyBinding(key="v", modifiers=[ModifierKey.CTRL], action="paste", description="Paste", category=KeyCategory.EDITING, is_builtin=True),
            KeyBinding(key="a", modifiers=[ModifierKey.CTRL], action="select_all", description="Select all", category=KeyCategory.EDITING, is_builtin=True),
            KeyBinding(key="f", modifiers=[ModifierKey.CTRL], action="find", description="Find", category=KeyCategory.EDITING, is_builtin=True),
            KeyBinding(key="h", modifiers=[ModifierKey.CTRL], action="replace", description="Find and replace", category=KeyCategory.EDITING, is_builtin=True),
            KeyBinding(key="d", modifiers=[ModifierKey.CTRL], action="duplicate_line", description="Duplicate line", category=KeyCategory.EDITING, is_builtin=True),
            KeyBinding(key="k", modifiers=[ModifierKey.CTRL], action="delete_line", description="Delete line", category=KeyCategory.EDITING, is_builtin=True),
            KeyBinding(key=";", modifiers=[ModifierKey.CTRL], action="toggle_comment", description="Toggle comment", category=KeyCategory.EDITING, is_builtin=True),
            KeyBinding(key="i", modifiers=[ModifierKey.CTRL, ModifierKey.SHIFT], action="format_document", description="Format document", category=KeyCategory.EDITING, is_builtin=True),
            KeyBinding(key="/", modifiers=[ModifierKey.CTRL], action="toggle_line_comment", description="Toggle line comment", category=KeyCategory.EDITING, is_builtin=True),
            KeyBinding(key="]", modifiers=[ModifierKey.CTRL], action="indent", description="Indent", category=KeyCategory.EDITING, is_builtin=True),
            KeyBinding(key="[", modifiers=[ModifierKey.CTRL], action="outdent", description="Outdent", category=KeyCategory.EDITING, is_builtin=True),
        ]
        
        # Navigation shortcuts
        navigation_shortcuts = [
            KeyBinding(key="left", modifiers=[], action="move_left", description="Move cursor left", category=KeyCategory.NAVIGATION, is_builtin=True),
            KeyBinding(key="right", modifiers=[], action="move_right", description="Move cursor right", category=KeyCategory.NAVIGATION, is_builtin=True),
            KeyBinding(key="up", modifiers=[], action="move_up", description="Move cursor up", category=KeyCategory.NAVIGATION, is_builtin=True),
            KeyBinding(key="down", modifiers=[], action="move_down", description="Move cursor down", category=KeyCategory.NAVIGATION, is_builtin=True),
            KeyBinding(key="home", modifiers=[], action="move_to_line_start", description="Move to line start", category=KeyCategory.NAVIGATION, is_builtin=True),
            KeyBinding(key="end", modifiers=[], action="move_to_line_end", description="Move to line end", category=KeyCategory.NAVIGATION, is_builtin=True),
            KeyBinding(key="pageup", modifiers=[], action="page_up", description="Page up", category=KeyCategory.NAVIGATION, is_builtin=True),
            KeyBinding(key="pagedown", modifiers=[], action="page_down", description="Page down", category=KeyCategory.NAVIGATION, is_builtin=True),
            KeyBinding(key="g", modifiers=[ModifierKey.CTRL], action="go_to_line", description="Go to line", category=KeyCategory.NAVIGATION, is_builtin=True),
            KeyBinding(key="p", modifiers=[ModifierKey.CTRL], action="go_to_file", description="Go to file", category=KeyCategory.NAVIGATION, is_builtin=True),
            KeyBinding(key="t", modifiers=[ModifierKey.CTRL], action="go_to_symbol", description="Go to symbol", category=KeyCategory.NAVIGATION, is_builtin=True),
        ]
        
        # Selection shortcuts
        selection_shortcuts = [
            KeyBinding(key="left", modifiers=[ModifierKey.SHIFT], action="select_left", description="Select left", category=KeyCategory.SELECTION, is_builtin=True),
            KeyBinding(key="right", modifiers=[ModifierKey.SHIFT], action="select_right", description="Select right", category=KeyCategory.SELECTION, is_builtin=True),
            KeyBinding(key="up", modifiers=[ModifierKey.SHIFT], action="select_up", description="Select up", category=KeyCategory.SELECTION, is_builtin=True),
            KeyBinding(key="down", modifiers=[ModifierKey.SHIFT], action="select_down", description="Select down", category=KeyCategory.SELECTION, is_builtin=True),
            KeyBinding(key="home", modifiers=[ModifierKey.SHIFT], action="select_to_line_start", description="Select to line start", category=KeyCategory.SELECTION, is_builtin=True),
            KeyBinding(key="end", modifiers=[ModifierKey.SHIFT], action="select_to_line_end", description="Select to line end", category=KeyCategory.SELECTION, is_builtin=True),
            KeyBinding(key="a", modifiers=[ModifierKey.CTRL, ModifierKey.SHIFT], action="expand_selection", description="Expand selection", category=KeyCategory.SELECTION, is_builtin=True),
        ]
        
        # View shortcuts
        view_shortcuts = [
            KeyBinding(key="b", modifiers=[ModifierKey.CTRL], action="toggle_sidebar", description="Toggle sidebar", category=KeyCategory.VIEW, is_builtin=True),
            KeyBinding(key="j", modifiers=[ModifierKey.CTRL], action="toggle_panel", description="Toggle panel", category=KeyCategory.VIEW, is_builtin=True),
            KeyBinding(key="=", modifiers=[ModifierKey.CTRL], action="zoom_in", description="Zoom in", category=KeyCategory.VIEW, is_builtin=True),
            KeyBinding(key="-", modifiers=[ModifierKey.CTRL], action="zoom_out", description="Zoom out", category=KeyCategory.VIEW, is_builtin=True),
            KeyBinding(key="0", modifiers=[ModifierKey.CTRL], action="reset_zoom", description="Reset zoom", category=KeyCategory.VIEW, is_builtin=True),
            KeyBinding(key="w", modifiers=[ModifierKey.CTRL], action="close_tab", description="Close tab", category=KeyCategory.VIEW, is_builtin=True),
            KeyBinding(key="tab", modifiers=[ModifierKey.CTRL], action="next_tab", description="Next tab", category=KeyCategory.VIEW, is_builtin=True),
            KeyBinding(key="tab", modifiers=[ModifierKey.CTRL, ModifierKey.SHIFT], action="previous_tab", description="Previous tab", category=KeyCategory.VIEW, is_builtin=True),
        ]
        
        # Search shortcuts
        search_shortcuts = [
            KeyBinding(key="p", modifiers=[ModifierKey.CTRL, ModifierKey.SHIFT], action="search_files", description="Search files", category=KeyCategory.SEARCH, is_builtin=True),
            KeyBinding(key="f", modifiers=[ModifierKey.CTRL, ModifierKey.SHIFT], action="search_in_files", description="Search in files", category=KeyCategory.SEARCH, is_builtin=True),
        ]
        
        # Terminal shortcuts
        terminal_shortcuts = [
            KeyBinding(key="`", modifiers=[ModifierKey.CTRL], action="toggle_terminal", description="Toggle terminal", category=KeyCategory.TERMINAL, is_builtin=True),
            KeyBinding(key="n", modifiers=[ModifierKey.CTRL, ModifierKey.SHIFT], action="new_terminal", description="New terminal", category=KeyCategory.TERMINAL, is_builtin=True),
        ]
        
        # Debug shortcuts
        debug_shortcuts = [
            KeyBinding(key="f5", modifiers=[], action="start_debugging", description="Start debugging", category=KeyCategory.DEBUG, is_builtin=True),
            KeyBinding(key="f9", modifiers=[], action="toggle_breakpoint", description="Toggle breakpoint", category=KeyCategory.DEBUG, is_builtin=True),
            KeyBinding(key="f10", modifiers=[], action="step_over", description="Step over", category=KeyCategory.DEBUG, is_builtin=True),
            KeyBinding(key="f11", modifiers=[], action="step_into", description="Step into", category=KeyCategory.DEBUG, is_builtin=True),
            KeyBinding(key="shift+f11", modifiers=[ModifierKey.SHIFT], action="step_out", description="Step out", category=KeyCategory.DEBUG, is_builtin=True),
        ]
        
        # Git shortcuts
        git_shortcuts = [
            KeyBinding(key="g", modifiers=[ModifierKey.CTRL, ModifierKey.SHIFT], action="git_commit", description="Git commit", category=KeyCategory.GIT, is_builtin=True),
            KeyBinding(key="p", modifiers=[ModifierKey.CTRL, ModifierKey.SHIFT, ModifierKey.ALT], action="git_push", description="Git push", category=KeyCategory.GIT, is_builtin=True),
            KeyBinding(key="u", modifiers=[ModifierKey.CTRL, ModifierKey.SHIFT, ModifierKey.ALT], action="git_pull", description="Git pull", category=KeyCategory.GIT, is_builtin=True),
        ]
        
        # Register all shortcuts
        for shortcut in editing_shortcuts + navigation_shortcuts + selection_shortcuts + view_shortcuts + search_shortcuts + terminal_shortcuts + debug_shortcuts + git_shortcuts:
            key_combo = self._get_key_combo(shortcut.key, shortcut.modifiers)
            self.key_bindings[key_combo] = shortcut
    
    def _get_key_combo(self, key: str, modifiers: List[ModifierKey]) -> str:
        """Get key combination string."""
        modifier_names = [m.value for m in sorted(modifiers, key=lambda x: x.value)]
        if modifier_names:
            return "+".join(modifier_names + [key])
        return key
    
    def register_binding(self, binding: KeyBinding) -> KeyBindingResult:
        """
        Key binding kaydet.
        
        Args:
            binding: Key binding
            
        Returns:
            KeyBindingResult: Kayıt sonucu
        """
        result = KeyBindingResult(success=False)
        
        try:
            key_combo = self._get_key_combo(binding.key, binding.modifiers)
            
            # Conflict kontrolü
            if key_combo in self.key_bindings:
                existing = self.key_bindings[key_combo]
                if not existing.is_builtin:
                    conflict = ShortcutConflict(
                        existing_binding=existing,
                        new_binding=binding
                    )
                    result.conflicts.append(conflict)
                    result.errors.append(f"Conflict with existing binding: {existing.action}")
                    return result
            
            self.key_bindings[key_combo] = binding
            result.success = True
            result.binding = binding
            result.action = binding.action
            result.message = f"Key binding registered: {key_combo}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_binding(self, key: str, modifiers: List[ModifierKey]) -> Optional[KeyBinding]:
        """
        Key binding al.
        
        Args:
            key: Key
            modifiers: Modifier keys
            
        Returns:
            Optional[KeyBinding]: Key binding
        """
        key_combo = self._get_key_combo(key, modifiers)
        return self.key_bindings.get(key_combo)
    
    def get_binding_by_action(self, action: str) -> Optional[KeyBinding]:
        """
        Action için key binding al.
        
        Args:
            action: Action
            
        Returns:
            Optional[KeyBinding]: Key binding
        """
        for binding in self.key_bindings.values():
            if binding.action == action:
                return binding
        return None
    
    def remove_binding(self, key: str, modifiers: List[ModifierKey]) -> bool:
        """
        Key binding kaldır.
        
        Args:
            key: Key
            modifiers: Modifier keys
            
        Returns:
            bool: Başarı durumu
        """
        try:
            key_combo = self._get_key_combo(key, modifiers)
            if key_combo in self.key_bindings:
                binding = self.key_bindings[key_combo]
                if not binding.is_builtin:
                    del self.key_bindings[key_combo]
                    return True
            return False
        except Exception:
            return False
    
    def get_bindings_by_category(self, category: KeyCategory) -> List[KeyBinding]:
        """
        Kategori için key binding'leri al.
        
        Args:
            category: Kategori
            
        Returns:
            List[KeyBinding]: Key binding listesi
        """
        return [b for b in self.key_bindings.values() if b.category == category]
    
    def get_all_bindings(self) -> List[KeyBinding]:
        """
        Tüm key binding'leri al.
        
        Returns:
            List[KeyBinding]: Key binding listesi
        """
        return list(self.key_bindings.values())
    
    def check_conflicts(self, binding: KeyBinding) -> List[ShortcutConflict]:
        """
        Conflict kontrolü yap.
        
        Args:
            binding: Key binding
            
        Returns:
            List[ShortcutConflict]: Conflict listesi
        """
        conflicts = []
        key_combo = self._get_key_combo(binding.key, binding.modifiers)
        
        if key_combo in self.key_bindings:
            existing = self.key_bindings[key_combo]
            conflict = ShortcutConflict(
                existing_binding=existing,
                new_binding=binding
            )
            conflicts.append(conflict)
        
        return conflicts
    
    def validate_binding(self, binding: KeyBinding) -> Tuple[bool, List[str]]:
        """
        Key binding doğrula.
        
        Args:
            binding: Key binding
            
        Returns:
            Tuple[bool, List[str]]: (valid, errors)
        """
        errors = []
        
        if not binding.key:
            errors.append("Key is required")
        
        if not binding.action:
            errors.append("Action is required")
        
        if not binding.category:
            errors.append("Category is required")
        
        return (len(errors) == 0, errors)
    
    def export_bindings(self) -> Dict[str, Any]:
        """
        Key binding'leri export et.
        
        Returns:
            Dict[str, Any]: Export data
        """
        export_data = {
            "bindings": []
        }
        
        for binding in self.key_bindings.values():
            if not binding.is_builtin:
                binding_data = {
                    "key": binding.key,
                    "modifiers": [m.value for m in binding.modifiers],
                    "action": binding.action,
                    "description": binding.description,
                    "category": binding.category.value,
                    "when": binding.when
                }
                export_data["bindings"].append(binding_data)
        
        return export_data
    
    def import_bindings(self, data: Dict[str, Any]) -> KeyBindingResult:
        """
        Key binding'leri import et.
        
        Args:
            data: Import data
            
        Returns:
            KeyBindingResult: Import sonucu
        """
        result = KeyBindingResult(success=False)
        
        try:
            if "bindings" not in data:
                result.errors.append("Invalid import data")
                return result
            
            imported_count = 0
            for binding_data in data["bindings"]:
                binding = KeyBinding(
                    key=binding_data.get("key", ""),
                    modifiers=[ModifierKey(m) for m in binding_data.get("modifiers", [])],
                    action=binding_data.get("action", ""),
                    description=binding_data.get("description", ""),
                    category=KeyCategory(binding_data.get("category", "custom")),
                    when=binding_data.get("when", ""),
                    is_builtin=False
                )
                
                register_result = self.register_binding(binding)
                if register_result.success:
                    imported_count += 1
            
            result.success = True
            result.message = f"Imported {imported_count} bindings"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def reset_to_defaults(self) -> KeyBindingResult:
        """
        Varsayılanlara sıfırla.
        
        Returns:
            KeyBindingResult: Reset sonucu
        """
        result = KeyBindingResult(success=False)
        
        try:
            # Custom binding'leri kaldır
            custom_bindings = [k for k, v in self.key_bindings.items() if not v.is_builtin]
            for key in custom_bindings:
                del self.key_bindings[key]
            
            result.success = True
            result.message = "Reset to defaults"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_categories(self) -> List[KeyCategory]:
        """
        Kategorileri al.
        
        Returns:
            List[KeyCategory]: Kategori listesi
        """
        categories = set()
        for binding in self.key_bindings.values():
            categories.add(binding.category)
        return list(categories)


if __name__ == "__main__":
    # Basit test
    engine = KeyboardShortcutsEngine()
    
    # Key binding al
    binding = engine.get_binding("s", [ModifierKey.CTRL])
    print(f"Binding: {binding.action if binding else 'None'}")
    
    # Custom binding
    custom = KeyBinding(
        key="q",
        modifiers=[ModifierKey.CTRL],
        action="quit",
        description="Quit",
        category=KeyCategory.CUSTOM
    )
    result = engine.register_binding(custom)
    print(f"Register: {result.success}")
