"""
Quality Test: Test Generation
Test generation system testleri.
"""

import sys
import os
import tempfile
import shutil
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.ai.test_generation import (
    TestGenerator,
    TestingFramework,
    TestCaseType,
    TestCase,
    TestSuite,
    TestGenerationResult
)


def test_generate_tests_for_file():
    """
    Test: Generate tests for file.
    """
    print("=" * 70)
    print("TEST: Generate Tests for File")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp(prefix="muhammedai_test_")
    
    try:
        # Test dosyası oluştur
        test_file = Path(temp_dir) / "test_module.py"
        test_file.write_text("""
def my_function():
    return 42

class MyClass:
    def method(self):
        pass
""", encoding='utf-8')
        
        generator = TestGenerator()
        
        # Generate tests
        result = generator.generate_tests_for_file(str(test_file))
        
        assert result.success, "Generation başarılı olmalı"
        assert result.test_suite is not None, "Test suite olmalı"
        assert len(result.test_suite.test_cases) > 0, "Test cases olmalı"
        
        print(f"  Success: {result.success}")
        print(f"  Test cases: {len(result.test_suite.test_cases)}")
        print(f"  Message: {result.message}")
        
        print("\n" + "=" * 70)
        print("PASS: Generate tests for file")
        print("=" * 70)
        
    finally:
        shutil.rmtree(temp_dir)


def test_generate_function_tests():
    """
    Test: Generate function tests.
    """
    print("=" * 70)
    print("TEST: Generate Function Tests")
    print("=" * 70)
    
    import ast
    code = "def my_function(x, y):\n    return x + y\n"
    tree = ast.parse(code)
    func_node = tree.body[0]
    
    generator = TestGenerator()
    test_cases = generator._generate_function_tests(func_node, code)
    
    assert len(test_cases) > 0, "Test cases olmalı"
    print(f"  Test cases generated: {len(test_cases)}")
    
    for test_case in test_cases:
        print(f"  - {test_case.name} ({test_case.type.value})")
    
    print("\n" + "=" * 70)
    print("PASS: Generate function tests")
    print("=" * 70)


def test_generate_class_tests():
    """
    Test: Generate class tests.
    """
    print("=" * 70)
    print("TEST: Generate Class Tests")
    print("=" * 70)
    
    import ast
    code = """
class MyClass:
    def __init__(self):
        self.x = 10
    
    def method(self):
        return self.x
"""
    tree = ast.parse(code)
    class_node = tree.body[0]
    
    generator = TestGenerator()
    test_cases = generator._generate_class_tests(class_node, code)
    
    assert len(test_cases) > 0, "Test cases olmalı"
    print(f"  Test cases generated: {len(test_cases)}")
    
    for test_case in test_cases:
        print(f"  - {test_case.name} ({test_case.type.value})")
    
    print("\n" + "=" * 70)
    print("PASS: Generate class tests")
    print("=" * 70)


def test_happy_path_test():
    """
    Test: Happy path test generation.
    """
    print("=" * 70)
    print("TEST: Happy Path Test Generation")
    print("=" * 70)
    
    import ast
    code = "def my_function(x):\n    return x\n"
    tree = ast.parse(code)
    func_node = tree.body[0]
    
    generator = TestGenerator()
    test_case = generator._generate_happy_path_test(func_node)
    
    assert test_case is not None, "Test case olmalı"
    assert test_case.type == TestCaseType.HAPPY_PATH, "Happy path olmalı"
    assert "my_function" in test_case.code, "Function name içermeli"
    
    print(f"  Test name: {test_case.name}")
    print(f"  Type: {test_case.type.value}")
    print(f"  Has function name: {'my_function' in test_case.code}")
    
    print("\n" + "=" * 70)
    print("PASS: Happy path test generation")
    print("=" * 70)


