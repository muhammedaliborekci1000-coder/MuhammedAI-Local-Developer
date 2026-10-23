"""
Quality Test: Enhanced Codebase Index
Codebase index gelişmiş özellikleri testleri.
"""

import sys
import os
import tempfile
import shutil
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.ai.codebase_index import CodebaseIndex


def test_enhanced_indexing():
    """
    Test: Gelişmiş indexing özellikleri.
    """
    print("=" * 70)
    print("TEST: Enhanced Codebase Indexing")
    print("=" * 70)
    
    # Geçici test projesi oluştur
    temp_dir = tempfile.mkdtemp(prefix="muhammedai_test_")
    
    try:
        # Test dosyaları oluştur
        test_files = {
            "base.py": '''class BaseClass:
    """Base class."""
    def base_method(self):
        pass
''',
            "derived.py": '''from base import BaseClass

class DerivedClass(BaseClass):
    """Derived class."""
    def derived_method(self):
        self.base_method()
        print("hello")
''',
            "utils.py": '''def helper_function():
    """Helper function."""
    return "result"

def main():
    result = helper_function()
    print(result)
'''
        }
        
        for filename, content in test_files.items():
            file_path = os.path.join(temp_dir, filename)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        
        print(f"Test projesi: {temp_dir}")
        
        # Index oluştur
        index = CodebaseIndex(project_root=Path(temp_dir))
        index.index_project()
        
        print(f"İndekslenen dosya sayısı: {len(index.files)}")
        
        # Test 1: Base class tracking
        print("\n--- Test 1: Base Class Tracking ---")
        derived_class = None
        for file_index in index.files.values():
            for symbol in file_index.symbols:
                if symbol.name == "DerivedClass":
                    derived_class = symbol
                    break
        
        assert derived_class is not None, "DerivedClass bulunmalı"
        assert "BaseClass" in derived_class.base_classes, "BaseClass base_classes içinde olmalı"
        print(f"  Base classes: {derived_class.base_classes}")
        
        # Test 2: Function call tracking
        print("\n--- Test 2: Function Call Tracking ---")
        main_func = None
        for file_index in index.files.values():
            for symbol in file_index.symbols:
                if symbol.name == "main":
                    main_func = symbol
                    break
        
        assert main_func is not None, "main function bulunmalı"
        assert "helper_function" in main_func.calls, "helper_function calls içinde olmalı"
        print(f"  Calls: {main_func.calls}")
        
        # Test 3: Inheritance hierarchy
        print("\n--- Test 3: Inheritance Hierarchy ---")
        hierarchy = index.get_inheritance_hierarchy("DerivedClass")
        print(f"  Base classes: {hierarchy['base_classes']}")
        print(f"  Derived classes: {hierarchy['derived_classes']}")
        
        # Test 4: Call hierarchy
        print("\n--- Test 4: Call Hierarchy ---")
        call_hierarchy = index.get_call_hierarchy("main")
        print(f"  Calls: {call_hierarchy['calls']}")
        print(f"  Called by: {call_hierarchy['called_by']}")
        
        # Test 5: Find usages
        print("\n--- Test 5: Find Usages ---")
        usages = index.find_usages("helper_function")
        print(f"  Usages count: {len(usages)}")
        if usages:
            print(f"  First usage: {usages[0]}")
        
        # Test 6: Go to definition
        print("\n--- Test 6: Go to Definition ---")
        definition = index.go_to_definition("helper_function", "utils.py", 1)
        assert definition is not None, "Definition bulunmalı"
        print(f"  Definition file: {definition['file']}")
        print(f"  Definition line: {definition['line']}")
        
        print("\n" + "=" * 70)
        print("PASS: Enhanced codebase indexing")
        print("=" * 70)
        
    finally:
        # Temizlik
        shutil.rmtree(temp_dir)
        print(f"Geçici klasör temizlendi: {temp_dir}")


def test_graph_building():
    """
    Test: Graph building.
    """
    print("=" * 70)
    print("TEST: Graph Building")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp(prefix="muhammedai_test_")
    
    try:
        # Test dosyası
        test_file = os.path.join(temp_dir, "test.py")
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write('''
class A:
    def method_a(self):
        pass

class B(A):
    def method_b(self):
        self.method_a()

def func_c():
    a = A()
    a.method_a()
''')
        
        # Index oluştur
        index = CodebaseIndex(project_root=Path(temp_dir))
        index.index_project()
        
        # Test call graph
        print("\n--- Test: Call Graph ---")
        assert len(index.call_graph) > 0, "Call graph dolu olmalı"
        print(f"  Call graph entries: {len(index.call_graph)}")
        
        # Test inheritance graph
        print("\n--- Test: Inheritance Graph ---")
        assert len(index.inheritance_graph) > 0, "Inheritance graph dolu olmalı"
        print(f"  Inheritance graph entries: {len(index.inheritance_graph)}")
        
        print("\n" + "=" * 70)
        print("PASS: Graph building")
        print("=" * 70)
        
    finally:
        shutil.rmtree(temp_dir)


def test_symbol_relationships():
    """
    Test: Symbol relationships.
    """
    print("=" * 70)
    print("TEST: Symbol Relationships")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp(prefix="muhammedai_test_")
    
    try:
        # Test dosyası
        test_file = os.path.join(temp_dir, "test.py")
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write('''
class MyClass:
    """Test class."""
    @property
    def my_property(self):
        return "value"
    
    def my_method(self):
        return self.my_property
''')
        
        # Index oluştur
        index = CodebaseIndex(project_root=Path(temp_dir))
        index.index_project()
        
        # Test decorators
        print("\n--- Test: Decorators ---")
        for file_index in index.files.values():
            for symbol in file_index.symbols:
                if symbol.name == "my_property":
                    print(f"  Decorators: {symbol.decorators}")
                    assert "property" in symbol.decorators, "property decorator olmalı"
        
        # Test docstrings
        print("\n--- Test: Docstrings ---")
        for file_index in index.files.values():
            for symbol in file_index.symbols:
                if symbol.name == "MyClass":
                    print(f"  Docstring: {symbol.docstring}")
                    assert symbol.docstring is not None, "Docstring olmalı"
        
        print("\n" + "=" * 70)
        print("PASS: Symbol relationships")
        print("=" * 70)
        
    finally:
        shutil.rmtree(temp_dir)


if __name__ == "__main__":
    from pathlib import Path
    
    try:
        test1 = test_enhanced_indexing()
        test2 = test_graph_building()
        test3 = test_symbol_relationships()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Enhanced Indexing: {'PASS' if test1 else 'FAIL'}")
        print(f"Graph Building: {'PASS' if test2 else 'FAIL'}")
        print(f"Symbol Relationships: {'PASS' if test3 else 'FAIL'}")
        
        all_passed = test1 and test2 and test3
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
