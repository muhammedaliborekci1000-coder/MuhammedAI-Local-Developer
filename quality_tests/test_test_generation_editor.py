"""
Quality Test: Test Generation (Editor)
Test generation system testleri for editor module.
"""

import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from app.editor.test_generation import (
    TestType,
    TestFramework,
    TestRange,
    GeneratedTest,
    TestGenerationConfig,
    TestGenerationResult,
    TestGenerationManager
)


def test_test_type_enum():
    """
    Test: TestType enum.
    """
    print("=" * 70)
    print("TEST: TestType Enum")
    print("=" * 70)
    
    assert TestType.UNIT.value == "unit"
    assert TestType.INTEGRATION.value == "integration"
    assert TestType.E2E.value == "e2e"
    assert TestType.PERFORMANCE.value == "performance"
    assert TestType.SECURITY.value == "security"
    assert TestType.CUSTOM.value == "custom"
    
    print(f"  All enum values verified")
    print(f"  Total types: {len(TestType)}")
    
    print("\n" + "=" * 70)
    print("PASS: TestType enum")
    print("=" * 70)


def test_test_framework_enum():
    """
    Test: TestFramework enum.
    """
    print("=" * 70)
    print("TEST: TestFramework Enum")
    print("=" * 70)
    
    assert TestFramework.PYTEST.value == "pytest"
    assert TestFramework.UNITTEST.value == "unittest"
    assert TestFramework.JEST.value == "jest"
    assert TestFramework.MOCHA.value == "mocha"
    assert TestFramework.JASMINE.value == "jasmine"
    assert TestFramework.CUSTOM.value == "custom"
    
    print(f"  All enum values verified")
    print(f"  Total frameworks: {len(TestFramework)}")
    
    print("\n" + "=" * 70)
    print("PASS: TestFramework enum")
    print("=" * 70)


def test_test_range_dataclass():
    """
    Test: TestRange dataclass.
    """
    print("=" * 70)
    print("TEST: TestRange Dataclass")
    print("=" * 70)
    
    range = TestRange(
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
    print("PASS: TestRange dataclass")
    print("=" * 70)


def test_generated_test_dataclass():
    """
    Test: GeneratedTest dataclass.
    """
    print("=" * 70)
    print("TEST: GeneratedTest Dataclass")
    print("=" * 70)
    
    range = TestRange(0, 0, 10, 0)
    test = GeneratedTest(
        id="test_1",
        type=TestType.UNIT,
        framework=TestFramework.PYTEST,
        range=range,
        code="def test_function(): pass",
        file_path="test.py"
    )
    
    assert test.id == "test_1", "ID eşleşmeli"
    assert test.type == TestType.UNIT, "Type eşleşmeli"
    assert test.framework == TestFramework.PYTEST, "Framework eşleşmeli"
    assert test.code == "def test_function(): pass", "Code eşleşmeli"
    assert test.file_path == "test.py", "File path eşleşmeli"
    
    print(f"  ID: {test.id}")
    print(f"  Type: {test.type.value}")
    print(f"  Framework: {test.framework.value}")
    print(f"  Code: {test.code}")
    
    print("\n" + "=" * 70)
    print("PASS: GeneratedTest dataclass")
    print("=" * 70)


def test_test_generation_config_dataclass():
    """
    Test: TestGenerationConfig dataclass.
    """
    print("=" * 70)
    print("TEST: TestGenerationConfig Dataclass")
    print("=" * 70)
    
    config = TestGenerationConfig(
        enabled=True,
        framework=TestFramework.PYTEST
    )
    
    assert config.enabled == True, "Enabled eşleşmeli"
    assert config.framework == TestFramework.PYTEST, "Framework eşleşmeli"
    
    print(f"  Enabled: {config.enabled}")
    print(f"  Framework: {config.framework.value}")
    
    print("\n" + "=" * 70)
    print("PASS: TestGenerationConfig dataclass")
    print("=" * 70)


def test_test_generation_result_dataclass():
    """
    Test: TestGenerationResult dataclass.
    """
    print("=" * 70)
    print("TEST: TestGenerationResult Dataclass")
    print("=" * 70)
    
    result = TestGenerationResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.tests, list), "Tests list olmalı"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Tests: {len(result.tests)}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: TestGenerationResult dataclass")
    print("=" * 70)


def test_test_generation_manager_initialization():
    """
    Test: TestGenerationManager initialization.
    """
    print("=" * 70)
    print("TEST: TestGenerationManager Initialization")
    print("=" * 70)
    
    config = TestGenerationConfig()
    manager = TestGenerationManager(config)
    
    assert manager.config == config, "Config eşleşmeli"
    assert len(manager.tests) == 0, "Tests boş olmalı"
    assert manager.cache == {}, "Cache boş olmalı"
    
    print(f"  Tests: {len(manager.tests)}")
    print(f"  Cache: {len(manager.cache)}")
    
    print("\n" + "=" * 70)
    print("PASS: TestGenerationManager initialization")
    print("=" * 70)


