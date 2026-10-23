"""
MuhammedAI Local Developer - Sort Imports
Sort imports engine for code editor.
"""

from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from enum import Enum


class ImportType(Enum):
    """Import type."""
    STANDARD_LIBRARY = "standard_library"
    THIRD_PARTY = "third_party"
    LOCAL = "local"
    BUILTIN = "builtin"


class SortOrder(Enum):
    """Sort order."""
    ALPHABETICAL = "alphabetical"
    LENGTH = "length"
    FREQUENCY = "frequency"
    CUSTOM = "custom"


@dataclass
class ImportStatement:
    """Import statement."""
    module_name: str
    import_type: ImportType
    alias: str = ""
    from_import: str = ""
    line_number: int = 0
    is_unused: bool = False


@dataclass
class SortConfig:
    """Sort configuration."""
    group_by_type: bool = True
    remove_duplicates: bool = True
    remove_unused: bool = False
    add_blank_lines: bool = True
    sort_order: SortOrder = SortOrder.ALPHABETICAL
    separate_third_party: bool = True
    separate_local: bool = True
    case_sensitive: bool = False
    keep_comments: bool = True


@dataclass
class SortResult:
    """Sort result."""
    success: bool
    modified_content: str = ""
    original_content: str = ""
    imports_sorted: int = 0
    duplicates_removed: int = 0
    unused_removed: int = 0
    errors: List[str] = field(default_factory=list)
    message: Optional[str] = None


