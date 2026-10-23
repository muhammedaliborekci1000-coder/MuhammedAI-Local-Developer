"""
MuhammedAI Local Developer - Diff Navigator
Diff navigator engine for code editor.
"""

from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from enum import Enum


class NavigationMode(Enum):
    """Navigation mode."""
    HUNK = "hunk"
    LINE = "line"
    FILE = "file"
    CHANGE = "change"
    CONFLICT = "conflict"


class NavigationDirection(Enum):
    """Navigation direction."""
    NEXT = "next"
    PREVIOUS = "previous"
    FIRST = "first"
    LAST = "last"


class NavigationScope(Enum):
    """Navigation scope."""
    CURRENT_FILE = "current_file"
    ALL_FILES = "all_files"
    VISIBLE = "visible"
    SELECTED = "selected"


class NavigationAction(Enum):
    """Navigation action."""
    NAVIGATE = "navigate"
    JUMP = "jump"
    GOTO = "goto"
    SEARCH = "search"
    BOOKMARK = "bookmark"
    MARK = "mark"


@dataclass
class NavigationPosition:
    """Navigation position."""
    file_index: int
    line_number: int
    hunk_index: int
    character_index: int = 0


@dataclass
class Bookmark:
    """Bookmark."""
    name: str
    position: NavigationPosition
    description: str = ""
    created_at: Optional[str] = None


@dataclass
class NavigationMark:
    """Navigation mark."""
    position: NavigationPosition
    mark_type: str = "change"
    description: str = ""


@dataclass
class NavigatorConfig:
    """Navigator configuration."""
    wrap_around: bool = True
    skip_unchanged: bool = True
    highlight_current: bool = True
    show_line_numbers: bool = True
    auto_scroll: bool = True
    smooth_scroll: bool = True
    scroll_duration: int = 200
    max_history: int = 100


@dataclass
class NavigatorResult:
    """Navigator result."""
    success: bool
    action: Optional[str] = None
    message: Optional[str] = None
    errors: List[str] = field(default_factory=list)
    position: Optional[NavigationPosition] = None
    total_hunks: int = 0
    total_changes: int = 0


