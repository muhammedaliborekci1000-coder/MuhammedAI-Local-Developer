"""
Quality Test: Git Remote
Git remote system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.editor.git_remote import (
    GitRemoteEngine,
    RemoteAction,
    RemoteProtocol,
    RemoteConfig,
    RemoteInfo,
    RemoteResult
)


def test_add_remote():
    """
    Test: Add remote.
    """
    print("=" * 70)
    print("TEST: Add Remote")
    print("=" * 70)
    
    engine = GitRemoteEngine()
    result = engine.add_remote("origin", "https://github.com/user/repo.git")
    
    assert result.success, "Ekleme başarılı olmalı"
    assert result.remote_name == "origin", "Remote adı eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Remote name: {result.remote_name}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add remote")
    print("=" * 70)


def test_add_remote_with_urls():
    """
    Test: Add remote with URLs.
    """
    print("=" * 70)
    print("TEST: Add Remote With URLs")
    print("=" * 70)
    
    engine = GitRemoteEngine()
    result = engine.add_remote(
        "origin",
        "https://github.com/user/repo.git",
        fetch_url="https://github.com/user/repo.git",
        push_url="git@github.com:user/repo.git"
    )
    
    assert result.success, "Ekleme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Remote name: {result.remote_name}")
    
    print("\n" + "=" * 70)
    print("PASS: Add remote with URLs")
    print("=" * 70)


def test_remove_remote():
    """
    Test: Remove remote.
    """
    print("=" * 70)
    print("TEST: Remove Remote")
    print("=" * 70)
    
    engine = GitRemoteEngine()
    engine.add_remote("origin", "https://github.com/user/repo.git")
    
    result = engine.remove_remote("origin")
    
    assert result.success, "Silme başarılı olmalı"
    assert not engine.remote_exists("origin"), "Remote silinmiş olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Remove remote")
    print("=" * 70)


def test_rename_remote():
    """
    Test: Rename remote.
    """
    print("=" * 70)
    print("TEST: Rename Remote")
    print("=" * 70)
    
    engine = GitRemoteEngine()
    engine.add_remote("origin", "https://github.com/user/repo.git")
    
    result = engine.rename_remote("origin", "upstream")
    
    assert result.success, "Yeniden adlandırma başarılı olmalı"
    assert not engine.remote_exists("origin"), "Eski ad silinmeli"
    assert engine.remote_exists("upstream"), "Yeni ad olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Rename remote")
    print("=" * 70)


def test_set_url():
    """
    Test: Set URL.
    """
    print("=" * 70)
    print("TEST: Set URL")
    print("=" * 70)
    
    engine = GitRemoteEngine()
    engine.add_remote("origin", "https://github.com/user/repo.git")
    
    result = engine.set_url("origin", "https://github.com/user/new-repo.git")
    
    assert result.success, "URL ayarlama başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set URL")
    print("=" * 70)


def test_get_url():
    """
    Test: Get URL.
    """
    print("=" * 70)
    print("TEST: Get URL")
    print("=" * 70)
    
    engine = GitRemoteEngine()
    engine.add_remote("origin", "https://github.com/user/repo.git")
    
    result = engine.get_url("origin")
    
    assert result.success, "URL alma başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  URL: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Get URL")
    print("=" * 70)


def test_list_remotes():
    """
    Test: List remotes.
    """
    print("=" * 70)
    print("TEST: List Remotes")
    print("=" * 70)
    
    engine = GitRemoteEngine()
    engine.add_remote("origin", "https://github.com/user/repo.git")
    engine.add_remote("upstream", "https://github.com/user/upstream.git")
    
    result = engine.list_remotes()
    
    assert result.success, "Listeleme başarılı olmalı"
    assert result.total_remotes == 2, "2 remote olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Total remotes: {result.total_remotes}")
    
    print("\n" + "=" * 70)
    print("PASS: List remotes")
    print("=" * 70)


def test_show_remote():
    """
    Test: Show remote.
    """
    print("=" * 70)
    print("TEST: Show Remote")
    print("=" * 70)
    
    engine = GitRemoteEngine()
    engine.add_remote("origin", "https://github.com/user/repo.git")
    
    result = engine.show_remote("origin")
    
    assert result.success, "Gösterme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Show remote")
    print("=" * 70)


def test_prune_remote():
    """
    Test: Prune remote.
    """
    print("=" * 70)
    print("TEST: Prune Remote")
    print("=" * 70)
    
    engine = GitRemoteEngine()
    engine.add_remote("origin", "https://github.com/user/repo.git")
    
    result = engine.prune_remote("origin")
    
    assert result.success, "Temizleme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Prune remote")
    print("=" * 70)


def test_update_remote():
    """
    Test: Update remote.
    """
    print("=" * 70)
    print("TEST: Update Remote")
    print("=" * 70)
    
    engine = GitRemoteEngine()
    engine.add_remote("origin", "https://github.com/user/repo.git")
    
    result = engine.update_remote("origin")
    
    assert result.success, "Güncelleme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Update remote")
    print("=" * 70)


def test_get_remote():
    """
    Test: Get remote.
    """
    print("=" * 70)
    print("TEST: Get Remote")
    print("=" * 70)
    
    engine = GitRemoteEngine()
    engine.add_remote("origin", "https://github.com/user/repo.git")
    
    remote = engine.get_remote("origin")
    
    assert remote is not None, "Remote bulunmalı"
    assert remote.name == "origin", "Remote adı eşleşmeli"
    
    print(f"  Remote name: {remote.name}")
    print(f"  Remote URL: {remote.url}")
    
    print("\n" + "=" * 70)
    print("PASS: Get remote")
    print("=" * 70)


def test_get_remote_count():
    """
    Test: Get remote count.
    """
    print("=" * 70)
    print("TEST: Get Remote Count")
    print("=" * 70)
    
    engine = GitRemoteEngine()
    engine.add_remote("origin", "https://github.com/user/repo.git")
    engine.add_remote("upstream", "https://github.com/user/upstream.git")
    
    count = engine.get_remote_count()
    
    assert count == 2, "Remote sayısı 2 olmalı"
    
    print(f"  Remote count: {count}")
    
    print("\n" + "=" * 70)
    print("PASS: Get remote count")
    print("=" * 70)


def test_remote_exists():
    """
    Test: Remote exists.
    """
    print("=" * 70)
    print("TEST: Remote Exists")
    print("=" * 70)
    
    engine = GitRemoteEngine()
    engine.add_remote("origin", "https://github.com/user/repo.git")
    
    exists = engine.remote_exists("origin")
    
    assert exists == True, "Remote var olmalı"
    
    print(f"  Remote exists: {exists}")
    
    print("\n" + "=" * 70)
    print("PASS: Remote exists")
    print("=" * 70)


def test_set_default_remote():
    """
    Test: Set default remote.
    """
    print("=" * 70)
    print("TEST: Set Default Remote")
    print("=" * 70)
    
    engine = GitRemoteEngine()
    engine.add_remote("origin", "https://github.com/user/repo.git")
    
    result = engine.set_default_remote("origin")
    
    assert result.success, "Default ayarlama başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set default remote")
    print("=" * 70)


def test_get_default_remote():
    """
    Test: Get default remote.
    """
    print("=" * 70)
    print("TEST: Get Default Remote")
    print("=" * 70)
    
    engine = GitRemoteEngine()
    engine.add_remote("origin", "https://github.com/user/repo.git")
    engine.set_default_remote("origin")
    
    remote = engine.get_default_remote()
    
    assert remote is not None, "Default remote bulunmalı"
    assert remote.name == "origin", "Remote adı eşleşmeli"
    
    print(f"  Default remote: {remote.name}")
    
    print("\n" + "=" * 70)
    print("PASS: Get default remote")
    print("=" * 70)


def test_get_remote_history():
    """
    Test: Get remote history.
    """
    print("=" * 70)
    print("TEST: Get Remote History")
    print("=" * 70)
    
    engine = GitRemoteEngine()
    engine.add_remote("origin", "https://github.com/user/repo.git")
    
    history = engine.get_remote_history()
    
    assert len(history) > 0, "Geçmiş olmalı"
    
    print(f"  History: {len(history)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get remote history")
    print("=" * 70)


def test_clear_history():
    """
    Test: Clear history.
    """
    print("=" * 70)
    print("TEST: Clear History")
    print("=" * 70)
    
    engine = GitRemoteEngine()
    engine.add_remote("origin", "https://github.com/user/repo.git")
    
    result = engine.clear_history()
    
    assert result.success, "Temizleme başarılı olmalı"
    assert len(engine.get_remote_history()) == 0, "Geçmiş temizlenmeli"
    
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
    
    engine = GitRemoteEngine()
    engine.add_remote("origin", "https://github.com/user/repo.git")
    engine.add_remote("upstream", "git@github.com:user/upstream.git")
    
    stats = engine.get_statistics()
    
    assert stats is not None, "İstatistikler olmalı"
    assert stats["total_remotes"] == 2, "Toplam remote 2 olmalı"
    
    print(f"  Total remotes: {stats['total_remotes']}")
    print(f"  HTTPS: {stats['https']}")
    print(f"  SSH: {stats['ssh']}")
    
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
    
    engine = GitRemoteEngine()
    
    new_config = RemoteConfig(auto_update=False)
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
    
    engine = GitRemoteEngine()
    
    config = engine.get_config()
    
    assert config is not None, "Config olmalı"
    assert config.auto_update == False, "Config eşleşmeli"
    
    print(f"  Auto update: {config.auto_update}")
    print(f"  Prune remotes: {config.prune_remotes}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


def test_remote_action_enum():
    """
    Test: RemoteAction enum.
    """
    print("=" * 70)
    print("TEST: RemoteAction Enum")
    print("=" * 70)
    
    assert RemoteAction.ADD.value == "add"
    assert RemoteAction.REMOVE.value == "remove"
    assert RemoteAction.RENAME.value == "rename"
    assert RemoteAction.SET_URL.value == "set_url"
    assert RemoteAction.GET_URL.value == "get_url"
    assert RemoteAction.LIST.value == "list"
    assert RemoteAction.SHOW.value == "show"
    assert RemoteAction.PRUNE.value == "prune"
    assert RemoteAction.UPDATE.value == "update"
    
    print(f"  All enum values verified")
    print(f"  Total actions: {len(RemoteAction)}")
    
    print("\n" + "=" * 70)
    print("PASS: RemoteAction enum")
    print("=" * 70)


def test_remote_protocol_enum():
    """
    Test: RemoteProtocol enum.
    """
    print("=" * 70)
    print("TEST: RemoteProtocol Enum")
    print("=" * 70)
    
    assert RemoteProtocol.HTTPS.value == "https"
    assert RemoteProtocol.SSH.value == "ssh"
    assert RemoteProtocol.GIT.value == "git"
    assert RemoteProtocol.FILE.value == "file"
    
    print(f"  All enum values verified")
    print(f"  Total protocols: {len(RemoteProtocol)}")
    
    print("\n" + "=" * 70)
    print("PASS: RemoteProtocol enum")
    print("=" * 70)


def test_remote_config_dataclass():
    """
    Test: RemoteConfig dataclass.
    """
    print("=" * 70)
    print("TEST: RemoteConfig Dataclass")
    print("=" * 70)
    
    config = RemoteConfig(
        auto_update=False,
        prune_remotes=False
    )
    
    assert config.auto_update == False, "Auto update eşleşmeli"
    assert config.prune_remotes == False, "Prune remotes eşleşmeli"
    
    print(f"  Auto update: {config.auto_update}")
    print(f"  Prune remotes: {config.prune_remotes}")
    
    print("\n" + "=" * 70)
    print("PASS: RemoteConfig dataclass")
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
        url="https://github.com/user/repo.git",
        protocol=RemoteProtocol.HTTPS
    )
    
    assert remote.name == "origin", "Name eşleşmeli"
    assert remote.url == "https://github.com/user/repo.git", "URL eşleşmeli"
    
    print(f"  Name: {remote.name}")
    print(f"  URL: {remote.url}")
    
    print("\n" + "=" * 70)
    print("PASS: RemoteInfo dataclass")
    print("=" * 70)


def test_remote_result_dataclass():
    """
    Test: RemoteResult dataclass.
    """
    print("=" * 70)
    print("TEST: RemoteResult Dataclass")
    print("=" * 70)
    
    result = RemoteResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: RemoteResult dataclass")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_add_remote()
        test2 = test_add_remote_with_urls()
        test3 = test_remove_remote()
        test4 = test_rename_remote()
        test5 = test_set_url()
        test6 = test_get_url()
        test7 = test_list_remotes()
        test8 = test_show_remote()
        test9 = test_prune_remote()
        test10 = test_update_remote()
        test11 = test_get_remote()
        test12 = test_get_remote_count()
        test13 = test_remote_exists()
        test14 = test_set_default_remote()
        test15 = test_get_default_remote()
        test16 = test_get_remote_history()
        test17 = test_clear_history()
        test18 = test_get_statistics()
        test19 = test_update_config()
        test20 = test_get_config()
        test21 = test_remote_action_enum()
        test22 = test_remote_protocol_enum()
        test23 = test_remote_config_dataclass()
        test24 = test_remote_info_dataclass()
        test25 = test_remote_result_dataclass()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Add Remote: {'PASS' if test1 else 'FAIL'}")
        print(f"Add Remote With URLs: {'PASS' if test2 else 'FAIL'}")
        print(f"Remove Remote: {'PASS' if test3 else 'FAIL'}")
        print(f"Rename Remote: {'PASS' if test4 else 'FAIL'}")
        print(f"Set URL: {'PASS' if test5 else 'FAIL'}")
        print(f"Get URL: {'PASS' if test6 else 'FAIL'}")
        print(f"List Remotes: {'PASS' if test7 else 'FAIL'}")
        print(f"Show Remote: {'PASS' if test8 else 'FAIL'}")
        print(f"Prune Remote: {'PASS' if test9 else 'FAIL'}")
        print(f"Update Remote: {'PASS' if test10 else 'FAIL'}")
        print(f"Get Remote: {'PASS' if test11 else 'FAIL'}")
        print(f"Get Remote Count: {'PASS' if test12 else 'FAIL'}")
        print(f"Remote Exists: {'PASS' if test13 else 'FAIL'}")
        print(f"Set Default Remote: {'PASS' if test14 else 'FAIL'}")
        print(f"Get Default Remote: {'PASS' if test15 else 'FAIL'}")
        print(f"Get Remote History: {'PASS' if test16 else 'FAIL'}")
        print(f"Clear History: {'PASS' if test17 else 'FAIL'}")
        print(f"Get Statistics: {'PASS' if test18 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test19 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test20 else 'FAIL'}")
        print(f"RemoteAction Enum: {'PASS' if test21 else 'FAIL'}")
        print(f"RemoteProtocol Enum: {'PASS' if test22 else 'FAIL'}")
        print(f"RemoteConfig Dataclass: {'PASS' if test23 else 'FAIL'}")
        print(f"RemoteInfo Dataclass: {'PASS' if test24 else 'FAIL'}")
        print(f"RemoteResult Dataclass: {'PASS' if test25 else 'FAIL'}")
        
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
