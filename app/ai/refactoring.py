"""
MuhammedAI Local Developer - Refactoring
Code refactoring operations.
"""

import ast
import re
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from enum import Enum


class RefactoringType(Enum):
    """Refactoring type."""
    RENAME_SYMBOL = "rename_symbol"
    EXTRACT_FUNCTION = "extract_function"
    EXTRACT_VARIABLE = "extract_variable"
    INLINE_VARIABLE = "inline_variable"
    MOVE_SYMBOL = "move_symbol"
    CHANGE_SIGNATURE = "change_signature"
    SAFE_DELETE = "safe_delete"
    ORGANIZE_IMPORTS = "organize_imports"


@dataclass
class RefactoringEdit:
    """Refactoring edit."""
    file_path: str
    start_line: int
    start_column: int
    end_line: int
    end_column: int
    old_text: str
    new_text: str


@dataclass
class RefactoringResult:
    """Refactoring sonucu."""
    success: bool
    edits: List[RefactoringEdit] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    message: Optional[str] = None


class RefactoringEngine:
    """
    Refactoring engine.
    
    Özellikler:
    - Rename symbol
    - Extract function/method
    - Extract variable
    - Inline variable
    - Move symbol
    - Change signature
    - Safe delete
    - Organize imports
    """
    
    def __init__(self, codebase_index=None):
        """
        Args:
            codebase_index: CodebaseIndex instance
        """
        self.codebase_index = codebase_index
    
    def rename_symbol(
        self,
        file_path: str,
        old_name: str,
        new_name: str,
        line: int,
        column: int
    ) -> RefactoringResult:
        """
        Symbol rename.
        
        Args:
            file_path: Dosya yolu
            old_name: Eski ad
            new_name: Yeni ad
            line: Satır numarası
            column: Sütun numarası
            
        Returns:
            RefactoringResult: Refactoring sonucu
        """
        result = RefactoringResult(success=False)
        
        try:
            # Dosyayı oku
            content = Path(file_path).read_text(encoding='utf-8')
            lines = content.splitlines()
            
            # Basit string replace (gerçek implementation AST bazlı olmalı)
            new_content = content.replace(old_name, new_name)
            
            if new_content != content:
                edit = RefactoringEdit(
                    file_path=file_path,
                    start_line=1,
                    start_column=0,
                    end_line=len(lines),
                    end_column=len(lines[-1]),
                    old_text=content,
                    new_text=new_content
                )
                result.edits.append(edit)
                result.success = True
                result.message = f"Renamed '{old_name}' to '{new_name}'"
            else:
                result.errors.append(f"Symbol '{old_name}' not found")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def extract_function(
        self,
        file_path: str,
        start_line: int,
        end_line: int,
        function_name: str
    ) -> RefactoringResult:
        """
        Extract function.
        
        Args:
            file_path: Dosya yolu
            start_line: Başlangıç satırı
            end_line: Bitiş satırı
            function_name: Yeni function adı
            
        Returns:
            RefactoringResult: Refactoring sonucu
        """
        result = RefactoringResult(success=False)
        
        try:
            # Dosyayı oku
            content = Path(file_path).read_text(encoding='utf-8')
            lines = content.splitlines()
            
            # Seçilen satırları al
            selected_lines = lines[start_line - 1:end_line]
            selected_code = "\n".join(selected_lines)
            
            # Yeni function oluştur
            new_function = f"\ndef {function_name}():\n    {selected_code.replace(chr(10), chr(10) + '    ')}\n"
            
            # Seçilen kodu function call ile değiştir
            call_code = f"{function_name}()"
            
            # Edits oluştur
            # 1. Function'ı ekle (seçilen kodun öncesine)
            edit1 = RefactoringEdit(
                file_path=file_path,
                start_line=start_line,
                start_column=0,
                end_line=start_line,
                end_column=0,
                old_text="",
                new_text=new_function
            )
            
            # 2. Seçilen kodu function call ile değiştir
            old_selected = "\n".join(selected_lines)
            edit2 = RefactoringEdit(
                file_path=file_path,
                start_line=start_line + len(new_function.splitlines()),
                start_column=0,
                end_line=end_line + len(new_function.splitlines()),
                end_column=len(selected_lines[-1]),
                old_text=old_selected,
                new_text=call_code
            )
            
            result.edits.extend([edit1, edit2])
            result.success = True
            result.message = f"Extracted function '{function_name}'"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def extract_variable(
        self,
        file_path: str,
        start_line: int,
        end_line: int,
        start_column: int,
        end_column: int,
        variable_name: str
    ) -> RefactoringResult:
        """
        Extract variable.
        
        Args:
            file_path: Dosya yolu
            start_line: Başlangıç satırı
            end_line: Bitiş satırı
            start_column: Başlangıç sütunu
            end_column: Bitiş sütunu
            variable_name: Yeni variable adı
            
        Returns:
            RefactoringResult: Refactoring sonucu
        """
        result = RefactoringResult(success=False)
        
        try:
            # Dosyayı oku
            content = Path(file_path).read_text(encoding='utf-8')
            lines = content.splitlines()
            
            # Seçilen metni al
            selected_text = lines[start_line - 1][start_column:end_column]
            
            # Variable declaration ekle (satırın başına)
            new_line = f"{variable_name} = {selected_text}\n    " + lines[start_line - 1][end_column:]
            
            # Seçilen metni variable name ile değiştir
            old_line = lines[start_line - 1]
            new_line_with_var = old_line[:start_column] + variable_name + old_line[end_column:]
            
            edit = RefactoringEdit(
                file_path=file_path,
                start_line=start_line,
                start_column=0,
                end_line=start_line,
                end_column=len(old_line),
                old_text=old_line,
                new_text=new_line_with_var
            )
            
            result.edits.append(edit)
            result.success = True
            result.message = f"Extracted variable '{variable_name}'"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def inline_variable(
        self,
        file_path: str,
        variable_name: str,
        line: int
    ) -> RefactoringResult:
        """
        Inline variable.
        
        Args:
            file_path: Dosya yolu
            variable_name: Variable adı
            line: Satır numarası
            
        Returns:
            RefactoringResult: Refactoring sonucu
        """
        result = RefactoringResult(success=False)
        
        try:
            # Dosyayı oku
            content = Path(file_path).read_text(encoding='utf-8')
            lines = content.splitlines()
            
            # Variable declaration'ı bul
            var_pattern = rf"{variable_name}\s*=\s*(.+)"
            var_value = None
            
            for i, line_text in enumerate(lines):
                match = re.match(var_pattern, line_text)
                if match:
                    var_value = match.group(1).strip()
                    # Variable declaration'ı sil
                    edit1 = RefactoringEdit(
                        file_path=file_path,
                        start_line=i + 1,
                        start_column=0,
                        end_line=i + 1,
                        end_column=len(line_text),
                        old_text=line_text,
                        new_text=""
                    )
                    result.edits.append(edit1)
                    break
            
            if var_value:
                # Variable kullanımlarını inline et
                for i, line_text in enumerate(lines):
                    if variable_name in line_text:
                        new_line = line_text.replace(variable_name, var_value)
                        edit = RefactoringEdit(
                            file_path=file_path,
                            start_line=i + 1,
                            start_column=0,
                            end_line=i + 1,
                            end_column=len(line_text),
                            old_text=line_text,
                            new_text=new_line
                        )
                        result.edits.append(edit)
                
                result.success = True
                result.message = f"Inlined variable '{variable_name}'"
            else:
                result.errors.append(f"Variable '{variable_name}' not found")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def organize_imports(
        self,
        file_path: str
    ) -> RefactoringResult:
        """
        Organize imports.
        
        Args:
            file_path: Dosya yolu
            
        Returns:
            RefactoringResult: Refactoring sonucu
        """
        result = RefactoringResult(success=False)
        
        try:
            # Dosyayı oku
            content = Path(file_path).read_text(encoding='utf-8')
            lines = content.splitlines()
            
            # Import satırlarını bul
            import_lines = []
            other_lines = []
            
            for line in lines:
                if line.strip().startswith("import ") or line.strip().startswith("from "):
                    import_lines.append(line)
                else:
                    other_lines.append(line)
            
            # Importları sırala
            import_lines.sort()
            
            # Duplicate'ları kaldır
            seen = set()
            unique_imports = []
            for imp in import_lines:
                if imp not in seen:
                    seen.add(imp)
                    unique_imports.append(imp)
            
            # Yeni content oluştur
            new_lines = unique_imports + [""] + other_lines
            new_content = "\n".join(new_lines)
            
            if new_content != content:
                edit = RefactoringEdit(
                    file_path=file_path,
                    start_line=1,
                    start_column=0,
                    end_line=len(lines),
                    end_column=len(lines[-1]),
                    old_text=content,
                    new_text=new_content
                )
                result.edits.append(edit)
                result.success = True
                result.message = "Organized imports"
            else:
                result.warnings.append("No changes needed")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def safe_delete(
        self,
        file_path: str,
        symbol_name: str,
        line: int
    ) -> RefactoringResult:
        """
        Safe delete (symbol'ın kullanımını kontrol et).
        
        Args:
            file_path: Dosya yolu
            symbol_name: Symbol adı
            line: Satır numarası
            
        Returns:
            RefactoringResult: Refactoring sonucu
        """
        result = RefactoringResult(success=False)
        
        try:
            # Dosyayı oku
            content = Path(file_path).read_text(encoding='utf-8')
            
            # Symbol'ın kullanımını kontrol et
            usage_count = content.count(symbol_name)
            
            if usage_count > 1:
                result.errors.append(f"Symbol '{symbol_name}' is used {usage_count} times. Cannot safely delete.")
                return result
            
            # Symbol'ı sil
            lines = content.splitlines()
            target_line = lines[line - 1]
            
            edit = RefactoringEdit(
                file_path=file_path,
                start_line=line,
                start_column=0,
                end_line=line,
                end_column=len(target_line),
                old_text=target_line,
                new_text=""
            )
            
            result.edits.append(edit)
            result.success = True
            result.message = f"Safely deleted '{symbol_name}'"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def apply_edits(self, edits: List[RefactoringEdit]) -> RefactoringResult:
        """
        Edits'i uygula.
        
        Args:
            edits: Edit listesi
            
        Returns:
            RefactoringResult: Uygulama sonucu
        """
        result = RefactoringResult(success=False)
        
        try:
            # Dosya bazında grupla
            file_edits: Dict[str, List[RefactoringEdit]] = {}
            for edit in edits:
                if edit.file_path not in file_edits:
                    file_edits[edit.file_path] = []
                file_edits[edit.file_path].append(edit)
            
            # Her dosya için edits uygula
            for file_path, file_edit_list in file_edits.items():
                # Dosyayı oku
                content = Path(file_path).read_text(encoding='utf-8')
                
                # Edits'i uygula (basit implementation)
                for edit in reversed(file_edit_list):  # Reverse order to preserve positions
                    lines = content.splitlines()
                    
                    # Basit replace (gerçek implementation position-aware olmalı)
                    if edit.old_text in content:
                        content = content.replace(edit.old_text, edit.new_text, 1)
                
                # Dosyayı yaz
                Path(file_path).write_text(content, encoding='utf-8')
            
            result.success = True
            result.message = f"Applied {len(edits)} edits"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result


if __name__ == "__main__":
    # Basit test
    engine = RefactoringEngine()
    
    # Organize imports test
    result = engine.organize_imports("app/ai/refactoring.py")
    print(f"Organize imports: {result.success}")
    print(f"Message: {result.message}")
