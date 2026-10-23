"""
Quality Test: Bracket Matching
Bracket matching system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.bracket_matching import (
    BracketMatcher,
    BracketType,
    BracketDirection,
    Bracket,
    BracketMatch,
    BracketMatchingResult
)


def test_match_brackets():
    """
    Test: Match brackets.
    """
    print("=" * 70)
    print("TEST: Match Brackets")
    print("=" * 70)
    
    code = """
def my_function(x, y):
    result = x + y
    return result
"""
    
    matcher = BracketMatcher()
    result = matcher.match_brackets(code)
    
    assert result.success, "Matching başarılı olmalı"
    assert isinstance(result.matches, list), "Matches list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Matches: {len(result.matches)}")
    print(f"  Unmatched: {len(result.unmatched_brackets)}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Match brackets")
    print("=" * 70)


def test_find_matching_bracket():
    """
    Test: Find matching bracket.
    """
    print("=" * 70)
    print("TEST: Find Matching Bracket")
    print("=" * 70)
    
    code = "def my_function(x, y):"
    
    matcher = BracketMatcher()
    result = matcher.find_matching_bracket(code, line=1, column=15)  # '(' pozisyonu
    
    assert result is not None, "Match bulunmalı"
    assert result.is_valid, "Match geçerli olmalı"
    
    print(f"  Match found: {result is not None}")
    print(f"  Valid: {result.is_valid}")
    print(f"  Open: {result.open_bracket.char} at line {result.open_bracket.line}")
    print(f"  Close: {result.close_bracket.char} at line {result.close_bracket.line}")
    
    print("\n" + "=" * 70)
    print("PASS: Find matching bracket")
    print("=" * 70)


def test_parenthesis_matching():
    """
    Test: Parenthesis matching.
    """
    print("=" * 70)
    print("TEST: Parenthesis Matching")
    print("=" * 70)
    
    code = "(x + y) * (z - w)"
    
    matcher = BracketMatcher()
    result = matcher.match_brackets(code)
    
    assert result.success, "Matching başarılı olmalı"
    
    parenthesis_matches = [m for m in result.matches if m.open_bracket.type == BracketType.PARENTHESIS]
    print(f"  Parenthesis matches: {len(parenthesis_matches)}")
    
    print("\n" + "=" * 70)
    print("PASS: Parenthesis matching")
    print("=" * 70)


def test_square_bracket_matching():
    """
    Test: Square bracket matching.
    """
    print("=" * 70)
    print("TEST: Square Bracket Matching")
    print("=" * 70)
    
    code = "x = [1, 2, 3]"
    
    matcher = BracketMatcher()
    result = matcher.match_brackets(code)
    
    assert result.success, "Matching başarılı olmalı"
    
    square_matches = [m for m in result.matches if m.open_bracket.type == BracketType.SQUARE]
    print(f"  Square bracket matches: {len(square_matches)}")
    
    print("\n" + "=" * 70)
    print("PASS: Square bracket matching")
    print("=" * 70)


def test_curly_bracket_matching():
    """
    Test: Curly bracket matching.
    """
    print("=" * 70)
    print("TEST: Curly Bracket Matching")
    print("=" * 70)
    
    code = "x = {'key': 'value'}"
    
    matcher = BracketMatcher()
    result = matcher.match_brackets(code)
    
    assert result.success, "Matching başarılı olmalı"
    
    curly_matches = [m for m in result.matches if m.open_bracket.type == BracketType.CURLY]
    print(f"  Curly bracket matches: {len(curly_matches)}")
    
    print("\n" + "=" * 70)
    print("PASS: Curly bracket matching")
    print("=" * 70)


def test_angle_bracket_matching():
    """
    Test: Angle bracket matching.
    """
    print("=" * 70)
    print("TEST: Angle Bracket Matching")
    print("=" * 70)
    
    code = "x < y > z"
    
    matcher = BracketMatcher()
    result = matcher.match_brackets(code)
    
    assert result.success, "Matching başarılı olmalı"
    
    angle_matches = [m for m in result.matches if m.open_bracket.type == BracketType.ANGLE]
    print(f"  Angle bracket matches: {len(angle_matches)}")
    
    print("\n" + "=" * 70)
    print("PASS: Angle bracket matching")
    print("=" * 70)


def test_nested_brackets():
    """
    Test: Nested brackets.
    """
    print("=" * 70)
    print("TEST: Nested Brackets")
    print("=" * 70)
    
    code = "((x + y) * z)"
    
    matcher = BracketMatcher()
    result = matcher.match_brackets(code)
    
    assert result.success, "Matching başarılı olmalı"
    
    print(f"  Matches: {len(result.matches)}")
    print(f"  Unmatched: {len(result.unmatched_brackets)}")
    
    print("\n" + "=" * 70)
    print("PASS: Nested brackets")
    print("=" * 70)


def test_unmatched_brackets():
    """
    Test: Unmatched brackets.
    """
    print("=" * 70)
    print("TEST: Unmatched Brackets")
    print("=" * 70)
    
    code = "def my_function(x, y:"  # Eşleşmeyen parantez
    
    matcher = BracketMatcher()
    result = matcher.match_brackets(code)
    
    assert result.success, "Matching başarılı olmalı"
    assert len(result.unmatched_brackets) > 0, "Unmatched bracket olmalı"
    
    print(f"  Unmatched brackets: {len(result.unmatched_brackets)}")
    
    print("\n" + "=" * 70)
    print("PASS: Unmatched brackets")
    print("=" * 70)


def test_bracket_type_enum():
    """
    Test: BracketType enum.
    """
    print("=" * 70)
    print("TEST: BracketType Enum")
    print("=" * 70)
    
    assert BracketType.PARENTHESIS.value == "parenthesis"
    assert BracketType.SQUARE.value == "square"
    assert BracketType.CURLY.value == "curly"
    assert BracketType.ANGLE.value == "angle"
    
    print(f"  All enum values verified")
    print(f"  Total types: {len(BracketType)}")
    
    print("\n" + "=" * 70)
    print("PASS: BracketType enum")
    print("=" * 70)


def test_bracket_direction_enum():
    """
    Test: BracketDirection enum.
    """
    print("=" * 70)
    print("TEST: BracketDirection Enum")
    print("=" * 70)
    
    assert BracketDirection.OPEN.value == "open"
    assert BracketDirection.CLOSE.value == "close"
    
    print(f"  All enum values verified")
    print(f"  Total directions: {len(BracketDirection)}")
    
    print("\n" + "=" * 70)
    print("PASS: BracketDirection enum")
    print("=" * 70)


def test_bracket_dataclass():
    """
    Test: Bracket dataclass.
    """
    print("=" * 70)
    print("TEST: Bracket Dataclass")
    print("=" * 70)
    
    bracket = Bracket(
        char="(",
        type=BracketType.PARENTHESIS,
        direction=BracketDirection.OPEN,
        line=1,
        column=0,
        index=0
    )
    
    assert bracket.char == "(", "Char eşleşmeli"
    assert bracket.type == BracketType.PARENTHESIS, "Type eşleşmeli"
    assert bracket.line == 1, "Line eşleşmeli"
    
    print(f"  Char: {bracket.char}")
    print(f"  Type: {bracket.type.value}")
    print(f"  Line: {bracket.line}")
    
    print("\n" + "=" * 70)
    print("PASS: Bracket dataclass")
    print("=" * 70)


def test_bracket_match_dataclass():
    """
    Test: BracketMatch dataclass.
    """
    print("=" * 70)
    print("TEST: BracketMatch Dataclass")
    print("=" * 70)
    
    open_bracket = Bracket("(", BracketType.PARENTHESIS, BracketDirection.OPEN, 1, 0, 0)
    close_bracket = Bracket(")", BracketType.PARENTHESIS, BracketDirection.CLOSE, 1, 5, 5)
    
    match = BracketMatch(
        open_bracket=open_bracket,
        close_bracket=close_bracket,
        is_valid=True
    )
    
    assert match.open_bracket.char == "(", "Open bracket eşleşmeli"
    assert match.close_bracket.char == ")", "Close bracket eşleşmeli"
    assert match.is_valid == True, "Valid eşleşmeli"
    
    print(f"  Open: {match.open_bracket.char}")
    print(f"  Close: {match.close_bracket.char}")
    print(f"  Valid: {match.is_valid}")
    
    print("\n" + "=" * 70)
    print("PASS: BracketMatch dataclass")
    print("=" * 70)


def test_bracket_matching_result_dataclass():
    """
    Test: BracketMatchingResult dataclass.
    """
    print("=" * 70)
    print("TEST: BracketMatchingResult Dataclass")
    print("=" * 70)
    
    result = BracketMatchingResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.matches, list), "Matches list olmalı"
    assert isinstance(result.unmatched_brackets, list), "Unmatched brackets list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Matches: {len(result.matches)}")
    print(f"  Unmatched: {len(result.unmatched_brackets)}")
    
    print("\n" + "=" * 70)
    print("PASS: BracketMatchingResult dataclass")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_match_brackets()
        test2 = test_find_matching_bracket()
        test3 = test_parenthesis_matching()
        test4 = test_square_bracket_matching()
        test5 = test_curly_bracket_matching()
        test6 = test_angle_bracket_matching()
        test7 = test_nested_brackets()
        test8 = test_unmatched_brackets()
        test9 = test_bracket_type_enum()
        test10 = test_bracket_direction_enum()
        test11 = test_bracket_dataclass()
        test12 = test_bracket_match_dataclass()
        test13 = test_bracket_matching_result_dataclass()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Match Brackets: {'PASS' if test1 else 'FAIL'}")
        print(f"Find Matching Bracket: {'PASS' if test2 else 'FAIL'}")
        print(f"Parenthesis Matching: {'PASS' if test3 else 'FAIL'}")
        print(f"Square Bracket Matching: {'PASS' if test4 else 'FAIL'}")
        print(f"Curly Bracket Matching: {'PASS' if test5 else 'FAIL'}")
        print(f"Angle Bracket Matching: {'PASS' if test6 else 'FAIL'}")
        print(f"Nested Brackets: {'PASS' if test7 else 'FAIL'}")
        print(f"Unmatched Brackets: {'PASS' if test8 else 'FAIL'}")
        print(f"BracketType Enum: {'PASS' if test9 else 'FAIL'}")
        print(f"BracketDirection Enum: {'PASS' if test10 else 'FAIL'}")
        print(f"Bracket Dataclass: {'PASS' if test11 else 'FAIL'}")
        print(f"BracketMatch Dataclass: {'PASS' if test12 else 'FAIL'}")
        print(f"BracketMatchingResult Dataclass: {'PASS' if test13 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13])
        print(f"\nTOPLAM: {'PASS' if all_passed else 'FAIL'}")
        print("=" * 70)
        
        sys.exit(0 if all_passed else 1)
    except Exception as e:
        print(f"\nTEST HATASI:")
        print("-" * 70)
        import traceback
        traceback.print_exc()
        print("=" * 70)
        sys.exit(1)
