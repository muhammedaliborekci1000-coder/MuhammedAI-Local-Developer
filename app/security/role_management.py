"""
MuhammedAI Local Developer - Role Management
Role management system for security.
"""

from typing import Dict, Any, Optional, List, Set
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime


class RoleType(Enum):
    """Role type."""
    SYSTEM = "system"
    CUSTOM = "custom"
    DEFAULT = "default"
    TEMPORARY = "temporary"


class RoleScope(Enum):
    """Role scope."""
    GLOBAL = "global"
    PROJECT = "project"
    ORGANIZATION = "organization"
    TEAM = "team"
    CUSTOM = "custom"


@dataclass
class RolePermission:
    """Role permission."""
    permission_id: str
    name: str
    description: str
    resource_type: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Role:
    """Role."""
    role_id: str
    name: str
    description: str
    role_type: RoleType = RoleType.CUSTOM
    scope: RoleScope = RoleScope.GLOBAL
    permissions: Set[str] = field(default_factory=set)
    parent_role_id: Optional[str] = None
    is_active: bool = True
    is_default: bool = False
    priority: int = 0
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RoleHierarchy:
    """Role hierarchy."""
    parent_role_id: str
    child_role_id: str
    inheritance_type: str = "full"  # full, partial, custom
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class RoleManagementConfig:
    """Role management configuration."""
    enable_role_creation: bool = True
    enable_role_deletion: bool = True
    enable_role_update: bool = True
    enable_inheritance: bool = True
    max_roles: int = 100
    max_hierarchy_depth: int = 5
    enable_default_roles: bool = True
    enable_system_roles: bool = True


@dataclass
class RoleManagementResult:
    """Role management result."""
    success: bool
    message: Optional[str] = None
    role: Optional[Role] = None
    roles: List[Role] = field(default_factory=list)
    hierarchy: Optional[RoleHierarchy] = None
    hierarchies: List[RoleHierarchy] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)


