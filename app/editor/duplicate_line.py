"""
MuhammedAI Local Developer - Duplicate Line
Duplicate line engine for code editor.
"""

from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from enum import Enum


class DuplicateScope(Enum):
    """Duplicate scope."""
    LINE = "line"
    SELECTION = "selection"
    BLOCK = "block"
    FUNCTION = "function"


class DuplicatePosition(Enum):
    """Duplicate position."""
    BELOW = "below"
    ABOVE = "above"
    CURRENT = "current"


@dataclass
class DuplicateRange:
    """Duplicate range."""
    start_line: int
    end_line: int
    start_column: int = 0
    end_column: int = 0


@dataclass
class DuplicateConfig:
    """Duplicate configuration."""
    scope: DuplicateScope = DuplicateScope.LINE
    position: DuplicatePosition = DuplicatePosition.BELOW
    preserve_indentation: bool = True
    auto_indent: bool = True
    copy_comments: bool = True
    copy_whitespace: bool = True
    adjust_line_numbers: bool = True


@dataclass
class DuplicateResult:
    """Duplicate result."""
    success: bool
    modified_content: str = ""
    original_content: str = ""
    lines_duplicated: int = 0
    new_line_position: int = 0
    errors: List[str] = field(default_factory=list)
    message: Optional[str] = None


