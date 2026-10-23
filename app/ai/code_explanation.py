"""
MuhammedAI Local Developer - Code Explanation
Automatic code explanation and analysis.
"""

import ast
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from enum import Enum


class ExplanationType(Enum):
    """Explanation type."""
    FUNCTION = "function"
    CLASS = "class"
    MODULE = "module"
    LINE = "line"
    CONCEPT = "concept"


class ExplanationDetail(Enum):
    """Explanation detail level."""
    SIMPLE = "simple"
    DETAILED = "detailed"
    TECHNICAL = "technical"


@dataclass
class CodeExplanation:
    """Code explanation."""
    type: ExplanationType
    detail: ExplanationDetail
    summary: str
    description: str
    complexity: Optional[str] = None
    data_flow: Optional[str] = None
    examples: List[str] = field(default_factory=list)
    related_concepts: List[str] = field(default_factory=list)


@dataclass
class ExplanationResult:
    """Explanation result."""
    success: bool
    explanation: Optional[CodeExplanation] = None
    file_path: Optional[str] = None
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    message: Optional[str] = None


class CodeExplainer:
    """
    Code explanation engine.
    
    Özellikler:
    - Function explanation
    - Class explanation
    - Module explanation
    - Line-by-line explanation
    - Concept explanation
    - Complexity analysis
    - Data flow analysis
    - Example generation
    """
    
    def __init__(self, detail: ExplanationDetail = ExplanationDetail.DETAILED):
        """
        Args:
            detail: Explanation detail level
        """
        self.detail = detail
    
    def explain_function(
        self,
        function_name: str,
        file_path: str
    ) -> ExplanationResult:
        """
        Function açıklaması oluştur.
        
        Args:
            function_name: Function adı
            file_path: Dosya yolu
            
        Returns:
            ExplanationResult: Explanation sonucu
        """
        result = ExplanationResult(success=False)
        result.file_path = file_path
        
        try:
            # Dosyayı oku
            content = Path(file_path).read_text(encoding='utf-8')
            
            # AST parse
            tree = ast.parse(content)
            
            # Function'ı bul
            func_node = self._find_function(tree, function_name)
            
            if func_node is None:
                result.errors.append(f"Function '{function_name}' not found")
                return result
            
            # Explanation oluştur
            explanation = self._generate_function_explanation(func_node, content)
            
            result.explanation = explanation
            result.success = True
            result.message = f"Explanation generated for '{function_name}'"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def explain_class(
        self,
        class_name: str,
        file_path: str
    ) -> ExplanationResult:
        """
        Class açıklaması oluştur.
        
        Args:
            class_name: Class adı
            file_path: Dosya yolu
            
        Returns:
            ExplanationResult: Explanation sonucu
        """
        result = ExplanationResult(success=False)
        result.file_path = file_path
        
        try:
            # Dosyayı oku
            content = Path(file_path).read_text(encoding='utf-8')
            
            # AST parse
            tree = ast.parse(content)
            
            # Class'ı bul
            class_node = self._find_class(tree, class_name)
            
            if class_node is None:
                result.errors.append(f"Class '{class_name}' not found")
                return result
            
            # Explanation oluştur
            explanation = self._generate_class_explanation(class_node, content)
            
            result.explanation = explanation
            result.success = True
            result.message = f"Explanation generated for '{class_name}'"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def explain_module(
        self,
        file_path: str
    ) -> ExplanationResult:
        """
        Module açıklaması oluştur.
        
        Args:
            file_path: Dosya yolu
            
        Returns:
            ExplanationResult: Explanation sonucu
        """
        result = ExplanationResult(success=False)
        result.file_path = file_path
        
        try:
            # Dosyayı oku
            content = Path(file_path).read_text(encoding='utf-8')
            
            # AST parse
            tree = ast.parse(content)
            
            # Explanation oluştur
            explanation = self._generate_module_explanation(tree, content, file_path)
            
            result.explanation = explanation
            result.success = True
            result.message = "Module explanation generated"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def explain_line(
        self,
        file_path: str,
        line: int
    ) -> ExplanationResult:
        """
        Satır açıklaması oluştur.
        
        Args:
            file_path: Dosya yolu
            line: Satır numarası
            
        Returns:
            ExplanationResult: Explanation sonucu
        """
        result = ExplanationResult(success=False)
        result.file_path = file_path
        
        try:
            # Dosyayı oku
            content = Path(file_path).read_text(encoding='utf-8')
            lines = content.splitlines()
            
            if line < 1 or line > len(lines):
                result.errors.append(f"Line {line} out of range")
                return result
            
            line_content = lines[line - 1]
            
            # Explanation oluştur
            explanation = self._generate_line_explanation(line_content, line)
            
            result.explanation = explanation
            result.success = True
            result.message = f"Line {line} explanation generated"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def _find_function(
        self,
        tree: ast.AST,
        function_name: str
    ) -> Optional[ast.FunctionDef]:
        """Function'ı bul."""
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == function_name:
                return node
        return None
    
    def _find_class(
        self,
        tree: ast.AST,
        class_name: str
    ) -> Optional[ast.ClassDef]:
        """Class'ı bul."""
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == class_name:
                return node
        return None
    
    def _generate_function_explanation(
        self,
        node: ast.FunctionDef,
        content: str
    ) -> CodeExplanation:
        """Function explanation oluştur."""
        args = [arg.arg for arg in node.args.args]
        returns = ast.unparse(node.returns) if node.returns else "None"
        
        summary = f"Function '{node.name}' takes {len(args)} argument(s) and returns {returns}"
        
        description = f"""
This function performs the following operations:
- Accepts parameters: {', '.join(args)}
- Returns: {returns}
- Complexity: {self._calculate_complexity(node)}
"""
        
        complexity = self._calculate_complexity(node)
        data_flow = self._analyze_data_flow(node)
        
        return CodeExplanation(
            type=ExplanationType.FUNCTION,
            detail=self.detail,
            summary=summary,
            description=description,
            complexity=complexity,
            data_flow=data_flow
        )
    
    def _generate_class_explanation(
        self,
        node: ast.ClassDef,
        content: str
    ) -> CodeExplanation:
        """Class explanation oluştur."""
        methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
        
        summary = f"Class '{node.name}' with {len(methods)} method(s)"
        
        description = f"""
This class provides the following functionality:
- Methods: {', '.join(methods)}
- Purpose: {self._infer_class_purpose(node)}
"""
        
        return CodeExplanation(
            type=ExplanationType.CLASS,
            detail=self.detail,
            summary=summary,
            description=description,
            related_concepts=methods
        )
    
    def _generate_module_explanation(
        self,
        tree: ast.AST,
        content: str,
        file_path: str
    ) -> CodeExplanation:
        """Module explanation oluştur."""
        module_name = Path(file_path).stem
        
        functions = []
        classes = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions.append(node.name)
            elif isinstance(node, ast.ClassDef):
                classes.append(node.name)
        
        summary = f"Module '{module_name}' with {len(functions)} function(s) and {len(classes)} class(es)"
        
        description = f"""
This module contains:
- Functions: {', '.join(functions)}
- Classes: {', '.join(classes)}
"""
        
        return CodeExplanation(
            type=ExplanationType.MODULE,
            detail=self.detail,
            summary=summary,
            description=description,
            related_concepts=functions + classes
        )
    
    def _generate_line_explanation(
        self,
        line_content: str,
        line: int
    ) -> CodeExplanation:
        """Satır explanation oluştur."""
        summary = f"Line {line}: {line_content.strip()[:50]}..."
        
        description = f"""
This line performs the following action:
{self._analyze_line(line_content)}
"""
        
        return CodeExplanation(
            type=ExplanationType.LINE,
            detail=self.detail,
            summary=summary,
            description=description
        )
    
    def _calculate_complexity(self, node: ast.AST) -> str:
        """Complexity hesapla."""
        complexity = 1
        
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.For, ast.While, ast.Try)):
                complexity += 1
        
        if complexity <= 3:
            return "Low"
        elif complexity <= 7:
            return "Medium"
        else:
            return "High"
    
    def _analyze_data_flow(self, node: ast.FunctionDef) -> str:
        """Data flow analizi."""
        args = [arg.arg for arg in node.args.args]
        return f"Input: {', '.join(args)} -> Processing -> Output"
    
    def _infer_class_purpose(self, node: ast.ClassDef) -> str:
        """Class amacını çıkar."""
        return "Provides functionality for " + node.name.lower()
    
    def _analyze_line(self, line: str) -> str:
        """Satır analizi."""
        if "def " in line:
            return "Defines a function"
        elif "class " in line:
            return "Defines a class"
        elif "if " in line:
            return "Conditional statement"
        elif "for " in line:
            return "Loop iteration"
        elif "return " in line:
            return "Returns a value"
        elif "=" in line:
            return "Variable assignment"
        else:
            return "Statement execution"


if __name__ == "__main__":
    # Basit test
    explainer = CodeExplainer()
    
    result = explainer.explain_module("app/ai/code_explanation.py")
    print(f"Code explanation: {result.success}")
    print(f"Message: {result.message}")
    if result.explanation:
        print(f"Summary: {result.explanation.summary}")
