"""
Quality Test: File Properties
File properties system testleri.
"""

import sys
import os
import tempfile
import shutil

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.file_properties import (
    FilePropertiesEngine,
    PropertyType,
    FileProperties,
    PropertiesConfig,
    PropertiesResult
)


def test_get_properties():
    """
    Test: Get properties.
    """
    print("=" * 70)
    print("TEST: Get Properties")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp()
    temp_file = os.path.join(temp_dir, "test.txt")
    
    with open(temp_file, 'w') as f:
        f.write("Hello World\nTest Line")
    
    try:
        engine = FilePropertiesEngine()
        result = engine.get_properties(temp_file)
        
        assert result.success, "Alma başarılı olmalı"
        assert result.properties is not None, "Properties olmalı"
        assert result.properties.name == "test.txt", "İsim eşleşmeli"
        
        print(f"  Success: {result.success}")
        print(f"  Name: {result.properties.name}")
        print(f"  Size: {result.properties.size_human}")
        
        print("\n" + "=" * 70)
        print("PASS: Get properties")
        print("=" * 70)
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def test_get_properties_basic():
    """
    Test: Get properties basic.
    """
    print("=" * 70)
    print("TEST: Get Properties Basic")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp()
    temp_file = os.path.join(temp_dir, "test.txt")
    
    with open(temp_file, 'w') as f:
        f.write("Hello World")
    
    try:
        engine = FilePropertiesEngine()
        result = engine.get_properties(temp_file, PropertyType.BASIC)
        
        assert result.success, "Alma başarılı olmalı"
        assert result.properties is not None, "Properties olmalı"
        
        print(f"  Success: {result.success}")
        print(f"  Name: {result.properties.name}")
        
        print("\n" + "=" * 70)
        print("PASS: Get properties basic")
        print("=" * 70)
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def test_get_properties_advanced():
    """
    Test: Get properties advanced.
    """
    print("=" * 70)
    print("TEST: Get Properties Advanced")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp()
    temp_file = os.path.join(temp_dir, "test.py")
    
    with open(temp_file, 'w') as f:
        f.write("print('Hello World')")
    
    try:
        engine = FilePropertiesEngine()
        result = engine.get_properties(temp_file, PropertyType.ADVANCED)
        
        assert result.success, "Alma başarılı olmalı"
        assert result.properties is not None, "Properties olmalı"
        assert result.properties.mime_type != "", "MIME type olmalı"
        
        print(f"  Success: {result.success}")
        print(f"  MIME type: {result.properties.mime_type}")
        
        print("\n" + "=" * 70)
        print("PASS: Get properties advanced")
        print("=" * 70)
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def test_get_properties_directory():
    """
    Test: Get properties directory.
    """
    print("=" * 70)
    print("TEST: Get Properties Directory")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp()
    
    try:
        engine = FilePropertiesEngine()
        result = engine.get_properties(temp_dir)
        
        assert result.success, "Alma başarılı olmalı"
        assert result.properties is not None, "Properties olmalı"
        assert result.properties.is_directory == True, "Dizin olmalı"
        
        print(f"  Success: {result.success}")
        print(f"  Is directory: {result.properties.is_directory}")
        
        print("\n" + "=" * 70)
        print("PASS: Get properties directory")
        print("=" * 70)
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def test_get_properties_history():
    """
    Test: Get properties history.
    """
    print("=" * 70)
    print("TEST: Get Properties History")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp()
    temp_file = os.path.join(temp_dir, "test.txt")
    
    with open(temp_file, 'w') as f:
        f.write("Hello World")
    
    try:
        engine = FilePropertiesEngine()
        engine.get_properties(temp_file)
        
        history = engine.get_properties_history()
        
        assert len(history) > 0, "Geçmiş olmalı"
        
        print(f"  History: {len(history)}")
        
        print("\n" + "=" * 70)
        print("PASS: Get properties history")
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
    
    with open(temp_file, 'w') as f:
        f.write("Hello World")
    
    try:
        engine = FilePropertiesEngine()
        engine.get_properties(temp_file)
        
        result = engine.clear_history()
        
        assert result.success, "Temizleme başarılı olmalı"
        assert len(engine.get_properties_history()) == 0, "Geçmiş temizlenmeli"
        
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
    
    engine = FilePropertiesEngine()
    
    new_config = PropertiesConfig(include_advanced=False)
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
    
    engine = FilePropertiesEngine()
    
    config = engine.get_config()
    
    assert config is not None, "Config olmalı"
    assert config.include_advanced == True, "Config eşleşmeli"
    
    print(f"  Include advanced: {config.include_advanced}")
    print(f"  Calculate stats: {config.calculate_stats}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


def test_property_type_enum():
    """
    Test: PropertyType enum.
    """
    print("=" * 70)
    print("TEST: PropertyType Enum")
    print("=" * 70)
    
    assert PropertyType.BASIC.value == "basic"
    assert PropertyType.ADVANCED.value == "advanced"
    assert PropertyType.ALL.value == "all"
    
    print(f"  All enum values verified")
    print(f"  Total types: {len(PropertyType)}")
    
    print("\n" + "=" * 70)
    print("PASS: PropertyType enum")
    print("=" * 70)


def test_file_properties_dataclass():
    """
    Test: FileProperties dataclass.
    """
    print("=" * 70)
    print("TEST: FileProperties Dataclass")
    print("=" * 70)
    
    props = FileProperties(
        path="/test/file.txt",
        name="file.txt",
        size=100,
        is_file=True
    )
    
    assert props.path == "/test/file.txt", "Path eşleşmeli"
    assert props.name == "file.txt", "Name eşleşmeli"
    assert props.size == 100, "Size eşleşmeli"
    
    print(f"  Path: {props.path}")
    print(f"  Name: {props.name}")
    print(f"  Size: {props.size}")
    
    print("\n" + "=" * 70)
    print("PASS: FileProperties dataclass")
    print("=" * 70)


def test_properties_config_dataclass():
    """
    Test: PropertiesConfig dataclass.
    """
    print("=" * 70)
    print("TEST: PropertiesConfig Dataclass")
    print("=" * 70)
    
    config = PropertiesConfig(
        include_advanced=False,
        calculate_stats=False
    )
    
    assert config.include_advanced == False, "Include advanced eşleşmeli"
    assert config.calculate_stats == False, "Calculate stats eşleşmeli"
    
    print(f"  Include advanced: {config.include_advanced}")
    print(f"  Calculate stats: {config.calculate_stats}")
    
    print("\n" + "=" * 70)
    print("PASS: PropertiesConfig dataclass")
    print("=" * 70)


def test_properties_result_dataclass():
    """
    Test: PropertiesResult dataclass.
    """
    print("=" * 70)
    print("TEST: PropertiesResult Dataclass")
    print("=" * 70)
    
    result = PropertiesResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: PropertiesResult dataclass")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_get_properties()
        test2 = test_get_properties_basic()
        test3 = test_get_properties_advanced()
        test4 = test_get_properties_directory()
        test5 = test_get_properties_history()
        test6 = test_clear_history()
        test7 = test_update_config()
        test8 = test_get_config()
        test9 = test_property_type_enum()
        test10 = test_file_properties_dataclass()
        test11 = test_properties_config_dataclass()
        test12 = test_properties_result_dataclass()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Get Properties: {'PASS' if test1 else 'FAIL'}")
        print(f"Get Properties Basic: {'PASS' if test2 else 'FAIL'}")
        print(f"Get Properties Advanced: {'PASS' if test3 else 'FAIL'}")
        print(f"Get Properties Directory: {'PASS' if test4 else 'FAIL'}")
        print(f"Get Properties History: {'PASS' if test5 else 'FAIL'}")
        print(f"Clear History: {'PASS' if test6 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test7 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test8 else 'FAIL'}")
        print(f"PropertyType Enum: {'PASS' if test9 else 'FAIL'}")
        print(f"FileProperties Dataclass: {'PASS' if test10 else 'FAIL'}")
        print(f"PropertiesConfig Dataclass: {'PASS' if test11 else 'FAIL'}")
        print(f"PropertiesResult Dataclass: {'PASS' if test12 else 'FAIL'}")
        
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