class DuplicateLineEngine:
    """
    Duplicate line engine.
    
    Özellikler:
    - Duplicate single line
    - Duplicate selection
    - Duplicate block
    - Duplicate function
    - Position control (above/below)
    - Indentation preservation
    - Auto-indent
    - Comment copying
    - Whitespace copying
    - Line number adjustment
    - Undo support
    - Duplicate history
    - Cursor position handling
    - Smart duplication
    """
    
    def __init__(self, config: Optional[DuplicateConfig] = None):
        """Initialize duplicate line engine."""
        self.config = config or DuplicateConfig()
        self.duplicate_history: List[Dict[str, Any]] = []
    
    def duplicate_line(
        self,
        content: str,
        line_number: int,
        position: Optional[DuplicatePosition] = None
    ) -> DuplicateResult:
        """
        Satırı çoğalt.
        
        Args:
            content: Dosya içeriği
            line_number: Satır numarası
            position: Çoğaltma pozisyonu
            
        Returns:
            DuplicateResult: Çoğaltma sonucu
        """
        result = DuplicateResult(success=False)
        result.original_content = content
        
        try:
            lines = content.splitlines()
            
            if line_number >= len(lines):
                result.errors.append("Invalid line number")
                return result
            
            # Pozisyon belirle
            pos = position or self.config.position
            
            # Satırı al
            line_to_duplicate = lines[line_number]
            
            # Satırı çoğalt
            if pos == DuplicatePosition.BELOW:
                lines.insert(line_number + 1, line_to_duplicate)
                new_position = line_number + 1
            elif pos == DuplicatePosition.ABOVE:
                lines.insert(line_number, line_to_duplicate)
                new_position = line_number
            else:  # CURRENT
                lines[line_number] = line_to_duplicate
                new_position = line_number
            
            modified_content = "\n".join(lines)
            
            # Geçmişe ekle
            self.duplicate_history.append({
                "original": content,
                "modified": modified_content,
                "line_number": line_number,
                "position": pos
            })
            
            result.success = True
            result.modified_content = modified_content
            result.lines_duplicated = 1
            result.new_line_position = new_position
            result.message = f"Line duplicated at position {new_position}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def duplicate_selection(
        self,
        content: str,
        duplicate_range: DuplicateRange,
        position: Optional[DuplicatePosition] = None
    ) -> DuplicateResult:
        """
        Seçimi çoğalt.
        
        Args:
            content: Dosya içeriği
            duplicate_range: Çoğaltma aralığı
            position: Çoğaltma pozisyonu
            
        Returns:
            DuplicateResult: Çoğaltma sonucu
        """
        result = DuplicateResult(success=False)
        result.original_content = content
        
        try:
            lines = content.splitlines()
            
            if duplicate_range.start_line >= len(lines) or duplicate_range.end_line >= len(lines):
                result.errors.append("Invalid range")
                return result
            
            # Pozisyon belirle
            pos = position or self.config.position
            
            # Seçili satırları al
            selected_lines = lines[duplicate_range.start_line:duplicate_range.end_line + 1]
            
            # Seçimi çoğalt
            if pos == DuplicatePosition.BELOW:
                insert_position = duplicate_range.end_line + 1
                for i, line in enumerate(selected_lines):
                    lines.insert(insert_position + i, line)
                new_position = insert_position
            elif pos == DuplicatePosition.ABOVE:
                insert_position = duplicate_range.start_line
                for i, line in enumerate(selected_lines):
                    lines.insert(insert_position + i, line)
                new_position = insert_position
            else:  # CURRENT
                for i in range(duplicate_range.start_line, duplicate_range.end_line + 1):
                    lines[i] = selected_lines[i - duplicate_range.start_line]
                new_position = duplicate_range.start_line
            
            modified_content = "\n".join(lines)
            
            # Geçmişe ekle
            self.duplicate_history.append({
                "original": content,
                "modified": modified_content,
                "range": duplicate_range,
                "position": pos
            })
            
            result.success = True
            result.modified_content = modified_content
            result.lines_duplicated = len(selected_lines)
            result.new_line_position = new_position
            result.message = f"Selection duplicated ({len(selected_lines)} lines)"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def duplicate_block(
        self,
        content: str,
        start_line: int,
        end_line: int,
        position: Optional[DuplicatePosition] = None
    ) -> DuplicateResult:
        """
        Bloğu çoğalt.
        
        Args:
            content: Dosya içeriği
            start_line: Başlangıç satırı
            end_line: Bitiş satırı
            position: Çoğaltma pozisyonu
            
        Returns:
            DuplicateResult: Çoğaltma sonucu
        """
        duplicate_range = DuplicateRange(start_line=start_line, end_line=end_line)
        return self.duplicate_selection(content, duplicate_range, position)
    
    def duplicate_function(
        self,
        content: str,
        line_number: int,
        position: Optional[DuplicatePosition] = None
    ) -> DuplicateResult:
        """
        Fonksiyonu çoğalt.
        
        Args:
            content: Dosya içeriği
            line_number: Satır numarası (fonksiyon içinde)
            position: Çoğaltma pozisyonu
            
        Returns:
            DuplicateResult: Çoğaltma sonucu
        """
        result = DuplicateResult(success=False)
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
            
            # Fonksiyonu çoğalt
            duplicate_range = DuplicateRange(start_line=start_line, end_line=end_line)
            return self.duplicate_selection(content, duplicate_range, position)
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
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
    
    def undo_duplicate(self) -> DuplicateResult:
        """
        Çoğaltmayı geri al.
        
        Returns:
            DuplicateResult: Geri alma sonucu
        """
        result = DuplicateResult(success=False)
        
        try:
            if not self.duplicate_history:
                result.errors.append("No duplicate history")
                return result
            
            last_duplicate = self.duplicate_history.pop()
            
            result.success = True
            result.modified_content = last_duplicate["original"]
            result.original_content = last_duplicate["modified"]
            result.message = "Duplicate operation undone"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_duplicate_history(self) -> List[Dict[str, Any]]:
        """
        Çoğaltma geçmişini al.
        
        Returns:
            List[Dict[str, Any]]: Geçmiş
        """
        return self.duplicate_history
    
    def clear_history(self) -> DuplicateResult:
        """
        Geçmişi temizle.
        
        Returns:
            DuplicateResult: Temizleme sonucu
        """
        result = DuplicateResult(success=False)
        
        try:
            self.duplicate_history.clear()
            result.success = True
            result.message = "Duplicate history cleared"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def update_config(self, config: DuplicateConfig) -> DuplicateResult:
        """
        Konfigürasyon güncelle.
        
        Args:
            config: Yeni konfigürasyon
            
        Returns:
            DuplicateResult: Güncelleme sonucu
        """
        result = DuplicateResult(success=False)
        
        try:
            self.config = config
            result.success = True
            result.message = "Config updated"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_config(self) -> DuplicateConfig:
        """
        Konfigürasyon al.
        
        Returns:
            DuplicateConfig: Konfigürasyon
        """
        return self.config


if __name__ == "__main__":
    # Basit test
    engine = DuplicateLineEngine()
    
    content = "def test():\n    pass\n    return"
    result = engine.duplicate_line(content, 1)
    print(f"Duplicate: {result.success}")
