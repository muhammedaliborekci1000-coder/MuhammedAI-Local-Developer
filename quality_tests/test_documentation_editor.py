"""
Quality Test: Documentation (Editor)
Documentation system testleri for editor module.
"""

import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from app.editor.documentation import (
    DocumentationType,
    DocumentationFormat,
    DocumentationRange,
    Documentation,
    DocumentationConfig,
    DocumentationResult,
    DocumentationManager
)


def test_documentation_type_enum():
    """
    Test: DocumentationType enum.
    """
    print("=" * 70)
    print("TEST: DocumentationType Enum")
    print("=" * 70)
    
    assert DocumentationType.FUNCTION.value == "function"
    assert DocumentationType.CLASS.value == "class"
    assert DocumentationType.MODULE.value == "module"
    assert DocumentationType.VARIABLE.value == "variable"
    assert DocumentationType.PARAMETER.value == "parameter"
    assert DocumentationType.RETURN.value == "return"
    assert DocumentationType.EXCEPTION.value == "exception"
    assert DocumentationType.EXAMPLE.value == "example"
    assert DocumentationType.CUSTOM.value == "custom"
    
    print(f"  All enum values verified")
    print(f"  Total types: {len(DocumentationType)}")
    
    print("\n" + "=" * 70)
    print("PASS: DocumentationType enum")
    print("=" * 70)


def test_documentation_format_enum():
    """
    Test: DocumentationFormat enum.
    """
    print("=" * 70)
    print("TEST: DocumentationFormat Enum")
    print("=" * 70)
    
    assert DocumentationFormat.PLAIN_TEXT.value == "plain_text"
    assert DocumentationFormat.MARKDOWN.value == "markdown"
    assert DocumentationFormat.HTML.value == "html"
    assert DocumentationFormat.DOCSTRING.value == "docstring"
    assert DocumentationFormat.RICH_TEXT.value == "rich_text"
    
    print(f"  All enum values verified")
    print(f"  Total formats: {len(DocumentationFormat)}")
    
    print("\n" + "=" * 70)
    print("PASS: DocumentationFormat enum")
    print("=" * 70)


def test_documentation_range_dataclass():
    """
    Test: DocumentationRange dataclass.
    """
    print("=" * 70)
    print("TEST: DocumentationRange Dataclass")
    print("=" * 70)
    
    range = DocumentationRange(
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
    print("PASS: DocumentationRange dataclass")
    print("=" * 70)


def test_documentation_dataclass():
    """
    Test: Documentation dataclass.
    """
    print("=" * 70)
    print("TEST: Documentation Dataclass")
    print("=" * 70)
    
    range = DocumentationRange(0, 0, 10, 0)
    documentation = Documentation(
        id="doc_1",
        type=DocumentationType.FUNCTION,
        range=range,
        text="This function does X"
    )
    
    assert documentation.id == "doc_1", "ID eşleşmeli"
    assert documentation.type == DocumentationType.FUNCTION, "Type eşleşmeli"
    assert documentation.text == "This function does X", "Text eşleşmeli"
    
    print(f"  ID: {documentation.id}")
    print(f"  Type: {documentation.type.value}")
    print(f"  Text: {documentation.text}")
    
    print("\n" + "=" * 70)
    print("PASS: Documentation dataclass")
    print("=" * 70)


def test_documentation_config_dataclass():
    """
    Test: DocumentationConfig dataclass.
    """
    print("=" * 70)
    print("TEST: DocumentationConfig Dataclass")
    print("=" * 70)
    
    config = DocumentationConfig(
        enabled=True,
        format=DocumentationFormat.MARKDOWN
    )
    
    assert config.enabled == True, "Enabled eşleşmeli"
    assert config.format == DocumentationFormat.MARKDOWN, "Format eşleşmeli"
    
    print(f"  Enabled: {config.enabled}")
    print(f"  Format: {config.format.value}")
    
    print("\n" + "=" * 70)
    print("PASS: DocumentationConfig dataclass")
    print("=" * 70)


def test_documentation_result_dataclass():
    """
    Test: DocumentationResult dataclass.
    """
    print("=" * 70)
    print("TEST: DocumentationResult Dataclass")
    print("=" * 70)
    
    result = DocumentationResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.documentation_list, list), "Documentation list olmalı"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Documentation: {len(result.documentation_list)}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: DocumentationResult dataclass")
    print("=" * 70)


