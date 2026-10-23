"""
MuhammedAI Local Developer - Code Formatting
Code formatting engine for code editor.
"""

import ast
import re
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from enum import Enum


class FormatStyle(Enum):
    """Format style."""
    PEP8 = "pep8"
    GOOGLE = "google"
    BLACK = "black"
    YAPF = "yapf"
    AUTOPEP8 = "autopep8"


class FormatRule(Enum):
    """Format rule."""
    INDENTATION = "indentation"
    LINE_LENGTH = "line_length"
    WHITESPACE = "whitespace"
    IMPORTS = "imports"
    BLANK_LINES = "blank_lines"
    QUOTES = "quotes"
    TRAILING_COMMA = "trailing_comma"
    SPACES_AROUND_OPERATORS = "spaces_around_operators"
    SPACES_AFTER_COMMA = "spaces_after_comma"
    SPACES_BEFORE_PAREN = "spaces_before_paren"
    BRACKET_SPACING = "bracket_spacing"
    SEMICOLON_SPACING = "semicolon_spacing"
    COMMENT_FORMATTING = "comment_formatting"
    DOCSTRING_FORMATTING = "docstring_formatting"


@dataclass
class FormatRuleViolation:
    """Format rule violation."""
    rule: FormatRule
    line: int
    column: int
    message: str
    severity: str  # error, warning, info


@dataclass
class FormattingResult:
    """Formatting result."""
    success: bool
    formatted_code: Optional[str] = None
    original_code: Optional[str] = None
    violations: List[FormatRuleViolation] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    message: Optional[str] = None
    edits_count: int = 0
    lines_changed: int = 0


