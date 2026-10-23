"""
Quality Test: Scrollbar
Scrollbar system testleri.
"""

import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from app.editor.scrollbar import (
    ScrollbarPosition,
    ScrollbarStyle,
    ScrollbarState,
    ScrollbarConfig,
    ScrollbarResult,
    ScrollbarManager
)


def test_scrollbar_position_enum():
    """
    Test: ScrollbarPosition enum.
    """
    print("=" * 70)
    print("TEST: ScrollbarPosition Enum")
    print("=" * 70)
    
    assert ScrollbarPosition.VERTICAL.value == "vertical"
    assert ScrollbarPosition.HORIZONTAL.value == "horizontal"
    assert ScrollbarPosition.BOTH.value == "both"
    
    print(f"  All enum values verified")
    print(f"  Total positions: {len(ScrollbarPosition)}")
    
    print("\n" + "=" * 70)
    print("PASS: ScrollbarPosition enum")
    print("=" * 70)


def test_scrollbar_style_enum():
    """
    Test: ScrollbarStyle enum.
    """
    print("=" * 70)
    print("TEST: ScrollbarStyle Enum")
    print("=" * 70)
    
    assert ScrollbarStyle.CLASSIC.value == "classic"
    assert ScrollbarStyle.MODERN.value == "modern"
    assert ScrollbarStyle.MINIMAL.value == "minimal"
    assert ScrollbarStyle.CUSTOM.value == "custom"
    
    print(f"  All enum values verified")
    print(f"  Total styles: {len(ScrollbarStyle)}")
    
    print("\n" + "=" * 70)
    print("PASS: ScrollbarStyle enum")
    print("=" * 70)


def test_scrollbar_state_dataclass():
    """
    Test: ScrollbarState dataclass.
    """
    print("=" * 70)
    print("TEST: ScrollbarState Dataclass")
    print("=" * 70)
    
    state = ScrollbarState(
        position=0.0,
        minimum=0.0,
        maximum=100.0
    )
    
    assert state.position == 0.0, "Position eşleşmeli"
    assert state.minimum == 0.0, "Minimum eşleşmeli"
    assert state.maximum == 100.0, "Maximum eşleşmeli"
    
    print(f"  Position: {state.position}")
    print(f"  Minimum: {state.minimum}")
    print(f"  Maximum: {state.maximum}")
    
    print("\n" + "=" * 70)
    print("PASS: ScrollbarState dataclass")
    print("=" * 70)


def test_scrollbar_config_dataclass():
    """
    Test: ScrollbarConfig dataclass.
    """
    print("=" * 70)
    print("TEST: ScrollbarConfig Dataclass")
    print("=" * 70)
    
    config = ScrollbarConfig(
        position=ScrollbarPosition.BOTH,
        style=ScrollbarStyle.MODERN
    )
    
    assert config.position == ScrollbarPosition.BOTH, "Position eşleşmeli"
    assert config.style == ScrollbarStyle.MODERN, "Style eşleşmeli"
    
    print(f"  Position: {config.position.value}")
    print(f"  Style: {config.style.value}")
    
    print("\n" + "=" * 70)
    print("PASS: ScrollbarConfig dataclass")
    print("=" * 70)


def test_scrollbar_result_dataclass():
    """
    Test: ScrollbarResult dataclass.
    """
    print("=" * 70)
    print("TEST: ScrollbarResult Dataclass")
    print("=" * 70)
    
    result = ScrollbarResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: ScrollbarResult dataclass")
    print("=" * 70)


def test_scrollbar_manager_initialization():
    """
    Test: ScrollbarManager initialization.
    """
    print("=" * 70)
    print("TEST: ScrollbarManager Initialization")
    print("=" * 70)
    
    config = ScrollbarConfig()
    manager = ScrollbarManager(config)
    
    assert manager.config == config, "Config eşleşmeli"
    assert manager.vertical_state is not None, "Vertical state olmalı"
    assert manager.horizontal_state is not None, "Horizontal state olmalı"
    
    print(f"  Vertical state: {manager.vertical_state.position}")
    print(f"  Horizontal state: {manager.horizontal_state.position}")
    
    print("\n" + "=" * 70)
    print("PASS: ScrollbarManager initialization")
    print("=" * 70)


def test_scroll_to():
    """
    Test: Scroll to position.
    """
    print("=" * 70)
    print("TEST: Scroll To Position")
    print("=" * 70)
    
    manager = ScrollbarManager()
    
    result = manager.scroll_to(50.0)
    
    assert result.success == True, "Scroll başarılı olmalı"
    assert result.state.position == 50.0, "Position eşleşmeli"
    
    print(f"  Scrolled: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Scroll to position")
    print("=" * 70)


