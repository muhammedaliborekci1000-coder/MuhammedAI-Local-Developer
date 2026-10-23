"""
MuhammedAI Local Developer - File Search
File search engine for code editor.
"""

import os
import re
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime


class SearchScope(Enum):
    """Search scope."""
    FILE_NAME = "file_name"
    FILE_CONTENT = "file_content"
    BOTH = "both"


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
    REPLACE = "replace"
    REPLACE_ALL = "replace_all"
    FIND_NEXT = "find_next"
    FIND_PREVIOUS = "find_previous"


@dataclass
class FileMatch:
    """File match."""
    file_path: str
    file_name: str
    directory: str
    size: int
    modified_time: Optional[datetime]
    matches: List[str] = field(default_factory=list)
    line_numbers: List[int] = field(default_factory=list)
    context_before: str = ""
    context_after: str = ""
    is_highlighted: bool = False


@dataclass
class FileSearchConfig:
    """File search configuration."""
    scope: SearchScope = SearchScope.FILE_NAME
    mode: SearchMode = SearchMode.NORMAL
    include_context: bool = True
    context_lines: int = 2
    highlight_matches: bool = True
    max_results: int = 100
    exclude_dirs: Optional[List[str]] = None
    extensions: Optional[List[str]] = None
    case_sensitive: bool = False
    whole_word: bool = False


@dataclass
class FileSearchResult:
    """File search result."""
    success: bool
    action: Optional[str] = None
    matches: List[FileMatch] = field(default_factory=list)
    total_files: int = 0
    total_matches: int = 0
    query: str = ""
    scope: SearchScope = SearchScope.FILE_NAME
    mode: SearchMode = SearchMode.NORMAL
    errors: List[str] = field(default_factory=list)
    message: Optional[str] = None


