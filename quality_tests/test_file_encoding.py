"""
Quality Test: File Encoding
File encoding system testleri.
"""

import sys
import os
import tempfile
import shutil

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.file_encoding import (
    FileEncodingEngine,
    EncodingType,
    EncodingAction,
    EncodingConfig,
    EncodingResult
)


def test_detect_encoding():
    """
    Test: Detect encoding.
    """
    print("=" * 70)
    print("TEST: Detect Encoding")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp()
    temp_file = os.path.join(temp_dir, "test.txt")
    
    with open(temp_file, 'w', encoding='utf-8') as f:
        f.write("Hello World")
    
    try:
        engine = FileEncodingEngine()
        result = engine.detect_encoding(temp_file)
        
        assert result.success, "Tespit başarılı olmalı"
        assert result.detected_encoding is not None, "Encoding tespit edilmeli"
        
        print(f"  Success: {result.success}")
        print(f"  Detected encoding: {result.detected_encoding}")
        print(f"  Confidence: {result.confidence}")
        
        print("\n" + "=" * 70)
        print("PASS: Detect encoding")
        print("=" * 70)
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def test_convert_encoding():
    """
    Test: Convert encoding.
    """
    print("=" * 70)
    print("TEST: Convert Encoding")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp()
    temp_file = os.path.join(temp_dir, "test.txt")
    
    with open(temp_file, 'w', encoding='utf-8') as f:
        f.write("Hello World")
    
    try:
        engine = FileEncodingEngine()
        result = engine.convert_encoding(temp_file, EncodingType.LATIN1)
        
        assert result.success, "Dönüştürme başarılı olmalı"
        assert result.detected_encoding == "latin-1", "Encoding değişmeli"
        
        print(f"  Success: {result.success}")
        print(f"  Original encoding: {result.original_encoding}")
        print(f"  Target encoding: {result.detected_encoding}")
        
        print("\n" + "=" * 70)
        print("PASS: Convert encoding")
        print("=" * 70)
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def test_validate_encoding():
    """
    Test: Validate encoding.
    """
    print("=" * 70)
    print("TEST: Validate Encoding")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp()
    temp_file = os.path.join(temp_dir, "test.txt")
    
    with open(temp_file, 'w', encoding='utf-8') as f:
        f.write("Hello World")
    
    try:
        engine = FileEncodingEngine()
        result = engine.validate_encoding(temp_file, EncodingType.UTF8)
        
        assert result.success, "Doğrulama başarılı olmalı"
        
        print(f"  Success: {result.success}")
        print(f"  Message: {result.message}")
        
        print("\n" + "=" * 70)
        print("PASS: Validate encoding")
        print("=" * 70)
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def test_reload_with_encoding():
    """
    Test: Reload with encoding.
    """
    print("=" * 70)
    print("TEST: Reload With Encoding")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp()
    temp_file = os.path.join(temp_dir, "test.txt")
    
    with open(temp_file, 'w', encoding='utf-8') as f:
        f.write("Hello World")
    
    try:
        engine = FileEncodingEngine()
        result = engine.reload_with_encoding(temp_file, EncodingType.UTF8)
        
        assert result.success, "Yükleme başarılı olmalı"
        assert result.converted_content == "Hello World", "İçerik eşleşmeli"
        
        print(f"  Success: {result.success}")
        print(f"  Content: {result.converted_content}")
        
        print("\n" + "=" * 70)
        print("PASS: Reload with encoding")
        print("=" * 70)
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def test_get_encoding_history():
    """
    Test: Get encoding history.
    """
    print("=" * 70)
    print("TEST: Get Encoding History")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp()
    temp_file = os.path.join(temp_dir, "test.txt")
    
    with open(temp_file, 'w', encoding='utf-8') as f:
        f.write("Hello World")
    
    try:
        engine = FileEncodingEngine()
        engine.detect_encoding(temp_file)
        
        history = engine.get_encoding_history()
        
        assert len(history) > 0, "Geçmiş olmalı"
        
        print(f"  History: {len(history)}")
        
        print("\n" + "=" * 70)
        print("PASS: Get encoding history")
        print("=" * 70)
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def test_clear_history():
    """
    Test: Clear history.
    """
    print("=" * 70)
    print("TEST: Clear History")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp()
    temp_file = os.path.join(temp_dir, "test.txt")
    
    with open(temp_file, 'w', encoding='utf-8') as f:
        f.write("Hello World")
    
    try:
        engine = FileEncodingEngine()
        engine.detect_encoding(temp_file)
        
        result = engine.clear_history()
        
        assert result.success, "Temizleme başarılı olmalı"
        assert len(engine.get_encoding_history()) == 0, "Geçmiş temizlenmeli"
        
        print(f"  Success: {result.success}")
        
        print("\n" + "=" * 70)
        print("PASS: Clear history")
        print("=" * 70)
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    engine = FileEncodingEngine()
    
    new_config = EncodingConfig(default_encoding=EncodingType.UTF16_LE)
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
    
    engine = FileEncodingEngine()
    
    config = engine.get_config()
    
    assert config is not None, "Config olmalı"
    assert config.default_encoding == EncodingType.UTF8, "Config eşleşmeli"
    
    print(f"  Default encoding: {config.default_encoding.value}")
    print(f"  Auto detect: {config.auto_detect}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


def test_encoding_type_enum():
    """
    Test: EncodingType enum.
    """
    print("=" * 70)
    print("TEST: EncodingType Enum")
    print("=" * 70)
    
    assert EncodingType.UTF8.value == "utf-8"
    assert EncodingType.UTF8_WITH_BOM.value == "utf-8-sig"
    assert EncodingType.UTF16_LE.value == "utf-16-le"
    assert EncodingType.ASCII.value == "ascii"
    assert EncodingType.AUTO_DETECT.value == "auto_detect"
    
    print(f"  All enum values verified")
    print(f"  Total encodings: {len(EncodingType)}")
    
    print("\n" + "=" * 70)
    print("PASS: EncodingType enum")
    print("=" * 70)


def test_encoding_action_enum():
    """
    Test: EncodingAction enum.
    """
    print("=" * 70)
    print("TEST: EncodingAction Enum")
    print("=" * 70)
    
    assert EncodingAction.DETECT.value == "detect"
    assert EncodingAction.CONVERT.value == "convert"
    assert EncodingAction.VALIDATE.value == "validate"
    assert EncodingAction.RELOAD.value == "reload"
    
    print(f"  All enum values verified")
    print(f"  Total actions: {len(EncodingAction)}")
    
    print("\n" + "=" * 70)
    print("PASS: EncodingAction enum")
    print("=" * 70)


def test_encoding_config_dataclass():
    """
    Test: EncodingConfig dataclass.
    """
    print("=" * 70)
    print("TEST: EncodingConfig Dataclass")
    print("=" * 70)
    
    config = EncodingConfig(
        default_encoding=EncodingType.UTF16_LE,
        auto_detect=False,
        fallback_encoding=EncodingType.LATIN1
    )
    
    assert config.default_encoding == EncodingType.UTF16_LE, "Default encoding eşleşmeli"
    assert config.auto_detect == False, "Auto detect eşleşmeli"
    assert config.fallback_encoding == EncodingType.LATIN1, "Fallback encoding eşleşmeli"
    
    print(f"  Default encoding: {config.default_encoding.value}")
    print(f"  Auto detect: {config.auto_detect}")
    print(f"  Fallback encoding: {config.fallback_encoding.value}")
    
    print("\n" + "=" * 70)
    print("PASS: EncodingConfig dataclass")
    print("=" * 70)


def test_encoding_result_dataclass():
    """
    Test: EncodingResult dataclass.
    """
    print("=" * 70)
    print("TEST: EncodingResult Dataclass")
    print("=" * 70)
    
    result = EncodingResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: EncodingResult dataclass")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_detect_encoding()
        test2 = test_convert_encoding()
        test3 = test_validate_encoding()
        test4 = test_reload_with_encoding()
        test5 = test_get_encoding_history()
        test6 = test_clear_history()
        test7 = test_update_config()
        test8 = test_get_config()
        test9 = test_encoding_type_enum()
        test10 = test_encoding_action_enum()
        test11 = test_encoding_config_dataclass()
        test12 = test_encoding_result_dataclass()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Detect Encoding: {'PASS' if test1 else 'FAIL'}")
        print(f"Convert Encoding: {'PASS' if test2 else 'FAIL'}")
        print(f"Validate Encoding: {'PASS' if test3 else 'FAIL'}")
        print(f"Reload With Encoding: {'PASS' if test4 else 'FAIL'}")
        print(f"Get Encoding History: {'PASS' if test5 else 'FAIL'}")
        print(f"Clear History: {'PASS' if test6 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test7 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test8 else 'FAIL'}")
        print(f"EncodingType Enum: {'PASS' if test9 else 'FAIL'}")
        print(f"EncodingAction Enum: {'PASS' if test10 else 'FAIL'}")
        print(f"EncodingConfig Dataclass: {'PASS' if test11 else 'FAIL'}")
        print(f"EncodingResult Dataclass: {'PASS' if test12 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12])
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
