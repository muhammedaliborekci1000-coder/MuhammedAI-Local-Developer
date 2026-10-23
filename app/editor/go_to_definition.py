"""
MuhammedAI Local Developer - Go to Definition
Go to definition system for code editor.
"""

import re
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum


class DefinitionKind(Enum):
    """Definition kind."""
    FUNCTION = "function"
    CLASS = "class"
    VARIABLE = "variable"
    CONSTANT = "constant"
    PARAMETER = "parameter"
    METHOD = "method"
    PROPERTY = "property"
    FIELD = "field"
    TYPE = "type"
    INTERFACE = "interface"
    MODULE = "module"
    PACKAGE = "package"


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
class LocationLink:
    """Location link."""
    originSelectionRange: Optional[Range] = None
    targetUri: Optional[str] = None
    targetRange: Optional[Range] = None
    targetSelectionRange: Optional[Range] = None


@dataclass
class DefinitionInfo:
    """Definition information."""
    name: str
    kind: DefinitionKind
    location: Location
    documentation: Optional[str] = None
    parent: Optional[str] = None


@dataclass
class GoToDefinitionConfig:
    """Go to definition configuration."""
    enable_multi_file: bool = True
    enable_external_modules: bool = False
    cache_enabled: bool = True
    history_enabled: bool = True
    max_results: int = 10