def test_add_test():
    """
    Test: Add test.
    """
    print("=" * 70)
    print("TEST: Add Test")
    print("=" * 70)
    
    manager = TestGenerationManager()
    
    range = TestRange(0, 0, 10, 0)
    test = GeneratedTest(
        id="",
        type=TestType.UNIT,
        framework=TestFramework.PYTEST,
        range=range,
        code="def test_function(): pass",
        file_path="test.py"
    )
    
    result = manager.add_test(test)
    
    assert result.success == True, "Ekleme başarılı olmalı"
    assert len(manager.tests) > 0, "Test eklenmeli"
    
    print(f"  Test added: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add test")
    print("=" * 70)


def test_remove_test():
    """
    Test: Remove test.
    """
    print("=" * 70)
    print("TEST: Remove Test")
    print("=" * 70)
    
    manager = TestGenerationManager()
    
    range = TestRange(0, 0, 10, 0)
    test = GeneratedTest(
        id="",
        type=TestType.UNIT,
        framework=TestFramework.PYTEST,
        range=range,
        code="def test_function(): pass",
        file_path="test.py"
    )
    
    result = manager.add_test(test)
    test_id = result.test.id
    
    result = manager.remove_test(test_id)
    
    assert result.success == True, "Kaldırma başarılı olmalı"
    assert test_id not in manager.tests, "Test silinmeli"
    
    print(f"  Test removed: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Remove test")
    print("=" * 70)


def test_get_test():
    """
    Test: Get test.
    """
    print("=" * 70)
    print("TEST: Get Test")
    print("=" * 70)
    
    manager = TestGenerationManager()
    
    range = TestRange(0, 0, 10, 0)
    test = GeneratedTest(
        id="",
        type=TestType.UNIT,
        framework=TestFramework.PYTEST,
        range=range,
        code="def test_function(): pass",
        file_path="test.py"
    )
    
    result = manager.add_test(test)
    test_id = result.test.id
    
    retrieved_test = manager.get_test(test_id)
    
    assert retrieved_test is not None, "Test bulunmalı"
    assert retrieved_test.id == test_id, "ID eşleşmeli"
    
    print(f"  Test: {retrieved_test.code}")
    
    print("\n" + "=" * 70)
    print("PASS: Get test")
    print("=" * 70)


def test_get_all_tests():
    """
    Test: Get all tests.
    """
    print("=" * 70)
    print("TEST: Get All Tests")
    print("=" * 70)
    
    manager = TestGenerationManager()
    
    range = TestRange(0, 0, 10, 0)
    test = GeneratedTest(
        id="",
        type=TestType.UNIT,
        framework=TestFramework.PYTEST,
        range=range,
        code="def test_function(): pass",
        file_path="test.py"
    )
    
    manager.add_test(test)
    tests = manager.get_all_tests()
    
    assert len(tests) > 0, "Tests olmalı"
    
    print(f"  Total tests: {len(tests)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get all tests")
    print("=" * 70)


def test_get_tests_by_type():
    """
    Test: Get tests by type.
    """
    print("=" * 70)
    print("TEST: Get Tests by Type")
    print("=" * 70)
    
    manager = TestGenerationManager()
    
    range = TestRange(0, 0, 10, 0)
    test = GeneratedTest(
        id="",
        type=TestType.UNIT,
        framework=TestFramework.PYTEST,
        range=range,
        code="def test_function(): pass",
        file_path="test.py"
    )
    
    manager.add_test(test)
    tests = manager.get_tests_by_type(TestType.UNIT)
    
    assert len(tests) > 0, "Unit tests olmalı"
    
    print(f"  Unit tests: {len(tests)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get tests by type")
    print("=" * 70)


def test_get_tests_by_framework():
    """
    Test: Get tests by framework.
    """
    print("=" * 70)
    print("TEST: Get Tests by Framework")
    print("=" * 70)
    
    manager = TestGenerationManager()
    
    range = TestRange(0, 0, 10, 0)
    test = GeneratedTest(
        id="",
        type=TestType.UNIT,
        framework=TestFramework.PYTEST,
        range=range,
        code="def test_function(): pass",
        file_path="test.py"
    )
    
    manager.add_test(test)
    tests = manager.get_tests_by_framework(TestFramework.PYTEST)
    
    assert len(tests) > 0, "Pytest tests olmalı"
    
    print(f"  Pytest tests: {len(tests)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get tests by framework")
    print("=" * 70)


