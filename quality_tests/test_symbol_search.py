"""
Quality Test: Symbol Search
Symbol search system testleri.
"""

import sys
import os
import tempfile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.symbol_search import (
    SymbolSearchEngine,
    SymbolType,
    SymbolScope,
    SearchMode,
    SearchAction,
    Symbol,
    SymbolSearchResult,
    SymbolSearchConfig
)


def test_search_symbols():
    """
    Test: Search symbols.
    """
    print("=" * 70)
    print("TEST: Search Symbols")
    print("=" * 70)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Test dosyası oluştur
        test_code = """
def my_function(x, y):
    result = x + y
    return result

class MyClass:
    def my_method(self):
        pass
"""
        test_file = os.path.join(tmpdir, "test.py")
        with open(test_file, "w") as f:
            f.write(test_code)
        
        engine = SymbolSearchEngine(tmpdir)
        engine.build_index(test_file)
        
        result = engine.search_symbols("my_function")
        
        assert result.success, "Search başarılı olmalı"
        assert result.total_symbols > 0, "Symbol bulunmalı"
        
        print(f"  Success: {result.success}")
        print(f"  Total symbols: {result.total_symbols}")
        print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Search symbols")
    print("=" * 70)


def test_search_by_type():
    """
    Test: Search by symbol type.
    """
    print("=" * 70)
    print("TEST: Search by Symbol Type")
    print("=" * 70)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Test dosyası oluştur
        test_code = """
def my_function():
    pass

class MyClass:
    pass
"""
        test_file = os.path.join(tmpdir, "test.py")
        with open(test_file, "w") as f:
            f.write(test_code)
        
        engine = SymbolSearchEngine(tmpdir)
        engine.build_index(test_file)
        
        result = engine.search_symbols("", SymbolType.FUNCTION)
        
        assert result.success, "Search başarılı olmalı"
        
        print(f"  Success: {result.success}")
        print(f"  Total symbols: {result.total_symbols}")
        print(f"  Symbol type: {result.symbol_type.value if result.symbol_type else None}")
    
    print("\n" + "=" * 70)
    print("PASS: Search by symbol type")
    print("=" * 70)


def test_build_index():
    """
    Test: Build index.
    """
    print("=" * 70)
    print("TEST: Build Index")
    print("=" * 70)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Test dosyası oluştur
        test_code = """
def my_function():
    pass
"""
        test_file = os.path.join(tmpdir, "test.py")
        with open(test_file, "w") as f:
            f.write(test_code)
        
        engine = SymbolSearchEngine(tmpdir)
        result = engine.build_index(test_file)
        
        assert result.success, "Index building başarılı olmalı"
        assert result.total_symbols > 0, "Symbol bulunmalı"
        
        print(f"  Success: {result.success}")
        print(f"  Total symbols: {result.total_symbols}")
        print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Build index")
    print("=" * 70)


def test_find_definition():
    """
    Test: Find definition.
    """
    print("=" * 70)
    print("TEST: Find Definition")
    print("=" * 70)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Test dosyası oluştur
        test_code = """
def my_function(x, y):
    result = x + y
    return result
"""
        test_file = os.path.join(tmpdir, "test.py")
        with open(test_file, "w") as f:
            f.write(test_code)
        
        engine = SymbolSearchEngine(tmpdir)
        result = engine.find_definition("my_function", test_file, 5)
        
        assert result.success, "Definition bulunmalı"
        assert result.total_symbols == 1, "1 symbol bulunmalı"
        assert result.symbols[0].name == "my_function", "İsim eşleşmeli"
        
        print(f"  Definition found: {result.success}")
        print(f"  Symbol name: {result.symbols[0].name if result.symbols else None}")
        print(f"  Symbol type: {result.symbols[0].type.value if result.symbols else None}")
    
    print("\n" + "=" * 70)
    print("PASS: Find definition")
    print("=" * 70)


def test_find_references():
    """
    Test: Find references.
    """
    print("=" * 70)
    print("TEST: Find References")
    print("=" * 70)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Test dosyası oluştur
        test_code = """
def my_function():
    pass

x = my_function()
"""
        test_file = os.path.join(tmpdir, "test.py")
        with open(test_file, "w") as f:
            f.write(test_code)
        
        engine = SymbolSearchEngine(tmpdir)
        result = engine.find_references("my_function", test_file)
        
        assert result.success, "References bulunmalı"
        
        print(f"  References found: {result.total_symbols}")
    
    print("\n" + "=" * 70)
    print("PASS: Find references")
    print("=" * 70)


