"""
Quality Test: User Management
User management system testleri for security module.
"""

import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from app.security.user_management import (
    UserStatus,
    UserTier,
    UserProfile,
    UserPreferences,
    UserActivity,
    User,
    UserManagementConfig,
    UserManagementResult,
    UserManager
)


def test_user_status_enum():
    """
    Test: UserStatus enum.
    """
    print("=" * 70)
    print("TEST: UserStatus Enum")
    print("=" * 70)
    
    assert UserStatus.ACTIVE.value == "active"
    assert UserStatus.INACTIVE.value == "inactive"
    assert UserStatus.SUSPENDED.value == "suspended"
    assert UserStatus.DELETED.value == "deleted"
    assert UserStatus.PENDING.value == "pending"
    
    print(f"  All enum values verified")
    print(f"  Total statuses: {len(UserStatus)}")
    
    print("\n" + "=" * 70)
    print("PASS: UserStatus enum")
    print("=" * 70)


def test_user_tier_enum():
    """
    Test: UserTier enum.
    """
    print("=" * 70)
    print("TEST: UserTier Enum")
    print("=" * 70)
    
    assert UserTier.FREE.value == "free"
    assert UserTier.BASIC.value == "basic"
    assert UserTier.PRO.value == "pro"
    assert UserTier.ENTERPRISE.value == "enterprise"
    assert UserTier.CUSTOM.value == "custom"
    
    print(f"  All enum values verified")
    print(f"  Total tiers: {len(UserTier)}")
    
    print("\n" + "=" * 70)
    print("PASS: UserTier enum")
    print("=" * 70)


def test_user_profile_dataclass():
    """
    Test: UserProfile dataclass.
    """
    print("=" * 70)
    print("TEST: UserProfile Dataclass")
    print("=" * 70)
    
    profile = UserProfile(
        first_name="John",
        last_name="Doe"
    )
    
    assert profile.first_name == "John", "First name eşleşmeli"
    assert profile.last_name == "Doe", "Last name eşleşmeli"
    
    print(f"  First name: {profile.first_name}")
    print(f"  Last name: {profile.last_name}")
    
    print("\n" + "=" * 70)
    print("PASS: UserProfile dataclass")
    print("=" * 70)


def test_user_preferences_dataclass():
    """
    Test: UserPreferences dataclass.
    """
    print("=" * 70)
    print("TEST: UserPreferences Dataclass")
    print("=" * 70)
    
    preferences = UserPreferences(theme="dark")
    
    assert preferences.theme == "dark", "Theme eşleşmeli"
    
    print(f"  Theme: {preferences.theme}")
    
    print("\n" + "=" * 70)
    print("PASS: UserPreferences dataclass")
    print("=" * 70)


def test_user_activity_dataclass():
    """
    Test: UserActivity dataclass.
    """
    print("=" * 70)
    print("TEST: UserActivity Dataclass")
    print("=" * 70)
    
    activity = UserActivity(
        activity_id="activity_1",
        user_id="user_1",
        action="login"
    )
    
    assert activity.activity_id == "activity_1", "Activity ID eşleşmeli"
    assert activity.user_id == "user_1", "User ID eşleşmeli"
    assert activity.action == "login", "Action eşleşmeli"
    
    print(f"  Activity ID: {activity.activity_id}")
    print(f"  Action: {activity.action}")
    
    print("\n" + "=" * 70)
    print("PASS: UserActivity dataclass")
    print("=" * 70)


def test_user_dataclass():
    """
    Test: User dataclass.
    """
    print("=" * 70)
    print("TEST: User Dataclass")
    print("=" * 70)
    
    user = User(
        user_id="user_1",
        username="testuser",
        email="test@example.com"
    )
    
    assert user.user_id == "user_1", "User ID eşleşmeli"
    assert user.username == "testuser", "Username eşleşmeli"
    assert user.email == "test@example.com", "Email eşleşmeli"
    
    print(f"  User ID: {user.user_id}")
    print(f"  Username: {user.username}")
    
    print("\n" + "=" * 70)
    print("PASS: User dataclass")
    print("=" * 70)


