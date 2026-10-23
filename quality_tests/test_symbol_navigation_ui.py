"""
Quality Test: Symbol Navigation UI
Symbol navigation UI system testleri.
"""

import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from app.editor.symbol_navigation_ui import (
    SymbolType,
    SymbolScope,
    Symbol,
    SymbolNavigationConfig,
    SymbolNavigationResult,
    SymbolNavigationUIManager
)


def test_symbol_type_enum():
    """
    Test: SymbolType enum.
    """
    print("=" * 70)
    print("TEST: SymbolType Enum")
    print("=" * 70)
    
    assert SymbolType.CLASS.value == "class"
    assert SymbolType.FUNCTION.value == "function"
    assert SymbolType.METHOD.value == "method"
    assert SymbolType.VARIABLE.value == "variable"
    assert SymbolType.CONSTANT.value == "constant"
    assert SymbolType.PROPERTY.value == "property"
    assert SymbolType.INTERFACE.value == "interface"
    assert SymbolType.ENUM.value == "enum"
    assert SymbolType.TYPE_ALIAS.value == "type_alias"
    assert SymbolType.NAMESPACE.value == "namespace"
    assert SymbolType.MODULE.value == "module"
    assert SymbolType.IMPORT.value == "import"
    
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
    
    assert SymbolScope.PUBLIC.value == "public"
    assert SymbolScope.PRIVATE.value == "private"
    assert SymbolScope.PROTECTED.value == "protected"
    assert SymbolScope.INTERNAL.value == "internal"
    assert SymbolScope.FILE.value == "file"
    assert SymbolScope.GLOBAL.value == "global"
    
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
        id="symbol_1",
        name="MyClass",
        type=SymbolType.CLASS,
        scope=SymbolScope.PUBLIC,
        line=1,
        column=0
    )
    
    assert symbol.id == "symbol_1", "ID eşleşmeli"
    assert symbol.name == "MyClass", "Name eşleşmeli"
    assert symbol.type == SymbolType.CLASS, "Type eşleşmeli"
    
    print(f"  ID: {symbol.id}")
    print(f"  Name: {symbol.name}")
    print(f"  Type: {symbol.type.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Symbol dataclass")
    print("=" * 70)


def test_symbol_navigation_config_dataclass():
    """
    Test: SymbolNavigationConfig dataclass.
    """
    print("=" * 70)
    print("TEST: SymbolNavigationConfig Dataclass")
    print("=" * 70)
    
    config = SymbolNavigationConfig(
        show_private_symbols=False,
        show_line_numbers=True
    )
    
    assert config.show_private_symbols == False, "Show private symbols eşleşmeli"
    assert config.show_line_numbers == True, "Show line numbers eşleşmeli"
    
    print(f"  Show private symbols: {config.show_private_symbols}")
    print(f"  Show line numbers: {config.show_line_numbers}")
    
    print("\n" + "=" * 70)
    print("PASS: SymbolNavigationConfig dataclass")
    print("=" * 70)


def test_symbol_navigation_result_dataclass():
    """
    Test: SymbolNavigationResult dataclass.
    """
    print("=" * 70)
    print("TEST: SymbolNavigationResult Dataclass")
    print("=" * 70)
    
    result = SymbolNavigationResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.symbols, list), "Symbols list olmalı"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Symbols: {len(result.symbols)}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: SymbolNavigationResult dataclass")
    print("=" * 70)


def test_symbol_navigation_ui_manager_initialization():
    """
    Test: SymbolNavigationUIManager initialization.
    """
    print("=" * 70)
    print("TEST: SymbolNavigationUIManager Initialization")
    print("=" * 70)
    
    config = SymbolNavigationConfig()
    manager = SymbolNavigationUIManager(config)
    
    assert manager.config == config, "Config eşleşmeli"
    assert len(manager.symbols) == 0, "Symbols boş olmalı"
    
    print(f"  Symbols: {len(manager.symbols)}")
    
    print("\n" + "=" * 70)
    print("PASS: SymbolNavigationUIManager initialization")
    print("=" * 70)


