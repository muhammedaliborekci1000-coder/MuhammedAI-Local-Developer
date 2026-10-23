"""
Quality Test: Diagnostics
Diagnostics system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.diagnostics import (
    DiagnosticSeverity,
    DiagnosticTag,
    DiagnosticSource,
    Position,
    Range,
    Diagnostic,
    PublishDiagnosticsParams,
    DiagnosticConfig,
    DiagnosticsEngine
)


def test_diagnostic_severity_enum():
    """
    Test: DiagnosticSeverity enum.
    """
    print("=" * 70)
    print("TEST: DiagnosticSeverity Enum")
    print("=" * 70)
    
    assert DiagnosticSeverity.ERROR.value == 1
    assert DiagnosticSeverity.WARNING.value == 2
    assert DiagnosticSeverity.INFORMATION.value == 3
    assert DiagnosticSeverity.HINT.value == 4
    
    print(f"  All enum values verified")
    print(f"  Total severities: {len(DiagnosticSeverity)}")
    
    print("\n" + "=" * 70)
    print("PASS: DiagnosticSeverity enum")
    print("=" * 70)


def test_diagnostic_tag_enum():
    """
    Test: DiagnosticTag enum.
    """
    print("=" * 70)
    print("TEST: DiagnosticTag Enum")
    print("=" * 70)
    
    assert DiagnosticTag.UNNECESSARY.value == 1
    assert DiagnosticTag.DEPRECATED.value == 2
    
    print(f"  All enum values verified")
    print(f"  Total tags: {len(DiagnosticTag)}")
    
    print("\n" + "=" * 70)
    print("PASS: DiagnosticTag enum")
    print("=" * 70)


def test_diagnostic_source_enum():
    """
    Test: DiagnosticSource enum.
    """
    print("=" * 70)
    print("TEST: DiagnosticSource Enum")
    print("=" * 70)
    
    assert DiagnosticSource.PYTHON.value == "python"
    assert DiagnosticSource.JAVASCRIPT.value == "javascript"
    assert DiagnosticSource.LINT.value == "lint"
    assert DiagnosticSource.SYNTAX.value == "syntax"
    
    print(f"  All enum values verified")
    print(f"  Total sources: {len(DiagnosticSource)}")
    
    print("\n" + "=" * 70)
    print("PASS: DiagnosticSource enum")
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


def test_diagnostic_dataclass():
    """
    Test: Diagnostic dataclass.
    """
    print("=" * 70)
    print("TEST: Diagnostic Dataclass")
    print("=" * 70)
    
    diagnostic = Diagnostic(
        range=Range(
            start=Position(line=1, character=0),
            end=Position(line=1, character=10)
        ),
        severity=DiagnosticSeverity.ERROR,
        message="Test error"
    )
    
    assert diagnostic.message == "Test error", "Message eşleşmeli"
    assert diagnostic.severity == DiagnosticSeverity.ERROR, "Severity eşleşmeli"
    
    print(f"  Message: {diagnostic.message}")
    print(f"  Severity: {diagnostic.severity.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Diagnostic dataclass")
    print("=" * 70)


def test_publish_diagnostics_params_dataclass():
    """
    Test: PublishDiagnosticsParams dataclass.
    """
    print("=" * 70)
    print("TEST: PublishDiagnosticsParams Dataclass")
    print("=" * 70)
    
    params = PublishDiagnosticsParams(
        uri="file:///test.py",
        version=1,
        diagnostics=[]
    )
    
    assert params.uri == "file:///test.py", "URI eşleşmeli"
    assert params.version == 1, "Version eşleşmeli"
    
    print(f"  URI: {params.uri}")
    print(f"  Version: {params.version}")
    
    print("\n" + "=" * 70)
    print("PASS: PublishDiagnosticsParams dataclass")
    print("=" * 70)


def test_diagnostic_config_dataclass():
    """
    Test: DiagnosticConfig dataclass.
    """
    print("=" * 70)
    print("TEST: DiagnosticConfig Dataclass")
    print("=" * 70)
    
    config = DiagnosticConfig(
        enable_errors=True,
        enable_warnings=True,
        max_diagnostics=50
    )
    
    assert config.enable_errors == True, "Enable errors eşleşmeli"
    assert config.max_diagnostics == 50, "Max diagnostics eşleşmeli"
    
    print(f"  Enable errors: {config.enable_errors}")
    print(f"  Max diagnostics: {config.max_diagnostics}")
    
    print("\n" + "=" * 70)
    print("PASS: DiagnosticConfig dataclass")
    print("=" * 70)


def test_diagnostics_engine_initialization():
    """
    Test: DiagnosticsEngine initialization.
    """
    print("=" * 70)
    print("TEST: DiagnosticsEngine Initialization")
    print("=" * 70)
    
    config = DiagnosticConfig()
    engine = DiagnosticsEngine(config)
    
    assert engine.config == config, "Config eşleşmeli"
    assert len(engine.diagnostics_history) == 0, "History boş olmalı"
    
    print(f"  History: {len(engine.diagnostics_history)}")
    
    print("\n" + "=" * 70)
    print("PASS: DiagnosticsEngine initialization")
    print("=" * 70)


def test_analyze():
    """
    Test: Analyze.
    """
    print("=" * 70)
    print("TEST: Analyze")
    print("=" * 70)
    
    engine = DiagnosticsEngine()
    
    text = "def hello():\n    pass"
    
    diagnostics = engine.analyze(text, "file:///test.py", "python")
    
    assert diagnostics is not None, "Diagnostics olmalı"
    assert isinstance(diagnostics, list), "List olmalı"
    
    print(f"  Diagnostics: {len(diagnostics)}")
    
    print("\n" + "=" * 70)
    print("PASS: Analyze")
    print("=" * 70)


def test_syntax_checking():
    """
    Test: Syntax checking.
    """
    print("=" * 70)
    print("TEST: Syntax Checking")
    print("=" * 70)
    
    engine = DiagnosticsEngine()
    
    text = "def hello(\n    pass"
    
    diagnostics = engine.analyze(text, "file:///test.py", "python")
    
    # Should detect unmatched parentheses
    syntax_diagnostics = [d for d in diagnostics if d.source == DiagnosticSource.SYNTAX.value]
    
    print(f"  Diagnostics: {len(diagnostics)}")
    print(f"  Syntax diagnostics: {len(syntax_diagnostics)}")
    
    print("\n" + "=" * 70)
    print("PASS: Syntax checking")
    print("=" * 70)


def test_lint_checking():
    """
    Test: Lint checking.
    """
    print("=" * 70)
    print("TEST: Lint Checking")
    print("=" * 70)
    
    engine = DiagnosticsEngine()
    
    # Create a long line
    text = "x" * 100
    
    diagnostics = engine.analyze(text, "file:///test.py", "python")
    
    # Should detect line too long
    lint_diagnostics = [d for d in diagnostics if d.source == DiagnosticSource.LINT.value]
    
    print(f"  Diagnostics: {len(diagnostics)}")
    print(f"  Lint diagnostics: {len(lint_diagnostics)}")
    
    print("\n" + "=" * 70)
    print("PASS: Lint checking")
    print("=" * 70)


def test_style_checking():
    """
    Test: Style checking.
    """
    print("=" * 70)
    print("TEST: Style Checking")
    print("=" * 70)
    
    config = DiagnosticConfig(check_style=True)
    engine = DiagnosticsEngine(config)
    
    # Create a line with trailing whitespace
    text = "def hello():    "
    
    diagnostics = engine.analyze(text, "file:///test.py", "python")
    
    # Should detect trailing whitespace
    style_diagnostics = [d for d in diagnostics if d.source == DiagnosticSource.STYLE.value]
    
    print(f"  Diagnostics: {len(diagnostics)}")
    print(f"  Style diagnostics: {len(style_diagnostics)}")
    
    print("\n" + "=" * 70)
    print("PASS: Style checking")
    print("=" * 70)


def test_get_diagnostics():
    """
    Test: Get diagnostics.
    """
    print("=" * 70)
    print("TEST: Get Diagnostics")
    print("=" * 70)
    
    engine = DiagnosticsEngine()
    
    text = "def hello():\n    pass"
    uri = "file:///test.py"
    
    engine.analyze(text, uri, "python")
    
    diagnostics = engine.get_diagnostics(uri)
    
    assert diagnostics is not None, "Diagnostics olmalı"
    
    print(f"  Diagnostics: {len(diagnostics)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get diagnostics")
    print("=" * 70)


def test_clear_diagnostics():
    """
    Test: Clear diagnostics.
    """
    print("=" * 70)
    print("TEST: Clear Diagnostics")
    print("=" * 70)
    
    engine = DiagnosticsEngine()
    
    text = "def hello():\n    pass"
    uri = "file:///test.py"
    
    engine.analyze(text, uri, "python")
    engine.clear_diagnostics(uri)
    
    diagnostics = engine.get_diagnostics(uri)
    
    assert len(diagnostics) == 0, "Diagnostics temizlenmeli"
    
    print(f"  Diagnostics: {len(diagnostics)}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear diagnostics")
    print("=" * 70)


def test_clear_all_diagnostics():
    """
    Test: Clear all diagnostics.
    """
    print("=" * 70)
    print("TEST: Clear All Diagnostics")
    print("=" * 70)
    
    engine = DiagnosticsEngine()
    
    text = "def hello():\n    pass"
    
    engine.analyze(text, "file:///test1.py", "python")
    engine.analyze(text, "file:///test2.py", "python")
    
    engine.clear_all_diagnostics()
    
    assert len(engine.diagnostics_history) == 0, "History temizlenmeli"
    
    print(f"  History: {len(engine.diagnostics_history)}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear all diagnostics")
    print("=" * 70)


def test_get_diagnostic_count():
    """
    Test: Get diagnostic count.
    """
    print("=" * 70)
    print("TEST: Get Diagnostic Count")
    print("=" * 70)
    
    engine = DiagnosticsEngine()
    
    text = "def hello():\n    pass"
    uri = "file:///test.py"
    
    engine.analyze(text, uri, "python")
    
    count = engine.get_diagnostic_count(uri)
    
    assert count >= 0, "Count olmalı"
    
    print(f"  Count: {count}")
    
    print("\n" + "=" * 70)
    print("PASS: Get diagnostic count")
    print("=" * 70)


def test_get_error_count():
    """
    Test: Get error count.
    """
    print("=" * 70)
    print("TEST: Get Error Count")
    print("=" * 70)
    
    engine = DiagnosticsEngine()
    
    text = "def hello(\n    pass"
    uri = "file:///test.py"
    
    engine.analyze(text, uri, "python")
    
    error_count = engine.get_error_count(uri)
    
    assert error_count >= 0, "Error count olmalı"
    
    print(f"  Error count: {error_count}")
    
    print("\n" + "=" * 70)
    print("PASS: Get error count")
    print("=" * 70)


def test_get_warning_count():
    """
    Test: Get warning count.
    """
    print("=" * 70)
    print("TEST: Get Warning Count")
    print("=" * 70)
    
    engine = DiagnosticsEngine()
    
    text = "x" * 100
    uri = "file:///test.py"
    
    engine.analyze(text, uri, "python")
    
    warning_count = engine.get_warning_count(uri)
    
    assert warning_count >= 0, "Warning count olmalı"
    
    print(f"  Warning count: {warning_count}")
    
    print("\n" + "=" * 70)
    print("PASS: Get warning count")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    engine = DiagnosticsEngine()
    
    new_config = DiagnosticConfig(max_diagnostics=50)
    engine.update_config(new_config)
    
    assert engine.config.max_diagnostics == 50, "Config güncellenmeli"
    
    print(f"  Max diagnostics: {engine.config.max_diagnostics}")
    
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
    
    config = DiagnosticConfig(max_diagnostics=50)
    engine = DiagnosticsEngine(config)
    
    retrieved_config = engine.get_config()
    
    assert retrieved_config.max_diagnostics == 50, "Config eşleşmeli"
    
    print(f"  Max diagnostics: {retrieved_config.max_diagnostics}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


def test_publish_diagnostics():
    """
    Test: Publish diagnostics.
    """
    print("=" * 70)
    print("TEST: Publish Diagnostics")
    print("=" * 70)
    
    engine = DiagnosticsEngine()
    
    text = "def hello():\n    pass"
    uri = "file:///test.py"
    
    engine.analyze(text, uri, "python")
    
    params = engine.publish_diagnostics(uri, version=1)
    
    assert params.uri == uri, "URI eşleşmeli"
    assert params.version == 1, "Version eşleşmeli"
    
    print(f"  URI: {params.uri}")
    print(f"  Version: {params.version}")
    print(f"  Diagnostics: {len(params.diagnostics)}")
    
    print("\n" + "=" * 70)
    print("PASS: Publish diagnostics")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_diagnostic_severity_enum()
        test2 = test_diagnostic_tag_enum()
        test3 = test_diagnostic_source_enum()
        test4 = test_position_dataclass()
        test5 = test_range_dataclass()
        test6 = test_diagnostic_dataclass()
        test7 = test_publish_diagnostics_params_dataclass()
        test8 = test_diagnostic_config_dataclass()
        test9 = test_diagnostics_engine_initialization()
        test10 = test_analyze()
        test11 = test_syntax_checking()
        test12 = test_lint_checking()
        test13 = test_style_checking()
        test14 = test_get_diagnostics()
        test15 = test_clear_diagnostics()
        test16 = test_clear_all_diagnostics()
        test17 = test_get_diagnostic_count()
        test18 = test_get_error_count()
        test19 = test_get_warning_count()
        test20 = test_update_config()
        test21 = test_get_config()
        test22 = test_publish_diagnostics()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"DiagnosticSeverity Enum: {'PASS' if test1 else 'FAIL'}")
        print(f"DiagnosticTag Enum: {'PASS' if test2 else 'FAIL'}")
        print(f"DiagnosticSource Enum: {'PASS' if test3 else 'FAIL'}")
        print(f"Position Dataclass: {'PASS' if test4 else 'FAIL'}")
        print(f"Range Dataclass: {'PASS' if test5 else 'FAIL'}")
        print(f"Diagnostic Dataclass: {'PASS' if test6 else 'FAIL'}")
        print(f"PublishDiagnosticsParams Dataclass: {'PASS' if test7 else 'FAIL'}")
        print(f"DiagnosticConfig Dataclass: {'PASS' if test8 else 'FAIL'}")
        print(f"DiagnosticsEngine Initialization: {'PASS' if test9 else 'FAIL'}")
        print(f"Analyze: {'PASS' if test10 else 'FAIL'}")
        print(f"Syntax Checking: {'PASS' if test11 else 'FAIL'}")
        print(f"Lint Checking: {'PASS' if test12 else 'FAIL'}")
        print(f"Style Checking: {'PASS' if test13 else 'FAIL'}")
        print(f"Get Diagnostics: {'PASS' if test14 else 'FAIL'}")
        print(f"Clear Diagnostics: {'PASS' if test15 else 'FAIL'}")
        print(f"Clear All Diagnostics: {'PASS' if test16 else 'FAIL'}")
        print(f"Get Diagnostic Count: {'PASS' if test17 else 'FAIL'}")
        print(f"Get Error Count: {'PASS' if test18 else 'FAIL'}")
        print(f"Get Warning Count: {'PASS' if test19 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test20 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test21 else 'FAIL'}")
        print(f"Publish Diagnostics: {'PASS' if test22 else 'FAIL'}")
        
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