class RoleManager:
    """
    Role manager.
    
    Özellikler:
    - Role creation
    - Role deletion
    - Role update
    - Role listing
    - Permission assignment
    - Role inheritance
    - Role hierarchy
    - Default roles
    """
    
    def __init__(self, config: Optional[RoleManagementConfig] = None):
        """
        Initialize role manager.
        
        Args:
            config: Role management configuration
        """
        self.config = config or RoleManagementConfig()
        self.roles: Dict[str, Role] = {}
        self.hierarchies: List[RoleHierarchy] = []
        self.role_id_counter = 0
        self._next_role_id()
        
        # Create default roles if enabled
        if self.config.enable_default_roles:
            self._create_default_roles()
    
    def _next_role_id(self) -> str:
        """
        Generate next role ID.
        
        Returns:
            str: Role ID
        """
        self.role_id_counter += 1
        return f"role_{self.role_id_counter}"
    
    def _create_default_roles(self):
        """Create default roles."""
        # Admin role
        admin_role = Role(
            role_id="role_admin",
            name="Admin",
            description="Administrator role with full access",
            role_type=RoleType.DEFAULT,
            scope=RoleScope.GLOBAL,
            is_default=True,
            priority=100
        )
        self.roles[admin_role.role_id] = admin_role
        
        # User role
        user_role = Role(
            role_id="role_user",
            name="User",
            description="Standard user role",
            role_type=RoleType.DEFAULT,
            scope=RoleScope.GLOBAL,
            is_default=True,
            priority=10
        )
        self.roles[user_role.role_id] = user_role
        
        # Guest role
        guest_role = Role(
            role_id="role_guest",
            name="Guest",
            description="Guest role with limited access",
            role_type=RoleType.DEFAULT,
            scope=RoleScope.GLOBAL,
            is_default=True,
            priority=1
        )
        self.roles[guest_role.role_id] = guest_role
    
    def create_role(self, name: str, description: str, role_type: Optional[RoleType] = None, scope: Optional[RoleScope] = None) -> RoleManagementResult:
        """
        Create a new role.
        
        Args:
            name: Role name
            description: Role description
            role_type: Role type
            scope: Role scope
            
        Returns:
            RoleManagementResult: Create result
        """
        result = RoleManagementResult(success=False)
        
        try:
            if not self.config.enable_role_creation:
                result.errors.append("Role creation is disabled")
                return result
            
            if len(self.roles) >= self.config.max_roles:
                result.errors.append(f"Maximum roles reached (max {self.config.max_roles})")
                return result
            
            # Check if name exists
            if any(r.name == name for r in self.roles.values()):
                result.errors.append("Role name already exists")
                return result
            
            role = Role(
                role_id=self._next_role_id(),
                name=name,
                description=description,
                role_type=role_type or RoleType.CUSTOM,
                scope=scope or RoleScope.GLOBAL
            )
            
            self.roles[role.role_id] = role
            
            result.success = True
            result.role = role
            result.roles = self.get_all_roles()
            result.message = f"Role '{name}' created successfully"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def delete_role(self, role_id: str) -> RoleManagementResult:
        """
        Delete a role.
        
        Args:
            role_id: Role ID
            
        Returns:
            RoleManagementResult: Delete result
        """
        result = RoleManagementResult(success=False)
        
        try:
            if not self.config.enable_role_deletion:
                result.errors.append("Role deletion is disabled")
                return result
            
            role = self.roles.get(role_id)
            if not role:
                result.errors.append("Role not found")
                return result
            
            # Prevent deletion of default roles
            if role.is_default and not self.config.enable_system_roles:
                result.errors.append("Cannot delete default role")
                return result
            
            # Remove hierarchies
            self.hierarchies = [h for h in self.hierarchies if h.parent_role_id != role_id and h.child_role_id != role_id]
            
            # Update child roles to remove parent reference
            for r in self.roles.values():
                if r.parent_role_id == role_id:
                    r.parent_role_id = None
            
            del self.roles[role_id]
            
            result.success = True
            result.roles = self.get_all_roles()
            result.message = f"Role '{role_id}' deleted successfully"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def update_role(self, role_id: str, **kwargs) -> RoleManagementResult:
        """
        Update role information.
        
        Args:
            role_id: Role ID
            **kwargs: Fields to update
            
        Returns:
            RoleManagementResult: Update result
        """
        result = RoleManagementResult(success=False)
        
        try:
            if not self.config.enable_role_update:
                result.errors.append("Role update is disabled")
                return result
            
            role = self.roles.get(role_id)
            if not role:
                result.errors.append("Role not found")
                return result
            
            # Update fields
            for key, value in kwargs.items():
                if hasattr(role, key):
                    setattr(role, key, value)
            
            role.updated_at = datetime.now()
            
            result.success = True
            result.role = role
            result.message = f"Role '{role_id}' updated successfully"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_role(self, role_id: str) -> Optional[Role]:
        """
        Get role by ID.
        
        Args:
            role_id: Role ID
            
        Returns:
            Optional[Role]: Role
        """
        return self.roles.get(role_id)
    
    def get_role_by_name(self, name: str) -> Optional[Role]:
        """
        Get role by name.
        
        Args:
            name: Role name
            
        Returns:
            Optional[Role]: Role
        """
        for role in self.roles.values():
            if role.name == name:
                return role
        return None
    
    def get_all_roles(self) -> List[Role]:
        """
        Get all roles.
        
        Returns:
            List[Role]: All roles
        """
        return list(self.roles.values())
    
    def assign_permission(self, role_id: str, permission_id: str) -> RoleManagementResult:
        """
        Assign permission to role.
        
        Args:
            role_id: Role ID
            permission_id: Permission ID
            
        Returns:
            RoleManagementResult: Assign result
        """
        result = RoleManagementResult(success=False)
        
        try:
            role = self.roles.get(role_id)
            if not role:
                result.errors.append("Role not found")
                return result
            
            role.permissions.add(permission_id)
            role.updated_at = datetime.now()
            
            result.success = True
            result.role = role
            result.message = f"Permission '{permission_id}' assigned to role '{role_id}'"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def revoke_permission(self, role_id: str, permission_id: str) -> RoleManagementResult:
        """
        Revoke permission from role.
        
        Args:
            role_id: Role ID
            permission_id: Permission ID
            
        Returns:
            RoleManagementResult: Revoke result
        """
        result = RoleManagementResult(success=False)
        
        try:
            role = self.roles.get(role_id)
            if not role:
                result.errors.append("Role not found")
                return result
            
            role.permissions.discard(permission_id)
            role.updated_at = datetime.now()
            
            result.success = True
            result.role = role
            result.message = f"Permission '{permission_id}' revoked from role '{role_id}'"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def set_parent_role(self, child_role_id: str, parent_role_id: str, inheritance_type: str = "full") -> RoleManagementResult:
        """
        Set parent role for inheritance.
        
        Args:
            child_role_id: Child role ID
            parent_role_id: Parent role ID
            inheritance_type: Inheritance type
            
        Returns:
            RoleManagementResult: Set result
        """
        result = RoleManagementResult(success=False)
        
        try:
            if not self.config.enable_inheritance:
                result.errors.append("Role inheritance is disabled")
                return result
            
            child_role = self.roles.get(child_role_id)
            parent_role = self.roles.get(parent_role_id)
            
            if not child_role:
                result.errors.append("Child role not found")
                return result
            
            if not parent_role:
                result.errors.append("Parent role not found")
                return result
            
            # Check hierarchy depth
            depth = self._get_hierarchy_depth(parent_role_id)
            if depth >= self.config.max_hierarchy_depth:
                result.errors.append(f"Maximum hierarchy depth reached (max {self.config.max_hierarchy_depth})")
                return result
            
            # Check for circular dependency
            if self._would_create_circular_dependency(child_role_id, parent_role_id):
                result.errors.append("Circular dependency detected")
                return result
            
            child_role.parent_role_id = parent_role_id
            child_role.updated_at = datetime.now()
            
            # Create hierarchy record
            hierarchy = RoleHierarchy(
                parent_role_id=parent_role_id,
                child_role_id=child_role_id,
                inheritance_type=inheritance_type
            )
            self.hierarchies.append(hierarchy)
            
            result.success = True
            result.role = child_role
            result.hierarchy = hierarchy
            result.message = f"Parent role set for '{child_role_id}'"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def remove_parent_role(self, child_role_id: str) -> RoleManagementResult:
        """
        Remove parent role.
        
        Args:
            child_role_id: Child role ID
            
        Returns:
            RoleManagementResult: Remove result
        """
        result = RoleManagementResult(success=False)
        
        try:
            child_role = self.roles.get(child_role_id)
            if not child_role:
                result.errors.append("Child role not found")
                return result
            
            child_role.parent_role_id = None
            child_role.updated_at = datetime.now()
            
            # Remove hierarchy record
            self.hierarchies = [h for h in self.hierarchies if h.child_role_id != child_role_id]
            
            result.success = True
            result.role = child_role
            result.message = f"Parent role removed from '{child_role_id}'"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_inherited_permissions(self, role_id: str) -> Set[str]:
        """
        Get inherited permissions from parent roles.
        
        Args:
            role_id: Role ID
            
        Returns:
            Set[str]: Inherited permissions
        """
        if not self.config.enable_inheritance:
            return set()
        
        permissions = set()
        role = self.roles.get(role_id)
        
        if not role:
            return permissions
        
        if role.parent_role_id:
            parent_permissions = self.get_inherited_permissions(role.parent_role_id)
            permissions.update(parent_permissions)
            parent_role = self.roles.get(role.parent_role_id)
            if parent_role:
                permissions.update(parent_role.permissions)
        
        return permissions
    
    def get_all_permissions(self, role_id: str) -> Set[str]:
        """
        Get all permissions for a role (direct + inherited).
        
        Args:
            role_id: Role ID
            
        Returns:
            Set[str]: All permissions
        """
        role = self.roles.get(role_id)
        if not role:
            return set()
        
        direct_permissions = role.permissions.copy()
        inherited_permissions = self.get_inherited_permissions(role_id)
        
        return direct_permissions.union(inherited_permissions)
    
    def _get_hierarchy_depth(self, role_id: str) -> int:
        """
        Get hierarchy depth for a role.
        
        Args:
            role_id: Role ID
            
        Returns:
            int: Depth
        """
        depth = 0
        role = self.roles.get(role_id)
        
        while role and role.parent_role_id:
            depth += 1
            role = self.roles.get(role.parent_role_id)
        
        return depth
    
    def _would_create_circular_dependency(self, child_role_id: str, parent_role_id: str) -> bool:
        """
        Check if setting parent would create circular dependency.
        
        Args:
            child_role_id: Child role ID
            parent_role_id: Parent role ID
            
        Returns:
            bool: Would create circular dependency
        """
        if child_role_id == parent_role_id:
            return True
        
        # Check if parent is already a descendant of child
        current = parent_role_id
        visited = set()
        
        while current and current not in visited:
            visited.add(current)
            if current == child_role_id:
                return True
            
            role = self.roles.get(current)
            current = role.parent_role_id if role else None
        
        return False
    
    def get_role_hierarchy(self, role_id: str) -> List[Role]:
        """
        Get role hierarchy (ancestors).
        
        Args:
            role_id: Role ID
            
        Returns:
            List[Role]: Ancestor roles
        """
        hierarchy = []
        role = self.roles.get(role_id)
        
        while role and role.parent_role_id:
            parent_role = self.roles.get(role.parent_role_id)
            if parent_role:
                hierarchy.append(parent_role)
                role = parent_role
            else:
                break
        
        return hierarchy
    
    def get_child_roles(self, role_id: str) -> List[Role]:
        """
        Get child roles.
        
        Args:
            role_id: Role ID
            
        Returns:
            List[Role]: Child roles
        """
        return [r for r in self.roles.values() if r.parent_role_id == role_id]
    
    def update_config(self, config: RoleManagementConfig) -> RoleManagementResult:
        """
        Update role management configuration.
        
        Args:
            config: New configuration
            
        Returns:
            RoleManagementResult: Update result
        """
        result = RoleManagementResult(success=True)
        
        try:
            self.config = config
            result.message = "Config updated"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def get_config(self) -> RoleManagementConfig:
        """
        Get role management configuration.
        
        Returns:
            RoleManagementConfig: Configuration
        """
        return self.config


if __name__ == "__main__":
    # Basit test
    config = RoleManagementConfig()
    manager = RoleManager(config)
    
    # Role oluştur
    result = manager.create_role("Editor", "Editor role")
    
    print(f"Role created: {result.message}")
    
    # Permission ata
    manager.assign_permission(result.role.role_id, "read")
    
    # Tüm rolleri al
    roles = manager.get_all_roles()
    
    print(f"Total roles: {len(roles)}")