def test_symbol_type_enum():
    """
    Test: SymbolType enum.
    """
    print("=" * 70)
    print("TEST: SymbolType Enum")
    print("=" * 70)
    
    assert SymbolType.FUNCTION.value == "function"
    assert SymbolType.CLASS.value == "class"
    assert SymbolType.VARIABLE.value == "variable"
    assert SymbolType.METHOD.value == "method"
    assert SymbolType.PARAMETER.value == "parameter"
    assert SymbolType.ATTRIBUTE.value == "attribute"
    assert SymbolType.IMPORT.value == "import"
    assert SymbolType.CONSTANT.value == "constant"
    assert SymbolType.MODULE.value == "module"
    
    print(f"  All enum values verified")
    print(f"  Total types: {len(SymbolType)}")
    
    print("\n" + "=" * 70)
    print("PASS: SymbolType enum")
    print("=" * 70)


def test_symbol_scope_enum():
    """
    Test: SymbolScope enum.
    """
    print("=" * 70)
    print("TEST: SymbolScope Enum")
    print("=" * 70)
    
    assert SymbolScope.GLOBAL.value == "global"
    assert SymbolScope.LOCAL.value == "local"
    assert SymbolScope.CLASS.value == "class"
    assert SymbolScope.FUNCTION.value == "function"
    assert SymbolScope.MODULE.value == "module"
    
    print(f"  All enum values verified")
    print(f"  Total scopes: {len(SymbolScope)}")
    
    print("\n" + "=" * 70)
    print("PASS: SymbolScope enum")
    print("=" * 70)


def test_symbol_dataclass():
    """
    Test: Symbol dataclass.
    """
    print("=" * 70)
    print("TEST: Symbol Dataclass")
    print("=" * 70)
    
    symbol = Symbol(
        name="my_function",
        type=SymbolType.FUNCTION,
        scope=SymbolScope.GLOBAL,
        file_path="/path/to/file.py",
        line=1,
        column=0
    )
    
    assert symbol.name == "my_function", "Name eşleşmeli"
    assert symbol.type == SymbolType.FUNCTION, "Type eşleşmeli"
    assert symbol.scope == SymbolScope.GLOBAL, "Scope eşleşmeli"
    
    print(f"  Name: {symbol.name}")
    print(f"  Type: {symbol.type.value}")
    print(f"  Scope: {symbol.scope.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Symbol dataclass")
    print("=" * 70)


def test_symbol_search_result_dataclass():
    """
    Test: SymbolSearchResult dataclass.
    """
    print("=" * 70)
    print("TEST: SymbolSearchResult Dataclass")
    print("=" * 70)
    
    result = SymbolSearchResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.symbols, list), "Symbols list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Symbols: {len(result.symbols)}")
    
    print("\n" + "=" * 70)
    print("PASS: SymbolSearchResult dataclass")
    print("=" * 70)


def test_function_extraction():
    """
    Test: Function extraction.
    """
    print("=" * 70)
    print("TEST: Function Extraction")
    print("=" * 70)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        test_code = """
def my_function(x, y):
    return x + y
"""
        test_file = os.path.join(tmpdir, "test.py")
        with open(test_file, "w") as f:
            f.write(test_code)
        
        engine = SymbolSearchEngine(tmpdir)
        result = engine.build_index(test_file)
        
        functions = [s for s in result.symbols if s.type == SymbolType.FUNCTION]
        
        assert len(functions) > 0, "Function bulunmalı"
        
        print(f"  Functions found: {len(functions)}")
        print(f"  Function names: {[f.name for f in functions]}")
    
    print("\n" + "=" * 70)
    print("PASS: Function extraction")
    print("=" * 70)


def test_class_extraction():
    """
    Test: Class extraction.
    """
    print("=" * 70)
    print("TEST: Class Extraction")
    print("=" * 70)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        test_code = """
class MyClass:
    def my_method(self):
        pass
"""
        test_file = os.path.join(tmpdir, "test.py")
        with open(test_file, "w") as f:
            f.write(test_code)
        
        engine = SymbolSearchEngine(tmpdir)
        result = engine.build_index(test_file)
        
        classes = [s for s in result.symbols if s.type == SymbolType.CLASS]
        
        assert len(classes) > 0, "Class bulunmalı"
        
        print(f"  Classes found: {len(classes)}")
        print(f"  Class names: {[c.name for c in classes]}")
    
    print("\n" + "=" * 70)
    print("PASS: Class extraction")
    print("=" * 70)


