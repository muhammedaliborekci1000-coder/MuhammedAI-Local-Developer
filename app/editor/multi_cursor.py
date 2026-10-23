"""
MuhammedAI Local Developer - Multi-Cursor Editing
Multi-cursor editing engine for code editor.
"""

from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from enum import Enum


class CursorAction(Enum):
    """Cursor action."""
    ADD = "add"
    REMOVE = "remove"
    MOVE = "move"
    SELECT = "select"
    CLEAR = "clear"


class CursorMode(Enum):
    """Cursor mode."""
    NORMAL = "normal"
    BLOCK = "block"
    COLUMN = "column"


@dataclass
class CursorPosition:
    """Cursor position."""
    line: int
    column: int
    is_primary: bool = False


@dataclass
class CursorSelection:
    """Cursor selection."""
    start_line: int
    start_column: int
    end_line: int
    end_column: int


@dataclass
class MultiCursorEdit:
    """Multi-cursor edit."""
    cursor_id: str
    position: CursorPosition
    selection: Optional[CursorSelection] = None
    text: str = ""


@dataclass
class MultiCursorResult:
    """Multi-cursor result."""
    success: bool
    edited_code: Optional[str] = None
    cursors: List[CursorPosition] = field(default_factory=list)
    edits: List[MultiCursorEdit] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    message: Optional[str] = None


