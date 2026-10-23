"""
Quality Test: File Copy
File copy system testleri.
"""

import sys
import os
import tempfile
import shutil

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.file_copy import (
    FileCopyEngine,
    CopyMode,
    CopyScope,
    CopyTarget,
    CopyConfig,
    CopyResult
)


def test_copy_file():
    """
    Test: Copy file.
    """
    print("=" * 70)
    print("TEST: Copy File")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp()
    source_file = os.path.join(temp_dir, "source.txt")
    dest_file = os.path.join(temp_dir, "dest.txt")
    
    with open(source_file, 'w') as f:
        f.write("test content")
    
    try:
        engine = FileCopyEngine()
        result = engine.copy_file(source_file, dest_file)
        
        assert result.success, "Kopyalama başarılı olmalı"
        assert os.path.exists(dest_file), "Dosya kopyalanmalı"
        
        with open(dest_file, 'r') as f:
            content = f.read()
            assert content == "test content", "İçerik eşleşmeli"
        
        print(f"  Success: {result.success}")
        print(f"  Message: {result.message}")
        
        print("\n" + "=" * 70)
        print("PASS: Copy file")
        print("=" * 70)
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def test_copy_directory():
    """
    Test: Copy directory.
    """
    print("=" * 70)
    print("TEST: Copy Directory")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp()
    source_dir = os.path.join(temp_dir, "source")
    dest_dir = os.path.join(temp_dir, "dest")
    
    os.makedirs(source_dir)
    with open(os.path.join(source_dir, "file.txt"), 'w') as f:
        f.write("test content")
    
    try:
        engine = FileCopyEngine()
        result = engine.copy_directory(source_dir, dest_dir)
        
        assert result.success, "Kopyalama başarılı olmalı"
        assert os.path.exists(dest_dir), "Dizin kopyalanmalı"
        assert os.path.exists(os.path.join(dest_dir, "file.txt")), "Dosya kopyalanmalı"
        
        print(f"  Success: {result.success}")
        print(f"  Message: {result.message}")
        
        print("\n" + "=" * 70)
        print("PASS: Copy directory")
        print("=" * 70)
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def test_copy_multiple():
    """
    Test: Copy multiple.
    """
    print("=" * 70)
    print("TEST: Copy Multiple")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp()
    source_files = [os.path.join(temp_dir, f"source{i}.txt") for i in range(3)]
    dest_files = [os.path.join(temp_dir, f"dest{i}.txt") for i in range(3)]
    
    for i, source in enumerate(source_files):
        with open(source, 'w') as f:
            f.write(f"content {i}")
    
    try:
        engine = FileCopyEngine()
        targets = [CopyTarget(source=source_files[i], destination=dest_files[i]) for i in range(3)]
        result = engine.copy_multiple(targets)
        
        assert result.success, "Kopyalama başarılı olmalı"
        assert result.copied_count == 3, "3 dosya kopyalanmalı"
        
        for dest in dest_files:
            assert os.path.exists(dest), f"{dest} kopyalanmalı"
        
        print(f"  Success: {result.success}")
        print(f"  Copied count: {result.copied_count}")
        
        print("\n" + "=" * 70)
        print("PASS: Copy multiple")
        print("=" * 70)
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def test_can_copy():
    """
    Test: Can copy.
    """
    print("=" * 70)
    print("TEST: Can Copy")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp()
    source_file = os.path.join(temp_dir, "source.txt")
    dest_file = os.path.join(temp_dir, "dest.txt")
    
    with open(source_file, 'w') as f:
        f.write("test content")
    
    try:
        engine = FileCopyEngine()
        can_copy = engine.can_copy(source_file, dest_file)
        
        assert can_copy == True, "Kopyalanabilir olmalı"
        
        print(f"  Can copy: {can_copy}")
        
        print("\n" + "=" * 70)
        print("PASS: Can copy")
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
    source_file = os.path.join(temp_dir, "source.txt")
    
    with open(source_file, 'w') as f:
        f.write("test content")
    
    try:
        engine = FileCopyEngine()
        size = engine.get_file_size(source_file)
        
        assert size > 0, "Boyut > 0 olmalı"
        
        print(f"  File size: {size}")
        
        print("\n" + "=" * 70)
        print("PASS: Get file size")
        print("=" * 70)
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def test_undo_copy():
    """
    Test: Undo copy.
    """
    print("=" * 70)
    print("TEST: Undo Copy")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp()
    source_file = os.path.join(temp_dir, "source.txt")
    dest_file = os.path.join(temp_dir, "dest.txt")
    
    with open(source_file, 'w') as f:
        f.write("test content")
    
    try:
        engine = FileCopyEngine()
        engine.copy_file(source_file, dest_file)
        
        result = engine.undo_copy(dest_file)
        
        assert result.success, "Geri alma başarılı olmalı"
        assert not os.path.exists(dest_file), "Dosya silinmeli"
        
        print(f"  Success: {result.success}")
        print(f"  Message: {result.message}")
        
        print("\n" + "=" * 70)
        print("PASS: Undo copy")
        print("=" * 70)
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def test_get_copy_history():
    """
    Test: Get copy history.
    """
    print("=" * 70)
    print("TEST: Get Copy History")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp()
    source_file = os.path.join(temp_dir, "source.txt")
    dest_file = os.path.join(temp_dir, "dest.txt")
    
    with open(source_file, 'w') as f:
        f.write("test content")
    
    try:
        engine = FileCopyEngine()
        engine.copy_file(source_file, dest_file)
        
        history = engine.get_copy_history()
        
        assert len(history) > 0, "Geçmiş olmalı"
        
        print(f"  History: {len(history)}")
        
        print("\n" + "=" * 70)
        print("PASS: Get copy history")
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
    source_file = os.path.join(temp_dir, "source.txt")
    dest_file = os.path.join(temp_dir, "dest.txt")
    
    with open(source_file, 'w') as f:
        f.write("test content")
    
    try:
        engine = FileCopyEngine()
        engine.copy_file(source_file, dest_file)
        
        result = engine.clear_history()
        
        assert result.success, "Temizleme başarılı olmalı"
        assert len(engine.get_copy_history()) == 0, "Geçmiş temizlenmeli"
        
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
    
    engine = FileCopyEngine()
    
    new_config = CopyConfig(mode=CopyMode.DEEP)
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
    
    engine = FileCopyEngine()
    
    config = engine.get_config()
    
    assert config is not None, "Config olmalı"
    assert config.mode == CopyMode.SIMPLE, "Config eşleşmeli"
    
    print(f"  Mode: {config.mode.value}")
    print(f"  Overwrite: {config.overwrite}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


def test_copy_mode_enum():
    """
    Test: CopyMode enum.
    """
    print("=" * 70)
    print("TEST: CopyMode Enum")
    print("=" * 70)
    
    assert CopyMode.SIMPLE.value == "simple"
    assert CopyMode.DEEP.value == "deep"
    assert CopyMode.SHALLOW.value == "shallow"
    assert CopyMode.PRESERVE_METADATA.value == "preserve_metadata"
    
    print(f"  All enum values verified")
    print(f"  Total modes: {len(CopyMode)}")
    
    print("\n" + "=" * 70)
    print("PASS: CopyMode enum")
    print("=" * 70)


def test_copy_scope_enum():
    """
    Test: CopyScope enum.
    """
    print("=" * 70)
    print("TEST: CopyScope Enum")
    print("=" * 70)
    
    assert CopyScope.FILE.value == "file"
    assert CopyScope.DIRECTORY.value == "directory"
    assert CopyScope.MULTIPLE.value == "multiple"
    
    print(f"  All enum values verified")
    print(f"  Total scopes: {len(CopyScope)}")
    
    print("\n" + "=" * 70)
    print("PASS: CopyScope enum")
    print("=" * 70)


def test_copy_target_dataclass():
    """
    Test: CopyTarget dataclass.
    """
    print("=" * 70)
    print("TEST: CopyTarget Dataclass")
    print("=" * 70)
    
    target = CopyTarget(
        source="/test/source.txt",
        destination="/test/dest.txt",
        is_directory=False
    )
    
    assert target.source == "/test/source.txt", "Source eşleşmeli"
    assert target.destination == "/test/dest.txt", "Destination eşleşmeli"
    assert target.is_directory == False, "Is directory eşleşmeli"
    
    print(f"  Source: {target.source}")
    print(f"  Destination: {target.destination}")
    print(f"  Is directory: {target.is_directory}")
    
    print("\n" + "=" * 70)
    print("PASS: CopyTarget dataclass")
    print("=" * 70)


def test_copy_config_dataclass():
    """
    Test: CopyConfig dataclass.
    """
    print("=" * 70)
    print("TEST: CopyConfig Dataclass")
    print("=" * 70)
    
    config = CopyConfig(
        mode=CopyMode.DEEP,
        overwrite=True,
        preserve_metadata=True
    )
    
    assert config.mode == CopyMode.DEEP, "Mode eşleşmeli"
    assert config.overwrite == True, "Overwrite eşleşmeli"
    assert config.preserve_metadata == True, "Preserve metadata eşleşmeli"
    
    print(f"  Mode: {config.mode.value}")
    print(f"  Overwrite: {config.overwrite}")
    print(f"  Preserve metadata: {config.preserve_metadata}")
    
    print("\n" + "=" * 70)
    print("PASS: CopyConfig dataclass")
    print("=" * 70)


def test_copy_result_dataclass():
    """
    Test: CopyResult dataclass.
    """
    print("=" * 70)
    print("TEST: CopyResult Dataclass")
    print("=" * 70)
    
    result = CopyResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: CopyResult dataclass")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_copy_file()
        test2 = test_copy_directory()
        test3 = test_copy_multiple()
        test4 = test_can_copy()
        test5 = test_get_file_size()
        test6 = test_undo_copy()
        test7 = test_get_copy_history()
        test8 = test_clear_history()
        test9 = test_update_config()
        test10 = test_get_config()
        test11 = test_copy_mode_enum()
        test12 = test_copy_scope_enum()
        test13 = test_copy_target_dataclass()
        test14 = test_copy_config_dataclass()
        test15 = test_copy_result_dataclass()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Copy File: {'PASS' if test1 else 'FAIL'}")
        print(f"Copy Directory: {'PASS' if test2 else 'FAIL'}")
        print(f"Copy Multiple: {'PASS' if test3 else 'FAIL'}")
        print(f"Can Copy: {'PASS' if test4 else 'FAIL'}")
        print(f"Get File Size: {'PASS' if test5 else 'FAIL'}")
        print(f"Undo Copy: {'PASS' if test6 else 'FAIL'}")
        print(f"Get Copy History: {'PASS' if test7 else 'FAIL'}")
        print(f"Clear History: {'PASS' if test8 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test9 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test10 else 'FAIL'}")
        print(f"CopyMode Enum: {'PASS' if test11 else 'FAIL'}")
        print(f"CopyScope Enum: {'PASS' if test12 else 'FAIL'}")
        print(f"CopyTarget Dataclass: {'PASS' if test13 else 'FAIL'}")
        print(f"CopyConfig Dataclass: {'PASS' if test14 else 'FAIL'}")
        print(f"CopyResult Dataclass: {'PASS' if test15 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14, test15])
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
