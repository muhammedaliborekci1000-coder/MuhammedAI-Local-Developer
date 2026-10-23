"""
Quality Test: Git Rebase
Git rebase system testleri.
"""

import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.git_rebase import (
    GitRebaseEngine,
    RebaseAction,
    RebaseStatus,
    RebaseMode,
    RebaseConfig,
    RebaseCommit,
    RebaseResult
)


def test_rebase():
    """
    Test: Rebase.
    """
    print("=" * 70)
    print("TEST: Rebase")
    print("=" * 70)
    
    engine = GitRebaseEngine()
    result = engine.rebase("main", "feature")
    
    assert result.success, "Rebase başarılı olmalı"
    assert result.action == RebaseAction.REBASE.value, "Action eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Rebase")
    print("=" * 70)


def test_rebase_with_mode():
    """
    Test: Rebase with mode.
    """
    print("=" * 70)
    print("TEST: Rebase With Mode")
    print("=" * 70)
    
    engine = GitRebaseEngine()
    result = engine.rebase("main", "feature", mode=RebaseMode.INTERACTIVE)
    
    assert result.success, "Rebase başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Rebase with mode")
    print("=" * 70)


def test_interactive_rebase():
    """
    Test: Interactive rebase.
    """
    print("=" * 70)
    print("TEST: Interactive Rebase")
    print("=" * 70)
    
    engine = GitRebaseEngine()
    commits = [
        RebaseCommit(hash="abc123", message="Commit 1", author="Dev", date=datetime.now()),
        RebaseCommit(hash="def456", message="Commit 2", author="Dev", date=datetime.now())
    ]
    
    result = engine.interactive_rebase("main", "feature", commits)
    
    assert result.success, "Interactive rebase başarılı olmalı"
    assert result.action == RebaseAction.INTERACTIVE.value, "Action eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Interactive rebase")
    print("=" * 70)


def test_continue_rebase():
    """
    Test: Continue rebase.
    """
    print("=" * 70)
    print("TEST: Continue Rebase")
    print("=" * 70)
    
    engine = GitRebaseEngine()
    engine.interactive_rebase("main", "feature")
    
    result = engine.continue_rebase()
    
    assert result.success, "Continue başarılı olmalı"
    assert result.action == RebaseAction.CONTINUE.value, "Action eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Continue rebase")
    print("=" * 70)


def test_abort_rebase():
    """
    Test: Abort rebase.
    """
    print("=" * 70)
    print("TEST: Abort Rebase")
    print("=" * 70)
    
    engine = GitRebaseEngine()
    engine.interactive_rebase("main", "feature")
    
    result = engine.abort_rebase()
    
    assert result.success, "Abort başarılı olmalı"
    assert result.action == RebaseAction.ABORT.value, "Action eşleşmeli"
    assert result.status == RebaseStatus.ABORTED, "Status aborted olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Abort rebase")
    print("=" * 70)


def test_skip_commit():
    """
    Test: Skip commit.
    """
    print("=" * 70)
    print("TEST: Skip Commit")
    print("=" * 70)
    
    engine = GitRebaseEngine()
    engine.interactive_rebase("main", "feature")
    
    result = engine.skip_commit()
    
    assert result.success, "Skip başarılı olmalı"
    assert result.action == RebaseAction.SKIP.value, "Action eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Skip commit")
    print("=" * 70)


def test_edit_commit():
    """
    Test: Edit commit.
    """
    print("=" * 70)
    print("TEST: Edit Commit")
    print("=" * 70)
    
    engine = GitRebaseEngine()
    commits = [RebaseCommit(hash="abc123", message="Commit 1", author="Dev", date=datetime.now())]
    engine.interactive_rebase("main", "feature", commits)
    
    result = engine.edit_commit("abc123")
    
    assert result.success, "Edit başarılı olmalı"
    assert result.action == RebaseAction.EDIT.value, "Action eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Edit commit")
    print("=" * 70)