def test_documentation_manager_initialization():
    """
    Test: DocumentationManager initialization.
    """
    print("=" * 70)
    print("TEST: DocumentationManager Initialization")
    print("=" * 70)
    
    config = DocumentationConfig()
    manager = DocumentationManager(config)
    
    assert manager.config == config, "Config eşleşmeli"
    assert len(manager.documentation) == 0, "Documentation boş olmalı"
    assert manager.cache == {}, "Cache boş olmalı"
    
    print(f"  Documentation: {len(manager.documentation)}")
    print(f"  Cache: {len(manager.cache)}")
    
    print("\n" + "=" * 70)
    print("PASS: DocumentationManager initialization")
    print("=" * 70)


def test_add_documentation():
    """
    Test: Add documentation.
    """
    print("=" * 70)
    print("TEST: Add Documentation")
    print("=" * 70)
    
    manager = DocumentationManager()
    
    range = DocumentationRange(0, 0, 10, 0)
    documentation = Documentation(
        id="",
        type=DocumentationType.FUNCTION,
        range=range,
        text="This function does X"
    )
    
    result = manager.add_documentation(documentation)
    
    assert result.success == True, "Ekleme başarılı olmalı"
    assert len(manager.documentation) > 0, "Documentation eklenmeli"
    
    print(f"  Documentation added: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add documentation")
    print("=" * 70)


def test_remove_documentation():
    """
    Test: Remove documentation.
    """
    print("=" * 70)
    print("TEST: Remove Documentation")
    print("=" * 70)
    
    manager = DocumentationManager()
    
    range = DocumentationRange(0, 0, 10, 0)
    documentation = Documentation(
        id="",
        type=DocumentationType.FUNCTION,
        range=range,
        text="This function does X"
    )
    
    result = manager.add_documentation(documentation)
    documentation_id = result.documentation.id
    
    result = manager.remove_documentation(documentation_id)
    
    assert result.success == True, "Kaldırma başarılı olmalı"
    assert documentation_id not in manager.documentation, "Documentation silinmeli"
    
    print(f"  Documentation removed: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Remove documentation")
    print("=" * 70)


def test_get_documentation():
    """
    Test: Get documentation.
    """
    print("=" * 70)
    print("TEST: Get Documentation")
    print("=" * 70)
    
    manager = DocumentationManager()
    
    range = DocumentationRange(0, 0, 10, 0)
    documentation = Documentation(
        id="",
        type=DocumentationType.FUNCTION,
        range=range,
        text="This function does X"
    )
    
    result = manager.add_documentation(documentation)
    documentation_id = result.documentation.id
    
    retrieved_documentation = manager.get_documentation(documentation_id)
    
    assert retrieved_documentation is not None, "Documentation bulunmalı"
    assert retrieved_documentation.id == documentation_id, "ID eşleşmeli"
    
    print(f"  Documentation: {retrieved_documentation.text}")
    
    print("\n" + "=" * 70)
    print("PASS: Get documentation")
    print("=" * 70)


def test_get_all_documentation():
    """
    Test: Get all documentation.
    """
    print("=" * 70)
    print("TEST: Get All Documentation")
    print("=" * 70)
    
    manager = DocumentationManager()
    
    range = DocumentationRange(0, 0, 10, 0)
    documentation = Documentation(
        id="",
        type=DocumentationType.FUNCTION,
        range=range,
        text="This function does X"
    )
    
    manager.add_documentation(documentation)
    documentation_list = manager.get_all_documentation()
    
    assert len(documentation_list) > 0, "Documentation olmalı"
    
    print(f"  Total documentation: {len(documentation_list)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get all documentation")
    print("=" * 70)


