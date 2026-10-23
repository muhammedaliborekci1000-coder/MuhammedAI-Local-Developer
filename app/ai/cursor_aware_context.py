"""
MuhammedAI Local Developer - Cursor-Aware Context
Cursor position ve surrounding code context extraction.
"""

import ast
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from enum import Enum


class CursorSemanticType(Enum):
    """Cursor semantic type."""
    UNKNOWN = "unknown"
    DEFINITION = "definition"  # Function/class/variable definition
    REFERENCE = "reference"  # Variable/function reference
    CALL = "call"  # Function call
    IMPORT = "import"  # Import statement
    DECORATOR = "decorator"  # Decorator
    COMMENT = "comment"  # Comment
    STRING = "string"  # String literal
    KEYWORD = "keyword"  # Python keyword
    OPERATOR = "operator"  # Operator


@dataclass
class CursorContext:
    """Cursor context bilgisi."""
    file_path: str
    line: int
    column: int
    surrounding_lines_before: List[str] = field(default_factory=list)
    surrounding_lines_after: List[str] = field(default_factory=list)
    current_function: Optional[str] = None
    current_class: Optional[str] = None
    current_scope: str = "module"  # module, class, function, method
    function_signature: Optional[str] = None
    class_signature: Optional[str] = None
    imports_in_scope: List[str] = field(default_factory=list)
    variables_in_scope: List[str] = field(default_factory=list)
    function_calls: List[str] = field(default_factory=list)  # Function call tracking
    decorators: List[str] = field(default_factory=list)  # Decorators
    docstring: Optional[str] = None  # Function/class docstring
    parent_functions: List[str] = field(default_factory=list)  # Call stack
    semantic_type: CursorSemanticType = CursorSemanticType.UNKNOWN  # Semantic type
    referenced_symbol: Optional[str] = None  # Referenced symbol name
    symbol_definition: Optional[Dict[str, Any]] = None  # Full symbol definition
    related_files: List[str] = field(default_factory=list)  # Related files


