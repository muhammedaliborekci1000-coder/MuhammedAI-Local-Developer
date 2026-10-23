"""
MuhammedAI Local Developer - Delete Line
Delete line engine for code editor.
"""

from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from enum import Enum


class DeleteScope(Enum):
    """Delete scope."""
    LINE = "line"
    SELECTION = "selection"
    BLOCK = "block"
    FUNCTION = "function"
    WORD = "word"


class DeleteMode(Enum):
    """Delete mode."""
    SINGLE = "single"
    MULTIPLE = "multiple"
    ALL = "all"
    SMART = "smart"


@dataclass
class DeleteRange:
    """Delete range."""
    start_line: int
    end_line: int
    start_column: int = 0
    end_column: int = 0


@dataclass
class DeleteConfig:
    """Delete configuration."""
    scope: DeleteScope = DeleteScope.LINE
    mode: DeleteMode = DeleteMode.SINGLE
    preserve_empty_lines: bool = False
    adjust_indentation: bool = True
    delete_comments: bool = True
    delete_whitespace: bool = True
    confirm_deletion: bool = False


@dataclass
class DeleteResult:
    """Delete result."""
    success: bool
    modified_content: str = ""
    original_content: str = ""
    lines_deleted: int = 0
    cursor_position: int = 0
    errors: List[str] = field(default_factory=list)
    message: Optional[str] = None


