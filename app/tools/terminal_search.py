"""
MuhammedAI Local Developer - Terminal Search
Terminal search management engine for code editor.
"""

from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import re


class SearchMode(Enum):
    """Search mode."""
    TEXT = "text"
    REGEX = "regex"
    FUZZY = "fuzzy"


class SearchScope(Enum):
    """Search scope."""
    CURRENT = "current"
    ALL = "all"
    HISTORY = "history"
    SCROLLBACK = "scrollback"


class SearchOption(Enum):
    """Search option."""
    CASE_SENSITIVE = "case_sensitive"
    CASE_INSENSITIVE = "case_insensitive"
    WHOLE_WORD = "whole_word"
    MATCH_WORD = "match_word"
    HIGHLIGHT = "highlight"


@dataclass
class SearchConfig:
    """Search configuration."""
    mode: SearchMode = SearchMode.TEXT
    scope: SearchScope = SearchScope.ALL
    case_sensitive: bool = False
    whole_word: bool = False
    enable_highlighting: bool = True
    enable_history: bool = True
    max_results: int = 100
    show_notifications: bool = True


@dataclass
class SearchResult:
    """Search result."""
    id: str
    content: str
    line_number: int
    start_index: int
    end_index: int
    panel_id: Optional[str] = None
    timestamp: Optional[str] = None


@dataclass
class SearchOutput:
    """Search output."""
    success: bool
    message: Optional[str] = None
    errors: List[str] = field(default_factory=list)
    results: List[SearchResult] = field(default_factory=list)
    count: int = 0
    query: Optional[str] = None


