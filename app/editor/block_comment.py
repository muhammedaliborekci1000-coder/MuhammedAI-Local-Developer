"""
MuhammedAI Local Developer - Block Comment
Block comment engine for code editor.
"""

from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from enum import Enum


class BlockCommentStyle(Enum):
    """Block comment style."""
    MULTILINE = "multiline"
    SINGLE_LINE = "single_line"
    WRAP = "wrap"
    BOX = "box"


class BlockCommentAction(Enum):
    """Block comment action."""
    ADD = "add"
    REMOVE = "remove"
    TOGGLE = "toggle"
    WRAP = "wrap"
    UNWRAP = "unwrap"


@dataclass
class BlockCommentRange:
    """Block comment range."""
    start_line: int
    end_line: int
    start_column: int = 0
    end_column: int = 0


@dataclass
class BlockCommentSyntax:
    """Block comment syntax for a language."""
    language: str
    start_marker: str = "/*"
    end_marker: str = "*/"
    line_prefix: str = "*"
    single_line_prefix: str = "//"
    wrap_start: str = "/*"
    wrap_end: str = "*/"


@dataclass
class BlockCommentConfig:
    """Block comment configuration."""
    style: BlockCommentStyle = BlockCommentStyle.MULTILINE
    add_space_after_marker: bool = True
    preserve_indentation: bool = True
    align_markers: bool = True
    box_style: bool = False
    box_width: int = 80
    comment_char: str = "*"


@dataclass
class BlockCommentResult:
    """Block comment result."""
    success: bool
    modified_content: str = ""
    original_content: str = ""
    lines_changed: int = 0
    action_performed: BlockCommentAction = BlockCommentAction.ADD
    errors: List[str] = field(default_factory=list)
    message: Optional[str] = None


