"""
Quality Test: Parameter Hints
Parameter hints system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.parameter_hints import (
    ParameterHintsEngine,
    HintDisplayMode,
    HintTriggerMode,
    ParameterHint,
    HintsConfig,
    HintsResult
)


def test_get_hints():
    """
    Test: Get hints.
    """
    print("=" * 70)
    print("TEST: Get Hints")
    print("=" * 70)
    
    engine = ParameterHintsEngine()
    
    result = engine.get_hints("print")
    
    assert result.success, "Hint alma başarılı olmalı"
    assert result.total_hints > 0, "Hint olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Total hints: {result.total_hints}")
    
    print("\n" + "=" * 70)
    print("PASS: Get hints")
    print("=" * 70)


def test_update_active_hint():
    """
    Test: Update active hint.
    """
    print("=" * 70)
    print("TEST: Update Active Hint")
    print("=" * 70)
    
    engine = ParameterHintsEngine()
    
    engine.get_hints("print")
    result = engine.update_active_hint(1)
    
    assert result.success, "Hint güncelleme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Active hint: {result.active_hint.name if result.active_hint else None}")
    
    print("\n" + "=" * 70)
    print("PASS: Update active hint")
    print("=" * 70)


def test_hide_hints():
    """
    Test: Hide hints.
    """
    print("=" * 70)
    print("TEST: Hide Hints")
    print("=" * 70)
    
    engine = ParameterHintsEngine()
    
    engine.get_hints("print")
    result = engine.hide_hints()
    
    assert result.success, "Gizleme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Hide hints")
    print("=" * 70)


def test_clear_cache():
    """
    Test: Clear cache.
    """
    print("=" * 70)
    print("TEST: Clear Cache")
    print("=" * 70)
    
    engine = ParameterHintsEngine()
    
    engine.get_hints("print")
    result = engine.clear_cache()
    
    assert result.success, "Cache temizleme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear cache")
    print("=" * 70)


def test_get_current_hints():
    """
    Test: Get current hints.
    """
    print("=" * 70)
    print("TEST: Get Current Hints")
    print("=" * 70)
    
    engine = ParameterHintsEngine()
    
    engine.get_hints("print")
    hints = engine.get_current_hints()
    
    assert len(hints) > 0, "Hintler olmalı"
    
    print(f"  Current hints: {len(hints)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get current hints")
    print("=" * 70)


def test_get_hint_count():
    """
    Test: Get hint count.
    """
    print("=" * 70)
    print("TEST: Get Hint Count")
    print("=" * 70)
    
    engine = ParameterHintsEngine()
    
    engine.get_hints("print")
    count = engine.get_hint_count()
    
    assert count > 0, "Hint sayısı 0'dan büyük olmalı"
    
    print(f"  Hint count: {count}")
    
    print("\n" + "=" * 70)
    print("PASS: Get hint count")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    engine = ParameterHintsEngine()
    
    new_config = HintsConfig(display_mode=HintDisplayMode.TOOLTIP)
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
    
    engine = ParameterHintsEngine()
    
    config = engine.get_config()
    
    assert config is not None, "Config olmalı"
    assert config.display_mode == HintDisplayMode.INLINE, "Config eşleşmeli"
    
    print(f"  Display mode: {config.display_mode.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


def test_hint_display_mode_enum():
    """
    Test: HintDisplayMode enum.
    """
    print("=" * 70)
    print("TEST: HintDisplayMode Enum")
    print("=" * 70)
    
    assert HintDisplayMode.INLINE.value == "inline"
    assert HintDisplayMode.ABOVE.value == "above"
    assert HintDisplayMode.BELOW.value == "below"
    assert HintDisplayMode.TOOLTIP.value == "tooltip"
    
    print(f"  All enum values verified")
    print(f"  Total modes: {len(HintDisplayMode)}")
    
    print("\n" + "=" * 70)
    print("PASS: HintDisplayMode enum")
    print("=" * 70)


def test_hint_trigger_mode_enum():
    """
    Test: HintTriggerMode enum.
    """
    print("=" * 70)
    print("TEST: HintTriggerMode Enum")
    print("=" * 70)
    
    assert HintTriggerMode.AUTO.value == "auto"
    assert HintTriggerMode.MANUAL.value == "manual"
    assert HintTriggerMode.ON_TYPE.value == "on_type"
    
    print(f"  All enum values verified")
    print(f"  Total modes: {len(HintTriggerMode)}")
    
    print("\n" + "=" * 70)
    print("PASS: HintTriggerMode enum")
    print("=" * 70)


def test_parameter_hint_dataclass():
    """
    Test: ParameterHint dataclass.
    """
    print("=" * 70)
    print("TEST: ParameterHint Dataclass")
    print("=" * 70)
    
    hint = ParameterHint(
        name="param1",
        type_hint="str",
        position=0
    )
    
    assert hint.name == "param1", "Name eşleşmeli"
    assert hint.type_hint == "str", "Type hint eşleşmeli"
    assert hint.is_active == False, "Is active eşleşmeli"
    
    print(f"  Name: {hint.name}")
    print(f"  Type hint: {hint.type_hint}")
    print(f"  Is active: {hint.is_active}")
    
    print("\n" + "=" * 70)
    print("PASS: ParameterHint dataclass")
    print("=" * 70)


def test_hints_config_dataclass():
    """
    Test: HintsConfig dataclass.
    """
    print("=" * 70)
    print("TEST: HintsConfig Dataclass")
    print("=" * 70)
    
    config = HintsConfig(
        display_mode=HintDisplayMode.INLINE,
        show_type_hints=True,
        show_default_values=True
    )
    
    assert config.display_mode == HintDisplayMode.INLINE, "Display mode eşleşmeli"
    assert config.show_type_hints == True, "Show type hints eşleşmeli"
    assert config.show_default_values == True, "Show default values eşleşmeli"
    
    print(f"  Display mode: {config.display_mode.value}")
    print(f"  Show type hints: {config.show_type_hints}")
    print(f"  Show default values: {config.show_default_values}")
    
    print("\n" + "=" * 70)
    print("PASS: HintsConfig dataclass")
    print("=" * 70)


def test_hints_result_dataclass():
    """
    Test: HintsResult dataclass.
    """
    print("=" * 70)
    print("TEST: HintsResult Dataclass")
    print("=" * 70)
    
    result = HintsResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.hints, list), "Hints list olmalı"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Hints: {len(result.hints)}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: HintsResult dataclass")
    print("=" * 70)


def test_cache_functionality():
    """
    Test: Cache functionality.
    """
    print("=" * 70)
    print("TEST: Cache Functionality")
    print("=" * 70)
    
    engine = ParameterHintsEngine()
    
    # İlk çağrı
    result1 = engine.get_hints("print")
    assert result1.success, "İlk çağrı başarılı olmalı"
    
    # İkinci çağrı (cache'den)
    result2 = engine.get_hints("print")
    assert result2.success, "Cache'den alma başarılı olmalı"
    
    print(f"  First call: {result1.message}")
    print(f"  Second call: {result2.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Cache functionality")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_get_hints()
        test2 = test_update_active_hint()
        test3 = test_hide_hints()
        test4 = test_clear_cache()
        test5 = test_get_current_hints()
        test6 = test_get_hint_count()
        test7 = test_update_config()
        test8 = test_get_config()
        test9 = test_hint_display_mode_enum()
        test10 = test_hint_trigger_mode_enum()
        test11 = test_parameter_hint_dataclass()
        test12 = test_hints_config_dataclass()
        test13 = test_hints_result_dataclass()
        test14 = test_cache_functionality()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Get Hints: {'PASS' if test1 else 'FAIL'}")
        print(f"Update Active Hint: {'PASS' if test2 else 'FAIL'}")
        print(f"Hide Hints: {'PASS' if test3 else 'FAIL'}")
        print(f"Clear Cache: {'PASS' if test4 else 'FAIL'}")
        print(f"Get Current Hints: {'PASS' if test5 else 'FAIL'}")
        print(f"Get Hint Count: {'PASS' if test6 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test7 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test8 else 'FAIL'}")
        print(f"HintDisplayMode Enum: {'PASS' if test9 else 'FAIL'}")
        print(f"HintTriggerMode Enum: {'PASS' if test10 else 'FAIL'}")
        print(f"ParameterHint Dataclass: {'PASS' if test11 else 'FAIL'}")
        print(f"HintsConfig Dataclass: {'PASS' if test12 else 'FAIL'}")
        print(f"HintsResult Dataclass: {'PASS' if test13 else 'FAIL'}")
        print(f"Cache Functionality: {'PASS' if test14 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14])
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
