"""
MuhammedAI Local Developer - Language Server
Language server manager and abstraction layer.
"""

import os
import subprocess
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum


class LanguageId(Enum):
    """Language identifiers."""
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    GO = "go"
    RUST = "rust"
    C = "c"
    CPP = "cpp"
    JAVA = "java"
    CSHARP = "csharp"
    PHP = "php"
    RUBY = "ruby"
    SWIFT = "swift"
    KOTLIN = "kotlin"
    HTML = "html"
    CSS = "css"
    JSON = "json"
    YAML = "yaml"
    XML = "xml"
    MARKDOWN = "markdown"
    SHELL = "shell"
    SQL = "sql"
    LUA = "lua"
    R = "r"
    JULIA = "julia"
    DART = "dart"
    ELIXIR = "elixir"
    HASKELL = "haskell"
    SCALA = "scala"
    CLOJURE = "clojure"


class ServerStatus(Enum):
    """Server status."""
    STOPPED = "stopped"
    STARTING = "starting"
    RUNNING = "running"
    STOPPING = "stopping"
    ERROR = "error"


@dataclass
class LanguageServerConfig:
    """Language server configuration."""
    language_id: LanguageId
    command: List[str]
    args: List[str] = field(default_factory=list)
    env: Dict[str, str] = field(default_factory=dict)
    working_dir: Optional[str] = None
    enabled: bool = True
    capabilities: List[str] = field(default_factory=list)


@dataclass
class ServerProcess:
    """Server process information."""
    config: LanguageServerConfig
    process: Optional[subprocess.Popen] = None
    status: ServerStatus = ServerStatus.STOPPED
    pid: Optional[int] = None
    port: Optional[int] = None