def test_squash_commits():
    """
    Test: Squash commits.
    """
    print("=" * 70)
    print("TEST: Squash Commits")
    print("=" * 70)
    
    engine = GitRebaseEngine()
    commits = [
        RebaseCommit(hash="abc123", message="Commit 1", author="Dev", date=datetime.now()),
        RebaseCommit(hash="def456", message="Commit 2", author="Dev", date=datetime.now())
    ]
    engine.interactive_rebase("main", "feature", commits)
    
    result = engine.squash_commits(["abc123", "def456"])
    
    assert result.success, "Squash başarılı olmalı"
    assert result.action == RebaseAction.SQUASH.value, "Action eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Squash commits")
    print("=" * 70)


def test_fixup_commit():
    """
    Test: Fixup commit.
    """
    print("=" * 70)
    print("TEST: Fixup Commit")
    print("=" * 70)
    
    engine = GitRebaseEngine()
    commits = [RebaseCommit(hash="abc123", message="Commit 1", author="Dev", date=datetime.now())]
    engine.interactive_rebase("main", "feature", commits)
    
    result = engine.fixup_commit("abc123")
    
    assert result.success, "Fixup başarılı olmalı"
    assert result.action == RebaseAction.FIXUP.value, "Action eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Fixup commit")
    print("=" * 70)


def test_drop_commit():
    """
    Test: Drop commit.
    """
    print("=" * 70)
    print("TEST: Drop Commit")
    print("=" * 70)
    
    engine = GitRebaseEngine()
    commits = [RebaseCommit(hash="abc123", message="Commit 1", author="Dev", date=datetime.now())]
    engine.interactive_rebase("main", "feature", commits)
    
    result = engine.drop_commit("abc123")
    
    assert result.success, "Drop başarılı olmalı"
    assert result.action == RebaseAction.DROP.value, "Action eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Drop commit")
    print("=" * 70)


def test_reword_commit():
    """
    Test: Reword commit.
    """
    print("=" * 70)
    print("TEST: Reword Commit")
    print("=" * 70)
    
    engine = GitRebaseEngine()
    commits = [RebaseCommit(hash="abc123", message="Commit 1", author="Dev", date=datetime.now())]
    engine.interactive_rebase("main", "feature", commits)
    
    result = engine.reword_commit("abc123", "New message")
    
    assert result.success, "Reword başarılı olmalı"
    assert result.action == RebaseAction.REWORD.value, "Action eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Reword commit")
    print("=" * 70)


def test_get_rebase_status():
    """
    Test: Get rebase status.
    """
    print("=" * 70)
    print("TEST: Get Rebase Status")
    print("=" * 70)
    
    engine = GitRebaseEngine()
    engine.interactive_rebase("main", "feature")
    
    status = engine.get_rebase_status()
    
    assert status is not None, "Durum olmalı"
    assert status == RebaseStatus.IN_PROGRESS, "Durum in_progress olmalı"
    
    print(f"  Rebase status: {status.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Get rebase status")
    print("=" * 70)


def test_get_pending_commits():
    """
    Test: Get pending commits.
    """
    print("=" * 70)
    print("TEST: Get Pending Commits")
    print("=" * 70)
    
    engine = GitRebaseEngine()
    commits = [RebaseCommit(hash="abc123", message="Commit 1", author="Dev", date=datetime.now())]
    engine.interactive_rebase("main", "feature", commits)
    
    pending = engine.get_pending_commits()
    
    assert len(pending) == 1, "1 pending commit olmalı"
    
    print(f"  Pending commits: {len(pending)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get pending commits")
    print("=" * 70)


def test_get_rebase_history():
    """
    Test: Get rebase history.
    """
    print("=" * 70)
    print("TEST: Get Rebase History")
    print("=" * 70)
    
    engine = GitRebaseEngine()
    engine.rebase("main", "feature")
    
    history = engine.get_rebase_history()
    
    assert len(history) > 0, "Geçmiş olmalı"
    
    print(f"  History: {len(history)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get rebase history")
    print("=" * 70)