def test_import_extraction():
    """
    Test: Import extraction.
    """
    print("=" * 70)
    print("TEST: Import Extraction")
    print("=" * 70)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        test_code = """
import os
import sys
from collections import defaultdict
"""
        test_file = os.path.join(tmpdir, "test.py")
        with open(test_file, "w") as f:
            f.write(test_code)
        
        engine = SymbolSearchEngine(tmpdir)
        result = engine.build_index(test_file)
        
        imports = [s for s in result.symbols if s.type == SymbolType.IMPORT]
        
        assert len(imports) > 0, "Import bulunmalı"
        
        print(f"  Imports found: {len(imports)}")
        print(f"  Import names: {[i.name for i in imports]}")
    
    print("\n" + "=" * 70)
    print("PASS: Import extraction")
    print("=" * 70)


def test_search_mode_enum():
    """
    Test: SearchMode enum.
    """
    print("=" * 70)
    print("TEST: SearchMode Enum")
    print("=" * 70)
    
    assert SearchMode.NORMAL.value == "normal"
    assert SearchMode.CASE_SENSITIVE.value == "case_sensitive"
    assert SearchMode.CASE_INSENSITIVE.value == "case_insensitive"
    assert SearchMode.REGEX.value == "regex"
    assert SearchMode.WHOLE_WORD.value == "whole_word"
    assert SearchMode.FUZZY.value == "fuzzy"
    
    print(f"  All enum values verified")
    print(f"  Total modes: {len(SearchMode)}")
    
    print("\n" + "=" * 70)
    print("PASS: SearchMode enum")
    print("=" * 70)


def test_search_action_enum():
    """
    Test: SearchAction enum.
    """
    print("=" * 70)
    print("TEST: SearchAction Enum")
    print("=" * 70)
    
    assert SearchAction.SEARCH.value == "search"
    assert SearchAction.FIND_DEFINITION.value == "find_definition"
    assert SearchAction.FIND_REFERENCES.value == "find_references"
    assert SearchAction.FILTER.value == "filter"
    assert SearchAction.CLEAR.value == "clear"
    
    print(f"  All enum values verified")
    print(f"  Total actions: {len(SearchAction)}")
    
    print("\n" + "=" * 70)
    print("PASS: SearchAction enum")
    print("=" * 70)


def test_symbol_search_config_dataclass():
    """
    Test: SymbolSearchConfig dataclass.
    """
    print("=" * 70)
    print("TEST: SymbolSearchConfig Dataclass")
    print("=" * 70)
    
    config = SymbolSearchConfig(
        mode=SearchMode.REGEX,
        case_sensitive=True
    )
    
    assert config.mode == SearchMode.REGEX, "Mode eşleşmeli"
    assert config.case_sensitive == True, "Case sensitive eşleşmeli"
    
    print(f"  Mode: {config.mode.value}")
    print(f"  Case sensitive: {config.case_sensitive}")
    print(f"  Include context: {config.include_context}")
    
    print("\n" + "=" * 70)
    print("PASS: SymbolSearchConfig dataclass")
    print("=" * 70)


def test_find_next():
    """
    Test: Find next.
    """
    print("=" * 70)
    print("TEST: Find Next")
    print("=" * 70)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        test_code = """
def my_function():
    pass

def another_function():
    pass
"""
        test_file = os.path.join(tmpdir, "test.py")
        with open(test_file, "w") as f:
            f.write(test_code)
        
        engine = SymbolSearchEngine(tmpdir)
        engine.build_index(test_file)
        engine.search_symbols("")
        
        result = engine.find_next()
        
        assert result.success, "Find next başarılı olmalı"
        
        print(f"  Success: {result.success}")
        print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Find next")
    print("=" * 70)


def test_find_previous():
    """
    Test: Find previous.
    """
    print("=" * 70)
    print("TEST: Find Previous")
    print("=" * 70)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        test_code = """
def my_function():
    pass

def another_function():
    pass
"""
        test_file = os.path.join(tmpdir, "test.py")
        with open(test_file, "w") as f:
            f.write(test_code)
        
        engine = SymbolSearchEngine(tmpdir)
        engine.build_index(test_file)
        engine.search_symbols("")
        
        result = engine.find_previous()
        
        assert result.success, "Find previous başarılı olmalı"
        
        print(f"  Success: {result.success}")
        print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Find previous")
    print("=" * 70)


def test_search_history():
    """
    Test: Search history.
    """
    print("=" * 70)
    print("TEST: Search History")
    print("=" * 70)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        test_code = """
def my_function():
    pass
"""
        test_file = os.path.join(tmpdir, "test.py")
        with open(test_file, "w") as f:
            f.write(test_code)
        
        engine = SymbolSearchEngine(tmpdir)
        engine.build_index(test_file)
        engine.search_symbols("my_function")
        
        history = engine.get_search_history()
        
        assert len(history) > 0, "Geçmiş olmalı"
        
        print(f"  History: {len(history)}")
    
    print("\n" + "=" * 70)
    print("PASS: Search history")
    print("=" * 70)


