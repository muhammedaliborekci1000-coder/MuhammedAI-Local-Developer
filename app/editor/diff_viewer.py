"""
MuhammedAI Local Developer - Diff Viewer
Diff viewer engine for code editor.
"""

from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from enum import Enum


class DiffViewMode(Enum):
    """Diff view mode."""
    UNIFIED = "unified"
    SIDE_BY_SIDE = "side_by_side"
    INLINE = "inline"
    SPLIT = "split"


class DiffTheme(Enum):
    """Diff theme."""
    LIGHT = "light"
    DARK = "dark"
    HIGH_CONTRAST = "high_contrast"
    MONOCHROME = "monochrome"


class ScrollMode(Enum):
    """Scroll mode."""
    SYNC = "sync"
    INDEPENDENT = "independent"
    LOCKED = "locked"


class ZoomLevel(Enum):
    """Zoom level."""
    SMALL = "small"
    NORMAL = "normal"
    LARGE = "large"
    EXTRA_LARGE = "extra_large"


@dataclass
class DiffLine:
    """Diff line."""
    line_number: int
    content: str
    line_type: str  # added, removed, unchanged, context
    old_line_number: Optional[int] = None
    new_line_number: Optional[int] = None


@dataclass
class DiffHunk:
    """Diff hunk."""
    old_start: int
    old_count: int
    new_start: int
    new_count: int
    lines: List[DiffLine] = field(default_factory=list)
    header: str = ""


@dataclass
class DiffFile:
    """Diff file."""
    file_path: str
    old_file: Optional[str] = None
    new_file: Optional[str] = None
    hunks: List[DiffHunk] = field(default_factory=list)
    added_lines: int = 0
    removed_lines: int = 0
    is_binary: bool = False


@dataclass
class ViewerConfig:
    """Viewer configuration."""
    view_mode: DiffViewMode = DiffViewMode.UNIFIED
    theme: DiffTheme = DiffTheme.DARK
    scroll_mode: ScrollMode = ScrollMode.SYNC
    zoom_level: ZoomLevel = ZoomLevel.NORMAL
    show_line_numbers: bool = True
    show_whitespace: bool = False
    show_context: bool = True
    context_lines: int = 3
    word_wrap: bool = False
    auto_scroll: bool = True
    highlight_changes: bool = True
    show_file_header: bool = True
    show_hunk_header: bool = True


@dataclass
class ViewerState:
    """Viewer state."""
    current_file_index: int = 0
    current_hunk_index: int = 0
    scroll_position: int = 0
    zoom_factor: float = 1.0
    is_loading: bool = False
    has_changes: bool = False


@dataclass
class ViewerResult:
    """Viewer result."""
    success: bool
    action: Optional[str] = None
    message: Optional[str] = None
    errors: List[str] = field(default_factory=list)
    files: List[DiffFile] = field(default_factory=list)
    total_files: int = 0
    total_added: int = 0
    total_removed: int = 0


