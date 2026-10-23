"""
MuhammedAI Local Developer - Authorization
Authorization system for security.
"""

from typing import Dict, Any, Optional, List, Set
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime


class Permission(Enum):
    """Permission types."""
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    EXECUTE = "execute"
    ADMIN = "admin"
    MANAGE = "manage"
    VIEW = "view"
    EDIT = "edit"
    CREATE = "create"
    UPDATE = "update"
    CUSTOM = "custom"


class ResourceType(Enum):
    """Resource types."""
    FILE = "file"
    DIRECTORY = "directory"
    PROJECT = "project"
    SETTINGS = "settings"
    USER = "user"
    ROLE = "role"
    API = "api"
    DATABASE = "database"
    SYSTEM = "system"
    CUSTOM = "custom"


class AccessDecision(Enum):
    """Access decision."""
    ALLOW = "allow"
    DENY = "deny"
    ABSTAIN = "abstain"


@dataclass
class Role:
    """Role."""
    id: str
    name: str
    description: str
    permissions: Set[Permission] = field(default_factory=set)
    resource_types: Set[ResourceType] = field(default_factory=set)
    is_active: bool = True
    is_default: bool = False
    parent_role_id: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Policy:
    """Access policy."""
    id: str
    name: str
    description: str
    effect: AccessDecision
    permissions: Set[Permission] = field(default_factory=set)
    resource_types: Set[ResourceType] = field(default_factory=set)
    resource_ids: Set[str] = field(default_factory=set)
    role_ids: Set[str] = field(default_factory=set)
    user_ids: Set[str] = field(default_factory=set)
    conditions: Dict[str, Any] = field(default_factory=dict)
    is_active: bool = True
    priority: int = 0
    created_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AccessRequest:
    """Access request."""
    user_id: str
    permission: Permission
    resource_type: ResourceType
    resource_id: Optional[str] = None
    context: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AccessResult:
    """Access result."""
    decision: AccessDecision
    allowed: bool
    reason: Optional[str] = None
    policy_id: Optional[str] = None
    errors: List[str] = field(default_factory=list)


@dataclass
class AuthorizationConfig:
    """Authorization configuration."""
    default_deny: bool = True
    enable_policy_caching: bool = True
    enable_role_inheritance: bool = True
    enable_audit_logging: bool = True
    max_policy_priority: int = 1000
    enable_conditional_policies: bool = True


