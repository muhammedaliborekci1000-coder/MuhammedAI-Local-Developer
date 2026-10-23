"""
MuhammedAI Local Developer - Auto Completion
Auto completion engine for code editor.
"""

import ast
import re
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from enum import Enum


class CompletionType(Enum):
    """Completion type."""
    KEYWORD = "keyword"
    BUILTIN = "builtin"
    VARIABLE = "variable"
    FUNCTION = "function"
    CLASS = "class"
    METHOD = "method"
    ATTRIBUTE = "attribute"
    IMPORT = "import"
    SNIPPET = "snippet"
    PATH = "path"
    FILE = "file"


class CompletionContext(Enum):
    """Completion context."""
    TOP_LEVEL = "top_level"
    FUNCTION_BODY = "function_body"
    CLASS_BODY = "class_body"
    IMPORT_STATEMENT = "import_statement"
    ATTRIBUTE_ACCESS = "attribute_access"
    FUNCTION_CALL = "function_call"


@dataclass
class CompletionItem:
    """Completion item."""
    label: str
    type: CompletionType
    detail: Optional[str] = None
    documentation: Optional[str] = None
    insert_text: Optional[str] = None
    sort_text: Optional[str] = None
    filter_text: Optional[str] = None
    score: float = 0.0


@dataclass
class AutoCompletionResult:
    """Auto completion result."""
    success: bool
    items: List[CompletionItem] = field(default_factory=list)
    context: Optional[CompletionContext] = None
    file_path: Optional[str] = None
    line: Optional[int] = None
    column: Optional[int] = None
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    message: Optional[str] = None


