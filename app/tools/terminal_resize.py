"""
MuhammedAI Local Developer - Terminal Resize
Terminal resize management engine for code editor.
"""

from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime


class ResizeMode(Enum):
    """Resize mode."""
    MANUAL = "manual"
    AUTO = "auto"
    PRESET = "preset"
    FIT = "fit"


class ResizeDirection(Enum):
    """Resize direction."""
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"
    BOTH = "both"


class ResizePreset(Enum):
    """Resize preset."""
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"
    FULLSCREEN = "fullscreen"
    HALF = "half"
    QUARTER = "quarter"


@dataclass
class ResizeConfig:
    """Resize configuration."""
    min_width: int = 400
    min_height: int = 300
    max_width: int = 1920
    max_height: int = 1080
    default_width: int = 800
    default_height: int = 600
    enable_constraints: bool = True
    enable_history: bool = True
    show_notifications: bool = True


@dataclass
class ResizeResult:
    """Resize result."""
    success: bool
    message: Optional[str] = None
    errors: List[str] = field(default_factory=list)
    width: Optional[int] = None
    height: Optional[int] = None
    previous_width: Optional[int] = None
    previous_height: Optional[int] = None


class TerminalResizeEngine:
    """
    Terminal resize management engine.
    
    Özellikler:
    - Resize terminal
    - Resize direction
    - Resize mode
    - Resize presets
    - Custom resize
    - Auto resize
    - Resize constraints
    - Resize validation
    - Resize undo
    - Resize history
    - Resize fit
    """
    
    def __init__(self, config: Optional[ResizeConfig] = None):
        """Initialize terminal resize engine."""
        self.config = config or ResizeConfig()
        self.current_width = self.config.default_width
        self.current_height = self.config.default_height
        self.resize_history: List[Dict[str, Any]] = []
    
    def resize(
        self,
        width: int,
        height: int,
        mode: Optional[ResizeMode] = None
    ) -> ResizeResult:
        """
        Terminali yeniden boyutlandır.
        
        Args:
            width: Genişlik
            height: Yükseklik
            mode: Boyutlandırma modu
            
        Returns:
            ResizeResult: Yeniden boyutlandırma sonucu
        """
        result = ResizeResult(success=False)
        result.previous_width = self.current_width
        result.previous_height = self.current_height
        
        try:
            # Validate
            if self.config.enable_constraints:
                validation = self._validate_size(width, height)
                if not validation:
                    result.errors.append(f"Size out of constraints: {width}x{height}")
                    return result
            
            # Resize
            self.current_width = width
            self.current_height = height
            
            # Add to history
            if self.config.enable_history:
                self.resize_history.append({
                    "action": "resize",
                    "width": width,
                    "height": height,
                    "previous_width": result.previous_width,
                    "previous_height": result.previous_height,
                    "mode": mode.value if mode else ResizeMode.MANUAL.value,
                    "timestamp": self._get_timestamp()
                })
            
            result.success = True
            result.width = width
            result.height = height
            result.message = f"Resized to {width}x{height}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def resize_horizontal(self, width: int) -> ResizeResult:
        """
    - Yatay yeniden boyutlandır.
        
        Args:
            width: Genişlik
            
        Returns:
            ResizeResult: Yeniden boyutlandırma sonucu
        """
        result = ResizeResult(success=False)
        result.previous_width = self.current_width
        
        try:
            # Validate
            if self.config.enable_constraints:
                if not self._validate_width(width):
                    result.errors.append(f"Width out of constraints: {width}")
                    return result
            
            # Resize
            self.current_width = width
            
            # Add to history
            if self.config.enable_history:
                self.resize_history.append({
                    "action": "resize_horizontal",
                    "width": width,
                    "previous_width": result.previous_width,
                    "direction": ResizeDirection.HORIZONTAL.value,
                    "timestamp": self._get_timestamp()
                })
            
            result.success = True
            result.width = width
            result.height = self.current_height
            result.message = f"Resized horizontally to {width}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def resize_vertical(self, height: int) -> ResizeResult:
        """
        Dikey yeniden boyutlandır.
        
        Args:
            height: Yükseklik
            
        Returns:
            ResizeResult: Yeniden boyutlandırma sonucu
        """
        result = ResizeResult(success=False)
        result.previous_height = self.current_height
        
        try:
            # Validate
            if self.config.enable_constraints:
                if not self._validate_height(height):
                    result.errors.append(f"Height out of constraints: {height}")
                    return result
            
            # Resize
            self.current_height = height
            
            # Add to history
            if self.config.enable_history:
                self.resize_history.append({
                    "action": "resize_vertical",
                    "height": height,
                    "previous_height": result.previous_height,
                    "direction": ResizeDirection.VERTICAL.value,
                    "timestamp": self._get_timestamp()
                })
            
            result.success = True
            result.width = self.current_width
            result.height = height
            result.message = f"Resized vertically to {height}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def apply_preset(self, preset: ResizePreset) -> ResizeResult:
        """
    - Ön ayar uygula.
        
        Args:
            preset: Ön ayar
            
        Returns:
            ResizeResult: Ön ayar uygulama sonucu
        """
        result = ResizeResult(success=False)
        result.previous_width = self.current_width
        result.previous_height = self.current_height
        
        try:
            # Get preset size
            width, height = self._get_preset_size(preset)
            
            # Resize
            self.current_width = width
            self.current_height = height
            
            # Add to history
            if self.config.enable_history:
                self.resize_history.append({
                    "action": "apply_preset",
                    "preset": preset.value,
                    "width": width,
                    "height": height,
                    "previous_width": result.previous_width,
                    "previous_height": result.previous_height,
                    "timestamp": self._get_timestamp()
                })
            
            result.success = True
            result.width = width
            result.height = height
            result.message = f"Applied preset: {preset.value}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def fit_to_content(self) -> ResizeResult:
        """
        İçeriğe sığdır.
        
        Returns:
            ResizeResult: Sığdırma sonucu
        """
        result = ResizeResult(success=False)
        result.previous_width = self.current_width
        result.previous_height = self.current_height
        
        try:
            # Calculate fit size (simplified)
            width = max(self.config.min_width, min(self.config.max_width, self.current_width))
            height = max(self.config.min_height, min(self.config.max_height, self.current_height))
            
            # Resize
            self.current_width = width
            self.current_height = height
            
            # Add to history
            if self.config.enable_history:
                self.resize_history.append({
                    "action": "fit_to_content",
                    "width": width,
                    "height": height,
                    "previous_width": result.previous_width,
                    "previous_height": result.previous_height,
                    "timestamp": self._get_timestamp()
                })
            
            result.success = True
            result.width = width
            result.height = height
            result.message = f"Fitted to content: {width}x{height}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def undo_resize(self) -> ResizeResult:
        """
        Yeniden boyutlandırmayı geri al.
        
        Returns:
            ResizeResult: Geri alma sonucu
        """
        result = ResizeResult(success=False)
        
        try:
            if not self.resize_history:
                result.errors.append("No resize history to undo")
                return result
            
            # Get last resize
            last_resize = self.resize_history[-1]
            
            # Restore previous size
            self.current_width = last_resize.get("previous_width", self.config.default_width)
            self.current_height = last_resize.get("previous_height", self.config.default_height)
            
            # Remove from history
            self.resize_history.pop()
            
            result.success = True
            result.width = self.current_width
            result.height = self.current_height
            result.message = f"Undid resize: {self.current_width}x{self.current_height}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_current_size(self) -> Tuple[int, int]:
        """
        Mevcut boyutu al.
        
        Returns:
            Tuple[int, int]: (width, height)
        """
        return (self.current_width, self.current_height)
    
    def get_resize_history(self) -> List[Dict[str, Any]]:
        """
        Yeniden boyutlandırma geçmişini al.
        
        Returns:
            List[Dict[str, Any]]: Geçmiş
        """
        return self.resize_history
    
    def clear_history(self) -> ResizeResult:
        """
        Geçmişi temizle.
        
        Returns:
            ResizeResult: Temizleme sonucu
        """
        result = ResizeResult(success=False)
        
        try:
            self.resize_history.clear()
            result.success = True
            result.message = "Resize history cleared"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def update_config(self, config: ResizeConfig) -> ResizeResult:
        """
        Konfigürasyon güncelle.
        
        Args:
            config: Yeni konfigürasyon
            
        Returns:
            ResizeResult: Güncelleme sonucu
        """
        result = ResizeResult(success=False)
        
        try:
            self.config = config
            result.success = True
            result.message = "Config updated"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_config(self) -> ResizeConfig:
        """
        Konfigürasyon al.
        
        Returns:
            ResizeConfig: Konfigürasyon
        """
        return self.config
    
    def _validate_size(self, width: int, height: int) -> bool:
        """
        Boyutu doğrula.
        
        Args:
            width: Genişlik
            height: Yükseklik
            
        Returns:
            bool: Geçerli mi
        """
        return (
            self.config.min_width <= width <= self.config.max_width and
            self.config.min_height <= height <= self.config.max_height
        )
    
    def _validate_width(self, width: int) -> bool:
        """
        Genişliği doğrula.
        
        Args:
            width: Genişlik
            
        Returns:
            bool: Geçerli mi
        """
        return self.config.min_width <= width <= self.config.max_width
    
    def _validate_height(self, height: int) -> bool:
        """
        Yüksekliği doğrula.
        
        Args:
            height: Yükseklik
            
        Returns:
            bool: Geçerli mi
        """
        return self.config.min_height <= height <= self.config.max_height
    
    def _get_preset_size(self, preset: ResizePreset) -> Tuple[int, int]:
        """
        Ön ayar boyutunu al.
        
        Args:
            preset: Ön ayar
            
        Returns:
            Tuple[int, int]: (width, height)
        """
        presets = {
            ResizePreset.SMALL: (600, 400),
            ResizePreset.MEDIUM: (800, 600),
            ResizePreset.LARGE: (1200, 800),
            ResizePreset.FULLSCREEN: (1920, 1080),
            ResizePreset.HALF: (960, 540),
            ResizePreset.QUARTER: (480, 270)
        }
        return presets.get(preset, (self.config.default_width, self.config.default_height))
    
    def _get_timestamp(self) -> str:
        """
        Zaman damgası al.
        
        Returns:
            str: ISO format zaman damgası
        """
        return datetime.now().isoformat()


if __name__ == "__main__":
    # Basit test
    engine = TerminalResizeEngine()
    
    print("Terminal Resize Engine initialized")
    print(f"Current size: {engine.get_current_size()}")
