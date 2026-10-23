"""
Quality Test: Role Management
Role management system testleri for security module.
"""

import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from app.security.role_management import (
    RoleType,
    RoleScope,
    RolePermission,
    Role,
    RoleHierarchy,
    RoleManagementConfig,
    RoleManagementResult,
    RoleManager
)


def test_role_type_enum():
    """
    Test: RoleType enum.
    """
    print("=" * 70)
    print("TEST: RoleType Enum")
    print("=" * 70)
    
    assert RoleType.SYSTEM.value == "system"
    assert RoleType.CUSTOM.value == "custom"
    assert RoleType.DEFAULT.value == "default"
    assert RoleType.TEMPORARY.value == "temporary"
    
    print(f"  All enum values verified")
    print(f"  Total types: {len(RoleType)}")
    
    print("\n" + "=" * 70)
    print("PASS: RoleType enum")
    print("=" * 70)


def test_role_scope_enum():
    """
    Test: RoleScope enum.
    """
    print("=" * 70)
    print("TEST: RoleScope Enum")
    print("=" * 70)
    
    assert RoleScope.GLOBAL.value == "global"
    assert RoleScope.PROJECT.value == "project"
    assert RoleScope.ORGANIZATION.value == "organization"
    assert RoleScope.TEAM.value == "team"
    assert RoleScope.CUSTOM.value == "custom"
    
    print(f"  All enum values verified")
    print(f"  Total scopes: {len(RoleScope)}")
    
    print("\n" + "=" * 70)
    print("PASS: RoleScope enum")
    print("=" * 70)


def test_role_permission_dataclass():
    """
    Test: RolePermission dataclass.
    """
    print("=" * 70)
    print("TEST: RolePermission Dataclass")
    print("=" * 70)
    
    permission = RolePermission(
        permission_id="perm_1",
        name="read",
        description="Read permission"
    )
    
    assert permission.permission_id == "perm_1", "Permission ID eşleşmeli"
    assert permission.name == "read", "Name eşleşmeli"
    
    print(f"  Permission ID: {permission.permission_id}")
    print(f"  Name: {permission.name}")
    
    print("\n" + "=" * 70)
    print("PASS: RolePermission dataclass")
    print("=" * 70)


def test_role_dataclass():
    """
    Test: Role dataclass.
    """
    print("=" * 70)
    print("TEST: Role Dataclass")
    print("=" * 70)
    
    role = Role(
        role_id="role_1",
        name="Admin",
        description="Administrator role"
    )
    
    assert role.role_id == "role_1", "Role ID eşleşmeli"
    assert role.name == "Admin", "Name eşleşmeli"
    
    print(f"  Role ID: {role.role_id}")
    print(f"  Name: {role.name}")
    
    print("\n" + "=" * 70)
    print("PASS: Role dataclass")
    print("=" * 70)


def test_role_hierarchy_dataclass():
    """
    Test: RoleHierarchy dataclass.
    """
    print("=" * 70)
    print("TEST: RoleHierarchy Dataclass")
    print("=" * 70)
    
    hierarchy = RoleHierarchy(
        parent_role_id="role_1",
        child_role_id="role_2"
    )
    
    assert hierarchy.parent_role_id == "role_1", "Parent role ID eşleşmeli"
    assert hierarchy.child_role_id == "role_2", "Child role ID eşleşmeli"
    
    print(f"  Parent: {hierarchy.parent_role_id}")
    print(f"  Child: {hierarchy.child_role_id}")
    
    print("\n" + "=" * 70)
    print("PASS: RoleHierarchy dataclass")
    print("=" * 70)


def test_role_management_config_dataclass():
    """
    Test: RoleManagementConfig dataclass.
    """
    print("=" * 70)
    print("TEST: RoleManagementConfig Dataclass")
    print("=" * 70)
    
    config = RoleManagementConfig(max_roles=50)
    
    assert config.max_roles == 50, "Max roles eşleşmeli"
    
    print(f"  Max roles: {config.max_roles}")
    
    print("\n" + "=" * 70)
    print("PASS: RoleManagementConfig dataclass")
    print("=" * 70)


def test_role_management_result_dataclass():
    """
    Test: RoleManagementResult dataclass.
    """
    print("=" * 70)
    print("TEST: RoleManagementResult Dataclass")
    print("=" * 70)
    
    result = RoleManagementResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.roles, list), "Roles list olmalı"
    assert isinstance(result.hierarchies, list), "Hierarchies list olmalı"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: RoleManagementResult dataclass")
    print("=" * 70)