class DiffNavigatorEngine:
    """
    Diff navigator engine.
    
    Özellikler:
    - Hunk navigation
    - Line navigation
    - File navigation
    - Jump to change
    - Next/previous hunk
    - Next/previous change
    - Next/previous file
    - First/last navigation
    - Bookmark management
    - Mark management
    - Position tracking
    - Navigation history
    - Search navigation
    - Wrap-around support
    - Skip unchanged support
    - Highlight current position
    - Auto-scroll support
    - Smooth scroll support
    - Configuration management
    - Statistics tracking
    """
    
    def __init__(self, config: Optional[NavigatorConfig] = None):
        """Initialize diff navigator engine."""
        self.config = config or NavigatorConfig()
        self.current_position = NavigationPosition(file_index=0, line_number=0, hunk_index=0)
        self.bookmarks: Dict[str, Bookmark] = {}
        self.marks: List[NavigationMark] = []
        self.navigation_history: List[Tuple[str, NavigationPosition]] = []  # (action, position)
        self.hunks: List[Tuple[int, int]] = []  # (start_line, end_line)
        self.changes: List[int] = []  # line numbers with changes
        self.files: List[str] = []
    
    def navigate_to_hunk(
        self,
        hunk_index: int,
        direction: NavigationDirection = NavigationDirection.NEXT
    ) -> NavigatorResult:
        """
        Hunk'a git.
        
        Args:
            hunk_index: Hunk indeksi
            direction: Yön
            
        Returns:
            NavigatorResult: Navigasyon sonucu
        """
        result = NavigatorResult(success=False)
        result.action = NavigationAction.NAVIGATE.value
        
        try:
            if not self.hunks:
                result.errors.append("No hunks available")
                return result
            
            if direction == NavigationDirection.NEXT:
                target_index = min(hunk_index + 1, len(self.hunks) - 1)
            elif direction == NavigationDirection.PREVIOUS:
                target_index = max(hunk_index - 1, 0)
            elif direction == NavigationDirection.FIRST:
                target_index = 0
            elif direction == NavigationDirection.LAST:
                target_index = len(self.hunks) - 1
            else:
                target_index = hunk_index
            
            if target_index < 0 or target_index >= len(self.hunks):
                if self.config.wrap_around:
                    target_index = target_index % len(self.hunks)
                else:
                    result.errors.append("Hunk index out of range")
                    return result
            
            hunk = self.hunks[target_index]
            self.current_position.hunk_index = target_index
            self.current_position.line_number = hunk[0]
            
            result.position = self.current_position
            result.total_hunks = len(self.hunks)
            result.success = True
            result.message = f"Navigated to hunk {target_index}"
            
            self._add_to_history("navigate_hunk", self.current_position)
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def navigate_to_line(
        self,
        line_number: int,
        direction: NavigationDirection = NavigationDirection.NEXT
    ) -> NavigatorResult:
        """
        Satıra git.
        
        Args:
            line_number: Satır numarası
            direction: Yön
            
        Returns:
            NavigatorResult: Navigasyon sonucu
        """
        result = NavigatorResult(success=False)
        result.action = NavigationAction.NAVIGATE.value
        
        try:
            self.current_position.line_number = line_number
            
            # Hunk indeksini güncelle
            for i, (start, end) in enumerate(self.hunks):
                if start <= line_number <= end:
                    self.current_position.hunk_index = i
                    break
            
            result.position = self.current_position
            result.success = True
            result.message = f"Navigated to line {line_number}"
            
            self._add_to_history("navigate_line", self.current_position)
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def navigate_to_file(
        self,
        file_index: int,
        direction: NavigationDirection = NavigationDirection.NEXT
    ) -> NavigatorResult:
        """
        Dosyaya git.
        
        Args:
            file_index: Dosya indeksi
            direction: Yön
            
        Returns:
            NavigatorResult: Navigasyon sonucu
        """
        result = NavigatorResult(success=False)
        result.action = NavigationAction.NAVIGATE.value
        
        try:
            if not self.files:
                result.errors.append("No files available")
                return result
            
            if direction == NavigationDirection.NEXT:
                target_index = min(file_index + 1, len(self.files) - 1) if file_index >= 0 else 0
            elif direction == NavigationDirection.PREVIOUS:
                target_index = max(file_index - 1, 0)
            elif direction == NavigationDirection.FIRST:
                target_index = 0
            elif direction == NavigationDirection.LAST:
                target_index = len(self.files) - 1
            else:
                target_index = file_index
            
            if target_index < 0 or target_index >= len(self.files):
                if self.config.wrap_around:
                    target_index = target_index % len(self.files)
                else:
                    result.errors.append("File index out of range")
                    return result
            
            self.current_position.file_index = target_index
            self.current_position.line_number = 0
            self.current_position.hunk_index = 0
            
            result.position = self.current_position
            result.success = True
            result.message = f"Navigated to file {target_index}"
            
            self._add_to_history("navigate_file", self.current_position)
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def jump_to_change(
        self,
        direction: NavigationDirection = NavigationDirection.NEXT
    ) -> NavigatorResult:
        """
        Değişikliğe atla.
        
        Args:
            direction: Yön
            
        Returns:
            NavigatorResult: Atlama sonucu
        """
        result = NavigatorResult(success=False)
        result.action = NavigationAction.JUMP.value
        
        try:
            if not self.changes:
                result.errors.append("No changes available")
                return result
            
            current_line = self.current_position.line_number
            
            if direction == NavigationDirection.NEXT:
                # Bir sonraki değişikliği bul
                target_line = None
                for change in self.changes:
                    if change > current_line:
                        target_line = change
                        break
                if target_line is None and self.config.wrap_around:
                    target_line = self.changes[0]
            elif direction == NavigationDirection.PREVIOUS:
                # Bir önceki değişikliği bul
                target_line = None
                for change in reversed(self.changes):
                    if change < current_line:
                        target_line = change
                        break
                if target_line is None and self.config.wrap_around:
                    target_line = self.changes[-1]
            elif direction == NavigationDirection.FIRST:
                target_line = self.changes[0]
            elif direction == NavigationDirection.LAST:
                target_line = self.changes[-1]
            else:
                result.errors.append("Invalid direction")
                return result
            
            if target_line is not None:
                line_result = self.navigate_to_line(target_line)
                if line_result.success:
                    result.position = line_result.position
                    result.success = True
                    result.message = f"Jumped to change at line {target_line}"
                return result
            else:
                result.errors.append("No change found")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def next_hunk(self) -> NavigatorResult:
        """
        Sonraki hunka git.
        
        Returns:
            NavigatorResult: Geçiş sonucu
        """
        return self.navigate_to_hunk(self.current_position.hunk_index, NavigationDirection.NEXT)
    
    def previous_hunk(self) -> NavigatorResult:
        """
        Önceki hunka git.
        
        Returns:
            NavigatorResult: Geçiş sonucu
        """
        return self.navigate_to_hunk(self.current_position.hunk_index, NavigationDirection.PREVIOUS)
    
    def first_hunk(self) -> NavigatorResult:
        """
        İlk hunka git.
        
        Returns:
            NavigatorResult: Geçiş sonucu
        """
        return self.navigate_to_hunk(0, NavigationDirection.FIRST)
    
    def last_hunk(self) -> NavigatorResult:
        """
        Son hunka git.
        
        Returns:
            NavigatorResult: Geçiş sonucu
        """
        return self.navigate_to_hunk(len(self.hunks) - 1, NavigationDirection.LAST)
    
    def next_change(self) -> NavigatorResult:
        """
        Sonraki değişikliğe git.
        
        Returns:
            NavigatorResult: Geçiş sonucu
        """
        return self.jump_to_change(NavigationDirection.NEXT)
    
    def previous_change(self) -> NavigatorResult:
        """
        Önceki değişikliğe git.
        
        Returns:
            NavigatorResult: Geçiş sonucu
        """
        return self.jump_to_change(NavigationDirection.PREVIOUS)
    
    def next_file(self) -> NavigatorResult:
        """
        Sonraki dosyaya git.
        
        Returns:
            NavigatorResult: Geçiş sonucu
        """
        return self.navigate_to_file(self.current_position.file_index, NavigationDirection.NEXT)
    
    def previous_file(self) -> NavigatorResult:
        """
        Önceki dosyaya git.
        
        Returns:
            NavigatorResult: Geçiş sonucu
        """
        return self.navigate_to_file(self.current_position.file_index, NavigationDirection.PREVIOUS)
    
    def add_bookmark(
        self,
        name: str,
        description: str = ""
    ) -> NavigatorResult:
        """
        Bookmark ekle.
        
        Args:
            name: Bookmark adı
            description: Açıklama
            
        Returns:
            NavigatorResult: Ekleme sonucu
        """
        result = NavigatorResult(success=False)
        result.action = NavigationAction.BOOKMARK.value
        
        try:
            bookmark = Bookmark(
                name=name,
                position=NavigationPosition(
                    file_index=self.current_position.file_index,
                    line_number=self.current_position.line_number,
                    hunk_index=self.current_position.hunk_index
                ),
                description=description
            )
            
            self.bookmarks[name] = bookmark
            
            result.success = True
            result.message = f"Added bookmark: {name}"
            
            self._add_to_history("add_bookmark", self.current_position)
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def remove_bookmark(self, name: str) -> NavigatorResult:
        """
        Bookmark sil.
        
        Args:
            name: Bookmark adı
            
        Returns:
            NavigatorResult: Silme sonucu
        """
        result = NavigatorResult(success=False)
        result.action = NavigationAction.BOOKMARK.value
        
        try:
            if name in self.bookmarks:
                del self.bookmarks[name]
                result.success = True
                result.message = f"Removed bookmark: {name}"
            else:
                result.errors.append(f"Bookmark not found: {name}")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def goto_bookmark(self, name: str) -> NavigatorResult:
        """
        Bookmark'a git.
        
        Args:
            name: Bookmark adı
            
        Returns:
            NavigatorResult: Gitme sonucu
        """
        result = NavigatorResult(success=False)
        result.action = NavigationAction.GOTO.value
        
        try:
            if name not in self.bookmarks:
                result.errors.append(f"Bookmark not found: {name}")
                return result
            
            bookmark = self.bookmarks[name]
            self.current_position = bookmark.position
            
            result.position = self.current_position
            result.success = True
            result.message = f"Jumped to bookmark: {name}"
            
            self._add_to_history("goto_bookmark", self.current_position)
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def add_mark(
        self,
        mark_type: str = "change",
        description: str = ""
    ) -> NavigatorResult:
        """
        Mark ekle.
        
        Args:
            mark_type: Mark tipi
            description: Açıklama
            
        Returns:
            NavigatorResult: Ekleme sonucu
        """
        result = NavigatorResult(success=False)
        result.action = NavigationAction.MARK.value
        
        try:
            mark = NavigationMark(
                position=NavigationPosition(
                    file_index=self.current_position.file_index,
                    line_number=self.current_position.line_number,
                    hunk_index=self.current_position.hunk_index
                ),
                mark_type=mark_type,
                description=description
            )
            
            self.marks.append(mark)
            
            result.success = True
            result.message = f"Added mark: {mark_type}"
            
            self._add_to_history("add_mark", self.current_position)
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_current_position(self) -> NavigationPosition:
        """
        Mevcut pozisyonu al.
        
        Returns:
            NavigationPosition: Pozisyon
        """
        return self.current_position
    
    def get_bookmarks(self) -> Dict[str, Bookmark]:
        """
        Bookmarkları al.
        
        Returns:
            Dict[str, Bookmark]: Bookmark sözlüğü
        """
        return self.bookmarks
    
    def get_marks(self) -> List[NavigationMark]:
        """
        Markları al.
        
        Returns:
            List[NavigationMark]: Mark listesi
        """
        return self.marks
    
    def get_navigation_history(self) -> List[Tuple[str, NavigationPosition]]:
        """
        Navigasyon geçmişini al.
        
        Returns:
            List[Tuple[str, NavigationPosition]]: Geçmiş
        """
        return self.navigation_history
    
    def clear_history(self) -> NavigatorResult:
        """
        Geçmişi temizle.
        
        Returns:
            NavigatorResult: Temizleme sonucu
        """
        result = NavigatorResult(success=False)
        
        try:
            self.navigation_history.clear()
            result.success = True
            result.message = "Navigation history cleared"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def set_hunks(self, hunks: List[Tuple[int, int]]):
        """
        Hunks ayarla.
        
        Args:
            hunks: Hunk listesi
        """
        self.hunks = hunks
    
    def set_changes(self, changes: List[int]):
        """
        Değişiklikleri ayarla.
        
        Args:
            changes: Değişiklik listesi
        """
        self.changes = changes
    
    def set_files(self, files: List[str]):
        """
        Dosyaları ayarla.
        
        Args:
            files: Dosya listesi
        """
        self.files = files
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        İstatistikleri al.
        
        Returns:
            Dict[str, Any]: İstatistikler
        """
        return {
            "total_hunks": len(self.hunks),
            "total_changes": len(self.changes),
            "total_files": len(self.files),
            "total_bookmarks": len(self.bookmarks),
            "total_marks": len(self.marks),
            "current_file_index": self.current_position.file_index,
            "current_line_number": self.current_position.line_number,
            "current_hunk_index": self.current_position.hunk_index
        }
    
    def update_config(self, config: NavigatorConfig) -> NavigatorResult:
        """
        Konfigürasyon güncelle.
        
        Args:
            config: Yeni konfigürasyon
            
        Returns:
            NavigatorResult: Güncelleme sonucu
        """
        result = NavigatorResult(success=False)
        
        try:
            self.config = config
            result.success = True
            result.message = "Config updated"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_config(self) -> NavigatorConfig:
        """
        Konfigürasyon al.
        
        Returns:
            NavigatorConfig: Konfigürasyon
        """
        return self.config
    
    def _add_to_history(self, action: str, position: NavigationPosition):
        """Geçmişe ekle."""
        self.navigation_history.append((action, position))
        
        # Geçmiş sınırla
        if len(self.navigation_history) > self.config.max_history:
            self.navigation_history.pop(0)


if __name__ == "__main__":
    # Basit test
    engine = DiffNavigatorEngine()
    
    engine.set_hunks([(1, 10), (20, 30)])
    engine.set_changes([5, 15, 25])
    engine.set_files(["file1.txt", "file2.txt"])
    
    result = engine.next_hunk()
    print(f"Next hunk: {result.success}")
    print(f"Position: {result.position}")