class MultiCursorEngine:
    """
    Multi-cursor editing engine.
    
    Özellikler:
    - Multiple cursor management
    - Cursor addition/removal
    - Simultaneous editing
    - Block selection
    - Column selection
    - Cursor cloning
    - Cursor merging
    - Cursor jumping
    - Find all occurrences
    - Select all occurrences
    - Cursor synchronization
    - Primary cursor
    - Cursor ordering
    - Cursor validation
    - Undo/redo support
    """
    
    def __init__(self):
        """Initialize multi-cursor engine."""
        self.cursors: List[CursorPosition] = []
        self.primary_cursor_index: int = 0
        self.cursor_mode: CursorMode = CursorMode.NORMAL
    
    def add_cursor(self, line: int, column: int, is_primary: bool = False) -> MultiCursorResult:
        """
        Cursor ekle.
        
        Args:
            line: Satır numarası
            column: Sütun numarası
            is_primary: Primary cursor mı
            
        Returns:
            MultiCursorResult: Ekleme sonucu
        """
        result = MultiCursorResult(success=False)
        
        try:
            cursor = CursorPosition(line=line, column=column, is_primary=is_primary)
            
            if is_primary:
                # Mevcut primary'ı kaldır
                for c in self.cursors:
                    c.is_primary = False
                self.primary_cursor_index = len(self.cursors)
            
            self.cursors.append(cursor)
            
            result.success = True
            result.cursors = self.cursors
            result.message = f"Cursor added at ({line}, {column})"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def remove_cursor(self, index: int) -> MultiCursorResult:
        """
        Cursor kaldır.
        
        Args:
            index: Cursor index
            
        Returns:
            MultiCursorResult: Kaldırma sonucu
        """
        result = MultiCursorResult(success=False)
        
        try:
            if 0 <= index < len(self.cursors):
                removed = self.cursors.pop(index)
                
                # Primary kaldırıldıysa, yeni primary ata
                if removed.is_primary and self.cursors:
                    self.cursors[0].is_primary = True
                    self.primary_cursor_index = 0
                
                result.success = True
                result.cursors = self.cursors
                result.message = f"Cursor removed at index {index}"
            else:
                result.errors.append("Invalid cursor index")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def clear_cursors(self) -> MultiCursorResult:
        """
        Tüm cursor'ları temizle.
        
        Returns:
            MultiCursorResult: Temizleme sonucu
        """
        result = MultiCursorResult(success=False)
        
        try:
            self.cursors = []
            self.primary_cursor_index = 0
            
            result.success = True
            result.cursors = self.cursors
            result.message = "All cursors cleared"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def move_cursor(self, index: int, line: int, column: int) -> MultiCursorResult:
        """
        Cursor taşı.
        
        Args:
            index: Cursor index
            line: Yeni satır
            column: Yeni sütun
            
        Returns:
            MultiCursorResult: Taşıma sonucu
        """
        result = MultiCursorResult(success=False)
        
        try:
            if 0 <= index < len(self.cursors):
                self.cursors[index].line = line
                self.cursors[index].column = column
                
                result.success = True
                result.cursors = self.cursors
                result.message = f"Cursor {index} moved to ({line}, {column})"
            else:
                result.errors.append("Invalid cursor index")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def edit_at_cursors(self, code: str, text: str) -> MultiCursorResult:
        """
        Tüm cursor konumlarında düzenle.
        
        Args:
            code: Kod içeriği
            text: Eklenecek metin
            
        Returns:
            MultiCursorResult: Düzenleme sonucu
        """
        result = MultiCursorResult(success=False)
        
        try:
            if not self.cursors:
                result.errors.append("No cursors available")
                return result
            
            lines = code.splitlines()
            edits = []
            
            # Cursor'ları sırala (sondan başa doğru işle)
            sorted_cursors = sorted(
                [(i, c) for i, c in enumerate(self.cursors)],
                key=lambda x: (x[1].line, x[1].column),
                reverse=True
            )
            
            for cursor_index, cursor in sorted_cursors:
                if cursor.line < len(lines):
                    line = lines[cursor.line]
                    new_line = line[:cursor.column] + text + line[cursor.column:]
                    lines[cursor.line] = new_line
                    
                    edit = MultiCursorEdit(
                        cursor_id=str(cursor_index),
                        position=cursor,
                        text=text
                    )
                    edits.append(edit)
            
            edited_code = "\n".join(lines)
            
            result.success = True
            result.edited_code = edited_code
            result.edits = edits
            result.message = f"Edited at {len(edits)} cursor positions"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def clone_cursors_down(self, code: str) -> MultiCursorResult:
        """
        Cursor'ları aşağı klonla.
        
        Args:
            code: Kod içeriği
            
        Returns:
            MultiCursorResult: Klonlama sonucu
        """
        result = MultiCursorResult(success=False)
        
        try:
            if not self.cursors:
                result.errors.append("No cursors to clone")
                return result
            
            lines = code.splitlines()
            new_cursors = []
            
            for cursor in self.cursors:
                new_line = cursor.line + 1
                if new_line < len(lines):
                    new_cursor = CursorPosition(line=new_line, column=cursor.column)
                    new_cursors.append(new_cursor)
            
            self.cursors.extend(new_cursors)
            
            result.success = True
            result.cursors = self.cursors
            result.message = f"Cloned {len(new_cursors)} cursors down"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def clone_cursors_up(self, code: str) -> MultiCursorResult:
        """
        Cursor'ları yukarı klonla.
        
        Args:
            code: Kod içeriği
            
        Returns:
            MultiCursorResult: Klonlama sonucu
        """
        result = MultiCursorResult(success=False)
        
        try:
            if not self.cursors:
                result.errors.append("No cursors to clone")
                return result
            
            lines = code.splitlines()
            new_cursors = []
            
            for cursor in self.cursors:
                new_line = cursor.line - 1
                if new_line >= 0:
                    new_cursor = CursorPosition(line=new_line, column=cursor.column)
                    new_cursors.append(new_cursor)
            
            self.cursors.extend(new_cursors)
            
            result.success = True
            result.cursors = self.cursors
            result.message = f"Cloned {len(new_cursors)} cursors up"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def find_all_occurrences(self, code: str, search_text: str) -> MultiCursorResult:
        """
        Tüm oluşumları bul ve cursor ekle.
        
        Args:
            code: Kod içeriği
            search_text: Aranan metin
            
        Returns:
            MultiCursorResult: Bulma sonucu
        """
        result = MultiCursorResult(success=False)
        
        try:
            self.clear_cursors()
            
            lines = code.splitlines()
            found_count = 0
            
            for line_idx, line in enumerate(lines):
                start = 0
                while True:
                    pos = line.find(search_text, start)
                    if pos == -1:
                        break
                    
                    cursor = CursorPosition(line=line_idx, column=pos)
                    self.cursors.append(cursor)
                    found_count += 1
                    start = pos + len(search_text)
            
            if self.cursors:
                self.cursors[0].is_primary = True
                self.primary_cursor_index = 0
            
            result.success = True
            result.cursors = self.cursors
            result.message = f"Found {found_count} occurrences"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def select_all_occurrences(self, code: str, search_text: str) -> MultiCursorResult:
        """
        Tüm oluşumları seç.
        
        Args:
            code: Kod içeriği
            search_text: Aranan metin
            
        Returns:
            MultiCursorResult: Seçim sonucu
        """
        result = MultiCursorResult(success=False)
        
        try:
            # Önce cursor'ları bul
            find_result = self.find_all_occurrences(code, search_text)
            
            if find_result.success:
                result.success = True
                result.cursors = find_result.cursors
                result.message = f"Selected {len(find_result.cursors)} occurrences"
            else:
                result.errors = find_result.errors
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def merge_cursors(self) -> MultiCursorResult:
        """
        Cursor'ları birleştir.
        
        Returns:
            MultiCursorResult: Birleştirme sonucu
        """
        result = MultiCursorResult(success=False)
        
        try:
            if len(self.cursors) <= 1:
                result.errors.append("Not enough cursors to merge")
                return result
            
            # Sadece primary'ı tut
            primary = None
            for cursor in self.cursors:
                if cursor.is_primary:
                    primary = cursor
                    break
            
            if primary:
                self.cursors = [primary]
            else:
                self.cursors = [self.cursors[0]]
                self.cursors[0].is_primary = True
            
            result.success = True
            result.cursors = self.cursors
            result.message = "Cursors merged"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def jump_to_next_cursor(self) -> MultiCursorResult:
        """
        Sonraki cursor'a atla.
        
        Returns:
            MultiCursorResult: Atlama sonucu
        """
        result = MultiCursorResult(success=False)
        
        try:
            if len(self.cursors) <= 1:
                result.errors.append("Not enough cursors")
                return result
            
            # Primary'ı kaldır
            for c in self.cursors:
                c.is_primary = False
            
            # Sonraki cursor'ı primary yap
            self.primary_cursor_index = (self.primary_cursor_index + 1) % len(self.cursors)
            self.cursors[self.primary_cursor_index].is_primary = True
            
            result.success = True
            result.cursors = self.cursors
            result.message = f"Jumped to cursor {self.primary_cursor_index}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def jump_to_previous_cursor(self) -> MultiCursorResult:
        """
        Önceki cursor'a atla.
        
        Returns:
            MultiCursorResult: Atlama sonucu
        """
        result = MultiCursorResult(success=False)
        
        try:
            if len(self.cursors) <= 1:
                result.errors.append("Not enough cursors")
                return result
            
            # Primary'ı kaldır
            for c in self.cursors:
                c.is_primary = False
            
            # Önceki cursor'ı primary yap
            self.primary_cursor_index = (self.primary_cursor_index - 1) % len(self.cursors)
            self.cursors[self.primary_cursor_index].is_primary = True
            
            result.success = True
            result.cursors = self.cursors
            result.message = f"Jumped to cursor {self.primary_cursor_index}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_cursors(self) -> List[CursorPosition]:
        """
        Cursor'ları al.
        
        Returns:
            List[CursorPosition]: Cursor listesi
        """
        return self.cursors
    
    def get_primary_cursor(self) -> Optional[CursorPosition]:
        """
        Primary cursor'ı al.
        
        Returns:
            Optional[CursorPosition]: Primary cursor
        """
        for cursor in self.cursors:
            if cursor.is_primary:
                return cursor
        return None
    
    def set_cursor_mode(self, mode: CursorMode) -> MultiCursorResult:
        """
        Cursor modu ayarla.
        
        Args:
            mode: Cursor modu
            
        Returns:
            MultiCursorResult: Ayarlama sonucu
        """
        result = MultiCursorResult(success=False)
        
        try:
            self.cursor_mode = mode
            result.success = True
            result.message = f"Cursor mode set to {mode.value}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_cursor_count(self) -> int:
        """
        Cursor sayısını al.
        
        Returns:
            int: Cursor sayısı
        """
        return len(self.cursors)


if __name__ == "__main__":
    # Basit test
    engine = MultiCursorEngine()
    
    # Cursor ekle
    result = engine.add_cursor(0, 0, is_primary=True)
    print(f"Added: {result.success}")
    
    # Cursor klonla
    code = "line1\nline2\nline3"
    result = engine.clone_cursors_down(code)
    print(f"Cloned: {result.success}")