class AuthorizationManager:
    """
    Authorization manager.
    
    Özellikler:
    - Permission checking
    - Role-based access control
    - Resource-based access control
    - Policy evaluation
    - Access denial
    - Audit logging
    - Role inheritance
    - Policy priority
    - Conditional policies
    """
    
    def __init__(self, config: Optional[AuthorizationConfig] = None):
        """
        Initialize authorization manager.
        
        Args:
            config: Authorization configuration
        """
        self.config = config or AuthorizationConfig()
        self.roles: Dict[str, Role] = {}
        self.policies: Dict[str, Policy] = {}
        self.user_roles: Dict[str, Set[str]] = {}
        self.role_id_counter = 0
        self.policy_id_counter = 0
        self._next_role_id()
        self._next_policy_id()
    
    def _next_role_id(self) -> str:
        """
        Generate next role ID.
        
        Returns:
            str: Role ID
        """
        self.role_id_counter += 1
        return f"role_{self.role_id_counter}"
    
    def _next_policy_id(self) -> str:
        """
        Generate next policy ID.
        
        Returns:
            str: Policy ID
        """
        self.policy_id_counter += 1
        return f"policy_{self.policy_id_counter}"
    
    def add_role(self, role: Role) -> bool:
        """
        Add a role.
        
        Args:
            role: Role to add
            
        Returns:
            bool: Success
        """
        if not role.id:
            role.id = self._next_role_id()
        
        self.roles[role.id] = role
        return True
    
    def remove_role(self, role_id: str) -> bool:
        """
        Remove a role.
        
        Args:
            role_id: Role ID
            
        Returns:
            bool: Success
        """
        if role_id in self.roles:
            del self.roles[role_id]
            # Remove from user roles
            for user_id, role_ids in self.user_roles.items():
                role_ids.discard(role_id)
            return True
        return False
    
    def get_role(self, role_id: str) -> Optional[Role]:
        """
        Get role by ID.
        
        Args:
            role_id: Role ID
            
        Returns:
            Optional[Role]: Role
        """
        return self.roles.get(role_id)
    
    def get_all_roles(self) -> List[Role]:
        """
        Get all roles.
        
        Returns:
            List[Role]: All roles
        """
        return list(self.roles.values())
    
    def assign_role_to_user(self, user_id: str, role_id: str) -> bool:
        """
        Assign role to user.
        
        Args:
            user_id: User ID
            role_id: Role ID
            
        Returns:
            bool: Success
        """
        if role_id not in self.roles:
            return False
        
        if user_id not in self.user_roles:
            self.user_roles[user_id] = set()
        
        self.user_roles[user_id].add(role_id)
        return True
    
    def remove_role_from_user(self, user_id: str, role_id: str) -> bool:
        """
        Remove role from user.
        
        Args:
            user_id: User ID
            role_id: Role ID
            
        Returns:
            bool: Success
        """
        if user_id in self.user_roles:
            self.user_roles[user_id].discard(role_id)
            if not self.user_roles[user_id]:
                del self.user_roles[user_id]
            return True
        return False
    
    def get_user_roles(self, user_id: str) -> Set[str]:
        """
        Get user roles.
        
        Args:
            user_id: User ID
            
        Returns:
            Set[str]: Role IDs
        """
        return self.user_roles.get(user_id, set())
    
    def add_policy(self, policy: Policy) -> bool:
        """
        Add a policy.
        
        Args:
            policy: Policy to add
            
        Returns:
            bool: Success
        """
        if not policy.id:
            policy.id = self._next_policy_id()
        
        self.policies[policy.id] = policy
        return True
    
    def remove_policy(self, policy_id: str) -> bool:
        """
        Remove a policy.
        
        Args:
            policy_id: Policy ID
            
        Returns:
            bool: Success
        """
        if policy_id in self.policies:
            del self.policies[policy_id]
            return True
        return False
    
    def get_policy(self, policy_id: str) -> Optional[Policy]:
        """
        Get policy by ID.
        
        Args:
            policy_id: Policy ID
            
        Returns:
            Optional[Policy]: Policy
        """
        return self.policies.get(policy_id)
    
    def get_all_policies(self) -> List[Policy]:
        """
        Get all policies.
        
        Returns:
            List[Policy]: All policies
        """
        return list(self.policies.values())
    
    def _get_inherited_permissions(self, role_id: str) -> Set[Permission]:
        """
        Get inherited permissions from parent role.
        
        Args:
            role_id: Role ID
            
        Returns:
            Set[Permission]: Inherited permissions
        """
        if not self.config.enable_role_inheritance:
            return set()
        
        permissions = set()
        role = self.roles.get(role_id)
        
        if role and role.parent_role_id:
            parent_permissions = self._get_inherited_permissions(role.parent_role_id)
            permissions.update(parent_permissions)
            parent_role = self.roles.get(role.parent_role_id)
            if parent_role:
                permissions.update(parent_role.permissions)
        
        return permissions
    
    def _get_user_permissions(self, user_id: str) -> Set[Permission]:
        """
        Get all permissions for a user.
        
        Args:
            user_id: User ID
            
        Returns:
            Set[Permission]: Permissions
        """
        permissions = set()
        role_ids = self.get_user_roles(user_id)
        
        for role_id in role_ids:
            role = self.roles.get(role_id)
            if role and role.is_active:
                permissions.update(role.permissions)
                # Add inherited permissions
                inherited = self._get_inherited_permissions(role_id)
                permissions.update(inherited)
        
        return permissions
    
    def check_permission(self, user_id: str, permission: Permission) -> bool:
        """
        Check if user has permission.
        
        Args:
            user_id: User ID
            permission: Permission
            
        Returns:
            bool: Has permission
        """
        permissions = self._get_user_permissions(user_id)
        return permission in permissions
    
    def check_access(self, request: AccessRequest) -> AccessResult:
        """
        Check access using policies.
        
        Args:
            request: Access request
            
        Returns:
            AccessResult: Access result
        """
        result = AccessResult(decision=AccessDecision.DENY, allowed=False)
        
        try:
            # Sort policies by priority (higher priority first)
            sorted_policies = sorted(
                self.policies.values(),
                key=lambda p: p.priority,
                reverse=True
            )
            
            for policy in sorted_policies:
                if not policy.is_active:
                    continue
                
                # Check if policy applies to user
                if policy.user_ids and request.user_id not in policy.user_ids:
                    continue
                
                # Check if policy applies to user roles
                if policy.role_ids:
                    user_role_ids = self.get_user_roles(request.user_id)
                    if not user_role_ids.intersection(policy.role_ids):
                        continue
                
                # Check if policy applies to resource type
                if policy.resource_types and request.resource_type not in policy.resource_types:
                    continue
                
                # Check if policy applies to specific resource
                if policy.resource_ids and request.resource_id not in policy.resource_ids:
                    continue
                
                # Check if policy applies to permission
                if policy.permissions and request.permission not in policy.permissions:
                    continue
                
                # Check conditions
                if self.config.enable_conditional_policies and policy.conditions:
                    if not self._evaluate_conditions(policy.conditions, request.context):
                        continue
                
                # Policy applies
                result.decision = policy.effect
                result.allowed = (policy.effect == AccessDecision.ALLOW)
                result.policy_id = policy.id
                result.reason = f"Policy '{policy.name}' evaluated"
                
                # If explicit deny, stop
                if policy.effect == AccessDecision.DENY:
                    break
            
            # Default deny if no policy matched
            if result.decision == AccessDecision.ABSTAIN:
                result.decision = AccessDecision.DENY if self.config.default_deny else AccessDecision.ALLOW
                result.allowed = (result.decision == AccessDecision.ALLOW)
                result.reason = "Default policy"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def _evaluate_conditions(self, conditions: Dict[str, Any], context: Dict[str, Any]) -> bool:
        """
        Evaluate policy conditions.
        
        Args:
            conditions: Conditions
            context: Request context
            
        Returns:
            bool: Conditions met
        """
        for key, value in conditions.items():
            if key not in context:
                return False
            if context[key] != value:
                return False
        return True
    
    def grant_permission(self, role_id: str, permission: Permission) -> bool:
        """
        Grant permission to role.
        
        Args:
            role_id: Role ID
            permission: Permission
            
        Returns:
            bool: Success
        """
        role = self.roles.get(role_id)
        if role:
            role.permissions.add(permission)
            return True
        return False
    
    def revoke_permission(self, role_id: str, permission: Permission) -> bool:
        """
        Revoke permission from role.
        
        Args:
            role_id: Role ID
            permission: Permission
            
        Returns:
            bool: Success
        """
        role = self.roles.get(role_id)
        if role:
            role.permissions.discard(permission)
            return True
        return False
    
    def update_config(self, config: AuthorizationConfig) -> bool:
        """
        Update authorization configuration.
        
        Args:
            config: New configuration
            
        Returns:
            bool: Success
        """
        self.config = config
        return True
    
    def get_config(self) -> AuthorizationConfig:
        """
        Get authorization configuration.
        
        Returns:
            AuthorizationConfig: Configuration
        """
        return self.config


if __name__ == "__main__":
    # Basit test
    config = AuthorizationConfig()
    manager = AuthorizationManager(config)
    
    # Role oluştur
    role = Role(
        id="",
        name="Admin",
        description="Administrator role",
        permissions={Permission.READ, Permission.WRITE, Permission.DELETE, Permission.ADMIN}
    )
    
    manager.add_role(role)
    
    # User'a role ata
    manager.assign_role_to_user("user_1", role.id)
    
    # Permission kontrolü
    has_permission = manager.check_permission("user_1", Permission.READ)
    
    print(f"Has READ permission: {has_permission}")