def test_user_management_config_dataclass():
    """
    Test: UserManagementConfig dataclass.
    """
    print("=" * 70)
    print("TEST: UserManagementConfig Dataclass")
    print("=" * 70)
    
    config = UserManagementConfig(max_users=100)
    
    assert config.max_users == 100, "Max users eşleşmeli"
    
    print(f"  Max users: {config.max_users}")
    
    print("\n" + "=" * 70)
    print("PASS: UserManagementConfig dataclass")
    print("=" * 70)


def test_user_management_result_dataclass():
    """
    Test: UserManagementResult dataclass.
    """
    print("=" * 70)
    print("TEST: UserManagementResult Dataclass")
    print("=" * 70)
    
    result = UserManagementResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.users, list), "Users list olmalı"
    assert isinstance(result.activities, list), "Activities list olmalı"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: UserManagementResult dataclass")
    print("=" * 70)


def test_user_manager_initialization():
    """
    Test: UserManager initialization.
    """
    print("=" * 70)
    print("TEST: UserManager Initialization")
    print("=" * 70)
    
    config = UserManagementConfig()
    manager = UserManager(config)
    
    assert manager.config == config, "Config eşleşmeli"
    assert len(manager.users) == 0, "Users boş olmalı"
    assert len(manager.activities) == 0, "Activities boş olmalı"
    
    print(f"  Users: {len(manager.users)}")
    print(f"  Activities: {len(manager.activities)}")
    
    print("\n" + "=" * 70)
    print("PASS: UserManager initialization")
    print("=" * 70)


def test_create_user():
    """
    Test: Create user.
    """
    print("=" * 70)
    print("TEST: Create User")
    print("=" * 70)
    
    manager = UserManager()
    
    result = manager.create_user("testuser", "test@example.com")
    
    assert result.success == True, "Ekleme başarılı olmalı"
    assert len(manager.users) > 0, "User eklenmeli"
    
    print(f"  User created: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Create user")
    print("=" * 70)


def test_delete_user():
    """
    Test: Delete user.
    """
    print("=" * 70)
    print("TEST: Delete User")
    print("=" * 70)
    
    manager = UserManager()
    
    result = manager.create_user("testuser", "test@example.com")
    user_id = result.user.user_id
    
    result = manager.delete_user(user_id)
    
    assert result.success == True, "Silme başarılı olmalı"
    assert user_id not in manager.users, "User silinmeli"
    
    print(f"  User deleted: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Delete user")
    print("=" * 70)


def test_update_user():
    """
    Test: Update user.
    """
    print("=" * 70)
    print("TEST: Update User")
    print("=" * 70)
    
    manager = UserManager()
    
    result = manager.create_user("testuser", "test@example.com")
    user_id = result.user.user_id
    
    result = manager.update_user(user_id, username="newusername")
    
    assert result.success == True, "Update başarılı olmalı"
    
    print(f"  User updated: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Update user")
    print("=" * 70)


def test_get_user():
    """
    Test: Get user.
    """
    print("=" * 70)
    print("TEST: Get User")
    print("=" * 70)
    
    manager = UserManager()
    
    result = manager.create_user("testuser", "test@example.com")
    user_id = result.user.user_id
    
    user = manager.get_user(user_id)
    
    assert user is not None, "User bulunmalı"
    assert user.username == "testuser", "Username eşleşmeli"
    
    print(f"  User: {user.username}")
    
    print("\n" + "=" * 70)
    print("PASS: Get user")
    print("=" * 70)


def test_get_user_by_username():
    """
    Test: Get user by username.
    """
    print("=" * 70)
    print("TEST: Get User by Username")
    print("=" * 70)
    
    manager = UserManager()
    
    manager.create_user("testuser", "test@example.com")
    user = manager.get_user_by_username("testuser")
    
    assert user is not None, "User bulunmalı"
    
    print(f"  User: {user.username}")
    
    print("\n" + "=" * 70)
    print("PASS: Get user by username")
    print("=" * 70)


