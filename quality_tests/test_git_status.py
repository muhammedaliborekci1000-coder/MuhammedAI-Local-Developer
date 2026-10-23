"""
Quality Test: Git Status
Git status system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.git_status import (
    GitStatusEngine,
    FileStatus,
    BranchStatus,
    StatusAction,
    StatusConfig,
    FileStatusInfo,
    BranchStatusInfo,
    StatusResult
)


def test_get_status():
    """
    Test: Get status.
    """
    print("=" * 70)
    print("TEST: Get Status")
    print("=" * 70)
    
    engine = GitStatusEngine()
    result = engine.get_status()
    
    assert result.success, "Durum alma başarılı olmalı"
    assert result.total_files > 0, "Dosyalar olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Total files: {result.total_files}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Get status")
    print("=" * 70)


def test_get_branch_status():
    """
    Test: Get branch status.
    """
    print("=" * 70)
    print("TEST: Get Branch Status")
    print("=" * 70)
    
    engine = GitStatusEngine()
    result = engine.get_branch_status()
    
    assert result.success, "Branch durumu alma başarılı olmalı"
    assert result.branch_status is not None, "Branch durumu olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Branch: {result.branch_status.branch}")
    print(f"  Status: {result.branch_status.status.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Get branch status")
    print("=" * 70)


def test_get_file_status():
    """
    Test: Get file status.
    """
    print("=" * 70)
    print("TEST: Get File Status")
    print("=" * 70)
    
    engine = GitStatusEngine()
    engine.get_status()
    
    file_status = engine.get_file_status("file1.py")
    
    assert file_status is not None, "Dosya durumu bulunmalı"
    assert file_status.path == "file1.py", "Dosya yolu eşleşmeli"
    
    print(f"  File path: {file_status.path}")
    print(f"  File status: {file_status.status.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Get file status")
    print("=" * 70)


def test_get_untracked_files():
    """
    Test: Get untracked files.
    """
    print("=" * 70)
    print("TEST: Get Untracked Files")
    print("=" * 70)
    
    engine = GitStatusEngine()
    result = engine.get_untracked_files()
    
    assert result.success, "Untracked dosyalar alma başarılı olmalı"
    assert result.action == StatusAction.GET_UNTRACKED.value, "Action eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Untracked count: {result.untracked_count}")
    
    print("\n" + "=" * 70)
    print("PASS: Get untracked files")
    print("=" * 70)


def test_get_modified_files():
    """
    Test: Get modified files.
    """
    print("=" * 70)
    print("TEST: Get Modified Files")
    print("=" * 70)
    
    engine = GitStatusEngine()
    result = engine.get_modified_files()
    
    assert result.success, "Modified dosyalar alma başarılı olmalı"
    assert result.action == StatusAction.GET_MODIFIED.value, "Action eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Modified count: {result.modified_count}")
    
    print("\n" + "=" * 70)
    print("PASS: Get modified files")
    print("=" * 70)


def test_get_staged_files():
    """
    Test: Get staged files.
    """
    print("=" * 70)
    print("TEST: Get Staged Files")
    print("=" * 70)
    
    engine = GitStatusEngine()
    result = engine.get_staged_files()
    
    assert result.success, "Staged dosyalar alma başarılı olmalı"
    assert result.action == StatusAction.GET_STAGED.value, "Action eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Staged count: {result.staged_count}")
    
    print("\n" + "=" * 70)
    print("PASS: Get staged files")
    print("=" * 70)


def test_get_deleted_files():
    """
    Test: Get deleted files.
    """
    print("=" * 70)
    print("TEST: Get Deleted Files")
    print("=" * 70)
    
    engine = GitStatusEngine()
    result = engine.get_deleted_files()
    
    assert result.success, "Deleted dosyalar alma başarılı olmalı"
    assert result.action == StatusAction.GET_DELETED.value, "Action eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Deleted count: {result.deleted_count}")
    
    print("\n" + "=" * 70)
    print("PASS: Get deleted files")
    print("=" * 70)


def test_get_ignored_files():
    """
    Test: Get ignored files.
    """
    print("=" * 70)
    print("TEST: Get Ignored Files")
    print("=" * 70)
    
    engine = GitStatusEngine()
    result = engine.get_ignored_files()
    
    assert result.success, "Ignored dosyalar alma başarılı olmalı"
    assert result.action == StatusAction.GET_IGNORED.value, "Action eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Total ignored: {result.total_files}")
    
    print("\n" + "=" * 70)
    print("PASS: Get ignored files")
    print("=" * 70)


def test_get_files_by_status():
    """
    Test: Get files by status.
    """
    print("=" * 70)
    print("TEST: Get Files By Status")
    print("=" * 70)
    
    engine = GitStatusEngine()
    engine.get_status()
    
    files = engine.get_files_by_status(FileStatus.MODIFIED)
    
    assert len(files) > 0, "Modified dosyalar olmalı"
    
    print(f"  Files count: {len(files)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get files by status")
    print("=" * 70)


def test_get_file_count():
    """
    Test: Get file count.
    """
    print("=" * 70)
    print("TEST: Get File Count")
    print("=" * 70)
    
    engine = GitStatusEngine()
    engine.get_status()
    
    count = engine.get_file_count()
    
    assert count > 0, "Dosya sayısı olmalı"
    
    print(f"  File count: {count}")
    
    print("\n" + "=" * 70)
    print("PASS: Get file count")
    print("=" * 70)


def test_has_conflicts():
    """
    Test: Has conflicts.
    """
    print("=" * 70)
    print("TEST: Has Conflicts")
    print("=" * 70)
    
    engine = GitStatusEngine()
    engine.get_status()
    
    has_conflicts = engine.has_conflicts()
    
    print(f"  Has conflicts: {has_conflicts}")
    
    print("\n" + "=" * 70)
    print("PASS: Has conflicts")
    print("=" * 70)


def test_get_conflicted_files():
    """
    Test: Get conflicted files.
    """
    print("=" * 70)
    print("TEST: Get Conflicted Files")
    print("=" * 70)
    
    engine = GitStatusEngine()
    engine.get_status()
    
    conflicted = engine.get_conflicted_files()
    
    print(f"  Conflicted files: {len(conflicted)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get conflicted files")
    print("=" * 70)


def test_is_clean():
    """
    Test: Is clean.
    """
    print("=" * 70)
    print("TEST: Is Clean")
    print("=" * 70)
    
    engine = GitStatusEngine()
    engine.get_status()
    
    is_clean = engine.is_clean()
    
    assert is_clean == False, "Temiz olmamalı (dosyalar var)"
    
    print(f"  Is clean: {is_clean}")
    
    print("\n" + "=" * 70)
    print("PASS: Is clean")
    print("=" * 70)


def test_get_status_history():
    """
    Test: Get status history.
    """
    print("=" * 70)
    print("TEST: Get Status History")
    print("=" * 70)
    
    engine = GitStatusEngine()
    engine.get_status()
    
    history = engine.get_status_history()
    
    assert len(history) > 0, "Geçmiş olmalı"
    
    print(f"  History: {len(history)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get status history")
    print("=" * 70)


def test_clear_history():
    """
    Test: Clear history.
    """
    print("=" * 70)
    print("TEST: Clear History")
    print("=" * 70)
    
    engine = GitStatusEngine()
    engine.get_status()
    
    result = engine.clear_history()
    
    assert result.success, "Temizleme başarılı olmalı"
    assert len(engine.get_status_history()) == 0, "Geçmiş temizlenmeli"
    
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
    
    engine = GitStatusEngine()
    engine.get_status()
    
    stats = engine.get_statistics()
    
    assert stats is not None, "İstatistikler olmalı"
    assert stats["total_files"] > 0, "Toplam dosya olmalı"
    
    print(f"  Total files: {stats['total_files']}")
    print(f"  Staged: {stats['staged']}")
    print(f"  Modified: {stats['modified']}")
    
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
    
    engine = GitStatusEngine()
    
    new_config = StatusConfig(show_untracked=False)
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
    
    engine = GitStatusEngine()
    
    config = engine.get_config()
    
    assert config is not None, "Config olmalı"
    assert config.show_untracked == True, "Config eşleşmeli"
    
    print(f"  Show untracked: {config.show_untracked}")
    print(f"  Show ignored: {config.show_ignored}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


def test_file_status_enum():
    """
    Test: FileStatus enum.
    """
    print("=" * 70)
    print("TEST: FileStatus Enum")
    print("=" * 70)
    
    assert FileStatus.UNTRACKED.value == "untracked"
    assert FileStatus.MODIFIED.value == "modified"
    assert FileStatus.STAGED.value == "staged"
    assert FileStatus.DELETED.value == "deleted"
    assert FileStatus.RENAMED.value == "renamed"
    assert FileStatus.COPIED.value == "copied"
    assert FileStatus.UNMERGED.value == "unmerged"
    assert FileStatus.IGNORED.value == "ignored"
    
    print(f"  All enum values verified")
    print(f"  Total statuses: {len(FileStatus)}")
    
    print("\n" + "=" * 70)
    print("PASS: FileStatus enum")
    print("=" * 70)


def test_branch_status_enum():
    """
    Test: BranchStatus enum.
    """
    print("=" * 70)
    print("TEST: BranchStatus Enum")
    print("=" * 70)
    
    assert BranchStatus.AHEAD.value == "ahead"
    assert BranchStatus.BEHIND.value == "behind"
    assert BranchStatus.DIVERGED.value == "diverged"
    assert BranchStatus.UP_TO_DATE.value == "up_to_date"
    assert BranchStatus.DETACHED.value == "detached"
    
    print(f"  All enum values verified")
    print(f"  Total statuses: {len(BranchStatus)}")
    
    print("\n" + "=" * 70)
    print("PASS: BranchStatus enum")
    print("=" * 70)


def test_status_action_enum():
    """
    Test: StatusAction enum.
    """
    print("=" * 70)
    print("TEST: StatusAction Enum")
    print("=" * 70)
    
    assert StatusAction.GET_STATUS.value == "get_status"
    assert StatusAction.GET_BRANCH_STATUS.value == "get_branch_status"
    assert StatusAction.GET_FILE_STATUS.value == "get_file_status"
    assert StatusAction.GET_UNTRACKED.value == "get_untracked"
    assert StatusAction.GET_MODIFIED.value == "get_modified"
    assert StatusAction.GET_STAGED.value == "get_staged"
    assert StatusAction.GET_DELETED.value == "get_deleted"
    assert StatusAction.GET_IGNORED.value == "get_ignored"
    
    print(f"  All enum values verified")
    print(f"  Total actions: {len(StatusAction)}")
    
    print("\n" + "=" * 70)
    print("PASS: StatusAction enum")
    print("=" * 70)


def test_status_config_dataclass():
    """
    Test: StatusConfig dataclass.
    """
    print("=" * 70)
    print("TEST: StatusConfig Dataclass")
    print("=" * 70)
    
    config = StatusConfig(
        show_untracked=False,
        show_ignored=False
    )
    
    assert config.show_untracked == False, "Show untracked eşleşmeli"
    assert config.show_ignored == False, "Show ignored eşleşmeli"
    
    print(f"  Show untracked: {config.show_untracked}")
    print(f"  Show ignored: {config.show_ignored}")
    
    print("\n" + "=" * 70)
    print("PASS: StatusConfig dataclass")
    print("=" * 70)


def test_file_status_info_dataclass():
    """
    Test: FileStatusInfo dataclass.
    """
    print("=" * 70)
    print("TEST: FileStatusInfo Dataclass")
    print("=" * 70)
    
    file_info = FileStatusInfo(
        path="test.py",
        status=FileStatus.MODIFIED
    )
    
    assert file_info.path == "test.py", "Path eşleşmeli"
    assert file_info.status == FileStatus.MODIFIED, "Status eşleşmeli"
    
    print(f"  Path: {file_info.path}")
    print(f"  Status: {file_info.status.value}")
    
    print("\n" + "=" * 70)
    print("PASS: FileStatusInfo dataclass")
    print("=" * 70)


def test_branch_status_info_dataclass():
    """
    Test: BranchStatusInfo dataclass.
    """
    print("=" * 70)
    print("TEST: BranchStatusInfo Dataclass")
    print("=" * 70)
    
    branch_info = BranchStatusInfo(
        branch="main",
        upstream="origin/main",
        status=BranchStatus.AHEAD
    )
    
    assert branch_info.branch == "main", "Branch eşleşmeli"
    assert branch_info.status == BranchStatus.AHEAD, "Status eşleşmeli"
    
    print(f"  Branch: {branch_info.branch}")
    print(f"  Status: {branch_info.status.value}")
    
    print("\n" + "=" * 70)
    print("PASS: BranchStatusInfo dataclass")
    print("=" * 70)


def test_status_result_dataclass():
    """
    Test: StatusResult dataclass.
    """
    print("=" * 70)
    print("TEST: StatusResult Dataclass")
    print("=" * 70)
    
    result = StatusResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: StatusResult dataclass")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_get_status()
        test2 = test_get_branch_status()
        test3 = test_get_file_status()
        test4 = test_get_untracked_files()
        test5 = test_get_modified_files()
        test6 = test_get_staged_files()
        test7 = test_get_deleted_files()
        test8 = test_get_ignored_files()
        test9 = test_get_files_by_status()
        test10 = test_get_file_count()
        test11 = test_has_conflicts()
        test12 = test_get_conflicted_files()
        test13 = test_is_clean()
        test14 = test_get_status_history()
        test15 = test_clear_history()
        test16 = test_get_statistics()
        test17 = test_update_config()
        test18 = test_get_config()
        test19 = test_file_status_enum()
        test20 = test_branch_status_enum()
        test21 = test_status_action_enum()
        test22 = test_status_config_dataclass()
        test23 = test_file_status_info_dataclass()
        test24 = test_branch_status_info_dataclass()
        test25 = test_status_result_dataclass()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Get Status: {'PASS' if test1 else 'FAIL'}")
        print(f"Get Branch Status: {'PASS' if test2 else 'FAIL'}")
        print(f"Get File Status: {'PASS' if test3 else 'FAIL'}")
        print(f"Get Untracked Files: {'PASS' if test4 else 'FAIL'}")
        print(f"Get Modified Files: {'PASS' if test5 else 'FAIL'}")
        print(f"Get Staged Files: {'PASS' if test6 else 'FAIL'}")
        print(f"Get Deleted Files: {'PASS' if test7 else 'FAIL'}")
        print(f"Get Ignored Files: {'PASS' if test8 else 'FAIL'}")
        print(f"Get Files By Status: {'PASS' if test9 else 'FAIL'}")
        print(f"Get File Count: {'PASS' if test10 else 'FAIL'}")
        print(f"Has Conflicts: {'PASS' if test11 else 'FAIL'}")
        print(f"Get Conflicted Files: {'PASS' if test12 else 'FAIL'}")
        print(f"Is Clean: {'PASS' if test13 else 'FAIL'}")
        print(f"Get Status History: {'PASS' if test14 else 'FAIL'}")
        print(f"Clear History: {'PASS' if test15 else 'FAIL'}")
        print(f"Get Statistics: {'PASS' if test16 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test17 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test18 else 'FAIL'}")
        print(f"FileStatus Enum: {'PASS' if test19 else 'FAIL'}")
        print(f"BranchStatus Enum: {'PASS' if test20 else 'FAIL'}")
        print(f"StatusAction Enum: {'PASS' if test21 else 'FAIL'}")
        print(f"StatusConfig Dataclass: {'PASS' if test22 else 'FAIL'}")
        print(f"FileStatusInfo Dataclass: {'PASS' if test23 else 'FAIL'}")
        print(f"BranchStatusInfo Dataclass: {'PASS' if test24 else 'FAIL'}")
        print(f"StatusResult Dataclass: {'PASS' if test25 else 'FAIL'}")
        
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
