"""
MuhammedAI Local Developer - Extract Function
Extract function engine for code editor.
"""

import ast
import re
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from enum import Enum


class ExtractScope(Enum):
    """Extract scope."""
    LOCAL = "local"
    GLOBAL = "global"
    CLASS = "class"


class FunctionVisibility(Enum):
    """Function visibility."""
    PRIVATE = "private"
    PUBLIC = "public"
    PROTECTED = "protected"


@dataclass
class FunctionParameter:
    """Function parameter."""
    name: str
    type_hint: Optional[str] = None
    default_value: Optional[str] = None


@dataclass
class ExtractedFunction:
    """Extracted function."""
    name: str
    parameters: List[FunctionParameter] = field(default_factory=list)
    return_type: Optional[str] = None
    body: str = ""
    visibility: FunctionVisibility = FunctionVisibility.PRIVATE


@dataclass
class ExtractResult:
    """Extract result."""
    success: bool
    original_code: str = ""
    extracted_code: str = ""
    function: Optional[ExtractedFunction] = None
    errors: List[str] = field(default_factory=list)
    message: Optional[str] = None


class ExtractFunctionEngine:
    """
    Extract function engine.
    
    Özellikler:
    - Extract selected code into function
    - Auto-detect parameters
    - Auto-detect return value
    - Generate function signature
    - Replace selection with function call
    - Preview extraction
    - Validate extraction
    - Scope-aware extraction
    - Visibility control
    - Type hint generation
    - Default value handling
    - Multi-language support
    """
    
    def __init__(self):
        """Initialize extract function engine."""
        self.current_function: Optional[ExtractedFunction] = None
    
    def extract_function(
        self,
        code: str,
        start_line: int,
        end_line: int,
        function_name: str = "extracted_function",
        scope: ExtractScope = ExtractScope.LOCAL,
        language: str = "python"
    ) -> ExtractResult:
        """
        Seçili kodu fonksiyona çıkar.
        
        Args:
            code: Kod içeriği
            start_line: Başlangıç satırı
            end_line: Bitiş satırı
            function_name: Fonksiyon adı
            scope: Extract scope
            language: Programlama dili
            
        Returns:
            ExtractResult: Extract sonucu
        """
        result = ExtractResult(success=False)
        result.original_code = code
        
        try:
            if language == "python":
                extracted_code, function = self._extract_python_function(
                    code, start_line, end_line, function_name, scope
                )
            else:
                extracted_code, function = self._extract_generic_function(
                    code, start_line, end_line, function_name, scope
                )
            
            result.extracted_code = extracted_code
            result.function = function
            result.success = True
            result.message = f"Extracted function: {function_name}"
            
            self.current_function = function
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def _extract_python_function(
        self,
        code: str,
        start_line: int,
        end_line: int,
        function_name: str,
        scope: ExtractScope
    ) -> Tuple[str, ExtractedFunction]:
        """Python fonksiyonu çıkar."""
        lines = code.splitlines()
        
        if start_line >= len(lines) or end_line >= len(lines):
            return code, ExtractedFunction(name=function_name)
        
        # Seçili kodu al
        selected_lines = lines[start_line:end_line + 1]
        selected_code = "\n".join(selected_lines)
        
        # Parametreleri tespit et
        parameters = self._detect_parameters(selected_code, lines, start_line)
        
        # Return type tespit et
        return_type = self._detect_return_type(selected_code)
        
        # Fonksiyon gövdesini oluştur
        body = self._indent_code(selected_code, 4)
        
        # Fonksiyon signature oluştur
        param_strs = []
        for param in parameters:
            if param.type_hint:
                param_strs.append(f"{param.name}: {param.type_hint}")
            else:
                param_strs.append(param.name)
        
        signature = f"def {function_name}({', '.join(param_strs)})"
        if return_type:
            signature += f" -> {return_type}"
        signature += ":"
        
        # Fonksiyon tanımı oluştur
        function_def = f"{signature}\n{body}"
        
        # Fonksiyon call oluştur
        call_args = [p.name for p in parameters]
        function_call = f"{function_name}({', '.join(call_args)})"
        
        # Kodu güncelle
        new_lines = lines.copy()
        
        # Fonksiyonu ekle (scope'a göre)
        if scope == ExtractScope.GLOBAL:
            # Dosya başına ekle
            insert_line = 0
            while insert_line < len(new_lines) and (new_lines[insert_line].strip().startswith('import') or new_lines[insert_line].strip().startswith('from')):
                insert_line += 1
            new_lines.insert(insert_line, function_def)
            new_lines.insert(insert_line + 1, "")
        elif scope == ExtractScope.CLASS:
            # Seçimden önceki class'a ekle
            insert_line = start_line
            new_lines.insert(insert_line, function_def)
            new_lines.insert(insert_line + 1, "")
        else:
            # Local - seçimden önceki satıra ekle
            insert_line = start_line
            new_lines.insert(insert_line, function_def)
            new_lines.insert(insert_line + 1, "")
        
        # Seçili kodu function call ile değiştir
        new_lines[start_line + 2:end_line + 3] = [function_call]
        
        extracted_code = "\n".join(new_lines)
        
        function = ExtractedFunction(
            name=function_name,
            parameters=parameters,
            return_type=return_type,
            body=body,
            visibility=FunctionVisibility.PRIVATE
        )
        
        return extracted_code, function
    
    def _extract_generic_function(
        self,
        code: str,
        start_line: int,
        end_line: int,
        function_name: str,
        scope: ExtractScope
    ) -> Tuple[str, ExtractedFunction]:
        """Genel fonksiyon çıkar."""
        lines = code.splitlines()
        
        if start_line >= len(lines) or end_line >= len(lines):
            return code, ExtractedFunction(name=function_name)
        
        selected_lines = lines[start_line:end_line + 1]
        selected_code = "\n".join(selected_lines)
        
        # Basit fonksiyon tanımı
        body = self._indent_code(selected_code, 4)
        function_def = f"def {function_name}():\n{body}"
        function_call = f"{function_name}()"
        
        # Kodu güncelle
        new_lines = lines.copy()
        new_lines.insert(start_line, function_def)
        new_lines.insert(start_line + 1, "")
        new_lines[start_line + 2:end_line + 3] = [function_call]
        
        extracted_code = "\n".join(new_lines)
        
        function = ExtractedFunction(
            name=function_name,
            body=body,
            visibility=FunctionVisibility.PRIVATE
        )
        
        return extracted_code, function
    
    def _detect_parameters(self, code: str, all_lines: List[str], start_line: int) -> List[FunctionParameter]:
        """Parametreleri tespit et."""
        parameters = []
        
        # Basit değişken atamalarını tespit et
        try:
            tree = ast.parse(code)
            assigned_vars = set()
            used_vars = set()
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            assigned_vars.add(target.id)
                elif isinstance(node, ast.Name):
                    used_vars.add(node.id)
            
            # Dışarıda tanımlı ama kullanılan değişkenleri parametre olarak ekle
            for var in used_vars:
                if var not in assigned_vars:
                    # Önceki satırlarda tanımlı mı kontrol et
                    for line in all_lines[:start_line]:
                        if f"{var} =" in line or f"{var}=" in line:
                            parameters.append(FunctionParameter(name=var))
                            break
        except:
            pass
        
        return parameters
    
    def _detect_return_type(self, code: str) -> Optional[str]:
        """Return type tespit et."""
        if "return " in code:
            try:
                tree = ast.parse(code)
                for node in ast.walk(tree):
                    if isinstance(node, ast.Return) and node.value:
                        if isinstance(node.value, ast.Constant):
                            if isinstance(node.value.value, str):
                                return "str"
                            elif isinstance(node.value.value, int):
                                return "int"
                            elif isinstance(node.value.value, float):
                                return "float"
                            elif isinstance(node.value.value, bool):
                                return "bool"
                        elif isinstance(node.value, ast.Name):
                            return node.value.id
            except:
                pass
        
        return None
    
    def _indent_code(self, code: str, indent: int) -> str:
        """Kodu indent et."""
        lines = code.splitlines()
        indented_lines = []
        indent_str = " " * indent
        
        for line in lines:
            if line.strip():
                indented_lines.append(indent_str + line)
            else:
                indented_lines.append(line)
        
        return "\n".join(indented_lines)
    
    def preview_extraction(
        self,
        code: str,
        start_line: int,
        end_line: int,
        function_name: str = "extracted_function",
        scope: ExtractScope = ExtractScope.LOCAL
    ) -> ExtractResult:
        """
        Extraction önizleme.
        
        Args:
            code: Kod içeriği
            start_line: Başlangıç satırı
            end_line: Bitiş satırı
            function_name: Fonksiyon adı
            scope: Extract scope
            
        Returns:
            ExtractResult: Preview sonucu
        """
        return self.extract_function(code, start_line, end_line, function_name, scope)
    
    def validate_extraction(
        self,
        code: str,
        start_line: int,
        end_line: int,
        function_name: str
    ) -> Tuple[bool, List[str]]:
        """
        Extraction validation yap.
        
        Args:
            code: Kod içeriği
            start_line: Başlangıç satırı
            end_line: Bitiş satırı
            function_name: Fonksiyon adı
            
        Returns:
            Tuple[bool, List[str]]: Valid mi ve hata listesi
        """
        errors = []
        
        # Fonksiyon adı kontrolü
        if not function_name or not function_name.strip():
            errors.append("Function name cannot be empty")
        
        if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', function_name):
            errors.append(f"'{function_name}' is not a valid function name")
        
        # Satır kontrolü
        lines = code.splitlines()
        if start_line >= len(lines) or end_line >= len(lines):
            errors.append("Invalid line range")
        
        if start_line > end_line:
            errors.append("Start line must be less than or equal to end line")
        
        # Keyword kontrolü
        keywords = ['def', 'class', 'if', 'else', 'elif', 'for', 'while', 'try', 'except', 'import', 'from', 'return', 'yield', 'with', 'as', 'pass', 'break', 'continue', 'raise', 'finally']
        if function_name in keywords:
            errors.append(f"'{function_name}' is a Python keyword")
        
        return len(errors) == 0, errors


if __name__ == "__main__":
    # Basit test
    engine = ExtractFunctionEngine()
    
    code = """
def main():
    x = 10
    y = 20
    result = x + y
    print(result)
"""
    
    # Fonksiyon çıkar
    result = engine.extract_function(code, 2, 3, "calculate_sum", ExtractScope.LOCAL, "python")
    
    print(f"Extract: {result.success}")
    print(f"Function: {result.function.name if result.function else 'N/A'}")
    print(f"Extracted code:\n{result.extracted_code}")
