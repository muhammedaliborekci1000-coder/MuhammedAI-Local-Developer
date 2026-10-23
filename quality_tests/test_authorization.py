"""
Quality Test: Authorization
Authorization system testleri for security module.
"""

import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from app.security.authorization import (
    Permission,
    ResourceType,
    AccessDecision,
    Role,
    Policy,
    AccessRequest,
    AccessResult,
    AuthorizationConfig,
    AuthorizationManager
)


def test_permission_enum():
    """
    Test: Permission enum.
    """
    print("=" * 70)
    print("TEST: Permission Enum")
    print("=" * 70)
    
    assert Permission.READ.value == "read"
    assert Permission.WRITE.value == "write"
    assert Permission.DELETE.value == "delete"
    assert Permission.EXECUTE.value == "execute"
    assert Permission.ADMIN.value == "admin"
    assert Permission.MANAGE.value == "manage"
    assert Permission.VIEW.value == "view"
    assert Permission.EDIT.value == "edit"
    assert Permission.CREATE.value == "create"
    assert Permission.UPDATE.value == "update"
    assert Permission.CUSTOM.value == "custom"
    
    print(f"  All enum values verified")
    print(f"  Total permissions: {len(Permission)}")
    
    print("\n" + "=" * 70)
    print("PASS: Permission enum")
    print("=" * 70)


def test_resource_type_enum():
    """
    Test: ResourceType enum.
    """
    print("=" * 70)
    print("TEST: ResourceType Enum")
    print("=" * 70)
    
    assert ResourceType.FILE.value == "file"
    assert ResourceType.DIRECTORY.value == "directory"
    assert ResourceType.PROJECT.value == "project"
    assert ResourceType.SETTINGS.value == "settings"
    assert ResourceType.USER.value == "user"
    assert ResourceType.ROLE.value == "role"
    assert ResourceType.API.value == "api"
    assert ResourceType.DATABASE.value == "database"
    assert ResourceType.SYSTEM.value == "system"
    assert ResourceType.CUSTOM.value == "custom"
    
    print(f"  All enum values verified")
    print(f"  Total resource types: {len(ResourceType)}")
    
    print("\n" + "=" * 70)
    print("PASS: ResourceType enum")
    print("=" * 70)


def test_access_decision_enum():
    """
    Test: AccessDecision enum.
    """
    print("=" * 70)
    print("TEST: AccessDecision Enum")
    print("=" * 70)
    
    assert AccessDecision.ALLOW.value == "allow"
    assert AccessDecision.DENY.value == "deny"
    assert AccessDecision.ABSTAIN.value == "abstain"
    
    print(f"  All enum values verified")
    print(f"  Total decisions: {len(AccessDecision)}")
    
    print("\n" + "=" * 70)
    print("PASS: AccessDecision enum")
    print("=" * 70)


def test_role_dataclass():
    """
    Test: Role dataclass.
    """
    print("=" * 70)
    print("TEST: Role Dataclass")
    print("=" * 70)
    
    role = Role(
        id="role_1",
        name="Admin",
        description="Administrator role"
    )
    
    assert role.id == "role_1", "ID eşleşmeli"
    assert role.name == "Admin", "Name eşleşmeli"
    assert role.description == "Administrator role", "Description eşleşmeli"
    
    print(f"  ID: {role.id}")
    print(f"  Name: {role.name}")
    
    print("\n" + "=" * 70)
    print("PASS: Role dataclass")
    print("=" * 70)


def test_policy_dataclass():
    """
    Test: Policy dataclass.
    """
    print("=" * 70)
    print("TEST: Policy Dataclass")
    print("=" * 70)
    
    policy = Policy(
        id="policy_1",
        name="Read Policy",
        description="Read access policy",
        effect=AccessDecision.ALLOW
    )
    
    assert policy.id == "policy_1", "ID eşleşmeli"
    assert policy.name == "Read Policy", "Name eşleşmeli"
    assert policy.effect == AccessDecision.ALLOW, "Effect eşleşmeli"
    
    print(f"  ID: {policy.id}")
    print(f"  Name: {policy.name}")
    
    print("\n" + "=" * 70)
    print("PASS: Policy dataclass")
    print("=" * 70)


