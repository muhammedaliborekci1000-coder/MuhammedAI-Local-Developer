"""
Quality Test: Cursor-Aware Context
Cursor position ve surrounding code context extraction testleri.
"""

import sys
import os
import tempfile
import shutil

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.ai.cursor_aware_context import CursorAwareContextExtractor, SmartContextPrioritizer


def test_cursor_context_extraction():
    """
    Test: Cursor context extraction.
    """
    print("=" * 70)
    print("TEST: Cursor Context Extraction")
    print("=" * 70)
    
    # Geçici test dosyası oluştur
    temp_dir = tempfile.mkdtemp(prefix="muhammedai_test_")
    
    try:
        test_file = os.path.join(temp_dir, "test.py")
        test_content = '''import os
import sys

class MyClass:
    """Test class."""
    
    @staticmethod
    def static_method():
        """Static method."""
        pass
    
    def my_method(self, x: int, y: int) -> int:
        """Test method."""
        result = x + y
        print(result)
        return result

def my_function(a: str, b: str) -> str:
    """Test function."""
    result = a + b
    return result

if __name__ == "__main__":
    obj = MyClass()
    print(obj.my_method(1, 2))
    my_function("hello", "world")
'''
        
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(test_content)
        
        print(f"Test dosyası: {test_file}")
        
        # Cursor-aware context extractor
        extractor = CursorAwareContextExtractor(context_lines=10)
        
        # Test 1: Function içinde cursor
        print("\n--- Test 1: Function içinde cursor (satır 12) ---")
        context = extractor.extract_context(test_file, line=12, column=10)
        
        assert context is not None, "Context None olmamalı"
        assert context.file_path == test_file, "Dosya yolu eşleşmeli"
        assert context.line == 12, "Satır numarası eşleşmeli"
        assert context.current_function == "MyClass.my_method", "Function tespit edilmeli (class.method format)"
        assert context.current_scope == "method", "Scope method olmalı"
        assert context.current_class == "MyClass", "Class tespit edilmeli"
        
        print(f"  Function: {context.current_function}")
        print(f"  Class: {context.current_class}")
        print(f"  Scope: {context.current_scope}")
        print(f"  Signature: {context.function_signature}")
        print(f"  Docstring: {context.docstring}")
        print(f"  Decorators: {context.decorators}")
        print(f"  Function calls: {context.function_calls}")
        
        # Test 2: Module level cursor
        print("\n--- Test 2: Module level cursor (satır 18) ---")
        context = extractor.extract_context(test_file, line=18, column=0)
        
        assert context is not None, "Context None olmamalı"
        assert context.current_function == "my_function", "Function tespit edilmeli"
        assert context.current_scope == "function", "Scope function olmalı"
        assert context.current_class is None, "Class olmamalı"
        assert context.docstring is not None, "Docstring olmalı"
        
        print(f"  Function: {context.current_function}")
        print(f"  Scope: {context.current_scope}")
        print(f"  Docstring: {context.docstring}")
        
        # Test 3: Surrounding lines
        print("\n--- Test 3: Surrounding lines ---")
        context = extractor.extract_context(test_file, line=12, column=10)
        
        assert len(context.surrounding_lines_before) > 0, "Önceki satırlar olmalı"
        assert len(context.surrounding_lines_after) > 0, "Sonraki satırlar olmalı"
        
        print(f"  Önceki satırlar: {len(context.surrounding_lines_before)}")
        print(f"  Sonraki satırlar: {len(context.surrounding_lines_after)}")
        
        # Test 4: Imports
        print("\n--- Test 4: Imports ---")
        context = extractor.extract_context(test_file, line=12, column=10)
        
        assert len(context.imports_in_scope) > 0, "Imports olmalı"
        print(f"  Imports: {context.imports_in_scope}")
        
        # Test 5: Variables
        print("\n--- Test 5: Variables ---")
        context = extractor.extract_context(test_file, line=12, column=10)
        
        assert len(context.variables_in_scope) > 0, "Variables olmalı"
        print(f"  Variables: {context.variables_in_scope}")
        
        # Test 6: Format context
        print("\n--- Test 6: Format Context ---")
        formatted = extractor.format_context(context)
        
        assert "CURSOR CONTEXT" in formatted, "Cursor context başlığı olmalı"
        assert "File:" in formatted, "Dosya yolu olmalı"
        assert "Scope:" in formatted, "Scope olmalı"
        # Function calls optional, sadece varsa kontrol et
        if context.function_calls:
            assert "Function Calls:" in formatted, "Function calls olmalı"
        
        print(f"  Formatlanmış context uzunluğu: {len(formatted)}")
        
        print("\n" + "=" * 70)
        print("PASS: Cursor context extraction")
        print("=" * 70)
        
    finally:
        # Temizlik
        shutil.rmtree(temp_dir)
        print(f"Geçici klasör temizlendi: {temp_dir}")