def test_generate_unit_test():
    """
    Test: Generate unit test.
    """
    print("=" * 70)
    print("TEST: Generate Unit Test")
    print("=" * 70)
    
    manager = TestGenerationManager()
    
    range = TestRange(0, 0, 10, 0)
    result = manager.generate_unit_test(range, "def test_function(): pass", "test.py", "test_function")
    
    assert result.success == True, "Unit test generation başarılı olmalı"
    
    print(f"  Unit test: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Generate unit test")
    print("=" * 70)


def test_generate_integration_test():
    """
    Test: Generate integration test.
    """
    print("=" * 70)
    print("TEST: Generate Integration Test")
    print("=" * 70)
    
    manager = TestGenerationManager()
    
    range = TestRange(0, 0, 10, 0)
    result = manager.generate_integration_test(range, "def test_integration(): pass", "test.py", "test_function")
    
    assert result.success == True, "Integration test generation başarılı olmalı"
    
    print(f"  Integration test: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Generate integration test")
    print("=" * 70)


def test_generate_e2e_test():
    """
    Test: Generate E2E test.
    """
    print("=" * 70)
    print("TEST: Generate E2E Test")
    print("=" * 70)
    
    manager = TestGenerationManager()
    
    range = TestRange(0, 0, 10, 0)
    result = manager.generate_e2e_test(range, "def test_e2e(): pass", "test.py")
    
    assert result.success == False, "E2E test generation disabled olmalı"
    
    print(f"  E2E test: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Generate E2E test")
    print("=" * 70)


def test_generate_performance_test():
    """
    Test: Generate performance test.
    """
    print("=" * 70)
    print("TEST: Generate Performance Test")
    print("=" * 70)
    
    manager = TestGenerationManager()
    
    range = TestRange(0, 0, 10, 0)
    result = manager.generate_performance_test(range, "def test_performance(): pass", "test.py")
    
    assert result.success == False, "Performance test generation disabled olmalı"
    
    print(f"  Performance test: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Generate performance test")
    print("=" * 70)


def test_generate_security_test():
    """
    Test: Generate security test.
    """
    print("=" * 70)
    print("TEST: Generate Security Test")
    print("=" * 70)
    
    manager = TestGenerationManager()
    
    range = TestRange(0, 0, 10, 0)
    result = manager.generate_security_test(range, "def test_security(): pass", "test.py")
    
    assert result.success == False, "Security test generation disabled olmalı"
    
    print(f"  Security test: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Generate security test")
    print("=" * 70)


def test_get_tests_for_file():
    """
    Test: Get tests for file.
    """
    print("=" * 70)
    print("TEST: Get Tests for File")
    print("=" * 70)
    
    manager = TestGenerationManager()
    
    range = TestRange(0, 0, 10, 0)
    manager.generate_unit_test(range, "def test_function(): pass", "test.py", "test_function")
    
    tests = manager.get_tests_for_file("test.py")
    
    assert len(tests) > 0, "test.py tests olmalı"
    
    print(f"  test.py tests: {len(tests)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get tests for file")
    print("=" * 70)


def test_get_tests_for_function():
    """
    Test: Get tests for function.
    """
    print("=" * 70)
    print("TEST: Get Tests for Function")
    print("=" * 70)
    
    manager = TestGenerationManager()
    
    range = TestRange(0, 0, 10, 0)
    manager.generate_unit_test(range, "def test_function(): pass", "test.py", "test_function")
    
    tests = manager.get_tests_for_function("test_function")
    
    assert len(tests) > 0, "test_function tests olmalı"
    
    print(f"  test_function tests: {len(tests)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get tests for function")
    print("=" * 70)


def test_clear_tests():
    """
    Test: Clear tests.
    """
    print("=" * 70)
    print("TEST: Clear Tests")
    print("=" * 70)
    
    manager = TestGenerationManager()
    
    range = TestRange(0, 0, 10, 0)
    manager.generate_unit_test(range, "def test_function(): pass", "test.py", "test_function")
    
    result = manager.clear_tests()
    
    assert result.success == True, "Clear başarılı olmalı"
    assert len(manager.tests) == 0, "Tests temizlenmeli"
    
    print(f"  Cleared: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear tests")
    print("=" * 70)


def test_clear_tests_by_type():
    """
    Test: Clear tests by type.
    """
    print("=" * 70)
    print("TEST: Clear Tests by Type")
    print("=" * 70)
    
    manager = TestGenerationManager()
    
    range = TestRange(0, 0, 10, 0)
    manager.generate_unit_test(range, "def test_function(): pass", "test.py", "test_function")
    
    result = manager.clear_tests_by_type(TestType.UNIT)
    
    assert result.success == True, "Clear başarılı olmalı"
    
    print(f"  Cleared by type: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear tests by type")
    print("=" * 70)