def test_get_user_by_email():
    """
    Test: Get user by email.
    """
    print("=" * 70)
    print("TEST: Get User by Email")
    print("=" * 70)
    
    manager = UserManager()
    
    manager.create_user("testuser", "test@example.com")
    user = manager.get_user_by_email("test@example.com")
    
    assert user is not None, "User bulunmalı"
    
    print(f"  User: {user.email}")
    
    print("\n" + "=" * 70)
    print("PASS: Get user by email")
    print("=" * 70)


def test_get_all_users():
    """
    Test: Get all users.
    """
    print("=" * 70)
    print("TEST: Get All Users")
    print("=" * 70)
    
    manager = UserManager()
    
    manager.create_user("testuser1", "test1@example.com")
    manager.create_user("testuser2", "test2@example.com")
    
    users = manager.get_all_users()
    
    assert len(users) == 2, "2 user olmalı"
    
    print(f"  Total users: {len(users)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get all users")
    print("=" * 70)


def test_search_users():
    """
    Test: Search users.
    """
    print("=" * 70)
    print("TEST: Search Users")
    print("=" * 70)
    
    manager = UserManager()
    
    manager.create_user("testuser", "test@example.com")
    users = manager.search_users("test")
    
    assert len(users) > 0, "Arama sonucu olmalı"
    
    print(f"  Search results: {len(users)}")
    
    print("\n" + "=" * 70)
    print("PASS: Search users")
    print("=" * 70)


def test_update_profile():
    """
    Test: Update profile.
    """
    print("=" * 70)
    print("TEST: Update Profile")
    print("=" * 70)
    
    manager = UserManager()
    
    result = manager.create_user("testuser", "test@example.com")
    user_id = result.user.user_id
    
    profile = UserProfile(first_name="John", last_name="Doe")
    result = manager.update_profile(user_id, profile)
    
    assert result.success == True, "Update başarılı olmalı"
    
    print(f"  Profile updated: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Update profile")
    print("=" * 70)


def test_update_preferences():
    """
    Test: Update preferences.
    """
    print("=" * 70)
    print("TEST: Update Preferences")
    print("=" * 70)
    
    manager = UserManager()
    
    result = manager.create_user("testuser", "test@example.com")
    user_id = result.user.user_id
    
    preferences = UserPreferences(theme="light")
    result = manager.update_preferences(user_id, preferences)
    
    assert result.success == True, "Update başarılı olmalı"
    
    print(f"  Preferences updated: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Update preferences")
    print("=" * 70)


def test_set_user_status():
    """
    Test: Set user status.
    """
    print("=" * 70)
    print("TEST: Set User Status")
    print("=" * 70)
    
    manager = UserManager()
    
    result = manager.create_user("testuser", "test@example.com")
    user_id = result.user.user_id
    
    result = manager.set_user_status(user_id, UserStatus.INACTIVE)
    
    assert result.success == True, "Set başarılı olmalı"
    
    print(f"  User status set: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set user status")
    print("=" * 70)


def test_set_user_tier():
    """
    Test: Set user tier.
    """
    print("=" * 70)
    print("TEST: Set User Tier")
    print("=" * 70)
    
    manager = UserManager()
    
    result = manager.create_user("testuser", "test@example.com")
    user_id = result.user.user_id
    
    result = manager.set_user_tier(user_id, UserTier.PRO)
    
    assert result.success == True, "Set başarılı olmalı"
    
    print(f"  User tier set: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set user tier")
    print("=" * 70)


def test_get_user_activities():
    """
    Test: Get user activities.
    """
    print("=" * 70)
    print("TEST: Get User Activities")
    print("=" * 70)
    
    manager = UserManager()
    
    result = manager.create_user("testuser", "test@example.com")
    user_id = result.user.user_id
    
    activities = manager.get_user_activities(user_id)
    
    assert len(activities) > 0, "Activities olmalı"
    
    print(f"  User activities: {len(activities)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get user activities")
    print("=" * 70)