def test_access_request_dataclass():
    """
    Test: AccessRequest dataclass.
    """
    print("=" * 70)
    print("TEST: AccessRequest Dataclass")
    print("=" * 70)
    
    request = AccessRequest(
        user_id="user_1",
        permission=Permission.READ,
        resource_type=ResourceType.FILE
    )
    
    assert request.user_id == "user_1", "User ID eşleşmeli"
    assert request.permission == Permission.READ, "Permission eşleşmeli"
    assert request.resource_type == ResourceType.FILE, "Resource type eşleşmeli"
    
    print(f"  User ID: {request.user_id}")
    print(f"  Permission: {request.permission.value}")
    
    print("\n" + "=" * 70)
    print("PASS: AccessRequest dataclass")
    print("=" * 70)


def test_access_result_dataclass():
    """
    Test: AccessResult dataclass.
    """
    print("=" * 70)
    print("TEST: AccessResult Dataclass")
    print("=" * 70)
    
    result = AccessResult(decision=AccessDecision.ALLOW, allowed=True)
    result.reason = "Test reason"
    
    assert result.decision == AccessDecision.ALLOW, "Decision eşleşmeli"
    assert result.allowed == True, "Allowed eşleşmeli"
    assert result.reason == "Test reason", "Reason eşleşmeli"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Decision: {result.decision.value}")
    print(f"  Allowed: {result.allowed}")
    
    print("\n" + "=" * 70)
    print("PASS: AccessResult dataclass")
    print("=" * 70)


def test_authorization_config_dataclass():
    """
    Test: AuthorizationConfig dataclass.
    """
    print("=" * 70)
    print("TEST: AuthorizationConfig Dataclass")
    print("=" * 70)
    
    config = AuthorizationConfig(default_deny=True)
    
    assert config.default_deny == True, "Default deny eşleşmeli"
    
    print(f"  Default deny: {config.default_deny}")
    
    print("\n" + "=" * 70)
    print("PASS: AuthorizationConfig dataclass")
    print("=" * 70)


def test_authorization_manager_initialization():
    """
    Test: AuthorizationManager initialization.
    """
    print("=" * 70)
    print("TEST: AuthorizationManager Initialization")
    print("=" * 70)
    
    config = AuthorizationConfig()
    manager = AuthorizationManager(config)
    
    assert manager.config == config, "Config eşleşmeli"
    assert len(manager.roles) == 0, "Roles boş olmalı"
    assert len(manager.policies) == 0, "Policies boş olmalı"
    
    print(f"  Roles: {len(manager.roles)}")
    print(f"  Policies: {len(manager.policies)}")
    
    print("\n" + "=" * 70)
    print("PASS: AuthorizationManager initialization")
    print("=" * 70)


def test_add_role():
    """
    Test: Add role.
    """
    print("=" * 70)
    print("TEST: Add Role")
    print("=" * 70)
    
    manager = AuthorizationManager()
    
    role = Role(
        id="",
        name="Admin",
        description="Administrator role"
    )
    
    result = manager.add_role(role)
    
    assert result == True, "Ekleme başarılı olmalı"
    assert len(manager.roles) > 0, "Role eklenmeli"
    
    print(f"  Role added: {role.id}")
    
    print("\n" + "=" * 70)
    print("PASS: Add role")
    print("=" * 70)


def test_remove_role():
    """
    Test: Remove role.
    """
    print("=" * 70)
    print("TEST: Remove Role")
    print("=" * 70)
    
    manager = AuthorizationManager()
    
    role = Role(
        id="",
        name="Admin",
        description="Administrator role"
    )
    
    manager.add_role(role)
    role_id = role.id
    
    result = manager.remove_role(role_id)
    
    assert result == True, "Silme başarılı olmalı"
    assert role_id not in manager.roles, "Role silinmeli"
    
    print(f"  Role removed")
    
    print("\n" + "=" * 70)
    print("PASS: Remove role")
    print("=" * 70)


