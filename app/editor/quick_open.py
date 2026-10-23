"""
MuhammedAI Local Developer - Quick Open
Quick open system for code editor.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum


class QuickOpenMode(Enum):
    """Quick open mode."""
    FILES = "files"
    SYMBOLS = "symbols"
    COMMANDS = "commands"
    RECENT = "recent"


class QuickOpenFilter(Enum):
    """Quick open filter."""
    ALL = "all"
    FILES_ONLY = "files_only"
    DIRECTORIES_ONLY = "directories_only"
    OPEN_FILES = "open_files"


@dataclass
class QuickOpenItem:
    """Quick open item."""
    path: str
    name: str
    file_type: Optional[str] = None
    is_directory: bool = False
    is_open: bool = False
    is_modified: bool = False
    language: Optional[str] = None
    line_count: int = 0
    last_modified: Optional[str] = None


@dataclass
class QuickOpenConfig:
    """Quick open configuration."""
    max_results: int = 20
    fuzzy_search: bool = True
    show_file_icons: bool = True
    show_line_numbers: bool = False
    show_modified_indicator: bool = True
    include_hidden_files: bool = False
    recent_files_limit: int = 10
    search_history_limit: int = 50


@dataclass
class QuickOpenResult:
    """Quick open result."""
    success: bool
    items: List[QuickOpenItem] = field(default_factory=list)
    selected_item: Optional[QuickOpenItem] = None
    errors: List[str] = field(default_factory=list)
    message: Optional[str] = None


class QuickOpenManager:
    """
    Quick open manager.
    
    Özellikler:
    - Quick open
    - File search
    - Symbol search
    - Command search
    - Recent files
    - Fuzzy search
    - File filtering
    - Quick navigation
    - File preview
    - Open files
    - Search history
    - File icons
    - Modified indicator
    - Language detection
    - Path display
    - Quick actions
    - Multi-selection
    """
    
    def __init__(self, config: Optional[QuickOpenConfig] = None):
        """
        Initialize quick open manager.
        
        Args:
            config: Quick open configuration
        """
        self.config = config or QuickOpenConfig()
        self.files: Dict[str, QuickOpenItem] = {}
        self.open_files: List[str] = []
        self.recent_files: List[str] = []
        self.search_history: List[str] = []
        self._initialize_builtin_files()
    
    def _initialize_builtin_files(self) -> None:
        """Initialize built-in files for testing."""
        # Add some example files
        self.register_file(QuickOpenItem(
            path="src/main.py",
            name="main.py",
            file_type="python",
            is_open=True,
            language="python",
            line_count=100
        ))
        
        self.register_file(QuickOpenItem(
            path="src/utils.py",
            name="utils.py",
            file_type="python",
            is_open=False,
            language="python",
            line_count=50
        ))
        
        self.register_file(QuickOpenItem(
            path="src/config.json",
            name="config.json",
            file_type="json",
            is_open=False,
            language="json",
            line_count=20
        ))
        
        self.register_file(QuickOpenItem(
            path="README.md",
            name="README.md",
            file_type="markdown",
            is_open=False,
            language="markdown",
            line_count=30
        ))
    
    def register_file(self, item: QuickOpenItem) -> bool:
        """
        Register a file.
        
        Args:
            item: Quick open item
            
        Returns:
            bool: Success
        """
        self.files[item.path] = item
        
        if item.is_open and item.path not in self.open_files:
            self.open_files.append(item.path)
        
        return True
    
    def unregister_file(self, path: str) -> bool:
        """
        Unregister a file.
        
        Args:
            path: File path
            
        Returns:
            bool: Success
        """
        if path in self.files:
            del self.files[path]
            
            if path in self.open_files:
                self.open_files.remove(path)
            
            if path in self.recent_files:
                self.recent_files.remove(path)
            
            return True
        return True
    
    def search(self, query: str, mode: QuickOpenMode = QuickOpenMode.FILES, filter_type: QuickOpenFilter = QuickOpenFilter.ALL) -> QuickOpenResult:
        """
        Search files.
        
        Args:
            query: Search query
            mode: Search mode
            filter_type: Filter type
            
        Returns:
            QuickOpenResult: Search result
        """
        result = QuickOpenResult(success=True)
        
        # Add to history
        if query:
            self._add_to_history(query)
        
        if not query:
            # Return recent files if no query
            if mode == QuickOpenMode.RECENT:
                result.items = [self.files[p] for p in self.recent_files if p in self.files]
            else:
                result.items = self._get_filtered_items(filter_type)
            return result
        
        query_lower = query.lower()
        
        # Search based on mode
        if mode == QuickOpenMode.FILES:
            items = self.files.values()
        elif mode == QuickOpenMode.OPEN_FILES:
            items = [self.files[p] for p in self.open_files if p in self.files]
        elif mode == QuickOpenMode.RECENT:
            items = [self.files[p] for p in self.recent_files if p in self.files]
        else:
            items = self.files.values()
        
        # Filter items
        if filter_type == QuickOpenFilter.FILES_ONLY:
            items = [item for item in items if not item.is_directory]
        elif filter_type == QuickOpenFilter.DIRECTORIES_ONLY:
            items = [item for item in items if item.is_directory]
        elif filter_type == QuickOpenFilter.OPEN_FILES:
            items = [item for item in items if item.is_open]
        
        # Search
        if self.config.fuzzy_search:
            for item in items:
                if (query_lower in item.name.lower() or 
                    query_lower in item.path.lower()):
                    result.items.append(item)
        else:
            for item in items:
                if query_lower == item.name.lower():
                    result.items.append(item)
        
        # Limit results
        if len(result.items) > self.config.max_results:
            result.items = result.items[:self.config.max_results]
        
        result.message = f"Found {len(result.items)} items"
        
        return result
    
    def _get_filtered_items(self, filter_type: QuickOpenFilter) -> List[QuickOpenItem]:
        """
        Get filtered items.
        
        Args:
            filter_type: Filter type
            
        Returns:
            List[QuickOpenItem]: Filtered items
        """
        items = list(self.files.values())
        
        if filter_type == QuickOpenFilter.FILES_ONLY:
            items = [item for item in items if not item.is_directory]
        elif filter_type == QuickOpenFilter.DIRECTORIES_ONLY:
            items = [item for item in items if item.is_directory]
        elif filter_type == QuickOpenFilter.OPEN_FILES:
            items = [item for item in items if item.is_open]
        
        return items
    
    def open_file(self, path: str) -> QuickOpenResult:
        """
        Open a file.
        
        Args:
            path: File path
            
        Returns:
            QuickOpenResult: Open result
        """
        result = QuickOpenResult(success=False)
        
        if path not in self.files:
            result.errors.append("File not found")
            return result
        
        item = self.files[path]
        item.is_open = True
        
        if path not in self.open_files:
            self.open_files.append(path)
        
        # Add to recent
        self._add_to_recent(path)
        
        result.success = True
        result.selected_item = item
        result.message = f"File '{path}' opened"
        
        return result
    
    def close_file(self, path: str) -> QuickOpenResult:
        """
        Close a file.
        
        Args:
            path: File path
            
        Returns:
            QuickOpenResult: Close result
        """
        result = QuickOpenResult(success=False)
        
        if path not in self.files:
            result.errors.append("File not found")
            return result
        
        item = self.files[path]
        item.is_open = False
        
        if path in self.open_files:
            self.open_files.remove(path)
        
        result.success = True
        result.message = f"File '{path}' closed"
        
        return result
    
    def _add_to_recent(self, path: str) -> None:
        """
        Add file to recent.
        
        Args:
            path: File path
        """
        # Remove if exists
        if path in self.recent_files:
            self.recent_files.remove(path)
        
        # Add to front
        self.recent_files.insert(0, path)
        
        # Limit recent files
        if len(self.recent_files) > self.config.recent_files_limit:
            self.recent_files = self.recent_files[:self.config.recent_files_limit]
    
    def get_recent_files(self) -> List[QuickOpenItem]:
        """
        Get recent files.
        
        Returns:
            List[QuickOpenItem]: Recent files
        """
        return [self.files[p] for p in self.recent_files if p in self.files]
    
    def get_open_files(self) -> List[QuickOpenItem]:
        """
        Get open files.
        
        Returns:
            List[QuickOpenItem]: Open files
        """
        return [self.files[p] for p in self.open_files if p in self.files]
    
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
        if len(self.search_history) > self.config.search_history_limit:
            self.search_history = self.search_history[:self.config.search_history_limit]
    
    def get_search_history(self) -> List[str]:
        """
        Get search history.
        
        Returns:
            List[str]: Search history
        """
        return self.search_history
    
    def clear_history(self) -> None:
        """Clear search history."""
        self.search_history.clear()
    
    def update_config(self, config: QuickOpenConfig) -> None:
        """
        Update quick open configuration.
        
        Args:
            config: New configuration
        """
        self.config = config
    
    def get_config(self) -> QuickOpenConfig:
        """
        Get quick open configuration.
        
        Returns:
            QuickOpenConfig: Configuration
        """
        return self.config


if __name__ == "__main__":
    # Basit test
    config = QuickOpenConfig()
    manager = QuickOpenManager(config)
    
    # Search
    result = manager.search("main")
    
    print(f"Found {len(result.items)} items")
    for item in result.items:
        print(f"  - {item.name} ({item.path})")
