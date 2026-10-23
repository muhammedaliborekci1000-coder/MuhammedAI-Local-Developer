"""
Quality Test: References
References system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.references import (
    ReferenceKind,
    Position,
    Range,
    Location,
    Reference,
    ReferenceConfig,
    ReferencesEngine
)


def test_reference_kind_enum():
    """
    Test: ReferenceKind enum.
    """
    print("=" * 70)
    print("TEST: ReferenceKind Enum")
    print("=" * 70)
    
    assert ReferenceKind.READ.value == "read"
    assert ReferenceKind.WRITE.value == "write"
    assert ReferenceKind.DEFINITION.value == "definition"
    
    print(f"  All enum values verified")
    print(f"  Total kinds: {len(ReferenceKind)}")
    
    print("\n" + "=" * 70)
    print("PASS: ReferenceKind enum")
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


def test_reference_dataclass():
    """
    Test: Reference dataclass.
    """
    print("=" * 70)
    print("TEST: Reference Dataclass")
    print("=" * 70)
    
    location = Location(
        uri="file:///test.py",
        range=Range(
            start=Position(line=1, character=0),
            end=Position(line=1, character=5)
        )
    )
    
    reference = Reference(
        location=location,
        kind=ReferenceKind.READ,
        name="test"
    )
    
    assert reference.name == "test", "Name eşleşmeli"
    assert reference.kind == ReferenceKind.READ, "Kind eşleşmeli"
    
    print(f"  Name: {reference.name}")
    print(f"  Kind: {reference.kind.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Reference dataclass")
    print("=" * 70)


def test_reference_config_dataclass():
    """
    Test: ReferenceConfig dataclass.
    """
    print("=" * 70)
    print("TEST: ReferenceConfig Dataclass")
    print("=" * 70)
    
    config = ReferenceConfig(
        include_definition=True,
        include_reads=True,
        max_results=50
    )
    
    assert config.include_definition == True, "Include definition eşleşmeli"
    assert config.max_results == 50, "Max results eşleşmeli"
    
    print(f"  Include definition: {config.include_definition}")
    print(f"  Max results: {config.max_results}")
    
    print("\n" + "=" * 70)
    print("PASS: ReferenceConfig dataclass")
    print("=" * 70)


def test_references_engine_initialization():
    """
    Test: ReferencesEngine initialization.
    """
    print("=" * 70)
    print("TEST: ReferencesEngine Initialization")
    print("=" * 70)
    
    config = ReferenceConfig()
    engine = ReferencesEngine(config)
    
    assert engine.config == config, "Config eşleşmeli"
    assert len(engine.symbol_index) == 0, "Index boş olmalı"
    
    print(f"  Index: {len(engine.symbol_index)}")
    print(f"  Cache: {len(engine.cache)}")
    
    print("\n" + "=" * 70)
    print("PASS: ReferencesEngine initialization")
    print("=" * 70)


def test_index_document():
    """
    Test: Index document.
    """
    print("=" * 70)
    print("TEST: Index Document")
    print("=" * 70)
    
    engine = ReferencesEngine()
    
    text = "def hello():\n    pass"
    uri = "file:///test.py"
    
    engine.index_document(text, uri, "python")
    
    assert uri in engine.symbol_index, "URI indexlenmeli"
    assert len(engine.symbol_index[uri]) > 0, "References olmalı"
    
    print(f"  References: {len(engine.symbol_index[uri])}")
    
    print("\n" + "=" * 70)
    print("PASS: Index document")
    print("=" * 70)


def test_find_references():
    """
    Test: Find references.
    """
    print("=" * 70)
    print("TEST: Find References")
    print("=" * 70)
    
    engine = ReferencesEngine()
    
    text = "def hello():\n    pass\nhello()"
    uri = "file:///test.py"
    
    engine.index_document(text, uri, "python")
    
    references = engine.find_references(text, uri, 0, 4, "python")
    
    assert references is not None, "References olmalı"
    assert isinstance(references, list), "List olmalı"
    
    print(f"  References: {len(references)}")
    
    print("\n" + "=" * 70)
    print("PASS: Find references")
    print("=" * 70)


def test_find_references_no_word():
    """
    Test: Find references with no word.
    """
    print("=" * 70)
    print("TEST: Find References No Word")
    print("=" * 70)
    
    engine = ReferencesEngine()
    
    text = "    "
    uri = "file:///test.py"
    
    references = engine.find_references(text, uri, 0, 2, "python")
    
    assert len(references) == 0, "References boş olmalı"
    
    print(f"  References: {len(references)}")
    
    print("\n" + "=" * 70)
    print("PASS: Find references no word")
    print("=" * 70)


def test_clear_cache():
    """
    Test: Clear cache.
    """
    print("=" * 70)
    print("TEST: Clear Cache")
    print("=" * 70)
    
    engine = ReferencesEngine()
    
    text = "def hello():\n    pass"
    uri = "file:///test.py"
    
    engine.index_document(text, uri, "python")
    engine.find_references(text, uri, 0, 4, "python")
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
    
    engine = ReferencesEngine()
    
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
    
    engine = ReferencesEngine()
    
    new_config = ReferenceConfig(max_results=50)
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
    
    config = ReferenceConfig(max_results=50)
    engine = ReferencesEngine(config)
    
    retrieved_config = engine.get_config()
    
    assert retrieved_config.max_results == 50, "Config eşleşmeli"
    
    print(f"  Max results: {retrieved_config.max_results}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


def test_multi_language_support():
    """
    Test: Multi-language support.
    """
    print("=" * 70)
    print("TEST: Multi-Language Support")
    print("=" * 70)
    
    engine = ReferencesEngine()
    
    # Python
    python_text = "def hello():\n    pass"
    python_uri = "file:///test.py"
    engine.index_document(python_text, python_uri, "python")
    python_refs = engine.find_references(python_text, python_uri, 0, 4, "python")
    
    # JavaScript
    js_text = "function hello() {\n    pass\n}"
    js_uri = "file:///test.js"
    engine.index_document(js_text, js_uri, "javascript")
    js_refs = engine.find_references(js_text, js_uri, 0, 9, "javascript")
    
    # At least one should have references
    total_refs = sum(1 for refs in [python_refs, js_refs] if len(refs) > 0)
    assert total_refs > 0, "En az bir dilde references olmalı"
    
    print(f"  Python: {len(python_refs)}")
    print(f"  JavaScript: {len(js_refs)}")
    
    print("\n" + "=" * 70)
    print("PASS: Multi-language support")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_reference_kind_enum()
        test2 = test_position_dataclass()
        test3 = test_range_dataclass()
        test4 = test_location_dataclass()
        test5 = test_reference_dataclass()
        test6 = test_reference_config_dataclass()
        test7 = test_references_engine_initialization()
        test8 = test_index_document()
        test9 = test_find_references()
        test10 = test_find_references_no_word()
        test11 = test_clear_cache()
        test12 = test_clear_index()
        test13 = test_update_config()
        test14 = test_get_config()
        test15 = test_multi_language_support()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"ReferenceKind Enum: {'PASS' if test1 else 'FAIL'}")
        print(f"Position Dataclass: {'PASS' if test2 else 'FAIL'}")
        print(f"Range Dataclass: {'PASS' if test3 else 'FAIL'}")
        print(f"Location Dataclass: {'PASS' if test4 else 'FAIL'}")
        print(f"Reference Dataclass: {'PASS' if test5 else 'FAIL'}")
        print(f"ReferenceConfig Dataclass: {'PASS' if test6 else 'FAIL'}")
        print(f"ReferencesEngine Initialization: {'PASS' if test7 else 'FAIL'}")
        print(f"Index Document: {'PASS' if test8 else 'FAIL'}")
        print(f"Find References: {'PASS' if test9 else 'FAIL'}")
        print(f"Find References No Word: {'PASS' if test10 else 'FAIL'}")
        print(f"Clear Cache: {'PASS' if test11 else 'FAIL'}")
        print(f"Clear Index: {'PASS' if test12 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test13 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test14 else 'FAIL'}")
        print(f"Multi-Language Support: {'PASS' if test15 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14, test15])
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
