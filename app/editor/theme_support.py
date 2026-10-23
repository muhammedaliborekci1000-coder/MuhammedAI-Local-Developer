"""
MuhammedAI Local Developer - Theme Support
Theme support engine for code editor.
"""

from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from enum import Enum


class ThemeType(Enum):
    """Theme type."""
    LIGHT = "light"
    DARK = "dark"
    HIGH_CONTRAST = "high_contrast"
    CUSTOM = "custom"


class ColorScheme(Enum):
    """Color scheme."""
    MONOKAI = "monokai"
    DRACULA = "dracula"
    SOLARIZED = "solarized"
    GITHUB = "github"
    NORD = "nord"
    ONE_DARK = "one_dark"
    VS_CODE = "vs_code"
    CUSTOM = "custom"


@dataclass
class ThemeColors:
    """Theme colors."""
    background: str = "#1e1e1e"
    foreground: str = "#d4d4d4"
    cursor: str = "#ffffff"
    selection: str = "#264f78"
    line_number: str = "#858585"
    line_number_active: str = "#c6c6c6"
    indent_guide: str = "#404040"
    indent_guide_active: str = "#707070"
    bracket: str = "#ffd700"
    bracket_match: str = "#00ff00"
    error: str = "#f14c4c"
    warning: str = "#cca700"
    info: str = "#3794ff"
    hint: str = "#eeeeee"
    string: str = "#ce9178"
    number: str = "#b5cea8"
    keyword: str = "#569cd6"
    comment: str = "#6a9955"
    function: str = "#dcdcaa"
    variable: str = "#9cdcfe"
    type: str = "#4ec9b0"
    operator: str = "#d4d4d4"
    constant: str = "#4fc1ff"


@dataclass
class Theme:
    """Theme."""
    name: str
    theme_type: ThemeType
    color_scheme: ColorScheme
    colors: ThemeColors
    is_builtin: bool = False
    is_active: bool = False


@dataclass
class ThemeConfig:
    """Theme configuration."""
    current_theme: str = "default"
    auto_switch: bool = False
    follow_system: bool = True
    custom_themes: List[Theme] = field(default_factory=list)


@dataclass
class ThemeResult:
    """Theme result."""
    success: bool
    theme: Optional[Theme] = None
    themes: List[Theme] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    message: Optional[str] = None


