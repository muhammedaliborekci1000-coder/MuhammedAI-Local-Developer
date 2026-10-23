"""
MuhammedAI Local Developer - Code Folding
Code folding engine for code editor.
"""

import re
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from enum import Enum


class FoldType(Enum):
    """Fold type."""
    FUNCTION = "function"
    CLASS = "class"
    BLOCK = "block"
    COMMENT = "comment"
    REGION = "region"
    IMPORT = "import"
    IF_STATEMENT = "if_statement"
    LOOP = "loop"
    TRY_EXCEPT = "try_except"
    WITH_STATEMENT = "with_statement"


class FoldState(Enum):
    """Fold state."""
    EXPANDED = "expanded"
    COLLAPSED = "collapsed"


@dataclass
class FoldRegion:
    """Fold region."""
    start_line: int
    end_line: int
    fold_type: FoldType
    state: FoldState = FoldState.EXPANDED
    name: str = ""
    level: int = 0
    is_collapsible: bool = True


@dataclass
class FoldResult:
    """Fold result."""
    success: bool
    folded_code: Optional[str] = None
    fold_regions: List[FoldRegion] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    message: Optional[str] = None


class CodeFoldingEngine:
    """
    Code folding engine.
    
    Özellikler:
    - Fold region detection
    - Fold/unfold operations
    - Nested folding
    - Language-specific folding
    - Auto-fold on load
    - Fold markers
    - Fold levels
    - Fold all/unfold all
    - Fold at cursor
    - Persist fold state
    - Comment folding
    - Import folding
    - Block folding
    """
    
    def __init__(self):
        """Initialize code folding engine."""
        self.fold_regions: List[FoldRegion] = []
        self.language_rules = self._init_language_rules()
    
    def _init_language_rules(self) -> Dict[str, Dict[str, Any]]:
        """Initialize language-specific folding rules."""
        return {
            "python": {
                "function_pattern": r"def\s+\w+.*:",
                "class_pattern": r"class\s+\w+.*:",
                "if_pattern": r"if\s+.*:",
                "elif_pattern": r"elif\s+.*:",
                "else_pattern": r"else:",
                "for_pattern": r"for\s+.*:",
                "while_pattern": r"while\s+.*:",
                "try_pattern": r"try:",
                "except_pattern": r"except.*:",
                "finally_pattern": r"finally:",
                "with_pattern": r"with\s+.*:",
                "comment_start": '"""',
                "comment_end": '"""',
                "import_pattern": r"^(import|from)\s+"
            },
            "javascript": {
                "function_pattern": r"function\s+\w+.*\{",
                "class_pattern": r"class\s+\w+.*\{",
                "if_pattern": r"if\s*\(.*\)\s*\{",
                "else_pattern": r"else\s*\{",
                "for_pattern": r"for\s*\(.*\)\s*\{",
                "while_pattern": r"while\s*\(.*\)\s*\{",
                "try_pattern": r"try\s*\{",
                "catch_pattern": r"catch\s*\(.*\)\s*\{",
                "finally_pattern": r"finally\s*\{",
                "comment_start": "/*",
                "comment_end": "*/",
                "import_pattern": r"^(import|const|let|var)\s+"
            },
            "typescript": {
                "function_pattern": r"function\s+\w+.*\{",
                "class_pattern": r"class\s+\w+.*\{",
                "if_pattern": r"if\s*\(.*\)\s*\{",
                "else_pattern": r"else\s*\{",
                "for_pattern": r"for\s*\(.*\)\s*\{",
                "while_pattern": r"while\s*\(.*\)\s*\{",
                "try_pattern": r"try\s*\{",
                "catch_pattern": r"catch\s*\(.*\)\s*\{",
                "finally_pattern": r"finally\s*\{",
                "comment_start": "/*",
                "comment_end": "*/",
                "import_pattern": r"^(import|const|let|var)\s+"
            },
            "java": {
                "function_pattern": r"(public|private|protected)?\s*(static)?\s*\w+\s+\w+\s*\(.*\)\s*\{",
                "class_pattern": r"(public|private|protected)?\s*class\s+\w+.*\{",
                "if_pattern": r"if\s*\(.*\)\s*\{",
                "else_pattern": r"else\s*\{",
                "for_pattern": r"for\s*\(.*\)\s*\{",
                "while_pattern": r"while\s*\(.*\)\s*\{",
                "try_pattern": r"try\s*\{",
                "catch_pattern": r"catch\s*\(.*\)\s*\{",
                "finally_pattern": r"finally\s*\{",
                "comment_start": "/*",
                "comment_end": "*/",
                "import_pattern": r"^import\s+"
            },
            "c": {
                "function_pattern": r"\w+\s+\w+\s*\(.*\)\s*\{",
                "if_pattern": r"if\s*\(.*\)\s*\{",
                "else_pattern": r"else\s*\{",
                "for_pattern": r"for\s*\(.*\)\s*\{",
                "while_pattern": r"while\s*\(.*\)\s*\{",
                "try_pattern": r"",
                "catch_pattern": r"",
                "finally_pattern": r"",
                "comment_start": "/*",
                "comment_end": "*/",
                "import_pattern": r"^#include"
            },
            "cpp": {
                "function_pattern": r"\w+\s+\w+\s*\(.*\)\s*\{",
                "class_pattern": r"class\s+\w+.*\{",
                "if_pattern": r"if\s*\(.*\)\s*\{",
                "else_pattern": r"else\s*\{",
                "for_pattern": r"for\s*\(.*\)\s*\{",
                "while_pattern": r"while\s*\(.*\)\s*\{",
                "try_pattern": r"try\s*\{",
                "catch_pattern": r"catch\s*\(.*\)\s*\{",
                "finally_pattern": r"",
                "comment_start": "/*",
                "comment_end": "*/",
                "import_pattern": r"^#include"
            },
            "csharp": {
                "function_pattern": r"(public|private|protected|internal)?\s*(static)?\s*\w+\s+\w+\s*\(.*\)\s*\{",
                "class_pattern": r"(public|private|protected|internal)?\s*class\s+\w+.*\{",
                "if_pattern": r"if\s*\(.*\)\s*\{",
                "else_pattern": r"else\s*\{",
                "for_pattern": r"for\s*\(.*\)\s*\{",
                "while_pattern": r"while\s*\(.*\)\s*\{",
                "try_pattern": r"try\s*\{",
                "catch_pattern": r"catch\s*\(.*\)\s*\{",
                "finally_pattern": r"finally\s*\{",
                "comment_start": "/*",
                "comment_end": "*/",
                "import_pattern": r"^using\s+"
            },
            "go": {
                "function_pattern": r"func\s+\w+.*\{",
                "if_pattern": r"if\s+.*\{",
                "else_pattern": r"else\s*\{",
                "for_pattern": r"for\s+.*\{",
                "while_pattern": r"",
                "try_pattern": r"",
                "catch_pattern": r"",
                "finally_pattern": r"",
                "comment_start": "/*",
                "comment_end": "*/",
                "import_pattern": r"^import\s+"
            },
            "rust": {
                "function_pattern": r"fn\s+\w+.*\{",
                "if_pattern": r"if\s+.*\{",
                "else_pattern": r"else\s*\{",
                "for_pattern": r"for\s+.*\{",
                "while_pattern": r"while\s+.*\{",
                "try_pattern": r"",
                "catch_pattern": r"",
                "finally_pattern": r"",
                "comment_start": "/*",
                "comment_end": "*/",
                "import_pattern": r"^use\s+"
            },
            "ruby": {
                "function_pattern": r"def\s+\w+.*",
                "class_pattern": r"class\s+\w+.*",
                "if_pattern": r"if\s+.*",
                "else_pattern": r"else",
                "for_pattern": r"for\s+.*",
                "while_pattern": r"while\s+.*",
                "try_pattern": r"begin",
                "catch_pattern": r"rescue",
                "finally_pattern": r"ensure",
                "comment_start": "=begin",
                "comment_end": "=end",
                "import_pattern": r"^require\s+"
            },
            "php": {
                "function_pattern": r"function\s+\w+.*\{",
                "class_pattern": r"class\s+\w+.*\{",
                "if_pattern": r"if\s*\(.*\)\s*\{",
                "else_pattern": r"else\s*\{",
                "for_pattern": r"for\s*\(.*\)\s*\{",
                "while_pattern": r"while\s*\(.*\)\s*\{",
                "try_pattern": r"try\s*\{",
                "catch_pattern": r"catch\s*\(.*\)\s*\{",
                "finally_pattern": r"finally\s*\{",
                "comment_start": "/*",
                "comment_end": "*/",
                "import_pattern": r"^(require|include)"
            },
            "html": {
                "function_pattern": r"",
                "class_pattern": r"",
                "if_pattern": r"",
                "else_pattern": r"",
                "for_pattern": r"",
                "while_pattern": r"",
                "try_pattern": r"",
                "catch_pattern": r"",
                "finally_pattern": r"",
                "comment_start": "<!--",
                "comment_end": "-->",
                "import_pattern": r""
            },
            "css": {
                "function_pattern": r"",
                "class_pattern": r"",
                "if_pattern": r"",
                "else_pattern": r"",
                "for_pattern": r"",
                "while_pattern": r"",
                "try_pattern": r"",
                "catch_pattern": r"",
                "finally_pattern": r"",
                "comment_start": "/*",
                "comment_end": "*/",
                "import_pattern": r"^@import"
            },
            "sql": {
                "function_pattern": r"",
                "class_pattern": r"",
                "if_pattern": r"",
                "else_pattern": r"",
                "for_pattern": r"",
                "while_pattern": r"",
                "try_pattern": r"",
                "catch_pattern": r"",
                "finally_pattern": r"",
                "comment_start": "/*",
                "comment_end": "*/",
                "import_pattern": r""
            },
            "json": {
                "function_pattern": r"",
                "class_pattern": r"",
                "if_pattern": r"",
                "else_pattern": r"",
                "for_pattern": r"",
                "while_pattern": r"",
                "try_pattern": r"",
                "catch_pattern": r"",
                "finally_pattern": r"",
                "comment_start": "",
                "comment_end": "",
                "import_pattern": r""
            },
            "xml": {
                "function_pattern": r"",
                "class_pattern": r"",
                "if_pattern": r"",
                "else_pattern": r"",
                "for_pattern": r"",
                "while_pattern": r"",
                "try_pattern": r"",
                "catch_pattern": r"",
                "finally_pattern": r"",
                "comment_start": "<!--",
                "comment_end": "-->",
                "import_pattern": r""
            },
            "yaml": {
                "function_pattern": r"",
                "class_pattern": r"",
                "if_pattern": r"",
                "else_pattern": r"",
                "for_pattern": r"",
                "while_pattern": r"",
                "try_pattern": r"",
                "catch_pattern": r"",
                "finally_pattern": r"",
                "comment_start": "#",
                "comment_end": "",
                "import_pattern": r""
            },
            "markdown": {
                "function_pattern": r"",
                "class_pattern": r"",
                "if_pattern": r"",
                "else_pattern": r"",
                "for_pattern": r"",
                "while_pattern": r"",
                "try_pattern": r"",
                "catch_pattern": r"",
                "finally_pattern": r"",
                "comment_start": "<!--",
                "comment_end": "-->",
                "import_pattern": r""
            }
        }
    
    def detect_fold_regions(
        self,
        code: str,
        language: str = "python"
    ) -> FoldResult:
        """
        Fold region'ları tespit et.
        
        Args:
            code: Kod içeriği
            language: Programlama dili
            
        Returns:
            FoldResult: Tespit sonucu
        """
        result = FoldResult(success=False)
        
        try:
            rules = self.language_rules.get(language.lower(), {})
            if not rules:
                result.errors.append(f"Unsupported language: {language}")
                return result
            
            lines = code.splitlines()
            fold_regions = []
            stack = []
            
            for i, line in enumerate(lines):
                stripped = line.strip()
                
                # Function detection
                if "function_pattern" in rules and rules["function_pattern"]:
                    match = re.search(rules["function_pattern"], stripped)
                    if match:
                        region = FoldRegion(
                            start_line=i,
                            end_line=i,
                            fold_type=FoldType.FUNCTION,
                            name=stripped[:50],
                            level=len(stack)
                        )
                        stack.append(region)
                
                # Class detection
                if "class_pattern" in rules and rules["class_pattern"]:
                    match = re.search(rules["class_pattern"], stripped)
                    if match:
                        region = FoldRegion(
                            start_line=i,
                            end_line=i,
                            fold_type=FoldType.CLASS,
                            name=stripped[:50],
                            level=len(stack)
                        )
                        stack.append(region)
                
                # If statement detection
                if "if_pattern" in rules and rules["if_pattern"]:
                    match = re.search(rules["if_pattern"], stripped)
                    if match:
                        region = FoldRegion(
                            start_line=i,
                            end_line=i,
                            fold_type=FoldType.IF_STATEMENT,
                            name=stripped[:50],
                            level=len(stack)
                        )
                        stack.append(region)
                
                # Loop detection
                if "for_pattern" in rules and rules["for_pattern"]:
                    match = re.search(rules["for_pattern"], stripped)
                    if match:
                        region = FoldRegion(
                            start_line=i,
                            end_line=i,
                            fold_type=FoldType.LOOP,
                            name=stripped[:50],
                            level=len(stack)
                        )
                        stack.append(region)
                
                # Try-except detection
                if "try_pattern" in rules and rules["try_pattern"]:
                    match = re.search(rules["try_pattern"], stripped)
                    if match:
                        region = FoldRegion(
                            start_line=i,
                            end_line=i,
                            fold_type=FoldType.TRY_EXCEPT,
                            name=stripped[:50],
                            level=len(stack)
                        )
                        stack.append(region)
                
                # With statement detection (Python)
                if "with_pattern" in rules and rules["with_pattern"]:
                    match = re.search(rules["with_pattern"], stripped)
                    if match:
                        region = FoldRegion(
                            start_line=i,
                            end_line=i,
                            fold_type=FoldType.WITH_STATEMENT,
                            name=stripped[:50],
                            level=len(stack)
                        )
                        stack.append(region)
                
                # Comment detection
                if "comment_start" in rules and rules["comment_start"]:
                    if stripped.startswith(rules["comment_start"]):
                        region = FoldRegion(
                            start_line=i,
                            end_line=i,
                            fold_type=FoldType.COMMENT,
                            name=stripped[:50],
                            level=len(stack)
                        )
                        stack.append(region)
                
                # Import detection
                if "import_pattern" in rules and rules["import_pattern"]:
                    match = re.search(rules["import_pattern"], stripped)
                    if match:
                        region = FoldRegion(
                            start_line=i,
                            end_line=i,
                            fold_type=FoldType.IMPORT,
                            name=stripped[:50],
                            level=len(stack)
                        )
                        stack.append(region)
                
                # End detection (simplified)
                if stripped.endswith(":") or stripped.endswith("{"):
                    if stack:
                        stack[-1].end_line = i
            
            # Close remaining regions
            for region in stack:
                if region.end_line == region.start_line:
                    region.end_line = min(region.start_line + 5, len(lines) - 1)
                fold_regions.append(region)
            
            self.fold_regions = fold_regions
            result.success = True
            result.fold_regions = fold_regions
            result.message = f"Detected {len(fold_regions)} fold regions"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def fold_region(
        self,
        line: int,
        code: str,
        language: str = "python"
    ) -> FoldResult:
        """
        Belirli bir region'ı fold et.
        
        Args:
            line: Satır numarası
            code: Kod içeriği
            language: Programlama dili
            
        Returns:
            FoldResult: Fold sonucu
        """
        result = FoldResult(success=False)
        
        try:
            # Region'ları tespit et
            detect_result = self.detect_fold_regions(code, language)
            if not detect_result.success:
                return detect_result
            
            # İlgili region'ı bul
            region = None
            for r in detect_result.fold_regions:
                if r.start_line <= line <= r.end_line:
                    region = r
                    break
            
            if not region:
                result.errors.append("No fold region found at line")
                return result
            
            # Fold et
            region.state = FoldState.COLLAPSED
            lines = code.splitlines()
            
            # Fold placeholder ekle
            placeholder = f"... {region.name} ..."
            lines[region.start_line + 1] = placeholder
            
            folded_code = "\n".join(lines)
            
            result.success = True
            result.folded_code = folded_code
            result.fold_regions = detect_result.fold_regions
            result.message = f"Folded region at line {line}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def unfold_region(
        self,
        line: int,
        code: str,
        language: str = "python"
    ) -> FoldResult:
        """
        Belirli bir region'ı unfold et.
        
        Args:
            line: Satır numarası
            code: Kod içeriği
            language: Programlama dili
            
        Returns:
            FoldResult: Unfold sonucu
        """
        result = FoldResult(success=False)
        
        try:
            # Region'ları tespit et
            detect_result = self.detect_fold_regions(code, language)
            if not detect_result.success:
                return detect_result
            
            # İlgili region'ı bul
            region = None
            for r in detect_result.fold_regions:
                if r.start_line <= line <= r.end_line:
                    region = r
                    break
            
            if not region:
                result.errors.append("No fold region found at line")
                return result
            
            # Unfold et
            region.state = FoldState.EXPANDED
            result.success = True
            result.fold_regions = detect_result.fold_regions
            result.message = f"Unfolded region at line {line}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def fold_all(
        self,
        code: str,
        language: str = "python"
    ) -> FoldResult:
        """
        Tüm region'ları fold et.
        
        Args:
            code: Kod içeriği
            language: Programlama dili
            
        Returns:
            FoldResult: Fold sonucu
        """
        result = FoldResult(success=False)
        
        try:
            detect_result = self.detect_fold_regions(code, language)
            if not detect_result.success:
                return detect_result
            
            for region in detect_result.fold_regions:
                region.state = FoldState.COLLAPSED
            
            result.success = True
            result.fold_regions = detect_result.fold_regions
            result.message = f"Folded all {len(detect_result.fold_regions)} regions"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def unfold_all(
        self,
        code: str,
        language: str = "python"
    ) -> FoldResult:
        """
        Tüm region'ları unfold et.
        
        Args:
            code: Kod içeriği
            language: Programlama dili
            
        Returns:
            FoldResult: Unfold sonucu
        """
        result = FoldResult(success=False)
        
        try:
            detect_result = self.detect_fold_regions(code, language)
            if not detect_result.success:
                return detect_result
            
            for region in detect_result.fold_regions:
                region.state = FoldState.EXPANDED
            
            result.success = True
            result.fold_regions = detect_result.fold_regions
            result.message = f"Unfolded all {len(detect_result.fold_regions)} regions"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_fold_regions(
        self,
        code: str,
        language: str = "python"
    ) -> FoldResult:
        """
        Fold region'ları al.
        
        Args:
            code: Kod içeriği
            language: Programlama dili
            
        Returns:
            FoldResult: Region listesi
        """
        return self.detect_fold_regions(code, language)
    
    def get_fold_level(
        self,
        line: int,
        code: str,
        language: str = "python"
    ) -> int:
        """
        Satırın fold level'ını al.
        
        Args:
            line: Satır numarası
            code: Kod içeriği
            language: Programlama dili
            
        Returns:
            int: Fold level
        """
        detect_result = self.detect_fold_regions(code, language)
        if not detect_result.success:
            return 0
        
        for region in detect_result.fold_regions:
            if region.start_line <= line <= region.end_line:
                return region.level
        
        return 0
    
    def toggle_fold(
        self,
        line: int,
        code: str,
        language: str = "python"
    ) -> FoldResult:
        """
        Fold/unfold toggle.
        
        Args:
            line: Satır numarası
            code: Kod içeriği
            language: Programlama dili
            
        Returns:
            FoldResult: Toggle sonucu
        """
        detect_result = self.detect_fold_regions(code, language)
        if not detect_result.success:
            return detect_result
        
        for region in detect_result.fold_regions:
            if region.start_line <= line <= region.end_line:
                if region.state == FoldState.EXPANDED:
                    return self.fold_region(line, code, language)
                else:
                    return self.unfold_region(line, code, language)
        
        result = FoldResult(success=False)
        result.errors.append("No fold region found at line")
        return result


if __name__ == "__main__":
    # Basit test
    engine = CodeFoldingEngine()
    
    code = """def my_function():
    x = 10
    y = 20
    return x + y

class MyClass:
    def __init__(self):
        self.value = 0
"""
    
    result = engine.detect_fold_regions(code, language="python")
    print(f"Detected regions: {len(result.fold_regions)}")
    
    for region in result.fold_regions:
        print(f"  {region.fold_type.value}: {region.start_line}-{region.end_line}")