def test_get_documentation_by_type():
    """
    Test: Get documentation by type.
    """
    print("=" * 70)
    print("TEST: Get Documentation by Type")
    print("=" * 70)
    
    manager = DocumentationManager()
    
    range = DocumentationRange(0, 0, 10, 0)
    documentation = Documentation(
        id="",
        type=DocumentationType.FUNCTION,
        range=range,
        text="This function does X"
    )
    
    manager.add_documentation(documentation)
    documentation_list = manager.get_documentation_by_type(DocumentationType.FUNCTION)
    
    assert len(documentation_list) > 0, "Function documentation olmalı"
    
    print(f"  Function documentation: {len(documentation_list)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get documentation by type")
    print("=" * 70)


def test_add_function_documentation():
    """
    Test: Add function documentation.
    """
    print("=" * 70)
    print("TEST: Add Function Documentation")
    print("=" * 70)
    
    manager = DocumentationManager()
    
    range = DocumentationRange(0, 0, 10, 0)
    result = manager.add_function_documentation(range, "This function does X", "test_function", "def test_function():")
    
    assert result.success == True, "Function documentation başarılı olmalı"
    
    print(f"  Function documentation: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add function documentation")
    print("=" * 70)


def test_add_class_documentation():
    """
    Test: Add class documentation.
    """
    print("=" * 70)
    print("TEST: Add Class Documentation")
    print("=" * 70)
    
    manager = DocumentationManager()
    
    range = DocumentationRange(0, 0, 20, 0)
    result = manager.add_class_documentation(range, "This class represents X", "TestClass")
    
    assert result.success == True, "Class documentation başarılı olmalı"
    
    print(f"  Class documentation: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add class documentation")
    print("=" * 70)


def test_add_module_documentation():
    """
    Test: Add module documentation.
    """
    print("=" * 70)
    print("TEST: Add Module Documentation")
    print("=" * 70)
    
    manager = DocumentationManager()
    
    range = DocumentationRange(0, 0, 100, 0)
    result = manager.add_module_documentation(range, "This module provides X", "test_module")
    
    assert result.success == True, "Module documentation başarılı olmalı"
    
    print(f"  Module documentation: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add module documentation")
    print("=" * 70)


def test_add_variable_documentation():
    """
    Test: Add variable documentation.
    """
    print("=" * 70)
    print("TEST: Add Variable Documentation")
    print("=" * 70)
    
    manager = DocumentationManager()
    
    range = DocumentationRange(0, 0, 0, 10)
    result = manager.add_variable_documentation(range, "This variable holds X", "test_var")
    
    assert result.success == True, "Variable documentation başarılı olmalı"
    
    print(f"  Variable documentation: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add variable documentation")
    print("=" * 70)


def test_add_parameter_documentation():
    """
    Test: Add parameter documentation.
    """
    print("=" * 70)
    print("TEST: Add Parameter Documentation")
    print("=" * 70)
    
    manager = DocumentationManager()
    
    range = DocumentationRange(0, 0, 0, 10)
    result = manager.add_parameter_documentation(range, "This parameter is X", "param")
    
    assert result.success == True, "Parameter documentation başarılı olmalı"
    
    print(f"  Parameter documentation: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add parameter documentation")
    print("=" * 70)


def test_add_return_documentation():
    """
    Test: Add return documentation.
    """
    print("=" * 70)
    print("TEST: Add Return Documentation")
    print("=" * 70)
    
    manager = DocumentationManager()
    
    range = DocumentationRange(10, 0, 10, 20)
    result = manager.add_return_documentation(range, "Returns X")
    
    assert result.success == True, "Return documentation başarılı olmalı"
    
    print(f"  Return documentation: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add return documentation")
    print("=" * 70)


def test_add_exception_documentation():
    """
    Test: Add exception documentation.
    """
    print("=" * 70)
    print("TEST: Add Exception Documentation")
    print("=" * 70)
    
    manager = DocumentationManager()
    
    range = DocumentationRange(0, 0, 0, 10)
    result = manager.add_exception_documentation(range, "This exception is raised when X", "TestException")
    
    assert result.success == True, "Exception documentation başarılı olmalı"
    
    print(f"  Exception documentation: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add exception documentation")
    print("=" * 70)


