"""
Quality Test: Code Explanation (Editor)
Code explanation system testleri for editor module.
"""

import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from app.editor.code_explanation import (
    ExplanationType,
    ExplanationFormat,
    ExplanationRange,
    CodeExplanation,
    ExplanationConfig,
    ExplanationResult,
    CodeExplanationManager
)


def test_explanation_type_enum():
    """
    Test: ExplanationType enum.
    """
    print("=" * 70)
    print("TEST: ExplanationType Enum")
    print("=" * 70)
    
    assert ExplanationType.FUNCTION.value == "function"
    assert ExplanationType.CLASS.value == "class"
    assert ExplanationType.VARIABLE.value == "variable"
    assert ExplanationType.MODULE.value == "module"
    assert ExplanationType.LINE.value == "line"
    assert ExplanationType.BLOCK.value == "block"
    assert ExplanationType.CUSTOM.value == "custom"
    
    print(f"  All enum values verified")
    print(f"  Total types: {len(ExplanationType)}")
    
    print("\n" + "=" * 70)
    print("PASS: ExplanationType enum")
    print("=" * 70)


def test_explanation_format_enum():
    """
    Test: ExplanationFormat enum.
    """
    print("=" * 70)
    print("TEST: ExplanationFormat Enum")
    print("=" * 70)
    
    assert ExplanationFormat.PLAIN_TEXT.value == "plain_text"
    assert ExplanationFormat.MARKDOWN.value == "markdown"
    assert ExplanationFormat.HTML.value == "html"
    assert ExplanationFormat.RICH_TEXT.value == "rich_text"
    
    print(f"  All enum values verified")
    print(f"  Total formats: {len(ExplanationFormat)}")
    
    print("\n" + "=" * 70)
    print("PASS: ExplanationFormat enum")
    print("=" * 70)


def test_explanation_range_dataclass():
    """
    Test: ExplanationRange dataclass.
    """
    print("=" * 70)
    print("TEST: ExplanationRange Dataclass")
    print("=" * 70)
    
    range = ExplanationRange(
        start_line=0,
        start_column=0,
        end_line=10,
        end_column=20
    )
    
    assert range.start_line == 0, "Start line eşleşmeli"
    assert range.start_column == 0, "Start column eşleşmeli"
    assert range.end_line == 10, "End line eşleşmeli"
    assert range.end_column == 20, "End column eşleşmeli"
    
    print(f"  Start: ({range.start_line}, {range.start_column})")
    print(f"  End: ({range.end_line}, {range.end_column})")
    
    print("\n" + "=" * 70)
    print("PASS: ExplanationRange dataclass")
    print("=" * 70)


def test_code_explanation_dataclass():
    """
    Test: CodeExplanation dataclass.
    """
    print("=" * 70)
    print("TEST: CodeExplanation Dataclass")
    print("=" * 70)
    
    range = ExplanationRange(0, 0, 10, 0)
    explanation = CodeExplanation(
        id="explanation_1",
        type=ExplanationType.FUNCTION,
        range=range,
        text="This function does X"
    )
    
    assert explanation.id == "explanation_1", "ID eşleşmeli"
    assert explanation.type == ExplanationType.FUNCTION, "Type eşleşmeli"
    assert explanation.text == "This function does X", "Text eşleşmeli"
    
    print(f"  ID: {explanation.id}")
    print(f"  Type: {explanation.type.value}")
    print(f"  Text: {explanation.text}")
    
    print("\n" + "=" * 70)
    print("PASS: CodeExplanation dataclass")
    print("=" * 70)


def test_explanation_config_dataclass():
    """
    Test: ExplanationConfig dataclass.
    """
    print("=" * 70)
    print("TEST: ExplanationConfig Dataclass")
    print("=" * 70)
    
    config = ExplanationConfig(
        enabled=True,
        format=ExplanationFormat.MARKDOWN
    )
    
    assert config.enabled == True, "Enabled eşleşmeli"
    assert config.format == ExplanationFormat.MARKDOWN, "Format eşleşmeli"
    
    print(f"  Enabled: {config.enabled}")
    print(f"  Format: {config.format.value}")
    
    print("\n" + "=" * 70)
    print("PASS: ExplanationConfig dataclass")
    print("=" * 70)