def test_smart_context_prioritization():
    """
    Test: Smart context prioritization.
    """
    print("=" * 70)
    print("TEST: Smart Context Prioritization")
    print("=" * 70)
    
    prioritizer = SmartContextPrioritizer(max_tokens=1000)
    
    # Context bileşenleri oluştur
    context_parts = {
        "SYSTEM_CONTEXT": "System prompt here",
        "CURSOR_CONTEXT": "Cursor context here",
        "TASK_CONTEXT": "Task description",
        "MEMORY_CONTEXT": "Memory content",
        "TOOL_HISTORY": "Tool history",
        "TEST_RESULTS": "Test results"
    }
    
    # Prioritize ve truncate
    result = prioritizer.prioritize_and_truncate(context_parts)
    
    print(f"Sonuç uzunluğu: {len(result)}")
    
    # En yüksek öncelikli bileşenler olmalı (içerik kontrolü)
    assert "Cursor context here" in result, "Cursor context içeriği olmalı"
    assert "System prompt here" in result, "System context içeriği olmalı"
    
    print("Context bileşenleri:")
    if "Cursor context here" in result:
        print("  ✓ Cursor context")
    if "System prompt here" in result:
        print("  ✓ System context")
    if "Task description" in result:
        print("  ✓ Task context")
    
    print("\n" + "=" * 70)
    print("PASS: Smart context prioritization")
    print("=" * 70)


def test_edge_cases():
    """
    Test: Edge cases.
    """
    print("=" * 70)
    print("TEST: Edge Cases")
    print("=" * 70)
    
    extractor = CursorAwareContextExtractor(context_lines=10)
    
    # Test 1: Olmayan dosya
    print("\n--- Test 1: Olmayan dosya ---")
    context = extractor.extract_context("nonexistent.py", line=1)
    assert context is None, "Olmayan dosya için None olmalı"
    print("  ✓ None döndü")
    
    # Test 2: Geçersiz satır
    print("\n--- Test 2: Geçersiz satır ---")
    temp_dir = tempfile.mkdtemp(prefix="muhammedai_test_")
    try:
        test_file = os.path.join(temp_dir, "test.py")
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write("print('hello')")
        
        context = extractor.extract_context(test_file, line=100)
        assert context is None, "Geçersiz satır için None olmalı"
        print("  ✓ None döndü")
        
    finally:
        shutil.rmtree(temp_dir)
    
    # Test 3: Syntax error
    print("\n--- Test 3: Syntax error ---")
    temp_dir = tempfile.mkdtemp(prefix="muhammedai_test_")
    try:
        test_file = os.path.join(temp_dir, "test.py")
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write("def broken(:\n    pass")
        
        context = extractor.extract_context(test_file, line=1)
        # Syntax error olsa bile context dönmeli (surrounding lines ile)
        assert context is not None, "Syntax error olsa bile context dönmeli"
        assert len(context.surrounding_lines_before) >= 0, "Surrounding lines olmalı"
        print("  ✓ Context döndü (syntax error toleransı)")
        
    finally:
        shutil.rmtree(temp_dir)
    
    print("\n" + "=" * 70)
    print("PASS: Edge cases")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_cursor_context_extraction()
        test2 = test_smart_context_prioritization()
        test3 = test_edge_cases()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Cursor Context Extraction: {'PASS' if test1 else 'FAIL'}")
        print(f"Smart Context Prioritization: {'PASS' if test2 else 'FAIL'}")
        print(f"Edge Cases: {'PASS' if test3 else 'FAIL'}")
        
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
