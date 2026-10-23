"""
MuhammedAI Local Developer - Glyph Margin
Glyph margin system for code editor.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum


class GlyphType(Enum):
    """Glyph type."""
    BREAKPOINT = "breakpoint"
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
    SUCCESS = "success"
    BOOKMARK = "bookmark"
    FOLDED = "folded"
    UNFOLDED = "unfolded"
    CUSTOM = "custom"


class GlyphPosition(Enum):
    """Glyph position."""
    LEFT = "left"
    RIGHT = "right"
    CENTER = "center"


@dataclass
class Glyph:
    """Glyph."""
    id: str
    type: GlyphType
    line: int
    icon: str
    position: GlyphPosition = GlyphPosition.LEFT
    is_enabled: bool = True
    is_visible: bool = True
    tooltip: Optional[str] = None
    color: Optional[str] = None


@dataclass
class GlyphMarginConfig:
    """Glyph margin configuration."""
    enabled: bool = True
    position: GlyphPosition = GlyphPosition.LEFT
    width: int = 20
    show_breakpoints: bool = True
    show_errors: bool = True
    show_warnings: bool = True
    show_info: bool = True
    show_bookmarks: bool = True
    show_fold_icons: bool = True
    show_tooltips: bool = True
    animate_glyphs: bool = True
    max_glyphs_per_line: int = 5


@dataclass
class GlyphMarginResult:
    """Glyph margin result."""
    success: bool
    glyphs: List[Glyph] = field(default_factory=list)
    html: Optional[str] = None
    errors: List[str] = field(default_factory=list)
    message: Optional[str] = None


class GlyphMarginManager:
    """
    Glyph margin manager.
    
    Özellikler:
    - Breakpoint glyphs
    - Error glyphs
    - Warning glyphs
    - Info glyphs
    - Bookmark glyphs
    - Fold glyphs
    - Custom glyphs
    - Glyph positioning
    - Glyph priority
    - Glyph filtering
    - Glyph visibility
    - Glyph animations
    - Glyph scope
    - Glyph context
    """
    
    def __init__(self, config: Optional[GlyphMarginConfig] = None):
        """
        Initialize glyph margin manager.
        
        Args:
            config: Glyph margin configuration
        """
        self.config = config or GlyphMarginConfig()
        self.glyphs: Dict[str, Glyph] = {}
        self.glyph_id_counter = 0
        self._next_id()
    
    def _next_id(self) -> str:
        """
        Generate next glyph ID.
        
        Returns:
            str: Glyph ID
        """
        self.glyph_id_counter += 1
        return f"glyph_{self.glyph_id_counter}"
    
    def add_glyph(self, glyph: Glyph) -> GlyphMarginResult:
        """
        Add a glyph.
        
        Args:
            glyph: Glyph to add
            
        Returns:
            GlyphMarginResult: Add result
        """
        result = GlyphMarginResult(success=True)
        
        try:
            if not glyph.id:
                glyph.id = self._next_id()
            
            self.glyphs[glyph.id] = glyph
            result.glyphs = self.get_all_glyphs()
            result.message = f"Glyph '{glyph.id}' added"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def remove_glyph(self, glyph_id: str) -> GlyphMarginResult:
        """
        Remove a glyph.
        
        Args:
            glyph_id: Glyph ID
            
        Returns:
            GlyphMarginResult: Remove result
        """
        result = GlyphMarginResult(success=False)
        
        try:
            if glyph_id in self.glyphs:
                del self.glyphs[glyph_id]
                result.success = True
                result.glyphs = self.get_all_glyphs()
                result.message = f"Glyph '{glyph_id}' removed"
            else:
                result.errors.append("Glyph not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_glyph(self, glyph_id: str) -> Optional[Glyph]:
        """
        Get glyph by ID.
        
        Args:
            glyph_id: Glyph ID
            
        Returns:
            Optional[Glyph]: Glyph
        """
        return self.glyphs.get(glyph_id)
    
    def get_all_glyphs(self) -> List[Glyph]:
        """
        Get all glyphs.
        
        Returns:
            List[Glyph]: All glyphs
        """
        return list(self.glyphs.values())
    
    def get_glyphs_by_type(self, glyph_type: GlyphType) -> List[Glyph]:
        """
        Get glyphs by type.
        
        Args:
            glyph_type: Glyph type
            
        Returns:
            List[Glyph]: Glyphs
        """
        return [g for g in self.glyphs.values() if g.type == glyph_type]
    
    def get_glyphs_at_line(self, line: int) -> List[Glyph]:
        """
        Get glyphs at specific line.
        
        Args:
            line: Line number
            
        Returns:
            List[Glyph]: Glyphs
        """
        return [g for g in self.glyphs.values() if g.line == line]
    
    def add_breakpoint(self, line: int, icon: str = "●") -> GlyphMarginResult:
        """
        Add breakpoint glyph.
        
        Args:
            line: Line number
            icon: Icon string
            
        Returns:
            GlyphMarginResult: Add result
        """
        if not self.config.show_breakpoints:
            result = GlyphMarginResult(success=False)
            result.message = "Breakpoint glyphs disabled"
            return result
        
        glyph = Glyph(
            id="",
            type=GlyphType.BREAKPOINT,
            line=line,
            icon=icon,
            position=self.config.position
        )
        
        return self.add_glyph(glyph)
    
    def add_error(self, line: int, icon: str = "✗", message: str = "") -> GlyphMarginResult:
        """
        Add error glyph.
        
        Args:
            line: Line number
            icon: Icon string
            message: Error message
            
        Returns:
            GlyphMarginResult: Add result
        """
        if not self.config.show_errors:
            result = GlyphMarginResult(success=False)
            result.message = "Error glyphs disabled"
            return result
        
        glyph = Glyph(
            id="",
            type=GlyphType.ERROR,
            line=line,
            icon=icon,
            position=self.config.position,
            tooltip=message
        )
        
        return self.add_glyph(glyph)
    
    def add_warning(self, line: int, icon: str = "!", message: str = "") -> GlyphMarginResult:
        """
        Add warning glyph.
        
        Args:
            line: Line number
            icon: Icon string
            message: Warning message
            
        Returns:
            GlyphMarginResult: Add result
        """
        if not self.config.show_warnings:
            result = GlyphMarginResult(success=False)
            result.message = "Warning glyphs disabled"
            return result
        
        glyph = Glyph(
            id="",
            type=GlyphType.WARNING,
            line=line,
            icon=icon,
            position=self.config.position,
            tooltip=message
        )
        
        return self.add_glyph(glyph)
    
    def add_info(self, line: int, icon: str = "i", message: str = "") -> GlyphMarginResult:
        """
        Add info glyph.
        
        Args:
            line: Line number
            icon: Icon string
            message: Info message
            
        Returns:
            GlyphMarginResult: Add result
        """
        if not self.config.show_info:
            result = GlyphMarginResult(success=False)
            result.message = "Info glyphs disabled"
            return result
        
        glyph = Glyph(
            id="",
            type=GlyphType.INFO,
            line=line,
            icon=icon,
            position=self.config.position,
            tooltip=message
        )
        
        return self.add_glyph(glyph)
    
    def add_bookmark(self, line: int, icon: str = "★") -> GlyphMarginResult:
        """
        Add bookmark glyph.
        
        Args:
            line: Line number
            icon: Icon string
            
        Returns:
            GlyphMarginResult: Add result
        """
        if not self.config.show_bookmarks:
            result = GlyphMarginResult(success=False)
            result.message = "Bookmark glyphs disabled"
            return result
        
        glyph = Glyph(
            id="",
            type=GlyphType.BOOKMARK,
            line=line,
            icon=icon,
            position=self.config.position
        )
        
        return self.add_glyph(glyph)
    
    def toggle_fold(self, line: int, folded: bool) -> GlyphMarginResult:
        """
        Toggle fold glyph.
        
        Args:
            line: Line number
            folded: Folded state
            
        Returns:
            GlyphMarginResult: Toggle result
        """
        if not self.config.show_fold_icons:
            result = GlyphMarginResult(success=False)
            result.message = "Fold icons disabled"
            return result
        
        icon = "▼" if folded else "▶"
        glyph_type = GlyphType.FOLDED if folded else GlyphType.UNFOLDED
        
        glyph = Glyph(
            id="",
            type=glyph_type,
            line=line,
            icon=icon,
            position=self.config.position
        )
        
        return self.add_glyph(glyph)
    
    def clear_glyphs(self) -> GlyphMarginResult:
        """
        Clear all glyphs.
        
        Returns:
            GlyphMarginResult: Clear result
        """
        result = GlyphMarginResult(success=True)
        
        try:
            self.glyphs.clear()
            result.message = "All glyphs cleared"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def clear_glyphs_by_type(self, glyph_type: GlyphType) -> GlyphMarginResult:
        """
        Clear glyphs by type.
        
        Args:
            glyph_type: Glyph type
            
        Returns:
            GlyphMarginResult: Clear result
        """
        result = GlyphMarginResult(success=True)
        
        try:
            to_remove = [id for id, g in self.glyphs.items() if g.type == glyph_type]
            for id in to_remove:
                del self.glyphs[id]
            
            result.message = f"Cleared {len(to_remove)} {glyph_type.value} glyphs"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def set_glyph_enabled(self, glyph_id: str, enabled: bool) -> GlyphMarginResult:
        """
        Set glyph enabled state.
        
        Args:
            glyph_id: Glyph ID
            enabled: Enabled state
            
        Returns:
            GlyphMarginResult: Set result
        """
        result = GlyphMarginResult(success=False)
        
        try:
            glyph = self.glyphs.get(glyph_id)
            if glyph:
                glyph.is_enabled = enabled
                result.success = True
                result.message = f"Glyph '{glyph_id}' {'enabled' if enabled else 'disabled'}"
            else:
                result.errors.append("Glyph not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def set_glyph_visible(self, glyph_id: str, visible: bool) -> GlyphMarginResult:
        """
        Set glyph visible state.
        
        Args:
            glyph_id: Glyph ID
            visible: Visible state
            
        Returns:
            GlyphMarginResult: Set result
        """
        result = GlyphMarginResult(success=False)
        
        try:
            glyph = self.glyphs.get(glyph_id)
            if glyph:
                glyph.is_visible = visible
                result.success = True
                result.message = f"Glyph '{glyph_id}' {'visible' if visible else 'hidden'}"
            else:
                result.errors.append("Glyph not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def update_config(self, config: GlyphMarginConfig) -> GlyphMarginResult:
        """
        Update glyph margin configuration.
        
        Args:
            config: New configuration
            
        Returns:
            GlyphMarginResult: Update result
        """
        result = GlyphMarginResult(success=True)
        
        try:
            self.config = config
            result.message = "Config updated"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def get_config(self) -> GlyphMarginConfig:
        """
        Get glyph margin configuration.
        
        Returns:
            GlyphMarginConfig: Configuration
        """
        return self.config


if __name__ == "__main__":
    # Basit test
    config = GlyphMarginConfig()
    manager = GlyphMarginManager(config)
    
    # Glyph ekle
    result = manager.add_breakpoint(10)
    
    print(f"Glyph added: {result.message}")
    
    # Tüm glyph'ları al
    glyphs = manager.get_all_glyphs()
    
    print(f"Total glyphs: {len(glyphs)}")
