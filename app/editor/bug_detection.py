"""
MuhammedAI Local Developer - Bug Detection
Bug detection system for code editor.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum


class BugSeverity(Enum):
    """Bug severity."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class BugCategory(Enum):
    """Bug category."""
    SYNTAX = "syntax"
    RUNTIME = "runtime"
    LOGIC = "logic"
    PERFORMANCE = "performance"
    SECURITY = "security"
    STYLE = "style"
    TYPE = "type"
    CUSTOM = "custom"


@dataclass
class BugRange:
    """Bug range."""
    start_line: int
    start_column: int
    end_line: int
    end_column: int


@dataclass
class Bug:
    """Bug detection result."""
    id: str
    category: BugCategory
    severity: BugSeverity
    range: BugRange
    message: str
    file_path: str
    is_enabled: bool = True
    is_visible: bool = True
    confidence: float = 0.0
    fix_suggestion: Optional[str] = None
    code_snippet: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class BugDetectionConfig:
    """Bug detection configuration."""
    enabled: bool = True
    show_syntax: bool = True
    show_runtime: bool = True
    show_logic: bool = True
    show_performance: bool = True
    show_security: bool = True
    show_style: bool = True
    show_type: bool = True
    min_severity: BugSeverity = BugSeverity.LOW
    min_confidence: float = 0.5
    auto_fix: bool = False
    max_bugs: int = 100
    enable_cache: bool = True


@dataclass
class BugDetectionResult:
    """Bug detection result."""
    success: bool
    bugs: List[Bug] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    message: Optional[str] = None


