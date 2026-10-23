"""
Quality Test: Terminal Profiles
Terminal profiles system testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.tools.terminal_profiles import (
    TerminalProfilesEngine,
    ShellType,
    ProfileScope,
    ProfileAction,
    ProfileConfig,
    ProfileEntry,
    ProfileResult
)


def test_create_profile():
    """
    Test: Create profile.
    """
    print("=" * 70)
    print("TEST: Create Profile")
    print("=" * 70)
    
    engine = TerminalProfilesEngine()
    result = engine.create_profile("Default", ShellType.BASH, "/home/user")
    
    assert result.success, "Oluşturma başarılı olmalı"
    assert result.profile_name == "Default", "Profil adı eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Profile ID: {result.profile_id}")
    print(f"  Profile name: {result.profile_name}")
    
    print("\n" + "=" * 70)
    print("PASS: Create profile")
    print("=" * 70)


def test_create_profile_with_options():
    """
    Test: Create profile with options.
    """
    print("=" * 70)
    print("TEST: Create Profile With Options")
    print("=" * 70)
    
    engine = TerminalProfilesEngine()
    result = engine.create_profile(
        "Dev",
        ShellType.ZSH,
        "/home/dev",
        environment={"VAR": "value"},
        aliases={"ll": "ls -la"},
        color_scheme="dark",
        font_family="monospace",
        font_size=14
    )
    
    assert result.success, "Oluşturma başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Profile ID: {result.profile_id}")
    
    print("\n" + "=" * 70)
    print("PASS: Create profile with options")
    print("=" * 70)


def test_update_profile():
    """
    Test: Update profile.
    """
    print("=" * 70)
    print("TEST: Update Profile")
    print("=" * 70)
    
    engine = TerminalProfilesEngine()
    result = engine.create_profile("Default", ShellType.BASH, "/home/user")
    profile_id = result.profile_id
    
    result = engine.update_profile(profile_id, name="Updated", working_directory="/home/updated")
    
    assert result.success, "Güncelleme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Update profile")
    print("=" * 70)


def test_delete_profile():
    """
    Test: Delete profile.
    """
    print("=" * 70)
    print("TEST: Delete Profile")
    print("=" * 70)
    
    engine = TerminalProfilesEngine()
    result = engine.create_profile("Default", ShellType.BASH, "/home/user")
    profile_id = result.profile_id
    
    result = engine.delete_profile(profile_id)
    
    assert result.success, "Silme başarılı olmalı"
    assert profile_id not in engine.profiles, "Profil silinmiş olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Delete profile")
    print("=" * 70)


def test_get_profile():
    """
    Test: Get profile.
    """
    print("=" * 70)
    print("TEST: Get Profile")
    print("=" * 70)
    
    engine = TerminalProfilesEngine()
    result = engine.create_profile("Default", ShellType.BASH, "/home/user")
    profile_id = result.profile_id
    
    result = engine.get_profile(profile_id)
    
    assert result.success, "Alma başarılı olmalı"
    assert result.profile_name == "Default", "Profil adı eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Profile name: {result.profile_name}")
    
    print("\n" + "=" * 70)
    print("PASS: Get profile")
    print("=" * 70)


def test_list_profiles():
    """
    Test: List profiles.
    """
    print("=" * 70)
    print("TEST: List Profiles")
    print("=" * 70)
    
    engine = TerminalProfilesEngine()
    engine.create_profile("Profile1", ShellType.BASH, "/home/user")
    engine.create_profile("Profile2", ShellType.ZSH, "/home/user")
    
    result = engine.list_profiles()
    
    assert result.success, "Listeleme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: List profiles")
    print("=" * 70)


def test_list_profiles_with_scope():
    """
    Test: List profiles with scope.
    """
    print("=" * 70)
    print("TEST: List Profiles With Scope")
    print("=" * 70)
    
    engine = TerminalProfilesEngine()
    engine.create_profile("Profile1", ShellType.BASH, "/home/user", scope=ProfileScope.GLOBAL)
    engine.create_profile("Profile2", ShellType.ZSH, "/home/user", scope=ProfileScope.SESSION)
    
    result = engine.list_profiles(scope=ProfileScope.GLOBAL)
    
    assert result.success, "Listeleme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: List profiles with scope")
    print("=" * 70)


def test_activate_profile():
    """
    Test: Activate profile.
    """
    print("=" * 70)
    print("TEST: Activate Profile")
    print("=" * 70)
    
    engine = TerminalProfilesEngine()
    result = engine.create_profile("Default", ShellType.BASH, "/home/user")
    profile_id = result.profile_id
    
    result = engine.activate_profile(profile_id)
    
    assert result.success, "Aktifleştirme başarılı olmalı"
    assert engine.profiles[profile_id].is_active, "Profil aktif olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Activate profile")
    print("=" * 70)


def test_clone_profile():
    """
    Test: Clone profile.
    """
    print("=" * 70)
    print("TEST: Clone Profile")
    print("=" * 70)
    
    engine = TerminalProfilesEngine()
    result = engine.create_profile("Default", ShellType.BASH, "/home/user")
    profile_id = result.profile_id
    
    result = engine.clone_profile(profile_id, "Cloned")
    
    assert result.success, "Klonlama başarılı olmalı"
    assert result.profile_name == "Cloned", "Yeni ad eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  New profile ID: {result.profile_id}")
    print(f"  New profile name: {result.profile_name}")
    
    print("\n" + "=" * 70)
    print("PASS: Clone profile")
    print("=" * 70)


def test_export_profile():
    """
    Test: Export profile.
    """
    print("=" * 70)
    print("TEST: Export Profile")
    print("=" * 70)
    
    engine = TerminalProfilesEngine()
    result = engine.create_profile("Default", ShellType.BASH, "/home/user")
    profile_id = result.profile_id
    
    result = engine.export_profile(profile_id, format="json")
    
    assert result.success, "Dışa aktarma başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Export profile")
    print("=" * 70)


def test_import_profile():
    """
    Test: Import profile.
    """
    print("=" * 70)
    print("TEST: Import Profile")
    print("=" * 70)
    
    engine = TerminalProfilesEngine()
    
    data = {
        "name": "Imported",
        "shell_type": "bash",
        "working_directory": "/home/imported",
        "environment": {"VAR": "value"},
        "aliases": {"ll": "ls -la"}
    }
    
    result = engine.import_profile(data)
    
    assert result.success, "İçe aktarma başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Import profile")
    print("=" * 70)


def test_set_default_profile():
    """
    Test: Set default profile.
    """
    print("=" * 70)
    print("TEST: Set Default Profile")
    print("=" * 70)
    
    engine = TerminalProfilesEngine()
    result = engine.create_profile("Default", ShellType.BASH, "/home/user")
    profile_id = result.profile_id
    
    result = engine.set_default_profile(profile_id)
    
    assert result.success, "Ayarlama başarılı olmalı"
    assert engine.profiles[profile_id].is_default, "Profil varsayılan olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set default profile")
    print("=" * 70)


def test_get_profile_history():
    """
    Test: Get profile history.
    """
    print("=" * 70)
    print("TEST: Get Profile History")
    print("=" * 70)
    
    engine = TerminalProfilesEngine()
    engine.create_profile("Default", ShellType.BASH, "/home/user")
    
    history = engine.get_profile_history()
    
    assert len(history) > 0, "Geçmiş olmalı"
    
    print(f"  History: {len(history)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get profile history")
    print("=" * 70)


def test_clear_history():
    """
    Test: Clear history.
    """
    print("=" * 70)
    print("TEST: Clear History")
    print("=" * 70)
    
    engine = TerminalProfilesEngine()
    engine.create_profile("Default", ShellType.BASH, "/home/user")
    
    result = engine.clear_history()
    
    assert result.success, "Temizleme başarılı olmalı"
    assert len(engine.get_profile_history()) == 0, "Geçmiş temizlenmeli"
    
    print(f"  Success: {result.success}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear history")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    engine = TerminalProfilesEngine()
    
    new_config = ProfileConfig(persist_profiles=False)
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
    
    engine = TerminalProfilesEngine()
    
    config = engine.get_config()
    
    assert config is not None, "Config olmalı"
    assert config.persist_profiles == True, "Config eşleşmeli"
    
    print(f"  Persist profiles: {config.persist_profiles}")
    print(f"  Auto load profiles: {config.auto_load_profiles}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


def test_shell_type_enum():
    """
    Test: ShellType enum.
    """
    print("=" * 70)
    print("TEST: ShellType Enum")
    print("=" * 70)
    
    assert ShellType.BASH.value == "bash"
    assert ShellType.ZSH.value == "zsh"
    assert ShellType.FISH.value == "fish"
    assert ShellType.POWERSHELL.value == "powershell"
    assert ShellType.CMD.value == "cmd"
    assert ShellType.SH.value == "sh"
    assert ShellType.TCSH.value == "tcsh"
    assert ShellType.CSH.value == "csh"
    
    print(f"  All enum values verified")
    print(f"  Total shell types: {len(ShellType)}")
    
    print("\n" + "=" * 70)
    print("PASS: ShellType enum")
    print("=" * 70)


def test_profile_scope_enum():
    """
    Test: ProfileScope enum.
    """
    print("=" * 70)
    print("TEST: ProfileScope Enum")
    print("=" * 70)
    
    assert ProfileScope.SESSION.value == "session"
    assert ProfileScope.TERMINAL.value == "terminal"
    assert ProfileScope.GLOBAL.value == "global"
    
    print(f"  All enum values verified")
    print(f"  Total scopes: {len(ProfileScope)}")
    
    print("\n" + "=" * 70)
    print("PASS: ProfileScope enum")
    print("=" * 70)


def test_profile_action_enum():
    """
    Test: ProfileAction enum.
    """
    print("=" * 70)
    print("TEST: ProfileAction Enum")
    print("=" * 70)
    
    assert ProfileAction.CREATE.value == "create"
    assert ProfileAction.UPDATE.value == "update"
    assert ProfileAction.DELETE.value == "delete"
    assert ProfileAction.GET.value == "get"
    assert ProfileAction.LIST.value == "list"
    assert ProfileAction.ACTIVATE.value == "activate"
    assert ProfileAction.CLONE.value == "clone"
    assert ProfileAction.IMPORT.value == "import"
    assert ProfileAction.EXPORT.value == "export"
    assert ProfileAction.SET_DEFAULT.value == "set_default"
    
    print(f"  All enum values verified")
    print(f"  Total actions: {len(ProfileAction)}")
    
    print("\n" + "=" * 70)
    print("PASS: ProfileAction enum")
    print("=" * 70)


def test_profile_config_dataclass():
    """
    Test: ProfileConfig dataclass.
    """
    print("=" * 70)
    print("TEST: ProfileConfig Dataclass")
    print("=" * 70)
    
    config = ProfileConfig(
        persist_profiles=False,
        auto_load_profiles=False
    )
    
    assert config.persist_profiles == False, "Persist eşleşmeli"
    assert config.auto_load_profiles == False, "Auto load eşleşmeli"
    
    print(f"  Persist profiles: {config.persist_profiles}")
    print(f"  Auto load profiles: {config.auto_load_profiles}")
    
    print("\n" + "=" * 70)
    print("PASS: ProfileConfig dataclass")
    print("=" * 70)


def test_profile_entry_dataclass():
    """
    Test: ProfileEntry dataclass.
    """
    print("=" * 70)
    print("TEST: ProfileEntry Dataclass")
    print("=" * 70)
    
    entry = ProfileEntry(
        id="profile_1",
        name="Default",
        shell_type=ShellType.BASH,
        working_directory="/home/user",
        environment={},
        aliases={},
        shell_args=[],
        timestamp="2024-01-01T00:00:00"
    )
    
    assert entry.id == "profile_1", "ID eşleşmeli"
    assert entry.name == "Default", "Ad eşleşmeli"
    
    print(f"  ID: {entry.id}")
    print(f"  Name: {entry.name}")
    
    print("\n" + "=" * 70)
    print("PASS: ProfileEntry dataclass")
    print("=" * 70)


def test_profile_result_dataclass():
    """
    Test: ProfileResult dataclass.
    """
    print("=" * 70)
    print("TEST: ProfileResult Dataclass")
    print("=" * 70)
    
    result = ProfileResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: ProfileResult dataclass")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_create_profile()
        test2 = test_create_profile_with_options()
        test3 = test_update_profile()
        test4 = test_delete_profile()
        test5 = test_get_profile()
        test6 = test_list_profiles()
        test7 = test_list_profiles_with_scope()
        test8 = test_activate_profile()
        test9 = test_clone_profile()
        test10 = test_export_profile()
        test11 = test_import_profile()
        test12 = test_set_default_profile()
        test13 = test_get_profile_history()
        test14 = test_clear_history()
        test15 = test_update_config()
        test16 = test_get_config()
        test17 = test_shell_type_enum()
        test18 = test_profile_scope_enum()
        test19 = test_profile_action_enum()
        test20 = test_profile_config_dataclass()
        test21 = test_profile_entry_dataclass()
        test22 = test_profile_result_dataclass()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Create Profile: {'PASS' if test1 else 'FAIL'}")
        print(f"Create Profile With Options: {'PASS' if test2 else 'FAIL'}")
        print(f"Update Profile: {'PASS' if test3 else 'FAIL'}")
        print(f"Delete Profile: {'PASS' if test4 else 'FAIL'}")
        print(f"Get Profile: {'PASS' if test5 else 'FAIL'}")
        print(f"List Profiles: {'PASS' if test6 else 'FAIL'}")
        print(f"List Profiles With Scope: {'PASS' if test7 else 'FAIL'}")
        print(f"Activate Profile: {'PASS' if test8 else 'FAIL'}")
        print(f"Clone Profile: {'PASS' if test9 else 'FAIL'}")
        print(f"Export Profile: {'PASS' if test10 else 'FAIL'}")
        print(f"Import Profile: {'PASS' if test11 else 'FAIL'}")
        print(f"Set Default Profile: {'PASS' if test12 else 'FAIL'}")
        print(f"Get Profile History: {'PASS' if test13 else 'FAIL'}")
        print(f"Clear History: {'PASS' if test14 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test15 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test16 else 'FAIL'}")
        print(f"ShellType Enum: {'PASS' if test17 else 'FAIL'}")
        print(f"ProfileScope Enum: {'PASS' if test18 else 'FAIL'}")
        print(f"ProfileAction Enum: {'PASS' if test19 else 'FAIL'}")
        print(f"ProfileConfig Dataclass: {'PASS' if test20 else 'FAIL'}")
        print(f"ProfileEntry Dataclass: {'PASS' if test21 else 'FAIL'}")
        print(f"ProfileResult Dataclass: {'PASS' if test22 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14, test15, test16, test17, test18, test19, test20, test21, test22])
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
