"""
MuhammedAI Local Developer - Password Management
Password management system for security.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum
import secrets
import hashlib
import re


class PasswordStrength(Enum):
    """Password strength."""
    VERY_WEAK = "very_weak"
    WEAK = "weak"
    MEDIUM = "medium"
    STRONG = "strong"
    VERY_STRONG = "very_strong"


class HashAlgorithm(Enum):
    """Hash algorithm."""
    SHA256 = "sha256"
    SHA512 = "sha512"
    BCRYPT = "bcrypt"
    ARGON2 = "argon2"
    CUSTOM = "custom"


class PasswordPolicy(Enum):
    """Password policy."""
    MIN_LENGTH = "min_length"
    MAX_LENGTH = "max_length"
    REQUIRE_UPPERCASE = "require_uppercase"
    REQUIRE_LOWERCASE = "require_lowercase"
    REQUIRE_DIGITS = "require_digits"
    REQUIRE_SPECIAL = "require_special"
    NO_COMMON_PASSWORDS = "no_common_passwords"
    NO_PERSONAL_INFO = "no_personal_info"


@dataclass
class PasswordPolicyConfig:
    """Password policy configuration."""
    min_length: int = 8
    max_length: int = 128
    require_uppercase: bool = True
    require_lowercase: bool = True
    require_digits: bool = True
    require_special: bool = True
    no_common_passwords: bool = True
    no_personal_info: bool = True
    special_characters: str = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    common_passwords: List[str] = field(default_factory=lambda: ["password", "123456", "qwerty", "admin"])


@dataclass
class PasswordHash:
    """Password hash."""
    hash_id: str
    password_hash: str
    salt: str
    algorithm: HashAlgorithm
    iterations: int
    created_at: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PasswordValidationResult:
    """Password validation result."""
    is_valid: bool
    strength: Optional[PasswordStrength] = None
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    score: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PasswordManagementResult:
    """Password management result."""
    success: bool
    message: Optional[str] = None
    password_hash: Optional[PasswordHash] = None
    validation_result: Optional[PasswordValidationResult] = None
    errors: List[str] = field(default_factory=list)


class PasswordManager:
    """
    Password manager.
    
    Özellikler:
    - Password hashing
    - Password validation
    - Password strength checking
    - Password policy enforcement
    - Salt generation
    """
    
    def __init__(self, policy: Optional[PasswordPolicyConfig] = None, default_algorithm: HashAlgorithm = HashAlgorithm.SHA256):
        """
        Initialize password manager.
        
        Args:
            policy: Password policy configuration
            default_algorithm: Default hash algorithm
        """
        self.policy = policy or PasswordPolicyConfig()
        self.default_algorithm = default_algorithm
        self.hashes: Dict[str, PasswordHash] = {}
        self.hash_id_counter = 0
        self._next_hash_id()
    
    def _next_hash_id(self) -> str:
        """
        Generate next hash ID.
        
        Returns:
            str: Hash ID
        """
        self.hash_id_counter += 1
        return f"hash_{self.hash_id_counter}"
    
    def generate_salt(self, length: int = 32) -> str:
        """
        Generate random salt.
        
        Args:
            length: Salt length
            
        Returns:
            str: Salt
        """
        return secrets.token_hex(length)
    
    def hash_password(self, password: str, algorithm: Optional[HashAlgorithm] = None, salt: Optional[str] = None, iterations: int = 100000) -> PasswordManagementResult:
        """
        Hash a password.
        
        Args:
            password: Password to hash
            algorithm: Hash algorithm
            salt: Salt (generated if not provided)
            iterations: Number of iterations
            
        Returns:
            PasswordManagementResult: Hash result
        """
        result = PasswordManagementResult(success=False)
        
        try:
            algorithm = algorithm or self.default_algorithm
            salt = salt or self.generate_salt()
            
            # Hash password
            if algorithm == HashAlgorithm.SHA256:
                password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
            elif algorithm == HashAlgorithm.SHA512:
                password_hash = hashlib.sha512((password + salt).encode()).hexdigest()
            else:
                password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
            
            # Apply iterations
            for _ in range(iterations):
                password_hash = hashlib.sha256((password_hash + salt).encode()).hexdigest()
            
            password_hash_obj = PasswordHash(
                hash_id=self._next_hash_id(),
                password_hash=password_hash,
                salt=salt,
                algorithm=algorithm,
                iterations=iterations,
                created_at=str(secrets.token_hex(16))
            )
            
            self.hashes[password_hash_obj.hash_id] = password_hash_obj
            
            result.success = True
            result.password_hash = password_hash_obj
            result.message = "Password hashed successfully"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def verify_password(self, password: str, password_hash: PasswordHash) -> bool:
        """
        Verify a password against a hash.
        
        Args:
            password: Password to verify
            password_hash: Password hash to verify against
            
        Returns:
            bool: Is valid
        """
        try:
            # Hash the password with the same parameters
            if password_hash.algorithm == HashAlgorithm.SHA256:
                computed_hash = hashlib.sha256((password + password_hash.salt).encode()).hexdigest()
            elif password_hash.algorithm == HashAlgorithm.SHA512:
                computed_hash = hashlib.sha512((password + password_hash.salt).encode()).hexdigest()
            else:
                computed_hash = hashlib.sha256((password + password_hash.salt).encode()).hexdigest()
            
            # Apply iterations
            for _ in range(password_hash.iterations):
                computed_hash = hashlib.sha256((computed_hash + password_hash.salt).encode()).hexdigest()
            
            return computed_hash == password_hash.password_hash
        except:
            return False
    
    def validate_password(self, password: str, personal_info: Optional[Dict[str, str]] = None) -> PasswordValidationResult:
        """
        Validate password against policy.
        
        Args:
            password: Password to validate
            personal_info: Personal information to avoid (e.g., username, email)
            
        Returns:
            PasswordValidationResult: Validation result
        """
        result = PasswordValidationResult(is_valid=True)
        score = 0
        
        # Check length
        if len(password) < self.policy.min_length:
            result.is_valid = False
            result.errors.append(f"Password must be at least {self.policy.min_length} characters")
        else:
            score += 1
        
        if len(password) > self.policy.max_length:
            result.is_valid = False
            result.errors.append(f"Password must not exceed {self.policy.max_length} characters")
        else:
            score += 1
        
        # Check uppercase
        if self.policy.require_uppercase and not re.search(r'[A-Z]', password):
            result.is_valid = False
            result.errors.append("Password must contain at least one uppercase letter")
        elif re.search(r'[A-Z]', password):
            score += 1
        
        # Check lowercase
        if self.policy.require_lowercase and not re.search(r'[a-z]', password):
            result.is_valid = False
            result.errors.append("Password must contain at least one lowercase letter")
        elif re.search(r'[a-z]', password):
            score += 1
        
        # Check digits
        if self.policy.require_digits and not re.search(r'\d', password):
            result.is_valid = False
            result.errors.append("Password must contain at least one digit")
        elif re.search(r'\d', password):
            score += 1
        
        # Check special characters
        if self.policy.require_special and not re.search(f'[{re.escape(self.policy.special_characters)}]', password):
            result.is_valid = False
            result.errors.append(f"Password must contain at least one special character ({self.policy.special_characters})")
        elif re.search(f'[{re.escape(self.policy.special_characters)}]', password):
            score += 1
        
        # Check common passwords
        if self.policy.no_common_passwords:
            password_lower = password.lower()
            for common in self.policy.common_passwords:
                if common in password_lower:
                    result.is_valid = False
                    result.errors.append("Password is too common")
                    break
        
        # Check personal info
        if self.policy.no_personal_info and personal_info:
            for key, value in personal_info.items():
                if value and value.lower() in password.lower():
                    result.is_valid = False
                    result.errors.append(f"Password must not contain {key}")
        
        # Calculate strength
        if score <= 2:
            result.strength = PasswordStrength.VERY_WEAK
        elif score <= 3:
            result.strength = PasswordStrength.WEAK
        elif score <= 4:
            result.strength = PasswordStrength.MEDIUM
        elif score <= 5:
            result.strength = PasswordStrength.STRONG
        else:
            result.strength = PasswordStrength.VERY_STRONG
        
        result.score = score
        
        return result
    
    def generate_password(self, length: int = 16, include_uppercase: bool = True, include_lowercase: bool = True, include_digits: bool = True, include_special: bool = True) -> str:
        """
        Generate a random password.
        
        Args:
            length: Password length
            include_uppercase: Include uppercase letters
            include_lowercase: Include lowercase letters
            include_digits: Include digits
            include_special: Include special characters
            
        Returns:
            str: Generated password
        """
        chars = ""
        if include_lowercase:
            chars += "abcdefghijklmnopqrstuvwxyz"
        if include_uppercase:
            chars += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if include_digits:
            chars += "0123456789"
        if include_special:
            chars += self.policy.special_characters
        
        if not chars:
            chars = "abcdefghijklmnopqrstuvwxyz"
        
        password = ''.join(secrets.choice(chars) for _ in range(length))
        return password
    
    def update_policy(self, policy: PasswordPolicyConfig) -> PasswordManagementResult:
        """
        Update password policy.
        
        Args:
            policy: New policy
            
        Returns:
            PasswordManagementResult: Update result
        """
        result = PasswordManagementResult(success=True)
        
        try:
            self.policy = policy
            result.message = "Policy updated"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def get_policy(self) -> PasswordPolicyConfig:
        """
        Get password policy.
        
        Returns:
            PasswordPolicyConfig: Policy
        """
        return self.policy


if __name__ == "__main__":
    # Basit test
    policy = PasswordPolicyConfig()
    manager = PasswordManager(policy)
    
    # Hash password
    result = manager.hash_password("MySecurePassword123!")
    
    print(f"Hashed: {result.message}")
    
    # Validate password
    validation = manager.validate_password("MySecurePassword123!")
    
    print(f"Valid: {validation.is_valid}")
    print(f"Strength: {validation.strength.value}")
    
    # Generate password
    password = manager.generate_password(16)
    
    print(f"Generated: {password}")