class TerminalSearchEngine:
    """
    Terminal search management engine.
    
    Özellikler:
    - Search text
    - Search regex
    - Search fuzzy
    - Case sensitive/insensitive
    - Whole word search
    - Search in scrollback
    - Search in history
    - Search navigation
    - Search highlighting
    - Search filters
    - Search history
    - Replace search
    """
    
    def __init__(self, config: Optional[SearchConfig] = None):
        """Initialize terminal search engine."""
        self.config = config or SearchConfig()
        self.search_history: List[Dict[str, Any]] = []
        self._result_counter = 0
    
    def search(
        self,
        query: str,
        content: List[str],
        panel_id: Optional[str] = None,
        options: Optional[List[SearchOption]] = None
    ) -> SearchOutput:
        """
        Ara.
        
        Args:
            query: Arama sorgusu
            content: İçerik listesi
            panel_id: Panel ID
            options: Arama seçenekleri
            
        Returns:
            SearchOutput: Arama sonucu
        """
        output = SearchOutput(success=False)
        output.query = query
        
        try:
            results = []
            
            for line_number, line in enumerate(content, start=1):
                matches = self._find_matches(query, line, options)
                
                for start_index, end_index in matches:
                    result_id = f"search_{self._result_counter}"
                    self._result_counter += 1
                    
                    result = SearchResult(
                        id=result_id,
                        content=line,
                        line_number=line_number,
                        start_index=start_index,
                        end_index=end_index,
                        panel_id=panel_id,
                        timestamp=self._get_timestamp()
                    )
                    
                    results.append(result)
                    
                    if len(results) >= self.config.max_results:
                        break
                
                if len(results) >= self.config.max_results:
                    break
            
            # Add to history
            if self.config.enable_history:
                self.search_history.append({
                    "query": query,
                    "mode": self.config.mode.value,
                    "scope": self.config.scope.value,
                    "results_count": len(results),
                    "timestamp": self._get_timestamp()
                })
            
            output.success = True
            output.results = results
            output.count = len(results)
            output.message = f"Found {len(results)} matches for '{query}'"
        
        except Exception as e:
            output.errors.append(f"Error: {str(e)}")
        
        return output
    
    def search_regex(
        self,
        pattern: str,
        content: List[str],
        panel_id: Optional[str] = None
    ) -> SearchOutput:
        """
        Regex ile ara.
        
        Args:
            pattern: Regex deseni
            content: İçerik listesi
            panel_id: Panel ID
            
        Returns:
            SearchOutput: Arama sonucu
        """
        output = SearchOutput(success=False)
        output.query = pattern
        
        try:
            results = []
            regex = re.compile(pattern)
            
            for line_number, line in enumerate(content, start=1):
                matches = list(regex.finditer(line))
                
                for match in matches:
                    result_id = f"search_{self._result_counter}"
                    self._result_counter += 1
                    
                    result = SearchResult(
                        id=result_id,
                        content=line,
                        line_number=line_number,
                        start_index=match.start(),
                        end_index=match.end(),
                        panel_id=panel_id,
                        timestamp=self._get_timestamp()
                    )
                    
                    results.append(result)
                    
                    if len(results) >= self.config.max_results:
                        break
                
                if len(results) >= self.config.max_results:
                    break
            
            # Add to history
            if self.config.enable_history:
                self.search_history.append({
                    "query": pattern,
                    "mode": SearchMode.REGEX.value,
                    "results_count": len(results),
                    "timestamp": self._get_timestamp()
                })
            
            output.success = True
            output.results = results
            output.count = len(results)
            output.message = f"Found {len(results)} regex matches"
        
        except Exception as e:
            output.errors.append(f"Error: {str(e)}")
        
        return output
    
    def search_whole_word(
        self,
        word: str,
        content: List[str],
        panel_id: Optional[str] = None
    ) -> SearchOutput:
        """
        Tam kelime ara.
        
        Args:
            word: Kelime
            content: İçerik listesi
            panel_id: Panel ID
            
        Returns:
            SearchOutput: Arama sonucu
        """
        output = SearchOutput(success=False)
        output.query = word
        
        try:
            results = []
            pattern = r'\b' + re.escape(word) + r'\b'
            regex = re.compile(pattern, re.IGNORECASE if not self.config.case_sensitive else 0)
            
            for line_number, line in enumerate(content, start=1):
                matches = [(m.start(), m.end()) for m in regex.finditer(line)]
                
                for start_index, end_index in matches:
                    result_id = f"search_{self._result_counter}"
                    self._result_counter += 1
                    
                    result = SearchResult(
                        id=result_id,
                        content=line,
                        line_number=line_number,
                        start_index=start_index,
                        end_index=end_index,
                        panel_id=panel_id,
                        timestamp=self._get_timestamp()
                    )
                    
                    results.append(result)
                    
                    if len(results) >= self.config.max_results:
                        break
                
                if len(results) >= self.config.max_results:
                    break
            
            # Add to history
            if self.config.enable_history:
                self.search_history.append({
                    "query": word,
                    "mode": SearchMode.TEXT.value,
                    "whole_word": True,
                    "results_count": len(results),
                    "timestamp": self._get_timestamp()
                })
            
            output.success = True
            output.results = results
            output.count = len(results)
            output.message = f"Found {len(results)} whole word matches"
        
        except Exception as e:
            output.errors.append(f"Error: {str(e)}")
        
        return output
    
    def navigate_next(self, current_index: int) -> Optional[SearchResult]:
        """
        Sonraki sonucu git.
        
        Args:
            current_index: Mevcut indeks
            
        Returns:
            Optional[SearchResult]: Sonraki sonuç
        """
        # This would be implemented with actual result storage
        return None
    
    def navigate_previous(self, current_index: int) -> Optional[SearchResult]:
        """
        Önceki sonucu git.
        
        Args:
            current_index: Mevcut indeks
            
        Returns:
            Optional[SearchResult]: Önceki sonuç
        """
        # This would be implemented with actual result storage
        return None
    
    def get_search_history(self) -> List[Dict[str, Any]]:
        """
        Arama geçmişini al.
        
        Returns:
            List[Dict[str, Any]]: Geçmiş
        """
        return self.search_history
    
    def clear_history(self) -> SearchOutput:
        """
        Geçmişi temizle.
        
        Returns:
            SearchOutput: Temizleme sonucu
        """
        output = SearchOutput(success=False)
        
        try:
            self.search_history.clear()
            output.success = True
            output.message = "Search history cleared"
        
        except Exception as e:
            output.errors.append(f"Error: {str(e)}")
        
        return output
    
    def update_config(self, config: SearchConfig) -> SearchOutput:
        """
        Konfigürasyon güncelle.
        
        Args:
            config: Yeni konfigürasyon
            
        Returns:
            SearchOutput: Güncelleme sonucu
        """
        output = SearchOutput(success=False)
        
        try:
            self.config = config
            output.success = True
            output.message = "Config updated"
        
        except Exception as e:
            output.errors.append(f"Error: {str(e)}")
        
        return output
    
    def get_config(self) -> SearchConfig:
        """
        Konfigürasyon al.
        
        Returns:
            SearchConfig: Konfigürasyon
        """
        return self.config
    
    def _find_matches(
        self,
        query: str,
        line: str,
        options: Optional[List[SearchOption]] = None
    ) -> List[Tuple[int, int]]:
        """
        Eşleşmeleri bul.
        
        Args:
            query: Arama sorgusu
            line: Satır
            options: Arama seçenekleri
            
        Returns:
            List[Tuple[int, int]]: Eşleşmeler (start, end)
        """
        matches = []
        search_line = line
        search_query = query
        
        # Case sensitivity
        case_sensitive = self.config.case_sensitive
        if options:
            if SearchOption.CASE_SENSITIVE in options:
                case_sensitive = True
            elif SearchOption.CASE_INSENSITIVE in options:
                case_sensitive = False
        
        if not case_sensitive:
            search_line = line.lower()
            search_query = query.lower()
        
        # Whole word
        whole_word = self.config.whole_word
        if options and SearchOption.WHOLE_WORD in options:
            whole_word = True
        
        if whole_word:
            pattern = r'\b' + re.escape(search_query) + r'\b'
            regex = re.compile(pattern)
            for match in regex.finditer(search_line):
                matches.append((match.start(), match.end()))
        else:
            start = 0
            while True:
                index = search_line.find(search_query, start)
                if index == -1:
                    break
                matches.append((index, index + len(search_query)))
                start = index + 1
        
        return matches
    
    def _get_timestamp(self) -> str:
        """
        Zaman damgası al.
        
        Returns:
            str: ISO format zaman damgası
        """
        return datetime.now().isoformat()


if __name__ == "__main__":
    # Basit test
    engine = TerminalSearchEngine()
    
    print("Terminal Search Engine initialized")
    print(f"Mode: {engine.config.mode.value}")
