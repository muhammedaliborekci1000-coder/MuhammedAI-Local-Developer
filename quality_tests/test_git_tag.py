"""
Quality Test: Git Tag
Git tag system testleri.
"""

import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.git_tag import (
    GitTagEngine,
    TagType,
    TagAction,
    TagScope,
    TagConfig,
    TagInfo,
    TagResult
)


def test_create_tag():
    """
    Test: Create tag.
    """
    print("=" * 70)
    print("TEST: Create Tag")
    print("=" * 70)
    
    engine = GitTagEngine()
    result = engine.create_tag("v1.0.0", "abc123")
    
    assert result.success, "Oluşturma başarılı olmalı"
    assert result.tag_name == "v1.0.0", "Tag adı eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Tag name: {result.tag_name}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Create tag")
    print("=" * 70)


def test_create_annotated_tag():
    """
    Test: Create annotated tag.
    """
    print("=" * 70)
    print("TEST: Create Annotated Tag")
    print("=" * 70)
    
    engine = GitTagEngine()
    result = engine.create_tag("v1.0.0", "abc123", "Version 1.0.0", TagType.ANNOTATED)
    
    assert result.success, "Oluşturma başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Tag name: {result.tag_name}")
    
    print("\n" + "=" * 70)
    print("PASS: Create annotated tag")
    print("=" * 70)


def test_delete_tag():
    """
    Test: Delete tag.
    """
    print("=" * 70)
    print("TEST: Delete Tag")
    print("=" * 70)
    
    engine = GitTagEngine()
    engine.create_tag("v1.0.0", "abc123")
    
    result = engine.delete_tag("v1.0.0")
    
    assert result.success, "Silme başarılı olmalı"
    assert not engine.tag_exists("v1.0.0"), "Tag silinmiş olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Delete tag")
    print("=" * 70)


def test_list_tags():
    """
    Test: List tags.
    """
    print("=" * 70)
    print("TEST: List Tags")
    print("=" * 70)
    
    engine = GitTagEngine()
    engine.create_tag("v1.0.0", "abc123")
    engine.create_tag("v2.0.0", "def456")
    
    result = engine.list_tags()
    
    assert result.success, "Listeleme başarılı olmalı"
    assert result.total_tags == 2, "2 tag olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Total tags: {result.total_tags}")
    
    print("\n" + "=" * 70)
    print("PASS: List tags")
    print("=" * 70)


def test_list_tags_by_type():
    """
    Test: List tags by type.
    """
    print("=" * 70)
    print("TEST: List Tags By Type")
    print("=" * 70)
    
    engine = GitTagEngine()
    engine.create_tag("v1.0.0", "abc123", tag_type=TagType.ANNOTATED)
    engine.create_tag("v2.0.0", "def456", tag_type=TagType.LIGHTWEIGHT)
    
    result = engine.list_tags(tag_type=TagType.ANNOTATED)
    
    assert result.success, "Listeleme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Total tags: {result.total_tags}")
    
    print("\n" + "=" * 70)
    print("PASS: List tags by type")
    print("=" * 70)


def test_show_tag():
    """
    Test: Show tag.
    """
    print("=" * 70)
    print("TEST: Show Tag")
    print("=" * 70)
    
    engine = GitTagEngine()
    engine.create_tag("v1.0.0", "abc123", "Version 1.0.0")
    
    result = engine.show_tag("v1.0.0")
    
    assert result.success, "Gösterme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Show tag")
    print("=" * 70)


def test_push_tag():
    """
    Test: Push tag.
    """
    print("=" * 70)
    print("TEST: Push Tag")
    print("=" * 70)
    
    engine = GitTagEngine()
    engine.create_tag("v1.0.0", "abc123")
    
    result = engine.push_tag("v1.0.0")
    
    assert result.success, "Push başarılı olmalı"
    assert result.action == TagAction.PUSH.value, "Action eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Push tag")
    print("=" * 70)


