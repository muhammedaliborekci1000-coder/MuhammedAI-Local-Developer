"""
MuhammedAI Local Developer - Whitespace Rendering
Whitespace rendering system for code editor.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum


class WhitespaceType(Enum):
    """Whitespace type."""
    SPACE = "space"
    TAB = "tab"
    NEWLINE = "newline"
    CARRIAGE_RETURN = "carriage_return"
    FORM_FEED = "form_feed"
    VERTICAL_TAB = "vertical_tab"


class WhitespaceRenderMode(Enum):
    """Whitespace render mode."""
    NONE = "none"
    BOUNDARIES = "boundaries"
    ALL = "all"
    CUSTOM = "custom"


@dataclass
class WhitespaceGlyph:
    """Whitespace glyph."""
    type: WhitespaceType
    glyph: str
    color: str = "#808080"
    size: int = 12


@dataclass
class WhitespaceConfig:
    """Whitespace configuration."""
    render_mode: WhitespaceRenderMode = WhitespaceRenderMode.BOUNDARIES
    show_spaces: bool = True
    show_tabs: bool = True
    show_newlines: bool = False
    show_trailing: bool = True
    show_leading: bool = False
    show_in_selection: bool = True
    space_glyph: str = "·"
    tab_glyph: str = "→"
    newline_glyph: str = "¶"
    custom_glyphs: Dict[WhitespaceType, str] = field(default_factory=dict)
    glyph_color: str = "#808080"
    glyph_size: int = 12


@dataclass
class WhitespaceRenderResult:
    """Whitespace render result."""
    success: bool
    rendered_text: Optional[str] = None
    html: Optional[str] = None
    errors: List[str] = field(default_factory=list)
    message: Optional[str] = None


class WhitespaceRenderer:
    """
    Whitespace renderer.
    
    Özellikler:
    - Space rendering
    - Tab rendering
    - Newline rendering
    - Trailing whitespace rendering
    - Leading whitespace rendering
    - Custom glyphs
    - Render modes
    - Color customization
    - Size customization
    - Selection rendering
    - Boundary rendering
    - All whitespace rendering
    - Custom rendering
    """
    
    def __init__(self, config: Optional[WhitespaceConfig] = None):
        """
        Initialize whitespace renderer.
        
        Args:
            config: Whitespace configuration
        """
        self.config = config or WhitespaceConfig()
        self._initialize_default_glyphs()
    
    def _initialize_default_glyphs(self) -> None:
        """Initialize default glyphs."""
        self.glyphs = {
            WhitespaceType.SPACE: WhitespaceGlyph(
                type=WhitespaceType.SPACE,
                glyph=self.config.space_glyph,
                color=self.config.glyph_color,
                size=self.config.glyph_size
            ),
            WhitespaceType.TAB: WhitespaceGlyph(
                type=WhitespaceType.TAB,
                glyph=self.config.tab_glyph,
                color=self.config.glyph_color,
                size=self.config.glyph_size
            ),
            WhitespaceType.NEWLINE: WhitespaceGlyph(
                type=WhitespaceType.NEWLINE,
                glyph=self.config.newline_glyph,
                color=self.config.glyph_color,
                size=self.config.glyph_size
            )
        }
        
        # Add custom glyphs
        for wtype, glyph in self.config.custom_glyphs.items():
            self.glyphs[wtype] = WhitespaceGlyph(
                type=wtype,
                glyph=glyph,
                color=self.config.glyph_color,
                size=self.config.glyph_size
            )
    
    def render(self, text: str) -> WhitespaceRenderResult:
        """
        Render whitespace in text.
        
        Args:
            text: Text to render
            
        Returns:
            WhitespaceRenderResult: Render result
        """
        result = WhitespaceRenderResult(success=True)
        
        try:
            rendered = text
            
            if self.config.render_mode == WhitespaceRenderMode.NONE:
                result.rendered_text = text
                result.message = "Whitespace rendering disabled"
                return result
            
            # Render spaces
            if self.config.show_spaces:
                rendered = rendered.replace(" ", self.glyphs[WhitespaceType.SPACE].glyph)
            
            # Render tabs
            if self.config.show_tabs:
                rendered = rendered.replace("\t", self.glyphs[WhitespaceType.TAB].glyph)
            
            # Render newlines
            if self.config.show_newlines:
                rendered = rendered.replace("\n", self.glyphs[WhitespaceType.NEWLINE].glyph + "\n")
            
            result.rendered_text = rendered
            result.html = self._generate_html(rendered)
            result.message = f"Whitespace rendered ({self.config.render_mode.value})"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def render_trailing(self, text: str) -> WhitespaceRenderResult:
        """
        Render trailing whitespace.
        
        Args:
            text: Text to render
            
        Returns:
            WhitespaceRenderResult: Render result
        """
        result = WhitespaceRenderResult(success=True)
        
        try:
            if not self.config.show_trailing:
                result.rendered_text = text
                result.message = "Trailing whitespace rendering disabled"
                return result
            
            lines = text.splitlines()
            rendered_lines = []
            
            for line in lines:
                stripped = line.rstrip()
                trailing = line[len(stripped):]
                
                if trailing:
                    rendered_trailing = trailing
                    if self.config.show_spaces:
                        rendered_trailing = rendered_trailing.replace(" ", self.glyphs[WhitespaceType.SPACE].glyph)
                    if self.config.show_tabs:
                        rendered_trailing = rendered_trailing.replace("\t", self.glyphs[WhitespaceType.TAB].glyph)
                    rendered_lines.append(stripped + rendered_trailing)
                else:
                    rendered_lines.append(line)
            
            result.rendered_text = "\n".join(rendered_lines)
            result.message = "Trailing whitespace rendered"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def render_leading(self, text: str) -> WhitespaceRenderResult:
        """
        Render leading whitespace.
        
        Args:
            text: Text to render
            
        Returns:
            WhitespaceRenderResult: Render result
        """
        result = WhitespaceRenderResult(success=True)
        
        try:
            if not self.config.show_leading:
                result.rendered_text = text
                result.message = "Leading whitespace rendering disabled"
                return result
            
            lines = text.splitlines()
            rendered_lines = []
            
            for line in lines:
                stripped = line.lstrip()
                leading = line[:len(line) - len(stripped)]
                
                if leading:
                    rendered_leading = leading
                    if self.config.show_spaces:
                        rendered_leading = rendered_leading.replace(" ", self.glyphs[WhitespaceType.SPACE].glyph)
                    if self.config.show_tabs:
                        rendered_leading = rendered_leading.replace("\t", self.glyphs[WhitespaceType.TAB].glyph)
                    rendered_lines.append(rendered_leading + stripped)
                else:
                    rendered_lines.append(line)
            
            result.rendered_text = "\n".join(rendered_lines)
            result.message = "Leading whitespace rendered"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def set_glyph(self, wtype: WhitespaceType, glyph: str) -> WhitespaceRenderResult:
        """
        Set glyph for whitespace type.
        
        Args:
            wtype: Whitespace type
            glyph: Glyph string
            
        Returns:
            WhitespaceRenderResult: Set result
        """
        result = WhitespaceRenderResult(success=True)
        
        try:
            if wtype in self.glyphs:
                self.glyphs[wtype].glyph = glyph
                result.message = f"Glyph for {wtype.value} set to '{glyph}'"
            else:
                self.glyphs[wtype] = WhitespaceGlyph(
                    type=wtype,
                    glyph=glyph,
                    color=self.config.glyph_color,
                    size=self.config.glyph_size
                )
                result.message = f"New glyph for {wtype.value} set to '{glyph}'"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def set_glyph_color(self, wtype: WhitespaceType, color: str) -> WhitespaceRenderResult:
        """
        Set glyph color.
        
        Args:
            wtype: Whitespace type
            color: Color string
            
        Returns:
            WhitespaceRenderResult: Set result
        """
        result = WhitespaceRenderResult(success=True)
        
        try:
            if wtype in self.glyphs:
                self.glyphs[wtype].color = color
                result.message = f"Glyph color for {wtype.value} set to '{color}'"
            else:
                result.errors.append("Whitespace type not found")
                result.success = False
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def update_config(self, config: WhitespaceConfig) -> WhitespaceRenderResult:
        """
        Update whitespace configuration.
        
        Args:
            config: New configuration
            
        Returns:
            WhitespaceRenderResult: Update result
        """
        result = WhitespaceRenderResult(success=True)
        
        try:
            self.config = config
            self._initialize_default_glyphs()
            result.message = "Config updated"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def get_config(self) -> WhitespaceConfig:
        """
        Get whitespace configuration.
        
        Returns:
            WhitespaceConfig: Configuration
        """
        return self.config
    
    def get_glyph(self, wtype: WhitespaceType) -> Optional[WhitespaceGlyph]:
        """
        Get glyph for whitespace type.
        
        Args:
            wtype: Whitespace type
            
        Returns:
            Optional[WhitespaceGlyph]: Glyph
        """
        return self.glyphs.get(wtype)
    
    def _generate_html(self, text: str) -> str:
        """
        Generate HTML output.
        
        Args:
            text: Rendered text
            
        Returns:
            str: HTML
        """
        html = text.replace("\n", "<br>")
        return f'<div class="whitespace-rendered">{html}</div>'


if __name__ == "__main__":
    # Basit test
    config = WhitespaceConfig()
    renderer = WhitespaceRenderer(config)
    
    # Render
    text = "hello world\n\tindented line"
    result = renderer.render(text)
    
    print(f"Rendered: {result.message}")
    print(f"Text: {result.rendered_text}")
