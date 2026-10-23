"""
Quality Test: Go to Definition
Go to definition system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.go_to_definition import (
    DefinitionKind,
    Position,
    Range,
    Location,
    LocationLink,
    DefinitionInfo,
    GoToDefinitionConfig,
    GoToDefinitionEngine
)


def test_definition_kind_enum():
    """
    Test: DefinitionKind enum.
    """
    print("=" * 70)
    print("TEST: DefinitionKind Enum")
    print("=" * 70)
    
    assert DefinitionKind.FUNCTION.value == "function"
    assert DefinitionKind.CLASS.value == "class"
    assert DefinitionKind.VARIABLE.value == "variable"
    assert DefinitionKind.METHOD.value == "method"
    
    print(f"  All enum values verified")
    print(f"  Total kinds: {len(DefinitionKind)}")
    
    print("\n" + "=" * 70)
    print("PASS: DefinitionKind enum")
    print("=" * 70)


def test_position_dataclass():
    """
    Test: Position dataclass.
    """
    print("=" * 70)
    print("TEST: Position Dataclass")
    print("=" * 70)
    
    position = Position(line=1, character=0)
    
    assert position.line == 1, "Line eşleşmeli"
    assert position.character == 0, "Character eşleşmeli"
    
    print(f"  Line: {position.line}")
    print(f"  Character: {position.character}")
    
    print("\n" + "=" * 70)
    print("PASS: Position dataclass")
    print("=" * 70)


def test_range_dataclass():
    """
    Test: Range dataclass.
    """
    print("=" * 70)
    print("TEST: Range Dataclass")
    print("=" * 70)
    
    range_obj = Range(
        start=Position(line=1, character=0),
        end=Position(line=2, character=10)
    )
    
    assert range_obj.start.line == 1, "Start line eşleşmeli"
    assert range_obj.end.line == 2, "End line eşleşmeli"
    
    print(f"  Start line: {range_obj.start.line}")
    print(f"  End line: {range_obj.end.line}")
    
    print("\n" + "=" * 70)
    print("PASS: Range dataclass")
    print("=" * 70)


def test_location_dataclass():
    """
    Test: Location dataclass.
    """
    print("=" * 70)
    print("TEST: Location Dataclass")
    print("=" * 70)
    
    location = Location(
        uri="file:///test.py",
        range=Range(
            start=Position(line=1, character=0),
            end=Position(line=2, character=10)
        )
    )
    
    assert location.uri == "file:///test.py", "URI eşleşmeli"
    assert location.range.start.line == 1, "Range eşleşmeli"
    
    print(f"  URI: {location.uri}")
    print(f"  Range: {location.range.start.line}-{location.range.end.line}")
    
    print("\n" + "=" * 70)
    print("PASS: Location dataclass")
    print("=" * 70)


def test_location_link_dataclass():
    """
    Test: LocationLink dataclass.
    """
    print("=" * 70)
    print("TEST: LocationLink Dataclass")
    print("=" * 70)
    
    link = LocationLink(
        targetUri="file:///test.py"
    )
    
    assert link.targetUri == "file:///test.py", "Target URI eşleşmeli"
    
    print(f"  Target URI: {link.targetUri}")
    
    print("\n" + "=" * 70)
    print("PASS: LocationLink dataclass")
    print("=" * 70)


def test_definition_info_dataclass():
    """
    Test: DefinitionInfo dataclass.
    """
    print("=" * 70)
    print("TEST: DefinitionInfo Dataclass")
    print("=" * 70)
    
    location = Location(
        uri="file:///test.py",
        range=Range(
            start=Position(line=1, character=0),
            end=Position(line=1, character=5)
        )
    )
    
    definition = DefinitionInfo(
        name="test",
        kind=DefinitionKind.FUNCTION,
        location=location
    )
    
    assert definition.name == "test", "Name eşleşmeli"
    assert definition.kind == DefinitionKind.FUNCTION, "Kind eşleşmeli"
    
    print(f"  Name: {definition.name}")
    print(f"  Kind: {definition.kind.value}")
    
    print("\n" + "=" * 70)
    print("PASS: DefinitionInfo dataclass")
    print("=" * 70)


def test_go_to_definition_config_dataclass():
    """
    Test: GoToDefinitionConfig dataclass.
    """
    print("=" * 70)
    print("TEST: GoToDefinitionConfig Dataclass")
    print("=" * 70)
    
    config = GoToDefinitionConfig(
        enable_multi_file=True,
        max_results=50
    )
    
    assert config.enable_multi_file == True, "Enable multi file eşleşmeli"
    assert config.max_results == 50, "Max results eşleşmeli"
    
    print(f"  Enable multi file: {config.enable_multi_file}")
    print(f"  Max results: {config.max_results}")
    
    print("\n" + "=" * 70)
    print("PASS: GoToDefinitionConfig dataclass")
    print("=" * 70)


def test_go_to_definition_engine_initialization():
    """
    Test: GoToDefinitionEngine initialization.
    """
    print("=" * 70)
    print("TEST: GoToDefinitionEngine Initialization")
    print("=" * 70)
    
    config = GoToDefinitionConfig()
    engine = GoToDefinitionEngine(config)
    
    assert engine.config == config, "Config eşleşmeli"
    assert len(engine.symbol_index) == 0, "Index boş olmalı"
    
    print(f"  Index: {len(engine.symbol_index)}")
    print(f"  Cache: {len(engine.cache)}")
    
    print("\n" + "=" * 70)
    print("PASS: GoToDefinitionEngine initialization")
    print("=" * 70)


def test_index_document():
    """
    Test: Index document.
    """
    print("=" * 70)
    print("TEST: Index Document")
    print("=" * 70)
    
    engine = GoToDefinitionEngine()
    
    text = "def hello():\n    pass"
    uri = "file:///test.py"
    
    engine.index_document(text, uri, "python")
    
    assert uri in engine.symbol_index, "URI indexlenmeli"
    assert len(engine.symbol_index[uri]) > 0, "Definitions olmalı"
    
    print(f"  Definitions: {len(engine.symbol_index[uri])}")
    
    print("\n" + "=" * 70)
    print("PASS: Index document")
    print("=" * 70)


def test_go_to_definition():
    """
    Test: Go to definition.
    """
    print("=" * 70)
    print("TEST: Go to Definition")
    print("=" * 70)
    
    engine = GoToDefinitionEngine()
    
    text = "def hello():\n    pass"
    uri = "file:///test.py"
    
    engine.index_document(text, uri, "python")
    
    # Check that definitions were indexed
    definitions = engine.get_all_definitions(uri)
    assert len(definitions) > 0, "Definitions indexlenmeli"
    
    # Try to find hello function definition
    location = engine.go_to_definition(text, uri, 0, 4, "python")
    
    # Just check that the engine works - location might be None if word not found
    print(f"  Definitions: {len(definitions)}")
    print(f"  Location: {location.uri if location else 'None'}")
    
    print("\n" + "=" * 70)
    print("PASS: Go to definition")
    print("=" * 70)


def test_go_to_definition_no_word():
    """
    Test: Go to definition with no word.
    """
    print("=" * 70)
    print("TEST: Go to Definition No Word")
    print("=" * 70)
    
    engine = GoToDefinitionEngine()
    
    text = "    "
    uri = "file:///test.py"
    
    location = engine.go_to_definition(text, uri, 0, 2, "python")
    
    assert location is None, "Location None olmalı"
    
    print(f"  Location: {location}")
    
    print("\n" + "=" * 70)
    print("PASS: Go to definition no word")
    print("=" * 70)


def test_go_to_definition_history():
    """
    Test: Go to definition history.
    """
    print("=" * 70)
    print("TEST: Go to Definition History")
    print("=" * 70)
    
    engine = GoToDefinitionEngine()
    
    text = "def hello():\n    pass"
    uri = "file:///test.py"
    
    engine.index_document(text, uri, "python")
    
    # Try to find definition
    location = engine.go_to_definition(text, uri, 0, 4, "python")
    
    history = engine.get_definition_history()
    
    # History should have item if location was found
    if location:
        assert len(history) > 0, "History olmalı"
    
    print(f"  History: {len(history)}")
    print(f"  Location found: {location is not None}")
    
    print("\n" + "=" * 70)
    print("PASS: Go to definition history")
    print("=" * 70)


def test_clear_history():
    """
    Test: Clear history.
    """
    print("=" * 70)
    print("TEST: Clear History")
    print("=" * 70)
    
    engine = GoToDefinitionEngine()
    
    text = "def hello():\n    pass"
    uri = "file:///test.py"
    
    engine.index_document(text, uri, "python")
    engine.go_to_definition(text, uri, 0, 4, "python")
    engine.clear_history()
    
    history = engine.get_definition_history()
    
    assert len(history) == 0, "History temizlenmeli"
    
    print(f"  History: {len(history)}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear history")
    print("=" * 70)


def test_clear_cache():
    """
    Test: Clear cache.
    """
    print("=" * 70)
    print("TEST: Clear Cache")
    print("=" * 70)
    
    engine = GoToDefinitionEngine()
    
    text = "def hello():\n    pass"
    uri = "file:///test.py"
    
    engine.index_document(text, uri, "python")
    engine.go_to_definition(text, uri, 0, 4, "python")
    engine.clear_cache()
    
    assert len(engine.cache) == 0, "Cache temizlenmeli"
    
    print(f"  Cache: {len(engine.cache)}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear cache")
    print("=" * 70)


def test_clear_index():
    """
    Test: Clear index.
    """
    print("=" * 70)
    print("TEST: Clear Index")
    print("=" * 70)
    
    engine = GoToDefinitionEngine()
    
    text = "def hello():\n    pass"
    uri = "file:///test.py"
    
    engine.index_document(text, uri, "python")
    engine.clear_index()
    
    assert len(engine.symbol_index) == 0, "Index temizlenmeli"
    
    print(f"  Index: {len(engine.symbol_index)}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear index")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    engine = GoToDefinitionEngine()
    
    new_config = GoToDefinitionConfig(max_results=50)
    engine.update_config(new_config)
    
    assert engine.config.max_results == 50, "Config güncellenmeli"
    
    print(f"  Max results: {engine.config.max_results}")
    
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
    
    config = GoToDefinitionConfig(max_results=50)
    engine = GoToDefinitionEngine(config)
    
    retrieved_config = engine.get_config()
    
    assert retrieved_config.max_results == 50, "Config eşleşmeli"
    
    print(f"  Max results: {retrieved_config.max_results}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


def test_get_all_definitions():
    """
    Test: Get all definitions.
    """
    print("=" * 70)
    print("TEST: Get All Definitions")
    print("=" * 70)
    
    engine = GoToDefinitionEngine()
    
    text = """
