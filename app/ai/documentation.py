"""
MuhammedAI Local Developer - Documentation
Automatic documentation generation for code.
"""

import ast
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from enum import Enum


class DocumentationType(Enum):
    """Documentation type."""
    DOCSTRING = "docstring"
    MARKDOWN = "markdown"
    API = "api"
    README = "readme"


class DocStyle(Enum):
    """Documentation style."""
    GOOGLE = "google"
    NUMPY = "numpy"
    SPHINX = "sphinx"
    PEP257 = "pep257"


@dataclass
class DocTemplate:
    """Documentation template."""
    name: str
    description: str
    template: str
    style: DocStyle


@dataclass
class DocumentationResult:
    """Documentation generation result."""
    success: bool
    documentation: Optional[str] = None
    file_path: Optional[str] = None
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    message: Optional[str] = None


class DocumentationGenerator:
    """
    Documentation generation engine.
    
    Özellikler:
    - Auto-generate docstrings
    - Function/method documentation
    - Class documentation
    - Module documentation
    - Parameter documentation
    - Return type documentation
    - Example code generation
    - Markdown documentation
    - API documentation
    - Multiple doc styles
    """
    
    def __init__(self, style: DocStyle = DocStyle.GOOGLE):
        """
        Args:
            style: Documentation style
        """
        self.style = style
    
    def generate_docstring(
        self,
        file_path: str,
        line: int,
        column: int
    ) -> DocumentationResult:
        """
        Docstring oluştur.
        
        Args:
            file_path: Dosya yolu
            line: Satır numarası
            column: Sütun numarası
            
        Returns:
            DocumentationResult: Documentation sonucu
        """
        result = DocumentationResult(success=False)
        
        try:
            # Dosyayı oku
            content = Path(file_path).read_text(encoding='utf-8')
            
            # AST parse
            tree = ast.parse(content)
            
            # Node'u bul
            node = self._find_node_at_position(tree, line, column)
            
            if node is None:
                result.errors.append("No node found at position")
                return result
            
            # Docstring oluştur
            docstring = self._generate_node_docstring(node)
            
            result.documentation = docstring
            result.success = True
            result.message = "Docstring generated successfully"
            result.file_path = file_path
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def generate_function_docs(
        self,
        function_name: str,
        file_path: str
    ) -> DocumentationResult:
        """
        Function documentation oluştur.
        
        Args:
            function_name: Function adı
            file_path: Dosya yolu
            
        Returns:
            DocumentationResult: Documentation sonucu
        """
        result = DocumentationResult(success=False)
        
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
            
            # Documentation oluştur
            docs = self._generate_function_documentation(func_node)
            
            result.documentation = docs
            result.success = True
            result.message = f"Documentation generated for '{function_name}'"
            result.file_path = file_path
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def generate_class_docs(
        self,
        class_name: str,
        file_path: str
    ) -> DocumentationResult:
        """
        Class documentation oluştur.
        
        Args:
            class_name: Class adı
            file_path: Dosya yolu
            
        Returns:
            DocumentationResult: Documentation sonucu
        """
        result = DocumentationResult(success=False)
        
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
            
            # Documentation oluştur
            docs = self._generate_class_documentation(class_node)
            
            result.documentation = docs
            result.success = True
            result.message = f"Documentation generated for '{class_name}'"
            result.file_path = file_path
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def generate_module_docs(
        self,
        file_path: str
    ) -> DocumentationResult:
        """
        Module documentation oluştur.
        
        Args:
            file_path: Dosya yolu
            
        Returns:
            DocumentationResult: Documentation sonucu
        """
        result = DocumentationResult(success=False)
        
        try:
            # Dosyayı oku
            content = Path(file_path).read_text(encoding='utf-8')
            
            # AST parse
            tree = ast.parse(content)
            
            # Module documentation oluştur
            docs = self._generate_module_documentation(tree, file_path)
            
            result.documentation = docs
            result.success = True
            result.message = "Module documentation generated"
            result.file_path = file_path
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def generate_markdown_docs(
        self,
        file_path: str
    ) -> DocumentationResult:
        """
        Markdown documentation oluştur.
        
        Args:
            file_path: Dosya yolu
            
        Returns:
            DocumentationResult: Documentation sonucu
        """
        result = DocumentationResult(success=False)
        
        try:
            # Dosyayı oku
            content = Path(file_path).read_text(encoding='utf-8')
            
            # AST parse
            tree = ast.parse(content)
            
            # Markdown documentation oluştur
            docs = self._generate_markdown_documentation(tree, file_path)
            
            result.documentation = docs
            result.success = True
            result.message = "Markdown documentation generated"
            result.file_path = file_path
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def _find_node_at_position(
        self,
        tree: ast.AST,
        line: int,
        column: int
    ) -> Optional[ast.AST]:
        """Position'daki node'u bul."""
        for node in ast.walk(tree):
            if hasattr(node, 'lineno') and node.lineno == line:
                return node
        return None
    
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
    
    def _generate_node_docstring(self, node: ast.AST) -> str:
        """Node için docstring oluştur."""
        if isinstance(node, ast.FunctionDef):
            return self._generate_function_docstring(node)
        elif isinstance(node, ast.ClassDef):
            return self._generate_class_docstring(node)
        else:
            return "# Documentation"
    
    def _generate_function_docstring(self, node: ast.FunctionDef) -> str:
        """Function için docstring oluştur."""
        args = [arg.arg for arg in node.args.args]
        returns = ast.unparse(node.returns) if node.returns else "None"
        
        if self.style == DocStyle.GOOGLE:
            docstring = f'''"""
Brief description of function.

Args:
{chr(10).join([f"    {arg}: Description of {arg}." for arg in args])}

Returns:
    {returns}: Description of return value.
"""'''
        elif self.style == DocStyle.NUMPY:
            docstring = f'''"""
Brief description of function.

Parameters
----------
{chr(10).join([f"{arg} : type" + chr(10) + "    Description of " + arg for arg in args])}

Returns
-------
{returns}
    Description of return value.
"""'''
        else:
            docstring = f'''"""Brief description of function.

Args:
{chr(10).join([f"    {arg}: Description" for arg in args])}

Returns:
    {returns}
"""'''
        
        return docstring
    
    def _generate_class_docstring(self, node: ast.ClassDef) -> str:
        """Class için docstring oluştur."""
        methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
        
        if self.style == DocStyle.GOOGLE:
            docstring = f'''"""Brief description of class.

Attributes:
{chr(10).join([f"    {method}: Description of {method}." for method in methods])}
"""'''
        else:
            docstring = f'''"""Brief description of class.

Methods:
{chr(10).join([f"    {method}: Description" for method in methods])}
"""'''
        
        return docstring
    
    def _generate_function_documentation(self, node: ast.FunctionDef) -> str:
        """Function documentation oluştur (detaylı)."""
        docstring = self._generate_function_docstring(node)
        
        # Example code
        example = f"""
Example:
    >>> result = {node.name}()
    >>> print(result)
"""
        
        return docstring + example
    
    def _generate_class_documentation(self, node: ast.ClassDef) -> str:
        """Class documentation oluştur (detaylı)."""
        docstring = self._generate_class_docstring(node)
        
        # Methods documentation
        methods_docs = []
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                methods_docs.append(f"\n### {item.name}\n{self._generate_function_docstring(item)}")
        
        return docstring + "\n".join(methods_docs)
    
    def _generate_module_documentation(self, tree: ast.AST, file_path: str) -> str:
        """Module documentation oluştur."""
        module_name = Path(file_path).stem
        
        functions = []
        classes = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions.append(node.name)
            elif isinstance(node, ast.ClassDef):
                classes.append(node.name)
        
        docs = f"""# {module_name}

Module description.

## Functions
{chr(10).join([f"- `{func}`" for func in functions])}

## Classes
{chr(10).join([f"- `{cls}`" for cls in classes])}
"""
        
        return docs
    
    def _generate_markdown_documentation(self, tree: ast.AST, file_path: str) -> str:
        """Markdown documentation oluştur."""
        return self._generate_module_documentation(tree, file_path)


if __name__ == "__main__":
    # Basit test
    generator = DocumentationGenerator()
    
    result = generator.generate_module_docs("app/ai/documentation.py")
    print(f"Documentation generation: {result.success}")
    print(f"Message: {result.message}")
    if result.documentation:
        print(f"Documentation length: {len(result.documentation)}")
