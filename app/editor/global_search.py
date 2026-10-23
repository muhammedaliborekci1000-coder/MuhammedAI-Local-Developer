"""
MuhammedAI Local Developer - Global Search
Global search engine for code editor.
"""

from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from enum import Enum


class SearchScope(Enum):
    """Search scope."""
    CURRENT_FILE = "current_file"
    OPEN_FILES = "open_files"
    PROJECT = "project"
    WORKSPACE = "workspace"


class SearchMode(Enum):
    """Search mode."""
    PLAIN_TEXT = "plain_text"
    REGEX = "regex"
    CASE_SENSITIVE = "case_sensitive"
    CASE_INSENSITIVE = "case_insensitive"
    WHOLE_WORD = "whole_word"
    FUZZY = "fuzzy"


class SearchAction(Enum):
    """Search action."""
    SEARCH = "search"
    REPLACE = "replace"
    REPLACE_ALL = "replace_all"
    FIND_NEXT = "find_next"
    FIND_PREVIOUS = "find_previous"
    FILTER = "filter"
    CLEAR = "clear"


class SearchContext(Enum):
    """Search context."""
    CODE = "code"
    COMMENTS = "comments"
    STRINGS = "strings"
    ALL = "all"


@dataclass
class SearchResult:
    """Search result."""
    file_path: str
    line_number: int
    column: int
    match_text: str
    context_before: str = ""
    context_after: str = ""
    is_selected: bool = False


@dataclass
class GlobalSearchConfig:
    """Global search configuration."""
    scope: SearchScope = SearchScope.PROJECT
    mode: SearchMode = SearchMode.PLAIN_TEXT
    context: SearchContext = SearchContext.ALL
    include_hidden: bool = False
    max_results: int = 1000
    show_context: bool = True
    context_lines: int = 2
    highlight_matches: bool = True


@dataclass
class GlobalSearchResult:
    """Global search result."""
    success: bool
    action: Optional[str] = None
    query: str = ""
    results: List[SearchResult] = field(default_factory=list)
    total_matches: int = 0
    files_searched: int = 0
    errors: List[str] = field(default_factory=list)
    message: Optional[str] = None
    total_files_filtered: int = 0


