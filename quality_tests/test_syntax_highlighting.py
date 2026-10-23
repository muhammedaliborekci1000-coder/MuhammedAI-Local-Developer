"""
Quality Test: Syntax Highlighting
Syntax highlighting system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.syntax_highlighting import (
    SyntaxHighlighter,
    TokenType,
    Theme,
    Token,
    HighlightedLine,
    SyntaxHighlightingResult
)


def test_highlight_python():
    """
    Test: Highlight Python code.
    """
    print("=" * 70)
    print("TEST: Highlight Python Code")
    print("=" * 70)
    
    code = """
def my_function(x, y):
    # This is a comment
    result = x + y
    return result
"""
    
    highlighter = SyntaxHighlighter()
    result = highlighter.highlight(code, language="python")
    
    assert result.success, "Highlighting başarılı olmalı"
    assert len(result.lines) > 0, "Lines olmalı"
    assert result.html is not None, "HTML olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Lines: {len(result.lines)}")
    print(f"  HTML length: {len(result.html)}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Highlight Python code")
    print("=" * 70)


def test_highlight_generic():
    """
    Test: Highlight generic code.
    """
    print("=" * 70)
    print("TEST: Highlight Generic Code")
    print("=" * 70)
    
    code = """
function test() {
    var x = 10;
    return x;
}
"""
    
    highlighter = SyntaxHighlighter()
    result = highlighter.highlight(code, language="javascript")
    
    assert result.success, "Highlighting başarılı olmalı"
    assert len(result.lines) > 0, "Lines olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Lines: {len(result.lines)}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Highlight generic code")
    print("=" * 70)


def test_token_type_enum():
    """
    Test: TokenType enum.
    """
    print("=" * 70)
    print("TEST: TokenType Enum")
    print("=" * 70)
    
    assert TokenType.KEYWORD.value == "keyword"
    assert TokenType.STRING.value == "string"
    assert TokenType.COMMENT.value == "comment"
    assert TokenType.FUNCTION.value == "function"
    assert TokenType.CLASS.value == "class"
    assert TokenType.VARIABLE.value == "variable"
    assert TokenType.OPERATOR.value == "operator"
    assert TokenType.NUMBER.value == "number"
    
    print(f"  All enum values verified")
    print(f"  Total types: {len(TokenType)}")
    
    print("\n" + "=" * 70)
    print("PASS: TokenType enum")
    print("=" * 70)


def test_theme_enum():
    """
    Test: Theme enum.
    """
    print("=" * 70)
    print("TEST: Theme Enum")
    print("=" * 70)
    
    assert Theme.MONOKAI.value == "monokai"
    assert Theme.DRACULA.value == "dracula"
    assert Theme.GITHUB_LIGHT.value == "github_light"
    assert Theme.GITHUB_DARK.value == "github_dark"
    assert Theme.VS_CODE_DARK.value == "vs_code_dark"
    assert Theme.SOLARIZED_DARK.value == "solarized_dark"
    assert Theme.SOLARIZED_LIGHT.value == "solarized_light"
    
    print(f"  All enum values verified")
    print(f"  Total themes: {len(Theme)}")
    
    print("\n" + "=" * 70)
    print("PASS: Theme enum")
    print("=" * 70)


def test_token_dataclass():
    """
    Test: Token dataclass.
    """
    print("=" * 70)
    print("TEST: Token Dataclass")
    print("=" * 70)
    
    token = Token(
        text="def",
        type=TokenType.KEYWORD,
        start=0,
        end=3,
        line=1,
        column=0
    )
    
    assert token.text == "def", "Text eşleşmeli"
    assert token.type == TokenType.KEYWORD, "Type eşleşmeli"
    assert token.line == 1, "Line eşleşmeli"
    
    print(f"  Text: {token.text}")
    print(f"  Type: {token.type.value}")
    print(f"  Line: {token.line}")
    
    print("\n" + "=" * 70)
    print("PASS: Token dataclass")
    print("=" * 70)


def test_highlighted_line_dataclass():
    """
    Test: HighlightedLine dataclass.
    """
    print("=" * 70)
    print("TEST: HighlightedLine Dataclass")
    print("=" * 70)
    
    line = HighlightedLine(
        line_number=1,
        tokens=[Token("def", TokenType.KEYWORD, 0, 3, 1, 0)]
    )
    
    assert line.line_number == 1, "Line number eşleşmeli"
    assert len(line.tokens) == 1, "Token sayısı eşleşmeli"
    
    print(f"  Line number: {line.line_number}")
    print(f"  Tokens: {len(line.tokens)}")
    
    print("\n" + "=" * 70)
    print("PASS: HighlightedLine dataclass")
    print("=" * 70)


def test_syntax_highlighting_result_dataclass():
    """
    Test: SyntaxHighlightingResult dataclass.
    """
    print("=" * 70)
    print("TEST: SyntaxHighlightingResult Dataclass")
    print("=" * 70)
    
    result = SyntaxHighlightingResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.lines, list), "Lines list olmalı"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Lines: {len(result.lines)}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: SyntaxHighlightingResult dataclass")
    print("=" * 70)


def test_vs_code_dark_theme():
    """
    Test: VS Code Dark theme.
    """
    print("=" * 70)
    print("TEST: VS Code Dark Theme")
    print("=" * 70)
    
    highlighter = SyntaxHighlighter(theme=Theme.VS_CODE_DARK)
    
    assert highlighter.theme == Theme.VS_CODE_DARK, "Theme eşleşmeli"
    assert len(highlighter.color_map) > 0, "Color map olmalı"
    
    print(f"  Theme: {highlighter.theme.value}")
    print(f"  Color map size: {len(highlighter.color_map)}")
    
    print("\n" + "=" * 70)
    print("PASS: VS Code Dark theme")
    print("=" * 70)


def test_monokai_theme():
    """
    Test: Monokai theme.
    """
    print("=" * 70)
    print("TEST: Monokai Theme")
    print("=" * 70)
    
    highlighter = SyntaxHighlighter(theme=Theme.MONOKAI)
    
    assert highlighter.theme == Theme.MONOKAI, "Theme eşleşmeli"
    assert len(highlighter.color_map) > 0, "Color map olmalı"
    
    print(f"  Theme: {highlighter.theme.value}")
    print(f"  Color map size: {len(highlighter.color_map)}")
    
    print("\n" + "=" * 70)
    print("PASS: Monokai theme")
    print("=" * 70)


def test_tokenization():
    """
    Test: Tokenization.
    """
    print("=" * 70)
    print("TEST: Tokenization")
    print("=" * 70)
    
    highlighter = SyntaxHighlighter()
    
    line = "def my_function():"
    tokens = highlighter._tokenize_line_simple(line, 1)
    
    assert len(tokens) > 0, "Token olmalı"
    
    print(f"  Line: {line}")
    print(f"  Tokens: {len(tokens)}")
    for token in tokens:
        print(f"    - {token.text} ({token.type.value})")
    
    print("\n" + "=" * 70)
    print("PASS: Tokenization")
    print("=" * 70)


def test_html_generation():
    """
    Test: HTML generation.
    """
    print("=" * 70)
    print("TEST: HTML Generation")
    print("=" * 70)
    
    highlighter = SyntaxHighlighter()
    
    highlighted_line = HighlightedLine(
        line_number=1,
        tokens=[Token("def", TokenType.KEYWORD, 0, 3, 1, 0)]
    )
    
    html = highlighter._generate_html([highlighted_line])
    
    assert html is not None, "HTML olmalı"
    assert "<div" in html, "Div tag olmalı"
    assert "style" in html, "Style attribute olmalı"
    
    print(f"  HTML length: {len(html)}")
    print(f"  Contains div: {'<div' in html}")
    print(f"  Contains style: {'style' in html}")
    
    print("\n" + "=" * 70)
    print("PASS: HTML generation")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_highlight_python()
        test2 = test_highlight_generic()
        test3 = test_token_type_enum()
        test4 = test_theme_enum()
        test5 = test_token_dataclass()
        test6 = test_highlighted_line_dataclass()
        test7 = test_syntax_highlighting_result_dataclass()
        test8 = test_vs_code_dark_theme()
        test9 = test_monokai_theme()
        test10 = test_tokenization()
        test11 = test_html_generation()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Highlight Python: {'PASS' if test1 else 'FAIL'}")
        print(f"Highlight Generic: {'PASS' if test2 else 'FAIL'}")
        print(f"TokenType Enum: {'PASS' if test3 else 'FAIL'}")
        print(f"Theme Enum: {'PASS' if test4 else 'FAIL'}")
        print(f"Token Dataclass: {'PASS' if test5 else 'FAIL'}")
        print(f"HighlightedLine Dataclass: {'PASS' if test6 else 'FAIL'}")
        print(f"SyntaxHighlightingResult Dataclass: {'PASS' if test7 else 'FAIL'}")
        print(f"VS Code Dark Theme: {'PASS' if test8 else 'FAIL'}")
        print(f"Monokai Theme: {'PASS' if test9 else 'FAIL'}")
        print(f"Tokenization: {'PASS' if test10 else 'FAIL'}")
        print(f"HTML Generation: {'PASS' if test11 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11])
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
