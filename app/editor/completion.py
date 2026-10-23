"""
MuhammedAI Local Developer - Completion
Auto-completion system for code editor.
"""

import re
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum


class CompletionTriggerKind(Enum):
    """Completion trigger kind."""
    INVOKED = 1
    TRIGGER_CHARACTER = 2
    TRIGGER_FOR_INCOMPLETE_COMPLETIONS = 3


class CompletionItemKind(Enum):
    """Completion item kind."""
    TEXT = 1
    METHOD = 2
    FUNCTION = 3
    CONSTRUCTOR = 4
    FIELD = 5
    VARIABLE = 6
    CLASS = 7
    INTERFACE = 8
    MODULE = 9
    PROPERTY = 10
    UNIT = 11
    VALUE = 12
    ENUM = 13
    KEYWORD = 14
    SNIPPET = 15
    COLOR = 16
    FILE = 17
    REFERENCE = 18
    FOLDER = 19
    ENUM_MEMBER = 20
    CONSTANT = 21
    STRUCT = 22
    EVENT = 23
    OPERATOR = 24
    TYPE_PARAMETER = 25


class InsertTextFormat(Enum):
    """Insert text format."""
    PLAIN_TEXT = 1
    SNIPPET = 2


@dataclass
class CompletionContext:
    """Completion context."""
    trigger_kind: CompletionTriggerKind
    trigger_character: Optional[str] = None


@dataclass
class CompletionItemLabelDetails:
    """Completion item label details."""
    detail: Optional[str] = None
    description: Optional[str] = None


@dataclass
class CompletionItem:
    """Completion item."""
    label: str
    kind: Optional[CompletionItemKind] = None
    detail: Optional[str] = None
    documentation: Optional[str] = None
    sort_text: Optional[str] = None
    filter_text: Optional[str] = None
    insert_text: Optional[str] = None
    insert_text_format: Optional[InsertTextFormat] = None
    label_details: Optional[CompletionItemLabelDetails] = None
    deprecated: bool = False
    preselect: bool = False
    commit_characters: Optional[List[str]] = None
    additional_text_edits: Optional[List[Any]] = None
    score: float = 0.0


@dataclass
class CompletionList:
    """Completion list."""
    is_incomplete: bool
    items: List[CompletionItem] = field(default_factory=list)


@dataclass
class CompletionConfig:
    """Completion configuration."""
    enable_snippets: bool = True
    enable_ai_completion: bool = False
    trigger_characters: List[str] = field(default_factory=lambda: [".", "(", "[", "{", " "])
    max_results: int = 100
    fuzzy_match: bool = True
    case_sensitive: bool = False
    sort_by_relevance: bool = True
    show_documentation: bool = True
    auto_trigger: bool = True