class CursorAwareContextExtractor:
    """
    Cursor-aware context extraction.
    
    Özellikler:
    - Surrounding code extraction
    - Function scope detection
    - Class scope detection
    - Import tracking
    - Variable tracking
    - Function call tracking
    - Decorator tracking
    - Docstring extraction
    - Call stack tracking
    - Semantic type detection
    - Symbol resolution
    - Multi-file context
    """
    
    def __init__(self, context_lines: int = 20, codebase_index=None):
        """
        Args:
            context_lines: Cursor etrafındaki satır sayısı (önce/sonra)
            codebase_index: CodebaseIndex instance (symbol resolution için)
        """
        self.context_lines = context_lines
        self.codebase_index = codebase_index
    
    def extract_context(
        self,
        file_path: str,
        line: int,
        column: int = 0
    ) -> Optional[CursorContext]:
        """
        Cursor context'i çıkar.
        
        Args:
            file_path: Dosya yolu
            line: Satır numarası (1-indexed)
            column: Sütun numarası (0-indexed)
            
        Returns:
            CursorContext: Cursor context bilgisi
        """
        try:
            file_path_obj = Path(file_path)
            if not file_path_obj.exists():
                return None
            
            # Dosyayı oku
            content = file_path_obj.read_text(encoding='utf-8')
            lines = content.splitlines()
            
            if line < 1 or line > len(lines):
                return None
            
            # Surrounding lines
            start_line = max(0, line - self.context_lines - 1)
            end_line = min(len(lines), line + self.context_lines)
            
            surrounding_before = lines[start_line:line - 1]
            surrounding_after = lines[line:end_line]
            
            cursor_context = CursorContext(
                file_path=file_path,
                line=line,
                column=column,
                surrounding_lines_before=surrounding_before,
                surrounding_lines_after=surrounding_after
            )
            
            # AST ile scope detection
            try:
                tree = ast.parse(content)
                self._detect_scopes(tree, line, cursor_context)
                self._detect_semantic_type(tree, line, column, cursor_context, content)
                self._resolve_symbol(cursor_context)
                self._find_related_files(cursor_context)
            except SyntaxError:
                # Syntax error varsa basit scope detection
                pass
            
            return cursor_context
            
        except Exception as e:
            return None
    
    def _detect_scopes(
        self,
        tree: ast.AST,
        target_line: int,
        context: CursorContext
    ) -> None:
        """
        AST ile function ve class scope tespiti.
        
        Args:
            tree: AST tree
            target_line: Hedef satır
            context: Cursor context
        """
        class ScopeVisitor(ast.NodeVisitor):
            def __init__(self, target_line: int, context: CursorContext):
                self.target_line = target_line
                self.context = context
                self.current_class = None
                self.current_function = None
                self.imports = []
                self.variables = set()
                self.function_calls = []
                self.decorators = []
                self.call_stack = []
            
            def visit_ClassDef(self, node: ast.ClassDef) -> None:
                # Class içinde mi?
                if node.lineno <= self.target_line <= self._get_end_line(node):
                    self.current_class = node.name
                    self.context.class_signature = self._get_class_signature(node)
                    self.context.current_class = node.name
                    self.context.current_scope = "class"
                    
                    # Class docstring
                    if ast.get_docstring(node):
                        self.context.docstring = ast.get_docstring(node)
                    
                    # Class decorators
                    for decorator in node.decorator_list:
                        self.decorators.append(self._get_decorator_name(decorator))
                
                self.generic_visit(node)
                
                # Class dışına çıkıldı
                if node.lineno <= self.target_line <= self._get_end_line(node):
                    pass  # Hala class içinde
                else:
                    self.current_class = None
            
            def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
                # Function/method içinde mi?
                if node.lineno <= self.target_line <= self._get_end_line(node):
                    self.current_function = node.name
                    self.context.function_signature = self._get_function_signature(node)
                    
                    if self.current_class:
                        self.context.current_function = f"{self.current_class}.{node.name}"
                        self.context.current_scope = "method"
                    else:
                        self.context.current_function = node.name
                        self.context.current_scope = "function"
                    
                    # Function arguments
                    for arg in node.args.args:
                        self.variables.add(arg.arg)
                    
                    # Function docstring
                    if ast.get_docstring(node):
                        self.context.docstring = ast.get_docstring(node)
                    
                    # Function decorators
                    for decorator in node.decorator_list:
                        self.decorators.append(self._get_decorator_name(decorator))
                    
                    # Add to call stack
                    self.call_stack.append(self.current_function)
                    self.context.parent_functions = list(self.call_stack)
                
                self.generic_visit(node)
                
                # Function dışına çıkıldı
                if node.lineno <= self.target_line <= self._get_end_line(node):
                    pass  # Hala function içinde
                else:
                    if self.call_stack and self.call_stack[-1] == self.current_function:
                        self.call_stack.pop()
            
            def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
                # Async function
                if node.lineno <= self.target_line <= self._get_end_line(node):
                    self.current_function = node.name
                    self.context.function_signature = f"async {self._get_function_signature(node)}"
                    
                    if self.current_class:
                        self.context.current_function = f"{self.current_class}.{node.name}"
                        self.context.current_scope = "async_method"
                    else:
                        self.context.current_function = node.name
                        self.context.current_scope = "async_function"
                    
                    # Function arguments
                    for arg in node.args.args:
                        self.variables.add(arg.arg)
                    
                    # Function docstring
                    if ast.get_docstring(node):
                        self.context.docstring = ast.get_docstring(node)
                    
                    # Function decorators
                    for decorator in node.decorator_list:
                        self.decorators.append(self._get_decorator_name(decorator))
                    
                    # Add to call stack
                    self.call_stack.append(self.current_function)
                    self.context.parent_functions = list(self.call_stack)
                
                self.generic_visit(node)
                
                # Function dışına çıkıldı
                if node.lineno <= self.target_line <= self._get_end_line(node):
                    pass  # Hala function içinde
                else:
                    if self.call_stack and self.call_stack[-1] == self.current_function:
                        self.call_stack.pop()
            
            def visit_Call(self, node: ast.Call) -> None:
                # Function call tracking
                if node.lineno <= self.target_line <= self._get_end_line(node):
                    call_name = self._get_call_name(node)
                    if call_name:
                        self.function_calls.append(call_name)
                self.generic_visit(node)
            
            def visit_Import(self, node: ast.Import) -> None:
                for alias in node.names:
                    self.imports.append(f"import {alias.name}")
                    if alias.asname:
                        self.imports[-1] += f" as {alias.asname}"
                self.generic_visit(node)
            
            def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
                module = node.module or ""
                for alias in node.names:
                    import_stmt = f"from {module} import {alias.name}"
                    if alias.asname:
                        import_stmt += f" as {alias.asname}"
                    self.imports.append(import_stmt)
                self.generic_visit(node)
            
            def visit_Name(self, node: ast.Name) -> None:
                # Variable tracking (basit)
                if isinstance(node.ctx, ast.Store):
                    self.variables.add(node.id)
                self.generic_visit(node)
            
            def _get_call_name(self, node: ast.Call) -> str:
                """Function call name'i al."""
                if isinstance(node.func, ast.Name):
                    return node.func.id
                elif isinstance(node.func, ast.Attribute):
                    return f"{self._get_attribute_name(node.func)}"
                return ""
            
            def _get_attribute_name(self, node: ast.Attribute) -> str:
                """Attribute name'i al."""
                if isinstance(node.value, ast.Name):
                    return f"{node.value.id}.{node.attr}"
                elif isinstance(node.value, ast.Attribute):
                    return f"{self._get_attribute_name(node.value)}.{node.attr}"
                return node.attr
            
            def _get_decorator_name(self, node: ast.expr) -> str:
                """Decorator name'i al."""
                if isinstance(node, ast.Name):
                    return f"@{node.id}"
                elif isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name):
                        return f"@{node.func.id}(...)"
                    elif isinstance(node.func, ast.Attribute):
                        return f"@{self._get_attribute_name(node.func)}(...)"
                elif isinstance(node, ast.Attribute):
                    return f"@{self._get_attribute_name(node)}"
                return "@"
            
            def _get_end_line(self, node: ast.AST) -> int:
                """Node'un bitiş satırını bul."""
                if hasattr(node, 'end_lineno') and node.end_lineno:
                    return node.end_lineno
                return node.lineno
            
            def _get_function_signature(self, node: ast.FunctionDef) -> str:
                """Function signature oluştur."""
                args = []
                for arg in node.args.args:
                    args.append(arg.arg)
                
                signature = f"def {node.name}({', '.join(args)})"
                if node.returns:
                    signature += f" -> {self._get_type_annotation(node.returns)}"
                return signature
            
            def _get_class_signature(self, node: ast.ClassDef) -> str:
                """Class signature oluştur."""
                bases = []
                for base in node.bases:
                    if isinstance(base, ast.Name):
                        bases.append(base.id)
                    elif isinstance(base, ast.Attribute):
                        bases.append(f"{base.value.id}.{base.attr}")
                
                signature = f"class {node.name}"
                if bases:
                    signature += f"({', '.join(bases)})"
                return signature
            
            def _get_type_annotation(self, node: ast.AST) -> str:
                """Type annotation string'i."""
                if isinstance(node, ast.Name):
                    return node.id
                elif isinstance(node, ast.Subscript):
                    return f"{self._get_type_annotation(node.value)}[{self._get_type_annotation(node.slice)}]"
                elif isinstance(node, ast.Constant):
                    return str(node.value)
                return "Any"
        
        visitor = ScopeVisitor(target_line, context)
        visitor.visit(tree)
        
        context.imports_in_scope = visitor.imports
        context.variables_in_scope = list(visitor.variables)
        context.function_calls = visitor.function_calls
        context.decorators = visitor.decorators
    
    def _detect_semantic_type(
        self,
        tree: ast.AST,
        target_line: int,
        target_column: int,
        context: CursorContext,
        content: str
    ) -> None:
        """
        Cursor semantic type tespiti.
        
        Args:
            tree: AST tree
            target_line: Hedef satır
            target_column: Hedef sütun
            context: Cursor context
            content: Dosya içeriği
        """
        class SemanticVisitor(ast.NodeVisitor):
            def __init__(self, target_line: int, target_column: int, context: CursorContext, content: str):
                self.target_line = target_line
                self.target_column = target_column
                self.context = context
                self.content = content
                self.lines = content.splitlines()
            
            def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
                # Function definition
                if node.lineno == self.target_line and node.col_offset <= self.target_column:
                    self.context.semantic_type = CursorSemanticType.DEFINITION
                    self.context.referenced_symbol = node.name
                self.generic_visit(node)
            
            def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
                # Async function definition
                if node.lineno == self.target_line and node.col_offset <= self.target_column:
                    self.context.semantic_type = CursorSemanticType.DEFINITION
                    self.context.referenced_symbol = node.name
                self.generic_visit(node)
            
            def visit_ClassDef(self, node: ast.ClassDef) -> None:
                # Class definition
                if node.lineno == self.target_line and node.col_offset <= self.target_column:
                    self.context.semantic_type = CursorSemanticType.DEFINITION
                    self.context.referenced_symbol = node.name
                self.generic_visit(node)
            
            def visit_Call(self, node: ast.Call) -> None:
                # Function call
                if node.lineno == self.target_line:
                    if node.col_offset <= self.target_column <= node.end_col_offset:
                        self.context.semantic_type = CursorSemanticType.CALL
                        if isinstance(node.func, ast.Name):
                            self.context.referenced_symbol = node.func.id
                        elif isinstance(node.func, ast.Attribute):
                            self.context.referenced_symbol = f"{node.func.value.id}.{node.func.attr}"
                self.generic_visit(node)
            
            def visit_Import(self, node: ast.Import) -> None:
                # Import statement
                if node.lineno == self.target_line:
                    self.context.semantic_type = CursorSemanticType.IMPORT
                self.generic_visit(node)
            
            def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
                # From import statement
                if node.lineno == self.target_line:
                    self.context.semantic_type = CursorSemanticType.IMPORT
                self.generic_visit(node)
            
            def visit_Name(self, node: ast.Name) -> None:
                # Variable reference
                if node.lineno == self.target_line and node.col_offset <= self.target_column <= node.end_col_offset:
                    if self.context.semantic_type == CursorSemanticType.UNKNOWN:
                        self.context.semantic_type = CursorSemanticType.REFERENCE
                        self.context.referenced_symbol = node.id
                self.generic_visit(node)
        
        visitor = SemanticVisitor(target_line, target_column, context, content)
        visitor.visit(tree)
    
    def _resolve_symbol(self, context: CursorContext) -> None:
        """
        Symbol resolution (codebase index kullanarak).
        
        Args:
            context: Cursor context
        """
        if not self.codebase_index or not context.referenced_symbol:
            return
        
        try:
            self.codebase_index.index_project()
            
            # Symbol'ı ara
            symbols = self.codebase_index.search_symbols(context.referenced_symbol)
            
            if symbols:
                # İlk eşleşen symbol'ı al
                symbol = symbols[0]
                context.symbol_definition = {
                    "name": symbol.name,
                    "type": symbol.type,
                    "file": symbol.file,
                    "line_start": symbol.line_start,
                    "line_end": symbol.line_end,
                    "signature": symbol.signature,
                    "parent_class": symbol.parent_class,
                    "docstring": symbol.docstring
                }
        except Exception:
            pass
    
    def _find_related_files(self, context: CursorContext) -> None:
        """
        İlgili dosyaları bul (codebase index kullanarak).
        
        Args:
            context: Cursor context
        """
        if not self.codebase_index:
            return
        
        try:
            self.codebase_index.index_project()
            
            # İlgili dosyaları bul
            related = self.codebase_index.find_related_files(context.file_path, max_results=5)
            
            context.related_files = related
        except Exception:
            pass
    
    def format_context(self, context: CursorContext) -> str:
        """
        Cursor context'i formatla.
        
        Args:
            context: Cursor context
            
        Returns:
            str: Formatlanmış context
        """
        lines = []
        
        lines.append("=== CURSOR CONTEXT ===")
        lines.append(f"File: {context.file_path}")
        lines.append(f"Line: {context.line}, Column: {context.column}")
        lines.append(f"Scope: {context.current_scope}")
        lines.append(f"Semantic Type: {context.semantic_type.value}")
        
        if context.referenced_symbol:
            lines.append(f"Referenced Symbol: {context.referenced_symbol}")
        
        if context.symbol_definition:
            lines.append(f"\nSymbol Definition:")
            lines.append(f"  Type: {context.symbol_definition.get('type')}")
            lines.append(f"  File: {context.symbol_definition.get('file')}")
            lines.append(f"  Line: {context.symbol_definition.get('line_start')}")
            if context.symbol_definition.get('signature'):
                lines.append(f"  Signature: {context.symbol_definition.get('signature')}")
        
        if context.related_files:
            lines.append(f"\nRelated Files:")
            for file in context.related_files[:5]:
                lines.append(f"  {file}")
        
        if context.current_class:
            lines.append(f"Class: {context.current_class}")
            if context.class_signature:
                lines.append(f"  {context.class_signature}")
        
        if context.current_function:
            lines.append(f"Function: {context.current_function}")
            if context.function_signature:
                lines.append(f"  {context.function_signature}")
        
        # Docstring
        if context.docstring:
            lines.append(f"\nDocstring:")
            lines.append(f"  {context.docstring[:200]}")  # Max 200 chars
        
        # Decorators
        if context.decorators:
            lines.append(f"\nDecorators:")
            for dec in context.decorators:
                lines.append(f"  {dec}")
        
        # Call stack
        if context.parent_functions:
            lines.append(f"\nCall Stack:")
            for func in context.parent_functions:
                lines.append(f"  {func}")
        
        # Surrounding code
        if context.surrounding_lines_before:
            lines.append("\n--- Code Before Cursor ---")
            for i, line in enumerate(context.surrounding_lines_before[-10:], 1):
                lines.append(f"  {line}")
        
        if context.surrounding_lines_after:
            lines.append("\n--- Code After Cursor ---")
            for i, line in enumerate(context.surrounding_lines_after[:10], 1):
                lines.append(f"  {line}")
        
        # Imports
        if context.imports_in_scope:
            lines.append("\n--- Imports in Scope ---")
            for imp in context.imports_in_scope:
                lines.append(f"  {imp}")
        
        # Variables
        if context.variables_in_scope:
            lines.append("\n--- Variables in Scope ---")
            for var in context.variables_in_scope[:20]:
                lines.append(f"  {var}")
        
        # Function calls
        if context.function_calls:
            lines.append("\n--- Function Calls ---")
            for call in context.function_calls[:10]:
                lines.append(f"  {call}")
        
        return "\n".join(lines)


