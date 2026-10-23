"""
MuhammedAI Local Developer - Terminal Profiles
Terminal profiles management engine for code editor.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime


class ShellType(Enum):
    """Shell type."""
    BASH = "bash"
    ZSH = "zsh"
    FISH = "fish"
    POWERSHELL = "powershell"
    CMD = "cmd"
    SH = "sh"
    TCSH = "tcsh"
    CSH = "csh"


class ProfileScope(Enum):
    """Profile scope."""
    SESSION = "session"
    TERMINAL = "terminal"
    GLOBAL = "global"


class ProfileAction(Enum):
    """Profile action."""
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


@dataclass
class ProfileConfig:
    """Profile configuration."""
    persist_profiles: bool = True
    auto_load_profiles: bool = True
    show_notifications: bool = True
    log_changes: bool = True
    validate_profiles: bool = True


@dataclass
class ProfileEntry:
    """Profile entry."""
    id: str
    name: str
    shell_type: ShellType
    working_directory: str
    environment: Dict[str, str]
    aliases: Dict[str, str]
    shell_args: List[str]
    color_scheme: Optional[str] = None
    font_family: Optional[str] = None
    font_size: Optional[int] = None
    scope: ProfileScope = ProfileScope.SESSION
    timestamp: str = ""
    is_default: bool = False
    is_active: bool = False
    terminal_id: Optional[str] = None
    session_id: Optional[str] = None


@dataclass
class ProfileResult:
    """Profile result."""
    success: bool
    message: Optional[str] = None
    errors: List[str] = field(default_factory=list)
    profile_id: Optional[str] = None
    profile_name: Optional[str] = None
    action: Optional[str] = None


class TerminalProfilesEngine:
    """
    Terminal profiles management engine.
    
    Özellikler:
    - Create profile
    - Update profile
    - Delete profile
    - Get profile
    - List profiles
    - Activate profile
    - Clone profile
    - Import profile
    - Export profile
    - Set default profile
    - Profile scope (session, terminal, global)
    - Profile persistence
    - Profile validation
    - Profile history
    - Profile search/filter
    """
    
    def __init__(self, config: Optional[ProfileConfig] = None):
        """Initialize terminal profiles engine."""
        self.config = config or ProfileConfig()
        self.profiles: Dict[str, ProfileEntry] = {}
        self.profile_history: List[Dict[str, Any]] = []
        self._profile_counter = 0
        self._default_profile: Optional[str] = None
        self._active_profile: Optional[str] = None
    
    def create_profile(
        self,
        name: str,
        shell_type: ShellType,
        working_directory: str,
        environment: Optional[Dict[str, str]] = None,
        aliases: Optional[Dict[str, str]] = None,
        shell_args: Optional[List[str]] = None,
        color_scheme: Optional[str] = None,
        font_family: Optional[str] = None,
        font_size: Optional[int] = None,
        scope: ProfileScope = ProfileScope.SESSION,
        terminal_id: Optional[str] = None,
        session_id: Optional[str] = None
    ) -> ProfileResult:
        """
        Profil oluştur.
        
        Args:
            name: Profil adı
            shell_type: Shell tipi
            working_directory: Çalışma dizini
            environment: Ortam değişkenleri
            aliases: Aliaslar
            shell_args: Shell argümanları
            color_scheme: Renk şeması
            font_family: Font ailesi
            font_size: Font boyutu
            scope: Kapsam
            terminal_id: Terminal ID
            session_id: Oturum ID
            
        Returns:
            ProfileResult: Oluşturma sonucu
        """
        result = ProfileResult(success=False)
        result.action = ProfileAction.CREATE.value
        result.profile_name = name
        
        try:
            # Validate
            if self.config.validate_profiles:
                if not name or not isinstance(name, str):
                    result.errors.append("Invalid profile name")
                    return result
            
            # Create entry
            profile_id = f"profile_{self._profile_counter}"
            self._profile_counter += 1
            
            entry = ProfileEntry(
                id=profile_id,
                name=name,
                shell_type=shell_type,
                working_directory=working_directory,
                environment=environment or {},
                aliases=aliases or {},
                shell_args=shell_args or [],
                color_scheme=color_scheme,
                font_family=font_family,
                font_size=font_size,
                scope=scope,
                timestamp=self._get_timestamp(),
                terminal_id=terminal_id,
                session_id=session_id
            )
            
            # Store
            self.profiles[profile_id] = entry
            
            # Set as default if first profile
            if self._default_profile is None:
                self._default_profile = profile_id
                entry.is_default = True
            
            # Add to history
            if self.config.log_changes:
                self.profile_history.append({
                    "action": "create",
                    "profile_id": profile_id,
                    "name": name,
                    "scope": scope.value,
                    "timestamp": entry.timestamp
                })
            
            result.success = True
            result.profile_id = profile_id
            result.message = f"Profile {name} created"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def update_profile(
        self,
        profile_id: str,
        name: Optional[str] = None,
        shell_type: Optional[ShellType] = None,
        working_directory: Optional[str] = None,
        environment: Optional[Dict[str, str]] = None,
        aliases: Optional[Dict[str, str]] = None,
        shell_args: Optional[List[str]] = None,
        color_scheme: Optional[str] = None,
        font_family: Optional[str] = None,
        font_size: Optional[int] = None
    ) -> ProfileResult:
        """
        Profil güncelle.
        
        Args:
            profile_id: Profil ID
            name: Profil adı
            shell_type: Shell tipi
            working_directory: Çalışma dizini
            environment: Ortam değişkenleri
            aliases: Aliaslar
            shell_args: Shell argümanları
            color_scheme: Renk şeması
            font_family: Font ailesi
            font_size: Font boyutu
            
        Returns:
            ProfileResult: Güncelleme sonucu
        """
        result = ProfileResult(success=False)
        result.action = ProfileAction.UPDATE.value
        result.profile_id = profile_id
        
        try:
            if profile_id not in self.profiles:
                result.errors.append(f"Profile not found: {profile_id}")
                return result
            
            entry = self.profiles[profile_id]
            
            if name is not None:
                entry.name = name
                result.profile_name = name
            if shell_type is not None:
                entry.shell_type = shell_type
            if working_directory is not None:
                entry.working_directory = working_directory
            if environment is not None:
                entry.environment = environment
            if aliases is not None:
                entry.aliases = aliases
            if shell_args is not None:
                entry.shell_args = shell_args
            if color_scheme is not None:
                entry.color_scheme = color_scheme
            if font_family is not None:
                entry.font_family = font_family
            if font_size is not None:
                entry.font_size = font_size
            
            entry.timestamp = self._get_timestamp()
            
            # Add to history
            if self.config.log_changes:
                self.profile_history.append({
                    "action": "update",
                    "profile_id": profile_id,
                    "timestamp": entry.timestamp
                })
            
            result.success = True
            result.message = f"Profile {profile_id} updated"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def delete_profile(self, profile_id: str) -> ProfileResult:
        """
        Profil sil.
        
        Args:
            profile_id: Profil ID
            
        Returns:
            ProfileResult: Silme sonucu
        """
        result = ProfileResult(success=False)
        result.action = ProfileAction.DELETE.value
        result.profile_id = profile_id
        
        try:
            if profile_id not in self.profiles:
                result.errors.append(f"Profile not found: {profile_id}")
                return result
            
            entry = self.profiles[profile_id]
            name = entry.name
            
            del self.profiles[profile_id]
            
            # Reset default if deleted
            if self._default_profile == profile_id:
                self._default_profile = None
                # Set new default if available
                if self.profiles:
                    self._default_profile = list(self.profiles.keys())[0]
                    self.profiles[self._default_profile].is_default = True
            
            # Reset active if deleted
            if self._active_profile == profile_id:
                self._active_profile = None
            
            # Add to history
            if self.config.log_changes:
                self.profile_history.append({
                    "action": "delete",
                    "profile_id": profile_id,
                    "name": name,
                    "timestamp": self._get_timestamp()
                })
            
            result.success = True
            result.message = f"Profile {name} deleted"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_profile(self, profile_id: str) -> ProfileResult:
        """
        Profil al.
        
        Args:
            profile_id: Profil ID
            
        Returns:
            ProfileResult: Alma sonucu
        """
        result = ProfileResult(success=False)
        result.action = ProfileAction.GET.value
        result.profile_id = profile_id
        
        try:
            if profile_id not in self.profiles:
                result.errors.append(f"Profile not found: {profile_id}")
                return result
            
            entry = self.profiles[profile_id]
            result.success = True
            result.profile_name = entry.name
            result.message = f"Profile {profile_id} retrieved"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def list_profiles(
        self,
        scope: Optional[ProfileScope] = None,
        terminal_id: Optional[str] = None,
        session_id: Optional[str] = None
    ) -> ProfileResult:
        """
        Profilleri listele.
        
        Args:
            scope: Kapsam
            terminal_id: Terminal ID
            session_id: Oturum ID
            
        Returns:
            ProfileResult: Listeleme sonucu
        """
        result = ProfileResult(success=False)
        result.action = ProfileAction.LIST.value
        
        try:
            filtered = list(self.profiles.values())
            
            if scope:
                filtered = [p for p in filtered if p.scope == scope]
            
            if terminal_id:
                filtered = [p for p in filtered if p.terminal_id == terminal_id]
            
            if session_id:
                filtered = [p for p in filtered if p.session_id == session_id]
            
            result.success = True
            result.message = f"Listed {len(filtered)} profiles"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def activate_profile(self, profile_id: str) -> ProfileResult:
        """
        Profil aktifleştir.
        
        Args:
            profile_id: Profil ID
            
        Returns:
            ProfileResult: Aktifleştirme sonucu
        """
        result = ProfileResult(success=False)
        result.action = ProfileAction.ACTIVATE.value
        result.profile_id = profile_id
        
        try:
            if profile_id not in self.profiles:
                result.errors.append(f"Profile not found: {profile_id}")
                return result
            
            # Deactivate current
            if self._active_profile and self._active_profile in self.profiles:
                self.profiles[self._active_profile].is_active = False
            
            # Activate new
            self._active_profile = profile_id
            self.profiles[profile_id].is_active = True
            
            # Add to history
            if self.config.log_changes:
                self.profile_history.append({
                    "action": "activate",
                    "profile_id": profile_id,
                    "timestamp": self._get_timestamp()
                })
            
            result.success = True
            result.message = f"Profile {profile_id} activated"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def clone_profile(self, profile_id: str, new_name: str) -> ProfileResult:
        """
        Profil klonla.
        
        Args:
            profile_id: Profil ID
            new_name: Yeni ad
            
        Returns:
            ProfileResult: Klonlama sonucu
        """
        result = ProfileResult(success=False)
        result.action = ProfileAction.CLONE.value
        result.profile_id = profile_id
        
        try:
            if profile_id not in self.profiles:
                result.errors.append(f"Profile not found: {profile_id}")
                return result
            
            source = self.profiles[profile_id]
            
            # Create clone
            new_profile_id = f"profile_{self._profile_counter}"
            self._profile_counter += 1
            
            entry = ProfileEntry(
                id=new_profile_id,
                name=new_name,
                shell_type=source.shell_type,
                working_directory=source.working_directory,
                environment=source.environment.copy(),
                aliases=source.aliases.copy(),
                shell_args=source.shell_args.copy(),
                color_scheme=source.color_scheme,
                font_family=source.font_family,
                font_size=source.font_size,
                scope=source.scope,
                timestamp=self._get_timestamp(),
                terminal_id=source.terminal_id,
                session_id=source.session_id
            )
            
            self.profiles[new_profile_id] = entry
            
            # Add to history
            if self.config.log_changes:
                self.profile_history.append({
                    "action": "clone",
                    "source_profile_id": profile_id,
                    "new_profile_id": new_profile_id,
                    "new_name": new_name,
                    "timestamp": entry.timestamp
                })
            
            result.success = True
            result.profile_id = new_profile_id
            result.profile_name = new_name
            result.message = f"Profile cloned as {new_name}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def export_profile(self, profile_id: str, format: str = "json") -> ProfileResult:
        """
        Profil dışa aktar.
        
        Args:
            profile_id: Profil ID
            format: Format (json)
            
        Returns:
            ProfileResult: Dışa aktarma sonucu
        """
        result = ProfileResult(success=False)
        result.action = ProfileAction.EXPORT.value
        result.profile_id = profile_id
        
        try:
            if profile_id not in self.profiles:
                result.errors.append(f"Profile not found: {profile_id}")
                return result
            
            entry = self.profiles[profile_id]
            
            if format == "json":
                import json
                data = {
                    "name": entry.name,
                    "shell_type": entry.shell_type.value,
                    "working_directory": entry.working_directory,
                    "environment": entry.environment,
                    "aliases": entry.aliases,
                    "shell_args": entry.shell_args,
                    "color_scheme": entry.color_scheme,
                    "font_family": entry.font_family,
                    "font_size": entry.font_size,
                    "scope": entry.scope.value
                }
                result.success = True
                result.message = f"Profile {profile_id} exported as JSON"
            else:
                result.errors.append(f"Unsupported format: {format}")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def import_profile(self, data: Dict[str, Any], scope: ProfileScope = ProfileScope.SESSION) -> ProfileResult:
        """
        Profil içe aktar.
        
        Args:
            data: Veri
            scope: Kapsam
            
        Returns:
            ProfileResult: İçe aktarma sonucu
        """
        result = ProfileResult(success=False)
        result.action = ProfileAction.IMPORT.value
        
        try:
            name = data.get("name", "imported_profile")
            shell_type = ShellType(data.get("shell_type", "bash"))
            working_directory = data.get("working_directory", "")
            environment = data.get("environment", {})
            aliases = data.get("aliases", {})
            shell_args = data.get("shell_args", [])
            color_scheme = data.get("color_scheme")
            font_family = data.get("font_family")
            font_size = data.get("font_size")
            
            return self.create_profile(
                name=name,
                shell_type=shell_type,
                working_directory=working_directory,
                environment=environment,
                aliases=aliases,
                shell_args=shell_args,
                color_scheme=color_scheme,
                font_family=font_family,
                font_size=font_size,
                scope=scope
            )
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def set_default_profile(self, profile_id: str) -> ProfileResult:
        """
