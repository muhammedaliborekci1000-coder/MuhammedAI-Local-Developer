"""
MuhammedAI Local Developer - File Tree
File tree management for code editor.
"""

import os
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime


class FileType(Enum):
    """File type."""
    FILE = "file"
    DIRECTORY = "directory"
    SYMLINK = "symlink"


class FileCategory(Enum):
    """File category."""
    CODE = "code"
    CONFIG = "config"
    DOCUMENTATION = "documentation"
    ASSET = "asset"
    TEST = "test"
    BUILD = "build"
    OTHER = "other"


@dataclass
class FileNode:
    """File tree node."""
    name: str
    path: str
    type: FileType
    category: FileCategory = FileCategory.OTHER
    is_expanded: bool = False
    is_selected: bool = False
    children: List['FileNode'] = field(default_factory=list)
    parent: Optional['FileNode'] = None
    size: int = 0
    modified_time: Optional[datetime] = None
    is_hidden: bool = False
    is_readonly: bool = False


@dataclass
class FileTreeResult:
    """File tree result."""
    success: bool
    root: Optional[FileNode] = None
    all_nodes: List[FileNode] = field(default_factory=list)
    selected_node: Optional[FileNode] = None
    total_files: int = 0
    total_directories: int = 0
    errors: List[str] = field(default_factory=list)
    message: Optional[str] = None


