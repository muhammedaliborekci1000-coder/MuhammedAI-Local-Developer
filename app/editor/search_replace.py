"""
MuhammedAI Local Developer - Search and Replace
Search and replace engine for code editor.
"""

import re
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from enum import Enum


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
    PREVIEW = "preview"
    FIND_NEXT = "find_next"
    FIND_PREVIOUS = "find_previous"
    UNDO = "undo"
    REDO = "redo"


class ReplaceMode(Enum):
    """Replace mode."""
    REPLACE_ONE = "replace_one"
    REPLACE_ALL = "replace_all"
    PREVIEW = "preview"


@dataclass
class SearchMatch:
    """Search match."""
    text: str
    start: int
    end: int
    line: int
    column: int
    line_text: str
    context_before: str = ""
    context_after: str = ""
    is_highlighted: bool = False


@dataclass
class SearchResult:
    """Search result."""
    success: bool
    action: Optional[str] = None
    matches: List[SearchMatch] = field(default_factory=list)
    total_matches: int = 0
    query: str = ""
    mode: SearchMode = SearchMode.NORMAL
    errors: List[str] = field(default_factory=list)
    message: Optional[str] = None
    current_index: int = -1


@dataclass
class ReplaceResult:
    """Replace result."""
    success: bool
    action: Optional[str] = None
    replaced_text: Optional[str] = None
    original_text: Optional[str] = None
    replacements_count: int = 0
    preview_matches: List[SearchMatch] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    message: Optional[str] = None
    position: int = -1


@dataclass
class SearchReplaceConfig:
    """Search replace configuration."""
    mode: SearchMode = SearchMode.NORMAL
    replace_mode: ReplaceMode = ReplaceMode.REPLACE_ALL
    case_sensitive: bool = False
    whole_word: bool = False
    include_context: bool = True
    context_lines: int = 2
    highlight_matches: bool = True
    max_results: int = 1000


