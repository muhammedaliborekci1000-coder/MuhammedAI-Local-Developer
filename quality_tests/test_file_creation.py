"""
Quality Test: File Creation
File creation system testleri.
"""

import sys
import os
import tempfile
import shutil

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.file_creation import (
    FileCreationEngine,
    FileType,
    CreateMode,
    FileTemplate,
    CreateConfig,
    CreateResult
)


def test_create_file():
    """
    Test: Create file.
    """
    print("=" * 70)
    print("TEST: Create File")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp()
    temp_file = os.path.join(temp_dir, "test_file.txt")
    
    try:
        engine = FileCreationEngine()
        result = engine.create_file(temp_file)
        
        assert result.success, "Oluşturma başarılı olmalı"
        assert os.path.exists(temp_file), "Dosya oluşturulmalı"
        
        print(f"  Success: {result.success}")
        print(f"  Message: {result.message}")
        
        print("\n" + "=" * 70)
        print("PASS: Create file")
        print("=" * 70)
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def test_create_directory():
    """
    Test: Create directory.
    """
    print("=" * 70)
    print("TEST: Create Directory")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp()
    new_dir = os.path.join(temp_dir, "new_directory")
    
    try:
        engine = FileCreationEngine()
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


def test_create_from_content():
    """
    Test: Create from content.
    """
    print("=" * 70)
    print("TEST: Create from Content")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp()
    temp_file = os.path.join(temp_dir, "test_file.txt")
    
    try:
        engine = FileCreationEngine(CreateConfig(mode=CreateMode.FROM_CONTENT))
        result = engine.create_file(temp_file, content="Hello World")
        
        assert result.success, "Oluşturma başarılı olmalı"
        
        with open(temp_file, 'r') as f:
            content = f.read()
            assert content == "Hello World\n", "İçerik eşleşmeli"
        
        print(f"  Success: {result.success}")
        print(f"  Message: {result.message}")
        
        print("\n" + "=" * 70)
        print("PASS: Create from content")
        print("=" * 70)
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def test_create_from_template():
    """
    Test: Create from template.
    """
    print("=" * 70)
    print("TEST: Create from Template")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp()
    temp_file = os.path.join(temp_dir, "test_file.py")
    
    try:
        engine = FileCreationEngine(CreateConfig(mode=CreateMode.TEMPLATE))
        result = engine.create_file(temp_file, template_name="python")
        
        assert result.success, "Oluşturma başarılı olmalı"
        
        with open(temp_file, 'r') as f:
            content = f.read()
            assert '"""' in content, "Şablon içeriği olmalı"
        
        print(f"  Success: {result.success}")
        print(f"  Message: {result.message}")
        
        print("\n" + "=" * 70)
        print("PASS: Create from template")
        print("=" * 70)
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def test_create_multiple():
    """
    Test: Create multiple.
    """
    print("=" * 70)
    print("TEST: Create Multiple")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp()
    files = [os.path.join(temp_dir, f"file{i}.txt") for i in range(3)]
    
    try:
        engine = FileCreationEngine()
        result = engine.create_multiple(files)
        
        assert result.success, "Oluşturma başarılı olmalı"
        assert result.created_count == 3, "3 dosya oluşturulmalı"
        
        for file in files:
            assert os.path.exists(file), f"{file} oluşturulmalı"
        
        print(f"  Success: {result.success}")
        print(f"  Created count: {result.created_count}")
        
        print("\n" + "=" * 70)
        print("PASS: Create multiple")
        print("=" * 70)
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def test_add_template():
    """
    Test: Add template.
    """
    print("=" * 70)
    print("TEST: Add Template")
    print("=" * 70)
    
    engine = FileCreationEngine()
    
    result = engine.add_template("custom", "Custom template content", FileType.TEXT)
    
    assert result.success, "Ekleme başarılı olmalı"
    assert engine.get_template("custom") is not None, "Şablon eklenmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add template")
    print("=" * 70)


def test_remove_template():
    """
    Test: Remove template.
    """
    print("=" * 70)
    print("TEST: Remove Template")
    print("=" * 70)
    
    engine = FileCreationEngine()
    
    result = engine.remove_template("python")
    
    assert result.success, "Kaldırma başarılı olmalı"
    assert engine.get_template("python") is None, "Şablon kaldırılmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Remove template")
    print("=" * 70)


