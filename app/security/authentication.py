"""
MuhammedAI Local Developer - Authentication
Authentication system for security.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
import hashlib
import secrets
import json


class AuthMethod(Enum):
    """Authentication method."""
    PASSWORD = "password"
    TOKEN = "token"
    OAUTH = "oauth"
    SSO = "sso"
    BIOMETRIC = "biometric"
    TWO_FACTOR = "two_factor"
    CUSTOM = "custom"


class AuthStatus(Enum):
    """Authentication status."""
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"
    EXPIRED = "expired"
    REVOKED = "revoked"
    LOCKED = "locked"


class TokenType(Enum):
    """Token type."""
    ACCESS = "access"
    REFRESH = "refresh"
    RESET = "reset"
    VERIFICATION = "verification"
    API_KEY = "api_key"
    CUSTOM = "custom"


@dataclass
class UserCredentials:
    """User credentials."""
    user_id: str
    username: str
    password_hash: str
    email: Optional[str] = None
    phone: Optional[str] = None
    is_active: bool = True
    is_verified: bool = False
    failed_attempts: int = 0
    last_login: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AuthSession:
    """Authentication session."""
    session_id: str
    user_id: str
    auth_method: AuthMethod
    token: str
    refresh_token: Optional[str] = None
    expires_at: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.now)
    last_activity: datetime = field(default_factory=datetime.now)
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    is_active: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AuthConfig:
    """Authentication configuration."""
    password_min_length: int = 8
    password_require_uppercase: bool = True
    password_require_lowercase: bool = True
    password_require_number: bool = True
    password_require_special: bool = True
    max_failed_attempts: int = 5
    lockout_duration: int = 3600  # seconds
    token_expiry: int = 3600  # seconds
    refresh_token_expiry: int = 86400  # seconds
    enable_two_factor: bool = False
    enable_oauth: bool = False
    enable_sso: bool = False
    enable_biometric: bool = False
    session_timeout: int = 1800  # seconds
    max_concurrent_sessions: int = 5


@dataclass
class AuthResult:
    """Authentication result."""
    success: bool
    status: AuthStatus
    message: Optional[str] = None
    session: Optional[AuthSession] = None
    token: Optional[str] = None
    errors: List[str] = field(default_factory=list)


class AuthenticationManager:
    """
    Authentication manager.
    
    Özellikler:
    - User authentication
    - Password hashing
    - Token generation
    - Session creation
    - Multi-factor authentication
    - OAuth integration
    - SSO support
    - Biometric authentication
    - Password validation
    - Account lockout
    - Session management
    - Token refresh
    """
    
    def __init__(self, config: Optional[AuthConfig] = None):
        """
        Initialize authentication manager.
        
        Args:
            config: Authentication configuration
        """
        self.config = config or AuthConfig()
        self.users: Dict[str, UserCredentials] = {}
        self.sessions: Dict[str, AuthSession] = {}
        self.session_id_counter = 0
        self._next_session_id()
    
    def _next_session_id(self) -> str:
        """
        Generate next session ID.
        
        Returns:
            str: Session ID
        """
        self.session_id_counter += 1
        return f"session_{self.session_id_counter}"
    
    def hash_password(self, password: str) -> str:
        """
        Hash password using SHA-256.
        
        Args:
            password: Plain text password
            
        Returns:
            str: Hashed password
        """
        return hashlib.sha256(password.encode()).hexdigest()
    
    def validate_password(self, password: str) -> bool:
        """
        Validate password against policy.
        
        Args:
            password: Password to validate
            
        Returns:
            bool: Valid or not
        """
        if len(password) < self.config.password_min_length:
            return False
        
        if self.config.password_require_uppercase and not any(c.isupper() for c in password):
            return False
        
        if self.config.password_require_lowercase and not any(c.islower() for c in password):
            return False
        
        if self.config.password_require_number and not any(c.isdigit() for c in password):
            return False
        
        if self.config.password_require_special and not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            return False
        
        return True
    
    def register_user(self, username: str, password: str, email: Optional[str] = None) -> AuthResult:
        """
        Register a new user.
        
        Args:
            username: Username
            password: Password
            email: Email address
            
        Returns:
            AuthResult: Registration result
        """
        result = AuthResult(success=False, status=AuthStatus.FAILED)
        
        try:
            # Check if username exists
            if any(u.username == username for u in self.users.values()):
                result.errors.append("Username already exists")
                return result
            
            # Validate password
            if not self.validate_password(password):
                result.errors.append("Password does not meet requirements")
                return result
            
            # Create user
            user_id = f"user_{len(self.users) + 1}"
            user = UserCredentials(
                user_id=user_id,
                username=username,
                password_hash=self.hash_password(password),
                email=email
            )
            
            self.users[user_id] = user
            result.success = True
            result.status = AuthStatus.SUCCESS
            result.message = f"User '{username}' registered successfully"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def authenticate(self, username: str, password: str, auth_method: AuthMethod = AuthMethod.PASSWORD) -> AuthResult:
        """
        Authenticate user.
        
        Args:
            username: Username
            password: Password
            auth_method: Authentication method
            
        Returns:
            AuthResult: Authentication result
        """
        result = AuthResult(success=False, status=AuthStatus.FAILED)
        
        try:
            # Find user
            user = None
            for u in self.users.values():
                if u.username == username:
                    user = u
                    break
            
            if not user:
                result.errors.append("User not found")
                return result
            
            # Check if locked
            if user.failed_attempts >= self.config.max_failed_attempts:
                result.status = AuthStatus.LOCKED
                result.errors.append("Account locked due to too many failed attempts")
                return result
            
            # Check if active
            if not user.is_active:
                result.errors.append("Account is inactive")
                return result
            
            # Verify password
            if user.password_hash != self.hash_password(password):
                user.failed_attempts += 1
                result.errors.append(f"Invalid password. Attempts remaining: {self.config.max_failed_attempts - user.failed_attempts}")
                return result
            
            # Reset failed attempts on success
            user.failed_attempts = 0
            user.last_login = datetime.now()
            
            # Create session
            session = self._create_session(user.user_id, auth_method)
            
            result.success = True
            result.status = AuthStatus.SUCCESS
            result.session = session
            result.token = session.token
            result.message = "Authentication successful"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def _create_session(self, user_id: str, auth_method: AuthMethod) -> AuthSession:
        """
        Create authentication session.
        
        Args:
            user_id: User ID
            auth_method: Authentication method
            
        Returns:
            AuthSession: Session
        """
        session_id = self._next_session_id()
        token = secrets.token_hex(32)
        refresh_token = secrets.token_hex(32)
        
        expires_at = datetime.now() + timedelta(seconds=self.config.token_expiry)
        refresh_expires_at = datetime.now() + timedelta(seconds=self.config.refresh_token_expiry)
        
        session = AuthSession(
            session_id=session_id,
            user_id=user_id,
            auth_method=auth_method,
            token=token,
            refresh_token=refresh_token,
            expires_at=expires_at,
            created_at=datetime.now(),
            last_activity=datetime.now()
        )
        
        self.sessions[session_id] = session
        
        return session
    
    def verify_token(self, token: str) -> AuthResult:
        """
        Verify authentication token.
        
        Args:
            token: Token to verify
            
        Returns:
            AuthResult: Verification result
        """
        result = AuthResult(success=False, status=AuthStatus.FAILED)
        
        try:
            # Find session by token
            session = None
            for s in self.sessions.values():
                if s.token == token:
                    session = s
                    break
            
            if not session:
                result.errors.append("Invalid token")
                return result
            
            # Check if active
            if not session.is_active:
                result.status = AuthStatus.REVOKED
                result.errors.append("Token revoked")
                return result
            
            # Check if expired
            if session.expires_at and datetime.now() > session.expires_at:
                result.status = AuthStatus.EXPIRED
                result.errors.append("Token expired")
                return result
            
            # Update last activity
            session.last_activity = datetime.now()
            
            result.success = True
            result.status = AuthStatus.SUCCESS
            result.session = session
            result.message = "Token valid"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def refresh_token(self, refresh_token: str) -> AuthResult:
        """
        Refresh authentication token.
        
        Args:
            refresh_token: Refresh token
            
        Returns:
            AuthResult: Refresh result
        """
        result = AuthResult(success=False, status=AuthStatus.FAILED)
        
        try:
            # Find session by refresh token
            session = None
            for s in self.sessions.values():
                if s.refresh_token == refresh_token:
                    session = s
                    break
            
            if not session:
                result.errors.append("Invalid refresh token")
                return result
            
            # Check if expired
            refresh_expires_at = session.created_at + timedelta(seconds=self.config.refresh_token_expiry)
            if datetime.now() > refresh_expires_at:
                result.status = AuthStatus.EXPIRED
                result.errors.append("Refresh token expired")
                return result
            
            # Generate new tokens
            session.token = secrets.token_hex(32)
            session.refresh_token = secrets.token_hex(32)
            session.expires_at = datetime.now() + timedelta(seconds=self.config.token_expiry)
            session.last_activity = datetime.now()
            
            result.success = True
            result.status = AuthStatus.SUCCESS
            result.session = session
            result.token = session.token
            result.message = "Token refreshed successfully"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def logout(self, session_id: str) -> AuthResult:
        """
        Logout user.
        
        Args:
            session_id: Session ID
            
        Returns:
            AuthResult: Logout result
        """
        result = AuthResult(success=False, status=AuthStatus.FAILED)
        
        try:
            if session_id in self.sessions:
                self.sessions[session_id].is_active = False
                result.success = True
                result.status = AuthStatus.SUCCESS
                result.message = "Logout successful"
            else:
                result.errors.append("Session not found")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def revoke_token(self, token: str) -> AuthResult:
        """
        Revoke authentication token.
        
        Args:
            token: Token to revoke
            
        Returns:
            AuthResult: Revoke result
        """
        result = AuthResult(success=False, status=AuthStatus.FAILED)
        
        try:
            for session in self.sessions.values():
                if session.token == token:
                    session.is_active = False
                    result.success = True
                    result.status = AuthStatus.REVOKED
                    result.message = "Token revoked"
                    return result
            
            result.errors.append("Token not found")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def change_password(self, user_id: str, old_password: str, new_password: str) -> AuthResult:
        """
        Change user password.
        
        Args:
            user_id: User ID
            old_password: Old password
            new_password: New password
            
        Returns:
            AuthResult: Change result
        """
        result = AuthResult(success=False, status=AuthStatus.FAILED)
        
        try:
            user = self.users.get(user_id)
            if not user:
                result.errors.append("User not found")
                return result
            
            # Verify old password
            if user.password_hash != self.hash_password(old_password):
                result.errors.append("Invalid old password")
                return result
            
            # Validate new password
            if not self.validate_password(new_password):
                result.errors.append("New password does not meet requirements")
                return result
            
            # Update password
            user.password_hash = self.hash_password(new_password)
            
            result.success = True
            result.status = AuthStatus.SUCCESS
            result.message = "Password changed successfully"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_user(self, user_id: str) -> Optional[UserCredentials]:
        """
        Get user by ID.
        
        Args:
            user_id: User ID
            
        Returns:
            Optional[UserCredentials]: User
        """
        return self.users.get(user_id)
    
    def get_all_users(self) -> List[UserCredentials]:
        """
        Get all users.
        
        Returns:
            List[UserCredentials]: All users
        """
        return list(self.users.values())
    
    def get_session(self, session_id: str) -> Optional[AuthSession]:
        """
        Get session by ID.
        
        Args:
            session_id: Session ID
            
        Returns:
            Optional[AuthSession]: Session
        """
        return self.sessions.get(session_id)
    
    def get_all_sessions(self) -> List[AuthSession]:
        """
        Get all sessions.
        
        Returns:
            List[AuthSession]: All sessions
        """
        return list(self.sessions.values())
    
    def update_config(self, config: AuthConfig) -> AuthResult:
        """
        Update authentication configuration.
        
        Args:
            config: New configuration
            
        Returns:
            AuthResult: Update result
        """
        result = AuthResult(success=True, status=AuthStatus.SUCCESS)
        
        try:
            self.config = config
            result.message = "Config updated"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
            result.status = AuthStatus.FAILED
        
        return result
    
    def get_config(self) -> AuthConfig:
        """
        Get authentication configuration.
        
        Returns:
            AuthConfig: Configuration
        """
        return self.config


if __name__ == "__main__":
    # Basit test
    config = AuthConfig()
    manager = AuthenticationManager(config)
    
    # User kayıt
    result = manager.register_user("testuser", "TestPass123!", "test@example.com")
    
    print(f"Registration: {result.message}")
    
    # Authentication
    result = manager.authenticate("testuser", "TestPass123!")
    
    print(f"Authentication: {result.message}")
    
    if result.success:
        print(f"Token: {result.token}")
