"""
Quality Test: Directory Creation
Directory creation system testleri.
"""

import sys
import os
import tempfile
import shutil

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.directory_creation import (
    DirectoryCreationEngine,
    CreateMode,
    TemplateType,
    CreateConfig,
    CreateResult
)


def test_create_directory():
    """
    Test: Create directory.
    """
    print("=" * 70)
    print("TEST: Create Directory")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp()
    new_dir = os.path.join(temp_dir, "new_dir")
    
    try:
        engine = DirectoryCreationEngine()
        result = engine.create_directory(new_dir)
        
        assert result.success, "Oluşturma başarılı olmalı"
        assert os.path.exists(new_dir), "Dizin oluşturulmalı"
        
        print(f"  Success: {result.success}")
        print(f"  Message: {result.message}")
        
        print("\n" + "=" * 70)
        print("PASS: Create directory")
        print("=" * 70)
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def test_create_nested():
    """
    Test: Create nested directory.
    """
    print("=" * 70)
    print("TEST: Create Nested Directory")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp()
    nested_dir = os.path.join(temp_dir, "parent", "child", "grandchild")
    
    try:
        config = CreateConfig(mode=CreateMode.NESTED)
        engine = DirectoryCreationEngine(config)
        result = engine.create_directory(nested_dir)
        
        assert result.success, "Oluşturma başarılı olmalı"
        assert os.path.exists(nested_dir), "Dizin oluşturulmalı"
        
        print(f"  Success: {result.success}")
        print(f"  Message: {result.message}")
        
        print("\n" + "=" * 70)
        print("PASS: Create nested directory")
        print("=" * 70)
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def test_create_with_parents():
    """
    Test: Create directory with parents.
    """
    print("=" * 70)
    print("TEST: Create Directory With Parents")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp()
    nested_dir = os.path.join(temp_dir, "parent", "child")
    
    try:
        config = CreateConfig(mode=CreateMode.WITH_PARENTS)
        engine = DirectoryCreationEngine(config)
        result = engine.create_directory(nested_dir)
        
        assert result.success, "Oluşturma başarılı olmalı"
        assert os.path.exists(nested_dir), "Dizin oluşturulmalı"
        
        print(f"  Success: {result.success}")
        print(f"  Message: {result.message}")
        
        print("\n" + "=" * 70)
        print("PASS: Create directory with parents")
        print("=" * 70)
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def test_create_force():
    """
    Test: Create directory force.
    """
    print("=" * 70)
    print("TEST: Create Directory Force")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp()
    new_dir = os.path.join(temp_dir, "new_dir")
    
    try:
        # Create first
        os.makedirs(new_dir)
        
        # Create again with force
        config = CreateConfig(mode=CreateMode.FORCE)
        engine = DirectoryCreationEngine(config)
        result = engine.create_directory(new_dir)
        
        assert result.success, "Oluşturma başarılı olmalı"
        
        print(f"  Success: {result.success}")
        print(f"  Message: {result.message}")
        
        print("\n" + "=" * 70)
        print("PASS: Create directory force")
        print("=" * 70)
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def test_create_multiple():
    """
    Test: Create multiple directories.
    """
    print("=" * 70)
    print("TEST: Create Multiple Directories")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp()
    dir1 = os.path.join(temp_dir, "dir1")
    dir2 = os.path.join(temp_dir, "dir2")
    dir3 = os.path.join(temp_dir, "dir3")
    
    try:
        engine = DirectoryCreationEngine()
        result = engine.create_multiple([dir1, dir2, dir3])
        
        assert result.success, "Oluşturma başarılı olmalı"
        assert result.created_count == 3, "3 dizin oluşturulmalı"
        
        print(f"  Success: {result.success}")
        print(f"  Created count: {result.created_count}")
        
        print("\n" + "=" * 70)
        print("PASS: Create multiple directories")
        print("=" * 70)
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def test_can_create():
    """
    Test: Can create.
    """
    print("=" * 70)
    print("TEST: Can Create")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp()
    new_dir = os.path.join(temp_dir, "new_dir")
    
    try:
        engine = DirectoryCreationEngine()
        can_create = engine.can_create(new_dir)
        
        assert can_create == True, "Oluşturulabilir olmalı"
        
        print(f"  Can create: {can_create}")
        
        print("\n" + "=" * 70)
        print("PASS: Can create")
        print("=" * 70)
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def test_undo_creation():
    """
    Test: Undo creation.
    """
    print("=" * 70)
    print("TEST: Undo Creation")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp()
    new_dir = os.path.join(temp_dir, "new_dir")
    
    try:
        engine = DirectoryCreationEngine()
        engine.create_directory(new_dir)
        
        result = engine.undo_creation(new_dir)
        
        assert result.success, "Geri alma başarılı olmalı"
        assert not os.path.exists(new_dir), "Dizin silinmeli"
        
        print(f"  Success: {result.success}")
        print(f"  Message: {result.message}")
        
        print("\n" + "=" * 70)
        print("PASS: Undo creation")
        print("=" * 70)
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def test_get_creation_history():
    """
    Test: Get creation history.
    """
    print("=" * 70)
    print("TEST: Get Creation History")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp()
    new_dir = os.path.join(temp_dir, "new_dir")
    
    try:
        engine = DirectoryCreationEngine()
        engine.create_directory(new_dir)
        
        history = engine.get_creation_history()
        
        assert len(history) > 0, "Geçmiş olmalı"
        
        print(f"  History: {len(history)}")
        
        print("\n" + "=" * 70)
        print("PASS: Get creation history")
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
    new_dir = os.path.join(temp_dir, "new_dir")
    
    try:
        engine = DirectoryCreationEngine()
        engine.create_directory(new_dir)
        
        result = engine.clear_history()
        
        assert result.success, "Temizleme başarılı olmalı"
        assert len(engine.get_creation_history()) == 0, "Geçmiş temizlenmeli"
        
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
    
    engine = DirectoryCreationEngine()
    
    new_config = CreateConfig(mode=CreateMode.FORCE)
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
    
    engine = DirectoryCreationEngine()
    
    config = engine.get_config()
    
    assert config is not None, "Config olmalı"
    assert config.mode == CreateMode.WITH_PARENTS, "Config eşleşmeli"
    
    print(f"  Mode: {config.mode.value}")
    print(f"  Template: {config.template.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


def test_create_mode_enum():
    """
    Test: CreateMode enum.
    """
    print("=" * 70)
    print("TEST: CreateMode Enum")
    print("=" * 70)
    
    assert CreateMode.SINGLE.value == "single"
    assert CreateMode.NESTED.value == "nested"
    assert CreateMode.WITH_PARENTS.value == "with_parents"
    assert CreateMode.FORCE.value == "force"
    
    print(f"  All enum values verified")
    print(f"  Total modes: {len(CreateMode)}")
    
    print("\n" + "=" * 70)
    print("PASS: CreateMode enum")
    print("=" * 70)


def test_template_type_enum():
    """
    Test: TemplateType enum.
    """
    print("=" * 70)
    print("TEST: TemplateType Enum")
    print("=" * 70)
    
    assert TemplateType.EMPTY.value == "empty"
    assert TemplateType.GIT.value == "git"
    assert TemplateType.PYTHON.value == "python"
    assert TemplateType.JAVASCRIPT.value == "javascript"
    
    print(f"  All enum values verified")
    print(f"  Total types: {len(TemplateType)}")
    
    print("\n" + "=" * 70)
    print("PASS: TemplateType enum")
    print("=" * 70)


def test_create_config_dataclass():
    """
    Test: CreateConfig dataclass.
    """
    print("=" * 70)
    print("TEST: CreateConfig Dataclass")
    print("=" * 70)
    
    config = CreateConfig(
        mode=CreateMode.FORCE,
        template=TemplateType.PYTHON
    )
    
    assert config.mode == CreateMode.FORCE, "Mode eşleşmeli"
    assert config.template == TemplateType.PYTHON, "Template eşleşmeli"
    
    print(f"  Mode: {config.mode.value}")
    print(f"  Template: {config.template.value}")
    
    print("\n" + "=" * 70)
    print("PASS: CreateConfig dataclass")
    print("=" * 70)


def test_create_result_dataclass():
    """
    Test: CreateResult dataclass.
    """
    print("=" * 70)
    print("TEST: CreateResult Dataclass")
    print("=" * 70)
    
    result = CreateResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: CreateResult dataclass")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_create_directory()
        test2 = test_create_nested()
        test3 = test_create_with_parents()
        test4 = test_create_force()
        test5 = test_create_multiple()
        test6 = test_can_create()
        test7 = test_undo_creation()
        test8 = test_get_creation_history()
        test9 = test_clear_history()
        test10 = test_update_config()
        test11 = test_get_config()
        test12 = test_create_mode_enum()
        test13 = test_template_type_enum()
        test14 = test_create_config_dataclass()
        test15 = test_create_result_dataclass()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Create Directory: {'PASS' if test1 else 'FAIL'}")
        print(f"Create Nested: {'PASS' if test2 else 'FAIL'}")
        print(f"Create With Parents: {'PASS' if test3 else 'FAIL'}")
        print(f"Create Force: {'PASS' if test4 else 'FAIL'}")
        print(f"Create Multiple: {'PASS' if test5 else 'FAIL'}")
        print(f"Can Create: {'PASS' if test6 else 'FAIL'}")
        print(f"Undo Creation: {'PASS' if test7 else 'FAIL'}")
        print(f"Get Creation History: {'PASS' if test8 else 'FAIL'}")
        print(f"Clear History: {'PASS' if test9 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test10 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test11 else 'FAIL'}")
        print(f"CreateMode Enum: {'PASS' if test12 else 'FAIL'}")
        print(f"TemplateType Enum: {'PASS' if test13 else 'FAIL'}")
        print(f"CreateConfig Dataclass: {'PASS' if test14 else 'FAIL'}")
        print(f"CreateResult Dataclass: {'PASS' if test15 else 'FAIL'}")
        
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
