"""
Quality Test: Block Comment
Block comment system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.block_comment import (
    BlockCommentEngine,
    BlockCommentStyle,
    BlockCommentAction,
    BlockCommentRange,
    BlockCommentSyntax,
    BlockCommentConfig,
    BlockCommentResult
)


def test_add_block_comment():
    """
    Test: Add block comment.
    """
    print("=" * 70)
    print("TEST: Add Block Comment")
    print("=" * 70)
    
    engine = BlockCommentEngine()
    
    content = "def test():\n    pass\n    return"
    comment_range = BlockCommentRange(start_line=0, end_line=2)
    result = engine.add_block_comment(content, comment_range)
    
    assert result.success, "Ekleme başarılı olmalı"
    assert result.modified_content != content, "İçerik değişmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Content changed: {result.modified_content != content}")
    
    print("\n" + "=" * 70)
    print("PASS: Add block comment")
    print("=" * 70)


def test_remove_block_comment():
    """
    Test: Remove block comment.
    """
    print("=" * 70)
    print("TEST: Remove Block Comment")
    print("=" * 70)
    
    engine = BlockCommentEngine()
    
    content = '"""def test():\n    pass\n    return"""'
    comment_range = BlockCommentRange(start_line=0, end_line=2)
    result = engine.remove_block_comment(content, comment_range)
    
    assert result.success, "Kaldırma başarılı olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Remove block comment")
    print("=" * 70)


def test_toggle_block_comment():
    """
    Test: Toggle block comment.
    """
    print("=" * 70)
    print("TEST: Toggle Block Comment")
    print("=" * 70)
    
    engine = BlockCommentEngine()
    
    content = "def test():\n    pass\n    return"
    comment_range = BlockCommentRange(start_line=0, end_line=2)
    result = engine.toggle_block_comment(content, comment_range)
    
    assert result.success, "Toggle başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Action: {result.action_performed.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Toggle block comment")
    print("=" * 70)


def test_unwrap_comment():
    """
    Test: Unwrap comment.
    """
    print("=" * 70)
    print("TEST: Unwrap Comment")
    print("=" * 70)
    
    engine = BlockCommentEngine()
    
    content = '"""\ndef test():\n    pass\n    return\n"""'
    comment_range = BlockCommentRange(start_line=0, end_line=4)
    result = engine.unwrap_comment(content, comment_range)
    
    assert result.success, "Unwrap başarılı olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Unwrap comment")
    print("=" * 70)


def test_multiline_style():
    """
    Test: Multiline style.
    """
    print("=" * 70)
    print("TEST: Multiline Style")
    print("=" * 70)
    
    config = BlockCommentConfig(style=BlockCommentStyle.MULTILINE)
    engine = BlockCommentEngine(config)
    
    content = "def test():\n    pass"
    comment_range = BlockCommentRange(start_line=0, end_line=1)
    result = engine.add_block_comment(content, comment_range)
    
    assert result.success, "Ekleme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Multiline style")
    print("=" * 70)


def test_single_line_style():
    """
    Test: Single line style.
    """
    print("=" * 70)
    print("TEST: Single Line Style")
    print("=" * 70)
    
    config = BlockCommentConfig(style=BlockCommentStyle.SINGLE_LINE)
    engine = BlockCommentEngine(config)
    
    content = "def test():\n    pass"
    comment_range = BlockCommentRange(start_line=0, end_line=1)
    result = engine.add_block_comment(content, comment_range, language="javascript")
    
    assert result.success, "Ekleme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Single line style")
    print("=" * 70)


def test_wrap_style():
    """
    Test: Wrap style.
    """
    print("=" * 70)
    print("TEST: Wrap Style")
    print("=" * 70)
    
    config = BlockCommentConfig(style=BlockCommentStyle.WRAP)
    engine = BlockCommentEngine(config)
    
    content = "def test():\n    pass"
    comment_range = BlockCommentRange(start_line=0, end_line=1)
    result = engine.add_block_comment(content, comment_range)
    
    assert result.success, "Ekleme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Wrap style")
    print("=" * 70)


def test_box_style():
    """
    Test: Box style.
    """
    print("=" * 70)
    print("TEST: Box Style")
    print("=" * 70)
    
    config = BlockCommentConfig(style=BlockCommentStyle.BOX)
    engine = BlockCommentEngine(config)
    
    content = "def test():\n    pass"
    comment_range = BlockCommentRange(start_line=0, end_line=1)
    result = engine.add_block_comment(content, comment_range)
    
    assert result.success, "Ekleme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Box style")
    print("=" * 70)


def test_invalid_range():
    """
    Test: Invalid range.
    """
    print("=" * 70)
    print("TEST: Invalid Range")
    print("=" * 70)
    
    engine = BlockCommentEngine()
    
    content = "def test():\n    pass"
    comment_range = BlockCommentRange(start_line=10, end_line=20)
    result = engine.add_block_comment(content, comment_range)
    
    assert result.success == False, "Başarısız olmalı"
    assert len(result.errors) > 0, "Hata olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Errors: {result.errors}")
    
    print("\n" + "=" * 70)
    print("PASS: Invalid range")
    print("=" * 70)


def test_unsupported_language():
    """
    Test: Unsupported language.
    """
    print("=" * 70)
    print("TEST: Unsupported Language")
    print("=" * 70)
    
    engine = BlockCommentEngine()
    
    content = "def test():\n    pass"
    comment_range = BlockCommentRange(start_line=0, end_line=1)
    result = engine.add_block_comment(content, comment_range, language="unknown")
    
    assert result.success == False, "Başarısız olmalı"
    assert len(result.errors) > 0, "Hata olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Errors: {result.errors}")
    
    print("\n" + "=" * 70)
    print("PASS: Unsupported language")
    print("=" * 70)


def test_undo_comment():
    """
    Test: Undo comment.
    """
    print("=" * 70)
    print("TEST: Undo Comment")
    print("=" * 70)
    
    engine = BlockCommentEngine()
    
    content = "def test():\n    pass"
    comment_range = BlockCommentRange(start_line=0, end_line=1)
    engine.add_block_comment(content, comment_range)
    result = engine.undo_comment()
    
    assert result.success, "Geri alma başarılı olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Undo comment")
    print("=" * 70)


def test_get_comment_history():
    """
    Test: Get comment history.
    """
    print("=" * 70)
    print("TEST: Get Comment History")
    print("=" * 70)
    
    engine = BlockCommentEngine()
    
    content = "def test():\n    pass"
    comment_range = BlockCommentRange(start_line=0, end_line=1)
    engine.add_block_comment(content, comment_range)
    history = engine.get_comment_history()
    
    assert len(history) > 0, "Geçmiş olmalı"
    
    print(f"  History: {len(history)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get comment history")
    print("=" * 70)


def test_clear_history():
    """
    Test: Clear history.
    """
    print("=" * 70)
    print("TEST: Clear History")
    print("=" * 70)
    
    engine = BlockCommentEngine()
    
    content = "def test():\n    pass"
    comment_range = BlockCommentRange(start_line=0, end_line=1)
    engine.add_block_comment(content, comment_range)
    result = engine.clear_history()
    
    assert result.success, "Temizleme başarılı olmalı"
    assert len(engine.get_comment_history()) == 0, "Geçmiş temizlenmeli"
    
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
    
    engine = BlockCommentEngine()
    
    new_config = BlockCommentConfig(style=BlockCommentStyle.WRAP)
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
    
    engine = BlockCommentEngine()
    
    config = engine.get_config()
    
    assert config is not None, "Config olmalı"
    assert config.style == BlockCommentStyle.MULTILINE, "Config eşleşmeli"
    
    print(f"  Style: {config.style.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


def test_block_comment_style_enum():
    """
    Test: BlockCommentStyle enum.
    """
    print("=" * 70)
    print("TEST: BlockCommentStyle Enum")
    print("=" * 70)
    
    assert BlockCommentStyle.MULTILINE.value == "multiline"
    assert BlockCommentStyle.SINGLE_LINE.value == "single_line"
    assert BlockCommentStyle.WRAP.value == "wrap"
    assert BlockCommentStyle.BOX.value == "box"
    
    print(f"  All enum values verified")
    print(f"  Total styles: {len(BlockCommentStyle)}")
    
    print("\n" + "=" * 70)
    print("PASS: BlockCommentStyle enum")
    print("=" * 70)


def test_block_comment_action_enum():
    """
    Test: BlockCommentAction enum.
    """
    print("=" * 70)
    print("TEST: BlockCommentAction Enum")
    print("=" * 70)
    
    assert BlockCommentAction.ADD.value == "add"
    assert BlockCommentAction.REMOVE.value == "remove"
    assert BlockCommentAction.TOGGLE.value == "toggle"
    assert BlockCommentAction.WRAP.value == "wrap"
    assert BlockCommentAction.UNWRAP.value == "unwrap"
    
    print(f"  All enum values verified")
    print(f"  Total actions: {len(BlockCommentAction)}")
    
    print("\n" + "=" * 70)
    print("PASS: BlockCommentAction enum")
    print("=" * 70)


def test_block_comment_range_dataclass():
    """
    Test: BlockCommentRange dataclass.
    """
    print("=" * 70)
    print("TEST: BlockCommentRange Dataclass")
    print("=" * 70)
    
    range = BlockCommentRange(
        start_line=0,
        end_line=5,
        start_column=0,
        end_column=10
    )
    
    assert range.start_line == 0, "Start line eşleşmeli"
    assert range.end_line == 5, "End line eşleşmeli"
    
    print(f"  Start line: {range.start_line}")
    print(f"  End line: {range.end_line}")
    
    print("\n" + "=" * 70)
    print("PASS: BlockCommentRange dataclass")
    print("=" * 70)


def test_block_comment_syntax_dataclass():
    """
    Test: BlockCommentSyntax dataclass.
    """
    print("=" * 70)
    print("TEST: BlockCommentSyntax Dataclass")
    print("=" * 70)
    
    syntax = BlockCommentSyntax(
        language="python",
        start_marker='"""',
        end_marker='"""'
    )
    
    assert syntax.language == "python", "Language eşleşmeli"
    assert syntax.start_marker == '"""', "Start marker eşleşmeli"
    
    print(f"  Language: {syntax.language}")
    print(f"  Start marker: {syntax.start_marker}")
    
    print("\n" + "=" * 70)
    print("PASS: BlockCommentSyntax dataclass")
    print("=" * 70)


