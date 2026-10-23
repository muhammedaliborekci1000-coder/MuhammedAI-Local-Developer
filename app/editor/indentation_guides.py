"""
MuhammedAI Local Developer - Indentation Guides
Indentation guides engine for code editor.
"""

from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from enum import Enum


class GuideStyle(Enum):
    """Guide style."""
    SOLID = "solid"
    DASHED = "dashed"
    DOTTED = "dotted"
    NONE = "none"


class GuideColor(Enum):
    """Guide color."""
    DEFAULT = "default"
    ACTIVE = "active"
    ERROR = "error"
    WARNING = "warning"


@dataclass
class IndentationLevel:
    """Indentation level."""
    level: int
    start_column: int
    end_column: int
    is_active: bool = False
    has_error: bool = False


@dataclass
class IndentationGuide:
    """Indentation guide."""
    line: int
    column: int
    level: int
    style: GuideStyle = GuideStyle.SOLID
    color: GuideColor = GuideColor.DEFAULT
    is_active: bool = False


@dataclass
class IndentationConfig:
    """Indentation configuration."""
    enabled: bool = True
    show_guides: bool = True
    guide_style: GuideStyle = GuideStyle.SOLID
    guide_color: GuideColor = GuideColor.DEFAULT
    show_active_guide: bool = True
    show_bracket_guides: bool = True
    show_indent_levels: bool = False
    tab_size: int = 4
    use_tabs: bool = False
    highlight_active_line: bool = True
    rainbow_indentation: bool = False


@dataclass
class IndentationResult:
    """Indentation result."""
    success: bool
    guides: List[IndentationGuide] = field(default_factory=list)
    levels: List[IndentationLevel] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    message: Optional[str] = None


