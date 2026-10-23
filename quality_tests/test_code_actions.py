"""
Quality Test: Code Actions
Code actions system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.code_actions import (
    CodeActionsEngine,
    ActionKind,
    ActionScope,
    TextEdit,
    CodeAction,
    CodeActionResult
)


def test_get_code_actions():
    """
    Test: Get code actions.
    """
    print("=" * 70)
    print("TEST: Get Code Actions")
    print("=" * 70)
    
    code = """
def my_function():
    x = 42
    return x
"""
    
    engine = CodeActionsEngine()
    result = engine.get_code_actions(code, 1, 3, "python")
    
    assert result.success, "Code actions başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Total actions: {result.total_actions}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Get code actions")
    print("=" * 70)


def test_extract_function_action():
    """
    Test: Extract function action.
    """
    print("=" * 70)
    print("TEST: Extract Function Action")
    print("=" * 70)
    
    code = """
x = 1
y = 2
z = x + y
"""
    
    engine = CodeActionsEngine()
    result = engine.get_code_actions(code, 0, 2, "python")
    
    assert result.success, "Code actions başarılı olmalı"
    
    extract_actions = [a for a in result.actions if a.kind == ActionKind.EXTRACT]
    
    print(f"  Success: {result.success}")
    print(f"  Extract actions: {len(extract_actions)}")
    
    print("\n" + "=" * 70)
    print("PASS: Extract function action")
    print("=" * 70)


def test_generate_docstring_action():
    """
    Test: Generate docstring action.
    """
    print("=" * 70)
    print("TEST: Generate Docstring Action")
    print("=" * 70)
    
    code = """
def my_function():
    return "Hello"
"""
    
    engine = CodeActionsEngine()
    result = engine.get_code_actions(code, 1, 1, "python")
    
    assert result.success, "Code actions başarılı olmalı"
    
    generate_actions = [a for a in result.actions if a.kind == ActionKind.GENERATE]
    
    print(f"  Success: {result.success}")
    print(f"  Generate actions: {len(generate_actions)}")
    
    print("\n" + "=" * 70)
    print("PASS: Generate docstring action")
    print("=" * 70)


def test_organize_imports_action():
    """
    Test: Organize imports action.
    """
    print("=" * 70)
    print("TEST: Organize Imports Action")
    print("=" * 70)
    
    code = """
import os
import sys
def my_function():
    return "Hello"
"""
    
    engine = CodeActionsEngine()
    result = engine.get_code_actions(code, 0, 4, "python")
    
    assert result.success, "Code actions başarılı olmalı"
    
    organize_actions = [a for a in result.actions if a.kind == ActionKind.ORGANIZE]
    
    print(f"  Success: {result.success}")
    print(f"  Organize actions: {len(organize_actions)}")
    
    print("\n" + "=" * 70)
    print("PASS: Organize imports action")
    print("=" * 70)


def test_apply_action():
    """
    Test: Apply action.
    """
    print("=" * 70)
    print("TEST: Apply Action")
    print("=" * 70)
    
    code = "Hello World"
    
    engine = CodeActionsEngine()
    action = CodeAction(
        title="Add text",
        kind=ActionKind.FORMAT,
        scope=ActionScope.FILE,
        description="Add text",
        edits=[TextEdit(
            start_line=0,
            start_column=5,
            end_line=0,
            end_column=5,
            new_text=" Beautiful"
        )]
    )
    
    fixed_code, result = engine.apply_action(code, action)
    
    assert result.success, "Action uygulanmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Fixed code: '{fixed_code}'")
    
    print("\n" + "=" * 70)
    print("PASS: Apply action")
    print("=" * 70)


def test_apply_multiple_actions():
    """
    Test: Apply multiple actions.
    """
    print("=" * 70)
    print("TEST: Apply Multiple Actions")
    print("=" * 70)
    
    code = "Hello"
    
    engine = CodeActionsEngine()
    action1 = CodeAction(
        title="Add text 1",
        kind=ActionKind.FORMAT,
        scope=ActionScope.FILE,
        description="Add text 1",
        edits=[TextEdit(
            start_line=0,
            start_column=5,
            end_line=0,
            end_column=5,
            new_text=" World"
        )]
    )
    
    action2 = CodeAction(
        title="Add text 2",
        kind=ActionKind.FORMAT,
        scope=ActionScope.FILE,
        description="Add text 2",
        edits=[TextEdit(
            start_line=0,
            start_column=11,
            end_line=0,
            end_column=11,
            new_text="!"
        )]
    )
    
    fixed_code, result = engine.apply_multiple_actions(code, [action1, action2])
    
    assert result.success, "Action'lar uygulanmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Applied actions: {result.applied_actions}")
    print(f"  Fixed code: '{fixed_code}'")
    
    print("\n" + "=" * 70)
    print("PASS: Apply multiple actions")
    print("=" * 70)


def test_filter_by_kind():
    """
    Test: Filter by kind.
    """
    print("=" * 70)
    print("TEST: Filter by Kind")
    print("=" * 70)
    
    code = """
