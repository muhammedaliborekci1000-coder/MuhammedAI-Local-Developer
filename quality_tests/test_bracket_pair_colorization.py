"""
Quality Test: Bracket Pair Colorization
Bracket pair colorization system testleri.
"""

import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from app.editor.bracket_pair_colorization import (
    BracketColor,
    BracketType,
    BracketPosition,
    BracketPair,
    BracketPairColorConfig,
    BracketPairColorResult,
    BracketPairColorizationManager
)


def test_bracket_color_enum():
    """
    Test: BracketColor enum.
    """
    print("=" * 70)
    print("TEST: BracketColor Enum")
    print("=" * 70)
    
    assert BracketColor.RED.value == "red"
    assert BracketColor.GREEN.value == "green"
    assert BracketColor.BLUE.value == "blue"
    assert BracketColor.YELLOW.value == "yellow"
    assert BracketColor.PURPLE.value == "purple"
    assert BracketColor.CYAN.value == "cyan"
    assert BracketColor.ORANGE.value == "orange"
    assert BracketColor.PINK.value == "pink"
    
    print(f"  All enum values verified")
    print(f"  Total colors: {len(BracketColor)}")
    
    print("\n" + "=" * 70)
    print("PASS: BracketColor enum")
    print("=" * 70)


def test_bracket_type_enum():
    """
    Test: BracketType enum.
    """
    print("=" * 70)
    print("TEST: BracketType Enum")
    print("=" * 70)
    
    assert BracketType.ROUND.value == "round"
    assert BracketType.SQUARE.value == "square"
    assert BracketType.CURLY.value == "curly"
    assert BracketType.ANGLE.value == "angle"
    
    print(f"  All enum values verified")
    print(f"  Total types: {len(BracketType)}")
    
    print("\n" + "=" * 70)
    print("PASS: BracketType enum")
    print("=" * 70)


def test_bracket_position_dataclass():
    """
    Test: BracketPosition dataclass.
    """
    print("=" * 70)
    print("TEST: BracketPosition Dataclass")
    print("=" * 70)
    
    position = BracketPosition(
        line=0,
        column=0
    )
    
    assert position.line == 0, "Line eşleşmeli"
    assert position.column == 0, "Column eşleşmeli"
    
    print(f"  Line: {position.line}")
    print(f"  Column: {position.column}")
    
    print("\n" + "=" * 70)
    print("PASS: BracketPosition dataclass")
    print("=" * 70)


def test_bracket_pair_dataclass():
    """
    Test: BracketPair dataclass.
    """
    print("=" * 70)
    print("TEST: BracketPair Dataclass")
    print("=" * 70)
    
    opening = BracketPosition(0, 0)
    closing = BracketPosition(0, 10)
    
    pair = BracketPair(
        opening=opening,
        closing=closing,
        type=BracketType.ROUND,
        color=BracketColor.RED,
        nesting_level=0
    )
    
    assert pair.type == BracketType.ROUND, "Type eşleşmeli"
    assert pair.color == BracketColor.RED, "Color eşleşmeli"
    assert pair.nesting_level == 0, "Nesting level eşleşmeli"
    
    print(f"  Type: {pair.type.value}")
    print(f"  Color: {pair.color.value}")
    print(f"  Nesting level: {pair.nesting_level}")
    
    print("\n" + "=" * 70)
    print("PASS: BracketPair dataclass")
    print("=" * 70)


def test_bracket_pair_color_config_dataclass():
    """
    Test: BracketPairColorConfig dataclass.
    """
    print("=" * 70)
    print("TEST: BracketPairColorConfig Dataclass")
    print("=" * 70)
    
    config = BracketPairColorConfig(
        enabled=True,
        color_scheme="rainbow"
    )
    
    assert config.enabled == True, "Enabled eşleşmeli"
    assert config.color_scheme == "rainbow", "Color scheme eşleşmeli"
    
    print(f"  Enabled: {config.enabled}")
    print(f"  Color scheme: {config.color_scheme}")
    
    print("\n" + "=" * 70)
    print("PASS: BracketPairColorConfig dataclass")
    print("=" * 70)


