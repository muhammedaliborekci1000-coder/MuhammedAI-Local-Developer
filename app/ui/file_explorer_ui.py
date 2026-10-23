"""
MuhammedAI Local Developer - File Explorer UI
File explorer UI system for web UI.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime


class FileType(Enum):
    """File type."""
    FILE = "file"
    DIRECTORY = "directory"
    SYMLINK = "symlink"
    HIDDEN = "hidden"
    ARCHIVE = "archive"
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    DOCUMENT = "document"
    CODE = "code"
    CUSTOM = "custom"


class ViewMode(Enum):
    """View mode."""
    LIST = "list"
    TREE = "tree"
    GRID = "grid"
    DETAILS = "details"
    CUSTOM = "custom"


class SortBy(Enum):
    """Sort by."""
    NAME = "name"
    SIZE = "size"
    TYPE = "type"
    MODIFIED = "modified"
    CREATED = "created"
    CUSTOM = "custom"


@dataclass
class FileNode:
    """File node."""
    id: str
    name: str
    path: str
    type: FileType
    size: int = 0
    is_expanded: bool = False
    is_selected: bool = False
    is_visible: bool = True
    parent_id: Optional[str] = None
    children: List[str] = field(default_factory=list)
    modified_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class FileExplorerConfig:
    """File explorer configuration."""
    enabled: bool = True
    show_hidden_files: bool = False
    show_file_sizes: bool = True
    show_file_dates: bool = True
    show_file_icons: bool = True
    enable_drag_drop: bool = True
    enable_multi_select: bool = True
    enable_context_menu: bool = True
    enable_search: bool = True
    enable_filter: bool = True
    view_mode: ViewMode = ViewMode.TREE
    sort_by: SortBy = SortBy.NAME
    sort_ascending: bool = True
    max_depth: int = 10
    auto_refresh: bool = True


@dataclass
class FileExplorerResult:
    """File explorer result."""
    success: bool
    node: Optional[FileNode] = None
    nodes: List[FileNode] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    message: Optional[str] = None


class FileExplorerUIManager:
    """
    File explorer UI manager.
    
    Özellikler:
    - File tree navigation
    - File selection
    - File expansion/collapse
    - View modes (list, tree, grid, details)
    - Sorting options
    - Hidden files
    - File sizes
    - File dates
    - File icons
    - Drag and drop
    - Multi select
    - Context menu
    - Search
    - Filter
    - Auto refresh
    """
    
    def __init__(self, config: Optional[FileExplorerConfig] = None):
        """
        Initialize file explorer UI manager.
        
        Args:
            config: File explorer configuration
        """
        self.config = config or FileExplorerConfig()
        self.nodes: Dict[str, FileNode] = {}
        self.root_node_id: Optional[str] = None
        self.selected_node_ids: List[str] = []
        self.node_id_counter = 0
        self._next_node_id()
    
    def _next_node_id(self) -> str:
        """
        Generate next node ID.
        
        Returns:
            str: Node ID
        """
        self.node_id_counter += 1
        return f"node_{self.node_id_counter}"
    
    def add_node(self, node: FileNode) -> FileExplorerResult:
        """
        Add a file node.
        
        Args:
            node: File node to add
            
        Returns:
            FileExplorerResult: Add result
        """
        result = FileExplorerResult(success=True)
        
        try:
            if not node.id:
                node.id = self._next_node_id()
            
            self.nodes[node.id] = node
            
            # Set as root if no root exists
            if not self.root_node_id:
                self.root_node_id = node.id
            
            # Add to parent's children if parent exists
            if node.parent_id and node.parent_id in self.nodes:
                self.nodes[node.parent_id].children.append(node.id)
            
            result.node = node
            result.nodes = self.get_all_nodes()
            result.message = f"Node '{node.id}' added"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def remove_node(self, node_id: str) -> FileExplorerResult:
        """
        Remove a file node.
        
        Args:
            node_id: Node ID
            
        Returns:
            FileExplorerResult: Remove result
        """
        result = FileExplorerResult(success=False)
        
        try:
            if node_id in self.nodes:
                node = self.nodes[node_id]
                
                # Remove from parent's children
                if node.parent_id and node.parent_id in self.nodes:
                    parent = self.nodes[node.parent_id]
                    if node_id in parent.children:
                        parent.children.remove(node_id)
                
                # Remove children recursively
                for child_id in node.children[:]:
                    self.remove_node(child_id)
                
                del self.nodes[node_id]
                
                if self.root_node_id == node_id:
                    self.root_node_id = None
                
                if node_id in self.selected_node_ids:
                    self.selected_node_ids.remove(node_id)
                
                result.success = True
                result.nodes = self.get_all_nodes()
                result.message = f"Node '{node_id}' removed"
            else:
                result.errors.append("Node not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_node(self, node_id: str) -> Optional[FileNode]:
        """
        Get node by ID.
        
        Args:
            node_id: Node ID
            
        Returns:
            Optional[FileNode]: Node
        """
        return self.nodes.get(node_id)
    
    def get_all_nodes(self) -> List[FileNode]:
        """
        Get all nodes.
        
        Returns:
            List[FileNode]: All nodes
        """
        return list(self.nodes.values())
    
    def get_root_node(self) -> Optional[FileNode]:
        """
        Get root node.
        
        Returns:
            Optional[FileNode]: Root node
        """
        if self.root_node_id:
            return self.nodes.get(self.root_node_id)
        return None
    
    def expand_node(self, node_id: str) -> FileExplorerResult:
        """
        Expand a node.
        
        Args:
            node_id: Node ID
            
        Returns:
            FileExplorerResult: Expand result
        """
        result = FileExplorerResult(success=False)
        
        try:
            node = self.nodes.get(node_id)
            if node:
                node.is_expanded = True
                result.success = True
                result.node = node
                result.message = f"Node '{node_id}' expanded"
            else:
                result.errors.append("Node not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def collapse_node(self, node_id: str) -> FileExplorerResult:
        """
        Collapse a node.
        
        Args:
            node_id: Node ID
            
        Returns:
            FileExplorerResult: Collapse result
        """
        result = FileExplorerResult(success=False)
        
        try:
            node = self.nodes.get(node_id)
            if node:
                node.is_expanded = False
                result.success = True
                result.node = node
                result.message = f"Node '{node_id}' collapsed"
            else:
                result.errors.append("Node not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def select_node(self, node_id: str, multi_select: bool = False) -> FileExplorerResult:
        """
        Select a node.
        
        Args:
            node_id: Node ID
            multi_select: Enable multi-select
            
        Returns:
            FileExplorerResult: Select result
        """
        result = FileExplorerResult(success=False)
        
        try:
            node = self.nodes.get(node_id)
            if node:
                if not multi_select or not self.config.enable_multi_select:
                    # Clear previous selection
                    for selected_id in self.selected_node_ids:
                        if selected_id in self.nodes:
                            self.nodes[selected_id].is_selected = False
                    self.selected_node_ids.clear()
                
                node.is_selected = True
                if node_id not in self.selected_node_ids:
                    self.selected_node_ids.append(node_id)
                
                result.success = True
                result.node = node
                result.message = f"Node '{node_id}' selected"
            else:
                result.errors.append("Node not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def deselect_node(self, node_id: str) -> FileExplorerResult:
        """
        Deselect a node.
        
        Args:
            node_id: Node ID
            
        Returns:
            FileExplorerResult: Deselect result
        """
        result = FileExplorerResult(success=False)
        
        try:
            node = self.nodes.get(node_id)
            if node:
                node.is_selected = False
                if node_id in self.selected_node_ids:
                    self.selected_node_ids.remove(node_id)
                result.success = True
                result.node = node
                result.message = f"Node '{node_id}' deselected"
            else:
                result.errors.append("Node not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_selected_nodes(self) -> List[FileNode]:
        """
        Get selected nodes.
        
        Returns:
            List[FileNode]: Selected nodes
        """
        return [self.nodes[id] for id in self.selected_node_ids if id in self.nodes]
    
    def get_nodes_by_type(self, file_type: FileType) -> List[FileNode]:
        """
        Get nodes by type.
        
        Args:
            file_type: File type
            
        Returns:
            List[FileNode]: Nodes
        """
        return [n for n in self.nodes.values() if n.type == file_type]
    
    def search_nodes(self, query: str) -> List[FileNode]:
        """
        Search nodes by name.
        
        Args:
            query: Search query
            
        Returns:
            List[FileNode]: Matching nodes
        """
        if not self.config.enable_search:
            return []
        
        return [n for n in self.nodes.values() if query.lower() in n.name.lower()]
    
    def set_view_mode(self, view_mode: ViewMode) -> FileExplorerResult:
        """
        Set view mode.
        
        Args:
            view_mode: View mode
            
        Returns:
            FileExplorerResult: Set result
        """
        result = FileExplorerResult(success=True)
        
        try:
            self.config.view_mode = view_mode
            result.message = f"View mode set to {view_mode.value}"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def set_sort_by(self, sort_by: SortBy, ascending: bool = True) -> FileExplorerResult:
        """
        Set sort by.
        
        Args:
            sort_by: Sort by
            ascending: Sort ascending
            
        Returns:
            FileExplorerResult: Set result
        """
        result = FileExplorerResult(success=True)
        
        try:
            self.config.sort_by = sort_by
            self.config.sort_ascending = ascending
            result.message = f"Sort by {sort_by.value} ({'ascending' if ascending else 'descending'})"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def toggle_hidden_files(self) -> FileExplorerResult:
        """
        Toggle hidden files visibility.
        
        Returns:
            FileExplorerResult: Toggle result
        """
        result = FileExplorerResult(success=True)
        
        try:
            self.config.show_hidden_files = not self.config.show_hidden_files
            
            # Update visibility of hidden files
            for node in self.nodes.values():
                if node.type == FileType.HIDDEN:
                    node.is_visible = self.config.show_hidden_files
            
            result.message = f"Hidden files {'shown' if self.config.show_hidden_files else 'hidden'}"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def clear_all_nodes(self) -> FileExplorerResult:
        """
        Clear all nodes.
        
        Returns:
            FileExplorerResult: Clear result
        """
        result = FileExplorerResult(success=True)
        
        try:
            self.nodes.clear()
            self.root_node_id = None
            self.selected_node_ids.clear()
            result.message = "All nodes cleared"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def update_config(self, config: FileExplorerConfig) -> FileExplorerResult:
        """
        Update file explorer configuration.
        
        Args:
            config: New configuration
            
        Returns:
            FileExplorerResult: Update result
        """
        result = FileExplorerResult(success=True)
        
        try:
            self.config = config
            result.message = "Config updated"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def get_config(self) -> FileExplorerConfig:
        """
        Get file explorer configuration.
        
        Returns:
            FileExplorerConfig: Configuration
        """
        return self.config


if __name__ == "__main__":
    # Basit test
    config = FileExplorerConfig()
    manager = FileExplorerUIManager(config)
    
    # Node ekle
    node = FileNode(
        id="",
        name="test.py",
        path="/test.py",
        type=FileType.FILE
    )
    
    result = manager.add_node(node)
    
    print(f"Node added: {result.message}")
    
    # Tüm node'ları al
    nodes = manager.get_all_nodes()
    
    print(f"Total nodes: {len(nodes)}")
