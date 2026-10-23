"""
MuhammedAI Local Developer - User Management
User management system for security.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta


class UserStatus(Enum):
    """User status."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    DELETED = "deleted"
    PENDING = "pending"


class UserTier(Enum):
    """User tier."""
    FREE = "free"
    BASIC = "basic"
    PRO = "pro"
    ENTERPRISE = "enterprise"
    CUSTOM = "custom"


@dataclass
class UserProfile:
    """User profile."""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    display_name: Optional[str] = None
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    website: Optional[str] = None
    timezone: Optional[str] = None
    language: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class UserPreferences:
    """User preferences."""
    theme: str = "dark"
    notifications_enabled: bool = True
    email_notifications: bool = True
    language: str = "en"
    timezone: str = "UTC"
    font_size: int = 14
    editor_font: str = "monospace"
    auto_save: bool = True
    tab_size: int = 4
    show_line_numbers: bool = True
    word_wrap: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class UserActivity:
    """User activity."""
    activity_id: str
    user_id: str
    action: str
    resource_type: Optional[str] = None
    resource_id: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class User:
    """User."""
    user_id: str
    username: str
    email: str
    status: UserStatus = UserStatus.ACTIVE
    tier: UserTier = UserTier.FREE
    profile: UserProfile = field(default_factory=UserProfile)
    preferences: UserPreferences = field(default_factory=UserPreferences)
    is_verified: bool = False
    is_admin: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    last_login: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class UserManagementConfig:
    """User management configuration."""
    enable_user_creation: bool = True
    enable_user_deletion: bool = True
    enable_user_update: bool = True
    enable_user_search: bool = True
    enable_activity_tracking: bool = True
    max_users: int = 1000
    default_tier: UserTier = UserTier.FREE
    require_verification: bool = False
    activity_retention_days: int = 30


@dataclass
class UserManagementResult:
    """User management result."""
    success: bool
    message: Optional[str] = None
    user: Optional[User] = None
    users: List[User] = field(default_factory=list)
    activity: Optional[UserActivity] = None
    activities: List[UserActivity] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)


