"""
MuhammedAI Local Developer - Toggle Comment
Toggle comment engine for code editor.
"""

import re
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from enum import Enum


class CommentStyle(Enum):
    """Comment style."""
    LINE = "line"
    BLOCK = "block"
    DOCSTRING = "docstring"


class CommentAction(Enum):
    """Comment action."""
    ADD = "add"
    REMOVE = "remove"
    TOGGLE = "toggle"


@dataclass
class CommentSyntax:
    """Comment syntax for a language."""
    language: str
    line_comment: str = "#"
    block_comment_start: str = "/*"
    block_comment_end: str = "*/"
    docstring_start: str = '"""'
    docstring_end: str = '"""'


@dataclass
class CommentEdit:
    """Comment edit."""
    start_line: int
    end_line: int
    start_column: int = 0
    end_column: int = 0
    old_text: str = ""
    new_text: str = ""
    action: CommentAction = CommentAction.TOGGLE


@dataclass
class ToggleCommentResult:
    """Toggle comment result."""
    success: bool
    original_code: Optional[str] = None
    modified_code: Optional[str] = None
    edits: List[CommentEdit] = field(default_factory=list)
    lines_changed: int = 0
    action_performed: CommentAction = CommentAction.TOGGLE
    errors: List[str] = field(default_factory=list)
    message: Optional[str] = None


