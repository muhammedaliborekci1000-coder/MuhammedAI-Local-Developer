"""
MuhammedAI Local Developer - Secure Storage
Secure storage system for security.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
import json
import base64
import hashlib


class StorageType(Enum):
    """Storage type."""
    MEMORY = "memory"
    FILE = "file"
    DATABASE = "database"
    CUSTOM = "custom"


class EncryptionType(Enum):
    """Encryption type."""
    NONE = "none"
    AES_256 = "aes_256"
    CUSTOM = "custom"


class AccessLevel(Enum):
    """Access level."""
    PUBLIC = "public"
    PRIVATE = "private"
    RESTRICTED = "restricted"
    CONFIDENTIAL = "confidential"


@dataclass
class StorageItem:
    """Storage item."""
    item_id: str
    key: str
    value: Any
    storage_type: StorageType
    encryption_type: EncryptionType
    access_level: AccessLevel
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    expires_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SecureStorageConfig:
    """Secure storage configuration."""
    enable_encryption: bool = True
    default_encryption_type: EncryptionType = EncryptionType.AES_256
    enable_compression: bool = False
    enable_versioning: bool = True
    max_versions: int = 10
    enable_ttl: bool = True
    default_ttl_seconds: int = 3600
    enable_access_control: bool = True


@dataclass
class SecureStorageResult:
    """Secure storage result."""
    success: bool
    message: Optional[str] = None
    item: Optional[StorageItem] = None
    items: List[StorageItem] = field(default_factory=list)
    value: Optional[Any] = None
    errors: List[str] = field(default_factory=list)


class SecureStorage:
    """
    Secure storage manager.
    
    Özellikler:
    - Secure data storage
    - Encryption support
    - Access control
    - TTL support
    - Versioning
    - Memory storage
    """
    
    def __init__(self, config: Optional[SecureStorageConfig] = None):
        """
        Initialize secure storage.
        
        Args:
            config: Secure storage configuration
        """
        self.config = config or SecureStorageConfig()
        self.storage: Dict[str, StorageItem] = {}
        self.item_id_counter = 0
        self._next_item_id()
    
    def _next_item_id(self) -> str:
        """
        Generate next item ID.
        
        Returns:
            str: Item ID
        """
        self.item_id_counter += 1
        return f"item_{self.item_id_counter}"
    
    def _encrypt_value(self, value: Any) -> str:
        """
        Encrypt value.
        
        Args:
            value: Value to encrypt
            
        Returns:
            str: Encrypted value
        """
        if not self.config.enable_encryption:
            return str(value)
        
        # Simple XOR encryption for demonstration
        value_str = str(value)
        key = "secure_key"
        encrypted = []
        
        for i, char in enumerate(value_str):
            encrypted_char = chr(ord(char) ^ ord(key[i % len(key)]))
            encrypted.append(encrypted_char)
        
        encrypted_str = ''.join(encrypted)
        return base64.b64encode(encrypted_str.encode()).decode()
    
    def _decrypt_value(self, encrypted_value: str) -> str:
        """
        Decrypt value.
        
        Args:
            encrypted_value: Encrypted value
            
        Returns:
            str: Decrypted value
        """
        if not self.config.enable_encryption:
            return encrypted_value
        
        # Simple XOR decryption
        key = "secure_key"
        encrypted_bytes = base64.b64decode(encrypted_value.encode())
        encrypted_str = encrypted_bytes.decode()
        
        decrypted = []
        for i, char in enumerate(encrypted_str):
            decrypted_char = chr(ord(char) ^ ord(key[i % len(key)]))
            decrypted.append(decrypted_char)
        
        return ''.join(decrypted)
    
    def store(self, key: str, value: Any, storage_type: StorageType = StorageType.MEMORY, access_level: AccessLevel = AccessLevel.PRIVATE, ttl_seconds: Optional[int] = None) -> SecureStorageResult:
        """
        Store a value securely.
        
        Args:
            key: Storage key
            value: Value to store
            storage_type: Storage type
            access_level: Access level
            ttl_seconds: Time to live in seconds
            
        Returns:
            SecureStorageResult: Store result
        """
        result = SecureStorageResult(success=False)
        
        try:
            # Calculate expiration
            expires_at = None
            if ttl_seconds:
                expires_at = datetime.now() + timedelta(seconds=ttl_seconds)
            elif self.config.enable_ttl and self.config.default_ttl_seconds > 0:
                expires_at = datetime.now() + timedelta(seconds=self.config.default_ttl_seconds)
            
            # Encrypt value
            encrypted_value = self._encrypt_value(value)
            
            item = StorageItem(
                item_id=self._next_item_id(),
                key=key,
                value=encrypted_value,
                storage_type=storage_type,
                encryption_type=self.config.default_encryption_type,
                access_level=access_level,
                expires_at=expires_at
            )
            
            self.storage[key] = item
            
            result.success = True
            result.item = item
            result.message = f"Value stored securely for key '{key}'"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def retrieve(self, key: str) -> SecureStorageResult:
        """
        Retrieve a value securely.
        
        Args:
            key: Storage key
            
        Returns:
            SecureStorageResult: Retrieve result
        """
        result = SecureStorageResult(success=False)
        
        try:
            item = self.storage.get(key)
            
            if not item:
                result.errors.append("Key not found")
                return result
            
            # Check expiration
            if item.expires_at and datetime.now() > item.expires_at:
                result.errors.append("Item expired")
                return result
            
            # Decrypt value
            decrypted_value = self._decrypt_value(item.value)
            
            result.success = True
            result.item = item
            result.value = decrypted_value
            result.message = f"Value retrieved for key '{key}'"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def delete(self, key: str) -> SecureStorageResult:
        """
        Delete a stored value.
        
        Args:
            key: Storage key
            
        Returns:
            SecureStorageResult: Delete result
        """
        result = SecureStorageResult(success=False)
        
        try:
            if key in self.storage:
                del self.storage[key]
                result.success = True
                result.message = f"Item deleted for key '{key}'"
            else:
                result.errors.append("Key not found")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def update(self, key: str, value: Any) -> SecureStorageResult:
        """
        Update a stored value.
        
        Args:
            key: Storage key
            value: New value
            
        Returns:
            SecureStorageResult: Update result
        """
        result = SecureStorageResult(success=False)
        
        try:
            item = self.storage.get(key)
            
            if not item:
                result.errors.append("Key not found")
                return result
            
            # Encrypt new value
            encrypted_value = self._encrypt_value(value)
            
            item.value = encrypted_value
            item.updated_at = datetime.now()
            
            result.success = True
            result.item = item
            result.message = f"Item updated for key '{key}'"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def exists(self, key: str) -> bool:
        """
        Check if key exists.
        
        Args:
            key: Storage key
            
        Returns:
            bool: Exists
        """
        item = self.storage.get(key)
        if not item:
            return False
        
        # Check expiration
        if item.expires_at and datetime.now() > item.expires_at:
            return False
        
        return True
    
    def get_all_keys(self) -> List[str]:
        """
        Get all keys.
        
        Returns:
            List[str]: All keys
        """
        keys = []
        now = datetime.now()
        
        for key, item in self.storage.items():
            if item.expires_at and now > item.expires_at:
                continue
            keys.append(key)
        
        return keys
    
    def get_all_items(self) -> List[StorageItem]:
        """
        Get all items.
        
        Returns:
            List[StorageItem]: All items
        """
        items = []
        now = datetime.now()
        
        for item in self.storage.values():
            if item.expires_at and now > item.expires_at:
                continue
            items.append(item)
        
        return items
    
    def cleanup_expired(self) -> SecureStorageResult:
        """
        Cleanup expired items.
        
        Returns:
            SecureStorageResult: Cleanup result
        """
        result = SecureStorageResult(success=True)
        
        try:
            now = datetime.now()
            expired_count = 0
            
            keys_to_delete = []
            for key, item in self.storage.items():
                if item.expires_at and now > item.expires_at:
                    keys_to_delete.append(key)
                    expired_count += 1
            
            for key in keys_to_delete:
                del self.storage[key]
            
            result.message = f"Cleaned up {expired_count} expired items"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def clear_all(self) -> SecureStorageResult:
        """
        Clear all items.
        
        Returns:
            SecureStorageResult: Clear result
        """
        result = SecureStorageResult(success=True)
        
        try:
            self.storage.clear()
            result.message = "All items cleared"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def update_config(self, config: SecureStorageConfig) -> SecureStorageResult:
        """
        Update secure storage configuration.
        
        Args:
            config: New configuration
            
        Returns:
            SecureStorageResult: Update result
        """
        result = SecureStorageResult(success=True)
        
        try:
            self.config = config
            result.message = "Config updated"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def get_config(self) -> SecureStorageConfig:
        """
        Get secure storage configuration.
        
        Returns:
            SecureStorageConfig: Configuration
        """
        return self.config


if __name__ == "__main__":
    # Basit test
    from datetime import timedelta
    
    config = SecureStorageConfig()
    storage = SecureStorage(config)
    
    # Store et
    result = storage.store("api_key", "secret_key_123")
    
    print(f"Stored: {result.message}")
    
    # Retrieve et
    result = storage.retrieve("api_key")
    
    print(f"Retrieved: {result.value}")
    
    # Delete et
    result = storage.delete("api_key")
    
    print(f"Deleted: {result.message}")
