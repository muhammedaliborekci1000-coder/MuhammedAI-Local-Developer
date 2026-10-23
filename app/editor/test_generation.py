"""
MuhammedAI Local Developer - Test Generation
Test generation system for code editor.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum


class TestType(Enum):
    """Test type."""
    UNIT = "unit"
    INTEGRATION = "integration"
    E2E = "e2e"
    PERFORMANCE = "performance"
    SECURITY = "security"
    CUSTOM = "custom"


class TestFramework(Enum):
    """Test framework."""
    PYTEST = "pytest"
    UNITTEST = "unittest"
    JEST = "jest"
    MOCHA = "mocha"
    JASMINE = "jasmine"
    CUSTOM = "custom"


@dataclass
class TestRange:
    """Test range."""
    start_line: int
    start_column: int
    end_line: int
    end_column: int


@dataclass
class GeneratedTest:
    """Generated test."""
    id: str
    type: TestType
    framework: TestFramework
    range: TestRange
    code: str
    file_path: str
    is_enabled: bool = True
    is_visible: bool = True
    language: Optional[str] = None
    function_name: Optional[str] = None
    class_name: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TestGenerationConfig:
    """Test generation configuration."""
    enabled: bool = True
    framework: TestFramework = TestFramework.PYTEST
    generate_unit_tests: bool = True
    generate_integration_tests: bool = True
    generate_e2e_tests: bool = False
    generate_performance_tests: bool = False
    generate_security_tests: bool = False
    auto_generate: bool = True
    max_tests: int = 100
    enable_cache: bool = True
    include_mocks: bool = True
    include_fixtures: bool = True


@dataclass
class TestGenerationResult:
    """Test generation result."""
    success: bool
    test: Optional[GeneratedTest] = None
    tests: List[GeneratedTest] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    message: Optional[str] = None


class TestGenerationManager:
    """
    Test generation manager.
    
    Özellikler:
    - Unit test generation
    - Integration test generation
    - E2E test generation
    - Performance test generation
    - Security test generation
    - Custom test generation
    - Test frameworks
    - Test filtering
    - Test caching
    - Test scope
    - Test context
    """
    
    def __init__(self, config: Optional[TestGenerationConfig] = None):
        """
        Initialize test generation manager.
        
        Args:
            config: Test generation configuration
        """
        self.config = config or TestGenerationConfig()
        self.tests: Dict[str, GeneratedTest] = {}
        self.cache: Dict[str, GeneratedTest] = {}
        self.test_id_counter = 0
        self._next_id()
    
    def _next_id(self) -> str:
        """
        Generate next test ID.
        
        Returns:
            str: Test ID
        """
        self.test_id_counter += 1
        return f"test_{self.test_id_counter}"
    
    def add_test(self, test: GeneratedTest) -> TestGenerationResult:
        """
        Add a test.
        
        Args:
            test: Test to add
            
        Returns:
            TestGenerationResult: Add result
        """
        result = TestGenerationResult(success=True)
        
        try:
            if not test.id:
                test.id = self._next_id()
            
            self.tests[test.id] = test
            
            # Cache if enabled
            if self.config.enable_cache:
                self.cache[test.id] = test
            
            result.test = test
            result.tests = self.get_all_tests()
            result.message = f"Test '{test.id}' added"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def remove_test(self, test_id: str) -> TestGenerationResult:
        """
        Remove a test.
        
        Args:
            test_id: Test ID
            
        Returns:
            TestGenerationResult: Remove result
        """
        result = TestGenerationResult(success=False)
        
        try:
            if test_id in self.tests:
                del self.tests[test_id]
                if test_id in self.cache:
                    del self.cache[test_id]
                result.success = True
                result.tests = self.get_all_tests()
                result.message = f"Test '{test_id}' removed"
            else:
                result.errors.append("Test not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_test(self, test_id: str) -> Optional[GeneratedTest]:
        """
        Get test by ID.
        
        Args:
            test_id: Test ID
            
        Returns:
            Optional[GeneratedTest]: Test
        """
        return self.tests.get(test_id)
    
    def get_all_tests(self) -> List[GeneratedTest]:
        """
        Get all tests.
        
        Returns:
            List[GeneratedTest]: All tests
        """
        return list(self.tests.values())
    
    def get_tests_by_type(self, test_type: TestType) -> List[GeneratedTest]:
        """
        Get tests by type.
        
        Args:
            test_type: Test type
            
        Returns:
            List[GeneratedTest]: Tests
        """
        return [t for t in self.tests.values() if t.type == test_type]
    
    def get_tests_by_framework(self, framework: TestFramework) -> List[GeneratedTest]:
        """
        Get tests by framework.
        
        Args:
            framework: Test framework
            
        Returns:
            List[GeneratedTest]: Tests
        """
        return [t for t in self.tests.values() if t.framework == framework]
    
    def generate_unit_test(self, range: TestRange, code: str, file_path: str, function_name: str = "") -> TestGenerationResult:
        """
        Generate unit test.
        
        Args:
            range: Test range
            code: Test code
            file_path: File path
            function_name: Function name
            
        Returns:
            TestGenerationResult: Generate result
        """
        if not self.config.generate_unit_tests:
            result = TestGenerationResult(success=False)
            result.message = "Unit test generation disabled"
            return result
        
        test = GeneratedTest(
            id="",
            type=TestType.UNIT,
            framework=self.config.framework,
            range=range,
            code=code,
            file_path=file_path,
            function_name=function_name
        )
        
        return self.add_test(test)
    
    def generate_integration_test(self, range: TestRange, code: str, file_path: str, function_name: str = "") -> TestGenerationResult:
        """
        Generate integration test.
        
        Args:
            range: Test range
            code: Test code
            file_path: File path
            function_name: Function name
            
        Returns:
            TestGenerationResult: Generate result
        """
        if not self.config.generate_integration_tests:
            result = TestGenerationResult(success=False)
            result.message = "Integration test generation disabled"
            return result
        
        test = GeneratedTest(
            id="",
            type=TestType.INTEGRATION,
            framework=self.config.framework,
            range=range,
            code=code,
            file_path=file_path,
            function_name=function_name
        )
        
        return self.add_test(test)
    
    def generate_e2e_test(self, range: TestRange, code: str, file_path: str) -> TestGenerationResult:
        """
        Generate E2E test.
        
        Args:
            range: Test range
            code: Test code
            file_path: File path
            
        Returns:
            TestGenerationResult: Generate result
        """
        if not self.config.generate_e2e_tests:
            result = TestGenerationResult(success=False)
            result.message = "E2E test generation disabled"
            return result
        
        test = GeneratedTest(
            id="",
            type=TestType.E2E,
            framework=self.config.framework,
            range=range,
            code=code,
            file_path=file_path
        )
        
        return self.add_test(test)
    
    def generate_performance_test(self, range: TestRange, code: str, file_path: str) -> TestGenerationResult:
        """
        Generate performance test.
        
        Args:
            range: Test range
            code: Test code
            file_path: File path
            
        Returns:
            TestGenerationResult: Generate result
        """
        if not self.config.generate_performance_tests:
            result = TestGenerationResult(success=False)
            result.message = "Performance test generation disabled"
            return result
        
        test = GeneratedTest(
            id="",
            type=TestType.PERFORMANCE,
            framework=self.config.framework,
            range=range,
            code=code,
            file_path=file_path
        )
        
        return self.add_test(test)
    
    def generate_security_test(self, range: TestRange, code: str, file_path: str) -> TestGenerationResult:
        """
        Generate security test.
        
        Args:
            range: Test range
            code: Test code
            file_path: File path
            
        Returns:
            TestGenerationResult: Generate result
        """
        if not self.config.generate_security_tests:
            result = TestGenerationResult(success=False)
            result.message = "Security test generation disabled"
            return result
        
        test = GeneratedTest(
            id="",
            type=TestType.SECURITY,
            framework=self.config.framework,
            range=range,
            code=code,
            file_path=file_path
        )
        
        return self.add_test(test)
    
    def get_tests_for_file(self, file_path: str) -> List[GeneratedTest]:
        """
        Get tests for specific file.
        
        Args:
            file_path: File path
            
        Returns:
            List[GeneratedTest]: Tests
        """
        return [t for t in self.tests.values() if t.file_path == file_path]
    
    def get_tests_for_function(self, function_name: str) -> List[GeneratedTest]:
        """
        Get tests for specific function.
        
        Args:
            function_name: Function name
            
        Returns:
            List[GeneratedTest]: Tests
        """
        return [t for t in self.tests.values() if t.function_name == function_name]
    
    def clear_tests(self) -> TestGenerationResult:
        """
        Clear all tests.
        
        Returns:
            TestGenerationResult: Clear result
        """
        result = TestGenerationResult(success=True)
        
        try:
            self.tests.clear()
            self.cache.clear()
            result.message = "All tests cleared"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def clear_tests_by_type(self, test_type: TestType) -> TestGenerationResult:
        """
        Clear tests by type.
        
        Args:
            test_type: Test type
            
        Returns:
            TestGenerationResult: Clear result
        """
        result = TestGenerationResult(success=True)
        
        try:
            to_remove = [id for id, t in self.tests.items() if t.type == test_type]
            for id in to_remove:
                del self.tests[id]
                if id in self.cache:
                    del self.cache[id]
            
            result.message = f"Cleared {len(to_remove)} {test_type.value} tests"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def set_test_enabled(self, test_id: str, enabled: bool) -> TestGenerationResult:
        """
        Set test enabled state.
        
        Args:
            test_id: Test ID
            enabled: Enabled state
            
        Returns:
            TestGenerationResult: Set result
        """
        result = TestGenerationResult(success=False)
        
        try:
            test = self.tests.get(test_id)
            if test:
                test.is_enabled = enabled
                result.success = True
                result.message = f"Test '{test_id}' {'enabled' if enabled else 'disabled'}"
            else:
                result.errors.append("Test not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def set_test_visible(self, test_id: str, visible: bool) -> TestGenerationResult:
        """
        Set test visible state.
        
        Args:
            test_id: Test ID
            visible: Visible state
            
        Returns:
            TestGenerationResult: Set result
        """
        result = TestGenerationResult(success=False)
        
        try:
            test = self.tests.get(test_id)
            if test:
                test.is_visible = visible
                result.success = True
                result.message = f"Test '{test_id}' {'visible' if visible else 'hidden'}"
            else:
                result.errors.append("Test not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def update_config(self, config: TestGenerationConfig) -> TestGenerationResult:
        """
        Update test generation configuration.
        
        Args:
            config: New configuration
            
        Returns:
            TestGenerationResult: Update result
        """
        result = TestGenerationResult(success=True)
        
        try:
            self.config = config
            result.message = "Config updated"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def get_config(self) -> TestGenerationConfig:
        """
        Get test generation configuration.
        
        Returns:
            TestGenerationConfig: Configuration
        """
        return self.config


if __name__ == "__main__":
    # Basit test
    config = TestGenerationConfig()
    manager = TestGenerationManager(config)
    
    # Test ekle
    range = TestRange(0, 0, 10, 0)
    result = manager.generate_unit_test(range, "def test_function(): pass", "test.py", "test_function")
    
    print(f"Test added: {result.message}")
    
    # Tüm testleri al
    tests = manager.get_all_tests()
    
    print(f"Total tests: {len(tests)}")
