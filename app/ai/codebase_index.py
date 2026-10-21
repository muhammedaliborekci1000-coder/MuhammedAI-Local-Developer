"""
MuhammedAI Local Developer - Codebase Index
Python projelerini AST kullanarak indeksler.
"""

import ast
import os
from pathlib import Path
from typing import Dict, List, Optional, Set, Any
from dataclasses import dataclass, field
from datetime import datetime
import hashlib

from app.core.config import PROJECT_ROOT, IGNORED_DIRECTORIES


@dataclass
class Symbol:
    """Kod sembolü (class, function, method)."""
    type: str  # class, function, method, async_function, async_method
    name: str
    file: str
    line_start: int
    line_end: int
    signature: str = ""
    parent_class: Optional[str] = None
    decorators: List[str] = field(default_factory=list)
    docstring: Optional[str] = None


@dataclass
class ImportInfo:
    """Import bilgisi."""
    module: str
    name: str  # as alias
    line: int
    is_from: bool = False
    from_module: Optional[str] = None


@dataclass
class FileIndex:
    """Dosya indeksi."""
    file_path: str
    symbols: List[Symbol] = field(default_factory=list)
    imports: List[ImportInfo] = field(default_factory=list)
    parse_error: Optional[str] = None
    mtime: float = 0.0
    hash: str = ""


