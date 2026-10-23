"""
MuhammedAI Local Developer - Diff Search
Diff search engine for code editor.
"""

from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from enum import Enum
import re


class SearchMode(Enum):
    """Search mode."""
    TEXT = "text"
    REGEX = "regex"
    FUZZY = "fuzzy"
    CASE_SENSITIVE = "case_sensitive"
    CASE_INSENSITIVE = "case_insensitive"
    WHOLE_WORD = "whole_word"


class SearchScope(Enum):
    """Search scope."""
    CURRENT_FILE = "current_file"
    ALL_FILES = "all_files"
    SELECTED_TEXT = "selected_text"
    VISIBLE_AREA = "visible_area"
    HUNKS_ONLY = "hunks_only"


class SearchDirection(Enum):
    """Search direction."""
    NEXT = "next"
    PREVIOUS = "previous"
    ALL = "all"
    FIRST = "first"
    LAST = "last"


class SearchAction(Enum):
    """Search action."""
    SEARCH = "search"
    REPLACE = "replace"
    REPLACE_ALL = "replace_all"
    FIND_NEXT = "find_next"
    FIND_PREVIOUS = "find_previous"
    CLEAR = "clear"


@dataclass
class SearchResult:
    """Search result."""
    line_number: int
    start_position: int
    end_position: int
    matched_text: str
    file_path: str
    context_before: str = ""
    context_after: str = ""


@dataclass
class ReplaceResult:
    """Replace result."""
    line_number: int
    original_text: str
    replaced_text: str
    file_path: str
    was_replaced: bool = True


@dataclass
class SearchConfig:
    """Search configuration."""
    mode: SearchMode = SearchMode.TEXT
    scope: SearchScope = SearchScope.CURRENT_FILE
    case_sensitive: bool = False
    whole_word: bool = False
    regex: bool = False
    wrap_around: bool = True
    highlight_matches: bool = True
    show_context: bool = True
    context_lines: int = 2
    max_results: int = 1000


@dataclass
class SearchEngineResult:
    """Search engine result."""
    success: bool
    action: Optional[str] = None
    message: Optional[str] = None
    errors: List[str] = field(default_factory=list)
    results: List[SearchResult] = field(default_factory=list)
    replace_results: List[ReplaceResult] = field(default_factory=list)
    total_matches: int = 0
    total_replaced: int = 0
    search_query: Optional[str] = None