def my_function():
    return "Hello"
"""
    
    engine = CodeActionsEngine()
    engine.get_code_actions(code, 1, 1, "python")
    
    format_actions = engine.filter_by_kind(ActionKind.FORMAT)
    
    print(f"  Format actions: {len(format_actions)}")
    
    print("\n" + "=" * 70)
    print("PASS: Filter by kind")
    print("=" * 70)


def test_filter_by_scope():
    """
    Test: Filter by scope.
    """
    print("=" * 70)
    print("TEST: Filter by Scope")
    print("=" * 70)
    
    code = """
def my_function():
    return "Hello"
"""
    
    engine = CodeActionsEngine()
    engine.get_code_actions(code, 1, 1, "python")
    
    file_actions = engine.filter_by_scope(ActionScope.FILE)
    
    print(f"  File actions: {len(file_actions)}")
    
    print("\n" + "=" * 70)
    print("PASS: Filter by scope")
    print("=" * 70)


def test_get_preferred_actions():
    """
    Test: Get preferred actions.
    """
    print("=" * 70)
    print("TEST: Get Preferred Actions")
    print("=" * 70)
    
    code = """
def my_function():
    return "Hello"
"""
    
    engine = CodeActionsEngine()
    engine.get_code_actions(code, 1, 1, "python")
    
    preferred = engine.get_preferred_actions()
    
    print(f"  Preferred actions: {len(preferred)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get preferred actions")
    print("=" * 70)


def test_add_custom_action():
    """
    Test: Add custom action.
    """
    print("=" * 70)
    print("TEST: Add Custom Action")
    print("=" * 70)
    
    engine = CodeActionsEngine()
    
    action = engine.add_custom_action(
        title="Custom action",
        kind=ActionKind.REFACTOR,
        scope=ActionScope.FILE,
        description="Custom action description",
        edits=[],
        is_preferred=True
    )
    
    assert action is not None, "Action oluşturulmalı"
    assert len(engine.current_actions) > 0, "Action listeye eklenmeli"
    
    print(f"  Action created: {action is not None}")
    print(f"  Total actions: {len(engine.current_actions)}")
    
    print("\n" + "=" * 70)
    print("PASS: Add custom action")
    print("=" * 70)


def test_clear_actions():
    """
    Test: Clear actions.
    """
    print("=" * 70)
    print("TEST: Clear Actions")
    print("=" * 70)
    
    engine = CodeActionsEngine()
    
    # Action ekle
    engine.add_custom_action(
        title="Custom action",
        kind=ActionKind.REFACTOR,
        scope=ActionScope.FILE,
        description="Custom action",
        edits=[]
    )
    
    # Temizle
    engine.clear_actions()
    
    assert len(engine.current_actions) == 0, "Action'lar temizlenmeli"
    
    print(f"  Actions cleared: {len(engine.current_actions) == 0}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear actions")
    print("=" * 70)


def test_action_kind_enum():
    """
    Test: ActionKind enum.
    """
    print("=" * 70)
    print("TEST: ActionKind Enum")
    print("=" * 70)
    
    assert ActionKind.REFACTOR.value == "refactor"
    assert ActionKind.EXTRACT.value == "extract"
    assert ActionKind.INLINE.value == "inline"
    assert ActionKind.RENAME.value == "rename"
    assert ActionKind.GENERATE.value == "generate"
    assert ActionKind.FORMAT.value == "format"
    assert ActionKind.ORGANIZE.value == "organize"
    assert ActionKind.MOVE.value == "move"
    assert ActionKind.QUICK_FIX.value == "quick_fix"
    
    print(f"  All enum values verified")
    print(f"  Total kinds: {len(ActionKind)}")
    
    print("\n" + "=" * 70)
    print("PASS: ActionKind enum")
    print("=" * 70)


def test_action_scope_enum():
    """
    Test: ActionScope enum.
    """
    print("=" * 70)
    print("TEST: ActionScope Enum")
    print("=" * 70)
    
    assert ActionScope.SELECTION.value == "selection"
    assert ActionScope.LINE.value == "line"
    assert ActionScope.FUNCTION.value == "function"
    assert ActionScope.CLASS.value == "class"
    assert ActionScope.FILE.value == "file"
    assert ActionScope.PROJECT.value == "project"
    
    print(f"  All enum values verified")
    print(f"  Total scopes: {len(ActionScope)}")
    
    print("\n" + "=" * 70)
    print("PASS: ActionScope enum")
    print("=" * 70)


def test_text_edit_dataclass():
    """
    Test: TextEdit dataclass.
    """
    print("=" * 70)
    print("TEST: TextEdit Dataclass")
    print("=" * 70)
    
    edit = TextEdit(
        start_line=0,
        start_column=0,
        end_line=0,
        end_column=5,
        new_text="Hello"
    )
    
    assert edit.start_line == 0, "Start line eşleşmeli"
    assert edit.new_text == "Hello", "New text eşleşmeli"
    
    print(f"  Start line: {edit.start_line}")
    print(f"  New text: {edit.new_text}")
    
    print("\n" + "=" * 70)
    print("PASS: TextEdit dataclass")
    print("=" * 70)


def test_code_action_dataclass():
    """
    Test: CodeAction dataclass.
    """
    print("=" * 70)
    print("TEST: CodeAction Dataclass")
    print("=" * 70)
    
    action = CodeAction(
        title="Refactor",
        kind=ActionKind.REFACTOR,
        scope=ActionScope.FILE,
        description="Refactor code"
    )
    
    assert action.title == "Refactor", "Title eşleşmeli"
    assert action.kind == ActionKind.REFACTOR, "Kind eşleşmeli"
    
    print(f"  Title: {action.title}")
    print(f"  Kind: {action.kind.value}")
    print(f"  Scope: {action.scope.value}")
    
    print("\n" + "=" * 70)
    print("PASS: CodeAction dataclass")
    print("=" * 70)


def test_code_action_result_dataclass():
    """
    Test: CodeActionResult dataclass.
    """
    print("=" * 70)
    print("TEST: CodeActionResult Dataclass")
    print("=" * 70)
    
    result = CodeActionResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.actions, list), "Actions list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Actions: {len(result.actions)}")
    
    print("\n" + "=" * 70)
    print("PASS: CodeActionResult dataclass")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_get_code_actions()
        test2 = test_extract_function_action()
        test3 = test_generate_docstring_action()
        test4 = test_organize_imports_action()
        test5 = test_apply_action()
        test6 = test_apply_multiple_actions()
        test7 = test_filter_by_kind()
        test8 = test_filter_by_scope()
        test9 = test_get_preferred_actions()
        test10 = test_add_custom_action()
        test11 = test_clear_actions()
        test12 = test_action_kind_enum()
        test13 = test_action_scope_enum()
        test14 = test_text_edit_dataclass()
        test15 = test_code_action_dataclass()
        test16 = test_code_action_result_dataclass()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Get Code Actions: {'PASS' if test1 else 'FAIL'}")
        print(f"Extract Function Action: {'PASS' if test2 else 'FAIL'}")
        print(f"Generate Docstring Action: {'PASS' if test3 else 'FAIL'}")
        print(f"Organize Imports Action: {'PASS' if test4 else 'FAIL'}")
        print(f"Apply Action: {'PASS' if test5 else 'FAIL'}")
        print(f"Apply Multiple Actions: {'PASS' if test6 else 'FAIL'}")
        print(f"Filter by Kind: {'PASS' if test7 else 'FAIL'}")
        print(f"Filter by Scope: {'PASS' if test8 else 'FAIL'}")
        print(f"Get Preferred Actions: {'PASS' if test9 else 'FAIL'}")
        print(f"Add Custom Action: {'PASS' if test10 else 'FAIL'}")
        print(f"Clear Actions: {'PASS' if test11 else 'FAIL'}")
        print(f"ActionKind Enum: {'PASS' if test12 else 'FAIL'}")
        print(f"ActionScope Enum: {'PASS' if test13 else 'FAIL'}")
        print(f"TextEdit Dataclass: {'PASS' if test14 else 'FAIL'}")
        print(f"CodeAction Dataclass: {'PASS' if test15 else 'FAIL'}")
        print(f"CodeActionResult Dataclass: {'PASS' if test16 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14, test15, test16])
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