def test_fetch_tags():
    """
    Test: Fetch tags.
    """
    print("=" * 70)
    print("TEST: Fetch Tags")
    print("=" * 70)
    
    engine = GitTagEngine()
    
    result = engine.fetch_tags()
    
    assert result.success, "Fetch başarılı olmalı"
    assert result.action == TagAction.FETCH.value, "Action eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Fetch tags")
    print("=" * 70)


def test_verify_tag():
    """
    Test: Verify tag.
    """
    print("=" * 70)
    print("TEST: Verify Tag")
    print("=" * 70)
    
    engine = GitTagEngine()
    engine.create_tag("v1.0.0", "abc123", sign=True)
    
    result = engine.verify_tag("v1.0.0")
    
    assert result.success, "Doğrulama başarılı olmalı"
    assert result.action == TagAction.VERIFY.value, "Action eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Verify tag")
    print("=" * 70)


def test_checkout_tag():
    """
    Test: Checkout tag.
    """
    print("=" * 70)
    print("TEST: Checkout Tag")
    print("=" * 70)
    
    engine = GitTagEngine()
    engine.create_tag("v1.0.0", "abc123")
    
    result = engine.checkout_tag("v1.0.0")
    
    assert result.success, "Checkout başarılı olmalı"
    assert result.action == TagAction.CHECKOUT.value, "Action eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Checkout tag")
    print("=" * 70)


def test_rename_tag():
    """
    Test: Rename tag.
    """
    print("=" * 70)
    print("TEST: Rename Tag")
    print("=" * 70)
    
    engine = GitTagEngine()
    engine.create_tag("v1.0.0", "abc123")
    
    result = engine.rename_tag("v1.0.0", "v1.0.1")
    
    assert result.success, "Yeniden adlandırma başarılı olmalı"
    assert not engine.tag_exists("v1.0.0"), "Eski ad silinmeli"
    assert engine.tag_exists("v1.0.1"), "Yeni ad olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Rename tag")
    print("=" * 70)


def test_get_tag():
    """
    Test: Get tag.
    """
    print("=" * 70)
    print("TEST: Get Tag")
    print("=" * 70)
    
    engine = GitTagEngine()
    engine.create_tag("v1.0.0", "abc123", "Version 1.0.0")
    
    tag = engine.get_tag("v1.0.0")
    
    assert tag is not None, "Tag bulunmalı"
    assert tag.name == "v1.0.0", "Tag adı eşleşmeli"
    
    print(f"  Tag name: {tag.name}")
    print(f"  Tag message: {tag.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Get tag")
    print("=" * 70)


def test_get_tag_count():
    """
    Test: Get tag count.
    """
    print("=" * 70)
    print("TEST: Get Tag Count")
    print("=" * 70)
    
    engine = GitTagEngine()
    engine.create_tag("v1.0.0", "abc123")
    engine.create_tag("v2.0.0", "def456")
    
    count = engine.get_tag_count()
    
    assert count == 2, "Tag sayısı 2 olmalı"
    
    print(f"  Tag count: {count}")
    
    print("\n" + "=" * 70)
    print("PASS: Get tag count")
    print("=" * 70)


def test_tag_exists():
    """
    Test: Tag exists.
    """
    print("=" * 70)
    print("TEST: Tag Exists")
    print("=" * 70)
    
    engine = GitTagEngine()
    engine.create_tag("v1.0.0", "abc123")
    
    exists = engine.tag_exists("v1.0.0")
    
    assert exists == True, "Tag var olmalı"
    
    print(f"  Tag exists: {exists}")
    
    print("\n" + "=" * 70)
    print("PASS: Tag exists")
    print("=" * 70)


def test_get_tag_history():
    """
    Test: Get tag history.
    """
    print("=" * 70)
    print("TEST: Get Tag History")
    print("=" * 70)
    
    engine = GitTagEngine()
    engine.create_tag("v1.0.0", "abc123")
    
    history = engine.get_tag_history()
    
    assert len(history) > 0, "Geçmiş olmalı"
    
    print(f"  History: {len(history)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get tag history")
    print("=" * 70)