class GlobalSearchEngine:
    """
    Global search engine.
    
    Özellikler:
    - Global text search
    - Multi-file search
    - Search scope control
    - Search modes (plain, regex, fuzzy)
    - Case sensitivity
    - Whole word search
    - Search context (code, comments, strings)
    - Result highlighting
    - Context display
    - Result filtering
    - Search history
    - Quick search
    - Replace functionality
    - File filtering
    - Extension filtering
    - Directory filtering
    - Pattern matching
    - Result navigation
    - Search statistics
    - Find next/previous
    """
    
    def __init__(self, config: Optional[GlobalSearchConfig] = None):
        """Initialize global search engine."""
        self.config = config or GlobalSearchConfig()
        self.search_history: List[str] = []
        self.current_results: List[SearchResult] = []
        self.current_index: int = -1
        self.file_filters: Optional[List[str]] = None
        self.extension_filters: Optional[List[str]] = None
        self.directory_filters: Optional[List[str]] = None
    
    def search(
        self,
        query: str,
        files: Optional[Dict[str, str]] = None
    ) -> GlobalSearchResult:
        """
        Global search yap.
        
        Args:
            query: Arama sorgusu
            files: Dosya içeriği (path -> content)
            
        Returns:
            GlobalSearchResult: Arama sonucu
        """
        result = GlobalSearchResult(success=False)
        result.action = SearchAction.SEARCH.value
        result.query = query
        
        try:
            if not query:
                result.errors.append("Query cannot be empty")
                return result
            
            if not files:
                result.errors.append("No files to search")
                return result
            
            # Geçmişe ekle
            if query not in self.search_history:
                self.search_history.append(query)
            
            results = []
            files_searched = 0
            
            for file_path, content in files.items():
                # Dosya filtrelerini uygula
                if self.file_filters and not any(f in file_path for f in self.file_filters):
                    continue
                if self.extension_filters:
                    import os
                    ext = os.path.splitext(file_path)[1].lower()
                    if ext not in self.extension_filters:
                        continue
                if self.directory_filters:
                    if not any(d in file_path for d in self.directory_filters):
                        continue
                
                file_results = self._search_in_file(query, file_path, content)
                results.extend(file_results)
                files_searched += 1
            
            # Max results limit
            if len(results) > self.config.max_results:
                results = results[:self.config.max_results]
            
            self.current_results = results
            self.current_index = 0 if results else -1
            
            result.success = True
            result.results = results
            result.total_matches = len(results)
            result.files_searched = files_searched
            result.message = f"Found {len(results)} matches in {files_searched} files"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def _search_in_file(
        self,
        query: str,
        file_path: str,
        content: str
    ) -> List[SearchResult]:
        """
        Dosyada ara.
        
        Args:
            query: Arama sorgusu
            file_path: Dosya yolu
            content: Dosya içeriği
            
        Returns:
            List[SearchResult]: Sonuçlar
        """
        results = []
        lines = content.splitlines()
        
        for line_num, line in enumerate(lines, start=1):
            match_info = self._find_match(query, line)
            
            if match_info:
                column, match_text = match_info
                
                # Context al
                context_before = ""
                context_after = ""
                if self.config.show_context:
                    context_lines = self.config.context_lines
                    start_idx = max(0, line_num - 1 - context_lines)
                    end_idx = min(len(lines), line_num + context_lines)
                    context_before = "\n".join(lines[start_idx:line_num - 1])
                    context_after = "\n".join(lines[line_num:end_idx])
                
                search_result = SearchResult(
                    file_path=file_path,
                    line_number=line_num,
                    column=column,
                    match_text=match_text,
                    context_before=context_before,
                    context_after=context_after
                )
                results.append(search_result)
        
        return results
    
    def _find_match(self, query: str, line: str) -> Optional[Tuple[int, str]]:
        """
        Eşleşme bul.
        
        Args:
            query: Arama sorgusu
            line: Satır
            
        Returns:
            Optional[Tuple[int, str]]: (column, match_text) veya None
        """
        if self.config.mode == SearchMode.PLAIN_TEXT:
            if self.config.mode == SearchMode.CASE_SENSITIVE:
                idx = line.find(query)
            else:
                idx = line.lower().find(query.lower())
            
            if idx != -1:
                return (idx, query)
        
        elif self.config.mode == SearchMode.WHOLE_WORD:
            import re
            pattern = r'\b' + re.escape(query) + r'\b'
            if self.config.mode == SearchMode.CASE_SENSITIVE:
                match = re.search(pattern, line)
            else:
                match = re.search(pattern, line, re.IGNORECASE)
            
            if match:
                return (match.start(), match.group())
        
        elif self.config.mode == SearchMode.REGEX:
            import re
            try:
                flags = 0 if self.config.mode == SearchMode.CASE_SENSITIVE else re.IGNORECASE
                match = re.search(query, line, flags)
                if match:
                    return (match.start(), match.group())
            except re.error:
                pass
        
        elif self.config.mode == SearchMode.FUZZY:
            # Basit fuzzy match
            idx = self._fuzzy_find(query, line)
            if idx != -1:
                return (idx, line[idx:idx + len(query)])
        
        return None
    
    def _fuzzy_find(self, query: str, text: str) -> int:
        """
        Fuzzy arama.
        
        Args:
            query: Arama sorgusu
            text: Metin
            
        Returns:
            int: Index veya -1
        """
        query_lower = query.lower()
        text_lower = text.lower()
        
        # Basit substring match
        idx = text_lower.find(query_lower)
        if idx != -1:
            return idx
        
        # Karakter bazlı match
        query_chars = list(query_lower)
        text_chars = list(text_lower)
        
        for i in range(len(text_chars) - len(query_chars) + 1):
            matched = 0
            for j, q_char in enumerate(query_chars):
                if text_chars[i + j] == q_char:
                    matched += 1
            
            if matched >= len(query_chars) * 0.7:
                return i
        
        return -1
    
    def replace(
        self,
        query: str,
        replacement: str,
        files: Optional[Dict[str, str]] = None
    ) -> GlobalSearchResult:
        """
        Değiştir.
        
        Args:
            query: Arama sorgusu
            replacement: Değiştirme metni
            files: Dosya içeriği
            
        Returns:
            GlobalSearchResult: Değiştirme sonucu
        """
        result = GlobalSearchResult(success=False)
        
        try:
            if not query:
                result.errors.append("Query cannot be empty")
                return result
            
            if not files:
                result.errors.append("No files to replace in")
                return result
            
            replaced_files = {}
            total_replacements = 0
            
            for file_path, content in files.items():
                new_content, count = self._replace_in_file(query, replacement, content)
                if count > 0:
                    replaced_files[file_path] = new_content
                    total_replacements += count
            
            result.success = True
            result.total_matches = total_replacements
            result.files_searched = len(replaced_files)
            result.message = f"Replaced {total_replacements} occurrences in {len(replaced_files)} files"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def _replace_in_file(
        self,
        query: str,
        replacement: str,
        content: str
    ) -> Tuple[str, int]:
        """
        Dosyada değiştir.
        
        Args:
            query: Arama sorgusu
            replacement: Değiştirme metni
            content: Dosya içeriği
            
        Returns:
            Tuple[str, int]: (yeni içerik, değiştirme sayısı)
        """
        count = 0
        
        if self.config.mode == SearchMode.CASE_SENSITIVE:
            new_content = content.replace(query, replacement)
            count = content.count(query)
        else:
            new_content = content.replace(query.lower(), replacement, content.lower().count(query.lower()))
            count = content.lower().count(query.lower())
        
        return (new_content, count)
    
    def filter_results(self, file_path: Optional[str] = None) -> List[SearchResult]:
        """
        Sonuçları filtrele.
        
        Args:
            file_path: Dosya yolu (None ise tümü)
            
        Returns:
            List[SearchResult]: Filtrelenmiş sonuçlar
        """
        result = GlobalSearchResult(success=False)
        result.action = SearchAction.FILTER.value
        
        try:
            if file_path:
                filtered = [r for r in self.current_results if r.file_path == file_path]
                result.total_files_filtered = len(filtered)
                return filtered
            result.total_files_filtered = len(self.current_results)
            return self.current_results
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            return self.current_results
    
    def find_next(self) -> GlobalSearchResult:
        """
        Sonraki eşleşmeyi bul.
        
        Returns:
            GlobalSearchResult: Bulma sonucu
        """
        result = GlobalSearchResult(success=False)
        result.action = SearchAction.FIND_NEXT.value
        
        try:
            if not self.current_results:
                result.errors.append("No matches available")
                return result
            
            self.current_index = (self.current_index + 1) % len(self.current_results)
            
            result.success = True
            result.message = f"Match {self.current_index + 1}/{len(self.current_results)}"
            
            self.search_history.append(("find_next", str(self.current_index)))
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def find_previous(self) -> GlobalSearchResult:
        """
        Önceki eşleşmeyi bul.
        
        Returns:
            GlobalSearchResult: Bulma sonucu
        """
        result = GlobalSearchResult(success=False)
        result.action = SearchAction.FIND_PREVIOUS.value
        
        try:
            if not self.current_results:
                result.errors.append("No matches available")
                return result
            
            self.current_index = (self.current_index - 1) % len(self.current_results)
            
            result.success = True
            result.message = f"Match {self.current_index + 1}/{len(self.current_results)}"
            
            self.search_history.append(("find_previous", str(self.current_index)))
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_result_count(self) -> int:
        """
        Sonuç sayısını al.
        
        Returns:
            int: Sonuç sayısı
        """
        return len(self.current_results)
    
    def clear_results(self) -> GlobalSearchResult:
        """
        Sonuçları temizle.
        
        Returns:
            GlobalSearchResult: Temizleme sonucu
        """
        result = GlobalSearchResult(success=False)
        result.action = SearchAction.CLEAR.value
        
        try:
            self.current_results.clear()
            self.current_index = -1
            result.success = True
            result.message = "Results cleared"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_search_history(self) -> List[str]:
        """
        Arama geçmişini al.
        
        Returns:
            List[str]: Geçmiş
        """
        return self.search_history
    
    def clear_history(self) -> GlobalSearchResult:
        """
        Geçmişi temizle.
        
        Returns:
            GlobalSearchResult: Temizleme sonucu
        """
        result = GlobalSearchResult(success=False)
        
        try:
            self.search_history.clear()
            result.success = True
            result.message = "Search history cleared"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def update_config(self, config: GlobalSearchConfig) -> GlobalSearchResult:
        """
        Konfigürasyon güncelle.
        
        Args:
            config: Yeni konfigürasyon
            
        Returns:
            GlobalSearchResult: Güncelleme sonucu
        """
        result = GlobalSearchResult(success=False)
        
        try:
            self.config = config
            result.success = True
            result.message = "Config updated"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_config(self) -> GlobalSearchConfig:
        """
        Konfigürasyon al.
        
        Returns:
            GlobalSearchConfig: Konfigürasyon
        """
        return self.config
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        İstatistikleri al.
        
        Returns:
            Dict[str, Any]: İstatistikler
        """
        return {
            "total_matches": len(self.current_results),
            "current_index": self.current_index,
            "search_history_count": len(self.search_history),
            "file_filters": self.file_filters,
            "extension_filters": self.extension_filters,
            "directory_filters": self.directory_filters
        }
    
    def set_file_filters(self, filters: Optional[List[str]]) -> GlobalSearchResult:
        """
        Dosya filtrelerini ayarla.
        
        Args:
            filters: Dosya filtreleri
            
        Returns:
            GlobalSearchResult: Ayarlama sonucu
        """
        result = GlobalSearchResult(success=False)
        
        try:
            self.file_filters = filters
            result.success = True
            result.message = "File filters updated"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def set_extension_filters(self, filters: Optional[List[str]]) -> GlobalSearchResult:
        """
        Uzantı filtrelerini ayarla.
        
        Args:
            filters: Uzantı filtreleri
            
        Returns:
            GlobalSearchResult: Ayarlama sonucu
        """
        result = GlobalSearchResult(success=False)
        
        try:
            self.extension_filters = filters
            result.success = True
            result.message = "Extension filters updated"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def set_directory_filters(self, filters: Optional[List[str]]) -> GlobalSearchResult:
        """
        Dizin filtrelerini ayarla.
        
        Args:
            filters: Dizin filtreleri
            
        Returns:
            GlobalSearchResult: Ayarlama sonucu
        """
        result = GlobalSearchResult(success=False)
        
        try:
            self.directory_filters = filters
            result.success = True
            result.message = "Directory filters updated"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result


if __name__ == "__main__":
    # Basit test
    engine = GlobalSearchEngine()
    
    files = {
        "test.py": "print('hello')\nprint('world')",
        "test2.py": "print('test')"
    }
    
    result = engine.search("print", files)
    print(f"Search: {result.success}, Matches: {result.total_matches}")
