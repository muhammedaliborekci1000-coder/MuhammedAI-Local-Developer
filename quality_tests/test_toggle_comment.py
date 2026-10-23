"""
Quality Test: Toggle Comment
Toggle comment system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.toggle_comment import (
    ToggleCommentEngine,
    CommentStyle,
    CommentAction,
    CommentSyntax,
    CommentEdit,
    ToggleCommentResult
)


def test_toggle_line_comment():
    """
    Test: Toggle line comment.
    """
    print("=" * 70)
    print("TEST: Toggle Line Comment")
    print("=" * 70)
    
    code = """def my_function():
    x = 10
    return x
"""
    
    engine = ToggleCommentEngine()
    result = engine.toggle_line_comment(code, 1, language="python")
    
    assert result.success, "Toggle line comment başarılı olmalı"
    assert result.lines_changed == 1, "1 satır değişmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Action: {result.action_performed.value}")
    print(f"  Lines changed: {result.lines_changed}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Toggle line comment")
    print("=" * 70)


def test_toggle_block_comment():
    """
    Test: Toggle block comment.
    """
    print("=" * 70)
    print("TEST: Toggle Block Comment")
    print("=" * 70)
    
    code = """def my_function():
    x = 10
    return x
"""
    
    engine = ToggleCommentEngine()
    result = engine.toggle_block_comment(code, 0, 2, language="python")
    
    assert result.success, "Toggle block comment başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Action: {result.action_performed.value}")
    print(f"  Lines changed: {result.lines_changed}")
    
    print("\n" + "=" * 70)
    print("PASS: Toggle block comment")
    print("=" * 70)


def test_comment_selection():
    """
    Test: Comment selection.
    """
    print("=" * 70)
    print("TEST: Comment Selection")
    print("=" * 70)
    
    code = """def my_function():
    x = 10
    y = 20
    return x + y
"""
    
    engine = ToggleCommentEngine()
    result = engine.comment_selection(code, 1, 2, language="python")
    
    assert result.success, "Comment selection başarılı olmalı"
    assert result.lines_changed > 0, "Satırlar değişmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Lines changed: {result.lines_changed}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Comment selection")
    print("=" * 70)


def test_uncomment_selection():
    """
    Test: Uncomment selection.
    """
    print("=" * 70)
    print("TEST: Uncomment Selection")
    print("=" * 70)
    
    code = """def my_function():
    # x = 10
    # y = 20
    return x + y
"""
    
    engine = ToggleCommentEngine()
    result = engine.uncomment_selection(code, 1, 2, language="python")
    
    assert result.success, "Uncomment selection başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Lines changed: {result.lines_changed}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Uncomment selection")
    print("=" * 70)


def test_smart_toggle():
    """
    Test: Smart toggle.
    """
    print("=" * 70)
    print("TEST: Smart Toggle")
    print("=" * 70)
    
    code = """def my_function():
    x = 10
    y = 20
    return x + y
"""
    
    engine = ToggleCommentEngine()
    result = engine.smart_toggle(code, 1, 2, language="python")
    
    assert result.success, "Smart toggle başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Action: {result.action_performed.value}")
    print(f"  Lines changed: {result.lines_changed}")
    
    print("\n" + "=" * 70)
    print("PASS: Smart toggle")
    print("=" * 70)


def test_add_docstring():
    """
    Test: Add docstring.
    """
    print("=" * 70)
    print("TEST: Add Docstring")
    print("=" * 70)
    
    code = """def my_function():
    x = 10
    return x
"""
    
    engine = ToggleCommentEngine()
    result = engine.add_docstring(code, 0, language="python")
    
    assert result.success, "Add docstring başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Lines changed: {result.lines_changed}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add docstring")
    print("=" * 70)


def test_get_comment_syntax():
    """
    Test: Get comment syntax.
    """
    print("=" * 70)
    print("TEST: Get Comment Syntax")
    print("=" * 70)
    
    engine = ToggleCommentEngine()
    
    python_syntax = engine.get_comment_syntax("python")
    assert python_syntax is not None, "Python syntax olmalı"
    assert python_syntax.line_comment == "#", "Python line comment # olmalı"
    
    js_syntax = engine.get_comment_syntax("javascript")
    assert js_syntax is not None, "JavaScript syntax olmalı"
    assert js_syntax.line_comment == "//", "JavaScript line comment // olmalı"
    
    print(f"  Python line comment: {python_syntax.line_comment}")
    print(f"  JavaScript line comment: {js_syntax.line_comment}")
    
    print("\n" + "=" * 70)
    print("PASS: Get comment syntax")
    print("=" * 70)


def test_is_commented():
    """
    Test: Is commented.
    """
    print("=" * 70)
    print("TEST: Is Commented")
    print("=" * 70)
    
    code = """def my_function():
    # x = 10
    y = 20
    return x + y