class AutoCompleter:
    """
    Auto completion engine.
    
    Özellikler:
    - Python keywords completion
    - Built-in functions completion
    - Local variables completion
    - Function/method completion
    - Class completion
    - Import completion
    - Snippet completion
    - Context-aware suggestions
    - Scoring and ranking
    - Multi-language support
    """
    
    def __init__(self, project_root: Optional[str] = None):
        """
        Args:
            project_root: Project root directory
        """
        self.project_root = project_root
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
        self.snippets = {
            'def': 'def ${1:function_name}(${2:args}):\n    ${3:pass}',
            'class': 'class ${1:ClassName}:\n    def __init__(self):\n        ${2:pass}',
            'if': 'if ${1:condition}:\n    ${2:pass}',
            'for': 'for ${1:item} in ${2:iterable}:\n    ${3:pass}',
            'while': 'while ${1:condition}:\n    ${2:pass}',
            'try': 'try:\n    ${1:pass}\nexcept ${2:Exception} as e:\n    ${3:pass}',
            'with': 'with ${1:context} as ${2:variable}:\n    ${3:pass}',
            'main': 'if __name__ == "__main__":\n    ${1:pass}'
        }
        self._build_index()
    
    def complete(
        self,
        file_path: str,
        line: int,
        column: int,
        prefix: str = ""
    ) -> AutoCompletionResult:
        """
        Auto completion.
        
        Args:
            file_path: Dosya yolu
            line: Satır numarası
            column: Sütun numarası
            prefix: Prefix
            
        Returns:
            AutoCompletionResult: Completion sonucu
        """
        result = AutoCompletionResult(success=False)
        result.file_path = file_path
        result.line = line
        result.column = column
        
        try:
            # Dosyayı oku
            content = Path(file_path).read_text(encoding='utf-8')
            lines = content.splitlines()
            
            # Context belirle
            context = self._determine_context(lines, line, column)
            result.context = context
            
            # Completion önerilerini topla
            items = []
            
            # Keywords
            if context in [CompletionContext.TOP_LEVEL, CompletionContext.FUNCTION_BODY, CompletionContext.CLASS_BODY]:
                items.extend(self._get_keyword_completions(prefix))
            
            # Built-ins
            if context in [CompletionContext.TOP_LEVEL, CompletionContext.FUNCTION_BODY]:
                items.extend(self._get_builtin_completions(prefix))
            
            # Local variables
            items.extend(self._get_local_variable_completions(content, line, prefix))
            
            # Functions ve classes
            items.extend(self._get_function_class_completions(content, prefix))
            
            # Snippets
            if context == CompletionContext.TOP_LEVEL:
                items.extend(self._get_snippet_completions(prefix))
            
            # Import
            if context == CompletionContext.IMPORT_STATEMENT:
                items.extend(self._get_import_completions(prefix))
            
            # Score ve sırala
            items = self._score_and_sort(items, prefix)
            
            result.items = items[:20]  # Max 20 öneri
            result.success = True
            result.message = f"Found {len(result.items)} completions"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def _build_index(self):
        """Index oluştur."""
        self.function_index = {}
        self.class_index = {}
        
        if not self.project_root:
            return
        
        for file_path in Path(self.project_root).rglob("*.py"):
            try:
                content = file_path.read_text(encoding='utf-8')
                tree = ast.parse(content)
                
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        self.function_index[node.name] = str(file_path)
                    elif isinstance(node, ast.ClassDef):
                        self.class_index[node.name] = str(file_path)
            
            except Exception:
                pass
    
    def _determine_context(
        self,
        lines: List[str],
        line: int,
        column: int
    ) -> CompletionContext:
        """Context belirle."""
        if line < 1 or line > len(lines):
            return CompletionContext.TOP_LEVEL
        
        line_content = lines[line - 1]
        
        # Import statement
        if "import" in line_content or "from" in line_content:
            return CompletionContext.IMPORT_STATEMENT
        
        # Attribute access
        if "." in line_content[:column]:
            return CompletionContext.ATTRIBUTE_ACCESS
        
        # Function call
        if "(" in line_content[:column]:
            return CompletionContext.FUNCTION_CALL
        
        # Class body
        # Basit kontrol - indentation ile
        if line > 1:
            prev_line = lines[line - 2]
            if prev_line.strip().startswith("class "):
                return CompletionContext.CLASS_BODY
        
        # Function body
        if line > 1:
            prev_line = lines[line - 2]
            if prev_line.strip().startswith("def "):
                return CompletionContext.FUNCTION_BODY
        
        return CompletionContext.TOP_LEVEL
    
    def _get_keyword_completions(self, prefix: str) -> List[CompletionItem]:
        """Keyword completion."""
        items = []
        prefix_lower = prefix.lower()
        
        for keyword in self.python_keywords:
            if keyword.lower().startswith(prefix_lower):
                items.append(CompletionItem(
                    label=keyword,
                    type=CompletionType.KEYWORD,
                    detail="Python keyword",
                    score=1.0
                ))
        
        return items
    
    def _get_builtin_completions(self, prefix: str) -> List[CompletionItem]:
        """Built-in completion."""
        items = []
        prefix_lower = prefix.lower()
        
        for builtin in self.python_builtins:
            if builtin.lower().startswith(prefix_lower):
                items.append(CompletionItem(
                    label=builtin,
                    type=CompletionType.BUILTIN,
                    detail="Built-in function",
                    score=0.9
                ))
        
        return items
    
    def _get_local_variable_completions(
        self,
        content: str,
        line: int,
        prefix: str
    ) -> List[CompletionItem]:
        """Local variable completion."""
        items = []
        prefix_lower = prefix.lower()
        
        try:
            tree = ast.parse(content)
            local_vars = set()
            
            # Satıra kadar olan değişkenleri topla
            for node in ast.walk(tree):
                if hasattr(node, 'lineno') and node.lineno <= line:
                    if isinstance(node, ast.Assign):
                        for target in node.targets:
                            if isinstance(target, ast.Name):
                                local_vars.add(target.id)
                    elif isinstance(node, ast.FunctionDef):
                        for arg in node.args.args:
                            local_vars.add(arg.arg)
            
            for var in local_vars:
                if var.lower().startswith(prefix_lower):
                    items.append(CompletionItem(
                        label=var,
                        type=CompletionType.VARIABLE,
                        detail="Local variable",
                        score=0.8
                    ))
        
        except Exception:
            pass
        
        return items
    
    def _get_function_class_completions(
        self,
        content: str,
        prefix: str
    ) -> List[CompletionItem]:
        """Function ve class completion."""
        items = []
        prefix_lower = prefix.lower()
        
        # Index'ten
        for func_name in self.function_index:
            if func_name.lower().startswith(prefix_lower):
                items.append(CompletionItem(
                    label=func_name,
                    type=CompletionType.FUNCTION,
                    detail=f"Function in {self.function_index[func_name]}",
                    score=0.7
                ))
        
        for class_name in self.class_index:
            if class_name.lower().startswith(prefix_lower):
                items.append(CompletionItem(
                    label=class_name,
                    type=CompletionType.CLASS,
                    detail=f"Class in {self.class_index[class_name]}",
                    score=0.7
                ))
        
        return items
    
    def _get_snippet_completions(self, prefix: str) -> List[CompletionItem]:
        """Snippet completion."""
        items = []
        prefix_lower = prefix.lower()
        
        for snippet_name, snippet_code in self.snippets.items():
            if snippet_name.lower().startswith(prefix_lower):
                items.append(CompletionItem(
                    label=snippet_name,
                    type=CompletionType.SNIPPET,
                    detail="Code snippet",
                    insert_text=snippet_code,
                    score=0.6
                ))
        
        return items
    
    def _get_import_completions(self, prefix: str) -> List[CompletionItem]:
        """Import completion."""
        items = []
        prefix_lower = prefix.lower()
        
        # Standart library modules
        stdlib_modules = [
            'os', 'sys', 're', 'json', 'pathlib', 'datetime',
            'collections', 'itertools', 'functools', 'math', 'random'
        ]
        
        for module in stdlib_modules:
            if module.lower().startswith(prefix_lower):
                items.append(CompletionItem(
                    label=module,
                    type=CompletionType.IMPORT,
                    detail="Standard library module",
                    score=0.8
                ))
        
        return items
    
    def _score_and_sort(
        self,
        items: List[CompletionItem],
        prefix: str
    ) -> List[CompletionItem]:
        """Score ve sırala."""
        prefix_lower = prefix.lower()
        
        for item in items:
            # Prefix match bonus
            if item.label.lower().startswith(prefix_lower):
                item.score += 0.5
            
            # Exact match bonus
            if item.label.lower() == prefix_lower:
                item.score += 1.0
        
        # Score'a göre sırala
        items.sort(key=lambda x: x.score, reverse=True)
        
        return items


if __name__ == "__main__":
    # Basit test
    completer = AutoCompleter()
    
    # Test için geçici dosya
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write("def my_function():\n    pass\n")
        test_file = f.name
    
    result = completer.complete(test_file, line=1, column=4, prefix="def")
    print(f"Completion: {result.success}")
    print(f"Items: {len(result.items)}")
    
    import os
    os.unlink(test_file)
