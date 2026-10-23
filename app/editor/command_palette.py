"""
MuhammedAI Local Developer - Command Palette
Command palette system for code editor.
"""

from typing import Dict, Any, Optional, List, Callable
from dataclasses import dataclass, field
from enum import Enum


class CommandType(Enum):
    """Command type."""
    FILE = "file"
    EDIT = "edit"
    VIEW = "view"
    NAVIGATION = "navigation"
    SEARCH = "search"
    TOOLS = "tools"
    PREFERENCES = "preferences"
    CUSTOM = "custom"


@dataclass
class Command:
    """Command information."""
    id: str
    title: str
    type: CommandType
    description: Optional[str] = None
    shortcut: Optional[str] = None
    category: Optional[str] = None
    icon: Optional[str] = None
    enabled: bool = True
    action: Optional[Callable] = None


@dataclass
class CommandPaletteConfig:
    """Command palette configuration."""
    max_results: int = 10
    fuzzy_search: bool = True
    show_shortcuts: bool = True
    show_categories: bool = True
    show_icons: bool = False
    recent_commands_limit: int = 5
    enable_history: bool = True


@dataclass
class CommandPaletteResult:
    """Command palette result."""
    success: bool
    commands: List[Command] = field(default_factory=list)
    selected_command: Optional[Command] = None
    errors: List[str] = field(default_factory=list)
    message: Optional[str] = None


