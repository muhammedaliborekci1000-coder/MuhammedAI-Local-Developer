"""
MuhammedAI Local Developer - Snippets
Snippets engine for code editor.
"""

import re
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from enum import Enum


class SnippetScope(Enum):
    """Snippet scope."""
    GLOBAL = "global"
    LANGUAGE = "language"
    PROJECT = "project"
    USER = "user"


class SnippetVariable(Enum):
    """Snippet variable."""
    TM_FILENAME = "TM_FILENAME"
    TM_FILENAME_BASE = "TM_FILENAME_BASE"
    TM_DIRECTORY = "TM_DIRECTORY"
    TM_FILEPATH = "TM_FILEPATH"
    TM_LINE_NUMBER = "TM_LINE_NUMBER"
    TM_SELECTED_TEXT = "TM_SELECTED_TEXT"
    TM_CURRENT_LINE = "TM_CURRENT_LINE"
    CURRENT_YEAR = "CURRENT_YEAR"
    CURRENT_MONTH = "CURRENT_MONTH"
    CURRENT_DATE = "CURRENT_DATE"
    CURRENT_HOUR = "CURRENT_HOUR"
    CURRENT_MINUTE = "CURRENT_MINUTE"
    CURRENT_SECOND = "CURRENT_SECOND"


@dataclass
class SnippetPlaceholder:
    """Snippet placeholder."""
    index: int
    name: str = ""
    default_value: str = ""
    is_tab_stop: bool = True


@dataclass
class Snippet:
    """Snippet definition."""
    name: str
    prefix: str
    description: str = ""
    body: str = ""
    scope: SnippetScope = SnippetScope.GLOBAL
    language: str = ""
    placeholders: List[SnippetPlaceholder] = field(default_factory=list)
    variables: Dict[str, str] = field(default_factory=list)
    is_builtin: bool = False


@dataclass
class SnippetInsertion:
    """Snippet insertion result."""
    success: bool
    inserted_code: Optional[str] = None
    cursor_position: Tuple[int, int] = (0, 0)
    placeholders: List[SnippetPlaceholder] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    message: Optional[str] = None


@dataclass
class SnippetSearchResult:
    """Snippet search result."""
    snippets: List[Snippet] = field(default_factory=list)
    total_count: int = 0
    query: str = ""


