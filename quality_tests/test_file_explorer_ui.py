"""
Quality Test: File Explorer UI
File explorer UI system testleri for UI module.
"""

import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from app.ui.file_explorer_ui import (
    FileType,
    ViewMode,
    SortBy,
    FileNode,
    FileExplorerConfig,
    FileExplorerResult,
    FileExplorerUIManager
)
from datetime import datetime


def test_file_type_enum():
    """
    Test: FileType enum.
    """
    print("=" * 70)
    print("TEST: FileType Enum")
    print("=" * 70)
    
    assert FileType.FILE.value == "file"
    assert FileType.DIRECTORY.value == "directory"
    assert FileType.SYMLINK.value == "symlink"
    assert FileType.HIDDEN.value == "hidden"
    assert FileType.ARCHIVE.value == "archive"
    assert FileType.IMAGE.value == "image"
    assert FileType.VIDEO.value == "video"
    assert FileType.AUDIO.value == "audio"
    assert FileType.DOCUMENT.value == "document"
    assert FileType.CODE.value == "code"
    assert FileType.CUSTOM.value == "custom"
    
    print(f"  All enum values verified")
    print(f"  Total types: {len(FileType)}")
    
    print("\n" + "=" * 70)
    print("PASS: FileType enum")
    print("=" * 70)


def test_view_mode_enum():
    """
    Test: ViewMode enum.
    """
    print("=" * 70)
    print("TEST: ViewMode Enum")
    print("=" * 70)
    
    assert ViewMode.LIST.value == "list"
    assert ViewMode.TREE.value == "tree"
    assert ViewMode.GRID.value == "grid"
    assert ViewMode.DETAILS.value == "details"
    assert ViewMode.CUSTOM.value == "custom"
    
    print(f"  All enum values verified")
    print(f"  Total modes: {len(ViewMode)}")
    
    print("\n" + "=" * 70)
    print("PASS: ViewMode enum")
    print("=" * 70)


def test_sort_by_enum():
    """
    Test: SortBy enum.
    """
    print("=" * 70)
    print("TEST: SortBy Enum")
    print("=" * 70)
    
    assert SortBy.NAME.value == "name"
    assert SortBy.SIZE.value == "size"
    assert SortBy.TYPE.value == "type"
    assert SortBy.MODIFIED.value == "modified"
    assert SortBy.CREATED.value == "created"
    assert SortBy.CUSTOM.value == "custom"
    
    print(f"  All enum values verified")
    print(f"  Total sorts: {len(SortBy)}")
    
    print("\n" + "=" * 70)
    print("PASS: SortBy enum")
    print("=" * 70)


def test_file_node_dataclass():
    """
    Test: FileNode dataclass.
    """
    print("=" * 70)
    print("TEST: FileNode Dataclass")
    print("=" * 70)
    
    node = FileNode(
        id="node_1",
        name="test.py",
        path="/test.py",
        type=FileType.FILE
    )
    
    assert node.id == "node_1", "ID eşleşmeli"
    assert node.name == "test.py", "Name eşleşmeli"
    assert node.path == "/test.py", "Path eşleşmeli"
    assert node.type == FileType.FILE, "Type eşleşmeli"
    
    print(f"  ID: {node.id}")
    print(f"  Name: {node.name}")
    print(f"  Type: {node.type.value}")
    
    print("\n" + "=" * 70)
    print("PASS: FileNode dataclass")
    print("=" * 70)


def test_file_explorer_config_dataclass():
    """
    Test: FileExplorerConfig dataclass.
    """
    print("=" * 70)
    print("TEST: FileExplorerConfig Dataclass")
    print("=" * 70)
    
    config = FileExplorerConfig(
        enabled=True,
        show_hidden_files=False
    )
    
    assert config.enabled == True, "Enabled eşleşmeli"
    assert config.show_hidden_files == False, "Show hidden files eşleşmeli"
    
    print(f"  Enabled: {config.enabled}")
    print(f"  Show hidden files: {config.show_hidden_files}")
    
    print("\n" + "=" * 70)
    print("PASS: FileExplorerConfig dataclass")
    print("=" * 70)


def test_file_explorer_result_dataclass():
    """
    Test: FileExplorerResult dataclass.
    """
    print("=" * 70)
    print("TEST: FileExplorerResult Dataclass")
    print("=" * 70)
    
    result = FileExplorerResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.nodes, list), "Nodes list olmalı"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Nodes: {len(result.nodes)}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: FileExplorerResult dataclass")
    print("=" * 70)


