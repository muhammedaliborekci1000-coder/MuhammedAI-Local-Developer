"""
Quality Test: Emmet Support
Emmet support system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.emmet_support import (
    EmmetSupportEngine,
    EmmetLanguage,
    EmmetAction,
    EmmetAbbreviation,
    EmmetConfig,
    EmmetResult
)


def test_expand_abbreviation():
    """
    Test: Expand abbreviation.
    """
    print("=" * 70)
    print("TEST: Expand Abbreviation")
    print("=" * 70)
    
    engine = EmmetSupportEngine()
    
    result = engine.expand_abbreviation("div")
    
    assert result.success, "Genişletme başarılı olmalı"
    assert "<div>" in result.expanded_content, "Div tag olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Expanded: {result.expanded_content}")
    
    print("\n" + "=" * 70)
    print("PASS: Expand abbreviation")
    print("=" * 70)


def test_expand_html():
    """
    Test: Expand HTML.
    """
    print("=" * 70)
    print("TEST: Expand HTML")
    print("=" * 70)
    
    engine = EmmetSupportEngine()
    
    result = engine.expand_abbreviation("p", EmmetLanguage.HTML)
    
    assert result.success, "Genişletme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Expanded: {result.expanded_content}")
    
    print("\n" + "=" * 70)
    print("PASS: Expand HTML")
    print("=" * 70)


def test_expand_css():
    """
    Test: Expand CSS.
    """
    print("=" * 70)
    print("TEST: Expand CSS")
    print("=" * 70)
    
    engine = EmmetSupportEngine()
    
    result = engine.expand_abbreviation("m", EmmetLanguage.CSS)
    
    assert result.success, "Genişletme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Expanded: {result.expanded_content}")
    
    print("\n" + "=" * 70)
    print("PASS: Expand CSS")
    print("=" * 70)


def test_expand_with_id():
    """
    Test: Expand with ID.
    """
    print("=" * 70)
    print("TEST: Expand with ID")
    print("=" * 70)
    
    engine = EmmetSupportEngine()
    
    result = engine.expand_abbreviation("div#main")
    
    assert result.success, "Genişletme başarılı olmalı"
    assert "id=\"main\"" in result.expanded_content, "ID olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Expanded: {result.expanded_content}")
    
    print("\n" + "=" * 70)
    print("PASS: Expand with ID")
    print("=" * 70)


def test_expand_with_class():
    """
    Test: Expand with class.
    """
    print("=" * 70)
    print("TEST: Expand with Class")
    print("=" * 70)
    
    engine = EmmetSupportEngine()
    
    result = engine.expand_abbreviation("div.container")
    
    assert result.success, "Genişletme başarılı olmalı"
    assert "class=\"container\"" in result.expanded_content, "Class olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Expanded: {result.expanded_content}")
    
    print("\n" + "=" * 70)
    print("PASS: Expand with class")
    print("=" * 70)


def test_expand_with_multiplier():
    """
    Test: Expand with multiplier.
    """
    print("=" * 70)
    print("TEST: Expand with Multiplier")
    print("=" * 70)
    
    engine = EmmetSupportEngine()
    
    result = engine.expand_abbreviation("div*3")
    
    assert result.success, "Genişletme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Expanded: {result.expanded_content}")
    
    print("\n" + "=" * 70)
    print("PASS: Expand with multiplier")
    print("=" * 70)


def test_wrap_with_abbreviation():
    """
    Test: Wrap with abbreviation.
    """
    print("=" * 70)
    print("TEST: Wrap with Abbreviation")
    print("=" * 70)
    
    engine = EmmetSupportEngine()
    
    content = "Hello World"
    result = engine.wrap_with_abbreviation(content, "p")
    
    assert result.success, "Sarma başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Wrapped: {result.expanded_content}")
    
    print("\n" + "=" * 70)
    print("PASS: Wrap with abbreviation")
    print("=" * 70)


def test_balance_tags():
    """
    Test: Balance tags.
    """
    print("=" * 70)
    print("TEST: Balance Tags")
    print("=" * 70)
    
    engine = EmmetSupportEngine()
    
    content = "<div>Hello</div>"
    result = engine.balance_tags(content)
    
    assert result.success, "Dengeleme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Balance tags")
    print("=" * 70)


def test_remove_tag():
    """
    Test: Remove tag.
    """
    print("=" * 70)
    print("TEST: Remove Tag")
    print("=" * 70)
    
    engine = EmmetSupportEngine()
    
    content = "<div>Hello</div>"
    result = engine.remove_tag(content)
    
    assert result.success, "Kaldırma başarılı olmalı"
    assert "<" not in result.expanded_content, "Tag kaldırılmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Removed: {result.expanded_content}")
    
    print("\n" + "=" * 70)
    print("PASS: Remove tag")
    print("=" * 70)


def test_update_tag():
    """
    Test: Update tag.
    """
    print("=" * 70)
    print("TEST: Update Tag")
    print("=" * 70)
    
    engine = EmmetSupportEngine()
    
    content = "<div>Hello</div>"
    result = engine.update_tag(content, "p")
    
    assert result.success, "Güncelleme başarılı olmalı"
    assert "<p>" in result.expanded_content, "Tag güncellenmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Updated: {result.expanded_content}")
    
    print("\n" + "=" * 70)
    print("PASS: Update tag")
    print("=" * 70)


def test_merge_lines():
    """
    Test: Merge lines.
    """
    print("=" * 70)
    print("TEST: Merge Lines")
    print("=" * 70)
    
    engine = EmmetSupportEngine()
    
    content = "line1\nline2\nline3"
    result = engine.merge_lines(content)
    
    assert result.success, "Birleştirme başarılı olmalı"
    assert "\n" not in result.expanded_content, "Satırlar birleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Merged: {result.expanded_content}")
    
    print("\n" + "=" * 70)
    print("PASS: Merge lines")
    print("=" * 70)


def test_add_custom_snippet():
    """
    Test: Add custom snippet.
    """
    print("=" * 70)
    print("TEST: Add Custom Snippet")
    print("=" * 70)
    
    engine = EmmetSupportEngine()
    
    result = engine.add_custom_snippet("custom", "<custom></custom>", EmmetLanguage.HTML)
    
    assert result.success, "Ekleme başarılı olmalı"
    assert "custom" in engine.html_snippets, "Snippet eklenmeli"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Add custom snippet")
    print("=" * 70)


def test_undo_expansion():
    """
    Test: Undo expansion.
    """
    print("=" * 70)
    print("TEST: Undo Expansion")
    print("=" * 70)
    
    engine = EmmetSupportEngine()
    
    engine.expand_abbreviation("div")
    result = engine.undo_expansion()
    
    assert result.success, "Geri alma başarılı olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Undo expansion")
    print("=" * 70)


def test_get_expansion_history():
    """
    Test: Get expansion history.
    """
    print("=" * 70)
    print("TEST: Get Expansion History")
    print("=" * 70)
    
    engine = EmmetSupportEngine()
    
    engine.expand_abbreviation("div")
    history = engine.get_expansion_history()
    
    assert len(history) > 0, "Geçmiş olmalı"
    
    print(f"  History: {len(history)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get expansion history")
    print("=" * 70)


def test_clear_history():
    """
    Test: Clear history.
    """
    print("=" * 70)
    print("TEST: Clear History")
    print("=" * 70)
    
    engine = EmmetSupportEngine()
    
    engine.expand_abbreviation("div")
    result = engine.clear_history()
    
    assert result.success, "Temizleme başarılı olmalı"
    assert len(engine.get_expansion_history()) == 0, "Geçmiş temizlenmeli"
    
    print(f"  Success: {result.success}")
    
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
    
    engine = EmmetSupportEngine()
    
    new_config = EmmetConfig(language=EmmetLanguage.CSS)
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
    
    engine = EmmetSupportEngine()
    
    config = engine.get_config()
    
    assert config is not None, "Config olmalı"
    assert config.language == EmmetLanguage.HTML, "Config eşleşmeli"
    
    print(f"  Language: {config.language.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


def test_emmet_language_enum():
    """
    Test: EmmetLanguage enum.
    """
    print("=" * 70)
    print("TEST: EmmetLanguage Enum")
    print("=" * 70)
    
    assert EmmetLanguage.HTML.value == "html"
    assert EmmetLanguage.CSS.value == "css"
    assert EmmetLanguage.JAVASCRIPT.value == "javascript"
    assert EmmetLanguage.XML.value == "xml"
    assert EmmetLanguage.JSX.value == "jsx"
    assert EmmetLanguage.TSX.value == "tsx"
    
    print(f"  All enum values verified")
    print(f"  Total languages: {len(EmmetLanguage)}")
    
    print("\n" + "=" * 70)
    print("PASS: EmmetLanguage enum")
    print("=" * 70)


def test_emmet_action_enum():
    """
    Test: EmmetAction enum.
    """
    print("=" * 70)
    print("TEST: EmmetAction Enum")
    print("=" * 70)
    
    assert EmmetAction.EXPAND.value == "expand"
    assert EmmetAction.WRAP.value == "wrap"
    assert EmmetAction.BALANCE.value == "balance"
    assert EmmetAction.REMOVE_TAG.value == "remove_tag"
    assert EmmetAction.SPLIT_JOIN_TAG.value == "split_join_tag"
    assert EmmetAction.UPDATE_TAG.value == "update_tag"
    assert EmmetAction.MERGE_LINES.value == "merge_lines"
    
    print(f"  All enum values verified")
    print(f"  Total actions: {len(EmmetAction)}")
    
    print("\n" + "=" * 70)
    print("PASS: EmmetAction enum")
    print("=" * 70)


def test_emmet_abbreviation_dataclass():
    """
    Test: EmmetAbbreviation dataclass.
    """
    print("=" * 70)
    print("TEST: EmmetAbbreviation Dataclass")
    print("=" * 70)
    
    abbreviation = EmmetAbbreviation(
        abbreviation="div",
        language=EmmetLanguage.HTML,
        line=0,
        column=0
    )
    
    assert abbreviation.abbreviation == "div", "Abbreviation eşleşmeli"
    assert abbreviation.language == EmmetLanguage.HTML, "Language eşleşmeli"
    
    print(f"  Abbreviation: {abbreviation.abbreviation}")
    print(f"  Language: {abbreviation.language.value}")
    
    print("\n" + "=" * 70)
    print("PASS: EmmetAbbreviation dataclass")
    print("=" * 70)


def test_emmet_config_dataclass():
    """
    Test: EmmetConfig dataclass.
    """
    print("=" * 70)
    print("TEST: EmmetConfig Dataclass")
    print("=" * 70)
    
    config = EmmetConfig(
        enabled=True,
        language=EmmetLanguage.HTML,
        auto_expand=True
    )
    
    assert config.enabled == True, "Enabled eşleşmeli"
    assert config.language == EmmetLanguage.HTML, "Language eşleşmeli"
    assert config.auto_expand == True, "Auto expand eşleşmeli"
    
    print(f"  Enabled: {config.enabled}")
    print(f"  Language: {config.language.value}")
    print(f"  Auto expand: {config.auto_expand}")
    
    print("\n" + "=" * 70)
    print("PASS: EmmetConfig dataclass")
    print("=" * 70)


def test_emmet_result_dataclass():
    """
    Test: EmmetResult dataclass.
    """
    print("=" * 70)
    print("TEST: EmmetResult Dataclass")
    print("=" * 70)
    
    result = EmmetResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: EmmetResult dataclass")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_expand_abbreviation()
        test2 = test_expand_html()
        test3 = test_expand_css()
        test4 = test_expand_with_id()
        test5 = test_expand_with_class()
        test6 = test_expand_with_multiplier()
        test7 = test_wrap_with_abbreviation()
        test8 = test_balance_tags()
        test9 = test_remove_tag()
        test10 = test_update_tag()
        test11 = test_merge_lines()
        test12 = test_add_custom_snippet()
        test13 = test_undo_expansion()
        test14 = test_get_expansion_history()
        test15 = test_clear_history()
        test16 = test_update_config()
        test17 = test_get_config()
        test18 = test_emmet_language_enum()
        test19 = test_emmet_action_enum()
        test20 = test_emmet_abbreviation_dataclass()
        test21 = test_emmet_config_dataclass()
        test22 = test_emmet_result_dataclass()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Expand Abbreviation: {'PASS' if test1 else 'FAIL'}")
        print(f"Expand HTML: {'PASS' if test2 else 'FAIL'}")
        print(f"Expand CSS: {'PASS' if test3 else 'FAIL'}")
        print(f"Expand with ID: {'PASS' if test4 else 'FAIL'}")
        print(f"Expand with Class: {'PASS' if test5 else 'FAIL'}")
        print(f"Expand with Multiplier: {'PASS' if test6 else 'FAIL'}")
        print(f"Wrap with Abbreviation: {'PASS' if test7 else 'FAIL'}")
        print(f"Balance Tags: {'PASS' if test8 else 'FAIL'}")
        print(f"Remove Tag: {'PASS' if test9 else 'FAIL'}")
        print(f"Update Tag: {'PASS' if test10 else 'FAIL'}")
        print(f"Merge Lines: {'PASS' if test11 else 'FAIL'}")
        print(f"Add Custom Snippet: {'PASS' if test12 else 'FAIL'}")
        print(f"Undo Expansion: {'PASS' if test13 else 'FAIL'}")
        print(f"Get Expansion History: {'PASS' if test14 else 'FAIL'}")
        print(f"Clear History: {'PASS' if test15 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test16 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test17 else 'FAIL'}")
        print(f"EmmetLanguage Enum: {'PASS' if test18 else 'FAIL'}")
        print(f"EmmetAction Enum: {'PASS' if test19 else 'FAIL'}")
        print(f"EmmetAbbreviation Dataclass: {'PASS' if test20 else 'FAIL'}")
        print(f"EmmetConfig Dataclass: {'PASS' if test21 else 'FAIL'}")
        print(f"EmmetResult Dataclass: {'PASS' if test22 else 'FAIL'}")
        
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
