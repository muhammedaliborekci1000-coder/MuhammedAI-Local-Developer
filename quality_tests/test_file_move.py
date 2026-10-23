"""
Quality Test: File Move
File move system testleri.
"""

import sys
import os
import tempfile
import shutil

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.file_move import (
    FileMoveEngine,
    MoveMode,
    MoveScope,
    MoveTarget,
    MoveConfig,
    MoveResult
)


def test_move_file():
    """
    Test: Move file.
    """
    print("=" * 70)
    print("TEST: Move File")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp()
    source_file = os.path.join(temp_dir, "source.txt")
    dest_file = os.path.join(temp_dir, "dest.txt")
    
    with open(source_file, 'w') as f:
        f.write("test content")
    
    try:
        engine = FileMoveEngine()
        result = engine.move_file(source_file, dest_file)
        
        assert result.success, "Taşıma başarılı olmalı"
        assert not os.path.exists(source_file), "Kaynak dosya olmamalı"
        assert os.path.exists(dest_file), "Hedef dosya olmalı"
        
        with open(dest_file, 'r') as f:
            content = f.read()
            assert content == "test content", "İçerik eşleşmeli"
        
        print(f"  Success: {result.success}")
        print(f"  Message: {result.message}")
        
        print("\n" + "=" * 70)
        print("PASS: Move file")
        print("=" * 70)
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def test_move_directory():
    """
    Test: Move directory.
    """
    print("=" * 70)
    print("TEST: Move Directory")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp()
    source_dir = os.path.join(temp_dir, "source")
    dest_dir = os.path.join(temp_dir, "dest")
    
    os.makedirs(source_dir)
    with open(os.path.join(source_dir, "file.txt"), 'w') as f:
        f.write("test content")
    
    try:
        engine = FileMoveEngine()
        result = engine.move_directory(source_dir, dest_dir)
        
        assert result.success, "Taşıma başarılı olmalı"
        assert not os.path.exists(source_dir), "Kaynak dizin olmamalı"
        assert os.path.exists(dest_dir), "Hedef dizin olmalı"
        assert os.path.exists(os.path.join(dest_dir, "file.txt")), "Dosya taşınmalı"
        
        print(f"  Success: {result.success}")
        print(f"  Message: {result.message}")
        
        print("\n" + "=" * 70)
        print("PASS: Move directory")
        print("=" * 70)
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def test_move_multiple():
    """
    Test: Move multiple.
    """
    print("=" * 70)
    print("TEST: Move Multiple")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp()
    source_files = [os.path.join(temp_dir, f"source{i}.txt") for i in range(3)]
    dest_files = [os.path.join(temp_dir, f"dest{i}.txt") for i in range(3)]
    
    for i, source in enumerate(source_files):
        with open(source, 'w') as f:
            f.write(f"content {i}")
    
    try:
        engine = FileMoveEngine()
        targets = [MoveTarget(source=source_files[i], destination=dest_files[i]) for i in range(3)]
        result = engine.move_multiple(targets)
        
        assert result.success, "Taşıma başarılı olmalı"
        assert result.moved_count == 3, "3 dosya taşınmalı"
        
        for dest in dest_files:
            assert os.path.exists(dest), f"{dest} taşınmalı"
        
        for source in source_files:
            assert not os.path.exists(source), f"{source} olmamalı"
        
        print(f"  Success: {result.success}")
        print(f"  Moved count: {result.moved_count}")
        
        print("\n" + "=" * 70)
        print("PASS: Move multiple")
        print("=" * 70)
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def test_can_move():
    """
    Test: Can move.
    """
    print("=" * 70)
    print("TEST: Can Move")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp()
    source_file = os.path.join(temp_dir, "source.txt")
    dest_file = os.path.join(temp_dir, "dest.txt")
    
    with open(source_file, 'w') as f:
        f.write("test content")
    
    try:
        engine = FileMoveEngine()
        can_move = engine.can_move(source_file, dest_file)
        
        assert can_move == True, "Taşınabilir olmalı"
        
        print(f"  Can move: {can_move}")
        
        print("\n" + "=" * 70)
        print("PASS: Can move")
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
        engine = FileMoveEngine()
        size = engine.get_file_size(source_file)
        
        assert size > 0, "Boyut > 0 olmalı"
        
        print(f"  File size: {size}")
        
        print("\n" + "=" * 70)
        print("PASS: Get file size")
        print("=" * 70)
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def test_undo_move():
    """
    Test: Undo move.
    """
    print("=" * 70)
    print("TEST: Undo Move")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp()
    source_file = os.path.join(temp_dir, "source.txt")
    dest_file = os.path.join(temp_dir, "dest.txt")
    
    with open(source_file, 'w') as f:
        f.write("test content")
    
    try:
        engine = FileMoveEngine()
        engine.move_file(source_file, dest_file)
        
        result = engine.undo_move(dest_file)
        
        assert result.success, "Geri alma başarılı olmalı"
        assert os.path.exists(source_file), "Kaynak dosya geri dönmeli"
        assert not os.path.exists(dest_file), "Hedef dosya olmamalı"
        
        print(f"  Success: {result.success}")
        print(f"  Message: {result.message}")
        
        print("\n" + "=" * 70)
        print("PASS: Undo move")
        print("=" * 70)
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def test_get_move_history():
    """
    Test: Get move history.
    """
    print("=" * 70)
    print("TEST: Get Move History")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp()
    source_file = os.path.join(temp_dir, "source.txt")
    dest_file = os.path.join(temp_dir, "dest.txt")
    
    with open(source_file, 'w') as f:
        f.write("test content")
    
    try:
        engine = FileMoveEngine()
        engine.move_file(source_file, dest_file)
        
        history = engine.get_move_history()
        
        assert len(history) > 0, "Geçmiş olmalı"
        
        print(f"  History: {len(history)}")
        
        print("\n" + "=" * 70)
        print("PASS: Get move history")
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
        engine = FileMoveEngine()
        engine.move_file(source_file, dest_file)
        
        result = engine.clear_history()
        
        assert result.success, "Temizleme başarılı olmalı"
        assert len(engine.get_move_history()) == 0, "Geçmiş temizlenmeli"
        
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
    
    engine = FileMoveEngine()
    
    new_config = MoveConfig(mode=MoveMode.FORCE)
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
    
    engine = FileMoveEngine()
    
    config = engine.get_config()
    
    assert config is not None, "Config olmalı"
    assert config.mode == MoveMode.SIMPLE, "Config eşleşmeli"
    
    print(f"  Mode: {config.mode.value}")
    print(f"  Overwrite: {config.overwrite}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


def test_move_mode_enum():
    """
    Test: MoveMode enum.
    """
    print("=" * 70)
    print("TEST: MoveMode Enum")
    print("=" * 70)
    
    assert MoveMode.SIMPLE.value == "simple"
    assert MoveMode.PRESERVE_METADATA.value == "preserve_metadata"
    assert MoveMode.FORCE.value == "force"
    
    print(f"  All enum values verified")
    print(f"  Total modes: {len(MoveMode)}")
    
    print("\n" + "=" * 70)
    print("PASS: MoveMode enum")
    print("=" * 70)


def test_move_scope_enum():
    """
    Test: MoveScope enum.
    """
    print("=" * 70)
    print("TEST: MoveScope Enum")
    print("=" * 70)
    
    assert MoveScope.FILE.value == "file"
    assert MoveScope.DIRECTORY.value == "directory"
    assert MoveScope.MULTIPLE.value == "multiple"
    
    print(f"  All enum values verified")
    print(f"  Total scopes: {len(MoveScope)}")
    
    print("\n" + "=" * 70)
    print("PASS: MoveScope enum")
    print("=" * 70)


def test_move_target_dataclass():
    """
    Test: MoveTarget dataclass.
    """
    print("=" * 70)
    print("TEST: MoveTarget Dataclass")
    print("=" * 70)
    
    target = MoveTarget(
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
    print("PASS: MoveTarget dataclass")
    print("=" * 70)


def test_move_config_dataclass():
    """
    Test: MoveConfig dataclass.
    """
    print("=" * 70)
    print("TEST: MoveConfig Dataclass")
    print("=" * 70)
    
    config = MoveConfig(
        mode=MoveMode.FORCE,
        overwrite=True,
        preserve_metadata=True
    )
    
    assert config.mode == MoveMode.FORCE, "Mode eşleşmeli"
    assert config.overwrite == True, "Overwrite eşleşmeli"
    assert config.preserve_metadata == True, "Preserve metadata eşleşmeli"
    
    print(f"  Mode: {config.mode.value}")
    print(f"  Overwrite: {config.overwrite}")
    print(f"  Preserve metadata: {config.preserve_metadata}")
    
    print("\n" + "=" * 70)
    print("PASS: MoveConfig dataclass")
    print("=" * 70)


def test_move_result_dataclass():
    """
    Test: MoveResult dataclass.
    """
    print("=" * 70)
    print("TEST: MoveResult Dataclass")
    print("=" * 70)
    
    result = MoveResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: MoveResult dataclass")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_move_file()
        test2 = test_move_directory()
        test3 = test_move_multiple()
        test4 = test_can_move()
        test5 = test_get_file_size()
        test6 = test_undo_move()
        test7 = test_get_move_history()
        test8 = test_clear_history()
        test9 = test_update_config()
        test10 = test_get_config()
        test11 = test_move_mode_enum()
        test12 = test_move_scope_enum()
        test13 = test_move_target_dataclass()
        test14 = test_move_config_dataclass()
        test15 = test_move_result_dataclass()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Move File: {'PASS' if test1 else 'FAIL'}")
        print(f"Move Directory: {'PASS' if test2 else 'FAIL'}")
        print(f"Move Multiple: {'PASS' if test3 else 'FAIL'}")
        print(f"Can Move: {'PASS' if test4 else 'FAIL'}")
        print(f"Get File Size: {'PASS' if test5 else 'FAIL'}")
        print(f"Undo Move: {'PASS' if test6 else 'FAIL'}")
        print(f"Get Move History: {'PASS' if test7 else 'FAIL'}")
        print(f"Clear History: {'PASS' if test8 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test9 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test10 else 'FAIL'}")
        print(f"MoveMode Enum: {'PASS' if test11 else 'FAIL'}")
        print(f"MoveScope Enum: {'PASS' if test12 else 'FAIL'}")
        print(f"MoveTarget Dataclass: {'PASS' if test13 else 'FAIL'}")
        print(f"MoveConfig Dataclass: {'PASS' if test14 else 'FAIL'}")
        print(f"MoveResult Dataclass: {'PASS' if test15 else 'FAIL'}")
        
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
