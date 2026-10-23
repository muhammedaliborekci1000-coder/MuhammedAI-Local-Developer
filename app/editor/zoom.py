"""
MuhammedAI Local Developer - Zoom
Zoom engine for code editor.
"""

from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from enum import Enum


class ZoomDirection(Enum):
    """Zoom direction."""
    IN = "in"
    OUT = "out"
    RESET = "reset"


class ZoomMode(Enum):
    """Zoom mode."""
    LINEAR = "linear"
    EXPONENTIAL = "exponential"
    LOGARITHMIC = "logarithmic"


@dataclass
class ZoomConfig:
    """Zoom configuration."""
    min_zoom: float = 0.5
    max_zoom: float = 3.0
    default_zoom: float = 1.0
    zoom_step: float = 0.1
    mode: ZoomMode = ZoomMode.LINEAR
    smooth_zoom: bool = True
    zoom_animation_duration: int = 200
    preserve_line_height: bool = True
    adjust_font_size: bool = True


@dataclass
class ZoomResult:
    """Zoom result."""
    success: bool
    current_zoom: float = 1.0
    previous_zoom: float = 1.0
    errors: List[str] = field(default_factory=list)
    message: Optional[str] = None


class ZoomEngine:
    """
    Zoom engine.
    
    Özellikler:
    - Zoom in
    - Zoom out
    - Reset zoom
    - Set zoom level
    - Linear zoom
    - Exponential zoom
    - Logarithmic zoom
    - Smooth zoom
    - Zoom animation
    - Preserve line height
    - Adjust font size
    - Min/max zoom limits
    - Zoom history
    - Undo support
    - Smart zoom
    """
    
    def __init__(self, config: Optional[ZoomConfig] = None):
        """Initialize zoom engine."""
        self.config = config or ZoomConfig()
        self.current_zoom = self.config.default_zoom
        self.zoom_history: List[float] = []
    
    def zoom_in(self, steps: int = 1) -> ZoomResult:
        """
        Zoom in.
        
        Args:
            steps: Adım sayısı
            
        Returns:
            ZoomResult: Zoom sonucu
        """
        result = ZoomResult(success=False)
        result.previous_zoom = self.current_zoom
        
        try:
            for _ in range(steps):
                if self.config.mode == ZoomMode.LINEAR:
                    new_zoom = self.current_zoom + self.config.zoom_step
                elif self.config.mode == ZoomMode.EXPONENTIAL:
                    new_zoom = self.current_zoom * (1 + self.config.zoom_step)
                elif self.config.mode == ZoomMode.LOGARITHMIC:
                    new_zoom = self.current_zoom + (self.config.zoom_step / self.current_zoom)
                else:
                    new_zoom = self.current_zoom + self.config.zoom_step
                
                # Check max limit
                if new_zoom <= self.config.max_zoom:
                    self.current_zoom = new_zoom
                else:
                    self.current_zoom = self.config.max_zoom
                    break
            
            # Geçmişe ekle
            self.zoom_history.append(result.previous_zoom)
            
            result.success = True
            result.current_zoom = self.current_zoom
            result.message = f"Zoomed in to {self.current_zoom:.2f}x"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def zoom_out(self, steps: int = 1) -> ZoomResult:
        """
        Zoom out.
        
        Args:
            steps: Adım sayısı
            
        Returns:
            ZoomResult: Zoom sonucu
        """
        result = ZoomResult(success=False)
        result.previous_zoom = self.current_zoom
        
        try:
            for _ in range(steps):
                if self.config.mode == ZoomMode.LINEAR:
                    new_zoom = self.current_zoom - self.config.zoom_step
                elif self.config.mode == ZoomMode.EXPONENTIAL:
                    new_zoom = self.current_zoom / (1 + self.config.zoom_step)
                elif self.config.mode == ZoomMode.LOGARITHMIC:
                    new_zoom = self.current_zoom - (self.config.zoom_step / self.current_zoom)
                else:
                    new_zoom = self.current_zoom - self.config.zoom_step
                
                # Check min limit
                if new_zoom >= self.config.min_zoom:
                    self.current_zoom = new_zoom
                else:
                    self.current_zoom = self.config.min_zoom
                    break
            
            # Geçmişe ekle
            self.zoom_history.append(result.previous_zoom)
            
            result.success = True
            result.current_zoom = self.current_zoom
            result.message = f"Zoomed out to {self.current_zoom:.2f}x"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def reset_zoom(self) -> ZoomResult:
        """
        Zoom'u sıfırla.
        
        Returns:
            ZoomResult: Sıfırlama sonucu
        """
        result = ZoomResult(success=False)
        result.previous_zoom = self.current_zoom
        
        try:
            self.zoom_history.append(self.current_zoom)
            self.current_zoom = self.config.default_zoom
            
            result.success = True
            result.current_zoom = self.current_zoom
            result.message = f"Zoom reset to {self.current_zoom:.2f}x"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def set_zoom(self, zoom_level: float) -> ZoomResult:
        """
        Zoom seviyesini ayarla.
        
        Args:
            zoom_level: Zoom seviyesi
            
        Returns:
            ZoomResult: Ayarlama sonucu
        """
        result = ZoomResult(success=False)
        result.previous_zoom = self.current_zoom
        
        try:
            if zoom_level < self.config.min_zoom:
                result.errors.append(f"Zoom level must be at least {self.config.min_zoom}")
                return result
            
            if zoom_level > self.config.max_zoom:
                result.errors.append(f"Zoom level must be at most {self.config.max_zoom}")
                return result
            
            self.zoom_history.append(self.current_zoom)
            self.current_zoom = zoom_level
            
            result.success = True
            result.current_zoom = self.current_zoom
            result.message = f"Zoom set to {self.current_zoom:.2f}x"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_zoom(self) -> float:
        """
        Mevcut zoom seviyesini al.
        
        Returns:
            float: Zoom seviyesi
        """
        return self.current_zoom
    
    def get_zoom_percentage(self) -> int:
        """
        Zoom yüzdesini al.
        
        Returns:
            int: Zoom yüzdesi
        """
        return int(self.current_zoom * 100)
    
    def undo_zoom(self) -> ZoomResult:
        """
        Zoom'u geri al.
        
        Returns:
            ZoomResult: Geri alma sonucu
        """
        result = ZoomResult(success=False)
        result.previous_zoom = self.current_zoom
        
        try:
            if not self.zoom_history:
                result.errors.append("No zoom history")
                return result
            
            previous_zoom = self.zoom_history.pop()
            self.current_zoom = previous_zoom
            
            result.success = True
            result.current_zoom = self.current_zoom
            result.message = f"Zoom undone to {self.current_zoom:.2f}x"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_zoom_history(self) -> List[float]:
        """
        Zoom geçmişini al.
        
        Returns:
            List[float]: Geçmiş
        """
        return self.zoom_history
    
    def clear_history(self) -> ZoomResult:
        """
        Geçmişi temizle.
        
        Returns:
            ZoomResult: Temizleme sonucu
        """
        result = ZoomResult(success=False)
        
        try:
            self.zoom_history.clear()
            result.success = True
            result.message = "Zoom history cleared"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def update_config(self, config: ZoomConfig) -> ZoomResult:
        """
        Konfigürasyon güncelle.
        
        Args:
            config: Yeni konfigürasyon
            
        Returns:
            ZoomResult: Güncelleme sonucu
        """
        result = ZoomResult(success=False)
        
        try:
            self.config = config
            result.success = True
            result.message = "Config updated"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_config(self) -> ZoomConfig:
        """
        Konfigürasyon al.
        
        Returns:
            ZoomConfig: Konfigürasyon
        """
        return self.config
    
    def can_zoom_in(self) -> bool:
        """
        Zoom in yapılabilir mi?
        
        Returns:
            bool: Zoom in yapılabilir mi
        """
        return self.current_zoom < self.config.max_zoom
    
    def can_zoom_out(self) -> bool:
        """
        Zoom out yapılabilir mi?
        
        Returns:
            bool: Zoom out yapılabilir mi
        """
        return self.current_zoom > self.config.min_zoom
    
    def get_font_size(self, base_font_size: int) -> int:
        """
        Font boyutunu al.
        
        Args:
            base_font_size: Temel font boyutu
            
        Returns:
            int: Font boyutu
        """
        if self.config.adjust_font_size:
            return int(base_font_size * self.current_zoom)
        return base_font_size
    
    def get_line_height(self, base_line_height: int) -> int:
        """
        Satır yüksekliğini al.
        
        Args:
            base_line_height: Temel satır yüksekliği
            
        Returns:
            int: Satır yüksekliği
        """
        if self.config.preserve_line_height:
            return int(base_line_height * self.current_zoom)
        return base_line_height


if __name__ == "__main__":
    # Basit test
    engine = ZoomEngine()
    
    result = engine.zoom_in()
    print(f"Zoom: {result.success}")
    print(f"Current zoom: {result.current_zoom}")