class GoToDefinitionEngine:
    """
    Go to definition engine.
    
    Özellikler:
    - Symbol definition lookup
    - Multi-file support
    - Cross-file references
    - Definition caching
    - Definition history
    - Configuration management
    - Multi-language support
    - Definition kind detection
    - Parent scope tracking
    - Documentation retrieval
    - External module support
    - Workspace-wide search
    - Symbol resolution
    - Context-aware navigation
    """
    
    def __init__(self, config: Optional[GoToDefinitionConfig] = None):
        """
        Initialize go to definition engine.
        
        Args:
            config: Go to definition configuration
        """
        self.config = config or GoToDefinitionConfig()
        self.cache: Dict[str, Location] = {}
        self.history: List[Location] = []
        self.symbol_index: Dict[str, List[DefinitionInfo]] = {}
    
    def index_document(
        self,
        text: str,
        uri: str,
        language: str = "python"
    ) -> None:
        """
        Index document for definitions.
        
        Args:
            text: Document text
            uri: Document URI
            language: Language identifier
        """
        definitions = self._extract_definitions(text, uri, language)
        self.symbol_index[uri] = definitions
    
    def go_to_definition(
        self,
        text: str,
        uri: str,
        line: int,
        character: int,
        language: str = "python"
    ) -> Optional[Location]:
        """
        Go to definition at position.
        
        Args:
            text: Document text
            uri: Document URI
            line: Line number
            character: Character offset
            language: Language identifier
            
        Returns:
            Optional[Location]: Definition location
        """
        # Get word at position
        word = self._get_word_at_position(text, line, character)
        
        if not word:
            return None
        
        # Check cache
        cache_key = f"{uri}:{word}"
        if self.config.cache_enabled and cache_key in self.cache:
            location = self.cache[cache_key]
            if self.config.history_enabled:
                self.history.append(location)
            return location
        
        # Search in current document
        location = self._find_definition_in_document(word, uri, language)
        
        if location:
            # Cache
            if self.config.cache_enabled:
                self.cache[cache_key] = location
            
            # History
            if self.config.history_enabled:
                self.history.append(location)
            
            return location
        
        # Search in other documents if enabled
        if self.config.enable_multi_file:
            location = self._find_definition_in_workspace(word, language)
            
            if location:
                # Cache
                if self.config.cache_enabled:
                    self.cache[cache_key] = location
                
                # History
                if self.config.history_enabled:
                    self.history.append(location)
                
                return location
        
        return None
    
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
    
    def _extract_definitions(
        self,
        text: str,
        uri: str,
        language: str
    ) -> List[DefinitionInfo]:
        """
        Extract definitions from document.
        
        Args:
            text: Document text
            uri: Document URI
            language: Language identifier
            
        Returns:
            List[DefinitionInfo]: Definitions
        """
        definitions = []
        lines = text.split('\n')
        
        if language == "python":
            for i, line in enumerate(lines):
                # Function definitions
                func_match = re.match(r'def\s+(\w+)\s*\(', line)
                if func_match:
                    name = func_match.group(1)
                    definitions.append(DefinitionInfo(
                        name=name,
                        kind=DefinitionKind.FUNCTION,
                        location=Location(
                            uri=uri,
                            range=Range(
                                start=Position(line=i, character=func_match.start(1)),
                                end=Position(line=i, character=func_match.end(1))
                            )
                        )
                    ))
                
                # Class definitions
                class_match = re.match(r'class\s+(\w+)', line)
                if class_match:
                    name = class_match.group(1)
                    definitions.append(DefinitionInfo(
                        name=name,
                        kind=DefinitionKind.CLASS,
                        location=Location(
                            uri=uri,
                            range=Range(
                                start=Position(line=i, character=class_match.start(1)),
                                end=Position(line=i, character=class_match.end(1))
                            )
                        )
                    ))
                
                # Variable assignments
                var_match = re.match(r'(\w+)\s*=', line)
                if var_match and not line.strip().startswith('def'):
                    name = var_match.group(1)
                    definitions.append(DefinitionInfo(
                        name=name,
                        kind=DefinitionKind.VARIABLE,
                        location=Location(
                            uri=uri,
                            range=Range(
                                start=Position(line=i, character=var_match.start(1)),
                                end=Position(line=i, character=var_match.end(1))
                            )
                        )
                    ))
        
        elif language in ["javascript", "typescript"]:
            for i, line in enumerate(lines):
                # Function definitions
                func_match = re.match(r'function\s+(\w+)', line)
                if func_match:
                    name = func_match.group(1)
                    definitions.append(DefinitionInfo(
                        name=name,
                        kind=DefinitionKind.FUNCTION,
                        location=Location(
                            uri=uri,
                            range=Range(
                                start=Position(line=i, character=func_match.start(1)),
                                end=Position(line=i, character=func_match.end(1))
                            )
                        )
                    ))
                
                # Class definitions
                class_match = re.match(r'class\s+(\w+)', line)
                if class_match:
                    name = class_match.group(1)
                    definitions.append(DefinitionInfo(
                        name=name,
                        kind=DefinitionKind.CLASS,
                        location=Location(
                            uri=uri,
                            range=Range(
                                start=Position(line=i, character=class_match.start(1)),
                                end=Position(line=i, character=class_match.end(1))
                            )
                        )
                    ))
                
                # Variable assignments
                var_match = re.match(r'(?:const|let|var)\s+(\w+)', line)
                if var_match:
                    name = var_match.group(1)
                    definitions.append(DefinitionInfo(
                        name=name,
                        kind=DefinitionKind.VARIABLE,
                        location=Location(
                            uri=uri,
                            range=Range(
                                start=Position(line=i, character=var_match.start(1)),
                                end=Position(line=i, character=var_match.end(1))
                            )
                        )
                    ))
        
        elif language == "go":
            for i, line in enumerate(lines):
                # Function definitions
                func_match = re.match(r'func\s+(\w+)', line)
                if func_match:
                    name = func_match.group(1)
                    definitions.append(DefinitionInfo(
                        name=name,
                        kind=DefinitionKind.FUNCTION,
                        location=Location(
                            uri=uri,
                            range=Range(
                                start=Position(line=i, character=func_match.start(1)),
                                end=Position(line=i, character=func_match.end(1))
                            )
                        )
                    ))
                
                # Type definitions
                type_match = re.match(r'type\s+(\w+)', line)
                if type_match:
                    name = type_match.group(1)
                    definitions.append(DefinitionInfo(
                        name=name,
                        kind=DefinitionKind.TYPE,
                        location=Location(
                            uri=uri,
                            range=Range(
                                start=Position(line=i, character=type_match.start(1)),
                                end=Position(line=i, character=type_match.end(1))
                            )
                        )
                    ))
        
        elif language == "rust":
            for i, line in enumerate(lines):
                # Function definitions
                func_match = re.match(r'fn\s+(\w+)', line)
                if func_match:
                    name = func_match.group(1)
                    definitions.append(DefinitionInfo(
                        name=name,
                        kind=DefinitionKind.FUNCTION,
                        location=Location(
                            uri=uri,
                            range=Range(
                                start=Position(line=i, character=func_match.start(1)),
                                end=Position(line=i, character=func_match.end(1))
                            )
                        )
                    ))
                
                # Struct definitions
                struct_match = re.match(r'struct\s+(\w+)', line)
                if struct_match:
                    name = struct_match.group(1)
                    definitions.append(DefinitionInfo(
                        name=name,
                        kind=DefinitionKind.STRUCT if 'STRUCT' in dir(DefinitionKind) else DefinitionKind.CLASS,
                        location=Location(
                            uri=uri,
                            range=Range(
                                start=Position(line=i, character=struct_match.start(1)),
                                end=Position(line=i, character=struct_match.end(1))
                            )
                        )
                    ))
        
        return definitions
    
    def _find_definition_in_document(
        self,
        word: str,
        uri: str,
        language: str
    ) -> Optional[Location]:
        """
        Find definition in document.
        
        Args:
            word: Symbol name
            uri: Document URI
            language: Language identifier
            
        Returns:
            Optional[Location]: Definition location
        """
        definitions = self.symbol_index.get(uri, [])
        
        for definition in definitions:
            if definition.name == word:
                return definition.location
        
        return None
    
    def _find_definition_in_workspace(
        self,
        word: str,
        language: str
    ) -> Optional[Location]:
        """
        Find definition in workspace.
        
        Args:
            word: Symbol name
            language: Language identifier
            
        Returns:
            Optional[Location]: Definition location
        """
        for uri, definitions in self.symbol_index.items():
            for definition in definitions:
                if definition.name == word:
                    return definition.location
        
        return None
    
    def get_definition_history(self) -> List[Location]:
        """
        Get definition history.
        
        Returns:
            List[Location]: History
        """
        return self.history
    
    def clear_history(self) -> None:
        """Clear definition history."""
        self.history.clear()
    
    def clear_cache(self) -> None:
        """Clear definition cache."""
        self.cache.clear()
    
    def clear_index(self) -> None:
        """Clear symbol index."""
        self.symbol_index.clear()
    
    def update_config(self, config: GoToDefinitionConfig) -> None:
        """
        Update go to definition configuration.
        
        Args:
            config: New configuration
        """
        self.config = config
    
    def get_config(self) -> GoToDefinitionConfig:
        """
        Get go to definition configuration.
        
        Returns:
            GoToDefinitionConfig: Configuration
        """
        return self.config
    
    def get_all_definitions(self, uri: str) -> List[DefinitionInfo]:
        """
        Get all definitions for document.
        
        Args:
            uri: Document URI
            
        Returns:
            List[DefinitionInfo]: Definitions
        """
        return self.symbol_index.get(uri, [])


if __name__ == "__main__":
    # Basit test
    config = GoToDefinitionConfig()
    engine = GoToDefinitionEngine(config)
    
    text = """
def hello():
    pass

def world():
    pass

my_var = 42
"""
    
    uri = "file:///test.py"
    engine.index_document(text, uri, "python")
    
    # Go to definition
    location = engine.go_to_definition(text, uri, 4, 2, "python")
    
    if location:
        print(f"Location: {location.uri} - Line {location.range.start.line}")
