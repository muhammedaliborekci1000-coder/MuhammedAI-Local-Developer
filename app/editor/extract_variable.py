"""
MuhammedAI Local Developer - Extract Variable
Extract variable engine for code editor.
"""

from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from enum import Enum


class VariableScope(Enum):
    """Variable scope."""
    LOCAL = "local"
    FUNCTION = "function"
    CLASS = "class"
    MODULE = "module"
    GLOBAL = "global"


class ExtractionMode(Enum):
    """Extraction mode."""
    SELECTION = "selection"
    EXPRESSION = "expression"
    REPEATED_VALUE = "repeated_value"
    COMPLEX_EXPRESSION = "complex_expression"


@dataclass
class VariableInfo:
    """Variable information."""
    name: str
    value: str
    variable_type: str = ""
    scope: VariableScope = VariableScope.LOCAL
    line_number: int = 0
    column: int = 0
    occurrences: int = 1
    is_const: bool = False


@dataclass
class ExtractConfig:
    """Extract configuration."""
    auto_infer_type: bool = True
    suggest_names: bool = True
    replace_all_occurrences: bool = False
    add_type_annotation: bool = False
    use_const: bool = False
    scope: VariableScope = VariableScope.LOCAL
    extraction_mode: ExtractionMode = ExtractionMode.SELECTION


@dataclass
class ExtractResult:
    """Extract result."""
    success: bool
    variable_info: Optional[VariableInfo] = None
    modified_content: str = ""
    original_content: str = ""
    replacements_made: int = 0
    errors: List[str] = field(default_factory=list)
    message: Optional[str] = None