def test_register_symbol():
    """
    Test: Register symbol.
    """
    print("=" * 70)
    print("TEST: Register Symbol")
    print("=" * 70)
    
    manager = SymbolNavigationUIManager()
    
    symbol = Symbol(
        id="symbol_1",
        name="MyClass",
        type=SymbolType.CLASS,
        line=1
    )
    
    result = manager.register_symbol(symbol)
    
    assert result.success == True, "Registration başarılı olmalı"
    assert "symbol_1" in manager.symbols, "Symbol kaydedilmeli"
    
    print(f"  Symbol registered: {symbol.name}")
    
    print("\n" + "=" * 70)
    print("PASS: Register symbol")
    print("=" * 70)


def test_unregister_symbol():
    """
    Test: Unregister symbol.
    """
    print("=" * 70)
    print("TEST: Unregister Symbol")
    print("=" * 70)
    
    manager = SymbolNavigationUIManager()
    
    symbol = Symbol(
        id="symbol_1",
        name="MyClass",
        type=SymbolType.CLASS
    )
    
    manager.register_symbol(symbol)
    result = manager.unregister_symbol("symbol_1")
    
    assert result.success == True, "Unregistration başarılı olmalı"
    assert "symbol_1" not in manager.symbols, "Symbol silinmeli"
    
    print(f"  Symbol unregistered: {symbol.name}")
    
    print("\n" + "=" * 70)
    print("PASS: Unregister symbol")
    print("=" * 70)


def test_get_symbol():
    """
    Test: Get symbol.
    """
    print("=" * 70)
    print("TEST: Get Symbol")
    print("=" * 70)
    
    manager = SymbolNavigationUIManager()
    
    symbol = Symbol(
        id="symbol_1",
        name="MyClass",
        type=SymbolType.CLASS
    )
    
    manager.register_symbol(symbol)
    retrieved_symbol = manager.get_symbol("symbol_1")
    
    assert retrieved_symbol is not None, "Symbol bulunmalı"
    assert retrieved_symbol.id == "symbol_1", "ID eşleşmeli"
    
    print(f"  Symbol: {retrieved_symbol.name}")
    
    print("\n" + "=" * 70)
    print("PASS: Get symbol")
    print("=" * 70)


def test_get_all_symbols():
    """
    Test: Get all symbols.
    """
    print("=" * 70)
    print("TEST: Get All Symbols")
    print("=" * 70)
    
    manager = SymbolNavigationUIManager()
    
    symbol = Symbol(
        id="symbol_1",
        name="MyClass",
        type=SymbolType.CLASS
    )
    
    manager.register_symbol(symbol)
    symbols = manager.get_all_symbols()
    
    assert len(symbols) > 0, "Symbols olmalı"
    
    print(f"  Total symbols: {len(symbols)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get all symbols")
    print("=" * 70)


def test_get_symbols_by_type():
    """
    Test: Get symbols by type.
    """
    print("=" * 70)
    print("TEST: Get Symbols by Type")
    print("=" * 70)
    
    manager = SymbolNavigationUIManager()
    
    symbol = Symbol(
        id="symbol_1",
        name="MyClass",
        type=SymbolType.CLASS
    )
    
    manager.register_symbol(symbol)
    symbols = manager.get_symbols_by_type(SymbolType.CLASS)
    
    assert len(symbols) > 0, "Class symbols olmalı"
    
    print(f"  Class symbols: {len(symbols)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get symbols by type")
    print("=" * 70)


def test_get_symbols_by_scope():
    """
    Test: Get symbols by scope.
    """
    print("=" * 70)
    print("TEST: Get Symbols by Scope")
    print("=" * 70)
    
    manager = SymbolNavigationUIManager()
    
    symbol = Symbol(
        id="symbol_1",
        name="MyClass",
        type=SymbolType.CLASS,
        scope=SymbolScope.PUBLIC
    )
    
    manager.register_symbol(symbol)
    symbols = manager.get_symbols_by_scope(SymbolScope.PUBLIC)
    
    assert len(symbols) > 0, "Public symbols olmalı"
    
    print(f"  Public symbols: {len(symbols)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get symbols by scope")
    print("=" * 70)


def test_get_symbols_by_parent():
    """
    Test: Get symbols by parent.
    """
    print("=" * 70)
    print("TEST: Get Symbols by Parent")
    print("=" * 70)
    
    manager = SymbolNavigationUIManager()
    
    parent = Symbol(
        id="parent_1",
        name="ParentClass",
        type=SymbolType.CLASS
    )
    
    child = Symbol(
        id="child_1",
        name="ChildMethod",
        type=SymbolType.METHOD,
        parent="parent_1"
    )
    
    manager.register_symbol(parent)
    manager.register_symbol(child)
    
    symbols = manager.get_symbols_by_parent("parent_1")
    
    assert len(symbols) > 0, "Child symbols olmalı"
    
    print(f"  Child symbols: {len(symbols)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get symbols by parent")
    print("=" * 70)


