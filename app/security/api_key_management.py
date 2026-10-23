"""
MuhammedAI Local Developer - API Key Management
API key management system for security.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
import secrets
import hashlib


class APIKeyType(Enum):
    """API key type."""
    READ_ONLY = "read_only"
    READ_WRITE = "read_write"
    ADMIN = "admin"
    CUSTOM = "custom"


class APIKeyStatus(Enum):
    """API key status."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    REVOKED = "revoked"
    EXPIRED = "expired"


class APIKeyScope(Enum):
    """API key scope."""
    GLOBAL = "global"
    PROJECT = "project"
    ORGANIZATION = "organization"
    USER = "user"
    CUSTOM = "custom"


@dataclass
class APIKey:
    """API key."""
    key_id: str
    user_id: str
    name: str
    key_type: APIKeyType
    scope: APIKeyScope
    key_hash: str
    status: APIKeyStatus = APIKeyStatus.ACTIVE
    description: Optional[str] = None
    expires_at: Optional[datetime] = None
    last_used_at: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class APIKeyUsage:
    """API key usage."""
    usage_id: str
    key_id: str
    endpoint: str
    method: str
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    status_code: Optional[int] = None
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class APIKeyManagementConfig:
    """API key management configuration."""
    enable_key_creation: bool = True
    enable_key_deletion: bool = True
    enable_key_update: bool = True
    enable_key_rotation: bool = True
    max_keys_per_user: int = 10
    default_expiry_days: int = 365
    enable_usage_tracking: bool = True
    enable_rate_limiting: bool = False
    rate_limit_per_minute: int = 60
    enable_ip_whitelist: bool = False


@dataclass
class APIKeyManagementResult:
    """API key management result."""
    success: bool
    message: Optional[str] = None
    api_key: Optional[APIKey] = None
    api_keys: List[APIKey] = field(default_factory=list)
    raw_key: Optional[str] = None
    usage: Optional[APIKeyUsage] = None
    usages: List[APIKeyUsage] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)