class DiffViewerEngine:
    """
    Diff viewer engine.
    
    Özellikler:
    - Unified diff view
    - Side-by-side diff view
    - Inline diff view
    - Diff rendering
    - Diff scrolling
    - Diff zoom
    - Diff theme
    - Line numbers
    - Whitespace display
    - Context display
    - Word wrap
    - Auto scroll
    - Change highlighting
    - File header display
    - Hunk header display
    - Sync scrolling
    - Independent scrolling
    - Locked scrolling
    - Zoom levels
    - Theme switching
    - View mode switching
    - File navigation
    - Hunk navigation
    - Scroll position tracking
    - State management
    - Configuration management
    """
    
    def __init__(self, config: Optional[ViewerConfig] = None):
        """Initialize diff viewer engine."""
        self.config = config or ViewerConfig()
        self.state = ViewerState()
        self.files: List[DiffFile] = []
        self.viewer_history: List[Tuple[str, str]] = []  # (action, target)
    
    def load_diff(
        self,
        old_content: str,
        new_content: str,
        file_path: str = "file.txt"
    ) -> ViewerResult:
        """
        Diff yükle.
        
        Args:
            old_content: Eski içerik
            new_content: Yeni içerik
            file_path: Dosya yolu
            
        Returns:
            ViewerResult: Yükleme sonucu
        """
        result = ViewerResult(success=False)
        result.action = "load_diff"
        
        try:
            # Diff oluştur
            diff_file = self._create_diff(old_content, new_content, file_path)
            
            self.files = [diff_file]
            self.state.current_file_index = 0
            self.state.current_hunk_index = 0
            self.state.scroll_position = 0
            self.state.has_changes = diff_file.added_lines > 0 or diff_file.removed_lines > 0
            
            result.files = self.files
            result.total_files = len(self.files)
            result.total_added = diff_file.added_lines
            result.total_removed = diff_file.removed_lines
            result.success = True
            result.message = f"Loaded diff for {file_path}"
            
            self.viewer_history.append(("load_diff", file_path))
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def set_view_mode(self, mode: DiffViewMode) -> ViewerResult:
        """
        Görünüm modunu ayarla.
        
        Args:
            mode: Görünüm modu
            
        Returns:
            ViewerResult: Ayarlama sonucu
        """
        result = ViewerResult(success=False)
        result.action = "set_view_mode"
        
        try:
            self.config.view_mode = mode
            result.success = True
            result.message = f"View mode set to {mode.value}"
            
            self.viewer_history.append(("set_view_mode", mode.value))
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def set_theme(self, theme: DiffTheme) -> ViewerResult:
        """
        Tema ayarla.
        
        Args:
            theme: Tema
            
        Returns:
            ViewerResult: Ayarlama sonucu
        """
        result = ViewerResult(success=False)
        result.action = "set_theme"
        
        try:
            self.config.theme = theme
            result.success = True
            result.message = f"Theme set to {theme.value}"
            
            self.viewer_history.append(("set_theme", theme.value))
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def set_scroll_mode(self, mode: ScrollMode) -> ViewerResult:
        """
    Scroll modunu ayarla.
        
        Args:
            mode: Scroll modu
            
        Returns:
            ViewerResult: Ayarlama sonucu
        """
        result = ViewerResult(success=False)
        result.action = "set_scroll_mode"
        
        try:
            self.config.scroll_mode = mode
            result.success = True
            result.message = f"Scroll mode set to {mode.value}"
            
            self.viewer_history.append(("set_scroll_mode", mode.value))
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def set_zoom_level(self, level: ZoomLevel) -> ViewerResult:
        """
        Zoom seviyesini ayarla.
        
        Args:
            level: Zoom seviyesi
            
        Returns:
            ViewerResult: Ayarlama sonucu
        """
        result = ViewerResult(success=False)
        result.action = "set_zoom_level"
        
        try:
            self.config.zoom_level = level
            
            # Zoom faktörünü ayarla
            zoom_factors = {
                ZoomLevel.SMALL: 0.8,
                ZoomLevel.NORMAL: 1.0,
                ZoomLevel.LARGE: 1.2,
                ZoomLevel.EXTRA_LARGE: 1.5
            }
            self.state.zoom_factor = zoom_factors.get(level, 1.0)
            
            result.success = True
            result.message = f"Zoom level set to {level.value}"
            
            self.viewer_history.append(("set_zoom_level", level.value))
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def scroll_to(self, position: int) -> ViewerResult:
        """
        Belirli bir konuma scroll et.
        
        Args:
            position: Scroll pozisyonu
            
        Returns:
            ViewerResult: Scroll sonucu
        """
        result = ViewerResult(success=False)
        result.action = "scroll_to"
        
        try:
            self.state.scroll_position = max(0, position)
            result.success = True
            result.message = f"Scrolled to position {position}"
            
            self.viewer_history.append(("scroll_to", str(position)))
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def scroll_to_line(self, line_number: int) -> ViewerResult:
        """
        Belirli bir satıra scroll et.
        
        Args:
            line_number: Satır numarası
            
        Returns:
            ViewerResult: Scroll sonucu
        """
        result = ViewerResult(success=False)
        result.action = "scroll_to_line"
        
        try:
            # Satır numarasını pozisyona çevir
            position = line_number * 20  # Tahmini satır yüksekliği
            self.state.scroll_position = max(0, position)
            
            result.success = True
            result.message = f"Scrolled to line {line_number}"
            
            self.viewer_history.append(("scroll_to_line", str(line_number)))
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def scroll_to_hunk(self, hunk_index: int) -> ViewerResult:
        """
        Belirli bir hunka scroll et.
        
        Args:
            hunk_index: Hunk indeksi
            
        Returns:
            ViewerResult: Scroll sonucu
        """
        result = ViewerResult(success=False)
        result.action = "scroll_to_hunk"
        
        try:
            if not self.files or self.state.current_file_index >= len(self.files):
                result.errors.append("No files loaded")
                return result
            
            current_file = self.files[self.state.current_file_index]
            
            if hunk_index < 0 or hunk_index >= len(current_file.hunks):
                result.errors.append(f"Invalid hunk index: {hunk_index}")
                return result
            
            self.state.current_hunk_index = hunk_index
            
            # Hunk başlangıç pozisyonunu hesapla
            hunk = current_file.hunks[hunk_index]
            position = hunk.old_start * 20
            self.state.scroll_position = max(0, position)
            
            result.success = True
            result.message = f"Scrolled to hunk {hunk_index}"
            
            self.viewer_history.append(("scroll_to_hunk", str(hunk_index)))
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def next_hunk(self) -> ViewerResult:
        """
        Sonraki hunka git.
        
        Returns:
            ViewerResult: Geçiş sonucu
        """
        result = ViewerResult(success=False)
        result.action = "next_hunk"
        
        try:
            if not self.files or self.state.current_file_index >= len(self.files):
                result.errors.append("No files loaded")
                return result
            
            current_file = self.files[self.state.current_file_index]
            next_index = self.state.current_hunk_index + 1
            
            if next_index < len(current_file.hunks):
                return self.scroll_to_hunk(next_index)
            else:
                result.errors.append("No more hunks")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def previous_hunk(self) -> ViewerResult:
        """
        Önceki hunka git.
        
        Returns:
            ViewerResult: Geçiş sonucu
        """
        result = ViewerResult(success=False)
        result.action = "previous_hunk"
        
        try:
            if not self.files or self.state.current_file_index >= len(self.files):
                result.errors.append("No files loaded")
                return result
            
            current_file = self.files[self.state.current_file_index]
            prev_index = self.state.current_hunk_index - 1
            
            if prev_index >= 0:
                return self.scroll_to_hunk(prev_index)
            else:
                result.errors.append("No previous hunk")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def next_file(self) -> ViewerResult:
        """
        Sonraki dosyaya git.
        
        Returns:
            ViewerResult: Geçiş sonucu
        """
        result = ViewerResult(success=False)
        result.action = "next_file"
        
        try:
            if not self.files:
                result.errors.append("No files loaded")
                return result
            
            next_index = self.state.current_file_index + 1
            
            if next_index < len(self.files):
                self.state.current_file_index = next_index
                self.state.current_hunk_index = 0
                self.state.scroll_position = 0
                
                result.success = True
                result.message = f"Switched to file {next_index}"
                
                self.viewer_history.append(("next_file", str(next_index)))
            else:
                result.errors.append("No more files")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def previous_file(self) -> ViewerResult:
        """
        Önceki dosyaya git.
        
        Returns:
            ViewerResult: Geçiş sonucu
        """
        result = ViewerResult(success=False)
        result.action = "previous_file"
        
        try:
            if not self.files:
                result.errors.append("No files loaded")
                return result
            
            prev_index = self.state.current_file_index - 1
            
            if prev_index >= 0:
                self.state.current_file_index = prev_index
                self.state.current_hunk_index = 0
                self.state.scroll_position = 0
                
                result.success = True
                result.message = f"Switched to file {prev_index}"
                
                self.viewer_history.append(("previous_file", str(prev_index)))
            else:
                result.errors.append("No previous file")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_current_file(self) -> Optional[DiffFile]:
        """
        Mevcut dosyayı al.
        
        Returns:
            Optional[DiffFile]: Dosya bilgisi
        """
        if self.files and self.state.current_file_index < len(self.files):
            return self.files[self.state.current_file_index]
        return None
    
    def get_current_hunk(self) -> Optional[DiffHunk]:
        """
        Mevcut hunka al.
        
        Returns:
            Optional[DiffHunk]: Hunk bilgisi
        """
        current_file = self.get_current_file()
        if current_file and self.state.current_hunk_index < len(current_file.hunks):
            return current_file.hunks[self.state.current_hunk_index]
        return None
    
    def get_scroll_position(self) -> int:
        """
        Scroll pozisyonunu al.
        
        Returns:
            int: Pozisyon
        """
        return self.state.scroll_position
    
    def get_zoom_factor(self) -> float:
        """
        Zoom faktörünü al.
        
        Returns:
            float: Faktör
        """
        return self.state.zoom_factor
    
    def get_viewer_history(self) -> List[Tuple[str, str]]:
        """
        Viewer geçmişini al.
        
        Returns:
            List[Tuple[str, str]]: Geçmiş
        """
        return self.viewer_history
    
    def clear_history(self) -> ViewerResult:
        """
        Geçmişi temizle.
        
        Returns:
            ViewerResult: Temizleme sonucu
        """
        result = ViewerResult(success=False)
        
        try:
            self.viewer_history.clear()
            result.success = True
            result.message = "Viewer history cleared"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        İstatistikleri al.
        
        Returns:
            Dict[str, Any]: İstatistikler
        """
        total_added = sum(f.added_lines for f in self.files)
        total_removed = sum(f.removed_lines for f in self.files)
        total_hunks = sum(len(f.hunks) for f in self.files)
        
        return {
            "total_files": len(self.files),
            "total_added": total_added,
            "total_removed": total_removed,
            "total_hunks": total_hunks,
            "current_file_index": self.state.current_file_index,
            "current_hunk_index": self.state.current_hunk_index,
            "scroll_position": self.state.scroll_position,
            "zoom_factor": self.state.zoom_factor
        }
    
    def update_config(self, config: ViewerConfig) -> ViewerResult:
        """
        Konfigürasyon güncelle.
        
        Args:
            config: Yeni konfigürasyon
            
        Returns:
            ViewerResult: Güncelleme sonucu
        """
        result = ViewerResult(success=False)
        
        try:
            self.config = config
            result.success = True
            result.message = "Config updated"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_config(self) -> ViewerConfig:
        """
        Konfigürasyon al.
        
        Returns:
            ViewerConfig: Konfigürasyon
        """
        return self.config
    
    def get_state(self) -> ViewerState:
        """
        Durumu al.
        
        Returns:
            ViewerState: Durum
        """
        return self.state
    
    def _create_diff(
        self,
        old_content: str,
        new_content: str,
        file_path: str
    ) -> DiffFile:
        """
        Diff oluştur.
        
        Args:
            old_content: Eski içerik
            new_content: Yeni içerik
            file_path: Dosya yolu
            
        Returns:
            DiffFile: Diff dosyası
        """
        old_lines = old_content.splitlines()
        new_lines = new_content.splitlines()
        
        diff_file = DiffFile(
            file_path=file_path,
            old_file=file_path,
            new_file=file_path
        )
        
        # Basit diff algoritması
        i = j = 0
        hunk = None
        context_lines = self.config.context_lines
        
        while i < len(old_lines) or j < len(new_lines):
            if i < len(old_lines) and j < len(new_lines):
                if old_lines[i] == new_lines[j]:
                    # Satır aynı
                    if hunk:
                        hunk.lines.append(DiffLine(
                            line_number=i + 1,
                            content=old_lines[i],
                            line_type="context",
                            old_line_number=i + 1,
                            new_line_number=j + 1
                        ))
                    i += 1
                    j += 1
                else:
                    # Satır farklı
                    if not hunk:
                        hunk = DiffHunk(
                            old_start=max(0, i - context_lines) + 1,
                            old_count=0,
                            new_start=max(0, j - context_lines) + 1,
                            new_count=0
                        )
                    
                    # Eski satırı ekle
                    hunk.lines.append(DiffLine(
                        line_number=i + 1,
                        content=old_lines[i],
                        line_type="removed",
                        old_line_number=i + 1
                    ))
                    diff_file.removed_lines += 1
                    hunk.old_count += 1
                    i += 1
                    
                    # Yeni satırı ekle
                    if j < len(new_lines):
                        hunk.lines.append(DiffLine(
                            line_number=j + 1,
                            content=new_lines[j],
                            line_type="added",
                            new_line_number=j + 1
                        ))
                        diff_file.added_lines += 1
                        hunk.new_count += 1
                        j += 1
            elif i < len(old_lines):
                # Sadece eski satırlar kaldı
                if not hunk:
                    hunk = DiffHunk(
                        old_start=i + 1,
                        old_count=0,
                        new_start=j + 1,
                        new_count=0
                    )
                
                hunk.lines.append(DiffLine(
                    line_number=i + 1,
                    content=old_lines[i],
                    line_type="removed",
                    old_line_number=i + 1
                ))
                diff_file.removed_lines += 1
                hunk.old_count += 1
                i += 1
            elif j < len(new_lines):
                # Sadece yeni satırlar kaldı
                if not hunk:
                    hunk = DiffHunk(
                        old_start=i + 1,
                        old_count=0,
                        new_start=j + 1,
                        new_count=0
                    )
                
                hunk.lines.append(DiffLine(
                    line_number=j + 1,
                    content=new_lines[j],
                    line_type="added",
                    new_line_number=j + 1
                ))
                diff_file.added_lines += 1
                hunk.new_count += 1
                j += 1
            
            # Hunk'u kapat
            if hunk and (i >= len(old_lines) or j >= len(new_lines) or 
                         (i < len(old_lines) and j < len(new_lines) and 
                          old_lines[i] == new_lines[j])):
                diff_file.hunks.append(hunk)
                hunk = None
        
        return diff_file


if __name__ == "__main__":
    # Basit test
    engine = DiffViewerEngine()
    
    old_content = "Line 1\nLine 2\nLine 3"
    new_content = "Line 1\nLine 2 modified\nLine 3\nLine 4"
    
    result = engine.load_diff(old_content, new_content, "test.txt")
    print(f"Load diff: {result.success}")
    print(f"Total added: {result.total_added}")
    print(f"Total removed: {result.total_removed}")