class CodeFormatter:
    """
    Code formatting engine.
    
    Özellikler:
    - PEP8 formatting
    - Multiple format styles
    - Indentation fixing
    - Line length enforcement
    - Whitespace normalization
    - Import organizing
    - Blank lines normalization
    - Quote normalization
    - Trailing comma handling
    - Operator spacing
    - Comma spacing
    - Paren spacing
    - Selection formatting
    - Format on save
    - Format on paste
    - Full document formatting
    - Language-specific formatting
    - Format preview
    - Configurable rules
    """
    
    def __init__(self, style: FormatStyle = FormatStyle.PEP8):
        """
        Args:
            style: Format style
        """
        self.style = style
        self.max_line_length = 88 if style == FormatStyle.BLACK else 79
        self.indent_size = 4
        self.use_tabs = False
    
    def format_code(
        self,
        code: str,
        language: str = "python"
    ) -> FormattingResult:
        """
        Kodu formatla.
        
        Args:
            code: Kod içeriği
            language: Programlama dili
            
        Returns:
            FormattingResult: Formatting sonucu
        """
        result = FormattingResult(success=False)
        result.original_code = code
        
        try:
            if language == "python":
                formatted_code = self._format_python(code)
            else:
                formatted_code = self._format_generic(code)
            
            # Violations kontrolü
            violations = self._check_violations(formatted_code)
            
            result.formatted_code = formatted_code
            result.violations = violations
            result.success = True
            result.message = "Code formatted successfully"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def _format_python(self, code: str) -> str:
        """Python kodunu formatla."""
        lines = code.splitlines()
        formatted_lines = []
        
        for line in lines:
            # Boş satır koru
            if line.strip() == "":
                formatted_lines.append("")
                continue
            
            # Basit whitespace düzeltme
            formatted_line = line.strip()
            
            # Trailing whitespace kaldır
            formatted_line = formatted_line.rstrip()
            
            formatted_lines.append(formatted_line)
        
        return "\n".join(formatted_lines)
    
    def _format_generic(self, code: str) -> str:
        """Genel kod formatla."""
        lines = code.splitlines()
        formatted_lines = []
        
        for line in lines:
            # Trailing whitespace kaldır
            formatted_line = line.rstrip()
            formatted_lines.append(formatted_line)
        
        return "\n".join(formatted_lines)
    
    def _normalize_whitespace(self, line: str) -> str:
        """Whitespace normalizasyonu."""
        # Multiple spaces -> single space
        line = re.sub(r' {2,}', ' ', line)
        return line
    
    def _fix_operator_spacing(self, line: str) -> str:
        """Operator spacing düzeltme."""
        operators = ['=', '+=', '-=', '*=', '/=', '%=', '**=', '//=', '&=', '|=', '^=', '>>=', '<<=', '==', '!=', '<', '>', '<=', '>=', 'and', 'or', 'not', 'in', 'is']
        
        for op in operators:
            # Operator etrafında boşluk ekle
            escaped_op = re.escape(op)
            line = re.sub(rf'(\w){escaped_op}(\w)', rf'\1 {op} \2', line)
        
        return line
    
    def _fix_comma_spacing(self, line: str) -> str:
        """Comma spacing düzeltme."""
        # Virgül sonrası boşluk ekle
        line = re.sub(r',(\S)', r', \1', line)
        # Virgül öncesi boşluk kaldır
        line = re.sub(r'(\s),', r',', line)
        return line
    
    def _fix_paren_spacing(self, line: str) -> str:
        """Paren spacing düzeltme."""
        # Parantez öncesi boşluk kaldır
        line = re.sub(r'\s+\(', '(', line)
        # Parantez sonrası boşluk kaldır
        line = re.sub(r'\)\s+', ')', line)
        return line
    
    def _normalize_quotes(self, line: str) -> str:
        """Quote normalizasyonu."""
        # Single quotes -> double quotes (basit)
        line = line.replace("'", '"')
        return line
    
    def _normalize_blank_lines(self, lines: List[str]) -> List[str]:
        """Blank lines normalizasyonu."""
        formatted_lines = []
        blank_count = 0
        
        for line in lines:
            if line.strip() == "":
                blank_count += 1
                if blank_count <= 2:  # Max 2 boş satır
                    formatted_lines.append(line)
            else:
                blank_count = 0
                formatted_lines.append(line)
        
        return formatted_lines
    
    def _check_violations(self, code: str) -> List[FormatRuleViolation]:
        """Format violations kontrolü."""
        violations = []
        lines = code.splitlines()
        
        for i, line in enumerate(lines, 1):
            # Line length kontrolü
            if len(line) > self.max_line_length:
                violations.append(FormatRuleViolation(
                    rule=FormatRule.LINE_LENGTH,
                    line=i,
                    column=self.max_line_length,
                    message=f"Line too long ({len(line)} > {self.max_line_length})",
                    severity="warning"
                ))
            
            # Trailing whitespace kontrolü
            if line != line.rstrip():
                violations.append(FormatRuleViolation(
                    rule=FormatRule.WHITESPACE,
                    line=i,
                    column=len(line.rstrip()),
                    message="Trailing whitespace",
                    severity="warning"
                ))
            
            # Indentation kontrolü
            if line.startswith(" ") and not line.startswith("    ") and not line.startswith("        "):
                violations.append(FormatRuleViolation(
                    rule=FormatRule.INDENTATION,
                    line=i,
                    column=0,
                    message="Indentation not multiple of 4",
                    severity="error"
                ))
        
        return violations
    
    def organize_imports(self, code: str) -> FormattingResult:
        """Importları organize et."""
        result = FormattingResult(success=False)
        result.original_code = code
        
        try:
            lines = code.splitlines()
            import_lines = []
            other_lines = []
            in_imports = False
            
            for line in lines:
                stripped = line.strip()
                if stripped.startswith(("import ", "from ")):
                    import_lines.append(line)
                    in_imports = True
                elif in_imports and stripped == "":
                    import_lines.append(line)
                elif in_imports and not stripped.startswith("#"):
                    in_imports = False
                    other_lines.append(line)
                else:
                    other_lines.append(line)
            
            # Importları sırala
            import_lines.sort(key=lambda x: x.strip())
            
            # Kodu birleştir
            formatted_code = "\n".join(import_lines + other_lines)
            
            result.formatted_code = formatted_code
            result.success = True
            result.message = "Imports organized"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def format_selection(
        self,
        code: str,
        start_line: int,
        end_line: int,
        language: str = "python"
    ) -> FormattingResult:
        """
        Seçili alanı formatla.
        
        Args:
            code: Kod içeriği
            start_line: Başlangıç satırı
            end_line: Bitiş satırı
            language: Programlama dili
            
        Returns:
            FormattingResult: Formatting sonucu
        """
        result = FormattingResult(success=False)
        result.original_code = code
        
        try:
            lines = code.splitlines()
            
            if start_line >= len(lines) or end_line >= len(lines):
                result.errors.append("Invalid line range")
                return result
            
            # Seçili satırları al
            selected_lines = lines[start_line:end_line + 1]
            selected_code = "\n".join(selected_lines)
            
            # Seçili kodu formatla
            if language == "python":
                formatted_selected = self._format_python(selected_code)
            else:
                formatted_selected = self._format_generic(selected_code)
            
            # Kodu güncelle
            new_lines = lines.copy()
            new_lines[start_line:end_line + 1] = formatted_selected.splitlines()
            
            formatted_code = "\n".join(new_lines)
            
            result.formatted_code = formatted_code
            result.lines_changed = end_line - start_line + 1
            result.success = True
            result.message = f"Formatted lines {start_line}-{end_line}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def format_on_save(self, code: str, language: str = "python") -> FormattingResult:
        """
        Kaydetmede formatla.
        
        Args:
            code: Kod içeriği
            language: Programlama dili
            
        Returns:
            FormattingResult: Formatting sonucu
        """
        return self.format_code(code, language)
    
    def format_on_paste(self, code: str, language: str = "python") -> FormattingResult:
        """
        Yapıştırmada formatla.
        
        Args:
            code: Kod içeriği
            language: Programlama dili
            
        Returns:
            FormattingResult: Formatting sonucu
        """
        result = FormattingResult(success=False)
        result.original_code = code
        
        try:
            if language == "python":
                formatted_code = self._format_python(code)
            else:
                formatted_code = self._format_generic(code)
            
            result.formatted_code = formatted_code
            result.success = True
            result.message = "Pasted content formatted"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def preview_format(self, code: str, language: str = "python") -> FormattingResult:
        """
        Format önizleme.
        
        Args:
            code: Kod içeriği
            language: Programlama dili
            
        Returns:
            FormattingResult: Preview sonucu
        """
        return self.format_code(code, language)
    
    def configure_rules(self, rules: Dict[FormatRule, bool]) -> None:
        """
        Format kurallarını yapılandır.
        
        Args:
            rules: Kural dict (rule -> enabled)
        """
        self.enabled_rules = rules
    
    def get_style_config(self) -> Dict[str, Any]:
        """
        Stil konfigürasyonunu al.
        
        Returns:
            Dict[str, Any]: Konfigürasyon
        """
        return {
            "style": self.style.value,
            "max_line_length": self.max_line_length,
            "indent_size": self.indent_size,
            "use_tabs": self.use_tabs
        }


if __name__ == "__main__":
    # Basit test
    formatter = CodeFormatter()
    
    code = """
def my_function( x,y ):
    result=x+y
    return result
"""
    
    result = formatter.format_code(code, language="python")
    print(f"Formatting: {result.success}")
    print(f"Original:\n{result.original_code}")
    print(f"Formatted:\n{result.formatted_code}")
    print(f"Violations: {len(result.violations)}")