def test_add_example_documentation():
    """
    Test: Add example documentation.
    """
    print("=" * 70)
    print("TEST: Add Example Documentation")
    print("=" * 70)
    
    manager = DocumentationManager()
    
    range = DocumentationRange(0, 0, 5, 0)
    result = manager.add_example_documentation(range, "Example usage")
    
    assert result.success == True, "Example documentation başarılı olmalı"
    
    print(f"  Example documentation: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add example documentation")
    print("=" * 70)


def test_get_documentation_at_line():
    """
    Test: Get documentation at line.
    """
    print("=" * 70)
    print("TEST: Get Documentation at Line")
    print("=" * 70)
    
    manager = DocumentationManager()
    
    range = DocumentationRange(0, 0, 10, 0)
    manager.add_function_documentation(range, "text", "test_function")
    
    documentation_list = manager.get_documentation_at_line(5)
    
    assert len(documentation_list) > 0, "Line 5 documentation olmalı"
    
    print(f"  Line 5 documentation: {len(documentation_list)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get documentation at line")
    print("=" * 70)


def test_get_documentation_by_symbol():
    """
    Test: Get documentation by symbol.
    """
    print("=" * 70)
    print("TEST: Get Documentation by Symbol")
    print("=" * 70)
    
    manager = DocumentationManager()
    
    range = DocumentationRange(0, 0, 10, 0)
    manager.add_function_documentation(range, "text", "test_function")
    
    documentation_list = manager.get_documentation_by_symbol("test_function")
    
    assert len(documentation_list) > 0, "test_function documentation olmalı"
    
    print(f"  test_function documentation: {len(documentation_list)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get documentation by symbol")
    print("=" * 70)


def test_clear_documentation():
    """
    Test: Clear documentation.
    """
    print("=" * 70)
    print("TEST: Clear Documentation")
    print("=" * 70)
    
    manager = DocumentationManager()
    
    range = DocumentationRange(0, 0, 10, 0)
    manager.add_function_documentation(range, "text", "test_function")
    
    result = manager.clear_documentation()
    
    assert result.success == True, "Clear başarılı olmalı"
    assert len(manager.documentation) == 0, "Documentation temizlenmeli"
    
    print(f"  Cleared: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear documentation")
    print("=" * 70)


def test_clear_documentation_by_type():
    """
    Test: Clear documentation by type.
    """
    print("=" * 70)
    print("TEST: Clear Documentation by Type")
    print("=" * 70)
    
    manager = DocumentationManager()
    
    range = DocumentationRange(0, 0, 10, 0)
    manager.add_function_documentation(range, "text", "test_function")
    
    result = manager.clear_documentation_by_type(DocumentationType.FUNCTION)
    
    assert result.success == True, "Clear başarılı olmalı"
    
    print(f"  Cleared by type: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear documentation by type")
    print("=" * 70)


def test_set_documentation_enabled():
    """
    Test: Set documentation enabled.
    """
    print("=" * 70)
    print("TEST: Set Documentation Enabled")
    print("=" * 70)
    
    manager = DocumentationManager()
    
    range = DocumentationRange(0, 0, 10, 0)
    result = manager.add_function_documentation(range, "text", "test_function")
    documentation_id = result.documentation.id
    
    result = manager.set_documentation_enabled(documentation_id, False)
    
    assert result.success == True, "Set başarılı olmalı"
    
    print(f"  Documentation enabled state: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set documentation enabled")
    print("=" * 70)


