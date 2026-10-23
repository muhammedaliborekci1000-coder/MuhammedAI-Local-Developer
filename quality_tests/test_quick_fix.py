"""
Quality Test: Quick Fix
Quick fix system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.quick_fix import (
    QuickFixEngine,
    FixKind,
    FixPriority,
    TextEdit,
    CodeAction,
    QuickFixResult
)


def test_get_quick_fixes():
    """
    Test: Get quick fixes.
    """
    print("=" * 70)
    print("TEST: Get Quick Fixes")
    print("=" * 70)
    
    code = """
def my_function():
    x = 42
    return "Hello"
"""
    
    engine = QuickFixEngine()
    result = engine.get_quick_fixes(code, 2, 0, "python")
    
    assert result.success, "Quick fix başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Total actions: {result.total_actions}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Get quick fixes")
    print("=" * 70)


def test_auto_import_fix():
    """
    Test: Auto import fix.
    """
    print("=" * 70)
    print("TEST: Auto Import Fix")
    print("=" * 70)
    
    code = """
def my_function():
    print(os.getcwd())
"""
    
    engine = QuickFixEngine()
    result = engine.get_quick_fixes(code, 1, 0, "python")
    
    assert result.success, "Quick fix başarılı olmalı"
    
    import_fixes = [a for a in result.actions if a.kind == FixKind.AUTO_IMPORT]
    
    print(f"  Success: {result.success}")
    print(f"  Auto import fixes: {len(import_fixes)}")
    
    print("\n" + "=" * 70)
    print("PASS: Auto import fix")
    print("=" * 70)


def test_unused_variable_fix():
    """
    Test: Unused variable fix.
    """
    print("=" * 70)
    print("TEST: Unused Variable Fix")
    print("=" * 70)
    
    code = """
def my_function():
    unused_var = 42
    return "Hello"
"""
    
    engine = QuickFixEngine()
    result = engine.get_quick_fixes(code, 2, 0, "python")
    
    assert result.success, "Quick fix başarılı olmalı"
    
    lint_fixes = [a for a in result.actions if a.kind == FixKind.LINT_FIX]
    
    print(f"  Success: {result.success}")
    print(f"  Lint fixes: {len(lint_fixes)}")
    
    print("\n" + "=" * 70)
    print("PASS: Unused variable fix")
    print("=" * 70)


def test_apply_fix():
    """
    Test: Apply fix.
    """
    print("=" * 70)
    print("TEST: Apply Fix")
    print("=" * 70)
    
    code = "Hello World   "
    
    engine = QuickFixEngine()
    action = CodeAction(
        title="Remove trailing whitespace",
        kind=FixKind.FORMAT_FIX,
        priority=FixPriority.LOW,
        description="Remove trailing whitespace",
        edits=[TextEdit(
            start_line=0,
            start_column=11,
            end_line=0,
            end_column=14,
            new_text=""
        )]
    )
    
    fixed_code, result = engine.apply_fix(code, action)
    
    assert result.success, "Fix uygulanmalı"
    assert fixed_code == "Hello World", "Kod düzeltilmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Fixed code: '{fixed_code}'")
    
    print("\n" + "=" * 70)
    print("PASS: Apply fix")
    print("=" * 70)


def test_apply_all_fixes():
    """
    Test: Apply all fixes.
    """
    print("=" * 70)
    print("TEST: Apply All Fixes")
    print("=" * 70)
    
    code = "Hello World   "
    
    engine = QuickFixEngine()
    action = CodeAction(
        title="Remove trailing whitespace",
        kind=FixKind.FORMAT_FIX,
        priority=FixPriority.LOW,
        description="Remove trailing whitespace",
        edits=[TextEdit(
            start_line=0,
            start_column=11,
            end_line=0,
            end_column=14,
            new_text=""
        )]
    )
    
    fixed_code, result = engine.apply_all_fixes(code, [action])
    
    assert result.success, "Fix'ler uygulanmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Applied fixes: {result.applied_fixes}")
    
    print("\n" + "=" * 70)
    print("PASS: Apply all fixes")
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
    x = 42
    return "Hello"
"""
    
    engine = QuickFixEngine()
    engine.get_quick_fixes(code, 2, 0, "python")
    
    lint_fixes = engine.filter_by_kind(FixKind.LINT_FIX)
    
    print(f"  Lint fixes: {len(lint_fixes)}")
    
    print("\n" + "=" * 70)
    print("PASS: Filter by kind")
    print("=" * 70)


def test_filter_by_priority():
    """
    Test: Filter by priority.
    """
    print("=" * 70)
    print("TEST: Filter by Priority")
    print("=" * 70)
    
    code = """
def my_function():
    x = 42
    return "Hello"
"""
    
    engine = QuickFixEngine()
    engine.get_quick_fixes(code, 2, 0, "python")
    
    high_priority = engine.filter_by_priority(FixPriority.HIGH)
    
    print(f"  High priority fixes: {len(high_priority)}")
    
    print("\n" + "=" * 70)
    print("PASS: Filter by priority")
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
    x = 42
    return "Hello"