def test_edge_case_test():
    """
    Test: Edge case test generation.
    """
    print("=" * 70)
    print("TEST: Edge Case Test Generation")
    print("=" * 70)
    
    import ast
    code = "def my_function(x):\n    return x\n"
    tree = ast.parse(code)
    func_node = tree.body[0]
    
    generator = TestGenerator()
    test_case = generator._generate_edge_case_test(func_node)
    
    assert test_case is not None, "Test case olmalı"
    assert test_case.type == TestCaseType.EDGE_CASE, "Edge case olmalı"
    
    print(f"  Test name: {test_case.name}")
    print(f"  Type: {test_case.type.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Edge case test generation")
    print("=" * 70)


def test_error_case_test():
    """
    Test: Error case test generation.
    """
    print("=" * 70)
    print("TEST: Error Case Test Generation")
    print("=" * 70)
    
    import ast
    code = "def my_function():\n    pass\n"
    tree = ast.parse(code)
    func_node = tree.body[0]
    
    generator = TestGenerator()
    test_case = generator._generate_error_case_test(func_node)
    
    assert test_case is not None, "Test case olmalı"
    assert test_case.type == TestCaseType.ERROR_CASE, "Error case olmalı"
    assert "pytest.raises" in test_case.code, "pytest.raises içermeli"
    
    print(f"  Test name: {test_case.name}")
    print(f"  Type: {test_case.type.value}")
    print(f"  Has pytest.raises: {'pytest.raises' in test_case.code}")
    
    print("\n" + "=" * 70)
    print("PASS: Error case test generation")
    print("=" * 70)


def test_generate_test_file():
    """
    Test: Generate test file.
    """
    print("=" * 70)
    print("TEST: Generate Test File")
    print("=" * 70)
    
    test_suite = TestSuite(
        file_path="test_module.py",
        module_name="test_module",
        framework=TestingFramework.PYTEST
    )
    
    test_suite.imports = ["import pytest", "from pathlib import Path"]
    test_suite.test_cases = [
        TestCase(
            name="test_example",
            description="Example test",
            type=TestCaseType.HAPPY_PATH,
            code="    assert True\n"
        )
    ]
    
    generator = TestGenerator()
    test_file_content = generator.generate_test_file(test_suite)
    
    assert "import pytest" in test_file_content, "Import içermeli"
    assert "test_example" in test_file_content, "Test name içermeli"
    assert "assert True" in test_file_content, "Assertion içermeli"
    
    print(f"  Test file length: {len(test_file_content)}")
    print(f"  Has imports: {'import pytest' in test_file_content}")
    print(f"  Has test: {'test_example' in test_file_content}")
    
    print("\n" + "=" * 70)
    print("PASS: Generate test file")
    print("=" * 70)


def test_test_framework_enum():
    """
    Test: TestingFramework enum.
    """
    print("=" * 70)
    print("TEST: TestingFramework Enum")
    print("=" * 70)
    
    assert TestingFramework.PYTEST.value == "pytest"
    assert TestingFramework.UNITTEST.value == "unittest"
    assert TestingFramework.PYTEST_ASYNC.value == "pytest_async"
    
    print(f"  All enum values verified")
    print(f"  Total frameworks: {len(TestingFramework)}")
    
    print("\n" + "=" * 70)
    print("PASS: TestingFramework enum")
    print("=" * 70)


def test_test_case_type_enum():
    """
    Test: TestCaseType enum.
    """
    print("=" * 70)
    print("TEST: TestCaseType Enum")
    print("=" * 70)
    
    assert TestCaseType.HAPPY_PATH.value == "happy_path"
    assert TestCaseType.EDGE_CASE.value == "edge_case"
    assert TestCaseType.ERROR_CASE.value == "error_case"
    assert TestCaseType.BOUNDARY_CASE.value == "boundary_case"
    
    print(f"  All enum values verified")
    print(f"  Total types: {len(TestCaseType)}")
    
    print("\n" + "=" * 70)
    print("PASS: TestCaseType enum")
    print("=" * 70)


