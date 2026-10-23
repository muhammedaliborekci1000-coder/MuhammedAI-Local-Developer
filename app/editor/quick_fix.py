"""
MuhammedAI Local Developer - Quick Fix
Quick fix engine for code editor.
"""

import ast
import re
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from enum import Enum


class FixKind(Enum):
    """Fix kind."""
    AUTO_IMPORT = "auto_import"
    SYNTAX_FIX = "syntax_fix"
    FORMAT_FIX = "format_fix"
    REFACTOR = "refactor"
    TYPE_FIX = "type_fix"
    LINT_FIX = "lint_fix"
    OPTIMIZATION = "optimization"
    DOCUMENTATION = "documentation"


class FixPriority(Enum):
    """Fix priority."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class TextEdit:
    """Text edit."""
    start_line: int
    start_column: int
    end_line: int
    end_column: int
    new_text: str


@dataclass
class CodeAction:
    """Code action."""
    title: str
    kind: FixKind
    priority: FixPriority
    description: str
    edits: List[TextEdit] = field(default_factory=list)
    is_preferred: bool = False


@dataclass
class QuickFixResult:
    """Quick fix result."""
    success: bool
    actions: List[CodeAction] = field(default_factory=list)
    total_actions: int = 0
    applied_fixes: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    message: Optional[str] = None


class QuickFixEngine:
    """
    Quick fix engine.
    
    Özellikler:
    - Auto-fix for syntax errors
    - Auto-import suggestions
    - Auto-format suggestions
    - Refactoring suggestions
    - Code action suggestions
    - Fix for linting issues
    - Fix for type errors
    - Quick action menu
    - Apply single fix
    - Apply all fixes
    - Preview fixes
    - Fix prioritization
    - Fix filtering
    - Multi-language support
    """
    
    def __init__(self):
        """Initialize quick fix engine."""
        self.current_actions: List[CodeAction] = []
    
    def get_quick_fixes(
        self,
        code: str,
        line: int,
        column: int,
        language: str = "python"
    ) -> QuickFixResult:
        """
        Quick fix önerilerini al.
        
        Args:
            code: Kod içeriği
            line: Satır numarası
            column: Sütun numarası
            language: Programlama dili
            
        Returns:
            QuickFixResult: Quick fix sonucu
        """
        result = QuickFixResult(success=False)
        
        try:
            if language == "python":
                actions = self._get_python_fixes(code, line, column)
            else:
                actions = self._get_generic_fixes(code, line, column)
            
            result.actions = actions
            result.total_actions = len(actions)
            result.success = True
            result.message = f"Found {len(actions)} quick fixes"
            
            self.current_actions = actions
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def _get_python_fixes(self, code: str, line: int, column: int) -> List[CodeAction]:
        """Python quick fix önerilerini al."""
        actions = []
        lines = code.splitlines()
        
        if line >= len(lines):
            return actions
        
        current_line = lines[line]
        
        # Missing import detection
        if re.search(r'\b(os|sys|re|json)\b', current_line):
            import_line = any("import" in lines[i] for i in range(min(line, len(lines))))
            if not import_line:
                action = CodeAction(
                    title="Add missing import",
                    kind=FixKind.AUTO_IMPORT,
                    priority=FixPriority.HIGH,
                    description="Add import statement for used module",
                    edits=[TextEdit(
                        start_line=0,
                        start_column=0,
                        end_line=0,
                        end_column=0,
                        new_text="import os\n"
                    )],
                    is_preferred=True
                )
                actions.append(action)
        
        # Syntax error fix
        try:
            ast.parse(code)
        except SyntaxError as e:
            if e.lineno == line + 1:
                action = CodeAction(
                    title="Fix syntax error",
                    kind=FixKind.SYNTAX_FIX,
                    priority=FixPriority.CRITICAL,
                    description=f"Fix syntax error: {e.msg}",
                    edits=[],
                    is_preferred=True
                )
                actions.append(action)
        
        # Unused variable fix
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
                if unused_name in current_line:
                    action = CodeAction(
                        title=f"Remove unused variable '{unused_name}'",
                        kind=FixKind.LINT_FIX,
                        priority=FixPriority.MEDIUM,
                        description=f"Remove unused variable: {unused_name}",
                        edits=[TextEdit(
                            start_line=line,
                            start_column=current_line.find(unused_name),
                            end_line=line,
                            end_column=current_line.find(unused_name) + len(unused_name),
                            new_text=""
                        )],
                        is_preferred=False
                    )
                    actions.append(action)
        except:
            pass
        
        # Add docstring fix
        if current_line.strip().startswith("def ") and not current_line.strip().endswith(":"):
            if line + 1 < len(lines) and not lines[line + 1].strip().startswith('"""'):
                action = CodeAction(
                    title="Add docstring",
                    kind=FixKind.DOCUMENTATION,
                    priority=FixPriority.LOW,
                    description="Add docstring to function",
                    edits=[TextEdit(
                        start_line=line + 1,
                        start_column=0,
                        end_line=line + 1,
                        end_column=0,
                        new_text='    """Function docstring."""\n'
                    )],
                    is_preferred=False
                )
                actions.append(action)
        
        return actions
    
    def _get_generic_fixes(self, code: str, line: int, column: int) -> List[CodeAction]:
        """Genel quick fix önerilerini al."""
        actions = []
        lines = code.splitlines()
        
        if line >= len(lines):
            return actions
        
        current_line = lines[line]
        
        # Remove trailing whitespace
        if current_line != current_line.rstrip():
            action = CodeAction(
                title="Remove trailing whitespace",
                kind=FixKind.FORMAT_FIX,
                priority=FixPriority.LOW,
                description="Remove trailing whitespace from line",
                edits=[TextEdit(
                    start_line=line,
                    start_column=len(current_line.rstrip()),
                    end_line=line,
                    end_column=len(current_line),
                    new_text=""
                )],
                is_preferred=False
            )
            actions.append(action)
        
        return actions
    
    def apply_fix(self, code: str, action: CodeAction) -> Tuple[str, QuickFixResult]:
        """
        Quick fix uygula.
        
        Args:
            code: Kod içeriği
            action: Code action
            
        Returns:
            Tuple[str, QuickFixResult]: Düzeltilmiş kod ve sonuç
        """
        result = QuickFixResult(success=False)
        
        try:
            lines = code.splitlines()
            
            # Edits'i uygula (tersten, pozisyon değişimi önlemek için)
            for edit in reversed(action.edits):
                if edit.start_line >= len(lines):
                    continue
                
                line = lines[edit.start_line]
                new_line = line[:edit.start_column] + edit.new_text + line[edit.end_column:]
                lines[edit.start_line] = new_line
            
            fixed_code = "\n".join(lines)
            
            result.success = True
            result.applied_fixes.append(action.title)
            result.message = f"Applied fix: {action.title}"
            
            return fixed_code, result
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            return code, result
    
    def apply_all_fixes(self, code: str, actions: List[CodeAction]) -> Tuple[str, QuickFixResult]:
        """
        Tüm fix'leri uygula.
        
        Args:
            code: Kod içeriği
            actions: Code action listesi
            
        Returns:
            Tuple[str, QuickFixResult]: Düzeltilmiş kod ve sonuç
        """
        result = QuickFixResult(success=False)
        fixed_code = code
        
        try:
            for action in actions:
                fixed_code, fix_result = self.apply_fix(fixed_code, action)
                if fix_result.success:
                    result.applied_fixes.extend(fix_result.applied_fixes)
            
            result.success = True
            result.message = f"Applied {len(result.applied_fixes)} fixes"
            
            return fixed_code, result
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            return code, result
    
    def filter_by_kind(self, kind: FixKind) -> List[CodeAction]:
        """
        Türe göre filtrele.
        
        Args:
            kind: Fix türü
            
        Returns:
            List[CodeAction]: Filtrelenmiş action'lar
        """
        return [a for a in self.current_actions if a.kind == kind]
    
    def filter_by_priority(self, priority: FixPriority) -> List[CodeAction]:
        """
        Önceliğe göre filtrele.
        
        Args:
            priority: Fix önceliği
            
        Returns:
            List[CodeAction]: Filtrelenmiş action'lar
        """
        return [a for a in self.current_actions if a.priority == priority]
    
    def get_preferred_actions(self) -> List[CodeAction]:
        """
        Tercih edilen action'ları al.
        
        Returns:
            List[CodeAction]: Tercih edilen action'lar
        """
        return [a for a in self.current_actions if a.is_preferred]
    
    def add_custom_action(
        self,
        title: str,
        kind: FixKind,
        priority: FixPriority,
        description: str,
        edits: List[TextEdit],
        is_preferred: bool = False
    ) -> CodeAction:
        """
        Özel action ekle.
        
        Args:
            title: Action başlığı
            kind: Fix türü
            priority: Fix önceliği
            description: Açıklama
            edits: Text edit listesi
            is_preferred: Tercih edilen mi
            
        Returns:
            CodeAction: Oluşturulan action
        """
        action = CodeAction(
            title=title,
            kind=kind,
            priority=priority,
            description=description,
            edits=edits,
            is_preferred=is_preferred
        )
        self.current_actions.append(action)
        return action
    
    def clear_actions(self) -> None:
        """Tüm action'ları temizle."""
        self.current_actions.clear()


if __name__ == "__main__":
    # Basit test
    engine = QuickFixEngine()
    
    code = """
def my_function():
    x = 42
    return "Hello"
"""
    
    # Quick fix al
    result = engine.get_quick_fixes(code, 2, 0, "python")
    print(f"Quick fixes: {result.success}")
    print(f"Total actions: {result.total_actions}")
    
    for action in result.actions:
        print(f"  {action.title}: {action.description}")