def test_scroll_by():
    """
    Test: Scroll by delta.
    """
    print("=" * 70)
    print("TEST: Scroll By Delta")
    print("=" * 70)
    
    manager = ScrollbarManager()
    
    result = manager.scroll_by(10.0)
    
    assert result.success == True, "Scroll başarılı olmalı"
    
    print(f"  Scrolled: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Scroll by delta")
    print("=" * 70)


def test_scroll_to_top():
    """
    Test: Scroll to top.
    """
    print("=" * 70)
    print("TEST: Scroll To Top")
    print("=" * 70)
    
    manager = ScrollbarManager()
    
    result = manager.scroll_to_top()
    
    assert result.success == True, "Scroll başarılı olmalı"
    
    print(f"  Scrolled: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Scroll to top")
    print("=" * 70)


def test_scroll_to_bottom():
    """
    Test: Scroll to bottom.
    """
    print("=" * 70)
    print("TEST: Scroll To Bottom")
    print("=" * 70)
    
    manager = ScrollbarManager()
    
    result = manager.scroll_to_bottom()
    
    assert result.success == True, "Scroll başarılı olmalı"
    
    print(f"  Scrolled: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Scroll to bottom")
    print("=" * 70)


def test_scroll_to_left():
    """
    Test: Scroll to left.
    """
    print("=" * 70)
    print("TEST: Scroll To Left")
    print("=" * 70)
    
    manager = ScrollbarManager()
    
    result = manager.scroll_to_left()
    
    assert result.success == True, "Scroll başarılı olmalı"
    
    print(f"  Scrolled: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Scroll to left")
    print("=" * 70)


def test_scroll_to_right():
    """
    Test: Scroll to right.
    """
    print("=" * 70)
    print("TEST: Scroll To Right")
    print("=" * 70)
    
    manager = ScrollbarManager()
    
    result = manager.scroll_to_right()
    
    assert result.success == True, "Scroll başarılı olmalı"
    
    print(f"  Scrolled: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Scroll to right")
    print("=" * 70)


def test_page_up():
    """
    Test: Page up.
    """
    print("=" * 70)
    print("TEST: Page Up")
    print("=" * 70)
    
    manager = ScrollbarManager()
    
    result = manager.page_up()
    
    assert result.success == True, "Page up başarılı olmalı"
    
    print(f"  Page up: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Page up")
    print("=" * 70)


def test_page_down():
    """
    Test: Page down.
    """
    print("=" * 70)
    print("TEST: Page Down")
    print("=" * 70)
    
    manager = ScrollbarManager()
    
    result = manager.page_down()
    
    assert result.success == True, "Page down başarılı olmalı"
    
    print(f"  Page down: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Page down")
    print("=" * 70)


def test_line_up():
    """
    Test: Line up.
    """
    print("=" * 70)
    print("TEST: Line Up")
    print("=" * 70)
    
    manager = ScrollbarManager()
    
    result = manager.line_up()
    
    assert result.success == True, "Line up başarılı olmalı"
    
    print(f"  Line up: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Line up")
    print("=" * 70)


def test_line_down():
    """
    Test: Line down.
    """
    print("=" * 70)
    print("TEST: Line Down")
    print("=" * 70)
    
    manager = ScrollbarManager()
    
    result = manager.line_down()
    
    assert result.success == True, "Line down başarılı olmalı"
    
    print(f"  Line down: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Line down")
    print("=" * 70)


def test_get_state():
    """
    Test: Get state.
    """
    print("=" * 70)
    print("TEST: Get State")
    print("=" * 70)
    
    manager = ScrollbarManager()
    
    state = manager.get_state()
    
    assert state is not None, "State bulunmalı"
    
    print(f"  Position: {state.position}")
    
    print("\n" + "=" * 70)
    print("PASS: Get state")
    print("=" * 70)


def test_set_range():
    """
    Test: Set range.
    """
    print("=" * 70)
    print("TEST: Set Range")
    print("=" * 70)
    
    manager = ScrollbarManager()
    
    result = manager.set_range(0.0, 200.0)
    
    assert result.success == True, "Set range başarılı olmalı"
    
    print(f"  Range set: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set range")
    print("=" * 70)


def test_set_page_size():
    """
    Test: Set page size.
    """
    print("=" * 70)
    print("TEST: Set Page Size")
    print("=" * 70)
    
    manager = ScrollbarManager()
    
    result = manager.set_page_size(20.0)
    
    assert result.success == True, "Set page size başarılı olmalı"
    
    print(f"  Page size set: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set page size")
    print("=" * 70)


def test_set_step_size():
    """
    Test: Set step size.
    """
    print("=" * 70)
    print("TEST: Set Step Size")
    print("=" * 70)
    
    manager = ScrollbarManager()
    
    result = manager.set_step_size(2.0)
    
    assert result.success == True, "Set step size başarılı olmalı"
    
    print(f"  Step size set: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set step size")
    print("=" * 70)


