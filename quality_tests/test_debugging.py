"""
Quality Test: Debugging
Debugging system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.debugging import (
    DebugState,
    BreakpointKind,
    StepKind,
    VariableScope,
    Position,
    Range,
    Breakpoint,
    StackFrame,
    Variable,
    WatchExpression,
    DebugSession,
    DebugConfig,
    DebuggingEngine
)


def test_debug_state_enum():
    """
    Test: DebugState enum.
    """
    print("=" * 70)
    print("TEST: DebugState Enum")
    print("=" * 70)
    
    assert DebugState.STOPPED.value == "stopped"
    assert DebugState.RUNNING.value == "running"
    assert DebugState.PAUSED.value == "paused"
    assert DebugState.STEPPING.value == "stepping"
    
    print(f"  All enum values verified")
    print(f"  Total states: {len(DebugState)}")
    
    print("\n" + "=" * 70)
    print("PASS: DebugState enum")
    print("=" * 70)


def test_breakpoint_kind_enum():
    """
    Test: BreakpointKind enum.
    """
    print("=" * 70)
    print("TEST: BreakpointKind Enum")
    print("=" * 70)
    
    assert BreakpointKind.LINE.value == "line"
    assert BreakpointKind.FUNCTION.value == "function"
    assert BreakpointKind.CONDITIONAL.value == "conditional"
    assert BreakpointKind.LOGPOINT.value == "logpoint"
    
    print(f"  All enum values verified")
    print(f"  Total kinds: {len(BreakpointKind)}")
    
    print("\n" + "=" * 70)
    print("PASS: BreakpointKind enum")
    print("=" * 70)


def test_step_kind_enum():
    """
    Test: StepKind enum.
    """
    print("=" * 70)
    print("TEST: StepKind Enum")
    print("=" * 70)
    
    assert StepKind.OVER.value == "over"
    assert StepKind.INTO.value == "into"
    assert StepKind.OUT.value == "out"
    assert StepKind.CONTINUE.value == "continue"
    
    print(f"  All enum values verified")
    print(f"  Total kinds: {len(StepKind)}")
    
    print("\n" + "=" * 70)
    print("PASS: StepKind enum")
    print("=" * 70)


def test_variable_scope_enum():
    """
    Test: VariableScope enum.
    """
    print("=" * 70)
    print("TEST: VariableScope Enum")
    print("=" * 70)
    
    assert VariableScope.LOCAL.value == "local"
    assert VariableScope.GLOBAL.value == "global"
    assert VariableScope.CLOSURE.value == "closure"
    assert VariableScope.THIS.value == "this"
    
    print(f"  All enum values verified")
    print(f"  Total scopes: {len(VariableScope)}")
    
    print("\n" + "=" * 70)
    print("PASS: VariableScope enum")
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


def test_breakpoint_dataclass():
    """
    Test: Breakpoint dataclass.
    """
    print("=" * 70)
    print("TEST: Breakpoint Dataclass")
    print("=" * 70)
    
    breakpoint = Breakpoint(
        id="bp_1",
        kind=BreakpointKind.LINE,
        uri="file:///test.py",
        line=10
    )
    
    assert breakpoint.id == "bp_1", "ID eşleşmeli"
    assert breakpoint.line == 10, "Line eşleşmeli"
    
    print(f"  ID: {breakpoint.id}")
    print(f"  Line: {breakpoint.line}")
    
    print("\n" + "=" * 70)
    print("PASS: Breakpoint dataclass")
    print("=" * 70)


def test_stack_frame_dataclass():
    """
    Test: StackFrame dataclass.
    """
    print("=" * 70)
    print("TEST: StackFrame Dataclass")
    print("=" * 70)
    
    frame = StackFrame(
        id=1,
        name="main",
        uri="file:///test.py",
        line=10,
        column=0
    )
    
    assert frame.name == "main", "Name eşleşmeli"
    assert frame.line == 10, "Line eşleşmeli"
    
    print(f"  Name: {frame.name}")
    print(f"  Line: {frame.line}")
    
    print("\n" + "=" * 70)
    print("PASS: StackFrame dataclass")
    print("=" * 70)


def test_variable_dataclass():
    """
    Test: Variable dataclass.
    """
    print("=" * 70)
    print("TEST: Variable Dataclass")
    print("=" * 70)
    
    variable = Variable(
        name="x",
        value=42,
        type="int",
        scope=VariableScope.LOCAL
    )
    
    assert variable.name == "x", "Name eşleşmeli"
    assert variable.value == 42, "Value eşleşmeli"
    
    print(f"  Name: {variable.name}")
    print(f"  Value: {variable.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Variable dataclass")
    print("=" * 70)


def test_watch_expression_dataclass():
    """
    Test: WatchExpression dataclass.
    """
    print("=" * 70)
    print("TEST: WatchExpression Dataclass")
    print("=" * 70)
    
    watch = WatchExpression(
        id="watch_1",
        expression="x + 1"
    )
    
    assert watch.id == "watch_1", "ID eşleşmeli"
    assert watch.expression == "x + 1", "Expression eşleşmeli"
    
    print(f"  ID: {watch.id}")
    print(f"  Expression: {watch.expression}")
    
    print("\n" + "=" * 70)
    print("PASS: WatchExpression dataclass")
    print("=" * 70)


def test_debug_session_dataclass():
    """
    Test: DebugSession dataclass.
    """
    print("=" * 70)
    print("TEST: DebugSession Dataclass")
    print("=" * 70)
    
    session = DebugSession(
        id="session_1",
        uri="file:///test.py",
        state=DebugState.STOPPED
    )
    
    assert session.id == "session_1", "ID eşleşmeli"
    assert session.state == DebugState.STOPPED, "State eşleşmeli"
    
    print(f"  ID: {session.id}")
    print(f"  State: {session.state.value}")
    
    print("\n" + "=" * 70)
    print("PASS: DebugSession dataclass")
    print("=" * 70)


def test_debug_config_dataclass():
    """
    Test: DebugConfig dataclass.
    """
    print("=" * 70)
    print("TEST: DebugConfig Dataclass")
    print("=" * 70)
    
    config = DebugConfig(
        enable_breakpoints=True,
        auto_continue=False
    )
    
    assert config.enable_breakpoints == True, "Enable breakpoints eşleşmeli"
    assert config.auto_continue == False, "Auto continue eşleşmeli"
    
    print(f"  Enable breakpoints: {config.enable_breakpoints}")
    print(f"  Auto continue: {config.auto_continue}")
    
    print("\n" + "=" * 70)
    print("PASS: DebugConfig dataclass")
    print("=" * 70)


def test_debugging_engine_initialization():
    """
    Test: DebuggingEngine initialization.
    """
    print("=" * 70)
    print("TEST: DebuggingEngine Initialization")
    print("=" * 70)
    
    config = DebugConfig()
    engine = DebuggingEngine(config)
    
    assert engine.config == config, "Config eşleşmeli"
    assert len(engine.sessions) == 0, "Sessions boş olmalı"
    
    print(f"  Sessions: {len(engine.sessions)}")
    
    print("\n" + "=" * 70)
    print("PASS: DebuggingEngine initialization")
    print("=" * 70)


def test_start_session():
    """
    Test: Start session.
    """
    print("=" * 70)
    print("TEST: Start Session")
    print("=" * 70)
    
    engine = DebuggingEngine()
    
    session = engine.start_session("file:///test.py")
    
    assert session is not None, "Session olmalı"
    assert session.state == DebugState.STOPPED, "State STOPPED olmalı"
    
    print(f"  Session ID: {session.id}")
    print(f"  State: {session.state.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Start session")
    print("=" * 70)


def test_stop_session():
    """
    Test: Stop session.
    """
    print("=" * 70)
    print("TEST: Stop Session")
    print("=" * 70)
    
    engine = DebuggingEngine()
    
    session = engine.start_session("file:///test.py")
    engine.stop_session(session.id)
    
    assert session.id not in engine.sessions, "Session silinmeli"
    
    print(f"  Session stopped: {session.id}")
    
    print("\n" + "=" * 70)
    print("PASS: Stop session")
    print("=" * 70)


def test_add_breakpoint():
    """
    Test: Add breakpoint.
    """
    print("=" * 70)
    print("TEST: Add Breakpoint")
    print("=" * 70)
    
    engine = DebuggingEngine()
    
    engine.start_session("file:///test.py")
    breakpoint = engine.add_breakpoint("file:///test.py", 10)
    
    assert breakpoint is not None, "Breakpoint olmalı"
    assert breakpoint.line == 10, "Line eşleşmeli"
    
    print(f"  Breakpoint ID: {breakpoint.id}")
    print(f"  Line: {breakpoint.line}")
    
    print("\n" + "=" * 70)
    print("PASS: Add breakpoint")
    print("=" * 70)


def test_remove_breakpoint():
    """
    Test: Remove breakpoint.
    """
    print("=" * 70)
    print("TEST: Remove Breakpoint")
    print("=" * 70)
    
    engine = DebuggingEngine()
    
    engine.start_session("file:///test.py")
    breakpoint = engine.add_breakpoint("file:///test.py", 10)
    result = engine.remove_breakpoint(breakpoint.id)
    
    assert result == True, "Removal başarılı olmalı"
    
    print(f"  Breakpoint removed: {breakpoint.id}")
    
    print("\n" + "=" * 70)
    print("PASS: Remove breakpoint")
    print("=" * 70)


def test_toggle_breakpoint():
    """
    Test: Toggle breakpoint.
    """
    print("=" * 70)
    print("TEST: Toggle Breakpoint")
    print("=" * 70)
    
    engine = DebuggingEngine()
    
    engine.start_session("file:///test.py")
    breakpoint = engine.add_breakpoint("file:///test.py", 10)
    initial_enabled = breakpoint.enabled
    
    result = engine.toggle_breakpoint(breakpoint.id)
    
    assert result == True, "Toggle başarılı olmalı"
    
    print(f"  Breakpoint toggled: {breakpoint.id}")
    
    print("\n" + "=" * 70)
    print("PASS: Toggle breakpoint")
    print("=" * 70)


def test_step():
    """
    Test: Step execution.
    """
    print("=" * 70)
    print("TEST: Step Execution")
    print("=" * 70)
    
    engine = DebuggingEngine()
    
    engine.start_session("file:///test.py")
    result = engine.step(StepKind.OVER)
    
    assert result == True, "Step başarılı olmalı"
    
    session = engine.get_current_session()
    assert session.state == DebugState.STEPPING, "State STEPPING olmalı"
    
    print(f"  State: {session.state.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Step execution")
    print("=" * 70)


def test_continue_execution():
    """
    Test: Continue execution.
    """
    print("=" * 70)
    print("TEST: Continue Execution")
    print("=" * 70)
    
    engine = DebuggingEngine()
    
    engine.start_session("file:///test.py")
    result = engine.continue_execution()
    
    assert result == True, "Continue başarılı olmalı"
    
    session = engine.get_current_session()
    assert session.state == DebugState.RUNNING, "State RUNNING olmalı"
    
    print(f"  State: {session.state.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Continue execution")
    print("=" * 70)


def test_pause_execution():
    """
    Test: Pause execution.
    """
    print("=" * 70)
    print("TEST: Pause Execution")
    print("=" * 70)
    
    engine = DebuggingEngine()
    
    engine.start_session("file:///test.py")
    result = engine.pause_execution()
    
    assert result == True, "Pause başarılı olmalı"
    
    session = engine.get_current_session()
    assert session.state == DebugState.PAUSED, "State PAUSED olmalı"
    
    print(f"  State: {session.state.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Pause execution")
    print("=" * 70)


def test_add_watch_expression():
    """
    Test: Add watch expression.
    """
    print("=" * 70)
    print("TEST: Add Watch Expression")
    print("=" * 70)
    
    engine = DebuggingEngine()
    
    engine.start_session("file:///test.py")
    watch = engine.add_watch_expression("x + 1")
    
    assert watch is not None, "Watch expression olmalı"
    assert watch.expression == "x + 1", "Expression eşleşmeli"
    
    print(f"  Watch ID: {watch.id}")
    print(f"  Expression: {watch.expression}")
    
    print("\n" + "=" * 70)
    print("PASS: Add watch expression")
    print("=" * 70)


def test_evaluate_expression():
    """
    Test: Evaluate expression.
    """
    print("=" * 70)
    print("TEST: Evaluate Expression")
    print("=" * 70)
    
    engine = DebuggingEngine()
    
    result = engine.evaluate_expression("1 + 1")
    
    assert result is not None, "Result olmalı"
    
    print(f"  Result: {result}")
    
    print("\n" + "=" * 70)
    print("PASS: Evaluate expression")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    engine = DebuggingEngine()
    
    new_config = DebugConfig(auto_continue=True)
    engine.update_config(new_config)
    
    assert engine.config.auto_continue == True, "Config güncellenmeli"
    
    print(f"  Auto continue: {engine.config.auto_continue}")
    
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
    
    config = DebugConfig(auto_continue=True)
    engine = DebuggingEngine(config)
    
    retrieved_config = engine.get_config()
    
    assert retrieved_config.auto_continue == True, "Config eşleşmeli"
    
    print(f"  Auto continue: {retrieved_config.auto_continue}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_debug_state_enum()
        test2 = test_breakpoint_kind_enum()
        test3 = test_step_kind_enum()
        test4 = test_variable_scope_enum()
        test5 = test_position_dataclass()
        test6 = test_range_dataclass()
        test7 = test_breakpoint_dataclass()
        test8 = test_stack_frame_dataclass()
        test9 = test_variable_dataclass()
        test10 = test_watch_expression_dataclass()
        test11 = test_debug_session_dataclass()
        test12 = test_debug_config_dataclass()
        test13 = test_debugging_engine_initialization()
        test14 = test_start_session()
        test15 = test_stop_session()
        test16 = test_add_breakpoint()
        test17 = test_remove_breakpoint()
        test18 = test_toggle_breakpoint()
        test19 = test_step()
        test20 = test_continue_execution()
        test21 = test_pause_execution()
        test22 = test_add_watch_expression()
        test23 = test_evaluate_expression()
        test24 = test_update_config()
        test25 = test_get_config()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"DebugState Enum: {'PASS' if test1 else 'FAIL'}")
        print(f"BreakpointKind Enum: {'PASS' if test2 else 'FAIL'}")
        print(f"StepKind Enum: {'PASS' if test3 else 'FAIL'}")
        print(f"VariableScope Enum: {'PASS' if test4 else 'FAIL'}")
        print(f"Position Dataclass: {'PASS' if test5 else 'FAIL'}")
        print(f"Range Dataclass: {'PASS' if test6 else 'FAIL'}")
        print(f"Breakpoint Dataclass: {'PASS' if test7 else 'FAIL'}")
        print(f"StackFrame Dataclass: {'PASS' if test8 else 'FAIL'}")
        print(f"Variable Dataclass: {'PASS' if test9 else 'FAIL'}")
        print(f"WatchExpression Dataclass: {'PASS' if test10 else 'FAIL'}")
        print(f"DebugSession Dataclass: {'PASS' if test11 else 'FAIL'}")
        print(f"DebugConfig Dataclass: {'PASS' if test12 else 'FAIL'}")
        print(f"DebuggingEngine Initialization: {'PASS' if test13 else 'FAIL'}")
        print(f"Start Session: {'PASS' if test14 else 'FAIL'}")
        print(f"Stop Session: {'PASS' if test15 else 'FAIL'}")
        print(f"Add Breakpoint: {'PASS' if test16 else 'FAIL'}")
        print(f"Remove Breakpoint: {'PASS' if test17 else 'FAIL'}")
        print(f"Toggle Breakpoint: {'PASS' if test18 else 'FAIL'}")
        print(f"Step Execution: {'PASS' if test19 else 'FAIL'}")
        print(f"Continue Execution: {'PASS' if test20 else 'FAIL'}")
        print(f"Pause Execution: {'PASS' if test21 else 'FAIL'}")
        print(f"Add Watch Expression: {'PASS' if test22 else 'FAIL'}")
        print(f"Evaluate Expression: {'PASS' if test23 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test24 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test25 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14, test15, test16, test17, test18, test19, test20, test21, test22, test23, test24, test25])
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
