"""
MuhammedAI Local Developer - Encryption
Encryption system for security.
"""

from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import secrets
import hashlib
import base64


class EncryptionAlgorithm(Enum):
    """Encryption algorithm."""
    AES_256 = "aes_256"
    AES_128 = "aes_128"
    RSA_4096 = "rsa_4096"
    RSA_2048 = "rsa_2048"
    CUSTOM = "custom"


class EncryptionMode(Enum):
    """Encryption mode."""
    ECB = "ecb"
    CBC = "cbc"
    GCM = "gcm"
    CTR = "ctr"
    CUSTOM = "custom"


class HashAlgorithm(Enum):
    """Hash algorithm."""
    SHA256 = "sha256"
    SHA512 = "sha512"
    MD5 = "md5"
    SHA1 = "sha1"
    CUSTOM = "custom"


class KeyType(Enum):
    """Key type."""
    SYMMETRIC = "symmetric"
    ASYMMETRIC = "asymmetric"
    HASH = "hash"
    CUSTOM = "custom"


@dataclass
class EncryptionKey:
    """Encryption key."""
    key_id: str
    key_type: KeyType
    algorithm: EncryptionAlgorithm
    key_data: str
    iv: Optional[str] = None
    salt: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    expires_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EncryptionConfig:
    """Encryption configuration."""
    default_algorithm: EncryptionAlgorithm = EncryptionAlgorithm.AES_256
    default_mode: EncryptionMode = EncryptionMode.GCM
    enable_key_rotation: bool = True
    key_rotation_days: int = 90
    enable_key_caching: bool = True
    enable_compression: bool = False
    enable_integrity_check: bool = True


@dataclass
class EncryptionResult:
    """Encryption result."""
    success: bool
    message: Optional[str] = None
    encrypted_data: Optional[str] = None
    decrypted_data: Optional[str] = None
    key: Optional[EncryptionKey] = None
    hash: Optional[str] = None
    errors: List[str] = field(default_factory=list)