def test_file_explorer_ui_manager_initialization():
    """
    Test: FileExplorerUIManager initialization.
    """
    print("=" * 70)
    print("TEST: FileExplorerUIManager Initialization")
    print("=" * 70)
    
    config = FileExplorerConfig()
    manager = FileExplorerUIManager(config)
    
    assert manager.config == config, "Config eşleşmeli"
    assert len(manager.nodes) == 0, "Nodes boş olmalı"
    assert manager.root_node_id is None, "Root node None olmalı"
    
    print(f"  Nodes: {len(manager.nodes)}")
    print(f"  Root node: {manager.root_node_id}")
    
    print("\n" + "=" * 70)
    print("PASS: FileExplorerUIManager initialization")
    print("=" * 70)


def test_add_node():
    """
    Test: Add node.
    """
    print("=" * 70)
    print("TEST: Add Node")
    print("=" * 70)
    
    manager = FileExplorerUIManager()
    
    node = FileNode(
        id="",
        name="test.py",
        path="/test.py",
        type=FileType.FILE
    )
    
    result = manager.add_node(node)
    
    assert result.success == True, "Ekleme başarılı olmalı"
    assert result.node is not None, "Node olmalı"
    assert len(manager.nodes) > 0, "Node eklenmeli"
    
    print(f"  Node added: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add node")
    print("=" * 70)


def test_remove_node():
    """
    Test: Remove node.
    """
    print("=" * 70)
    print("TEST: Remove Node")
    print("=" * 70)
    
    manager = FileExplorerUIManager()
    
    node = FileNode(
        id="",
        name="test.py",
        path="/test.py",
        type=FileType.FILE
    )
    
    result = manager.add_node(node)
    node_id = result.node.id
    
    result = manager.remove_node(node_id)
    
    assert result.success == True, "Silme başarılı olmalı"
    assert node_id not in manager.nodes, "Node silinmeli"
    
    print(f"  Node removed: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Remove node")
    print("=" * 70)


def test_get_node():
    """
    Test: Get node.
    """
    print("=" * 70)
    print("TEST: Get Node")
    print("=" * 70)
    
    manager = FileExplorerUIManager()
    
    node = FileNode(
        id="",
        name="test.py",
        path="/test.py",
        type=FileType.FILE
    )
    
    result = manager.add_node(node)
    node_id = result.node.id
    
    retrieved_node = manager.get_node(node_id)
    
    assert retrieved_node is not None, "Node bulunmalı"
    assert retrieved_node.id == node_id, "ID eşleşmeli"
    
    print(f"  Node: {retrieved_node.name}")
    
    print("\n" + "=" * 70)
    print("PASS: Get node")
    print("=" * 70)


def test_get_all_nodes():
    """
    Test: Get all nodes.
    """
    print("=" * 70)
    print("TEST: Get All Nodes")
    print("=" * 70)
    
    manager = FileExplorerUIManager()
    
    node = FileNode(
        id="",
        name="test.py",
        path="/test.py",
        type=FileType.FILE
    )
    
    manager.add_node(node)
    nodes = manager.get_all_nodes()
    
    assert len(nodes) > 0, "Nodes olmalı"
    
    print(f"  Total nodes: {len(nodes)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get all nodes")
    print("=" * 70)


def test_get_root_node():
    """
    Test: Get root node.
    """
    print("=" * 70)
    print("TEST: Get Root Node")
    print("=" * 70)
    
    manager = FileExplorerUIManager()
    
    node = FileNode(
        id="",
        name="root",
        path="/",
        type=FileType.DIRECTORY
    )
    
    manager.add_node(node)
    root_node = manager.get_root_node()
    
    assert root_node is not None, "Root node olmalı"
    assert root_node.name == "root", "Root node eşleşmeli"
    
    print(f"  Root node: {root_node.name}")
    
    print("\n" + "=" * 70)
    print("PASS: Get root node")
    print("=" * 70)


def test_expand_node():
    """
    Test: Expand node.
    """
    print("=" * 70)
    print("TEST: Expand Node")
    print("=" * 70)
    
    manager = FileExplorerUIManager()
    
    node = FileNode(
        id="",
        name="test",
        path="/test",
        type=FileType.DIRECTORY
    )
    
    result = manager.add_node(node)
    node_id = result.node.id
    
    result = manager.expand_node(node_id)
    
    assert result.success == True, "Expand başarılı olmalı"
    
    print(f"  Node expanded: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Expand node")
    print("=" * 70)


def test_collapse_node():
    """
    Test: Collapse node.
    """
    print("=" * 70)
    print("TEST: Collapse Node")
    print("=" * 70)
    
    manager = FileExplorerUIManager()
    
    node = FileNode(
        id="",
        name="test",
        path="/test",
        type=FileType.DIRECTORY
    )
    
    result = manager.add_node(node)
    node_id = result.node.id
    
    manager.expand_node(node_id)
    result = manager.collapse_node(node_id)
    
    assert result.success == True, "Collapse başarılı olmalı"
    
    print(f"  Node collapsed: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Collapse node")
    print("=" * 70)