- Varsayılan profil ayarla.
        
        Args:
            profile_id: Profil ID
            
        Returns:
            ProfileResult: Ayarlama sonucu
        """
        result = ProfileResult(success=False)
        result.action = ProfileAction.SET_DEFAULT.value
        result.profile_id = profile_id
        
        try:
            if profile_id not in self.profiles:
                result.errors.append(f"Profile not found: {profile_id}")
                return result
            
            # Unset current default
            if self._default_profile and self._default_profile in self.profiles:
                self.profiles[self._default_profile].is_default = False
            
            # Set new default
            self._default_profile = profile_id
            self.profiles[profile_id].is_default = True
            
            # Add to history
            if self.config.log_changes:
                self.profile_history.append({
                    "action": "set_default",
                    "profile_id": profile_id,
                    "timestamp": self._get_timestamp()
                })
            
            result.success = True
            result.message = f"Profile {profile_id} set as default"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_profile_history(self) -> List[Dict[str, Any]]:
        """
        Profil geçmişini al.
        
        Returns:
            List[Dict[str, Any]]: Geçmiş
        """
        return self.profile_history
    
    def clear_history(self) -> ProfileResult:
        """
        Geçmişi temizle.
        
        Returns:
            ProfileResult: Temizleme sonucu
        """
        result = ProfileResult(success=False)
        
        try:
            self.profile_history.clear()
            result.success = True
            result.message = "Profile history cleared"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def update_config(self, config: ProfileConfig) -> ProfileResult:
        """
        Konfigürasyon güncelle.
        
        Args:
            config: Yeni konfigürasyon
            
        Returns:
            ProfileResult: Güncelleme sonucu
        """
        result = ProfileResult(success=False)
        
        try:
            self.config = config
            result.success = True
            result.message = "Config updated"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_config(self) -> ProfileConfig:
        """
        Konfigürasyon al.
        
        Returns:
            ProfileConfig: Konfigürasyon
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
    engine = TerminalProfilesEngine()
    
    print("Terminal Profiles Engine initialized")
    print(f"Persist profiles: {engine.config.persist_profiles}")
