"""
Quality Test: File Open
File open system testleri.
"""

import sys
import os
import tempfile
import shutil

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.file_open import (
    FileOpenEngine,
    OpenMode,
    Encoding,
    LineEnding,
    OpenConfig,
    OpenResult
)


def test_open_file():
    """
    Test: Open file.
    """
    print("=" * 70)
    print("TEST: Open File")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp()
    temp_file = os.path.join(temp_dir, "test.txt")
    
    with open(temp_file, 'w') as f:
        f.write("Hello World")
    
    try:
        engine = FileOpenEngine()
        result = engine.open_file(temp_file)
        
        assert result.success, "Açma başarılı olmalı"
        assert result.content == "Hello World", "İçerik eşleşmeli"
        assert result.encoding is not None, "Encoding olmalı"
        
        print(f"  Success: {result.success}")
        print(f"  Message: {result.message}")
        print(f"  Encoding: {result.encoding}")
        
        print("\n" + "=" * 70)
        print("PASS: Open file")
        print("=" * 70)
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def test_open_with_encoding():
    """
    Test: Open with encoding.
    """
    print("=" * 70)
    print("TEST: Open With Encoding")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp()
    temp_file = os.path.join(temp_dir, "test.txt")
    
    with open(temp_file, 'w', encoding='utf-8') as f:
        f.write("Hello World")
    
    try:
        engine = FileOpenEngine()
        result = engine.open_with_encoding(temp_file, Encoding.UTF8)
        
        assert result.success, "Açma başarılı olmalı"
        assert result.encoding == "utf-8", "Encoding eşleşmeli"
        
        print(f"  Success: {result.success}")
        print(f"  Message: {result.message}")
        print(f"  Encoding: {result.encoding}")
        
        print("\n" + "=" * 70)
        print("PASS: Open with encoding")
        print("=" * 70)
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def test_open_readonly():
    """
    Test: Open readonly.
    """
    print("=" * 70)
    print("TEST: Open Readonly")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp()
    temp_file = os.path.join(temp_dir, "test.txt")
    
    with open(temp_file, 'w') as f:
        f.write("Hello World")
    
    try:
        engine = FileOpenEngine()
        result = engine.open_readonly(temp_file)
        
        assert result.success, "Açma başarılı olmalı"
        assert result.content == "Hello World", "İçerik eşleşmeli"
        
        print(f"  Success: {result.success}")
        print(f"  Message: {result.message}")
        
        print("\n" + "=" * 70)
        print("PASS: Open readonly")
        print("=" * 70)
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def test_open_recent():
    """
    Test: Open recent.
    """
    print("=" * 70)
    print("TEST: Open Recent")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp()
    temp_file = os.path.join(temp_dir, "test.txt")
    
    with open(temp_file, 'w') as f:
        f.write("Hello World")
    
    try:
        engine = FileOpenEngine()
        engine.open_file(temp_file)
        
        result = engine.open_recent(0)
        
        assert result.success, "Açma başarılı olmalı"
        assert result.content == "Hello World", "İçerik eşleşmeli"
        
        print(f"  Success: {result.success}")
        print(f"  Message: {result.message}")
        
        print("\n" + "=" * 70)
        print("PASS: Open recent")
        print("=" * 70)
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def test_can_open():
    """
    Test: Can open.
    """
    print("=" * 70)
    print("TEST: Can Open")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp()
    temp_file = os.path.join(temp_dir, "test.txt")
    
    with open(temp_file, 'w') as f:
        f.write("Hello World")
    
    try:
        engine = FileOpenEngine()
        can_open = engine.can_open(temp_file)
        
        assert can_open == True, "Açılabilir olmalı"
        
        print(f"  Can open: {can_open}")
        
        print("\n" + "=" * 70)
        print("PASS: Can open")
        print("=" * 70)
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def test_get_file_size():
    """
    Test: Get file size.
    """
    print("=" * 70)
    print("TEST: Get File Size")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp()
    temp_file = os.path.join(temp_dir, "test.txt")
    
    with open(temp_file, 'w') as f:
        f.write("Hello World")
    
    try:
        engine = FileOpenEngine()
        size = engine.get_file_size(temp_file)
        
        assert size > 0, "Boyut > 0 olmalı"
        
        print(f"  File size: {size}")
        
        print("\n" + "=" * 70)
        print("PASS: Get file size")
        print("=" * 70)
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def test_get_recent_files():
    """
    Test: Get recent files.
    """
    print("=" * 70)
    print("TEST: Get Recent Files")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp()
    temp_file = os.path.join(temp_dir, "test.txt")
    
    with open(temp_file, 'w') as f:
        f.write("Hello World")
    
    try:
        engine = FileOpenEngine()
        engine.open_file(temp_file)
        
        recent_files = engine.get_recent_files()
        
        assert len(recent_files) > 0, "Son dosyalar olmalı"
        
        print(f"  Recent files: {len(recent_files)}")
        
        print("\n" + "=" * 70)
        print("PASS: Get recent files")
        print("=" * 70)
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def test_clear_recent_files():
    """
    Test: Clear recent files.
    """
    print("=" * 70)
    print("TEST: Clear Recent Files")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp()
    temp_file = os.path.join(temp_dir, "test.txt")
    
    with open(temp_file, 'w') as f:
        f.write("Hello World")
    
    try:
        engine = FileOpenEngine()
        engine.open_file(temp_file)
        
        result = engine.clear_recent_files()
        
        assert result.success, "Temizleme başarılı olmalı"
        assert len(engine.get_recent_files()) == 0, "Son dosyalar temizlenmeli"
        
        print(f"  Success: {result.success}")
        
        print("\n" + "=" * 70)
        print("PASS: Clear recent files")
        print("=" * 70)
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def test_get_open_history():
    """
    Test: Get open history.
    """
    print("=" * 70)
    print("TEST: Get Open History")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp()
    temp_file = os.path.join(temp_dir, "test.txt")
    
    with open(temp_file, 'w') as f:
        f.write("Hello World")
    
    try:
        engine = FileOpenEngine()
        engine.open_file(temp_file)
        
        history = engine.get_open_history()
        
        assert len(history) > 0, "Geçmiş olmalı"
        
        print(f"  History: {len(history)}")
        
        print("\n" + "=" * 70)
        print("PASS: Get open history")
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
        engine = FileOpenEngine()
        engine.open_file(temp_file)
        
        result = engine.clear_history()
        
        assert result.success, "Temizleme başarılı olmalı"
        assert len(engine.get_open_history()) == 0, "Geçmiş temizlenmeli"
        
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
    
    engine = FileOpenEngine()
    
    new_config = OpenConfig(mode=OpenMode.OPEN_WITH_ENCODING, encoding=Encoding.UTF16)
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
    
    engine = FileOpenEngine()
    
    config = engine.get_config()
    
    assert config is not None, "Config olmalı"
    assert config.mode == OpenMode.OPEN, "Config eşleşmeli"
    
    print(f"  Mode: {config.mode.value}")
    print(f"  Encoding: {config.encoding.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


def test_open_mode_enum():
    """
    Test: OpenMode enum.
    """
    print("=" * 70)
    print("TEST: OpenMode Enum")
    print("=" * 70)
    
    assert OpenMode.OPEN.value == "open"
    assert OpenMode.OPEN_RECENT.value == "open_recent"
    assert OpenMode.OPEN_WITH_ENCODING.value == "open_with_encoding"
    assert OpenMode.OPEN_READONLY.value == "open_readonly"
    
    print(f"  All enum values verified")
    print(f"  Total modes: {len(OpenMode)}")
    
    print("\n" + "=" * 70)
    print("PASS: OpenMode enum")
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
    assert Encoding.AUTO_DETECT.value == "auto_detect"
    
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
    assert LineEnding.AUTO_DETECT.value == "auto_detect"
    
    print(f"  All enum values verified")
    print(f"  Total line endings: {len(LineEnding)}")
    
    print("\n" + "=" * 70)
    print("PASS: LineEnding enum")
    print("=" * 70)


def test_open_config_dataclass():
    """
    Test: OpenConfig dataclass.
    """
    print("=" * 70)
    print("TEST: OpenConfig Dataclass")
    print("=" * 70)
    
    config = OpenConfig(
        mode=OpenMode.OPEN_WITH_ENCODING,
        encoding=Encoding.UTF16,
        readonly=True
    )
    
    assert config.mode == OpenMode.OPEN_WITH_ENCODING, "Mode eşleşmeli"
    assert config.encoding == Encoding.UTF16, "Encoding eşleşmeli"
    assert config.readonly == True, "Readonly eşleşmeli"
    
    print(f"  Mode: {config.mode.value}")
    print(f"  Encoding: {config.encoding.value}")
    print(f"  Readonly: {config.readonly}")
    
    print("\n" + "=" * 70)
    print("PASS: OpenConfig dataclass")
    print("=" * 70)


def test_open_result_dataclass():
    """
    Test: OpenResult dataclass.
    """
    print("=" * 70)
    print("TEST: OpenResult Dataclass")
    print("=" * 70)
    
    result = OpenResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: OpenResult dataclass")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_open_file()
        test2 = test_open_with_encoding()
        test3 = test_open_readonly()
        test4 = test_open_recent()
        test5 = test_can_open()
        test6 = test_get_file_size()
        test7 = test_get_recent_files()
        test8 = test_clear_recent_files()
        test9 = test_get_open_history()
        test10 = test_clear_history()
        test11 = test_update_config()
        test12 = test_get_config()
        test13 = test_open_mode_enum()
        test14 = test_encoding_enum()
        test15 = test_line_ending_enum()
        test16 = test_open_config_dataclass()
        test17 = test_open_result_dataclass()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Open File: {'PASS' if test1 else 'FAIL'}")
        print(f"Open With Encoding: {'PASS' if test2 else 'FAIL'}")
        print(f"Open Readonly: {'PASS' if test3 else 'FAIL'}")
        print(f"Open Recent: {'PASS' if test4 else 'FAIL'}")
        print(f"Can Open: {'PASS' if test5 else 'FAIL'}")
        print(f"Get File Size: {'PASS' if test6 else 'FAIL'}")
        print(f"Get Recent Files: {'PASS' if test7 else 'FAIL'}")
        print(f"Clear Recent Files: {'PASS' if test8 else 'FAIL'}")
        print(f"Get Open History: {'PASS' if test9 else 'FAIL'}")
        print(f"Clear History: {'PASS' if test10 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test11 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test12 else 'FAIL'}")
        print(f"OpenMode Enum: {'PASS' if test13 else 'FAIL'}")
        print(f"Encoding Enum: {'PASS' if test14 else 'FAIL'}")
        print(f"LineEnding Enum: {'PASS' if test15 else 'FAIL'}")
        print(f"OpenConfig Dataclass: {'PASS' if test16 else 'FAIL'}")
        print(f"OpenResult Dataclass: {'PASS' if test17 else 'FAIL'}")
        
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