class SnippetsEngine:
    """
    Snippets engine.
    
    Özellikler:
    - Snippet insertion
    - Snippet templates
    - Placeholder handling
    - Tab stops
    - Variables
    - Language-specific snippets
    - Snippet search
    - Snippet management
    - Custom snippets
    - Builtin snippets
    - Snippet preview
    - Snippet validation
    """
    
    def __init__(self):
        """Initialize snippets engine."""
        self.snippets: Dict[str, List[Snippet]] = {}
        self._init_builtin_snippets()
    
    def _init_builtin_snippets(self):
        """Initialize builtin snippets."""
        # Python snippets
        python_snippets = [
            Snippet(
                name="def",
                prefix="def",
                description="Function definition",
                body="def ${1:function_name}(${2:args}):\n    ${3:pass}",
                scope=SnippetScope.LANGUAGE,
                language="python",
                is_builtin=True
            ),
            Snippet(
                name="class",
                prefix="class",
                description="Class definition",
                body="class ${1:ClassName}:\n    def __init__(self):\n        ${2:pass}",
                scope=SnippetScope.LANGUAGE,
                language="python",
                is_builtin=True
            ),
            Snippet(
                name="if",
                prefix="if",
                description="If statement",
                body="if ${1:condition}:\n    ${2:pass}",
                scope=SnippetScope.LANGUAGE,
                language="python",
                is_builtin=True
            ),
            Snippet(
                name="for",
                prefix="for",
                description="For loop",
                body="for ${1:item} in ${2:iterable}:\n    ${3:pass}",
                scope=SnippetScope.LANGUAGE,
                language="python",
                is_builtin=True
            ),
            Snippet(
                name="while",
                prefix="while",
                description="While loop",
                body="while ${1:condition}:\n    ${2:pass}",
                scope=SnippetScope.LANGUAGE,
                language="python",
                is_builtin=True
            ),
            Snippet(
                name="try",
                prefix="try",
                description="Try-except block",
                body="try):\n    ${1:pass}\nexcept ${2:Exception} as e:\n    ${3:pass}",
                scope=SnippetScope.LANGUAGE,
                language="python",
                is_builtin=True
            ),
            Snippet(
                name="with",
                prefix="with",
                description="With statement",
                body="with ${1:context} as ${2:variable}:\n    ${3:pass}",
                scope=SnippetScope.LANGUAGE,
                language="python",
                is_builtin=True
            ),
            Snippet(
                name="lambda",
                prefix="lambda",
                description="Lambda function",
                body="lambda ${1:args}: ${2:expression}",
                scope=SnippetScope.LANGUAGE,
                language="python",
                is_builtin=True
            )
        ]
        
        # JavaScript snippets
        js_snippets = [
            Snippet(
                name="function",
                prefix="function",
                description="Function declaration",
                body="function ${1:functionName}(${2:args}) {\n    ${3:// body}\n}",
                scope=SnippetScope.LANGUAGE,
                language="javascript",
                is_builtin=True
            ),
            Snippet(
                name="const",
                prefix="const",
                description="Const declaration",
                body="const ${1:name} = ${2:value};",
                scope=SnippetScope.LANGUAGE,
                language="javascript",
                is_builtin=True
            ),
            Snippet(
                name="let",
                prefix="let",
                description="Let declaration",
                body="let ${1:name} = ${2:value};",
                scope=SnippetScope.LANGUAGE,
                language="javascript",
                is_builtin=True
            ),
            Snippet(
                name="arrow",
                prefix="arrow",
                description="Arrow function",
                body="const ${1:name} = (${2:args}) => {\n    ${3:// body}\n};",
                scope=SnippetScope.LANGUAGE,
                language="javascript",
                is_builtin=True
            ),
            Snippet(
                name="if",
                prefix="if",
                description="If statement",
                body="if (${1:condition}) {\n    ${2:// body}\n}",
                scope=SnippetScope.LANGUAGE,
                language="javascript",
                is_builtin=True
            ),
            Snippet(
                name="for",
                prefix="for",
                description="For loop",
                body="for (let ${1:i} = 0; ${1:i} < ${2:array}.length; ${1:i}++) {\n    ${3:// body}\n}",
                scope=SnippetScope.LANGUAGE,
                language="javascript",
                is_builtin=True
            ),
            Snippet(
                name="try",
                prefix="try",
                description="Try-catch block",
                body="try {\n    ${1:// body}\n} catch (${2:error}) {\n    ${3:// handle error}\n}",
                scope=SnippetScope.LANGUAGE,
                language="javascript",
                is_builtin=True
            ),
            Snippet(
                name="console.log",
                prefix="log",
                description="Console log",
                body="console.log(${1:value});",
                scope=SnippetScope.LANGUAGE,
                language="javascript",
                is_builtin=True
            )
        ]
        
        # HTML snippets
        html_snippets = [
            Snippet(
                name="div",
                prefix="div",
                description="Div element",
                body="<div class=\"${1:class}\">\n    ${2:content}\n</div>",
                scope=SnippetScope.LANGUAGE,
                language="html",
                is_builtin=True
            ),
            Snippet(
                name="p",
                prefix="p",
                description="Paragraph",
                body="<p>${1:text}</p>",
                scope=SnippetScope.LANGUAGE,
                language="html",
                is_builtin=True
            ),
            Snippet(
                name="a",
                prefix="a",
                description="Anchor link",
                body="<a href=\"${1:url}\">${2:text}</a>",
                scope=SnippetScope.LANGUAGE,
                language="html",
                is_builtin=True
            ),
            Snippet(
                name="img",
                prefix="img",
                description="Image",
                body="<img src=\"${1:src}\" alt=\"${2:alt}\" />",
                scope=SnippetScope.LANGUAGE,
                language="html",
                is_builtin=True
            ),
            Snippet(
                name="ul",
                prefix="ul",
                description="Unordered list",
                body="<ul>\n    <li>${1:item}</li>\n</ul>",
                scope=SnippetScope.LANGUAGE,
                language="html",
                is_builtin=True
            ),
            Snippet(
                name="ol",
                prefix="ol",
                description="Ordered list",
                body="<ol>\n    <li>${1:item}</li>\n</ol>",
                scope=SnippetScope.LANGUAGE,
                language="html",
                is_builtin=True
            ),
            Snippet(
                name="table",
                prefix="table",
                description="Table",
                body="<table>\n    <tr>\n        <th>${1:header}</th>\n    </tr>\n    <tr>\n        <td>${2:cell}</td>\n    </tr>\n</table>",
                scope=SnippetScope.LANGUAGE,
                language="html",
                is_builtin=True
            )
        ]
        
        # CSS snippets
        css_snippets = [
            Snippet(
                name="margin",
                prefix="margin",
                description="Margin shorthand",
                body="margin: ${1:0} ${2:auto};",
                scope=SnippetScope.LANGUAGE,
                language="css",
                is_builtin=True
            ),
            Snippet(
                name="padding",
                prefix="padding",
                description="Padding shorthand",
                body="padding: ${1:0} ${2:auto};",
                scope=SnippetScope.LANGUAGE,
                language="css",
                is_builtin=True
            ),
            Snippet(
                name="border",
                prefix="border",
                description="Border shorthand",
                body="border: ${1:1px} solid ${2:black};",
                scope=SnippetScope.LANGUAGE,
                language="css",
                is_builtin=True
            ),
            Snippet(
                name="background",
                prefix="bg",
                description="Background shorthand",
                body="background: ${1:#fff} ${2:url()};",
                scope=SnippetScope.LANGUAGE,
                language="css",
                is_builtin=True
            ),
            Snippet(
                name="flex",
                prefix="flex",
                description="Flex display",
                body="display: flex;\njustify-content: ${1:center};\nalign-items: ${2:center};",
                scope=SnippetScope.LANGUAGE,
                language="css",
                is_builtin=True
            ),
            Snippet(
                name="grid",
                prefix="grid",
                description="Grid display",
                body="display: grid;\ngrid-template-columns: ${1:repeat(auto-fit, minmax(200px, 1fr))};",
                scope=SnippetScope.LANGUAGE,
                language="css",
                is_builtin=True
            )
        ]
        
        # Register snippets
        self.snippets["python"] = python_snippets
        self.snippets["javascript"] = js_snippets
        self.snippets["typescript"] = js_snippets
        self.snippets["html"] = html_snippets
        self.snippets["css"] = css_snippets
        self.snippets["global"] = []
    
    def insert_snippet(
        self,
        prefix: str,
        language: str = "python",
        variables: Optional[Dict[str, str]] = None
    ) -> SnippetInsertion:
        """
        Snippet ekle.
        
        Args:
            prefix: Snippet prefix
            language: Programlama dili
            variables: Değişken değerleri
            
        Returns:
            SnippetInsertion: Insertion sonucu
        """
        result = SnippetInsertion(success=False)
        
        try:
            # Snippet bul
            snippet = self._find_snippet(prefix, language)
            if not snippet:
                result.errors.append(f"Snippet not found: {prefix}")
                return result
            
            # Placeholder'ları parse et
            placeholders = self._parse_placeholders(snippet.body)
            snippet.placeholders = placeholders
            
            # Değişkenleri değiştir
            body = self._replace_variables(snippet.body, variables)
            
            # Placeholder'ları değiştir
            body = self._replace_placeholders(body, placeholders)
            
            result.inserted_code = body
            result.placeholders = placeholders
            result.success = True
            result.message = f"Snippet '{prefix}' inserted"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def _find_snippet(self, prefix: str, language: str) -> Optional[Snippet]:
        """Snippet bul."""
        # Language-specific snippets
        if language in self.snippets:
            for snippet in self.snippets[language]:
                if snippet.prefix == prefix:
                    return snippet
        
        # Global snippets
        if "global" in self.snippets:
            for snippet in self.snippets["global"]:
                if snippet.prefix == prefix:
                    return snippet
        
        return None
    
    def _parse_placeholders(self, body: str) -> List[SnippetPlaceholder]:
        """Placeholder'ları parse et."""
        placeholders = []
        pattern = r'\$\{(\d+)(?::([^}]+))?\}'
        matches = re.finditer(pattern, body)
        
        for match in matches:
            index = int(match.group(1))
            default = match.group(2) or ""
            placeholder = SnippetPlaceholder(
                index=index,
                default_value=default,
                is_tab_stop=True
            )
            placeholders.append(placeholder)
        
        return placeholders
    
    def _replace_variables(self, body: str, variables: Optional[Dict[str, str]]) -> str:
        """Değişkenleri değiştir."""
        if not variables:
            return body
        
        for var_name, var_value in variables.items():
            pattern = r'\$\{' + re.escape(var_name) + r'\}'
            body = re.sub(pattern, var_value, body)
        
        return body
    
    def _replace_placeholders(self, body: str, placeholders: List[SnippetPlaceholder]) -> str:
        """Placeholder'ları değiştir."""
        for placeholder in placeholders:
            pattern = r'\$\{' + str(placeholder.index) + r'(?::[^}]+)?\}'
            body = re.sub(pattern, placeholder.default_value, body)
        
        return body
    
    def search_snippets(
        self,
        query: str,
        language: str = "python"
    ) -> SnippetSearchResult:
        """
        Snippet ara.
        
        Args:
            query: Arama sorgusu
            language: Programlama dili
            
        Returns:
            SnippetSearchResult: Arama sonucu
        """
        result = SnippetSearchResult(query=query)
        
        try:
            matching_snippets = []
            
            # Language-specific snippets
            if language in self.snippets:
                for snippet in self.snippets[language]:
                    if (query.lower() in snippet.prefix.lower() or
                        query.lower() in snippet.name.lower() or
                        query.lower() in snippet.description.lower()):
                        matching_snippets.append(snippet)
            
            # Global snippets
            if "global" in self.snippets:
                for snippet in self.snippets["global"]:
                    if (query.lower() in snippet.prefix.lower() or
                        query.lower() in snippet.name.lower() or
                        query.lower() in snippet.description.lower()):
                        matching_snippets.append(snippet)
            
            result.snippets = matching_snippets
            result.total_count = len(matching_snippets)
        
        except Exception as e:
            pass
        
        return result
    
    def add_snippet(self, snippet: Snippet) -> bool:
        """
        Snippet ekle.
        
        Args:
            snippet: Snippet
            
        Returns:
            bool: Başarı durumu
        """
        try:
            language = snippet.language or "global"
            if language not in self.snippets:
                self.snippets[language] = []
            
            self.snippets[language].append(snippet)
            return True
        except Exception:
            return False
    
    def remove_snippet(self, prefix: str, language: str = "python") -> bool:
        """
        Snippet kaldır.
        
        Args:
            prefix: Snippet prefix
            language: Programlama dili
            
        Returns:
            bool: Başarı durumu
        """
        try:
            if language in self.snippets:
                self.snippets[language] = [
                    s for s in self.snippets[language]
                    if s.prefix != prefix or s.is_builtin
                ]
                return True
            return False
        except Exception:
            return False
    
    def get_snippets(self, language: str = "python") -> List[Snippet]:
        """
        Dil için snippet'ları al.
        
        Args:
            language: Programlama dili
            
        Returns:
            List[Snippet]: Snippet listesi
        """
        return self.snippets.get(language, [])
    
    def get_snippet(self, prefix: str, language: str = "python") -> Optional[Snippet]:
        """
        Snippet al.
        
        Args:
            prefix: Snippet prefix
            language: Programlama dili
            
        Returns:
            Optional[Snippet]: Snippet
        """
        return self._find_snippet(prefix, language)
    
    def preview_snippet(self, prefix: str, language: str = "python") -> Optional[str]:
        """
        Snippet önizleme.
        
        Args:
            prefix: Snippet prefix
            language: Programlama dili
            
        Returns:
            Optional[str]: Önizleme
        """
        snippet = self._find_snippet(prefix, language)
        if snippet:
            return snippet.body
        return None
    
    def validate_snippet(self, snippet: Snippet) -> Tuple[bool, List[str]]:
        """
        Snippet doğrula.
        
        Args:
            snippet: Snippet
            
        Returns:
            Tuple[bool, List[str]]: (valid, errors)
        """
        errors = []
        
        if not snippet.name:
            errors.append("Snippet name is required")
        
        if not snippet.prefix:
            errors.append("Snippet prefix is required")
        
        if not snippet.body:
            errors.append("Snippet body is required")
        
        # Placeholder syntax kontrolü
        placeholders = self._parse_placeholders(snippet.body)
        indices = [p.index for p in placeholders]
        if len(indices) != len(set(indices)):
            errors.append("Duplicate placeholder indices")
        
        return (len(errors) == 0, errors)
    
    def get_supported_languages(self) -> List[str]:
        """
        Desteklenen dilleri al.
        
        Returns:
            List[str]: Dil listesi
        """
        return list(self.snippets.keys())
    
    def get_builtin_snippets(self, language: str = "python") -> List[Snippet]:
        """
        Builtin snippet'ları al.
        
        Args:
            language: Programlama dili
            
        Returns:
            List[Snippet]: Builtin snippet listesi
        """
        if language in self.snippets:
            return [s for s in self.snippets[language] if s.is_builtin]
        return []


if __name__ == "__main__":
    # Basit test
    engine = SnippetsEngine()
    
    # Snippet ekle
    result = engine.insert_snippet("def", language="python")
    print(f"Insert snippet: {result.success}")
    print(f"Inserted code:\n{result.inserted_code}")