def test_clear_history():
    """
    Test: Clear history.
    """
    print("=" * 70)
    print("TEST: Clear History")
    print("=" * 70)
    
    engine = GitRebaseEngine()
    engine.rebase("main", "feature")
    
    result = engine.clear_history()
    
    assert result.success, "Temizleme başarılı olmalı"
    assert len(engine.get_rebase_history()) == 0, "Geçmiş temizlenmeli"
    
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
    
    engine = GitRebaseEngine()
    engine.rebase("main", "feature")
    engine.interactive_rebase("main", "feature")
    
    stats = engine.get_statistics()
    
    assert stats is not None, "İstatistikler olmalı"
    assert stats["total_rebases"] == 2, "Toplam rebase 2 olmalı"
    
    print(f"  Total rebases: {stats['total_rebases']}")
    print(f"  Rebases: {stats['rebases']}")
    print(f"  Interactive: {stats['interactive']}")
    
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
    
    engine = GitRebaseEngine()
    
    new_config = RebaseConfig(auto_continue=False)
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
    
    engine = GitRebaseEngine()
    
    config = engine.get_config()
    
    assert config is not None, "Config olmalı"
    assert config.auto_continue == False, "Config eşleşmeli"
    
    print(f"  Auto continue: {config.auto_continue}")
    print(f"  Auto stash: {config.auto_stash}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


def test_rebase_action_enum():
    """
    Test: RebaseAction enum.
    """
    print("=" * 70)
    print("TEST: RebaseAction Enum")
    print("=" * 70)
    
    assert RebaseAction.REBASE.value == "rebase"
    assert RebaseAction.INTERACTIVE.value == "interactive"
    assert RebaseAction.CONTINUE.value == "continue"
    assert RebaseAction.ABORT.value == "abort"
    assert RebaseAction.SKIP.value == "skip"
    assert RebaseAction.EDIT.value == "edit"
    assert RebaseAction.SQUASH.value == "squash"
    assert RebaseAction.FIXUP.value == "fixup"
    assert RebaseAction.DROP.value == "drop"
    assert RebaseAction.REWORD.value == "reword"
    
    print(f"  All enum values verified")
    print(f"  Total actions: {len(RebaseAction)}")
    
    print("\n" + "=" * 70)
    print("PASS: RebaseAction enum")
    print("=" * 70)


def test_rebase_status_enum():
    """
    Test: RebaseStatus enum.
    """
    print("=" * 70)
    print("TEST: RebaseStatus Enum")
    print("=" * 70)
    
    assert RebaseStatus.SUCCESS.value == "success"
    assert RebaseStatus.FAILED.value == "failed"
    assert RebaseStatus.CONFLICT.value == "conflict"
    assert RebaseStatus.IN_PROGRESS.value == "in_progress"
    assert RebaseStatus.ABORTED.value == "aborted"
    assert RebaseStatus.SKIPPED.value == "skipped"
    
    print(f"  All enum values verified")
    print(f"  Total statuses: {len(RebaseStatus)}")
    
    print("\n" + "=" * 70)
    print("PASS: RebaseStatus enum")
    print("=" * 70)


def test_rebase_mode_enum():
    """
    Test: RebaseMode enum.
    """
    print("=" * 70)
    print("TEST: RebaseMode Enum")
    print("=" * 70)
    
    assert RebaseMode.NORMAL.value == "normal"
    assert RebaseMode.INTERACTIVE.value == "interactive"
    assert RebaseMode.AUTOSQUASH.value == "autosquash"
    assert RebaseMode.MERGE.value == "merge"
    
    print(f"  All enum values verified")
    print(f"  Total modes: {len(RebaseMode)}")
    
    print("\n" + "=" * 70)
    print("PASS: RebaseMode enum")
    print("=" * 70)


def test_rebase_config_dataclass():
    """
    Test: RebaseConfig dataclass.
    """
    print("=" * 70)
    print("TEST: RebaseConfig Dataclass")
    print("=" * 70)
    
    config = RebaseConfig(
        auto_continue=False,
        auto_stash=False
    )
    
    assert config.auto_continue == False, "Auto continue eşleşmeli"
    assert config.auto_stash == False, "Auto stash eşleşmeli"
    
    print(f"  Auto continue: {config.auto_continue}")
    print(f"  Auto stash: {config.auto_stash}")
    
    print("\n" + "=" * 70)
    print("PASS: RebaseConfig dataclass")
    print("=" * 70)


def test_rebase_commit_dataclass():
    """
    Test: RebaseCommit dataclass.
    """
    print("=" * 70)
    print("TEST: RebaseCommit Dataclass")
    print("=" * 70)
    
    commit = RebaseCommit(
        hash="abc123",
        message="Commit 1",
        author="Dev",
        date=datetime.now()
    )
    
    assert commit.hash == "abc123", "Hash eşleşmeli"
    assert commit.message == "Commit 1", "Message eşleşmeli"
    
    print(f"  Hash: {commit.hash}")
    print(f"  Message: {commit.message}")
    
    print("\n" + "=" * 70)
    print("PASS: RebaseCommit dataclass")
    print("=" * 70)


def test_rebase_result_dataclass():
    """
    Test: RebaseResult dataclass.
    """
    print("=" * 70)
    print("TEST: RebaseResult Dataclass")
    print("=" * 70)
    
    result = RebaseResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: RebaseResult dataclass")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_rebase()
        test2 = test_rebase_with_mode()
        test3 = test_interactive_rebase()
        test4 = test_continue_rebase()
        test5 = test_abort_rebase()
        test6 = test_skip_commit()
        test7 = test_edit_commit()
        test8 = test_squash_commits()
        test9 = test_fixup_commit()
        test10 = test_drop_commit()
        test11 = test_reword_commit()
        test12 = test_get_rebase_status()
        test13 = test_get_pending_commits()
        test14 = test_get_rebase_history()
        test15 = test_clear_history()
        test16 = test_get_statistics()
        test17 = test_update_config()
        test18 = test_get_config()
        test19 = test_rebase_action_enum()
        test20 = test_rebase_status_enum()
        test21 = test_rebase_mode_enum()
        test22 = test_rebase_config_dataclass()
        test23 = test_rebase_commit_dataclass()
        test24 = test_rebase_result_dataclass()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Rebase: {'PASS' if test1 else 'FAIL'}")
        print(f"Rebase With Mode: {'PASS' if test2 else 'FAIL'}")
        print(f"Interactive Rebase: {'PASS' if test3 else 'FAIL'}")
        print(f"Continue Rebase: {'PASS' if test4 else 'FAIL'}")
        print(f"Abort Rebase: {'PASS' if test5 else 'FAIL'}")
        print(f"Skip Commit: {'PASS' if test6 else 'FAIL'}")
        print(f"Edit Commit: {'PASS' if test7 else 'FAIL'}")
        print(f"Squash Commits: {'PASS' if test8 else 'FAIL'}")
        print(f"Fixup Commit: {'PASS' if test9 else 'FAIL'}")
        print(f"Drop Commit: {'PASS' if test10 else 'FAIL'}")
        print(f"Reword Commit: {'PASS' if test11 else 'FAIL'}")
        print(f"Get Rebase Status: {'PASS' if test12 else 'FAIL'}")
        print(f"Get Pending Commits: {'PASS' if test13 else 'FAIL'}")
        print(f"Get Rebase History: {'PASS' if test14 else 'FAIL'}")
        print(f"Clear History: {'PASS' if test15 else 'FAIL'}")
        print(f"Get Statistics: {'PASS' if test16 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test17 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test18 else 'FAIL'}")
        print(f"RebaseAction Enum: {'PASS' if test19 else 'FAIL'}")
        print(f"RebaseStatus Enum: {'PASS' if test20 else 'FAIL'}")
        print(f"RebaseMode Enum: {'PASS' if test21 else 'FAIL'}")
        print(f"RebaseConfig Dataclass: {'PASS' if test22 else 'FAIL'}")
        print(f"RebaseCommit Dataclass: {'PASS' if test23 else 'FAIL'}")
        print(f"RebaseResult Dataclass: {'PASS' if test24 else 'FAIL'}")
        
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
