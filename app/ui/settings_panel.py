"""
MuhammedAI Local Developer - Settings Panel
Settings panel system for web UI.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum


class SettingType(Enum):
    """Setting type."""
    BOOLEAN = "boolean"
    STRING = "string"
    NUMBER = "number"
    INTEGER = "integer"
    SELECT = "select"
    MULTI_SELECT = "multi_select"
    COLOR = "color"
    PATH = "path"
    HOTKEY = "hotkey"
    CUSTOM = "custom"


class SettingCategory(Enum):
    """Setting category."""
    GENERAL = "general"
    EDITOR = "editor"
    THEME = "theme"
    KEYBINDINGS = "keybindings"
    TERMINAL = "terminal"
    GIT = "git"
    AI = "ai"
    SECURITY = "security"
    ADVANCED = "advanced"
    CUSTOM = "custom"


@dataclass
class SettingOption:
    """Setting option for select/multi-select."""
    value: str
    label: str
    description: Optional[str] = None


@dataclass
class Setting:
    """Setting entry."""
    id: str
    type: SettingType
    category: SettingCategory
    key: str
    label: str
    default_value: Any
    current_value: Any
    is_enabled: bool = True
    is_visible: bool = True
    is_sensitive: bool = False
    requires_restart: bool = False
    options: List[SettingOption] = field(default_factory=list)
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    description: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SettingsPanelConfig:
    """Settings panel configuration."""
    enabled: bool = True
    show_categories: bool = True
    show_search: bool = True
    show_reset: bool = True
    auto_save: bool = True
    enable_validation: bool = True
    enable_import_export: bool = True
    max_settings_per_category: int = 50


@dataclass
class SettingsPanelResult:
    """Settings panel result."""
    success: bool
    setting: Optional[Setting] = None
    settings: List[Setting] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    message: Optional[str] = None


class SettingsPanelManager:
    """
    Settings panel manager.
    
    Özellikler:
    - Boolean settings
    - String settings
    - Number settings
    - Integer settings
    - Select settings
    - Multi-select settings
    - Color settings
    - Path settings
    - Hotkey settings
    - Custom settings
    - Setting categories
    - Setting validation
    - Setting persistence
    - Import/Export
    - Reset to defaults
    """
    
    def __init__(self, config: Optional[SettingsPanelConfig] = None):
        """
        Initialize settings panel manager.
        
        Args:
            config: Settings panel configuration
        """
        self.config = config or SettingsPanelConfig()
        self.settings: Dict[str, Setting] = {}
        self.setting_id_counter = 0
        self._next_id()
    
    def _next_id(self) -> str:
        """
        Generate next setting ID.
        
        Returns:
            str: Setting ID
        """
        self.setting_id_counter += 1
        return f"setting_{self.setting_id_counter}"
    
    def add_setting(self, setting: Setting) -> SettingsPanelResult:
        """
        Add a setting.
        
        Args:
            setting: Setting to add
            
        Returns:
            SettingsPanelResult: Add result
        """
        result = SettingsPanelResult(success=True)
        
        try:
            if not setting.id:
                setting.id = self._next_id()
            
            self.settings[setting.id] = setting
            result.setting = setting
            result.settings = self.get_all_settings()
            result.message = f"Setting '{setting.id}' added"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def remove_setting(self, setting_id: str) -> SettingsPanelResult:
        """
        Remove a setting.
        
        Args:
            setting_id: Setting ID
            
        Returns:
            SettingsPanelResult: Remove result
        """
        result = SettingsPanelResult(success=False)
        
        try:
            if setting_id in self.settings:
                del self.settings[setting_id]
                result.success = True
                result.settings = self.get_all_settings()
                result.message = f"Setting '{setting_id}' removed"
            else:
                result.errors.append("Setting not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_setting(self, setting_id: str) -> Optional[Setting]:
        """
        Get setting by ID.
        
        Args:
            setting_id: Setting ID
            
        Returns:
            Optional[Setting]: Setting
        """
        return self.settings.get(setting_id)
    
    def get_all_settings(self) -> List[Setting]:
        """
        Get all settings.
        
        Returns:
            List[Setting]: All settings
        """
        return list(self.settings.values())
    
    def get_settings_by_category(self, category: SettingCategory) -> List[Setting]:
        """
        Get settings by category.
        
        Args:
            category: Setting category
            
        Returns:
            List[Setting]: Settings
        """
        return [s for s in self.settings.values() if s.category == category]
    
    def get_settings_by_type(self, setting_type: SettingType) -> List[Setting]:
        """
        Get settings by type.
        
        Args:
            setting_type: Setting type
            
        Returns:
            List[Setting]: Settings
        """
        return [s for s in self.settings.values() if s.type == setting_type]
    
    def update_setting_value(self, setting_id: str, new_value: Any) -> SettingsPanelResult:
        """
        Update setting value.
        
        Args:
            setting_id: Setting ID
            new_value: New value
            
        Returns:
            SettingsPanelResult: Update result
        """
        result = SettingsPanelResult(success=False)
        
        try:
            setting = self.settings.get(setting_id)
            if setting:
                # Validation
                if self.config.enable_validation:
                    if setting.min_value is not None and isinstance(new_value, (int, float)):
                        if new_value < setting.min_value:
                            result.errors.append(f"Value must be >= {setting.min_value}")
                            return result
                    if setting.max_value is not None and isinstance(new_value, (int, float)):
                        if new_value > setting.max_value:
                            result.errors.append(f"Value must be <= {setting.max_value}")
                            return result
                
                setting.current_value = new_value
                result.success = True
                result.setting = setting
                result.message = f"Setting '{setting_id}' updated"
            else:
                result.errors.append("Setting not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def reset_setting_to_default(self, setting_id: str) -> SettingsPanelResult:
        """
        Reset setting to default value.
        
        Args:
            setting_id: Setting ID
            
        Returns:
            SettingsPanelResult: Reset result
        """
        result = SettingsPanelResult(success=False)
        
        try:
            setting = self.settings.get(setting_id)
            if setting:
                setting.current_value = setting.default_value
                result.success = True
                result.setting = setting
                result.message = f"Setting '{setting_id}' reset to default"
            else:
                result.errors.append("Setting not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def reset_all_to_defaults(self) -> SettingsPanelResult:
        """
        Reset all settings to default values.
        
        Returns:
            SettingsPanelResult: Reset result
        """
        result = SettingsPanelResult(success=True)
        
        try:
            for setting in self.settings.values():
                setting.current_value = setting.default_value
            
            result.message = "All settings reset to default"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def add_boolean_setting(self, category: SettingCategory, key: str, label: str, default_value: bool, description: str = "") -> SettingsPanelResult:
        """
        Add boolean setting.
        
        Args:
            category: Setting category
            key: Setting key
            label: Setting label
            default_value: Default value
            description: Description
            
        Returns:
            SettingsPanelResult: Add result
        """
        setting = Setting(
            id="",
            type=SettingType.BOOLEAN,
            category=category,
            key=key,
            label=label,
            default_value=default_value,
            current_value=default_value,
            description=description
        )
        
        return self.add_setting(setting)
    
    def add_string_setting(self, category: SettingCategory, key: str, label: str, default_value: str, description: str = "") -> SettingsPanelResult:
        """
        Add string setting.
        
        Args:
            category: Setting category
            key: Setting key
            label: Setting label
            default_value: Default value
            description: Description
            
        Returns:
            SettingsPanelResult: Add result
        """
        setting = Setting(
            id="",
            type=SettingType.STRING,
            category=category,
            key=key,
            label=label,
            default_value=default_value,
            current_value=default_value,
            description=description
        )
        
        return self.add_setting(setting)
    
    def add_number_setting(self, category: SettingCategory, key: str, label: str, default_value: float, min_value: Optional[float] = None, max_value: Optional[float] = None, description: str = "") -> SettingsPanelResult:
        """
        Add number setting.
        
        Args:
            category: Setting category
            key: Setting key
            label: Setting label
            default_value: Default value
            min_value: Minimum value
            max_value: Maximum value
            description: Description
            
        Returns:
            SettingsPanelResult: Add result
        """
        setting = Setting(
            id="",
            type=SettingType.NUMBER,
            category=category,
            key=key,
            label=label,
            default_value=default_value,
            current_value=default_value,
            min_value=min_value,
            max_value=max_value,
            description=description
        )
        
        return self.add_setting(setting)
    
    def add_select_setting(self, category: SettingCategory, key: str, label: str, default_value: str, options: List[SettingOption], description: str = "") -> SettingsPanelResult:
        """
        Add select setting.
        
        Args:
            category: Setting category
            key: Setting key
            label: Setting label
            default_value: Default value
            options: Select options
            description: Description
            
        Returns:
            SettingsPanelResult: Add result
        """
        setting = Setting(
            id="",
            type=SettingType.SELECT,
            category=category,
            key=key,
            label=label,
            default_value=default_value,
            current_value=default_value,
            options=options,
            description=description
        )
        
        return self.add_setting(setting)
    
    def add_color_setting(self, category: SettingCategory, key: str, label: str, default_value: str, description: str = "") -> SettingsPanelResult:
        """
        Add color setting.
        
        Args:
            category: Setting category
            key: Setting key
            label: Setting label
            default_value: Default value (hex color)
            description: Description
            
        Returns:
            SettingsPanelResult: Add result
        """
        setting = Setting(
            id="",
            type=SettingType.COLOR,
            category=category,
            key=key,
            label=label,
            default_value=default_value,
            current_value=default_value,
            description=description
        )
        
        return self.add_setting(setting)
    
    def add_hotkey_setting(self, category: SettingCategory, key: str, label: str, default_value: str, description: str = "") -> SettingsPanelResult:
        """
        Add hotkey setting.
        
        Args:
            category: Setting category
            key: Setting key
            label: Setting label
            default_value: Default value (key combination)
            description: Description
            
        Returns:
            SettingsPanelResult: Add result
        """
        setting = Setting(
            id="",
            type=SettingType.HOTKEY,
            category=category,
            key=key,
            label=label,
            default_value=default_value,
            current_value=default_value,
            description=description
        )
        
        return self.add_setting(setting)
    
    def export_settings(self) -> Dict[str, Any]:
        """
        Export all settings as dictionary.
        
        Returns:
            Dict[str, Any]: Settings dictionary
        """
        return {s.key: s.current_value for s in self.settings.values()}
    
    def import_settings(self, settings_dict: Dict[str, Any]) -> SettingsPanelResult:
        """
        Import settings from dictionary.
        
        Args:
            settings_dict: Settings dictionary
            
        Returns:
            SettingsPanelResult: Import result
        """
        result = SettingsPanelResult(success=True)
        
        try:
            for setting in self.settings.values():
                if setting.key in settings_dict:
                    setting.current_value = settings_dict[setting.key]
            
            result.message = "Settings imported successfully"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def clear_settings(self) -> SettingsPanelResult:
        """
        Clear all settings.
        
        Returns:
            SettingsPanelResult: Clear result
        """
        result = SettingsPanelResult(success=True)
        
        try:
            self.settings.clear()
            result.message = "All settings cleared"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def set_setting_enabled(self, setting_id: str, enabled: bool) -> SettingsPanelResult:
        """
        Set setting enabled state.
        
        Args:
            setting_id: Setting ID
            enabled: Enabled state
            
        Returns:
            SettingsPanelResult: Set result
        """
        result = SettingsPanelResult(success=False)
        
        try:
            setting = self.settings.get(setting_id)
            if setting:
                setting.is_enabled = enabled
                result.success = True
                result.message = f"Setting '{setting_id}' {'enabled' if enabled else 'disabled'}"
            else:
                result.errors.append("Setting not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def set_setting_visible(self, setting_id: str, visible: bool) -> SettingsPanelResult:
        """
        Set setting visible state.
        
        Args:
            setting_id: Setting ID
            visible: Visible state
            
        Returns:
            SettingsPanelResult: Set result
        """
        result = SettingsPanelResult(success=False)
        
        try:
            setting = self.settings.get(setting_id)
            if setting:
                setting.is_visible = visible
                result.success = True
                result.message = f"Setting '{setting_id}' {'visible' if visible else 'hidden'}"
            else:
                result.errors.append("Setting not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def update_config(self, config: SettingsPanelConfig) -> SettingsPanelResult:
        """
        Update settings panel configuration.
        
        Args:
            config: New configuration
            
        Returns:
            SettingsPanelResult: Update result
        """
        result = SettingsPanelResult(success=True)
        
        try:
            self.config = config
            result.message = "Config updated"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def get_config(self) -> SettingsPanelConfig:
        """
        Get settings panel configuration.
        
        Returns:
            SettingsPanelConfig: Configuration
        """
        return self.config


if __name__ == "__main__":
    # Basit test
    config = SettingsPanelConfig()
    manager = SettingsPanelManager(config)
    
    # Setting ekle
    result = manager.add_boolean_setting(SettingCategory.GENERAL, "auto_save", "Auto Save", True, "Automatically save files")
    
    print(f"Setting added: {result.message}")
    
    # Tüm setting'leri al
    settings = manager.get_all_settings()
    
    print(f"Total settings: {len(settings)}")
