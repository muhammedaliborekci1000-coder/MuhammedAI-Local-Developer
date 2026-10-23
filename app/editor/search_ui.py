"""
MuhammedAI Local Developer - Search UI
Search UI system for code editor.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum


class SearchMode(Enum):
    """Search mode."""
    FIND = "find"
    REPLACE = "replace"
    FIND_IN_FILES = "find_in_files"
    REPLACE_IN_FILES = "replace_in_files"


class SearchScope(Enum):
    """Search scope."""
    CURRENT_FILE = "current_file"
    OPEN_FILES = "open_files"
    PROJECT = "project"
    SELECTION = "selection"


class MatchCase(Enum):
    """Match case option."""
    SENSITIVE = "sensitive"
    INSENSITIVE = "insensitive"


@dataclass
class SearchResult:
    """Search result."""
    file_path: str
    line_number: int
    column: int
    line_content: str
    match_text: str
    context_before: List[str] = field(default_factory=list)
    context_after: List[str] = field(default_factory=list)


@dataclass
class SearchQuery:
    """Search query."""
    search_text: str
    replace_text: Optional[str] = None
    mode: SearchMode = SearchMode.FIND
    scope: SearchScope = SearchScope.CURRENT_FILE
    match_case: MatchCase = MatchCase.INSENSITIVE
    use_regex: bool = False
    use_whole_word: bool = False
    include_ignored_files: bool = False


@dataclass
class SearchConfig:
    """Search configuration."""
    max_results: int = 100
    show_context: bool = True
    context_lines: int = 3
    highlight_matches: bool = True
    auto_expand_results: bool = False
    preserve_case: bool = False
    search_history_limit: int = 50


@dataclass
class SearchUIResult:
    """Search UI result."""
    success: bool
    results: List[SearchResult] = field(default_factory=list)
    total_matches: int = 0
    errors: List[str] = field(default_factory=list)
    message: Optional[str] = None
    output: Optional[str] = None


class SearchUIManager:
    """
    Search UI manager.
    
    Özellikler:
    - Search UI
    - Search results
    - Search highlighting
    - Replace UI
    - Replace preview
    - Replace all
    - Search in files
    - Search history
    - Search filters
    - Regex support
    - Case sensitivity
    - Whole word search
    - Context display
    - Result navigation
    - Quick navigation
    - Multi-file search
    - Search statistics
    """
    
    def __init__(self, config: Optional[SearchConfig] = None):
        """
        Initialize search UI manager.
        
        Args:
            config: Search configuration
        """
        self.config = config or SearchConfig()
        self.search_history: List[SearchQuery] = []
        self.current_query: Optional[SearchQuery] = None
        self.current_results: List[SearchResult] = []
    
    def search(self, query: SearchQuery, content: str, file_path: str) -> SearchUIResult:
        """
        Perform search.
        
        Args:
            query: Search query
            content: Content to search
            file_path: File path
            
        Returns:
            SearchUIResult: Search result
        """
        result = SearchUIResult(success=True)
        
        self.current_query = query
        self.current_results = []
        
        search_text = query.search_text
        if not search_text:
            result.errors.append("Search text is empty")
            result.success = False
            return result
        
        # Add to history
        self._add_to_history(query)
        
        # Perform search
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines):
            if self._matches_query(line, query):
                # Find column
                column = line.lower().find(search_text.lower()) if query.match_case == MatchCase.INSENSITIVE else line.find(search_text)
                
                # Create context
                context_before = []
                context_after = []
                
                if self.config.show_context:
                    start_line = max(0, line_num - self.config.context_lines)
                    end_line = min(len(lines), line_num + self.config.context_lines + 1)
                    
                    context_before = lines[start_line:line_num]
                    context_after = lines[line_num + 1:end_line]
                
                search_result = SearchResult(
                    file_path=file_path,
                    line_number=line_num + 1,
                    column=column,
                    line_content=line,
                    match_text=search_text,
                    context_before=context_before,
                    context_after=context_after
                )
                
                self.current_results.append(search_result)
                
                # Limit results
                if len(self.current_results) >= self.config.max_results:
                    break
        
        result.results = self.current_results
        result.total_matches = len(self.current_results)
        result.message = f"Found {len(self.current_results)} matches"
        
        return result
    
    def _matches_query(self, line: str, query: SearchQuery) -> bool:
        """
        Check if line matches query.
        
        Args:
            line: Line content
            query: Search query
            
        Returns:
            bool: Match result
        """
        search_text = query.search_text
        
        if query.match_case == MatchCase.INSENSITIVE:
            line_lower = line.lower()
            search_text_lower = search_text.lower()
            
            if query.use_whole_word:
                words = line_lower.split()
                return search_text_lower in words
            else:
                return search_text_lower in line_lower
        else:
            if query.use_whole_word:
                words = line.split()
                return search_text in words
            else:
                return search_text in line
    
    def replace(self, query: SearchQuery, content: str) -> SearchUIResult:
        """
        Perform replace.
        
        Args:
            query: Search query with replace text
            content: Content to replace in
            
        Returns:
            SearchUIResult: Replace result
        """
        result = SearchUIResult(success=True)
        
        if not query.replace_text:
            result.errors.append("Replace text is empty")
            result.success = False
            return result
        
        search_text = query.search_text
        replace_text = query.replace_text
        
        if query.match_case == MatchCase.INSENSITIVE:
            content = content.replace(search_text.lower(), replace_text)
        else:
            content = content.replace(search_text, replace_text)
        
        result.message = "Replace completed"
        result.output = content
        
        return result
    
    def replace_all(self, query: SearchQuery, content: str) -> SearchUIResult:
        """
        Perform replace all.
        
        Args:
            query: Search query with replace text
            content: Content to replace in
            
        Returns:
            SearchUIResult: Replace result
        """
        result = SearchUIResult(success=True)
        
        if not query.replace_text:
            result.errors.append("Replace text is empty")
            result.success = False
            return result
        
        search_text = query.search_text
        replace_text = query.replace_text
        
        count = 0
        if query.match_case == MatchCase.INSENSITIVE:
            count = content.lower().count(search_text.lower())
            content = content.replace(search_text.lower(), replace_text)
        else:
            count = content.count(search_text)
            content = content.replace(search_text, replace_text)
        
        result.message = f"Replaced {count} occurrences"
        result.output = content
        
        return result
    
    def get_search_history(self) -> List[SearchQuery]:
        """
        Get search history.
        
        Returns:
            List[SearchQuery]: Search history
        """
        return self.search_history
    
    def _add_to_history(self, query: SearchQuery) -> None:
        """
        Add query to history.
        
        Args:
            query: Search query
        """
        # Remove duplicates
        self.search_history = [q for q in self.search_history if q.search_text != query.search_text]
        
        # Add to front
        self.search_history.insert(0, query)
        
        # Limit history
        if len(self.search_history) > self.config.search_history_limit:
            self.search_history = self.search_history[:self.config.search_history_limit]
    
    def clear_history(self) -> None:
        """Clear search history."""
        self.search_history.clear()
    
    def get_current_results(self) -> List[SearchResult]:
        """
        Get current search results.
        
        Returns:
            List[SearchResult]: Current results
        """
        return self.current_results
    
    def navigate_to_result(self, index: int) -> Optional[SearchResult]:
        """
        Navigate to search result.
        
        Args:
            index: Result index
            
        Returns:
            Optional[SearchResult]: Search result
        """
        if 0 <= index < len(self.current_results):
            return self.current_results[index]
        return None
    
    def get_result_count(self) -> int:
        """
        Get result count.
        
        Returns:
            int: Result count
        """
        return len(self.current_results)
    
    def update_config(self, config: SearchConfig) -> None:
        """
        Update search configuration.
        
        Args:
            config: New configuration
        """
        self.config = config
    
    def get_config(self) -> SearchConfig:
        """
        Get search configuration.
        
        Returns:
            SearchConfig: Configuration
        """
        return self.config


if __name__ == "__main__":
    # Basit test
    config = SearchConfig()
    manager = SearchUIManager(config)
    
    # Search
    query = SearchQuery(search_text="hello")
    content = "hello world\nhello there"
    
    result = manager.search(query, content, "test.py")
    
    print(f"Found {result.total_matches} matches")
    for res in result.results:
        print(f"  Line {res.line_number}: {res.line_content}")
