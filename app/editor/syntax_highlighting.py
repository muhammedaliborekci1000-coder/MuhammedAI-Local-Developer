"""
MuhammedAI Local Developer - Syntax Highlighting
Syntax highlighting engine for code editor.
"""

import ast
import re
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from enum import Enum


class TokenType(Enum):
    """Token type."""
    KEYWORD = "keyword"
    STRING = "string"
    COMMENT = "comment"
    FUNCTION = "function"
    CLASS = "class"
    VARIABLE = "variable"
    OPERATOR = "operator"
    NUMBER = "number"
    DECORATOR = "decorator"
    BUILTIN = "builtin"
    PARAMETER = "parameter"
    ATTRIBUTE = "attribute"
    CONSTANT = "constant"
    CONTROL_FLOW = "control_flow"
    EXCEPTION = "exception"
    IMPORT = "import"
    TYPE = "type"


class Theme(Enum):
    """Color theme."""
    MONOKAI = "monokai"
    DRACULA = "dracula"
    GITHUB_LIGHT = "github_light"
    GITHUB_DARK = "github_dark"
    VS_CODE_DARK = "vs_code_dark"
    SOLARIZED_DARK = "solarized_dark"
    SOLARIZED_LIGHT = "solarized_light"


@dataclass
class Token:
    """Token."""
    text: str
    type: TokenType
    start: int
    end: int
    line: int
    column: int


@dataclass
class HighlightedLine:
    """Highlighted line."""
    line_number: int
    tokens: List[Token] = field(default_factory=list)
    html: Optional[str] = None


@dataclass
class SyntaxHighlightingResult:
    """Syntax highlighting result."""
    success: bool
    lines: List[HighlightedLine] = field(default_factory=list)
    html: Optional[str] = None
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    message: Optional[str] = None


