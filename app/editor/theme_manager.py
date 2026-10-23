"""
MuhammedAI Local Developer - Theme Manager
Theme management system for code editor.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum


class ThemeType(Enum):
    """Theme type."""
    DARK = "dark"
    LIGHT = "light"
    CUSTOM = "custom"


class ThemeCategory(Enum):
    """Theme category."""
    BUILT_IN = "built_in"
    USER_INSTALLED = "user_installed"
    COMMUNITY = "community"


@dataclass
class ThemeColors:
    """Theme color palette."""
    background: str = "#1e1e1e"
    foreground: str = "#d4d4d4"
    cursor: str = "#aeafad"
    selection: str = "#264f78"
    line_number: str = "#858585"
    line_number_active: str = "#c6c6c6"
    keyword: str = "#569cd6"
    string: str = "#ce9178"
    comment: str = "#6a9955"
    function: str = "#dcdcaa"
    variable: str = "#9cdcfe"
    type: str = "#4ec9b0"
    constant: str = "#4fc1ff"
    operator: str = "#d4d4d4"
    bracket: str = "#ffd700"
    error: str = "#f48771"
    warning: str = "#cca700"
    info: str = "#75beff"
    hint: str = "#eeeeee"
    added: str = "#81b88b"
    removed: str = "#c74e14"
    modified: str = "#e2c08d"


@dataclass
class ThemeSettings:
    """Theme settings."""
    font_family: str = "Consolas"
    font_size: int = 14
    line_height: int = 20
    tab_size: int = 4
    insert_spaces: bool = True
    word_wrap: bool = False
    minimap_enabled: bool = True
    line_numbers: bool = True
    render_whitespace: bool = False
    bracket_pair_colorization: bool = True
    indent_guides: bool = True


@dataclass
class Theme:
    """Theme information."""
    id: str
    name: str
    type: ThemeType
    category: ThemeCategory
    colors: ThemeColors = field(default_factory=ThemeColors)
    settings: ThemeSettings = field(default_factory=ThemeSettings)
    description: Optional[str] = None
    author: Optional[str] = None
    version: str = "1.0.0"


@dataclass
class ThemeConfig:
    """Theme configuration."""
    current_theme_id: str = "default_dark"
    auto_switch: bool = False
    follow_system: bool = False
    custom_themes_path: Optional[str] = None
    enable_community_themes: bool = False


class ThemeManager:
    """
    Theme manager.
    
    Özellikler:
    - Dark/light mode
    - Custom themes
    - Theme switching
    - Syntax highlighting themes
    - UI themes
    - Color customization
    - Theme persistence
    - Theme preview
    - Theme export/import
    - Built-in themes
    - User themes
    - Community themes
    - Theme validation
    - Theme settings
    """
    
    def __init__(self, config: Optional[ThemeConfig] = None):
        """
        Initialize theme manager.
        
        Args:
            config: Theme configuration
        """
        self.config = config or ThemeConfig()
        self.themes: Dict[str, Theme] = {}
        self._initialize_builtin_themes()
    
    def _initialize_builtin_themes(self) -> None:
        """Initialize built-in themes."""
        # Default Dark Theme
        dark_colors = ThemeColors(
            background="#1e1e1e",
            foreground="#d4d4d4",
            cursor="#aeafad",
            selection="#264f78",
            line_number="#858585",
            line_number_active="#c6c6c6",
            keyword="#569cd6",
            string="#ce9178",
            comment="#6a9955",
            function="#dcdcaa",
            variable="#9cdcfe",
            type="#4ec9b0",
            constant="#4fc1ff",
            operator="#d4d4d4",
            bracket="#ffd700",
            error="#f48771",
            warning="#cca700",
            info="#75beff",
            hint="#eeeeee",
            added="#81b88b",
            removed="#c74e14",
            modified="#e2c08d"
        )
        
        self.themes["default_dark"] = Theme(
            id="default_dark",
            name="Default Dark",
            type=ThemeType.DARK,
            category=ThemeCategory.BUILT_IN,
            colors=dark_colors,
            description="Default dark theme"
        )
        
        # Default Light Theme
        light_colors = ThemeColors(
            background="#ffffff",
            foreground="#000000",
            cursor="#000000",
            selection="#add6ff",
            line_number="#237893",
            line_number_active="#000000",
            keyword="#0000ff",
            string="#a31515",
            comment="#008000",
            function="#795e26",
            variable="#001080",
            type="#2b91af",
            constant="#000000",
            operator="#000000",
            bracket="#000000",
            error="#cd3131",
            warning="#9c8a0e",
            info="#0000ff",
            hint="#6a6a6a",
            added="#81b88b",
            removed="#c74e14",
            modified="#e2c08d"
        )
        
        self.themes["default_light"] = Theme(
            id="default_light",
            name="Default Light",
            type=ThemeType.LIGHT,
            category=ThemeCategory.BUILT_IN,
            colors=light_colors,
            description="Default light theme"
        )
        
        # Monokai Theme
        monokai_colors = ThemeColors(
            background="#272822",
            foreground="#f8f8f2",
            cursor="#f8f8f0",
            selection="#49483e",
            line_number="#90908a",
            line_number_active="#c6c6c6",
            keyword="#f92672",
            string="#e6db74",
            comment="#75715e",
            function="#a6e22e",
            variable="#fd971f",
            type="#66d9ef",
            constant="#ae81ff",
            operator="#f92672",
            bracket="#f8f8f2",
            error="#f92672",
            warning="#e6db74",
            info="#66d9ef",
            hint="#75715e",
            added="#a6e22e",
            removed="#f92672",
            modified="#fd971f"
        )
        
        self.themes["monokai"] = Theme(
            id="monokai",
            name="Monokai",
            type=ThemeType.DARK,
            category=ThemeCategory.BUILT_IN,
            colors=monokai_colors,
            description="Monokai theme"
        )
        
        # Dracula Theme
        dracula_colors = ThemeColors(
            background="#282a36",
            foreground="#f8f8f2",
            cursor="#44475a",
            selection="#44475a",
            line_number="#6272a4",
            line_number_active="#f8f8f2",
            keyword="#ff79c6",
            string="#f1fa8c",
            comment="#6272a4",
            function="#50fa7b",
            variable="#8be9fd",
            type="#bd93f9",
            constant="#ffb86c",
            operator="#ff79c6",
            bracket="#ff79c6",
            error="#ff5555",
            warning="#f1fa8c",
            info="#8be9fd",
            hint="#6272a4",
            added="#50fa7b",
            removed="#ff5555",
            modified="#ffb86c"
        )
        
        self.themes["dracula"] = Theme(
            id="dracula",
            name="Dracula",
            type=ThemeType.DARK,
            category=ThemeCategory.BUILT_IN,
            colors=dracula_colors,
            description="Dracula theme"
        )
    
    def get_theme(self, theme_id: str) -> Optional[Theme]:
        """
        Get theme by ID.
        
        Args:
            theme_id: Theme ID
            
        Returns:
            Optional[Theme]: Theme
        """
        return self.themes.get(theme_id)
    
    def get_current_theme(self) -> Optional[Theme]:
        """
        Get current theme.
        
        Returns:
            Optional[Theme]: Current theme
        """
        return self.get_theme(self.config.current_theme_id)
    
    def set_theme(self, theme_id: str) -> bool:
        """
        Set current theme.
        
        Args:
            theme_id: Theme ID
            
        Returns:
            bool: Success
        """
        if theme_id in self.themes:
            self.config.current_theme_id = theme_id
            return True
        return False
    
    def switch_theme_type(self, theme_type: ThemeType) -> bool:
        """
        Switch theme type (dark/light).
        
        Args:
            theme_type: Theme type
            
        Returns:
            bool: Success
        """
        for theme_id, theme in self.themes.items():
            if theme.type == theme_type:
                return self.set_theme(theme_id)
        return False
    
    def toggle_dark_light(self) -> bool:
        """
        Toggle between dark and light themes.
        
        Returns:
            bool: Success
        """
        current_theme = self.get_current_theme()
        if current_theme:
            if current_theme.type == ThemeType.DARK:
                return self.switch_theme_type(ThemeType.LIGHT)
            else:
                return self.switch_theme_type(ThemeType.DARK)
        return False
    
    def add_custom_theme(self, theme: Theme) -> bool:
        """
        Add custom theme.
        
        Args:
            theme: Theme to add
            
        Returns:
            bool: Success
        """
        if theme.id not in self.themes:
            self.themes[theme.id] = theme
            return True
        return False
    
    def remove_theme(self, theme_id: str) -> bool:
        """
        Remove theme (only custom themes).
        
        Args:
            theme_id: Theme ID
            
        Returns:
            bool: Success
        """
        theme = self.get_theme(theme_id)
        if theme and theme.category == ThemeCategory.USER_INSTALLED:
            del self.themes[theme_id]
            return True
        return False
    
    def get_all_themes(self) -> List[Theme]:
        """
        Get all themes.
        
        Returns:
            List[Theme]: All themes
        """
        return list(self.themes.values())
    
    def get_themes_by_type(self, theme_type: ThemeType) -> List[Theme]:
        """
        Get themes by type.
        
        Args:
            theme_type: Theme type
            
        Returns:
            List[Theme]: Themes
        """
        return [theme for theme in self.themes.values() if theme.type == theme_type]
    
    def get_themes_by_category(self, category: ThemeCategory) -> List[Theme]:
        """
        Get themes by category.
        
        Args:
            category: Theme category
            
        Returns:
            List[Theme]: Themes
        """
        return [theme for theme in self.themes.values() if theme.category == category]
    
    def create_custom_theme(
        self,
        name: str,
        colors: Optional[ThemeColors] = None,
        settings: Optional[ThemeSettings] = None,
        description: Optional[str] = None
    ) -> Theme:
        """
        Create custom theme.
        
        Args:
            name: Theme name
            colors: Theme colors
            settings: Theme settings
            description: Theme description
            
        Returns:
            Theme: Created theme
        """
        theme_id = f"custom_{name.lower().replace(' ', '_')}"
        
        theme = Theme(
            id=theme_id,
            name=name,
            type=ThemeType.CUSTOM,
            category=ThemeCategory.USER_INSTALLED,
            colors=colors or ThemeColors(),
            settings=settings or ThemeSettings(),
            description=description
        )
        
        self.add_custom_theme(theme)
        return theme
    
    def update_theme_colors(self, theme_id: str, colors: ThemeColors) -> bool:
        """
        Update theme colors.
        
        Args:
            theme_id: Theme ID
            colors: New colors
            
        Returns:
            bool: Success
        """
        theme = self.get_theme(theme_id)
        if theme:
            theme.colors = colors
            return True
        return False
    
    def update_theme_settings(self, theme_id: str, settings: ThemeSettings) -> bool:
        """
        Update theme settings.
        
        Args:
            theme_id: Theme ID
            settings: New settings
            
        Returns:
            bool: Success
        """
        theme = self.get_theme(theme_id)
        if theme:
            theme.settings = settings
            return True
        return False
    
    def update_config(self, config: ThemeConfig) -> None:
        """
        Update theme configuration.
        
        Args:
            config: New configuration
        """
        self.config = config
    
    def get_config(self) -> ThemeConfig:
        """
        Get theme configuration.
        
        Returns:
            ThemeConfig: Configuration
        """
        return self.config


if __name__ == "__main__":
    # Basit test
    config = ThemeConfig()
    manager = ThemeManager(config)
    
    # Get current theme
    current_theme = manager.get_current_theme()
    
    print(f"Current theme: {current_theme.name}")
    print(f"Background: {current_theme.colors.background}")
    
    # Toggle dark/light
    manager.toggle_dark_light()
    
    new_theme = manager.get_current_theme()
    print(f"New theme: {new_theme.name}")