class FileTreeManager:
    """
    File tree manager.
    
    Özellikler:
    - File/directory tree construction
    - Tree navigation
    - File/directory operations
    - Search functionality
    - Filtering
    - Expansion/collapse
    - Selection management
    - File type detection
    - Hidden file handling
    - Read-only file detection
    """
    
    def __init__(self, root_path: str):
        """
        Args:
            root_path: Kök dizin yolu
        """
        self.root_path = root_path
        self.root: Optional[FileNode] = None
        self.selected_node: Optional[FileNode] = None
        self.all_nodes: List[FileNode] = []
        self._node_counter = 0
    
    def build_tree(self, include_hidden: bool = False) -> FileTreeResult:
        """
        Dosya ağacını oluştur.
        
        Args:
            include_hidden: Gizli dosyaları dahil et
            
        Returns:
            FileTreeResult: Ağaç oluşturma sonucu
        """
        result = FileTreeResult(success=False)
        
        try:
            if not os.path.exists(self.root_path):
                result.errors.append(f"Path {self.root_path} does not exist")
                return result
            
            # Kök node'u oluştur
            self.root = self._create_node(self.root_path, None, include_hidden)
            
            # Tüm node'ları topla
            self.all_nodes = self._collect_all_nodes(self.root)
            
            # İstatistikleri hesapla
            total_files = sum(1 for node in self.all_nodes if node.type == FileType.FILE)
            total_directories = sum(1 for node in self.all_nodes if node.type == FileType.DIRECTORY)
            
            result.root = self.root
            result.all_nodes = self.all_nodes
            result.selected_node = self.selected_node
            result.total_files = total_files
            result.total_directories = total_directories
            result.success = True
            result.message = f"File tree built: {total_files} files, {total_directories} directories"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def _create_node(
        self,
        path: str,
        parent: Optional[FileNode],
        include_hidden: bool
    ) -> FileNode:
        """Node oluştur."""
        name = os.path.basename(path)
        is_hidden = name.startswith('.')
        is_readonly = not os.access(path, os.W_OK)
        
        # Dosya tipi belirle
        if os.path.isdir(path):
            file_type = FileType.DIRECTORY
            category = FileCategory.OTHER
            children = []
            
            # Çocukları oluştur
            if include_hidden or not is_hidden:
                try:
                    for item in os.listdir(path):
                        item_path = os.path.join(path, item)
                        child = self._create_node(item_path, None, include_hidden)
                        child.parent = None  # Parent sonra ayarlanacak
                        children.append(child)
                except PermissionError:
                    pass
            
            # Çocukları sırala (dizinler önce, sonra dosyalar)
            children.sort(key=lambda x: (x.type != FileType.DIRECTORY, x.name.lower()))
            
            # Parent'ları ayarla
            for child in children:
                child.parent = None
            
        elif os.path.isfile(path):
            file_type = FileType.FILE
            category = self._determine_category(path)
            children = []
        elif os.path.islink(path):
            file_type = FileType.SYMLINK
            category = FileCategory.OTHER
            children = []
        else:
            file_type = FileType.FILE
            category = FileCategory.OTHER
            children = []
        
        # Modified time
        modified_time = None
        try:
            modified_time = datetime.fromtimestamp(os.path.getmtime(path))
        except:
            pass
        
        # Size
        size = 0
        try:
            size = os.path.getsize(path)
        except:
            pass
        
        node = FileNode(
            name=name,
            path=path,
            type=file_type,
            category=category,
            is_hidden=is_hidden,
            is_readonly=is_readonly,
            children=children,
            parent=parent,
            modified_time=modified_time,
            size=size
        )
        
        # Çocukların parent'ını ayarla
        for child in children:
            child.parent = node
        
        return node
    
    def _determine_category(self, path: str) -> FileCategory:
        """Dosya kategorisi belirle."""
        name = os.path.basename(path).lower()
        ext = os.path.splitext(name)[1]
        
        # Code dosyaları
        code_extensions = ['.py', '.js', '.ts', '.java', '.cpp', '.c', '.h', '.go', '.rs', '.rb', '.php']
        if ext in code_extensions:
            return FileCategory.CODE
        
        # Config dosyaları
        config_extensions = ['.json', '.yaml', '.yml', '.xml', '.ini', '.cfg', '.conf', '.toml']
        if ext in config_extensions or name in ['package.json', 'requirements.txt', 'setup.py']:
            return FileCategory.CONFIG
        
        # Documentation dosyaları
        doc_extensions = ['.md', '.rst', '.txt', '.pdf', '.doc', '.docx']
        if ext in doc_extensions:
            return FileCategory.DOCUMENTATION
        
        # Test dosyaları
        if 'test' in name or 'spec' in name or ext in ['.test.js', '.spec.js']:
            return FileCategory.TEST
        
        # Build dosyaları
        build_extensions = ['.lock', '.log', '.cache']
        if ext in build_extensions or name in['__pycache__', 'node_modules', '.git']:
            return FileCategory.BUILD
        
        # Asset dosyaları
        asset_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.css', '.scss', '.less']
        if ext in asset_extensions:
            return FileCategory.ASSET
        
        return FileCategory.OTHER
    
    def _collect_all_nodes(self, node: FileNode) -> List[FileNode]:
        """Tüm node'ları topla."""
        nodes = [node]
        for child in node.children:
            nodes.extend(self._collect_all_nodes(child))
        return nodes
    
    def expand_node(self, node_path: str) -> FileTreeResult:
        """
        Node'u genişlet.
        
        Args:
            node_path: Node yolu
            
        Returns:
            FileTreeResult: Genişletme sonucu
        """
        result = FileTreeResult(success=False)
        
        try:
            node = self._find_node_by_path(node_path)
            if node and node.type == FileType.DIRECTORY:
                node.is_expanded = True
                
                result.root = self.root
                result.all_nodes = self.all_nodes
                result.selected_node = self.selected_node
                result.success = True
                result.message = f"Node '{node.name}' expanded"
            else:
                result.errors.append(f"Node {node_path} not found or not a directory")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def collapse_node(self, node_path: str) -> FileTreeResult:
        """
        Node'u daralt.
        
        Args:
            node_path: Node yolu
            
        Returns:
            FileTreeResult: Daraltma sonucu
        """
        result = FileTreeResult(success=False)
        
        try:
            node = self._find_node_by_path(node_path)
            if node and node.type == FileType.DIRECTORY:
                node.is_expanded = False
                
                result.root = self.root
                result.all_nodes = self.all_nodes
                result.selected_node = self.selected_node
                result.success = True
                result.message = f"Node '{node.name}' collapsed"
            else:
                result.errors.append(f"Node {node_path} not found or not a directory")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def select_node(self, node_path: str) -> FileTreeResult:
        """
        Node'u seç.
        
        Args:
            node_path: Node yolu
            
        Returns:
            FileTreeResult: Seçme sonucu
        """
        result = FileTreeResult(success=False)
        
        try:
            # Önceki seçimi kaldır
            if self.selected_node:
                self.selected_node.is_selected = False
            
            node = self._find_node_by_path(node_path)
            if node:
                node.is_selected = True
                self.selected_node = node
                
                result.root = self.root
                result.all_nodes = self.all_nodes
                result.selected_node = node
                result.success = True
                result.message = f"Node '{node.name}' selected"
            else:
                result.errors.append(f"Node {node_path} not found")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def _find_node_by_path(self, path: str) -> Optional[FileNode]:
        """Yola göre node bul."""
        for node in self.all_nodes:
            if node.path == path:
                return node
        return None
    
    def search_nodes(self, query: str) -> List[FileNode]:
        """
        Node'larda ara.
        
        Args:
            query: Arama sorgusu
            
        Returns:
            List[FileNode]: Eşleşen node'lar
        """
        query_lower = query.lower()
        matching_nodes = []
        
        for node in self.all_nodes:
            if query_lower in node.name.lower():
                matching_nodes.append(node)
        
        return matching_nodes
    
    def filter_by_category(self, category: FileCategory) -> List[FileNode]:
        """
        Kategoriye göre filtrele.
        
        Args:
            category: Dosya kategorisi
            
        Returns:
            List[FileNode]: Filtrelenmiş node'lar
        """
        return [node for node in self.all_nodes if node.category == category]
    
    def get_file_path(self, node_path: str) -> Optional[str]:
        """
        Dosya yolunu al.
        
        Args:
            node_path: Node yolu
            
        Returns:
            Optional[str]: Dosya yolu
        """
        node = self._find_node_by_path(node_path)
        if node and node.type == FileType.FILE:
            return node.path
        return None


if __name__ == "__main__":
    # Basit test
    import tempfile
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Test dosyaları oluştur
        os.makedirs(os.path.join(tmpdir, "src"))
        with open(os.path.join(tmpdir, "src", "main.py"), "w") as f:
            f.write("def main():\n    pass")
        
        manager = FileTreeManager(tmpdir)
        result = manager.build_tree()
        
        print(f"Tree built: {result.success}")
        print(f"Total files: {result.total_files}")
        print(f"Total directories: {result.total_directories}")
