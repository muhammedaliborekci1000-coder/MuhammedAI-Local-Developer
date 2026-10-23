"""
Quality Test: Terminal Resize
Terminal resize system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.tools.terminal_resize import (
    TerminalResizeEngine,
    ResizeMode,
    ResizeDirection,
    ResizePreset,
    ResizeConfig,
    ResizeResult
)


def test_resize():
    """
    Test: Resize.
    """
    print("=" * 70)
    print("TEST: Resize")
    print("=" * 70)
    
    engine = TerminalResizeEngine()
    result = engine.resize(1000, 700)
    
    assert result.success, "Yeniden boyutlandırma başarılı olmalı"
    assert result.width == 1000, "Genişlik eşleşmeli"
    assert result.height == 700, "Yükseklik eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Width: {result.width}")
    print(f"  Height: {result.height}")
    
    print("\n" + "=" * 70)
    print("PASS: Resize")
    print("=" * 70)


def test_resize_with_mode():
    """
    Test: Resize with mode.
    """
    print("=" * 70)
    print("TEST: Resize With Mode")
    print("=" * 70)
    
    engine = TerminalResizeEngine()
    result = engine.resize(1000, 700, ResizeMode.AUTO)
    
    assert result.success, "Yeniden boyutlandırma başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Resize with mode")
    print("=" * 70)


def test_resize_horizontal():
    """
    Test: Resize horizontal.
    """
    print("=" * 70)
    print("TEST: Resize Horizontal")
    print("=" * 70)
    
    engine = TerminalResizeEngine()
    result = engine.resize_horizontal(1200)
    
    assert result.success, "Yeniden boyutlandırma başarılı olmalı"
    assert result.width == 1200, "Genişlik eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Width: {result.width}")
    
    print("\n" + "=" * 70)
    print("PASS: Resize horizontal")
    print("=" * 70)


def test_resize_vertical():
    """
    Test: Resize vertical.
    """
    print("=" * 70)
    print("TEST: Resize Vertical")
    print("=" * 70)
    
    engine = TerminalResizeEngine()
    result = engine.resize_vertical(800)
    
    assert result.success, "Yeniden boyutlandırma başarılı olmalı"
    assert result.height == 800, "Yükseklik eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Height: {result.height}")
    
    print("\n" + "=" * 70)
    print("PASS: Resize vertical")
    print("=" * 70)


def test_apply_preset():
    """
    Test: Apply preset.
    """
    print("=" * 70)
    print("TEST: Apply Preset")
    print("=" * 70)
    
    engine = TerminalResizeEngine()
    result = engine.apply_preset(ResizePreset.LARGE)
    
    assert result.success, "Ön ayar uygulama başarılı olmalı"
    assert result.width == 1200, "Genişlik eşleşmeli"
    assert result.height == 800, "Yükseklik eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Width: {result.width}")
    print(f"  Height: {result.height}")
    
    print("\n" + "=" * 70)
    print("PASS: Apply preset")
    print("=" * 70)


def test_fit_to_content():
    """
    Test: Fit to content.
    """
    print("=" * 70)
    print("TEST: Fit To Content")
    print("=" * 70)
    
    engine = TerminalResizeEngine()
    result = engine.fit_to_content()
    
    assert result.success, "Sığdırma başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Fit to content")
    print("=" * 70)


def test_undo_resize():
    """
    Test: Undo resize.
    """
    print("=" * 70)
    print("TEST: Undo Resize")
    print("=" * 70)
    
    engine = TerminalResizeEngine()
    engine.resize(1000, 700)
    
    result = engine.undo_resize()
    
    assert result.success, "Geri alma başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Undo resize")
    print("=" * 70)


def test_get_current_size():
    """
    Test: Get current size.
    """
    print("=" * 70)
    print("TEST: Get Current Size")
    print("=" * 70)
    
    engine = TerminalResizeEngine()
    engine.resize(1000, 700)
    
    width, height = engine.get_current_size()
    
    assert width == 1000, "Genişlik eşleşmeli"
    assert height == 700, "Yükseklik eşleşmeli"
    
    print(f"  Width: {width}")
    print(f"  Height: {height}")
    
    print("\n" + "=" * 70)
    print("PASS: Get current size")
    print("=" * 70)


def test_get_resize_history():
    """
    Test: Get resize history.
    """
    print("=" * 70)
    print("TEST: Get Resize History")
    print("=" * 70)
    
    engine = TerminalResizeEngine()
    engine.resize(1000, 700)
    
    history = engine.get_resize_history()
    
    assert len(history) > 0, "Geçmiş olmalı"
    
    print(f"  History: {len(history)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get resize history")
    print("=" * 70)


def test_clear_history():
    """
    Test: Clear history.
    """
    print("=" * 70)
    print("TEST: Clear History")
    print("=" * 70)
    
    engine = TerminalResizeEngine()
    engine.resize(1000, 700)
    
    result = engine.clear_history()
    
    assert result.success, "Temizleme başarılı olmalı"
    assert len(engine.get_resize_history()) == 0, "Geçmiş temizlenmeli"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear history")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    engine = TerminalResizeEngine()
    
    new_config = ResizeConfig(min_width=500, min_height=400)
    result = engine.update_config(new_config)
    
    assert result.success, "Güncelleme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    
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
    
    engine = TerminalResizeEngine()
    
    config = engine.get_config()
    
    assert config is not None, "Config olmalı"
    assert config.min_width == 400, "Config eşleşmeli"
    
    print(f"  Min width: {config.min_width}")
    print(f"  Min height: {config.min_height}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


def test_resize_mode_enum():
    """
    Test: ResizeMode enum.
    """
    print("=" * 70)
    print("TEST: ResizeMode Enum")
    print("=" * 70)
    
    assert ResizeMode.MANUAL.value == "manual"
    assert ResizeMode.AUTO.value == "auto"
    assert ResizeMode.PRESET.value == "preset"
    assert ResizeMode.FIT.value == "fit"
    
    print(f"  All enum values verified")
    print(f"  Total modes: {len(ResizeMode)}")
    
    print("\n" + "=" * 70)
    print("PASS: ResizeMode enum")
    print("=" * 70)


def test_resize_direction_enum():
    """
    Test: ResizeDirection enum.
    """
    print("=" * 70)
    print("TEST: ResizeDirection Enum")
    print("=" * 70)
    
    assert ResizeDirection.HORIZONTAL.value == "horizontal"
    assert ResizeDirection.VERTICAL.value == "vertical"
    assert ResizeDirection.BOTH.value == "both"
    
    print(f"  All enum values verified")
    print(f"  Total directions: {len(ResizeDirection)}")
    
    print("\n" + "=" * 70)
    print("PASS: ResizeDirection enum")
    print("=" * 70)


def test_resize_preset_enum():
    """
    Test: ResizePreset enum.
    """
    print("=" * 70)
    print("TEST: ResizePreset Enum")
    print("=" * 70)
    
    assert ResizePreset.SMALL.value == "small"
    assert ResizePreset.MEDIUM.value == "medium"
    assert ResizePreset.LARGE.value == "large"
    assert ResizePreset.FULLSCREEN.value == "fullscreen"
    assert ResizePreset.HALF.value == "half"
    assert ResizePreset.QUARTER.value == "quarter"
    
    print(f"  All enum values verified")
    print(f"  Total presets: {len(ResizePreset)}")
    
    print("\n" + "=" * 70)
    print("PASS: ResizePreset enum")
    print("=" * 70)


def test_resize_config_dataclass():
    """
    Test: ResizeConfig dataclass.
    """
    print("=" * 70)
    print("TEST: ResizeConfig Dataclass")
    print("=" * 70)
    
    config = ResizeConfig(
        min_width=500,
        min_height=400,
        max_width=1600,
        max_height=900
    )
    
    assert config.min_width == 500, "Min width eşleşmeli"
    assert config.min_height == 400, "Min height eşleşmeli"
    
    print(f"  Min width: {config.min_width}")
    print(f"  Min height: {config.min_height}")
    
    print("\n" + "=" * 70)
    print("PASS: ResizeConfig dataclass")
    print("=" * 70)


def test_resize_result_dataclass():
    """
    Test: ResizeResult dataclass.
    """
    print("=" * 70)
    print("TEST: ResizeResult Dataclass")
    print("=" * 70)
    
    result = ResizeResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: ResizeResult dataclass")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_resize()
        test2 = test_resize_with_mode()
        test3 = test_resize_horizontal()
        test4 = test_resize_vertical()
        test5 = test_apply_preset()
        test6 = test_fit_to_content()
        test7 = test_undo_resize()
        test8 = test_get_current_size()
        test9 = test_get_resize_history()
        test10 = test_clear_history()
        test11 = test_update_config()
        test12 = test_get_config()
        test13 = test_resize_mode_enum()
        test14 = test_resize_direction_enum()
        test15 = test_resize_preset_enum()
        test16 = test_resize_config_dataclass()
        test17 = test_resize_result_dataclass()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Resize: {'PASS' if test1 else 'FAIL'}")
        print(f"Resize With Mode: {'PASS' if test2 else 'FAIL'}")
        print(f"Resize Horizontal: {'PASS' if test3 else 'FAIL'}")
        print(f"Resize Vertical: {'PASS' if test4 else 'FAIL'}")
        print(f"Apply Preset: {'PASS' if test5 else 'FAIL'}")
        print(f"Fit To Content: {'PASS' if test6 else 'FAIL'}")
        print(f"Undo Resize: {'PASS' if test7 else 'FAIL'}")
        print(f"Get Current Size: {'PASS' if test8 else 'FAIL'}")
        print(f"Get Resize History: {'PASS' if test9 else 'FAIL'}")
        print(f"Clear History: {'PASS' if test10 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test11 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test12 else 'FAIL'}")
        print(f"ResizeMode Enum: {'PASS' if test13 else 'FAIL'}")
        print(f"ResizeDirection Enum: {'PASS' if test14 else 'FAIL'}")
        print(f"ResizePreset Enum: {'PASS' if test15 else 'FAIL'}")
        print(f"ResizeConfig Dataclass: {'PASS' if test16 else 'FAIL'}")
        print(f"ResizeResult Dataclass: {'PASS' if test17 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14, test15, test16, test17])
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
