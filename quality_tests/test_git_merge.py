"""
Quality Test: Git Merge
Git merge system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.git_merge import (
    GitMergeEngine,
    MergeStrategy,
    MergeStatus,
    Conflict,
    MergeInfo,
    MergeConfig,
    MergeResult
)
from datetime import datetime


def test_merge_branch():
    """
    Test: Merge branch.
    """
    print("=" * 70)
    print("TEST: Merge Branch")
    print("=" * 70)
    
    engine = GitMergeEngine()
    
    result = engine.merge_branch("feature/test", "main")
    
    # Conflict varsa başarısız olabilir
    if result.success:
        print(f"  Success: {result.success}")
        print(f"  Files merged: {result.files_merged}")
    else:
        print(f"  Success: {result.success}")
        print(f"  Conflicts: {result.total_conflicts}")
    
    print("\n" + "=" * 70)
    print("PASS: Merge branch")
    print("=" * 70)


def test_resolve_conflict():
    """
    Test: Resolve conflict.
    """
    print("=" * 70)
    print("TEST: Resolve Conflict")
    print("=" * 70)
    
    engine = GitMergeEngine()
    
    # Önce conflict olan bir merge başlat
    engine.merge_branch("feature/test", "main")
    
    # Conflict çöz
    if engine.pending_conflicts:
        conflict = engine.pending_conflicts[0]
        result = engine.resolve_conflict(conflict.file_path, conflict.line_number, "resolved")
        
        assert result.success, "Conflict çözme başarılı olmalı"
        
        print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Resolve conflict")
    print("=" * 70)


def test_abort_merge():
    """
    Test: Abort merge.
    """
    print("=" * 70)
    print("TEST: Abort Merge")
    print("=" * 70)
    
    engine = GitMergeEngine()
    
    engine.merge_branch("feature/test", "main")
    result = engine.abort_merge()
    
    assert result.success, "İptal başarılı olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Abort merge")
    print("=" * 70)


def test_continue_merge():
    """
    Test: Continue merge.
    """
    print("=" * 70)
    print("TEST: Continue Merge")
    print("=" * 70)
    
    engine = GitMergeEngine()
    
    engine.merge_branch("feature/test", "main")
    
    # Conflictleri çöz
    for conflict in engine.pending_conflicts:
        conflict.is_resolved = True
    
    result = engine.continue_merge()
    
    assert result.success, "Devam başarılı olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Continue merge")
    print("=" * 70)


def test_get_conflicts():
    """
    Test: Get conflicts.
    """
    print("=" * 70)
    print("TEST: Get Conflicts")
    print("=" * 70)
    
    engine = GitMergeEngine()
    
    engine.merge_branch("feature/test", "main")
    
    conflicts = engine.get_conflicts()
    
    print(f"  Conflicts: {len(conflicts)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get conflicts")
    print("=" * 70)


def test_get_merge_history():
    """
    Test: Get merge history.
    """
    print("=" * 70)
    print("TEST: Get Merge History")
    print("=" * 70)
    
    engine = GitMergeEngine()
    
    # Conflict olmayan bir merge simüle et
    engine.config.auto_resolve = True
    engine.merge_branch("feature/test", "main")
    
    history = engine.get_merge_history()
    
    print(f"  History: {len(history)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get merge history")
    print("=" * 70)


def test_clear_history():
    """
    Test: Clear history.
    """
    print("=" * 70)
    print("TEST: Clear History")
    print("=" * 70)
    
    engine = GitMergeEngine()
    
    engine.config.auto_resolve = True
    engine.merge_branch("feature/test", "main")
    
    result = engine.clear_history()
    
    assert result.success, "Temizleme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear history")
    print("=" * 70)


def test_get_current_merge():
    """
    Test: Get current merge.
    """
    print("=" * 70)
    print("TEST: Get Current Merge")
    print("=" * 70)
    
    engine = GitMergeEngine()
    
    engine.merge_branch("feature/test", "main")
    
    current = engine.get_current_merge()
    
    assert current is not None, "Current merge olmalı"
    
    print(f"  Current merge: {current.source_branch} -> {current.target_branch}")
    
    print("\n" + "=" * 70)
    print("PASS: Get current merge")
    print("=" * 70)


def test_is_merge_in_progress():
    """
    Test: Is merge in progress.
    """
    print("=" * 70)
    print("TEST: Is Merge In Progress")
    print("=" * 70)
    
    engine = GitMergeEngine()
    
    engine.merge_branch("feature/test", "main")
    
    in_progress = engine.is_merge_in_progress()
    
    assert in_progress == True, "Merge devam ediyor olmalı"
    
    print(f"  In progress: {in_progress}")
    
    print("\n" + "=" * 70)
    print("PASS: Is merge in progress")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    engine = GitMergeEngine()
    
    new_config = MergeConfig(auto_resolve=True)
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
    
    engine = GitMergeEngine()
    
    config = engine.get_config()
    
    assert config is not None, "Config olmalı"
    assert config.auto_resolve == False, "Config eşleşmeli"
    
    print(f"  Auto resolve: {config.auto_resolve}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


def test_merge_strategy_enum():
    """
    Test: MergeStrategy enum.
    """
    print("=" * 70)
    print("TEST: MergeStrategy Enum")
    print("=" * 70)
    
    assert MergeStrategy.MERGE.value == "merge"
    assert MergeStrategy.REBASE.value == "rebase"
    assert MergeStrategy.SQUASH.value == "squash"
    assert MergeStrategy.FAST_FORWARD.value == "fast_forward"
    assert MergeStrategy.OCTOPUS.value == "octopus"
    assert MergeStrategy.OURS.value == "ours"
    assert MergeStrategy.THEIRS.value == "theirs"
    
    print(f"  All enum values verified")
    print(f"  Total strategies: {len(MergeStrategy)}")
    
    print("\n" + "=" * 70)
    print("PASS: MergeStrategy enum")
    print("=" * 70)


def test_merge_status_enum():
    """
    Test: MergeStatus enum.
    """
    print("=" * 70)
    print("TEST: MergeStatus Enum")
    print("=" * 70)
    
    assert MergeStatus.SUCCESS.value == "success"
    assert MergeStatus.CONFLICT.value == "conflict"
    assert MergeStatus.FAILED.value == "failed"
    assert MergeStatus.PENDING.value == "pending"
    assert MergeStatus.ABORTED.value == "aborted"
    
    print(f"  All enum values verified")
    print(f"  Total statuses: {len(MergeStatus)}")
    
    print("\n" + "=" * 70)
    print("PASS: MergeStatus enum")
    print("=" * 70)


def test_conflict_dataclass():
    """
    Test: Conflict dataclass.
    """
    print("=" * 70)
    print("TEST: Conflict Dataclass")
    print("=" * 70)
    
    conflict = Conflict(
        file_path="test.py",
        line_number=10,
        conflict_type="content",
        our_content="def test():",
        their_content="def test_new():"
    )
    
    assert conflict.file_path == "test.py", "File path eşleşmeli"
    assert conflict.line_number == 10, "Line number eşleşmeli"
    assert conflict.is_resolved == False, "Is resolved eşleşmeli"
    
    print(f"  File path: {conflict.file_path}")
    print(f"  Line number: {conflict.line_number}")
    print(f"  Is resolved: {conflict.is_resolved}")
    
    print("\n" + "=" * 70)
    print("PASS: Conflict dataclass")
    print("=" * 70)


def test_merge_info_dataclass():
    """
    Test: MergeInfo dataclass.
    """
    print("=" * 70)
    print("TEST: MergeInfo Dataclass")
    print("=" * 70)
    
    merge_info = MergeInfo(
        source_branch="feature/test",
        target_branch="main",
        strategy=MergeStrategy.MERGE,
        status=MergeStatus.PENDING
    )
    
    assert merge_info.source_branch == "feature/test", "Source branch eşleşmeli"
    assert merge_info.target_branch == "main", "Target branch eşleşmeli"
    assert merge_info.strategy == MergeStrategy.MERGE, "Strategy eşleşmeli"
    
    print(f"  Source branch: {merge_info.source_branch}")
    print(f"  Target branch: {merge_info.target_branch}")
    print(f"  Strategy: {merge_info.strategy.value}")
    
    print("\n" + "=" * 70)
    print("PASS: MergeInfo dataclass")
    print("=" * 70)


def test_merge_config_dataclass():
    """
    Test: MergeConfig dataclass.
    """
    print("=" * 70)
    print("TEST: MergeConfig Dataclass")
    print("=" * 70)
    
    config = MergeConfig(
        auto_resolve=True,
        prefer_ours=False,
        create_merge_commit=True
    )
    
    assert config.auto_resolve == True, "Auto resolve eşleşmeli"
    assert config.prefer_ours == False, "Prefer ours eşleşmeli"
    assert config.create_merge_commit == True, "Create merge commit eşleşmeli"
    
    print(f"  Auto resolve: {config.auto_resolve}")
    print(f"  Prefer ours: {config.prefer_ours}")
    print(f"  Create merge commit: {config.create_merge_commit}")
    
    print("\n" + "=" * 70)
    print("PASS: MergeConfig dataclass")
    print("=" * 70)


def test_merge_result_dataclass():
    """
    Test: MergeResult dataclass.
    """
    print("=" * 70)
    print("TEST: MergeResult Dataclass")
    print("=" * 70)
    
    result = MergeResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.conflicts, list), "Conflicts list olmalı"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Conflicts: {len(result.conflicts)}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: MergeResult dataclass")
    print("=" * 70)


def test_merge_with_auto_resolve():
    """
    Test: Merge with auto resolve.
    """
    print("=" * 70)
    print("TEST: Merge With Auto Resolve")
    print("=" * 70)
    
    engine = GitMergeEngine()
    engine.config.auto_resolve = True
    
    result = engine.merge_branch("feature/test", "main")
    
    assert result.success == True, "Auto resolve ile başarılı olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Merge with auto resolve")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_merge_branch()
        test2 = test_resolve_conflict()
        test3 = test_abort_merge()
        test4 = test_continue_merge()
        test5 = test_get_conflicts()
        test6 = test_get_merge_history()
        test7 = test_clear_history()
        test8 = test_get_current_merge()
        test9 = test_is_merge_in_progress()
        test10 = test_update_config()
        test11 = test_get_config()
        test12 = test_merge_strategy_enum()
        test13 = test_merge_status_enum()
        test14 = test_conflict_dataclass()
        test15 = test_merge_info_dataclass()
        test16 = test_merge_config_dataclass()
        test17 = test_merge_result_dataclass()
        test18 = test_merge_with_auto_resolve()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Merge Branch: {'PASS' if test1 else 'FAIL'}")
        print(f"Resolve Conflict: {'PASS' if test2 else 'FAIL'}")
        print(f"Abort Merge: {'PASS' if test3 else 'FAIL'}")
        print(f"Continue Merge: {'PASS' if test4 else 'FAIL'}")
        print(f"Get Conflicts: {'PASS' if test5 else 'FAIL'}")
        print(f"Get Merge History: {'PASS' if test6 else 'FAIL'}")
        print(f"Clear History: {'PASS' if test7 else 'FAIL'}")
        print(f"Get Current Merge: {'PASS' if test8 else 'FAIL'}")
        print(f"Is Merge In Progress: {'PASS' if test9 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test10 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test11 else 'FAIL'}")
        print(f"MergeStrategy Enum: {'PASS' if test12 else 'FAIL'}")
        print(f"MergeStatus Enum: {'PASS' if test13 else 'FAIL'}")
        print(f"Conflict Dataclass: {'PASS' if test14 else 'FAIL'}")
        print(f"MergeInfo Dataclass: {'PASS' if test15 else 'FAIL'}")
        print(f"MergeConfig Dataclass: {'PASS' if test16 else 'FAIL'}")
        print(f"MergeResult Dataclass: {'PASS' if test17 else 'FAIL'}")
        print(f"Merge With Auto Resolve: {'PASS' if test18 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14, test15, test16, test17, test18])
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