def test_get_role():
    """
    Test: Get role.
    """
    print("=" * 70)
    print("TEST: Get Role")
    print("=" * 70)
    
    manager = AuthorizationManager()
    
    role = Role(
        id="",
        name="Admin",
        description="Administrator role"
    )
    
    manager.add_role(role)
    retrieved_role = manager.get_role(role.id)
    
    assert retrieved_role is not None, "Role bulunmalı"
    assert retrieved_role.name == "Admin", "Name eşleşmeli"
    
    print(f"  Role: {retrieved_role.name}")
    
    print("\n" + "=" * 70)
    print("PASS: Get role")
    print("=" * 70)


def test_get_all_roles():
    """
    Test: Get all roles.
    """
    print("=" * 70)
    print("TEST: Get All Roles")
    print("=" * 70)
    
    manager = AuthorizationManager()
    
    role = Role(
        id="",
        name="Admin",
        description="Administrator role"
    )
    
    manager.add_role(role)
    roles = manager.get_all_roles()
    
    assert len(roles) > 0, "Roles olmalı"
    
    print(f"  Total roles: {len(roles)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get all roles")
    print("=" * 70)


def test_assign_role_to_user():
    """
    Test: Assign role to user.
    """
    print("=" * 70)
    print("TEST: Assign Role to User")
    print("=" * 70)
    
    manager = AuthorizationManager()
    
    role = Role(
        id="",
        name="Admin",
        description="Administrator role"
    )
    
    manager.add_role(role)
    result = manager.assign_role_to_user("user_1", role.id)
    
    assert result == True, "Atama başarılı olmalı"
    
    print(f"  Role assigned to user")
    
    print("\n" + "=" * 70)
    print("PASS: Assign role to user")
    print("=" * 70)


def test_remove_role_from_user():
    """
    Test: Remove role from user.
    """
    print("=" * 70)
    print("TEST: Remove Role from User")
    print("=" * 70)
    
    manager = AuthorizationManager()
    
    role = Role(
        id="",
        name="Admin",
        description="Administrator role"
    )
    
    manager.add_role(role)
    manager.assign_role_to_user("user_1", role.id)
    result = manager.remove_role_from_user("user_1", role.id)
    
    assert result == True, "Kaldırma başarılı olmalı"
    
    print(f"  Role removed from user")
    
    print("\n" + "=" * 70)
    print("PASS: Remove role from user")
    print("=" * 70)


def test_get_user_roles():
    """
    Test: Get user roles.
    """
    print("=" * 70)
    print("TEST: Get User Roles")
    print("=" * 70)
    
    manager = AuthorizationManager()
    
    role = Role(
        id="",
        name="Admin",
        description="Administrator role"
    )
    
    manager.add_role(role)
    manager.assign_role_to_user("user_1", role.id)
    roles = manager.get_user_roles("user_1")
    
    assert len(roles) > 0, "User roles olmalı"
    
    print(f"  User roles: {len(roles)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get user roles")
    print("=" * 70)


def test_add_policy():
    """
    Test: Add policy.
    """
    print("=" * 70)
    print("TEST: Add Policy")
    print("=" * 70)
    
    manager = AuthorizationManager()
    
    policy = Policy(
        id="",
        name="Read Policy",
        description="Read access policy",
        effect=AccessDecision.ALLOW
    )
    
    result = manager.add_policy(policy)
    
    assert result == True, "Ekleme başarılı olmalı"
    assert len(manager.policies) > 0, "Policy eklenmeli"
    
    print(f"  Policy added: {policy.id}")
    
    print("\n" + "=" * 70)
    print("PASS: Add policy")
    print("=" * 70)


def test_remove_policy():
    """
    Test: Remove policy.
    """
    print("=" * 70)
    print("TEST: Remove Policy")
    print("=" * 70)
    
    manager = AuthorizationManager()
    
    policy = Policy(
        id="",
        name="Read Policy",
        description="Read access policy",
        effect=AccessDecision.ALLOW
    )
    
    manager.add_policy(policy)
    policy_id = policy.id
    
    result = manager.remove_policy(policy_id)
    
    assert result == True, "Silme başarılı olmalı"
    assert policy_id not in manager.policies, "Policy silinmeli"
    
    print(f"  Policy removed")
    
    print("\n" + "=" * 70)
    print("PASS: Remove policy")
    print("=" * 70)


