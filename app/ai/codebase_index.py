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
    type: str  # class, function, method, async_function, async_method, variable
    name: str
    file: str
    line_start: int
    line_end: int
    signature: str = ""
    parent_class: Optional[str] = None
    decorators: List[str] = field(default_factory=list)
    docstring: Optional[str] = None
    references: List[str] = field(default_factory=list)  # Dosya yolları (referanslar)
    calls: List[str] = field(default_factory=list)  # Çağırdığı semboller
    called_by: List[str] = field(default_factory=list)  # Kendisini çağıran semboller
    base_classes: List[str] = field(default_factory=list)  # Miras aldığı class'lar
    derived_classes: List[str] = field(default_factory=list)  # Kendisinden türeyen class'lar
    type_hint: Optional[str] = None  # Type hint (varsa)


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
    call_graph: Dict[str, Set[str]] = field(default_factory=dict)  # symbol -> calls
    reverse_call_graph: Dict[str, Set[str]] = field(default_factory=dict)  # symbol -> called_by
    inheritance_graph: Dict[str, Set[str]] = field(default_factory=dict)  # class -> bases
    reverse_inheritance_graph: Dict[str, Set[str]] = field(default_factory=dict)  # class -> derived
    
    def __init__(self, project_root: Path = PROJECT_ROOT):
        self.project_root = Path(project_root)
        self.files = {}
        self.import_graph = {}
        self.reverse_import_graph = {}
        self.call_graph = {}
        self.reverse_call_graph = {}
        self.inheritance_graph = {}
        self.reverse_inheritance_graph = {}
    
    def index_project(self) -> None:
        """Projeyi indeksle."""
        for py_file in self._scan_python_files():
            self.index_file(py_file)
        
        self._build_import_graph()
        self._build_call_graph()
        self._build_inheritance_graph()
        self._build_symbol_references()
    
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
    
    def find_usages(self, symbol_name: str, file_path: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Sembolün kullanımlarını bul (find usages).
        
        Args:
            symbol_name: Sembol adı
            file_path: Dosya yolu (opsiyonel - belirli dosyada ara)
            
        Returns:
            List[Dict]: Kullanımlar (file, line, context)
        """
        usages = []
        
        for file_index in self.files.values():
            if file_path and file_index.file_path != file_path:
                continue
            
            if file_index.parse_error:
                continue
            
            # Dosyayı oku ve symbol kullanımlarını ara
            try:
                full_path = self.project_root / file_index.file_path
                content = full_path.read_text(encoding='utf-8')
                lines = content.splitlines()
                
                for line_num, line in enumerate(lines, 1):
                    if symbol_name in line:
                        # Basit string matching - daha gelişmiş AST tracking yapılabilir
                        usages.append({
                            "file": file_index.file_path,
                            "line": line_num,
                            "context": line.strip(),
                            "symbol": symbol_name
                        })
            except Exception:
                pass
        
        return usages
    
    def go_to_definition(self, symbol_name: str, file_path: str, line: int) -> Optional[Dict[str, Any]]:
        """
        Symbol definition'ına git (go to definition).
        
        Args:
            symbol_name: Sembol adı
            file_path: Dosya yolu
            line: Satır numarası
            
        Returns:
            Optional[Dict]: Definition bilgisi
        """
        # Önce aynı dosyada ara
        if file_path in self.files:
            for symbol in self.files[file_path].symbols:
                if symbol.name == symbol_name:
                    return {
                        "file": symbol.file,
                        "line": symbol.line_start,
                        "line_end": symbol.line_end,
                        "type": symbol.type,
                        "signature": symbol.signature,
                        "docstring": symbol.docstring
                    }
        
        # Tüm dosyalarda ara
        for file_index in self.files.values():
            for symbol in file_index.symbols:
                if symbol.name == symbol_name:
                    return {
                        "file": symbol.file,
                        "line": symbol.line_start,
                        "line_end": symbol.line_end,
                        "type": symbol.type,
                        "signature": symbol.signature,
                        "docstring": symbol.docstring
                    }
        
        return None
    
    def get_call_hierarchy(self, symbol_name: str) -> Dict[str, List[str]]:
        """
        Call hierarchy al (çağırdığı ve çağıran semboller).
        
        Args:
            symbol_name: Sembol adı
            
        Returns:
            Dict: calls (çağırdığı), called_by (çağıran)
        """
        symbol_key = f"{symbol_name}"
        
        return {
            "calls": list(self.call_graph.get(symbol_key, set())),
            "called_by": list(self.reverse_call_graph.get(symbol_key, set()))
        }
    
    def get_inheritance_hierarchy(self, class_name: str) -> Dict[str, List[str]]:
        """
        Inheritance hierarchy al (miras ve türeyen class'lar).
        
        Args:
            class_name: Class adı
            
        Returns:
            Dict: base_classes (miras aldığı), derived_classes (türeyen)
        """
        class_key = f"{class_name}"
        
        return {
            "base_classes": list(self.inheritance_graph.get(class_key, set())),
            "derived_classes": list(self.reverse_inheritance_graph.get(class_key, set()))
        }
    
    def _build_call_graph(self) -> None:
        """Call graph oluştur."""
        self.call_graph = {}
        self.reverse_call_graph = {}
        
        for file_index in self.files.values():
            if file_index.parse_error:
                continue
            
            for symbol in file_index.symbols:
                if symbol.type in ["function", "method", "async_function", "async_method"]:
                    symbol_key = f"{symbol.file}:{symbol.name}"
                    self.call_graph[symbol_key] = set(symbol.calls)
                    
                    # Reverse graph
                    for called in symbol.calls:
                        if called not in self.reverse_call_graph:
                            self.reverse_call_graph[called] = set()
                        self.reverse_call_graph[called].add(symbol_key)
    
    def _build_inheritance_graph(self) -> None:
        """Inheritance graph oluştur."""
        self.inheritance_graph = {}
        self.reverse_inheritance_graph = {}
        
        for file_index in self.files.values():
            if file_index.parse_error:
                continue
            
            for symbol in file_index.symbols:
                if symbol.type == "class":
                    class_key = f"{symbol.file}:{symbol.name}"
                    self.inheritance_graph[class_key] = set(symbol.base_classes)
                    
                    # Reverse graph
                    for base in symbol.base_classes:
                        if base not in self.reverse_inheritance_graph:
                            self.reverse_inheritance_graph[base] = set()
                        self.reverse_inheritance_graph[base].add(class_key)
    
    def _build_symbol_references(self) -> None:
        """Symbol referanslarını oluştur."""
        for file_index in self.files.values():
            if file_index.parse_error:
                continue
            
            for symbol in file_index.symbols:
                symbol_key = f"{symbol.file}:{symbol.name}"
                symbol.references = list(self.reverse_call_graph.get(symbol_key, set()))


class CodeIndexVisitor(ast.NodeVisitor):
    """AST visitor for code indexing."""
    
    def __init__(self, file_path: Path, relative_path: str):
        self.file_path = file_path
        self.relative_path = relative_path
        self.symbols: List[Symbol] = []
        self.imports: List[ImportInfo] = []
        self.current_class: Optional[str] = None
        self.current_function: Optional[str] = None
        self.function_calls: List[str] = []
    
    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """Class definition."""
        decorators = [self._get_decorator_name(d) for d in node.decorator_list]
        
        # Base classes
        base_classes = []
        for base in node.bases:
            if isinstance(base, ast.Name):
                base_classes.append(base.id)
            elif isinstance(base, ast.Attribute):
                base_classes.append(self._get_attribute_name(base))
        
        symbol = Symbol(
            type="class",
            name=node.name,
            file=self.relative_path,
            line_start=node.lineno,
            line_end=self._get_end_line(node),
            signature=f"class {node.name}",
            decorators=decorators,
            docstring=ast.get_docstring(node),
            base_classes=base_classes
        )
        
        self.symbols.append(symbol)
        
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
        
        # Function calls reset
        self.function_calls = []
        
        # Visit body to collect calls
        old_function = self.current_function
        self.current_function = node.name
        self.generic_visit(node)
        self.current_function = old_function
        
        symbol = Symbol(
            type=symbol_type,
            name=node.name,
            file=self.relative_path,
            line_start=node.lineno,
            line_end=self._get_end_line(node),
            signature=signature,
            parent_class=self.current_class,
            decorators=decorators,
            docstring=ast.get_docstring(node),
            calls=list(self.function_calls)
        )
        
        self.symbols.append(symbol)
        self.function_calls = []
    
    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        """Async function/method definition."""
        decorators = [self._get_decorator_name(d) for d in node.decorator_list]
        
        if self.current_class:
            symbol_type = "async_method"
            signature = f"async def {node.name}({self._get_args(node)})"
        else:
            symbol_type = "async_function"
            signature = f"async def {node.name}({self._get_args(node)})"
        
        # Function calls reset
        self.function_calls = []
        
        # Visit body to collect calls
        old_function = self.current_function
        self.current_function = node.name
        self.generic_visit(node)
        self.current_function = old_function
        
        symbol = Symbol(
            type=symbol_type,
            name=node.name,
            file=self.relative_path,
            line_start=node.lineno,
            line_end=self._get_end_line(node),
            signature=signature,
            parent_class=self.current_class,
            decorators=decorators,
            docstring=ast.get_docstring(node),
            calls=list(self.function_calls)
        )
        
        self.symbols.append(symbol)
        self.function_calls = []
    
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
    
    def visit_Call(self, node: ast.Call) -> None:
        """Function call tracking."""
        call_name = self._get_call_name(node)
        if call_name:
            self.function_calls.append(call_name)
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
    
    def _get_call_name(self, node: ast.Call) -> str:
        """Function call name."""
        if isinstance(node.func, ast.Name):
            return node.func.id
        elif isinstance(node.func, ast.Attribute):
            return self._get_attribute_name(node.func)
        return ""
    
    def _get_attribute_name(self, node: ast.Attribute) -> str:
        """Attribute name."""
        if isinstance(node.value, ast.Name):
            return f"{node.value.id}.{node.attr}"
        elif isinstance(node.value, ast.Attribute):
            return f"{self._get_attribute_name(node.value)}.{node.attr}"
        return node.attr
    
    def _get_end_line(self, node: ast.AST) -> int:
        """Get end line of node."""
        if hasattr(node, 'end_lineno') and node.end_lineno:
            return node.end_lineno
        return node.lineno
