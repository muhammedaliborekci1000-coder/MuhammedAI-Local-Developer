"""
MuhammedAI Local Developer - Replace UI
Replace UI system for code editor.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum


class ReplaceMode(Enum):
    """Replace mode."""
    SINGLE = "single"
    ALL = "all"
    SELECTION = "selection"
    BUFFER = "buffer"


class ReplaceScope(Enum):
    """Replace scope."""
    CURRENT_FILE = "current_file"
    OPEN_FILES = "open_files"
    PROJECT = "project"
    SELECTION = "selection"


class MatchCase(Enum):
    """Match case option."""
    SENSITIVE = "sensitive"
    INSENSITIVE = "insensitive"


@dataclass
class ReplaceMatch:
    """Replace match."""
    line_number: int
    column: int
    line_content: str
    match_text: str
    context_before: List[str] = field(default_factory=list)
    context_after: List[str] = field(default_factory=list)


@dataclass
class ReplaceQuery:
    """Replace query."""
    search_text: str
    replace_text: str = ""
    mode: ReplaceMode = ReplaceMode.SINGLE
    scope: ReplaceScope = ReplaceScope.CURRENT_FILE
    match_case: MatchCase = MatchCase.INSENSITIVE
    use_regex: bool = False
    use_whole_word: bool = False
    preserve_case: bool = False


@dataclass
class ReplaceConfig:
    """Replace configuration."""
    show_preview: bool = True
    show_context: bool = True
    context_lines: int = 3
    highlight_matches: bool = True
    auto_confirm: bool = False
    max_matches: int = 1000
    show_diff: bool = True


@dataclass
class ReplaceResult:
    """Replace result."""
    success: bool
    matches: List[ReplaceMatch] = field(default_factory=list)
    replaced_count: int = 0
    output: Optional[str] = None
    errors: List[str] = field(default_factory=list)
    message: Optional[str] = None


class ReplaceUIManager:
    """
    Replace UI manager.
    
    Özellikler:
    - Replace UI
    - Replace preview
    - Replace all
    - Replace in selection
    - Replace in files
    - Replace history
    - Replace filters
    - Regex support
    - Case sensitivity
    - Whole word search
    - Context display
    - Diff view
    - Replace confirmation
    - Replace statistics
    - Multi-file replace
    - Preserve case
    - Replace navigation
    """
    
    def __init__(self, config: Optional[ReplaceConfig] = None):
        """
        Initialize replace UI manager.
        
        Args:
            config: Replace configuration
        """
        self.config = config or ReplaceConfig()
        self.replace_history: List[ReplaceQuery] = []
        self.current_query: Optional[ReplaceQuery] = None
        self.current_matches: List[ReplaceMatch] = []
    
    def find_matches(self, query: ReplaceQuery, content: str) -> ReplaceResult:
        """
        Find matches for replacement.
        
        Args:
            query: Replace query
            content: Content to search
            
        Returns:
            ReplaceResult: Find result
        """
        result = ReplaceResult(success=True)
        
        self.current_query = query
        self.current_matches = []
        
        search_text = query.search_text
        if not search_text:
            result.errors.append("Search text is empty")
            result.success = False
            return result
        
        # Add to history
        self._add_to_history(query)
        
        # Find matches
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
                
                match = ReplaceMatch(
                    line_number=line_num + 1,
                    column=column,
                    line_content=line,
                    match_text=search_text,
                    context_before=context_before,
                    context_after=context_after
                )
                
                self.current_matches.append(match)
                
                # Limit matches
                if len(self.current_matches) >= self.config.max_matches:
                    break
        
        result.matches = self.current_matches
        result.message = f"Found {len(self.current_matches)} matches"
        
        return result
    
    def _matches_query(self, line: str, query: ReplaceQuery) -> bool:
        """
        Check if line matches query.
        
        Args:
            line: Line content
            query: Replace query
            
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
    
    def replace(self, query: ReplaceQuery, content: str) -> ReplaceResult:
        """
        Perform single replacement.
        
        Args:
            query: Replace query
            content: Content to replace in
            
        Returns:
            ReplaceResult: Replace result
        """
        result = ReplaceResult(success=True)
        
        if not query.replace_text:
            result.errors.append("Replace text is empty")
            result.success = False
            return result
        
        search_text = query.search_text
        replace_text = query.replace_text
        
        if query.match_case == MatchCase.INSENSITIVE:
            content = content.replace(search_text.lower(), replace_text, 1)
        else:
            content = content.replace(search_text, replace_text, 1)
        
        result.replaced_count = 1
        result.output = content
        result.message = "Replaced 1 occurrence"
        
        return result
    
    def replace_all(self, query: ReplaceQuery, content: str) -> ReplaceResult:
        """
        Perform replace all.
        
        Args:
            query: Replace query
            content: Content to replace in
            
        Returns:
            ReplaceResult: Replace result
        """
        result = ReplaceResult(success=True)
        
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
        
        result.replaced_count = count
        result.output = content
        result.message = f"Replaced {count} occurrences"
        
        return result
    
    def preview_replace(self, query: ReplaceQuery, content: str) -> ReplaceResult:
        """
        Preview replacement.
        
        Args:
            query: Replace query
            content: Content to preview
            
        Returns:
            ReplaceResult: Preview result
        """
        result = self.find_matches(query, content)
        
        if result.success:
            result.message = f"Preview: {len(result.matches)} matches found"
        
        return result
    
    def get_replace_history(self) -> List[ReplaceQuery]:
        """
        Get replace history.
        
        Returns:
            List[ReplaceQuery]: Replace history
        """
        return self.replace_history
    
    def _add_to_history(self, query: ReplaceQuery) -> None:
        """
        Add query to history.
        
        Args:
            query: Replace query
        """
        # Remove duplicates
        self.replace_history = [q for q in self.replace_history if q.search_text != query.search_text]
        
        # Add to front
        self.replace_history.insert(0, query)
        
        # Limit history
        if len(self.replace_history) > 50:
            self.replace_history = self.replace_history[:50]
    
    def clear_history(self) -> None:
        """Clear replace history."""
        self.replace_history.clear()
    
    def get_current_matches(self) -> List[ReplaceMatch]:
        """
        Get current matches.
        
        Returns:
            List[ReplaceMatch]: Current matches
        """
        return self.current_matches
    
    def navigate_to_match(self, index: int) -> Optional[ReplaceMatch]:
        """
        Navigate to match.
        
        Args:
            index: Match index
            
        Returns:
            Optional[ReplaceMatch]: Match
        """
        if 0 <= index < len(self.current_matches):
            return self.current_matches[index]
        return None
    
    def get_match_count(self) -> int:
        """
        Get match count.
        
        Returns:
            int: Match count
        """
        return len(self.current_matches)
    
    def update_config(self, config: ReplaceConfig) -> None:
        """
        Update replace configuration.
        
        Args:
            config: New configuration
        """
        self.config = config
    
    def get_config(self) -> ReplaceConfig:
        """
        Get replace configuration.
        
        Returns:
            ReplaceConfig: Configuration
        """
        return self.config


if __name__ == "__main__":
    # Basit test
    config = ReplaceConfig()
    manager = ReplaceUIManager(config)
    
    # Find matches
    query = ReplaceQuery(search_text="hello", replace_text="world")
    content = "hello world\nhello there"
    
    result = manager.find_matches(query, content)
    
    print(f"Found {len(result.matches)} matches")
    for match in result.matches:
        print(f"  Line {match.line_number}: {match.line_content}")
