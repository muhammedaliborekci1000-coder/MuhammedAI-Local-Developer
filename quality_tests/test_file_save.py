"""
Quality Test: File Save
File save system testleri.
"""

import sys
import os
import tempfile
import shutil

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.file_save import (
    FileSaveEngine,
    SaveMode,
    Encoding,
    LineEnding,
    SaveConfig,
    SaveResult
)


def test_save_file():
    """
    Test: Save file.
    """
    print("=" * 70)
    print("TEST: Save File")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp()
    temp_file = os.path.join(temp_dir, "test.txt")
    
    try:
        engine = FileSaveEngine()
        result = engine.save_file(temp_file, "Hello World")
        
        assert result.success, "Kaydetme başarılı olmalı"
        assert os.path.exists(temp_file), "Dosya oluşturulmalı"
        
        with open(temp_file, 'r') as f:
            content = f.read()
            assert content == "Hello World\n", "İçerik eşleşmeli"
        
        print(f"  Success: {result.success}")
        print(f"  Message: {result.message}")
        
        print("\n" + "=" * 70)
        print("PASS: Save file")
        print("=" * 70)
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def test_save_as():
    """
    Test: Save as.
    """
    print("=" * 70)
    print("TEST: Save As")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp()
    original_file = os.path.join(temp_dir, "original.txt")
    new_file = os.path.join(temp_dir, "new.txt")
    
    try:
        engine = FileSaveEngine()
        result = engine.save_as(original_file, new_file, "Hello World")
        
        assert result.success, "Kaydetme başarılı olmalı"
        assert os.path.exists(new_file), "Yeni dosya oluşturulmalı"
        
        with open(new_file, 'r') as f:
            content = f.read()
            assert content == "Hello World\n", "İçerik eşleşmeli"
        
        print(f"  Success: {result.success}")
        print(f"  Message: {result.message}")
        
        print("\n" + "=" * 70)
        print("PASS: Save as")
        print("=" * 70)
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def test_auto_save():
    """
    Test: Auto save.
    """
    print("=" * 70)
    print("TEST: Auto Save")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp()
    temp_file = os.path.join(temp_dir, "test.txt")
    
    try:
        engine = FileSaveEngine()
        engine.enable_auto_save()
        
        result = engine.auto_save(temp_file, "Hello World")
        
        assert result.success, "Otomatik kaydetme başarılı olmalı"
        assert os.path.exists(temp_file), "Dosya oluşturulmalı"
        
        print(f"  Success: {result.success}")
        print(f"  Message: {result.message}")
        
        print("\n" + "=" * 70)
        print("PASS: Auto save")
        print("=" * 70)
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def test_can_save():
    """
    Test: Can save.
    """
    print("=" * 70)
    print("TEST: Can Save")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp()
    temp_file = os.path.join(temp_dir, "test.txt")
    
    try:
        engine = FileSaveEngine()
        can_save = engine.can_save(temp_file)
        
        assert can_save == True, "Kaydedilebilir olmalı"
        
        print(f"  Can save: {can_save}")
        
        print("\n" + "=" * 70)
        print("PASS: Can save")
        print("=" * 70)
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def test_get_file_content():
    """
    Test: Get file content.
    """
    print("=" * 70)
    print("TEST: Get File Content")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp()
    temp_file = os.path.join(temp_dir, "test.txt")
    
    with open(temp_file, 'w') as f:
        f.write("Hello World")
    
    try:
        engine = FileSaveEngine()
        content = engine.get_file_content(temp_file)
        
        assert content == "Hello World", "İçerik eşleşmeli"
        
        print(f"  Content: {content}")
        
        print("\n" + "=" * 70)
        print("PASS: Get file content")
        print("=" * 70)
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def test_enable_auto_save():
    """
    Test: Enable auto save.
    """
    print("=" * 70)
    print("TEST: Enable Auto Save")
    print("=" * 70)
    
    engine = FileSaveEngine()
    
    result = engine.enable_auto_save(60)
    
    assert result.success, "Etkinleştirme başarılı olmalı"
    assert engine.auto_save_enabled == True, "Otomatik kaydetme etkin olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Enable auto save")
    print("=" * 70)


def test_disable_auto_save():
    """
    Test: Disable auto save.
    """
    print("=" * 70)
    print("TEST: Disable Auto Save")
    print("=" * 70)
    
    engine = FileSaveEngine()
    engine.enable_auto_save()
    
    result = engine.disable_auto_save()
    
    assert result.success, "Devre dışı bırakma başarılı olmalı"
    assert engine.auto_save_enabled == False, "Otomatik kaydetme devre dışı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Disable auto save")
    print("=" * 70)


