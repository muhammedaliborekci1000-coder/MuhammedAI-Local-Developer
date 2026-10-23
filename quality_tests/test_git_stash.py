"""
Quality Test: Git Stash
Git stash system testleri.
"""

import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.git_stash import (
    GitStashEngine,
    StashAction,
    StashStatus,
    StashType,
    StashConfig,
    StashEntry,
    StashResult
)


def test_create_stash():
    """
    Test: Create stash.
    """
    print("=" * 70)
    print("TEST: Create Stash")
    print("=" * 70)
    
    engine = GitStashEngine()
    result = engine.create_stash("WIP: Feature work")
    
    assert result.success, "Oluşturma başarılı olmalı"
    assert result.stash_id is not None, "Stash ID olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Stash ID: {result.stash_id}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Create stash")
    print("=" * 70)


def test_create_stash_with_options():
    """
    Test: Create stash with options.
    """
    print("=" * 70)
    print("TEST: Create Stash With Options")
    print("=" * 70)
    
    engine = GitStashEngine()
    
    result = engine.create_stash(
        "WIP: Feature work",
        include_untracked=True,
        include_ignored=False,
        keep_index=True
    )
    
    assert result.success, "Oluşturma başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Stash ID: {result.stash_id}")
    
    print("\n" + "=" * 70)
    print("PASS: Create stash with options")
    print("=" * 70)


def test_list_stashes():
    """
    Test: List stashes.
    """
    print("=" * 70)
    print("TEST: List Stashes")
    print("=" * 70)
    
    engine = GitStashEngine()
    engine.create_stash("WIP: Feature 1")
    engine.create_stash("WIP: Feature 2")
    
    result = engine.list_stashes()
    
    assert result.success, "Listeleme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: List stashes")
    print("=" * 70)


def test_show_stash():
    """
    Test: Show stash.
    """
    print("=" * 70)
    print("TEST: Show Stash")
    print("=" * 70)
    
    engine = GitStashEngine()
    result = engine.create_stash("WIP: Feature work")
    stash_id = result.stash_id
    
    result = engine.show_stash(stash_id)
    
    assert result.success, "Gösterme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Show stash")
    print("=" * 70)


def test_apply_stash():
    """
    Test: Apply stash.
    """
    print("=" * 70)
    print("TEST: Apply Stash")
    print("=" * 70)
    
    engine = GitStashEngine()
    result = engine.create_stash("WIP: Feature work")
    stash_id = result.stash_id
    
    result = engine.apply_stash(stash_id)
    
    assert result.success, "Uygulama başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Apply stash")
    print("=" * 70)


def test_pop_stash():
    """
    Test: Pop stash.
    """
    print("=" * 70)
    print("TEST: Pop Stash")
    print("=" * 70)
    
    engine = GitStashEngine()
    result = engine.create_stash("WIP: Feature work")
    stash_id = result.stash_id
    
    result = engine.pop_stash(stash_id)
    
    assert result.success, "Pop başarılı olmalı"
    assert not engine.stash_exists(stash_id), "Stash silinmiş olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Pop stash")
    print("=" * 70)


def test_drop_stash():
    """
    Test: Drop stash.
    """
    print("=" * 70)
    print("TEST: Drop Stash")
    print("=" * 70)
    
    engine = GitStashEngine()
    result = engine.create_stash("WIP: Feature work")
    stash_id = result.stash_id
    
    result = engine.drop_stash(stash_id)
    
    assert result.success, "Silme başarılı olmalı"
    assert not engine.stash_exists(stash_id), "Stash silinmiş olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Drop stash")
    print("=" * 70)


def test_clear_stashes():
    """
    Test: Clear stashes.
    """
    print("=" * 70)
    print("TEST: Clear Stashes")
    print("=" * 70)
    
    engine = GitStashEngine()
    engine.create_stash("WIP: Feature 1")
    engine.create_stash("WIP: Feature 2")
    
    result = engine.clear_stashes()
    
    assert result.success, "Temizleme başarılı olmalı"
    assert engine.get_stash_count() == 0, "Tüm stashler silinmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear stashes")
    print("=" * 70)


def test_create_branch_from_stash():
    """
    Test: Create branch from stash.
    """
    print("=" * 70)
    print("TEST: Create Branch From Stash")
    print("=" * 70)
    
    engine = GitStashEngine()
    result = engine.create_stash("WIP: Feature work")
    stash_id = result.stash_id
    
    result = engine.create_branch_from_stash(stash_id, "feature/new")
    
    assert result.success, "Branch oluşturma başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Create branch from stash")
    print("=" * 70)