def test_test_case_dataclass():
    """
    Test: TestCase dataclass.
    """
    print("=" * 70)
    print("TEST: TestCase Dataclass")
    print("=" * 70)
    
    test_case = TestCase(
        name="test_example",
        description="Example test",
        type=TestCaseType.HAPPY_PATH,
        code="assert True"
    )
    
    assert test_case.name == "test_example", "Name eşleşmeli"
    assert test_case.type == TestCaseType.HAPPY_PATH, "Type eşleşmeli"
    assert test_case.code == "assert True", "Code eşleşmeli"
    
    print(f"  Name: {test_case.name}")
    print(f"  Type: {test_case.type.value}")
    print(f"  Code: {test_case.code}")
    
    print("\n" + "=" * 70)
    print("PASS: TestCase dataclass")
    print("=" * 70)


def test_test_suite_dataclass():
    """
    Test: TestSuite dataclass.
    """
    print("=" * 70)
    print("TEST: TestSuite Dataclass")
    print("=" * 70)
    
    test_suite = TestSuite(
        file_path="test_module.py",
        module_name="test_module",
        framework=TestingFramework.PYTEST
    )
    
    assert test_suite.file_path == "test_module.py", "File path eşleşmeli"
    assert test_suite.module_name == "test_module", "Module name eşleşmeli"
    assert test_suite.framework == TestingFramework.PYTEST, "Framework eşleşmeli"
    
    print(f"  File path: {test_suite.file_path}")
    print(f"  Module name: {test_suite.module_name}")
    print(f"  Framework: {test_suite.framework.value}")
    
    print("\n" + "=" * 70)
    print("PASS: TestSuite dataclass")
    print("=" * 70)


def test_analyze_coverage():
    """
    Test: Analyze coverage.
    """
    print("=" * 70)
    print("TEST: Analyze Coverage")
    print("=" * 70)
    
    generator = TestGenerator()
    
    coverage = generator.analyze_coverage(
        file_path="test_module.py",
        test_file_path="test_test_module.py"
    )
    
    assert isinstance(coverage, dict), "Dict olmalı"
    assert "file_path" in coverage, "File path içermeli"
    assert "test_file_path" in coverage, "Test file path içermeli"
    assert "coverage_percentage" in coverage, "Coverage percentage içermeli"
    
    print(f"  File path: {coverage['file_path']}")
    print(f"  Test file path: {coverage['test_file_path']}")
    print(f"  Coverage: {coverage['coverage_percentage']}")
    
    print("\n" + "=" * 70)
    print("PASS: Analyze coverage")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_generate_tests_for_file()
        test2 = test_generate_function_tests()
        test3 = test_generate_class_tests()
        test4 = test_happy_path_test()
        test5 = test_edge_case_test()
        test6 = test_error_case_test()
        test7 = test_generate_test_file()
        test8 = test_test_framework_enum()
        test9 = test_test_case_type_enum()
        test10 = test_test_case_dataclass()
        test11 = test_test_suite_dataclass()
        test12 = test_analyze_coverage()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Generate Tests for File: {'PASS' if test1 else 'FAIL'}")
        print(f"Generate Function Tests: {'PASS' if test2 else 'FAIL'}")
        print(f"Generate Class Tests: {'PASS' if test3 else 'FAIL'}")
        print(f"Happy Path Test: {'PASS' if test4 else 'FAIL'}")
        print(f"Edge Case Test: {'PASS' if test5 else 'FAIL'}")
        print(f"Error Case Test: {'PASS' if test6 else 'FAIL'}")
        print(f"Generate Test File: {'PASS' if test7 else 'FAIL'}")
        print(f"TestingFramework Enum: {'PASS' if test8 else 'FAIL'}")
        print(f"TestCaseType Enum: {'PASS' if test9 else 'FAIL'}")
        print(f"TestCase Dataclass: {'PASS' if test10 else 'FAIL'}")
        print(f"TestSuite Dataclass: {'PASS' if test11 else 'FAIL'}")
        print(f"Analyze Coverage: {'PASS' if test12 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12])
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
