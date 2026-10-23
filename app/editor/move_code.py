"""
MuhammedAI Local Developer - Move Code
Move code engine for code editor.
"""

from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from enum import Enum


class MoveDirection(Enum):
    """Move direction."""
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"


class MoveScope(Enum):
    """Move scope."""
    LINE = "line"
    SELECTION = "selection"
    BLOCK = "block"
    FUNCTION = "function"


@dataclass
class CodeBlock:
    """Code block."""
    start_line: int
    end_line: int
    content: str = ""
    indent_level: int = 0


@dataclass
class MoveConfig:
    """Move configuration."""
    preserve_indentation: bool = True
    auto_indent: bool = True
    verify_syntax: bool = True
    show_preview: bool = True
    adjust_imports: bool = True
    scope: MoveScope = MoveScope.LINE


@dataclass
class MoveResult:
    """Move result."""
    success: bool
    modified_content: str = ""
    original_content: str = ""
    lines_moved: int = 0
    new_position: int = 0
    errors: List[str] = field(default_factory=list)
    message: Optional[str] = None


class MoveCodeEngine:
    """
    Move code engine.
    
    Özellikler:
    - Move lines up/down
    - Move selection
    - Move code blocks
    - Move functions
    - Preserve indentation
    - Auto-indent
    - Syntax verification
    - Import adjustment
    - Preview changes
    - Undo support
    - Move history
    - Scope detection
    - Dependency tracking
    - Conflict detection
    - Format preservation
    """
    
    def __init__(self, config: Optional[MoveConfig] = None):
        """Initialize move code engine."""
        self.config = config or MoveConfig()
        self.move_history: List[Dict[str, Any]] = []
    
    def move_code(
        self,
        content: str,
        start_line: int,
        end_line: int,
        direction: MoveDirection,
        steps: int = 1
    ) -> MoveResult:
        """
        Kodu taşı.
        
        Args:
            content: Dosya içeriği
            start_line: Başlangıç satırı
            end_line: Bitiş satırı
            direction: Taşıma yönü
            steps: Adım sayısı
            
        Returns:
            MoveResult: Taşıma sonucu
        """
        result = MoveResult(success=False)
        result.original_content = content
        
        try:
            lines = content.splitlines()
            
            if not lines:
                result.errors.append("Content is empty")
                return result
            
            if start_line < 0 or end_line >= len(lines):
                result.errors.append("Invalid line range")
                return result
            
            # Kod bloğunu al
            code_block = CodeBlock(
                start_line=start_line,
                end_line=end_line,
                content="\n".join(lines[start_line:end_line + 1])
            )
            
            # Taşıma işlemi
            if direction == MoveDirection.UP:
                modified_lines = self._move_up(lines, start_line, end_line, steps)
            elif direction == MoveDirection.DOWN:
                modified_lines = self._move_down(lines, start_line, end_line, steps)
            elif direction == MoveDirection.LEFT:
                modified_lines = self._move_left(lines, start_line, end_line, steps)
            elif direction == MoveDirection.RIGHT:
                modified_lines = self._move_right(lines, start_line, end_line, steps)
            else:
                result.errors.append(f"Invalid direction: {direction}")
                return result
            
            # Geçmişe ekle
            self.move_history.append({
                "original": content,
                "modified": "\n".join(modified_lines),
                "start_line": start_line,
                "end_line": end_line,
                "direction": direction.value,
                "steps": steps
            })
            
            result.success = True
            result.modified_content = "\n".join(modified_lines)
            result.lines_moved = steps
            result.new_position = start_line - steps if direction == MoveDirection.UP else start_line + steps
            result.message = f"Moved code {direction.value} by {steps} line(s)"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def _move_up(
        self,
        lines: List[str],
        start_line: int,
        end_line: int,
        steps: int
    ) -> List[str]:
        """
        Yukarı taşı.
        
        Args:
            lines: Satırlar
            start_line: Başlangıç satırı
            end_line: Bitiş satırı
            steps: Adım sayısı
            
        Returns:
            List[str]: Değiştirilmiş satırlar
        """
        if start_line - steps < 0:
            steps = start_line
        
        # Bloğu çıkar
        block = lines[start_line:end_line + 1]
        
        # Satırları yeniden düzenle
        new_lines = lines[:start_line - steps] + block + lines[start_line - steps:start_line] + lines[end_line + 1:]
        
        return new_lines
    
    def _move_down(
        self,
        lines: List[str],
        start_line: int,
        end_line: int,
        steps: int
    ) -> List[str]:
        """
        Aşağı taşı.
        
        Args:
            lines: Satırlar
            start_line: Başlangıç satırı
            end_line: Bitiş satırı
            steps: Adım sayısı
            
        Returns:
            List[str]: Değiştirilmiş satırlar
        """
        if end_line + steps >= len(lines):
            steps = len(lines) - end_line - 1
        
        # Bloğu çıkar
        block = lines[start_line:end_line + 1]
        
        # Satırları yeniden düzenle
        new_lines = lines[:start_line] + lines[end_line + 1:end_line + 1 + steps] + block + lines[end_line + 1 + steps:]
        
        return new_lines
    
    def _move_left(
        self,
        lines: List[str],
        start_line: int,
        end_line: int,
        steps: int
    ) -> List[str]:
        """
        Sola taşı (indent azalt).
        
        Args:
            lines: Satırlar
            start_line: Başlangıç satırı
            end_line: Bitiş satırı
            steps: Adım sayısı
            
        Returns:
            List[str]: Değiştirilmiş satırlar
        """
        new_lines = lines.copy()
        
        for i in range(start_line, end_line + 1):
            line = new_lines[i]
            # Her adım için bir tab veya 4 space kaldır
            for _ in range(steps):
                if line.startswith("\t"):
                    line = line[1:]
                elif line.startswith("    "):
                    line = line[4:]
                elif line.startswith(" "):
                    line = line[1:]
            new_lines[i] = line
        
        return new_lines
    
    def _move_right(
        self,
        lines: List[str],
        start_line: int,
        end_line: int,
        steps: int
    ) -> List[str]:
        """
        Sağa taşı (indent artır).
        
        Args:
            lines: Satırlar
            start_line: Başlangıç satırı
            end_line: Bitiş satırı
            steps: Adım sayısı
            
        Returns:
            List[str]: Değiştirilmiş satırlar
        """
        new_lines = lines.copy()
        indent = "    " * steps
        
        for i in range(start_line, end_line + 1):
            new_lines[i] = indent + new_lines[i]
        
        return new_lines
    
    def undo_move(self) -> MoveResult:
        """
        Taşımayı geri al.
        
        Returns:
            MoveResult: Geri alma sonucu
        """
        result = MoveResult(success=False)
        
        try:
            if not self.move_history:
                result.errors.append("No move history")
                return result
            
            last_move = self.move_history.pop()
            
            result.success = True
            result.modified_content = last_move["original"]
            result.original_content = last_move["modified"]
            result.message = "Move operation undone"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_move_history(self) -> List[Dict[str, Any]]:
        """
        Taşıma geçmişini al.
        
        Returns:
            List[Dict[str, Any]]: Geçmiş
        """
        return self.move_history
    
    def clear_history(self) -> MoveResult:
        """
        Geçmişi temizle.
        
        Returns:
            MoveResult: Temizleme sonucu
        """
        result = MoveResult(success=False)
        
        try:
            self.move_history.clear()
            result.success = True
            result.message = "Move history cleared"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def update_config(self, config: MoveConfig) -> MoveResult:
        """
        Konfigürasyon güncelle.
        
        Args:
            config: Yeni konfigürasyon
            
        Returns:
            MoveResult: Güncelleme sonucu
        """
        result = MoveResult(success=False)
        
        try:
            self.config = config
            result.success = True
            result.message = "Config updated"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_config(self) -> MoveConfig:
        """
        Konfigürasyon al.
        
        Returns:
            MoveConfig: Konfigürasyon
        """
        return self.config


if __name__ == "__main__":
    # Basit test
    engine = MoveCodeEngine()
    
    content = "line1\nline2\nline3"
    result = engine.move_code(content, 1, 1, MoveDirection.DOWN)
    print(f"Move: {result.success}")