class APIKeyManager:
    """
    API key manager.
    
    Özellikler:
    - API key generation
    - API key validation
    - API key revocation
    - API key rotation
    - API key permissions
    - API key usage tracking
    - API key expiration
    - Rate limiting
    - IP whitelist
    """
    
    def __init__(self, config: Optional[APIKeyManagementConfig] = None):
        """
        Initialize API key manager.
        
        Args:
            config: API key management configuration
        """
        self.config = config or APIKeyManagementConfig()
        self.api_keys: Dict[str, APIKey] = {}
        self.usages: List[APIKeyUsage] = []
        self.key_id_counter = 0
        self.usage_id_counter = 0
        self._next_key_id()
        self._next_usage_id()
    
    def _next_key_id(self) -> str:
        """
        Generate next key ID.
        
        Returns:
            str: Key ID
        """
        self.key_id_counter += 1
        return f"key_{self.key_id_counter}"
    
    def _next_usage_id(self) -> str:
        """
        Generate next usage ID.
        
        Returns:
            str: Usage ID
        """
        self.usage_id_counter += 1
        return f"usage_{self.usage_id_counter}"
    
    def _generate_key(self) -> str:
        """
        Generate secure API key.
        
        Returns:
            str: API key
        """
        prefix = "mk_"
        random_part = secrets.token_urlsafe(32)
        return f"{prefix}{random_part}"
    
    def _hash_key(self, key: str) -> str:
        """
        Hash API key.
        
        Args:
            key: API key
            
        Returns:
            str: Hashed key
        """
        return hashlib.sha256(key.encode()).hexdigest()
    
    def create_api_key(self, user_id: str, name: str, key_type: APIKeyType, scope: APIKeyScope, description: Optional[str] = None, expires_in_days: Optional[int] = None) -> APIKeyManagementResult:
        """
        Create a new API key.
        
        Args:
            user_id: User ID
            name: Key name
            key_type: Key type
            scope: Key scope
            description: Key description
            expires_in_days: Expiration in days
            
        Returns:
            APIKeyManagementResult: Create result
        """
        result = APIKeyManagementResult(success=False)
        
        try:
            if not self.config.enable_key_creation:
                result.errors.append("API key creation is disabled")
                return result
            
            # Check max keys per user
            user_keys = self.get_user_api_keys(user_id)
            active_keys = [k for k in user_keys if k.status == APIKeyStatus.ACTIVE]
            
            if len(active_keys) >= self.config.max_keys_per_user:
                result.errors.append(f"Maximum API keys reached (max {self.config.max_keys_per_user})")
                return result
            
            # Generate key
            raw_key = self._generate_key()
            key_hash = self._hash_key(raw_key)
            
            # Calculate expiration
            expires_at = None
            if expires_in_days:
                expires_at = datetime.now() + timedelta(days=expires_in_days)
            elif self.config.default_expiry_days > 0:
                expires_at = datetime.now() + timedelta(days=self.config.default_expiry_days)
            
            api_key = APIKey(
                key_id=self._next_key_id(),
                user_id=user_id,
                name=name,
                key_type=key_type,
                scope=scope,
                key_hash=key_hash,
                description=description,
                expires_at=expires_at
            )
            
            self.api_keys[api_key.key_id] = api_key
            
            result.success = True
            result.api_key = api_key
            result.raw_key = raw_key
            result.api_keys = self.get_all_api_keys()
            result.message = f"API key '{name}' created successfully"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def delete_api_key(self, key_id: str) -> APIKeyManagementResult:
        """
        Delete an API key.
        
        Args:
            key_id: Key ID
            
        Returns:
            APIKeyManagementResult: Delete result
        """
        result = APIKeyManagementResult(success=False)
        
        try:
            if not self.config.enable_key_deletion:
                result.errors.append("API key deletion is disabled")
                return result
            
            if key_id in self.api_keys:
                del self.api_keys[key_id]
                result.success = True
                result.api_keys = self.get_all_api_keys()
                result.message = f"API key '{key_id}' deleted"
            else:
                result.errors.append("API key not found")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def update_api_key(self, key_id: str, **kwargs) -> APIKeyManagementResult:
        """
        Update API key information.
        
        Args:
            key_id: Key ID
            **kwargs: Fields to update
            
        Returns:
            APIKeyManagementResult: Update result
        """
        result = APIKeyManagementResult(success=False)
        
        try:
            if not self.config.enable_key_update:
                result.errors.append("API key update is disabled")
                return result
            
            api_key = self.api_keys.get(key_id)
            if not api_key:
                result.errors.append("API key not found")
                return result
            
            # Update fields
            for key, value in kwargs.items():
                if hasattr(api_key, key):
                    setattr(api_key, key, value)
            
            api_key.updated_at = datetime.now()
            
            result.success = True
            result.api_key = api_key
            result.message = f"API key '{key_id}' updated"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_api_key(self, key_id: str) -> Optional[APIKey]:
        """
        Get API key by ID.
        
        Args:
            key_id: Key ID
            
        Returns:
            Optional[APIKey]: API key
        """
        return self.api_keys.get(key_id)
    
    def get_api_key_by_hash(self, key_hash: str) -> Optional[APIKey]:
        """
        Get API key by hash.
        
        Args:
            key_hash: Key hash
            
        Returns:
            Optional[APIKey]: API key
        """
        for api_key in self.api_keys.values():
            if api_key.key_hash == key_hash:
                return api_key
        return None
    
    def get_all_api_keys(self) -> List[APIKey]:
        """
        Get all API keys.
        
        Returns:
            List[APIKey]: All API keys
        """
        return list(self.api_keys.values())
    
    def get_user_api_keys(self, user_id: str) -> List[APIKey]:
        """
        Get API keys for a user.
        
        Args:
            user_id: User ID
            
        Returns:
            List[APIKey]: User API keys
        """
        return [k for k in self.api_keys.values() if k.user_id == user_id]
    
    def validate_api_key(self, raw_key: str) -> APIKeyManagementResult:
        """
        Validate API key.
        
        Args:
            raw_key: Raw API key
            
        Returns:
            APIKeyManagementResult: Validation result
        """
        result = APIKeyManagementResult(success=False)
        
        try:
            key_hash = self._hash_key(raw_key)
            api_key = self.get_api_key_by_hash(key_hash)
            
            if not api_key:
                result.errors.append("Invalid API key")
                return result
            
            # Check status
            if api_key.status != APIKeyStatus.ACTIVE:
                result.errors.append(f"API key is {api_key.status.value}")
                return result
            
            # Check expiration
            if api_key.expires_at and datetime.now() > api_key.expires_at:
                api_key.status = APIKeyStatus.EXPIRED
                result.errors.append("API key expired")
                return result
            
            # Update last used
            api_key.last_used_at = datetime.now()
            
            # Track usage
            if self.config.enable_usage_tracking:
                self._track_usage(api_key.key_id, "validation")
            
            result.success = True
            result.api_key = api_key
            result.message = "API key valid"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def revoke_api_key(self, key_id: str) -> APIKeyManagementResult:
        """
        Revoke API key.
        
        Args:
            key_id: Key ID
            
        Returns:
            APIKeyManagementResult: Revoke result
        """
        result = APIKeyManagementResult(success=False)
        
        try:
            api_key = self.api_keys.get(key_id)
            if not api_key:
                result.errors.append("API key not found")
                return result
            
            api_key.status = APIKeyStatus.REVOKED
            api_key.updated_at = datetime.now()
            
            result.success = True
            result.api_key = api_key
            result.message = f"API key '{key_id}' revoked"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def rotate_api_key(self, key_id: str) -> APIKeyManagementResult:
        """
        Rotate API key (generate new key, keep same ID).
        
        Args:
            key_id: Key ID
            
        Returns:
            APIKeyManagementResult: Rotation result
        """
        result = APIKeyManagementResult(success=False)
        
        try:
            if not self.config.enable_key_rotation:
                result.errors.append("API key rotation is disabled")
                return result
            
            api_key = self.api_keys.get(key_id)
            if not api_key:
                result.errors.append("API key not found")
                return result
            
            # Generate new key
            new_raw_key = self._generate_key()
            new_key_hash = self._hash_key(new_raw_key)
            
            # Update key hash
            api_key.key_hash = new_key_hash
            api_key.updated_at = datetime.now()
            
            result.success = True
            result.api_key = api_key
            result.raw_key = new_raw_key
            result.message = f"API key '{key_id}' rotated"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def _track_usage(self, key_id: str, endpoint: str, method: str = "GET", **kwargs) -> APIKeyUsage:
        """
        Track API key usage.
        
        Args:
            key_id: Key ID
            endpoint: Endpoint
            method: HTTP method
            **kwargs: Additional usage data
            
        Returns:
            APIKeyUsage: Usage
        """
        usage = APIKeyUsage(
            usage_id=self._next_usage_id(),
            key_id=key_id,
            endpoint=endpoint,
            method=method,
            **kwargs
        )
        
        self.usages.append(usage)
        
        return usage
    
    def get_key_usage(self, key_id: str) -> List[APIKeyUsage]:
        """
        Get usage for an API key.
        
        Args:
            key_id: Key ID
            
        Returns:
            List[APIKeyUsage]: Usage records
        """
        return [u for u in self.usages if u.key_id == key_id]
    
    def get_all_usage(self) -> List[APIKeyUsage]:
        """
        Get all usage records.
        
        Returns:
            List[APIKeyUsage]: All usage records
        """
        return self.usages
    
    def cleanup_expired_keys(self) -> APIKeyManagementResult:
        """
        Cleanup expired API keys.
        
        Returns:
            APIKeyManagementResult: Cleanup result
        """
        result = APIKeyManagementResult(success=True)
        
        try:
            now = datetime.now()
            expired_count = 0
            
            for api_key in self.api_keys.values():
                if api_key.expires_at and now > api_key.expires_at:
                    api_key.status = APIKeyStatus.EXPIRED
                    expired_count += 1
            
            result.message = f"Cleaned up {expired_count} expired API keys"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def update_config(self, config: APIKeyManagementConfig) -> APIKeyManagementResult:
        """
        Update API key management configuration.
        
        Args:
            config: New configuration
            
        Returns:
            APIKeyManagementResult: Update result
        """
        result = APIKeyManagementResult(success=True)
        
        try:
            self.config = config
            result.message = "Config updated"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def get_config(self) -> APIKeyManagementConfig:
        """
        Get API key management configuration.
        
        Returns:
            APIKeyManagementConfig: Configuration
        """
        return self.config


if __name__ == "__main__":
    # Basit test
    config = APIKeyManagementConfig()
    manager = APIKeyManager(config)
    
    # API key oluştur
    result = manager.create_api_key("user_1", "Test Key", APIKeyType.READ_ONLY, APIKeyScope.GLOBAL)
    
    print(f"API key created: {result.message}")
    
    # API key validate et
    validation = manager.validate_api_key(result.raw_key)
    
    print(f"API key valid: {validation.success}")