def test_get_template():
    """
    Test: Get template.
    """
    print("=" * 70)
    print("TEST: Get Template")
    print("=" * 70)
    
    engine = FileCreationEngine()
    
    template = engine.get_template("python")
    
    assert template is not None, "Şablon olmalı"
    assert template.name == "Python", "Şablon adı eşleşmeli"
    
    print(f"  Template name: {template.name}")
    print(f"  File type: {template.file_type.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Get template")
    print("=" * 70)


def test_get_all_templates():
    """
    Test: Get all templates.
    """
    print("=" * 70)
    print("TEST: Get All Templates")
    print("=" * 70)
    
    engine = FileCreationEngine()
    
    templates = engine.get_all_templates()
    
    assert len(templates) > 0, "Şablonlar olmalı"
    
    print(f"  Total templates: {len(templates)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get all templates")
    print("=" * 70)


def test_can_create():
    """
    Test: Can create.
    """
    print("=" * 70)
    print("TEST: Can Create")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp()
    temp_file = os.path.join(temp_dir, "test_file.txt")
    
    try:
        engine = FileCreationEngine()
        can_create = engine.can_create(temp_file)
        
        assert can_create == True, "Oluşturulabilir olmalı"
        
        print(f"  Can create: {can_create}")
        
        print("\n" + "=" * 70)
        print("PASS: Can create")
        print("=" * 70)
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def test_detect_file_type():
    """
    Test: Detect file type.
    """
    print("=" * 70)
    print("TEST: Detect File Type")
    print("=" * 70)
    
    engine = FileCreationEngine()
    
    file_type = engine.detect_file_type("test.py")
    
    assert file_type == FileType.PYTHON, "Python dosyası olmalı"
    
    print(f"  File type: {file_type.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Detect file type")
    print("=" * 70)


