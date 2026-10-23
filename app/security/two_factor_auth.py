"""
MuhammedAI Local Developer - Two-Factor Authentication
Two-factor authentication system for security.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum
import secrets
import hashlib
import time


class TwoFactorMethod(Enum):
    """Two-factor authentication method."""
    TOTP = "totp"
    SMS = "sms"
    EMAIL = "email"
    AUTHENTICATOR_APP = "authenticator_app"
    HARDWARE_TOKEN = "hardware_token"
    BACKUP_CODES = "backup_codes"
    CUSTOM = "custom"


class TwoFactorStatus(Enum):
    """Two-factor authentication status."""
    DISABLED = "disabled"
    ENABLED = "enabled"
    REQUIRED = "required"
    VERIFIED = "verified"
    LOCKED = "locked"


@dataclass
class TwoFactorSecret:
    """Two-factor secret."""
    secret_id: str
    user_id: str
    secret: str
    method: TwoFactorMethod
    status: TwoFactorStatus
    created_at: str
    expires_at: Optional[str] = None
    verified_at: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TwoFactorConfig:
    """Two-factor authentication configuration."""
    enable_2fa: bool = True
    default_method: TwoFactorMethod = TwoFactorMethod.TOTP
    require_2fa: bool = False
    totp_expiry_seconds: int = 30
    backup_codes_count: int = 10
    max_attempts: int = 5
    lockout_duration_seconds: int = 300


@dataclass
class TwoFactorResult:
    """Two-factor authentication result."""
    success: bool
    message: Optional[str] = None
    secret: Optional[TwoFactorSecret] = None
    code: Optional[str] = None
    is_valid: bool = False
    errors: List[str] = field(default_factory=list)


class TwoFactorAuth:
    """
    Two-factor authentication manager.
    
    Özellikler:
    - TOTP generation
    - TOTP verification
    - Secret generation
    - Backup codes
    - Status management
    - Attempt tracking
    """
    
    def __init__(self, config: Optional[TwoFactorConfig] = None):
        """
        Initialize two-factor authentication.
        
        Args:
            config: Two-factor configuration
        """
        self.config = config or TwoFactorConfig()
        self.secrets: Dict[str, TwoFactorSecret] = {}
        self.attempts: Dict[str, int] = {}
        self.lockouts: Dict[str, float] = {}
        self.secret_id_counter = 0
        self._next_secret_id()
    
    def _next_secret_id(self) -> str:
        """
        Generate next secret ID.
        
        Returns:
            str: Secret ID
        """
        self.secret_id_counter += 1
        return f"secret_{self.secret_id_counter}"
    
    def generate_secret(self, user_id: str, method: TwoFactorMethod = None) -> TwoFactorResult:
        """
        Generate a two-factor secret.
        
        Args:
            user_id: User ID
            method: Two-factor method
            
        Returns:
            TwoFactorResult: Generation result
        """
        result = TwoFactorResult(success=False)
        
        try:
            if not self.config.enable_2fa:
                result.errors.append("2FA disabled")
                return result
            
            method = method or self.config.default_method
            
            # Generate secret
            secret = secrets.token_hex(16)
            
            secret_obj = TwoFactorSecret(
                secret_id=self._next_secret_id(),
                user_id=user_id,
                secret=secret,
                method=method,
                status=TwoFactorStatus.ENABLED,
                created_at=str(time.time())
            )
            
            self.secrets[secret_obj.secret_id] = secret_obj
            
            result.success = True
            result.secret = secret_obj
            result.message = "Secret generated successfully"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def generate_totp(self, secret_id: str) -> TwoFactorResult:
        """
        Generate TOTP code.
        
        Args:
            secret_id: Secret ID
            
        Returns:
            TwoFactorResult: TOTP generation result
        """
        result = TwoFactorResult(success=False)
        
        try:
            secret_obj = self.secrets.get(secret_id)
            
            if not secret_obj:
                result.errors.append("Secret not found")
                return result
            
            # Generate TOTP based on time
            timestamp = int(time.time() // self.config.totp_expiry_seconds)
            totp_input = f"{secret_obj.secret}{timestamp}"
            totp_code = hashlib.sha256(totp_input.encode()).hexdigest()[:6].upper()
            
            result.success = True
            result.code = totp_code
            result.message = "TOTP generated"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def verify_code(self, secret_id: str, code: str) -> TwoFactorResult:
        """
        Verify two-factor code.
        
        Args:
            secret_id: Secret ID
            code: Code to verify
            
        Returns:
            TwoFactorResult: Verification result
        """
        result = TwoFactorResult(success=False)
        
        try:
            # Check lockout
            if secret_id in self.lockouts:
                if time.time() < self.lockouts[secret_id]:
                    result.errors.append("Account locked due to too many attempts")
                    return result
                else:
                    del self.lockouts[secret_id]
                    self.attempts[secret_id] = 0
            
            secret_obj = self.secrets.get(secret_id)
            
            if not secret_obj:
                result.errors.append("Secret not found")
                return result
            
            # Generate current TOTP
            totp_result = self.generate_totp(secret_id)
            expected_code = totp_result.code
            
            # Verify code
            if code == expected_code:
                result.success = True
                result.is_valid = True
                result.message = "Code verified successfully"
                
                # Reset attempts
                if secret_id in self.attempts:
                    del self.attempts[secret_id]
                
                # Update secret status
                secret_obj.status = TwoFactorStatus.VERIFIED
                secret_obj.verified_at = str(time.time())
            else:
                # Increment attempts
                self.attempts[secret_id] = self.attempts.get(secret_id, 0) + 1
                
                # Check max attempts
                if self.attempts[secret_id] >= self.config.max_attempts:
                    self.lockouts[secret_id] = time.time() + self.config.lockout_duration_seconds
                    result.errors.append("Too many failed attempts. Account locked.")
                else:
                    result.errors.append(f"Invalid code. Attempts remaining: {self.config.max_attempts - self.attempts[secret_id]}")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def generate_backup_codes(self, secret_id: str) -> TwoFactorResult:
        """
        Generate backup codes.
        
        Args:
            secret_id: Secret ID
            
        Returns:
            TwoFactorResult: Backup codes generation result
        """
        result = TwoFactorResult(success=False)
        
        try:
            secret_obj = self.secrets.get(secret_id)
            
            if not secret_obj:
                result.errors.append("Secret not found")
                return result
            
            # Generate backup codes
            backup_codes = [secrets.token_hex(4).upper() for _ in range(self.config.backup_codes_count)]
            
            result.success = True
            result.code = ",".join(backup_codes)
            result.message = f"Generated {self.config.backup_codes_count} backup codes"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def disable_2fa(self, secret_id: str) -> TwoFactorResult:
        """
        Disable two-factor authentication.
        
        Args:
            secret_id: Secret ID
            
        Returns:
            TwoFactorResult: Disable result
        """
        result = TwoFactorResult(success=False)
        
        try:
            secret_obj = self.secrets.get(secret_id)
            
            if not secret_obj:
                result.errors.append("Secret not found")
                return result
            
            secret_obj.status = TwoFactorStatus.DISABLED
            
            result.success = True
            result.secret = secret_obj
            result.message = "2FA disabled"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_secret(self, secret_id: str) -> Optional[TwoFactorSecret]:
        """
        Get secret by ID.
        
        Args:
            secret_id: Secret ID
            
        Returns:
            Optional[TwoFactorSecret]: Secret
        """
        return self.secrets.get(secret_id)
    
    def get_user_secrets(self, user_id: str) -> List[TwoFactorSecret]:
        """
        Get secrets for a user.
        
        Args:
            user_id: User ID
            
        Returns:
            List[TwoFactorSecret]: User secrets
        """
        return [s for s in self.secrets.values() if s.user_id == user_id]
    
    def update_config(self, config: TwoFactorConfig) -> TwoFactorResult:
        """
        Update two-factor configuration.
        
        Args:
            config: New configuration
            
        Returns:
            TwoFactorResult: Update result
        """
        result = TwoFactorResult(success=True)
        
        try:
            self.config = config
            result.message = "Config updated"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def get_config(self) -> TwoFactorConfig:
        """
        Get two-factor configuration.
        
        Returns:
            TwoFactorConfig: Configuration
        """
        return self.config


if __name__ == "__main__":
    # Basit test
    config = TwoFactorConfig()
    auth = TwoFactorAuth(config)
    
    # Secret oluştur
    result = auth.generate_secret("user_1")
    
    print(f"Secret generated: {result.message}")
    secret_id = result.secret.secret_id
    
    # TOTP oluştur
    totp_result = auth.generate_totp(secret_id)
    
    print(f"TOTP: {totp_result.code}")
    
    # Verify et
    verify_result = auth.verify_code(secret_id, totp_result.code)
    
    print(f"Verified: {verify_result.message}")