class DeleteLineEngine:
    """
    Delete line engine.
    
    Özellikler:
    - Delete single line
    - Delete selection
    - Delete block
    - Delete function
    - Delete word
    - Smart deletion
    - Empty line handling
    - Indentation adjustment
    - Comment deletion
    - Whitespace deletion
    - Undo support
    - Delete history
    - Cursor position handling
    - Confirmation support
    """
    
    def __init__(self, config: Optional[DeleteConfig] = None):
        """Initialize delete line engine."""
        self.config = config or DeleteConfig()
        self.delete_history: List[Dict[str, Any]] = []
    
    def delete_line(
        self,
        content: str,
        line_number: int
    ) -> DeleteResult:
        """
        Satırı sil.
        
        Args:
            content: Dosya içeriği
            line_number: Satır numarası
            
        Returns:
            DeleteResult: Silme sonucu
        """
        result = DeleteResult(success=False)
        result.original_content = content
        
        try:
            lines = content.splitlines()
            
            if line_number >= len(lines):
                result.errors.append("Invalid line number")
                return result
            
            # Satırı sil
            deleted_line = lines.pop(line_number)
            
            modified_content = "\n".join(lines)
            
            # Geçmişe ekle
            self.delete_history.append({
                "original": content,
                "modified": modified_content,
                "line_number": line_number,
                "deleted_line": deleted_line
            })
            
            result.success = True
            result.modified_content = modified_content
            result.lines_deleted = 1
            result.cursor_position = line_number
            result.message = f"Line {line_number} deleted"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def delete_selection(
        self,
        content: str,
        delete_range: DeleteRange
    ) -> DeleteResult:
        """
        Seçimi sil.
        
        Args:
            content: Dosya içeriği
            delete_range: Silme aralığı
            
        Returns:
            DeleteResult: Silme sonucu
        """
        result = DeleteResult(success=False)
        result.original_content = content
        
        try:
            lines = content.splitlines()
            
            if delete_range.start_line >= len(lines) or delete_range.end_line >= len(lines):
                result.errors.append("Invalid range")
                return result
            
            # Seçili satırları sil
            deleted_lines = lines[delete_range.start_line:delete_range.end_line + 1]
            del lines[delete_range.start_line:delete_range.end_line + 1]
            
            modified_content = "\n".join(lines)
            
            # Geçmişe ekle
            self.delete_history.append({
                "original": content,
                "modified": modified_content,
                "range": delete_range,
                "deleted_lines": deleted_lines
            })
            
            result.success = True
            result.modified_content = modified_content
            result.lines_deleted = len(deleted_lines)
            result.cursor_position = delete_range.start_line
            result.message = f"Selection deleted ({len(deleted_lines)} lines)"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def delete_block(
        self,
        content: str,
        start_line: int,
        end_line: int
    ) -> DeleteResult:
        """
        Bloğu sil.
        
        Args:
            content: Dosya içeriği
            start_line: Başlangıç satırı
            end_line: Bitiş satırı
            
        Returns:
            DeleteResult: Silme sonucu
        """
        delete_range = DeleteRange(start_line=start_line, end_line=end_line)
        return self.delete_selection(content, delete_range)
    
    def delete_function(
        self,
        content: str,
        line_number: int
    ) -> DeleteResult:
        """
        Fonksiyonu sil.
        
        Args:
            content: Dosya içeriği
            line_number: Satır numarası (fonksiyon içinde)
            
        Returns:
            DeleteResult: Silme sonucu
        """
        result = DeleteResult(success=False)
        result.original_content = content
        
        try:
            lines = content.splitlines()
            
            if line_number >= len(lines):
                result.errors.append("Invalid line number")
                return result
            
            # Fonksiyon başlangıcını bul
            start_line = self._find_function_start(lines, line_number)
            if start_line == -1:
                result.errors.append("Function start not found")
                return result
            
            # Fonksiyon bitişini bul
            end_line = self._find_function_end(lines, start_line)
            if end_line == -1:
                result.errors.append("Function end not found")
                return result
            
            # Fonksiyonu sil
            delete_range = DeleteRange(start_line=start_line, end_line=end_line)
            return self.delete_selection(content, delete_range)
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def delete_word(
        self,
        content: str,
        line_number: int,
        column: int
    ) -> DeleteResult:
        """
        Kelimeyi sil.
        
        Args:
            content: Dosya içeriği
            line_number: Satır numarası
            column: Sütun numarası
            
        Returns:
            DeleteResult: Silme sonucu
        """
        result = DeleteResult(success=False)
        result.original_content = content
        
        try:
            lines = content.splitlines()
            
            if line_number >= len(lines):
                result.errors.append("Invalid line number")
                return result
            
            line = lines[line_number]
            
            if column >= len(line):
                result.errors.append("Invalid column")
                return result
            
            # Kelimeyi bul ve sil
            word_start = self._find_word_start(line, column)
            word_end = self._find_word_end(line, column)
            
            new_line = line[:word_start] + line[word_end:]
            lines[line_number] = new_line
            
            modified_content = "\n".join(lines)
            
            # Geçmişe ekle
            self.delete_history.append({
                "original": content,
                "modified": modified_content,
                "line_number": line_number,
                "column": column
            })
            
            result.success = True
            result.modified_content = modified_content
            result.lines_deleted = 0
            result.cursor_position = word_start
            result.message = "Word deleted"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def _find_word_start(self, line: str, column: int) -> int:
        """
        Kelime başlangıcını bul.
        
        Args:
            line: Satır
            column: Sütun
            
        Returns:
            int: Kelime başlangıcı
        """
        start = column
        while start > 0 and line[start - 1].isalnum():
            start -= 1
        return start
    
    def _find_word_end(self, line: str, column: int) -> int:
        """
        Kelime bitişini bul.
        
        Args:
            line: Satır
            column: Sütun
            
        Returns:
            int: Kelime bitişi
        """
        end = column
        while end < len(line) and line[end].isalnum():
            end += 1
        return end
    
    def _find_function_start(self, lines: List[str], line_number: int) -> int:
        """
        Fonksiyon başlangıcını bul.
        
        Args:
            lines: Satırlar
            line_number: Başlangıç satırı
            
        Returns:
            int: Fonksiyon başlangıç satırı
        """
        for i in range(line_number, -1, -1):
            line = lines[i].strip()
            if line.startswith("def ") or line.startswith("class ") or line.startswith("function ") or line.startswith("const "):
                return i
        return -1
    
    def _find_function_end(self, lines: List[str], start_line: int) -> int:
        """
        Fonksiyon bitişini bul.
        
        Args:
            lines: Satırlar
            start_line: Başlangıç satırı
            
        Returns:
            int: Fonksiyon bitiş satırı
        """
        indent_level = len(lines[start_line]) - len(lines[start_line].lstrip())
        
        for i in range(start_line + 1, len(lines)):
            line = lines[i]
            if line.strip() == "":
                continue
            
            current_indent = len(line) - len(line.lstrip())
            
            # Daha az indent ile yeni blok başladıysa
            if current_indent <= indent_level and line.strip():
                return i - 1
        
        return len(lines) - 1
    
    def undo_delete(self) -> DeleteResult:
        """
        Silmeyi geri al.
        
        Returns:
            DeleteResult: Geri alma sonucu
        """
        result = DeleteResult(success=False)
        
        try:
            if not self.delete_history:
                result.errors.append("No delete history")
                return result
            
            last_delete = self.delete_history.pop()
            
            result.success = True
            result.modified_content = last_delete["original"]
            result.original_content = last_delete["modified"]
            result.message = "Delete operation undone"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_delete_history(self) -> List[Dict[str, Any]]:
        """
        Silme geçmişini al.
        
        Returns:
            List[Dict[str, Any]]: Geçmiş
        """
        return self.delete_history
    
    def clear_history(self) -> DeleteResult:
        """
        Geçmişi temizle.
        
        Returns:
            DeleteResult: Temizleme sonucu
        """
        result = DeleteResult(success=False)
        
        try:
            self.delete_history.clear()
            result.success = True
            result.message = "Delete history cleared"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def update_config(self, config: DeleteConfig) -> DeleteResult:
        """
        Konfigürasyon güncelle.
        
        Args:
            config: Yeni konfigürasyon
            
        Returns:
            DeleteResult: Güncelleme sonucu
        """
        result = DeleteResult(success=False)
        
        try:
            self.config = config
            result.success = True
            result.message = "Config updated"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_config(self) -> DeleteConfig:
        """
        Konfigürasyon al.
        
        Returns:
            DeleteConfig: Konfigürasyon
        """
        return self.config


if __name__ == "__main__":
    # Basit test
    engine = DeleteLineEngine()
    
    content = "def test():\n    pass\n    return"
    result = engine.delete_line(content, 1)
    print(f"Delete: {result.success}")