class DiffSearchEngine:
    """
    Diff search engine.
    
    Özellikler:
    - Search in diff
    - Regex search
    - Case-sensitive search
    - Replace in diff
    - Replace all
    - Find next/previous
    - Multiple search modes
    - Multiple search scopes
    - Search history
    - Context display
    - Match highlighting
    - Wrap-around support
    - Whole word matching
    - Fuzzy search
    - Search statistics
    - Configuration management
    """
    
    def __init__(self, config: Optional[SearchConfig] = None):
        """Initialize diff search engine."""
        self.config = config or SearchConfig()
        self.search_results: List[SearchResult] = []
        self.replace_results: List[ReplaceResult] = []
        self.search_history: List[Tuple[str, str]] = []  # (action, query)
        self.current_index: int = -1
        self.lines: List[str] = []
        self.file_path: str = ""
    
    def search(
        self,
        query: str,
        direction: SearchDirection = SearchDirection.ALL
    ) -> SearchEngineResult:
        """
        Ara.
        
        Args:
            query: Arama sorgusu
            direction: Arama yönü
            
        Returns:
            SearchEngineResult: Arama sonucu
        """
        result = SearchEngineResult(success=False)
        result.action = SearchAction.SEARCH.value
        result.search_query = query
        
        try:
            if not query:
                result.errors.append("Search query is empty")
                return result
            
            if not self.lines:
                result.errors.append("No content to search")
                return result
            
            self.search_results.clear()
            
            # Arama yap
            for i, line in enumerate(self.lines):
                matches = self._find_matches(line, query)
                
                for match in matches:
                    search_result = SearchResult(
                        line_number=i + 1,
                        start_position=match.start(),
                        end_position=match.end(),
                        matched_text=match.group(),
                        file_path=self.file_path
                    )
                    
                    # Bağlam ekle
                    if self.config.show_context:
                        search_result.context_before = self._get_context(i, -1)
                        search_result.context_after = self._get_context(i, 1)
                    
                    self.search_results.append(search_result)
            
            # Sonuçları sınırla
            if len(self.search_results) > self.config.max_results:
                self.search_results = self.search_results[:self.config.max_results]
            
            result.results = self.search_results
            result.total_matches = len(self.search_results)
            result.success = True
            result.message = f"Found {len(self.search_results)} matches"
            
            self.search_history.append(("search", query))
            self.current_index = 0 if self.search_results else -1
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def replace(
        self,
        search_query: str,
        replace_text: str,
        line_number: Optional[int] = None
    ) -> SearchEngineResult:
        """
        Değiştir.
        
        Args:
            search_query: Arama sorgusu
            replace_text: Değiştirme metni
            line_number: Satır numarası (opsiyonel)
            
        Returns:
            SearchEngineResult: Değiştirme sonucu
        """
        result = SearchEngineResult(success=False)
        result.action = SearchAction.REPLACE.value
        result.search_query = search_query
        
        try:
            if not search_query:
                result.errors.append("Search query is empty")
                return result
            
            if not self.lines:
                result.errors.append("No content to replace")
                return result
            
            self.replace_results.clear()
            
            # Değiştirme yap
            for i, line in enumerate(self.lines):
                if line_number is not None and i + 1 != line_number:
                    continue
                
                matches = self._find_matches(line, search_query)
                
                if matches:
                    replaced_line = line
                    for match in reversed(matches):
                        replaced_line = replaced_line[:match.start()] + replace_text + replaced_line[match.end():]
                    
                    replace_result = ReplaceResult(
                        line_number=i + 1,
                        original_text=line,
                        replaced_text=replaced_line,
                        file_path=self.file_path,
                        was_replaced=True
                    )
                    
                    self.replace_results.append(replace_result)
                    
                    # Satırı güncelle
                    self.lines[i] = replaced_line
            
            result.replace_results = self.replace_results
            result.total_replaced = len(self.replace_results)
            result.success = True
            result.message = f"Replaced {len(self.replace_results)} occurrences"
            
            self.search_history.append(("replace", search_query))
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def replace_all(
        self,
        search_query: str,
        replace_text: str
    ) -> SearchEngineResult:
        """
        Tümünü değiştir.
        
        Args:
            search_query: Arama sorgusu
            replace_text: Değiştirme metni
            
        Returns:
            SearchEngineResult: Değiştirme sonucu
        """
        result = SearchEngineResult(success=False)
        result.action = SearchAction.REPLACE_ALL.value
        result.search_query = search_query
        
        try:
            # Tüm satırlarda değiştir
            if not search_query:
                result.errors.append("Search query is empty")
                return result
            
            if not self.lines:
                result.errors.append("No content to replace")
                return result
            
            self.replace_results.clear()
            
            # Değiştirme yap
            for i, line in enumerate(self.lines):
                matches = self._find_matches(line, search_query)
                
                if matches:
                    replaced_line = line
                    for match in reversed(matches):
                        replaced_line = replaced_line[:match.start()] + replace_text + replaced_line[match.end():]
                    
                    replace_result = ReplaceResult(
                        line_number=i + 1,
                        original_text=line,
                        replaced_text=replaced_line,
                        file_path=self.file_path,
                        was_replaced=True
                    )
                    
                    self.replace_results.append(replace_result)
                    
                    # Satırı güncelle
                    self.lines[i] = replaced_line
            
            result.replace_results = self.replace_results
            result.total_replaced = len(self.replace_results)
            result.success = True
            result.message = f"Replaced {len(self.replace_results)} occurrences"
            
            self.search_history.append(("replace_all", search_query))
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def find_next(self) -> SearchEngineResult:
        """
        Sonrakini bul.
        
        Returns:
            SearchEngineResult: Bulma sonucu
        """
        result = SearchEngineResult(success=False)
        result.action = SearchAction.FIND_NEXT.value
        
        try:
            if not self.search_results:
                result.errors.append("No search results available")
                return result
            
            self.current_index = (self.current_index + 1) % len(self.search_results)
            
            result.results = [self.search_results[self.current_index]]
            result.total_matches = len(self.search_results)
            result.success = True
            result.message = f"Found match {self.current_index + 1}/{len(self.search_results)}"
            
            self.search_history.append(("find_next", str(self.current_index)))
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def find_previous(self) -> SearchEngineResult:
        """
        Öncekini bul.
        
        Returns:
            SearchEngineResult: Bulma sonucu
        """
        result = SearchEngineResult(success=False)
        result.action = SearchAction.FIND_PREVIOUS.value
        
        try:
            if not self.search_results:
                result.errors.append("No search results available")
                return result
            
            self.current_index = (self.current_index - 1) % len(self.search_results)
            
            result.results = [self.search_results[self.current_index]]
            result.total_matches = len(self.search_results)
            result.success = True
            result.message = f"Found match {self.current_index + 1}/{len(self.search_results)}"
            
            self.search_history.append(("find_previous", str(self.current_index)))
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def clear_results(self) -> SearchEngineResult:
        """
        Sonuçları temizle.
        
        Returns:
            SearchEngineResult: Temizleme sonucu
        """
        result = SearchEngineResult(success=False)
        result.action = SearchAction.CLEAR.value
        
        try:
            self.search_results.clear()
            self.replace_results.clear()
            self.current_index = -1
            
            result.success = True
            result.message = "Search results cleared"
            
            self.search_history.append(("clear", "all"))
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def set_content(self, lines: List[str], file_path: str = ""):
        """
        İçerik ayarla.
        
        Args:
            lines: Satır listesi
            file_path: Dosya yolu
        """
        self.lines = lines
        self.file_path = file_path
    
    def get_results(self) -> List[SearchResult]:
        """
        Sonuçları al.
        
        Returns:
            List[SearchResult]: Sonuç listesi
        """
        return self.search_results
    
    def get_current_match(self) -> Optional[SearchResult]:
        """
        Mevcut eşleşmeyi al.
        
        Returns:
            Optional[SearchResult]: Eşleşme bilgisi
        """
        if self.search_results and 0 <= self.current_index < len(self.search_results):
            return self.search_results[self.current_index]
        return None
    
    def get_search_history(self) -> List[Tuple[str, str]]:
        """
        Arama geçmişini al.
        
        Returns:
            List[Tuple[str, str]]: Geçmiş
        """
        return self.search_history
    
    def clear_history(self) -> SearchEngineResult:
        """
        Geçmişi temizle.
        
        Returns:
            SearchEngineResult: Temizleme sonucu
        """
        result = SearchEngineResult(success=False)
        
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
            "total_matches": len(self.search_results),
            "total_replaced": len(self.replace_results),
            "current_index": self.current_index,
            "total_lines": len(self.lines),
            "search_history_count": len(self.search_history)
        }
    
    def update_config(self, config: SearchConfig) -> SearchEngineResult:
        """
        Konfigürasyon güncelle.
        
        Args:
            config: Yeni konfigürasyon
            
        Returns:
            SearchEngineResult: Güncelleme sonucu
        """
        result = SearchEngineResult(success=False)
        
        try:
            self.config = config
            result.success = True
            result.message = "Config updated"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_config(self) -> SearchConfig:
        """
        Konfigürasyon al.
        
        Returns:
            SearchConfig: Konfigürasyon
        """
        return self.config
    
    def _find_matches(self, line: str, query: str) -> List:
        """Eşleşmeleri bul."""
        if self.config.regex or self.config.mode == SearchMode.REGEX:
            try:
                flags = 0 if self.config.case_sensitive else re.IGNORECASE
                return list(re.finditer(query, line, flags))
            except re.error:
                return []
        
        # Basit string matching için regex kullan
        if self.config.case_sensitive:
            if self.config.whole_word:
                pattern = r'\b' + re.escape(query) + r'\b'
                return list(re.finditer(pattern, line))
            else:
                pattern = re.escape(query)
                return list(re.finditer(pattern, line))
        else:
            if self.config.whole_word:
                pattern = r'\b' + re.escape(query) + r'\b'
                return list(re.finditer(pattern, line, re.IGNORECASE))
            else:
                pattern = re.escape(query)
                return list(re.finditer(pattern, line, re.IGNORECASE))
    
    def _get_context(self, line_index: int, direction: int) -> str:
        """Bağlam al."""
        context_lines = []
        for i in range(1, self.config.context_lines + 1):
            target_index = line_index + (i * direction)
            if 0 <= target_index < len(self.lines):
                context_lines.append(self.lines[target_index])
        
        return "\n".join(context_lines)


if __name__ == "__main__":
    # Basit test
    engine = DiffSearchEngine()
    
    lines = ["Line 1 with test", "Line 2 with test", "Line 3"]
    engine.set_content(lines, "test.txt")
    
    result = engine.search("test")
    print(f"Search: {result.success}")
    print(f"Total matches: {result.total_matches}")
