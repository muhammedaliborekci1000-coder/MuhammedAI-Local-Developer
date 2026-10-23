"""
MuhammedAI Local Developer - Code Explanation
Code explanation system for code editor.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum


class ExplanationType(Enum):
    """Explanation type."""
    FUNCTION = "function"
    CLASS = "class"
    VARIABLE = "variable"
    MODULE = "module"
    LINE = "line"
    BLOCK = "block"
    CUSTOM = "custom"


class ExplanationFormat(Enum):
    """Explanation format."""
    PLAIN_TEXT = "plain_text"
    MARKDOWN = "markdown"
    HTML = "html"
    RICH_TEXT = "rich_text"


@dataclass
class ExplanationRange:
    """Explanation range."""
    start_line: int
    start_column: int
    end_line: int
    end_column: int


@dataclass
class CodeExplanation:
    """Code explanation."""
    id: str
    type: ExplanationType
    range: ExplanationRange
    text: str
    format: ExplanationFormat = ExplanationFormat.PLAIN_TEXT
    is_enabled: bool = True
    is_visible: bool = True
    confidence: float = 0.0
    language: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ExplanationConfig:
    """Explanation configuration."""
    enabled: bool = True
    format: ExplanationFormat = ExplanationFormat.MARKDOWN
    show_functions: bool = True
    show_classes: bool = True
    show_variables: bool = True
    show_modules: bool = True
    show_lines: bool = True
    show_blocks: bool = True
    auto_generate: bool = True
    min_confidence: float = 0.5
    max_explanations: int = 100
    enable_cache: bool = True


@dataclass
class ExplanationResult:
    """Explanation result."""
    success: bool
    explanation: Optional[CodeExplanation] = None
    explanations: List[CodeExplanation] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    message: Optional[str] = None


class CodeExplanationManager:
    """
    Code explanation manager.
    
    Özellikler:
    - Function explanations
    - Class explanations
    - Variable explanations
    - Module explanations
    - Line explanations
    - Block explanations
    - Custom explanations
    - Explanation formats
    - Explanation filtering
    - Explanation confidence
    - Explanation caching
    - Explanation scope
    - Explanation context
    """
    
    def __init__(self, config: Optional[ExplanationConfig] = None):
        """
        Initialize code explanation manager.
        
        Args:
            config: Explanation configuration
        """
        self.config = config or ExplanationConfig()
        self.explanations: Dict[str, CodeExplanation] = {}
        self.cache: Dict[str, CodeExplanation] = {}
        self.explanation_id_counter = 0
        self._next_id()
    
    def _next_id(self) -> str:
        """
        Generate next explanation ID.
        
        Returns:
            str: Explanation ID
        """
        self.explanation_id_counter += 1
        return f"explanation_{self.explanation_id_counter}"
    
    def add_explanation(self, explanation: CodeExplanation) -> ExplanationResult:
        """
        Add an explanation.
        
        Args:
            explanation: Explanation to add
            
        Returns:
            ExplanationResult: Add result
        """
        result = ExplanationResult(success=True)
        
        try:
            if not explanation.id:
                explanation.id = self._next_id()
            
            self.explanations[explanation.id] = explanation
            
            # Cache if enabled
            if self.config.enable_cache:
                self.cache[explanation.id] = explanation
            
            result.explanation = explanation
            result.explanations = self.get_all_explanations()
            result.message = f"Explanation '{explanation.id}' added"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def remove_explanation(self, explanation_id: str) -> ExplanationResult:
        """
        Remove an explanation.
        
        Args:
            explanation_id: Explanation ID
            
        Returns:
            ExplanationResult: Remove result
        """
        result = ExplanationResult(success=False)
        
        try:
            if explanation_id in self.explanations:
                del self.explanations[explanation_id]
                if explanation_id in self.cache:
                    del self.cache[explanation_id]
                result.success = True
                result.explanations = self.get_all_explanations()
                result.message = f"Explanation '{explanation_id}' removed"
            else:
                result.errors.append("Explanation not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_explanation(self, explanation_id: str) -> Optional[CodeExplanation]:
        """
        Get explanation by ID.
        
        Args:
            explanation_id: Explanation ID
            
        Returns:
            Optional[CodeExplanation]: Explanation
        """
        return self.explanations.get(explanation_id)
    
    def get_all_explanations(self) -> List[CodeExplanation]:
        """
        Get all explanations.
        
        Returns:
            List[CodeExplanation]: All explanations
        """
        return list(self.explanations.values())
    
    def get_explanations_by_type(self, explanation_type: ExplanationType) -> List[CodeExplanation]:
        """
        Get explanations by type.
        
        Args:
            explanation_type: Explanation type
            
        Returns:
            List[CodeExplanation]: Explanations
        """
        return [e for e in self.explanations.values() if e.type == explanation_type]
    
    def add_function_explanation(self, range: ExplanationRange, text: str, confidence: float = 0.8) -> ExplanationResult:
        """
        Add function explanation.
        
        Args:
            range: Explanation range
            text: Explanation text
            confidence: Confidence score
            
        Returns:
            ExplanationResult: Add result
        """
        if not self.config.show_functions:
            result = ExplanationResult(success=False)
            result.message = "Function explanations disabled"
            return result
        
        explanation = CodeExplanation(
            id="",
            type=ExplanationType.FUNCTION,
            range=range,
            text=text,
            format=self.config.format,
            confidence=confidence
        )
        
        return self.add_explanation(explanation)
    
    def add_class_explanation(self, range: ExplanationRange, text: str, confidence: float = 0.8) -> ExplanationResult:
        """
        Add class explanation.
        
        Args:
            range: Explanation range
            text: Explanation text
            confidence: Confidence score
            
        Returns:
            ExplanationResult: Add result
        """
        if not self.config.show_classes:
            result = ExplanationResult(success=False)
            result.message = "Class explanations disabled"
            return result
        
        explanation = CodeExplanation(
            id="",
            type=ExplanationType.CLASS,
            range=range,
            text=text,
            format=self.config.format,
            confidence=confidence
        )
        
        return self.add_explanation(explanation)
    
    def add_variable_explanation(self, range: ExplanationRange, text: str, confidence: float = 0.7) -> ExplanationResult:
        """
        Add variable explanation.
        
        Args:
            range: Explanation range
            text: Explanation text
            confidence: Confidence score
            
        Returns:
            ExplanationResult: Add result
        """
        if not self.config.show_variables:
            result = ExplanationResult(success=False)
            result.message = "Variable explanations disabled"
            return result
        
        explanation = CodeExplanation(
            id="",
            type=ExplanationType.VARIABLE,
            range=range,
            text=text,
            format=self.config.format,
            confidence=confidence
        )
        
        return self.add_explanation(explanation)
    
    def add_module_explanation(self, range: ExplanationRange, text: str, confidence: float = 0.8) -> ExplanationResult:
        """
        Add module explanation.
        
        Args:
            range: Explanation range
            text: Explanation text
            confidence: Confidence score
            
        Returns:
            ExplanationResult: Add result
        """
        if not self.config.show_modules:
            result = ExplanationResult(success=False)
            result.message = "Module explanations disabled"
            return result
        
        explanation = CodeExplanation(
            id="",
            type=ExplanationType.MODULE,
            range=range,
            text=text,
            format=self.config.format,
            confidence=confidence
        )
        
        return self.add_explanation(explanation)
    
    def add_line_explanation(self, range: ExplanationRange, text: str, confidence: float = 0.6) -> ExplanationResult:
        """
        Add line explanation.
        
        Args:
            range: Explanation range
            text: Explanation text
            confidence: Confidence score
            
        Returns:
            ExplanationResult: Add result
        """
        if not self.config.show_lines:
            result = ExplanationResult(success=False)
            result.message = "Line explanations disabled"
            return result
        
        explanation = CodeExplanation(
            id="",
            type=ExplanationType.LINE,
            range=range,
            text=text,
            format=self.config.format,
            confidence=confidence
        )
        
        return self.add_explanation(explanation)
    
    def add_block_explanation(self, range: ExplanationRange, text: str, confidence: float = 0.7) -> ExplanationResult:
        """
        Add block explanation.
        
        Args:
            range: Explanation range
            text: Explanation text
            confidence: Confidence score
            
        Returns:
            ExplanationResult: Add result
        """
        if not self.config.show_blocks:
            result = ExplanationResult(success=False)
            result.message = "Block explanations disabled"
            return result
        
        explanation = CodeExplanation(
            id="",
            type=ExplanationType.BLOCK,
            range=range,
            text=text,
            format=self.config.format,
            confidence=confidence
        )
        
        return self.add_explanation(explanation)
    
    def filter_by_confidence(self, min_confidence: float) -> List[CodeExplanation]:
        """
        Filter explanations by confidence.
        
        Args:
            min_confidence: Minimum confidence
            
        Returns:
            List[CodeExplanation]: Filtered explanations
        """
        return [e for e in self.explanations.values() if e.confidence >= min_confidence]
    
    def get_explanations_at_line(self, line: int) -> List[CodeExplanation]:
        """
        Get explanations at specific line.
        
        Args:
            line: Line number
            
        Returns:
            List[CodeExplanation]: Explanations
        """
        return [e for e in self.explanations.values() if e.range.start_line <= line <= e.range.end_line]
    
    def clear_explanations(self) -> ExplanationResult:
        """
        Clear all explanations.
        
        Returns:
            ExplanationResult: Clear result
        """
        result = ExplanationResult(success=True)
        
        try:
            self.explanations.clear()
            self.cache.clear()
            result.message = "All explanations cleared"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def clear_explanations_by_type(self, explanation_type: ExplanationType) -> ExplanationResult:
        """
        Clear explanations by type.
        
        Args:
            explanation_type: Explanation type
            
        Returns:
            ExplanationResult: Clear result
        """
        result = ExplanationResult(success=True)
        
        try:
            to_remove = [id for id, e in self.explanations.items() if e.type == explanation_type]
            for id in to_remove:
                del self.explanations[id]
                if id in self.cache:
                    del self.cache[id]
            
            result.message = f"Cleared {len(to_remove)} {explanation_type.value} explanations"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def set_explanation_enabled(self, explanation_id: str, enabled: bool) -> ExplanationResult:
        """
        Set explanation enabled state.
        
        Args:
            explanation_id: Explanation ID
            enabled: Enabled state
            
        Returns:
            ExplanationResult: Set result
        """
        result = ExplanationResult(success=False)
        
        try:
            explanation = self.explanations.get(explanation_id)
            if explanation:
                explanation.is_enabled = enabled
                result.success = True
                result.message = f"Explanation '{explanation_id}' {'enabled' if enabled else 'disabled'}"
            else:
                result.errors.append("Explanation not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def set_explanation_visible(self, explanation_id: str, visible: bool) -> ExplanationResult:
        """
        Set explanation visible state.
        
        Args:
            explanation_id: Explanation ID
            visible: Visible state
            
        Returns:
            ExplanationResult: Set result
        """
        result = ExplanationResult(success=False)
        
        try:
            explanation = self.explanations.get(explanation_id)
            if explanation:
                explanation.is_visible = visible
                result.success = True
                result.message = f"Explanation '{explanation_id}' {'visible' if visible else 'hidden'}"
            else:
                result.errors.append("Explanation not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def update_config(self, config: ExplanationConfig) -> ExplanationResult:
        """
        Update explanation configuration.
        
        Args:
            config: New configuration
            
        Returns:
            ExplanationResult: Update result
        """
        result = ExplanationResult(success=True)
        
        try:
            self.config = config
            result.message = "Config updated"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def get_config(self) -> ExplanationConfig:
        """
        Get explanation configuration.
        
        Returns:
            ExplanationConfig: Configuration
        """
        return self.config


if __name__ == "__main__":
    # Basit test
    config = ExplanationConfig()
    manager = CodeExplanationManager(config)
    
    # Explanation ekle
    range = ExplanationRange(0, 0, 10, 0)
    result = manager.add_function_explanation(range, "This function does X", 0.8)
    
    print(f"Explanation added: {result.message}")
    
    # Tüm explanation'ları al
    explanations = manager.get_all_explanations()
    
    print(f"Total explanations: {len(explanations)}")
