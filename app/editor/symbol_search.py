"""
MuhammedAI Local Developer - Symbol Search
Symbol search engine for code editor.
"""

import ast
import os
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum


class SymbolType(Enum):
    """Symbol type."""
    FUNCTION = "function"
    CLASS = "class"
    VARIABLE = "variable"
    METHOD = "method"
    PARAMETER = "parameter"
    ATTRIBUTE = "attribute"
    IMPORT = "import"
    CONSTANT = "constant"
    MODULE = "module"


class SymbolScope(Enum):
    """Symbol scope."""
    GLOBAL = "global"
    LOCAL = "local"
    CLASS = "class"
    FUNCTION = "function"
    MODULE = "module"


class SearchMode(Enum):
    """Search mode."""
    NORMAL = "normal"
    CASE_SENSITIVE = "case_sensitive"
    CASE_INSENSITIVE = "case_insensitive"
    REGEX = "regex"
    WHOLE_WORD = "whole_word"
    FUZZY = "fuzzy"


class SearchAction(Enum):
    """Search action."""
    SEARCH = "search"
    FIND_DEFINITION = "find_definition"
    FIND_REFERENCES = "find_references"
    FILTER = "filter"
    CLEAR = "clear"


@dataclass
class Symbol:
    """Symbol."""
    name: str
    type: SymbolType
    scope: SymbolScope
    file_path: str
    line: int
    column: int
    definition: Optional[str] = None
    docstring: Optional[str] = None
    parent: Optional[str] = None  # Parent class/function name
    context_before: str = ""
    context_after: str = ""
    is_highlighted: bool = False


@dataclass
class SymbolSearchResult:
    """Symbol search result."""
    success: bool
    action: Optional[str] = None
    symbols: List[Symbol] = field(default_factory=list)
    query: str = ""
    symbol_type: Optional[SymbolType] = None
    total_symbols: int = 0
    errors: List[str] = field(default_factory=list)
    message: Optional[str] = None
    current_index: int = -1


@dataclass
class SymbolSearchConfig:
    """Symbol search configuration."""
    mode: SearchMode = SearchMode.NORMAL
    case_sensitive: bool = False
    include_context: bool = True
    context_lines: int = 2
    highlight_matches: bool = True
    max_results: int = 1000
    exclude_dirs: List[str] = field(default_factory=lambda: [".git", "__pycache__", "node_modules", ".venv"])