def test_get_stash():
    """
    Test: Get stash.
    """
    print("=" * 70)
    print("TEST: Get Stash")
    print("=" * 70)
    
    engine = GitStashEngine()
    result = engine.create_stash("WIP: Feature work")
    stash_id = result.stash_id
    
    stash = engine.get_stash(stash_id)
    
    assert stash is not None, "Stash bulunmalı"
    assert stash.id == stash_id, "Stash ID eşleşmeli"
    
    print(f"  Stash ID: {stash.id}")
    print(f"  Stash message: {stash.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Get stash")
    print("=" * 70)


def test_get_stash_count():
    """
    Test: Get stash count.
    """
    print("=" * 70)
    print("TEST: Get Stash Count")
    print("=" * 70)
    
    engine = GitStashEngine()
    engine.create_stash("WIP: Feature 1")
    engine.create_stash("WIP: Feature 2")
    
    count = engine.get_stash_count()
    
    assert count == 2, "Stash sayısı 2 olmalı"
    
    print(f"  Stash count: {count}")
    
    print("\n" + "=" * 70)
    print("PASS: Get stash count")
    print("=" * 70)


def test_stash_exists():
    """
    Test: Stash exists.
    """
    print("=" * 70)
    print("TEST: Stash Exists")
    print("=" * 70)
    
    engine = GitStashEngine()
    result = engine.create_stash("WIP: Feature work")
    stash_id = result.stash_id
    
    exists = engine.stash_exists(stash_id)
    
    assert exists == True, "Stash var olmalı"
    
    print(f"  Stash exists: {exists}")
    
    print("\n" + "=" * 70)
    print("PASS: Stash exists")
    print("=" * 70)


def test_get_stash_history():
    """
    Test: Get stash history.
    """
    print("=" * 70)
    print("TEST: Get Stash History")
    print("=" * 70)
    
    engine = GitStashEngine()
    engine.create_stash("WIP: Feature work")
    
    history = engine.get_stash_history()
    
    assert len(history) > 0, "Geçmiş olmalı"
    
    print(f"  History: {len(history)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get stash history")
    print("=" * 70)


