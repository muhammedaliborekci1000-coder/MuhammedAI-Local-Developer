"""
Quality Test: Trim Whitespace
Trim whitespace system testlesi.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.trim_whitespace import (
    TrimWhitespaceEngine,
    TrimScope,
    TrimMode,
    TrimRange,
    TrimConfig,
    TrimResult
)


def test_trim_whitespace():
    """
    Test: Trim whitespace.
    """
    print("=" * 70)
    print("TEST: Trim Whitespace")
    print("=" * 70)
    
    engine = TrimWhitespaceEngine()
    
    content = "def test():\n    pass  \n    return  "
    result = engine.trim_whitespace(content)
    
    assert result.success, "Temizleme başarılı olmalı"
    assert result.whitespace_removed > 0, "Whitespace kaldırılmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Whitespace removed: {result.whitespace_removed}")
    
    print("\n" + "=" * 70)
    print("PASS: Trim whitespace")
    print("=" * 70)


def test_trim_trailing():
    """
    Test: Trim trailing.
    """
    print("=" * 70)
    print("TEST: Trim Trailing")
    print("=" * 70)
    
    engine = TrimWhitespaceEngine()
    
    content = "def test():\n    pass  \n    return  "
    result = engine.trim_trailing(content)
    
    assert result.success, "Temizleme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Trim trailing")
    print("=" * 70)


def test_trim_leading():
    """
    Test: Trim leading.
    """
    print("=" * 70)
    print("TEST: Trim Leading")
    print("=" * 70)
    
    engine = TrimWhitespaceEngine()
    
    content = "def test():\n    pass\n    return"
    result = engine.trim_leading(content)
    
    assert result.success, "Temizleme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Trim leading")
    print("=" * 70)


def test_trim_both():
    """
    Test: Trim both.
    """
    print("=" * 70)
    print("TEST: Trim Both")
    print("=" * 70)
    
    engine = TrimWhitespaceEngine()
    
    content = "  def test():  \n    pass  \n    return  "
    result = engine.trim_both(content)
    
    assert result.success, "Temizleme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Trim both")
    print("=" * 70)


def test_trim_selection():
    """
    Test: Trim selection.
    """
    print("=" * 70)
    print("TEST: Trim Selection")
    print("=" * 70)
    
    config = TrimConfig(scope=TrimScope.SELECTION)
    engine = TrimWhitespaceEngine(config)
    
    content = "def test():\n    pass  \n    return  "
    trim_range = TrimRange(start_line=1, end_line=2)
    result = engine.trim_whitespace(content, trim_range)
    
    assert result.success, "Temizleme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Trim selection")
    print("=" * 70)


def test_trim_line():
    """
    Test: Trim line.
    """
    print("=" * 70)
    print("TEST: Trim Line")
    print("=" * 70)
    
    config = TrimConfig(scope=TrimScope.LINE)
    engine = TrimWhitespaceEngine(config)
    
    content = "def test():\n    pass  \n    return  "
    trim_range = TrimRange(start_line=1, end_line=1)
    result = engine.trim_whitespace(content, trim_range)
    
    assert result.success, "Temizleme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Trim line")
    print("=" * 70)


def test_trim_document():
    """
    Test: Trim document.
    """
    print("=" * 70)
    print("TEST: Trim Document")
    print("=" * 70)
    
    config = TrimConfig(scope=TrimScope.DOCUMENT)
    engine = TrimWhitespaceEngine(config)
    
    content = "def test():\n    pass  \n    return  "
    result = engine.trim_whitespace(content)
    
    assert result.success, "Temizleme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Trim document")
    print("=" * 70)


def test_trim_all_lines():
    """
    Test: Trim all lines.
    """
    print("=" * 70)
    print("TEST: Trim All Lines")
    print("=" * 70)
    
    config = TrimConfig(scope=TrimScope.ALL_LINES)
    engine = TrimWhitespaceEngine(config)
    
    content = "def test():\n    pass  \n    return  "
    result = engine.trim_whitespace(content)
    
    assert result.success, "Temizleme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Trim all lines")
    print("=" * 70)


def test_trim_mode_all():
    """
    Test: Trim mode all.
    """
    print("=" * 70)
    print("TEST: Trim Mode All")
    print("=" * 70)
    
    config = TrimConfig(mode=TrimMode.ALL)
    engine = TrimWhitespaceEngine(config)
    
    content = "  def test():  \n    pass  \n    return  "
    result = engine.trim_whitespace(content)
    
    assert result.success, "Temizleme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Trim mode all")
    print("=" * 70)


def test_undo_trim():
    """
    Test: Undo trim.
    """
    print("=" * 70)
    print("TEST: Undo Trim")
    print("=" * 70)
    
    engine = TrimWhitespaceEngine()
    
    content = "def test():\n    pass  "
    engine.trim_whitespace(content)
    result = engine.undo_trim()
    
    assert result.success, "Geri alma başarılı olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Undo trim")
    print("=" * 70)


def test_get_trim_history():
    """
    Test: Get trim history.
    """
    print("=" * 70)
    print("TEST: Get Trim History")
    print("=" * 70)
    
    engine = TrimWhitespaceEngine()
    
    content = "def test():\n    pass  "
    engine.trim_whitespace(content)
    history = engine.get_trim_history()
    
    assert len(history) > 0, "Geçmiş olmalı"
    
    print(f"  History: {len(history)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get trim history")
    print("=" * 70)


def test_clear_history():
    """
    Test: Clear history.
    """
    print("=" * 70)
    print("TEST: Clear History")
    print("=" * 70)
    
    engine = TrimWhitespaceEngine()
    
    content = "def test():\n    pass  "
    engine.trim_whitespace(content)
    result = engine.clear_history()
    
    assert result.success, "Temizleme başarılı olmalı"
    assert len(engine.get_trim_history()) == 0, "Geçmiş temizlenmeli"
    
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
    
    engine = TrimWhitespaceEngine()
    
    new_config = TrimConfig(mode=TrimMode.LEADING)
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
    
    engine = TrimWhitespaceEngine()
    
    config = engine.get_config()
    
    assert config is not None, "Config olmalı"
    assert config.mode == TrimMode.TRAILING, "Config eşleşmeli"
    
    print(f"  Mode: {config.mode.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


def test_trim_scope_enum():
    """
    Test: TrimScope enum.
    """
    print("=" * 70)
    print("TEST: TrimScope Enum")
    print("=" * 70)
    
    assert TrimScope.LINE.value == "line"
    assert TrimScope.SELECTION.value == "selection"
    assert TrimScope.DOCUMENT.value == "document"
    assert TrimScope.ALL_LINES.value == "all_lines"
    
    print(f"  All enum values verified")
    print(f"  Total scopes: {len(TrimScope)}")
    
    print("\n" + "=" * 70)
    print("PASS: TrimScope enum")
    print("=" * 70)


def test_trim_mode_enum():
    """
    Test: TrimMode enum.
    """
    print("=" * 70)
    print("TEST: TrimMode Enum")
    print("=" * 70)
    
    assert TrimMode.TRAILING.value == "trailing"
    assert TrimMode.LEADING.value == "leading"
    assert TrimMode.BOTH.value == "both"
    assert TrimMode.ALL.value == "all"
    
    print(f"  All enum values verified")
    print(f"  Total modes: {len(TrimMode)}")
    
    print("\n" + "=" * 70)
    print("PASS: TrimMode enum")
    print("=" * 70)


def test_trim_range_dataclass():
    """
    Test: TrimRange dataclass.
    """
    print("=" * 70)
    print("TEST: TrimRange Dataclass")
    print("=" * 70)
    
    trim_range = TrimRange(
        start_line=0,
        end_line=5,
        start_column=0,
        end_column=10
    )
    
    assert trim_range.start_line == 0, "Start line eşleşmeli"
    assert trim_range.end_line == 5, "End line eşleşmeli"
    
    print(f"  Start line: {trim_range.start_line}")
    print(f"  End line: {trim_range.end_line}")
    
    print("\n" + "=" * 70)
    print("PASS: TrimRange dataclass")
    print("=" * 70)


def test_trim_config_dataclass():
    """
    Test: TrimConfig dataclass.
    """
    print("=" * 70)
    print("TEST: TrimConfig Dataclass")
    print("=" * 70)
    
    config = TrimConfig(
        scope=TrimScope.DOCUMENT,
        mode=TrimMode.TRAILING,
        trim_empty_lines=True
    )
    
    assert config.scope == TrimScope.DOCUMENT, "Scope eşleşmeli"
    assert config.mode == TrimMode.TRAILING, "Mode eşleşmeli"
    assert config.trim_empty_lines == True, "Trim empty lines eşleşmeli"
    
    print(f"  Scope: {config.scope.value}")
    print(f"  Mode: {config.mode.value}")
    print(f"  Trim empty lines: {config.trim_empty_lines}")
    
    print("\n" + "=" * 70)
    print("PASS: TrimConfig dataclass")
    print("=" * 70)


def test_trim_result_dataclass():
    """
    Test: TrimResult dataclass.
    """
    print("=" * 70)
    print("TEST: TrimResult Dataclass")
    print("=" * 70)
    
    result = TrimResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: TrimResult dataclass")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_trim_whitespace()
        test2 = test_trim_trailing()
        test3 = test_trim_leading()
        test4 = test_trim_both()
        test5 = test_trim_selection()
        test6 = test_trim_line()
        test7 = test_trim_document()
        test8 = test_trim_all_lines()
        test9 = test_trim_mode_all()
        test10 = test_undo_trim()
        test11 = test_get_trim_history()
        test12 = test_clear_history()
        test13 = test_update_config()
        test14 = test_get_config()
        test15 = test_trim_scope_enum()
        test16 = test_trim_mode_enum()
        test17 = test_trim_range_dataclass()
        test18 = test_trim_config_dataclass()
        test19 = test_trim_result_dataclass()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Trim Whitespace: {'PASS' if test1 else 'FAIL'}")
        print(f"Trim Trailing: {'PASS' if test2 else 'FAIL'}")
        print(f"Trim Leading: {'PASS' if test3 else 'FAIL'}")
        print(f"Trim Both: {'PASS' if test4 else 'FAIL'}")
        print(f"Trim Selection: {'PASS' if test5 else 'FAIL'}")
        print(f"Trim Line: {'PASS' if test6 else 'FAIL'}")
        print(f"Trim Document: {'PASS' if test7 else 'FAIL'}")
        print(f"Trim All Lines: {'PASS' if test8 else 'FAIL'}")
        print(f"Trim Mode All: {'PASS' if test9 else 'FAIL'}")
        print(f"Undo Trim: {'PASS' if test10 else 'FAIL'}")
        print(f"Get Trim History: {'PASS' if test11 else 'FAIL'}")
        print(f"Clear History: {'PASS' if test12 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test13 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test14 else 'FAIL'}")
        print(f"TrimScope Enum: {'PASS' if test15 else 'FAIL'}")
        print(f"TrimMode Enum: {'PASS' if test16 else 'FAIL'}")
        print(f"TrimRange Dataclass: {'PASS' if test17 else 'FAIL'}")
        print(f"TrimConfig Dataclass: {'PASS' if test18 else 'FAIL'}")
        print(f"TrimResult Dataclass: {'PASS' if test19 else 'FAIL'}")
        
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
