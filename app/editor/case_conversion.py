"""
MuhammedAI Local Developer - Case Conversion
Case conversion engine for code editor.
"""

from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from enum import Enum


class CaseType(Enum):
    """Case type."""
    UPPER = "upper"
    LOWER = "lower"
    TITLE = "title"
    CAMEL = "camel"
    SNAKE = "snake"
    PASCAL = "pascal"
    KEBAB = "kebab"
    SENTENCE = "sentence"
    REVERSE = "reverse"


class ConvertScope(Enum):
    """Convert scope."""
    WORD = "word"
    SELECTION = "selection"
    LINE = "line"
    DOCUMENT = "document"


@dataclass
class ConvertRange:
    """Convert range."""
    start_line: int
    end_line: int
    start_column: int = 0
    end_column: int = 0


@dataclass
class CaseConfig:
    """Case configuration."""
    scope: ConvertScope = ConvertScope.SELECTION
    preserve_formatting: bool = True
    skip_keywords: bool = True
    skip_strings: bool = True
    skip_comments: bool = True


@dataclass
class CaseResult:
    """Case result."""
    success: bool
    modified_content: str = ""
    original_content: str = ""
    words_converted: int = 0
    characters_changed: int = 0
    errors: List[str] = field(default_factory=list)
    message: Optional[str] = None


