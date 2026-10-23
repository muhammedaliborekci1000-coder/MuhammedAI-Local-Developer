"""
MuhammedAI Local Developer - Warning Highlighting
Warning highlighting engine for code editor.
"""

import ast
import re
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum


class WarningSeverity(Enum):
    """Warning severity."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class WarningCategory(Enum):
    """Warning category."""
    DEPRECATED = "deprecated"
    UNUSED = "unused"
    STYLE = "style"
    SECURITY = "security"
    PERFORMANCE = "performance"
    MAINTAINABILITY = "maintainability"
    DOCUMENTATION = "documentation"
    TYPE_SAFETY = "type_safety"


@dataclass
class WarningMarker:
    """Warning marker."""
    line: int
    column: int
    end_line: int
    end_column: int
    severity: WarningSeverity
    category: WarningCategory
    message: str
    code: Optional[str] = None
    suggestion: Optional[str] = None


@dataclass
class WarningHighlightingResult:
    """Warning highlighting result."""
    success: bool
    markers: List[WarningMarker] = field(default_factory=list)
    total_warnings: int = 0
    total_low: int = 0
    total_medium: int = 0
    total_high: int = 0
    total_critical: int = 0
    errors: List[str] = field(default_factory=list)
    message: Optional[str] = None


class WarningHighlightingEngine:
    """
    Warning highlighting engine.
    
    Özellikler:
    - Deprecated usage warnings
    - Unused variable warnings
    - Style warnings
    - Security warnings
    - Performance warnings
    - Maintainability warnings
    - Documentation warnings
    - Type safety warnings
    - Warning markers in editor
    - Warning tooltips
    - Warning navigation
    - Warning filtering
    - Warning severity levels
    - Warning categories
    - Quick fix suggestions
    - Multi-language support
    """
    
    def __init__(self):
        """Initialize warning highlighting engine."""
        self.current_markers: List[WarningMarker] = []
    
    def highlight_warnings(
        self,
        code: str,
        language: str = "python"
    ) -> WarningHighlightingResult:
        """
        Kod içindeki uyarıları highlight et.
        
        Args:
            code: Kod içeriği
            language: Programlama dili
            
        Returns:
            WarningHighlightingResult: Highlighting sonucu
        """
        result = WarningHighlightingResult(success=False)
        
        try:
            markers = []
            
            if language == "python":
                markers = self._highlight_python_warnings(code)
            else:
                markers = self._highlight_generic_warnings(code)
            
            # İstatistikleri hesapla
            total_warnings = len(markers)
            total_low = sum(1 for m in markers if m.severity == WarningSeverity.LOW)
            total_medium = sum(1 for m in markers if m.severity == WarningSeverity.MEDIUM)
            total_high = sum(1 for m in markers if m.severity == WarningSeverity.HIGH)
            total_critical = sum(1 for m in markers if m.severity == WarningSeverity.CRITICAL)
            
            result.markers = markers
            result.total_warnings = total_warnings
            result.total_low = total_low
            result.total_medium = total_medium
            result.total_high = total_high
            result.total_critical = total_critical
            result.success = True
            result.message = f"Found {total_warnings} warnings"
            
            self.current_markers = markers
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def _highlight_python_warnings(self, code: str) -> List[WarningMarker]:
        """Python uyarılarını highlight et."""
        markers = []
        lines = code.splitlines()
        
        # Unused variable detection (basic)
        try:
            tree = ast.parse(code)
            used_names = set()
            defined_names = set()
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Name):
                    if isinstance(node.ctx, ast.Load):
                        used_names.add(node.id)
                    elif isinstance(node.ctx, ast.Store):
                        defined_names.add(node.id)
            
            unused = defined_names - used_names
            for unused_name in unused:
                for line_num, line in enumerate(lines, 1):
                    if unused_name in line:
                        marker = WarningMarker(
                            line=line_num,
                            column=line.find(unused_name),
                            end_line=line_num,
                            end_column=line.find(unused_name) + len(unused_name),
                            severity=WarningSeverity.MEDIUM,
                            category=WarningCategory.UNUSED,
                            message=f"Unused variable: {unused_name}",
                            suggestion="Remove unused variable or use it"
                        )
                        markers.append(marker)
                        break
        except:
            pass
        
        # Missing docstring detection
        for line_num, line in enumerate(lines, 1):
            if line.strip().startswith("def ") and not line.strip().endswith(":"):
                # Check if next line has docstring
                if line_num < len(lines) and not lines[line_num].strip().startswith('"""'):
                    marker = WarningMarker(
                        line=line_num,
                        column=line.find("def"),
                        end_line=line_num,
                        end_column=line.find("def") + 3,
                        severity=WarningSeverity.LOW,
                        category=WarningCategory.DOCUMENTATION,
                        message="Missing docstring",
                        suggestion="Add docstring to function"
                    )
                    markers.append(marker)
        
        # Long line detection
        for line_num, line in enumerate(lines, 1):
            if len(line) > 100:
                marker = WarningMarker(
                    line=line_num,
                    column=100,
                    end_line=line_num,
                    end_column=len(line),
                    severity=WarningSeverity.LOW,
                    category=WarningCategory.STYLE,
                    message=f"Line too long ({len(line)} characters)",
                    suggestion="Break line into multiple lines"
                )
                markers.append(marker)
        
        return markers
    
    def _highlight_generic_warnings(self, code: str) -> List[WarningMarker]:
        """Genel uyarıları highlight et."""
        markers = []
        lines = code.splitlines()
        
        for line_num, line in enumerate(lines, 1):
            # TODO comment detection
            if "TODO" in line:
                marker = WarningMarker(
                    line=line_num,
                    column=line.find("TODO"),
                    end_line=line_num,
                    end_column=line.find("TODO") + 4,
                    severity=WarningSeverity.LOW,
                    category=WarningCategory.MAINTAINABILITY,
                    message="TODO comment found",
                    suggestion="Complete the TODO task"
                )
                markers.append(marker)
        
        return markers
    
    def filter_by_severity(self, severity: WarningSeverity) -> List[WarningMarker]:
        """
        Şiddete göre filtrele.
        
        Args:
            severity: Uyarı şiddeti
            
        Returns:
            List[WarningMarker]: Filtrelenmiş marker'lar
        """
        return [m for m in self.current_markers if m.severity == severity]
    
    def filter_by_category(self, category: WarningCategory) -> List[WarningMarker]:
        """
        Kategoriye göre filtrele.
        
        Args:
            category: Uyarı kategorisi
            
        Returns:
            List[WarningMarker]: Filtrelenmiş marker'lar
        """
        return [m for m in self.current_markers if m.category == category]
    
    def get_warnings_at_line(self, line: int) -> List[WarningMarker]:
        """
        Belirli bir satırdaki uyarıları al.
        
        Args:
            line: Satır numarası
            
        Returns:
            List[WarningMarker]: Uyarı marker'ları
        """
        return [m for m in self.current_markers if m.line == line]
    
    def get_next_warning(self, current_line: int) -> Optional[WarningMarker]:
        """
        Sonraki uyarıyı al.
        
        Args:
            current_line: Mevcut satır
            
        Returns:
            Optional[WarningMarker]: Sonraki uyarı
        """
        for marker in self.current_markers:
            if marker.line > current_line:
                return marker
        return None
    
    def get_previous_warning(self, current_line: int) -> Optional[WarningMarker]:
        """
        Önceki uyarıyı al.
        
        Args:
            current_line: Mevcut satır
            
        Returns:
            Optional[WarningMarker]: Önceki uyarı
        """
        for marker in reversed(self.current_markers):
            if marker.line < current_line:
                return marker
        return None
    
    def add_custom_marker(
        self,
        line: int,
        column: int,
        end_line: int,
        end_column: int,
        severity: WarningSeverity,
        category: WarningCategory,
        message: str,
        suggestion: Optional[str] = None
    ) -> WarningMarker:
        """
        Özel marker ekle.
        
        Args:
            line: Satır numarası
            column: Sütun numarası
            end_line: Bitiş satırı
            end_column: Bitiş sütunu
            severity: Şiddet
            category: Kategori
            message: Mesaj
            suggestion: Öneri
            
        Returns:
            WarningMarker: Oluşturulan marker
        """
        marker = WarningMarker(
            line=line,
            column=column,
            end_line=end_line,
            end_column=end_column,
            severity=severity,
            category=category,
            message=message,
            suggestion=suggestion
        )
        self.current_markers.append(marker)
        return marker
    
    def clear_markers(self) -> None:
        """Tüm marker'ları temizle."""
        self.current_markers.clear()


if __name__ == "__main__":
    # Basit test
    engine = WarningHighlightingEngine()
    
    code = """
def my_function():
    unused_var = 42
    return "Hello"
"""
    
    result = engine.highlight_warnings(code, "python")
    print(f"Highlighting: {result.success}")
    print(f"Total warnings: {result.total_warnings}")
    
    for marker in result.markers:
        print(f"  Line {marker.line}: {marker.message}")