class CompletionEngine:
    """
    Completion engine.
    
    Özellikler:
    - Auto-completion
    - Snippet support
    - Trigger characters
    - Completion item kinds
    - Completion context
    - Completion filtering
    - Completion sorting
    - Completion ranking
    - Multi-language support
    - Completion caching
    - Completion history
    - Configuration management
    - Keyword completion
    - Variable completion
    - Function completion
    - Class completion
    - Module completion
    """
    
    def __init__(self, config: Optional[CompletionConfig] = None):
        """
        Initialize completion engine.
        
        Args:
            config: Completion configuration
        """
        self.config = config or CompletionConfig()
        self.completion_history: List[CompletionItem] = []
        self.cache: Dict[str, CompletionList] = {}
        self._initialize_keywords()
    
    def _initialize_keywords(self) -> None:
        """Initialize common keywords."""
        self.keywords = {
            "python": [
                "def", "class", "if", "else", "elif", "for", "while", "try", "except",
                "finally", "with", "import", "from", "as", "return", "yield", "raise",
                "pass", "break", "continue", "and", "or", "not", "in", "is", "lambda",
                "True", "False", "None", "self", "super", "global", "nonlocal", "assert"
            ],
            "javascript": [
                "const", "let", "var", "function", "class", "if", "else", "for", "while",
                "return", "break", "continue", "switch", "case", "default", "try", "catch",
                "finally", "throw", "new", "this", "super", "extends", "import", "export",
                "async", "await", "typeof", "instanceof", "in", "of", "true", "false", "null"
            ],
            "typescript": [
                "const", "let", "var", "function", "class", "interface", "type", "enum",
                "if", "else", "for", "while", "return", "break", "continue", "switch",
                "case", "default", "try", "catch", "finally", "throw", "new", "this",
                "super", "extends", "import", "export", "async", "await", "typeof",
                "instanceof", "in", "of", "true", "false", "null", "any", "void", "never"
            ],
            "go": [
                "func", "var", "const", "type", "struct", "interface", "if", "else", "for",
                "range", "switch", "case", "default", "select", "defer", "go", "chan",
                "return", "break", "continue", "fallthrough", "goto", "package", "import"
            ],
            "rust": [
                "fn", "let", "mut", "const", "static", "struct", "enum", "impl", "trait",
                "type", "if", "else", "match", "for", "while", "loop", "break", "continue",
                "return", "use", "mod", "crate", "pub", "unsafe", "where", "move", "ref"
            ]
        }
    
    def get_completions(
        self,
        text: str,
        line: int,
        column: int,
        language: str = "python",
        context: Optional[CompletionContext] = None
    ) -> CompletionList:
        """
        Get completions for given position.
        
        Args:
            text: Document text
            line: Line number
            column: Column number
            language: Language identifier
            context: Completion context
            
        Returns:
            CompletionList: Completion list
        """
        # Get word before cursor
        word = self._get_word_before_cursor(text, line, column)
        
        if not word and not (context and context.trigger_kind == CompletionTriggerKind.TRIGGER_CHARACTER):
            return CompletionList(is_incomplete=False, items=[])
        
        items = []
        
        # Add keyword completions
        keyword_items = self._get_keyword_completions(word, language)
        items.extend(keyword_items)
        
        # Add snippet completions
        if self.config.enable_snippets:
            snippet_items = self._get_snippet_completions(word, language)
            items.extend(snippet_items)
        
        # Add variable/function completions (from text)
        local_items = self._get_local_completions(text, word, line)
        items.extend(local_items)
        
        # Filter and sort
        items = self._filter_completions(items, word)
        
        if self.config.sort_by_relevance:
            items = self._sort_completions(items, word)
        
        # Limit results
        if len(items) > self.config.max_results:
            items = items[:self.config.max_results]
        
        # Add to history
        self.completion_history.extend(items)
        
        return CompletionList(
            is_incomplete=False,
            items=items
        )
    
    def _get_word_before_cursor(self, text: str, line: int, column: int) -> str:
        """
        Get word before cursor position.
        
        Args:
            text: Document text
            line: Line number
            column: Column number
            
        Returns:
            str: Word before cursor
        """
        lines = text.split('\n')
        if line >= len(lines):
            return ""
        
        current_line = lines[line]
        if column >= len(current_line):
            return ""
        
        # Get characters before cursor
        before_cursor = current_line[:column]
        
        # Extract word
        word = ""
        for char in reversed(before_cursor):
            if char.isalnum() or char == '_':
                word = char + word
            else:
                break
        
        return word
    
    def _get_keyword_completions(self, word: str, language: str) -> List[CompletionItem]:
        """
        Get keyword completions.
        
        Args:
            word: Current word
            language: Language identifier
            
        Returns:
            List[CompletionItem]: Keyword completions
        """
        keywords = self.keywords.get(language, self.keywords.get("python", []))
        
        items = []
        for keyword in keywords:
            if self._matches_query(keyword, word):
                item = CompletionItem(
                    label=keyword,
                    kind=CompletionItemKind.KEYWORD,
                    detail="keyword",
                    insert_text=keyword,
                    score=1.0
                )
                items.append(item)
        
        return items
    
    def _get_snippet_completions(self, word: str, language: str) -> List[CompletionItem]:
        """
        Get snippet completions.
        
        Args:
            word: Current word
            language: Language identifier
            
        Returns:
            List[CompletionItem]: Snippet completions
        """
        snippets = self._get_snippets_for_language(language)
        
        items = []
        for snippet in snippets:
            if self._matches_query(snippet["label"], word):
                item = CompletionItem(
                    label=snippet["label"],
                    kind=CompletionItemKind.SNIPPET,
                    detail=snippet.get("detail"),
                    documentation=snippet.get("documentation"),
                    insert_text=snippet["insert_text"],
                    insert_text_format=InsertTextFormat.SNIPPET,
                    score=0.9
                )
                items.append(item)
        
        return items
    
    def _get_snippets_for_language(self, language: str) -> List[Dict[str, Any]]:
        """
        Get snippets for language.
        
        Args:
            language: Language identifier
            
        Returns:
            List[Dict[str, Any]]: Snippets
        """
        if language == "python":
            return [
                {
                    "label": "def",
                    "detail": "function",
                    "documentation": "Define a function",
                    "insert_text": "def ${1:function_name}(${2:args}):\n    ${3:pass}"
                },
                {
                    "label": "class",
                    "detail": "class",
                    "documentation": "Define a class",
                    "insert_text": "class ${1:ClassName}:\n    def __init__(self):\n        ${2:pass}"
                },
                {
                    "label": "if",
                    "detail": "if statement",
                    "documentation": "If statement",
                    "insert_text": "if ${1:condition}:\n    ${2:pass}"
                },
                {
                    "label": "for",
                    "detail": "for loop",
                    "documentation": "For loop",
                    "insert_text": "for ${1:item} in ${2:iterable}:\n    ${3:pass}"
                }
            ]
        elif language in ["javascript", "typescript"]:
            return [
                {
                    "label": "function",
                    "detail": "function",
                    "documentation": "Define a function",
                    "insert_text": "function ${1:functionName}(${2:args}) {\n    ${3:// body}\n}"
                },
                {
                    "label": "class",
                    "detail": "class",
                    "documentation": "Define a class",
                    "insert_text": "class ${1:ClassName} {\n    constructor() {\n        ${2:// body}\n    }\n}"
                },
                {
                    "label": "if",
                    "detail": "if statement",
                    "documentation": "If statement",
                    "insert_text": "if (${1:condition}) {\n    ${2:// body}\n}"
                },
                {
                    "label": "for",
                    "detail": "for loop",
                    "documentation": "For loop",
                    "insert_text": "for (let ${1:item} of ${2:iterable}) {\n    ${3:// body}\n}"
                }
            ]
        elif language == "go":
            return [
                {
                    "label": "func",
                    "detail": "function",
                    "documentation": "Define a function",
                    "insert_text": "func ${1:functionName}(${2:args}) ${3:returnType} {\n    ${4:// body}\n}"
                },
                {
                    "label": "if",
                    "detail": "if statement",
                    "documentation": "If statement",
                    "insert_text": "if ${1:condition} {\n    ${2:// body}\n}"
                },
                {
                    "label": "for",
                    "detail": "for loop",
                    "documentation": "For loop",
                    "insert_text": "for ${1:index}, ${2:item} := range ${3:iterable} {\n    ${4:// body}\n}"
                }
            ]
        elif language == "rust":
            return [
                {
                    "label": "fn",
                    "detail": "function",
                    "documentation": "Define a function",
                    "insert_text": "fn ${1:function_name}(${2:args}) -> ${3:return_type} {\n    ${4:// body}\n}"
                },
                {
                    "label": "if",
                    "detail": "if statement",
                    "documentation": "If statement",
                    "insert_text": "if ${1:condition} {\n    ${2:// body}\n}"
                },
                {
                    "label": "for",
                    "detail": "for loop",
                    "documentation": "For loop",
                    "insert_text": "for ${1:item} in ${2:iterable} {\n    ${3:// body}\n}"
                }
            ]
        
        return []
    
    def _get_local_completions(self, text: str, word: str, current_line: int) -> List[CompletionItem]:
        """
        Get local variable/function completions.
        
        Args:
            text: Document text
            word: Current word
            current_line: Current line number
            
        Returns:
            List[CompletionItem]: Local completions
        """
        items = []
        lines = text.split('\n')
        
        # Simple regex to find variable/function definitions
        for i, line in enumerate(lines):
            if i >= current_line:
                break
            
            # Find function definitions
            func_match = re.match(r'def\s+(\w+)', line)
            if func_match and self._matches_query(func_match.group(1), word):
                items.append(CompletionItem(
                    label=func_match.group(1),
                    kind=CompletionItemKind.FUNCTION,
                    detail="function",
                    insert_text=func_match.group(1),
                    score=0.8
                ))
            
            # Find variable assignments
            var_match = re.match(r'(\w+)\s*=', line)
            if var_match and self._matches_query(var_match.group(1), word):
                items.append(CompletionItem(
                    label=var_match.group(1),
                    kind=CompletionItemKind.VARIABLE,
                    detail="variable",
                    insert_text=var_match.group(1),
                    score=0.7
                ))
        
        return items
    
    def _matches_query(self, text: str, query: str) -> bool:
        """
        Check if text matches query.
        
        Args:
            text: Text to check
            query: Query string
            
        Returns:
            bool: Match status
        """
        if not query:
            return True
        
        if self.config.fuzzy_match:
            return query.lower() in text.lower()
        elif self.config.case_sensitive:
            return query in text
        else:
            return query.lower() in text.lower()
    
    def _filter_completions(self, items: List[CompletionItem], query: str) -> List[CompletionItem]:
        """
        Filter completions by query.
        
        Args:
            items: Completion items
            query: Query string
            
        Returns:
            List[CompletionItem]: Filtered items
        """
        if not query:
            return items
        
        return [item for item in items if self._matches_query(item.label, query)]
    
    def _sort_completions(self, items: List[CompletionItem], query: str) -> List[CompletionItem]:
        """
        Sort completions by relevance.
        
        Args:
            items: Completion items
            query: Query string
            
        Returns:
            List[CompletionItem]: Sorted items
        """
        def sort_key(item: CompletionItem) -> tuple:
            # Primary sort by score
            score = -item.score
            
            # Secondary sort by prefix match
            prefix_match = item.label.lower().startswith(query.lower()) if query else False
            
            # Tertiary sort by label
            label = item.label.lower()
            
            return (score, not prefix_match, label)
        
        return sorted(items, key=sort_key)
    
    def get_completion_history(self) -> List[CompletionItem]:
        """
        Get completion history.
        
        Returns:
            List[CompletionItem]: History
        """
        return self.completion_history
    
    def clear_history(self) -> None:
        """Clear completion history."""
        self.completion_history.clear()
    
    def clear_cache(self) -> None:
        """Clear completion cache."""
        self.cache.clear()
    
    def update_config(self, config: CompletionConfig) -> None:
        """
        Update completion configuration.
        
        Args:
            config: New configuration
        """
        self.config = config
    
    def get_config(self) -> CompletionConfig:
        """
        Get completion configuration.
        
        Returns:
            CompletionConfig: Configuration
        """
        return self.config


if __name__ == "__main__":
    # Basit test
    config = CompletionConfig()
    engine = CompletionEngine(config)
    
    text = """
def hello():
    pass

def world():
    pass

my_var = 42
"""
    
    # Get completions
    completions = engine.get_completions(text, 5, 2, "python")
    
    print(f"Completions: {len(completions.items)}")
    for item in completions.items:
        print(f"  - {item.label} ({item.kind.value if item.kind else 'N/A'})")
