"""
Quality Test: Git Branch
Git branch system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.git_branch import (
    GitBranchEngine,
    BranchType,
    BranchStatus,
    Branch,
    BranchConfig,
    BranchResult
)
from datetime import datetime


def test_create_branch():
    """
    Test: Create branch.
    """
    print("=" * 70)
    print("TEST: Create Branch")
    print("=" * 70)
    
    engine = GitBranchEngine()
    
    result = engine.create_branch("feature/test")
    
    assert result.success, "Branch oluşturma başarılı olmalı"
    assert result.total_branches == 1, "1 branch olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Total branches: {result.total_branches}")
    
    print("\n" + "=" * 70)
    print("PASS: Create branch")
    print("=" * 70)


def test_delete_branch():
    """
    Test: Delete branch.
    """
    print("=" * 70)
    print("TEST: Delete Branch")
    print("=" * 70)
    
    engine = GitBranchEngine()
    
    engine.create_branch("feature/test")
    result = engine.delete_branch("feature/test")
    
    assert result.success, "Branch silme başarılı olmalı"
    assert result.total_branches == 0, "0 branch olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Total branches: {result.total_branches}")
    
    print("\n" + "=" * 70)
    print("PASS: Delete branch")
    print("=" * 70)


def test_switch_branch():
    """
    Test: Switch branch.
    """
    print("=" * 70)
    print("TEST: Switch Branch")
    print("=" * 70)
    
    engine = GitBranchEngine()
    
    engine.create_branch("feature/test")
    result = engine.switch_branch("feature/test")
    
    assert result.success, "Branch değiştirme başarılı olmalı"
    assert result.current_branch == "feature/test", "Current branch eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Current branch: {result.current_branch}")
    
    print("\n" + "=" * 70)
    print("PASS: Switch branch")
    print("=" * 70)


def test_list_branches():
    """
    Test: List branches.
    """
    print("=" * 70)
    print("TEST: List Branches")
    print("=" * 70)
    
    engine = GitBranchEngine()
    
    engine.create_branch("feature/test")
    engine.create_branch("feature/test2")
    
    result = engine.list_branches()
    
    assert result.success, "Listeleme başarılı olmalı"
    assert result.total_branches == 2, "2 branch olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Total branches: {result.total_branches}")
    
    print("\n" + "=" * 70)
    print("PASS: List branches")
    print("=" * 70)


def test_get_current_branch():
    """
    Test: Get current branch.
    """
    print("=" * 70)
    print("TEST: Get Current Branch")
    print("=" * 70)
    
    engine = GitBranchEngine()
    
    engine.create_branch("feature/test")
    engine.switch_branch("feature/test")
    
    current = engine.get_current_branch()
    
    assert current == "feature/test", "Current branch eşleşmeli"
    
    print(f"  Current branch: {current}")
    
    print("\n" + "=" * 70)
    print("PASS: Get current branch")
    print("=" * 70)


def test_get_branch():
    """
    Test: Get branch.
    """
    print("=" * 70)
    print("TEST: Get Branch")
    print("=" * 70)
    
    engine = GitBranchEngine()
    
    engine.create_branch("feature/test")
    branch = engine.get_branch("feature/test")
    
    assert branch is not None, "Branch olmalı"
    assert branch.name == "feature/test", "Branch adı eşleşmeli"
    
    print(f"  Branch name: {branch.name}")
    
    print("\n" + "=" * 70)
    print("PASS: Get branch")
    print("=" * 70)


def test_rename_branch():
    """
    Test: Rename branch.
    """
    print("=" * 70)
    print("TEST: Rename Branch")
    print("=" * 70)
    
    engine = GitBranchEngine()
    
    engine.create_branch("feature/test")
    result = engine.rename_branch("feature/test", "feature/new")
    
    assert result.success, "Yeniden adlandırma başarılı olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Rename branch")
    print("=" * 70)


def test_compare_branches():
    """
    Test: Compare branches.
    """
    print("=" * 70)
    print("TEST: Compare Branches")
    print("=" * 70)
    
    engine = GitBranchEngine()
    
    engine.create_branch("feature/test")
    engine.create_branch("feature/test2")
    
    result = engine.compare_branches("feature/test", "feature/test2")
    
    assert result.success, "Karşılaştırma başarılı olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Compare branches")
    print("=" * 70)


def test_get_branch_history():
    """
    Test: Get branch history.
    """
    print("=" * 70)
    print("TEST: Get Branch History")
    print("=" * 70)
    
    engine = GitBranchEngine()
    
    engine.create_branch("feature/test")
    engine.switch_branch("feature/test")
    
    history = engine.get_branch_history()
    
    assert len(history) > 0, "Geçmiş olmalı"
    
    print(f"  History: {history}")
    
    print("\n" + "=" * 70)
    print("PASS: Get branch history")
    print("=" * 70)


def test_clear_history():
    """
    Test: Clear history.
    """
    print("=" * 70)
    print("TEST: Clear History")
    print("=" * 70)
    
    engine = GitBranchEngine()
    
    engine.create_branch("feature/test")
    result = engine.clear_history()
    
    assert result.success, "Temizleme başarılı olmalı"
    assert len(engine.get_branch_history()) == 0, "Geçmiş temizlenmeli"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear history")
    print("=" * 70)


def test_get_branch_count():
    """
    Test: Get branch count.
    """
    print("=" * 70)
    print("TEST: Get Branch Count")
    print("=" * 70)
    
    engine = GitBranchEngine()
    
    engine.create_branch("feature/test")
    engine.create_branch("feature/test2")
    
    count = engine.get_branch_count()
    
    assert count == 2, "2 branch olmalı"
    
    print(f"  Branch count: {count}")
    
    print("\n" + "=" * 70)
    print("PASS: Get branch count")
    print("=" * 70)


def test_branch_exists():
    """
    Test: Branch exists.
    """
    print("=" * 70)
    print("TEST: Branch Exists")
    print("=" * 70)
    
    engine = GitBranchEngine()
    
    engine.create_branch("feature/test")
    
    exists = engine.branch_exists("feature/test")
    
    assert exists == True, "Branch var olmalı"
    
    print(f"  Exists: {exists}")
    
    print("\n" + "=" * 70)
    print("PASS: Branch exists")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    engine = GitBranchEngine()
    
    new_config = BranchConfig(protect_main=False)
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
    
    engine = GitBranchEngine()
    
    config = engine.get_config()
    
    assert config is not None, "Config olmalı"
    assert config.protect_main == True, "Config eşleşmeli"
    
    print(f"  Protect main: {config.protect_main}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


def test_branch_type_enum():
    """
    Test: BranchType enum.
    """
    print("=" * 70)
    print("TEST: BranchType Enum")
    print("=" * 70)
    
    assert BranchType.LOCAL.value == "local"
    assert BranchType.REMOTE.value == "remote"
    assert BranchType.TRACKING.value == "tracking"
    assert BranchType.DETACHED.value == "detached"
    
    print(f"  All enum values verified")
    print(f"  Total types: {len(BranchType)}")
    
    print("\n" + "=" * 70)
    print("PASS: BranchType enum")
    print("=" * 70)


def test_branch_status_enum():
    """
    Test: BranchStatus enum.
    """
    print("=" * 70)
    print("TEST: BranchStatus Enum")
    print("=" * 70)
    
    assert BranchStatus.ACTIVE.value == "active"
    assert BranchStatus.INACTIVE.value == "inactive"
    assert BranchStatus.AHEAD.value == "ahead"
    assert BranchStatus.BEHIND.value == "behind"
    assert BranchStatus.DIVERGED.value == "diverged"
    assert BranchStatus.UP_TO_DATE.value == "up_to_date"
    
    print(f"  All enum values verified")
    print(f"  Total statuses: {len(BranchStatus)}")
    
    print("\n" + "=" * 70)
    print("PASS: BranchStatus enum")
    print("=" * 70)


def test_branch_dataclass():
    """
    Test: Branch dataclass.
    """
    print("=" * 70)
    print("TEST: Branch Dataclass")
    print("=" * 70)
    
    branch = Branch(
        name="feature/test",
        branch_type=BranchType.LOCAL,
        status=BranchStatus.INACTIVE,
        commit_hash="abc123",
        commit_message="Test commit",
        author="Developer",
        created_at=datetime.now(),
        last_commit_at=datetime.now()
    )
    
    assert branch.name == "feature/test", "Name eşleşmeli"
    assert branch.branch_type == BranchType.LOCAL, "Type eşleşmeli"
    
    print(f"  Name: {branch.name}")
    print(f"  Type: {branch.branch_type.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Branch dataclass")
    print("=" * 70)


def test_branch_config_dataclass():
    """
    Test: BranchConfig dataclass.
    """
    print("=" * 70)
    print("TEST: BranchConfig Dataclass")
    print("=" * 70)
    
    config = BranchConfig(
        auto_create_tracking=True,
        show_remote_branches=True,
        protect_main=True
    )
    
    assert config.auto_create_tracking == True, "Auto create tracking eşleşmeli"
    assert config.show_remote_branches == True, "Show remote branches eşleşmeli"
    assert config.protect_main == True, "Protect main eşleşmeli"
    
    print(f"  Auto create tracking: {config.auto_create_tracking}")
    print(f"  Show remote branches: {config.show_remote_branches}")
    print(f"  Protect main: {config.protect_main}")
    
    print("\n" + "=" * 70)
    print("PASS: BranchConfig dataclass")
    print("=" * 70)


def test_branch_result_dataclass():
    """
    Test: BranchResult dataclass.
    """
    print("=" * 70)
    print("TEST: BranchResult Dataclass")
    print("=" * 70)
    
    result = BranchResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.branches, list), "Branches list olmalı"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Branches: {len(result.branches)}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: BranchResult dataclass")
    print("=" * 70)


def test_create_duplicate_branch():
    """
    Test: Create duplicate branch.
    """
    print("=" * 70)
    print("TEST: Create Duplicate Branch")
    print("=" * 70)
    
    engine = GitBranchEngine()
    
    engine.create_branch("feature/test")
    result = engine.create_branch("feature/test")
    
    assert result.success == False, "Başarısız olmalı"
    assert len(result.errors) > 0, "Hata olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Errors: {result.errors}")
    
    print("\n" + "=" * 70)
    print("PASS: Create duplicate branch")
    print("=" * 70)


def test_delete_protected_branch():
    """
    Test: Delete protected branch.
    """
    print("=" * 70)
    print("TEST: Delete Protected Branch")
    print("=" * 70)
    
    engine = GitBranchEngine()
    
    engine.create_branch("main")
    result = engine.delete_branch("main")
    
    assert result.success == False, "Başarısız olmalı"
    assert len(result.errors) > 0, "Hata olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Errors: {result.errors}")
    
    print("\n" + "=" * 70)
    print("PASS: Delete protected branch")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_create_branch()
        test2 = test_delete_branch()
        test3 = test_switch_branch()
        test4 = test_list_branches()
        test5 = test_get_current_branch()
        test6 = test_get_branch()
        test7 = test_rename_branch()
        test8 = test_compare_branches()
        test9 = test_get_branch_history()
        test10 = test_clear_history()
        test11 = test_get_branch_count()
        test12 = test_branch_exists()
        test13 = test_update_config()
        test14 = test_get_config()
        test15 = test_branch_type_enum()
        test16 = test_branch_status_enum()
        test17 = test_branch_dataclass()
        test18 = test_branch_config_dataclass()
        test19 = test_branch_result_dataclass()
        test20 = test_create_duplicate_branch()
        test21 = test_delete_protected_branch()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Create Branch: {'PASS' if test1 else 'FAIL'}")
        print(f"Delete Branch: {'PASS' if test2 else 'FAIL'}")
        print(f"Switch Branch: {'PASS' if test3 else 'FAIL'}")
        print(f"List Branches: {'PASS' if test4 else 'FAIL'}")
        print(f"Get Current Branch: {'PASS' if test5 else 'FAIL'}")
        print(f"Get Branch: {'PASS' if test6 else 'FAIL'}")
        print(f"Rename Branch: {'PASS' if test7 else 'FAIL'}")
        print(f"Compare Branches: {'PASS' if test8 else 'FAIL'}")
        print(f"Get Branch History: {'PASS' if test9 else 'FAIL'}")
        print(f"Clear History: {'PASS' if test10 else 'FAIL'}")
        print(f"Get Branch Count: {'PASS' if test11 else 'FAIL'}")
        print(f"Branch Exists: {'PASS' if test12 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test13 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test14 else 'FAIL'}")
        print(f"BranchType Enum: {'PASS' if test15 else 'FAIL'}")
        print(f"BranchStatus Enum: {'PASS' if test16 else 'FAIL'}")
        print(f"Branch Dataclass: {'PASS' if test17 else 'FAIL'}")
        print(f"BranchConfig Dataclass: {'PASS' if test18 else 'FAIL'}")
        print(f"BranchResult Dataclass: {'PASS' if test19 else 'FAIL'}")
        print(f"Create Duplicate Branch: {'PASS' if test20 else 'FAIL'}")
        print(f"Delete Protected Branch: {'PASS' if test21 else 'FAIL'}")
        
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
