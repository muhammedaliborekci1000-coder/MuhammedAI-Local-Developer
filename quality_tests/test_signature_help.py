"""
Quality Test: Signature Help
Signature help system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.signature_help import (
    SignatureHelpEngine,
    SignatureTriggerMode,
    ParameterType,
    Parameter,
    FunctionSignature,
    SignatureConfig,
    SignatureResult
)


def test_get_signature():
    """
    Test: Get signature.
    """
    print("=" * 70)
    print("TEST: Get Signature")
    print("=" * 70)
    
    engine = SignatureHelpEngine()
    
    result = engine.get_signature("print")
    
    assert result.success, "İmza alma başarılı olmalı"
    assert result.total_signatures > 0, "İmza olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Total signatures: {result.total_signatures}")
    
    print("\n" + "=" * 70)
    print("PASS: Get signature")
    print("=" * 70)


def test_update_active_parameter():
    """
    Test: Update active parameter.
    """
    print("=" * 70)
    print("TEST: Update Active Parameter")
    print("=" * 70)
    
    engine = SignatureHelpEngine()
    
    engine.get_signature("print")
    result = engine.update_active_parameter(1)
    
    assert result.success, "Parametre güncelleme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Active parameter: {result.active_parameter}")
    
    print("\n" + "=" * 70)
    print("PASS: Update active parameter")
    print("=" * 70)


def test_next_signature():
    """
    Test: Next signature.
    """
    print("=" * 70)
    print("TEST: Next Signature")
    print("=" * 70)
    
    engine = SignatureHelpEngine()
    
    engine.get_signature("print")
    result = engine.next_signature()
    
    assert result.success, "Sonraki imza geçişi başarılı olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Next signature")
    print("=" * 70)


def test_previous_signature():
    """
    Test: Previous signature.
    """
    print("=" * 70)
    print("TEST: Previous Signature")
    print("=" * 70)
    
    engine = SignatureHelpEngine()
    
    engine.get_signature("print")
    result = engine.previous_signature()
    
    assert result.success, "Önceki imza geçişi başarılı olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Previous signature")
    print("=" * 70)


def test_hide_signature():
    """
    Test: Hide signature.
    """
    print("=" * 70)
    print("TEST: Hide Signature")
    print("=" * 70)
    
    engine = SignatureHelpEngine()
    
    engine.get_signature("print")
    result = engine.hide_signature()
    
    assert result.success, "Gizleme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Hide signature")
    print("=" * 70)


def test_get_signature_history():
    """
    Test: Get signature history.
    """
    print("=" * 70)
    print("TEST: Get Signature History")
    print("=" * 70)
    
    engine = SignatureHelpEngine()
    
    engine.get_signature("print")
    engine.get_signature("len")
    
    history = engine.get_signature_history()
    
    assert len(history) > 0, "Geçmiş olmalı"
    
    print(f"  History: {history}")
    
    print("\n" + "=" * 70)
    print("PASS: Get signature history")
    print("=" * 70)


def test_clear_history():
    """
    Test: Clear history.
    """
    print("=" * 70)
    print("TEST: Clear History")
    print("=" * 70)
    
    engine = SignatureHelpEngine()
    
    engine.get_signature("print")
    result = engine.clear_history()
    
    assert result.success, "Temizleme başarılı olmalı"
    assert len(engine.get_signature_history()) == 0, "Geçmiş temizlenmeli"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear history")
    print("=" * 70)


def test_clear_cache():
    """
    Test: Clear cache.
    """
    print("=" * 70)
    print("TEST: Clear Cache")
    print("=" * 70)
    
    engine = SignatureHelpEngine()
    
    engine.get_signature("print")
    result = engine.clear_cache()
    
    assert result.success, "Cache temizleme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear cache")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    engine = SignatureHelpEngine()
    
    new_config = SignatureConfig(trigger_mode=SignatureTriggerMode.MANUAL)
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
    
    engine = SignatureHelpEngine()
    
    config = engine.get_config()
    
    assert config is not None, "Config olmalı"
    assert config.trigger_mode == SignatureTriggerMode.AUTO, "Config eşleşmeli"
    
    print(f"  Trigger mode: {config.trigger_mode.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


def test_signature_trigger_mode_enum():
    """
    Test: SignatureTriggerMode enum.
    """
    print("=" * 70)
    print("TEST: SignatureTriggerMode Enum")
    print("=" * 70)
    
    assert SignatureTriggerMode.AUTO.value == "auto"
    assert SignatureTriggerMode.MANUAL.value == "manual"
    assert SignatureTriggerMode.BOTH.value == "both"
    
    print(f"  All enum values verified")
    print(f"  Total modes: {len(SignatureTriggerMode)}")
    
    print("\n" + "=" * 70)
    print("PASS: SignatureTriggerMode enum")
    print("=" * 70)


def test_parameter_type_enum():
    """
    Test: ParameterType enum.
    """
    print("=" * 70)
    print("TEST: ParameterType Enum")
    print("=" * 70)
    
    assert ParameterType.REQUIRED.value == "required"
    assert ParameterType.OPTIONAL.value == "optional"
    assert ParameterType.VARARGS.value == "varargs"
    assert ParameterType.KWARGS.value == "kwargs"
    
    print(f"  All enum values verified")
    print(f"  Total types: {len(ParameterType)}")
    
    print("\n" + "=" * 70)
    print("PASS: ParameterType enum")
    print("=" * 70)


def test_parameter_dataclass():
    """
    Test: Parameter dataclass.
    """
    print("=" * 70)
    print("TEST: Parameter Dataclass")
    print("=" * 70)
    
    parameter = Parameter(
        name="param1",
        param_type=ParameterType.REQUIRED,
        type_hint="str"
    )
    
    assert parameter.name == "param1", "Name eşleşmeli"
    assert parameter.param_type == ParameterType.REQUIRED, "Type eşleşmeli"
    assert parameter.is_active == False, "Is active eşleşmeli"
    
    print(f"  Name: {parameter.name}")
    print(f"  Type: {parameter.param_type.value}")
    print(f"  Is active: {parameter.is_active}")
    
    print("\n" + "=" * 70)
    print("PASS: Parameter dataclass")
    print("=" * 70)


def test_function_signature_dataclass():
    """
    Test: FunctionSignature dataclass.
    """
    print("=" * 70)
    print("TEST: FunctionSignature Dataclass")
    print("=" * 70)
    
    signature = FunctionSignature(
        name="test_func",
        return_type="void",
        description="Test function"
    )
    
    assert signature.name == "test_func", "Name eşleşmeli"
    assert signature.return_type == "void", "Return type eşleşmeli"
    
    print(f"  Name: {signature.name}")
    print(f"  Return type: {signature.return_type}")
    
    print("\n" + "=" * 70)
    print("PASS: FunctionSignature dataclass")
    print("=" * 70)


def test_signature_config_dataclass():
    """
    Test: SignatureConfig dataclass.
    """
    print("=" * 70)
    print("TEST: SignatureConfig Dataclass")
    print("=" * 70)
    
    config = SignatureConfig(
        trigger_mode=SignatureTriggerMode.AUTO,
        show_documentation=True,
        show_return_type=True
    )
    
    assert config.trigger_mode == SignatureTriggerMode.AUTO, "Trigger mode eşleşmeli"
    assert config.show_documentation == True, "Show documentation eşleşmeli"
    assert config.show_return_type == True, "Show return type eşleşmeli"
    
    print(f"  Trigger mode: {config.trigger_mode.value}")
    print(f"  Show documentation: {config.show_documentation}")
    print(f"  Show return type: {config.show_return_type}")
    
    print("\n" + "=" * 70)
    print("PASS: SignatureConfig dataclass")
    print("=" * 70)


def test_signature_result_dataclass():
    """
    Test: SignatureResult dataclass.
    """
    print("=" * 70)
    print("TEST: SignatureResult Dataclass")
    print("=" * 70)
    
    result = SignatureResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.signatures, list), "Signatures list olmalı"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Signatures: {len(result.signatures)}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: SignatureResult dataclass")
    print("=" * 70)


def test_cache_functionality():
    """
    Test: Cache functionality.
    """
    print("=" * 70)
    print("TEST: Cache Functionality")
    print("=" * 70)
    
    engine = SignatureHelpEngine()
    
    # İlk çağrı
    result1 = engine.get_signature("print")
    assert result1.success, "İlk çağrı başarılı olmalı"
    
    # İkinci çağrı (cache'den)
    result2 = engine.get_signature("print")
    assert result2.success, "Cache'den alma başarılı olmalı"
    
    print(f"  First call: {result1.message}")
    print(f"  Second call: {result2.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Cache functionality")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_get_signature()
        test2 = test_update_active_parameter()
        test3 = test_next_signature()
        test4 = test_previous_signature()
        test5 = test_hide_signature()
        test6 = test_get_signature_history()
        test7 = test_clear_history()
        test8 = test_clear_cache()
        test9 = test_update_config()
        test10 = test_get_config()
        test11 = test_signature_trigger_mode_enum()
        test12 = test_parameter_type_enum()
        test13 = test_parameter_dataclass()
        test14 = test_function_signature_dataclass()
        test15 = test_signature_config_dataclass()
        test16 = test_signature_result_dataclass()
        test17 = test_cache_functionality()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Get Signature: {'PASS' if test1 else 'FAIL'}")
        print(f"Update Active Parameter: {'PASS' if test2 else 'FAIL'}")
        print(f"Next Signature: {'PASS' if test3 else 'FAIL'}")
        print(f"Previous Signature: {'PASS' if test4 else 'FAIL'}")
        print(f"Hide Signature: {'PASS' if test5 else 'FAIL'}")
        print(f"Get Signature History: {'PASS' if test6 else 'FAIL'}")
        print(f"Clear History: {'PASS' if test7 else 'FAIL'}")
        print(f"Clear Cache: {'PASS' if test8 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test9 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test10 else 'FAIL'}")
        print(f"SignatureTriggerMode Enum: {'PASS' if test11 else 'FAIL'}")
        print(f"ParameterType Enum: {'PASS' if test12 else 'FAIL'}")
        print(f"Parameter Dataclass: {'PASS' if test13 else 'FAIL'}")
        print(f"FunctionSignature Dataclass: {'PASS' if test14 else 'FAIL'}")
        print(f"SignatureConfig Dataclass: {'PASS' if test15 else 'FAIL'}")
        print(f"SignatureResult Dataclass: {'PASS' if test16 else 'FAIL'}")
        print(f"Cache Functionality: {'PASS' if test17 else 'FAIL'}")
        
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
