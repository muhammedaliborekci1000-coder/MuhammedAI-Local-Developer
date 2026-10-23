"""
MuhammedAI Local Developer - Hover Information
Hover information engine for code editor.
"""

import ast
import os
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum


class HoverKind(Enum):
    """Hover kind."""
    VARIABLE = "variable"
    FUNCTION = "function"
    CLASS = "class"
    METHOD = "method"
    PARAMETER = "parameter"
    MODULE = "module"
    IMPORT = "import"
    KEYWORD = "keyword"
    STRING = "string"
    NUMBER = "number"
    COMMENT = "comment"


@dataclass
class HoverContent:
    """Hover content."""
    text: str
    kind: HoverKind
    documentation: Optional[str] = None
    type_info: Optional[str] = None
    definition: Optional[str] = None
    file_path: Optional[str] = None
    line: Optional[int] = None
    column: Optional[int] = None


@dataclass
class HoverResult:
    """Hover result."""
    success: bool
    content: Optional[HoverContent] = None
    range_start: int = 0
    range_end: int = 0
    errors: List[str] = field(default_factory=list)
    message: Optional[str] = None


class HoverInformationEngine:
    """
    Hover information engine.
    
    Özellikler:
    - Variable type information
    - Function signature display
    - Class information display
    - Method information display
    - Documentation display
    - Definition location
    - Type hints
    - Import information
    - Keyword information
    - Rich text formatting
    - Multi-language support
    - Hover for symbols
    - Hover for literals
    - Quick actions
    """
    
    def __init__(self):
        """Initialize hover information engine."""
        self.current_content: Optional[HoverContent] = None
    
    def get_hover_info(
        self,
        code: str,
        position: int,
        language: str = "python"
    ) -> HoverResult:
        """
        Hover bilgisini al.
        
        Args:
            code: Kod içeriği
            position: Cursor pozisyonu
            language: Programlama dili
            
        Returns:
            HoverResult: Hover sonucu
        """
        result = HoverResult(success=False)
        
        try:
            if language == "python":
                content = self._get_python_hover(code, position)
            else:
                content = self._get_generic_hover(code, position)
            
            if content:
                result.content = content
                result.range_start = position
                result.range_end = position + len(content.text)
                result.success = True
                result.message = f"Hover info for: {content.text}"
            else:
                result.success = True
                result.message = "No hover information available"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def _get_python_hover(self, code: str, position: int) -> Optional[HoverContent]:
        """Python hover bilgisini al."""
        lines = code.splitlines()
        char_count = 0
        target_line = 0
        target_column = 0
        
        # Satır ve sütun bul
        for line_num, line in enumerate(lines):
            if char_count + len(line) >= position:
                target_line = line_num
                target_column = position - char_count
                break
            char_count += len(line) + 1  # +1 for newline
        
        if target_line >= len(lines):
            return None
        
        line = lines[target_line]
        
        # Kelimeyi bul
        word = self._extract_word_at_position(line, target_column)
        
        if not word:
            return None
        
        # Kelime türünü belirle
        kind = self._determine_word_kind(word, code)
        
        # İçeriği oluştur
        documentation = self._get_documentation(word, code)
        type_info = self._get_type_info(word, code)
        definition = self._get_definition(word, code)
        
        return HoverContent(
            text=word,
            kind=kind,
            documentation=documentation,
            type_info=type_info,
            definition=definition
        )
    
    def _get_generic_hover(self, code: str, position: int) -> Optional[HoverContent]:
        """Genel hover bilgisini al."""
        lines = code.splitlines()
        char_count = 0
        target_line = 0
        target_column = 0
        
        for line_num, line in enumerate(lines):
            if char_count + len(line) >= position:
                target_line = line_num
                target_column = position - char_count
                break
            char_count += len(line) + 1
        
        if target_line >= len(lines):
            return None
        
        line = lines[target_line]
        word = self._extract_word_at_position(line, target_column)
        
        if not word:
            return None
        
        return HoverContent(
            text=word,
            kind=HoverKind.VARIABLE,
            documentation=f"Hover information for: {word}"
        )
    
    def _extract_word_at_position(self, line: str, column: int) -> Optional[str]:
        """Pozisyondaki kelimeyi çıkar."""
        if column >= len(line):
            return None
        
        # Kelime başlangıcını bul
        start = column
        while start > 0 and (line[start - 1].isalnum() or line[start - 1] == '_'):
            start -= 1
        
        # Kelime bitişini bul
        end = column
        while end < len(line) and (line[end].isalnum() or line[end] == '_'):
            end += 1
        
        if start < end:
            return line[start:end]
        
        return None
    
    def _determine_word_kind(self, word: str, code: str) -> HoverKind:
        """Kelime türünü belirle."""
        # Python keywords
        keywords = ['def', 'class', 'if', 'else', 'elif', 'for', 'while', 'try', 'except', 'import', 'from', 'return', 'yield', 'with', 'as', 'pass', 'break', 'continue', 'raise', 'finally']
        if word in keywords:
            return HoverKind.KEYWORD
        
        # Built-in functions
        builtins = ['print', 'len', 'range', 'str', 'int', 'float', 'list', 'dict', 'set', 'tuple', 'bool', 'open', 'type', 'isinstance']
        if word in builtins:
            return HoverKind.FUNCTION
        
        # Try to parse and check
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and node.name == word:
                    return HoverKind.FUNCTION
                elif isinstance(node, ast.ClassDef) and node.name == word:
                    return HoverKind.CLASS
                elif isinstance(node, ast.Name) and node.id == word:
                    if isinstance(node.ctx, ast.Load):
                        return HoverKind.VARIABLE
        except:
            pass
        
        return HoverKind.VARIABLE
    
    def _get_documentation(self, word: str, code: str) -> Optional[str]:
        """Dokümantasyon al."""
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.ClassDef)) and node.name == word:
                    docstring = ast.get_docstring(node)
                    if docstring:
                        return docstring
        except:
            pass
        
        return None
    
    def _get_type_info(self, word: str, code: str) -> Optional[str]:
        """Tip bilgisini al."""
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and node.name == word:
                    args = [arg.arg for arg in node.args.args]
                    returns = ast.unparse(node.returns) if node.returns else "None"
                    return f"def {word}({', '.join(args)}) -> {returns}"
                elif isinstance(node, ast.ClassDef) and node.name == word:
                    return f"class {word}"
        except:
            pass
        
        return None
    
    def _get_definition(self, word: str, code: str) -> Optional[str]:
        """Definition al."""
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.ClassDef)) and node.name == word:
                    if isinstance(node, ast.FunctionDef):
                        args = [arg.arg for arg in node.args.args]
                        return f"def {word}({', '.join(args)})"
                    else:
                        return f"class {word}"
        except:
            pass
        
        return None
    
    def get_hover_for_symbol(
        self,
        symbol: str,
        symbol_type: HoverKind,
        documentation: Optional[str] = None,
        type_info: Optional[str] = None
    ) -> HoverContent:
        """
        Symbol için hover oluştur.
        
        Args:
            symbol: Symbol adı
            symbol_type: Symbol tipi
            documentation: Dokümantasyon
            type_info: Tip bilgisi
            
        Returns:
            HoverContent: Hover içeriği
        """
        return HoverContent(
            text=symbol,
            kind=symbol_type,
            documentation=documentation,
            type_info=type_info
        )


if __name__ == "__main__":
    # Basit test
    engine = HoverInformationEngine()
    
    code = """
def my_function(x, y):
    \"\"\"This is a docstring.\"\"\"
    return x + y

result = my_function(1, 2)
"""
    
    # my_function üzerinde hover
    position = code.find("my_function")
    result = engine.get_hover_info(code, position, "python")
    
    print(f"Hover: {result.success}")
    if result.content:
        print(f"Text: {result.content.text}")
        print(f"Kind: {result.content.kind.value}")
        print(f"Documentation: {result.content.documentation}")
        print(f"Type info: {result.content.type_info}")
