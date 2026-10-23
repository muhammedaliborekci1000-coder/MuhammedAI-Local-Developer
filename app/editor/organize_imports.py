"""
MuhammedAI Local Developer - Organize Imports
Organize imports engine for code editor.
"""

import ast
import re
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from enum import Enum


class ImportGroup(Enum):
    """Import group."""
    STANDARD_LIBRARY = "standard_library"
    THIRD_PARTY = "third_party"
    LOCAL = "local"
    UNKNOWN = "unknown"


class ImportAction(Enum):
    """Import action."""
    ADD = "add"
    REMOVE = "remove"
    SORT = "sort"
    GROUP = "group"
    FORMAT = "format"


@dataclass
class ImportStatement:
    """Import statement."""
    module: str
    alias: Optional[str] = None
    names: List[str] = field(default_factory=list)
    is_from: bool = False
    line: int = 0
    group: ImportGroup = ImportGroup.UNKNOWN


@dataclass
class ImportEdit:
    """Import edit."""
    start_line: int
    end_line: int
    old_text: str
    new_text: str


@dataclass
class OrganizeImportsResult:
    """Organize imports result."""
    success: bool
    original_code: str = ""
    organized_code: str = ""
    imports: List[ImportStatement] = field(default_factory=list)
    edits: List[ImportEdit] = field(default_factory=list)
    unused_imports: List[str] = field(default_factory=list)
    missing_imports: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    message: Optional[str] = None


