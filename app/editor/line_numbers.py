"""
MuhammedAI Local Developer - Line Numbers
Line numbers engine for code editor.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum


class LineNumberStyle(Enum):
    """Line number style."""
    STANDARD = "standard"
    RELATIVE = "relative"
    BOTH = "both"


class LineNumberFormat(Enum):
    """Line number format."""
    DECIMAL = "decimal"
    HEXADECIMAL = "hexadecimal"
    OCTAL = "octal"
    BINARY = "binary"


@dataclass
class LineNumber:
    """Line number."""
    number: int
    text: str
    is_active: bool = False
    has_breakpoint: bool = False
    has_error: bool = False
    has_warning: bool = False


@dataclass
class LineNumbersResult:
    """Line numbers result."""
    success: bool
    line_numbers: List[LineNumber] = field(default_factory=list)
    html: Optional[str] = None
    total_lines: int = 0
    errors: List[str] = field(default_factory=list)
    message: Optional[str] = None


class LineNumberGenerator:
    """
    Line numbers generator.
    
    Özellikler:
    - Standard line numbers
    - Relative line numbers
    - Multiple number formats
    - Active line highlighting
    - Breakpoint support
    - Error/warning indicators
    - HTML output
    - Custom styling
    """
    
    def __init__(
        self,
        style: LineNumberStyle = LineNumberStyle.STANDARD,
        number_format: LineNumberFormat = LineNumberFormat.DECIMAL,
        start_line: int = 1
    ):
        """
        Args:
            style: Line number style
            number_format: Number format
            start_line: Starting line number
        """
        self.style = style
        self.number_format = number_format
        self.start_line = start_line
        self.active_line: Optional[int] = None
        self.breakpoints: set = set()
        self.error_lines: set = set()
        self.warning_lines: set = set()
    
    def generate_line_numbers(
        self,
        code: str,
        active_line: Optional[int] = None
    ) -> LineNumbersResult:
        """
        Satır numaralarını oluştur.
        
        Args:
            code: Kod içeriği
            active_line: Aktif satır numarası
            
        Returns:
            LineNumbersResult: Line numbers sonucu
        """
        result = LineNumbersResult(success=False)
        
        try:
            lines = code.splitlines()
            result.total_lines = len(lines)
            
            line_numbers = []
            
            for i, line in enumerate(lines, start=self.start_line):
                # Line number text'i oluştur
                if self.style == LineNumberStyle.STANDARD:
                    text = self._format_number(i)
                elif self.style == LineNumberStyle.RELATIVE:
                    if active_line:
                        text = self._format_number(abs(i - active_line))
                    else:
                        text = self._format_number(i)
                else:  # BOTH
                    standard = self._format_number(i)
                    if active_line:
                        relative = self._format_number(abs(i - active_line))
                        text = f"{standard}/{relative}"
                    else:
                        text = standard
                
                # Line number oluştur
                line_number = LineNumber(
                    number=i,
                    text=text,
                    is_active=(i == active_line),
                    has_breakpoint=(i in self.breakpoints),
                    has_error=(i in self.error_lines),
                    has_warning=(i in self.warning_lines)
                )
                
                line_numbers.append(line_number)
            
            result.line_numbers = line_numbers
            result.html = self._generate_html(line_numbers)
            result.success = True
            result.message = f"Generated {len(line_numbers)} line numbers"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def set_active_line(self, line: int):
        """Aktif satırı ayarla."""
        self.active_line = line
    
    def add_breakpoint(self, line: int):
        """Breakpoint ekle."""
        self.breakpoints.add(line)
    
    def remove_breakpoint(self, line: int):
        """Breakpoint kaldır."""
        self.breakpoints.discard(line)
    
    def add_error_line(self, line: int):
        """Error satırı ekle."""
        self.error_lines.add(line)
    
    def remove_error_line(self, line: int):
        """Error satırı kaldır."""
        self.error_lines.discard(line)
    
    def add_warning_line(self, line: int):
        """Warning satırı ekle."""
        self.warning_lines.add(line)
    
    def remove_warning_line(self, line: int):
        """Warning satırı kaldır."""
        self.warning_lines.discard(line)
    
    def _format_number(self, number: int) -> str:
        """Numarayı formatla."""
        if self.number_format == LineNumberFormat.DECIMAL:
            return str(number)
        elif self.number_format == LineNumberFormat.HEXADECIMAL:
            return hex(number)[2:].upper()
        elif self.number_format == LineNumberFormat.OCTAL:
            return oct(number)[2:]
        elif self.number_format == LineNumberFormat.BINARY:
            return bin(number)[2:]
        else:
            return str(number)
    
    def _generate_html(self, line_numbers: List[LineNumber]) -> str:
        """HTML output oluştur."""
        html_lines = []
        
        for line_number in line_numbers:
            classes = ["line-number"]
            
            if line_number.is_active:
                classes.append("active")
            if line_number.has_breakpoint:
                classes.append("breakpoint")
            if line_number.has_error:
                classes.append("error")
            if line_number.has_warning:
                classes.append("warning")
            
            class_str = " ".join(classes)
            html_lines.append(f'<div class="{class_str}" data-line="{line_number.number}">{line_number.text}</div>')
        
        return '<div class="line-numbers">' + "\n".join(html_lines) + "</div>"


if __name__ == "__main__":
    # Basit test
    generator = LineNumberGenerator()
    
    code = """
def my_function(x, y):
    result = x + y
    return result
"""
    
    result = generator.generate_line_numbers(code, active_line=2)
    print(f"Generation: {result.success}")
    print(f"Total lines: {result.total_lines}")
    print(f"Line numbers: {len(result.line_numbers)}")