def test_explanation_result_dataclass():
    """
    Test: ExplanationResult dataclass.
    """
    print("=" * 70)
    print("TEST: ExplanationResult Dataclass")
    print("=" * 70)
    
    result = ExplanationResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.explanations, list), "Explanations list olmalı"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Explanations: {len(result.explanations)}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: ExplanationResult dataclass")
    print("=" * 70)


def test_code_explanation_manager_initialization():
    """
    Test: CodeExplanationManager initialization.
    """
    print("=" * 70)
    print("TEST: CodeExplanationManager Initialization")
    print("=" * 70)
    
    config = ExplanationConfig()
    manager = CodeExplanationManager(config)
    
    assert manager.config == config, "Config eşleşmeli"
    assert len(manager.explanations) == 0, "Explanations boş olmalı"
    assert manager.cache == {}, "Cache boş olmalı"
    
    print(f"  Explanations: {len(manager.explanations)}")
    print(f"  Cache: {len(manager.cache)}")
    
    print("\n" + "=" * 70)
    print("PASS: CodeExplanationManager initialization")
    print("=" * 70)


def test_add_explanation():
    """
    Test: Add explanation.
    """
    print("=" * 70)
    print("TEST: Add Explanation")
    print("=" * 70)
    
    manager = CodeExplanationManager()
    
    range = ExplanationRange(0, 0, 10, 0)
    explanation = CodeExplanation(
        id="",
        type=ExplanationType.FUNCTION,
        range=range,
        text="This function does X"
    )
    
    result = manager.add_explanation(explanation)
    
    assert result.success == True, "Ekleme başarılı olmalı"
    assert len(manager.explanations) > 0, "Explanation eklenmeli"
    
    print(f"  Explanation added: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add explanation")
    print("=" * 70)


def test_remove_explanation():
    """
    Test: Remove explanation.
    """
    print("=" * 70)
    print("TEST: Remove Explanation")
    print("=" * 70)
    
    manager = CodeExplanationManager()
    
    range = ExplanationRange(0, 0, 10, 0)
    explanation = CodeExplanation(
        id="",
        type=ExplanationType.FUNCTION,
        range=range,
        text="This function does X"
    )
    
    result = manager.add_explanation(explanation)
    explanation_id = result.explanation.id
    
    result = manager.remove_explanation(explanation_id)
    
    assert result.success == True, "Kaldırma başarılı olmalı"
    assert explanation_id not in manager.explanations, "Explanation silinmeli"
    
    print(f"  Explanation removed: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Remove explanation")
    print("=" * 70)


def test_get_explanation():
    """
    Test: Get explanation.
    """
    print("=" * 70)
    print("TEST: Get Explanation")
    print("=" * 70)
    
    manager = CodeExplanationManager()
    
    range = ExplanationRange(0, 0, 10, 0)
    explanation = CodeExplanation(
        id="",
        type=ExplanationType.FUNCTION,
        range=range,
        text="This function does X"
    )
    
    result = manager.add_explanation(explanation)
    explanation_id = result.explanation.id
    
    retrieved_explanation = manager.get_explanation(explanation_id)
    
    assert retrieved_explanation is not None, "Explanation bulunmalı"
    assert retrieved_explanation.id == explanation_id, "ID eşleşmeli"
    
    print(f"  Explanation: {retrieved_explanation.text}")
    
    print("\n" + "=" * 70)
    print("PASS: Get explanation")
    print("=" * 70)