class UserManager:
    """
    User manager.
    
    Özellikler:
    - User creation
    - User deletion
    - User update
    - User listing
    - User search
    - User profile management
    - User preferences
    - User activity tracking
    """
    
    def __init__(self, config: Optional[UserManagementConfig] = None):
        """
        Initialize user manager.
        
        Args:
            config: User management configuration
        """
        self.config = config or UserManagementConfig()
        self.users: Dict[str, User] = {}
        self.activities: List[UserActivity] = []
        self.user_id_counter = 0
        self.activity_id_counter = 0
        self._next_user_id()
        self._next_activity_id()
    
    def _next_user_id(self) -> str:
        """
        Generate next user ID.
        
        Returns:
            str: User ID
        """
        self.user_id_counter += 1
        return f"user_{self.user_id_counter}"
    
    def _next_activity_id(self) -> str:
        """
        Generate next activity ID.
        
        Returns:
            str: Activity ID
        """
        self.activity_id_counter += 1
        return f"activity_{self.activity_id_counter}"
    
    def create_user(self, username: str, email: str, tier: Optional[UserTier] = None) -> UserManagementResult:
        """
        Create a new user.
        
        Args:
            username: Username
            email: Email address
            tier: User tier
            
        Returns:
            UserManagementResult: Create result
        """
        result = UserManagementResult(success=False)
        
        try:
            if not self.config.enable_user_creation:
                result.errors.append("User creation is disabled")
                return result
            
            if len(self.users) >= self.config.max_users:
                result.errors.append(f"Maximum users reached (max {self.config.max_users})")
                return result
            
            # Check if username exists
            if any(u.username == username for u in self.users.values()):
                result.errors.append("Username already exists")
                return result
            
            # Check if email exists
            if any(u.email == email for u in self.users.values()):
                result.errors.append("Email already exists")
                return result
            
            user = User(
                user_id=self._next_user_id(),
                username=username,
                email=email,
                tier=tier or self.config.default_tier,
                is_verified=not self.config.require_verification
            )
            
            self.users[user.user_id] = user
            
            # Track activity
            if self.config.enable_activity_tracking:
                self._track_activity(user.user_id, "user_created")
            
            result.success = True
            result.user = user
            result.users = self.get_all_users()
            result.message = f"User '{username}' created successfully"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def delete_user(self, user_id: str) -> UserManagementResult:
        """
        Delete a user.
        
        Args:
            user_id: User ID
            
        Returns:
            UserManagementResult: Delete result
        """
        result = UserManagementResult(success=False)
        
        try:
            if not self.config.enable_user_deletion:
                result.errors.append("User deletion is disabled")
                return result
            
            if user_id in self.users:
                user = self.users[user_id]
                user.status = UserStatus.DELETED
                del self.users[user_id]
                
                # Track activity
                if self.config.enable_activity_tracking:
                    self._track_activity(user_id, "user_deleted")
                
                result.success = True
                result.users = self.get_all_users()
                result.message = f"User '{user_id}' deleted successfully"
            else:
                result.errors.append("User not found")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def update_user(self, user_id: str, **kwargs) -> UserManagementResult:
        """
        Update user information.
        
        Args:
            user_id: User ID
            **kwargs: Fields to update
            
        Returns:
            UserManagementResult: Update result
        """
        result = UserManagementResult(success=False)
        
        try:
            if not self.config.enable_user_update:
                result.errors.append("User update is disabled")
                return result
            
            user = self.users.get(user_id)
            if not user:
                result.errors.append("User not found")
                return result
            
            # Update fields
            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)
            
            user.updated_at = datetime.now()
            
            # Track activity
            if self.config.enable_activity_tracking:
                self._track_activity(user_id, "user_updated")
            
            result.success = True
            result.user = user
            result.message = f"User '{user_id}' updated successfully"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_user(self, user_id: str) -> Optional[User]:
        """
        Get user by ID.
        
        Args:
            user_id: User ID
            
        Returns:
            Optional[User]: User
        """
        return self.users.get(user_id)
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """
        Get user by username.
        
        Args:
            username: Username
            
        Returns:
            Optional[User]: User
        """
        for user in self.users.values():
            if user.username == username:
                return user
        return None
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Get user by email.
        
        Args:
            email: Email
            
        Returns:
            Optional[User]: User
        """
        for user in self.users.values():
            if user.email == email:
                return user
        return None
    
    def get_all_users(self) -> List[User]:
        """
        Get all users.
        
        Returns:
            List[User]: All users
        """
        return list(self.users.values())
    
    def search_users(self, query: str) -> List[User]:
        """
        Search users by username or email.
        
        Args:
            query: Search query
            
        Returns:
            List[User]: Matching users
        """
        if not self.config.enable_user_search:
            return []
        
        query_lower = query.lower()
        return [
            u for u in self.users.values()
            if query_lower in u.username.lower() or query_lower in u.email.lower()
        ]
    
    def update_profile(self, user_id: str, profile: UserProfile) -> UserManagementResult:
        """
        Update user profile.
        
        Args:
            user_id: User ID
            profile: Profile data
            
        Returns:
            UserManagementResult: Update result
        """
        result = UserManagementResult(success=False)
        
        try:
            user = self.users.get(user_id)
            if not user:
                result.errors.append("User not found")
                return result
            
            user.profile = profile
            user.updated_at = datetime.now()
            
            # Track activity
            if self.config.enable_activity_tracking:
                self._track_activity(user_id, "profile_updated")
            
            result.success = True
            result.user = user
            result.message = f"Profile updated for user '{user_id}'"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def update_preferences(self, user_id: str, preferences: UserPreferences) -> UserManagementResult:
        """
        Update user preferences.
        
        Args:
            user_id: User ID
            preferences: Preferences data
            
        Returns:
            UserManagementResult: Update result
        """
        result = UserManagementResult(success=False)
        
        try:
            user = self.users.get(user_id)
            if not user:
                result.errors.append("User not found")
                return result
            
            user.preferences = preferences
            user.updated_at = datetime.now()
            
            # Track activity
            if self.config.enable_activity_tracking:
                self._track_activity(user_id, "preferences_updated")
            
            result.success = True
            result.user = user
            result.message = f"Preferences updated for user '{user_id}'"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def set_user_status(self, user_id: str, status: UserStatus) -> UserManagementResult:
        """
        Set user status.
        
        Args:
            user_id: User ID
            status: User status
            
        Returns:
            UserManagementResult: Set result
        """
        result = UserManagementResult(success=False)
        
        try:
            user = self.users.get(user_id)
            if not user:
                result.errors.append("User not found")
                return result
            
            user.status = status
            user.updated_at = datetime.now()
            
            # Track activity
            if self.config.enable_activity_tracking:
                self._track_activity(user_id, f"status_changed_to_{status.value}")
            
            result.success = True
            result.user = user
            result.message = f"User status set to '{status.value}'"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def set_user_tier(self, user_id: str, tier: UserTier) -> UserManagementResult:
        """
        Set user tier.
        
        Args:
            user_id: User ID
            tier: User tier
            
        Returns:
            UserManagementResult: Set result
        """
        result = UserManagementResult(success=False)
        
        try:
            user = self.users.get(user_id)
            if not user:
                result.errors.append("User not found")
                return result
            
            user.tier = tier
            user.updated_at = datetime.now()
            
            # Track activity
            if self.config.enable_activity_tracking:
                self._track_activity(user_id, f"tier_changed_to_{tier.value}")
            
            result.success = True
            result.user = user
            result.message = f"User tier set to '{tier.value}'"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def _track_activity(self, user_id: str, action: str, **kwargs) -> UserActivity:
        """
        Track user activity.
        
        Args:
            user_id: User ID
            action: Action
            **kwargs: Additional activity data
            
        Returns:
            UserActivity: Activity
        """
        activity = UserActivity(
            activity_id=self._next_activity_id(),
            user_id=user_id,
            action=action,
            **kwargs
        )
        
        self.activities.append(activity)
        
        # Cleanup old activities
        self._cleanup_old_activities()
        
        return activity
    
    def get_user_activities(self, user_id: str) -> List[UserActivity]:
        """
        Get user activities.
        
        Args:
            user_id: User ID
            
        Returns:
            List[UserActivity]: Activities
        """
        return [a for a in self.activities if a.user_id == user_id]
    
    def get_all_activities(self) -> List[UserActivity]:
        """
        Get all activities.
        
        Returns:
            List[UserActivity]: All activities
        """
        return self.activities
    
    def _cleanup_old_activities(self):
        """Cleanup old activities based on retention policy."""
        if self.config.activity_retention_days <= 0:
            return
        
        cutoff_date = datetime.now() - timedelta(days=self.config.activity_retention_days)
        self.activities = [a for a in self.activities if a.timestamp > cutoff_date]
    
    def update_config(self, config: UserManagementConfig) -> UserManagementResult:
        """
        Update user management configuration.
        
        Args:
            config: New configuration
            
        Returns:
            UserManagementResult: Update result
        """
        result = UserManagementResult(success=True)
        
        try:
            self.config = config
            result.message = "Config updated"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def get_config(self) -> UserManagementConfig:
        """
        Get user management configuration.
        
        Returns:
            UserManagementConfig: Configuration
        """
        return self.config


if __name__ == "__main__":
    # Basit test
    config = UserManagementConfig()
    manager = UserManager(config)
    
    # User oluştur
    result = manager.create_user("testuser", "test@example.com")
    
    print(f"User created: {result.message}")
    
    # User ara
    users = manager.search_users("test")
    
    print(f"Search results: {len(users)}")