class ThemeSupportEngine:
    """
    Theme support engine.
    
    Özellikler:
    - Theme management
    - Light/dark themes
    - Custom themes
    - Theme switching
    - Color schemes
    - Syntax highlighting themes
    - UI element theming
    - Theme persistence
    - Theme presets
    - Custom color configuration
    - Auto theme switching
    - System theme following
    - Theme validation
    - Theme export/import
    """
    
    def __init__(self, config: Optional[ThemeConfig] = None):
        """Initialize theme support engine."""
        self.config = config or ThemeConfig()
        self.themes: List[Theme] = []
        self._register_builtin_themes()
    
    def _register_builtin_themes(self):
        """Builtin temaları kaydet."""
        # Dark theme (Monokai)
        monokai_colors = ThemeColors(
            background="#272822",
            foreground="#f8f8f2",
            cursor="#f8f8f0",
            selection="#49483e",
            line_number="#90908a",
            line_number_active="#f8f8f2",
            indent_guide="#49483e",
            indent_guide_active="#75715e",
            bracket="#f92672",
            bracket_match="#a6e22e",
            error="#f92672",
            warning="#e6db74",
            info="#66d9ef",
            hint="#ae81ff",
            string="#e6db74",
            number="#ae81ff",
            keyword="#f92672",
            comment="#75715e",
            function="#a6e22e",
            variable="#f8f8f2",
            type="#66d9ef",
            operator="#f92672",
            constant="#ae81ff"
        )
        monokai = Theme(
            name="Monokai",
            theme_type=ThemeType.DARK,
            color_scheme=ColorScheme.MONOKAI,
            colors=monokai_colors,
            is_builtin=True
        )
        self.themes.append(monokai)
        
        # Light theme (GitHub)
        github_colors = ThemeColors(
            background="#ffffff",
            foreground="#24292e",
            cursor="#24292e",
            selection="#c8e1ff",
            line_number="#959da5",
            line_number_active="#24292e",
            indent_guide="#e1e4e8",
            indent_guide_active="#d1d5da",
            bracket="#0366d6",
            bracket_match="#28a745",
            error="#d73a49",
            warning="#e36209",
            info="#0366d6",
            hint="#6f42c1",
            string="#032f62",
            number="#005cc5",
            keyword="#d73a49",
            comment="#6a737d",
            function="#6f42c1",
            variable="#e36209",
            type="#d73a49",
            operator="#24292e",
            constant="#005cc5"
        )
        github = Theme(
            name="GitHub Light",
            theme_type=ThemeType.LIGHT,
            color_scheme=ColorScheme.GITHUB,
            colors=github_colors,
            is_builtin=True
        )
        self.themes.append(github)
        
        # Dracula theme
        dracula_colors = ThemeColors(
            background="#282a36",
            foreground="#f8f8f2",
            cursor="#f8f8f2",
            selection="#44475a",
            line_number="#6272a4",
            line_number_active="#f8f8f2",
            indent_guide="#44475a",
            indent_guide_active="#6272a4",
            bracket="#ff79c6",
            bracket_match="#50fa7b",
            error="#ff5555",
            warning="#f1fa8c",
            info="#8be9fd",
            hint="#bd93f9",
            string="#f1fa8c",
            number="#bd93f9",
            keyword="#ff79c6",
            comment="#6272a4",
            function="#50fa7b",
            variable="#f8f8f2",
            type="#8be9fd",
            operator="#ff79c6",
            constant="#bd93f9"
        )
        dracula = Theme(
            name="Dracula",
            theme_type=ThemeType.DARK,
            color_scheme=ColorScheme.DRACULA,
            colors=dracula_colors,
            is_builtin=True
        )
        self.themes.append(dracula)
        
        # Solarized Dark
        solarized_colors = ThemeColors(
            background="#002b36",
            foreground="#839496",
            cursor="#839496",
            selection="#073642",
            line_number="#586e75",
            line_number_active="#839496",
            indent_guide="#073642",
            indent_guide_active="#586e75",
            bracket="#cb4b16",
            bracket_match="#859900",
            error="#dc322f",
            warning="#b58900",
            info="#268bd2",
            hint="#6c71c4",
            string="#2aa198",
            number="#d33682",
            keyword="#859900",
            comment="#586e75",
            function="#268bd2",
            variable="#b58900",
            type="#2aa198",
            operator="#cb4b16",
            constant="#d33682"
        )
        solarized = Theme(
            name="Solarized Dark",
            theme_type=ThemeType.DARK,
            color_scheme=ColorScheme.SOLARIZED,
            colors=solarized_colors,
            is_builtin=True
        )
        self.themes.append(solarized)
        
        # Set default active theme
        if self.themes:
            self.themes[0].is_active = True
            self.config.current_theme = self.themes[0].name
    
    def get_theme(self, name: str) -> ThemeResult:
        """
        Tema al.
        
        Args:
            name: Tema adı
            
        Returns:
            ThemeResult: Tema sonucu
        """
        result = ThemeResult(success=False)
        
        try:
            for theme in self.themes:
                if theme.name == name:
                    result.success = True
                    result.theme = theme
                    result.message = f"Theme '{name}' found"
                    return result
            
            result.errors.append(f"Theme '{name}' not found")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_all_themes(self) -> ThemeResult:
        """
        Tüm temaları al.
        
        Returns:
            ThemeResult: Tüm temalar
        """
        result = ThemeResult(success=False)
        
        try:
            result.success = True
            result.themes = self.themes
            result.message = f"Found {len(self.themes)} themes"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_active_theme(self) -> ThemeResult:
        """
        Aktif temayı al.
        
        Returns:
            ThemeResult: Aktif tema
        """
        result = ThemeResult(success=False)
        
        try:
            for theme in self.themes:
                if theme.is_active:
                    result.success = True
                    result.theme = theme
                    result.message = f"Active theme: {theme.name}"
                    return result
            
            result.errors.append("No active theme found")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def set_theme(self, name: str) -> ThemeResult:
        """
        Tema ayarla.
        
        Args:
            name: Tema adı
            
        Returns:
            ThemeResult: Ayarlama sonucu
        """
        result = ThemeResult(success=False)
        
        try:
            theme_found = False
            for theme in self.themes:
                if theme.name == name:
                    theme.is_active = True
                    theme_found = True
                    self.config.current_theme = name
                else:
                    theme.is_active = False
            
            if theme_found:
                result.success = True
                result.theme = self.get_theme(name).theme
                result.message = f"Theme set to '{name}'"
            else:
                result.errors.append(f"Theme '{name}' not found")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def add_custom_theme(self, theme: Theme) -> ThemeResult:
        """
        Özel tema ekle.
        
        Args:
            theme: Tema
            
        Returns:
            ThemeResult: Ekleme sonucu
        """
        result = ThemeResult(success=False)
        
        try:
            # Mevcut tema kontrolü
            for t in self.themes:
                if t.name == theme.name:
                    result.errors.append(f"Theme '{theme.name}' already exists")
                    return result
            
            theme.is_builtin = False
            self.themes.append(theme)
            self.config.custom_themes.append(theme)
            
            result.success = True
            result.theme = theme
            result.themes = self.themes
            result.message = f"Custom theme '{theme.name}' added"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def remove_theme(self, name: str) -> ThemeResult:
        """
        Tema kaldır.
        
        Args:
            name: Tema adı
            
        Returns:
            ThemeResult: Kaldırma sonucu
        """
        result = ThemeResult(success=False)
        
        try:
            theme_to_remove = None
            for theme in self.themes:
                if theme.name == name:
                    if theme.is_builtin:
                        result.errors.append("Cannot remove builtin theme")
                        return result
                    theme_to_remove = theme
                    break
            
            if theme_to_remove:
                self.themes.remove(theme_to_remove)
                if theme_to_remove in self.config.custom_themes:
                    self.config.custom_themes.remove(theme_to_remove)
                
                # Aktif tema kaldırıldıysa, yeni active ata
                if theme_to_remove.is_active and self.themes:
                    self.themes[0].is_active = True
                    self.config.current_theme = self.themes[0].name
                
                result.success = True
                result.themes = self.themes
                result.message = f"Theme '{name}' removed"
            else:
                result.errors.append(f"Theme '{name}' not found")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_themes_by_type(self, theme_type: ThemeType) -> ThemeResult:
        """
    Tipe göre temaları al.
        
        Args:
            theme_type: Tema tipi
            
        Returns:
            ThemeResult: Temalar
        """
        result = ThemeResult(success=False)
        
        try:
            filtered_themes = [t for t in self.themes if t.theme_type == theme_type]
            
            result.success = True
            result.themes = filtered_themes
            result.message = f"Found {len(filtered_themes)} themes of type {theme_type.value}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_builtin_themes(self) -> ThemeResult:
        """
        Builtin temaları al.
        
        Returns:
            ThemeResult: Builtin temalar
        """
        result = ThemeResult(success=False)
        
        try:
            builtin_themes = [t for t in self.themes if t.is_builtin]
            
            result.success = True
            result.themes = builtin_themes
            result.message = f"Found {len(builtin_themes)} builtin themes"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_custom_themes(self) -> ThemeResult:
        """
        Özel temaları al.
        
        Returns:
            ThemeResult: Özel temalar
        """
        result = ThemeResult(success=False)
        
        try:
            custom_themes = [t for t in self.themes if not t.is_builtin]
            
            result.success = True
            result.themes = custom_themes
            result.message = f"Found {len(custom_themes)} custom themes"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def update_config(self, config: ThemeConfig) -> ThemeResult:
        """
        Konfigürasyon güncelle.
        
        Args:
            config: Yeni konfigürasyon
            
        Returns:
            ThemeResult: Güncelleme sonucu
        """
        result = ThemeResult(success=False)
        
        try:
            self.config = config
            result.success = True
            result.message = "Config updated"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_config(self) -> ThemeConfig:
        """
        Konfigürasyon al.
        
        Returns:
            ThemeConfig: Konfigürasyon
        """
        return self.config
    
    def toggle_auto_switch(self) -> ThemeResult:
        """
        Auto switch'i aç/kapat.
        
        Returns:
            ThemeResult: Toggle sonucu
        """
        result = ThemeResult(success=False)
        
        try:
            self.config.auto_switch = not self.config.auto_switch
            result.success = True
            result.message = f"Auto switch {'enabled' if self.config.auto_switch else 'disabled'}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def toggle_follow_system(self) -> ThemeResult:
        """
        System theme follow'ı aç/kapat.
        
        Returns:
            ThemeResult: Toggle sonucu
        """
        result = ThemeResult(success=False)
        
        try:
            self.config.follow_system = not self.config.follow_system
            result.success = True
            result.message = f"Follow system {'enabled' if self.config.follow_system else 'disabled'}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result


if __name__ == "__main__":
    # Basit test
    engine = ThemeSupportEngine()
    
    # Tüm temaları al
    result = engine.get_all_themes()
    print(f"Themes: {len(result.themes)}")
    
    # Aktif temayı al
    active = engine.get_active_theme()
    print(f"Active: {active.theme.name if active.theme else 'None'}")