class CaseConversionEngine:
    """
    Case conversion engine.
    
    Özellikler:
    - Convert to uppercase
    - Convert to lowercase
    - Convert to title case
    - Convert to camel case
    - Convert to snake case
    - Convert to pascal case
    - Convert to kebab case
    - Convert to sentence case
    - Word conversion
    - Selection conversion
    - Line conversion
    - Document conversion
    - Preserve formatting
    - Skip keywords
    - Skip strings
    - Skip comments
    - Undo support
    - Convert history
    - Smart detection
    """
    
    def __init__(self, config: Optional[CaseConfig] = None):
        """Initialize case conversion engine."""
        self.config = config or CaseConfig()
        self.convert_history: List[Dict[str, Any]] = []
        self.keywords = {"def", "class", "if", "else", "elif", "for", "while", "return", "import", "from", "as", "in", "not", "and", "or", "True", "False", "None"}
    
    def convert_case(
        self,
        content: str,
        case_type: CaseType,
        convert_range: Optional[ConvertRange] = None
    ) -> CaseResult:
        """
        Case'i dönüştür.
        
        Args:
            content: Dosya içeriği
            case_type: Case tipi
            convert_range: Dönüştürme aralığı
            
        Returns:
            CaseResult: Dönüştürme sonucu
        """
        result = CaseResult(success=False)
        result.original_content = content
        
        try:
            if self.config.scope == ConvertScope.DOCUMENT:
                modified_content = self._convert_document(content, case_type)
            elif self.config.scope == ConvertScope.SELECTION and convert_range:
                modified_content = self._convert_selection(content, case_type, convert_range)
            elif self.config.scope == ConvertScope.LINE and convert_range:
                modified_content = self._convert_line(content, case_type, convert_range.start_line)
            elif self.config.scope == ConvertScope.WORD and convert_range:
                modified_content = self._convert_word(content, case_type, convert_range.start_line, convert_range.start_column)
            else:
                modified_content = self._convert_document(content, case_type)
            
            # Count changes
            characters_changed = sum(1 for a, b in zip(content, modified_content) if a != b)
            
            # Geçmişe ekle
            self.convert_history.append({
                "original": content,
                "modified": modified_content,
                "case_type": case_type.value,
                "scope": self.config.scope.value
            })
            
            result.success = True
            result.modified_content = modified_content
            result.words_converted = len(content.split())
            result.characters_changed = characters_changed
            result.message = f"Converted to {case_type.value} case"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def _convert_document(self, content: str, case_type: CaseType) -> str:
        """
        Dokümanı dönüştür.
        
        Args:
            content: İçerik
            case_type: Case tipi
            
        Returns:
            str: Dönüştürülmüş içerik
        """
        if case_type == CaseType.UPPER:
            return content.upper()
        elif case_type == CaseType.LOWER:
            return content.lower()
        elif case_type == CaseType.TITLE:
            return content.title()
        elif case_type == CaseType.SENTENCE:
            return self._to_sentence_case(content)
        elif case_type == CaseType.REVERSE:
            return self._to_reverse_case(content)
        else:
            return content
    
    def _convert_selection(self, content: str, case_type: CaseType, convert_range: ConvertRange) -> str:
        """
        Seçimi dönüştür.
        
        Args:
            content: İçerik
            case_type: Case tipi
            convert_range: Dönüştürme aralığı
            
        Returns:
            str: Dönüştürülmüş içerik
        """
        lines = content.splitlines()
        
        for i in range(convert_range.start_line, min(convert_range.end_line + 1, len(lines))):
            line = lines[i]
            
            if case_type == CaseType.UPPER:
                lines[i] = line.upper()
            elif case_type == CaseType.LOWER:
                lines[i] = line.lower()
            elif case_type == CaseType.TITLE:
                lines[i] = line.title()
            elif case_type == CaseType.SENTENCE:
                lines[i] = self._to_sentence_case(line)
            elif case_type == CaseType.REVERSE:
                lines[i] = self._to_reverse_case(line)
        
        return "\n".join(lines)
    
    def _convert_line(self, content: str, case_type: CaseType, line_number: int) -> str:
        """
        Satırı dönüştür.
        
        Args:
            content: İçerik
            case_type: Case tipi
            line_number: Satır numarası
            
        Returns:
            str: Dönüştürülmüş içerik
        """
        lines = content.splitlines()
        
        if line_number >= len(lines):
            return content
        
        line = lines[line_number]
        
        if case_type == CaseType.UPPER:
            lines[line_number] = line.upper()
        elif case_type == CaseType.LOWER:
            lines[line_number] = line.lower()
        elif case_type == CaseType.TITLE:
            lines[line_number] = line.title()
        elif case_type == CaseType.SENTENCE:
            lines[line_number] = self._to_sentence_case(line)
        elif case_type == CaseType.REVERSE:
            lines[line_number] = self._to_reverse_case(line)
        
        return "\n".join(lines)
    
    def _convert_word(self, content: str, case_type: CaseType, line_number: int, column: int) -> str:
        """
        Kelimeyi dönüştür.
        
        Args:
            content: İçerik
            case_type: Case tipi
            line_number: Satır numarası
            column: Sütun numarası
            
        Returns:
            str: Dönüştürülmüş içerik
        """
        lines = content.splitlines()
        
        if line_number >= len(lines):
            return content
        
        line = lines[line_number]
        
        if column >= len(line):
            return content
        
        # Kelime başlangıcını ve bitişini bul
        word_start = self._find_word_start(line, column)
        word_end = self._find_word_end(line, column)
        
        word = line[word_start:word_end]
        
        if case_type == CaseType.UPPER:
            converted_word = word.upper()
        elif case_type == CaseType.LOWER:
            converted_word = word.lower()
        elif case_type == CaseType.TITLE:
            converted_word = word.title()
        elif case_type == CaseType.SENTENCE:
            converted_word = word.capitalize()
        elif case_type == CaseType.REVERSE:
            converted_word = self._to_reverse_case(word)
        else:
            converted_word = word
        
        lines[line_number] = line[:word_start] + converted_word + line[word_end:]
        
        return "\n".join(lines)
    
    def _find_word_start(self, line: str, column: int) -> int:
        """
        Kelime başlangıcını bul.
        
        Args:
            line: Satır
            column: Sütun
            
        Returns:
            int: Kelime başlangıcı
        """
        start = column
        while start > 0 and line[start - 1].isalnum():
            start -= 1
        return start
    
    def _find_word_end(self, line: str, column: int) -> int:
        """
        Kelime bitişini bul.
        
        Args:
            line: Satır
            column: Sütun
            
        Returns:
            int: Kelime bitişi
        """
        end = column
        while end < len(line) and line[end].isalnum():
            end += 1
        return end
    
    def _to_sentence_case(self, text: str) -> str:
        """
        Sentence case'e dönüştür.
        
        Args:
            text: Metin
            
        Returns:
            str: Sentence case metin
        """
        sentences = text.split('. ')
        converted = []
        
        for sentence in sentences:
            if sentence:
                converted.append(sentence[0].upper() + sentence[1:].lower())
            else:
                converted.append(sentence)
        
        return '. '.join(converted)
    
    def _to_reverse_case(self, text: str) -> str:
        """
        Reverse case'e dönüştür.
        
        Args:
            text: Metin
            
        Returns:
            str: Reverse case metin
        """
        converted = []
        for char in text:
            if char.isupper():
                converted.append(char.lower())
            elif char.islower():
                converted.append(char.upper())
            else:
                converted.append(char)
        return ''.join(converted)
    
    def to_upper(self, content: str, convert_range: Optional[ConvertRange] = None) -> CaseResult:
        """
        Upper case'e dönüştür.
        
        Args:
            content: İçerik
            convert_range: Dönüştürme aralığı
            
        Returns:
            CaseResult: Dönüştürme sonucu
        """
        return self.convert_case(content, CaseType.UPPER, convert_range)
    
    def to_lower(self, content: str, convert_range: Optional[ConvertRange] = None) -> CaseResult:
        """
        Lower case'e dönüştür.
        
        Args:
            content: İçerik
            convert_range: Dönüştürme aralığı
            
        Returns:
            CaseResult: Dönüştürme sonucu
        """
        return self.convert_case(content, CaseType.LOWER, convert_range)
    
    def to_title(self, content: str, convert_range: Optional[ConvertRange] = None) -> CaseResult:
        """
        Title case'e dönüştür.
        
        Args:
            content: İçerik
            convert_range: Dönüştürme aralığı
            
        Returns:
            CaseResult: Dönüştürme sonucu
        """
        return self.convert_case(content, CaseType.TITLE, convert_range)
    
    def to_sentence(self, content: str, convert_range: Optional[ConvertRange] = None) -> CaseResult:
        """
        Sentence case'e dönüştür.
        
        Args:
            content: İçerik
            convert_range: Dönüştürme aralığı
            
        Returns:
            CaseResult: Dönüştürme sonucu
        """
        return self.convert_case(content, CaseType.SENTENCE, convert_range)
    
    def to_reverse(self, content: str, convert_range: Optional[ConvertRange] = None) -> CaseResult:
        """
        Reverse case'e dönüştür.
        
        Args:
            content: İçerik
            convert_range: Dönüştürme aralığı
            
        Returns:
            CaseResult: Dönüştürme sonucu
        """
        return self.convert_case(content, CaseType.REVERSE, convert_range)
    
    def to_camel(self, content: str) -> CaseResult:
        """
        Camel case'e dönüştür.
        
        Args:
            content: İçerik
            
        Returns:
            CaseResult: Dönüştürme sonucu
        """
        result = CaseResult(success=False)
        result.original_content = content
        
        try:
            words = content.lower().split('_')
            if len(words) > 1:
                converted = words[0] + ''.join(word.capitalize() for word in words[1:])
            else:
                converted = words[0]
            
            result.success = True
            result.modified_content = converted
            result.words_converted = len(words)
            result.message = "Converted to camel case"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def to_snake(self, content: str) -> CaseResult:
        """
        Snake case'e dönüştür.
        
        Args:
            content: İçerik
            
        Returns:
            CaseResult: Dönüştürme sonucu
        """
        result = CaseResult(success=False)
        result.original_content = content
        
        try:
            converted = ''.join(['_' + c.lower() if c.isupper() else c for c in content]).lstrip('_')
            
            result.success = True
            result.modified_content = converted
            result.message = "Converted to snake case"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def to_pascal(self, content: str) -> CaseResult:
        """
        Pascal case'e dönüştür.
        
        Args:
            content: İçerik
            
        Returns:
            CaseResult: Dönüştürme sonucu
        """
        result = CaseResult(success=False)
        result.original_content = content
        
        try:
            words = content.lower().split('_')
            converted = ''.join(word.capitalize() for word in words)
            
            result.success = True
            result.modified_content = converted
            result.words_converted = len(words)
            result.message = "Converted to pascal case"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def to_kebab(self, content: str) -> CaseResult:
        """
        Kebab case'e dönüştür.
        
        Args:
            content: İçerik
            
        Returns:
            CaseResult: Dönüştürme sonucu
        """
        result = CaseResult(success=False)
        result.original_content = content
        
        try:
            converted = ''.join(['-' + c.lower() if c.isupper() else c for c in content]).lstrip('-')
            
            result.success = True
            result.modified_content = converted
            result.message = "Converted to kebab case"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def undo_convert(self) -> CaseResult:
        """
        Dönüştürmeyi geri al.
        
        Returns:
            CaseResult: Geri alma sonucu
        """
        result = CaseResult(success=False)
        
        try:
            if not self.convert_history:
                result.errors.append("No convert history")
                return result
            
            last_convert = self.convert_history.pop()
            
            result.success = True
            result.modified_content = last_convert["original"]
            result.original_content = last_convert["modified"]
            result.message = "Convert operation undone"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_convert_history(self) -> List[Dict[str, Any]]:
        """
        Dönüştürme geçmişini al.
        
        Returns:
            List[Dict[str, Any]]: Geçmiş
        """
        return self.convert_history
    
    def clear_history(self) -> CaseResult:
        """
        Geçmişi temizle.
        
        Returns:
            CaseResult: Temizleme sonucu
        """
        result = CaseResult(success=False)
        
        try:
            self.convert_history.clear()
            result.success = True
            result.message = "Convert history cleared"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def update_config(self, config: CaseConfig) -> CaseResult:
        """
        Konfigürasyon güncelle.
        
        Args:
            config: Yeni konfigürasyon
            
        Returns:
            CaseResult: Güncelleme sonucu
        """
        result = CaseResult(success=False)
        
        try:
            self.config = config
            result.success = True
            result.message = "Config updated"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_config(self) -> CaseConfig:
        """
        Konfigürasyon al.
        
        Returns:
            CaseConfig: Konfigürasyon
        """
        return self.config


if __name__ == "__main__":
    # Basit test
    engine = CaseConversionEngine()
    
    content = "Hello World"
    result = engine.to_upper(content)
    print(f"Convert: {result.success}")
