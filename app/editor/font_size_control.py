"""
MuhammedAI Local Developer - Font Size Control
Font size control engine for code editor.
"""

from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from enum import Enum


class FontSizePreset(Enum):
    """Font size preset."""
    EXTRA_SMALL = 8
    SMALL = 10
    MEDIUM = 12
    LARGE = 14
    EXTRA_LARGE = 16
    HUGE = 18
    EXTRA_HUGE = 20


class FontFamily(Enum):
    """Font family."""
    MONOSPACE = "monospace"
    SANS_SERIF = "sans-serif"
    SERIF = "serif"
    CUSTOM = "custom"


@dataclass
class FontSettings:
    """Font settings."""
    editor_font_size: int = 14
    ui_font_size: int = 12
    line_height: float = 1.5
    font_family: FontFamily = FontFamily.MONOSPACE
    custom_font_family: str = ""
    letter_spacing: float = 0.0
    word_spacing: float = 0.0
    min_font_size: int = 8
    max_font_size: int = 32


@dataclass
class FontSizeResult:
    """Font size result."""
    success: bool
    font_size: int = 14
    font_settings: Optional[FontSettings] = None
    errors: List[str] = field(default_factory=list)
    message: Optional[str] = None


class FontSizeControlEngine:
    """
    Font size control engine.
    
    Özellikler:
    - Font size management
    - Increase/decrease font size
    - Font size presets
    - Custom font size
    - Font size persistence
    - Zoom in/out
    - Reset to default
    - Line height control
    - Font family control
    - UI font size control
    - Editor font size control
    - Font size validation
    - Letter spacing
    - Word spacing
    - Min/max font size limits
    """
    
    def __init__(self, settings: Optional[FontSettings] = None):
        """Initialize font size control engine."""
        self.settings = settings or FontSettings()
    
    def increase_font_size(self, amount: int = 2) -> FontSizeResult:
        """
        Font boyutunu artır.
        
        Args:
            amount: Artış miktarı
            
        Returns:
            FontSizeResult: Artırma sonucu
        """
        result = FontSizeResult(success=False)
        
        try:
            new_size = self.settings.editor_font_size + amount
            
            if new_size <= self.settings.max_font_size:
                self.settings.editor_font_size = new_size
                result.success = True
                result.font_size = new_size
                result.font_settings = self.settings
                result.message = f"Font size increased to {new_size}"
            else:
                result.errors.append(f"Font size cannot exceed {self.settings.max_font_size}")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def decrease_font_size(self, amount: int = 2) -> FontSizeResult:
        """
        Font boyutunu azalt.
        
        Args:
            amount: Azaltma miktarı
            
        Returns:
            FontSizeResult: Azaltma sonucu
        """
        result = FontSizeResult(success=False)
        
        try:
            new_size = self.settings.editor_font_size - amount
            
            if new_size >= self.settings.min_font_size:
                self.settings.editor_font_size = new_size
                result.success = True
                result.font_size = new_size
                result.font_settings = self.settings
                result.message = f"Font size decreased to {new_size}"
            else:
                result.errors.append(f"Font size cannot be less than {self.settings.min_font_size}")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def set_font_size(self, size: int) -> FontSizeResult:
        """
        Font boyutunu ayarla.
        
        Args:
            size: Font boyutu
            
        Returns:
            FontSizeResult: Ayarlama sonucu
        """
        result = FontSizeResult(success=False)
        
        try:
            if self.settings.min_font_size <= size <= self.settings.max_font_size:
                self.settings.editor_font_size = size
                result.success = True
                result.font_size = size
                result.font_settings = self.settings
                result.message = f"Font size set to {size}"
            else:
                result.errors.append(f"Font size must be between {self.settings.min_font_size} and {self.settings.max_font_size}")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_font_size(self) -> FontSizeResult:
        """
        Font boyutunu al.
        
        Returns:
            FontSizeResult: Font boyutu
        """
        result = FontSizeResult(success=False)
        
        try:
            result.success = True
            result.font_size = self.settings.editor_font_size
            result.font_settings = self.settings
            result.message = f"Current font size: {self.settings.editor_font_size}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def reset_font_size(self) -> FontSizeResult:
        """
        Font boyutunu sıfırla.
        
        Returns:
            FontSizeResult: Sıfırlama sonucu
        """
        result = FontSizeResult(success=False)
        
        try:
            self.settings.editor_font_size = 14
            result.success = True
            result.font_size = 14
            result.font_settings = self.settings
            result.message = "Font size reset to default (14)"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def set_preset(self, preset: FontSizePreset) -> FontSizeResult:
        """
        Preset ayarla.
        
        Args:
            preset: Font size preset
            
        Returns:
            FontSizeResult: Ayarlama sonucu
        """
        result = FontSizeResult(success=False)
        
        try:
            size = preset.value
            if self.settings.min_font_size <= size <= self.settings.max_font_size:
                self.settings.editor_font_size = size
                result.success = True
                result.font_size = size
                result.font_settings = self.settings
                result.message = f"Font size set to preset {preset.name} ({size})"
            else:
                result.errors.append(f"Preset size {size} is out of range")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def zoom_in(self) -> FontSizeResult:
        """
        Zoom in.
        
        Returns:
            FontSizeResult: Zoom sonucu
        """
        return self.increase_font_size(2)
    
    def zoom_out(self) -> FontSizeResult:
        """
        Zoom out.
        
        Returns:
            FontSizeResult: Zoom sonucu
        """
        return self.decrease_font_size(2)
    
    def set_line_height(self, height: float) -> FontSizeResult:
        """
        Satır yüksekliğini ayarla.
        
        Args:
            height: Satır yüksekliği
            
        Returns:
            FontSizeResult: Ayarlama sonucu
        """
        result = FontSizeResult(success=False)
        
        try:
            if 1.0 <= height <= 3.0:
                self.settings.line_height = height
                result.success = True
                result.font_settings = self.settings
                result.message = f"Line height set to {height}"
            else:
                result.errors.append("Line height must be between 1.0 and 3.0")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def set_font_family(self, family: FontFamily) -> FontSizeResult:
        """
        Font ailesini ayarla.
        
        Args:
            family: Font ailesi
            
        Returns:
            FontSizeResult: Ayarlama sonucu
        """
        result = FontSizeResult(success=False)
        
        try:
            self.settings.font_family = family
            result.success = True
            result.font_settings = self.settings
            result.message = f"Font family set to {family.value}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def set_custom_font_family(self, family: str) -> FontSizeResult:
        """
        Özel font ailesini ayarla.
        
        Args:
            family: Özel font ailesi
            
        Returns:
            FontSizeResult: Ayarlama sonucu
        """
        result = FontSizeResult(success=False)
        
        try:
            self.settings.custom_font_family = family
            self.settings.font_family = FontFamily.CUSTOM
            result.success = True
            result.font_settings = self.settings
            result.message = f"Custom font family set to {family}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def set_ui_font_size(self, size: int) -> FontSizeResult:
        """
        UI font boyutunu ayarla.
        
        Args:
            size: UI font boyutu
            
        Returns:
            FontSizeResult: Ayarlama sonucu
        """
        result = FontSizeResult(success=False)
        
        try:
            if self.settings.min_font_size <= size <= self.settings.max_font_size:
                self.settings.ui_font_size = size
                result.success = True
                result.font_settings = self.settings
                result.message = f"UI font size set to {size}"
            else:
                result.errors.append(f"UI font size must be between {self.settings.min_font_size} and {self.settings.max_font_size}")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def set_letter_spacing(self, spacing: float) -> FontSizeResult:
        """
        Letter spacing ayarla.
        
        Args:
            spacing: Letter spacing
            
        Returns:
            FontSizeResult: Ayarlama sonucu
        """
        result = FontSizeResult(success=False)
        
        try:
            if -2.0 <= spacing <= 5.0:
                self.settings.letter_spacing = spacing
                result.success = True
                result.font_settings = self.settings
                result.message = f"Letter spacing set to {spacing}"
            else:
                result.errors.append("Letter spacing must be between -2.0 and 5.0")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def set_word_spacing(self, spacing: float) -> FontSizeResult:
        """
        Word spacing ayarla.
        
        Args:
            spacing: Word spacing
            
        Returns:
            FontSizeResult: Ayarlama sonucu
        """
        result = FontSizeResult(success=False)
        
        try:
            if -2.0 <= spacing <= 5.0:
                self.settings.word_spacing = spacing
                result.success = True
                result.font_settings = self.settings
                result.message = f"Word spacing set to {spacing}"
            else:
                result.errors.append("Word spacing must be between -2.0 and 5.0")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def set_min_font_size(self, size: int) -> FontSizeResult:
        """
        Minimum font boyutunu ayarla.
        
        Args:
            size: Minimum font boyutu
            
        Returns:
            FontSizeResult: Ayarlama sonucu
        """
        result = FontSizeResult(success=False)
        
        try:
            if size > 0 and size < self.settings.max_font_size:
                self.settings.min_font_size = size
                result.success = True
                result.font_settings = self.settings
                result.message = f"Min font size set to {size}"
            else:
                result.errors.append("Invalid min font size")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def set_max_font_size(self, size: int) -> FontSizeResult:
        """
        Maksimum font boyutunu ayarla.
        
        Args:
            size: Maksimum font boyutu
            
        Returns:
            FontSizeResult: Ayarlama sonucu
        """
        result = FontSizeResult(success=False)
        
        try:
            if size > self.settings.min_font_size:
                self.settings.max_font_size = size
                result.success = True
                result.font_settings = self.settings
                result.message = f"Max font size set to {size}"
            else:
                result.errors.append("Invalid max font size")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_settings(self) -> FontSettings:
        """
        Ayarları al.
        
        Returns:
            FontSettings: Ayarlar
        """
        return self.settings
    
    def update_settings(self, settings: FontSettings) -> FontSizeResult:
        """
        Ayarları güncelle.
        
        Args:
            settings: Yeni ayarlar
            
        Returns:
            FontSizeResult: Güncelleme sonucu
        """
        result = FontSizeResult(success=False)
        
        try:
            self.settings = settings
            result.success = True
            result.font_settings = self.settings
            result.message = "Settings updated"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result


if __name__ == "__main__":
    # Basit test
    engine = FontSizeControlEngine()
    
    # Font boyutunu artır
    result = engine.increase_font_size()
    print(f"Increased: {result.success}, Size: {result.font_size}")
    
    # Font boyutunu azalt
    result = engine.decrease_font_size()
    print(f"Decreased: {result.success}, Size: {result.font_size}")