class LanguageServerManager:
    """
    Language server manager.
    
    Özellikler:
    - Multi-language support
    - Server lifecycle management
    - Server configuration
    - Server status tracking
    - Server discovery
    - Server capabilities
    - Server health monitoring
    - Automatic server startup
    - Server shutdown
    - Server restart
    - Configuration management
    """
    
    def __init__(self):
        """Initialize language server manager."""
        self.servers: Dict[str, ServerProcess] = {}
        self.configs: Dict[LanguageId, LanguageServerConfig] = {}
        self._initialize_default_configs()
    
    def _initialize_default_configs(self) -> None:
        """Initialize default language server configurations."""
        # Python - pylsp
        self.configs[LanguageId.PYTHON] = LanguageServerConfig(
            language_id=LanguageId.PYTHON,
            command=["python"],
            args=["-m", "pylsp"],
            capabilities=["completion", "hover", "definition", "references", "formatting"]
        )
        
        # JavaScript/TypeScript - tsserver
        self.configs[LanguageId.JAVASCRIPT] = LanguageServerConfig(
            language_id=LanguageId.JAVASCRIPT,
            command=["node"],
            args=["./node_modules/typescript/lib/tsserver.js"],
            capabilities=["completion", "hover", "definition", "references", "formatting"]
        )
        
        self.configs[LanguageId.TYPESCRIPT] = LanguageServerConfig(
            language_id=LanguageId.TYPESCRIPT,
            command=["node"],
            args=["./node_modules/typescript/lib/tsserver.js"],
            capabilities=["completion", "hover", "definition", "references", "formatting"]
        )
        
        # Go - gopls
        self.configs[LanguageId.GO] = LanguageServerConfig(
            language_id=LanguageId.GO,
            command=["gopls"],
            capabilities=["completion", "hover", "definition", "references", "formatting"]
        )
        
        # Rust - rust-analyzer
        self.configs[LanguageId.RUST] = LanguageServerConfig(
            language_id=LanguageId.RUST,
            command=["rust-analyzer"],
            capabilities=["completion", "hover", "definition", "references", "formatting"]
        )
        
        # C/C++ - clangd
        self.configs[LanguageId.C] = LanguageServerConfig(
            language_id=LanguageId.C,
            command=["clangd"],
            capabilities=["completion", "hover", "definition", "references", "formatting"]
        )
        
        self.configs[LanguageId.CPP] = LanguageServerConfig(
            language_id=LanguageId.CPP,
            command=["clangd"],
            capabilities=["completion", "hover", "definition", "references", "formatting"]
        )
    
    def register_server(self, config: LanguageServerConfig) -> bool:
        """
        Register a language server.
        
        Args:
            config: Server configuration
            
        Returns:
            bool: Success status
        """
        try:
            self.configs[config.language_id] = config
            return True
        except Exception:
            return False
    
    def unregister_server(self, language_id: LanguageId) -> bool:
        """
        Unregister a language server.
        
        Args:
            language_id: Language identifier
            
        Returns:
            bool: Success status
        """
        try:
            if language_id in self.configs:
                # Stop server if running
                self.stop_server(language_id)
                del self.configs[language_id]
                return True
            return False
        except Exception:
            return False
    
    def start_server(self, language_id: LanguageId) -> bool:
        """
        Start a language server.
        
        Args:
            language_id: Language identifier
            
        Returns:
            bool: Success status
        """
        if language_id not in self.configs:
            return False
        
        config = self.configs[language_id]
        
        if not config.enabled:
            return False
        
        # Check if already running
        server_key = language_id.value
        if server_key in self.servers and self.servers[server_key].status == ServerStatus.RUNNING:
            return True
        
        try:
            # Create server process
            process = subprocess.Popen(
                config.command + config.args,
                env={**os.environ, **config.env},
                cwd=config.working_dir,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Create server process info
            server_process = ServerProcess(
                config=config,
                process=process,
                status=ServerStatus.RUNNING,
                pid=process.pid
            )
            
            self.servers[server_key] = server_process
            return True
        except Exception:
            return False
    
    def stop_server(self, language_id: LanguageId) -> bool:
        """
        Stop a language server.
        
        Args:
            language_id: Language identifier
            
        Returns:
            bool: Success status
        """
        server_key = language_id.value
        
        if server_key not in self.servers:
            return False
        
        server_process = self.servers[server_key]
        
        if server_process.process is None:
            return False
        
        try:
            server_process.status = ServerStatus.STOPPING
            server_process.process.terminate()
            server_process.process.wait(timeout=5)
            server_process.status = ServerStatus.STOPPED
            server_process.process = None
            server_process.pid = None
            return True
        except Exception:
            try:
                server_process.process.kill()
                server_process.status = ServerStatus.STOPPED
                server_process.process = None
                server_process.pid = None
                return True
            except Exception:
                server_process.status = ServerStatus.ERROR
                return False
    
    def restart_server(self, language_id: LanguageId) -> bool:
        """
        Restart a language server.
        
        Args:
            language_id: Language identifier
            
        Returns:
            bool: Success status
        """
        self.stop_server(language_id)
        return self.start_server(language_id)
    
    def get_server_status(self, language_id: LanguageId) -> Optional[ServerStatus]:
        """
        Get server status.
        
        Args:
            language_id: Language identifier
            
        Returns:
            Optional[ServerStatus]: Server status
        """
        server_key = language_id.value
        
        if server_key not in self.servers:
            return None
        
        return self.servers[server_key].status
    
    def get_server_config(self, language_id: LanguageId) -> Optional[LanguageServerConfig]:
        """
        Get server configuration.
        
        Args:
            language_id: Language identifier
            
        Returns:
            Optional[LanguageServerConfig]: Server configuration
        """
        return self.configs.get(language_id)
    
    def update_server_config(self, language_id: LanguageId, config: LanguageServerConfig) -> bool:
        """
        Update server configuration.
        
        Args:
            language_id: Language identifier
            config: New configuration
            
        Returns:
            bool: Success status
        """
        try:
            self.configs[language_id] = config
            # Restart server if running
            if self.get_server_status(language_id) == ServerStatus.RUNNING:
                self.restart_server(language_id)
            return True
        except Exception:
            return False
    
    def get_all_servers(self) -> Dict[str, ServerStatus]:
        """
        Get all servers and their statuses.
        
        Returns:
            Dict[str, ServerStatus]: Server statuses
        """
        return {key: server.status for key, server in self.servers.items()}
    
    def get_supported_languages(self) -> List[LanguageId]:
        """
        Get supported languages.
        
        Returns:
            List[LanguageId]: Supported languages
        """
        return list(self.configs.keys())
    
    def is_language_supported(self, language_id: LanguageId) -> bool:
        """
        Check if language is supported.
        
        Args:
            language_id: Language identifier
            
        Returns:
            bool: Supported status
        """
        return language_id in self.configs
    
    def get_server_capabilities(self, language_id: LanguageId) -> List[str]:
        """
        Get server capabilities.
        
        Args:
            language_id: Language identifier
            
        Returns:
            List[str]: Capabilities
        """
        config = self.configs.get(language_id)
        return config.capabilities if config else []
    
    def stop_all_servers(self) -> None:
        """Stop all running servers."""
        for language_id in list(self.configs.keys()):
            self.stop_server(language_id)
    
    def get_server_pid(self, language_id: LanguageId) -> Optional[int]:
        """
        Get server process ID.
        
        Args:
            language_id: Language identifier
            
        Returns:
            Optional[int]: Process ID
        """
        server_key = language_id.value
        
        if server_key not in self.servers:
            return None
        
        return self.servers[server_key].pid
    
    def is_server_running(self, language_id: LanguageId) -> bool:
        """
        Check if server is running.
        
        Args:
            language_id: Language identifier
            
        Returns:
            bool: Running status
        """
        status = self.get_server_status(language_id)
        return status == ServerStatus.RUNNING
    
    def enable_server(self, language_id: LanguageId) -> bool:
        """
        Enable a language server.
        
        Args:
            language_id: Language identifier
            
        Returns:
            bool: Success status
        """
        config = self.configs.get(language_id)
        if config:
            config.enabled = True
            return True
        return False
    
    def disable_server(self, language_id: LanguageId) -> bool:
        """
        Disable a language server.
        
        Args:
            language_id: Language identifier
            
        Returns:
            bool: Success status
        """
        config = self.configs.get(language_id)
        if config:
            config.enabled = False
            self.stop_server(language_id)
            return True
        return False


if __name__ == "__main__":
    # Basit test
    manager = LanguageServerManager()
    
    # Desteklenen diller
    languages = manager.get_supported_languages()
    print(f"Supported languages: {[lang.value for lang in languages]}")
    
    # Python sunucusunu başlat
    if manager.start_server(LanguageId.PYTHON):
        print("Python server started")
        
        # Durumu kontrol et
        status = manager.get_server_status(LanguageId.PYTHON)
        print(f"Status: {status.value}")
        
        # Durdur
        if manager.stop_server(LanguageId.PYTHON):
            print("Python server stopped")
