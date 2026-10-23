"""
MuhammedAI Local Developer - Code Navigation
Code navigation ve symbol jumping özellikleri.
"""

from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field


@dataclass
class NavigationTarget:
    """Navigation hedefi."""
    file_path: str
    line: int
    column: int
    symbol_name: str
    symbol_type: str  # function, class, variable, etc.
    description: Optional[str] = None


@dataclass
class Reference:
    """Symbol referansı."""
    file_path: str
    line: int
    column: int
    context: str  # Surrounding code


@dataclass
class CallSite:
    """Call site bilgisi."""
    file_path: str
    line: int
    column: int
    caller_function: str
    callee_symbol: str


class CodeNavigator:
    """
    Code navigation engine.
    
    Özellikler:
    - Go to definition
    - Find references
    - Go to implementation
    - Symbol search
    - File outline
    - Call hierarchy
    """
    
    def __init__(self, codebase_index=None):
        """
        Args:
            codebase_index: CodebaseIndex instance
        """
        self.codebase_index = codebase_index
    
    def go_to_definition(
        self,
        file_path: str,
        line: int,
        column: int,
        symbol_name: str
    ) -> Optional[NavigationTarget]:
        """
        Go to definition.
        
        Args:
            file_path: Dosya yolu
            line: Satır numarası
            column: Sütun numarası
            symbol_name: Symbol adı
            
        Returns:
            Optional[NavigationTarget]: Definition hedefi
        """
        if not self.codebase_index or not symbol_name:
            return None
        
        try:
            self.codebase_index.index_project()
            
            # Symbol ara
            symbols = self.codebase_index.search_symbols(symbol_name)
            
            if not symbols:
                return None
            
            # İlk eşleşen symbol'ı al (definition)
            symbol = symbols[0]
            
            return NavigationTarget(
                file_path=symbol.file,
                line=symbol.line_start,
                column=0,
                symbol_name=symbol.name,
                symbol_type=symbol.type,
                description=symbol.signature
            )
        except Exception:
            return None
    
    def find_references(
        self,
        symbol_name: str,
        file_path: Optional[str] = None
    ) -> List[Reference]:
        """
        Find references.
        
        Args:
            symbol_name: Symbol adı
            file_path: Dosya yolu (opsiyonel - sadece bu dosyada ara)
            
        Returns:
            List[Reference]: Referans listesi
        """
        if not self.codebase_index or not symbol_name:
            return []
        
        references = []
        
        try:
            self.codebase_index.index_project()
            
            # Dependents'ı bul (bu symbol'ı kullanan dosyalar)
            if file_path:
                dependents = self.codebase_index.get_dependents(file_path)
            else:
                # Tüm dosyalarda ara
                dependents = []
                # Basit implementation: symbol search
                symbols = self.codebase_index.search_symbols(symbol_name)
                if symbols:
                    # Symbol'ın kendi dosyasını bul
                    symbol_file = symbols[0].file
                    dependents = self.codebase_index.get_dependents(symbol_file)
            
            # Referansları oluştur
            for dep_file in dependents:
                # Basit implementation: dosya içinde symbol ara
                # Gerçek implementation için grep kullanılabilir
                references.append(Reference(
                    file_path=dep_file,
                    line=1,  # Placeholder
                    column=0,
                    context=f"Reference in {dep_file}"
                ))
            
        except Exception:
            pass
        
        return references
    
    def go_to_implementation(
        self,
        symbol_name: str
    ) -> Optional[NavigationTarget]:
        """
        Go to implementation (interface'den concrete implementation'a).
        
        Args:
            symbol_name: Symbol adı
            
        Returns:
            Optional[NavigationTarget]: Implementation hedefi
        """
        if not self.codebase_index or not symbol_name:
            return None
        
        try:
            self.codebase_index.index_project()
            
            # Symbol ara
            symbols = self.codebase_index.search_symbols(symbol_name)
            
            if not symbols:
                return None
            
            # Implementation'ı bul (class/method)
            for symbol in symbols:
                if symbol.type in ["class", "method", "function"]:
                    return NavigationTarget(
                        file_path=symbol.file,
                        line=symbol.line_start,
                        column=0,
                        symbol_name=symbol.name,
                        symbol_type=symbol.type,
                        description=symbol.signature
                    )
            
            return None
        except Exception:
            return None
    
    def symbol_search(
        self,
        query: str,
        max_results: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Symbol search.
        
        Args:
            query: Arama sorgusu
            max_results: Maksimum sonuç
            
        Returns:
            List[Dict]: Symbol listesi
        """
        if not self.codebase_index or not query:
            return []
        
        try:
            self.codebase_index.index_project()
            
            symbols = self.codebase_index.search_symbols(query)
            
            results = []
            for symbol in symbols[:max_results]:
                results.append({
                    "name": symbol.name,
                    "type": symbol.type,
                    "file": symbol.file,
                    "line": symbol.line_start,
                    "signature": symbol.signature,
                    "parent_class": symbol.parent_class
                })
            
            return results
        except Exception:
            return []
    
    def get_file_outline(
        self,
        file_path: str
    ) -> List[Dict[str, Any]]:
        """
        File outline (classes, functions, methods).
        
        Args:
            file_path: Dosya yolu
            
        Returns:
            List[Dict]: Outline listesi
        """
        if not self.codebase_index:
            return []
        
        try:
            self.codebase_index.index_project()
            
            # Dosya içindeki sembolleri bul
            symbols = self.codebase_index.search_symbols("")
            
            # Dosyaya göre filtrele
            file_symbols = [s for s in symbols if s.file == file_path]
            
            # Outline oluştur
            outline = []
            for symbol in file_symbols:
                outline.append({
                    "name": symbol.name,
                    "type": symbol.type,
                    "line": symbol.line_start,
                    "end_line": symbol.line_end,
                    "signature": symbol.signature,
                    "parent_class": symbol.parent_class,
                    "docstring": symbol.docstring
                })
            
            # Line number'a göre sırala
            outline.sort(key=lambda x: x["line"])
            
            return outline
        except Exception:
            return []
    
    def get_call_hierarchy(
        self,
        symbol_name: str,
        direction: str = "callers"  # "callers" or "callees"
    ) -> List[CallSite]:
        """
        Call hierarchy.
        
        Args:
            symbol_name: Symbol adı
            direction: "callers" (bu symbol'ı çağıranlar) veya "callees" (bu symbol'ın çağırdıkları)
            
        Returns:
            List[CallSite]: Call site listesi
        """
        if not self.codebase_index or not symbol_name:
            return []
        
        call_sites = []
        
        try:
            self.codebase_index.index_project()
            
            if direction == "callers":
                # Bu symbol'ı çağıranları bul
                symbols = self.codebase_index.search_symbols(symbol_name)
                if symbols:
                    symbol_file = symbols[0].file
                    dependents = self.codebase_index.get_dependents(symbol_file)
                    
                    for dep_file in dependents:
                        call_sites.append(CallSite(
                            file_path=dep_file,
                            line=1,  # Placeholder
                            column=0,
                            caller_function="unknown",
                            callee_symbol=symbol_name
                        ))
            
            elif direction == "callees":
                # Bu symbol'ın çağırdıklarını bul
                # Basit implementation: symbol'ın içindeki function call'ları
                symbols = self.codebase_index.search_symbols(symbol_name)
                if symbols:
                    # Placeholder implementation
                    pass
            
        except Exception:
            pass
        
        return call_sites
    
    def get_breadcrumbs(
        self,
        file_path: str,
        line: int
    ) -> List[Dict[str, Any]]:
        """
        Breadcrumbs (current scope path).
        
        Args:
            file_path: Dosya yolu
            line: Satır numarası
            
        Returns:
            List[Dict]: Breadcrumb listesi
        """
        if not self.codebase_index:
            return []
        
        try:
            self.codebase_index.index_project()
            
            # Dosya outline'ı al
            outline = self.get_file_outline(file_path)
            
            # Line'a göre scope'u bul
            breadcrumbs = []
            current_scope = None
            
            for item in outline:
                if item["line"] <= line <= item["end_line"]:
                    if item["type"] == "class":
                        breadcrumbs.append({
                            "name": item["name"],
                            "type": "class",
                            "line": item["line"]
                        })
                    elif item["type"] in ["function", "method"]:
                        breadcrumbs.append({
                            "name": item["name"],
                            "type": item["type"],
                            "line": item["line"],
                            "parent_class": item.get("parent_class")
                        })
            
            return breadcrumbs
        except Exception:
            return []


if __name__ == "__main__":
    # Basit test
    from app.ai.codebase_index import CodebaseIndex
    
    codebase_index = CodebaseIndex()
    navigator = CodeNavigator(codebase_index=codebase_index)
    
    # Symbol search
    results = navigator.symbol_search("AgentLoop")
    print(f"Symbol search results: {len(results)}")
    for result in results[:5]:
        print(f"  - {result['name']} ({result['type']}) in {result['file']}")
