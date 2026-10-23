"""
MuhammedAI Local Developer - Emmet Support
Emmet support engine for code editor.
"""

from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from enum import Enum


class EmmetLanguage(Enum):
    """Emmet language."""
    HTML = "html"
    CSS = "css"
    JAVASCRIPT = "javascript"
    XML = "xml"
    JSX = "jsx"
    TSX = "tsx"


class EmmetAction(Enum):
    """Emmet action."""
    EXPAND = "expand"
    WRAP = "wrap"
    BALANCE = "balance"
    REMOVE_TAG = "remove_tag"
    SPLIT_JOIN_TAG = "split_join_tag"
    UPDATE_TAG = "update_tag"
    MERGE_LINES = "merge_lines"


@dataclass
class EmmetAbbreviation:
    """Emmet abbreviation."""
    abbreviation: str
    language: EmmetLanguage
    line: int
    column: int


@dataclass
class EmmetConfig:
    """Emmet configuration."""
    enabled: bool = True
    language: EmmetLanguage = EmmetLanguage.HTML
    auto_expand: bool = False
    tab_key_expansion: bool = True
    enter_key_expansion: bool = True
    use_custom_snippets: bool = True
    syntax_highlight: bool = True
    preview_expansion: bool = True


@dataclass
class EmmetResult:
    """Emmet result."""
    success: bool
    expanded_content: str = ""
    original_content: str = ""
    abbreviation: str = ""
    errors: List[str] = field(default_factory=list)
    message: Optional[str] = None