def test_undo_create():
    """
    Test: Undo create.
    """
    print("=" * 70)
    print("TEST: Undo Create")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp()
    temp_file = os.path.join(temp_dir, "test_file.txt")
    
    try:
        engine = FileCreationEngine()
        engine.create_file(temp_file)
        
        result = engine.undo_create(temp_file)
        
        assert result.success, "Geri alma başarılı olmalı"
        assert not os.path.exists(temp_file), "Dosya silinmeli"
        
        print(f"  Success: {result.success}")
        print(f"  Message: {result.message}")
        
        print("\n" + "=" * 70)
        print("PASS: Undo create")
        print("=" * 70)
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def test_get_create_history():
    """
    Test: Get create history.
    """
    print("=" * 70)
    print("TEST: Get Create History")
    print("=" * 70)
    
    temp_dir = tempfile.mkdtemp()
    temp_file = os.path.join(temp_dir, "test_file.txt")
    
    try:
        engine = FileCreationEngine()
        engine.create_file(temp_file)
        
        history = engine.get_create_history()
        
        assert len(history) > 0, "Geçmiş olmalı"
        
        print(f"  History: {len(history)}")
        
        print("\n" + "=" * 70)
        print("PASS: Get create history")
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
    temp_file = os.path.join(temp_dir, "test_file.txt")
    
    try:
        engine = FileCreationEngine()
        engine.create_file(temp_file)
        
        result = engine.clear_history()
        
        assert result.success, "Temizleme başarılı olmalı"
        assert len(engine.get_create_history()) == 0, "Geçmiş temizlenmeli"
        
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
    
    engine = FileCreationEngine()
    
    new_config = CreateConfig(mode=CreateMode.TEMPLATE)
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
    
    engine = FileCreationEngine()
    
    config = engine.get_config()
    
    assert config is not None, "Config olmalı"
    assert config.mode == CreateMode.EMPTY, "Config eşleşmeli"
    
    print(f"  Mode: {config.mode.value}")
    print(f"  Encoding: {config.encoding}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


def test_file_type_enum():
    """
    Test: FileType enum.
    """
    print("=" * 70)
    print("TEST: FileType Enum")
    print("=" * 70)
    
    assert FileType.TEXT.value == "text"
    assert FileType.CODE.value == "code"
    assert FileType.PYTHON.value == "python"
    assert FileType.JAVASCRIPT.value == "javascript"
    
    print(f"  All enum values verified")
    print(f"  Total types: {len(FileType)}")
    
    print("\n" + "=" * 70)
    print("PASS: FileType enum")
    print("=" * 70)


def test_create_mode_enum():
    """
    Test: CreateMode enum.
    """
    print("=" * 70)
    print("TEST: CreateMode Enum")
    print("=" * 70)
    
    assert CreateMode.EMPTY.value == "empty"
    assert CreateMode.TEMPLATE.value == "template"
    assert CreateMode.COPY.value == "copy"
    assert CreateMode.FROM_CONTENT.value == "from_content"
    
    print(f"  All enum values verified")
    print(f"  Total modes: {len(CreateMode)}")
    
    print("\n" + "=" * 70)
    print("PASS: CreateMode enum")
    print("=" * 70)


def test_file_template_dataclass():
    """
    Test: FileTemplate dataclass.
    """
    print("=" * 70)
    print("TEST: FileTemplate Dataclass")
    print("=" * 70)
    
    template = FileTemplate(
        name="Test",
        content="Test content",
        file_type=FileType.TEXT
    )
    
    assert template.name == "Test", "Name eşleşmeli"
    assert template.content == "Test content", "Content eşleşmeli"
    
    print(f"  Name: {template.name}")
    print(f"  File type: {template.file_type.value}")
    
    print("\n" + "=" * 70)
    print("PASS: FileTemplate dataclass")
    print("=" * 70)


def test_create_config_dataclass():
    """
    Test: CreateConfig dataclass.
    """
    print("=" * 70)
    print("TEST: CreateConfig Dataclass")
    print("=" * 70)
    
    config = CreateConfig(
        mode=CreateMode.TEMPLATE,
        encoding="utf-8",
        line_ending="\n"
    )
    
    assert config.mode == CreateMode.TEMPLATE, "Mode eşleşmeli"
    assert config.encoding == "utf-8", "Encoding eşleşmeli"
    
    print(f"  Mode: {config.mode.value}")
    print(f"  Encoding: {config.encoding}")
    
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
        test1 = test_create_file()
        test2 = test_create_directory()
        test3 = test_create_from_content()
        test4 = test_create_from_template()
        test5 = test_create_multiple()
        test6 = test_add_template()
        test7 = test_remove_template()
        test8 = test_get_template()
        test9 = test_get_all_templates()
        test10 = test_can_create()
        test11 = test_detect_file_type()
        test12 = test_undo_create()
        test13 = test_get_create_history()
        test14 = test_clear_history()
        test15 = test_update_config()
        test16 = test_get_config()
        test17 = test_file_type_enum()
        test18 = test_create_mode_enum()
        test19 = test_file_template_dataclass()
        test20 = test_create_config_dataclass()
        test21 = test_create_result_dataclass()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Create File: {'PASS' if test1 else 'FAIL'}")
        print(f"Create Directory: {'PASS' if test2 else 'FAIL'}")
        print(f"Create from Content: {'PASS' if test3 else 'FAIL'}")
        print(f"Create from Template: {'PASS' if test4 else 'FAIL'}")
        print(f"Create Multiple: {'PASS' if test5 else 'FAIL'}")
        print(f"Add Template: {'PASS' if test6 else 'FAIL'}")
        print(f"Remove Template: {'PASS' if test7 else 'FAIL'}")
        print(f"Get Template: {'PASS' if test8 else 'FAIL'}")
        print(f"Get All Templates: {'PASS' if test9 else 'FAIL'}")
        print(f"Can Create: {'PASS' if test10 else 'FAIL'}")
        print(f"Detect File Type: {'PASS' if test11 else 'FAIL'}")
        print(f"Undo Create: {'PASS' if test12 else 'FAIL'}")
        print(f"Get Create History: {'PASS' if test13 else 'FAIL'}")
        print(f"Clear History: {'PASS' if test14 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test15 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test16 else 'FAIL'}")
        print(f"FileType Enum: {'PASS' if test17 else 'FAIL'}")
        print(f"CreateMode Enum: {'PASS' if test18 else 'FAIL'}")
        print(f"FileTemplate Dataclass: {'PASS' if test19 else 'FAIL'}")
        print(f"CreateConfig Dataclass: {'PASS' if test20 else 'FAIL'}")
        print(f"CreateResult Dataclass: {'PASS' if test21 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14, test15, test16, test17, test18, test19, test20, test21])
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
