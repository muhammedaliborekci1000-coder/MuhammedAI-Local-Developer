"""
MuhammedAI Local Developer - Semantic Search
Semantic search for code and documentation.
"""

import ast
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from enum import Enum


class SearchType(Enum):
    """Search type."""
    CODE = "code"
    SYMBOL = "symbol"
    DOCUMENTATION = "documentation"
    FILE = "file"


class SearchScope(Enum):
    """Search scope."""
    PROJECT = "project"
    FILE = "file"
    DIRECTORY = "directory"


@dataclass
class SearchResult:
    """Search result."""
    file_path: str
    line: int
    column: int
    score: float
    content: str
    context: Optional[str] = None
    symbol_name: Optional[str] = None
    symbol_type: Optional[str] = None


@dataclass
class SemanticSearchResult:
    """Semantic search result."""
    success: bool
    results: List[SearchResult] = field(default_factory=list)
    query: Optional[str] = None
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    message: Optional[str] = None


class SemanticSearchEngine:
    """
    Semantic search engine.
    
    Özellikler:
    - Semantic code search
    - Natural language queries
    - Code similarity search
    - Symbol search
    - Documentation search
    - Ranking and scoring
    - Context-aware results
    """
    
    def __init__(self, project_root: Optional[str] = None):
        """
        Args:
            project_root: Project root directory
        """
        self.project_root = project_root
        self.index: Dict[str, List[Dict]] = {}
        self._build_index()
    
    def search(
        self,
        query: str,
        search_type: SearchType = SearchType.CODE,
        scope: SearchScope = SearchScope.PROJECT,
        max_results: int = 10
    ) -> SemanticSearchResult:
        """
        Semantic search.
        
        Args:
            query: Arama sorgusu
            search_type: Search tipi
            scope: Search scope
            max_results: Max sonuç sayısı
            
        Returns:
            SemanticSearchResult: Search sonucu
        """
        result = SemanticSearchResult(success=False)
        result.query = query
        
        try:
            # Query'den keywords çıkar
            keywords = self._extract_keywords(query)
            
            # Index'te ara
            matched_results = []
            
            for file_path, items in self.index.items():
                for item in items:
                    # Keyword matching
                    score = self._calculate_score(keywords, item)
                    
                    if score > 0:
                        search_result = SearchResult(
                            file_path=file_path,
                            line=item.get("line", 0),
                            column=item.get("column", 0),
                            score=score,
                            content=item.get("content", ""),
                            context=item.get("context"),
                            symbol_name=item.get("name"),
                            symbol_type=item.get("type")
                        )
                        matched_results.append(search_result)
            
            # Score'a göre sırala
            matched_results.sort(key=lambda r: r.score, reverse=True)
            
            # Limit
            matched_results = matched_results[:max_results]
            
            result.success = True
            result.results = matched_results
            result.message = f"Found {len(matched_results)} results"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def search_symbols(
        self,
        query: str,
        symbol_type: Optional[str] = None,
        max_results: int = 10
    ) -> SemanticSearchResult:
        """
        Symbol search.
        
        Args:
            query: Arama sorgusu
            symbol_type: Symbol tipi (function, class, variable)
            max_results: Max sonuç sayısı
            
        Returns:
            SemanticSearchResult: Search sonucu
        """
        result = SemanticSearchResult(success=False)
        result.query = query
        
        try:
            keywords = self._extract_keywords(query)
            matched_results = []
            
            for file_path, items in self.index.items():
                for item in items:
                    # Symbol type filtresi
                    if symbol_type and item.get("type") != symbol_type:
                        continue
                    
                    # Keyword matching
                    score = self._calculate_score(keywords, item)
                    
                    if score > 0:
                        search_result = SearchResult(
                            file_path=file_path,
                            line=item.get("line", 0),
                            column=item.get("column", 0),
                            score=score,
                            content=item.get("content", ""),
                            symbol_name=item.get("name"),
                            symbol_type=item.get("type")
                        )
                        matched_results.append(search_result)
            
            matched_results.sort(key=lambda r: r.score, reverse=True)
            matched_results = matched_results[:max_results]
            
            result.success = True
            result.results = matched_results
            result.message = f"Found {len(matched_results)} symbols"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def search_files(
        self,
        query: str,
        max_results: int = 10
    ) -> SemanticSearchResult:
        """
        File search.
        
        Args:
            query: Arama sorgusu
            max_results: Max sonuç sayısı
            
        Returns:
            SemanticSearchResult: Search sonucu
        """
        result = SemanticSearchResult(success=False)
        result.query = query
        
        try:
            if not self.project_root:
                result.errors.append("Project root not set")
                return result
            
            keywords = self._extract_keywords(query)
            matched_files = []
            
            # Dosya adlarında ara
            for file_path in Path(self.project_root).rglob("*.py"):
                file_name = file_path.name.lower()
                
                # Keyword matching
                score = sum(1 for kw in keywords if kw in file_name)
                
                if score > 0:
                    search_result = SearchResult(
                        file_path=str(file_path),
                        line=0,
                        column=0,
                        score=score,
                        content=file_name,
                        symbol_name=file_name,
                        symbol_type="file"
                    )
                    matched_files.append(search_result)
            
            matched_files.sort(key=lambda r: r.score, reverse=True)
            matched_files = matched_files[:max_results]
            
            result.success = True
            result.results = matched_files
            result.message = f"Found {len(matched_files)} files"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def _build_index(self):
        """Index oluştur."""
        if not self.project_root:
            return
        
        for file_path in Path(self.project_root).rglob("*.py"):
            try:
                content = file_path.read_text(encoding='utf-8')
                lines = content.splitlines()
                
                # AST parse
                tree = ast.parse(content)
                
                # Index'e ekle
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        self.index.setdefault(str(file_path), []).append({
                            "name": node.name,
                            "type": "function",
                            "line": node.lineno,
                            "column": node.col_offset or 0,
                            "content": lines[node.lineno - 1] if node.lineno <= len(lines) else "",
                            "context": self._get_context(lines, node.lineno)
                        })
                    elif isinstance(node, ast.ClassDef):
                        self.index.setdefault(str(file_path), []).append({
                            "name": node.name,
                            "type": "class",
                            "line": node.lineno,
                            "column": node.col_offset or 0,
                            "content": lines[node.lineno - 1] if node.lineno <= len(lines) else "",
                            "context": self._get_context(lines, node.lineno)
                        })
            
            except Exception:
                pass
    
    def _extract_keywords(self, query: str) -> List[str]:
        """Query'den keywords çıkar."""
        # Basit keyword extraction
        keywords = query.lower().split()
        # Stop words kaldır
        stop_words = {"the", "a", "an", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "do", "does", "did", "will", "would", "could", "should", "may", "might", "must", "shall", "can", "need", "dare", "ought", "used", "to", "of", "in", "for", "on", "with", "at", "by", "from", "as", "into", "through", "during", "before", "after", "above", "below", "between", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "just"}
        keywords = [kw for kw in keywords if kw not in stop_words and len(kw) > 2]
        return keywords
    
    def _calculate_score(self, keywords: List[str], item: Dict) -> float:
        """Score hesapla."""
        score = 0.0
        content = item.get("content", "").lower()
        name = item.get("name", "").lower()
        
        for keyword in keywords:
            # Name'de match
            if keyword in name:
                score += 2.0
            
            # Content'te match
            if keyword in content:
                score += 1.0
        
        return score
    
    def _get_context(self, lines: List[str], line: int) -> str:
        """Context al."""
        start = max(0, line - 3)
        end = min(len(lines), line + 2)
        return "\n".join(lines[start:end])


if __name__ == "__main__":
    # Basit test
    engine = SemanticSearchEngine(project_root=".")
    
    result = engine.search("function")
    print(f"Search result: {result.success}")
    print(f"Results: {len(result.results)}")