def test_clear_history():
    """
    Test: Clear history.
    """
    print("=" * 70)
    print("TEST: Clear History")
    print("=" * 70)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        test_code = """
def my_function():
    pass
"""
        test_file = os.path.join(tmpdir, "test.py")
        with open(test_file, "w") as f:
            f.write(test_code)
        
        engine = SymbolSearchEngine(tmpdir)
        engine.build_index(test_file)
        engine.search_symbols("my_function")
        
        result = engine.clear_history()
        
        assert result.success, "Temizleme başarılı olmalı"
        assert len(engine.get_search_history()) == 0, "Geçmiş temizlenmeli"
        
        print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear history")
    print("=" * 70)


def test_get_statistics():
    """
    Test: Get statistics.
    """
    print("=" * 70)
    print("TEST: Get Statistics")
    print("=" * 70)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        test_code = """
def my_function():
    pass
"""
        test_file = os.path.join(tmpdir, "test.py")
        with open(test_file, "w") as f:
            f.write(test_code)
        
        engine = SymbolSearchEngine(tmpdir)
        engine.build_index(test_file)
        engine.search_symbols("my_function")
        
        stats = engine.get_statistics()
        
        assert stats is not None, "İstatistikler olmalı"
        assert "total_symbols" in stats, "Total symbols olmalı"
        
        print(f"  Total symbols: {stats['total_symbols']}")
        print(f"  Current index: {stats['current_index']}")
    
    print("\n" + "=" * 70)
    print("PASS: Get statistics")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        engine = SymbolSearchEngine(tmpdir)
        
        new_config = SymbolSearchConfig(case_sensitive=True)
        result = engine.update_config(new_config)
        
        assert result.success, "Güncelleme başarılı olmalı"
        
        print(f"  Success: {result.success}")
    
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
    
    with tempfile.TemporaryDirectory() as tmpdir:
        engine = SymbolSearchEngine(tmpdir)
        
        config = engine.get_config()
        
        assert config is not None, "Config olmalı"
        assert config.mode == SearchMode.NORMAL, "Mode eşleşmeli"
        
        print(f"  Mode: {config.mode.value}")
        print(f"  Case sensitive: {config.case_sensitive}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_search_symbols()
        test2 = test_search_by_type()
        test3 = test_build_index()
        test4 = test_find_definition()
        test5 = test_find_references()
        test6 = test_symbol_type_enum()
        test7 = test_symbol_scope_enum()
        test8 = test_symbol_dataclass()
        test9 = test_symbol_search_result_dataclass()
        test10 = test_function_extraction()
        test11 = test_class_extraction()
        test12 = test_import_extraction()
        test13 = test_search_mode_enum()
        test14 = test_search_action_enum()
        test15 = test_symbol_search_config_dataclass()
        test16 = test_find_next()
        test17 = test_find_previous()
        test18 = test_search_history()
        test19 = test_clear_history()
        test20 = test_get_statistics()
        test21 = test_update_config()
        test22 = test_get_config()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Search Symbols: {'PASS' if test1 else 'FAIL'}")
        print(f"Search by Type: {'PASS' if test2 else 'FAIL'}")
        print(f"Build Index: {'PASS' if test3 else 'FAIL'}")
        print(f"Find Definition: {'PASS' if test4 else 'FAIL'}")
        print(f"Find References: {'PASS' if test5 else 'FAIL'}")
        print(f"SymbolType Enum: {'PASS' if test6 else 'FAIL'}")
        print(f"SymbolScope Enum: {'PASS' if test7 else 'FAIL'}")
        print(f"Symbol Dataclass: {'PASS' if test8 else 'FAIL'}")
        print(f"SymbolSearchResult Dataclass: {'PASS' if test9 else 'FAIL'}")
        print(f"Function Extraction: {'PASS' if test10 else 'FAIL'}")
        print(f"Class Extraction: {'PASS' if test11 else 'FAIL'}")
        print(f"Import Extraction: {'PASS' if test12 else 'FAIL'}")
        print(f"SearchMode Enum: {'PASS' if test13 else 'FAIL'}")
        print(f"SearchAction Enum: {'PASS' if test14 else 'FAIL'}")
        print(f"SymbolSearchConfig Dataclass: {'PASS' if test15 else 'FAIL'}")
        print(f"Find Next: {'PASS' if test16 else 'FAIL'}")
        print(f"Find Previous: {'PASS' if test17 else 'FAIL'}")
        print(f"Search History: {'PASS' if test18 else 'FAIL'}")
        print(f"Clear History: {'PASS' if test19 else 'FAIL'}")
        print(f"Get Statistics: {'PASS' if test20 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test21 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test22 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14, test15, test16, test17, test18, test19, test20, test21, test22])
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