def test_get_policy():
    """
    Test: Get policy.
    """
    print("=" * 70)
    print("TEST: Get Policy")
    print("=" * 70)
    
    manager = AuthorizationManager()
    
    policy = Policy(
        id="",
        name="Read Policy",
        description="Read access policy",
        effect=AccessDecision.ALLOW
    )
    
    manager.add_policy(policy)
    retrieved_policy = manager.get_policy(policy.id)
    
    assert retrieved_policy is not None, "Policy bulunmalı"
    assert retrieved_policy.name == "Read Policy", "Name eşleşmeli"
    
    print(f"  Policy: {retrieved_policy.name}")
    
    print("\n" + "=" * 70)
    print("PASS: Get policy")
    print("=" * 70)


def test_get_all_policies():
    """
    Test: Get all policies.
    """
    print("=" * 70)
    print("TEST: Get All Policies")
    print("=" * 70)
    
    manager = AuthorizationManager()
    
    policy = Policy(
        id="",
        name="Read Policy",
        description="Read access policy",
        effect=AccessDecision.ALLOW
    )
    
    manager.add_policy(policy)
    policies = manager.get_all_policies()
    
    assert len(policies) > 0, "Policies olmalı"
    
    print(f"  Total policies: {len(policies)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get all policies")
    print("=" * 70)


def test_check_permission():
    """
    Test: Check permission.
    """
    print("=" * 70)
    print("TEST: Check Permission")
    print("=" * 70)
    
    manager = AuthorizationManager()
    
    role = Role(
        id="",
        name="Admin",
        description="Administrator role",
        permissions={Permission.READ, Permission.WRITE}
    )
    
    manager.add_role(role)
    manager.assign_role_to_user("user_1", role.id)
    
    has_permission = manager.check_permission("user_1", Permission.READ)
    
    assert has_permission == True, "Permission olmalı"
    
    print(f"  Has READ permission: {has_permission}")
    
    print("\n" + "=" * 70)
    print("PASS: Check permission")
    print("=" * 70)


def test_check_access():
    """
    Test: Check access.
    """
    print("=" * 70)
    print("TEST: Check Access")
    print("=" * 70)
    
    manager = AuthorizationManager()
    
    # Create role and assign to user
    role = Role(
        id="",
        name="Admin",
        description="Administrator role"
    )
    
    manager.add_role(role)
    manager.assign_role_to_user("user_1", role.id)
    
    # Create policy
    policy = Policy(
        id="",
        name="Read Policy",
        description="Read access policy",
        effect=AccessDecision.ALLOW,
        permissions={Permission.READ},
        resource_types={ResourceType.FILE},
        role_ids={role.id}
    )
    
    manager.add_policy(policy)
    
    # Check access
    request = AccessRequest(
        user_id="user_1",
        permission=Permission.READ,
        resource_type=ResourceType.FILE
    )
    
    result = manager.check_access(request)
    
    assert result.allowed == True, "Access izinli olmalı"
    
    print(f"  Access allowed: {result.allowed}")
    
    print("\n" + "=" * 70)
    print("PASS: Check access")
    print("=" * 70)


def test_grant_permission():
    """
    Test: Grant permission.
    """
    print("=" * 70)
    print("TEST: Grant Permission")
    print("=" * 70)
    
    manager = AuthorizationManager()
    
    role = Role(
        id="",
        name="Admin",
        description="Administrator role"
    )
    
    manager.add_role(role)
    result = manager.grant_permission(role.id, Permission.READ)
    
    assert result == True, "Grant başarılı olmalı"
    
    print(f"  Permission granted")
    
    print("\n" + "=" * 70)
    print("PASS: Grant permission")
    print("=" * 70)


