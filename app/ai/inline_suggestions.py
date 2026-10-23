"""
MuhammedAI Local Developer - Inline Suggestions
Context-aware code completion ve inline suggestions.
"""

import ast
import re
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from enum import Enum


class SuggestionType(Enum):
    """Suggestion type."""
    COMPLETION = "completion"  # Code completion
    IMPORT = "import"  # Import suggestion
    FUNCTION = "function"  # Function/method completion
    VARIABLE = "variable"  # Variable completion
    SNIPPET = "snippet"  # Code snippet
    CORRECTION = "correction"  # Code correction


class SuggestionPriority(Enum):
    """Suggestion priority."""
    HIGH = 3
    MEDIUM = 2
    LOW = 1


@dataclass
class Suggestion:
    """Tekil suggestion."""
    text: str
    type: SuggestionType
    priority: SuggestionPriority = SuggestionPriority.MEDIUM
    description: Optional[str] = None
    label: Optional[str] = None
    start_line: Optional[int] = None
    start_column: Optional[int] = None
    end_line: Optional[int] = None
    end_column: Optional[int] = None
    confidence: float = 1.0  # 0-1 arası confidence score


@dataclass
class SuggestionContext:
    """Suggestion context bilgisi."""
    file_path: str
    line: int
    column: int
    current_line: str
    lines_before: List[str] = field(default_factory=list)
    lines_after: List[str] = field(default_factory=list)
    current_function: Optional[str] = None
    current_class: Optional[str] = None
    imports: List[str] = field(default_factory=list)
    variables_in_scope: List[str] = field(default_factory=list)
    current_word: Optional[str] = None
    prefix: str = ""  # Cursor'dan önceki metin


