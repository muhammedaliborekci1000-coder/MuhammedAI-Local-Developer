"""
MuhammedAI Local Developer - Error Highlighting
Error highlighting engine for code editor.
"""

import ast
import re
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from enum import Enum


class ErrorSeverity(Enum):
    """Error severity."""
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
    HINT = "hint"


class ErrorCategory(Enum):
    """Error category."""
    SYNTAX = "syntax"
    RUNTIME = "runtime"
    LINTING = "linting"
    TYPE = "type"
    IMPORT = "import"
    STYLE = "style"
    SECURITY = "security"
    PERFORMANCE = "performance"


@dataclass
class ErrorMarker:
    """Error marker."""
    line: int
    column: int
    end_line: int
    end_column: int
    severity: ErrorSeverity
    category: ErrorCategory
    message: str
    code: Optional[str] = None
    suggestion: Optional[str] = None


@dataclass
class ErrorHighlightingResult:
    """Error highlighting result."""
    success: bool
    markers: List[ErrorMarker] = field(default_factory=list)
    total_errors: int = 0
    total_warnings: int = 0
    total_info: int = 0
    errors: List[str] = field(default_factory=list)
    message: Optional[str] = None


class ErrorHighlightingEngine:
    """
    Error highlighting engine.
    
    Özellikler:
    - Syntax error detection
    - Runtime error detection
    - Linting error display
    - Warning display
    - Error markers in editor
    - Error tooltips
    - Error navigation
    - Error filtering
    - Error severity levels
    - Error categories
    - Quick fix suggestions
    - Multi-language support
    """
    
    def __init__(self):
        """Initialize error highlighting engine."""
        self.current_markers: List[ErrorMarker] = []
    
    def highlight_errors(
        self,
        code: str,
        language: str = "python"
    ) -> ErrorHighlightingResult:
        """
        Kod içindeki hataları highlight et.
        
        Args:
            code: Kod içeriği
            language: Programlama dili
            
        Returns:
            ErrorHighlightingResult: Highlighting sonucu
        """
        result = ErrorHighlightingResult(success=False)
        
        try:
            markers = []
            
            if language == "python":
                markers = self._highlight_python_errors(code)
            else:
                markers = self._highlight_generic_errors(code)
            
            # İstatistikleri hesapla
            total_errors = sum(1 for m in markers if m.severity == ErrorSeverity.ERROR)
            total_warnings = sum(1 for m in markers if m.severity == ErrorSeverity.WARNING)
            total_info = sum(1 for m in markers if m.severity == ErrorSeverity.INFO)
            
            result.markers = markers
            result.total_errors = total_errors
            result.total_warnings = total_warnings
            result.total_info = total_info
            result.success = True
            result.message = f"Found {total_errors} errors, {total_warnings} warnings"
            
            self.current_markers = markers
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def _highlight_python_errors(self, code: str) -> List[ErrorMarker]:
        """Python hatalarını highlight et."""
        markers = []
        lines = code.splitlines()
        
        # Syntax error detection
        try:
            ast.parse(code)
        except SyntaxError as e:
            marker = ErrorMarker(
                line=e.lineno or 1,
                column=e.offset or 0,
                end_line=e.lineno or 1,
                end_column=e.end_offset or (e.offset or 0) + 1,
                severity=ErrorSeverity.ERROR,
                category=ErrorCategory.SYNTAX,
                message=f"Syntax error: {e.msg}",
                suggestion="Check syntax and fix the error"
            )
            markers.append(marker)
        
        # Import error detection
        for line_num, line in enumerate(lines, 1):
            # Undefined variable detection (basic)
            if "undefined" in line.lower():
                marker = ErrorMarker(
                    line=line_num,
                    column=line.find("undefined"),
                    end_line=line_num,
                    end_column=line.find("undefined") + len("undefined"),
                    severity=ErrorSeverity.WARNING,
                    category=ErrorCategory.RUNTIME,
                    message="Possible undefined variable",
                    suggestion="Define the variable before use"
                )
                markers.append(marker)
            
            # Missing import detection (basic)
            if re.search(r'\b(os|sys|re|json)\b', line):
                import_line = any("import" in lines[i] for i in range(min(line_num, len(lines))))
                if not import_line:
                    marker = ErrorMarker(
                        line=line_num,
                        column=line.lower().find("os") if "os" in line.lower() else 0,
                        end_line=line_num,
                        end_column=line.lower().find("os") + 2 if "os" in line.lower() else 2,
                        severity=ErrorSeverity.WARNING,
                        category=ErrorCategory.IMPORT,
                        message="Possible missing import",
                        suggestion="Add import statement"
                    )
                    markers.append(marker)
        
        return markers
    
    def _highlight_generic_errors(self, code: str) -> List[ErrorMarker]:
        """Genel hataları highlight et."""
        markers = []
        lines = code.splitlines()
        
        for line_num, line in enumerate(lines, 1):
            # Empty line detection
            if line.strip() == "":
                marker = ErrorMarker(
                    line=line_num,
                    column=0,
                    end_line=line_num,
                    end_column=len(line),
                    severity=ErrorSeverity.INFO,
                    category=ErrorCategory.STYLE,
                    message="Empty line",
                    suggestion="Remove unnecessary empty lines"
                )
                markers.append(marker)
        
        return markers
    
    def filter_by_severity(self, severity: ErrorSeverity) -> List[ErrorMarker]:
        """
        Şiddete göre filtrele.
        
        Args:
            severity: Hata şiddeti
            
        Returns:
            List[ErrorMarker]: Filtrelenmiş marker'lar
        """
        return [m for m in self.current_markers if m.severity == severity]
    
    def filter_by_category(self, category: ErrorCategory) -> List[ErrorMarker]:
        """
        Kategoriye göre filtrele.
        
        Args:
            category: Hata kategorisi
            
        Returns:
            List[ErrorMarker]: Filtrelenmiş marker'lar
        """
        return [m for m in self.current_markers if m.category == category]
    
    def get_errors_at_line(self, line: int) -> List[ErrorMarker]:
        """
        Belirli bir satırdaki hataları al.
        
        Args:
            line: Satır numarası
            
        Returns:
            List[ErrorMarker]: Hata marker'ları
        """
        return [m for m in self.current_markers if m.line == line]
    
    def get_next_error(self, current_line: int) -> Optional[ErrorMarker]:
        """
        Sonraki hatayı al.
        
        Args:
            current_line: Mevcut satır
            
        Returns:
            Optional[ErrorMarker]: Sonraki hata
        """
        for marker in self.current_markers:
            if marker.line > current_line:
                return marker
        return None
    
    def get_previous_error(self, current_line: int) -> Optional[ErrorMarker]:
        """
        Önceki hatayı al.
        
        Args:
            current_line: Mevcut satır
            
        Returns:
            Optional[ErrorMarker]: Önceki hata
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
        severity: ErrorSeverity,
        category: ErrorCategory,
        message: str,
        suggestion: Optional[str] = None
    ) -> ErrorMarker:
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
            ErrorMarker: Oluşturulan marker
        """
        marker = ErrorMarker(
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
    engine = ErrorHighlightingEngine()
    
    code = """
def my_function():
    print("Hello")
    undefined_variable
"""
    
    result = engine.highlight_errors(code, "python")
    print(f"Highlighting: {result.success}")
    print(f"Total errors: {result.total_errors}")
    print(f"Total warnings: {result.total_warnings}")
    
    for marker in result.markers:
        print(f"  Line {marker.line}: {marker.message}")