"""
    
    engine = ToggleCommentEngine()
    
    is_commented = engine.is_commented(code, 1, language="python")
    assert is_commented == True, "Satır 1 yorumlanmış olmalı"
    
    not_commented = engine.is_commented(code, 2, language="python")
    assert not_commented == False, "Satır 2 yorumlanmamış olmalı"
    
    print(f"  Line 1 commented: {is_commented}")
    print(f"  Line 2 commented: {not_commented}")
    
    print("\n" + "=" * 70)
    print("PASS: Is commented")
    print("=" * 70)


def test_comment_style_enum():
    """
    Test: CommentStyle enum.
    """
    print("=" * 70)
    print("TEST: CommentStyle Enum")
    print("=" * 70)
    
    assert CommentStyle.LINE.value == "line"
    assert CommentStyle.BLOCK.value == "block"
    assert CommentStyle.DOCSTRING.value == "docstring"
    
    print(f"  All enum values verified")
    print(f"  Total styles: {len(CommentStyle)}")
    
    print("\n" + "=" * 70)
    print("PASS: CommentStyle enum")
    print("=" * 70)


def test_comment_action_enum():
    """
    Test: CommentAction enum.
    """
    print("=" * 70)
    print("TEST: CommentAction Enum")
    print("=" * 70)
    
    assert CommentAction.ADD.value == "add"
    assert CommentAction.REMOVE.value == "remove"
    assert CommentAction.TOGGLE.value == "toggle"
    
    print(f"  All enum values verified")
    print(f"  Total actions: {len(CommentAction)}")
    
    print("\n" + "=" * 70)
    print("PASS: CommentAction enum")
    print("=" * 70)


def test_comment_syntax_dataclass():
    """
    Test: CommentSyntax dataclass.
    """
    print("=" * 70)
    print("TEST: CommentSyntax Dataclass")
    print("=" * 70)
    
    syntax = CommentSyntax(
        language="python",
        line_comment="#",
        block_comment_start='"""',
        block_comment_end='"""'
    )
    
    assert syntax.language == "python", "Language eşleşmeli"
    assert syntax.line_comment == "#", "Line comment eşleşmeli"
    
    print(f"  Language: {syntax.language}")
    print(f"  Line comment: {syntax.line_comment}")
    print(f"  Block comment start: {syntax.block_comment_start}")
    
    print("\n" + "=" * 70)
    print("PASS: CommentSyntax dataclass")
    print("=" * 70)


def test_comment_edit_dataclass():
    """
    Test: CommentEdit dataclass.
    """
    print("=" * 70)
    print("TEST: CommentEdit Dataclass")
    print("=" * 70)
    
    edit = CommentEdit(
        start_line=0,
        end_line=1,
        old_text="x = 10",
        new_text="# x = 10",
        action=CommentAction.ADD
    )
    
    assert edit.start_line == 0, "Start line eşleşmeli"
    assert edit.action == CommentAction.ADD, "Action eşleşmeli"
    
    print(f"  Start line: {edit.start_line}")
    print(f"  End line: {edit.end_line}")
    print(f"  Action: {edit.action.value}")
    
    print("\n" + "=" * 70)
    print("PASS: CommentEdit dataclass")
    print("=" * 70)


def test_toggle_comment_result_dataclass():
    """
    Test: ToggleCommentResult dataclass.
    """
    print("=" * 70)
    print("TEST: ToggleCommentResult Dataclass")
    print("=" * 70)
    
    result = ToggleCommentResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.edits, list), "Edits list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Edits: {len(result.edits)}")
    
    print("\n" + "=" * 70)
    print("PASS: ToggleCommentResult dataclass")
    print("=" * 70)


def test_multiple_languages():
    """
    Test: Multiple languages.
    """
    print("=" * 70)
    print("TEST: Multiple Languages")
    print("=" * 70)
    
    engine = ToggleCommentEngine()
    
    # Python
    python_code = "x = 10"
    python_result = engine.toggle_line_comment(python_code, 0, language="python")
    assert python_result.success, "Python toggle başarılı olmalı"
    
    # JavaScript
    js_code = "const x = 10;"
    js_result = engine.toggle_line_comment(js_code, 0, language="javascript")
    assert js_result.success, "JavaScript toggle başarılı olmalı"
    
    # HTML
    html_code = "<div>test</div>"
    html_result = engine.toggle_line_comment(html_code, 0, language="html")
    assert html_result.success, "HTML toggle başarılı olmalı"
    
    print(f"  Python: {python_result.success}")
    print(f"  JavaScript: {js_result.success}")
    print(f"  HTML: {html_result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Multiple languages")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_toggle_line_comment()
        test2 = test_toggle_block_comment()
        test3 = test_comment_selection()
        test4 = test_uncomment_selection()
        test5 = test_smart_toggle()
        test6 = test_add_docstring()
        test7 = test_get_comment_syntax()
        test8 = test_is_commented()
        test9 = test_comment_style_enum()
        test10 = test_comment_action_enum()
        test11 = test_comment_syntax_dataclass()
        test12 = test_comment_edit_dataclass()
        test13 = test_toggle_comment_result_dataclass()
        test14 = test_multiple_languages()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Toggle Line Comment: {'PASS' if test1 else 'FAIL'}")
        print(f"Toggle Block Comment: {'PASS' if test2 else 'FAIL'}")
        print(f"Comment Selection: {'PASS' if test3 else 'FAIL'}")
        print(f"Uncomment Selection: {'PASS' if test4 else 'FAIL'}")
        print(f"Smart Toggle: {'PASS' if test5 else 'FAIL'}")
        print(f"Add Docstring: {'PASS' if test6 else 'FAIL'}")
        print(f"Get Comment Syntax: {'PASS' if test7 else 'FAIL'}")
        print(f"Is Commented: {'PASS' if test8 else 'FAIL'}")
        print(f"CommentStyle Enum: {'PASS' if test9 else 'FAIL'}")
        print(f"CommentAction Enum: {'PASS' if test10 else 'FAIL'}")
        print(f"CommentSyntax Dataclass: {'PASS' if test11 else 'FAIL'}")
        print(f"CommentEdit Dataclass: {'PASS' if test12 else 'FAIL'}")
        print(f"ToggleCommentResult Dataclass: {'PASS' if test13 else 'FAIL'}")
        print(f"Multiple Languages: {'PASS' if test14 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14])
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
