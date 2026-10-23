"""
MuhammedAI Local Developer - Symbol Navigation UI
Symbol navigation UI system for code editor.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum


class SymbolType(Enum):
    """Symbol type."""
    CLASS = "class"
    FUNCTION = "function"
    METHOD = "method"
    VARIABLE = "variable"
    CONSTANT = "constant"
    PROPERTY = "property"
    INTERFACE = "interface"
    ENUM = "enum"
    TYPE_ALIAS = "type_alias"
    NAMESPACE = "namespace"
    MODULE = "module"
    IMPORT = "import"


class SymbolScope(Enum):
    """Symbol scope."""
    PUBLIC = "public"
    PRIVATE = "private"
    PROTECTED = "protected"
    INTERNAL = "internal"
    FILE = "file"
    GLOBAL = "global"


@dataclass
class Symbol:
    """Symbol information."""
    id: str
    name: str
    type: SymbolType
    scope: SymbolScope = SymbolScope.PUBLIC
    line: int = 0
    column: int = 0
    file_path: Optional[str] = None
    parent: Optional[str] = None
    children: List[str] = field(default_factory=list)
    is_static: bool = False
    is_abstract: bool = False
    is_async: bool = False
    documentation: Optional[str] = None


@dataclass
class SymbolNavigationConfig:
    """Symbol navigation configuration."""
    show_private_symbols: bool = False
    show_protected_symbols: bool = True
    show_internal_symbols: bool = True
    group_by_type: bool = True
    group_by_scope: bool = False
    show_line_numbers: bool = True
    show_icons: bool = True
    show_documentation: bool = False
    max_symbols: int = 1000
    enable_fuzzy_search: bool = True


@dataclass
class SymbolNavigationResult:
    """Symbol navigation result."""
    success: bool
    symbols: List[Symbol] = field(default_factory=list)
    selected_symbol: Optional[Symbol] = None
    errors: List[str] = field(default_factory=list)
    message: Optional[str] = None


class SymbolNavigationUIManager:
    """
    Symbol navigation UI manager.
    
    Özellikler:
    - Symbol navigation
    - Symbol search
    - Symbol filtering
    - Symbol grouping
    - Symbol hierarchy
    - Go to symbol
    - Find references
    - Symbol preview
    - Symbol documentation
    - Symbol icons
    - Symbol scope filtering
    - Symbol type filtering
    - Quick navigation
    - Symbol outline
    - Symbol tree view
    - Symbol breadcrumbs
    - Symbol statistics
    """
    
    def __init__(self, config: Optional[SymbolNavigationConfig] = None):
        """
        Initialize symbol navigation UI manager.
        
        Args:
            config: Symbol navigation configuration
        """
        self.config = config or SymbolNavigationConfig()
        self.symbols: Dict[str, Symbol] = {}
        self.symbol_tree: Dict[str, List[str]] = {}
        self.search_history: List[str] = []
    
    def register_symbol(self, symbol: Symbol) -> SymbolNavigationResult:
        """
        Register a symbol.
        
        Args:
            symbol: Symbol to register
            
        Returns:
            SymbolNavigationResult: Registration result
        """
        result = SymbolNavigationResult(success=True)
        
        try:
            self.symbols[symbol.id] = symbol
            
            # Add to tree
            if symbol.parent:
                if symbol.parent not in self.symbol_tree:
                    self.symbol_tree[symbol.parent] = []
                self.symbol_tree[symbol.parent].append(symbol.id)
            
            result.symbols = self.get_all_symbols()
            result.message = f"Symbol '{symbol.name}' registered"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def unregister_symbol(self, symbol_id: str) -> SymbolNavigationResult:
        """
        Unregister a symbol.
        
        Args:
            symbol_id: Symbol ID
            
        Returns:
            SymbolNavigationResult: Unregistration result
        """
        result = SymbolNavigationResult(success=False)
        
        try:
            if symbol_id in self.symbols:
                symbol = self.symbols[symbol_id]
                del self.symbols[symbol_id]
                
                # Remove from tree
                if symbol.parent and symbol.parent in self.symbol_tree:
                    if symbol_id in self.symbol_tree[symbol.parent]:
                        self.symbol_tree[symbol.parent].remove(symbol_id)
                
                result.success = True
                result.symbols = self.get_all_symbols()
                result.message = f"Symbol '{symbol_id}' unregistered"
            else:
                result.errors.append("Symbol not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_symbol(self, symbol_id: str) -> Optional[Symbol]:
        """
        Get symbol by ID.
        
        Args:
            symbol_id: Symbol ID
            
        Returns:
            Optional[Symbol]: Symbol
        """
        return self.symbols.get(symbol_id)
    
    def get_all_symbols(self) -> List[Symbol]:
        """
        Get all symbols.
        
        Returns:
            List[Symbol]: All symbols
        """
        return list(self.symbols.values())
    
    def get_symbols_by_type(self, symbol_type: SymbolType) -> List[Symbol]:
        """
        Get symbols by type.
        
        Args:
            symbol_type: Symbol type
            
        Returns:
            List[Symbol]: Symbols
        """
        return [s for s in self.symbols.values() if s.type == symbol_type]
    
    def get_symbols_by_scope(self, scope: SymbolScope) -> List[Symbol]:
        """
        Get symbols by scope.
        
        Args:
            scope: Symbol scope
            
        Returns:
            List[Symbol]: Symbols
        """
        return [s for s in self.symbols.values() if s.scope == scope]
    
    def get_symbols_by_parent(self, parent_id: str) -> List[Symbol]:
        """
        Get symbols by parent.
        
        Args:
            parent_id: Parent ID
            
        Returns:
            List[Symbol]: Symbols
        """
        if parent_id in self.symbol_tree:
            return [self.symbols[sid] for sid in self.symbol_tree[parent_id] if sid in self.symbols]
        return []
    
    def search_symbols(self, query: str) -> SymbolNavigationResult:
        """
        Search symbols.
        
        Args:
            query: Search query
            
        Returns:
            SymbolNavigationResult: Search result
        """
        result = SymbolNavigationResult(success=True)
        
        if not query:
            result.symbols = self.get_all_symbols()
            result.message = f"Showing all {len(result.symbols)} symbols"
            return result
        
        # Add to history
        self._add_to_history(query)
        
        query_lower = query.lower()
        
        if self.config.enable_fuzzy_search:
            symbols = [s for s in self.symbols.values() if query_lower in s.name.lower()]
        else:
            symbols = [s for s in self.symbols.values() if s.name.lower() == query_lower]
        
        result.symbols = symbols
        result.message = f"Found {len(symbols)} symbols"
        
        return result
    
    def navigate_to_symbol(self, symbol_id: str) -> SymbolNavigationResult:
        """
        Navigate to symbol.
        
        Args:
            symbol_id: Symbol ID
            
        Returns:
            SymbolNavigationResult: Navigation result
        """
        result = SymbolNavigationResult(success=False)
        
        try:
            symbol = self.symbols.get(symbol_id)
            if symbol:
                result.success = True
                result.selected_symbol = symbol
                result.message = f"Navigated to '{symbol.name}'"
            else:
                result.errors.append("Symbol not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_symbol_hierarchy(self, symbol_id: str) -> List[Symbol]:
        """
        Get symbol hierarchy (path to root).
        
        Args:
            symbol_id: Symbol ID
            
        Returns:
            List[Symbol]: Hierarchy
        """
        hierarchy = []
        current_id = symbol_id
        
        while current_id:
            symbol = self.symbols.get(current_id)
            if symbol:
                hierarchy.insert(0, symbol)
                current_id = symbol.parent
            else:
                break
        
        return hierarchy
    
    def get_symbol_children(self, symbol_id: str) -> List[Symbol]:
        """
        Get symbol children.
        
        Args:
            symbol_id: Symbol ID
            
        Returns:
            List[Symbol]: Children
        """
        return self.get_symbols_by_parent(symbol_id)
    
    def filter_symbols_by_scope(self, symbols: List[Symbol]) -> List[Symbol]:
        """
        Filter symbols by scope based on config.
        
        Args:
            symbols: Symbols to filter
            
        Returns:
            List[Symbol]: Filtered symbols
        """
        filtered = []
        
        for symbol in symbols:
            if symbol.scope == SymbolScope.PUBLIC:
                filtered.append(symbol)
            elif symbol.scope == SymbolScope.PROTECTED and self.config.show_protected_symbols:
                filtered.append(symbol)
            elif symbol.scope == SymbolScope.INTERNAL and self.config.show_internal_symbols:
                filtered.append(symbol)
            elif symbol.scope == SymbolScope.PRIVATE and self.config.show_private_symbols:
                filtered.append(symbol)
        
        return filtered
    
    def get_search_history(self) -> List[str]:
        """
        Get search history.
        
        Returns:
            List[str]: Search history
        """
        return self.search_history
    
    def _add_to_history(self, query: str) -> None:
        """
        Add query to history.
        
        Args:
            query: Search query
        """
        # Remove duplicates
        self.search_history = [q for q in self.search_history if q != query]
        
        # Add to front
        self.search_history.insert(0, query)
        
        # Limit history
        if len(self.search_history) > 50:
            self.search_history = self.search_history[:50]
    
    def clear_history(self) -> None:
        """Clear search history."""
        self.search_history.clear()
    
    def update_config(self, config: SymbolNavigationConfig) -> SymbolNavigationResult:
        """
        Update symbol navigation configuration.
        
        Args:
            config: New configuration
            
        Returns:
            SymbolNavigationResult: Update result
        """
        result = SymbolNavigationResult(success=True)
        
        try:
            self.config = config
            result.message = "Config updated"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def get_config(self) -> SymbolNavigationConfig:
        """
        Get symbol navigation configuration.
        
        Returns:
            SymbolNavigationConfig: Configuration
        """
        return self.config


if __name__ == "__main__":
    # Basit test
    config = SymbolNavigationConfig()
    manager = SymbolNavigationUIManager(config)
    
    # Symbol kaydet
    symbol = Symbol(
        id="symbol_1",
        name="MyClass",
        type=SymbolType.CLASS,
        line=1,
        column=0
    )
    
    result = manager.register_symbol(symbol)
    
    print(f"Symbol registered: {result.message}")
    
    # Tüm symbol'ları al
    symbols = manager.get_all_symbols()
    
    print(f"Total symbols: {len(symbols)}")
    for symbol in symbols:
        print(f"  - {symbol.name} ({symbol.type.value})")