"""
    
    engine = QuickFixEngine()
    engine.get_quick_fixes(code, 2, 0, "python")
    
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
    
    engine = QuickFixEngine()
    
    action = engine.add_custom_action(
        title="Custom fix",
        kind=FixKind.REFACTOR,
        priority=FixPriority.MEDIUM,
        description="Custom fix description",
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
    
    engine = QuickFixEngine()
    
    # Action ekle
    engine.add_custom_action(
        title="Custom fix",
        kind=FixKind.REFACTOR,
        priority=FixPriority.MEDIUM,
        description="Custom fix",
        edits=[]
    )
    
    # Temizle
    engine.clear_actions()
    
    assert len(engine.current_actions) == 0, "Action'lar temizlenmeli"
    
    print(f"  Actions cleared: {len(engine.current_actions) == 0}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear actions")
    print("=" * 70)


def test_fix_kind_enum():
    """
    Test: FixKind enum.
    """
    print("=" * 70)
    print("TEST: FixKind Enum")
    print("=" * 70)
    
    assert FixKind.AUTO_IMPORT.value == "auto_import"
    assert FixKind.SYNTAX_FIX.value == "syntax_fix"
    assert FixKind.FORMAT_FIX.value == "format_fix"
    assert FixKind.REFACTOR.value == "refactor"
    assert FixKind.TYPE_FIX.value == "type_fix"
    assert FixKind.LINT_FIX.value == "lint_fix"
    assert FixKind.OPTIMIZATION.value == "optimization"
    assert FixKind.DOCUMENTATION.value == "documentation"
    
    print(f"  All enum values verified")
    print(f"  Total kinds: {len(FixKind)}")
    
    print("\n" + "=" * 70)
    print("PASS: FixKind enum")
    print("=" * 70)


def test_fix_priority_enum():
    """
    Test: FixPriority enum.
    """
    print("=" * 70)
    print("TEST: FixPriority Enum")
    print("=" * 70)
    
    assert FixPriority.LOW.value == "low"
    assert FixPriority.MEDIUM.value == "medium"
    assert FixPriority.HIGH.value == "high"
    assert FixPriority.CRITICAL.value == "critical"
    
    print(f"  All enum values verified")
    print(f"  Total priorities: {len(FixPriority)}")
    
    print("\n" + "=" * 70)
    print("PASS: FixPriority enum")
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
        title="Fix syntax",
        kind=FixKind.SYNTAX_FIX,
        priority=FixPriority.HIGH,
        description="Fix syntax error"
    )
    
    assert action.title == "Fix syntax", "Title eşleşmeli"
    assert action.kind == FixKind.SYNTAX_FIX, "Kind eşleşmeli"
    
    print(f"  Title: {action.title}")
    print(f"  Kind: {action.kind.value}")
    print(f"  Priority: {action.priority.value}")
    
    print("\n" + "=" * 70)
    print("PASS: CodeAction dataclass")
    print("=" * 70)


def test_quick_fix_result_dataclass():
    """
    Test: QuickFixResult dataclass.
    """
    print("=" * 70)
    print("TEST: QuickFixResult Dataclass")
    print("=" * 70)
    
    result = QuickFixResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.actions, list), "Actions list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Actions: {len(result.actions)}")
    
    print("\n" + "=" * 70)
    print("PASS: QuickFixResult dataclass")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_get_quick_fixes()
        test2 = test_auto_import_fix()
        test3 = test_unused_variable_fix()
        test4 = test_apply_fix()
        test5 = test_apply_all_fixes()
        test6 = test_filter_by_kind()
        test7 = test_filter_by_priority()
        test8 = test_get_preferred_actions()
        test9 = test_add_custom_action()
        test10 = test_clear_actions()
        test11 = test_fix_kind_enum()
        test12 = test_fix_priority_enum()
        test13 = test_text_edit_dataclass()
        test14 = test_code_action_dataclass()
        test15 = test_quick_fix_result_dataclass()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Get Quick Fixes: {'PASS' if test1 else 'FAIL'}")
        print(f"Auto Import Fix: {'PASS' if test2 else 'FAIL'}")
        print(f"Unused Variable Fix: {'PASS' if test3 else 'FAIL'}")
        print(f"Apply Fix: {'PASS' if test4 else 'FAIL'}")
        print(f"Apply All Fixes: {'PASS' if test5 else 'FAIL'}")
        print(f"Filter by Kind: {'PASS' if test6 else 'FAIL'}")
        print(f"Filter by Priority: {'PASS' if test7 else 'FAIL'}")
        print(f"Get Preferred Actions: {'PASS' if test8 else 'FAIL'}")
        print(f"Add Custom Action: {'PASS' if test9 else 'FAIL'}")
        print(f"Clear Actions: {'PASS' if test10 else 'FAIL'}")
        print(f"FixKind Enum: {'PASS' if test11 else 'FAIL'}")
        print(f"FixPriority Enum: {'PASS' if test12 else 'FAIL'}")
        print(f"TextEdit Dataclass: {'PASS' if test13 else 'FAIL'}")
        print(f"CodeAction Dataclass: {'PASS' if test14 else 'FAIL'}")
        print(f"QuickFixResult Dataclass: {'PASS' if test15 else 'FAIL'}")
        
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
