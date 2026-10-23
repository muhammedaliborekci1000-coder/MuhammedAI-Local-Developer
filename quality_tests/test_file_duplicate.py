"""
Quality Test: File Duplicate
File duplicate system testleri.
"""

import sys
import os
import tempfile
import shutil

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.file_duplicate import (
    FileDuplicateEngine,
    DuplicateMode,
    DuplicateScope,
    DuplicateTarget,
    DuplicateConfig,
    DuplicateResult
)


def test_duplicate_file():
    """
    Test: Duplicate file.
    """
    print("=" * 70)
    print("TEST: Duplicate File")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp()
    source_file = os.path.join(temp_dir, "source.txt")
    
    with open(source_file, 'w') as f:
        f.write("test content")
    
    try:
        engine = FileDuplicateEngine()
        result = engine.duplicate_file(source_file)
        
        assert result.success, "Çoğaltma başarılı olmalı"
        assert len(result.destination_paths) == 1, "1 hedef olmalı"
        assert os.path.exists(result.destination_paths[0]), "Çoğaltılan dosya olmalı"
        
        with open(result.destination_paths[0], 'r') as f:
            content = f.read()
            assert content == "test content", "İçerik eşleşmeli"
        
        print(f"  Success: {result.success}")
        print(f"  Message: {result.message}")
        
        print("\n" + "=" * 70)
        print("PASS: Duplicate file")
        print("=" * 70)
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def test_duplicate_directory():
    """
    Test: Duplicate directory.
    """
    print("=" * 70)
    print("TEST: Duplicate Directory")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp()
    source_dir = os.path.join(temp_dir, "source")
    
    os.makedirs(source_dir)
    with open(os.path.join(source_dir, "file.txt"), 'w') as f:
        f.write("test content")
    
    try:
        engine = FileDuplicateEngine()
        result = engine.duplicate_directory(source_dir)
        
        assert result.success, "Çoğaltma başarılı olmalı"
        assert len(result.destination_paths) == 1, "1 hedef olmalı"
        assert os.path.exists(result.destination_paths[0]), "Çoğaltılan dizin olmalı"
        assert os.path.exists(os.path.join(result.destination_paths[0], "file.txt")), "Dosya çoğaltılmalı"
        
        print(f"  Success: {result.success}")
        print(f"  Message: {result.message}")
        
        print("\n" + "=" * 70)
        print("PASS: Duplicate directory")
        print("=" * 70)
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def test_duplicate_multiple():
    """
    Test: Duplicate multiple.
    """
    print("=" * 70)
    print("TEST: Duplicate Multiple")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp()
    source_files = [os.path.join(temp_dir, f"source{i}.txt") for i in range(3)]
    
    for i, source in enumerate(source_files):
        with open(source, 'w') as f:
            f.write(f"content {i}")
    
    try:
        engine = FileDuplicateEngine()
        targets = [DuplicateTarget(source=source_files[i]) for i in range(3)]
        result = engine.duplicate_multiple(targets)
        
        assert result.success, "Çoğaltma başarılı olmalı"
        assert result.duplicated_count == 3, "3 dosya çoğaltılmalı"
        assert len(result.destination_paths) == 3, "3 hedef olmalı"
        
        for dest in result.destination_paths:
            assert os.path.exists(dest), f"{dest} çoğaltılmalı"
        
        print(f"  Success: {result.success}")
        print(f"  Duplicated count: {result.duplicated_count}")
        
        print("\n" + "=" * 70)
        print("PASS: Duplicate multiple")
        print("=" * 70)
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def test_can_duplicate():
    """
    Test: Can duplicate.
    """
    print("=" * 70)
    print("TEST: Can Duplicate")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp()
    source_file = os.path.join(temp_dir, "source.txt")
    
    with open(source_file, 'w') as f:
        f.write("test content")
    
    try:
        engine = FileDuplicateEngine()
        can_duplicate = engine.can_duplicate(source_file)
        
        assert can_duplicate == True, "Çoğaltılabilir olmalı"
        
        print(f"  Can duplicate: {can_duplicate}")
        
        print("\n" + "=" * 70)
        print("PASS: Can duplicate")
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
        engine = FileDuplicateEngine()
        size = engine.get_file_size(source_file)
        
        assert size > 0, "Boyut > 0 olmalı"
        
        print(f"  File size: {size}")
        
        print("\n" + "=" * 70)
        print("PASS: Get file size")
        print("=" * 70)
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def test_undo_duplicate():
    """
    Test: Undo duplicate.
    """
    print("=" * 70)
    print("TEST: Undo Duplicate")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp()
    source_file = os.path.join(temp_dir, "source.txt")
    
    with open(source_file, 'w') as f:
        f.write("test content")
    
    try:
        engine = FileDuplicateEngine()
        result = engine.duplicate_file(source_file)
        dest_file = result.destination_paths[0]
        
        result = engine.undo_duplicate(dest_file)
        
        assert result.success, "Geri alma başarılı olmalı"
        assert not os.path.exists(dest_file), "Çoğaltılan dosya silinmeli"
        
        print(f"  Success: {result.success}")
        print(f"  Message: {result.message}")
        
        print("\n" + "=" * 70)
        print("PASS: Undo duplicate")
        print("=" * 70)
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def test_get_duplicate_history():
    """
    Test: Get duplicate history.
    """
    print("=" * 70)
    print("TEST: Get Duplicate History")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp()
    source_file = os.path.join(temp_dir, "source.txt")
    
    with open(source_file, 'w') as f:
        f.write("test content")
    
    try:
        engine = FileDuplicateEngine()
        engine.duplicate_file(source_file)
        
        history = engine.get_duplicate_history()
        
        assert len(history) > 0, "Geçmiş olmalı"
        
        print(f"  History: {len(history)}")
        
        print("\n" + "=" * 70)
        print("PASS: Get duplicate history")
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
    
    with open(source_file, 'w') as f:
        f.write("test content")
    
    try:
        engine = FileDuplicateEngine()
        engine.duplicate_file(source_file)
        
        result = engine.clear_history()
        
        assert result.success, "Temizleme başarılı olmalı"
        assert len(engine.get_duplicate_history()) == 0, "Geçmiş temizlenmeli"
        
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
    
    engine = FileDuplicateEngine()
    
    new_config = DuplicateConfig(mode=DuplicateMode.TIMESTAMP)
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
    
    engine = FileDuplicateEngine()
    
    config = engine.get_config()
    
    assert config is not None, "Config olmalı"
    assert config.mode == DuplicateMode.NUMBERED, "Config eşleşmeli"
    
    print(f"  Mode: {config.mode.value}")
    print(f"  Preserve metadata: {config.preserve_metadata}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


def test_duplicate_mode_enum():
    """
    Test: DuplicateMode enum.
    """
    print("=" * 70)
    print("TEST: DuplicateMode Enum")
    print("=" * 70)
    
    assert DuplicateMode.NUMBERED.value == "numbered"
    assert DuplicateMode.TIMESTAMP.value == "timestamp"
    assert DuplicateMode.CUSTOM_SUFFIX.value == "custom_suffix"
    assert DuplicateMode.COPY_SUFFIX.value == "copy_suffix"
    
    print(f"  All enum values verified")
    print(f"  Total modes: {len(DuplicateMode)}")
    
    print("\n" + "=" * 70)
    print("PASS: DuplicateMode enum")
    print("=" * 70)


def test_duplicate_scope_enum():
    """
    Test: DuplicateScope enum.
    """
    print("=" * 70)
    print("TEST: DuplicateScope Enum")
    print("=" * 70)
    
    assert DuplicateScope.FILE.value == "file"
    assert DuplicateScope.DIRECTORY.value == "directory"
    assert DuplicateScope.MULTIPLE.value == "multiple"
    
    print(f"  All enum values verified")
    print(f"  Total scopes: {len(DuplicateScope)}")
    
    print("\n" + "=" * 70)
    print("PASS: DuplicateScope enum")
    print("=" * 70)


def test_duplicate_target_dataclass():
    """
    Test: DuplicateTarget dataclass.
    """
    print("=" * 70)
    print("TEST: DuplicateTarget Dataclass")
    print("=" * 70)
    
    target = DuplicateTarget(
        source="/test/source.txt",
        is_directory=False
    )
    
    assert target.source == "/test/source.txt", "Source eşleşmeli"
    assert target.is_directory == False, "Is directory eşleşmeli"
    
    print(f"  Source: {target.source}")
    print(f"  Is directory: {target.is_directory}")
    
    print("\n" + "=" * 70)
    print("PASS: DuplicateTarget dataclass")
    print("=" * 70)


def test_duplicate_config_dataclass():
    """
    Test: DuplicateConfig dataclass.
    """
    print("=" * 70)
    print("TEST: DuplicateConfig Dataclass")
    print("=" * 70)
    
    config = DuplicateConfig(
        mode=DuplicateMode.TIMESTAMP,
        custom_suffix="_backup",
        preserve_metadata=True
    )
    
    assert config.mode == DuplicateMode.TIMESTAMP, "Mode eşleşmeli"
    assert config.custom_suffix == "_backup", "Custom suffix eşleşmeli"
    assert config.preserve_metadata == True, "Preserve metadata eşleşmeli"
    
    print(f"  Mode: {config.mode.value}")
    print(f"  Custom suffix: {config.custom_suffix}")
    print(f"  Preserve metadata: {config.preserve_metadata}")
    
    print("\n" + "=" * 70)
    print("PASS: DuplicateConfig dataclass")
    print("=" * 70)


def test_duplicate_result_dataclass():
    """
    Test: DuplicateResult dataclass.
    """
    print("=" * 70)
    print("TEST: DuplicateResult Dataclass")
    print("=" * 70)
    
    result = DuplicateResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: DuplicateResult dataclass")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_duplicate_file()
        test2 = test_duplicate_directory()
        test3 = test_duplicate_multiple()
        test4 = test_can_duplicate()
        test5 = test_get_file_size()
        test6 = test_undo_duplicate()
        test7 = test_get_duplicate_history()
        test8 = test_clear_history()
        test9 = test_update_config()
        test10 = test_get_config()
        test11 = test_duplicate_mode_enum()
        test12 = test_duplicate_scope_enum()
        test13 = test_duplicate_target_dataclass()
        test14 = test_duplicate_config_dataclass()
        test15 = test_duplicate_result_dataclass()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Duplicate File: {'PASS' if test1 else 'FAIL'}")
        print(f"Duplicate Directory: {'PASS' if test2 else 'FAIL'}")
        print(f"Duplicate Multiple: {'PASS' if test3 else 'FAIL'}")
        print(f"Can Duplicate: {'PASS' if test4 else 'FAIL'}")
        print(f"Get File Size: {'PASS' if test5 else 'FAIL'}")
        print(f"Undo Duplicate: {'PASS' if test6 else 'FAIL'}")
        print(f"Get Duplicate History: {'PASS' if test7 else 'FAIL'}")
        print(f"Clear History: {'PASS' if test8 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test9 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test10 else 'FAIL'}")
        print(f"DuplicateMode Enum: {'PASS' if test11 else 'FAIL'}")
        print(f"DuplicateScope Enum: {'PASS' if test12 else 'FAIL'}")
        print(f"DuplicateTarget Dataclass: {'PASS' if test13 else 'FAIL'}")
        print(f"DuplicateConfig Dataclass: {'PASS' if test14 else 'FAIL'}")
        print(f"DuplicateResult Dataclass: {'PASS' if test15 else 'FAIL'}")
        
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