class SearchReplaceEngine:
    """
    Search and replace engine.
    
    Özellikler:
    - Text search (normal, case-sensitive, case-insensitive)
    - Regex search
    - Whole word search
    - Fuzzy search
    - Replace one
    - Replace all
    - Preview replacements
    - Line and column tracking
    - Match highlighting
    - Multiple search modes
    - Context display
    - Find next/previous
    - Undo/redo
    - Search history
    - Configuration management
    - Statistics tracking
    """
    
    def __init__(self, config: Optional[SearchReplaceConfig] = None):
        """Initialize search replace engine."""
        self.config = config or SearchReplaceConfig()
        self.current_query: str = ""
        self.current_mode: SearchMode = SearchMode.NORMAL
        self.current_matches: List[SearchMatch] = []
        self.current_index: int = -1
        self.search_history: List[Tuple[str, str]] = []  # (action, query)
        self.undo_stack: List[str] = []
        self.redo_stack: List[str] = []
    
    def search(
        self,
        text: str,
        query: str,
        mode: Optional[SearchMode] = None
    ) -> SearchResult:
        """
        Metin içinde ara.
        
        Args:
            text: Aranacak metin
            query: Arama sorgusu
            mode: Arama modu
            
        Returns:
            SearchResult: Arama sonucu
        """
        result = SearchResult(success=False)
        result.action = SearchAction.SEARCH.value
        result.query = query
        result.mode = mode or self.config.mode
        
        try:
            matches = []
            lines = text.splitlines()
            
            for line_num, line in enumerate(lines, 1):
                line_matches = self._search_in_line(line, query, result.mode, line_num, lines)
                matches.extend(line_matches)
            
            # Max results limit
            if len(matches) > self.config.max_results:
                matches = matches[:self.config.max_results]
            
            self.current_matches = matches
            self.current_index = 0 if matches else -1
            
            result.matches = matches
            result.total_matches = len(matches)
            result.current_index = self.current_index
            result.success = True
            result.message = f"Found {len(matches)} matches"
            
            # Geçmişe ekle
            self.search_history.append(("search", query))
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def _search_in_line(
        self,
        line: str,
        query: str,
        mode: SearchMode,
        line_num: int,
        lines: List[str]
    ) -> List[SearchMatch]:
        """Satır içinde ara."""
        matches = []
        
        if mode == SearchMode.NORMAL:
            # Normal arama (case-insensitive)
            pattern = re.escape(query)
            flags = re.IGNORECASE
        elif mode == SearchMode.CASE_SENSITIVE:
            # Case-sensitive arama
            pattern = re.escape(query)
            flags = 0
        elif mode == SearchMode.CASE_INSENSITIVE:
            # Case-insensitive arama
            pattern = re.escape(query)
            flags = re.IGNORECASE
        elif mode == SearchMode.REGEX:
            # Regex arama
            pattern = query
            flags = 0
        elif mode == SearchMode.WHOLE_WORD:
            # Whole word arama
            pattern = r'\b' + re.escape(query) + r'\b'
            flags = re.IGNORECASE
        elif mode == SearchMode.FUZZY:
            # Fuzzy arama
            return self._fuzzy_search_in_line(line, query, line_num, lines)
        else:
            pattern = re.escape(query)
            flags = re.IGNORECASE
        
        try:
            for match in re.finditer(pattern, line, flags):
                context_before = ""
                context_after = ""
                if self.config.include_context:
                    start_idx = max(0, line_num - self.config.context_lines - 1)
                    context_before = "\n".join(lines[start_idx:line_num-1])
                    end_idx = min(len(lines), line_num + self.config.context_lines)
                    context_after = "\n".join(lines[line_num:end_idx])
                
                search_match = SearchMatch(
                    text=match.group(),
                    start=match.start(),
                    end=match.end(),
                    line=line_num,
                    column=match.start(),
                    line_text=line,
                    context_before=context_before,
                    context_after=context_after,
                    is_highlighted=self.config.highlight_matches
                )
                matches.append(search_match)
        except re.error:
            pass
        
        return matches
    
    def _fuzzy_search_in_line(
        self,
        line: str,
        query: str,
        line_num: int,
        lines: List[str]
    ) -> List[SearchMatch]:
        """Fuzzy search in line."""
        matches = []
        query_lower = query.lower()
        line_lower = line.lower()
        
        # Basit substring match
        if query_lower in line_lower:
            start = line_lower.find(query_lower)
            end = start + len(query)
            
            context_before = ""
            context_after = ""
            if self.config.include_context:
                start_idx = max(0, line_num - self.config.context_lines - 1)
                context_before = "\n".join(lines[start_idx:line_num-1])
                end_idx = min(len(lines), line_num + self.config.context_lines)
                context_after = "\n".join(lines[line_num:end_idx])
            
            search_match = SearchMatch(
                text=line[start:end],
                start=start,
                end=end,
                line=line_num,
                column=start,
                line_text=line,
                context_before=context_before,
                context_after=context_after,
                is_highlighted=self.config.highlight_matches
            )
            matches.append(search_match)
        
        return matches
    
    def replace(
        self,
        text: str,
        query: str,
        replacement: str,
        mode: Optional[SearchMode] = None,
        replace_mode: Optional[ReplaceMode] = None
    ) -> ReplaceResult:
        """
        Metin içinde değiştir.
        
        Args:
            text: Metin
            query: Arama sorgusu
            replacement: Değiştirme metni
            mode: Arama modu
            replace_mode: Değiştirme modu
            
        Returns:
            ReplaceResult: Değiştirme sonucu
        """
        result = ReplaceResult(success=False)
        result.action = SearchAction.REPLACE.value
        result.original_text = text
        result.mode = mode or self.config.mode
        result.replace_mode = replace_mode or self.config.replace_mode
        
        try:
            # Önce ara
            search_result = self.search(text, query, result.mode)
            
            if not search_result.success or search_result.total_matches == 0:
                result.errors.append("No matches found")
                return result
            
            if result.replace_mode == ReplaceMode.PREVIEW:
                # Önizleme
                result.preview_matches = search_result.matches
                result.replacements_count = search_result.total_matches
                result.action = SearchAction.PREVIEW.value
                result.success = True
                result.message = f"Preview: {search_result.total_matches} matches to replace"
                return result
            
            # Undo stack'e ekle
            self.undo_stack.append(text)
            self.redo_stack.clear()
            
            if result.replace_mode == ReplaceMode.REPLACE_ONE:
                # Sadece ilk eşleşmeyi değiştir
                if search_result.matches:
                    first_match = search_result.matches[0]
                    replaced_text = text[:first_match.start] + replacement + text[first_match.end:]
                    result.replaced_text = replaced_text
                    result.replacements_count = 1
                    result.position = 0
                    result.success = True
                    result.message = "Replaced 1 occurrence"
            elif result.replace_mode == ReplaceMode.REPLACE_ALL:
                # Tüm eşleşmeleri değiştir
                replaced_text = self._replace_all(text, query, replacement, result.mode)
                result.replaced_text = replaced_text
                result.replacements_count = search_result.total_matches
                result.action = SearchAction.REPLACE_ALL.value
                result.success = True
                result.message = f"Replaced {search_result.total_matches} occurrences"
            
            # Geçmişe ekle
            self.search_history.append(("replace", query))
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def _replace_all(
        self,
        text: str,
        query: str,
        replacement: str,
        mode: SearchMode
    ) -> str:
        """Tüm eşleşmeleri değiştir."""
        if mode == SearchMode.REGEX:
            # Regex replace
            try:
                return re.sub(query, replacement, text)
            except re.error:
                return text
        elif mode == SearchMode.WHOLE_WORD:
            # Whole word replace
            pattern = r'\b' + re.escape(query) + r'\b'
            return re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        elif mode == SearchMode.CASE_SENSITIVE:
            # Case-sensitive replace
            pattern = re.escape(query)
            return re.sub(pattern, replacement, text)
        else:
            # Case-insensitive replace
            pattern = re.escape(query)
            return re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    
    def replace_at_position(
        self,
        text: str,
        query: str,
        replacement: str,
        position: int,
        mode: Optional[SearchMode] = None
    ) -> ReplaceResult:
        """
        Belirli bir pozisyondaki eşleşmeyi değiştir.
        
        Args:
            text: Metin
            query: Arama sorgusu
            replacement: Değiştirme metni
            position: Pozisyon (match index)
            mode: Arama modu
            
        Returns:
            ReplaceResult: Değiştirme sonucu
        """
        result = ReplaceResult(success=False)
        result.action = SearchAction.REPLACE.value
        result.original_text = text
        result.mode = mode or self.config.mode
        
        try:
            # Önce ara
            search_result = self.search(text, query, result.mode)
            
            if not search_result.success or position >= len(search_result.matches):
                result.errors.append("Invalid position or no matches found")
                return result
            
            # Undo stack'e ekle
            self.undo_stack.append(text)
            self.redo_stack.clear()
            
            # Belirli pozisyondaki eşleşmeyi değiştir
            match = search_result.matches[position]
            replaced_text = text[:match.start] + replacement + text[match.end:]
            
            result.replaced_text = replaced_text
            result.replacements_count = 1
            result.position = position
            result.success = True
            result.message = f"Replaced match at position {position}"
            
            # Geçmişe ekle
            self.search_history.append(("replace_at_position", query))
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_next_match(
        self,
        current_position: int,
        direction: str = "forward"
    ) -> Optional[SearchMatch]:
        """
        Sonraki/önceki eşleşmeyi al.
        
        Args:
            current_position: Mevcut pozisyon
            direction: Yön (forward/backward)
            
        Returns:
            Optional[SearchMatch]: Eşleşme veya None
        """
        if not self.current_matches:
            return None
        
        if direction == "forward":
            for match in self.current_matches:
                if match.start > current_position:
                    return match
            # Sonra başa dön
            if self.current_matches:
                return self.current_matches[0]
        else:  # backward
            for match in reversed(self.current_matches):
                if match.start < current_position:
                    return match
            # Başa sona dön
            if self.current_matches:
                return self.current_matches[-1]
        
        return None
    
    def find_next(self) -> SearchResult:
        """
        Sonraki eşleşmeyi bul.
        
        Returns:
            SearchResult: Bulma sonucu
        """
        result = SearchResult(success=False)
        result.action = SearchAction.FIND_NEXT.value
        
        try:
            if not self.current_matches:
                result.errors.append("No matches available")
                return result
            
            self.current_index = (self.current_index + 1) % len(self.current_matches)
            
            result.success = True
            result.current_index = self.current_index
            result.message = f"Match {self.current_index + 1}/{len(self.current_matches)}"
            
            self.search_history.append(("find_next", str(self.current_index)))
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def find_previous(self) -> SearchResult:
        """
        Önceki eşleşmeyi bul.
        
        Returns:
            SearchResult: Bulma sonucu
        """
        result = SearchResult(success=False)
        result.action = SearchAction.FIND_PREVIOUS.value
        
        try:
            if not self.current_matches:
                result.errors.append("No matches available")
                return result
            
            self.current_index = (self.current_index - 1) % len(self.current_matches)
            
            result.success = True
            result.current_index = self.current_index
            result.message = f"Match {self.current_index + 1}/{len(self.current_matches)}"
            
            self.search_history.append(("find_previous", str(self.current_index)))
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def undo(self) -> ReplaceResult:
        """
        Son değiştirmeyi geri al.
        
        Returns:
            ReplaceResult: Geri alma sonucu
        """
        result = ReplaceResult(success=False)
        result.action = SearchAction.UNDO.value
        
        try:
            if not self.undo_stack:
                result.errors.append("Nothing to undo")
                return result
            
            previous_text = self.undo_stack.pop()
            self.redo_stack.append(previous_text)
            
            result.replaced_text = previous_text
            result.success = True
            result.message = "Undo successful"
            
            self.search_history.append(("undo", ""))
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def redo(self) -> ReplaceResult:
        """
        Geri alınan değiştirmeyi tekrar uygula.
        
        Returns:
            ReplaceResult: Tekrar uygulama sonucu
        """
        result = ReplaceResult(success=False)
        result.action = SearchAction.REDO.value
        
        try:
            if not self.redo_stack:
                result.errors.append("Nothing to redo")
                return result
            
            next_text = self.redo_stack.pop()
            self.undo_stack.append(next_text)
            
            result.replaced_text = next_text
            result.success = True
            result.message = "Redo successful"
            
            self.search_history.append(("redo", ""))
        
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
    
    def clear_history(self) -> SearchResult:
        """
        Geçmişi temizle.
        
        Returns:
            SearchResult: Temizleme sonucu
        """
        result = SearchResult(success=False)
        
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
            "undo_stack_size": len(self.undo_stack),
            "redo_stack_size": len(self.redo_stack),
            "current_query": self.current_query,
            "current_mode": self.current_mode.value
        }
    
    def update_config(self, config: SearchReplaceConfig) -> SearchResult:
        """
        Konfigürasyon güncelle.
        
        Args:
            config: Yeni konfigürasyon
            
        Returns:
            SearchResult: Güncelleme sonucu
        """
        result = SearchResult(success=False)
        
        try:
            self.config = config
            result.success = True
            result.message = "Config updated"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_config(self) -> SearchReplaceConfig:
        """
        Konfigürasyon al.
        
        Returns:
            SearchReplaceConfig: Konfigürasyon
        """
        return self.config


if __name__ == "__main__":
    # Basit test
    engine = SearchReplaceEngine()
    
    text = "Hello world, hello Python, hello AI"
    
    # Ara
    result = engine.search(text, "hello", SearchMode.CASE_INSENSITIVE)
    print(f"Search: {result.success}")
    print(f"Matches: {result.total_matches}")
    
    # Değiştir
    replace_result = engine.replace(text, "hello", "Hi", SearchMode.CASE_INSENSITIVE, ReplaceMode.REPLACE_ALL)
    print(f"Replace: {replace_result.success}")
    print(f"Replaced text: {replace_result.replaced_text}")