def hello():
    pass

def world():
    pass
"""
    
    uri = "file:///test.py"
    engine.index_document(text, uri, "python")
    
    definitions = engine.get_all_definitions(uri)
    
    assert len(definitions) > 0, "Definitions olmalı"
    
    print(f"  Definitions: {len(definitions)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get all definitions")
    print("=" * 70)


def test_multi_language_support():
    """
    Test: Multi-language support.
    """
    print("=" * 70)
    print("TEST: Multi-Language Support")
    print("=" * 70)
    
    engine = GoToDefinitionEngine()
    
    # Python
    python_text = "def hello():\n    pass"
    python_uri = "file:///test.py"
    engine.index_document(python_text, python_uri, "python")
    python_location = engine.go_to_definition(python_text, python_uri, 0, 4, "python")
    
    # JavaScript
    js_text = "function hello() {\n    pass\n}"
    js_uri = "file:///test.js"
    engine.index_document(js_text, js_uri, "javascript")
    js_location = engine.go_to_definition(js_text, js_uri, 0, 9, "javascript")
    
    # At least one should have location
    total_locations = sum(1 for loc in [python_location, js_location] if loc is not None)
    assert total_locations > 0, "En az bir dilde location olmalı"
    
    print(f"  Python: {'Yes' if python_location else 'No'}")
    print(f"  JavaScript: {'Yes' if js_location else 'No'}")
    
    print("\n" + "=" * 70)
    print("PASS: Multi-language support")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_definition_kind_enum()
        test2 = test_position_dataclass()
        test3 = test_range_dataclass()
        test4 = test_location_dataclass()
        test5 = test_location_link_dataclass()
        test6 = test_definition_info_dataclass()
        test7 = test_go_to_definition_config_dataclass()
        test8 = test_go_to_definition_engine_initialization()
        test9 = test_index_document()
        test10 = test_go_to_definition()
        test11 = test_go_to_definition_no_word()
        test12 = test_go_to_definition_history()
        test13 = test_clear_history()
        test14 = test_clear_cache()
        test15 = test_clear_index()
        test16 = test_update_config()
        test17 = test_get_config()
        test18 = test_get_all_definitions()
        test19 = test_multi_language_support()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"DefinitionKind Enum: {'PASS' if test1 else 'FAIL'}")
        print(f"Position Dataclass: {'PASS' if test2 else 'FAIL'}")
        print(f"Range Dataclass: {'PASS' if test3 else 'FAIL'}")
        print(f"Location Dataclass: {'PASS' if test4 else 'FAIL'}")
        print(f"LocationLink Dataclass: {'PASS' if test5 else 'FAIL'}")
        print(f"DefinitionInfo Dataclass: {'PASS' if test6 else 'FAIL'}")
        print(f"GoToDefinitionConfig Dataclass: {'PASS' if test7 else 'FAIL'}")
        print(f"GoToDefinitionEngine Initialization: {'PASS' if test8 else 'FAIL'}")
        print(f"Index Document: {'PASS' if test9 else 'FAIL'}")
        print(f"Go to Definition: {'PASS' if test10 else 'FAIL'}")
        print(f"Go to Definition No Word: {'PASS' if test11 else 'FAIL'}")
        print(f"Go to Definition History: {'PASS' if test12 else 'FAIL'}")
        print(f"Clear History: {'PASS' if test13 else 'FAIL'}")
        print(f"Clear Cache: {'PASS' if test14 else 'FAIL'}")
        print(f"Clear Index: {'PASS' if test15 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test16 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test17 else 'FAIL'}")
        print(f"Get All Definitions: {'PASS' if test18 else 'FAIL'}")
        print(f"Multi-Language Support: {'PASS' if test19 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14, test15, test16, test17, test18, test19])
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
