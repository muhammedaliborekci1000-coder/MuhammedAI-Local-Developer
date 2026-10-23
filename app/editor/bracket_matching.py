"""
MuhammedAI Local Developer - Bracket Matching
Bracket matching engine for code editor.
"""

from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from enum import Enum


class BracketType(Enum):
    """Bracket type."""
    PARENTHESIS = "parenthesis"  # ()
    SQUARE = "square"  # []
    CURLY = "curly"  # {}
    ANGLE = "angle"  # <>


class BracketDirection(Enum):
    """Bracket direction."""
    OPEN = "open"
    CLOSE = "close"


@dataclass
class Bracket:
    """Bracket."""
    char: str
    type: BracketType
    direction: BracketDirection
    line: int
    column: int
    index: int


@dataclass
class BracketMatch:
    """Bracket match."""
    open_bracket: Bracket
    close_bracket: Bracket
    is_valid: bool
    error_message: Optional[str] = None


@dataclass
class BracketMatchingResult:
    """Bracket matching result."""
    success: bool
    matches: List[BracketMatch] = field(default_factory=list)
    unmatched_brackets: List[Bracket] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    message: Optional[str] = None


class BracketMatcher:
    """
    Bracket matching engine.
    
    Özellikler:
    - Parenthesis matching ()
    - Square bracket matching []
    - Curly bracket matching {}
    - Angle bracket matching <>
    - Multi-line support
    - Nested bracket support
    - Invalid bracket detection
    - Unmatched bracket detection
    - Bracket pair highlighting
    """
    
    def __init__(self):
        """Initialize bracket matcher."""
        self.bracket_pairs = {
            '(': (')', BracketType.PARENTHESIS),
            ')': ('(', BracketType.PARENTHESIS),
            '[': (']', BracketType.SQUARE),
            ']': ('[', BracketType.SQUARE),
            '{': ('}', BracketType.CURLY),
            '}': ('{', BracketType.CURLY),
            '<': ('>', BracketType.ANGLE),
            '>': ('<', BracketType.ANGLE)
        }
    
    def match_brackets(
        self,
        code: str
    ) -> BracketMatchingResult:
        """
        Parantezleri eşleştir.
        
        Args:
            code: Kod içeriği
            
        Returns:
            BracketMatchingResult: Matching sonucu
        """
        result = BracketMatchingResult(success=False)
        
        try:
            # Bracket'ları bul
            brackets = self._find_brackets(code)
            
            # Eşleştir
            matches, unmatched = self._match_brackets(brackets)
            
            result.matches = matches
            result.unmatched_brackets = unmatched
            result.success = True
            result.message = f"Found {len(matches)} matches, {len(unmatched)} unmatched"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def find_matching_bracket(
        self,
        code: str,
        line: int,
        column: int
    ) -> Optional[BracketMatch]:
        """
        Belirli bir pozisyondaki bracket'ın eşleşmesini bul.
        
        Args:
            code: Kod içeriği
            line: Satır numarası
            column: Sütun numarası
            
        Returns:
            BracketMatch: Bracket eşleşmesi veya None
        """
        try:
            # Bracket'ları bul
            brackets = self._find_brackets(code)
            
            # İstenen pozisyonu bul
            target_index = self._get_position_index(code, line, column)
            
            for bracket in brackets:
                if bracket.index == target_index:
                    # Eşleşmeyi bul
                    return self._find_match_for_bracket(bracket, brackets)
            
            return None
        
        except Exception:
            return None
    
    def _find_brackets(self, code: str) -> List[Bracket]:
        """Tüm bracket'ları bul."""
        brackets = []
        lines = code.splitlines()
        index = 0
        
        for line_num, line in enumerate(lines, 1):
            for col_num, char in enumerate(line, 0):
                if char in self.bracket_pairs:
                    bracket_type, direction = self._get_bracket_info(char)
                    
                    bracket = Bracket(
                        char=char,
                        type=bracket_type,
                        direction=direction,
                        line=line_num,
                        column=col_num,
                        index=index
                    )
                    brackets.append(bracket)
                
                index += 1
            
            index += 1  # Newline karakteri için
        
        return brackets
    
    def _get_bracket_info(self, char: str) -> Tuple[BracketType, BracketDirection]:
        """Bracket bilgisi al."""
        if char in '()':
            return BracketType.PARENTHESIS, BracketDirection.OPEN if char == '(' else BracketDirection.CLOSE
        elif char in '[]':
            return BracketType.SQUARE, BracketDirection.OPEN if char == '[' else BracketDirection.CLOSE
        elif char in '{}':
            return BracketType.CURLY, BracketDirection.OPEN if char == '{' else BracketDirection.CLOSE
        elif char in '<>':
            return BracketType.ANGLE, BracketDirection.OPEN if char == '<' else BracketDirection.CLOSE
        else:
            return BracketType.PARENTHESIS, BracketDirection.OPEN
    
    def _match_brackets(
        self,
        brackets: List[Bracket]
    ) -> Tuple[List[BracketMatch], List[Bracket]]:
        """Bracket'ları eşleştir."""
        matches = []
        unmatched = []
        stack = []
        
        for bracket in brackets:
            if bracket.direction == BracketDirection.OPEN:
                stack.append(bracket)
            else:
                # Close bracket - stack'ten matching open bracket'ı bul
                if stack:
                    open_bracket = stack.pop()
                    
                    # Tip kontrolü
                    if open_bracket.type == bracket.type:
                        match = BracketMatch(
                            open_bracket=open_bracket,
                            close_bracket=bracket,
                            is_valid=True
                        )
                        matches.append(match)
                    else:
                        # Tip uyuşmazlığı
                        match = BracketMatch(
                            open_bracket=open_bracket,
                            close_bracket=bracket,
                            is_valid=False,
                            error_message=f"Mismatched bracket types: {open_bracket.char} and {bracket.char}"
                        )
                        matches.append(match)
                        unmatched.append(open_bracket)
                        unmatched.append(bracket)
                else:
                    # Eşleşme yok
                    unmatched.append(bracket)
        
        # Stack'te kalan open bracket'lar
        unmatched.extend(stack)
        
        return matches, unmatched
    
    def _find_match_for_bracket(
        self,
        bracket: Bracket,
        brackets: List[Bracket]
    ) -> Optional[BracketMatch]:
        """Bracket için eşleşme bul."""
        if bracket.direction == BracketDirection.OPEN:
            # Open bracket - matching close bracket'ı bul
            matching_char = self.bracket_pairs[bracket.char][0]
            depth = 0
            
            for b in brackets:
                if b.index <= bracket.index:
                    continue
                
                if b.char == bracket.char:
                    depth += 1
                elif b.char == matching_char:
                    if depth == 0:
                        return BracketMatch(
                            open_bracket=bracket,
                            close_bracket=b,
                            is_valid=True
                        )
                    depth -= 1
            
            return None
        else:
            # Close bracket - matching open bracket'ı bul
            matching_char = self.bracket_pairs[bracket.char][0]
            depth = 0
            
            for b in reversed(brackets):
                if b.index >= bracket.index:
                    continue
                
                if b.char == bracket.char:
                    depth += 1
                elif b.char == matching_char:
                    if depth == 0:
                        return BracketMatch(
                            open_bracket=b,
                            close_bracket=bracket,
                            is_valid=True
                        )
                    depth -= 1
            
            return None
    
    def _get_position_index(self, code: str, line: int, column: int) -> int:
        """Pozisyon index'ini hesapla."""
        lines = code.splitlines()
        index = 0
        
        for i in range(line - 1):
            index += len(lines[i]) + 1  # +1 for newline
        
        index += column
        
        return index


if __name__ == "__main__":
    # Basit test
    matcher = BracketMatcher()
    
    code = """
def my_function(x, y):
    result = x + y
    return result
"""
    
    result = matcher.match_brackets(code)
    print(f"Matching: {result.success}")
    print(f"Matches: {len(result.matches)}")
    print(f"Unmatched: {len(result.unmatched_brackets)}")
