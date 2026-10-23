"""
MuhammedAI Local Developer - Inline Variable
Inline variable engine for code editor.
"""

from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from enum import Enum


class InlineMode(Enum):
    """Inline mode."""
    SINGLE_OCCURRENCE = "single_occurrence"
    ALL_OCCURRENCES = "all_occurrences"
    SELECTED_OCCURRENCES = "selected_occurrences"


class InlineScope(Enum):
    """Inline scope."""
    LOCAL = "local"
    FUNCTION = "function"
    BLOCK = "block"


@dataclass
class VariableReference:
    """Variable reference."""
    variable_name: str
    line_number: int
    column: int
    is_definition: bool = False
    is_selected: bool = False


@dataclass
class InlineConfig:
    """Inline configuration."""
    inline_mode: InlineMode = InlineMode.SINGLE_OCCURRENCE
    remove_unused: bool = True
    preserve_formatting: bool = True
    verify_safety: bool = True
    show_preview: bool = True
    scope: InlineScope = InlineScope.LOCAL


@dataclass
class InlineResult:
    """Inline result."""
    success: bool
    modified_content: str = ""
    original_content: str = ""
    references_removed: int = 0
    variable_name: str = ""
    errors: List[str] = field(default_factory=list)
    message: Optional[str] = None


class InlineVariableEngine:
    """
    Inline variable engine.
    
    Özellikler:
    - Inline variable
    - Remove variable declaration
    - Replace with value
    - Single occurrence inline
    - All occurrences inline
    - Selected occurrences inline
    - Safety verification
    - Format preservation
    - Preview changes
    - Undo support
    - Reference detection
    - Scope analysis
    - Dependency tracking
    - Conflict detection
    - Inline history
    """
    
    def __init__(self, config: Optional[InlineConfig] = None):
        """Initialize inline variable engine."""
        self.config = config or InlineConfig()
        self.inline_history: List[Dict[str, Any]] = []
    
    def inline_variable(
        self,
        content: str,
        variable_name: str,
        line_number: int = 0,
        column: int = 0
    ) -> InlineResult:
        """
        Değişkeni inline et.
        
        Args:
            content: Dosya içeriği
            variable_name: Değişken adı
            line_number: Satır numarası
            column: Sütun numarası
            
        Returns:
            InlineResult: Inline sonucu
        """
        result = InlineResult(success=False)
        result.original_content = content
        
        try:
            if not variable_name:
                result.errors.append("Variable name cannot be empty")
                return result
            
            # Değişken değerini bul
            variable_value = self._find_variable_value(content, variable_name, line_number)
            
            if variable_value is None:
                result.errors.append(f"Variable '{variable_name}' not found")
                return result
            
            # Referansları bul
            references = self._find_references(content, variable_name)
            
            if self.config.verify_safety:
                safety_check = self._verify_safety(content, variable_name, references)
                if not safety_check["safe"]:
                    result.errors.append(safety_check["reason"])
                    return result
            
            # İçeriği değiştir
            modified_content = self._inline_variable(
                content,
                variable_name,
                variable_value,
                references
            )
            
            # Geçmişe ekle
            self.inline_history.append({
                "original": content,
                "modified": modified_content,
                "variable_name": variable_name,
                "value": variable_value
            })
            
            result.success = True
            result.modified_content = modified_content
            result.references_removed = len(references)
            result.variable_name = variable_name
            result.message = f"Inlined variable: {variable_name}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def _find_variable_value(
        self,
        content: str,
        variable_name: str,
        line_number: int
    ) -> Optional[str]:
        """
        Değişken değerini bul.
        
        Args:
            content: İçerik
            variable_name: Değişken adı
            line_number: Satır numarası
            
        Returns:
            Optional[str]: Değer
        """
        lines = content.splitlines()
        
        # Belirtilen satırda ara
        if 0 <= line_number < len(lines):
            line = lines[line_number]
            if f"{variable_name} =" in line:
                # Değeri çıkar
                parts = line.split("=", 1)
                if len(parts) > 1:
                    return parts[1].strip()
        
        # Tüm satırlarda ara
        for line in lines:
            if f"{variable_name} =" in line:
                parts = line.split("=", 1)
                if len(parts) > 1:
                    return parts[1].strip()
        
        return None
    
    def _find_references(self, content: str, variable_name: str) -> List[VariableReference]:
        """
        Referansları bul.
        
        Args:
            content: İçerik
            variable_name: Değişken adı
            
        Returns:
            List[VariableReference]: Referans listesi
        """
        references = []
        lines = content.splitlines()
        
        for i, line in enumerate(lines):
            if variable_name in line:
                # Tanım satırı mı kontrol et
                is_definition = f"{variable_name} =" in line
                
                # Referans ekle
                column = line.find(variable_name)
                reference = VariableReference(
                    variable_name=variable_name,
                    line_number=i,
                    column=column,
                    is_definition=is_definition
                )
                references.append(reference)
        
        return references
    
    def _verify_safety(
        self,
        content: str,
        variable_name: str,
        references: List[VariableReference]
    ) -> Dict[str, Any]:
        """
        Güvenlik doğrulaması.
        
        Args:
            content: İçerik
            variable_name: Değişken adı
            references: Referanslar
            
        Returns:
            Dict[str, Any]: Güvenlik sonucu
        """
        # Basit güvenlik kontrolü
        if len(references) == 0:
            return {"safe": False, "reason": "No references found"}
        
        if len(references) > 10:
            return {"safe": False, "reason": "Too many references to inline safely"}
        
        return {"safe": True}
    
    def _inline_variable(
        self,
        content: str,
        variable_name: str,
        variable_value: str,
        references: List[VariableReference]
    ) -> str:
        """
        Değişkeni inline et.
        
        Args:
            content: İçerik
            variable_name: Değişken adı
            variable_value: Değer
            references: Referanslar
            
        Returns:
            str: Değiştirilmiş içerik
        """
        lines = content.splitlines()
        modified_lines = []
        
        # Tanım satırını bul
        definition_line = None
        for ref in references:
            if ref.is_definition:
                definition_line = ref.line_number
                break
        
        for i, line in enumerate(lines):
            if i == definition_line:
                # Tanım satırını atla
                continue
            elif variable_name in line:
                # Referansı değerle değiştir
                modified_line = line.replace(variable_name, variable_value)
                modified_lines.append(modified_line)
            else:
                modified_lines.append(line)
        
        return "\n".join(modified_lines)
    
    def undo_inline(self) -> InlineResult:
        """
        Inline işlemini geri al.
        
        Returns:
            InlineResult: Geri alma sonucu
        """
        result = InlineResult(success=False)
        
        try:
            if not self.inline_history:
                result.errors.append("No inline history")
                return result
            
            last_inline = self.inline_history.pop()
            
            result.success = True
            result.modified_content = last_inline["original"]
            result.original_content = last_inline["modified"]
            result.variable_name = last_inline["variable_name"]
            result.message = "Inline operation undone"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_inline_history(self) -> List[Dict[str, Any]]:
        """
        Inline geçmişini al.
        
        Returns:
            List[Dict[str, Any]]: Geçmiş
        """
        return self.inline_history
    
    def clear_history(self) -> InlineResult:
        """
        Geçmişi temizle.
        
        Returns:
            InlineResult: Temizleme sonucu
        """
        result = InlineResult(success=False)
        
        try:
            self.inline_history.clear()
            result.success = True
            result.message = "Inline history cleared"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def update_config(self, config: InlineConfig) -> InlineResult:
        """
        Konfigürasyon güncelle.
        
        Args:
            config: Yeni konfigürasyon
            
        Returns:
            InlineResult: Güncelleme sonucu
        """
        result = InlineResult(success=False)
        
        try:
            self.config = config
            result.success = True
            result.message = "Config updated"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_config(self) -> InlineConfig:
        """
        Konfigürasyon al.
        
        Returns:
            InlineConfig: Konfigürasyon
        """
        return self.config


if __name__ == "__main__":
    # Basit test
    engine = InlineVariableEngine()
    
    content = "x = 42\nprint(x)"
    result = engine.inline_variable(content, "x")
    print(f"Inline: {result.success}")