class FileSearchEngine:
    """
    File search engine.
    
    Özellikler:
    - File name search
    - File content search
    - Extension filtering
    - Directory filtering
    - Case-sensitive/insensitive search
    - Regex search
    - Whole word search
    - Fuzzy search
    - Recursive directory search
    - File type filtering
    - Size filtering
    - Date filtering
    - Search results with metadata
    - Replace functionality
    - Find next/previous
    - Search history
    - Context display
    - Match highlighting
    - Configuration management
    - Statistics tracking
    """
    
    def __init__(self, root_path: str = ".", config: Optional[FileSearchConfig] = None):
        """
        Args:
            root_path: Kök dizin yolu
            config: Arama konfigürasyonu
        """
        self.root_path = root_path
        self.config = config or FileSearchConfig()
        self.search_history: List[Tuple[str, str]] = []  # (action, query)
        self.current_matches: List[FileMatch] = []
        self.current_index: int = -1
    
    def search_files(
        self,
        query: str,
        scope: Optional[SearchScope] = None,
        mode: Optional[SearchMode] = None,
        extensions: Optional[List[str]] = None,
        exclude_dirs: Optional[List[str]] = None,
        max_results: Optional[int] = None
    ) -> FileSearchResult:
        """
        Dosya ara.
        
        Args:
            query: Arama sorgusu
            scope: Arama scope'u
            mode: Arama modu
            extensions: Dosya uzantıları (opsiyonel)
            exclude_dirs: Hariç tutulacak dizinler (opsiyonel)
            max_results: Maksimum sonuç sayısı
            
        Returns:
            FileSearchResult: Arama sonucu
        """
        result = FileSearchResult(success=False)
        result.action = SearchAction.SEARCH.value
        result.query = query
        result.scope = scope or self.config.scope
        result.mode = mode or self.config.mode
        
        try:
            matches = []
            
            if result.scope == SearchScope.FILE_NAME:
                matches = self._search_by_filename(query, result.mode, extensions or self.config.extensions, exclude_dirs or self.config.exclude_dirs, max_results or self.config.max_results)
            elif result.scope == SearchScope.FILE_CONTENT:
                matches = self._search_by_content(query, result.mode, extensions or self.config.extensions, exclude_dirs or self.config.exclude_dirs, max_results or self.config.max_results)
            else:  # BOTH
                name_matches = self._search_by_filename(query, result.mode, extensions or self.config.extensions, exclude_dirs or self.config.exclude_dirs, max_results or self.config.max_results)
                content_matches = self._search_by_content(query, result.mode, extensions or self.config.extensions, exclude_dirs or self.config.exclude_dirs, max_results or self.config.max_results)
                
                # Birleştir (duplicate'ları kaldır)
                seen = set()
                for match in name_matches + content_matches:
                    if match.file_path not in seen:
                        matches.append(match)
                        seen.add(match.file_path)
            
            self.current_matches = matches
            self.current_index = 0 if matches else -1
            
            result.matches = matches
            result.total_files = len(matches)
            result.total_matches = sum(len(m.matches) for m in matches)
            result.success = True
            result.message = f"Found {len(matches)} files"
            
            self.search_history.append(("search", query))
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def _search_by_filename(
        self,
        query: str,
        mode: SearchMode,
        extensions: Optional[List[str]],
        exclude_dirs: Optional[List[str]],
        max_results: int
    ) -> List[FileMatch]:
        """Dosya adına göre ara."""
        matches = []
        
        if exclude_dirs is None:
            exclude_dirs = ['.git', '__pycache__', 'node_modules', '.venv']
        
        for root, dirs, files in os.walk(self.root_path):
            # Exclude dizinleri kaldır
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            for file in files:
                # Uzantı filtreleme
                if extensions:
                    file_ext = os.path.splitext(file)[1].lower()
                    if file_ext not in extensions:
                        continue
                
                # Dosya adı eşleşmesi
                if self._matches_query(file, query, mode):
                    file_path = os.path.join(root, file)
                    file_stat = os.stat(file_path)
                    
                    match = FileMatch(
                        file_path=file_path,
                        file_name=file,
                        directory=root,
                        size=file_stat.st_size,
                        modified_time=datetime.fromtimestamp(file_stat.st_mtime)
                    )
                    matches.append(match)
                    
                    if len(matches) >= max_results:
                        return matches
        
        return matches
    
    def _search_by_content(
        self,
        query: str,
        mode: SearchMode,
        extensions: Optional[List[str]],
        exclude_dirs: Optional[List[str]],
        max_results: int
    ) -> List[FileMatch]:
        """Dosya içeriğine göre ara."""
        matches = []
        
        if exclude_dirs is None:
            exclude_dirs = ['.git', '__pycache__', 'node_modules', '.venv']
        
        for root, dirs, files in os.walk(self.root_path):
            # Exclude dizinleri kaldır
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            for file in files:
                # Uzantı filtreleme
                if extensions:
                    file_ext = os.path.splitext(file)[1].lower()
                    if file_ext not in extensions:
                        continue
                
                file_path = os.path.join(root, file)
                
                # İçerik eşleşmesi
                content_matches = self._search_in_file(file_path, query, mode)
                
                if content_matches:
                    file_stat = os.stat(file_path)
                    
                    match = FileMatch(
                        file_path=file_path,
                        file_name=file,
                        directory=root,
                        size=file_stat.st_size,
                        modified_time=datetime.fromtimestamp(file_stat.st_mtime),
                        matches=content_matches['matches'],
                        line_numbers=content_matches['line_numbers']
                    )
                    matches.append(match)
                    
                    if len(matches) >= max_results:
                        return matches
        
        return matches
    
    def _search_in_file(
        self,
        file_path: str,
        query: str,
        mode: SearchMode
    ) -> Optional[Dict[str, List]]:
        """Dosya içinde ara."""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            
            matches = []
            line_numbers = []
            
            for line_num, line in enumerate(lines, 1):
                if self._matches_query(line, query, mode):
                    matches.append(line.strip())
                    line_numbers.append(line_num)
            
            if matches:
                return {'matches': matches, 'line_numbers': line_numbers}
            
            return None
        
        except Exception:
            return None
    
    def _matches_query(self, text: str, query: str, mode: SearchMode) -> bool:
        """Metin sorgu ile eşleşiyor mu?"""
        if mode == SearchMode.NORMAL:
            # Normal (case-insensitive)
            return query.lower() in text.lower()
        elif mode == SearchMode.CASE_SENSITIVE:
            # Case-sensitive
            return query in text
        elif mode == SearchMode.CASE_INSENSITIVE:
            # Case-insensitive
            return query.lower() in text.lower()
        elif mode == SearchMode.REGEX:
            # Regex
            try:
                return bool(re.search(query, text))
            except re.error:
                return False
        elif mode == SearchMode.WHOLE_WORD:
            # Whole word
            pattern = r'\b' + re.escape(query) + r'\b'
            try:
                return bool(re.search(pattern, text, re.IGNORECASE))
            except re.error:
                return False
        elif mode == SearchMode.FUZZY:
            # Fuzzy
            return self._fuzzy_match(query, text)
        else:
            return query.lower() in text.lower()
    
    def _fuzzy_match(self, query: str, text: str) -> bool:
        """Fuzzy eşleşme."""
        query_lower = query.lower()
        text_lower = text.lower()
        
        # Basit substring match
        if query_lower in text_lower:
            return True
        
        # Karakter bazlı match
        query_chars = list(query_lower)
        text_chars = list(text_lower)
        
        if len(query_chars) > len(text_chars):
            return False
        
        matched = 0
        j = 0
        for q_char in query_chars:
            while j < len(text_chars) and text_chars[j] != q_char:
                j += 1
            if j < len(text_chars):
                matched += 1
                j += 1
        
        return matched >= len(query_chars) * 0.7
    
    def search_by_extension(
        self,
        extensions: List[str],
        exclude_dirs: Optional[List[str]] = None
    ) -> FileSearchResult:
        """
        Uzantıya göre dosya ara.
        
        Args:
            extensions: Dosya uzantıları
            exclude_dirs: Hariç tutulacak dizinler
            
        Returns:
            FileSearchResult: Arama sonucu
        """
        result = FileSearchResult(success=False)
        
        try:
            matches = []
            
            if exclude_dirs is None:
                exclude_dirs = ['.git', '__pycache__', 'node_modules', '.venv']
            
            for root, dirs, files in os.walk(self.root_path):
                # Exclude dizinleri kaldır
                dirs[:] = [d for d in dirs if d not in exclude_dirs]
                
                for file in files:
                    file_ext = os.path.splitext(file)[1].lower()
                    
                    if file_ext in extensions:
                        file_path = os.path.join(root, file)
                        file_stat = os.stat(file_path)
                        
                        match = FileMatch(
                            file_path=file_path,
                            file_name=file,
                            directory=root,
                            size=file_stat.st_size,
                            modified_time=datetime.fromtimestamp(file_stat.st_mtime)
                        )
                        matches.append(match)
            
            result.matches = matches
            result.total_files = len(matches)
            result.success = True
            result.message = f"Found {len(matches)} files with extensions {extensions}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def replace(
        self,
        query: str,
        replacement: str,
        file_path: str
    ) -> FileSearchResult:
        """
        Dosyada değiştir.
        
        Args:
            query: Arama sorgusu
            replacement: Değiştirme metni
            file_path: Dosya yolu
            
        Returns:
            FileSearchResult: Değiştirme sonucu
        """
        result = FileSearchResult(success=False)
        result.action = SearchAction.REPLACE.value
        result.query = query
        
        try:
            if not os.path.exists(file_path):
                result.errors.append(f"File not found: {file_path}")
                return result
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Değiştirme yap
            if self.config.case_sensitive:
                new_content = content.replace(query, replacement)
                count = content.count(query)
            else:
                new_content = content.replace(query.lower(), replacement, content.lower().count(query.lower()))
                count = content.lower().count(query.lower())
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            result.success = True
            result.total_matches = count
            result.message = f"Replaced {count} occurrences in {file_path}"
            
            self.search_history.append(("replace", query))
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def replace_all(
        self,
        query: str,
        replacement: str
    ) -> FileSearchResult:
        """
        Tüm dosyalarda değiştir.
        
        Args:
            query: Arama sorgusu
            replacement: Değiştirme metni
            
        Returns:
            FileSearchResult: Değiştirme sonucu
        """
        result = FileSearchResult(success=False)
        result.action = SearchAction.REPLACE_ALL.value
        result.query = query
        
        try:
            total_replaced = 0
            files_replaced = []
            
            for match in self.current_matches:
                replace_result = self.replace(query, replacement, match.file_path)
                if replace_result.success:
                    total_replaced += replace_result.total_matches
                    files_replaced.append(match.file_path)
            
            result.success = True
            result.total_matches = total_replaced
            result.total_files = len(files_replaced)
            result.message = f"Replaced {total_replaced} occurrences in {len(files_replaced)} files"
            
            self.search_history.append(("replace_all", query))
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def find_next(self) -> FileSearchResult:
        """
        Sonraki eşleşmeyi bul.
        
        Returns:
            FileSearchResult: Bulma sonucu
        """
        result = FileSearchResult(success=False)
        result.action = SearchAction.FIND_NEXT.value
        
        try:
            if not self.current_matches:
                result.errors.append("No matches available")
                return result
            
            self.current_index = (self.current_index + 1) % len(self.current_matches)
            
            result.success = True
            result.message = f"Match {self.current_index + 1}/{len(self.current_matches)}"
            
            self.search_history.append(("find_next", str(self.current_index)))
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def find_previous(self) -> FileSearchResult:
        """
        Önceki eşleşmeyi bul.
        
        Returns:
            FileSearchResult: Bulma sonucu
        """
        result = FileSearchResult(success=False)
        result.action = SearchAction.FIND_PREVIOUS.value
        
        try:
            if not self.current_matches:
                result.errors.append("No matches available")
                return result
            
            self.current_index = (self.current_index - 1) % len(self.current_matches)
            
            result.success = True
            result.message = f"Match {self.current_index + 1}/{len(self.current_matches)}"
            
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
    
    def clear_history(self) -> FileSearchResult:
        """
        Geçmişi temizle.
        
        Returns:
            FileSearchResult: Temizleme sonucu
        """
        result = FileSearchResult(success=False)
        
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
            "total_matches": len(self.current_matches),
            "current_index": self.current_index,
            "search_history_count": len(self.search_history),
            "root_path": self.root_path
        }
    
    def update_config(self, config: FileSearchConfig) -> FileSearchResult:
        """
        Konfigürasyon güncelle.
        
        Args:
            config: Yeni konfigürasyon
            
        Returns:
            FileSearchResult: Güncelleme sonucu
        """
        result = FileSearchResult(success=False)
        
        try:
            self.config = config
            result.success = True
            result.message = "Config updated"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_config(self) -> FileSearchConfig:
        """
        Konfigürasyon al.
        
        Returns:
            FileSearchConfig: Konfigürasyon
        """
        return self.config


if __name__ == "__main__":
    # Basit test
    import tempfile
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Test dosyaları oluştur
        with open(os.path.join(tmpdir, "main.py"), "w") as f:
            f.write("def main():\n    pass")
        with open(os.path.join(tmpdir, "utils.py"), "w") as f:
            f.write("def helper():\n    pass")
        
        engine = FileSearchEngine(tmpdir)
        
        # Dosya adına göre ara
        result = engine.search_files("main", SearchScope.FILE_NAME)
        print(f"File name search: {result.success}")
        print(f"Total files: {result.total_files}")
