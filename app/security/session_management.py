"""
MuhammedAI Local Developer - Session Management
Session management system for security.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
import secrets


class SessionStatus(Enum):
    """Session status."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    EXPIRED = "expired"
    REVOKED = "revoked"
    TERMINATED = "terminated"


class SessionType(Enum):
    """Session type."""
    WEB = "web"
    API = "api"
    DESKTOP = "desktop"
    MOBILE = "mobile"
    CUSTOM = "custom"


@dataclass
class SessionData:
    """Session data."""
    key: str
    value: Any
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


@dataclass
class Session:
    """Session."""
    session_id: str
    user_id: str
    session_type: SessionType
    token: str
    status: SessionStatus = SessionStatus.ACTIVE
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    device_info: Optional[str] = None
    location: Optional[str] = None
    data: Dict[str, SessionData] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    last_activity: datetime = field(default_factory=datetime.now)
    expires_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SessionManagementConfig:
    """Session management configuration."""
    enable_session_creation: bool = True
    enable_session_deletion: bool = True
    enable_session_update: bool = True
    enable_persistence: bool = True
    enable_encryption: bool = False
    session_timeout: int = 1800  # seconds
    max_concurrent_sessions: int = 5
    enable_auto_refresh: bool = True
    auto_refresh_threshold: int = 300  # seconds
    enable_ip_binding: bool = False
    enable_device_binding: bool = False


@dataclass
class SessionManagementResult:
    """Session management result."""
    success: bool
    message: Optional[str] = None
    session: Optional[Session] = None
    sessions: List[Session] = field(default_factory=list)
    token: Optional[str] = None
    errors: List[str] = field(default_factory=list)


