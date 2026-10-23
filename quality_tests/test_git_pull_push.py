"""
Quality Test: Git Pull/Push
Git pull/push system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.git_pull_push import (
    GitPullPushEngine,
    PullStrategy,
    PushStrategy,
    SyncAction,
    SyncStatus,
    SyncConfig,
    RemoteInfo,
    SyncResult
)


def test_pull():
    """
    Test: Pull.
    """
    print("=" * 70)
    print("TEST: Pull")
    print("=" * 70)
    
    engine = GitPullPushEngine()
    result = engine.pull("origin", "main")
    
    assert result.success, "Pull başarılı olmalı"
    assert result.action == SyncAction.PULL.value, "Action eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Pull")
    print("=" * 70)


def test_pull_with_strategy():
    """
    Test: Pull with strategy.
    """
    print("=" * 70)
    print("TEST: Pull With Strategy")
    print("=" * 70)
    
    engine = GitPullPushEngine()
    result = engine.pull("origin", "main", strategy=PullStrategy.REBASE, rebase=True)
    
    assert result.success, "Pull başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Pull with strategy")
    print("=" * 70)


def test_push():
    """
    Test: Push.
    """
    print("=" * 70)
    print("TEST: Push")
    print("=" * 70)
    
    engine = GitPullPushEngine()
    result = engine.push("origin", "main")
    
    assert result.success, "Push başarılı olmalı"
    assert result.action == SyncAction.PUSH.value, "Action eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Push")
    print("=" * 70)


def test_push_force():
    """
    Test: Push force.
    """
    print("=" * 70)
    print("TEST: Push Force")
    print("=" * 70)
    
    engine = GitPullPushEngine()
    # Force push disabled by default
    result = engine.push("origin", "main", force=True)
    
    # Should fail due to confirmation
    assert not result.success, "Force push onay gerektirir"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Push force (confirmation required)")
    print("=" * 70)


def test_fetch():
    """
    Test: Fetch.
    """
    print("=" * 70)
    print("TEST: Fetch")
    print("=" * 70)
    
    engine = GitPullPushEngine()
    result = engine.fetch("origin")
    
    assert result.success, "Fetch başarılı olmalı"
    assert result.action == SyncAction.FETCH.value, "Action eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Fetch")
    print("=" * 70)


def test_clone():
    """
    Test: Clone.
    """
    print("=" * 70)
    print("TEST: Clone")
    print("=" * 70)
    
    engine = GitPullPushEngine()
    result = engine.clone("https://github.com/user/repo.git", "/tmp/repo")
    
    assert result.success, "Clone başarılı olmalı"
    assert result.action == SyncAction.CLONE.value, "Action eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Clone")
    print("=" * 70)


def test_sync():
    """
    Test: Sync.
    """
    print("=" * 70)
    print("TEST: Sync")
    print("=" * 70)
    
    engine = GitPullPushEngine()
    result = engine.sync("origin", "main")
    
    assert result.success, "Sync başarılı olmalı"
    assert result.action == SyncAction.SYNC.value, "Action eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Sync")
    print("=" * 70)


def test_add_remote():
    """
    Test: Add remote.
    """
    print("=" * 70)
    print("TEST: Add Remote")
    print("=" * 70)
    
    engine = GitPullPushEngine()
    result = engine.add_remote("origin", "https://github.com/user/repo.git")
    
    assert result.success, "Remote ekleme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add remote")
    print("=" * 70)


def test_remove_remote():
    """
    Test: Remove remote.
    """
    print("=" * 70)
    print("TEST: Remove Remote")
    print("=" * 70)
    
    engine = GitPullPushEngine()
    engine.add_remote("origin", "https://github.com/user/repo.git")
    
    result = engine.remove_remote("origin")
    
    assert result.success, "Remote silme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Remove remote")
    print("=" * 70)


def test_get_remote():
    """
    Test: Get remote.
    """
    print("=" * 70)
    print("TEST: Get Remote")
    print("=" * 70)
    
    engine = GitPullPushEngine()
    engine.add_remote("origin", "https://github.com/user/repo.git")
    
    remote = engine.get_remote("origin")
    
    assert remote is not None, "Remote bulunmalı"
    assert remote.name == "origin", "Remote adı eşleşmeli"
    
    print(f"  Remote name: {remote.name}")
    print(f"  Remote URL: {remote.url}")
    
    print("\n" + "=" * 70)
    print("PASS: Get remote")
    print("=" * 70)


def test_list_remotes():
    """
    Test: List remotes.
    """
    print("=" * 70)
    print("TEST: List Remotes")
    print("=" * 70)
    
    engine = GitPullPushEngine()
    engine.add_remote("origin", "https://github.com/user/repo.git")
    engine.add_remote("upstream", "https://github.com/user/upstream.git")
    
    remotes = engine.list_remotes()
    
    assert len(remotes) == 2, "2 remote olmalı"
    
    print(f"  Total remotes: {len(remotes)}")
    
    print("\n" + "=" * 70)
    print("PASS: List remotes")
    print("=" * 70)


def test_get_sync_status():
    """
    Test: Get sync status.
    """
    print("=" * 70)
    print("TEST: Get Sync Status")
    print("=" * 70)
    
    engine = GitPullPushEngine()
    status = engine.get_sync_status("origin", "main")
    
    assert status is not None, "Durum olmalı"
    
    print(f"  Sync status: {status.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Get sync status")
    print("=" * 70)


def test_get_sync_history():
    """
    Test: Get sync history.
    """
    print("=" * 70)
    print("TEST: Get Sync History")
    print("=" * 70)
    
    engine = GitPullPushEngine()
    engine.pull("origin", "main")
    
    history = engine.get_sync_history()
    
    assert len(history) > 0, "Geçmiş olmalı"
    
    print(f"  History: {len(history)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get sync history")
    print("=" * 70)


def test_clear_history():
    """
    Test: Clear history.
    """
    print("=" * 70)
    print("TEST: Clear History")
    print("=" * 70)
    
    engine = GitPullPushEngine()
    engine.pull("origin", "main")
    
    result = engine.clear_history()
    
    assert result.success, "Temizleme başarılı olmalı"
    assert len(engine.get_sync_history()) == 0, "Geçmiş temizlenmeli"
    
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
    
    engine = GitPullPushEngine()
    engine.pull("origin", "main")
    engine.push("origin", "main")
    
    stats = engine.get_statistics()
    
    assert stats is not None, "İstatistikler olmalı"
    assert stats["total_syncs"] == 2, "Toplam sync 2 olmalı"
    
    print(f"  Total syncs: {stats['total_syncs']}")
    print(f"  Pulls: {stats['pulls']}")
    print(f"  Pushes: {stats['pushes']}")
    
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
    
    engine = GitPullPushEngine()
    
    new_config = SyncConfig(auto_fetch=False)
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
    
    engine = GitPullPushEngine()
    
    config = engine.get_config()
    
    assert config is not None, "Config olmalı"
    assert config.auto_fetch == True, "Config eşleşmeli"
    
    print(f"  Auto fetch: {config.auto_fetch}")
    print(f"  Auto push: {config.auto_push}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


def test_pull_strategy_enum():
    """
    Test: PullStrategy enum.
    """
    print("=" * 70)
    print("TEST: PullStrategy Enum")
    print("=" * 70)
    
    assert PullStrategy.MERGE.value == "merge"
    assert PullStrategy.REBASE.value == "rebase"
    assert PullStrategy.FAST_FORWARD.value == "fast_forward"
    assert PullStrategy.FF_ONLY.value == "ff_only"
    
    print(f"  All enum values verified")
    print(f"  Total strategies: {len(PullStrategy)}")
    
    print("\n" + "=" * 70)
    print("PASS: PullStrategy enum")
    print("=" * 70)


def test_push_strategy_enum():
    """
    Test: PushStrategy enum.
    """
    print("=" * 70)
    print("TEST: PushStrategy Enum")
    print("=" * 70)
    
    assert PushStrategy.NORMAL.value == "normal"
    assert PushStrategy.FORCE.value == "force"
    assert PushStrategy.FORCE_WITH_LEASE.value == "force_with_lease"
    assert PushStrategy.CAS.value == "cas"
    
    print(f"  All enum values verified")
    print(f"  Total strategies: {len(PushStrategy)}")
    
    print("\n" + "=" * 70)
    print("PASS: PushStrategy enum")
    print("=" * 70)


def test_sync_action_enum():
    """
    Test: SyncAction enum.
    """
    print("=" * 70)
    print("TEST: SyncAction Enum")
    print("=" * 70)
    
    assert SyncAction.PULL.value == "pull"
    assert SyncAction.PUSH.value == "push"
    assert SyncAction.FETCH.value == "fetch"
    assert SyncAction.CLONE.value == "clone"
    assert SyncAction.SYNC.value == "sync"
    
    print(f"  All enum values verified")
    print(f"  Total actions: {len(SyncAction)}")
    
    print("\n" + "=" * 70)
    print("PASS: SyncAction enum")
    print("=" * 70)


def test_sync_status_enum():
    """
    Test: SyncStatus enum.
    """
    print("=" * 70)
    print("TEST: SyncStatus Enum")
    print("=" * 70)
    
    assert SyncStatus.SUCCESS.value == "success"
    assert SyncStatus.FAILED.value == "failed"
    assert SyncStatus.CONFLICT.value == "conflict"
    assert SyncStatus.AHEAD.value == "ahead"
    assert SyncStatus.BEHIND.value == "behind"
    assert SyncStatus.DIVERGED.value == "diverged"
    assert SyncStatus.UP_TO_DATE.value == "up_to_date"
    
    print(f"  All enum values verified")
    print(f"  Total statuses: {len(SyncStatus)}")
    
    print("\n" + "=" * 70)
    print("PASS: SyncStatus enum")
    print("=" * 70)


def test_sync_config_dataclass():
    """
    Test: SyncConfig dataclass.
    """
    print("=" * 70)
    print("TEST: SyncConfig Dataclass")
    print("=" * 70)
    
    config = SyncConfig(
        auto_fetch=False,
        auto_push=False
    )
    
    assert config.auto_fetch == False, "Auto fetch eşleşmeli"
    assert config.auto_push == False, "Auto push eşleşmeli"
    
    print(f"  Auto fetch: {config.auto_fetch}")
    print(f"  Auto push: {config.auto_push}")
    
    print("\n" + "=" * 70)
    print("PASS: SyncConfig dataclass")
    print("=" * 70)


def test_remote_info_dataclass():
    """
    Test: RemoteInfo dataclass.
    """
    print("=" * 70)
    print("TEST: RemoteInfo Dataclass")
    print("=" * 70)
    
    remote = RemoteInfo(
        name="origin",
        url="https://github.com/user/repo.git"
    )
    
    assert remote.name == "origin", "Name eşleşmeli"
    assert remote.url == "https://github.com/user/repo.git", "URL eşleşmeli"
    
    print(f"  Name: {remote.name}")
    print(f"  URL: {remote.url}")
    
    print("\n" + "=" * 70)
    print("PASS: RemoteInfo dataclass")
    print("=" * 70)


def test_sync_result_dataclass():
    """
    Test: SyncResult dataclass.
    """
    print("=" * 70)
    print("TEST: SyncResult Dataclass")
    print("=" * 70)
    
    result = SyncResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: SyncResult dataclass")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_pull()
        test2 = test_pull_with_strategy()
        test3 = test_push()
        test4 = test_push_force()
        test5 = test_fetch()
        test6 = test_clone()
        test7 = test_sync()
        test8 = test_add_remote()
        test9 = test_remove_remote()
        test10 = test_get_remote()
        test11 = test_list_remotes()
        test12 = test_get_sync_status()
        test13 = test_get_sync_history()
        test14 = test_clear_history()
        test15 = test_get_statistics()
        test16 = test_update_config()
        test17 = test_get_config()
        test18 = test_pull_strategy_enum()
        test19 = test_push_strategy_enum()
        test20 = test_sync_action_enum()
        test21 = test_sync_status_enum()
        test22 = test_sync_config_dataclass()
        test23 = test_remote_info_dataclass()
        test24 = test_sync_result_dataclass()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Pull: {'PASS' if test1 else 'FAIL'}")
        print(f"Pull With Strategy: {'PASS' if test2 else 'FAIL'}")
        print(f"Push: {'PASS' if test3 else 'FAIL'}")
        print(f"Push Force: {'PASS' if test4 else 'FAIL'}")
        print(f"Fetch: {'PASS' if test5 else 'FAIL'}")
        print(f"Clone: {'PASS' if test6 else 'FAIL'}")
        print(f"Sync: {'PASS' if test7 else 'FAIL'}")
        print(f"Add Remote: {'PASS' if test8 else 'FAIL'}")
        print(f"Remove Remote: {'PASS' if test9 else 'FAIL'}")
        print(f"Get Remote: {'PASS' if test10 else 'FAIL'}")
        print(f"List Remotes: {'PASS' if test11 else 'FAIL'}")
        print(f"Get Sync Status: {'PASS' if test12 else 'FAIL'}")
        print(f"Get Sync History: {'PASS' if test13 else 'FAIL'}")
        print(f"Clear History: {'PASS' if test14 else 'FAIL'}")
        print(f"Get Statistics: {'PASS' if test15 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test16 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test17 else 'FAIL'}")
        print(f"PullStrategy Enum: {'PASS' if test18 else 'FAIL'}")
        print(f"PushStrategy Enum: {'PASS' if test19 else 'FAIL'}")
        print(f"SyncAction Enum: {'PASS' if test20 else 'FAIL'}")
        print(f"SyncStatus Enum: {'PASS' if test21 else 'FAIL'}")
        print(f"SyncConfig Dataclass: {'PASS' if test22 else 'FAIL'}")
        print(f"RemoteInfo Dataclass: {'PASS' if test23 else 'FAIL'}")
        print(f"SyncResult Dataclass: {'PASS' if test24 else 'FAIL'}")
        
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
