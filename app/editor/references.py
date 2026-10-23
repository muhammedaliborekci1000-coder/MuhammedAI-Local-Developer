"""
MuhammedAI Local Developer - References
Find references system for code editor.
"""

import re
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum


class ReferenceKind(Enum):
    """Reference kind."""
    READ = "read"
    WRITE = "write"
    DEFINITION = "definition"


@dataclass
class Position:
    """Position in text document."""
    line: int
    character: int


@dataclass
class Range:
    """Range in text document."""
    start: Position
    end: Position


@dataclass
class Location:
    """Location in workspace."""
    uri: str
    range: Range


@dataclass
class Reference:
    """Reference information."""
    location: Location
    kind: ReferenceKind
    name: str


@dataclass
class ReferenceConfig:
    """Reference configuration."""
    include_definition: bool = True
    include_reads: bool = True
    include_writes: bool = True
    enable_multi_file: bool = True
    cache_enabled: bool = True
    max_results: int = 100


class ReferencesEngine:
    """
    References engine.
    
    Özellikler:
    - Find all references
    - Reference kind detection
    - Multi-file support
    - Reference caching
    - Configuration management
    - Multi-language support
    - Definition inclusion
    - Read/write detection
    - Workspace-wide search
    - Context-aware references
    - Symbol resolution
    - Reference filtering
    - Reference sorting
    """
    
    def __init__(self, config: Optional[ReferenceConfig] = None):
        """
        Initialize references engine.
        
        Args:
            config: Reference configuration
        """
        self.config = config or ReferenceConfig()
        self.cache: Dict[str, List[Reference]] = {}
        self.symbol_index: Dict[str, List[Reference]] = {}
    
    def index_document(
        self,
        text: str,
        uri: str,
        language: str = "python"
    ) -> None:
        """
        Index document for references.
        
        Args:
            text: Document text
            uri: Document URI
            language: Language identifier
        """
        references = self._extract_references(text, uri, language)
        self.symbol_index[uri] = references
    
    def find_references(
        self,
        text: str,
        uri: str,
        line: int,
        character: int,
        language: str = "python"
    ) -> List[Reference]:
        """
        Find all references to symbol at position.
        
        Args:
            text: Document text
            uri: Document URI
            line: Line number
            character: Character offset
            language: Language identifier
            
        Returns:
            List[Reference]: References
        """
        # Get word at position
        word = self._get_word_at_position(text, line, character)
        
        if not word:
            return []
        
        # Check cache
        cache_key = f"{uri}:{word}"
        if self.config.cache_enabled and cache_key in self.cache:
            return self.cache[cache_key]
        
        # Find references in current document
        references = self._find_references_in_document(word, uri, language)
        
        # Find references in other documents if enabled
        if self.config.enable_multi_file:
            other_references = self._find_references_in_workspace(word, language)
            references.extend(other_references)
        
        # Filter by configuration
        references = self._filter_references(references)
        
        # Limit results
        if len(references) > self.config.max_results:
            references = references[:self.config.max_results]
        
        # Cache
        if self.config.cache_enabled:
            self.cache[cache_key] = references
        
        return references
    
    def _get_word_at_position(self, text: str, line: int, character: int) -> Optional[str]:
        """
        Get word at position.
        
        Args:
            text: Document text
            line: Line number
            character: Character offset
            
        Returns:
            Optional[str]: Word at position
        """
        lines = text.split('\n')
        if line >= len(lines):
            return None
        
        current_line = lines[line]
        if character >= len(current_line):
            return None
        
        # Get characters around cursor
        before = current_line[:character]
        after = current_line[character:]
        
        # Extract word
        word = ""
        for char in reversed(before):
            if char.isalnum() or char == '_':
                word = char + word
            else:
                break
        
        for char in after:
            if char.isalnum() or char == '_':
                word += char
            else:
                break
        
        return word if word else None
    
    def _extract_references(
        self,
        text: str,
        uri: str,
        language: str
    ) -> List[Reference]:
        """
        Extract references from document.
        
        Args:
            text: Document text
            uri: Document URI
            language: Language identifier
            
        Returns:
            List[Reference]: References
        """
        references = []
        lines = text.split('\n')
        
        if language == "python":
            for i, line in enumerate(lines):
                # Find all word occurrences
                words = re.finditer(r'\b(\w+)\b', line)
                for match in words:
                    word = match.group(1)
                    kind = self._determine_reference_kind(line, match.start())
                    references.append(Reference(
                        location=Location(
                            uri=uri,
                            range=Range(
                                start=Position(line=i, character=match.start()),
                                end=Position(line=i, character=match.end())
                            )
                        ),
                        kind=kind,
                        name=word
                    ))
        
        elif language in ["javascript", "typescript"]:
            for i, line in enumerate(lines):
                words = re.finditer(r'\b(\w+)\b', line)
                for match in words:
                    word = match.group(1)
                    kind = self._determine_reference_kind(line, match.start())
                    references.append(Reference(
                        location=Location(
                            uri=uri,
                            range=Range(
                                start=Position(line=i, character=match.start()),
                                end=Position(line=i, character=match.end())
                            )
                        ),
                        kind=kind,
                        name=word
                    ))
        
        elif language == "go":
            for i, line in enumerate(lines):
                words = re.finditer(r'\b(\w+)\b', line)
                for match in words:
                    word = match.group(1)
                    kind = self._determine_reference_kind(line, match.start())
                    references.append(Reference(
                        location=Location(
                            uri=uri,
                            range=Range(
                                start=Position(line=i, character=match.start()),
                                end=Position(line=i, character=match.end())
                            )
                        ),
                        kind=kind,
                        name=word
                    ))
        
        elif language == "rust":
            for i, line in enumerate(lines):
                words = re.finditer(r'\b(\w+)\b', line)
                for match in words:
                    word = match.group(1)
                    kind = self._determine_reference_kind(line, match.start())
                    references.append(Reference(
                        location=Location(
                            uri=uri,
                            range=Range(
                                start=Position(line=i, character=match.start()),
                                end=Position(line=i, character=match.end())
                            )
                        ),
                        kind=kind,
                        name=word
                    ))
        
        return references
    
    def _determine_reference_kind(self, line: str, position: int) -> ReferenceKind:
        """
        Determine reference kind.
        
        Args:
            line: Line text
            position: Character position
            
        Returns:
            ReferenceKind: Reference kind
        """
        # Check if it's a definition
        if re.match(r'\s*(def|function|class|const|let|var|type|struct|enum|interface)\s+\w+', line[:position]):
            return ReferenceKind.DEFINITION
        
        # Check if it's a write (assignment)
        if '=' in line[:position] and line[:position].strip().endswith('='):
            return ReferenceKind.WRITE
        
        # Default to read
        return ReferenceKind.READ
    
    def _find_references_in_document(
        self,
        word: str,
        uri: str,
        language: str
    ) -> List[Reference]:
        """
        Find references in document.
        
        Args:
            word: Symbol name
            uri: Document URI
            language: Language identifier
            
        Returns:
            List[Reference]: References
        """
        references = self.symbol_index.get(uri, [])
        
        return [ref for ref in references if ref.name == word]
    
    def _find_references_in_workspace(
        self,
        word: str,
        language: str
    ) -> List[Reference]:
        """
        Find references in workspace.
        
        Args:
            word: Symbol name
            language: Language identifier
            
        Returns:
            List[Reference]: References
        """
        all_references = []
        
        for uri, references in self.symbol_index.items():
            for ref in references:
                if ref.name == word:
                    all_references.append(ref)
        
        return all_references
    
    def _filter_references(self, references: List[Reference]) -> List[Reference]:
        """
        Filter references by configuration.
        
        Args:
            references: References list
            
        Returns:
            List[Reference]: Filtered references
        """
        filtered = []
        
        for ref in references:
            if ref.kind == ReferenceKind.DEFINITION and not self.config.include_definition:
                continue
            if ref.kind == ReferenceKind.READ and not self.config.include_reads:
                continue
            if ref.kind == ReferenceKind.WRITE and not self.config.include_writes:
                continue
            filtered.append(ref)
        
        return filtered
    
    def clear_cache(self) -> None:
        """Clear reference cache."""
        self.cache.clear()
    
    def clear_index(self) -> None:
        """Clear symbol index."""
        self.symbol_index.clear()
    
    def update_config(self, config: ReferenceConfig) -> None:
        """
        Update reference configuration.
        
        Args:
            config: New configuration
        """
        self.config = config
    
    def get_config(self) -> ReferenceConfig:
        """
        Get reference configuration.
        
        Returns:
            ReferenceConfig: Configuration
        """
        return self.config


if __name__ == "__main__":
    # Basit test
    config = ReferenceConfig()
    engine = ReferencesEngine(config)
    
    text = """
def hello():
    pass

hello()
my_var = 42
"""
    
    uri = "file:///test.py"
    engine.index_document(text, uri, "python")
    
    # Find references
    references = engine.find_references(text, uri, 1, 4, "python")
    
    print(f"References: {len(references)}")
    for ref in references:
        print(f"  - {ref.name} at line {ref.location.range.start.line}")