class SessionManager:
    """
    Session manager.
    
    Özellikler:
    - Session creation
    - Session deletion
    - Session update
    - Session validation
    - Session timeout
    - Session persistence
    - Concurrent session control
    - Auto refresh
    - IP binding
    - Device binding
    """
    
    def __init__(self, config: Optional[SessionManagementConfig] = None):
        """
        Initialize session manager.
        
        Args:
            config: Session management configuration
        """
        self.config = config or SessionManagementConfig()
        self.sessions: Dict[str, Session] = {}
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
    
    def _generate_token(self) -> str:
        """
        Generate secure token.
        
        Returns:
            str: Token
        """
        return secrets.token_hex(32)
    
    def create_session(self, user_id: str, session_type: SessionType, ip_address: Optional[str] = None, user_agent: Optional[str] = None) -> SessionManagementResult:
        """
        Create a new session.
        
        Args:
            user_id: User ID
            session_type: Session type
            ip_address: IP address
            user_agent: User agent
            
        Returns:
            SessionManagementResult: Create result
        """
        result = SessionManagementResult(success=False)
        
        try:
            if not self.config.enable_session_creation:
                result.errors.append("Session creation is disabled")
                return result
            
            # Check concurrent sessions limit
            user_sessions = self.get_user_sessions(user_id)
            active_sessions = [s for s in user_sessions if s.status == SessionStatus.ACTIVE]
            
            if len(active_sessions) >= self.config.max_concurrent_sessions:
                # Terminate oldest session
                oldest = min(active_sessions, key=lambda s: s.created_at)
                self.terminate_session(oldest.session_id)
            
            session_id = self._next_session_id()
            token = self._generate_token()
            
            expires_at = datetime.now() + timedelta(seconds=self.config.session_timeout)
            
            session = Session(
                session_id=session_id,
                user_id=user_id,
                session_type=session_type,
                token=token,
                ip_address=ip_address,
                user_agent=user_agent,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                last_activity=datetime.now(),
                expires_at=expires_at
            )
            
            self.sessions[session_id] = session
            
            result.success = True
            result.session = session
            result.token = token
            result.sessions = self.get_all_sessions()
            result.message = f"Session created for user '{user_id}'"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def delete_session(self, session_id: str) -> SessionManagementResult:
        """
        Delete a session.
        
        Args:
            session_id: Session ID
            
        Returns:
            SessionManagementResult: Delete result
        """
        result = SessionManagementResult(success=False)
        
        try:
            if not self.config.enable_session_deletion:
                result.errors.append("Session deletion is disabled")
                return result
            
            if session_id in self.sessions:
                del self.sessions[session_id]
                result.success = True
                result.sessions = self.get_all_sessions()
                result.message = f"Session '{session_id}' deleted"
            else:
                result.errors.append("Session not found")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def update_session(self, session_id: str, **kwargs) -> SessionManagementResult:
        """
        Update session information.
        
        Args:
            session_id: Session ID
            **kwargs: Fields to update
            
        Returns:
            SessionManagementResult: Update result
        """
        result = SessionManagementResult(success=False)
        
        try:
            if not self.config.enable_session_update:
                result.errors.append("Session update is disabled")
                return result
            
            session = self.sessions.get(session_id)
            if not session:
                result.errors.append("Session not found")
                return result
            
            # Update fields
            for key, value in kwargs.items():
                if hasattr(session, key):
                    setattr(session, key, value)
            
            session.updated_at = datetime.now()
            session.last_activity = datetime.now()
            
            result.success = True
            result.session = session
            result.message = f"Session '{session_id}' updated"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_session(self, session_id: str) -> Optional[Session]:
        """
        Get session by ID.
        
        Args:
            session_id: Session ID
            
        Returns:
            Optional[Session]: Session
        """
        return self.sessions.get(session_id)
    
    def get_session_by_token(self, token: str) -> Optional[Session]:
        """
        Get session by token.
        
        Args:
            token: Token
            
        Returns:
            Optional[Session]: Session
        """
        for session in self.sessions.values():
            if session.token == token:
                return session
        return None
    
    def get_all_sessions(self) -> List[Session]:
        """
        Get all sessions.
        
        Returns:
            List[Session]: All sessions
        """
        return list(self.sessions.values())
    
    def get_user_sessions(self, user_id: str) -> List[Session]:
        """
        Get sessions for a user.
        
        Args:
            user_id: User ID
            
        Returns:
            List[Session]: User sessions
        """
        return [s for s in self.sessions.values() if s.user_id == user_id]
    
    def validate_session(self, session_id: str) -> SessionManagementResult:
        """
        Validate session.
        
        Args:
            session_id: Session ID
            
        Returns:
            SessionManagementResult: Validation result
        """
        result = SessionManagementResult(success=False)
        
        try:
            session = self.sessions.get(session_id)
            if not session:
                result.errors.append("Session not found")
                return result
            
            # Check status
            if session.status != SessionStatus.ACTIVE:
                result.errors.append(f"Session is {session.status.value}")
                return result
            
            # Check expiration
            if session.expires_at and datetime.now() > session.expires_at:
                session.status = SessionStatus.EXPIRED
                result.errors.append("Session expired")
                return result
            
            # Check IP binding
            if self.config.enable_ip_binding and session.ip_address:
                # In real implementation, compare with current IP
                pass
            
            # Check device binding
            if self.config.enable_device_binding and session.device_info:
                # In real implementation, compare with current device
                pass
            
            result.success = True
            result.session = session
            result.message = "Session valid"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def refresh_session(self, session_id: str) -> SessionManagementResult:
        """
        Refresh session (extend expiration).
        
        Args:
            session_id: Session ID
            
        Returns:
            SessionManagementResult: Refresh result
        """
        result = SessionManagementResult(success=False)
        
        try:
            session = self.sessions.get(session_id)
            if not session:
                result.errors.append("Session not found")
                return result
            
            # Extend expiration
            session.expires_at = datetime.now() + timedelta(seconds=self.config.session_timeout)
            session.last_activity = datetime.now()
            session.updated_at = datetime.now()
            
            result.success = True
            result.session = session
            result.message = f"Session '{session_id}' refreshed"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def terminate_session(self, session_id: str) -> SessionManagementResult:
        """
        Terminate session.
        
        Args:
            session_id: Session ID
            
        Returns:
            SessionManagementResult: Terminate result
        """
        result = SessionManagementResult(success=False)
        
        try:
            session = self.sessions.get(session_id)
            if not session:
                result.errors.append("Session not found")
                return result
            
            session.status = SessionStatus.TERMINATED
            session.updated_at = datetime.now()
            
            result.success = True
            result.session = session
            result.message = f"Session '{session_id}' terminated"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def revoke_session(self, session_id: str) -> SessionManagementResult:
        """
        Revoke session.
        
        Args:
            session_id: Session ID
            
        Returns:
            SessionManagementResult: Revoke result
        """
        result = SessionManagementResult(success=False)
        
        try:
            session = self.sessions.get(session_id)
            if not session:
                result.errors.append("Session not found")
                return result
            
            session.status = SessionStatus.REVOKED
            session.updated_at = datetime.now()
            
            result.success = True
            result.session = session
            result.message = f"Session '{session_id}' revoked"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def set_session_data(self, session_id: str, key: str, value: Any) -> SessionManagementResult:
        """
        Set session data.
        
        Args:
            session_id: Session ID
            key: Data key
            value: Data value
            
        Returns:
            SessionManagementResult: Set result
        """
        result = SessionManagementResult(success=False)
        
        try:
            session = self.sessions.get(session_id)
            if not session:
                result.errors.append("Session not found")
                return result
            
            session_data = SessionData(key=key, value=value)
            session.data[key] = session_data
            session.updated_at = datetime.now()
            
            result.success = True
            result.session = session
            result.message = f"Session data set for '{key}'"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_session_data(self, session_id: str, key: str) -> Optional[Any]:
        """
        Get session data.
        
        Args:
            session_id: Session ID
            key: Data key
            
        Returns:
            Optional[Any]: Data value
        """
        session = self.sessions.get(session_id)
        if session and key in session.data:
            return session.data[key].value
        return None
    
    def remove_session_data(self, session_id: str, key: str) -> SessionManagementResult:
        """
        Remove session data.
        
        Args:
            session_id: Session ID
            key: Data key
            
        Returns:
            SessionManagementResult: Remove result
        """
        result = SessionManagementResult(success=False)
        
        try:
            session = self.sessions.get(session_id)
            if not session:
                result.errors.append("Session not found")
                return result
            
            if key in session.data:
                del session.data[key]
                session.updated_at = datetime.now()
                result.success = True
                result.message = f"Session data removed for '{key}'"
            else:
                result.errors.append("Data key not found")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def cleanup_expired_sessions(self) -> SessionManagementResult:
        """
        Cleanup expired sessions.
        
        Returns:
            SessionManagementResult: Cleanup result
        """
        result = SessionManagementResult(success=True)
        
        try:
            now = datetime.now()
            expired_count = 0
            
            for session in self.sessions.values():
                if session.expires_at and now > session.expires_at:
                    session.status = SessionStatus.EXPIRED
                    expired_count += 1
            
            result.message = f"Cleaned up {expired_count} expired sessions"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def update_config(self, config: SessionManagementConfig) -> SessionManagementResult:
        """
        Update session management configuration.
        
        Args:
            config: New configuration
            
        Returns:
            SessionManagementResult: Update result
        """
        result = SessionManagementResult(success=True)
        
        try:
            self.config = config
            result.message = "Config updated"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def get_config(self) -> SessionManagementConfig:
        """
        Get session management configuration.
        
        Returns:
            SessionManagementConfig: Configuration
        """
        return self.config


if __name__ == "__main__":
    # Basit test
    config = SessionManagementConfig()
    manager = SessionManager(config)
    
    # Session oluştur
    result = manager.create_session("user_1", SessionType.WEB)
    
    print(f"Session created: {result.message}")
    
    # Session validate et
    validation = manager.validate_session(result.session.session_id)
    
    print(f"Session valid: {validation.success}")
