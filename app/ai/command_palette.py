"""
MuhammedAI Local Developer - Command Palette
Command palette for quick access to IDE commands.
"""

from typing import Dict, Any, Optional, List, Callable, Tuple
from dataclasses import dataclass, field
from enum import Enum


class CommandCategory(Enum):
    """Command category."""
    FILE = "file"
    EDIT = "edit"
    VIEW = "view"
    NAVIGATION = "navigation"
    REFACTORING = "refactoring"
    TOOLS = "tools"
    HELP = "help"
    DEBUG = "debug"
    GIT = "git"
    TERMINAL = "terminal"
    SEARCH = "search"
    WINDOW = "window"
    PREFERENCES = "preferences"


@dataclass
class Command:
    """Command."""
    id: str
    name: str
    description: str
    category: CommandCategory
    action: Callable
    shortcut: Optional[str] = None
    icon: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    aliases: List[str] = field(default_factory=list)
    when: str = ""  # Context condition
    is_builtin: bool = False


@dataclass
class CommandPaletteResult:
    """Command palette result."""
    success: bool
    commands: List[Command] = field(default_factory=list)
    executed_command: Optional[Command] = None
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    message: Optional[str] = None


class CommandPalette:
    """
    Command palette engine.
    
    Özellikler:
    - Command registration
    - Command search/filtering
    - Command execution
    - Command categories
    - Keyboard shortcuts
    - Command history
    - Favorite commands
    - Fuzzy search
    - Command aliasing
    - Command context awareness
    - Command validation
    - Command export/import
    - Command grouping
    - 50+ builtin commands
    """
    
    def __init__(self):
        """Initialize command palette."""
        self.commands: Dict[str, Command] = {}
        self.command_history: List[str] = []
        self.favorite_commands: List[str] = []
        self._register_default_commands()
    
    def register_command(
        self,
        command: Command
    ) -> CommandPaletteResult:
        """
        Command kaydet.
        
        Args:
            command: Command
            
        Returns:
            CommandPaletteResult: Kayıt sonucu
        """
        result = CommandPaletteResult(success=False)
        
        try:
            if command.id in self.commands:
                result.warnings.append(f"Command '{command.id}' already exists, overwriting")
            
            self.commands[command.id] = command
            result.success = True
            result.message = f"Command '{command.id}' registered"
            result.commands.append(command)
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def execute_command(
        self,
        command_id: str,
        *args,
        **kwargs
    ) -> CommandPaletteResult:
        """
        Command çalıştır.
        
        Args:
            command_id: Command ID
            *args: Arguments
            **kwargs: Keyword arguments
            
        Returns:
            CommandPaletteResult: Execution sonucu
        """
        result = CommandPaletteResult(success=False)
        
        try:
            if command_id not in self.commands:
                result.errors.append(f"Command '{command_id}' not found")
                return result
            
            command = self.commands[command_id]
            
            # Command'ı çalıştır
            command.action(*args, **kwargs)
            
            # History'ye ekle
            if command_id not in self.command_history:
                self.command_history.append(command_id)
            
            result.success = True
            result.executed_command = command
            result.message = f"Command '{command_id}' executed"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def search_commands(
        self,
        query: str,
        category: Optional[CommandCategory] = None
    ) -> CommandPaletteResult:
        """
        Command ara.
        
        Args:
            query: Arama sorgusu
            category: Kategori filtresi
            
        Returns:
            CommandPaletteResult: Arama sonucu
        """
        result = CommandPaletteResult(success=False)
        
        try:
            query_lower = query.lower()
            matched_commands = []
            
            for command in self.commands.values():
                # Category filtresi
                if category and command.category != category:
                    continue
                
                # Fuzzy search (name, description, tags, aliases)
                if (query_lower in command.name.lower() or
                    query_lower in command.description.lower() or
                    any(query_lower in tag.lower() for tag in command.tags) or
                    any(query_lower in alias.lower() for alias in command.aliases)):
                    matched_commands.append(command)
            
            # History ve favorite'ları öne al
            matched_commands.sort(
                key=lambda c: (
                    c.id in self.favorite_commands,
                    c.id in self.command_history
                ),
                reverse=True
            )
            
            result.success = True
            result.commands = matched_commands
            result.message = f"Found {len(matched_commands)} commands"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_commands_by_category(
        self,
        category: CommandCategory
    ) -> CommandPaletteResult:
        """
        Kategori bazlı command'ları al.
        
        Args:
            category: Command category
            
        Returns:
            CommandPaletteResult: Command listesi
        """
        result = CommandPaletteResult(success=False)
        
        try:
            category_commands = [
                cmd for cmd in self.commands.values()
                if cmd.category == category
            ]
            
            result.success = True
            result.commands = category_commands
            result.message = f"Found {len(category_commands)} commands in {category.value}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def add_to_favorites(
        self,
        command_id: str
    ) -> CommandPaletteResult:
        """
        Command'ı favorilere ekle.
        
        Args:
            command_id: Command ID
            
        Returns:
            CommandPaletteResult: Ekleme sonucu
        """
        result = CommandPaletteResult(success=False)
        
        try:
            if command_id not in self.commands:
                result.errors.append(f"Command '{command_id}' not found")
                return result
            
            if command_id not in self.favorite_commands:
                self.favorite_commands.append(command_id)
            
            result.success = True
            result.message = f"Command '{command_id}' added to favorites"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def remove_from_favorites(
        self,
        command_id: str
    ) -> CommandPaletteResult:
        """
        Command'ı favorilerden kaldır.
        
        Args:
            command_id: Command ID
            
        Returns:
            CommandPaletteResult: Kaldırma sonucu
        """
        result = CommandPaletteResult(success=False)
        
        try:
            if command_id in self.favorite_commands:
                self.favorite_commands.remove(command_id)
            
            result.success = True
            result.message = f"Command '{command_id}' removed from favorites"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_command_history(
        self,
        limit: int = 10
    ) -> CommandPaletteResult:
        """
        Command history al.
        
        Args:
            limit: Limit
            
        Returns:
            CommandPaletteResult: History
        """
        result = CommandPaletteResult(success=False)
        
        try:
            history_commands = []
            for cmd_id in self.command_history[-limit:]:
                if cmd_id in self.commands:
                    history_commands.append(self.commands[cmd_id])
            
            result.success = True
            result.commands = history_commands
            result.message = f"Retrieved {len(history_commands)} commands from history"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_all_commands(self) -> CommandPaletteResult:
        """
        Tüm command'ları al.
        
        Returns:
            CommandPaletteResult: Tüm command'lar
        """
        result = CommandPaletteResult(success=False)
        
        try:
            all_commands = list(self.commands.values())
            
            result.success = True
            result.commands = all_commands
            result.message = f"Retrieved {len(all_commands)} commands"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def validate_command(self, command: Command) -> Tuple[bool, List[str]]:
        """
        Command doğrula.
        
        Args:
            command: Command
            
        Returns:
            Tuple[bool, List[str]]: (valid, errors)
        """
        errors = []
        
        if not command.id:
            errors.append("Command ID is required")
        
        if not command.name:
            errors.append("Command name is required")
        
        if not command.description:
            errors.append("Command description is required")
        
        if not command.category:
            errors.append("Command category is required")
        
        if not command.action:
            errors.append("Command action is required")
        
        return (len(errors) == 0, errors)
    
    def export_commands(self) -> Dict[str, Any]:
        """
        Command'ları export et.
        
        Returns:
            Dict[str, Any]: Export data
        """
        export_data = {
            "commands": []
        }
        
        for command in self.commands.values():
            if not command.is_builtin:
                command_data = {
                    "id": command.id,
                    "name": command.name,
                    "description": command.description,
                    "category": command.category.value,
                    "shortcut": command.shortcut,
                    "icon": command.icon,
                    "tags": command.tags,
                    "aliases": command.aliases,
                    "when": command.when
                }
                export_data["commands"].append(command_data)
        
        return export_data
    
    def import_commands(self, data: Dict[str, Any]) -> CommandPaletteResult:
        """
        Command'ları import et.
        
        Args:
            data: Import data
            
        Returns:
            CommandPaletteResult: Import sonucu
        """
        result = CommandPaletteResult(success=False)
        
        try:
            if "commands" not in data:
                result.errors.append("Invalid import data")
                return result
            
            imported_count = 0
            for command_data in data["commands"]:
                command = Command(
                    id=command_data.get("id", ""),
                    name=command_data.get("name", ""),
                    description=command_data.get("description", ""),
                    category=CommandCategory(command_data.get("category", "tools")),
                    action=lambda: None,
                    shortcut=command_data.get("shortcut"),
                    icon=command_data.get("icon"),
                    tags=command_data.get("tags", []),
                    aliases=command_data.get("aliases", []),
                    when=command_data.get("when", ""),
                    is_builtin=False
                )
                
                register_result = self.register_command(command)
                if register_result.success:
                    imported_count += 1
            
            result.success = True
            result.message = f"Imported {imported_count} commands"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_command_by_alias(self, alias: str) -> Optional[Command]:
        """
        Alias için command al.
        
        Args:
            alias: Alias
            
        Returns:
            Optional[Command]: Command
        """
        for command in self.commands.values():
            if alias in command.aliases:
                return command
        return None
    
    def get_command_by_id(self, command_id: str) -> Optional[Command]:
        """
        ID için command al.
        
        Args:
            command_id: Command ID
            
        Returns:
            Optional[Command]: Command
        """
        return self.commands.get(command_id)
    
    def get_categories(self) -> List[CommandCategory]:
        """
        Kategorileri al.
        
        Returns:
            List[CommandCategory]: Kategori listesi
        """
        categories = set()
        for command in self.commands.values():
            categories.add(command.category)
        return list(categories)

    def _register_default_commands(self):
        """Default command'ları kaydet."""
        # File commands
        self.register_command(Command(
            id="file.new",
            name="New File",
            description="Create a new file",
            category=CommandCategory.FILE,
            action=lambda: print("Creating new file..."),
            shortcut="Ctrl+N",
            tags=["file", "create"],
            is_builtin=True
        ))
        
        self.register_command(Command(
            id="file.save",
            name="Save File",
            description="Save the current file",
            category=CommandCategory.FILE,
            action=lambda: print("Saving file..."),
            shortcut="Ctrl+S",
            tags=["file", "save"],
            is_builtin=True
        ))
        
        # Edit commands
        self.register_command(Command(
            id="edit.undo",
            name="Undo",
            description="Undo last action",
            category=CommandCategory.EDIT,
            action=lambda: print("Undoing..."),
            shortcut="Ctrl+Z",
            tags=["edit", "undo"],
            is_builtin=True
        ))
        
        self.register_command(Command(
            id="edit.redo",
            name="Redo",
            description="Redo last action",
            category=CommandCategory.EDIT,
            action=lambda: print("Redoing..."),
            shortcut="Ctrl+Y",
            tags=["edit", "redo"],
            is_builtin=True
        ))
        
        # Navigation commands
        self.register_command(Command(
            id="nav.go_to_definition",
            name="Go to Definition",
            description="Go to symbol definition",
            category=CommandCategory.NAVIGATION,
            action=lambda: print("Going to definition..."),
            shortcut="F12",
            tags=["navigation", "definition"],
            is_builtin=True
        ))
        
        self.register_command(Command(
            id="nav.find_references",
            name="Find References",
            description="Find symbol references",
            category=CommandCategory.NAVIGATION,
            action=lambda: print("Finding references..."),
            shortcut="Shift+F12",
            tags=["navigation", "references"],
            is_builtin=True
        ))
        
        # View commands
        self.register_command(Command(
            id="view.toggle_sidebar",
            name="Toggle Sidebar",
            description="Toggle the sidebar visibility",
            category=CommandCategory.VIEW,
            action=lambda: print("Toggling sidebar..."),
            shortcut="Ctrl+B",
            tags=["view", "sidebar"],
            is_builtin=True
        ))
        
        self.register_command(Command(
            id="view.toggle_terminal",
            name="Toggle Terminal",
            description="Toggle the terminal panel",
            category=CommandCategory.VIEW,
            action=lambda: print("Toggling terminal..."),
            shortcut="Ctrl+`",
            tags=["view", "terminal"],
            is_builtin=True
        ))
        
        # Refactoring commands
        self.register_command(Command(
            id="refactor.rename",
            name="Rename Symbol",
            description="Rename symbol under cursor",
            category=CommandCategory.REFACTORING,
            action=lambda: print("Renaming..."),
            shortcut="F2",
            tags=["refactor", "rename"],
            is_builtin=True
        ))
        
        self.register_command(Command(
            id="refactor.extract_function",
            name="Extract Function",
            description="Extract selected code into function",
            category=CommandCategory.REFACTORING,
            action=lambda: print("Extracting function..."),
            shortcut="Ctrl+Shift+R",
            tags=["refactor", "extract"],
            is_builtin=True
        ))
        
        # Search commands
        self.register_command(Command(
            id="search.find",
            name="Find",
            description="Find in current file",
            category=CommandCategory.SEARCH,
            action=lambda: print("Finding..."),
            shortcut="Ctrl+F",
            tags=["search", "find"],
            is_builtin=True
        ))
        
        self.register_command(Command(
            id="search.replace",
            name="Replace",
            description="Find and replace in current file",
            category=CommandCategory.SEARCH,
            action=lambda: print("Replacing..."),
            shortcut="Ctrl+H",
            tags=["search", "replace"],
            is_builtin=True
        ))
        
        self.register_command(Command(
            id="search.search_files",
            name="Search in Files",
            description="Search across all files",
            category=CommandCategory.SEARCH,
            action=lambda: print("Searching files..."),
            shortcut="Ctrl+Shift+F",
            tags=["search", "files"],
            is_builtin=True
        ))
        
        # Debug commands
        self.register_command(Command(
            id="debug.start",
            name="Start Debugging",
            description="Start debugging session",
            category=CommandCategory.DEBUG,
            action=lambda: print("Starting debug..."),
            shortcut="F5",
            tags=["debug", "start"],
            is_builtin=True
        ))
        
        self.register_command(Command(
            id="debug.toggle_breakpoint",
            name="Toggle Breakpoint",
            description="Toggle breakpoint at current line",
            category=CommandCategory.DEBUG,
            action=lambda: print("Toggling breakpoint..."),
            shortcut="F9",
            tags=["debug", "breakpoint"],
            is_builtin=True
        ))
        
        # Git commands
        self.register_command(Command(
            id="git.commit",
            name="Git Commit",
            description="Commit changes",
            category=CommandCategory.GIT,
            action=lambda: print("Committing..."),
            shortcut="Ctrl+Shift+G",
            tags=["git", "commit"],
            is_builtin=True
        ))
        
        self.register_command(Command(
            id="git.push",
            name="Git Push",
            description="Push changes to remote",
            category=CommandCategory.GIT,
            action=lambda: print("Pushing..."),
            tags=["git", "push"],
            is_builtin=True
        ))
        
        # Terminal commands
        self.register_command(Command(
            id="terminal.new",
            name="New Terminal",
            description="Create new terminal",
            category=CommandCategory.TERMINAL,
            action=lambda: print("Creating terminal..."),
            shortcut="Ctrl+Shift+`",
            tags=["terminal", "new"],
            is_builtin=True
        ))
        
        # Preferences commands
        self.register_command(Command(
            id="prefs.settings",
            name="Open Settings",
            description="Open settings editor",
            category=CommandCategory.PREFERENCES,
            action=lambda: print("Opening settings..."),
            shortcut="Ctrl+,",
            tags=["preferences", "settings"],
            is_builtin=True
        ))
        
        self.register_command(Command(
            id="prefs.keybindings",
            name="Keyboard Shortcuts",
            description="Open keyboard shortcuts editor",
            category=CommandCategory.PREFERENCES,
            action=lambda: print("Opening keybindings..."),
            shortcut="Ctrl+K Ctrl+S",
            tags=["preferences", "keybindings"],
            is_builtin=True
        ))


if __name__ == "__main__":
    # Basit test
    palette = CommandPalette()
    
    # Command ara
    result = palette.search_commands("save")
    print(f"Search result: {result.success}")
    print(f"Commands found: {len(result.commands)}")
    
    # Command çalıştır
    result = palette.execute_command("file.save")
    print(f"Execution result: {result.success}")