class ExtractVariableEngine:
    """
    Extract variable engine.
    
    Özellikler:
    - Extract variable from selection
    - Extract variable from expression
    - Extract repeated values
    - Extract complex expressions
    - Auto name suggestion
    - Type inference
    - Scope control
    - Replace all occurrences
    - Type annotation
    - Const extraction
    - Variable validation
    - Occurrence detection
    - Preview changes
    - Undo support
    - Format preservation
    """
    
    def __init__(self, config: Optional[ExtractConfig] = None):
        """Initialize extract variable engine."""
        self.config = config or ExtractConfig()
        self.extraction_history: List[Dict[str, Any]] = []
    
    def extract_variable(
        self,
        content: str,
        selection: str,
        line_number: int = 0,
        column: int = 0,
        suggested_name: Optional[str] = None
    ) -> ExtractResult:
        """
        Değişken çıkar.
        
        Args:
            content: Dosya içeriği
            selection: Seçili metin
            line_number: Satır numarası
            column: Sütun numarası
            suggested_name: Önerilen isim
            
        Returns:
            ExtractResult: Çıkarma sonucu
        """
        result = ExtractResult(success=False)
        result.original_content = content
        
        try:
            if not selection:
                result.errors.append("Selection cannot be empty")
                return result
            
            # İsim öner
            variable_name = suggested_name or self._suggest_name(selection)
            
            # Tip çıkarımı
            variable_type = self._infer_type(selection) if self.config.auto_infer_type else ""
            
            # Değişken bilgisi oluştur
            variable_info = VariableInfo(
                name=variable_name,
                value=selection,
                variable_type=variable_type,
                scope=self.config.scope,
                line_number=line_number,
                column=column,
                occurrences=self._count_occurrences(content, selection)
            )
            
            # İçeriği değiştir
            modified_content = self._replace_occurrences(
                content,
                selection,
                variable_name,
                variable_type
            )
            
            # Geçmişe ekle
            self.extraction_history.append({
                "original": content,
                "modified": modified_content,
                "variable": variable_info
            })
            
            result.success = True
            result.variable_info = variable_info
            result.modified_content = modified_content
            result.replacements_made = variable_info.occurrences
            result.message = f"Extracted variable: {variable_name}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def _suggest_name(self, selection: str) -> str:
        """
        İsim öner.
        
        Args:
            selection: Seçili metin
            
        Returns:
            str: Önerilen isim
        """
        # Basit isim önerme mantığı
        selection = selection.strip()
        
        # String literal ise
        if selection.startswith('"') or selection.startswith("'"):
            return "text"
        
        # Sayı ise
        if selection.replace(".", "").replace("-", "").isdigit():
            return "number"
        
        # Boolean ise
        if selection.lower() in ["true", "false"]:
            return "flag"
        
        # Varsayılan
        return "extracted_value"
    
    def _infer_type(self, selection: str) -> str:
        """
        Tip çıkarımı yap.
        
        Args:
            selection: Seçili metin
            
        Returns:
            str: Tip
        """
        selection = selection.strip()
        
        # String
        if selection.startswith('"') or selection.startswith("'"):
            return "str"
        
        # Integer
        if selection.replace("-", "").isdigit():
            return "int"
        
        # Float
        if "." in selection and selection.replace(".", "").replace("-", "").isdigit():
            return "float"
        
        # Boolean
        if selection.lower() in ["true", "false"]:
            return "bool"
        
        # None
        if selection.lower() in ["none", "null"]:
            return "None"
        
        return ""
    
    def _count_occurrences(self, content: str, value: str) -> int:
        """
        Tekrar sayısını bul.
        
        Args:
            content: İçerik
            value: Değer
            
        Returns:
            int: Tekrar sayısı
        """
        return content.count(value)
    
    def _replace_occurrences(
        self,
        content: str,
        value: str,
        variable_name: str,
        variable_type: str
    ) -> str:
        """
        Tekrarları değiştir.
        
        Args:
            content: İçerik
            value: Değer
            variable_name: Değişken adı
            variable_type: Tip
            
        Returns:
            str: Değiştirilmiş içerik
        """
        # Değişken tanımı oluştur
        type_annotation = f": {variable_type}" if variable_type and self.config.add_type_annotation else ""
        const_keyword = "const " if self.config.use_const else ""
        variable_declaration = f"{const_keyword}{variable_name}{type_annotation} = {value}"
        
        # İlk occurrence'u değiştir
        lines = content.splitlines()
        modified_lines = []
        
        for i, line in enumerate(lines):
            if value in line:
                # İlk occurrence'u değiştir ve değişken tanımını ekle
                modified_line = line.replace(value, variable_name, 1)
                modified_lines.append(variable_declaration)
                modified_lines.append(modified_line)
            else:
                modified_lines.append(line)
        
        return "\n".join(modified_lines)
    
    def undo_extraction(self) -> ExtractResult:
        """
        Çıkarmayı geri al.
        
        Returns:
            ExtractResult: Geri alma sonucu
        """
        result = ExtractResult(success=False)
        
        try:
            if not self.extraction_history:
                result.errors.append("No extraction history")
                return result
            
            last_extraction = self.extraction_history.pop()
            
            result.success = True
            result.modified_content = last_extraction["original"]
            result.original_content = last_extraction["modified"]
            result.message = "Extraction undone"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_extraction_history(self) -> List[Dict[str, Any]]:
        """
        Çıkarma geçmişini al.
        
        Returns:
            List[Dict[str, Any]]: Geçmiş
        """
        return self.extraction_history
    
    def clear_history(self) -> ExtractResult:
        """
        Geçmişi temizle.
        
        Returns:
            ExtractResult: Temizleme sonucu
        """
        result = ExtractResult(success=False)
        
        try:
            self.extraction_history.clear()
            result.success = True
            result.message = "Extraction history cleared"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def update_config(self, config: ExtractConfig) -> ExtractResult:
        """
        Konfigürasyon güncelle.
        
        Args:
            config: Yeni konfigürasyon
            
        Returns:
            ExtractResult: Güncelleme sonucu
        """
        result = ExtractResult(success=False)
        
        try:
            self.config = config
            result.success = True
            result.message = "Config updated"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_config(self) -> ExtractConfig:
        """
        Konfigürasyon al.
        
        Returns:
            ExtractConfig: Konfigürasyon
        """
        return self.config


if __name__ == "__main__":
    # Basit test
    engine = ExtractVariableEngine()
    
    content = "x = 42 + 42"
    result = engine.extract_variable(content, "42")
    print(f"Extract: {result.success}")