def test_set_test_enabled():
    """
    Test: Set test enabled.
    """
    print("=" * 70)
    print("TEST: Set Test Enabled")
    print("=" * 70)
    
    manager = TestGenerationManager()
    
    range = TestRange(0, 0, 10, 0)
    result = manager.generate_unit_test(range, "def test_function(): pass", "test.py", "test_function")
    test_id = result.test.id
    
    result = manager.set_test_enabled(test_id, False)
    
    assert result.success == True, "Set başarılı olmalı"
    
    print(f"  Test enabled state: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set test enabled")
    print("=" * 70)


def test_set_test_visible():
    """
    Test: Set test visible.
    """
    print("=" * 70)
    print("TEST: Set Test Visible")
    print("=" * 70)
    
    manager = TestGenerationManager()
    
    range = TestRange(0, 0, 10, 0)
    result = manager.generate_unit_test(range, "def test_function(): pass", "test.py", "test_function")
    test_id = result.test.id
    
    result = manager.set_test_visible(test_id, False)
    
    assert result.success == True, "Set başarılı olmalı"
    
    print(f"  Test visible state: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set test visible")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    manager = TestGenerationManager()
    
    new_config = TestGenerationConfig(max_tests=200)
    result = manager.update_config(new_config)
    
    assert result.success == True, "Update başarılı olmalı"
    assert manager.config.max_tests == 200, "Config güncellenmeli"
    
    print(f"  Max tests: {manager.config.max_tests}")
    
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
    
    config = TestGenerationConfig(max_tests=200)
    manager = TestGenerationManager(config)
    
    retrieved_config = manager.get_config()
    
    assert retrieved_config.max_tests == 200, "Config eşleşmeli"
    
    print(f"  Max tests: {retrieved_config.max_tests}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_test_type_enum()
        test2 = test_test_framework_enum()
        test3 = test_test_range_dataclass()
        test4 = test_generated_test_dataclass()
        test5 = test_test_generation_config_dataclass()
        test6 = test_test_generation_result_dataclass()
        test7 = test_test_generation_manager_initialization()
        test8 = test_add_test()
        test9 = test_remove_test()
        test10 = test_get_test()
        test11 = test_get_all_tests()
        test12 = test_get_tests_by_type()
        test13 = test_get_tests_by_framework()
        test14 = test_generate_unit_test()
        test15 = test_generate_integration_test()
        test16 = test_generate_e2e_test()
        test17 = test_generate_performance_test()
        test18 = test_generate_security_test()
        test19 = test_get_tests_for_file()
        test20 = test_get_tests_for_function()
        test21 = test_clear_tests()
        test22 = test_clear_tests_by_type()
        test23 = test_set_test_enabled()
        test24 = test_set_test_visible()
        test25 = test_update_config()
        test26 = test_get_config()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"TestType Enum: {'PASS' if test1 else 'FAIL'}")
        print(f"TestFramework Enum: {'PASS' if test2 else 'FAIL'}")
        print(f"TestRange Dataclass: {'PASS' if test3 else 'FAIL'}")
        print(f"GeneratedTest Dataclass: {'PASS' if test4 else 'FAIL'}")
        print(f"TestGenerationConfig Dataclass: {'PASS' if test5 else 'FAIL'}")
        print(f"TestGenerationResult Dataclass: {'PASS' if test6 else 'FAIL'}")
        print(f"TestGenerationManager Initialization: {'PASS' if test7 else 'FAIL'}")
        print(f"Add Test: {'PASS' if test8 else 'FAIL'}")
        print(f"Remove Test: {'PASS' if test9 else 'FAIL'}")
        print(f"Get Test: {'PASS' if test10 else 'FAIL'}")
        print(f"Get All Tests: {'PASS' if test11 else 'FAIL'}")
        print(f"Get Tests by Type: {'PASS' if test12 else 'FAIL'}")
        print(f"Get Tests by Framework: {'PASS' if test13 else 'FAIL'}")
        print(f"Generate Unit Test: {'PASS' if test14 else 'FAIL'}")
        print(f"Generate Integration Test: {'PASS' if test15 else 'FAIL'}")
        print(f"Generate E2E Test: {'PASS' if test16 else 'FAIL'}")
        print(f"Generate Performance Test: {'PASS' if test17 else 'FAIL'}")
        print(f"Generate Security Test: {'PASS' if test18 else 'FAIL'}")
        print(f"Get Tests for File: {'PASS' if test19 else 'FAIL'}")
        print(f"Get Tests for Function: {'PASS' if test20 else 'FAIL'}")
        print(f"Clear Tests: {'PASS' if test21 else 'FAIL'}")
        print(f"Clear Tests by Type: {'PASS' if test22 else 'FAIL'}")
        print(f"Set Test Enabled: {'PASS' if test23 else 'FAIL'}")
        print(f"Set Test Visible: {'PASS' if test24 else 'FAIL'}")
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