class BugDetectionManager:
    """
    Bug detection manager.
    
    Özellikler:
    - Syntax bugs
    - Runtime bugs
    - Logic bugs
    - Performance bugs
    - Security bugs
    - Style bugs
    - Type bugs
    - Custom bugs
    - Bug severity
    - Bug filtering
    - Bug confidence
    - Bug fixing
    - Bug caching
    - Bug scope
    - Bug context
    """
    
    def __init__(self, config: Optional[BugDetectionConfig] = None):
        """
        Initialize bug detection manager.
        
        Args:
            config: Bug detection configuration
        """
        self.config = config or BugDetectionConfig()
        self.bugs: Dict[str, Bug] = {}
        self.cache: Dict[str, Bug] = {}
        self.bug_id_counter = 0
        self._next_id()
    
    def _next_id(self) -> str:
        """
        Generate next bug ID.
        
        Returns:
            str: Bug ID
        """
        self.bug_id_counter += 1
        return f"bug_{self.bug_id_counter}"
    
    def add_bug(self, bug: Bug) -> BugDetectionResult:
        """
        Add a bug.
        
        Args:
            bug: Bug to add
            
        Returns:
            BugDetectionResult: Add result
        """
        result = BugDetectionResult(success=True)
        
        try:
            if not bug.id:
                bug.id = self._next_id()
            
            self.bugs[bug.id] = bug
            
            # Cache if enabled
            if self.config.enable_cache:
                self.cache[bug.id] = bug
            
            result.bugs = self.get_all_bugs()
            result.message = f"Bug '{bug.id}' added"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def remove_bug(self, bug_id: str) -> BugDetectionResult:
        """
        Remove a bug.
        
        Args:
            bug_id: Bug ID
            
        Returns:
            BugDetectionResult: Remove result
        """
        result = BugDetectionResult(success=False)
        
        try:
            if bug_id in self.bugs:
                del self.bugs[bug_id]
                if bug_id in self.cache:
                    del self.cache[bug_id]
                result.success = True
                result.bugs = self.get_all_bugs()
                result.message = f"Bug '{bug_id}' removed"
            else:
                result.errors.append("Bug not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_bug(self, bug_id: str) -> Optional[Bug]:
        """
        Get bug by ID.
        
        Args:
            bug_id: Bug ID
            
        Returns:
            Optional[Bug]: Bug
        """
        return self.bugs.get(bug_id)
    
    def get_all_bugs(self) -> List[Bug]:
        """
        Get all bugs.
        
        Returns:
            List[Bug]: All bugs
        """
        return list(self.bugs.values())
    
    def get_bugs_by_category(self, category: BugCategory) -> List[Bug]:
        """
        Get bugs by category.
        
        Args:
            category: Bug category
            
        Returns:
            List[Bug]: Bugs
        """
        return [b for b in self.bugs.values() if b.category == category]
    
    def get_bugs_by_severity(self, severity: BugSeverity) -> List[Bug]:
        """
        Get bugs by severity.
        
        Args:
            severity: Bug severity
            
        Returns:
            List[Bug]: Bugs
        """
        return [b for b in self.bugs.values() if b.severity == severity]
    
    def add_syntax_bug(self, range: BugRange, message: str, file_path: str, confidence: float = 0.9) -> BugDetectionResult:
        """
        Add syntax bug.
        
        Args:
            range: Bug range
            message: Bug message
            file_path: File path
            confidence: Confidence score
            
        Returns:
            BugDetectionResult: Add result
        """
        if not self.config.show_syntax:
            result = BugDetectionResult(success=False)
            result.message = "Syntax bugs disabled"
            return result
        
        bug = Bug(
            id="",
            category=BugCategory.SYNTAX,
            severity=BugSeverity.CRITICAL,
            range=range,
            message=message,
            file_path=file_path,
            confidence=confidence
        )
        
        return self.add_bug(bug)
    
    def add_runtime_bug(self, range: BugRange, message: str, file_path: str, severity: BugSeverity = BugSeverity.HIGH, confidence: float = 0.8) -> BugDetectionResult:
        """
        Add runtime bug.
        
        Args:
            range: Bug range
            message: Bug message
            file_path: File path
            severity: Bug severity
            confidence: Confidence score
            
        Returns:
            BugDetectionResult: Add result
        """
        if not self.config.show_runtime:
            result = BugDetectionResult(success=False)
            result.message = "Runtime bugs disabled"
            return result
        
        bug = Bug(
            id="",
            category=BugCategory.RUNTIME,
            severity=severity,
            range=range,
            message=message,
            file_path=file_path,
            confidence=confidence
        )
        
        return self.add_bug(bug)
    
    def add_logic_bug(self, range: BugRange, message: str, file_path: str, severity: BugSeverity = BugSeverity.MEDIUM, confidence: float = 0.7) -> BugDetectionResult:
        """
        Add logic bug.
        
        Args:
            range: Bug range
            message: Bug message
            file_path: File path
            severity: Bug severity
            confidence: Confidence score
            
        Returns:
            BugDetectionResult: Add result
        """
        if not self.config.show_logic:
            result = BugDetectionResult(success=False)
            result.message = "Logic bugs disabled"
            return result
        
        bug = Bug(
            id="",
            category=BugCategory.LOGIC,
            severity=severity,
            range=range,
            message=message,
            file_path=file_path,
            confidence=confidence
        )
        
        return self.add_bug(bug)
    
    def add_performance_bug(self, range: BugRange, message: str, file_path: str, confidence: float = 0.7) -> BugDetectionResult:
        """
        Add performance bug.
        
        Args:
            range: Bug range
            message: Bug message
            file_path: File path
            confidence: Confidence score
            
        Returns:
            BugDetectionResult: Add result
        """
        if not self.config.show_performance:
            result = BugDetectionResult(success=False)
            result.message = "Performance bugs disabled"
            return result
        
        bug = Bug(
            id="",
            category=BugCategory.PERFORMANCE,
            severity=BugSeverity.MEDIUM,
            range=range,
            message=message,
            file_path=file_path,
            confidence=confidence
        )
        
        return self.add_bug(bug)
    
    def add_security_bug(self, range: BugRange, message: str, file_path: str, severity: BugSeverity = BugSeverity.HIGH, confidence: float = 0.8) -> BugDetectionResult:
        """
        Add security bug.
        
        Args:
            range: Bug range
            message: Bug message
            file_path: File path
            severity: Bug severity
            confidence: Confidence score
            
        Returns:
            BugDetectionResult: Add result
        """
        if not self.config.show_security:
            result = BugDetectionResult(success=False)
            result.message = "Security bugs disabled"
            return result
        
        bug = Bug(
            id="",
            category=BugCategory.SECURITY,
            severity=severity,
            range=range,
            message=message,
            file_path=file_path,
            confidence=confidence
        )
        
        return self.add_bug(bug)
    
    def add_style_bug(self, range: BugRange, message: str, file_path: str, confidence: float = 0.6) -> BugDetectionResult:
        """
        Add style bug.
        
        Args:
            range: Bug range
            message: Bug message
            file_path: File path
            confidence: Confidence score
            
        Returns:
            BugDetectionResult: Add result
        """
        if not self.config.show_style:
            result = BugDetectionResult(success=False)
            result.message = "Style bugs disabled"
            return result
        
        bug = Bug(
            id="",
            category=BugCategory.STYLE,
            severity=BugSeverity.LOW,
            range=range,
            message=message,
            file_path=file_path,
            confidence=confidence
        )
        
        return self.add_bug(bug)
    
    def add_type_bug(self, range: BugRange, message: str, file_path: str, severity: BugSeverity = BugSeverity.MEDIUM, confidence: float = 0.8) -> BugDetectionResult:
        """
        Add type bug.
        
        Args:
            range: Bug range
            message: Bug message
            file_path: File path
            severity: Bug severity
            confidence: Confidence score
            
        Returns:
            BugDetectionResult: Add result
        """
        if not self.config.show_type:
            result = BugDetectionResult(success=False)
            result.message = "Type bugs disabled"
            return result
        
        bug = Bug(
            id="",
            category=BugCategory.TYPE,
            severity=severity,
            range=range,
            message=message,
            file_path=file_path,
            confidence=confidence
        )
        
        return self.add_bug(bug)
    
    def filter_by_severity(self, min_severity: BugSeverity) -> List[Bug]:
        """
        Filter bugs by severity.
        
        Args:
            min_severity: Minimum severity
            
        Returns:
            List[Bug]: Filtered bugs
        """
        severity_order = {
            BugSeverity.INFO: 0,
            BugSeverity.LOW: 1,
            BugSeverity.MEDIUM: 2,
            BugSeverity.HIGH: 3,
            BugSeverity.CRITICAL: 4
        }
        
        min_level = severity_order.get(min_severity, 0)
        return [b for b in self.bugs.values() if severity_order.get(b.severity, 0) >= min_level]
    
    def filter_by_confidence(self, min_confidence: float) -> List[Bug]:
        """
        Filter bugs by confidence.
        
        Args:
            min_confidence: Minimum confidence
            
        Returns:
            List[Bug]: Filtered bugs
        """
        return [b for b in self.bugs.values() if b.confidence >= min_confidence]
    
    def get_bugs_in_file(self, file_path: str) -> List[Bug]:
        """
        Get bugs in specific file.
        
        Args:
            file_path: File path
            
        Returns:
            List[Bug]: Bugs
        """
        return [b for b in self.bugs.values() if b.file_path == file_path]
    
    def get_bugs_at_line(self, file_path: str, line: int) -> List[Bug]:
        """
        Get bugs at specific line.
        
        Args:
            file_path: File path
            line: Line number
            
        Returns:
            List[Bug]: Bugs
        """
        return [b for b in self.bugs.values() if b.file_path == file_path and b.range.start_line <= line <= b.range.end_line]
    
    def clear_bugs(self) -> BugDetectionResult:
        """
        Clear all bugs.
        
        Returns:
            BugDetectionResult: Clear result
        """
        result = BugDetectionResult(success=True)
        
        try:
            self.bugs.clear()
            self.cache.clear()
            result.message = "All bugs cleared"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def clear_bugs_by_category(self, category: BugCategory) -> BugDetectionResult:
        """
        Clear bugs by category.
        
        Args:
            category: Bug category
            
        Returns:
            BugDetectionResult: Clear result
        """
        result = BugDetectionResult(success=True)
        
        try:
            to_remove = [id for id, b in self.bugs.items() if b.category == category]
            for id in to_remove:
                del self.bugs[id]
                if id in self.cache:
                    del self.cache[id]
            
            result.message = f"Cleared {len(to_remove)} {category.value} bugs"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def set_bug_enabled(self, bug_id: str, enabled: bool) -> BugDetectionResult:
        """
        Set bug enabled state.
        
        Args:
            bug_id: Bug ID
            enabled: Enabled state
            
        Returns:
            BugDetectionResult: Set result
        """
        result = BugDetectionResult(success=False)
        
        try:
            bug = self.bugs.get(bug_id)
            if bug:
                bug.is_enabled = enabled
                result.success = True
                result.message = f"Bug '{bug_id}' {'enabled' if enabled else 'disabled'}"
            else:
                result.errors.append("Bug not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def set_bug_visible(self, bug_id: str, visible: bool) -> BugDetectionResult:
        """
        Set bug visible state.
        
        Args:
            bug_id: Bug ID
            visible: Visible state
            
        Returns:
            BugDetectionResult: Set result
        """
        result = BugDetectionResult(success=False)
        
        try:
            bug = self.bugs.get(bug_id)
            if bug:
                bug.is_visible = visible
                result.success = True
                result.message = f"Bug '{bug_id}' {'visible' if visible else 'hidden'}"
            else:
                result.errors.append("Bug not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def update_config(self, config: BugDetectionConfig) -> BugDetectionResult:
        """
        Update bug detection configuration.
        
        Args:
            config: New configuration
            
        Returns:
            BugDetectionResult: Update result
        """
        result = BugDetectionResult(success=True)
        
        try:
            self.config = config
            result.message = "Config updated"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def get_config(self) -> BugDetectionConfig:
        """
        Get bug detection configuration.
        
        Returns:
            BugDetectionConfig: Configuration
        """
        return self.config


if __name__ == "__main__":
    # Basit test
    config = BugDetectionConfig()
    manager = BugDetectionManager(config)
    
    # Bug ekle
    range = BugRange(0, 0, 0, 10)
    result = manager.add_syntax_bug(range, "Syntax error", "test.py", 0.9)
    
    print(f"Bug added: {result.message}")
    
    # Tüm bug'ları al
    bugs = manager.get_all_bugs()
    
    print(f"Total bugs: {len(bugs)}")