def test_get_all_activities():
    """
    Test: Get all activities.
    """
    print("=" * 70)
    print("TEST: Get All Activities")
    print("=" * 70)
    
    manager = UserManager()
    
    manager.create_user("testuser", "test@example.com")
    
    activities = manager.get_all_activities()
    
    assert len(activities) > 0, "Activities olmalı"
    
    print(f"  Total activities: {len(activities)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get all activities")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    manager = UserManager()
    
    new_config = UserManagementConfig(max_users=500)
    result = manager.update_config(new_config)
    
    assert result.success == True, "Update başarılı olmalı"
    assert manager.config.max_users == 500, "Config güncellenmeli"
    
    print(f"  Max users: {manager.config.max_users}")
    
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
    
    config = UserManagementConfig(max_users=500)
    manager = UserManager(config)
    
    retrieved_config = manager.get_config()
    
    assert retrieved_config.max_users == 500, "Config eşleşmeli"
    
    print(f"  Max users: {retrieved_config.max_users}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_user_status_enum()
        test2 = test_user_tier_enum()
        test3 = test_user_profile_dataclass()
        test4 = test_user_preferences_dataclass()
        test5 = test_user_activity_dataclass()
        test6 = test_user_dataclass()
        test7 = test_user_management_config_dataclass()
        test8 = test_user_management_result_dataclass()
        test9 = test_user_manager_initialization()
        test10 = test_create_user()
        test11 = test_delete_user()
        test12 = test_update_user()
        test13 = test_get_user()
        test14 = test_get_user_by_username()
        test15 = test_get_user_by_email()
        test16 = test_get_all_users()
        test17 = test_search_users()
        test18 = test_update_profile()
        test19 = test_update_preferences()
        test20 = test_set_user_status()
        test21 = test_set_user_tier()
        test22 = test_get_user_activities()
        test23 = test_get_all_activities()
        test24 = test_update_config()
        test25 = test_get_config()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"UserStatus Enum: {'PASS' if test1 else 'FAIL'}")
        print(f"UserTier Enum: {'PASS' if test2 else 'FAIL'}")
        print(f"UserProfile Dataclass: {'PASS' if test3 else 'FAIL'}")
        print(f"UserPreferences Dataclass: {'PASS' if test4 else 'FAIL'}")
        print(f"UserActivity Dataclass: {'PASS' if test5 else 'FAIL'}")
        print(f"User Dataclass: {'PASS' if test6 else 'FAIL'}")
        print(f"UserManagementConfig Dataclass: {'PASS' if test7 else 'FAIL'}")
        print(f"UserManagementResult Dataclass: {'PASS' if test8 else 'FAIL'}")
        print(f"UserManager Initialization: {'PASS' if test9 else 'FAIL'}")
        print(f"Create User: {'PASS' if test10 else 'FAIL'}")
        print(f"Delete User: {'PASS' if test11 else 'FAIL'}")
        print(f"Update User: {'PASS' if test12 else 'FAIL'}")
        print(f"Get User: {'PASS' if test13 else 'FAIL'}")
        print(f"Get User by Username: {'PASS' if test14 else 'FAIL'}")
        print(f"Get User by Email: {'PASS' if test15 else 'FAIL'}")
        print(f"Get All Users: {'PASS' if test16 else 'FAIL'}")
        print(f"Search Users: {'PASS' if test17 else 'FAIL'}")
        print(f"Update Profile: {'PASS' if test18 else 'FAIL'}")
        print(f"Update Preferences: {'PASS' if test19 else 'FAIL'}")
        print(f"Set User Status: {'PASS' if test20 else 'FAIL'}")
        print(f"Set User Tier: {'PASS' if test21 else 'FAIL'}")
        print(f"Get User Activities: {'PASS' if test22 else 'FAIL'}")
        print(f"Get All Activities: {'PASS' if test23 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test24 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test25 else 'FAIL'}")
        
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