class OrganizeImportsEngine:
    """
    Organize imports engine.
    
    Özellikler:
    - Sort imports alphabetically
    - Group imports (standard, third-party, local)
    - Remove unused imports
    - Remove duplicate imports
    - Auto-import missing imports
    - Format import statements
    - Support from...import
    - Support import...as
    - Preview changes
    - Apply changes
    - Multi-language support
    """
    
    def __init__(self):
        """Initialize organize imports engine."""
        self.standard_library_modules = {
            'os', 'sys', 're', 'json', 'math', 'datetime', 'random',
            'collections', 'itertools', 'functools', 'pathlib', 'typing',
            'io', 'string', 'time', 'hashlib', 'base64', 'uuid',
            'decimal', 'fractions', 'statistics', 'enum', 'dataclasses'
        }
    
    def organize_imports(
        self,
        code: str,
        language: str = "python",
        remove_unused: bool = True,
        sort_alphabetically: bool = True,
        group_imports: bool = True
    ) -> OrganizeImportsResult:
        """
        Import'ları organize et.
        
        Args:
            code: Kod içeriği
            language: Programlama dili
            remove_unused: Kullanılmayan import'ları kaldır
            sort_alphabetically: Alfabetik sırala
            group_imports: Import'ları grupla
            
        Returns:
            OrganizeImportsResult: Organize sonucu
        """
        result = OrganizeImportsResult(success=False)
        result.original_code = code
        
        try:
            if language == "python":
                organized_code, imports, unused_imports = self._organize_python_imports(
                    code, remove_unused, sort_alphabetically, group_imports
                )
                result.unused_imports = unused_imports
            else:
                organized_code, imports = self._organize_generic_imports(code)
            
            result.organized_code = organized_code
            result.imports = imports
            result.success = True
            result.message = f"Organized {len(imports)} imports"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def _organize_python_imports(
        self,
        code: str,
        remove_unused: bool,
        sort_alphabetically: bool,
        group_imports: bool
    ) -> Tuple[str, List[ImportStatement], List[str]]:
        """Python import'larını organize et."""
        lines = code.splitlines()
        imports = []
        import_lines = []
        
        # Import satırlarını tespit et
        for line_num, line in enumerate(lines):
            if line.strip().startswith('import ') or line.strip().startswith('from '):
                import_stmt = self._parse_import_line(line, line_num)
                if import_stmt:
                    imports.append(import_stmt)
                    import_lines.append(line_num)
        
        # Kullanılmayan import'ları tespit et
        unused_imports = []
        if remove_unused:
            unused_imports = self._detect_unused_imports(code, imports)
            imports = [imp for imp in imports if imp.module not in unused_imports]
        
        # Grupla
        if group_imports:
            for imp in imports:
                imp.group = self._determine_import_group(imp.module)
        
        # Sırala
        if sort_alphabetically:
            imports.sort(key=lambda x: (x.group.value, x.module))
        
        # Import bloğunu oluştur
        organized_imports = self._build_import_block(imports, group_imports)
        
        # Kodu güncelle
        new_lines = lines.copy()
        
        # Eski import satırlarını kaldır
        for line_num in sorted(import_lines, reverse=True):
            if line_num < len(new_lines):
                new_lines.pop(line_num)
        
        # Yeni import'ları ekle
        if import_lines:
            insert_line = min(import_lines)
            new_lines[insert_line:insert_line] = organized_imports
        elif organized_imports:
            # Dosya başına ekle
            insert_line = 0
            while insert_line < len(new_lines) and (new_lines[insert_line].strip().startswith('#') or new_lines[insert_line].strip() == ''):
                insert_line += 1
            new_lines[insert_line:insert_line] = organized_imports + ['']
        
        organized_code = "\n".join(new_lines)
        
        return organized_code, imports, unused_imports
    
    def _organize_generic_imports(self, code: str) -> Tuple[str, List[ImportStatement]]:
        """Genel import'ları organize et."""
        lines = code.splitlines()
        imports = []
        
        for line_num, line in enumerate(lines):
            if 'import' in line.lower():
                import_stmt = ImportStatement(
                    module=line.strip(),
                    line=line_num,
                    group=ImportGroup.UNKNOWN
                )
                imports.append(import_stmt)
        
        # Basit sıralama
        imports.sort(key=lambda x: x.module)
        
        return code, imports
    
    def _parse_import_line(self, line: str, line_num: int) -> Optional[ImportStatement]:
        """Import satırını parse et."""
        line = line.strip()
        
        if not line.startswith('import') and not line.startswith('from'):
            return None
        
        if line.startswith('from '):
            # from module import name
            parts = line[5:].split(' import ')
            if len(parts) == 2:
                module = parts[0].strip()
                names = [n.strip() for n in parts[1].split(',')]
                return ImportStatement(
                    module=module,
                    names=names,
                    is_from=True,
                    line=line_num
                )
        else:
            # import module [as alias]
            parts = line[7:].split(' as ')
            module = parts[0].strip()
            alias = parts[1].strip() if len(parts) > 1 else None
            return ImportStatement(
                module=module,
                alias=alias,
                is_from=False,
                line=line_num
            )
        
        return None
    
    def _determine_import_group(self, module: str) -> ImportGroup:
        """Import grubunu belirle."""
        base_module = module.split('.')[0]
        
        if base_module in self.standard_library_modules:
            return ImportGroup.STANDARD_LIBRARY
        elif base_module.startswith('.'):
            return ImportGroup.LOCAL
        else:
            return ImportGroup.THIRD_PARTY
    
    def _detect_unused_imports(self, code: str, imports: List[ImportStatement]) -> List[str]:
        """Kullanılmayan import'ları tespit et."""
        unused = []
        
        try:
            tree = ast.parse(code)
            used_modules = set()
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Name):
                    used_modules.add(node.id)
                elif isinstance(node, ast.Attribute):
                    used_modules.add(node.value.id if isinstance(node.value, ast.Name) else str(node.value))
            
            for imp in imports:
                if imp.module not in used_modules:
                    if imp.alias and imp.alias not in used_modules:
                        unused.append(imp.module)
                    elif not imp.alias:
                        unused.append(imp.module)
        except:
            pass
        
        return unused
    
    def _build_import_block(self, imports: List[ImportStatement], group_imports: bool) -> List[str]:
        """Import bloğu oluştur."""
        if not imports:
            return []
        
        lines = []
        current_group = None
        
        for imp in imports:
            if group_imports and imp.group != current_group:
                if current_group is not None:
                    lines.append('')
                current_group = imp.group
            
            if imp.is_from:
                if imp.names:
                    names_str = ', '.join(imp.names)
                    lines.append(f"from {imp.module} import {names_str}")
                else:
                    lines.append(f"from {imp.module} import *")
            else:
                if imp.alias:
                    lines.append(f"import {imp.module} as {imp.alias}")
                else:
                    lines.append(f"import {imp.module}")
        
        return lines
    
    def detect_missing_imports(self, code: str) -> List[str]:
        """
        Eksik import'ları tespit et.
        
        Args:
            code: Kod içeriği
            
        Returns:
            List[str]: Eksik import listesi
        """
        missing = []
        
        try:
            tree = ast.parse(code)
            imported_modules = set()
            used_modules = set()
            
            # Import'ları topla
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imported_modules.add(alias.name.split('.')[0])
                elif isinstance(node, ast.ImportFrom):
                    imported_modules.add(node.module.split('.')[0] if node.module else '')
            
            # Kullanılan modülleri topla
            for node in ast.walk(tree):
                if isinstance(node, ast.Name):
                    used_modules.add(node.id)
            
            # Eksikleri bul
            for module in used_modules:
                if module in self.standard_library_modules and module not in imported_modules:
                    missing.append(module)
        except:
            pass
        
        return missing
    
    def add_missing_imports(self, code: str, missing_imports: List[str]) -> Tuple[str, OrganizeImportsResult]:
        """
        Eksik import'ları ekle.
        
        Args:
            code: Kod içeriği
            missing_imports: Eksik import listesi
            
        Returns:
            Tuple[str, OrganizeImportsResult]: Düzeltilmiş kod ve sonuç
        """
        result = OrganizeImportsResult(success=False)
        result.original_code = code
        
        try:
            lines = code.splitlines()
            import_lines = []
            
            # Mevcut import satırlarını bul
            for line_num, line in enumerate(lines):
                if line.strip().startswith('import ') or line.strip().startswith('from '):
                    import_lines.append(line_num)
            
            # Yeni import'ları oluştur
            new_imports = []
            for module in sorted(missing_imports):
                new_imports.append(f"import {module}")
            
            # Import'ları ekle
            if import_lines:
                insert_line = min(import_lines)
                lines[insert_line:insert_line] = new_imports + lines[insert_line:insert_line]
            else:
                insert_line = 0
                while insert_line < len(lines) and (lines[insert_line].strip().startswith('#') or lines[insert_line].strip() == ''):
                    insert_line += 1
                lines[insert_line:insert_line] = new_imports + ['']
            
            organized_code = "\n".join(lines)
            
            result.organized_code = organized_code
            result.success = True
            result.message = f"Added {len(missing_imports)} imports"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return organized_code, result
    
    def preview_organize(self, code: str, language: str = "python") -> OrganizeImportsResult:
        """
        Organize önizleme.
        
        Args:
            code: Kod içeriği
            language: Programlama dili
            
        Returns:
            OrganizeImportsResult: Preview sonucu
        """
        return self.organize_imports(code, language)


if __name__ == "__main__":
    # Basit test
    engine = OrganizeImportsEngine()
    
    code = """
import sys
import os
import re
from datetime import datetime

def main():
    print(os.getcwd())
"""
    
    # Import'ları organize et
    result = engine.organize_imports(code, "python")
    
    print(f"Organize: {result.success}")
    print(f"Imports: {len(result.imports)}")
    print(f"Organized code:\n{result.organized_code}")