def test_role_manager_initialization():
    """
    Test: RoleManager initialization.
    """
    print("=" * 70)
    print("TEST: RoleManager Initialization")
    print("=" * 70)
    
    config = RoleManagementConfig(enable_default_roles=False)
    manager = RoleManager(config)
    
    assert manager.config == config, "Config eşleşmeli"
    assert len(manager.roles) == 0, "Roles boş olmalı"
    
    print(f"  Roles: {len(manager.roles)}")
    
    print("\n" + "=" * 70)
    print("PASS: RoleManager initialization")
    print("=" * 70)


def test_create_role():
    """
    Test: Create role.
    """
    print("=" * 70)
    print("TEST: Create Role")
    print("=" * 70)
    
    config = RoleManagementConfig(enable_default_roles=False)
    manager = RoleManager(config)
    
    result = manager.create_role("Editor", "Editor role")
    
    assert result.success == True, "Ekleme başarılı olmalı"
    assert len(manager.roles) > 0, "Role eklenmeli"
    
    print(f"  Role created: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Create role")
    print("=" * 70)


def test_delete_role():
    """
    Test: Delete role.
    """
    print("=" * 70)
    print("TEST: Delete Role")
    print("=" * 70)
    
    config = RoleManagementConfig(enable_default_roles=False)
    manager = RoleManager(config)
    
    result = manager.create_role("Editor", "Editor role")
    role_id = result.role.role_id
    
    result = manager.delete_role(role_id)
    
    assert result.success == True, "Silme başarılı olmalı"
    assert role_id not in manager.roles, "Role silinmeli"
    
    print(f"  Role deleted: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Delete role")
    print("=" * 70)


def test_update_role():
    """
    Test: Update role.
    """
    print("=" * 70)
    print("TEST: Update Role")
    print("=" * 70)
    
    config = RoleManagementConfig(enable_default_roles=False)
    manager = RoleManager(config)
    
    result = manager.create_role("Editor", "Editor role")
    role_id = result.role.role_id
    
    result = manager.update_role(role_id, description="Updated description")
    
    assert result.success == True, "Update başarılı olmalı"
    
    print(f"  Role updated: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Update role")
    print("=" * 70)


def test_get_role():
    """
    Test: Get role.
    """
    print("=" * 70)
    print("TEST: Get Role")
    print("=" * 70)
    
    config = RoleManagementConfig(enable_default_roles=False)
    manager = RoleManager(config)
    
    result = manager.create_role("Editor", "Editor role")
    role_id = result.role.role_id
    
    role = manager.get_role(role_id)
    
    assert role is not None, "Role bulunmalı"
    assert role.name == "Editor", "Name eşleşmeli"
    
    print(f"  Role: {role.name}")
    
    print("\n" + "=" * 70)
    print("PASS: Get role")
    print("=" * 70)


def test_get_role_by_name():
    """
    Test: Get role by name.
    """
    print("=" * 70)
    print("TEST: Get Role by Name")
    print("=" * 70)
    
    config = RoleManagementConfig(enable_default_roles=False)
    manager = RoleManager(config)
    
    manager.create_role("Editor", "Editor role")
    role = manager.get_role_by_name("Editor")
    
    assert role is not None, "Role bulunmalı"
    
    print(f"  Role: {role.name}")
    
    print("\n" + "=" * 70)
    print("PASS: Get role by name")
    print("=" * 70)


def test_get_all_roles():
    """
    Test: Get all roles.
    """
    print("=" * 70)
    print("TEST: Get All Roles")
    print("=" * 70)
    
    config = RoleManagementConfig(enable_default_roles=False)
    manager = RoleManager(config)
    
    manager.create_role("Editor", "Editor role")
    manager.create_role("Viewer", "Viewer role")
    
    roles = manager.get_all_roles()
    
    assert len(roles) == 2, "2 role olmalı"
    
    print(f"  Total roles: {len(roles)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get all roles")
    print("=" * 70)