def test_get_all_explanations():
    """
    Test: Get all explanations.
    """
    print("=" * 70)
    print("TEST: Get All Explanations")
    print("=" * 70)
    
    manager = CodeExplanationManager()
    
    range = ExplanationRange(0, 0, 10, 0)
    explanation = CodeExplanation(
        id="",
        type=ExplanationType.FUNCTION,
        range=range,
        text="This function does X"
    )
    
    manager.add_explanation(explanation)
    explanations = manager.get_all_explanations()
    
    assert len(explanations) > 0, "Explanations olmalı"
    
    print(f"  Total explanations: {len(explanations)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get all explanations")
    print("=" * 70)


def test_get_explanations_by_type():
    """
    Test: Get explanations by type.
    """
    print("=" * 70)
    print("TEST: Get Explanations by Type")
    print("=" * 70)
    
    manager = CodeExplanationManager()
    
    range = ExplanationRange(0, 0, 10, 0)
    explanation = CodeExplanation(
        id="",
        type=ExplanationType.FUNCTION,
        range=range,
        text="This function does X"
    )
    
    manager.add_explanation(explanation)
    explanations = manager.get_explanations_by_type(ExplanationType.FUNCTION)
    
    assert len(explanations) > 0, "Function explanations olmalı"
    
    print(f"  Function explanations: {len(explanations)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get explanations by type")
    print("=" * 70)


def test_add_function_explanation():
    """
    Test: Add function explanation.
    """
    print("=" * 70)
    print("TEST: Add Function Explanation")
    print("=" * 70)
    
    manager = CodeExplanationManager()
    
    range = ExplanationRange(0, 0, 10, 0)
    result = manager.add_function_explanation(range, "This function does X", 0.8)
    
    assert result.success == True, "Function explanation başarılı olmalı"
    
    print(f"  Function explanation: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add function explanation")
    print("=" * 70)


def test_add_class_explanation():
    """
    Test: Add class explanation.
    """
    print("=" * 70)
    print("TEST: Add Class Explanation")
    print("=" * 70)
    
    manager = CodeExplanationManager()
    
    range = ExplanationRange(0, 0, 10, 0)
    result = manager.add_class_explanation(range, "This class represents X", 0.8)
    
    assert result.success == True, "Class explanation başarılı olmalı"
    
    print(f"  Class explanation: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add class explanation")
    print("=" * 70)


def test_add_variable_explanation():
    """
    Test: Add variable explanation.
    """
    print("=" * 70)
    print("TEST: Add Variable Explanation")
    print("=" * 70)
    
    manager = CodeExplanationManager()
    
    range = ExplanationRange(0, 0, 0, 10)
    result = manager.add_variable_explanation(range, "This variable holds X", 0.7)
    
    assert result.success == True, "Variable explanation başarılı olmalı"
    
    print(f"  Variable explanation: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add variable explanation")
    print("=" * 70)


def test_add_module_explanation():
    """
    Test: Add module explanation.
    """
    print("=" * 70)
    print("TEST: Add Module Explanation")
    print("=" * 70)
    
    manager = CodeExplanationManager()
    
    range = ExplanationRange(0, 0, 100, 0)
    result = manager.add_module_explanation(range, "This module provides X", 0.8)
    
    assert result.success == True, "Module explanation başarılı olmalı"
    
    print(f"  Module explanation: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add module explanation")
    print("=" * 70)


def test_add_line_explanation():
    """
    Test: Add line explanation.
    """
    print("=" * 70)
    print("TEST: Add Line Explanation")
    print("=" * 70)
    
    manager = CodeExplanationManager()
    
    range = ExplanationRange(5, 0, 5, 20)
    result = manager.add_line_explanation(range, "This line does X", 0.6)
    
    assert result.success == True, "Line explanation başarılı olmalı"
    
    print(f"  Line explanation: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add line explanation")
    print("=" * 70)


def test_add_block_explanation():
    """
    Test: Add block explanation.
    """
    print("=" * 70)
    print("TEST: Add Block Explanation")
    print("=" * 70)
    
    manager = CodeExplanationManager()
    
    range = ExplanationRange(0, 0, 10, 0)
    result = manager.add_block_explanation(range, "This block does X", 0.7)
    
    assert result.success == True, "Block explanation başarılı olmalı"
    
    print(f"  Block explanation: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add block explanation")
    print("=" * 70)