class ToggleCommentEngine:
    """
    Toggle comment engine.
    
    Özellikler:
    - Toggle line comment
    - Toggle block comment
    - Comment selection
    - Uncomment selection
    - Language-specific comment syntax
    - Comment nesting
    - Comment preservation
    - Smart comment detection
    - Multi-line comment
    - Docstring comment
    """
    
    def __init__(self):
        """Initialize toggle comment engine."""
        self.comment_syntax_map = self._init_comment_syntax_map()
    
    def _init_comment_syntax_map(self) -> Dict[str, CommentSyntax]:
        """Initialize comment syntax map."""
        return {
            "python": CommentSyntax(
                language="python",
                line_comment="#",
                block_comment_start='"""',
                block_comment_end='"""',
                docstring_start='"""',
                docstring_end='"""'
            ),
            "javascript": CommentSyntax(
                language="javascript",
                line_comment="//",
                block_comment_start="/*",
                block_comment_end="*/",
                docstring_start="/**",
                docstring_end="*/"
            ),
            "typescript": CommentSyntax(
                language="typescript",
                line_comment="//",
                block_comment_start="/*",
                block_comment_end="*/",
                docstring_start="/**",
                docstring_end="*/"
            ),
            "java": CommentSyntax(
                language="java",
                line_comment="//",
                block_comment_start="/*",
                block_comment_end="*/",
                docstring_start="/**",
                docstring_end="*/"
            ),
            "c": CommentSyntax(
                language="c",
                line_comment="//",
                block_comment_start="/*",
                block_comment_end="*/",
                docstring_start="/*",
                docstring_end="*/"
            ),
            "cpp": CommentSyntax(
                language="cpp",
                line_comment="//",
                block_comment_start="/*",
                block_comment_end="*/",
                docstring_start="/**",
                docstring_end="*/"
            ),
            "csharp": CommentSyntax(
                language="csharp",
                line_comment="//",
                block_comment_start="/*",
                block_comment_end="*/",
                docstring_start="///",
                docstring_end=""
            ),
            "go": CommentSyntax(
                language="go",
                line_comment="//",
                block_comment_start="/*",
                block_comment_end="*/",
                docstring_start="/*",
                docstring_end="*/"
            ),
            "rust": CommentSyntax(
                language="rust",
                line_comment="//",
                block_comment_start="/*",
                block_comment_end="*/",
                docstring_start="//!",
                docstring_end=""
            ),
            "ruby": CommentSyntax(
                language="ruby",
                line_comment="#",
                block_comment_start="=begin",
                block_comment_end="=end",
                docstring_start="=begin",
                docstring_end="=end"
            ),
            "php": CommentSyntax(
                language="php",
                line_comment="//",
                block_comment_start="/*",
                block_comment_end="*/",
                docstring_start="/**",
                docstring_end="*/"
            ),
            "html": CommentSyntax(
                language="html",
                line_comment="<!--",
                block_comment_start="<!--",
                block_comment_end="-->",
                docstring_start="<!--",
                docstring_end="-->"
            ),
            "css": CommentSyntax(
                language="css",
                line_comment="/*",
                block_comment_start="/*",
                block_comment_end="*/",
                docstring_start="/*",
                docstring_end="*/"
            ),
            "sql": CommentSyntax(
                language="sql",
                line_comment="--",
                block_comment_start="/*",
                block_comment_end="*/",
                docstring_start="/*",
                docstring_end="*/"
            ),
            "shell": CommentSyntax(
                language="shell",
                line_comment="#",
                block_comment_start="",
                block_comment_end="",
                docstring_start="",
                docstring_end=""
            ),
            "bash": CommentSyntax(
                language="bash",
                line_comment="#",
                block_comment_start="",
                block_comment_end="",
                docstring_start="",
                docstring_end=""
            ),
            "json": CommentSyntax(
                language="json",
                line_comment="",
                block_comment_start="",
                block_comment_end="",
                docstring_start="",
                docstring_end=""
            ),
            "xml": CommentSyntax(
                language="xml",
                line_comment="<!--",
                block_comment_start="<!--",
                block_comment_end="-->",
                docstring_start="<!--",
                docstring_end="-->"
            ),
            "yaml": CommentSyntax(
                language="yaml",
                line_comment="#",
                block_comment_start="",
                block_comment_end="",
                docstring_start="",
                docstring_end=""
            ),
            "markdown": CommentSyntax(
                language="markdown",
                line_comment="<!--",
                block_comment_start="<!--",
                block_comment_end="-->",
                docstring_start="<!--",
                docstring_end="-->"
            )
        }
    
    def toggle_line_comment(
        self,
        code: str,
        line: int,
        language: str = "python"
    ) -> ToggleCommentResult:
        """
        Tek satır yorumu aç/kapat.
        
        Args:
            code: Kod içeriği
            line: Satır numarası
            language: Programlama dili
            
        Returns:
            ToggleCommentResult: Toggle sonucu
        """
        result = ToggleCommentResult(success=False)
        result.original_code = code
        
        try:
            syntax = self.comment_syntax_map.get(language.lower())
            if not syntax:
                result.errors.append(f"Unsupported language: {language}")
                return result
            
            lines = code.splitlines()
            if line >= len(lines):
                result.errors.append("Invalid line number")
                return result
            
            target_line = lines[line]
            stripped = target_line.strip()
            
            # Satır zaten yorumlanmış mı?
            if stripped.startswith(syntax.line_comment):
                # Yorumu kaldır
                new_line = target_line.replace(syntax.line_comment, "", 1).lstrip()
                lines[line] = new_line
                action = CommentAction.REMOVE
            else:
                # Yorum ekle
                new_line = syntax.line_comment + " " + target_line
                lines[line] = new_line
                action = CommentAction.ADD
            
            modified_code = "\n".join(lines)
            
            edit = CommentEdit(
                start_line=line,
                end_line=line,
                old_text=target_line,
                new_text=lines[line],
                action=action
            )
            
            result.modified_code = modified_code
            result.edits = [edit]
            result.lines_changed = 1
            result.action_performed = action
            result.success = True
            result.message = f"Line comment {action.value}d"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def toggle_block_comment(
        self,
        code: str,
        start_line: int,
        end_line: int,
        language: str = "python"
    ) -> ToggleCommentResult:
        """
        Blok yorumu aç/kapat.
        
        Args:
            code: Kod içeriği
            start_line: Başlangıç satırı
            end_line: Bitiş satırı
            language: Programlama dili
            
        Returns:
            ToggleCommentResult: Toggle sonucu
        """
        result = ToggleCommentResult(success=False)
        result.original_code = code
        
        try:
            syntax = self.comment_syntax_map.get(language.lower())
            if not syntax:
                result.errors.append(f"Unsupported language: {language}")
                return result
            
            if not syntax.block_comment_start or not syntax.block_comment_end:
                result.errors.append(f"Block comments not supported for {language}")
                return result
            
            lines = code.splitlines()
            if start_line >= len(lines) or end_line >= len(lines):
                result.errors.append("Invalid line range")
                return result
            
            # İlk satırı kontrol et
            first_line = lines[start_line].strip()
            last_line = lines[end_line].strip()
            
            # Blok yorumu zaten var mı?
            if first_line.startswith(syntax.block_comment_start) and last_line.endswith(syntax.block_comment_end):
                # Yorumu kaldır
                lines[start_line] = lines[start_line].replace(syntax.block_comment_start, "", 1).lstrip()
                lines[end_line] = lines[end_line].replace(syntax.block_comment_end, "").rstrip()
                action = CommentAction.REMOVE
            else:
                # Yorum ekle
                lines[start_line] = syntax.block_comment_start + " " + lines[start_line]
                lines[end_line] = lines[end_line] + " " + syntax.block_comment_end
                action = CommentAction.ADD
            
            modified_code = "\n".join(lines)
            
            edit = CommentEdit(
                start_line=start_line,
                end_line=end_line,
                action=action
            )
            
            result.modified_code = modified_code
            result.edits = [edit]
            result.lines_changed = end_line - start_line + 1
            result.action_performed = action
            result.success = True
            result.message = f"Block comment {action.value}d"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def comment_selection(
        self,
        code: str,
        start_line: int,
        end_line: int,
        language: str = "python"
    ) -> ToggleCommentResult:
        """
        Seçimi yorumla.
        
        Args:
            code: Kod içeriği
            start_line: Başlangıç satırı
            end_line: Bitiş satırı
            language: Programlama dili
            
        Returns:
            ToggleCommentResult: Comment sonucu
        """
        result = ToggleCommentResult(success=False)
        result.original_code = code
        
        try:
            syntax = self.comment_syntax_map.get(language.lower())
            if not syntax:
                result.errors.append(f"Unsupported language: {language}")
                return result
            
            lines = code.splitlines()
            if start_line >= len(lines) or end_line >= len(lines):
                result.errors.append("Invalid line range")
                return result
            
            edits = []
            for i in range(start_line, end_line + 1):
                target_line = lines[i]
                stripped = target_line.strip()
                
                if not stripped.startswith(syntax.line_comment):
                    new_line = syntax.line_comment + " " + target_line
                    lines[i] = new_line
                    
                    edit = CommentEdit(
                        start_line=i,
                        end_line=i,
                        old_text=target_line,
                        new_text=new_line,
                        action=CommentAction.ADD
                    )
                    edits.append(edit)
            
            modified_code = "\n".join(lines)
            
            result.modified_code = modified_code
            result.edits = edits
            result.lines_changed = len(edits)
            result.action_performed = CommentAction.ADD
            result.success = True
            result.message = f"Commented {len(edits)} lines"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def uncomment_selection(
        self,
        code: str,
        start_line: int,
        end_line: int,
        language: str = "python"
    ) -> ToggleCommentResult:
        """
        Seçimin yorumunu kaldır.
        
        Args:
            code: Kod içeriği
            start_line: Başlangıç satırı
            end_line: Bitiş satırı
            language: Programlama dili
            
        Returns:
            ToggleCommentResult: Uncomment sonucu
        """
        result = ToggleCommentResult(success=False)
        result.original_code = code
        
        try:
            syntax = self.comment_syntax_map.get(language.lower())
            if not syntax:
                result.errors.append(f"Unsupported language: {language}")
                return result
            
            lines = code.splitlines()
            if start_line >= len(lines) or end_line >= len(lines):
                result.errors.append("Invalid line range")
                return result
            
            edits = []
            for i in range(start_line, end_line + 1):
                target_line = lines[i]
                stripped = target_line.strip()
                
                if stripped.startswith(syntax.line_comment):
                    new_line = target_line.replace(syntax.line_comment, "", 1).lstrip()
                    lines[i] = new_line
                    
                    edit = CommentEdit(
                        start_line=i,
                        end_line=i,
                        old_text=target_line,
                        new_text=new_line,
                        action=CommentAction.REMOVE
                    )
                    edits.append(edit)
            
            modified_code = "\n".join(lines)
            
            result.modified_code = modified_code
            result.edits = edits
            result.lines_changed = len(edits)
            result.action_performed = CommentAction.REMOVE
            result.success = True
            result.message = f"Uncommented {len(edits)} lines"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def smart_toggle(
        self,
        code: str,
        start_line: int,
        end_line: int,
        language: str = "python"
    ) -> ToggleCommentResult:
        """
        Akıllı toggle (comment/uncomment otomatik).
        
        Args:
            code: Kod içeriği
            start_line: Başlangıç satırı
            end_line: Bitiş satırı
            language: Programlama dili
            
        Returns:
            ToggleCommentResult: Toggle sonucu
        """
        result = ToggleCommentResult(success=False)
        result.original_code = code
        
        try:
            syntax = self.comment_syntax_map.get(language.lower())
            if not syntax:
                result.errors.append(f"Unsupported language: {language}")
                return result
            
            lines = code.splitlines()
            if start_line >= len(lines) or end_line >= len(lines):
                result.errors.append("Invalid line range")
                return result
            
            # Tüm satırlar yorumlanmış mı kontrol et
            all_commented = True
            for i in range(start_line, end_line + 1):
                if not lines[i].strip().startswith(syntax.line_comment):
                    all_commented = False
                    break
            
            if all_commented:
                # Yorumları kaldır
                return self.uncomment_selection(code, start_line, end_line, language)
            else:
                # Yorumla
                return self.comment_selection(code, start_line, end_line, language)
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def add_docstring(
        self,
        code: str,
        line: int,
        language: str = "python"
    ) -> ToggleCommentResult:
        """
        Docstring ekle.
        
        Args:
            code: Kod içeriği
            line: Satır numarası
            language: Programlama dili
            
        Returns:
            ToggleCommentResult: Docstring ekleme sonucu
        """
        result = ToggleCommentResult(success=False)
        result.original_code = code
        
        try:
            syntax = self.comment_syntax_map.get(language.lower())
            if not syntax:
                result.errors.append(f"Unsupported language: {language}")
                return result
            
            if not syntax.docstring_start or not syntax.docstring_end:
                result.errors.append(f"Docstrings not supported for {language}")
                return result
            
            lines = code.splitlines()
            if line >= len(lines):
                result.errors.append("Invalid line number")
                return result
            
            # Docstring ekle
            docstring_line = syntax.docstring_start
            lines.insert(line, docstring_line)
            
            if syntax.docstring_end:
                lines.insert(line + 1, syntax.docstring_end)
            
            modified_code = "\n".join(lines)
            
            edit = CommentEdit(
                start_line=line,
                end_line=line + 1,
                action=CommentAction.ADD
            )
            
            result.modified_code = modified_code
            result.edits = [edit]
            result.lines_changed = 2 if syntax.docstring_end else 1
            result.action_performed = CommentAction.ADD
            result.success = True
            result.message = "Docstring added"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_comment_syntax(self, language: str) -> Optional[CommentSyntax]:
        """
        Dil için comment syntax al.
        
        Args:
            language: Programlama dili
            
        Returns:
            Optional[CommentSyntax]: Comment syntax
        """
        return self.comment_syntax_map.get(language.lower())
    
    def is_commented(self, code: str, line: int, language: str = "python") -> bool:
        """
        Satırın yorumlanmış olup olmadığını kontrol et.
        
        Args:
            code: Kod içeriği
            line: Satır numarası
            language: Programlama dili
            
        Returns:
            bool: Yorumlanmış mı
        """
        syntax = self.comment_syntax_map.get(language.lower())
        if not syntax:
            return False
        
        lines = code.splitlines()
        if line >= len(lines):
            return False
        
        return lines[line].strip().startswith(syntax.line_comment)


if __name__ == "__main__":
    # Basit test
    engine = ToggleCommentEngine()
    
    code = """def my_function():
    x = 10
    return x
"""
    
    # Line comment toggle
    result = engine.toggle_line_comment(code, 1, language="python")
    print(f"Toggle line comment: {result.success}")
    print(f"Modified code:\n{result.modified_code}")