def test_assign_permission():
    """
    Test: Assign permission.
    """
    print("=" * 70)
    print("TEST: Assign Permission")
    print("=" * 70)
    
    config = RoleManagementConfig(enable_default_roles=False)
    manager = RoleManager(config)
    
    result = manager.create_role("Editor", "Editor role")
    role_id = result.role.role_id
    
    result = manager.assign_permission(role_id, "read")
    
    assert result.success == True, "Assign başarılı olmalı"
    
    print(f"  Permission assigned: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Assign permission")
    print("=" * 70)


def test_revoke_permission():
    """
    Test: Revoke permission.
    """
    print("=" * 70)
    print("TEST: Revoke Permission")
    print("=" * 70)
    
    config = RoleManagementConfig(enable_default_roles=False)
    manager = RoleManager(config)
    
    result = manager.create_role("Editor", "Editor role")
    role_id = result.role.role_id
    
    manager.assign_permission(role_id, "read")
    result = manager.revoke_permission(role_id, "read")
    
    assert result.success == True, "Revoke başarılı olmalı"
    
    print(f"  Permission revoked: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Revoke permission")
    print("=" * 70)


def test_set_parent_role():
    """
    Test: Set parent role.
    """
    print("=" * 70)
    print("TEST: Set Parent Role")
    print("=" * 70)
    
    config = RoleManagementConfig(enable_default_roles=False)
    manager = RoleManager(config)
    
    parent_result = manager.create_role("Admin", "Admin role")
    child_result = manager.create_role("Editor", "Editor role")
    
    result = manager.set_parent_role(child_result.role.role_id, parent_result.role.role_id)
    
    assert result.success == True, "Set başarılı olmalı"
    
    print(f"  Parent role set: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set parent role")
    print("=" * 70)


def test_remove_parent_role():
    """
    Test: Remove parent role.
    """
    print("=" * 70)
    print("TEST: Remove Parent Role")
    print("=" * 70)
    
    config = RoleManagementConfig(enable_default_roles=False)
    manager = RoleManager(config)
    
    parent_result = manager.create_role("Admin", "Admin role")
    child_result = manager.create_role("Editor", "Editor role")
    
    manager.set_parent_role(child_result.role.role_id, parent_result.role.role_id)
    result = manager.remove_parent_role(child_result.role.role_id)
    
    assert result.success == True, "Remove başarılı olmalı"
    
    print(f"  Parent role removed: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Remove parent role")
    print("=" * 70)


def test_get_inherited_permissions():
    """
    Test: Get inherited permissions.
    """
    print("=" * 70)
    print("TEST: Get Inherited Permissions")
    print("=" * 70)
    
    config = RoleManagementConfig(enable_default_roles=False)
    manager = RoleManager(config)
    
    parent_result = manager.create_role("Admin", "Admin role")
    child_result = manager.create_role("Editor", "Editor role")
    
    manager.assign_permission(parent_result.role.role_id, "read")
    manager.set_parent_role(child_result.role.role_id, parent_result.role.role_id)
    
    permissions = manager.get_inherited_permissions(child_result.role.role_id)
    
    assert "read" in permissions, "Inherited permission olmalı"
    
    print(f"  Inherited permissions: {len(permissions)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get inherited permissions")
    print("=" * 70)


def test_get_all_permissions():
    """
    Test: Get all permissions.
    """
    print("=" * 70)
    print("TEST: Get All Permissions")
    print("=" * 70)
    
    config = RoleManagementConfig(enable_default_roles=False)
    manager = RoleManager(config)
    
    result = manager.create_role("Editor", "Editor role")
    role_id = result.role.role_id
    
    manager.assign_permission(role_id, "read")
    manager.assign_permission(role_id, "write")
    
    permissions = manager.get_all_permissions(role_id)
    
    assert len(permissions) == 2, "2 permission olmalı"
    
    print(f"  All permissions: {len(permissions)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get all permissions")
    print("=" * 70)


def test_get_role_hierarchy():
    """
    Test: Get role hierarchy.
    """
    print("=" * 70)
    print("TEST: Get Role Hierarchy")
    print("=" * 70)
    
    config = RoleManagementConfig(enable_default_roles=False)
    manager = RoleManager(config)
    
    parent_result = manager.create_role("Admin", "Admin role")
    child_result = manager.create_role("Editor", "Editor role")
    
    manager.set_parent_role(child_result.role.role_id, parent_result.role.role_id)
    
    hierarchy = manager.get_role_hierarchy(child_result.role.role_id)
    
    assert len(hierarchy) > 0, "Hierarchy olmalı"
    
    print(f"  Hierarchy depth: {len(hierarchy)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get role hierarchy")
    print("=" * 70)