def test_bracket_pair_color_result_dataclass():
    """
    Test: BracketPairColorResult dataclass.
    """
    print("=" * 70)
    print("TEST: BracketPairColorResult Dataclass")
    print("=" * 70)
    
    result = BracketPairColorResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.bracket_pairs, list), "Bracket pairs list olmalı"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Bracket pairs: {len(result.bracket_pairs)}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: BracketPairColorResult dataclass")
    print("=" * 70)


def test_bracket_pair_colorization_manager_initialization():
    """
    Test: BracketPairColorizationManager initialization.
    """
    print("=" * 70)
    print("TEST: BracketPairColorizationManager Initialization")
    print("=" * 70)
    
    config = BracketPairColorConfig()
    manager = BracketPairColorizationManager(config)
    
    assert manager.config == config, "Config eşleşmeli"
    assert len(manager.bracket_pairs) == 0, "Bracket pairs boş olmalı"
    
    print(f"  Bracket pairs: {len(manager.bracket_pairs)}")
    
    print("\n" + "=" * 70)
    print("PASS: BracketPairColorizationManager initialization")
    print("=" * 70)


def test_colorize_brackets():
    """
    Test: Colorize brackets.
    """
    print("=" * 70)
    print("TEST: Colorize Brackets")
    print("=" * 70)
    
    manager = BracketPairColorizationManager()
    
    code = "(hello)"
    result = manager.colorize_brackets(code)
    
    assert result.success == True, "Colorization başarılı olmalı"
    assert len(result.bracket_pairs) > 0, "Bracket pairs bulunmalı"
    
    print(f"  Colorized: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Colorize brackets")
    print("=" * 70)


def test_get_bracket_pairs():
    """
    Test: Get bracket pairs.
    """
    print("=" * 70)
    print("TEST: Get Bracket Pairs")
    print("=" * 70)
    
    manager = BracketPairColorizationManager()
    
    code = "(hello)"
    manager.colorize_brackets(code)
    
    pairs = manager.get_bracket_pairs()
    
    assert len(pairs) > 0, "Bracket pairs olmalı"
    
    print(f"  Total pairs: {len(pairs)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get bracket pairs")
    print("=" * 70)


def test_get_bracket_pairs_by_type():
    """
    Test: Get bracket pairs by type.
    """
    print("=" * 70)
    print("TEST: Get Bracket Pairs by Type")
    print("=" * 70)
    
    manager = BracketPairColorizationManager()
    
    code = "(hello)"
    manager.colorize_brackets(code)
    
    pairs = manager.get_bracket_pairs_by_type(BracketType.ROUND)
    
    assert len(pairs) > 0, "Round bracket pairs olmalı"
    
    print(f"  Round pairs: {len(pairs)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get bracket pairs by type")
    print("=" * 70)


def test_get_bracket_pairs_by_color():
    """
    Test: Get bracket pairs by color.
    """
    print("=" * 70)
    print("TEST: Get Bracket Pairs by Color")
    print("=" * 70)
    
    manager = BracketPairColorizationManager()
    
    code = "(hello)"
    manager.colorize_brackets(code)
    
    pairs = manager.get_bracket_pairs()
    if pairs:
        color = pairs[0].color
        colored_pairs = manager.get_bracket_pairs_by_color(color)
        
        assert len(colored_pairs) > 0, "Colored bracket pairs olmalı"
        
        print(f"  {color.value} pairs: {len(colored_pairs)}")
    else:
        print(f"  No pairs found")
    
    print("\n" + "=" * 70)
    print("PASS: Get bracket pairs by color")
    print("=" * 70)


def test_get_matching_bracket():
    """
    Test: Get matching bracket.
    """
    print("=" * 70)
    print("TEST: Get Matching Bracket")
    print("=" * 70)
    
    manager = BracketPairColorizationManager()
    
    code = "(hello)"
    manager.colorize_brackets(code)
    
    pairs = manager.get_bracket_pairs()
    if pairs:
        opening = pairs[0].opening
        matching = manager.get_matching_bracket(opening)
        
        assert matching is not None, "Matching bracket bulunmalı"
        
        print(f"  Matching bracket found at line {matching.line}, column {matching.column}")
    else:
        print(f"  No pairs found")
    
    print("\n" + "=" * 70)
    print("PASS: Get matching bracket")
    print("=" * 70)