def test_get_thumb_position():
    """
    Test: Get thumb position.
    """
    print("=" * 70)
    print("TEST: Get Thumb Position")
    print("=" * 70)
    
    manager = ScrollbarManager()
    
    manager.scroll_to(50.0)
    thumb_pos = manager.get_thumb_position()
    
    assert 0.0 <= thumb_pos <= 1.0, "Thumb position 0-1 arası olmalı"
    
    print(f"  Thumb position: {thumb_pos}")
    
    print("\n" + "=" * 70)
    print("PASS: Get thumb position")
    print("=" * 70)


def test_get_thumb_size():
    """
    Test: Get thumb size.
    """
    print("=" * 70)
    print("TEST: Get Thumb Size")
    print("=" * 70)
    
    manager = ScrollbarManager()
    
    thumb_size = manager.get_thumb_size()
    
    assert 0.0 <= thumb_size <= 1.0, "Thumb size 0-1 arası olmalı"
    
    print(f"  Thumb size: {thumb_size}")
    
    print("\n" + "=" * 70)
    print("PASS: Get thumb size")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    manager = ScrollbarManager()
    
    new_config = ScrollbarConfig(scroll_speed=2.0)
    result = manager.update_config(new_config)
    
    assert result.success == True, "Update başarılı olmalı"
    assert manager.config.scroll_speed == 2.0, "Config güncellenmeli"
    
    print(f"  Scroll speed: {manager.config.scroll_speed}")
    
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
    
    config = ScrollbarConfig(scroll_speed=2.0)
    manager = ScrollbarManager(config)
    
    retrieved_config = manager.get_config()
    
    assert retrieved_config.scroll_speed == 2.0, "Config eşleşmeli"
    
    print(f"  Scroll speed: {retrieved_config.scroll_speed}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_scrollbar_position_enum()
        test2 = test_scrollbar_style_enum()
        test3 = test_scrollbar_state_dataclass()
        test4 = test_scrollbar_config_dataclass()
        test5 = test_scrollbar_result_dataclass()
        test6 = test_scrollbar_manager_initialization()
        test7 = test_scroll_to()
        test8 = test_scroll_by()
        test9 = test_scroll_to_top()
        test10 = test_scroll_to_bottom()
        test11 = test_scroll_to_left()
        test12 = test_scroll_to_right()
        test13 = test_page_up()
        test14 = test_page_down()
        test15 = test_line_up()
        test16 = test_line_down()
        test17 = test_get_state()
        test18 = test_set_range()
        test19 = test_set_page_size()
        test20 = test_set_step_size()
        test21 = test_get_thumb_position()
        test22 = test_get_thumb_size()
        test23 = test_update_config()
        test24 = test_get_config()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"ScrollbarPosition Enum: {'PASS' if test1 else 'FAIL'}")
        print(f"ScrollbarStyle Enum: {'PASS' if test2 else 'FAIL'}")
        print(f"ScrollbarState Dataclass: {'PASS' if test3 else 'FAIL'}")
        print(f"ScrollbarConfig Dataclass: {'PASS' if test4 else 'FAIL'}")
        print(f"ScrollbarResult Dataclass: {'PASS' if test5 else 'FAIL'}")
        print(f"ScrollbarManager Initialization: {'PASS' if test6 else 'FAIL'}")
        print(f"Scroll To: {'PASS' if test7 else 'FAIL'}")
        print(f"Scroll By: {'PASS' if test8 else 'FAIL'}")
        print(f"Scroll To Top: {'PASS' if test9 else 'FAIL'}")
        print(f"Scroll To Bottom: {'PASS' if test10 else 'FAIL'}")
        print(f"Scroll To Left: {'PASS' if test11 else 'FAIL'}")
        print(f"Scroll To Right: {'PASS' if test12 else 'FAIL'}")
        print(f"Page Up: {'PASS' if test13 else 'FAIL'}")
        print(f"Page Down: {'PASS' if test14 else 'FAIL'}")
        print(f"Line Up: {'PASS' if test15 else 'FAIL'}")
        print(f"Line Down: {'PASS' if test16 else 'FAIL'}")
        print(f"Get State: {'PASS' if test17 else 'FAIL'}")
        print(f"Set Range: {'PASS' if test18 else 'FAIL'}")
        print(f"Set Page Size: {'PASS' if test19 else 'FAIL'}")
        print(f"Set Step Size: {'PASS' if test20 else 'FAIL'}")
        print(f"Get Thumb Position: {'PASS' if test21 else 'FAIL'}")
        print(f"Get Thumb Size: {'PASS' if test22 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test23 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test24 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14, test15, test16, test17, test18, test19, test20, test21, test22, test23, test24])
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