def test_search_symbols():
    """
    Test: Search symbols.
    """
    print("=" * 70)
    print("TEST: Search Symbols")
    print("=" * 70)
    
    manager = SymbolNavigationUIManager()
    
    symbol = Symbol(
        id="symbol_1",
        name="MyClass",
        type=SymbolType.CLASS
    )
    
    manager.register_symbol(symbol)
    result = manager.search_symbols("My")
    
    assert result.success == True, "Search başarılı olmalı"
    assert len(result.symbols) > 0, "Symbols bulunmalı"
    
    print(f"  Found: {len(result.symbols)} symbols")
    
    print("\n" + "=" * 70)
    print("PASS: Search symbols")
    print("=" * 70)


def test_navigate_to_symbol():
    """
    Test: Navigate to symbol.
    """
    print("=" * 70)
    print("TEST: Navigate to Symbol")
    print("=" * 70)
    
    manager = SymbolNavigationUIManager()
    
    symbol = Symbol(
        id="symbol_1",
        name="MyClass",
        type=SymbolType.CLASS
    )
    
    manager.register_symbol(symbol)
    result = manager.navigate_to_symbol("symbol_1")
    
    assert result.success == True, "Navigation başarılı olmalı"
    assert result.selected_symbol is not None, "Selected symbol olmalı"
    
    print(f"  Navigated: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Navigate to symbol")
    print("=" * 70)


def test_get_symbol_hierarchy():
    """
    Test: Get symbol hierarchy.
    """
    print("=" * 70)
    print("TEST: Get Symbol Hierarchy")
    print("=" * 70)
    
    manager = SymbolNavigationUIManager()
    
    parent = Symbol(
        id="parent_1",
        name="ParentClass",
        type=SymbolType.CLASS
    )
    
    child = Symbol(
        id="child_1",
        name="ChildMethod",
        type=SymbolType.METHOD,
        parent="parent_1"
    )
    
    manager.register_symbol(parent)
    manager.register_symbol(child)
    
    hierarchy = manager.get_symbol_hierarchy("child_1")
    
    assert len(hierarchy) > 0, "Hierarchy olmalı"
    
    print(f"  Hierarchy: {len(hierarchy)} levels")
    
    print("\n" + "=" * 70)
    print("PASS: Get symbol hierarchy")
    print("=" * 70)


def test_get_symbol_children():
    """
    Test: Get symbol children.
    """
    print("=" * 70)
    print("TEST: Get Symbol Children")
    print("=" * 70)
    
    manager = SymbolNavigationUIManager()
    
    parent = Symbol(
        id="parent_1",
        name="ParentClass",
        type=SymbolType.CLASS
    )
    
    child = Symbol(
        id="child_1",
        name="ChildMethod",
        type=SymbolType.METHOD,
        parent="parent_1"
    )
    
    manager.register_symbol(parent)
    manager.register_symbol(child)
    
    children = manager.get_symbol_children("parent_1")
    
    assert len(children) > 0, "Children olmalı"
    
    print(f"  Children: {len(children)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get symbol children")
    print("=" * 70)


def test_filter_symbols_by_scope():
    """
    Test: Filter symbols by scope.
    """
    print("=" * 70)
    print("TEST: Filter Symbols by Scope")
    print("=" * 70)
    
    manager = SymbolNavigationUIManager()
    
    public_symbol = Symbol(
        id="public_1",
        name="PublicMethod",
        type=SymbolType.METHOD,
        scope=SymbolScope.PUBLIC
    )
    
    private_symbol = Symbol(
        id="private_1",
        name="PrivateMethod",
        type=SymbolType.METHOD,
        scope=SymbolScope.PRIVATE
    )
    
    manager.register_symbol(public_symbol)
    manager.register_symbol(private_symbol)
    
    symbols = manager.get_all_symbols()
    filtered = manager.filter_symbols_by_scope(symbols)
    
    assert len(filtered) > 0, "Filtered symbols olmalı"
    
    print(f"  Filtered: {len(filtered)} symbols")
    
    print("\n" + "=" * 70)
    print("PASS: Filter symbols by scope")
    print("=" * 70)