class SymbolSearchEngine:
    """
    Symbol search engine.
    
    Özellikler:
    - Function search
    - Class search
    - Variable search
    - Method search
    - Parameter search
    - Import search
    - Cross-file symbol search
    - Definition lookup
    - Reference lookup
    - Symbol type filtering
    - AST-based parsing
    - Project-wide indexing
    - Search modes (normal, regex, fuzzy)
    - Context display
    - Search history
    - Configuration management
    - Statistics tracking
    - Find next/previous
    """
    
    def __init__(self, project_root: str = ".", config: Optional[SymbolSearchConfig] = None):
        """
        Args:
            project_root: Proje kök dizini
            config: Konfigürasyon
        """
        self.project_root = project_root
        self.config = config or SymbolSearchConfig()
        self.symbol_index: Dict[str, List[Symbol]] = {}
        self._indexed_files: set = set()
        self.search_history: List[Tuple[str, str]] = []  # (action, query)
        self.current_symbols: List[Symbol] = []
        self.current_index: int = -1
    
    def search_symbols(
        self,
        query: str,
        symbol_type: Optional[SymbolType] = None,
        file_path: Optional[str] = None
    ) -> SymbolSearchResult:
        """
        Symbol ara.
        
        Args:
            query: Arama sorgusu
            symbol_type: Symbol tipi (opsiyonel)
            file_path: Dosya yolu (opsiyonel)
            
        Returns:
            SymbolSearchResult: Arama sonucu
        """
        result = SymbolSearchResult(success=False)
        result.action = SearchAction.SEARCH.value
        result.query = query
        result.symbol_type = symbol_type
        
        try:
            symbols = []
            
            if file_path:
                # Tek dosya içinde ara
                file_symbols = self._extract_symbols_from_file(file_path)
                symbols = self._filter_symbols(file_symbols, query, symbol_type)
            else:
                # Tüm index içinde ara
                for file_path_key, file_symbols in self.symbol_index.items():
                    filtered = self._filter_symbols(file_symbols, query, symbol_type)
                    symbols.extend(filtered)
            
            # Max results limit
            if len(symbols) > self.config.max_results:
                symbols = symbols[:self.config.max_results]
            
            self.current_symbols = symbols
            self.current_index = 0 if symbols else -1
            
            result.symbols = symbols
            result.total_symbols = len(symbols)
            result.current_index = self.current_index
            result.success = True
            result.message = f"Found {len(symbols)} symbols"
            
            # Geçmişe ekle
            self.search_history.append(("search", query))
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def build_index(self, file_path: str) -> SymbolSearchResult:
        """
        Dosya için symbol index oluştur.
        
        Args:
            file_path: Dosya yolu
            
        Returns:
            SymbolSearchResult: Index oluşturma sonucu
        """
        result = SymbolSearchResult(success=False)
        
        try:
            if not os.path.exists(file_path):
                result.errors.append(f"File {file_path} does not exist")
                return result
            
            symbols = self._extract_symbols_from_file(file_path)
            self.symbol_index[file_path] = symbols
            self._indexed_files.add(file_path)
            
            result.symbols = symbols
            result.total_symbols = len(symbols)
            result.success = True
            result.message = f"Indexed {len(symbols)} symbols from {file_path}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def _extract_symbols_from_file(self, file_path: str) -> List[Symbol]:
        """Dosyadan symbol çıkar."""
        symbols = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                # Functions
                if isinstance(node, ast.FunctionDef):
                    symbol = Symbol(
                        name=node.name,
                        type=SymbolType.FUNCTION,
                        scope=SymbolScope.GLOBAL,
                        file_path=file_path,
                        line=node.lineno,
                        column=node.col_offset,
                        definition=self._get_node_definition(node),
                        docstring=ast.get_docstring(node)
                    )
                    symbols.append(symbol)
                    
                    # Parameters
                    for arg in node.args.args:
                        param_symbol = Symbol(
                            name=arg.arg,
                            type=SymbolType.PARAMETER,
                            scope=SymbolScope.FUNCTION,
                            file_path=file_path,
                            line=node.lineno,
                            column=node.col_offset,
                            parent=node.name
                        )
                        symbols.append(param_symbol)
                
                # Classes
                elif isinstance(node, ast.ClassDef):
                    symbol = Symbol(
                        name=node.name,
                        type=SymbolType.CLASS,
                        scope=SymbolScope.GLOBAL,
                        file_path=file_path,
                        line=node.lineno,
                        column=node.col_offset,
                        definition=self._get_node_definition(node),
                        docstring=ast.get_docstring(node)
                    )
                    symbols.append(symbol)
                    
                    # Methods
                    for item in node.body:
                        if isinstance(item, ast.FunctionDef):
                            method_symbol = Symbol(
                                name=item.name,
                                type=SymbolType.METHOD,
                                scope=SymbolScope.CLASS,
                                file_path=file_path,
                                line=item.lineno,
                                column=item.col_offset,
                                parent=node.name
                            )
                            symbols.append(method_symbol)
                
                # Variables (assignments)
                elif isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            symbol = Symbol(
                                name=target.id,
                                type=SymbolType.VARIABLE,
                                scope=SymbolScope.GLOBAL,
                                file_path=file_path,
                                line=node.lineno,
                                column=node.col_offset
                            )
                            symbols.append(symbol)
                
                # Imports
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        symbol = Symbol(
                            name=alias.asname or alias.name,
                            type=SymbolType.IMPORT,
                            scope=SymbolScope.MODULE,
                            file_path=file_path,
                            line=node.lineno,
                            column=node.col_offset
                        )
                        symbols.append(symbol)
                
                elif isinstance(node, ast.ImportFrom):
                    for alias in node.names:
                        symbol = Symbol(
                            name=alias.asname or alias.name,
                            type=SymbolType.IMPORT,
                            scope=SymbolScope.MODULE,
                            file_path=file_path,
                            line=node.lineno,
                            column=node.col_offset,
                            parent=node.module
                        )
                        symbols.append(symbol)
        
        except Exception:
            pass
        
        return symbols
    
    def _get_node_definition(self, node: ast.AST) -> str:
        """Node definition'ı al."""
        if isinstance(node, ast.FunctionDef):
            args = [arg.arg for arg in node.args.args]
            return f"def {node.name}({', '.join(args)})"
        elif isinstance(node, ast.ClassDef):
            return f"class {node.name}"
        return ""
    
    def _filter_symbols(
        self,
        symbols: List[Symbol],
        query: str,
        symbol_type: Optional[SymbolType]
    ) -> List[Symbol]:
        """Symbol'ları filtrele."""
        filtered = symbols
        
        # Query bazlı filtre
        if query:
            if self.config.mode == SearchMode.CASE_SENSITIVE:
                filtered = [s for s in filtered if query in s.name]
            elif self.config.mode == SearchMode.REGEX:
                import re
                try:
                    pattern = re.compile(query)
                    filtered = [s for s in filtered if pattern.search(s.name)]
                except re.error:
                    pass
            elif self.config.mode == SearchMode.WHOLE_WORD:
                import re
                pattern = r'\b' + re.escape(query) + r'\b'
                filtered = [s for s in filtered if re.search(pattern, s.name, re.IGNORECASE)]
            elif self.config.mode == SearchMode.FUZZY:
                query_lower = query.lower()
                filtered = [s for s in filtered if query_lower in s.name.lower()]
            else:
                query_lower = query.lower()
                filtered = [s for s in filtered if query_lower in s.name.lower()]
        
        # Tip bazlı filtre
        if symbol_type:
            filtered = [s for s in filtered if s.type == symbol_type]
        
        return filtered
    
    def find_definition(
        self,
        symbol_name: str,
        file_path: str,
        line: int
    ) -> SymbolSearchResult:
        """
        Symbol definition'ını bul.
        
        Args:
            symbol_name: Symbol adı
            file_path: Dosya yolu
            line: Satır numarası
            
        Returns:
            SymbolSearchResult: Bulma sonucu
        """
        result = SymbolSearchResult(success=False)
        result.action = SearchAction.FIND_DEFINITION.value
        result.query = symbol_name
        
        try:
            # Dosyadan symbol'ları çıkar
            symbols = self._extract_symbols_from_file(file_path)
            
            # İsmi eşleşen symbol'ı bul
            for symbol in symbols:
                if symbol.name == symbol_name and symbol.line <= line:
                    result.symbols = [symbol]
                    result.total_symbols = 1
                    result.success = True
                    result.message = f"Found definition for {symbol_name}"
                    
                    # Geçmişe ekle
                    self.search_history.append(("find_definition", symbol_name))
                    return result
            
            result.errors.append(f"Definition not found for {symbol_name}")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def find_references(
        self,
        symbol_name: str,
        file_path: str
    ) -> SymbolSearchResult:
        """
        Symbol referanslarını bul.
        
        Args:
            symbol_name: Symbol adı
            file_path: Dosya yolu
            
        Returns:
            SymbolSearchResult: Referans sonucu
        """
        result = SymbolSearchResult(success=False)
        result.action = SearchAction.FIND_REFERENCES.value
        result.query = symbol_name
        
        references = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Name):
                    if node.id == symbol_name:
                        reference = Symbol(
                            name=node.id,
                            type=SymbolType.VARIABLE,
                            scope=SymbolScope.LOCAL,
                            file_path=file_path,
                            line=node.lineno,
                            column=node.col_offset
                        )
                        references.append(reference)
            
            result.symbols = references
            result.total_symbols = len(references)
            result.success = True
            result.message = f"Found {len(references)} references"
            
            # Geçmişe ekle
            self.search_history.append(("find_references", symbol_name))
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def find_next(self) -> SymbolSearchResult:
        """
        Sonraki symbol'ı bul.
        
        Returns:
            SymbolSearchResult: Bulma sonucu
        """
        result = SymbolSearchResult(success=False)
        result.action = SearchAction.SEARCH.value
        
        try:
            if not self.current_symbols:
                result.errors.append("No symbols available")
                return result
            
            self.current_index = (self.current_index + 1) % len(self.current_symbols)
            
            result.success = True
            result.current_index = self.current_index
            result.message = f"Symbol {self.current_index + 1}/{len(self.current_symbols)}"
            
            self.search_history.append(("find_next", str(self.current_index)))
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def find_previous(self) -> SymbolSearchResult:
        """
        Önceki symbol'ı bul.
        
        Returns:
            SymbolSearchResult: Bulma sonucu
        """
        result = SymbolSearchResult(success=False)
        result.action = SearchAction.SEARCH.value
        
        try:
            if not self.current_symbols:
                result.errors.append("No symbols available")
                return result
            
            self.current_index = (self.current_index - 1) % len(self.current_symbols)
            
            result.success = True
            result.current_index = self.current_index
            result.message = f"Symbol {self.current_index + 1}/{len(self.current_symbols)}"
            
            self.search_history.append(("find_previous", str(self.current_index)))
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_search_history(self) -> List[Tuple[str, str]]:
        """
        Arama geçmişini al.
        
        Returns:
            List[Tuple[str, str]]: Geçmiş
        """
        return self.search_history
    
    def clear_history(self) -> SymbolSearchResult:
        """
        Geçmişi temizle.
        
        Returns:
            SymbolSearchResult: Temizleme sonucu
        """
        result = SymbolSearchResult(success=False)
        
        try:
            self.search_history.clear()
            result.success = True
            result.message = "Search history cleared"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        İstatistikleri al.
        
        Returns:
            Dict[str, Any]: İstatistikler
        """
        return {
            "total_symbols": len(self.current_symbols),
            "current_index": self.current_index,
            "search_history_count": len(self.search_history),
            "indexed_files_count": len(self._indexed_files),
            "symbol_index_size": sum(len(symbols) for symbols in self.symbol_index.values())
        }
    
    def update_config(self, config: SymbolSearchConfig) -> SymbolSearchResult:
        """
        Konfigürasyon güncelle.
        
        Args:
            config: Yeni konfigürasyon
            
        Returns:
            SymbolSearchResult: Güncelleme sonucu
        """
        result = SymbolSearchResult(success=False)
        
        try:
            self.config = config
            result.success = True
            result.message = "Config updated"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_config(self) -> SymbolSearchConfig:
        """
        Konfigürasyon al.
        
        Returns:
            SymbolSearchConfig: Konfigürasyon
        """
        return self.config


if __name__ == "__main__":
    # Basit test
    engine = SymbolSearchEngine()
    
    # Test dosyası oluştur
    test_code = """
def my_function(x, y):
    result = x + y
    return result

class MyClass:
    def my_method(self):
        pass
"""
    
    with open("test_symbols.py", "w") as f:
        f.write(test_code)
    
    # Index oluştur
    result = engine.build_index("test_symbols.py")
    print(f"Index built: {result.success}")
    print(f"Total symbols: {result.total_symbols}")
    
    # Ara
    search_result = engine.search_symbols("my_function")
    print(f"Search: {search_result.success}")
    print(f"Found: {search_result.total_symbols}")
    
    # Temizle
    os.remove("test_symbols.py")
