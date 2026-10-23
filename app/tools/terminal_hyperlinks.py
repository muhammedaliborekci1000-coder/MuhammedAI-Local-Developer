"""
MuhammedAI Local Developer - Terminal Hyperlinks
Terminal hyperlinks management engine for code editor.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime


class HyperlinkType(Enum):
    """Hyperlink type."""
    URL = "url"
    FILE = "file"
    EMAIL = "email"
    COMMAND = "command"
    DIRECTORY = "directory"
    CUSTOM = "custom"


class HyperlinkScope(Enum):
    """Hyperlink scope."""
    SESSION = "session"
    TERMINAL = "terminal"
    GLOBAL = "global"


class HyperlinkAction(Enum):
    """Hyperlink action."""
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
    CLICK = "click"
    HOVER = "hover"
    RESET = "reset"


@dataclass
class HyperlinkConfig:
    """Hyperlink configuration."""
    persist_hyperlinks: bool = True
    auto_load_hyperlinks: bool = True
    show_notifications: bool = True
    log_changes: bool = True
    validate_hyperlinks: bool = True


@dataclass
class HyperlinkEntry:
    """Hyperlink entry."""
    id: str
    name: str
    link_type: HyperlinkType
    url: str
    text: str
    color: str
    underline: bool
    hover_color: Optional[str] = None
    hover_underline: Optional[bool] = None
    click_action: Optional[str] = None
    scope: HyperlinkScope = HyperlinkScope.SESSION
    timestamp: str = ""
    is_default: bool = False
    is_active: bool = False
    terminal_id: Optional[str] = None
    session_id: Optional[str] = None


@dataclass
class HyperlinkResult:
    """Hyperlink result."""
    success: bool
    message: Optional[str] = None
    errors: List[str] = field(default_factory=list)
    hyperlink_id: Optional[str] = None
    hyperlink_name: Optional[str] = None
    action: Optional[str] = None
    url: Optional[str] = None


class TerminalHyperlinksEngine:
    """
    Terminal hyperlinks management engine.
    
    Özellikler:
    - Create hyperlink
    - Update hyperlink
    - Delete hyperlink
    - Get hyperlink
    - List hyperlinks
    - Activate hyperlink
    - Clone hyperlink
    - Import hyperlink
    - Export hyperlink
    - Set default hyperlink
    - Click hyperlink
    - Hover hyperlink
    - Reset hyperlink
    - Hyperlink scope (session, terminal, global)
    - Hyperlink type management
    - Hyperlink URL management
    - Hyperlink text management
    - Hyperlink color management
    - Hyperlink underline management
    - Hyperlink hover management
    - Hyperlink click action
    - Hyperlink persistence
    - Hyperlink validation
    - Hyperlink history
    - Hyperlink search/filter
    """
    
    def __init__(self, config: Optional[HyperlinkConfig] = None):
        """Initialize terminal hyperlinks engine."""
        self.config = config or HyperlinkConfig()
        self.hyperlinks: Dict[str, HyperlinkEntry] = {}
        self.hyperlink_history: List[Dict[str, Any]] = []
        self._hyperlink_counter = 0
        self._default_hyperlink: Optional[str] = None
        self._active_hyperlink: Optional[str] = None
    
    def create_hyperlink(
        self,
        name: str,
        link_type: HyperlinkType = HyperlinkType.URL,
        url: str = "",
        text: str = "",
        color: str = "#00ff00",
        underline: bool = True,
        hover_color: Optional[str] = None,
        hover_underline: Optional[bool] = None,
        click_action: Optional[str] = None,
        scope: HyperlinkScope = HyperlinkScope.SESSION,
        terminal_id: Optional[str] = None,
        session_id: Optional[str] = None
    ) -> HyperlinkResult:
        """
        Hyperlink oluştur.
        
        Args:
            name: Hyperlink adı
            link_type: Hyperlink tipi
            url: URL
            text: Metin
            color: Renk
            underline: Alt çizgi
            hover_color: Hover rengi
            hover_underline: Hover alt çizgi
            click_action: Tıklama eylemi
            scope: Kapsam
            terminal_id: Terminal ID
            session_id: Oturum ID
            
        Returns:
            HyperlinkResult: Oluşturma sonucu
        """
        result = HyperlinkResult(success=False)
        result.action = HyperlinkAction.CREATE.value
        result.hyperlink_name = name
        
        try:
            # Validate
            if self.config.validate_hyperlinks:
                if not name or not isinstance(name, str):
                    result.errors.append("Invalid hyperlink name")
                    return result
                if link_type == HyperlinkType.URL and not url:
                    result.errors.append("URL is required for URL type")
                    return result
            
            # Create entry
            hyperlink_id = f"hyperlink_{self._hyperlink_counter}"
            self._hyperlink_counter += 1
            
            entry = HyperlinkEntry(
                id=hyperlink_id,
                name=name,
                link_type=link_type,
                url=url,
                text=text,
                color=color,
                underline=underline,
                hover_color=hover_color,
                hover_underline=hover_underline,
                click_action=click_action,
                scope=scope,
                timestamp=self._get_timestamp(),
                terminal_id=terminal_id,
                session_id=session_id
            )
            
            # Store
            self.hyperlinks[hyperlink_id] = entry
            
            # Set as default if first hyperlink
            if self._default_hyperlink is None:
                self._default_hyperlink = hyperlink_id
                entry.is_default = True
            
            # Add to history
            if self.config.log_changes:
                self.hyperlink_history.append({
                    "action": "create",
                    "hyperlink_id": hyperlink_id,
                    "name": name,
                    "scope": scope.value,
                    "timestamp": entry.timestamp
                })
            
            result.success = True
            result.hyperlink_id = hyperlink_id
            result.url = url
            result.message = f"Hyperlink {name} created"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def update_hyperlink(
        self,
        hyperlink_id: str,
        name: Optional[str] = None,
        link_type: Optional[HyperlinkType] = None,
        url: Optional[str] = None,
        text: Optional[str] = None,
        color: Optional[str] = None,
        underline: Optional[bool] = None,
        hover_color: Optional[str] = None,
        hover_underline: Optional[bool] = None,
        click_action: Optional[str] = None
    ) -> HyperlinkResult:
        """
        Hyperlink güncelle.
        
        Args:
            hyperlink_id: Hyperlink ID
            name: Hyperlink adı
            link_type: Hyperlink tipi
            url: URL
            text: Metin
            color: Renk
            underline: Alt çizgi
            hover_color: Hover rengi
            hover_underline: Hover alt çizgi
            click_action: Tıklama eylemi
            
        Returns:
            HyperlinkResult: Güncelleme sonucu
        """
        result = HyperlinkResult(success=False)
        result.action = HyperlinkAction.UPDATE.value
        result.hyperlink_id = hyperlink_id
        
        try:
            if hyperlink_id not in self.hyperlinks:
                result.errors.append(f"Hyperlink not found: {hyperlink_id}")
                return result
            
            entry = self.hyperlinks[hyperlink_id]
            
            if name is not None:
                entry.name = name
                result.hyperlink_name = name
            if link_type is not None:
                entry.link_type = link_type
            if url is not None:
                entry.url = url
                result.url = url
            if text is not None:
                entry.text = text
            if color is not None:
                entry.color = color
            if underline is not None:
                entry.underline = underline
            if hover_color is not None:
                entry.hover_color = hover_color
            if hover_underline is not None:
                entry.hover_underline = hover_underline
            if click_action is not None:
                entry.click_action = click_action
            
            entry.timestamp = self._get_timestamp()
            
            # Add to history
            if self.config.log_changes:
                self.hyperlink_history.append({
                    "action": "update",
                    "hyperlink_id": hyperlink_id,
                    "timestamp": entry.timestamp
                })
            
            result.success = True
            result.message = f"Hyperlink {hyperlink_id} updated"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def delete_hyperlink(self, hyperlink_id: str) -> HyperlinkResult:
        """
        Hyperlink sil.
        
        Args:
            hyperlink_id: Hyperlink ID
            
        Returns:
            HyperlinkResult: Silme sonucu
        """
        result = HyperlinkResult(success=False)
        result.action = HyperlinkAction.DELETE.value
        result.hyperlink_id = hyperlink_id
        
        try:
            if hyperlink_id not in self.hyperlinks:
                result.errors.append(f"Hyperlink not found: {hyperlink_id}")
                return result
            
            entry = self.hyperlinks[hyperlink_id]
            name = entry.name
            
            del self.hyperlinks[hyperlink_id]
            
            # Reset default if deleted
            if self._default_hyperlink == hyperlink_id:
                self._default_hyperlink = None
                # Set new default if available
                if self.hyperlinks:
                    self._default_hyperlink = list(self.hyperlinks.keys())[0]
                    self.hyperlinks[self._default_hyperlink].is_default = True
            
            # Reset active if deleted
            if self._active_hyperlink == hyperlink_id:
                self._active_hyperlink = None
            
            # Add to history
            if self.config.log_changes:
                self.hyperlink_history.append({
                    "action": "delete",
                    "hyperlink_id": hyperlink_id,
                    "name": name,
                    "timestamp": self._get_timestamp()
                })
            
            result.success = True
            result.message = f"Hyperlink {name} deleted"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_hyperlink(self, hyperlink_id: str) -> HyperlinkResult:
        """
        Hyperlink al.
        
        Args:
            hyperlink_id: Hyperlink ID
            
        Returns:
            HyperlinkResult: Alma sonucu
        """
        result = HyperlinkResult(success=False)
        result.action = HyperlinkAction.GET.value
        result.hyperlink_id = hyperlink_id
        
        try:
            if hyperlink_id not in self.hyperlinks:
                result.errors.append(f"Hyperlink not found: {hyperlink_id}")
                return result
            
            entry = self.hyperlinks[hyperlink_id]
            result.success = True
            result.hyperlink_name = entry.name
            result.url = entry.url
            result.message = f"Hyperlink {hyperlink_id} retrieved"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def list_hyperlinks(
        self,
        scope: Optional[HyperlinkScope] = None,
        terminal_id: Optional[str] = None,
        session_id: Optional[str] = None
    ) -> HyperlinkResult:
        """
        Hyperlinkleri listele.
        
        Args:
            scope: Kapsam
            terminal_id: Terminal ID
            session_id: Oturum ID
            
        Returns:
            HyperlinkResult: Listeleme sonucu
        """
        result = HyperlinkResult(success=False)
        result.action = HyperlinkAction.LIST.value
        
        try:
            filtered = list(self.hyperlinks.values())
            
            if scope:
                filtered = [h for h in filtered if h.scope == scope]
            
            if terminal_id:
                filtered = [h for h in filtered if h.terminal_id == terminal_id]
            
            if session_id:
                filtered = [h for h in filtered if h.session_id == session_id]
            
            result.success = True
            result.message = f"Listed {len(filtered)} hyperlinks"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def activate_hyperlink(self, hyperlink_id: str) -> HyperlinkResult:
        """
        Hyperlink aktifleştir.
        
        Args:
            hyperlink_id: Hyperlink ID
            
        Returns:
            HyperlinkResult: Aktifleştirme sonucu
        """
        result = HyperlinkResult(success=False)
        result.action = HyperlinkAction.ACTIVATE.value
        result.hyperlink_id = hyperlink_id
        
        try:
            if hyperlink_id not in self.hyperlinks:
                result.errors.append(f"Hyperlink not found: {hyperlink_id}")
                return result
            
            # Deactivate current
            if self._active_hyperlink and self._active_hyperlink in self.hyperlinks:
                self.hyperlinks[self._active_hyperlink].is_active = False
            
            # Activate new
            self._active_hyperlink = hyperlink_id
            self.hyperlinks[hyperlink_id].is_active = True
            
            # Add to history
            if self.config.log_changes:
                self.hyperlink_history.append({
                    "action": "activate",
                    "hyperlink_id": hyperlink_id,
                    "timestamp": self._get_timestamp()
                })
            
            result.success = True
            result.message = f"Hyperlink {hyperlink_id} activated"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def clone_hyperlink(self, hyperlink_id: str, new_name: str) -> HyperlinkResult:
        """
        Hyperlink klonla.
        
        Args:
            hyperlink_id: Hyperlink ID
            new_name: Yeni ad
            
        Returns:
            HyperlinkResult: Klonlama sonucu
        """
        result = HyperlinkResult(success=False)
        result.action = HyperlinkAction.CLONE.value
        result.hyperlink_id = hyperlink_id
        
        try:
            if hyperlink_id not in self.hyperlinks:
                result.errors.append(f"Hyperlink not found: {hyperlink_id}")
                return result
            
            source = self.hyperlinks[hyperlink_id]
            
            # Create clone
            new_hyperlink_id = f"hyperlink_{self._hyperlink_counter}"
            self._hyperlink_counter += 1
            
            entry = HyperlinkEntry(
                id=new_hyperlink_id,
                name=new_name,
                link_type=source.link_type,
                url=source.url,
                text=source.text,
                color=source.color,
                underline=source.underline,
                hover_color=source.hover_color,
                hover_underline=source.hover_underline,
                click_action=source.click_action,
                scope=source.scope,
                timestamp=self._get_timestamp(),
                terminal_id=source.terminal_id,
                session_id=source.session_id
            )
            
            self.hyperlinks[new_hyperlink_id] = entry
            
            # Add to history
            if self.config.log_changes:
                self.hyperlink_history.append({
                    "action": "clone",
                    "source_hyperlink_id": hyperlink_id,
                    "new_hyperlink_id": new_hyperlink_id,
                    "new_name": new_name,
                    "timestamp": entry.timestamp
                })
            
            result.success = True
            result.hyperlink_id = new_hyperlink_id
            result.hyperlink_name = new_name
            result.message = f"Hyperlink cloned as {new_name}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def export_hyperlink(self, hyperlink_id: str, format: str = "json") -> HyperlinkResult:
        """
        Hyperlink dışa aktar.
        
        Args:
            hyperlink_id: Hyperlink ID
            format: Format (json)
            
        Returns:
            HyperlinkResult: Dışa aktarma sonucu
        """
        result = HyperlinkResult(success=False)
        result.action = HyperlinkAction.EXPORT.value
        result.hyperlink_id = hyperlink_id
        
        try:
            if hyperlink_id not in self.hyperlinks:
                result.errors.append(f"Hyperlink not found: {hyperlink_id}")
                return result
            
            entry = self.hyperlinks[hyperlink_id]
            
            if format == "json":
                import json
                data = {
                    "name": entry.name,
                    "link_type": entry.link_type.value,
                    "url": entry.url,
                    "text": entry.text,
                    "color": entry.color,
                    "underline": entry.underline,
                    "hover_color": entry.hover_color,
                    "hover_underline": entry.hover_underline,
                    "click_action": entry.click_action,
                    "scope": entry.scope.value
                }
                result.success = True
                result.message = f"Hyperlink {hyperlink_id} exported as JSON"
            else:
                result.errors.append(f"Unsupported format: {format}")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def import_hyperlink(self, data: Dict[str, Any], scope: HyperlinkScope = HyperlinkScope.SESSION) -> HyperlinkResult:
        """
        Hyperlink içe aktar.
        
        Args:
            data: Veri
            scope: Kapsam
            
        Returns:
            HyperlinkResult: İçe aktarma sonucu
        """
        result = HyperlinkResult(success=False)
        result.action = HyperlinkAction.IMPORT.value
        
        try:
            name = data.get("name", "imported_hyperlink")
            link_type = HyperlinkType(data.get("link_type", "url"))
            url = data.get("url", "")
            text = data.get("text", "")
            color = data.get("color", "#00ff00")
            underline = data.get("underline", True)
            hover_color = data.get("hover_color")
            hover_underline = data.get("hover_underline")
            click_action = data.get("click_action")
            
            return self.create_hyperlink(
                name=name,
                link_type=link_type,
                url=url,
                text=text,
                color=color,
                underline=underline,
                hover_color=hover_color,
                hover_underline=hover_underline,
                click_action=click_action,
                scope=scope
            )
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def set_default_hyperlink(self, hyperlink_id: str) -> HyperlinkResult:
        """
        Varsayılan hyperlink ayarla.
        
        Args:
            hyperlink_id: Hyperlink ID
            
        Returns:
            HyperlinkResult: Ayarlama sonucu
        """
        result = HyperlinkResult(success=False)
        result.action = HyperlinkAction.SET_DEFAULT.value
        result.hyperlink_id = hyperlink_id
        
        try:
            if hyperlink_id not in self.hyperlinks:
                result.errors.append(f"Hyperlink not found: {hyperlink_id}")
                return result
            
            # Unset current default
            if self._default_hyperlink and self._default_hyperlink in self.hyperlinks:
                self.hyperlinks[self._default_hyperlink].is_default = False
            
            # Set new default
            self._default_hyperlink = hyperlink_id
            self.hyperlinks[hyperlink_id].is_default = True
            
            # Add to history
            if self.config.log_changes:
                self.hyperlink_history.append({
                    "action": "set_default",
                    "hyperlink_id": hyperlink_id,
                    "timestamp": self._get_timestamp()
                })
            
            result.success = True
            result.message = f"Hyperlink {hyperlink_id} set as default"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def click_hyperlink(self, hyperlink_id: str) -> HyperlinkResult:
        """
        Hyperlink tıkla.
        
        Args:
            hyperlink_id: Hyperlink ID
            
        Returns:
            HyperlinkResult: Tıklama sonucu
        """
        result = HyperlinkResult(success=False)
        result.action = HyperlinkAction.CLICK.value
        result.hyperlink_id = hyperlink_id
        
        try:
            if hyperlink_id not in self.hyperlinks:
                result.errors.append(f"Hyperlink not found: {hyperlink_id}")
                return result
            
            entry = self.hyperlinks[hyperlink_id]
            result.url = entry.url
            
            # Add to history
            if self.config.log_changes:
                self.hyperlink_history.append({
                    "action": "click",
                    "hyperlink_id": hyperlink_id,
                    "url": entry.url,
                    "timestamp": self._get_timestamp()
                })
            
            result.success = True
            result.message = f"Hyperlink {hyperlink_id} clicked"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def hover_hyperlink(self, hyperlink_id: str) -> HyperlinkResult:
        """
        Hyperlink hover.
        
        Args:
            hyperlink_id: Hyperlink ID
            
        Returns:
            HyperlinkResult: Hover sonucu
        """
        result = HyperlinkResult(success=False)
        result.action = HyperlinkAction.HOVER.value
        result.hyperlink_id = hyperlink_id
        
        try:
            if hyperlink_id not in self.hyperlinks:
                result.errors.append(f"Hyperlink not found: {hyperlink_id}")
                return result
            
            entry = self.hyperlinks[hyperlink_id]
            
            # Add to history
            if self.config.log_changes:
                self.hyperlink_history.append({
                    "action": "hover",
                    "hyperlink_id": hyperlink_id,
                    "timestamp": self._get_timestamp()
                })
            
            result.success = True
            result.message = f"Hyperlink {hyperlink_id} hovered"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def reset_hyperlink(self, hyperlink_id: str) -> HyperlinkResult:
        """
        Hyperlink sıfırla.
        
        Args:
            hyperlink_id: Hyperlink ID
            
        Returns:
            HyperlinkResult: Sıfırlama sonucu
        """
        result = HyperlinkResult(success=False)
        result.action = HyperlinkAction.RESET.value
        result.hyperlink_id = hyperlink_id
        
        try:
            if hyperlink_id not in self.hyperlinks:
                result.errors.append(f"Hyperlink not found: {hyperlink_id}")
                return result
            
            entry = self.hyperlinks[hyperlink_id]
            
            # Reset to defaults
            entry.link_type = HyperlinkType.URL
            entry.color = "#00ff00"
            entry.underline = True
            entry.hover_color = None
            entry.hover_underline = None
            entry.click_action = None
            entry.timestamp = self._get_timestamp()
            
            # Add to history
            if self.config.log_changes:
                self.hyperlink_history.append({
                    "action": "reset",
                    "hyperlink_id": hyperlink_id,
                    "timestamp": entry.timestamp
                })
            
            result.success = True
            result.message = f"Hyperlink {hyperlink_id} reset"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_hyperlink_history(self) -> List[Dict[str, Any]]:
        """
        Hyperlink geçmişini al.
        
        Returns:
            List[Dict[str, Any]]: Geçmiş
        """
        return self.hyperlink_history
    
    def clear_history(self) -> HyperlinkResult:
        """
        Geçmişi temizle.
        
        Returns:
            HyperlinkResult: Temizleme sonucu
        """
        result = HyperlinkResult(success=False)
        
        try:
            self.hyperlink_history.clear()
            result.success = True
            result.message = "Hyperlink history cleared"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def update_config(self, config: HyperlinkConfig) -> HyperlinkResult:
        """
        Konfigürasyon güncelle.
        
        Args:
            config: Yeni konfigürasyon
            
        Returns:
            HyperlinkResult: Güncelleme sonucu
        """
        result = HyperlinkResult(success=False)
        
        try:
            self.config = config
            result.success = True
            result.message = "Config updated"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_config(self) -> HyperlinkConfig:
        """
        Konfigürasyon al.
        
        Returns:
            HyperlinkConfig: Konfigürasyon
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
    engine = TerminalHyperlinksEngine()
    
    print("Terminal Hyperlinks Engine initialized")
    print(f"Persist hyperlinks: {engine.config.persist_hyperlinks}")