class SmartContextPrioritizer:
    """
    Smart context prioritization.
    
    Context bileşenlerini önceliklendir ve truncate et.
    """
    
    def __init__(self, max_tokens: int = 8000):
        """
        Args:
            max_tokens: Maksimum token limiti
        """
        self.max_tokens = max_tokens
        self.priorities = {
            "CURSOR_CONTEXT": 100,  # En yüksek öncelik
            "SYSTEM_CONTEXT": 95,
            "TASK_CONTEXT": 90,
            "CURRENT_PLAN": 85,
            "FAILURE_DETAILS": 80,
            "MEMORY": 75,
            "PROJECT_RULES": 70,
            "SESSION_CONTEXT": 65,
            "PROJECT_CONTEXT": 60,
            "CODEBASE_CONTEXT": 55,
            "TOOL_HISTORY": 50,
            "TEST_RESULTS": 45,
            "MEMORY_CONTEXT": 40
        }
    
    def prioritize_and_truncate(
        self,
        context_parts: Dict[str, str]
    ) -> str:
        """
        Context bileşenlerini önceliklendir ve truncate et.
        
        Args:
            context_parts: Context bileşenleri {name: content}
            
        Returns:
            str: Önceliklendirilmiş ve truncate edilmiş context
        """
        # Öncelik sırasına göre sırala
        sorted_parts = sorted(
            context_parts.items(),
            key=lambda x: self.priorities.get(x[0], 0),
            reverse=True
        )
        
        # Context'i oluştur
        parts = []
        current_length = 0
        char_limit = self.max_tokens * 4  # Yaklaşık 4 char/token
        
        for name, content in sorted_parts:
            if not content or not content.strip():
                continue
            
            # Bu bölüm eklenebilir mi?
            part_length = len(content)
            
            if current_length + part_length <= char_limit:
                parts.append(content)
                current_length += part_length
            else:
                # Truncate et
                remaining = char_limit - current_length
                if remaining > 100:  # En az 100 char bırak
                    truncated = content[:remaining]
                    truncated += "\n\n...[CONTEXT TRUNCATED]..."
                    parts.append(truncated)
                    current_length += len(truncated)
                break
        
        return "\n\n".join(parts)