class EncryptionManager:
    """
    Encryption manager.
    
    Özellikler:
    - Symmetric encryption
    - Asymmetric encryption
    - Hashing
    - Key generation
    - Key management
    - Data encryption/decryption
    - Integrity checking
    """
    
    def __init__(self, config: Optional[EncryptionConfig] = None):
        """
        Initialize encryption manager.
        
        Args:
            config: Encryption configuration
        """
        self.config = config or EncryptionConfig()
        self.keys: Dict[str, EncryptionKey] = {}
        self.key_id_counter = 0
        self._next_key_id()
    
    def _next_key_id(self) -> str:
        """
        Generate next key ID.
        
        Returns:
            str: Key ID
        """
        self.key_id_counter += 1
        return f"key_{self.key_id_counter}"
    
    def generate_key(self, key_type: KeyType, algorithm: EncryptionAlgorithm, key_length: int = 32) -> EncryptionResult:
        """
        Generate encryption key.
        
        Args:
            key_type: Key type
            algorithm: Encryption algorithm
            key_length: Key length in bytes
            
        Returns:
            EncryptionResult: Generation result
        """
        result = EncryptionResult(success=False)
        
        try:
            key_data = secrets.token_bytes(key_length)
            key_b64 = base64.b64encode(key_data).decode()
            
            # Generate IV for symmetric keys
            iv = None
            if key_type == KeyType.SYMMETRIC:
                iv_bytes = secrets.token_bytes(16)
                iv = base64.b64encode(iv_bytes).decode()
            
            # Generate salt for hashing
            salt = None
            if key_type == KeyType.HASH:
                salt_bytes = secrets.token_bytes(16)
                salt = base64.b64encode(salt_bytes).decode()
            
            key = EncryptionKey(
                key_id=self._next_key_id(),
                key_type=key_type,
                algorithm=algorithm,
                key_data=key_b64,
                iv=iv,
                salt=salt
            )
            
            self.keys[key.key_id] = key
            
            result.success = True
            result.key = key
            result.message = f"Key generated successfully"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def encrypt(self, data: str, key_id: Optional[str] = None, algorithm: Optional[EncryptionAlgorithm] = None, mode: Optional[EncryptionMode] = None) -> EncryptionResult:
        """
        Encrypt data.
        
        Args:
            data: Data to encrypt
            key_id: Key ID (optional, will generate if not provided)
            algorithm: Encryption algorithm
            mode: Encryption mode
            
        Returns:
            EncryptionResult: Encryption result
        """
        result = EncryptionResult(success=False)
        
        try:
            # Use provided key or generate new one
            if key_id:
                key = self.keys.get(key_id)
                if not key:
                    result.errors.append("Key not found")
                    return result
            else:
                key_result = self.generate_key(KeyType.SYMMETRIC, algorithm or self.config.default_algorithm)
                if not key_result.success:
                    result.errors.extend(key_result.errors)
                    return result
                key = key_result.key
            
            # Simple XOR encryption for demonstration (in production, use proper crypto library)
            key_bytes = base64.b64decode(key.key_data)
            data_bytes = data.encode()
            
            encrypted_bytes = bytearray()
            for i, byte in enumerate(data_bytes):
                encrypted_bytes.append(byte ^ key_bytes[i % len(key_bytes)])
            
            encrypted_b64 = base64.b64encode(bytes(encrypted_bytes)).decode()
            
            # Add integrity check if enabled
            if self.config.enable_integrity_check:
                hash_result = self.hash(encrypted_b64)
                if hash_result.success:
                    result.hash = hash_result.hash
            
            result.success = True
            result.encrypted_data = encrypted_b64
            result.key = key
            result.message = "Data encrypted successfully"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def decrypt(self, encrypted_data: str, key_id: str, expected_hash: Optional[str] = None) -> EncryptionResult:
        """
        Decrypt data.
        
        Args:
            encrypted_data: Encrypted data
            key_id: Key ID
            expected_hash: Expected hash for integrity check
            
        Returns:
            EncryptionResult: Decryption result
        """
        result = EncryptionResult(success=False)
        
        try:
            key = self.keys.get(key_id)
            if not key:
                result.errors.append("Key not found")
                return result
            
            # Verify integrity if hash provided
            if self.config.enable_integrity_check and expected_hash:
                hash_result = self.hash(encrypted_data)
                if hash_result.success and hash_result.hash != expected_hash:
                    result.errors.append("Integrity check failed")
                    return result
            
            # Simple XOR decryption
            key_bytes = base64.b64decode(key.key_data)
            encrypted_bytes = base64.b64decode(encrypted_data)
            
            decrypted_bytes = bytearray()
            for i, byte in enumerate(encrypted_bytes):
                decrypted_bytes.append(byte ^ key_bytes[i % len(key_bytes)])
            
            decrypted_data = decrypted_bytes.decode()
            
            result.success = True
            result.decrypted_data = decrypted_data
            result.message = "Data decrypted successfully"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def hash(self, data: str, algorithm: Optional[HashAlgorithm] = None) -> EncryptionResult:
        """
        Hash data.
        
        Args:
            data: Data to hash
            algorithm: Hash algorithm
            
        Returns:
            EncryptionResult: Hash result
        """
        result = EncryptionResult(success=False)
        
        try:
            algo = algorithm or HashAlgorithm.SHA256
            
            if algo == HashAlgorithm.SHA256:
                hash_obj = hashlib.sha256()
            elif algo == HashAlgorithm.SHA512:
                hash_obj = hashlib.sha512()
            elif algo == HashAlgorithm.MD5:
                hash_obj = hashlib.md5()
            elif algo == HashAlgorithm.SHA1:
                hash_obj = hashlib.sha1()
            else:
                result.errors.append("Unsupported hash algorithm")
                return result
            
            hash_obj.update(data.encode())
            hash_hex = hash_obj.hexdigest()
            
            result.success = True
            result.hash = hash_hex
            result.message = "Data hashed successfully"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def verify_hash(self, data: str, expected_hash: str, algorithm: Optional[HashAlgorithm] = None) -> EncryptionResult:
        """
        Verify hash.
        
        Args:
            data: Data to verify
            expected_hash: Expected hash
            algorithm: Hash algorithm
            
        Returns:
            EncryptionResult: Verification result
        """
        result = EncryptionResult(success=False)
        
        try:
            hash_result = self.hash(data, algorithm)
            
            if hash_result.success and hash_result.hash == expected_hash:
                result.success = True
                result.message = "Hash verified successfully"
            else:
                result.errors.append("Hash verification failed")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_key(self, key_id: str) -> Optional[EncryptionKey]:
        """
        Get key by ID.
        
        Args:
            key_id: Key ID
            
        Returns:
            Optional[EncryptionKey]: Key
        """
        return self.keys.get(key_id)
    
    def get_all_keys(self) -> List[EncryptionKey]:
        """
        Get all keys.
        
        Returns:
            List[EncryptionKey]: All keys
        """
        return list(self.keys.values())
    
    def delete_key(self, key_id: str) -> EncryptionResult:
        """
        Delete key.
        
        Args:
            key_id: Key ID
            
        Returns:
            EncryptionResult: Delete result
        """
        result = EncryptionResult(success=False)
        
        try:
            if key_id in self.keys:
                del self.keys[key_id]
                result.success = True
                result.message = f"Key '{key_id}' deleted"
            else:
                result.errors.append("Key not found")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def rotate_key(self, key_id: str) -> EncryptionResult:
        """
        Rotate key (generate new key, keep same ID).
        
        Args:
            key_id: Key ID
            
        Returns:
            EncryptionResult: Rotation result
        """
        result = EncryptionResult(success=False)
        
        try:
            if not self.config.enable_key_rotation:
                result.errors.append("Key rotation is disabled")
                return result
            
            old_key = self.keys.get(key_id)
            if not old_key:
                result.errors.append("Key not found")
                return result
            
            # Generate new key with same parameters
            key_result = self.generate_key(old_key.key_type, old_key.algorithm)
            if not key_result.success:
                result.errors.extend(key_result.errors)
                return result
            
            # Replace old key
            new_key = key_result.key
            new_key.key_id = key_id
            self.keys[key_id] = new_key
            
            result.success = True
            result.key = new_key
            result.message = f"Key '{key_id}' rotated successfully"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def update_config(self, config: EncryptionConfig) -> EncryptionResult:
        """
        Update encryption configuration.
        
        Args:
            config: New configuration
            
        Returns:
            EncryptionResult: Update result
        """
        result = EncryptionResult(success=True)
        
        try:
            self.config = config
            result.message = "Config updated"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def get_config(self) -> EncryptionConfig:
        """
        Get encryption configuration.
        
        Returns:
            EncryptionConfig: Configuration
        """
        return self.config


if __name__ == "__main__":
    # Basit test
    config = EncryptionConfig()
    manager = EncryptionManager(config)
    
    # Key oluştur
    result = manager.generate_key(KeyType.SYMMETRIC, EncryptionAlgorithm.AES_256)
    
    print(f"Key generated: {result.message}")
    
    # Data encrypt et
    encrypt_result = manager.encrypt("Hello, World!", result.key.key_id)
    
    print(f"Encrypted: {encrypt_result.encrypted_data}")
    
    # Data decrypt et
    decrypt_result = manager.decrypt(encrypt_result.encrypted_data, result.key.key_id)
    
    print(f"Decrypted: {decrypt_result.decrypted_data}")