def test_select_node():
    """
    Test: Select node.
    """
    print("=" * 70)
    print("TEST: Select Node")
    print("=" * 70)
    
    manager = FileExplorerUIManager()
    
    node = FileNode(
        id="",
        name="test.py",
        path="/test.py",
        type=FileType.FILE
    )
    
    result = manager.add_node(node)
    node_id = result.node.id
    
    result = manager.select_node(node_id)
    
    assert result.success == True, "Select başarılı olmalı"
    
    print(f"  Node selected: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Select node")
    print("=" * 70)


def test_deselect_node():
    """
    Test: Deselect node.
    """
    print("=" * 70)
    print("TEST: Deselect Node")
    print("=" * 70)
    
    manager = FileExplorerUIManager()
    
    node = FileNode(
        id="",
        name="test.py",
        path="/test.py",
        type=FileType.FILE
    )
    
    result = manager.add_node(node)
    node_id = result.node.id
    
    manager.select_node(node_id)
    result = manager.deselect_node(node_id)
    
    assert result.success == True, "Deselect başarılı olmalı"
    
    print(f"  Node deselected: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Deselect node")
    print("=" * 70)


def test_get_selected_nodes():
    """
    Test: Get selected nodes.
    """
    print("=" * 70)
    print("TEST: Get Selected Nodes")
    print("=" * 70)
    
    manager = FileExplorerUIManager()
    
    node = FileNode(
        id="",
        name="test.py",
        path="/test.py",
        type=FileType.FILE
    )
    
    result = manager.add_node(node)
    manager.select_node(result.node.id)
    
    selected_nodes = manager.get_selected_nodes()
    
    assert len(selected_nodes) > 0, "Selected nodes olmalı"
    
    print(f"  Selected nodes: {len(selected_nodes)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get selected nodes")
    print("=" * 70)


def test_get_nodes_by_type():
    """
    Test: Get nodes by type.
    """
    print("=" * 70)
    print("TEST: Get Nodes by Type")
    print("=" * 70)
    
    manager = FileExplorerUIManager()
    
    node = FileNode(
        id="",
        name="test.py",
        path="/test.py",
        type=FileType.FILE
    )
    
    manager.add_node(node)
    nodes = manager.get_nodes_by_type(FileType.FILE)
    
    assert len(nodes) > 0, "File nodes olmalı"
    
    print(f"  File nodes: {len(nodes)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get nodes by type")
    print("=" * 70)


def test_search_nodes():
    """
    Test: Search nodes.
    """
    print("=" * 70)
    print("TEST: Search Nodes")
    print("=" * 70)
    
    manager = FileExplorerUIManager()
    
    node = FileNode(
        id="",
        name="test.py",
        path="/test.py",
        type=FileType.FILE
    )
    
    manager.add_node(node)
    nodes = manager.search_nodes("test")
    
    assert len(nodes) > 0, "Arama sonucu olmalı"
    
    print(f"  Search results: {len(nodes)}")
    
    print("\n" + "=" * 70)
    print("PASS: Search nodes")
    print("=" * 70)


def test_set_view_mode():
    """
    Test: Set view mode.
    """
    print("=" * 70)
    print("TEST: Set View Mode")
    print("=" * 70)
    
    manager = FileExplorerUIManager()
    
    result = manager.set_view_mode(ViewMode.LIST)
    
    assert result.success == True, "Set başarılı olmalı"
    assert manager.config.view_mode == ViewMode.LIST, "View mode eşleşmeli"
    
    print(f"  View mode set: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set view mode")
    print("=" * 70)


def test_set_sort_by():
    """
    Test: Set sort by.
    """
    print("=" * 70)
    print("TEST: Set Sort By")
    print("=" * 70)
    
    manager = FileExplorerUIManager()
    
    result = manager.set_sort_by(SortBy.SIZE, True)
    
    assert result.success == True, "Set başarılı olmalı"
    assert manager.config.sort_by == SortBy.SIZE, "Sort by eşleşmeli"
    
    print(f"  Sort by set: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set sort by")
    print("=" * 70)


def test_toggle_hidden_files():
    """
    Test: Toggle hidden files.
    """
    print("=" * 70)
    print("TEST: Toggle Hidden Files")
    print("=" * 70)
    
    manager = FileExplorerUIManager()
    
    result = manager.toggle_hidden_files()
    
    assert result.success == True, "Toggle başarılı olmalı"
    
    print(f"  Hidden files toggled: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Toggle hidden files")
    print("=" * 70)


