"""
Quality Test: Zoom
Zoom system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.zoom import (
    ZoomEngine,
    ZoomDirection,
    ZoomMode,
    ZoomConfig,
    ZoomResult
)


def test_zoom_in():
    """
    Test: Zoom in.
    """
    print("=" * 70)
    print("TEST: Zoom In")
    print("=" * 70)
    
    engine = ZoomEngine()
    
    result = engine.zoom_in()
    
    assert result.success, "Zoom başarılı olmalı"
    assert result.current_zoom > result.previous_zoom, "Zoom artmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Previous zoom: {result.previous_zoom}")
    print(f"  Current zoom: {result.current_zoom}")
    
    print("\n" + "=" * 70)
    print("PASS: Zoom in")
    print("=" * 70)


def test_zoom_out():
    """
    Test: Zoom out.
    """
    print("=" * 70)
    print("TEST: Zoom Out")
    print("=" * 70)
    
    engine = ZoomEngine()
    
    # First zoom in
    engine.zoom_in()
    
    result = engine.zoom_out()
    
    assert result.success, "Zoom başarılı olmalı"
    assert result.current_zoom < result.previous_zoom, "Zoom azalmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Previous zoom: {result.previous_zoom}")
    print(f"  Current zoom: {result.current_zoom}")
    
    print("\n" + "=" * 70)
    print("PASS: Zoom out")
    print("=" * 70)


def test_reset_zoom():
    """
    Test: Reset zoom.
    """
    print("=" * 70)
    print("TEST: Reset Zoom")
    print("=" * 70)
    
    engine = ZoomEngine()
    
    # Zoom in first
    engine.zoom_in()
    
    result = engine.reset_zoom()
    
    assert result.success, "Sıfırlama başarılı olmalı"
    assert result.current_zoom == engine.config.default_zoom, "Default zoom olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Current zoom: {result.current_zoom}")
    
    print("\n" + "=" * 70)
    print("PASS: Reset zoom")
    print("=" * 70)


def test_set_zoom():
    """
    Test: Set zoom.
    """
    print("=" * 70)
    print("TEST: Set Zoom")
    print("=" * 70)
    
    engine = ZoomEngine()
    
    result = engine.set_zoom(2.0)
    
    assert result.success, "Ayarlama başarılı olmalı"
    assert result.current_zoom == 2.0, "Zoom 2.0 olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Current zoom: {result.current_zoom}")
    
    print("\n" + "=" * 70)
    print("PASS: Set zoom")
    print("=" * 70)


def test_set_zoom_invalid():
    """
    Test: Set zoom invalid.
    """
    print("=" * 70)
    print("TEST: Set Zoom Invalid")
    print("=" * 70)
    
    engine = ZoomEngine()
    
    result = engine.set_zoom(10.0)
    
    assert result.success == False, "Başarısız olmalı"
    assert len(result.errors) > 0, "Hata olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Errors: {result.errors}")
    
    print("\n" + "=" * 70)
    print("PASS: Set zoom invalid")
    print("=" * 70)


def test_get_zoom():
    """
    Test: Get zoom.
    """
    print("=" * 70)
    print("TEST: Get Zoom")
    print("=" * 70)
    
    engine = ZoomEngine()
    
    zoom = engine.get_zoom()
    
    assert zoom == engine.config.default_zoom, "Default zoom olmalı"
    
    print(f"  Zoom: {zoom}")
    
    print("\n" + "=" * 70)
    print("PASS: Get zoom")
    print("=" * 70)


def test_get_zoom_percentage():
    """
    Test: Get zoom percentage.
    """
    print("=" * 70)
    print("TEST: Get Zoom Percentage")
    print("=" * 70)
    
    engine = ZoomEngine()
    
    percentage = engine.get_zoom_percentage()
    
    assert percentage == 100, "100% olmalı"
    
    print(f"  Percentage: {percentage}%")
    
    print("\n" + "=" * 70)
    print("PASS: Get zoom percentage")
    print("=" * 70)


def test_undo_zoom():
    """
    Test: Undo zoom.
    """
    print("=" * 70)
    print("TEST: Undo Zoom")
    print("=" * 70)
    
    engine = ZoomEngine()
    
    engine.zoom_in()
    result = engine.undo_zoom()
    
    assert result.success, "Geri alma başarılı olmalı"
    assert result.current_zoom == engine.config.default_zoom, "Default zoom olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Current zoom: {result.current_zoom}")
    
    print("\n" + "=" * 70)
    print("PASS: Undo zoom")
    print("=" * 70)


def test_get_zoom_history():
    """
    Test: Get zoom history.
    """
    print("=" * 70)
    print("TEST: Get Zoom History")
    print("=" * 70)
    
    engine = ZoomEngine()
    
    engine.zoom_in()
    history = engine.get_zoom_history()
    
    assert len(history) > 0, "Geçmiş olmalı"
    
    print(f"  History: {len(history)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get zoom history")
    print("=" * 70)


def test_clear_history():
    """
    Test: Clear history.
    """
    print("=" * 70)
    print("TEST: Clear History")
    print("=" * 70)
    
    engine = ZoomEngine()
    
    engine.zoom_in()
    result = engine.clear_history()
    
    assert result.success, "Temizleme başarılı olmalı"
    assert len(engine.get_zoom_history()) == 0, "Geçmiş temizlenmeli"
    
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
    
    engine = ZoomEngine()
    
    new_config = ZoomConfig(min_zoom=0.3, max_zoom=5.0)
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
    
    engine = ZoomEngine()
    
    config = engine.get_config()
    
    assert config is not None, "Config olmalı"
    assert config.min_zoom == 0.5, "Config eşleşmeli"
    
    print(f"  Min zoom: {config.min_zoom}")
    print(f"  Max zoom: {config.max_zoom}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


def test_can_zoom_in():
    """
    Test: Can zoom in.
    """
    print("=" * 70)
    print("TEST: Can Zoom In")
    print("=" * 70)
    
    engine = ZoomEngine()
    
    can_zoom = engine.can_zoom_in()
    
    assert can_zoom == True, "Zoom in yapılabilir olmalı"
    
    print(f"  Can zoom in: {can_zoom}")
    
    print("\n" + "=" * 70)
    print("PASS: Can zoom in")
    print("=" * 70)


def test_can_zoom_out():
    """
    Test: Can zoom out.
    """
    print("=" * 70)
    print("TEST: Can Zoom Out")
    print("=" * 70)
    
    engine = ZoomEngine()
    
    can_zoom = engine.can_zoom_out()
    
    assert can_zoom == True, "Zoom outside yapılabilir olmalı"
    
    print(f"  Can zoom out: {can_zoom}")
    
    print("\n" + "=" * 70)
    print("PASS: Can zoom out")
    print("=" * 70)


def test_get_font_size():
    """
    Test: Get font size.
    """
    print("=" * 70)
    print("TEST: Get Font Size")
    print("=" * 70)
    
    engine = ZoomEngine()
    
    font_size = engine.get_font_size(12)
    
    assert font_size == 12, "Font size 12 olmalı"
    
    print(f"  Font size: {font_size}")
    
    print("\n" + "=" * 70)
    print("PASS: Get font size")
    print("=" * 70)


def test_get_line_height():
    """
    Test: Get line height.
    """
    print("=" * 70)
    print("TEST: Get Line Height")
    print("=" * 70)
    
    engine = ZoomEngine()
    
    line_height = engine.get_line_height(20)
    
    assert line_height == 20, "Line height 20 olmalı"
    
    print(f"  Line height: {line_height}")
    
    print("\n" + "=" * 70)
    print("PASS: Get line height")
    print("=" * 70)


def test_zoom_mode_linear():
    """
    Test: Zoom mode linear.
    """
    print("=" * 70)
    print("TEST: Zoom Mode Linear")
    print("=" * 70)
    
    config = ZoomConfig(mode=ZoomMode.LINEAR)
    engine = ZoomEngine(config)
    
    result = engine.zoom_in()
    
    assert result.success, "Zoom başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Current zoom: {result.current_zoom}")
    
    print("\n" + "=" * 70)
    print("PASS: Zoom mode linear")
    print("=" * 70)


def test_zoom_mode_exponential():
    """
    Test: Zoom mode exponential.
    """
    print("=" * 70)
    print("TEST: Zoom Mode Exponential")
    print("=" * 70)
    
    config = ZoomConfig(mode=ZoomMode.EXPONENTIAL)
    engine = ZoomEngine(config)
    
    result = engine.zoom_in()
    
    assert result.success, "Zoom başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Current zoom: {result.current_zoom}")
    
    print("\n" + "=" * 70)
    print("PASS: Zoom mode exponential")
    print("=" * 70)


def test_zoom_direction_enum():
    """
    Test: ZoomDirection enum.
    """
    print("=" * 70)
    print("TEST: ZoomDirection Enum")
    print("=" * 70)
    
    assert ZoomDirection.IN.value == "in"
    assert ZoomDirection.OUT.value == "out"
    assert ZoomDirection.RESET.value == "reset"
    
    print(f"  All enum values verified")
    print(f"  Total directions: {len(ZoomDirection)}")
    
    print("\n" + "=" * 70)
    print("PASS: ZoomDirection enum")
    print("=" * 70)


def test_zoom_mode_enum():
    """
    Test: ZoomMode enum.
    """
    print("=" * 70)
    print("TEST: ZoomMode Enum")
    print("=" * 70)
    
    assert ZoomMode.LINEAR.value == "linear"
    assert ZoomMode.EXPONENTIAL.value == "exponential"
    assert ZoomMode.LOGARITHMIC.value == "logarithmic"
    
    print(f"  All enum values verified")
    print(f"  Total modes: {len(ZoomMode)}")
    
    print("\n" + "=" * 70)
    print("PASS: ZoomMode enum")
    print("=" * 70)


def test_zoom_config_dataclass():
    """
    Test: ZoomConfig dataclass.
    """
    print("=" * 70)
    print("TEST: ZoomConfig Dataclass")
    print("=" * 70)
    
    config = ZoomConfig(
        min_zoom=0.5,
        max_zoom=3.0,
        default_zoom=1.0,
        zoom_step=0.1
    )
    
    assert config.min_zoom == 0.5, "Min zoom eşleşmeli"
    assert config.max_zoom == 3.0, "Max zoom eşleşmeli"
    assert config.default_zoom == 1.0, "Default zoom eşleşmeli"
    
    print(f"  Min zoom: {config.min_zoom}")
    print(f"  Max zoom: {config.max_zoom}")
    print(f"  Default zoom: {config.default_zoom}")
    
    print("\n" + "=" * 70)
    print("PASS: ZoomConfig dataclass")
    print("=" * 70)


def test_zoom_result_dataclass():
    """
    Test: ZoomResult dataclass.
    """
    print("=" * 70)
    print("TEST: ZoomResult Dataclass")
    print("=" * 70)
    
    result = ZoomResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: ZoomResult dataclass")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_zoom_in()
        test2 = test_zoom_out()
        test3 = test_reset_zoom()
        test4 = test_set_zoom()
        test5 = test_set_zoom_invalid()
        test6 = test_get_zoom()
        test7 = test_get_zoom_percentage()
        test8 = test_undo_zoom()
        test9 = test_get_zoom_history()
        test10 = test_clear_history()
        test11 = test_update_config()
        test12 = test_get_config()
        test13 = test_can_zoom_in()
        test14 = test_can_zoom_out()
        test15 = test_get_font_size()
        test16 = test_get_line_height()
        test17 = test_zoom_mode_linear()
        test18 = test_zoom_mode_exponential()
        test19 = test_zoom_direction_enum()
        test20 = test_zoom_mode_enum()
        test21 = test_zoom_config_dataclass()
        test22 = test_zoom_result_dataclass()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Zoom In: {'PASS' if test1 else 'FAIL'}")
        print(f"Zoom Out: {'PASS' if test2 else 'FAIL'}")
        print(f"Reset Zoom: {'PASS' if test3 else 'FAIL'}")
        print(f"Set Zoom: {'PASS' if test4 else 'FAIL'}")
        print(f"Set Zoom Invalid: {'PASS' if test5 else 'FAIL'}")
        print(f"Get Zoom: {'PASS' if test6 else 'FAIL'}")
        print(f"Get Zoom Percentage: {'PASS' if test7 else 'FAIL'}")
        print(f"Undo Zoom: {'PASS' if test8 else 'FAIL'}")
        print(f"Get Zoom History: {'PASS' if test9 else 'FAIL'}")
        print(f"Clear History: {'PASS' if test10 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test11 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test12 else 'FAIL'}")
        print(f"Can Zoom In: {'PASS' if test13 else 'FAIL'}")
        print(f"Can Zoom Out: {'PASS' if test14 else 'FAIL'}")
        print(f"Get Font Size: {'PASS' if test15 else 'FAIL'}")
        print(f"Get Line Height: {'PASS' if test16 else 'FAIL'}")
        print(f"Zoom Mode Linear: {'PASS' if test17 else 'FAIL'}")
        print(f"Zoom Mode Exponential: {'PASS' if test18 else 'FAIL'}")
        print(f"ZoomDirection Enum: {'PASS' if test19 else 'FAIL'}")
        print(f"ZoomMode Enum: {'PASS' if test20 else 'FAIL'}")
        print(f"ZoomConfig Dataclass: {'PASS' if test21 else 'FAIL'}")
        print(f"ZoomResult Dataclass: {'PASS' if test22 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14, test15, test16, test17, test18, test19, test20, test21, test22])
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
