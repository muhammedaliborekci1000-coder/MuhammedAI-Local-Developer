"""
Quality Test: Snippets
Snippets system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.snippets import (
    SnippetsEngine,
    SnippetScope,
    SnippetVariable,
    SnippetPlaceholder,
    Snippet,
    SnippetInsertion,
    SnippetSearchResult
)


def test_insert_snippet():
    """
    Test: Insert snippet.
    """
    print("=" * 70)
    print("TEST: Insert Snippet")
    print("=" * 70)
    
    engine = SnippetsEngine()
    result = engine.insert_snippet("def", language="python")
    
    assert result.success, "Insert snippet başarılı olmalı"
    assert result.inserted_code is not None, "Inserted code olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Inserted code:\n{result.inserted_code}")
    
    print("\n" + "=" * 70)
    print("PASS: Insert snippet")
    print("=" * 70)


def test_search_snippets():
    """
    Test: Search snippets.
    """
    print("=" * 70)
    print("TEST: Search Snippets")
    print("=" * 70)
    
    engine = SnippetsEngine()
    result = engine.search_snippets("def", language="python")
    
    assert result.total_count > 0, "Snippet bulunmalı"
    
    print(f"  Total count: {result.total_count}")
    print(f"  Query: {result.query}")
    
    for snippet in result.snippets:
        print(f"  - {snippet.prefix}: {snippet.description}")
    
    print("\n" + "=" * 70)
    print("PASS: Search snippets")
    print("=" * 70)


def test_add_snippet():
    """
    Test: Add snippet.
    """
    print("=" * 70)
    print("TEST: Add Snippet")
    print("=" * 70)
    
    engine = SnippetsEngine()
    
    snippet = Snippet(
        name="custom",
        prefix="custom",
        description="Custom snippet",
        body="print('hello world')",
        scope=SnippetScope.USER,
        language="python"
    )
    
    success = engine.add_snippet(snippet)
    
    assert success, "Snippet eklenmeli"
    
    # Verify
    found = engine.get_snippet("custom", language="python")
    assert found is not None, "Snippet bulunmalı"
    
    print(f"  Success: {success}")
    print(f"  Snippet added: {found.name}")
    
    print("\n" + "=" * 70)
    print("PASS: Add snippet")
    print("=" * 70)


def test_remove_snippet():
    """
    Test: Remove snippet.
    """
    print("=" * 70)
    print("TEST: Remove Snippet")
    print("=" * 70)
    
    engine = SnippetsEngine()
    
    # Add custom snippet
    snippet = Snippet(
        name="temp",
        prefix="temp",
        description="Temp snippet",
        body="temp code",
        scope=SnippetScope.USER,
        language="python"
    )
    engine.add_snippet(snippet)
    
    # Remove
    success = engine.remove_snippet("temp", language="python")
    
    assert success, "Snippet kaldırılmalı"
    
    # Verify
    found = engine.get_snippet("temp", language="python")
    assert found is None, "Snippet bulunmamalı"
    
    print(f"  Success: {success}")
    
    print("\n" + "=" * 70)
    print("PASS: Remove snippet")
    print("=" * 70)


def test_get_snippets():
    """
    Test: Get snippets.
    """
    print("=" * 70)
    print("TEST: Get Snippets")
    print("=" * 70)
    
    engine = SnippetsEngine()
    snippets = engine.get_snippets(language="python")
    
    assert len(snippets) > 0, "Snippet'lar olmalı"
    
    print(f"  Total snippets: {len(snippets)}")
    
    for snippet in snippets[:5]:  # Show first 5
        print(f"  - {snippet.prefix}: {snippet.description}")
    
    print("\n" + "=" * 70)
    print("PASS: Get snippets")
    print("=" * 70)


def test_get_snippet():
    """
    Test: Get snippet.
    """
    print("=" * 70)
    print("TEST: Get Snippet")
    print("=" * 70)
    
    engine = SnippetsEngine()
    snippet = engine.get_snippet("def", language="python")
    
    assert snippet is not None, "Snippet bulunmalı"
    assert snippet.name == "def", "Snippet name eşleşmeli"
    
    print(f"  Name: {snippet.name}")
    print(f"  Prefix: {snippet.prefix}")
    print(f"  Description: {snippet.description}")
    
    print("\n" + "=" * 70)
    print("PASS: Get snippet")
    print("=" * 70)


def test_preview_snippet():
    """
    Test: Preview snippet.
    """
    print("=" * 70)
    print("TEST: Preview Snippet")
    print("=" * 70)
    
    engine = SnippetsEngine()
    preview = engine.preview_snippet("def", language="python")
    
    assert preview is not None, "Preview olmalı"
    
    print(f"  Preview:\n{preview}")
    
    print("\n" + "=" * 70)
    print("PASS: Preview snippet")
    print("=" * 70)


def test_validate_snippet():
    """
    Test: Validate snippet.
    """
    print("=" * 70)
    print("TEST: Validate Snippet")
    print("=" * 70)
    
    engine = SnippetsEngine()
    
    # Valid snippet
    valid_snippet = Snippet(
        name="test",
        prefix="test",
        description="Test snippet",
        body="test code",
        scope=SnippetScope.USER,
        language="python"
    )
    
    is_valid, errors = engine.validate_snippet(valid_snippet)
    assert is_valid, "Snippet geçerli olmalı"
    
    # Invalid snippet (no name)
    invalid_snippet = Snippet(
        name="",
        prefix="test",
        description="Test snippet",
        body="test code",
        scope=SnippetScope.USER,
        language="python"
    )
    
    is_valid, errors = engine.validate_snippet(invalid_snippet)
    assert not is_valid, "Snippet geçersiz olmalı"
    assert len(errors) > 0, "Hatalar olmalı"
    
    print(f"  Valid snippet: {is_valid}")
    print(f"  Invalid snippet errors: {errors}")
    
    print("\n" + "=" * 70)
    print("PASS: Validate snippet")
    print("=" * 70)


def test_get_supported_languages():
    """
    Test: Get supported languages.
    """
    print("=" * 70)
    print("TEST: Get Supported Languages")
    print("=" * 70)
    
    engine = SnippetsEngine()
    languages = engine.get_supported_languages()
    
    assert len(languages) > 0, "Diller olmalı"
    assert "python" in languages, "Python olmalı"
    assert "javascript" in languages, "JavaScript olmalı"
    
    print(f"  Supported languages: {languages}")
    
    print("\n" + "=" * 70)
    print("PASS: Get supported languages")
    print("=" * 70)


def test_get_builtin_snippets():
    """
    Test: Get builtin snippets.
    """
    print("=" * 70)
    print("TEST: Get Builtin Snippets")
    print("=" * 70)
    
    engine = SnippetsEngine()
    builtin = engine.get_builtin_snippets(language="python")
    
    assert len(builtin) > 0, "Builtin snippet'lar olmalı"
    
    print(f"  Builtin snippets: {len(builtin)}")
    
    for snippet in builtin[:5]:
        print(f"  - {snippet.prefix}: {snippet.description}")
    
    print("\n" + "=" * 70)
    print("PASS: Get builtin snippets")
    print("=" * 70)


def test_snippet_scope_enum():
    """
    Test: SnippetScope enum.
    """
    print("=" * 70)
    print("TEST: SnippetScope Enum")
    print("=" * 70)
    
    assert SnippetScope.GLOBAL.value == "global"
    assert SnippetScope.LANGUAGE.value == "language"
    assert SnippetScope.PROJECT.value == "project"
    assert SnippetScope.USER.value == "user"
    
    print(f"  All enum values verified")
    print(f"  Total scopes: {len(SnippetScope)}")
    
    print("\n" + "=" * 70)
    print("PASS: SnippetScope enum")
    print("=" * 70)


def test_snippet_variable_enum():
    """
    Test: SnippetVariable enum.
    """
    print("=" * 70)
    print("TEST: SnippetVariable Enum")
    print("=" * 70)
    
    assert SnippetVariable.TM_FILENAME.value == "TM_FILENAME"
    assert SnippetVariable.TM_DIRECTORY.value == "TM_DIRECTORY"
    assert SnippetVariable.CURRENT_YEAR.value == "CURRENT_YEAR"
    
    print(f"  All enum values verified")
    print(f"  Total variables: {len(SnippetVariable)}")
    
    print("\n" + "=" * 70)
    print("PASS: SnippetVariable enum")
    print("=" * 70)


def test_snippet_placeholder_dataclass():
    """
    Test: SnippetPlaceholder dataclass.
    """
    print("=" * 70)
    print("TEST: SnippetPlaceholder Dataclass")
    print("=" * 70)
    
    placeholder = SnippetPlaceholder(
        index=1,
        name="name",
        default_value="value",
        is_tab_stop=True
    )
    
    assert placeholder.index == 1, "Index eşleşmeli"
    assert placeholder.is_tab_stop == True, "Tab stop eşleşmeli"
    
    print(f"  Index: {placeholder.index}")
    print(f"  Name: {placeholder.name}")
    print(f"  Default value: {placeholder.default_value}")
    
    print("\n" + "=" * 70)
    print("PASS: SnippetPlaceholder dataclass")
    print("=" * 70)


def test_snippet_dataclass():
    """
    Test: Snippet dataclass.
    """
    print("=" * 70)
    print("TEST: Snippet Dataclass")
    print("=" * 70)
    
    snippet = Snippet(
        name="test",
        prefix="test",
        description="Test snippet",
        body="test code",
        scope=SnippetScope.USER,
        language="python"
    )
    
    assert snippet.name == "test", "Name eşleşmeli"
    assert snippet.prefix == "test", "Prefix eşleşmeli"
    assert snippet.scope == SnippetScope.USER, "Scope eşleşmeli"
    
    print(f"  Name: {snippet.name}")
    print(f"  Prefix: {snippet.prefix}")
    print(f"  Scope: {snippet.scope.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Snippet dataclass")
    print("=" * 70)


def test_snippet_insertion_dataclass():
    """
    Test: SnippetInsertion dataclass.
    """
    print("=" * 70)
    print("TEST: SnippetInsertion Dataclass")
    print("=" * 70)
    
    insertion = SnippetInsertion(success=True)
    insertion.message = "Test message"
    
    assert insertion.success == True, "Success eşleşmeli"
    assert insertion.message == "Test message", "Message eşleşmeli"
    assert isinstance(insertion.placeholders, list), "Placeholders list olmalı"
    
    print(f"  Success: {insertion.success}")
    print(f"  Message: {insertion.message}")
    print(f"  Placeholders: {len(insertion.placeholders)}")
    
    print("\n" + "=" * 70)
    print("PASS: SnippetInsertion dataclass")
    print("=" * 70)


def test_snippet_search_result_dataclass():
    """
    Test: SnippetSearchResult dataclass.
    """
    print("=" * 70)
    print("TEST: SnippetSearchResult Dataclass")
    print("=" * 70)
    
    result = SnippetSearchResult(query="test")
    result.total_count = 5
    
    assert result.query == "test", "Query eşleşmeli"
    assert result.total_count == 5, "Total count eşleşmeli"
    assert isinstance(result.snippets, list), "Snippets list olmalı"
    
    print(f"  Query: {result.query}")
    print(f"  Total count: {result.total_count}")
    print(f"  Snippets: {len(result.snippets)}")
    
    print("\n" + "=" * 70)
    print("PASS: SnippetSearchResult dataclass")
    print("=" * 70)


def test_multiple_languages():
    """
    Test: Multiple languages.
    """
    print("=" * 70)
    print("TEST: Multiple Languages")
    print("=" * 70)
    
    engine = SnippetsEngine()
    
    # Python
    python_snippets = engine.get_snippets(language="python")
    assert len(python_snippets) > 0, "Python snippet'lar olmalı"
    
    # JavaScript
    js_snippets = engine.get_snippets(language="javascript")
    assert len(js_snippets) > 0, "JavaScript snippet'lar olmalı"
    
    # HTML
    html_snippets = engine.get_snippets(language="html")
    assert len(html_snippets) > 0, "HTML snippet'lar olmalı"
    
    # CSS
    css_snippets = engine.get_snippets(language="css")
    assert len(css_snippets) > 0, "CSS snippet'lar olmalı"
    
    print(f"  Python: {len(python_snippets)} snippets")
    print(f"  JavaScript: {len(js_snippets)} snippets")
    print(f"  HTML: {len(html_snippets)} snippets")
    print(f"  CSS: {len(css_snippets)} snippets")
    
    print("\n" + "=" * 70)
    print("PASS: Multiple languages")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_insert_snippet()
        test2 = test_search_snippets()
        test3 = test_add_snippet()
        test4 = test_remove_snippet()
        test5 = test_get_snippets()
        test6 = test_get_snippet()
        test7 = test_preview_snippet()
        test8 = test_validate_snippet()
        test9 = test_get_supported_languages()
        test10 = test_get_builtin_snippets()
        test11 = test_snippet_scope_enum()
        test12 = test_snippet_variable_enum()
        test13 = test_snippet_placeholder_dataclass()
        test14 = test_snippet_dataclass()
        test15 = test_snippet_insertion_dataclass()
        test16 = test_snippet_search_result_dataclass()
        test17 = test_multiple_languages()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Insert Snippet: {'PASS' if test1 else 'FAIL'}")
        print(f"Search Snippets: {'PASS' if test2 else 'FAIL'}")
        print(f"Add Snippet: {'PASS' if test3 else 'FAIL'}")
        print(f"Remove Snippet: {'PASS' if test4 else 'FAIL'}")
        print(f"Get Snippets: {'PASS' if test5 else 'FAIL'}")
        print(f"Get Snippet: {'PASS' if test6 else 'FAIL'}")
        print(f"Preview Snippet: {'PASS' if test7 else 'FAIL'}")
        print(f"Validate Snippet: {'PASS' if test8 else 'FAIL'}")
        print(f"Get Supported Languages: {'PASS' if test9 else 'FAIL'}")
        print(f"Get Builtin Snippets: {'PASS' if test10 else 'FAIL'}")
        print(f"SnippetScope Enum: {'PASS' if test11 else 'FAIL'}")
        print(f"SnippetVariable Enum: {'PASS' if test12 else 'FAIL'}")
        print(f"SnippetPlaceholder Dataclass: {'PASS' if test13 else 'FAIL'}")
        print(f"Snippet Dataclass: {'PASS' if test14 else 'FAIL'}")
        print(f"SnippetInsertion Dataclass: {'PASS' if test15 else 'FAIL'}")
        print(f"SnippetSearchResult Dataclass: {'PASS' if test16 else 'FAIL'}")
        print(f"Multiple Languages: {'PASS' if test17 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14, test15, test16, test17])
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
