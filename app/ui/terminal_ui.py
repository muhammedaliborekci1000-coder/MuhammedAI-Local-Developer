"""
MuhammedAI Local Developer - Terminal UI
Terminal UI system for web UI.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime


class TerminalMode(Enum):
    """Terminal mode."""
    NORMAL = "normal"
    INSERT = "insert"
    VISUAL = "visual"
    COMMAND = "command"
    CUSTOM = "custom"


class TerminalTheme(Enum):
    """Terminal theme."""
    LIGHT = "light"
    DARK = "dark"
    HIGH_CONTRAST = "high_contrast"
    SOLARIZED = "solarized"
    DRACULA = "dracula"
    MONOKAI = "monokai"
    CUSTOM = "custom"


class ShellType(Enum):
    """Shell type."""
    BASH = "bash"
    ZSH = "zsh"
    FISH = "fish"
    POWERSHELL = "powershell"
    CMD = "cmd"
    SH = "sh"
    CUSTOM = "custom"


@dataclass
class TerminalSession:
    """Terminal session."""
    id: str
    title: str
    shell_type: ShellType
    working_directory: str
    created_at: datetime
    is_active: bool = True
    is_visible: bool = True
    history: List[str] = field(default_factory=list)
    environment: Dict[str, str] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TerminalOutput:
    """Terminal output."""
    id: str
    session_id: str
    content: str
    timestamp: datetime
    is_error: bool = False
    is_warning: bool = False
    is_info: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TerminalUIConfig:
    """Terminal UI configuration."""
    enabled: bool = True
    show_line_numbers: bool = False
    show_timestamps: bool = True
    show_prompt: bool = True
    enable_syntax_highlighting: bool = True
    enable_auto_complete: bool = True
    enable_history: bool = True
    max_history: int = 1000
    max_output_lines: int = 10000
    font_size: int = 14
    font_family: str = "Consolas"
    theme: TerminalTheme = TerminalTheme.DARK
    enable_copy_paste: bool = True
    enable_clear: bool = True
    enable_search: bool = True


@dataclass
class TerminalUIResult:
    """Terminal UI result."""
    success: bool
    session: Optional[TerminalSession] = None
    sessions: List[TerminalSession] = field(default_factory=list)
    output: Optional[TerminalOutput] = None
    outputs: List[TerminalOutput] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    message: Optional[str] = None


class TerminalUIManager:
    """
    Terminal UI manager.
    
    Özellikler:
    - Terminal sessions
    - Shell types (bash, zsh, fish, powershell, cmd, sh)
    - Terminal modes
    - Terminal themes
    - Command history
    - Output management
    - Environment variables
    - Working directory
    - Syntax highlighting
    - Auto complete
    - Copy/paste
    - Clear terminal
    - Search
    - Line numbers
    - Timestamps
    - Prompt
    """
    
    def __init__(self, config: Optional[TerminalUIConfig] = None):
        """
        Initialize terminal UI manager.
        
        Args:
            config: Terminal UI configuration
        """
        self.config = config or TerminalUIConfig()
        self.sessions: Dict[str, TerminalSession] = {}
        self.outputs: Dict[str, List[TerminalOutput]] = {}
        self.active_session_id: Optional[str] = None
        self.session_id_counter = 0
        self.output_id_counter = 0
        self._next_session_id()
        self._next_output_id()
    
    def _next_session_id(self) -> str:
        """
        Generate next session ID.
        
        Returns:
            str: Session ID
        """
        self.session_id_counter += 1
        return f"session_{self.session_id_counter}"
    
    def _next_output_id(self) -> str:
        """
        Generate next output ID.
        
        Returns:
            str: Output ID
        """
        self.output_id_counter += 1
        return f"output_{self.output_id_counter}"
    
    def create_session(self, title: str, shell_type: ShellType, working_directory: str = "/") -> TerminalUIResult:
        """
        Create a terminal session.
        
        Args:
            title: Session title
            shell_type: Shell type
            working_directory: Working directory
            
        Returns:
            TerminalUIResult: Create result
        """
        result = TerminalUIResult(success=True)
        
        try:
            session = TerminalSession(
                id=self._next_session_id(),
                title=title,
                shell_type=shell_type,
                working_directory=working_directory,
                created_at=datetime.now()
            )
            
            self.sessions[session.id] = session
            self.outputs[session.id] = []
            self.active_session_id = session.id
            
            result.session = session
            result.sessions = self.get_all_sessions()
            result.message = f"Session '{session.id}' created"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def delete_session(self, session_id: str) -> TerminalUIResult:
        """
        Delete a terminal session.
        
        Args:
            session_id: Session ID
            
        Returns:
            TerminalUIResult: Delete result
        """
        result = TerminalUIResult(success=False)
        
        try:
            if session_id in self.sessions:
                del self.sessions[session_id]
                if session_id in self.outputs:
                    del self.outputs[session_id]
                if self.active_session_id == session_id:
                    self.active_session_id = None
                result.success = True
                result.sessions = self.get_all_sessions()
                result.message = f"Session '{session_id}' deleted"
            else:
                result.errors.append("Session not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_session(self, session_id: str) -> Optional[TerminalSession]:
        """
        Get session by ID.
        
        Args:
            session_id: Session ID
            
        Returns:
            Optional[TerminalSession]: Session
        """
        return self.sessions.get(session_id)
    
    def get_all_sessions(self) -> List[TerminalSession]:
        """
        Get all sessions.
        
        Returns:
            List[TerminalSession]: All sessions
        """
        return list(self.sessions.values())
    
    def set_active_session(self, session_id: str) -> TerminalUIResult:
        """
        Set active session.
        
        Args:
            session_id: Session ID
            
        Returns:
            TerminalUIResult: Set result
        """
        result = TerminalUIResult(success=False)
        
        try:
            if session_id in self.sessions:
                self.active_session_id = session_id
                result.success = True
                result.session = self.sessions[session_id]
                result.message = f"Session '{session_id}' set as active"
            else:
                result.errors.append("Session not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def add_output(self, content: str, session_id: Optional[str] = None, is_error: bool = False) -> TerminalUIResult:
        """
        Add terminal output.
        
        Args:
            content: Output content
            session_id: Session ID (uses active if not provided)
            is_error: Is error output
            
        Returns:
            TerminalUIResult: Add result
        """
        result = TerminalUIResult(success=True)
        
        try:
            target_session_id = session_id or self.active_session_id
            
            if not target_session_id:
                result.errors.append("No active session")
                result.success = False
                return result
            
            if target_session_id not in self.sessions:
                result.errors.append("Session not found")
                result.success = False
                return result
            
            session_outputs = self.outputs.get(target_session_id, [])
            
            if len(session_outputs) >= self.config.max_output_lines:
                result.errors.append(f"Maximum output lines reached (max {self.config.max_output_lines})")
                result.success = False
                return result
            
            output = TerminalOutput(
                id=self._next_output_id(),
                session_id=target_session_id,
                content=content,
                timestamp=datetime.now(),
                is_error=is_error
            )
            
            self.outputs[target_session_id].append(output)
            
            result.output = output
            result.outputs = self.outputs[target_session_id]
            result.message = f"Output '{output.id}' added"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def get_outputs(self, session_id: Optional[str] = None) -> List[TerminalOutput]:
        """
        Get outputs from session.
        
        Args:
            session_id: Session ID (uses active if not provided)
            
        Returns:
            List[TerminalOutput]: Outputs
        """
        target_session_id = session_id or self.active_session_id
        
        if target_session_id in self.outputs:
            return self.outputs[target_session_id]
        return []
    
    def add_command_to_history(self, command: str, session_id: Optional[str] = None) -> TerminalUIResult:
        """
        Add command to history.
        
        Args:
            command: Command string
            session_id: Session ID (uses active if not provided)
            
        Returns:
            TerminalUIResult: Add result
        """
        result = TerminalUIResult(success=True)
        
        try:
            target_session_id = session_id or self.active_session_id
            
            if not target_session_id:
                result.errors.append("No active session")
                result.success = False
                return result
            
            session = self.sessions.get(target_session_id)
            if not session:
                result.errors.append("Session not found")
                result.success = False
                return result
            
            if len(session.history) >= self.config.max_history:
                session.history.pop(0)
            
            session.history.append(command)
            
            result.session = session
            result.message = f"Command added to history"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def get_history(self, session_id: Optional[str] = None) -> List[str]:
        """
        Get command history.
        
        Args:
            session_id: Session ID (uses active if not provided)
            
        Returns:
            List[str]: History
        """
        target_session_id = session_id or self.active_session_id
        
        if target_session_id in self.sessions:
            return self.sessions[target_session_id].history
        return []
    
    def set_working_directory(self, directory: str, session_id: Optional[str] = None) -> TerminalUIResult:
        """
        Set working directory.
        
        Args:
            directory: Working directory
            session_id: Session ID (uses active if not provided)
            
        Returns:
            TerminalUIResult: Set result
        """
        result = TerminalUIResult(success=False)
        
        try:
            target_session_id = session_id or self.active_session_id
            session = self.sessions.get(target_session_id)
            
            if session:
                session.working_directory = directory
                result.success = True
                result.session = session
                result.message = f"Working directory set to {directory}"
            else:
                result.errors.append("Session not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def set_environment_variable(self, key: str, value: str, session_id: Optional[str] = None) -> TerminalUIResult:
        """
        Set environment variable.
        
        Args:
            key: Variable key
            value: Variable value
            session_id: Session ID (uses active if not provided)
            
        Returns:
            TerminalUIResult: Set result
        """
        result = TerminalUIResult(success=False)
        
        try:
            target_session_id = session_id or self.active_session_id
            session = self.sessions.get(target_session_id)
            
            if session:
                session.environment[key] = value
                result.success = True
                result.session = session
                result.message = f"Environment variable '{key}' set"
            else:
                result.errors.append("Session not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def clear_outputs(self, session_id: Optional[str] = None) -> TerminalUIResult:
        """
        Clear outputs.
        
        Args:
            session_id: Session ID (uses active if not provided)
            
        Returns:
            TerminalUIResult: Clear result
        """
        result = TerminalUIResult(success=True)
        
        try:
            target_session_id = session_id or self.active_session_id
            
            if target_session_id in self.outputs:
                self.outputs[target_session_id].clear()
                result.message = f"Outputs cleared for session '{target_session_id}'"
            else:
                result.errors.append("Session not found")
                result.success = False
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def clear_history(self, session_id: Optional[str] = None) -> TerminalUIResult:
        """
        Clear history.
        
        Args:
            session_id: Session ID (uses active if not provided)
            
        Returns:
            TerminalUIResult: Clear result
        """
        result = TerminalUIResult(success=True)
        
        try:
            target_session_id = session_id or self.active_session_id
            session = self.sessions.get(target_session_id)
            
            if session:
                session.history.clear()
                result.message = f"History cleared for session '{target_session_id}'"
            else:
                result.errors.append("Session not found")
                result.success = False
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def set_theme(self, theme: TerminalTheme) -> TerminalUIResult:
        """
        Set terminal theme.
        
        Args:
            theme: Terminal theme
            
        Returns:
            TerminalUIResult: Set result
        """
        result = TerminalUIResult(success=True)
        
        try:
            self.config.theme = theme
            result.message = f"Theme set to {theme.value}"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def set_font_size(self, size: int) -> TerminalUIResult:
        """
        Set font size.
        
        Args:
            size: Font size
            
        Returns:
            TerminalUIResult: Set result
        """
        result = TerminalUIResult(success=True)
        
        try:
            self.config.font_size = size
            result.message = f"Font size set to {size}"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def update_config(self, config: TerminalUIConfig) -> TerminalUIResult:
        """
        Update terminal UI configuration.
        
        Args:
            config: New configuration
            
        Returns:
            TerminalUIResult: Update result
        """
        result = TerminalUIResult(success=True)
        
        try:
            self.config = config
            result.message = "Config updated"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def get_config(self) -> TerminalUIConfig:
        """
        Get terminal UI configuration.
        
        Returns:
            TerminalUIConfig: Configuration
        """
        return self.config


if __name__ == "__main__":
    # Basit test
    config = TerminalUIConfig()
    manager = TerminalUIManager(config)
    
    # Session oluştur
    result = manager.create_session("Terminal 1", ShellType.BASH, "/home")
    
    print(f"Session created: {result.message}")
    
    # Output ekle
    result = manager.add_output("Hello World!")
    
    print(f"Output added: {result.message}")
    
    # Tüm session'ları al
    sessions = manager.get_all_sessions()
    
    print(f"Total sessions: {len(sessions)}")