def test_get_child_roles():
    """
    Test: Get child roles.
    """
    print("=" * 70)
    print("TEST: Get Child Roles")
    print("=" * 70)
    
    config = RoleManagementConfig(enable_default_roles=False)
    manager = RoleManager(config)
    
    parent_result = manager.create_role("Admin", "Admin role")
    child_result = manager.create_role("Editor", "Editor role")
    
    manager.set_parent_role(child_result.role.role_id, parent_result.role.role_id)
    
    children = manager.get_child_roles(parent_result.role.role_id)
    
    assert len(children) > 0, "Child roles olmalı"
    
    print(f"  Child roles: {len(children)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get child roles")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    config = RoleManagementConfig(enable_default_roles=False)
    manager = RoleManager(config)
    
    new_config = RoleManagementConfig(max_roles=50)
    result = manager.update_config(new_config)
    
    assert result.success == True, "Update başarılı olmalı"
    assert manager.config.max_roles == 50, "Config güncellenmeli"
    
    print(f"  Max roles: {manager.config.max_roles}")
    
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
    
    config = RoleManagementConfig(max_roles=50)
    manager = RoleManager(config)
    
    retrieved_config = manager.get_config()
    
    assert retrieved_config.max_roles == 50, "Config eşleşmeli"
    
    print(f"  Max roles: {retrieved_config.max_roles}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_role_type_enum()
        test2 = test_role_scope_enum()
        test3 = test_role_permission_dataclass()
        test4 = test_role_dataclass()
        test5 = test_role_hierarchy_dataclass()
        test6 = test_role_management_config_dataclass()
        test7 = test_role_management_result_dataclass()
        test8 = test_role_manager_initialization()
        test9 = test_create_role()
        test10 = test_delete_role()
        test11 = test_update_role()
        test12 = test_get_role()
        test13 = test_get_role_by_name()
        test14 = test_get_all_roles()
        test15 = test_assign_permission()
        test16 = test_revoke_permission()
        test17 = test_set_parent_role()
        test18 = test_remove_parent_role()
        test19 = test_get_inherited_permissions()
        test20 = test_get_all_permissions()
        test21 = test_get_role_hierarchy()
        test22 = test_get_child_roles()
        test23 = test_update_config()
        test24 = test_get_config()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"RoleType Enum: {'PASS' if test1 else 'FAIL'}")
        print(f"RoleScope Enum: {'PASS' if test2 else 'FAIL'}")
        print(f"RolePermission Dataclass: {'PASS' if test3 else 'FAIL'}")
        print(f"Role Dataclass: {'PASS' if test4 else 'FAIL'}")
        print(f"RoleHierarchy Dataclass: {'PASS' if test5 else 'FAIL'}")
        print(f"RoleManagementConfig Dataclass: {'PASS' if test6 else 'FAIL'}")
        print(f"RoleManagementResult Dataclass: {'PASS' if test7 else 'FAIL'}")
        print(f"RoleManager Initialization: {'PASS' if test8 else 'FAIL'}")
        print(f"Create Role: {'PASS' if test9 else 'FAIL'}")
        print(f"Delete Role: {'PASS' if test10 else 'FAIL'}")
        print(f"Update Role: {'PASS' if test11 else 'FAIL'}")
        print(f"Get Role: {'PASS' if test12 else 'FAIL'}")
        print(f"Get Role by Name: {'PASS' if test13 else 'FAIL'}")
        print(f"Get All Roles: {'PASS' if test14 else 'FAIL'}")
        print(f"Assign Permission: {'PASS' if test15 else 'FAIL'}")
        print(f"Revoke Permission: {'PASS' if test16 else 'FAIL'}")
        print(f"Set Parent Role: {'PASS' if test17 else 'FAIL'}")
        print(f"Remove Parent Role: {'PASS' if test18 else 'FAIL'}")
        print(f"Get Inherited Permissions: {'PASS' if test19 else 'FAIL'}")
        print(f"Get All Permissions: {'PASS' if test20 else 'FAIL'}")
        print(f"Get Role Hierarchy: {'PASS' if test21 else 'FAIL'}")
        print(f"Get Child Roles: {'PASS' if test22 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test23 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test24 else 'FAIL'}")
        
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
