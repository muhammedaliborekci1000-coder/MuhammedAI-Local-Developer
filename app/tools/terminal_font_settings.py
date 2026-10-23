"""
MuhammedAI Local Developer - Terminal Font Settings
Terminal font settings management engine for code editor.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime


class FontWeight(Enum):
    """Font weight."""
    THIN = "thin"
    EXTRA_LIGHT = "extra_light"
    LIGHT = "light"
    NORMAL = "normal"
    MEDIUM = "medium"
    SEMI_BOLD = "semi_bold"
    BOLD = "bold"
    EXTRA_BOLD = "extra_bold"
    BLACK = "black"


class FontStyle(Enum):
    """Font style."""
    NORMAL = "normal"
    ITALIC = "italic"
    OBLIQUE = "oblique"


class FontScope(Enum):
    """Font scope."""
    SESSION = "session"
    TERMINAL = "terminal"
    GLOBAL = "global"


class FontAction(Enum):
    """Font action."""
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
    RESET = "reset"


@dataclass
class FontConfig:
    """Font configuration."""
    persist_fonts: bool = True
    auto_load_fonts: bool = True
    show_notifications: bool = True
    log_changes: bool = True
    validate_fonts: bool = True


@dataclass
class FontEntry:
    """Font entry."""
    id: str
    name: str
    family: str
    size: int
    weight: FontWeight
    style: FontStyle
    line_height: float
    letter_spacing: float
    word_spacing: float
    font_smoothing: Optional[str] = None
    antialiasing: Optional[bool] = None
    ligatures: Optional[bool] = None
    fallback_fonts: Optional[List[str]] = None
    scope: FontScope = FontScope.SESSION
    timestamp: str = ""
    is_default: bool = False
    is_active: bool = False
    terminal_id: Optional[str] = None
    session_id: Optional[str] = None


@dataclass
class FontResult:
    """Font result."""
    success: bool
    message: Optional[str] = None
    errors: List[str] = field(default_factory=list)
    font_id: Optional[str] = None
    font_name: Optional[str] = None
    action: Optional[str] = None


class TerminalFontSettingsEngine:
    """
    Terminal font settings management engine.
    
    Özellikler:
    - Create font setting
    - Update font setting
    - Delete font setting
    - Get font setting
    - List font settings
    - Activate font setting
    - Clone font setting
    - Import font setting
    - Export font setting
    - Set default font setting
    - Reset font setting
    - Font scope (session, terminal, global)
    - Font family management
    - Font size management
    - Font weight management
    - Font style management
    - Line height management
    - Letter spacing management
    - Word spacing management
    - Font smoothing
    - Antialiasing
    - Ligatures
    - Fallback fonts
    - Font persistence
    - Font validation
    - Font history
    - Font search/filter
    """
    
    def __init__(self, config: Optional[FontConfig] = None):
        """Initialize terminal font settings engine."""
        self.config = config or FontConfig()
        self.fonts: Dict[str, FontEntry] = {}
        self.font_history: List[Dict[str, Any]] = []
        self._font_counter = 0
        self._default_font: Optional[str] = None
        self._active_font: Optional[str] = None
    
    def create_font_setting(
        self,
        name: str,
        family: str,
        size: int,
        weight: FontWeight = FontWeight.NORMAL,
        style: FontStyle = FontStyle.NORMAL,
        line_height: float = 1.0,
        letter_spacing: float = 0.0,
        word_spacing: float = 0.0,
        font_smoothing: Optional[str] = None,
        antialiasing: Optional[bool] = None,
        ligatures: Optional[bool] = None,
        fallback_fonts: Optional[List[str]] = None,
        scope: FontScope = FontScope.SESSION,
        terminal_id: Optional[str] = None,
        session_id: Optional[str] = None
    ) -> FontResult:
        """
        Font ayarı oluştur.
        
        Args:
            name: Font adı
            family: Font ailesi
            size: Font boyutu
            weight: Font ağırlığı
            style: Font stili
            line_height: Satır yüksekliği
            letter_spacing: Harf aralığı
            word_spacing: Kelime aralığı
            font_smoothing: Font yumuşatma
            antialiasing: Kenar yumuşatma
            ligatures: Ligatürler
            fallback_fonts: Yedek fontlar
            scope: Kapsam
            terminal_id: Terminal ID
            session_id: Oturum ID
            
        Returns:
            FontResult: Oluşturma sonucu
        """
        result = FontResult(success=False)
        result.action = FontAction.CREATE.value
        result.font_name = name
        
        try:
            # Validate
            if self.config.validate_fonts:
                if not name or not isinstance(name, str):
                    result.errors.append("Invalid font name")
                    return result
                if not family or not isinstance(family, str):
                    result.errors.append("Invalid font family")
                    return result
                if size <= 0:
                    result.errors.append("Invalid font size")
                    return result
            
            # Create entry
            font_id = f"font_{self._font_counter}"
            self._font_counter += 1
            
            entry = FontEntry(
                id=font_id,
                name=name,
                family=family,
                size=size,
                weight=weight,
                style=style,
                line_height=line_height,
                letter_spacing=letter_spacing,
                word_spacing=word_spacing,
                font_smoothing=font_smoothing,
                antialiasing=antialiasing,
                ligatures=ligatures,
                fallback_fonts=fallback_fonts,
                scope=scope,
                timestamp=self._get_timestamp(),
                terminal_id=terminal_id,
                session_id=session_id
            )
            
            # Store
            self.fonts[font_id] = entry
            
            # Set as default if first font
            if self._default_font is None:
                self._default_font = font_id
                entry.is_default = True
            
            # Add to history
            if self.config.log_changes:
                self.font_history.append({
                    "action": "create",
                    "font_id": font_id,
                    "name": name,
                    "scope": scope.value,
                    "timestamp": entry.timestamp
                })
            
            result.success = True
            result.font_id = font_id
            result.message = f"Font setting {name} created"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def update_font_setting(
        self,
        font_id: str,
        name: Optional[str] = None,
        family: Optional[str] = None,
        size: Optional[int] = None,
        weight: Optional[FontWeight] = None,
        style: Optional[FontStyle] = None,
        line_height: Optional[float] = None,
        letter_spacing: Optional[float] = None,
        word_spacing: Optional[float] = None,
        font_smoothing: Optional[str] = None,
        antialiasing: Optional[bool] = None,
        ligatures: Optional[bool] = None,
        fallback_fonts: Optional[List[str]] = None
    ) -> FontResult:
        """
        Font ayarı güncelle.
        
        Args:
            font_id: Font ID
            name: Font adı
            family: Font ailesi
            size: Font boyutu
            weight: Font ağırlığı
            style: Font stili
            line_height: Satır yüksekliği
            letter_spacing: Harf aralığı
            word_spacing: Kelime aralığı
            font_smoothing: Font yumuşatma
            antialiasing: Kenar yumuşatma
            ligatures: Ligatürler
            fallback_fonts: Yedek fontlar
            
        Returns:
            FontResult: Güncelleme sonucu
        """
        result = FontResult(success=False)
        result.action = FontAction.UPDATE.value
        result.font_id = font_id
        
        try:
            if font_id not in self.fonts:
                result.errors.append(f"Font setting not found: {font_id}")
                return result
            
            entry = self.fonts[font_id]
            
            if name is not None:
                entry.name = name
                result.font_name = name
            if family is not None:
                entry.family = family
            if size is not None:
                entry.size = size
            if weight is not None:
                entry.weight = weight
            if style is not None:
                entry.style = style
            if line_height is not None:
                entry.line_height = line_height
            if letter_spacing is not None:
                entry.letter_spacing = letter_spacing
            if word_spacing is not None:
                entry.word_spacing = word_spacing
            if font_smoothing is not None:
                entry.font_smoothing = font_smoothing
            if antialiasing is not None:
                entry.antialiasing = antialiasing
            if ligatures is not None:
                entry.ligatures = ligatures
            if fallback_fonts is not None:
                entry.fallback_fonts = fallback_fonts
            
            entry.timestamp = self._get_timestamp()
            
            # Add to history
            if self.config.log_changes:
                self.font_history.append({
                    "action": "update",
                    "font_id": font_id,
                    "timestamp": entry.timestamp
                })
            
            result.success = True
            result.message = f"Font setting {font_id} updated"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def delete_font_setting(self, font_id: str) -> FontResult:
        """
        Font ayarı sil.
        
        Args:
            font_id: Font ID
            
        Returns:
            FontResult: Silme sonucu
        """
        result = FontResult(success=False)
        result.action = FontAction.DELETE.value
        result.font_id = font_id
        
        try:
            if font_id not in self.fonts:
                result.errors.append(f"Font setting not found: {font_id}")
                return result
            
            entry = self.fonts[font_id]
            name = entry.name
            
            del self.fonts[font_id]
            
            # Reset default if deleted
            if self._default_font == font_id:
                self._default_font = None
                # Set new default if available
                if self.fonts:
                    self._default_font = list(self.fonts.keys())[0]
                    self.fonts[self._default_font].is_default = True
            
            # Reset active if deleted
            if self._active_font == font_id:
                self._active_font = None
            
            # Add to history
            if self.config.log_changes:
                self.font_history.append({
                    "action": "delete",
                    "font_id": font_id,
                    "name": name,
                    "timestamp": self._get_timestamp()
                })
            
            result.success = True
            result.message = f"Font setting {name} deleted"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_font_setting(self, font_id: str) -> FontResult:
        """
        Font ayarı al.
        
        Args:
            font_id: Font ID
            
        Returns:
            FontResult: Alma sonucu
        """
        result = FontResult(success=False)
        result.action = FontAction.GET.value
        result.font_id = font_id
        
        try:
            if font_id not in self.fonts:
                result.errors.append(f"Font setting not found: {font_id}")
                return result
            
            entry = self.fonts[font_id]
            result.success = True
            result.font_name = entry.name
            result.message = f"Font setting {font_id} retrieved"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def list_font_settings(
        self,
        scope: Optional[FontScope] = None,
        terminal_id: Optional[str] = None,
        session_id: Optional[str] = None
    ) -> FontResult:
        """
        Font ayarlarını listele.
        
        Args:
            scope: Kapsam
            terminal_id: Terminal ID
            session_id: Oturum ID
            
        Returns:
            FontResult: Listeleme sonucu
        """
        result = FontResult(success=False)
        result.action = FontAction.LIST.value
        
        try:
            filtered = list(self.fonts.values())
            
            if scope:
                filtered = [f for f in filtered if f.scope == scope]
            
            if terminal_id:
                filtered = [f for f in filtered if f.terminal_id == terminal_id]
            
            if session_id:
                filtered = [f for f in filtered if f.session_id == session_id]
            
            result.success = True
            result.message = f"Listed {len(filtered)} font settings"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def activate_font_setting(self, font_id: str) -> FontResult:
        """
        Font ayarı aktifleştir.
        
        Args:
            font_id: Font ID
            
        Returns:
            FontResult: Aktifleştirme sonucu
        """
        result = FontResult(success=False)
        result.action = FontAction.ACTIVATE.value
        result.font_id = font_id
        
        try:
            if font_id not in self.fonts:
                result.errors.append(f"Font setting not found: {font_id}")
                return result
            
            # Deactivate current
            if self._active_font and self._active_font in self.fonts:
                self.fonts[self._active_font].is_active = False
            
            # Activate new
            self._active_font = font_id
            self.fonts[font_id].is_active = True
            
            # Add to history
            if self.config.log_changes:
                self.font_history.append({
                    "action": "activate",
                    "font_id": font_id,
                    "timestamp": self._get_timestamp()
                })
            
            result.success = True
            result.message = f"Font setting {font_id} activated"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def clone_font_setting(self, font_id: str, new_name: str) -> FontResult:
        """
        Font ayarı klonla.
        
        Args:
            font_id: Font ID
            new_name: Yeni ad
            
        Returns:
            FontResult: Klonlama sonucu
        """
        result = FontResult(success=False)
        result.action = FontAction.CLONE.value
        result.font_id = font_id
        
        try:
            if font_id not in self.fonts:
                result.errors.append(f"Font setting not found: {font_id}")
                return result
            
            source = self.fonts[font_id]
            
            # Create clone
            new_font_id = f"font_{self._font_counter}"
            self._font_counter += 1
            
            entry = FontEntry(
                id=new_font_id,
                name=new_name,
                family=source.family,
                size=source.size,
                weight=source.weight,
                style=source.style,
                line_height=source.line_height,
                letter_spacing=source.letter_spacing,
                word_spacing=source.word_spacing,
                font_smoothing=source.font_smoothing,
                antialiasing=source.antialiasing,
                ligatures=source.ligatures,
                fallback_fonts=source.fallback_fonts.copy() if source.fallback_fonts else None,
                scope=source.scope,
                timestamp=self._get_timestamp(),
                terminal_id=source.terminal_id,
                session_id=source.session_id
            )
            
            self.fonts[new_font_id] = entry
            
            # Add to history
            if self.config.log_changes:
                self.font_history.append({
                    "action": "clone",
                    "source_font_id": font_id,
                    "new_font_id": new_font_id,
                    "new_name": new_name,
                    "timestamp": entry.timestamp
                })
            
            result.success = True
            result.font_id = new_font_id
            result.font_name = new_name
            result.message = f"Font setting cloned as {new_name}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def export_font_setting(self, font_id: str, format: str = "json") -> FontResult:
        """
        Font ayarı dışa aktar.
        
        Args:
            font_id: Font ID
            format: Format (json)
            
        Returns:
            FontResult: Dışa aktarma sonucu
        """
        result = FontResult(success=False)
        result.action = FontAction.EXPORT.value
        result.font_id = font_id
        
        try:
            if font_id not in self.fonts:
                result.errors.append(f"Font setting not found: {font_id}")
                return result
            
            entry = self.fonts[font_id]
            
            if format == "json":
                import json
                data = {
                    "name": entry.name,
                    "family": entry.family,
                    "size": entry.size,
                    "weight": entry.weight.value,
                    "style": entry.style.value,
                    "line_height": entry.line_height,
                    "letter_spacing": entry.letter_spacing,
                    "word_spacing": entry.word_spacing,
                    "font_smoothing": entry.font_smoothing,
                    "antialiasing": entry.antialiasing,
                    "ligatures": entry.ligatures,
                    "fallback_fonts": entry.fallback_fonts,
                    "scope": entry.scope.value
                }
                result.success = True
                result.message = f"Font setting {font_id} exported as JSON"
            else:
                result.errors.append(f"Unsupported format: {format}")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def import_font_setting(self, data: Dict[str, Any], scope: FontScope = FontScope.SESSION) -> FontResult:
        """
        Font ayarı içe aktar.
        
        Args:
            data: Veri
            scope: Kapsam
            
        Returns:
            FontResult: İçe aktarma sonucu
        """
        result = FontResult(success=False)
        result.action = FontAction.IMPORT.value
        
        try:
            name = data.get("name", "imported_font")
            family = data.get("family", "monospace")
            size = data.get("size", 12)
            weight = FontWeight(data.get("weight", "normal"))
            style = FontStyle(data.get("style", "normal"))
            line_height = data.get("line_height", 1.0)
            letter_spacing = data.get("letter_spacing", 0.0)
            word_spacing = data.get("word_spacing", 0.0)
            font_smoothing = data.get("font_smoothing")
            antialiasing = data.get("antialiasing")
            ligatures = data.get("ligatures")
            fallback_fonts = data.get("fallback_fonts")
            
            return self.create_font_setting(
                name=name,
                family=family,
                size=size,
                weight=weight,
                style=style,
                line_height=line_height,
                letter_spacing=letter_spacing,
                word_spacing=word_spacing,
                font_smoothing=font_smoothing,
                antialiasing=antialiasing,
                ligatures=ligatures,
                fallback_fonts=fallback_fonts,
                scope=scope
            )
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def set_default_font_setting(self, font_id: str) -> FontResult:
        """
        Varsayılan font ayarı ayarla.
        
        Args:
            font_id: Font ID
            
        Returns:
            FontResult: Ayarlama sonucu
        """
        result = FontResult(success=False)
        result.action = FontAction.SET_DEFAULT.value
        result.font_id = font_id
        
        try:
            if font_id not in self.fonts:
                result.errors.append(f"Font setting not found: {font_id}")
                return result
            
            # Unset current default
            if self._default_font and self._default_font in self.fonts:
                self.fonts[self._default_font].is_default = False
            
            # Set new default
            self._default_font = font_id
            self.fonts[font_id].is_default = True
            
            # Add to history
            if self.config.log_changes:
                self.font_history.append({
                    "action": "set_default",
                    "font_id": font_id,
                    "timestamp": self._get_timestamp()
                })
            
            result.success = True
            result.message = f"Font setting {font_id} set as default"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def reset_font_setting(self, font_id: str) -> FontResult:
        """
        Font ayarı sıfırla.
        
        Args:
            font_id: Font ID
            
        Returns:
            FontResult: Sıfırlama sonucu
        """
        result = FontResult(success=False)
        result.action = FontAction.RESET.value
        result.font_id = font_id
        
        try:
            if font_id not in self.fonts:
                result.errors.append(f"Font setting not found: {font_id}")
                return result
            
            entry = self.fonts[font_id]
            
            # Reset to defaults
            entry.size = 12
            entry.weight = FontWeight.NORMAL
            entry.style = FontStyle.NORMAL
            entry.line_height = 1.0
            entry.letter_spacing = 0.0
            entry.word_spacing = 0.0
            entry.font_smoothing = None
            entry.antialiasing = None
            entry.ligatures = None
            entry.timestamp = self._get_timestamp()
            
            # Add to history
            if self.config.log_changes:
                self.font_history.append({
                    "action": "reset",
                    "font_id": font_id,
                    "timestamp": entry.timestamp
                })
            
            result.success = True
            result.message = f"Font setting {font_id} reset"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_font_history(self) -> List[Dict[str, Any]]:
        """
        Font geçmişini al.
        
        Returns:
            List[Dict[str, Any]]: Geçmiş
        """
        return self.font_history
    
    def clear_history(self) -> FontResult:
        """
        Geçmişi temizle.
        
        Returns:
            FontResult: Temizleme sonucu
        """
        result = FontResult(success=False)
        
        try:
            self.font_history.clear()
            result.success = True
            result.message = "Font history cleared"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def update_config(self, config: FontConfig) -> FontResult:
        """
        Konfigürasyon güncelle.
        
        Args:
            config: Yeni konfigürasyon
            
        Returns:
            FontResult: Güncelleme sonucu
        """
        result = FontResult(success=False)
        
        try:
            self.config = config
            result.success = True
            result.message = "Config updated"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_config(self) -> FontConfig:
        """
        Konfigürasyon al.
        
        Returns:
            FontConfig: Konfigürasyon
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
    engine = TerminalFontSettingsEngine()
    
    print("Terminal Font Settings Engine initialized")
    print(f"Persist fonts: {engine.config.persist_fonts}")
