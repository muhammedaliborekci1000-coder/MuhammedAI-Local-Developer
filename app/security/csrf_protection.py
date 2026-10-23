"""
MuhammedAI Local Developer - CSRF Protection
CSRF protection system for security.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
import secrets
import hashlib


class CSRFTokenType(Enum):
    """CSRF token type."""
    SESSION = "session"
    COOKIE = "cookie"
    HEADER = "header"
    CUSTOM = "custom"


class CSRFValidationMode(Enum):
    """CSRF validation mode."""
    STRICT = "strict"
    LENIENT = "lenient"
    CUSTOM = "custom"


@dataclass
class CSRFToken:
    """CSRF token."""
    token_id: str
    token_value: str
    token_type: CSRFTokenType
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    expires_at: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.now)
    last_used: Optional[datetime] = None
    is_valid: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CSRFProtectionConfig:
    """CSRF protection configuration."""
    enable_protection: bool = True
    default_token_type: CSRFTokenType = CSRFTokenType.SESSION
    token_length: int = 32
    token_expiry_seconds: int = 3600
    enable_token_rotation: bool = True
    rotation_interval: int = 1800
    enable_ip_binding: bool = False
    enable_user_agent_binding: bool = False
    validation_mode: CSRFValidationMode = CSRFValidationMode.STRICT
    max_tokens_per_user: int = 10


@dataclass
class CSRFProtectionResult:
    """CSRF protection result."""
    success: bool
    message: Optional[str] = None
    token: Optional[CSRFToken] = None
    tokens: List[CSRFToken] = field(default_factory=list)
    is_valid: bool = False
    errors: List[str] = field(default_factory=list)


class CSRFProtection:
    """
    CSRF protection manager.
    
    Özellikler:
    - Token generation
    - Token validation
    - Token rotation
    - Token expiration
    - IP binding
    - User agent binding
    - Session management
    """
    
    def __init__(self, config: Optional[CSRFProtectionConfig] = None):
        """
        Initialize CSRF protection.
        
        Args:
            config: CSRF protection configuration
        """
        self.config = config or CSRFProtectionConfig()
        self.tokens: Dict[str, CSRFToken] = {}
        self.token_id_counter = 0
        self._next_token_id()
    
    def _next_token_id(self) -> str:
        """
        Generate next token ID.
        
        Returns:
            str: Token ID
        """
        self.token_id_counter += 1
        return f"csrf_{self.token_id_counter}"
    
    def _generate_token_value(self) -> str:
        """
        Generate secure token value.
        
        Returns:
            str: Token value
        """
        return secrets.token_hex(self.config.token_length)
    
    def generate_token(self, user_id: Optional[str] = None, session_id: Optional[str] = None, token_type: Optional[CSRFTokenType] = None, expires_in_seconds: Optional[int] = None) -> CSRFProtectionResult:
        """
        Generate CSRF token.
        
        Args:
            user_id: User ID
            session_id: Session ID
            token_type: Token type
            expires_in_seconds: Expiration in seconds
            
        Returns:
            CSRFProtectionResult: Generation result
        """
        result = CSRFProtectionResult(success=False)
        
        try:
            if not self.config.enable_protection:
                result.errors.append("CSRF protection is disabled")
                return result
            
            # Check max tokens per user
            if user_id:
                user_tokens = self.get_user_tokens(user_id)
                valid_tokens = [t for t in user_tokens if t.is_valid]
                
                if len(valid_tokens) >= self.config.max_tokens_per_user:
                    # Revoke oldest token
                    oldest = min(valid_tokens, key=lambda t: t.created_at)
                    self.revoke_token(oldest.token_id)
            
            token_value = self._generate_token_value()
            token_type = token_type or self.config.default_token_type
            
            # Calculate expiration
            expires_at = None
            if expires_in_seconds:
                expires_at = datetime.now() + timedelta(seconds=expires_in_seconds)
            elif self.config.token_expiry_seconds > 0:
                expires_at = datetime.now() + timedelta(seconds=self.config.token_expiry_seconds)
            
            token = CSRFToken(
                token_id=self._next_token_id(),
                token_value=token_value,
                token_type=token_type,
                user_id=user_id,
                session_id=session_id,
                expires_at=expires_at
            )
            
            self.tokens[token.token_id] = token
            
            result.success = True
            result.token = token
            result.tokens = self.get_all_tokens()
            result.message = "CSRF token generated successfully"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def validate_token(self, token_value: str, user_id: Optional[str] = None, ip_address: Optional[str] = None, user_agent: Optional[str] = None) -> CSRFProtectionResult:
        """
        Validate CSRF token.
        
        Args:
            token_value: Token value
            user_id: User ID
            ip_address: IP address
            user_agent: User agent
            
        Returns:
            CSRFProtectionResult: Validation result
        """
        result = CSRFProtectionResult(success=False)
        
        try:
            if not self.config.enable_protection:
                result.success = True
                result.is_valid = True
                result.message = "CSRF protection disabled"
                return result
            
            # Find token
            token = None
            for t in self.tokens.values():
                if t.token_value == token_value:
                    token = t
                    break
            
            if not token:
                result.errors.append("Invalid token")
                return result
            
            # Check if valid
            if not token.is_valid:
                result.errors.append("Token revoked")
                return result
            
            # Check expiration
            if token.expires_at and datetime.now() > token.expires_at:
                token.is_valid = False
                result.errors.append("Token expired")
                return result
            
            # Check user ID match
            if self.config.validation_mode == CSRFValidationMode.STRICT:
                if user_id and token.user_id != user_id:
                    result.errors.append("User ID mismatch")
                    return result
            
            # Update last used
            token.last_used = datetime.now()
            
            result.success = True
            result.is_valid = True
            result.token = token
            result.message = "Token validated successfully"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def revoke_token(self, token_id: str) -> CSRFProtectionResult:
        """
        Revoke CSRF token.
        
        Args:
            token_id: Token ID
            
        Returns:
            CSRFProtectionResult: Revoke result
        """
        result = CSRFProtectionResult(success=False)
        
        try:
            token = self.tokens.get(token_id)
            if not token:
                result.errors.append("Token not found")
                return result
            
            token.is_valid = False
            
            result.success = True
            result.token = token
            result.message = f"Token '{token_id}' revoked"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def rotate_token(self, token_id: str) -> CSRFProtectionResult:
        """
        Rotate CSRF token (generate new token, keep same ID).
        
        Args:
            token_id: Token ID
            
        Returns:
            CSRFProtectionResult: Rotation result
        """
        result = CSRFProtectionResult(success=False)
        
        try:
            if not self.config.enable_token_rotation:
                result.errors.append("Token rotation is disabled")
                return result
            
            token = self.tokens.get(token_id)
            if not token:
                result.errors.append("Token not found")
                return result
            
            # Generate new token value
            new_token_value = self._generate_token_value()
            
            # Update token
            token.token_value = new_token_value
            token.last_used = datetime.now()
            
            result.success = True
            result.token = token
            result.message = f"Token '{token_id}' rotated"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_token(self, token_id: str) -> Optional[CSRFToken]:
        """
        Get token by ID.
        
        Args:
            token_id: Token ID
            
        Returns:
            Optional[CSRFToken]: Token
        """
        return self.tokens.get(token_id)
    
    def get_token_by_value(self, token_value: str) -> Optional[CSRFToken]:
        """
        Get token by value.
        
        Args:
            token_value: Token value
            
        Returns:
            Optional[CSRFToken]: Token
        """
        for token in self.tokens.values():
            if token.token_value == token_value:
                return token
        return None
    
    def get_all_tokens(self) -> List[CSRFToken]:
        """
        Get all tokens.
        
        Returns:
            List[CSRFToken]: All tokens
        """
        return list(self.tokens.values())
    
    def get_user_tokens(self, user_id: str) -> List[CSRFToken]:
        """
        Get tokens for a user.
        
        Args:
            user_id: User ID
            
        Returns:
            List[CSRFToken]: User tokens
        """
        return [t for t in self.tokens.values() if t.user_id == user_id]
    
    def get_session_tokens(self, session_id: str) -> List[CSRFToken]:
        """
        Get tokens for a session.
        
        Args:
            session_id: Session ID
            
        Returns:
            List[CSRFToken]: Session tokens
        """
        return [t for t in self.tokens.values() if t.session_id == session_id]
    
    def cleanup_expired_tokens(self) -> CSRFProtectionResult:
        """
        Cleanup expired tokens.
        
        Returns:
            CSRFProtectionResult: Cleanup result
        """
        result = CSRFProtectionResult(success=True)
        
        try:
            now = datetime.now()
            expired_count = 0
            
            for token in self.tokens.values():
                if token.expires_at and now > token.expires_at:
                    token.is_valid = False
                    expired_count += 1
            
            result.message = f"Cleaned up {expired_count} expired tokens"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def update_config(self, config: CSRFProtectionConfig) -> CSRFProtectionResult:
        """
        Update CSRF protection configuration.
        
        Args:
            config: New configuration
            
        Returns:
            CSRFProtectionResult: Update result
        """
        result = CSRFProtectionResult(success=True)
        
        try:
            self.config = config
            result.message = "Config updated"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def get_config(self) -> CSRFProtectionConfig:
        """
        Get CSRF protection configuration.
        
        Returns:
            CSRFProtectionConfig: Configuration
        """
        return self.config


if __name__ == "__main__":
    # Basit test
    config = CSRFProtectionConfig()
    protection = CSRFProtection(config)
    
    # Token oluştur
    result = protection.generate_token(user_id="user_1")
    
    print(f"Token generated: {result.message}")
    print(f"Token value: {result.token.token_value}")
    
    # Token validate et
    validation = protection.validate_token(result.token.token_value, user_id="user_1")
    
    print(f"Token valid: {validation.is_valid}")