def test_revoke_permission():
    """
    Test: Revoke permission.
    """
    print("=" * 70)
    print("TEST: Revoke Permission")
    print("=" * 70)
    
    manager = AuthorizationManager()
    
    role = Role(
        id="",
        name="Admin",
        description="Administrator role",
        permissions={Permission.READ}
    )
    
    manager.add_role(role)
    result = manager.revoke_permission(role.id, Permission.READ)
    
    assert result == True, "Revoke başarılı olmalı"
    
    print(f"  Permission revoked")
    
    print("\n" + "=" * 70)
    print("PASS: Revoke permission")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    manager = AuthorizationManager()
    
    new_config = AuthorizationConfig(default_deny=False)
    result = manager.update_config(new_config)
    
    assert result == True, "Update başarılı olmalı"
    assert manager.config.default_deny == False, "Config güncellenmeli"
    
    print(f"  Default deny: {manager.config.default_deny}")
    
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
    
    config = AuthorizationConfig(default_deny=False)
    manager = AuthorizationManager(config)
    
    retrieved_config = manager.get_config()
    
    assert retrieved_config.default_deny == False, "Config eşleşmeli"
    
    print(f"  Default deny: {retrieved_config.default_deny}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_permission_enum()
        test2 = test_resource_type_enum()
        test3 = test_access_decision_enum()
        test4 = test_role_dataclass()
        test5 = test_policy_dataclass()
        test6 = test_access_request_dataclass()
        test7 = test_access_result_dataclass()
        test8 = test_authorization_config_dataclass()
        test9 = test_authorization_manager_initialization()
        test10 = test_add_role()
        test11 = test_remove_role()
        test12 = test_get_role()
        test13 = test_get_all_roles()
        test14 = test_assign_role_to_user()
        test15 = test_remove_role_from_user()
        test16 = test_get_user_roles()
        test17 = test_add_policy()
        test18 = test_remove_policy()
        test19 = test_get_policy()
        test20 = test_get_all_policies()
        test21 = test_check_permission()
        test22 = test_check_access()
        test23 = test_grant_permission()
        test24 = test_revoke_permission()
        test25 = test_update_config()
        test26 = test_get_config()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Permission Enum: {'PASS' if test1 else 'FAIL'}")
        print(f"ResourceType Enum: {'PASS' if test2 else 'FAIL'}")
        print(f"AccessDecision Enum: {'PASS' if test3 else 'FAIL'}")
        print(f"Role Dataclass: {'PASS' if test4 else 'FAIL'}")
        print(f"Policy Dataclass: {'PASS' if test5 else 'FAIL'}")
        print(f"AccessRequest Dataclass: {'PASS' if test6 else 'FAIL'}")
        print(f"AccessResult Dataclass: {'PASS' if test7 else 'FAIL'}")
        print(f"AuthorizationConfig Dataclass: {'PASS' if test8 else 'FAIL'}")
        print(f"AuthorizationManager Initialization: {'PASS' if test9 else 'FAIL'}")
        print(f"Add Role: {'PASS' if test10 else 'FAIL'}")
        print(f"Remove Role: {'PASS' if test11 else 'FAIL'}")
        print(f"Get Role: {'PASS' if test12 else 'FAIL'}")
        print(f"Get All Roles: {'PASS' if test13 else 'FAIL'}")
        print(f"Assign Role to User: {'PASS' if test14 else 'FAIL'}")
        print(f"Remove Role from User: {'PASS' if test15 else 'FAIL'}")
        print(f"Get User Roles: {'PASS' if test16 else 'FAIL'}")
        print(f"Add Policy: {'PASS' if test17 else 'FAIL'}")
        print(f"Remove Policy: {'PASS' if test18 else 'FAIL'}")
        print(f"Get Policy: {'PASS' if test19 else 'FAIL'}")
        print(f"Get All Policies: {'PASS' if test20 else 'FAIL'}")
        print(f"Check Permission: {'PASS' if test21 else 'FAIL'}")
        print(f"Check Access: {'PASS' if test22 else 'FAIL'}")
        print(f"Grant Permission: {'PASS' if test23 else 'FAIL'}")
        print(f"Revoke Permission: {'PASS' if test24 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test25 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test26 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14, test15, test16, test17, test18, test19, test20, test21, test22, test23, test24, test25, test26])
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