def test_get_save_history():
    """
    Test: Get save history.
    """
    print("=" * 70)
    print("TEST: Get Save History")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp()
    temp_file = os.path.join(temp_dir, "test.txt")
    
    try:
        engine = FileSaveEngine()
        engine.save_file(temp_file, "Hello World")
        
        history = engine.get_save_history()
        
        assert len(history) > 0, "Geçmiş olmalı"
        
        print(f"  History: {len(history)}")
        
        print("\n" + "=" * 70)
        print("PASS: Get save history")
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
    
    try:
        engine = FileSaveEngine()
        engine.save_file(temp_file, "Hello World")
        
        result = engine.clear_history()
        
        assert result.success, "Temizleme başarılı olmalı"
        assert len(engine.get_save_history()) == 0, "Geçmiş temizlenmeli"
        
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
    
    engine = FileSaveEngine()
    
    new_config = SaveConfig(mode=SaveMode.SAVE_AS, encoding=Encoding.UTF16)
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
    
    engine = FileSaveEngine()
    
    config = engine.get_config()
    
    assert config is not None, "Config olmalı"
    assert config.mode == SaveMode.SAVE, "Config eşleşmeli"
    
    print(f"  Mode: {config.mode.value}")
    print(f"  Encoding: {config.encoding.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


def test_save_mode_enum():
    """
    Test: SaveMode enum.
    """
    print("=" * 70)
    print("TEST: SaveMode Enum")
    print("=" * 70)
    
    assert SaveMode.SAVE.value == "save"
    assert SaveMode.SAVE_AS.value == "save_as"
    assert SaveMode.AUTO_SAVE.value == "auto_save"
    assert SaveMode.BACKUP.value == "backup"
    
    print(f"  All enum values verified")
    print(f"  Total modes: {len(SaveMode)}")
    
    print("\n" + "=" * 70)
    print("PASS: SaveMode enum")
    print("=" * 70)


def test_encoding_enum():
    """
    Test: Encoding enum.
    """
    print("=" * 70)
    print("TEST: Encoding Enum")
    print("=" * 70)
    
    assert Encoding.UTF8.value == "utf-8"
    assert Encoding.UTF8_WITH_BOM.value == "utf-8-sig"
    assert Encoding.UTF16.value == "utf-16"
    assert Encoding.ASCII.value == "ascii"
    
    print(f"  All enum values verified")
    print(f"  Total encodings: {len(Encoding)}")
    
    print("\n" + "=" * 70)
    print("PASS: Encoding enum")
    print("=" * 70)


def test_line_ending_enum():
    """
    Test: LineEnding enum.
    """
    print("=" * 70)
    print("TEST: LineEnding Enum")
    print("=" * 70)
    
    assert LineEnding.LF.value == "\n"
    assert LineEnding.CRLF.value == "\r\n"
    assert LineEnding.CR.value == "\r"
    
    print(f"  All enum values verified")
    print(f"  Total line endings: {len(LineEnding)}")
    
    print("\n" + "=" * 70)
    print("PASS: LineEnding enum")
    print("=" * 70)


def test_save_config_dataclass():
    """
    Test: SaveConfig dataclass.
    """
    print("=" * 70)
    print("TEST: SaveConfig Dataclass")
    print("=" * 70)
    
    config = SaveConfig(
        mode=SaveMode.SAVE_AS,
        encoding=Encoding.UTF16,
        line_ending=LineEnding.CRLF
    )
    
    assert config.mode == SaveMode.SAVE_AS, "Mode eşleşmeli"
    assert config.encoding == Encoding.UTF16, "Encoding eşleşmeli"
    assert config.line_ending == LineEnding.CRLF, "Line ending eşleşmeli"
    
    print(f"  Mode: {config.mode.value}")
    print(f"  Encoding: {config.encoding.value}")
    print(f"  Line ending: {repr(config.line_ending.value)}")
    
    print("\n" + "=" * 70)
    print("PASS: SaveConfig dataclass")
    print("=" * 70)


def test_save_result_dataclass():
    """
    Test: SaveResult dataclass.
    """
    print("=" * 70)
    print("TEST: SaveResult Dataclass")
    print("=" * 70)
    
    result = SaveResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: SaveResult dataclass")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_save_file()
        test2 = test_save_as()
        test3 = test_auto_save()
        test4 = test_can_save()
        test5 = test_get_file_content()
        test6 = test_enable_auto_save()
        test7 = test_disable_auto_save()
        test8 = test_get_save_history()
        test9 = test_clear_history()
        test10 = test_update_config()
        test11 = test_get_config()
        test12 = test_save_mode_enum()
        test13 = test_encoding_enum()
        test14 = test_line_ending_enum()
        test15 = test_save_config_dataclass()
        test16 = test_save_result_dataclass()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Save File: {'PASS' if test1 else 'FAIL'}")
        print(f"Save As: {'PASS' if test2 else 'FAIL'}")
        print(f"Auto Save: {'PASS' if test3 else 'FAIL'}")
        print(f"Can Save: {'PASS' if test4 else 'FAIL'}")
        print(f"Get File Content: {'PASS' if test5 else 'FAIL'}")
        print(f"Enable Auto Save: {'PASS' if test6 else 'FAIL'}")
        print(f"Disable Auto Save: {'PASS' if test7 else 'FAIL'}")
        print(f"Get Save History: {'PASS' if test8 else 'FAIL'}")
        print(f"Clear History: {'PASS' if test9 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test10 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test11 else 'FAIL'}")
        print(f"SaveMode Enum: {'PASS' if test12 else 'FAIL'}")
        print(f"Encoding Enum: {'PASS' if test13 else 'FAIL'}")
        print(f"LineEnding Enum: {'PASS' if test14 else 'FAIL'}")
        print(f"SaveConfig Dataclass: {'PASS' if test15 else 'FAIL'}")
        print(f"SaveResult Dataclass: {'PASS' if test16 else 'FAIL'}")
        
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