def test_set_documentation_visible():
    """
    Test: Set documentation visible.
    """
    print("=" * 70)
    print("TEST: Set Documentation Visible")
    print("=" * 70)
    
    manager = DocumentationManager()
    
    range = DocumentationRange(0, 0, 10, 0)
    result = manager.add_function_documentation(range, "text", "test_function")
    documentation_id = result.documentation.id
    
    result = manager.set_documentation_visible(documentation_id, False)
    
    assert result.success == True, "Set başarılı olmalı"
    
    print(f"  Documentation visible state: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set documentation visible")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    manager = DocumentationManager()
    
    new_config = DocumentationConfig(max_documentation=200)
    result = manager.update_config(new_config)
    
    assert result.success == True, "Update başarılı olmalı"
    assert manager.config.max_documentation == 200, "Config güncellenmeli"
    
    print(f"  Max documentation: {manager.config.max_documentation}")
    
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
    
    config = DocumentationConfig(max_documentation=200)
    manager = DocumentationManager(config)
    
    retrieved_config = manager.get_config()
    
    assert retrieved_config.max_documentation == 200, "Config eşleşmeli"
    
    print(f"  Max documentation: {retrieved_config.max_documentation}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_documentation_type_enum()
        test2 = test_documentation_format_enum()
        test3 = test_documentation_range_dataclass()
        test4 = test_documentation_dataclass()
        test5 = test_documentation_config_dataclass()
        test6 = test_documentation_result_dataclass()
        test7 = test_documentation_manager_initialization()
        test8 = test_add_documentation()
        test9 = test_remove_documentation()
        test10 = test_get_documentation()
        test11 = test_get_all_documentation()
        test12 = test_get_documentation_by_type()
        test13 = test_add_function_documentation()
        test14 = test_add_class_documentation()
        test15 = test_add_module_documentation()
        test16 = test_add_variable_documentation()
        test17 = test_add_parameter_documentation()
        test18 = test_add_return_documentation()
        test19 = test_add_exception_documentation()
        test20 = test_add_example_documentation()
        test21 = test_get_documentation_at_line()
        test22 = test_get_documentation_by_symbol()
        test23 = test_clear_documentation()
        test24 = test_clear_documentation_by_type()
        test25 = test_set_documentation_enabled()
        test26 = test_set_documentation_visible()
        test27 = test_update_config()
        test28 = test_get_config()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"DocumentationType Enum: {'PASS' if test1 else 'FAIL'}")
        print(f"DocumentationFormat Enum: {'PASS' if test2 else 'FAIL'}")
        print(f"DocumentationRange Dataclass: {'PASS' if test3 else 'FAIL'}")
        print(f"Documentation Dataclass: {'PASS' if test4 else 'FAIL'}")
        print(f"DocumentationConfig Dataclass: {'PASS' if test5 else 'FAIL'}")
        print(f"DocumentationResult Dataclass: {'PASS' if test6 else 'FAIL'}")
        print(f"DocumentationManager Initialization: {'PASS' if test7 else 'FAIL'}")
        print(f"Add Documentation: {'PASS' if test8 else 'FAIL'}")
        print(f"Remove Documentation: {'PASS' if test9 else 'FAIL'}")
        print(f"Get Documentation: {'PASS' if test10 else 'FAIL'}")
        print(f"Get All Documentation: {'PASS' if test11 else 'FAIL'}")
        print(f"Get Documentation by Type: {'PASS' if test12 else 'FAIL'}")
        print(f"Add Function Documentation: {'PASS' if test13 else 'FAIL'}")
        print(f"Add Class Documentation: {'PASS' if test14 else 'FAIL'}")
        print(f"Add Module Documentation: {'PASS' if test15 else 'FAIL'}")
        print(f"Add Variable Documentation: {'PASS' if test16 else 'FAIL'}")
        print(f"Add Parameter Documentation: {'PASS' if test17 else 'FAIL'}")
        print(f"Add Return Documentation: {'PASS' if test18 else 'FAIL'}")
        print(f"Add Exception Documentation: {'PASS' if test19 else 'FAIL'}")
        print(f"Add Example Documentation: {'PASS' if test20 else 'FAIL'}")
        print(f"Get Documentation at Line: {'PASS' if test21 else 'FAIL'}")
        print(f"Get Documentation by Symbol: {'PASS' if test22 else 'FAIL'}")
        print(f"Clear Documentation: {'PASS' if test23 else 'FAIL'}")
        print(f"Clear Documentation by Type: {'PASS' if test24 else 'FAIL'}")
        print(f"Set Documentation Enabled: {'PASS' if test25 else 'FAIL'}")
        print(f"Set Documentation Visible: {'PASS' if test26 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test27 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test28 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14, test15, test16, test17, test18, test19, test20, test21, test22, test23, test24, test25, test26, test27, test28])
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