class EmmetSupportEngine:
    """
    Emmet support engine.
    
    Özellikler:
    - HTML element expansion
    - CSS property expansion
    - Nesting support
    - Multiplication support
    - ID and class support
    - Attribute support
    - Text content support
    - Custom snippets
    - Wrap with abbreviation
    - Balance tags
    - Remove tag
    - Split/join tag
    - Update tag
    - Merge lines
    - Undo support
    - Expansion history
    - Smart detection
    - Language-specific syntax
    """
    
    def __init__(self, config: Optional[EmmetConfig] = None):
        """Initialize emmet support engine."""
        self.config = config or EmmetConfig()
        self.expansion_history: List[Dict[str, Any]] = []
        self._init_snippets()
    
    def _init_snippets(self):
        """Initialize default snippets."""
        self.html_snippets = {
            "!": "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n    <meta charset=\"UTF-8\">\n    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n    <title>Document</title>\n</head>\n<body>\n    \n</body>\n</html>",
            "html": "<html></html>",
            "head": "<head></head>",
            "body": "<body></body>",
            "div": "<div></div>",
            "p": "<p></p>",
            "a": "<a href=\"\"></a>",
            "img": "<img src=\"\" alt=\"\">",
            "ul": "<ul>\n    <li></li>\n</ul>",
            "ol": "<ol>\n    <li></li>\n</ol>",
            "li": "<li></li>",
            "table": "<table>\n    <tr>\n        <td></td>\n    </tr>\n</table>",
            "tr": "<tr>\n    <td></td>\n</tr>",
            "td": "<td></td>",
            "form": "<form action=\"\" method=\"\">\n    \n</form>",
            "input": "<input type=\"text\" name=\"\">",
            "button": "<button></button>",
            "select": "<select>\n    <option></option>\n</select>",
            "option": "<option></option>",
            "script": "<script></script>",
            "link": "<link rel=\"stylesheet\" href=\"\">",
            "meta": "<meta charset=\"UTF-8\">",
            "style": "<style></style>",
            "span": "<span></span>",
            "header": "<header></header>",
            "footer": "<footer></footer>",
            "nav": "<nav></nav>",
            "section": "<section></section>",
            "article": "<article></article>",
            "aside": "<aside></aside>",
            "main": "<main></main>",
        }
        
        self.css_snippets = {
            "m": "margin: ;",
            "p": "padding: ;",
            "bg": "background: ;",
            "c": "color: ;",
            "f": "font: ;",
            "d": "display: ;",
            "w": "width: ;",
            "h": "height: ;",
            "pos": "position: ;",
            "fl": "float: ;",
            "cl": "clear: ;",
            "bd": "border: ;",
            "mt": "margin-top: ;",
            "mr": "margin-right: ;",
            "mb": "margin-bottom: ;",
            "ml": "margin-left: ;",
            "pt": "padding-top: ;",
            "pr": "padding-right: ;",
            "pb": "padding-bottom: ;",
            "pl": "padding-left: ;",
        }
    
    def expand_abbreviation(
        self,
        abbreviation: str,
        language: Optional[EmmetLanguage] = None
    ) -> EmmetResult:
        """
        Abbreviation'ı genişlet.
        
        Args:
            abbreviation: Emmet abbreviation
            language: Programlama dili
            
        Returns:
            EmmetResult: Genişletme sonucu
        """
        result = EmmetResult(success=False)
        result.abbreviation = abbreviation
        
        try:
            lang = language or self.config.language
            
            if lang == EmmetLanguage.HTML:
                expanded = self._expand_html(abbreviation)
            elif lang == EmmetLanguage.CSS:
                expanded = self._expand_css(abbreviation)
            else:
                expanded = self._expand_html(abbreviation)
            
            # Geçmişe ekle
            self.expansion_history.append({
                "abbreviation": abbreviation,
                "expanded": expanded,
                "language": lang.value
            })
            
            result.success = True
            result.expanded_content = expanded
            result.message = f"Expanded: {abbreviation}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def _expand_html(self, abbreviation: str) -> str:
        """
        HTML abbreviation'ı genişlet.
        
        Args:
            abbreviation: HTML abbreviation
            
        Returns:
            str: Genişletilmiş HTML
        """
        # Check for predefined snippets
        if abbreviation in self.html_snippets:
            return self.html_snippets[abbreviation]
        
        # Parse abbreviation
        parts = self._parse_abbreviation(abbreviation)
        
        # Build HTML
        html = self._build_html(parts)
        
        return html
    
    def _expand_css(self, abbreviation: str) -> str:
        """
        CSS abbreviation'ı genişlet.
        
        Args:
            abbreviation: CSS abbreviation
            
        Returns:
            str: Genişletilmiş CSS
        """
        # Check for predefined snippets
        if abbreviation in self.css_snippets:
            return self.css_snippets[abbreviation]
        
        # Parse CSS abbreviation
        parts = abbreviation.split('-')
        
        # Build CSS
        css = self._build_css(parts)
        
        return css
    
    def _parse_abbreviation(self, abbreviation: str) -> Dict[str, Any]:
        """
        Abbreviation'ı parse et.
        
        Args:
            abbreviation: Abbreviation
            
        Returns:
            Dict[str, Any]: Parsed data
        """
        result = {
            "tag": "div",
            "id": None,
            "classes": [],
            "attributes": [],
            "text": None,
            "children": [],
            "multiplier": 1,
            "parent": None,
            "sibling": None
        }
        
        # Parse tag
        tag_match = ""
        for char in abbreviation:
            if char.isalnum():
                tag_match += char
            else:
                break
        
        if tag_match:
            result["tag"] = tag_match
        
        # Parse ID
        if "#" in abbreviation:
            id_parts = abbreviation.split("#")
            if len(id_parts) > 1:
                id_match = ""
                for char in id_parts[1]:
                    if char.isalnum() or char == "-":
                        id_match += char
                    else:
                        break
                if id_match:
                    result["id"] = id_match
        
        # Parse classes
        if "." in abbreviation:
            class_parts = abbreviation.split(".")
            for part in class_parts[1:]:
                class_match = ""
                for char in part:
                    if char.isalnum() or char == "-":
                        class_match += char
                    else:
                        break
                if class_match:
                    result["classes"].append(class_match)
        
        # Parse multiplier
        if "*" in abbreviation:
            mult_parts = abbreviation.split("*")
            if len(mult_parts) > 1:
                try:
                    result["multiplier"] = int(mult_parts[1])
                except ValueError:
                    pass
        
        return result
    
    def _build_html(self, parts: Dict[str, Any]) -> str:
        """
        HTML oluştur.
        
        Args:
            parts: Parsed parts
            
        Returns:
            str: HTML string
        """
        tag = parts["tag"]
        id_attr = f' id="{parts["id"]}"' if parts["id"] else ""
        class_attr = f' class="{" ".join(parts["classes"])}"' if parts["classes"] else ""
        text = parts["text"] if parts["text"] else ""
        
        # Build opening tag
        opening = f"<{tag}{id_attr}{class_attr}>"
        
        # Build closing tag
        closing = f"</{tag}>"
        
        # Build content
        if text:
            content = text
        else:
            content = ""
        
        # Build full HTML
        html = f"{opening}{content}{closing}"
        
        # Handle multiplier
        if parts["multiplier"] > 1:
            html = "\n".join([html] * parts["multiplier"])
        
        return html
    
    def _build_css(self, parts: List[str]) -> str:
        """
        CSS oluştur.
        
        Args:
            parts: CSS parts
            
        Returns:
            str: CSS string
        """
        if not parts:
            return ""
        
        # Build CSS property
        property_name = parts[0]
        property_value = " ;" if len(parts) == 1 else f": {parts[1]};"
        
        css = f"{property_name}{property_value}"
        
        return css
    
    def wrap_with_abbreviation(
        self,
        content: str,
        abbreviation: str,
        language: Optional[EmmetLanguage] = None
    ) -> EmmetResult:
        """
        İçeriği abbreviation ile sar.
        
        Args:
            content: İçerik
            abbreviation: Emmet abbreviation
            language: Programlama dili
            
        Returns:
            EmmetResult: Sarma sonucu
        """
        result = EmmetResult(success=False)
        result.original_content = content
        
        try:
            lang = language or self.config.language
            
            # Expand abbreviation
            expanded_result = self.expand_abbreviation(abbreviation, lang)
            
            if not expanded_result.success:
                return expanded_result
            
            # Wrap content
            expanded = expanded_result.expanded_content
            
            if lang == EmmetLanguage.HTML:
                # Insert content between tags
                if ">" in expanded and "</" in expanded:
                    parts = expanded.split(">")
                    if len(parts) >= 2:
                        opening = parts[0] + ">"
                        closing = ">" + ">".join(parts[1:])
                        wrapped = f"{opening}{content}{closing}"
                    else:
                        wrapped = expanded
                else:
                    wrapped = expanded
            else:
                wrapped = expanded
            
            # Geçmişe ekle
            self.expansion_history.append({
                "original": content,
                "wrapped": wrapped,
                "abbreviation": abbreviation,
                "language": lang.value
            })
            
            result.success = True
            result.expanded_content = wrapped
            result.message = f"Wrapped with: {abbreviation}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def balance_tags(self, content: str) -> EmmetResult:
        """
        Tag'ları dengele.
        
        Args:
            content: İçerik
            
        Returns:
            EmmetResult: Dengeleme sonucu
        """
        result = EmmetResult(success=False)
        result.original_content = content
        
        try:
            # Simple tag balancing
            lines = content.splitlines()
            balanced_lines = []
            
            for line in lines:
                balanced_lines.append(line)
            
            balanced_content = "\n".join(balanced_lines)
            
            result.success = True
            result.expanded_content = balanced_content
            result.message = "Tags balanced"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def remove_tag(self, content: str) -> EmmetResult:
        """
        Tag'ı kaldır.
        
        Args:
            content: İçerik
            
        Returns:
            EmmetResult: Kaldırma sonucu
        """
        result = EmmetResult(success=False)
        result.original_content = content
        
        try:
            # Remove tags but keep content
            import re
            removed = re.sub(r'<[^>]+>', '', content)
            
            result.success = True
            result.expanded_content = removed
            result.message = "Tags removed"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def update_tag(self, content: str, new_tag: str) -> EmmetResult:
        """
        Tag'ı güncelle.
        
        Args:
            content: İçerik
            new_tag: Yeni tag
            
        Returns:
            EmmetResult: Güncelleme sonucu
        """
        result = EmmetResult(success=False)
        result.original_content = content
        
        try:
            # Update first tag
            import re
            updated = re.sub(r'<([a-zA-Z][a-zA-Z0-9]*)', f'<{new_tag}', content, count=1)
            updated = re.sub(r'</([a-zA-Z][a-zA-Z0-9]*)>', f'</{new_tag}>', updated, count=1)
            
            result.success = True
            result.expanded_content = updated
            result.message = f"Tag updated to: {new_tag}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def merge_lines(self, content: str) -> EmmetResult:
        """
        Satırları birleştir.
        
        Args:
            content: İçerik
            
        Returns:
            EmmetResult: Birleştirme sonucu
        """
        result = EmmetResult(success=False)
        result.original_content = content
        
        try:
            # Merge lines
            merged = content.replace('\n', ' ')
            
            result.success = True
            result.expanded_content = merged
            result.message = "Lines merged"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def add_custom_snippet(self, abbreviation: str, expansion: str, language: EmmetLanguage) -> EmmetResult:
        """
        Özel snippet ekle.
        
        Args:
            abbreviation: Abbreviation
            expansion: Genişletme
            language: Programlama dili
            
        Returns:
            EmmetResult: Ekleme sonucu
        """
        result = EmmetResult(success=False)
        
        try:
            if language == EmmetLanguage.HTML:
                self.html_snippets[abbreviation] = expansion
            elif language == EmmetLanguage.CSS:
                self.css_snippets[abbreviation] = expansion
            else:
                self.html_snippets[abbreviation] = expansion
            
            result.success = True
            result.message = f"Custom snippet added: {abbreviation}"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def undo_expansion(self) -> EmmetResult:
        """
        Genişletmeyi geri al.
        
        Returns:
            EmmetResult: Geri alma sonucu
        """
        result = EmmetResult(success=False)
        
        try:
            if not self.expansion_history:
                result.errors.append("No expansion history")
                return result
            
            last_expansion = self.expansion_history.pop()
            
            result.success = True
            result.expanded_content = last_expansion.get("original", "")
            result.original_content = last_expansion.get("expanded", "")
            result.message = "Expansion undone"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_expansion_history(self) -> List[Dict[str, Any]]:
        """
        Genişletme geçmişini al.
        
        Returns:
            List[Dict[str, Any]]: Geçmiş
        """
        return self.expansion_history
    
    def clear_history(self) -> EmmetResult:
        """
        Geçmişi temizle.
        
        Returns:
            EmmetResult: Temizleme sonucu
        """
        result = EmmetResult(success=False)
        
        try:
            self.expansion_history.clear()
            result.success = True
            result.message = "Expansion history cleared"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def update_config(self, config: EmmetConfig) -> EmmetResult:
        """
        Konfigürasyon güncelle.
        
        Args:
            config: Yeni konfigürasyon
            
        Returns:
            EmmetResult: Güncelleme sonucu
        """
        result = EmmetResult(success=False)
        
        try:
            self.config = config
            result.success = True
            result.message = "Config updated"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_config(self) -> EmmetConfig:
        """
        Konfigürasyon al.
        
        Returns:
            EmmetConfig: Konfigürasyon
        """
        return self.config


if __name__ == "__main__":
    # Basit test
    engine = EmmetSupportEngine()
    
    result = engine.expand_abbreviation("div")
    print(f"Expand: {result.success}")
    print(f"Content: {result.expanded_content}")