def test_clear_history():
    """
    Test: Clear history.
    """
    print("=" * 70)
    print("TEST: Clear History")
    print("=" * 70)
    
    engine = GitStashEngine()
    engine.create_stash("WIP: Feature work")
    
    result = engine.clear_history()
    
    assert result.success, "Temizleme başarılı olmalı"
    assert len(engine.get_stash_history()) == 0, "Geçmiş temizlenmeli"
    
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
    
    engine = GitStashEngine()
    engine.create_stash("WIP: Feature work")
    
    stats = engine.get_statistics()
    
    assert stats is not None, "İstatistikler olmalı"
    assert stats["total_stashes"] == 1, "Toplam stash 1 olmalı"
    
    print(f"  Total stashes: {stats['total_stashes']}")
    print(f"  Active stashes: {stats['active_stashes']}")
    
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
    
    engine = GitStashEngine()
    
    new_config = StashConfig(include_untracked=False)
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
    
    engine = GitStashEngine()
    
    config = engine.get_config()
    
    assert config is not None, "Config olmalı"
    assert config.include_untracked == True, "Config eşleşmeli"
    
    print(f"  Include untracked: {config.include_untracked}")
    print(f"  Include ignored: {config.include_ignored}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


def test_stash_action_enum():
    """
    Test: StashAction enum.
    """
    print("=" * 70)
    print("TEST: StashAction Enum")
    print("=" * 70)
    
    assert StashAction.CREATE.value == "create"
    assert StashAction.LIST.value == "list"
    assert StashAction.SHOW.value == "show"
    assert StashAction.APPLY.value == "apply"
    assert StashAction.POP.value == "pop"
    assert StashAction.DROP.value == "drop"
    assert StashAction.CLEAR.value == "clear"
    assert StashAction.BRANCH.value == "branch"
    assert StashAction.SAVE.value == "save"
    
    print(f"  All enum values verified")
    print(f"  Total actions: {len(StashAction)}")
    
    print("\n" + "=" * 70)
    print("PASS: StashAction enum")
    print("=" * 70)


def test_stash_status_enum():
    """
    Test: StashStatus enum.
    """
    print("=" * 70)
    print("TEST: StashStatus Enum")
    print("=" * 70)
    
    assert StashStatus.ACTIVE.value == "active"
    assert StashStatus.APPLIED.value == "applied"
    assert StashStatus.DROPPED.value == "dropped"
    assert StashStatus.CONFLICT.value == "conflict"
    
    print(f"  All enum values verified")
    print(f"  Total statuses: {len(StashStatus)}")
    
    print("\n" + "=" * 70)
    print("PASS: StashStatus enum")
    print("=" * 70)


def test_stash_type_enum():
    """
    Test: StashType enum.
    """
    print("=" * 70)
    print("TEST: StashType Enum")
    print("=" * 70)
    
    assert StashType.REGULAR.value == "regular"
    assert StashType.INDEX.value == "index"
    assert StashType.UNTRACKED.value == "untracked"
    assert StashType.ALL.value == "all"
    
    print(f"  All enum values verified")
    print(f"  Total types: {len(StashType)}")
    
    print("\n" + "=" * 70)
    print("PASS: StashType enum")
    print("=" * 70)


def test_stash_config_dataclass():
    """
    Test: StashConfig dataclass.
    """
    print("=" * 70)
    print("TEST: StashConfig Dataclass")
    print("=" * 70)
    
    config = StashConfig(
        include_untracked=False,
        include_ignored=False
    )
    
    assert config.include_untracked == False, "Include untracked eşleşmeli"
    assert config.include_ignored == False, "Include ignored eşleşmeli"
    
    print(f"  Include untracked: {config.include_untracked}")
    print(f"  Include ignored: {config.include_ignored}")
    
    print("\n" + "=" * 70)
    print("PASS: StashConfig dataclass")
    print("=" * 70)


def test_stash_entry_dataclass():
    """
    Test: StashEntry dataclass.
    """
    print("=" * 70)
    print("TEST: StashEntry Dataclass")
    print("=" * 70)
    
    entry = StashEntry(
        id="stash@{0}",
        message="WIP",
        branch="main",
        commit_hash="abc123",
        author="Developer",
        date=datetime.now()
    )
    
    assert entry.id == "stash@{0}", "ID eşleşmeli"
    assert entry.message == "WIP", "Mesaj eşleşmeli"
    
    print(f"  ID: {entry.id}")
    print(f"  Message: {entry.message}")
    
    print("\n" + "=" * 70)
    print("PASS: StashEntry dataclass")
    print("=" * 70)


def test_stash_result_dataclass():
    """
    Test: StashResult dataclass.
    """
    print("=" * 70)
    print("TEST: StashResult Dataclass")
    print("=" * 70)
    
    result = StashResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: StashResult dataclass")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_create_stash()
        test2 = test_create_stash_with_options()
        test3 = test_list_stashes()
        test4 = test_show_stash()
        test5 = test_apply_stash()
        test6 = test_pop_stash()
        test7 = test_drop_stash()
        test8 = test_clear_stashes()
        test9 = test_create_branch_from_stash()
        test10 = test_get_stash()
        test11 = test_get_stash_count()
        test12 = test_stash_exists()
        test13 = test_get_stash_history()
        test14 = test_clear_history()
        test15 = test_get_statistics()
        test16 = test_update_config()
        test17 = test_get_config()
        test18 = test_stash_action_enum()
        test19 = test_stash_status_enum()
        test20 = test_stash_type_enum()
        test21 = test_stash_config_dataclass()
        test22 = test_stash_entry_dataclass()
        test23 = test_stash_result_dataclass()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Create Stash: {'PASS' if test1 else 'FAIL'}")
        print(f"Create Stash With Options: {'PASS' if test2 else 'FAIL'}")
        print(f"List Stashes: {'PASS' if test3 else 'FAIL'}")
        print(f"Show Stash: {'PASS' if test4 else 'FAIL'}")
        print(f"Apply Stash: {'PASS' if test5 else 'FAIL'}")
        print(f"Pop Stash: {'PASS' if test6 else 'FAIL'}")
        print(f"Drop Stash: {'PASS' if test7 else 'FAIL'}")
        print(f"Clear Stashes: {'PASS' if test8 else 'FAIL'}")
        print(f"Create Branch From Stash: {'PASS' if test9 else 'FAIL'}")
        print(f"Get Stash: {'PASS' if test10 else 'FAIL'}")
        print(f"Get Stash Count: {'PASS' if test11 else 'FAIL'}")
        print(f"Stash Exists: {'PASS' if test12 else 'FAIL'}")
        print(f"Get Stash History: {'PASS' if test13 else 'FAIL'}")
        print(f"Clear History: {'PASS' if test14 else 'FAIL'}")
        print(f"Get Statistics: {'PASS' if test15 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test16 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test17 else 'FAIL'}")
        print(f"StashAction Enum: {'PASS' if test18 else 'FAIL'}")
        print(f"StashStatus Enum: {'PASS' if test19 else 'FAIL'}")
        print(f"StashType Enum: {'PASS' if test20 else 'FAIL'}")
        print(f"StashConfig Dataclass: {'PASS' if test21 else 'FAIL'}")
        print(f"StashEntry Dataclass: {'PASS' if test22 else 'FAIL'}")
        print(f"StashResult Dataclass: {'PASS' if test23 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14, test15, test16, test17, test18, test19, test20, test21, test22, test23])
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
