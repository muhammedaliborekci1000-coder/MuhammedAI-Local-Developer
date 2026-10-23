"""
Quality Test: File Tree
File tree system testleri.
"""

import sys
import os
import tempfile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.file_tree import (
    FileTreeManager,
    FileType,
    FileCategory,
    FileNode,
    FileTreeResult
)


def test_build_tree():
    """
    Test: Build file tree.
    """
    print("=" * 70)
    print("TEST: Build File Tree")
    print("=" * 70)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Test dosyaları oluştur
        os.makedirs(os.path.join(tmpdir, "src"))
        with open(os.path.join(tmpdir, "src", "main.py"), "w") as f:
            f.write("def main():\n    pass")
        
        manager = FileTreeManager(tmpdir)
        result = manager.build_tree()
        
        assert result.success, "Tree building başarılı olmalı"
        assert result.root is not None, "Root node olmalı"
        
        print(f"  Success: {result.success}")
        print(f"  Total files: {result.total_files}")
        print(f"  Total directories: {result.total_directories}")
        print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Build file tree")
    print("=" * 70)


def test_expand_node():
    """
    Test: Expand node.
    """
    print("=" * 70)
    print("TEST: Expand Node")
    print("=" * 70)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Test dosyaları oluştur
        os.makedirs(os.path.join(tmpdir, "src"))
        with open(os.path.join(tmpdir, "src", "main.py"), "w") as f:
            f.write("def main():\n    pass")
        
        manager = FileTreeManager(tmpdir)
        manager.build_tree()
        
        # src dizinini genişlet
        src_path = os.path.join(tmpdir, "src")
        result = manager.expand_node(src_path)
        
        assert result.success, "Expansion başarılı olmalı"
        
        print(f"  Success: {result.success}")
        print(f"  Message: {result.message}")
    
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
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Test dosyaları oluştur
        os.makedirs(os.path.join(tmpdir, "src"))
        with open(os.path.join(tmpdir, "src", "main.py"), "w") as f:
            f.write("def main():\n    pass")
        
        manager = FileTreeManager(tmpdir)
        manager.build_tree()
        
        # src dizinini daralt
        src_path = os.path.join(tmpdir, "src")
        result = manager.collapse_node(src_path)
        
        assert result.success, "Collapse başarılı olmalı"
        
        print(f"  Success: {result.success}")
        print(f"  Message: {result.message}")
    
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
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Test dosyaları oluştur
        with open(os.path.join(tmpdir, "main.py"), "w") as f:
            f.write("def main():\n    pass")
        
        manager = FileTreeManager(tmpdir)
        manager.build_tree()
        
        # main.py dosyasını seç
        main_path = os.path.join(tmpdir, "main.py")
        result = manager.select_node(main_path)
        
        assert result.success, "Selection başarılı olmalı"
        assert result.selected_node is not None, "Seçilen node olmalı"
        
        print(f"  Success: {result.success}")
        print(f"  Selected node: {result.selected_node.name if result.selected_node else None}")
        print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Select node")
    print("=" * 70)


def test_search_nodes():
    """
    Test: Search nodes.
    """
    print("=" * 70)
    print("TEST: Search Nodes")
    print("=" * 70)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Test dosyaları oluştur
        with open(os.path.join(tmpdir, "main.py"), "w") as f:
            f.write("def main():\n    pass")
        with open(os.path.join(tmpdir, "utils.py"), "w") as f:
            f.write("def helper():\n    pass")
        
        manager = FileTreeManager(tmpdir)
        manager.build_tree()
        
        # "main" ile ara
        results = manager.search_nodes("main")
        
        assert len(results) > 0, "Sonuç bulunmalı"
        
        print(f"  Search results: {len(results)}")
        print(f"  Node names: {[node.name for node in results]}")
    
    print("\n" + "=" * 70)
    print("PASS: Search nodes")
    print("=" * 70)


def test_filter_by_category():
    """
    Test: Filter by category.
    """
    print("=" * 70)
    print("TEST: Filter by Category")
    print("=" * 70)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Test dosyaları oluştur
        with open(os.path.join(tmpdir, "main.py"), "w") as f:
            f.write("def main():\n    pass")
        with open(os.path.join(tmpdir, "README.md"), "w") as f:
            f.write("# README")
        
        manager = FileTreeManager(tmpdir)
        manager.build_tree()
        
        # Code kategorisi ile filtrele
        code_files = manager.filter_by_category(FileCategory.CODE)
        
        print(f"  Code files: {len(code_files)}")
        print(f"  File names: {[node.name for node in code_files]}")
    
    print("\n" + "=" * 70)
    print("PASS: Filter by category")
    print("=" * 70)