def test_filter_by_confidence():
    """
    Test: Filter by confidence.
    """
    print("=" * 70)
    print("TEST: Filter by Confidence")
    print("=" * 70)
    
    manager = CodeExplanationManager()
    
    range = ExplanationRange(0, 0, 10, 0)
    manager.add_function_explanation(range, "text1", 0.9)
    manager.add_function_explanation(range, "text2", 0.5)
    
    filtered = manager.filter_by_confidence(0.7)
    
    assert len(filtered) > 0, "Filtered explanations olmalı"
    
    print(f"  Filtered explanations: {len(filtered)}")
    
    print("\n" + "=" * 70)
    print("PASS: Filter by confidence")
    print("=" * 70)


def test_get_explanations_at_line():
    """
    Test: Get explanations at line.
    """
    print("=" * 70)
    print("TEST: Get Explanations at Line")
    print("=" * 70)
    
    manager = CodeExplanationManager()
    
    range = ExplanationRange(0, 0, 10, 0)
    manager.add_function_explanation(range, "text", 0.8)
    
    explanations = manager.get_explanations_at_line(5)
    
    assert len(explanations) > 0, "Line 5 explanations olmalı"
    
    print(f"  Line 5 explanations: {len(explanations)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get explanations at line")
    print("=" * 70)


def test_clear_explanations():
    """
    Test: Clear explanations.
    """
    print("=" * 70)
    print("TEST: Clear Explanations")
    print("=" * 70)
    
    manager = CodeExplanationManager()
    
    range = ExplanationRange(0, 0, 10, 0)
    manager.add_function_explanation(range, "text", 0.8)
    
    result = manager.clear_explanations()
    
    assert result.success == True, "Clear başarılı olmalı"
    assert len(manager.explanations) == 0, "Explanations temizlenmeli"
    
    print(f"  Cleared: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear explanations")
    print("=" * 70)


def test_clear_explanations_by_type():
    """
    Test: Clear explanations by type.
    """
    print("=" * 70)
    print("TEST: Clear Explanations by Type")
    print("=" * 70)
    
    manager = CodeExplanationManager()
    
    range = ExplanationRange(0, 0, 10, 0)
    manager.add_function_explanation(range, "text", 0.8)
    
    result = manager.clear_explanations_by_type(ExplanationType.FUNCTION)
    
    assert result.success == True, "Clear başarılı olmalı"
    
    print(f"  Cleared by type: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear explanations by type")
    print("=" * 70)


def test_set_explanation_enabled():
    """
    Test: Set explanation enabled.
    """
    print("=" * 70)
    print("TEST: Set Explanation Enabled")
    print("=" * 70)
    
    manager = CodeExplanationManager()
    
    range = ExplanationRange(0, 0, 10, 0)
    result = manager.add_function_explanation(range, "text", 0.8)
    explanation_id = result.explanation.id
    
    result = manager.set_explanation_enabled(explanation_id, False)
    
    assert result.success == True, "Set başarılı olmalı"
    
    print(f"  Explanation enabled state: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set explanation enabled")
    print("=" * 70)