class IndentationGuidesEngine:
    """
    Indentation guides engine.
    
    Özellikler:
    - Guide rendering
    - Level detection
    - Active guide highlighting
    - Bracket guide rendering
    - Rainbow indentation
    - Customizable styles
    - Tab/space handling
    - Error detection
    - Warning detection
    - Multi-language support
    - Auto-indent detection
    - Guide visibility control
    - Color customization
    - Style customization
    """
    
    def __init__(self, config: Optional[IndentationConfig] = None):
        """Initialize indentation guides engine."""
        self.config = config or IndentationConfig()
        self.guides: List[IndentationGuide] = []
        self.levels: List[IndentationLevel] = []
    
    def calculate_indentation(
        self,
        code: str,
        current_line: int = 0,
        language: str = "python"
    ) -> IndentationResult:
        """
        Indentation hesapla.
        
        Args:
            code: Kod içeriği
            current_line: Mevcut satır
            language: Programlama dili
            
        Returns:
            IndentationResult: Hesaplama sonucu
        """
        result = IndentationResult(success=False)
        
        try:
            if not self.config.enabled:
                result.message = "Indentation guides disabled"
                return result
            
            lines = code.splitlines()
            guides = []
            levels = []
            
            for line_idx, line in enumerate(lines):
                # Leading whitespace'ı hesapla
                leading_spaces = len(line) - len(line.lstrip())
                leading_tabs = line.count('\t', 0, leading_spaces)
                
                # Tab size hesapla
                if self.config.use_tabs:
                    indent_size = leading_tabs * self.config.tab_size
                else:
                    indent_size = leading_spaces
                
                # Level hesapla
                level = indent_size // self.config.tab_size
                
                # Guide'ları oluştur
                for lvl in range(1, level + 1):
                    column = lvl * self.config.tab_size
                    
                    guide = IndentationGuide(
                        line=line_idx,
                        column=column,
                        level=lvl,
                        style=self.config.guide_style,
                        color=self._get_guide_color(lvl, line_idx == current_line),
                        is_active=line_idx == current_line and lvl == level
                    )
                    guides.append(guide)
                
                # Level kaydı
                level_info = IndentationLevel(
                    level=level,
                    start_column=0,
                    end_column=indent_size,
                    is_active=line_idx == current_line
                )
                levels.append(level_info)
            
            self.guides = guides
            self.levels = levels
            
            result.success = True
            result.guides = guides
            result.levels = levels
            result.message = f"Calculated {len(guides)} guides"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def _get_guide_color(self, level: int, is_active: bool) -> GuideColor:
        """
        Guide rengi al.
        
        Args:
            level: Level
            is_active: Active mi
            
        Returns:
            GuideColor: Renk
        """
        if is_active:
            return GuideColor.ACTIVE
        
        if self.config.rainbow_indentation:
            colors = [GuideColor.DEFAULT, GuideColor.ACTIVE, GuideColor.WARNING, GuideColor.ERROR]
            return colors[level % len(colors)]
        
        return GuideColor.DEFAULT
    
    def get_guide_at_position(self, line: int, column: int) -> Optional[IndentationGuide]:
        """
        Pozisyondaki guide'ı al.
        
        Args:
            line: Satır
            column: Sütun
            
        Returns:
            Optional[IndentationGuide]: Guide
        """
        for guide in self.guides:
            if guide.line == line and guide.column == column:
                return guide
        return None
    
    def get_guides_for_line(self, line: int) -> List[IndentationGuide]:
        """
        Satır için guide'ları al.
        
        Args:
            line: Satır numarası
            
        Returns:
            List[IndentationGuide]: Guide listesi
        """
        return [g for g in self.guides if g.line == line]
    
    def get_level_for_line(self, line: int) -> int:
        """
        Satırın level'ını al.
        
        Args:
            line: Satır numarası
            
        Returns:
            int: Level
        """
        for level_info in self.levels:
            if level_info.level == line:
                return level_info.level
        return 0
    
    def update_config(self, config: IndentationConfig) -> IndentationResult:
        """
        Konfigürasyon güncelle.
        
        Args:
            config: Yeni konfigürasyon
            
        Returns:
            IndentationResult: Güncelleme sonucu
        """
        result = IndentationResult(success=False)
        
        try:
            self.config = config
            result.success = True
            result.message = "Config updated"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_config(self) -> IndentationConfig:
        """
        Konfigürasyon al.
        
        Returns:
            IndentationConfig: Konfigürasyon
        """
        return self.config
    
    def toggle_guides(self) -> IndentationResult:
        """
        Guide'ları aç/kapat.
        
        Returns:
            IndentationResult: Toggle sonucu
        """
        result = IndentationResult(success=False)
        
        try:
            self.config.show_guides = not self.config.show_guides
            result.success = True
            result.message = f"Guides {'enabled' if self.config.show_guides else 'disabled'}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def set_guide_style(self, style: GuideStyle) -> IndentationResult:
        """
        Guide stili ayarla.
        
        Args:
            style: Guide stili
            
        Returns:
            IndentationResult: Ayarlama sonucu
        """
        result = IndentationResult(success=False)
        
        try:
            self.config.guide_style = style
            result.success = True
            result.message = f"Guide style set to {style.value}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def set_guide_color(self, color: GuideColor) -> IndentationResult:
        """
        Guide rengi ayarla.
        
        Args:
            color: Guide rengi
            
        Returns:
            IndentationResult: Ayarlama sonucu
        """
        result = IndentationResult(success=False)
        
        try:
            self.config.guide_color = color
            result.success = True
            result.message = f"Guide color set to {color.value}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def set_tab_size(self, tab_size: int) -> IndentationResult:
        """
        Tab boyutu ayarla.
        
        Args:
            tab_size: Tab boyutu
            
        Returns:
            IndentationResult: Ayarlama sonucu
        """
        result = IndentationResult(success=False)
        
        try:
            if tab_size > 0:
                self.config.tab_size = tab_size
                result.success = True
                result.message = f"Tab size set to {tab_size}"
            else:
                result.errors.append("Tab size must be positive")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def set_use_tabs(self, use_tabs: bool) -> IndentationResult:
        """
        Tab kullanımını ayarla.
        
        Args:
            use_tabs: Tab kullanımı
            
        Returns:
            IndentationResult: Ayarlama sonucu
        """
        result = IndentationResult(success=False)
        
        try:
            self.config.use_tabs = use_tabs
            result.success = True
            result.message = f"Use tabs set to {use_tabs}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def toggle_rainbow_indentation(self) -> IndentationResult:
        """
        Rainbow indentation'ı aç/kapat.
        
        Returns:
            IndentationResult: Toggle sonucu
        """
        result = IndentationResult(success=False)
        
        try:
            self.config.rainbow_indentation = not self.config.rainbow_indentation
            result.success = True
            result.message = f"Rainbow indentation {'enabled' if self.config.rainbow_indentation else 'disabled'}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_all_guides(self) -> List[IndentationGuide]:
        """
        Tüm guide'ları al.
        
        Returns:
            List[IndentationGuide]: Guide listesi
        """
        return self.guides
    
    def get_all_levels(self) -> List[IndentationLevel]:
        """
        Tüm level'ları al.
        
        Returns:
            List[IndentationLevel]: Level listesi
        """
        return self.levels


if __name__ == "__main__":
    # Basit test
    config = IndentationConfig()
    engine = IndentationGuidesEngine(config)
    
    code = """def my_function():
    x = 10
    if x > 5:
        print("Hello")
"""
    
    result = engine.calculate_indentation(code, current_line=0)
    print(f"Calculated: {result.success}")
    print(f"Guides: {len(result.guides)}")