class InlineSuggestionsEngine:
    """
    Inline suggestions engine.
    
    Özellikler:
    - Context-aware code completion
    - Multi-line suggestions
    - Function/method completion
    - Variable completion
    - Import suggestions
    - Syntax-aware suggestions
    - Priority-based suggestions
    """
    
    def __init__(self, codebase_index=None):
        """
        Args:
            codebase_index: CodebaseIndex instance (symbol completion için)
        """
        self.codebase_index = codebase_index
        self.common_imports = [
            "import os",
            "import sys",
            "import json",
            "import re",
            "from typing import List, Dict, Any, Optional",
            "from pathlib import Path",
            "from dataclasses import dataclass",
            "import datetime",
            "from enum import Enum"
        ]
        self.common_patterns = {
            "def ": ["def function_name(self, arg1, arg2):\n    pass"],
            "class ": ["class ClassName:\n    def __init__(self):\n        pass"],
            "if __": ["if __name__ == \"__main__\":\n    pass"],
            "for ": ["for item in items:\n    pass"],
            "with ": ["with open('file.txt', 'r') as f:\n    content = f.read()"],
        }
    
    def get_suggestions(
        self,
        file_path: str,
        line: int,
        column: int,
        current_line: str,
        lines_before: List[str],
        lines_after: List[str]
    ) -> List[Suggestion]:
        """
        Inline suggestions al.
        
        Args:
            file_path: Dosya yolu
            line: Satır numarası (1-indexed)
            column: Sütun numarası (0-indexed)
            current_line: Mevcut satır
            lines_before: Önceki satırlar
            lines_after: Sonraki satırlar
            
        Returns:
            List[Suggestion]: Suggestion listesi
        """
        suggestions = []
        
        # Context oluştur
        context = self._build_context(
            file_path, line, column, current_line, lines_before, lines_after
        )
        
        # Import suggestions
        import_suggestions = self._get_import_suggestions(context)
        suggestions.extend(import_suggestions)
        
        # Function/method suggestions
        function_suggestions = self._get_function_suggestions(context)
        suggestions.extend(function_suggestions)
        
        # Variable suggestions
        variable_suggestions = self._get_variable_suggestions(context)
        suggestions.extend(variable_suggestions)
        
        # Pattern-based suggestions
        pattern_suggestions = self._get_pattern_suggestions(context)
        suggestions.extend(pattern_suggestions)
        
        # Symbol-based suggestions (codebase index ile)
        if self.codebase_index:
            symbol_suggestions = self._get_symbol_suggestions(context)
            suggestions.extend(symbol_suggestions)
        
        # Priority ve confidence'e göre sırala
        suggestions = sorted(
            suggestions,
            key=lambda s: (s.priority.value, s.confidence),
            reverse=True
        )
        
        # Top 20 suggestion
        return suggestions[:20]
    
    def _build_context(
        self,
        file_path: str,
        line: int,
        column: int,
        current_line: str,
        lines_before: List[str],
        lines_after: List[str]
    ) -> SuggestionContext:
        """
        Suggestion context oluştur.
        
        Args:
            file_path: Dosya yolu
            line: Satır numarası
            column: Sütun numarası
            current_line: Mevcut satır
            lines_before: Önceki satırlar
            lines_after: Sonraki satırlar
            
        Returns:
            SuggestionContext: Context bilgisi
        """
        # Current word ve prefix
        current_word = self._get_current_word(current_line, column)
        prefix = current_line[:column]
        
        context = SuggestionContext(
            file_path=file_path,
            line=line,
            column=column,
            current_line=current_line,
            lines_before=lines_before,
            lines_after=lines_after,
            current_word=current_word,
            prefix=prefix
        )
        
        # AST ile scope detection
        try:
            all_lines = lines_before + [current_line] + lines_after
            content = "\n".join(all_lines)
            tree = ast.parse(content)
            self._detect_scope(tree, line, context)
        except SyntaxError:
            pass
        
        return context
    
    def _get_current_word(self, line: str, column: int) -> Optional[str]:
        """
        Cursor'daki current word'ü al.
        
        Args:
            line: Satır
            column: Sütun (0-indexed)
            
        Returns:
            Optional[str]: Current word
        """
        # Word boundary bul
        word_chars = []
        i = column
        while i >= 0 and i < len(line) and (line[i].isalnum() or line[i] in "_"):
            word_chars.append(line[i])
            i -= 1
        
        return "".join(reversed(word_chars)) if word_chars else None
    
    def _detect_scope(
        self,
        tree: ast.AST,
        target_line: int,
        context: SuggestionContext
    ) -> None:
        """
        AST ile scope detection.
        
        Args:
            tree: AST tree
            target_line: Hedef satır
            context: Context
        """
        class ScopeVisitor(ast.NodeVisitor):
            def __init__(self, target_line: int, context: SuggestionContext):
                self.target_line = target_line
                self.context = context
                self.current_class = None
                self.current_function = None
                self.variables = set()
                self.imports = []
            
            def visit_ClassDef(self, node: ast.ClassDef) -> None:
                if node.lineno <= self.target_line <= self._get_end_line(node):
                    self.current_class = node.name
                    self.context.current_class = node.name
                self.generic_visit(node)
            
            def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
                if node.lineno <= self.target_line <= self._get_end_line(node):
                    if self.current_class:
                        self.context.current_function = f"{self.current_class}.{node.name}"
                    else:
                        self.context.current_function = node.name
                    
                    # Function arguments
                    for arg in node.args.args:
                        self.variables.add(arg.arg)
                self.generic_visit(node)
            
            def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
                if node.lineno <= self.target_line <= self._get_end_line(node):
                    if self.current_class:
                        self.context.current_function = f"{self.current_class}.{node.name}"
                    else:
                        self.context.current_function = node.name
                    
                    for arg in node.args.args:
                        self.variables.add(arg.arg)
                self.generic_visit(node)
            
            def visit_Import(self, node: ast.Import) -> None:
                for alias in node.names:
                    self.imports.append(alias.name)
                self.generic_visit(node)
            
            def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
                module = node.module or ""
                for alias in node.names:
                    self.imports.append(f"{module}.{alias.name}")
                self.generic_visit(node)
            
            def visit_Name(self, node: ast.Name) -> None:
                if isinstance(node.ctx, ast.Store):
                    self.variables.add(node.id)
                self.generic_visit(node)
            
            def _get_end_line(self, node: ast.AST) -> int:
                if hasattr(node, 'end_lineno') and node.end_lineno:
                    return node.end_lineno
                return node.lineno
        
        visitor = ScopeVisitor(target_line, context)
        visitor.visit(tree)
        
        context.imports = visitor.imports
        context.variables_in_scope = list(visitor.variables)
    
    def _get_import_suggestions(self, context: SuggestionContext) -> List[Suggestion]:
        """
        Import suggestions al.
        
        Args:
            context: Context
            
        Returns:
            List[Suggestion]: Import suggestions
        """
        suggestions = []
        
        # "import" veya "from" ile başlıyorsa
        if context.prefix.strip().startswith("import") or context.prefix.strip().startswith("from"):
            for imp in self.common_imports:
                if imp.startswith(context.prefix.strip()):
                    suggestions.append(Suggestion(
                        text=imp,
                        type=SuggestionType.IMPORT,
                        priority=SuggestionPriority.HIGH,
                        description=f"Import: {imp}",
                        confidence=0.9
                    ))
        
        return suggestions
    
    def _get_function_suggestions(self, context: SuggestionContext) -> List[Suggestion]:
        """
        Function/method suggestions al.
        
        Args:
            context: Context
            
        Returns:
            List[Suggestion]: Function suggestions
        """
        suggestions = []
        
        # "def " ile başlıyorsa
        if context.prefix.strip().startswith("def "):
            suggestions.append(Suggestion(
                text="def function_name(self, arg1, arg2):\n    pass",
                type=SuggestionType.SNIPPET,
                priority=SuggestionPriority.HIGH,
                description="Function template",
                confidence=0.8
            ))
        
        # Class içindeyse method suggestion
        if context.current_class and context.prefix.strip().startswith("def "):
            suggestions.append(Suggestion(
                text="def method_name(self, arg1):\n    pass",
                type=SuggestionType.SNIPPET,
                priority=SuggestionPriority.HIGH,
                description="Method template",
                confidence=0.85
            ))
        
        return suggestions
    
    def _get_variable_suggestions(self, context: SuggestionContext) -> List[Suggestion]:
        """
        Variable suggestions al.
        
        Args:
            context: Context
            
        Returns:
            List[Suggestion]: Variable suggestions
        """
        suggestions = []
        
        # Scope içindeki değişkenler
        for var in context.variables_in_scope:
            if var.startswith(context.current_word or ""):
                suggestions.append(Suggestion(
                    text=var,
                    type=SuggestionType.VARIABLE,
                    priority=SuggestionPriority.MEDIUM,
                    description=f"Variable: {var}",
                    confidence=0.7
                ))
        
        return suggestions
    
    def _get_pattern_suggestions(self, context: SuggestionContext) -> List[Suggestion]:
        """
        Pattern-based suggestions al.
        
        Args:
            context: Context
            
        Returns:
            List[Suggestion]: Pattern suggestions
        """
        suggestions = []
        
        # Common patterns
        for pattern, completions in self.common_patterns.items():
            if context.prefix.strip().startswith(pattern):
                for completion in completions:
                    suggestions.append(Suggestion(
                        text=completion,
                        type=SuggestionType.SNIPPET,
                        priority=SuggestionPriority.HIGH,
                        description=f"Pattern: {pattern}",
                        confidence=0.75
                    ))
        
        return suggestions
    
    def _get_symbol_suggestions(self, context: SuggestionContext) -> List[Suggestion]:
        """
        Symbol-based suggestions (codebase index ile).
        
        Args:
            context: Context
            
        Returns:
            List[Suggestion]: Symbol suggestions
        """
        suggestions = []
        
        if not self.codebase_index or not context.current_word:
            return suggestions
        
        try:
            self.codebase_index.index_project()
            
            # Symbol ara
            symbols = self.codebase_index.search_symbols(context.current_word)
            
            for symbol in symbols[:10]:
                suggestion_text = symbol.name
                
                # Function ise parantez ekle
                if symbol.type == "function" or symbol.type == "method":
                    suggestion_text += "()"
                
                suggestions.append(Suggestion(
                    text=suggestion_text,
                    type=SuggestionType.FUNCTION if symbol.type in ["function", "method"] else SuggestionType.VARIABLE,
                    priority=SuggestionPriority.MEDIUM,
                    description=f"{symbol.type}: {symbol.name} ({symbol.file})",
                    confidence=0.6
                ))
        except Exception:
            pass
        
        return suggestions


if __name__ == "__main__":
    # Basit test
    engine = InlineSuggestionsEngine()
    
    suggestions = engine.get_suggestions(
        file_path="test.py",
        line=1,
        column=5,
        current_line="imp",
        lines_before=[],
        lines_after=[]
    )
    
    print(f"Suggestions: {len(suggestions)}")
    for suggestion in suggestions:
        print(f"  - {suggestion.text} ({suggestion.type.value})")