class SyntaxHighlighter:
    """
    Syntax highlighting engine.
    
    Özellikler:
    - Python syntax highlighting
    - AST-based parsing
    - Multiple token types
    - Color themes
    - HTML output
    - Line-by-line highlighting
    - Multi-language support
    """
    
    def __init__(self, theme: Theme = Theme.VS_CODE_DARK):
        """
        Args:
            theme: Color theme
        """
        self.theme = theme
        self.color_map = self._get_color_map(theme)
        self.python_keywords = {
            'False', 'None', 'True', 'and', 'as', 'assert', 'async', 
            'await', 'break', 'class', 'continue', 'def', 'del', 'elif', 
            'else', 'except', 'finally', 'for', 'from', 'global', 'if', 
            'import', 'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 
            'raise', 'return', 'try', 'while', 'with', 'yield'
        }
        self.python_builtins = {
            'abs', 'all', 'any', 'bin', 'bool', 'bytearray', 'bytes', 
            'callable', 'chr', 'classmethod', 'compile', 'complex', 'delattr', 
            'dict', 'dir', 'divmod', 'enumerate', 'eval', 'exec', 'filter', 
            'float', 'format', 'frozenset', 'getattr', 'globals', 'hasattr', 
            'hash', 'help', 'hex', 'id', 'input', 'int', 'isinstance', 
            'issubclass', 'iter', 'len', 'list', 'locals', 'map', 'max', 
            'memoryview', 'min', 'next', 'object', 'oct', 'open', 'ord', 
            'pow', 'print', 'property', 'range', 'repr', 'reversed', 'round', 
            'set', 'setattr', 'slice', 'sorted', 'staticmethod', 'str', 
            'sum', 'super', 'tuple', 'type', 'vars', 'zip'
        }
        self.python_exceptions = {
            'ArithmeticError', 'AssertionError', 'AttributeError', 'BaseException',
            'BlockingIOError', 'BrokenPipeError', 'BufferError', 'BytesWarning',
            'ChildProcessError', 'ConnectionAbortedError', 'ConnectionError',
            'ConnectionRefusedError', 'ConnectionResetError', 'DeprecationWarning',
            'EOFError', 'Ellipsis', 'EnvironmentError', 'Exception', 'False',
            'FileExistsError', 'FileNotFoundError', 'FloatingPointError',
            'FutureWarning', 'GeneratorExit', 'IOError', 'ImportError',
            'ImportWarning', 'IndentationError', 'IndexError', 'InterruptedError',
            'IsADirectoryError', 'KeyError', 'KeyboardInterrupt', 'LookupError',
            'MemoryError', 'ModuleNotFoundError', 'NameError', 'NotADirectoryError',
            'NotImplemented', 'NotImplementedError', 'OSError', 'OverflowError',
            'PendingDeprecationWarning', 'PermissionError', 'ProcessLookupError',
            'RecursionError', 'ReferenceError', 'ResourceWarning', 'RuntimeError',
            'RuntimeWarning', 'StopAsyncIteration', 'StopIteration', 'SyntaxError',
            'SyntaxWarning', 'SystemError', 'SystemExit', 'TabError', 'TimeoutError',
            'True', 'TypeError', 'UnboundLocalError', 'UnicodeDecodeError',
            'UnicodeEncodeError', 'UnicodeError', 'UnicodeTranslateError',
            'UnicodeWarning', 'UserWarning', 'ValueError', 'Warning', 'ZeroDivisionError'
        }
    
    def highlight(
        self,
        code: str,
        language: str = "python"
    ) -> SyntaxHighlightingResult:
        """
        Kodu highlight et.
        
        Args:
            code: Kod içeriği
            language: Programlama dili
            
        Returns:
            SyntaxHighlightingResult: Highlighting sonucu
        """
        result = SyntaxHighlightingResult(success=False)
        
        try:
            lines = code.splitlines()
            highlighted_lines = []
            
            if language == "python":
                highlighted_lines = self._highlight_python(code, lines)
            else:
                # Basit regex-based highlighting için diğer diller
                highlighted_lines = self._highlight_generic(code, lines)
            
            result.lines = highlighted_lines
            result.html = self._generate_html(highlighted_lines)
            result.success = True
            result.message = f"Highlighted {len(highlighted_lines)} lines"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def _highlight_python(
        self,
        code: str,
        lines: List[str]
    ) -> List[HighlightedLine]:
        """Python kodunu highlight et."""
        highlighted_lines = []
        
        try:
            # AST parse
            tree = ast.parse(code)
            
            # Token bilgilerini topla
            token_info = self._collect_python_tokens(tree, lines)
            
            # Her satır için highlight et
            for i, line in enumerate(lines):
                line_num = i + 1
                tokens = self._tokenize_line(line, line_num, token_info)
                
                highlighted_line = HighlightedLine(
                    line_number=line_num,
                    tokens=tokens
                )
                highlighted_lines.append(highlighted_line)
        
        except SyntaxError:
            # Syntax error varsa basit tokenization kullan
            for i, line in enumerate(lines):
                line_num = i + 1
                tokens = self._tokenize_line_simple(line, line_num)
                
                highlighted_line = HighlightedLine(
                    line_number=line_num,
                    tokens=tokens
                )
                highlighted_lines.append(highlighted_line)
        
        return highlighted_lines
    
    def _highlight_generic(
        self,
        code: str,
        lines: List[str]
    ) -> List[HighlightedLine]:
        """Genel kod highlight et."""
        highlighted_lines = []
        
        for i, line in enumerate(lines):
            line_num = i + 1
            tokens = self._tokenize_line_simple(line, line_num)
            
            highlighted_line = HighlightedLine(
                line_number=line_num,
                tokens=tokens
            )
            highlighted_lines.append(highlighted_line)
        
        return highlighted_lines
    
    def _collect_python_tokens(
        self,
        tree: ast.AST,
        lines: List[str]
    ) -> Dict[Tuple[int, int], Tuple[TokenType, str]]:
        """Python token bilgilerini topla."""
        token_info = {}
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                token_info[(node.lineno, node.col_offset)] = (TokenType.FUNCTION, node.name)
            elif isinstance(node, ast.ClassDef):
                token_info[(node.lineno, node.col_offset)] = (TokenType.CLASS, node.name)
            elif isinstance(node, ast.Name):
                if isinstance(node.ctx, ast.Store):
                    if node.id in self.python_keywords:
                        token_info[(node.lineno, node.col_offset)] = (TokenType.KEYWORD, node.id)
                    elif node.id in self.python_builtins:
                        token_info[(node.lineno, node.col_offset)] = (TokenType.BUILTIN, node.id)
                    elif node.id in self.python_exceptions:
                        token_info[(node.lineno, node.col_offset)] = (TokenType.EXCEPTION, node.id)
        
        return token_info
    
    def _tokenize_line(
        self,
        line: str,
        line_num: int,
        token_info: Dict[Tuple[int, int], Tuple[TokenType, str]]
    ) -> List[Token]:
        """Satırı tokenize et (AST bilgisi ile)."""
        tokens = []
        i = 0
        
        while i < len(line):
            # Comment
            if line[i] == '#':
                comment_text = line[i:].rstrip()
                tokens.append(Token(
                    text=comment_text,
                    type=TokenType.COMMENT,
                    start=i,
                    end=i + len(comment_text),
                    line=line_num,
                    column=i
                ))
                break
            
            # String
            if line[i] in ['"', "'"]:
                quote_char = line[i]
                string_start = i
                i += 1
                string_content = quote_char
                
                while i < len(line):
                    string_content += line[i]
                    if line[i] == quote_char:
                        # Escape kontrolü
                        if i > 0 and line[i-1] == '\\':
                            i += 1
                            continue
                        break
                    i += 1
                
                tokens.append(Token(
                    text=string_content,
                    type=TokenType.STRING,
                    start=string_start,
                    end=i + 1,
                    line=line_num,
                    column=string_start
                ))
                i += 1
                continue
            
            # Decorator
            if line[i] == '@':
                decorator_text = line[i:].split()[0]
                tokens.append(Token(
                    text=decorator_text,
                    type=TokenType.DECORATOR,
                    start=i,
                    end=i + len(decorator_text),
                    line=line_num,
                    column=i
                ))
                i += len(decorator_text)
                continue
            
            # Keyword veya identifier
            if line[i].isalpha() or line[i] == '_':
                word_start = i
                while i < len(line) and (line[i].isalnum() or line[i] == '_'):
                    i += 1
                word = line[word_start:i]
                
                # Token tipi belirle
                token_type = self._get_token_type(word)
                
                tokens.append(Token(
                    text=word,
                    type=token_type,
                    start=word_start,
                    end=i,
                    line=line_num,
                    column=word_start
                ))
                continue
            
            # Number
            if line[i].isdigit():
                num_start = i
                while i < len(line) and (line[i].isdigit() or line[i] == '.'):
                    i += 1
                num = line[num_start:i]
                
                tokens.append(Token(
                    text=num,
                    type=TokenType.NUMBER,
                    start=num_start,
                    end=i,
                    line=line_num,
                    column=num_start
                ))
                continue
            
            # Operator
            if line[i] in '+-*/%=<>!&|^~':
                op_start = i
                while i < len(line) and line[i] in '+-*/%=<>!&|^~':
                    i += 1
                op = line[op_start:i]
                
                tokens.append(Token(
                    text=op,
                    type=TokenType.OPERATOR,
                    start=op_start,
                    end=i,
                    line=line_num,
                    column=op_start
                ))
                continue
            
            # Diğer karakterler
            i += 1
        
        return tokens
    
    def _tokenize_line_simple(
        self,
        line: str,
        line_num: int
    ) -> List[Token]:
        """Basit satır tokenization."""
        tokens = []
        i = 0
        
        while i < len(line):
            # Comment
            if line[i] == '#':
                comment_text = line[i:].rstrip()
                tokens.append(Token(
                    text=comment_text,
                    type=TokenType.COMMENT,
                    start=i,
                    end=i + len(comment_text),
                    line=line_num,
                    column=i
                ))
                break
            
            # String
            if line[i] in ['"', "'"]:
                quote_char = line[i]
                string_start = i
                i += 1
                string_content = quote_char
                
                while i < len(line):
                    string_content += line[i]
                    if line[i] == quote_char:
                        if i > 0 and line[i-1] == '\\':
                            i += 1
                            continue
                        break
                    i += 1
                
                tokens.append(Token(
                    text=string_content,
                    type=TokenType.STRING,
                    start=string_start,
                    end=i + 1,
                    line=line_num,
                    column=string_start
                ))
                i += 1
                continue
            
            # Word
            if line[i].isalpha() or line[i] == '_':
                word_start = i
                while i < len(line) and (line[i].isalnum() or line[i] == '_'):
                    i += 1
                word = line[word_start:i]
                
                token_type = self._get_token_type(word)
                
                tokens.append(Token(
                    text=word,
                    type=token_type,
                    start=word_start,
                    end=i,
                    line=line_num,
                    column=word_start
                ))
                continue
            
            # Number
            if line[i].isdigit():
                num_start = i
                while i < len(line) and (line[i].isdigit() or line[i] == '.'):
                    i += 1
                num = line[num_start:i]
                
                tokens.append(Token(
                    text=num,
                    type=TokenType.NUMBER,
                    start=num_start,
                    end=i,
                    line=line_num,
                    column=num_start
                ))
                continue
            
            # Operator
            if line[i] in '+-*/%=<>!&|^~':
                op_start = i
                while i < len(line) and line[i] in '+-*/%=<>!&|^~':
                    i += 1
                op = line[op_start:i]
                
                tokens.append(Token(
                    text=op,
                    type=TokenType.OPERATOR,
                    start=op_start,
                    end=i,
                    line=line_num,
                    column=op_start
                ))
                continue
            
            i += 1
        
        return tokens
    
    def _get_token_type(self, word: str) -> TokenType:
        """Token tipi belirle."""
        if word in self.python_keywords:
            return TokenType.KEYWORD
        elif word in self.python_builtins:
            return TokenType.BUILTIN
        elif word in self.python_exceptions:
            return TokenType.EXCEPTION
        elif word in ['def', 'class', 'import', 'from']:
            return TokenType.KEYWORD
        else:
            return TokenType.VARIABLE
    
    def _generate_html(
        self,
        highlighted_lines: List[HighlightedLine]
    ) -> str:
        """HTML output oluştur."""
        html_lines = []
        
        for line in highlighted_lines:
            line_html = ""
            for token in line.tokens:
                color = self.color_map.get(token.type, "#ffffff")
                line_html += f'<span style="color: {color};">{self._escape_html(token.text.replace(" ", "&nbsp;"))}</span>'
            
            html_lines.append(f'<div class="line" data-line="{line.line_number}">{line_html}</div>')
        
        return '<div class="code">' + '\n'.join(html_lines) + '</div>'
    
    def _escape_html(self, text: str) -> str:
        """HTML escape."""
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')
        return text
    
    def _get_color_map(self, theme: Theme) -> Dict[TokenType, str]:
        """Tema bazlı renk haritası."""
        color_maps = {
            Theme.VS_CODE_DARK: {
                TokenType.KEYWORD: "#569cd6",
                TokenType.STRING: "#ce9178",
                TokenType.COMMENT: "#6a9955",
                TokenType.FUNCTION: "#dcdcaa",
                TokenType.CLASS: "#4ec9b0",
                TokenType.VARIABLE: "#9cdcfe",
                TokenType.OPERATOR: "#d4d4d4",
                TokenType.NUMBER: "#b5cea8",
                TokenType.DECORATOR: "#c586c0",
                TokenType.BUILTIN: "#dcdcaa",
                TokenType.PARAMETER: "#9cdcfe",
                TokenType.ATTRIBUTE: "#9cdcfe",
                TokenType.CONSTANT: "#4fc1ff",
                TokenType.CONTROL_FLOW: "#c586c0",
                TokenType.EXCEPTION: "#f48771",
                TokenType.IMPORT: "#c586c0",
                TokenType.TYPE: "#4ec9b0"
            },
            Theme.MONOKAI: {
                TokenType.KEYWORD: "#f92672",
                TokenType.STRING: "#e6db74",
                TokenType.COMMENT: "#75715e",
                TokenType.FUNCTION: "#a6e22e",
                TokenType.CLASS: "#66d9ef",
                TokenType.VARIABLE: "#f8f8f2",
                TokenType.OPERATOR: "#f92672",
                TokenType.NUMBER: "#ae81ff",
                TokenType.DECORATOR: "#fd971f",
                TokenType.BUILTIN: "#66d9ef",
                TokenType.PARAMETER: "#fd971f",
                TokenType.ATTRIBUTE: "#a6e22e",
                TokenType.CONSTANT: "#ae81ff",
                TokenType.CONTROL_FLOW: "#f92672",
                TokenType.EXCEPTION: "#f92672",
                TokenType.IMPORT: "#f92672",
                TokenType.TYPE: "#66d9ef"
            },
            Theme.DRACULA: {
                TokenType.KEYWORD: "#ff79c6",
                TokenType.STRING: "#f1fa8c",
                TokenType.COMMENT: "#6272a4",
                TokenType.FUNCTION: "#50fa7b",
                TokenType.CLASS: "#8be9fd",
                TokenType.VARIABLE: "#f8f8f2",
                TokenType.OPERATOR: "#ff79c6",
                TokenType.NUMBER: "#bd93f9",
                TokenType.DECORATOR: "#ffb86c",
                TokenType.BUILTIN: "#8be9fd",
                TokenType.PARAMETER: "#ffb86c",
                TokenType.ATTRIBUTE: "#50fa7b",
                TokenType.CONSTANT: "#bd93f9",
                TokenType.CONTROL_FLOW: "#ff79c6",
                TokenType.EXCEPTION: "#ff79c6",
                TokenType.IMPORT: "#ff79c6",
                TokenType.TYPE: "#8be9fd"
            },
            Theme.GITHUB_LIGHT: {
                TokenType.KEYWORD: "#d73a49",
                TokenType.STRING: "#032f62",
                TokenType.COMMENT: "#6a737d",
                TokenType.FUNCTION: "#6f42c1",
                TokenType.CLASS: "#e36209",
                TokenType.VARIABLE: "#24292e",
                TokenType.OPERATOR: "#d73a49",
                TokenType.NUMBER: "#005cc5",
                TokenType.DECORATOR: "#6f42c1",
                TokenType.BUILTIN: "#005cc5",
                TokenType.PARAMETER: "#e36209",
                TokenType.ATTRIBUTE: "#6f42c1",
                TokenType.CONSTANT: "#005cc5",
                TokenType.CONTROL_FLOW: "#d73a49",
                TokenType.EXCEPTION: "#d73a49",
                TokenType.IMPORT: "#d73a49",
                TokenType.TYPE: "#e36209"
            },
            Theme.GITHUB_DARK: {
                TokenType.KEYWORD: "#ff7b72",
                TokenType.STRING: "#a5d6ff",
                TokenType.COMMENT: "#8b949e",
                TokenType.FUNCTION: "#d2a8ff",
                TokenType.CLASS: "#ffa657",
                TokenType.VARIABLE: "#c9d1d9",
                TokenType.OPERATOR: "#ff7b72",
                TokenType.NUMBER: "#79c0ff",
                TokenType.DECORATOR: "#d2a8ff",
                TokenType.BUILTIN: "#79c0ff",
                TokenType.PARAMETER: "#ffa657",
                TokenType.ATTRIBUTE: "#d2a8ff",
                TokenType.CONSTANT: "#79c0ff",
                TokenType.CONTROL_FLOW: "#ff7b72",
                TokenType.EXCEPTION: "#ff7b72",
                TokenType.IMPORT: "#ff7b72",
                TokenType.TYPE: "#ffa657"
            },
            Theme.SOLARIZED_DARK: {
                TokenType.KEYWORD: "#859900",
                TokenType.STRING: "#2aa198",
                TokenType.COMMENT: "#93a1a1",
                TokenType.FUNCTION: "#268bd2",
                TokenType.CLASS: "#b58900",
                TokenType.VARIABLE: "#839496",
                TokenType.OPERATOR: "#859900",
                TokenType.NUMBER: "#d33682",
                TokenType.DECORATOR: "#cb4b16",
                TokenType.BUILTIN: "#268bd2",
                TokenType.PARAMETER: "#cb4b16",
                TokenType.ATTRIBUTE: "#2aa198",
                TokenType.CONSTANT: "#d33682",
                TokenType.CONTROL_FLOW: "#859900",
                TokenType.EXCEPTION: "#dc322f",
                TokenType.IMPORT: "#cb4b16",
                TokenType.TYPE: "#b58900"
            },
            Theme.SOLARIZED_LIGHT: {
                TokenType.KEYWORD: "#586e75",
                TokenType.STRING: "#2aa1988",
                TokenType.COMMENT: "#93a1a1",
                TokenType.FUNCTION: "#268bd2",
                TokenType.CLASS: "#b58900",
                TokenType.VARIABLE: "#657b83",
                TokenType.OPERATOR: "#586e75",
                TokenType.NUMBER: "#d33682",
                TokenType.DECORATOR: "#cb4b16",
                TokenType.BUILTIN: "#268bd2",
                TokenType.PARAMETER: "#cb4b16",
                TokenType.ATTRIBUTE: "#2aa198",
                TokenType.CONSTANT: "#d33682",
                TokenType.CONTROL_FLOW: "#586e75",
                TokenType.EXCEPTION: "#dc322f",
                TokenType.IMPORT: "#cb4b16",
                TokenType.TYPE: "#b58900"
            }
        }
        
        return color_maps.get(theme, color_maps[Theme.VS_CODE_DARK])


if __name__ == "__main__":
    # Basit test
    highlighter = SyntaxHighlighter()
    
    code = """
def my_function(x, y):
    # This is a comment
    result = x + y
    return result
"""
    
    result = highlighter.highlight(code, language="python")
    print(f"Highlighting: {result.success}")
    print(f"Lines: {len(result.lines)}")
    print(f"HTML length: {len(result.html) if result.html else 0}")