def test_get_file_path():
    """
    Test: Get file path.
    """
    print("=" * 70)
    print("TEST: Get File Path")
    print("=" * 70)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Test dosyası oluştur
        with open(os.path.join(tmpdir, "main.py"), "w") as f:
            f.write("def main():\n    pass")
        
        manager = FileTreeManager(tmpdir)
        manager.build_tree()
        
        # Dosya yolunu al
        main_path = os.path.join(tmpdir, "main.py")
        file_path = manager.get_file_path(main_path)
        
        assert file_path == main_path, "Dosya yolu eşleşmeli"
        
        print(f"  File path: {file_path}")
    
    print("\n" + "=" * 70)
    print("PASS: Get file path")
    print("=" * 70)


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
    
    print(f"  All enum values verified")
    print(f"  Total types: {len(FileType)}")
    
    print("\n" + "=" * 70)
    print("PASS: FileType enum")
    print("=" * 70)


def test_file_category_enum():
    """
    Test: FileCategory enum.
    """
    print("=" * 70)
    print("TEST: FileCategory Enum")
    print("=" * 70)
    
    assert FileCategory.CODE.value == "code"
    assert FileCategory.CONFIG.value == "config"
    assert FileCategory.DOCUMENTATION.value == "documentation"
    assert FileCategory.ASSET.value == "asset"
    assert FileCategory.TEST.value == "test"
    assert FileCategory.BUILD.value == "build"
    assert FileCategory.OTHER.value == "other"
    
    print(f"  All enum values verified")
    print(f"  Total categories: {len(FileCategory)}")
    
    print("\n" + "=" * 70)
    print("PASS: FileCategory enum")
    print("=" * 70)


def test_file_node_dataclass():
    """
    Test: FileNode dataclass.
    """
    print("=" * 70)
    print("TEST: FileNode Dataclass")
    print("=" * 70)
    
    node = FileNode(
        name="main.py",
        path="/path/to/main.py",
        type=FileType.FILE,
        category=FileCategory.CODE
    )
    
    assert node.name == "main.py", "Name eşleşmeli"
    assert node.type == FileType.FILE, "Type eşleşmeli"
    assert node.category == FileCategory.CODE, "Category eşleşmeli"
    
    print(f"  Name: {node.name}")
    print(f"  Type: {node.type.value}")
    print(f"  Category: {node.category.value}")
    
    print("\n" + "=" * 70)
    print("PASS: FileNode dataclass")
    print("=" * 70)


def test_file_tree_result_dataclass():
    """
    Test: FileTreeResult dataclass.
    """
    print("=" * 70)
    print("TEST: FileTreeResult Dataclass")
    print("=" * 70)
    
    result = FileTreeResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.all_nodes, list), "All nodes list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  All nodes: {len(result.all_nodes)}")
    
    print("\n" + "=" * 70)
    print("PASS: FileTreeResult dataclass")
    print("=" * 70)


def test_file_category_detection():
    """
    Test: File category detection.
    """
    print("=" * 70)
    print("TEST: File Category Detection")
    print("=" * 70)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        manager = FileTreeManager(tmpdir)
        
        # Code dosyası
        with open(os.path.join(tmpdir, "main.py"), "w") as f:
            f.write("def main():\n    pass")
        
        # Config dosyası
        with open(os.path.join(tmpdir, "config.json"), "w") as f:
            f.write("{}")
        
        # Documentation dosyası
        with open(os.path.join(tmpdir, "README.md"), "w") as f:
            f.write("# README")
        
        manager.build_tree()
        
        code_files = manager.filter_by_category(FileCategory.CODE)
        config_files = manager.filter_by_category(FileCategory.CONFIG)
        doc_files = manager.filter_by_category(FileCategory.DOCUMENTATION)
        
        print(f"  Code files: {len(code_files)}")
        print(f"  Config files: {len(config_files)}")
        print(f"  Documentation files: {len(doc_files)}")
    
    print("\n" + "=" * 70)
    print("PASS: File category detection")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_build_tree()
        test2 = test_expand_node()
        test3 = test_collapse_node()
        test4 = test_select_node()
        test5 = test_search_nodes()
        test6 = test_filter_by_category()
        test7 = test_get_file_path()
        test8 = test_file_type_enum()
        test9 = test_file_category_enum()
        test10 = test_file_node_dataclass()
        test11 = test_file_tree_result_dataclass()
        test12 = test_file_category_detection()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Build Tree: {'PASS' if test1 else 'FAIL'}")
        print(f"Expand Node: {'PASS' if test2 else 'FAIL'}")
        print(f"Collapse Node: {'PASS' if test3 else 'FAIL'}")
        print(f"Select Node: {'PASS' if test4 else 'FAIL'}")
        print(f"Search Nodes: {'PASS' if test5 else 'FAIL'}")
        print(f"Filter by Category: {'PASS' if test6 else 'FAIL'}")
        print(f"Get File Path: {'PASS' if test7 else 'FAIL'}")
        print(f"FileType Enum: {'PASS' if test8 else 'FAIL'}")
        print(f"FileCategory Enum: {'PASS' if test9 else 'FAIL'}")
        print(f"FileNode Dataclass: {'PASS' if test10 else 'FAIL'}")
        print(f"FileTreeResult Dataclass: {'PASS' if test11 else 'FAIL'}")
        print(f"File Category Detection: {'PASS' if test12 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12])
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