class BlockCommentEngine:
    """
    Block comment engine.
    
    Özellikler:
    - Add block comment
    - Remove block comment
    - Toggle block comment
    - Wrap selection in block comment
    - Unwrap block comment
    - Multiline block comment
    - Single-line block comment
    - Box-style block comment
    - Language-specific syntax
    - Indentation preservation
    - Marker alignment
    - Comment wrapping
    - Nested block comments
    - Comment validation
    - Undo support
    - Comment history
    - Smart detection
    - Preview changes
    """
    
    def __init__(self, config: Optional[BlockCommentConfig] = None):
        """Initialize block comment engine."""
        self.config = config or BlockCommentConfig()
        self.comment_history: List[Dict[str, Any]] = []
        self.syntax_map = self._init_syntax_map()
    
    def _init_syntax_map(self) -> Dict[str, BlockCommentSyntax]:
        """Initialize syntax map."""
        return {
            "python": BlockCommentSyntax(
                language="python",
                start_marker='"""',
                end_marker='"""',
                line_prefix="",
                single_line_prefix="#",
                wrap_start='"""',
                wrap_end='"""'
            ),
            "javascript": BlockCommentSyntax(
                language="javascript",
                start_marker="/*",
                end_marker="*/",
                line_prefix="*",
                single_line_prefix="//",
                wrap_start="/*",
                wrap_end="*/"
            ),
            "typescript": BlockCommentSyntax(
                language="typescript",
                start_marker="/*",
                end_marker="*/",
                line_prefix="*",
                single_line_prefix="//",
                wrap_start="/*",
                wrap_end="*/"
            ),
            "java": BlockCommentSyntax(
                language="java",
                start_marker="/*",
                end_marker="*/",
                line_prefix="*",
                single_line_prefix="//",
                wrap_start="/*",
                wrap_end="*/"
            ),
            "c": BlockCommentSyntax(
                language="c",
                start_marker="/*",
                end_marker="*/",
                line_prefix="*",
                single_line_prefix="//",
                wrap_start="/*",
                wrap_end="*/"
            ),
            "cpp": BlockCommentSyntax(
                language="cpp",
                start_marker="/*",
                end_marker="*/",
                line_prefix="*",
                single_line_prefix="//",
                wrap_start="/*",
                wrap_end="*/"
            ),
            "csharp": BlockCommentSyntax(
                language="csharp",
                start_marker="/*",
                end_marker="*/",
                line_prefix="*",
                single_line_prefix="//",
                wrap_start="/*",
                wrap_end="*/"
            ),
            "go": BlockCommentSyntax(
                language="go",
                start_marker="/*",
                end_marker="*/",
                line_prefix="*",
                single_line_prefix="//",
                wrap_start="/*",
                wrap_end="*/"
            ),
            "rust": BlockCommentSyntax(
                language="rust",
                start_marker="/*",
                end_marker="*/",
                line_prefix="*",
                single_line_prefix="//",
                wrap_start="/*",
                wrap_end="*/"
            ),
            "ruby": BlockCommentSyntax(
                language="ruby",
                start_marker="=begin",
                end_marker="=end",
                line_prefix="",
                single_line_prefix="#",
                wrap_start="=begin",
                wrap_end="=end"
            ),
            "php": BlockCommentSyntax(
                language="php",
                start_marker="/*",
                end_marker="*/",
                line_prefix="*",
                single_line_prefix="//",
                wrap_start="/*",
                wrap_end="*/"
            ),
            "html": BlockCommentSyntax(
                language="html",
                start_marker="<!--",
                end_marker="-->",
                line_prefix="",
                single_line_prefix="<!--",
                wrap_start="<!--",
                wrap_end="-->"
            ),
            "css": BlockCommentSyntax(
                language="css",
                start_marker="/*",
                end_marker="*/",
                line_prefix="*",
                single_line_prefix="",
                wrap_start="/*",
                wrap_end="*/"
            ),
            "sql": BlockCommentSyntax(
                language="sql",
                start_marker="/*",
                end_marker="*/",
                line_prefix="*",
                single_line_prefix="--",
                wrap_start="/*",
                wrap_end="*/"
            ),
            "shell": BlockCommentSyntax(
                language="shell",
                start_marker="",
                end_marker="",
                line_prefix="",
                single_line_prefix="#",
                wrap_start="",
                wrap_end=""
            ),
            "bash": BlockCommentSyntax(
                language="bash",
                start_marker="",
                end_marker="",
                line_prefix="",
                single_line_prefix="#",
                wrap_start="",
                wrap_end=""
            ),
            "xml": BlockCommentSyntax(
                language="xml",
                start_marker="<!--",
                end_marker="-->",
                line_prefix="",
                single_line_prefix="<!--",
                wrap_start="<!--",
                wrap_end="-->"
            ),
            "yaml": BlockCommentSyntax(
                language="yaml",
                start_marker="",
                end_marker="",
                line_prefix="",
                single_line_prefix="#",
                wrap_start="",
                wrap_end=""
            )
        }
    
    def add_block_comment(
        self,
        content: str,
        comment_range: BlockCommentRange,
        language: str = "python"
    ) -> BlockCommentResult:
        """
        Blok yorumu ekle.
        
        Args:
            content: Dosya içeriği
            comment_range: Blok aralığı
            language: Programlama dili
            
        Returns:
            BlockCommentResult: Ekleme sonucu
        """
        result = BlockCommentResult(success=False)
        result.original_content = content
        
        try:
            syntax = self.syntax_map.get(language.lower())
            if not syntax:
                result.errors.append(f"Unsupported language: {language}")
                return result
            
            if not syntax.start_marker or not syntax.end_marker:
                result.errors.append(f"Block comments not supported for {language}")
                return result
            
            lines = content.splitlines()
            
            if comment_range.start_line >= len(lines) or comment_range.end_line >= len(lines):
                result.errors.append("Invalid range")
                return result
            
            # Blok yorumu ekle
            if self.config.style == BlockCommentStyle.MULTILINE:
                modified_lines = self._add_multiline_comment(lines, comment_range, syntax)
            elif self.config.style == BlockCommentStyle.SINGLE_LINE:
                modified_lines = self._add_single_line_comment(lines, comment_range, syntax)
            elif self.config.style == BlockCommentStyle.WRAP:
                modified_lines = self._wrap_comment(lines, comment_range, syntax)
            elif self.config.style == BlockCommentStyle.BOX:
                modified_lines = self._add_box_comment(lines, comment_range, syntax)
            else:
                modified_lines = self._add_multiline_comment(lines, comment_range, syntax)
            
            modified_content = "\n".join(modified_lines)
            
            # Geçmişe ekle
            self.comment_history.append({
                "original": content,
                "modified": modified_content,
                "range": comment_range,
                "language": language,
                "action": BlockCommentAction.ADD
            })
            
            result.success = True
            result.modified_content = modified_content
            result.lines_changed = len(modified_lines) - len(lines)
            result.action_performed = BlockCommentAction.ADD
            result.message = f"Block comment added (lines {comment_range.start_line}-{comment_range.end_line})"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def _add_multiline_comment(
        self,
        lines: List[str],
        comment_range: BlockCommentRange,
        syntax: BlockCommentSyntax
    ) -> List[str]:
        """
        Multiline blok yorumu ekle.
        
        Args:
            lines: Satırlar
            comment_range: Aralık
            syntax: Syntax
            
        Returns:
            List[str]: Değiştirilmiş satırlar
        """
        modified_lines = lines.copy()
        
        # Başlangıç işaretçisini ekle
        start_line = modified_lines[comment_range.start_line]
        if self.config.add_space_after_marker:
            modified_lines[comment_range.start_line] = syntax.start_marker + " " + start_line
        else:
            modified_lines[comment_range.start_line] = syntax.start_marker + start_line
        
        # Bitiş işaretçisini ekle
        end_line = modified_lines[comment_range.end_line]
        if self.config.add_space_after_marker:
            modified_lines[comment_range.end_line] = end_line + " " + syntax.end_marker
        else:
            modified_lines[comment_range.end_line] = end_line + syntax.end_marker
        
        return modified_lines
    
    def _add_single_line_comment(
        self,
        lines: List[str],
        comment_range: BlockCommentRange,
        syntax: BlockCommentSyntax
    ) -> List[str]:
        """
        Single-line blok yorumu ekle.
        
        Args:
            lines: Satırlar
            comment_range: Aralık
            syntax: Syntax
            
        Returns:
            List[str]: Değiştirilmiş satırlar
        """
        modified_lines = lines.copy()
        
        for i in range(comment_range.start_line, comment_range.end_line + 1):
            line = modified_lines[i]
            if syntax.single_line_prefix:
                if self.config.add_space_after_marker:
                    modified_lines[i] = syntax.single_line_prefix + " " + line
                else:
                    modified_lines[i] = syntax.single_line_prefix + line
        
        return modified_lines
    
    def _wrap_comment(
        self,
        lines: List[str],
        comment_range: BlockCommentRange,
        syntax: BlockCommentSyntax
    ) -> List[str]:
        """
        Seçimi blok yorumuna sar.
        
        Args:
            lines: Satırlar
            comment_range: Aralık
            syntax: Syntax
            
        Returns:
            List[str]: Değiştirilmiş satırlar
        """
        modified_lines = lines.copy()
        
        # Başlangıç satırını ekle
        indent = " " * (len(lines[comment_range.start_line]) - len(lines[comment_range.start_line].lstrip()))
        start_marker = indent + syntax.wrap_start
        modified_lines.insert(comment_range.start_line, start_marker)
        
        # Bitiş satırını ekle
        end_marker = indent + syntax.wrap_end
        modified_lines.insert(comment_range.end_line + 2, end_marker)
        
        return modified_lines
    
    def _add_box_comment(
        self,
        lines: List[str],
        comment_range: BlockCommentRange,
        syntax: BlockCommentSyntax
    ) -> List[str]:
        """
        Box-style blok yorumu ekle.
        
        Args:
            lines: Satırlar
            comment_range: Aralık
            syntax: Syntax
            
        Returns:
            List[str]: Değiştirilmiş satırlar
        """
        modified_lines = lines.copy()
        width = self.config.box_width
        char = self.config.comment_char
        
        # Üst sınır
        top_border = " " + char * (width - 2)
        modified_lines.insert(comment_range.start_line, top_border)
        
        # Alt sınır
        bottom_border = " " + char * (width - 2)
        modified_lines.insert(comment_range.end_line + 2, bottom_border)
        
        # Yan sınırlar
        for i in range(comment_range.start_line + 1, comment_range.end_line + 2):
            line = modified_lines[i]
            if len(line) < width - 2:
                line = line + " " * (width - 2 - len(line))
            modified_lines[i] = char + " " + line + " " + char
        
        return modified_lines
    
    def remove_block_comment(
        self,
        content: str,
        comment_range: BlockCommentRange,
        language: str = "python"
    ) -> BlockCommentResult:
        """
        Blok yorumunu kaldır.
        
        Args:
            content: Dosya içeriği
            comment_range: Blok aralığı
            language: Programlama dili
            
        Returns:
            BlockCommentResult: Kaldırma sonucu
        """
        result = BlockCommentResult(success=False)
        result.original_content = content
        
        try:
            syntax = self.syntax_map.get(language.lower())
            if not syntax:
                result.errors.append(f"Unsupported language: {language}")
                return result
            
            lines = content.splitlines()
            
            if comment_range.start_line >= len(lines) or comment_range.end_line >= len(lines):
                result.errors.append("Invalid range")
                return result
            
            # Blok yorumunu kaldır
            modified_lines = lines.copy()
            
            # Başlangıç işaretçisini kaldır
            modified_lines[comment_range.start_line] = modified_lines[comment_range.start_line].replace(syntax.start_marker, "", 1).lstrip()
            
            # Bitiş işaretçisini kaldır
            modified_lines[comment_range.end_line] = modified_lines[comment_range.end_line].replace(syntax.end_marker, "").rstrip()
            
            modified_content = "\n".join(modified_lines)
            
            # Geçmişe ekle
            self.comment_history.append({
                "original": content,
                "modified": modified_content,
                "range": comment_range,
                "language": language,
                "action": BlockCommentAction.REMOVE
            })
            
            result.success = True
            result.modified_content = modified_content
            result.lines_changed = comment_range.end_line - comment_range.start_line + 1
            result.action_performed = BlockCommentAction.REMOVE
            result.message = f"Block comment removed (lines {comment_range.start_line}-{comment_range.end_line})"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def toggle_block_comment(
        self,
        content: str,
        comment_range: BlockCommentRange,
        language: str = "python"
    ) -> BlockCommentResult:
        """
        Blok yorumunu aç/kapat.
        
        Args:
            content: Dosya içeriği
            comment_range: Blok aralığı
            language: Programlama dili
            
        Returns:
            BlockCommentResult: Toggle sonucu
        """
        result = BlockCommentResult(success=False)
        result.original_content = content
        
        try:
            syntax = self.syntax_map.get(language.lower())
            if not syntax:
                result.errors.append(f"Unsupported language: {language}")
                return result
            
            lines = content.splitlines()
            
            if comment_range.start_line >= len(lines) or comment_range.end_line >= len(lines):
                result.errors.append("Invalid range")
                return result
            
            # Blok yorumu var mı kontrol et
            first_line = lines[comment_range.start_line].strip()
            last_line = lines[comment_range.end_line].strip()
            
            if first_line.startswith(syntax.start_marker) and last_line.endswith(syntax.end_marker):
                # Yorumu kaldır
                return self.remove_block_comment(content, comment_range, language)
            else:
                # Yorum ekle
                return self.add_block_comment(content, comment_range, language)
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def unwrap_comment(
        self,
        content: str,
        comment_range: BlockCommentRange,
        language: str = "python"
    ) -> BlockCommentResult:
        """
        Blok yorumunu aç (unwrap).
        
        Args:
            content: Dosya içeriği
            comment_range: Blok aralığı
            language: Programlama dili
            
        Returns:
            BlockCommentResult: Unwrap sonucu
        """
        result = BlockCommentResult(success=False)
        result.original_content = content
        
        try:
            syntax = self.syntax_map.get(language.lower())
            if not syntax:
                result.errors.append(f"Unsupported language: {language}")
                return result
            
            lines = content.splitlines()
            
            if comment_range.start_line >= len(lines) or comment_range.end_line >= len(lines):
                result.errors.append("Invalid range")
                return result
            
            # Wrap satırlarını kaldır
            modified_lines = lines.copy()
            
            # Başlangıç wrap satırını kontrol et ve kaldır
            if modified_lines[comment_range.start_line].strip() == syntax.wrap_start:
                modified_lines.pop(comment_range.start_line)
                comment_range.end_line -= 1
            
            # Bitiş wrap satırını kontrol et ve kaldır
            if comment_range.end_line < len(modified_lines) and modified_lines[comment_range.end_line].strip() == syntax.wrap_end:
                modified_lines.pop(comment_range.end_line)
            
            modified_content = "\n".join(modified_lines)
            
            result.success = True
            result.modified_content = modified_content
            result.lines_changed = len(lines) - len(modified_lines)
            result.action_performed = BlockCommentAction.UNWRAP
            result.message = "Comment unwrapped"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def undo_comment(self) -> BlockCommentResult:
        """
        Yorumu geri al.
        
        Returns:
            BlockCommentResult: Geri alma sonucu
        """
        result = BlockCommentResult(success=False)
        
        try:
            if not self.comment_history:
                result.errors.append("No comment history")
                return result
            
            last_comment = self.comment_history.pop()
            
            result.success = True
            result.modified_content = last_comment["original"]
            result.original_content = last_comment["modified"]
            result.message = "Comment operation undone"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_comment_history(self) -> List[Dict[str, Any]]:
        """
        Yorum geçmişini al.
        
        Returns:
            List[Dict[str, Any]]: Geçmiş
        """
        return self.comment_history
    
    def clear_history(self) -> BlockCommentResult:
        """
        Geçmişi temizle.
        
        Returns:
            BlockCommentResult: Temizleme sonucu
        """
        result = BlockCommentResult(success=False)
        
        try:
            self.comment_history.clear()
            result.success = True
            result.message = "Comment history cleared"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def update_config(self, config: BlockCommentConfig) -> BlockCommentResult:
        """
        Konfigürasyon güncelle.
        
        Args:
            config: Yeni konfigürasyon
            
        Returns:
            BlockCommentResult: Güncelleme sonucu
        """
        result = BlockCommentResult(success=False)
        
        try:
            self.config = config
            result.success = True
            result.message = "Config updated"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_config(self) -> BlockCommentConfig:
        """
        Konfigürasyon al.
        
        Returns:
            BlockCommentConfig: Konfigürasyon
        """
        return self.config


if __name__ == "__main__":
    # Basit test
    engine = BlockCommentEngine()
    
    content = "def test():\n    pass\n    return"
    range = BlockCommentRange(start_line=0, end_line=2)
    result = engine.add_block_comment(content, range)
    print(f"Add block comment: {result.success}")