@dataclass
class CodebaseIndex:
    """
    Codebase indeksi.
    
    Python projelerini AST kullanarak indeksler.
    """
    project_root: Path = PROJECT_ROOT
    files: Dict[str, FileIndex] = field(default_factory=dict)
    import_graph: Dict[str, Set[str]] = field(default_factory=dict)  # file -> imports
    reverse_import_graph: Dict[str, Set[str]] = field(default_factory=dict)  # file -> imported_by
    
    def __init__(self, project_root: Path = PROJECT_ROOT):
        self.project_root = Path(project_root)
        self.files = {}
        self.import_graph = {}
        self.reverse_import_graph = {}
    
    def index_project(self) -> None:
        """Projeyi indeksle."""
        for py_file in self._scan_python_files():
            self.index_file(py_file)
        
        self._build_import_graph()
    
    def _scan_python_files(self) -> List[Path]:
        """Python dosyalarını tara."""
        py_files = []
        
        for path in self.project_root.rglob("*.py"):
            if not path.is_file():
                continue
            
            # Workspace boundary kontrolü
            try:
                path.resolve().relative_to(self.project_root.resolve())
            except ValueError:
                continue
            
            # Ignored directories kontrolü
            if any(ignored in path.parts for ignored in IGNORED_DIRECTORIES):
                continue
            
            py_files.append(path)
        
        return sorted(py_files)
    
    def index_file(self, file_path: Path) -> FileIndex:
        """
        Tek dosyayı indeksle.
        
        Args:
            file_path: Dosya yolu
            
        Returns:
            FileIndex: Dosya indeksi
        """
        relative_path = str(file_path.relative_to(self.project_root))
        
        # Cache kontrolü
        if relative_path in self.files:
            existing = self.files[relative_path]
            current_mtime = file_path.stat().st_mtime
            if existing.mtime == current_mtime:
                return existing
        
        # Dosyayı oku
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            self.files[relative_path] = FileIndex(
                file_path=relative_path,
                parse_error=f"Read error: {e}"
            )
            return self.files[relative_path]
        
        # Hash hesapla
        file_hash = hashlib.md5(content.encode()).hexdigest()
        current_mtime = file_path.stat().st_mtime
        
        # AST parse
        try:
            tree = ast.parse(content, filename=str(file_path))
        except SyntaxError as e:
            self.files[relative_path] = FileIndex(
                file_path=relative_path,
                mtime=current_mtime,
                hash=file_hash,
                parse_error=f"Syntax error at line {e.lineno}: {e.msg}"
            )
            return self.files[relative_path]
        
        # Index oluştur
        symbols = []
        imports = []
        
        visitor = CodeIndexVisitor(file_path, relative_path)
        visitor.visit(tree)
        
        symbols = visitor.symbols
        imports = visitor.imports
        
        self.files[relative_path] = FileIndex(
            file_path=relative_path,
            symbols=symbols,
            imports=imports,
            mtime=current_mtime,
            hash=file_hash
        )
        
        return self.files[relative_path]
    
    def _build_import_graph(self) -> None:
        """Import graph oluştur."""
        self.import_graph = {}
        self.reverse_import_graph = {}
        
        for file_path, file_index in self.files.items():
            if file_index.parse_error:
                continue
            
            imports = set()
            for imp in file_index.imports:
                if imp.is_from:
                    imports.add(imp.from_module or "")
                else:
                    imports.add(imp.module)
            
            self.import_graph[file_path] = imports
        
        # Reverse graph
        for file_path, imports in self.import_graph.items():
            for imp in imports:
                if imp not in self.reverse_import_graph:
                    self.reverse_import_graph[imp] = set()
                self.reverse_import_graph[imp].add(file_path)
    
    def search_symbols(self, query: str) -> List[Symbol]:
        """
        Sembol ara.
        
        Args:
            query: Sorgu (symbol adı)
            
        Returns:
            List[Symbol]: Eşleşen semboller
        """
        results = []
        query_lower = query.lower()
        
        for file_index in self.files.values():
            if file_index.parse_error:
                continue
            
            for symbol in file_index.symbols:
                if query_lower in symbol.name.lower():
                    results.append(symbol)
        
        return results
    
    def get_symbol_details(self, symbol_name: str, file_path: Optional[str] = None) -> Optional[Symbol]:
        """
        Sembol detaylarını al.
        
        Args:
            symbol_name: Sembol adı
            file_path: Dosya yolu (opsiyonel)
            
        Returns:
            Optional[Symbol]: Sembol detayları
        """
        if file_path:
            if file_path not in self.files:
                return None
            
            for symbol in self.files[file_path].symbols:
                if symbol.name == symbol_name:
                    return symbol
        else:
            for file_index in self.files.values():
                for symbol in file_index.symbols:
                    if symbol.name == symbol_name:
                        return symbol
        
        return None
    
    def find_related_files(self, file_path: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """
        İlgili dosyaları bul.
        
        Args:
            file_path: Dosya yolu
            max_results: Maksimum sonuç
            
        Returns:
            List[Dict]: İlgili dosyalar (score ile)
        """
        results = []
        
        if file_path not in self.files:
            return results
        
        # Direct imports
        score = 100
        for imp in self.import_graph.get(file_path, []):
            results.append({"file": imp, "score": score, "reason": "direct_import"})
            score -= 5
        
        # Reverse imports (imported_by)
        score = 90
        for imp in self.reverse_import_graph.get(file_path, []):
            results.append({"file": imp, "score": score, "reason": "imported_by"})
            score -= 5
        
        # Sort by score
        results.sort(key=lambda x: x["score"], reverse=True)
        
        return results[:max_results]
    
    def get_file_dependencies(self, file_path: str) -> Set[str]:
        """
        Dosyanın bağımlılıklarını al.
        
        Args:
            file_path: Dosya yolu
            
        Returns:
            Set[str]: Bağımlılıklar
        """
        return self.import_graph.get(file_path, set())
    
    def get_dependents(self, file_path: str) -> Set[str]:
        """
        Dosyayı import eden dosyaları al.
        
        Args:
            file_path: Dosya yolu
            
        Returns:
            Set[str]: Dependents
        """
        return self.reverse_import_graph.get(file_path, set())


class CodeIndexVisitor(ast.NodeVisitor):
    """AST visitor for code indexing."""
    
    def __init__(self, file_path: Path, relative_path: str):
        self.file_path = file_path
        self.relative_path = relative_path
        self.symbols: List[Symbol] = []
        self.imports: List[ImportInfo] = []
        self.current_class: Optional[str] = None
    
    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """Class definition."""
        decorators = [self._get_decorator_name(d) for d in node.decorator_list]
        
        symbol = Symbol(
            type="class",
            name=node.name,
            file=self.relative_path,
            line_start=node.lineno,
            line_end=self._get_end_line(node),
            signature=f"class {node.name}",
            decorators=decorators,
            docstring=ast.get_docstring(node)
        )
        
        self.symbols.append(symbol)
        
        # Inheritance
        for base in node.bases:
            if isinstance(base, ast.Name):
                pass  # Inheritance info eklenebilir
        
        # Visit methods
        old_class = self.current_class
        self.current_class = node.name
        self.generic_visit(node)
        self.current_class = old_class
    
    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Function/method definition."""
        decorators = [self._get_decorator_name(d) for d in node.decorator_list]
        
        if self.current_class:
            symbol_type = "method"
            signature = f"def {node.name}({self._get_args(node)})"
        else:
            symbol_type = "function"
            signature = f"def {node.name}({self._get_args(node)})"
        
        symbol = Symbol(
            type=symbol_type,
            name=node.name,
            file=self.relative_path,
            line_start=node.lineno,
            line_end=self._get_end_line(node),
            signature=signature,
            parent_class=self.current_class,
            decorators=decorators,
            docstring=ast.get_docstring(node)
        )
        
        self.symbols.append(symbol)
        self.generic_visit(node)
    
    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        """Async function/method definition."""
        decorators = [self._get_decorator_name(d) for d in node.decorator_list]
        
        if self.current_class:
            symbol_type = "async_method"
            signature = f"async def {node.name}({self._get_args(node)})"
        else:
            symbol_type = "async_function"
            signature = f"async def {node.name}({self._get_args(node)})"
        
        symbol = Symbol(
            type=symbol_type,
            name=node.name,
            file=self.relative_path,
            line_start=node.lineno,
            line_end=self._get_end_line(node),
            signature=signature,
            parent_class=self.current_class,
            decorators=decorators,
            docstring=ast.get_docstring(node)
        )
        
        self.symbols.append(symbol)
        self.generic_visit(node)
    
    def visit_Import(self, node: ast.Import) -> None:
        """Import statement."""
        for alias in node.names:
            self.imports.append(ImportInfo(
                module=alias.name,
                name=alias.asname or alias.name,
                line=node.lineno,
                is_from=False
            ))
        self.generic_visit(node)
    
    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        """From import statement."""
        module = node.module or ""
        for alias in node.names:
            self.imports.append(ImportInfo(
                module=alias.name,
                name=alias.asname or alias.name,
                line=node.lineno,
                is_from=True,
                from_module=module
            ))
        self.generic_visit(node)
    
    def _get_args(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
        """Function arguments string."""
        args = []
        
        # Positional args
        for arg in node.args.posonlyargs:
            args.append(arg.arg)
        
        # Regular args
        for arg in node.args.args:
            args.append(arg.arg)
        
        # Varargs
        if node.args.vararg:
            args.append(f"*{node.args.vararg.arg}")
        
        # Kwargs
        if node.args.kwarg:
            args.append(f"**{node.args.kwarg.arg}")
        
        return ", ".join(args)
    
    def _get_decorator_name(self, decorator: ast.expr) -> str:
        """Decorator name."""
        if isinstance(decorator, ast.Name):
            return decorator.id
        elif isinstance(decorator, ast.Attribute):
            # Nested attribute (e.g., pytest.mark.slow)
            if isinstance(decorator.value, ast.Name):
                return f"{decorator.value.id}.{decorator.attr}"
            elif isinstance(decorator.value, ast.Attribute):
                return f"{self._get_decorator_name(decorator.value)}.{decorator.attr}"
            else:
                return str(decorator.attr)
        elif isinstance(decorator, ast.Call):
            return self._get_decorator_name(decorator.func)
        return ""
    
    def _get_end_line(self, node: ast.AST) -> int:
        """Get end line of node."""
        if hasattr(node, 'end_lineno') and node.end_lineno:
            return node.end_lineno
        return node.lineno
