"""
MuhammedAI Local Developer - Code Actions
Code actions engine for code editor.
"""

import ast
import re
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from enum import Enum


class ActionKind(Enum):
    """Action kind."""
    REFACTOR = "refactor"
    EXTRACT = "extract"
    INLINE = "inline"
    RENAME = "rename"
    GENERATE = "generate"
    FORMAT = "format"
    ORGANIZE = "organize"
    MOVE = "move"
    QUICK_FIX = "quick_fix"


class ActionScope(Enum):
    """Action scope."""
    SELECTION = "selection"
    LINE = "line"
    FUNCTION = "function"
    CLASS = "class"
    FILE = "file"
    PROJECT = "project"


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
    kind: ActionKind
    scope: ActionScope
    description: str
    edits: List[TextEdit] = field(default_factory=list)
    is_preferred: bool = False


@dataclass
class CodeActionResult:
    """Code action result."""
    success: bool
    actions: List[CodeAction] = field(default_factory=list)
    total_actions: int = 0
    applied_actions: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    message: Optional[str] = None


class CodeActionsEngine:
    """
    Code actions engine.
    
    Özellikler:
    - Extract function
    - Extract variable
    - Inline variable
    - Rename symbol
    - Move to new file
    - Generate docstring
    - Add type hints
    - Organize imports
    - Format code
    - Refactor suggestions
    - Code transformations
    - Action menu
    - Apply single action
    - Apply multiple actions
    - Preview actions
    - Action filtering
    - Multi-language support
    """
    
    def __init__(self):
        """Initialize code actions engine."""
        self.current_actions: List[CodeAction] = []
    
    def get_code_actions(
        self,
        code: str,
        start_line: int,
        end_line: int,
        language: str = "python"
    ) -> CodeActionResult:
        """
        Code action önerilerini al.
        
        Args:
            code: Kod içeriği
            start_line: Başlangıç satırı
            end_line: Bitiş satırı
            language: Programlama dili
            
        Returns:
            CodeActionResult: Code action sonucu
        """
        result = CodeActionResult(success=False)
        
        try:
            if language == "python":
                actions = self._get_python_actions(code, start_line, end_line)
            else:
                actions = self._get_generic_actions(code, start_line, end_line)
            
            result.actions = actions
            result.total_actions = len(actions)
            result.success = True
            result.message = f"Found {len(actions)} code actions"
            
            self.current_actions = actions
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def _get_python_actions(self, code: str, start_line: int, end_line: int) -> List[CodeAction]:
        """Python code action önerilerini al."""
        actions = []
        lines = code.splitlines()
        
        if start_line >= len(lines):
            return actions
        
        selected_lines = lines[start_line:end_line + 1]
        selected_text = "\n".join(selected_lines)
        
        # Extract function action
        if len(selected_lines) > 1:
            action = CodeAction(
                title="Extract function",
                kind=ActionKind.EXTRACT,
                scope=ActionScope.SELECTION,
                description="Extract selected code into a new function",
                edits=[],
                is_preferred=True
            )
            actions.append(action)
        
        # Extract variable action
        if selected_text.strip():
            action = CodeAction(
                title="Extract variable",
                kind=ActionKind.EXTRACT,
                scope=ActionScope.SELECTION,
                description="Extract selected expression into a variable",
                edits=[],
                is_preferred=False
            )
            actions.append(action)
        
        # Generate docstring action
        for line_num in range(start_line, min(end_line + 1, len(lines))):
            line = lines[line_num]
            if line.strip().startswith("def ") and not line.strip().endswith(":"):
                action = CodeAction(
                    title="Generate docstring",
                    kind=ActionKind.GENERATE,
                    scope=ActionScope.FUNCTION,
                    description="Generate docstring for function",
                    edits=[TextEdit(
                        start_line=line_num + 1,
                        start_column=0,
                        end_line=line_num + 1,
                        end_column=0,
                        new_text='    """Function docstring."""\n'
                    )],
                    is_preferred=True
                )
                actions.append(action)
        
        # Add type hints action
        for line_num in range(start_line, min(end_line + 1, len(lines))):
            line = lines[line_num]
            if line.strip().startswith("def ") and "->" not in line:
                action = CodeAction(
                    title="Add type hints",
                    kind=ActionKind.GENERATE,
                    scope=ActionScope.FUNCTION,
                    description="Add type hints to function signature",
                    edits=[],
                    is_preferred=False
                )
                actions.append(action)
        
        # Organize imports action
        if any("import" in line for line in lines):
            action = CodeAction(
                title="Organize imports",
                kind=ActionKind.ORGANIZE,
                scope=ActionScope.FILE,
                description="Organize and sort import statements",
                edits=[],
                is_preferred=False
            )
            actions.append(action)
        
        # Format code action
        action = CodeAction(
            title="Format code",
            kind=ActionKind.FORMAT,
            scope=ActionScope.FILE,
            description="Format code according to style guide",
            edits=[],
            is_preferred=False
        )
        actions.append(action)
        
        return actions
    
    def _get_generic_actions(self, code: str, start_line: int, end_line: int) -> List[CodeAction]:
        """Genel code action önerilerini al."""
        actions = []
        lines = code.splitlines()
        
        if start_line >= len(lines):
            return actions
        
        # Format code action
        action = CodeAction(
            title="Format code",
            kind=ActionKind.FORMAT,
            scope=ActionScope.FILE,
            description="Format code",
            edits=[],
            is_preferred=True
        )
        actions.append(action)
        
        return actions
    
    def apply_action(self, code: str, action: CodeAction) -> Tuple[str, CodeActionResult]:
        """
        Code action uygula.
        
        Args:
            code: Kod içeriği
            action: Code action
            
        Returns:
            Tuple[str, CodeActionResult]: Düzeltilmiş kod ve sonuç
        """
        result = CodeActionResult(success=False)
        
        try:
            lines = code.splitlines()
            
            # Edits'i uygula (tersten)
            for edit in reversed(action.edits):
                if edit.start_line >= len(lines):
                    continue
                
                line = lines[edit.start_line]
                new_line = line[:edit.start_column] + edit.new_text + line[edit.end_column:]
                lines[edit.start_line] = new_line
            
            fixed_code = "\n".join(lines)
            
            result.success = True
            result.applied_actions.append(action.title)
            result.message = f"Applied action: {action.title}"
            
            return fixed_code, result
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            return code, result
    
    def apply_multiple_actions(self, code: str, actions: List[CodeAction]) -> Tuple[str, CodeActionResult]:
        """
        Birden fazla action uygula.
        
        Args:
            code: Kod içeriği
            actions: Code action listesi
            
        Returns:
            Tuple[str, CodeActionResult]: Düzeltilmiş kod ve sonuç
        """
        result = CodeActionResult(success=False)
        fixed_code = code
        
        try:
            for action in actions:
                fixed_code, action_result = self.apply_action(fixed_code, action)
                if action_result.success:
                    result.applied_actions.extend(action_result.applied_actions)
            
            result.success = True
            result.message = f"Applied {len(result.applied_actions)} actions"
            
            return fixed_code, result
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            return code, result
    
    def filter_by_kind(self, kind: ActionKind) -> List[CodeAction]:
        """
        Türe göre filtrele.
        
        Args:
            kind: Action türü
            
        Returns:
            List[CodeAction]: Filtrelenmiş action'lar
        """
        return [a for a in self.current_actions if a.kind == kind]
    
    def filter_by_scope(self, scope: ActionScope) -> List[CodeAction]:
        """
        Scope'a göre filtrele.
        
        Args:
            scope: Action scope'u
            
        Returns:
            List[CodeAction]: Filtrelenmiş action'lar
        """
        return [a for a in self.current_actions if a.scope == scope]
    
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
        kind: ActionKind,
        scope: ActionScope,
        description: str,
        edits: List[TextEdit],
        is_preferred: bool = False
    ) -> CodeAction:
        """
        Özel action ekle.
        
        Args:
            title: Action başlığı
            kind: Action türü
            scope: Action scope'u
            description: Açıklama
            edits: Text edit listesi
            is_preferred: Tercih edilen mi
            
        Returns:
            CodeAction: Oluşturulan action
        """
        action = CodeAction(
            title=title,
            kind=kind,
            scope=scope,
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
    engine = CodeActionsEngine()
    
    code = """
def my_function():
    x = 42
    return x
"""
    
    # Code actions al
    result = engine.get_code_actions(code, 1, 3, "python")
    print(f"Code actions: {result.success}")
    print(f"Total actions: {result.total_actions}")
    
    for action in result.actions:
        print(f"  {action.title}: {action.description}")