def test_clear_all_nodes():
    """
    Test: Clear all nodes.
    """
    print("=" * 70)
    print("TEST: Clear All Nodes")
    print("=" * 70)
    
    manager = FileExplorerUIManager()
    
    node = FileNode(
        id="",
        name="test.py",
        path="/test.py",
        type=FileType.FILE
    )
    
    manager.add_node(node)
    result = manager.clear_all_nodes()
    
    assert result.success == True, "Clear başarılı olmalı"
    assert len(manager.nodes) == 0, "Nodes temizlenmeli"
    
    print(f"  Nodes cleared: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear all nodes")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    manager = FileExplorerUIManager()
    
    new_config = FileExplorerConfig(max_depth=20)
    result = manager.update_config(new_config)
    
    assert result.success == True, "Update başarılı olmalı"
    assert manager.config.max_depth == 20, "Config güncellenmeli"
    
    print(f"  Max depth: {manager.config.max_depth}")
    
    print("\n" + "=" * 70)
    print("PASS: Update config")
    print("=" * 70)


def test_get_config():
    """
    Test: Get config.
    """
    print("=" * 70)
    print("TEST: Get Config")
    print("=" * 70)
    
    config = FileExplorerConfig(max_depth=20)
    manager = FileExplorerUIManager(config)
    
    retrieved_config = manager.get_config()
    
    assert retrieved_config.max_depth == 20, "Config eşleşmeli"
    
    print(f"  Max depth: {retrieved_config.max_depth}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_file_type_enum()
        test2 = test_view_mode_enum()
        test3 = test_sort_by_enum()
        test4 = test_file_node_dataclass()
        test5 = test_file_explorer_config_dataclass()
        test6 = test_file_explorer_result_dataclass()
        test7 = test_file_explorer_ui_manager_initialization()
        test8 = test_add_node()
        test9 = test_remove_node()
        test10 = test_get_node()
        test11 = test_get_all_nodes()
        test12 = test_get_root_node()
        test13 = test_expand_node()
        test14 = test_collapse_node()
        test15 = test_select_node()
        test16 = test_deselect_node()
        test17 = test_get_selected_nodes()
        test18 = test_get_nodes_by_type()
        test19 = test_search_nodes()
        test20 = test_set_view_mode()
        test21 = test_set_sort_by()
        test22 = test_toggle_hidden_files()
        test23 = test_clear_all_nodes()
        test24 = test_update_config()
        test25 = test_get_config()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"FileType Enum: {'PASS' if test1 else 'FAIL'}")
        print(f"ViewMode Enum: {'PASS' if test2 else 'FAIL'}")
        print(f"SortBy Enum: {'PASS' if test3 else 'FAIL'}")
        print(f"FileNode Dataclass: {'PASS' if test4 else 'FAIL'}")
        print(f"FileExplorerConfig Dataclass: {'PASS' if test5 else 'FAIL'}")
        print(f"FileExplorerResult Dataclass: {'PASS' if test6 else 'FAIL'}")
        print(f"FileExplorerUIManager Initialization: {'PASS' if test7 else 'FAIL'}")
        print(f"Add Node: {'PASS' if test8 else 'FAIL'}")
        print(f"Remove Node: {'PASS' if test9 else 'FAIL'}")
        print(f"Get Node: {'PASS' if test10 else 'FAIL'}")
        print(f"Get All Nodes: {'PASS' if test11 else 'FAIL'}")
        print(f"Get Root Node: {'PASS' if test12 else 'FAIL'}")
        print(f"Expand Node: {'PASS' if test13 else 'FAIL'}")
        print(f"Collapse Node: {'PASS' if test14 else 'FAIL'}")
        print(f"Select Node: {'PASS' if test15 else 'FAIL'}")
        print(f"Deselect Node: {'PASS' if test16 else 'FAIL'}")
        print(f"Get Selected Nodes: {'PASS' if test17 else 'FAIL'}")
        print(f"Get Nodes by Type: {'PASS' if test18 else 'FAIL'}")
        print(f"Search Nodes: {'PASS' if test19 else 'FAIL'}")
        print(f"Set View Mode: {'PASS' if test20 else 'FAIL'}")
        print(f"Set Sort By: {'PASS' if test21 else 'FAIL'}")
        print(f"Toggle Hidden Files: {'PASS' if test22 else 'FAIL'}")
        print(f"Clear All Nodes: {'PASS' if test23 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test24 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test25 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14, test15, test16, test17, test18, test19, test20, test21, test22, test23, test24, test25])
        print(f"\nTOPLAM: {'PASS' if all_passed else 'FAIL'}")
        print("=" * 70)
        
        sys.exit(0 if all_passed else 1)
    except Exception as e:
        print(f"\nTEST HATASI:")
        print("-" * 70)
        import traceback
        traceback.print_exc()
        print("=" * 70)
        sys.exit(1)