class CommandPaletteEngine:
    """
    Command palette engine.
    
    Özellikler:
    - Command palette
    - Quick commands
    - Command search
    - Fuzzy search
    - Command categories
    - Command shortcuts
    - Command history
    - Recent commands
    - Command execution
    - Custom commands
    - Command filtering
    - Command sorting
    - Command icons
    - Command descriptions
    """
    
    def __init__(self, config: Optional[CommandPaletteConfig] = None):
        """
        Initialize command palette engine.
        
        Args:
            config: Command palette configuration
        """
        self.config = config or CommandPaletteConfig()
        self.commands: Dict[str, Command] = {}
        self.command_history: List[str] = []
        self.recent_commands: List[str] = []
        self._initialize_builtin_commands()
    
    def _initialize_builtin_commands(self) -> None:
        """Initialize built-in commands."""
        # File commands
        self.register_command(Command(
            id="file.new",
            title="New File",
            type=CommandType.FILE,
            description="Create a new file",
            shortcut="Ctrl+N",
            category="File"
        ))
        
        self.register_command(Command(
            id="file.open",
            title="Open File",
            type=CommandType.FILE,
            description="Open a file",
            shortcut="Ctrl+O",
            category="File"
        ))
        
        self.register_command(Command(
            id="file.save",
            title="Save File",
            type=CommandType.FILE,
            description="Save the current file",
            shortcut="Ctrl+S",
            category="File"
        ))
        
        self.register_command(Command(
            id="file.save_all",
            title="Save All Files",
            type=CommandType.FILE,
            description="Save all files",
            shortcut="Ctrl+K S",
            category="File"
        ))
        
        # Edit commands
        self.register_command(Command(
            id="edit.undo",
            title="Undo",
            type=CommandType.EDIT,
            description="Undo the last action",
            shortcut="Ctrl+Z",
            category="Edit"
        ))
        
        self.register_command(Command(
            id="edit.redo",
            title="Redo",
            type=CommandType.EDIT,
            description="Redo the last undone action",
            shortcut="Ctrl+Y",
            category="Edit"
        ))
        
        self.register_command(Command(
            id="edit.cut",
            title="Cut",
            type=CommandType.EDIT,
            description="Cut the selection",
            shortcut="Ctrl+X",
            category="Edit"
        ))
        
        self.register_command(Command(
            id="edit.copy",
            title="Copy",
            type=CommandType.EDIT,
            description="Copy the selection",
            shortcut="Ctrl+C",
            category="Edit"
        ))
        
        self.register_command(Command(
            id="edit.paste",
            title="Paste",
            type=CommandType.EDIT,
            description="Paste the clipboard",
            shortcut="Ctrl+V",
            category="Edit"
        ))
        
        # View commands
        self.register_command(Command(
            id="view.command_palette",
            title="Command Palette",
            type=CommandType.VIEW,
            description="Open command palette",
            shortcut="Ctrl+Shift+P",
            category="View"
        ))
        
        self.register_command(Command(
            id="view.toggle_sidebar",
            title="Toggle Sidebar",
            type=CommandType.VIEW,
            description="Toggle sidebar visibility",
            shortcut="Ctrl+B",
            category="View"
        ))
        
        self.register_command(Command(
            id="view.toggle_terminal",
            title="Toggle Terminal",
            type=CommandType.VIEW,
            description="Toggle terminal visibility",
            shortcut="Ctrl+`",
            category="View"
        ))
        
        # Navigation commands
        self.register_command(Command(
            id="nav.go_to_line",
            title="Go to Line",
            type=CommandType.NAVIGATION,
            description="Go to a specific line",
            shortcut="Ctrl+G",
            category="Navigation"
        ))
        
        self.register_command(Command(
            id="nav.go_to_file",
            title="Go to File",
            type=CommandType.NAVIGATION,
            description="Go to a file",
            shortcut="Ctrl+P",
            category="Navigation"
        ))
        
        # Search commands
        self.register_command(Command(
            id="search.find",
            title="Find",
            type=CommandType.SEARCH,
            description="Find in current file",
            shortcut="Ctrl+F",
            category="Search"
        ))
        
        self.register_command(Command(
            id="search.replace",
            title="Replace",
            type=CommandType.SEARCH,
            description="Find and replace",
            shortcut="Ctrl+H",
            category="Search"
        ))
        
        self.register_command(Command(
            id="search.find_in_files",
            title="Find in Files",
            type=CommandType.SEARCH,
            description="Search across files",
            shortcut="Ctrl+Shift+F",
            category="Search"
        ))
        
        # Preferences commands
        self.register_command(Command(
            id="pref.settings",
            title="Open Settings",
            type=CommandType.PREFERENCES,
            description="Open settings",
            shortcut="Ctrl+,",
            category="Preferences"
        ))
        
        self.register_command(Command(
            id="pref.keybindings",
            title="Keyboard Shortcuts",
            type=CommandType.PREFERENCES,
            description="View keyboard shortcuts",
            shortcut="Ctrl+K Ctrl+S",
            category="Preferences"
        ))
    
    def register_command(self, command: Command) -> bool:
        """
        Register a command.
        
        Args:
            command: Command to register
            
        Returns:
            bool: Success
        """
        self.commands[command.id] = command
        return True
    
    def unregister_command(self, command_id: str) -> bool:
        """
        Unregister a command.
        
        Args:
            command_id: Command ID
            
        Returns:
            bool: Success
        """
        if command_id in self.commands:
            del self.commands[command_id]
            return True
        return False
    
    def get_command(self, command_id: str) -> Optional[Command]:
        """
        Get command by ID.
        
        Args:
            command_id: Command ID
            
        Returns:
            Optional[Command]: Command
        """
        return self.commands.get(command_id)
    
    def get_all_commands(self) -> List[Command]:
        """
        Get all commands.
        
        Returns:
            List[Command]: All commands
        """
        return list(self.commands.values())
    
    def get_commands_by_type(self, command_type: CommandType) -> List[Command]:
        """
        Get commands by type.
        
        Args:
            command_type: Command type
            
        Returns:
            List[Command]: Commands
        """
        return [cmd for cmd in self.commands.values() if cmd.type == command_type]
    
    def get_commands_by_category(self, category: str) -> List[Command]:
        """
        Get commands by category.
        
        Args:
            category: Category name
            
        Returns:
            List[Command]: Commands
        """
        return [cmd for cmd in self.commands.values() if cmd.category == category]
    
    def search_commands(self, query: str) -> CommandPaletteResult:
        """
        Search commands.
        
        Args:
            query: Search query
            
        Returns:
            CommandPaletteResult: Search result
        """
        result = CommandPaletteResult(success=True)
        
        if not query:
            # Return recent commands if no query
            if self.config.enable_history and self.recent_commands:
                result.commands = [self.commands[cid] for cid in self.recent_commands if cid in self.commands]
            else:
                result.commands = self.get_all_commands()
            return result
        
        query_lower = query.lower()
        
        if self.config.fuzzy_search:
            # Fuzzy search
            for command in self.commands.values():
                if not command.enabled:
                    continue
                
                # Search in title and description
                if (query_lower in command.title.lower() or 
                    (command.description and query_lower in command.description.lower())):
                    result.commands.append(command)
        else:
            # Exact search
            for command in self.commands.values():
                if not command.enabled:
                    continue
                
                if query_lower == command.title.lower():
                    result.commands.append(command)
        
        # Limit results
        if len(result.commands) > self.config.max_results:
            result.commands = result.commands[:self.config.max_results]
        
        return result
    
    def execute_command(self, command_id: str) -> CommandPaletteResult:
        """
        Execute a command.
        
        Args:
            command_id: Command ID
            
        Returns:
            CommandPaletteResult: Execution result
        """
        result = CommandPaletteResult(success=False)
        
        command = self.get_command(command_id)
        if not command:
            result.errors.append("Command not found")
            return result
        
        if not command.enabled:
            result.errors.append("Command is disabled")
            return result
        
        # Execute action
        if command.action:
            try:
                command.action()
                result.success = True
                result.message = f"Command '{command.title}' executed"
            except Exception as e:
                result.errors.append(f"Error executing command: {str(e)}")
        else:
            result.success = True
            result.message = f"Command '{command.title}' executed (no action)"
        
        # Add to history
        if self.config.enable_history:
            self._add_to_history(command_id)
        
        result.selected_command = command
        return result
    
    def _add_to_history(self, command_id: str) -> None:
        """
        Add command to history.
        
        Args:
            command_id: Command ID
        """
        # Remove from recent if exists
        if command_id in self.recent_commands:
            self.recent_commands.remove(command_id)
        
        # Add to front
        self.recent_commands.insert(0, command_id)
        
        # Limit recent commands
        if len(self.recent_commands) > self.config.recent_commands_limit:
            self.recent_commands = self.recent_commands[:self.config.recent_commands_limit]
        
        # Add to full history
        self.command_history.append(command_id)
    
    def get_recent_commands(self) -> List[Command]:
        """
        Get recent commands.
        
        Returns:
            List[Command]: Recent commands
        """
        return [self.commands[cid] for cid in self.recent_commands if cid in self.commands]
    
    def get_command_history(self) -> List[str]:
        """
        Get command history.
        
        Returns:
            List[str]: Command history
        """
        return self.command_history
    
    def clear_history(self) -> None:
        """Clear command history."""
        self.command_history.clear()
        self.recent_commands.clear()
    
    def update_config(self, config: CommandPaletteConfig) -> None:
        """
        Update command palette configuration.
        
        Args:
            config: New configuration
        """
        self.config = config
    
    def get_config(self) -> CommandPaletteConfig:
        """
        Get command palette configuration.
        
        Returns:
            CommandPaletteConfig: Configuration
        """
        return self.config


if __name__ == "__main__":
    # Basit test
    config = CommandPaletteConfig()
    engine = CommandPaletteEngine(config)
    
    # Search commands
    result = engine.search_commands("save")
    
    print(f"Found {len(result.commands)} commands")
    for cmd in result.commands:
        print(f"  - {cmd.title} ({cmd.shortcut})")