def test_set_color_scheme():
    """
    Test: Set color scheme.
    """
    print("=" * 70)
    print("TEST: Set Color Scheme")
    print("=" * 70)
    
    manager = BracketPairColorizationManager()
    
    result = manager.set_color_scheme("monochrome")
    
    assert result.success == True, "Set başarılı olmalı"
    
    print(f"  Color scheme: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set color scheme")
    print("=" * 70)


def test_set_custom_colors():
    """
    Test: Set custom colors.
    """
    print("=" * 70)
    print("TEST: Set Custom Colors")
    print("=" * 70)
    
    manager = BracketPairColorizationManager()
    
    colors = [BracketColor.RED, BracketColor.BLUE]
    result = manager.set_custom_colors(colors)
    
    assert result.success == True, "Set başarılı olmalı"
    
    print(f"  Custom colors: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set custom colors")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    manager = BracketPairColorizationManager()
    
    new_config = BracketPairColorConfig(max_nesting_level=20)
    result = manager.update_config(new_config)
    
    assert result.success == True, "Update başarılı olmalı"
    assert manager.config.max_nesting_level == 20, "Config güncellenmeli"
    
    print(f"  Max nesting level: {manager.config.max_nesting_level}")
    
    print("\n" + "=" * 70)
    print("PASS: Update config")
    print("=" * 70)


def test_get_config():
    """
    Test: Get config.
    """
    print("=" * 70)
    print("TEST: Get Config")
    print("=" * 70)
    
    config = BracketPairColorConfig(max_nesting_level=20)
    manager = BracketPairColorizationManager(config)
    
    retrieved_config = manager.get_config()
    
    assert retrieved_config.max_nesting_level == 20, "Config eşleşmeli"
    
    print(f"  Max nesting level: {retrieved_config.max_nesting_level}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_bracket_color_enum()
        test2 = test_bracket_type_enum()
        test3 = test_bracket_position_dataclass()
        test4 = test_bracket_pair_dataclass()
        test5 = test_bracket_pair_color_config_dataclass()
        test6 = test_bracket_pair_color_result_dataclass()
        test7 = test_bracket_pair_colorization_manager_initialization()
        test8 = test_colorize_brackets()
        test9 = test_get_bracket_pairs()
        test10 = test_get_bracket_pairs_by_type()
        test11 = test_get_bracket_pairs_by_color()
        test12 = test_get_matching_bracket()
        test13 = test_set_color_scheme()
        test14 = test_set_custom_colors()
        test15 = test_update_config()
        test16 = test_get_config()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"BracketColor Enum: {'PASS' if test1 else 'FAIL'}")
        print(f"BracketType Enum: {'PASS' if test2 else 'FAIL'}")
        print(f"BracketPosition Dataclass: {'PASS' if test3 else 'FAIL'}")
        print(f"BracketPair Dataclass: {'PASS' if test4 else 'FAIL'}")
        print(f"BracketPairColorConfig Dataclass: {'PASS' if test5 else 'FAIL'}")
        print(f"BracketPairColorResult Dataclass: {'PASS' if test6 else 'FAIL'}")
        print(f"BracketPairColorizationManager Initialization: {'PASS' if test7 else 'FAIL'}")
        print(f"Colorize Brackets: {'PASS' if test8 else 'FAIL'}")
        print(f"Get Bracket Pairs: {'PASS' if test9 else 'FAIL'}")
        print(f"Get Bracket Pairs by Type: {'PASS' if test10 else 'FAIL'}")
        print(f"Get Bracket Pairs by Color: {'PASS' if test11 else 'FAIL'}")
        print(f"Get Matching Bracket: {'PASS' if test12 else 'FAIL'}")
        print(f"Set Color Scheme: {'PASS' if test13 else 'FAIL'}")
        print(f"Set Custom Colors: {'PASS' if test14 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test15 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test16 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14, test15, test16])
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