def test_clear_history():
    """
    Test: Clear history.
    """
    print("=" * 70)
    print("TEST: Clear History")
    print("=" * 70)
    
    engine = GitTagEngine()
    engine.create_tag("v1.0.0", "abc123")
    
    result = engine.clear_history()
    
    assert result.success, "Temizleme başarılı olmalı"
    assert len(engine.get_tag_history()) == 0, "Geçmiş temizlenmeli"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear history")
    print("=" * 70)


def test_get_statistics():
    """
    Test: Get statistics.
    """
    print("=" * 70)
    print("TEST: Get Statistics")
    print("=" * 70)
    
    engine = GitTagEngine()
    engine.create_tag("v1.0.0", "abc123")
    engine.create_tag("v2.0.0", "def456", tag_type=TagType.ANNOTATED)
    
    stats = engine.get_statistics()
    
    assert stats is not None, "İstatistikler olmalı"
    assert stats["total_tags"] == 2, "Toplam tag 2 olmalı"
    
    print(f"  Total tags: {stats['total_tags']}")
    print(f"  Lightweight: {stats['lightweight']}")
    print(f"  Annotated: {stats['annotated']}")
    
    print("\n" + "=" * 70)
    print("PASS: Get statistics")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    engine = GitTagEngine()
    
    new_config = TagConfig(auto_push=False)
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
    
    engine = GitTagEngine()
    
    config = engine.get_config()
    
    assert config is not None, "Config olmalı"
    assert config.auto_push == False, "Config eşleşmeli"
    
    print(f"  Auto push: {config.auto_push}")
    print(f"  Sign tags: {config.sign_tags}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


def test_tag_type_enum():
    """
    Test: TagType enum.
    """
    print("=" * 70)
    print("TEST: TagType Enum")
    print("=" * 70)
    
    assert TagType.LIGHTWEIGHT.value == "lightweight"
    assert TagType.ANNOTATED.value == "annotated"
    assert TagType.SIGNED.value == "signed"
    
    print(f"  All enum values verified")
    print(f"  Total types: {len(TagType)}")
    
    print("\n" + "=" * 70)
    print("PASS: TagType enum")
    print("=" * 70)


def test_tag_action_enum():
    """
    Test: TagAction enum.
    """
    print("=" * 70)
    print("TEST: TagAction Enum")
    print("=" * 70)
    
    assert TagAction.CREATE.value == "create"
    assert TagAction.DELETE.value == "delete"
    assert TagAction.LIST.value == "list"
    assert TagAction.SHOW.value == "show"
    assert TagAction.PUSH.value == "push"
    assert TagAction.FETCH.value == "fetch"
    assert TagAction.VERIFY.value == "verify"
    assert TagAction.CHECKOUT.value == "checkout"
    assert TagAction.RENAME.value == "rename"
    
    print(f"  All enum values verified")
    print(f"  Total actions: {len(TagAction)}")
    
    print("\n" + "=" * 70)
    print("PASS: TagAction enum")
    print("=" * 70)


def test_tag_scope_enum():
    """
    Test: TagScope enum.
    """
    print("=" * 70)
    print("TEST: TagScope Enum")
    print("=" * 70)
    
    assert TagScope.LOCAL.value == "local"
    assert TagScope.REMOTE.value == "remote"
    assert TagScope.ALL.value == "all"
    
    print(f"  All enum values verified")
    print(f"  Total scopes: {len(TagScope)}")
    
    print("\n" + "=" * 70)
    print("PASS: TagScope enum")
    print("=" * 70)


def test_tag_config_dataclass():
    """
    Test: TagConfig dataclass.
    """
    print("=" * 70)
    print("TEST: TagConfig Dataclass")
    print("=" * 70)
    
    config = TagConfig(
        auto_push=False,
        sign_tags=False
    )
    
    assert config.auto_push == False, "Auto push eşleşmeli"
    assert config.sign_tags == False, "Sign tags eşleşmeli"
    
    print(f"  Auto push: {config.auto_push}")
    print(f"  Sign tags: {config.sign_tags}")
    
    print("\n" + "=" * 70)
    print("PASS: TagConfig dataclass")
    print("=" * 70)


def test_tag_info_dataclass():
    """
    Test: TagInfo dataclass.
    """
    print("=" * 70)
    print("TEST: TagInfo Dataclass")
    print("=" * 70)
    
    tag = TagInfo(
        name="v1.0.0",
        tag_type=TagType.ANNOTATED,
        commit_hash="abc123",
        message="Version 1.0.0",
        author="Dev",
        date=datetime.now()
    )
    
    assert tag.name == "v1.0.0", "Name eşleşmeli"
    assert tag.message == "Version 1.0.0", "Message eşleşmeli"
    
    print(f"  Name: {tag.name}")
    print(f"  Message: {tag.message}")
    
    print("\n" + "=" * 70)
    print("PASS: TagInfo dataclass")
    print("=" * 70)


def test_tag_result_dataclass():
    """
    Test: TagResult dataclass.
    """
    print("=" * 70)
    print("TEST: TagResult Dataclass")
    print("=" * 70)
    
    result = TagResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: TagResult dataclass")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_create_tag()
        test2 = test_create_annotated_tag()
        test3 = test_delete_tag()
        test4 = test_list_tags()
        test5 = test_list_tags_by_type()
        test6 = test_show_tag()
        test7 = test_push_tag()
        test8 = test_fetch_tags()
        test9 = test_verify_tag()
        test10 = test_checkout_tag()
        test11 = test_rename_tag()
        test12 = test_get_tag()
        test13 = test_get_tag_count()
        test14 = test_tag_exists()
        test15 = test_get_tag_history()
        test16 = test_clear_history()
        test17 = test_get_statistics()
        test18 = test_update_config()
        test19 = test_get_config()
        test20 = test_tag_type_enum()
        test21 = test_tag_action_enum()
        test22 = test_tag_scope_enum()
        test23 = test_tag_config_dataclass()
        test24 = test_tag_info_dataclass()
        test25 = test_tag_result_dataclass()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Create Tag: {'PASS' if test1 else 'FAIL'}")
        print(f"Create Annotated Tag: {'PASS' if test2 else 'FAIL'}")
        print(f"Delete Tag: {'PASS' if test3 else 'FAIL'}")
        print(f"List Tags: {'PASS' if test4 else 'FAIL'}")
        print(f"List Tags By Type: {'PASS' if test5 else 'FAIL'}")
        print(f"Show Tag: {'PASS' if test6 else 'FAIL'}")
        print(f"Push Tag: {'PASS' if test7 else 'FAIL'}")
        print(f"Fetch Tags: {'PASS' if test8 else 'FAIL'}")
        print(f"Verify Tag: {'PASS' if test9 else 'FAIL'}")
        print(f"Checkout Tag: {'PASS' if test10 else 'FAIL'}")
        print(f"Rename Tag: {'PASS' if test11 else 'FAIL'}")
        print(f"Get Tag: {'PASS' if test12 else 'FAIL'}")
        print(f"Get Tag Count: {'PASS' if test13 else 'FAIL'}")
        print(f"Tag Exists: {'PASS' if test14 else 'FAIL'}")
        print(f"Get Tag History: {'PASS' if test15 else 'FAIL'}")
        print(f"Clear History: {'PASS' if test16 else 'FAIL'}")
        print(f"Get Statistics: {'PASS' if test17 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test18 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test19 else 'FAIL'}")
        print(f"TagType Enum: {'PASS' if test20 else 'FAIL'}")
        print(f"TagAction Enum: {'PASS' if test21 else 'FAIL'}")
        print(f"TagScope Enum: {'PASS' if test22 else 'FAIL'}")
        print(f"TagConfig Dataclass: {'PASS' if test23 else 'FAIL'}")
        print(f"TagInfo Dataclass: {'PASS' if test24 else 'FAIL'}")
        print(f"TagResult Dataclass: {'PASS' if test25 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14, test15, test16, test17, test18, test19, test20, test21, test22, test23, test24, test25])
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