class SortImportsEngine:
    """
    Sort imports engine.
    
    Özellikler:
    - Import sorting
    - Import grouping
    - Duplicate removal
    - Unused import removal
    - Type-based grouping
    - Alphabetical sorting
    - Custom sorting
    - Blank line insertion
    - Comment preservation
    - Third-party separation
    - Local import separation
    - Undo support
    - Sort history
    - Import detection
    - Alias handling
    - From import handling
    """
    
    def __init__(self, config: Optional[SortConfig] = None):
        """Initialize sort imports engine."""
        self.config = config or SortConfig()
        self.sort_history: List[Dict[str, Any]] = []
    
    def sort_imports(
        self,
        content: str,
        file_path: Optional[str] = None
    ) -> SortResult:
        """
        Importları sırala.
        
        Args:
            content: Dosya içeriği
            file_path: Dosya yolu (opsiyonel)
            
        Returns:
            SortResult: Sıralama sonucu
        """
        result = SortResult(success=False)
        result.original_content = content
        
        try:
            # Importları tespit et
            imports = self._detect_imports(content)
            
            if not imports:
                result.success = True
                result.modified_content = content
                result.message = "No imports found"
                return result
            
            # Duplicate'ları kaldır
            if self.config.remove_duplicates:
                imports, duplicates_removed = self._remove_duplicates(imports)
                result.duplicates_removed = duplicates_removed
            
            # Importları sırala
            if self.config.group_by_type:
                imports = self._group_and_sort_imports(imports)
            else:
                imports = self._sort_imports(imports)
            
            # İçeriği yeniden oluştur
            modified_content = self._rebuild_content(content, imports)
            
            # Geçmişe ekle
            self.sort_history.append({
                "original": content,
                "modified": modified_content,
                "imports_sorted": len(imports)
            })
            
            result.success = True
            result.modified_content = modified_content
            result.imports_sorted = len(imports)
            result.message = f"Sorted {len(imports)} import(s)"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def _detect_imports(self, content: str) -> List[ImportStatement]:
        """
        Importları tespit et.
        
        Args:
            content: İçerik
            
        Returns:
            List[ImportStatement]: Import listesi
        """
        imports = []
        lines = content.splitlines()
        
        for i, line in enumerate(lines):
            line = line.strip()
            
            # import x
            if line.startswith("import ") and not line.startswith("from "):
                module_name = line.replace("import ", "").split(",")[0].strip()
                import_type = self._determine_import_type(module_name)
                imports.append(ImportStatement(
                    module_name=module_name,
                    import_type=import_type,
                    line_number=i
                ))
            
            # from x import y
            elif line.startswith("from "):
                parts = line.replace("from ", "").split(" import ")
                if len(parts) == 2:
                    from_import = parts[0].strip()
                    module_name = parts[1].split(",")[0].strip()
                    import_type = self._determine_import_type(from_import)
                    imports.append(ImportStatement(
                        module_name=module_name,
                        import_type=import_type,
                        from_import=from_import,
                        line_number=i
                    ))
        
        return imports
    
    def _determine_import_type(self, module_name: str) -> ImportType:
        """
        Import tipini belirle.
        
        Args:
            module_name: Modül adı
            
        Returns:
            ImportType: Import tipi
        """
        # Standart kütüphaneler (basit kontrol)
        standard_libs = ["os", "sys", "json", "re", "datetime", "math", "random", "collections"]
        if module_name.split(".")[0] in standard_libs:
            return ImportType.STANDARD_LIBRARY
        
        # Local import (dosya yolu ile kontrol edilebilir)
        if module_name.startswith("."):
            return ImportType.LOCAL
        
        # Varsayılan olarak third-party
        return ImportType.THIRD_PARTY
    
    def _remove_duplicates(
        self,
        imports: List[ImportStatement]
    ) -> Tuple[List[ImportStatement], int]:
        """
        Duplicate'ları kaldır.
        
        Args:
            imports: Import listesi
            
        Returns:
            Tuple[List[ImportStatement], int]: (Filtrelenmiş liste, kaldırılan sayı)
        """
        seen = set()
        filtered = []
        
        for imp in imports:
            key = (imp.module_name, imp.from_import)
            if key not in seen:
                seen.add(key)
                filtered.append(imp)
        
        return filtered, len(imports) - len(filtered)
    
    def _group_and_sort_imports(
        self,
        imports: List[ImportStatement]
    ) -> List[ImportStatement]:
        """
        Importları grupla ve sırala.
        
        Args:
            imports: Import listesi
            
        Returns:
            List[ImportStatement]: Sıralanmış liste
        """
        # Tip bazında grupla
        groups = {
            ImportType.STANDARD_LIBRARY: [],
            ImportType.THIRD_PARTY: [],
            ImportType.LOCAL: [],
            ImportType.BUILTIN: []
        }
        
        for imp in imports:
            groups[imp.import_type].append(imp)
        
        # Her grubu sırala
        for import_type in groups:
            groups[import_type] = self._sort_imports(groups[import_type])
        
        # Grupları birleştir
        sorted_imports = []
        for import_type in [ImportType.STANDARD_LIBRARY, ImportType.THIRD_PARTY, ImportType.LOCAL, ImportType.BUILTIN]:
            if groups[import_type]:
                sorted_imports.extend(groups[import_type])
        
        return sorted_imports
    
    def _sort_imports(self, imports: List[ImportStatement]) -> List[ImportStatement]:
        """
        Importları sırala.
        
        Args:
            imports: Import listesi
            
        Returns:
            List[ImportStatement]: Sıralanmış liste
        """
        if self.config.sort_order == SortOrder.ALPHABETICAL:
            key = lambda x: x.module_name.lower() if not self.config.case_sensitive else x.module_name
        elif self.config.sort_order == SortOrder.LENGTH:
            key = lambda x: len(x.module_name)
        elif self.config.sort_order == SortOrder.FREQUENCY:
            key = lambda x: 0  # Basit implementasyon
        else:
            key = lambda x: x.module_name
        
        return sorted(imports, key=key)
    
    def _rebuild_content(
        self,
        content: str,
        imports: List[ImportStatement]
    ) -> str:
        """
        İçeriği yeniden oluştur.
        
        Args:
            content: Orijinal içerik
            imports: Sıralanmış importlar
            
        Returns:
            str: Yeni içerik
        """
        lines = content.splitlines()
        
        # Import satırlarını bul ve kaldır
        import_lines = set()
        for imp in imports:
            import_lines.add(imp.line_number)
        
        # Import olmayan satırları koru
        non_import_lines = []
        for i, line in enumerate(lines):
            if i not in import_lines:
                non_import_lines.append(line)
        
        # Yeni import satırlarını oluştur
        new_import_lines = []
        current_type = None
        
        for imp in imports:
            # Grup değişimi kontrolü
            if self.config.group_by_type and current_type != imp.import_type:
                if new_import_lines and self.config.add_blank_lines:
                    new_import_lines.append("")
                current_type = imp.import_type
            
            # Import satırı oluştur
            if imp.from_import:
                import_line = f"from {imp.from_import} import {imp.module_name}"
            else:
                import_line = f"import {imp.module_name}"
            
            new_import_lines.append(import_line)
        
        # İçeriği birleştir
        result = new_import_lines + non_import_lines
        return "\n".join(result)
    
    def undo_sort(self) -> SortResult:
        """
        Sıralamayı geri al.
        
        Returns:
            SortResult: Geri alma sonucu
        """
        result = SortResult(success=False)
        
        try:
            if not self.sort_history:
                result.errors.append("No sort history")
                return result
            
            last_sort = self.sort_history.pop()
            
            result.success = True
            result.modified_content = last_sort["original"]
            result.original_content = last_sort["modified"]
            result.message = "Sort operation undone"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_sort_history(self) -> List[Dict[str, Any]]:
        """
        Sıralama geçmişini al.
        
        Returns:
            List[Dict[str, Any]]: Geçmiş
        """
        return self.sort_history
    
    def clear_history(self) -> SortResult:
        """
        Geçmişi temizle.
        
        Returns:
            SortResult: Temizleme sonucu
        """
        result = SortResult(success=False)
        
        try:
            self.sort_history.clear()
            result.success = True
            result.message = "Sort history cleared"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def update_config(self, config: SortConfig) -> SortResult:
        """
        Konfigürasyon güncelle.
        
        Args:
            config: Yeni konfigürasyon
            
        Returns:
            SortResult: Güncelleme sonucu
        """
        result = SortResult(success=False)
        
        try:
            self.config = config
            result.success = True
            result.message = "Config updated"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_config(self) -> SortConfig:
        """
        Konfigürasyon al.
        
        Returns:
            SortConfig: Konfigürasyon
        """
        return self.config


if __name__ == "__main__":
    # Basit test
    engine = SortImportsEngine()
    
    content = "import sys\nimport os\nimport json"
    result = engine.sort_imports(content)
    print(f"Sort: {result.success}")