def test_get_search_history():
    """
    Test: Get search history.
    """
    print("=" * 70)
    print("TEST: Get Search History")
    print("=" * 70)
    
    manager = SymbolNavigationUIManager()
    
    manager.search_symbols("MyClass")
    
    history = manager.get_search_history()
    
    assert len(history) > 0, "History olmalı"
    
    print(f"  History: {len(history)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get search history")
    print("=" * 70)


def test_clear_history():
    """
    Test: Clear history.
    """
    print("=" * 70)
    print("TEST: Clear History")
    print("=" * 70)
    
    manager = SymbolNavigationUIManager()
    
    manager.search_symbols("MyClass")
    manager.clear_history()
    
    history = manager.get_search_history()
    
    assert len(history) == 0, "History temizlenmeli"
    
    print(f"  History cleared")
    
    print("\n" + "=" * 70)
    print("PASS: Clear history")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    manager = SymbolNavigationUIManager()
    
    new_config = SymbolNavigationConfig(max_symbols=500)
    result = manager.update_config(new_config)
    
    assert result.success == True, "Update başarılı olmalı"
    assert manager.config.max_symbols == 500, "Config güncellenmeli"
    
    print(f"  Max symbols: {manager.config.max_symbols}")
    
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
    
    config = SymbolNavigationConfig(max_symbols=500)
    manager = SymbolNavigationUIManager(config)
    
    retrieved_config = manager.get_config()
    
    assert retrieved_config.max_symbols == 500, "Config eşleşmeli"
    
    print(f"  Max symbols: {retrieved_config.max_symbols}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_symbol_type_enum()
        test2 = test_symbol_scope_enum()
        test3 = test_symbol_dataclass()
        test4 = test_symbol_navigation_config_dataclass()
        test5 = test_symbol_navigation_result_dataclass()
        test6 = test_symbol_navigation_ui_manager_initialization()
        test7 = test_register_symbol()
        test8 = test_unregister_symbol()
        test9 = test_get_symbol()
        test10 = test_get_all_symbols()
        test11 = test_get_symbols_by_type()
        test12 = test_get_symbols_by_scope()
        test13 = test_get_symbols_by_parent()
        test14 = test_search_symbols()
        test15 = test_navigate_to_symbol()
        test16 = test_get_symbol_hierarchy()
        test17 = test_get_symbol_children()
        test18 = test_filter_symbols_by_scope()
        test19 = test_get_search_history()
        test20 = test_clear_history()
        test21 = test_update_config()
        test22 = test_get_config()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"SymbolType Enum: {'PASS' if test1 else 'FAIL'}")
        print(f"SymbolScope Enum: {'PASS' if test2 else 'FAIL'}")
        print(f"Symbol Dataclass: {'PASS' if test3 else 'FAIL'}")
        print(f"SymbolNavigationConfig Dataclass: {'PASS' if test4 else 'FAIL'}")
        print(f"SymbolNavigationResult Dataclass: {'PASS' if test5 else 'FAIL'}")
        print(f"SymbolNavigationUIManager Initialization: {'PASS' if test6 else 'FAIL'}")
        print(f"Register Symbol: {'PASS' if test7 else 'FAIL'}")
        print(f"Unregister Symbol: {'PASS' if test8 else 'FAIL'}")
        print(f"Get Symbol: {'PASS' if test9 else 'FAIL'}")
        print(f"Get All Symbols: {'PASS' if test10 else 'FAIL'}")
        print(f"Get Symbols by Type: {'PASS' if test11 else 'FAIL'}")
        print(f"Get Symbols by Scope: {'PASS' if test12 else 'FAIL'}")
        print(f"Get Symbols by Parent: {'PASS' if test13 else 'FAIL'}")
        print(f"Search Symbols: {'PASS' if test14 else 'FAIL'}")
        print(f"Navigate to Symbol: {'PASS' if test15 else 'FAIL'}")
        print(f"Get Symbol Hierarchy: {'PASS' if test16 else 'FAIL'}")
        print(f"Get Symbol Children: {'PASS' if test17 else 'FAIL'}")
        print(f"Filter Symbols by Scope: {'PASS' if test18 else 'FAIL'}")
        print(f"Get Search History: {'PASS' if test19 else 'FAIL'}")
        print(f"Clear History: {'PASS' if test20 else 'FAIL'}")
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
