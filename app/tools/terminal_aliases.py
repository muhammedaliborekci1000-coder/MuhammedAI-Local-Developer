"""
MuhammedAI Local Developer - Terminal Aliases
Terminal aliases management engine for code editor.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime


class AliasScope(Enum):
    """Alias scope."""
    SESSION = "session"
    TERMINAL = "terminal"
    GLOBAL = "global"


class AliasAction(Enum):
    """Alias action."""
    ADD = "add"
    REMOVE = "remove"
    GET = "get"
    LIST = "list"
    CLEAR = "clear"
    IMPORT = "import"
    EXPORT = "export"
    EXECUTE = "execute"


@dataclass
class AliasConfig:
    """Alias configuration."""
    persist_aliases: bool = True
    auto_load_from_shell: bool = True
    show_notifications: bool = True
    log_changes: bool = True
    validate_commands: bool = True


@dataclass
class AliasEntry:
    """Alias entry."""
    name: str
    command: str
    description: Optional[str] = None
    scope: AliasScope = AliasScope.SESSION
    timestamp: str = ""
    terminal_id: Optional[str] = None
    session_id: Optional[str] = None


@dataclass
class AliasResult:
    """Alias result."""
    success: bool
    message: Optional[str] = None
    errors: List[str] = field(default_factory=list)
    alias_name: Optional[str] = None
    alias_command: Optional[str] = None
    action: Optional[str] = None


class TerminalAliasesEngine:
    """
    Terminal aliases management engine.
    
    Özellikler:
    - Add alias
    - Remove alias
    - Get alias
    - List aliases
    - Clear aliases
    - Import aliases
    - Export aliases
    - Execute alias
    - Alias scope (session, terminal, global)
    - Alias persistence
    - Alias validation
    - Alias history
    - Alias search/filter
    """
    
    def __init__(self, config: Optional[AliasConfig] = None):
        """Initialize terminal aliases engine."""
        self.config = config or AliasConfig()
        self.aliases: Dict[str, AliasEntry] = {}
        self.alias_history: List[Dict[str, Any]] = []
        self._entry_counter = 0
    
    def add_alias(
        self,
        name: str,
        command: str,
        description: Optional[str] = None,
        scope: AliasScope = AliasScope.SESSION,
        terminal_id: Optional[str] = None,
        session_id: Optional[str] = None
    ) -> AliasResult:
        """
        Alias ekle.
        
        Args:
            name: Alias adı
            command: Komut
            description: Açıklama
            scope: Kapsam
            terminal_id: Terminal ID
            session_id: Oturum ID
            
        Returns:
            AliasResult: Ekleme sonucu
        """
        result = AliasResult(success=False)
        result.action = AliasAction.ADD.value
        result.alias_name = name
        result.alias_command = command
        
        try:
            # Validate
            if self.config.validate_commands:
                if not name or not isinstance(name, str):
                    result.errors.append("Invalid alias name")
                    return result
                if not command or not isinstance(command, str):
                    result.errors.append("Invalid command")
                    return result
            
            # Create entry
            entry = AliasEntry(
                name=name,
                command=command,
                description=description,
                scope=scope,
                timestamp=self._get_timestamp(),
                terminal_id=terminal_id,
                session_id=session_id
            )
            
            # Store
            self.aliases[name] = entry
            
            # Add to history
            if self.config.log_changes:
                self.alias_history.append({
                    "action": "add",
                    "name": name,
                    "command": command,
                    "scope": scope.value,
                    "timestamp": entry.timestamp
                })
            
            result.success = True
            result.message = f"Alias {name} added"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def remove_alias(self, name: str) -> AliasResult:
        """
        Alias kaldır.
        
        Args:
            name: Alias adı
            
        Returns:
            AliasResult: Kaldırma sonucu
        """
        result = AliasResult(success=False)
        result.action = AliasAction.REMOVE.value
        result.alias_name = name
        
        try:
            if name not in self.aliases:
                result.errors.append(f"Alias not found: {name}")
                return result
            
            del self.aliases[name]
            
            # Add to history
            if self.config.log_changes:
                self.alias_history.append({
                    "action": "remove",
                    "name": name,
                    "timestamp": self._get_timestamp()
                })
            
            result.success = True
            result.message = f"Alias {name} removed"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_alias(self, name: str) -> AliasResult:
        """
        Alias al.
        
        Args:
            name: Alias adı
            
        Returns:
            AliasResult: Alma sonucu
        """
        result = AliasResult(success=False)
        result.action = AliasAction.GET.value
        result.alias_name = name
        
        try:
            if name not in self.aliases:
                result.errors.append(f"Alias not found: {name}")
                return result
            
            entry = self.aliases[name]
            result.success = True
            result.alias_command = entry.command
            result.message = f"Alias {name} retrieved"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def list_aliases(
        self,
        scope: Optional[AliasScope] = None,
        terminal_id: Optional[str] = None,
        session_id: Optional[str] = None
    ) -> AliasResult:
        """
        Aliasleri listele.
        
        Args:
            scope: Kapsam
            terminal_id: Terminal ID
            session_id: Oturum ID
            
        Returns:
            AliasResult: Listeleme sonucu
        """
        result = AliasResult(success=False)
        result.action = AliasAction.LIST.value
        
        try:
            filtered = list(self.aliases.values())
            
            if scope:
                filtered = [a for a in filtered if a.scope == scope]
            
            if terminal_id:
                filtered = [a for a in filtered if a.terminal_id == terminal_id]
            
            if session_id:
                filtered = [a for a in filtered if a.session_id == session_id]
            
            result.success = True
            result.message = f"Listed {len(filtered)} aliases"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def clear_aliases(
        self,
        scope: Optional[AliasScope] = None
    ) -> AliasResult:
        """
        Aliasleri temizle.
        
        Args:
            scope: Kapsam
            
        Returns:
            AliasResult: Temizleme sonucu
        """
        result = AliasResult(success=False)
        result.action = AliasAction.CLEAR.value
        
        try:
            if scope:
                to_remove = [name for name, entry in self.aliases.items() if entry.scope == scope]
                for name in to_remove:
                    del self.aliases[name]
            else:
                self.aliases.clear()
            
            # Add to history
            if self.config.log_changes:
                self.alias_history.append({
                    "action": "clear",
                    "scope": scope.value if scope else "all",
                    "timestamp": self._get_timestamp()
                })
            
            result.success = True
            result.message = "Aliases cleared"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def export_aliases(
        self,
        format: str = "json"
    ) -> AliasResult:
        """
        Aliasleri dışa aktar.
        
        Args:
            format: Format (json, shell)
            
        Returns:
            AliasResult: Dışa aktarma sonucu
        """
        result = AliasResult(success=False)
        result.action = AliasAction.EXPORT.value
        
        try:
            if format == "json":
                import json
                data = {
                    name: {
                        "command": entry.command,
                        "description": entry.description,
                        "scope": entry.scope.value,
                        "timestamp": entry.timestamp
                    }
                    for name, entry in self.aliases.items()
                }
                result.success = True
                result.message = f"Exported {len(data)} aliases as JSON"
            elif format == "shell":
                lines = [f"alias {name}='{entry.command}'" for name, entry in self.aliases.items()]
                result.success = True
                result.message = f"Exported {len(lines)} aliases as shell"
            else:
                result.errors.append(f"Unsupported format: {format}")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def import_aliases(
        self,
        data: Dict[str, str],
        scope: AliasScope = AliasScope.SESSION
    ) -> AliasResult:
        """
        Aliasleri içe aktar.
        
        Args:
            data: Veri
            scope: Kapsam
            
        Returns:
            AliasResult: İçe aktarma sonucu
        """
        result = AliasResult(success=False)
        result.action = AliasAction.IMPORT.value
        
        try:
            imported_count = 0
            for name, command in data.items():
                entry = AliasEntry(
                    name=name,
                    command=command,
                    scope=scope,
                    timestamp=self._get_timestamp()
                )
                self.aliases[name] = entry
                imported_count += 1
            
            # Add to history
            if self.config.log_changes:
                self.alias_history.append({
                    "action": "import",
                    "count": imported_count,
                    "scope": scope.value,
                    "timestamp": self._get_timestamp()
                })
            
            result.success = True
            result.message = f"Imported {imported_count} aliases"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def execute_alias(self, name: str) -> AliasResult:
        """
        Alias çalıştır.
        
        Args:
            name: Alias adı
            
        Returns:
            AliasResult: Çalıştırma sonucu
        """
        result = AliasResult(success=False)
        result.action = AliasAction.EXECUTE.value
        result.alias_name = name
        
        try:
            if name not in self.aliases:
                result.errors.append(f"Alias not found: {name}")
                return result
            
            entry = self.aliases[name]
            result.success = True
            result.alias_command = entry.command
            result.message = f"Executing alias {name}: {entry.command}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_alias_history(self) -> List[Dict[str, Any]]:
        """
        Alias geçmişini al.
        
        Returns:
            List[Dict[str, Any]]: Geçmiş
        """
        return self.alias_history
    
    def clear_history(self) -> AliasResult:
        """
        Geçmişi temizle.
        
        Returns:
            AliasResult: Temizleme sonucu
        """
        result = AliasResult(success=False)
        
        try:
            self.alias_history.clear()
            result.success = True
            result.message = "Alias history cleared"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def update_config(self, config: AliasConfig) -> AliasResult:
        """
        Konfigürasyon güncelle.
        
        Args:
            config: Yeni konfigürasyon
            
        Returns:
            AliasResult: Güncelleme sonucu
        """
        result = AliasResult(success=False)
        
        try:
            self.config = config
            result.success = True
            result.message = "Config updated"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_config(self) -> AliasConfig:
        """
        Konfigürasyon al.
        
        Returns:
            AliasConfig: Konfigürasyon
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
    engine = TerminalAliasesEngine()
    
    print("Terminal Aliases Engine initialized")
    print(f"Persist aliases: {engine.config.persist_aliases}")