def test_set_explanation_visible():
    """
    Test: Set explanation visible.
    """
    print("=" * 70)
    print("TEST: Set Explanation Visible")
    print("=" * 70)
    
    manager = CodeExplanationManager()
    
    range = ExplanationRange(0, 0, 10, 0)
    result = manager.add_function_explanation(range, "text", 0.8)
    explanation_id = result.explanation.id
    
    result = manager.set_explanation_visible(explanation_id, False)
    
    assert result.success == True, "Set başarılı olmalı"
    
    print(f"  Explanation visible state: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set explanation visible")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    manager = CodeExplanationManager()
    
    new_config = ExplanationConfig(max_explanations=200)
    result = manager.update_config(new_config)
    
    assert result.success == True, "Update başarılı olmalı"
    assert manager.config.max_explanations == 200, "Config güncellenmeli"
    
    print(f"  Max explanations: {manager.config.max_explanations}")
    
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
    
    config = ExplanationConfig(max_explanations=200)
    manager = CodeExplanationManager(config)
    
    retrieved_config = manager.get_config()
    
    assert retrieved_config.max_explanations == 200, "Config eşleşmeli"
    
    print(f"  Max explanations: {retrieved_config.max_explanations}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_explanation_type_enum()
        test2 = test_explanation_format_enum()
        test3 = test_explanation_range_dataclass()
        test4 = test_code_explanation_dataclass()
        test5 = test_explanation_config_dataclass()
        test6 = test_explanation_result_dataclass()
        test7 = test_code_explanation_manager_initialization()
        test8 = test_add_explanation()
        test9 = test_remove_explanation()
        test10 = test_get_explanation()
        test11 = test_get_all_explanations()
        test12 = test_get_explanations_by_type()
        test13 = test_add_function_explanation()
        test14 = test_add_class_explanation()
        test15 = test_add_variable_explanation()
        test16 = test_add_module_explanation()
        test17 = test_add_line_explanation()
        test18 = test_add_block_explanation()
        test19 = test_filter_by_confidence()
        test20 = test_get_explanations_at_line()
        test21 = test_clear_explanations()
        test22 = test_clear_explanations_by_type()
        test23 = test_set_explanation_enabled()
        test24 = test_set_explanation_visible()
        test25 = test_update_config()
        test26 = test_get_config()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"ExplanationType Enum: {'PASS' if test1 else 'FAIL'}")
        print(f"ExplanationFormat Enum: {'PASS' if test2 else 'FAIL'}")
        print(f"ExplanationRange Dataclass: {'PASS' if test3 else 'FAIL'}")
        print(f"CodeExplanation Dataclass: {'PASS' if test4 else 'FAIL'}")
        print(f"ExplanationConfig Dataclass: {'PASS' if test5 else 'FAIL'}")
        print(f"ExplanationResult Dataclass: {'PASS' if test6 else 'FAIL'}")
        print(f"CodeExplanationManager Initialization: {'PASS' if test7 else 'FAIL'}")
        print(f"Add Explanation: {'PASS' if test8 else 'FAIL'}")
        print(f"Remove Explanation: {'PASS' if test9 else 'FAIL'}")
        print(f"Get Explanation: {'PASS' if test10 else 'FAIL'}")
        print(f"Get All Explanations: {'PASS' if test11 else 'FAIL'}")
        print(f"Get Explanations by Type: {'PASS' if test12 else 'FAIL'}")
        print(f"Add Function Explanation: {'PASS' if test13 else 'FAIL'}")
        print(f"Add Class Explanation: {'PASS' if test14 else 'FAIL'}")
        print(f"Add Variable Explanation: {'PASS' if test15 else 'FAIL'}")
        print(f"Add Module Explanation: {'PASS' if test16 else 'FAIL'}")
        print(f"Add Line Explanation: {'PASS' if test17 else 'FAIL'}")
        print(f"Add Block Explanation: {'PASS' if test18 else 'FAIL'}")
        print(f"Filter by Confidence: {'PASS' if test19 else 'FAIL'}")
        print(f"Get Explanations at Line: {'PASS' if test20 else 'FAIL'}")
        print(f"Clear Explanations: {'PASS' if test21 else 'FAIL'}")
        print(f"Clear Explanations by Type: {'PASS' if test22 else 'FAIL'}")
        print(f"Set Explanation Enabled: {'PASS' if test23 else 'FAIL'}")
        print(f"Set Explanation Visible: {'PASS' if test24 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test25 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test26 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14, test15, test16, test17, test18, test19, test20, test21, test22, test23, test24, test25, test26])
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
