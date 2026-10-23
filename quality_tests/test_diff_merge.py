"""
Quality Test: Diff Merge
Diff merge system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.diff_merge import (
    DiffMergeEngine,
    MergeStrategy,
    MergeStatus,
    ConflictResolution,
    MergeAction,
    ConflictInfo,
    MergeResult,
    MergeConfig
)


def test_merge():
    """
    Test: Merge.
    """
    print("=" * 70)
    print("TEST: Merge")
    print("=" * 70)
    
    engine = DiffMergeEngine()
    base = "Line 1\nLine 2\nLine 3"
    ours = "Line 1\nLine 2 modified\nLine 3"
    theirs = "Line 1\nLine 2 changed\nLine 3"
    
    result = engine.merge(base, ours, theirs, "test.txt")
    
    assert result.success, "Merge başarılı olmalı"
    assert result.action == MergeAction.MERGE.value, "Action eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Total conflicts: {result.total_conflicts}")
    print(f"  Status: {result.status.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Merge")
    print("=" * 70)


def test_resolve_conflict():
    """
    Test: Resolve conflict.
    """
    print("=" * 70)
    print("TEST: Resolve Conflict")
    print("=" * 70)
    
    engine = DiffMergeEngine()
    base = "Line 1\nLine 2\nLine 3"
    ours = "Line 1\nLine 2 modified\nLine 3"
    theirs = "Line 1\nLine 2 changed\nLine 3"
    engine.merge(base, ours, theirs, "test.txt")
    
    result = engine.resolve_conflict(2, ConflictResolution.ACCEPT_OURS)
    
    assert result.success, "Çözüm başarılı olmalı"
    assert result.action == MergeAction.RESOLVE.value, "Action eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Resolved conflicts: {result.resolved_conflicts}")
    
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
    
    engine = DiffMergeEngine()
    base = "Line 1\nLine 2\nLine 3"
    ours = "Line 1\nLine 2 modified\nLine 3"
    theirs = "Line 1\nLine 2 changed\nLine 3"
    engine.merge(base, ours, theirs, "test.txt")
    
    result = engine.abort_merge()
    
    assert result.success, "İptal başarılı olmalı"
    assert result.status == MergeStatus.ABORTED, "Status aborted olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
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
    
    engine = DiffMergeEngine()
    base = "Line 1\nLine 2\nLine 3"
    ours = "Line 1\nLine 2\nLine 3"
    theirs = "Line 1\nLine 2\nLine 3"
    engine.merge(base, ours, theirs, "test.txt")
    
    result = engine.continue_merge()
    
    assert result.success, "Devam başarılı olmalı"
    assert result.status == MergeStatus.SUCCESS, "Status success olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Continue merge")
    print("=" * 70)


def test_skip_conflict():
    """
    Test: Skip conflict.
    """
    print("=" * 70)
    print("TEST: Skip Conflict")
    print("=" * 70)
    
    engine = DiffMergeEngine()
    base = "Line 1\nLine 2\nLine 3"
    ours = "Line 1\nLine 2 modified\nLine 3"
    theirs = "Line 1\nLine 2 changed\nLine 3"
    engine.merge(base, ours, theirs, "test.txt")
    
    result = engine.skip_conflict(2)
    
    assert result.success, "Atlama başarılı olmalı"
    assert result.action == MergeAction.SKIP.value, "Action eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Skip conflict")
    print("=" * 70)


def test_preview_merge():
    """
    Test: Preview merge.
    """
    print("=" * 70)
    print("TEST: Preview Merge")
    print("=" * 70)
    
    engine = DiffMergeEngine()
    base = "Line 1\nLine 2\nLine 3"
    ours = "Line 1\nLine 2 modified\nLine 3"
    theirs = "Line 1\nLine 2 changed\nLine 3"
    
    result = engine.preview_merge(base, ours, theirs)
    
    assert result.success, "Önizleme başarılı olmalı"
    assert result.action == MergeAction.PREVIEW.value, "Action eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Total conflicts: {result.total_conflicts}")
    
    print("\n" + "=" * 70)
    print("PASS: Preview merge")
    print("=" * 70)


def test_auto_merge():
    """
    Test: Auto merge.
    """
    print("=" * 70)
    print("TEST: Auto Merge")
    print("=" * 70)
    
    engine = DiffMergeEngine()
    base = "Line 1\nLine 2\nLine 3"
    ours = "Line 1\nLine 2 modified\nLine 3"
    theirs = "Line 1\nLine 2 changed\nLine 3"
    
    result = engine.auto_merge(base, ours, theirs, "test.txt")
    
    assert result.success, "Auto-merge başarılı olmalı"
    assert result.action == MergeAction.AUTO_MERGE.value, "Action eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Resolved conflicts: {result.resolved_conflicts}")
    
    print("\n" + "=" * 70)
    print("PASS: Auto merge")
    print("=" * 70)


def test_get_conflicts():
    """
    Test: Get conflicts.
    """
    print("=" * 70)
    print("TEST: Get Conflicts")
    print("=" * 70)
    
    engine = DiffMergeEngine()
    base = "Line 1\nLine 2\nLine 3"
    ours = "Line 1\nLine 2 modified\nLine 3"
    theirs = "Line 1\nLine 2 changed\nLine 3"
    engine.merge(base, ours, theirs, "test.txt")
    
    conflicts = engine.get_conflicts()
    
    assert len(conflicts) > 0, "Çakışmalar olmalı"
    
    print(f"  Conflicts: {len(conflicts)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get conflicts")
    print("=" * 70)


def test_get_conflict():
    """
    Test: Get conflict.
    """
    print("=" * 70)
    print("TEST: Get Conflict")
    print("=" * 70)
    
    engine = DiffMergeEngine()
    base = "Line 1\nLine 2\nLine 3"
    ours = "Line 1\nLine 2 modified\nLine 3"
    theirs = "Line 1\nLine 2 changed\nLine 3"
    engine.merge(base, ours, theirs, "test.txt")
    
    conflict = engine.get_conflict(2)
    
    assert conflict is not None, "Çakışma bulunmalı"
    assert conflict.line_number == 2, "Satır numarası eşleşmeli"
    
    print(f"  Line number: {conflict.line_number}")
    print(f"  Is resolved: {conflict.is_resolved}")
    
    print("\n" + "=" * 70)
    print("PASS: Get conflict")
    print("=" * 70)


def test_get_unresolved_conflicts():
    """
    Test: Get unresolved conflicts.
    """
    print("=" * 70)
    print("TEST: Get Unresolved Conflicts")
    print("=" * 70)
    
    engine = DiffMergeEngine()
    base = "Line 1\nLine 2\nLine 3"
    ours = "Line 1\nLine 2 modified\nLine 3"
    theirs = "Line 1\nLine 2 changed\nLine 3"
    engine.merge(base, ours, theirs, "test.txt")
    
    unresolved = engine.get_unresolved_conflicts()
    
    assert len(unresolved) > 0, "Çözülmemiş çakışmalar olmalı"
    
    print(f"  Unresolved conflicts: {len(unresolved)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get unresolved conflicts")
    print("=" * 70)


def test_get_resolved_conflicts():
    """
    Test: Get resolved conflicts.
    """
    print("=" * 70)
    print("TEST: Get Resolved Conflicts")
    print("=" * 70)
    
    engine = DiffMergeEngine()
    base = "Line 1\nLine 2\nLine 3"
    ours = "Line 1\nLine 2 modified\nLine 3"
    theirs = "Line 1\nLine 2 changed\nLine 3"
    engine.merge(base, ours, theirs, "test.txt")
    engine.resolve_conflict(2, ConflictResolution.ACCEPT_OURS)
    
    resolved = engine.get_resolved_conflicts()
    
    assert len(resolved) > 0, "Çözülmüş çakışmalar olmalı"
    
    print(f"  Resolved conflicts: {len(resolved)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get resolved conflicts")
    print("=" * 70)


def test_get_merge_status():
    """
    Test: Get merge status.
    """
    print("=" * 70)
    print("TEST: Get Merge Status")
    print("=" * 70)
    
    engine = DiffMergeEngine()
    base = "Line 1\nLine 2\nLine 3"
    ours = "Line 1\nLine 2\nLine 3"
    theirs = "Line 1\nLine 2\nLine 3"
    engine.merge(base, ours, theirs, "test.txt")
    
    status = engine.get_merge_status()
    
    assert status == MergeStatus.SUCCESS, "Status success olmalı"
    
    print(f"  Status: {status.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Get merge status")
    print("=" * 70)


def test_get_merge_history():
    """
    Test: Get merge history.
    """
    print("=" * 70)
    print("TEST: Get Merge History")
    print("=" * 70)
    
    engine = DiffMergeEngine()
    base = "Line 1\nLine 2\nLine 3"
    ours = "Line 1\nLine 2\nLine 3"
    theirs = "Line 1\nLine 2\nLine 3"
    engine.merge(base, ours, theirs, "test.txt")
    
    history = engine.get_merge_history()
    
    assert len(history) > 0, "Geçmiş olmalı"
    
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
    
    engine = DiffMergeEngine()
    base = "Line 1\nLine 2\nLine 3"
    ours = "Line 1\nLine 2\nLine 3"
    theirs = "Line 1\nLine 2\nLine 3"
    engine.merge(base, ours, theirs, "test.txt")
    
    result = engine.clear_history()
    
    assert result.success, "Temizleme başarılı olmalı"
    assert len(engine.get_merge_history()) == 0, "Geçmiş temizlenmeli"
    
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
    
    engine = DiffMergeEngine()
    base = "Line 1\nLine 2\nLine 3"
    ours = "Line 1\nLine 2 modified\nLine 3"
    theirs = "Line 1\nLine 2 changed\nLine 3"
    engine.merge(base, ours, theirs, "test.txt")
    
    stats = engine.get_statistics()
    
    assert stats is not None, "İstatistikler olmalı"
    assert stats["total_conflicts"] > 0, "Toplam çakışma olmalı"
    
    print(f"  Total conflicts: {stats['total_conflicts']}")
    print(f"  Resolved conflicts: {stats['resolved_conflicts']}")
    print(f"  Status: {stats['status']}")
    
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
    
    engine = DiffMergeEngine()
    
    new_config = MergeConfig(strategy=MergeStrategy.MANUAL)
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
    
    engine = DiffMergeEngine()
    
    config = engine.get_config()
    
    assert config is not None, "Config olmalı"
    assert config.strategy == MergeStrategy.AUTO, "Strategy eşleşmeli"
    
    print(f"  Strategy: {config.strategy.value}")
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
    
    assert MergeStrategy.AUTO.value == "auto"
    assert MergeStrategy.MANUAL.value == "manual"
    assert MergeStrategy.THEIRS.value == "theirs"
    assert MergeStrategy.OURS.value == "ours"
    assert MergeStrategy.UNION.value == "union"
    assert MergeStrategy.INTERSECTION.value == "intersection"
    
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
    assert MergeStatus.SKIPPED.value == "skipped"
    
    print(f"  All enum values verified")
    print(f"  Total statuses: {len(MergeStatus)}")
    
    print("\n" + "=" * 70)
    print("PASS: MergeStatus enum")
    print("=" * 70)


def test_conflict_resolution_enum():
    """
    Test: ConflictResolution enum.
    """
    print("=" * 70)
    print("TEST: ConflictResolution Enum")
    print("=" * 70)
    
    assert ConflictResolution.ACCEPT_OURS.value == "accept_ours"
    assert ConflictResolution.ACCEPT_THEIRS.value == "accept_theirs"
    assert ConflictResolution.ACCEPT_BOTH.value == "accept_both"
    assert ConflictResolution.MANUAL_EDIT.value == "manual_edit"
    assert ConflictResolution.MARK_UNRESOLVED.value == "mark_unresolved"
    
    print(f"  All enum values verified")
    print(f"  Total resolutions: {len(ConflictResolution)}")
    
    print("\n" + "=" * 70)
    print("PASS: ConflictResolution enum")
    print("=" * 70)


def test_merge_action_enum():
    """
    Test: MergeAction enum.
    """
    print("=" * 70)
    print("TEST: MergeAction Enum")
    print("=" * 70)
    
    assert MergeAction.MERGE.value == "merge"
    assert MergeAction.RESOLVE.value == "resolve"
    assert MergeAction.ABORT.value == "abort"
    assert MergeAction.CONTINUE.value == "continue"
    assert MergeAction.SKIP.value == "skip"
    assert MergeAction.PREVIEW.value == "preview"
    assert MergeAction.AUTO_MERGE.value == "auto_merge"
    
    print(f"  All enum values verified")
    print(f"  Total actions: {len(MergeAction)}")
    
    print("\n" + "=" * 70)
    print("PASS: MergeAction enum")
    print("=" * 70)


def test_merge_config_dataclass():
    """
    Test: MergeConfig dataclass.
    """
    print("=" * 70)
    print("TEST: MergeConfig Dataclass")
    print("=" * 70)
    
    config = MergeConfig(
        strategy=MergeStrategy.MANUAL,
        auto_resolve=False
    )
    
    assert config.strategy == MergeStrategy.MANUAL, "Strategy eşleşmeli"
    assert config.auto_resolve == False, "Auto resolve eşleşmeli"
    
    print(f"  Strategy: {config.strategy.value}")
    print(f"  Auto resolve: {config.auto_resolve}")
    
    print("\n" + "=" * 70)
    print("PASS: MergeConfig dataclass")
    print("=" * 70)


def test_conflict_info_dataclass():
    """
    Test: ConflictInfo dataclass.
    """
    print("=" * 70)
    print("TEST: ConflictInfo Dataclass")
    print("=" * 70)
    
    conflict = ConflictInfo(
        line_number=1,
        our_content="Our content",
        their_content="Their content",
        base_content="Base content",
        file_path="test.txt"
    )
    
    assert conflict.line_number == 1, "Line number eşleşmeli"
    assert conflict.our_content == "Our content", "Our content eşleşmeli"
    
    print(f"  Line number: {conflict.line_number}")
    print(f"  Is resolved: {conflict.is_resolved}")
    
    print("\n" + "=" * 70)
    print("PASS: ConflictInfo dataclass")
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
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: MergeResult dataclass")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_merge()
        test2 = test_resolve_conflict()
        test3 = test_abort_merge()
        test4 = test_continue_merge()
        test5 = test_skip_conflict()
        test6 = test_preview_merge()
        test7 = test_auto_merge()
        test8 = test_get_conflicts()
        test9 = test_get_conflict()
        test10 = test_get_unresolved_conflicts()
        test11 = test_get_resolved_conflicts()
        test12 = test_get_merge_status()
        test13 = test_get_merge_history()
        test14 = test_clear_history()
        test15 = test_get_statistics()
        test16 = test_update_config()
        test17 = test_get_config()
        test18 = test_merge_strategy_enum()
        test19 = test_merge_status_enum()
        test20 = test_conflict_resolution_enum()
        test21 = test_merge_action_enum()
        test22 = test_merge_config_dataclass()
        test23 = test_conflict_info_dataclass()
        test24 = test_merge_result_dataclass()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Merge: {'PASS' if test1 else 'FAIL'}")
        print(f"Resolve Conflict: {'PASS' if test2 else 'FAIL'}")
        print(f"Abort Merge: {'PASS' if test3 else 'FAIL'}")
        print(f"Continue Merge: {'PASS' if test4 else 'FAIL'}")
        print(f"Skip Conflict: {'PASS' if test5 else 'FAIL'}")
        print(f"Preview Merge: {'PASS' if test6 else 'FAIL'}")
        print(f"Auto Merge: {'PASS' if test7 else 'FAIL'}")
        print(f"Get Conflicts: {'PASS' if test8 else 'FAIL'}")
        print(f"Get Conflict: {'PASS' if test9 else 'FAIL'}")
        print(f"Get Unresolved Conflicts: {'PASS' if test10 else 'FAIL'}")
        print(f"Get Resolved Conflicts: {'PASS' if test11 else 'FAIL'}")
        print(f"Get Merge Status: {'PASS' if test12 else 'FAIL'}")
        print(f"Get Merge History: {'PASS' if test13 else 'FAIL'}")
        print(f"Clear History: {'PASS' if test14 else 'FAIL'}")
        print(f"Get Statistics: {'PASS' if test15 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test16 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test17 else 'FAIL'}")
        print(f"MergeStrategy Enum: {'PASS' if test18 else 'FAIL'}")
        print(f"MergeStatus Enum: {'PASS' if test19 else 'FAIL'}")
        print(f"ConflictResolution Enum: {'PASS' if test20 else 'FAIL'}")
        print(f"MergeAction Enum: {'PASS' if test21 else 'FAIL'}")
        print(f"MergeConfig Dataclass: {'PASS' if test22 else 'FAIL'}")
        print(f"ConflictInfo Dataclass: {'PASS' if test23 else 'FAIL'}")
        print(f"MergeResult Dataclass: {'PASS' if test24 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14, test15, test16, test17, test18, test19, test20, test21, test22, test23, test24])
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