def test_block_comment_config_dataclass():
    """
    Test: BlockCommentConfig dataclass.
    """
    print("=" * 70)
    print("TEST: BlockCommentConfig Dataclass")
    print("=" * 70)
    
    config = BlockCommentConfig(
        style=BlockCommentStyle.MULTILINE,
        add_space_after_marker=True,
        preserve_indentation=True
    )
    
    assert config.style == BlockCommentStyle.MULTILINE, "Style eşleşmeli"
    assert config.add_space_after_marker == True, "Add space after marker eşleşmeli"
    assert config.preserve_indentation == True, "Preserve indentation eşleşmeli"
    
    print(f"  Style: {config.style.value}")
    print(f"  Add space after marker: {config.add_space_after_marker}")
    print(f"  Preserve indentation: {config.preserve_indentation}")
    
    print("\n" + "=" * 70)
    print("PASS: BlockCommentConfig dataclass")
    print("=" * 70)


def test_block_comment_result_dataclass():
    """
    Test: BlockCommentResult dataclass.
    """
    print("=" * 70)
    print("TEST: BlockCommentResult Dataclass")
    print("=" * 70)
    
    result = BlockCommentResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: BlockCommentResult dataclass")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_add_block_comment()
        test2 = test_remove_block_comment()
        test3 = test_toggle_block_comment()
        test4 = test_unwrap_comment()
        test5 = test_multiline_style()
        test6 = test_single_line_style()
        test7 = test_wrap_style()
        test8 = test_box_style()
        test9 = test_invalid_range()
        test10 = test_unsupported_language()
        test11 = test_undo_comment()
        test12 = test_get_comment_history()
        test13 = test_clear_history()
        test14 = test_update_config()
        test15 = test_get_config()
        test16 = test_block_comment_style_enum()
        test17 = test_block_comment_action_enum()
        test18 = test_block_comment_range_dataclass()
        test19 = test_block_comment_syntax_dataclass()
        test20 = test_block_comment_config_dataclass()
        test21 = test_block_comment_result_dataclass()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Add Block Comment: {'PASS' if test1 else 'FAIL'}")
        print(f"Remove Block Comment: {'PASS' if test2 else 'FAIL'}")
        print(f"Toggle Block Comment: {'PASS' if test3 else 'FAIL'}")
        print(f"Unwrap Comment: {'PASS' if test4 else 'FAIL'}")
        print(f"Multiline Style: {'PASS' if test5 else 'FAIL'}")
        print(f"Single Line Style: {'PASS' if test6 else 'FAIL'}")
        print(f"Wrap Style: {'PASS' if test7 else 'FAIL'}")
        print(f"Box Style: {'PASS' if test8 else 'FAIL'}")
        print(f"Invalid Range: {'PASS' if test9 else 'FAIL'}")
        print(f"Unsupported Language: {'PASS' if test10 else 'FAIL'}")
        print(f"Undo Comment: {'PASS' if test11 else 'FAIL'}")
        print(f"Get Comment History: {'PASS' if test12 else 'FAIL'}")
        print(f"Clear History: {'PASS' if test13 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test14 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test15 else 'FAIL'}")
        print(f"BlockCommentStyle Enum: {'PASS' if test16 else 'FAIL'}")
        print(f"BlockCommentAction Enum: {'PASS' if test17 else 'FAIL'}")
        print(f"BlockCommentRange Dataclass: {'PASS' if test18 else 'FAIL'}")
        print(f"BlockCommentSyntax Dataclass: {'PASS' if test19 else 'FAIL'}")
        print(f"BlockCommentConfig Dataclass: {'PASS' if test20 else 'FAIL'}")
        print(f"BlockCommentResult Dataclass: {'PASS' if test21 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14, test15, test16, test17, test18, test19, test20, test21])
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
