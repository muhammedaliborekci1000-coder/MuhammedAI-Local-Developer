"""
MuhammedAI Local Developer - Audit Logging
Audit logging system for security.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
import json


class AuditLogLevel(Enum):
    """Audit log level."""
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class AuditLogCategory(Enum):
    """Audit log category."""
    AUTHENTICATION = "authentication"
    AUTHORIZATION = "authorization"
    USER_MANAGEMENT = "user_management"
    ROLE_MANAGEMENT = "role_management"
    SESSION_MANAGEMENT = "session_management"
    API_KEY_MANAGEMENT = "api_key_management"
    ENCRYPTION = "encryption"
    DATA_ACCESS = "data_access"
    SYSTEM = "system"
    CUSTOM = "custom"


class AuditLogAction(Enum):
    """Audit log action."""
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    LOGIN = "login"
    LOGOUT = "logout"
    GRANT = "grant"
    REVOKE = "revoke"
    EXPORT = "export"
    IMPORT = "import"
    CUSTOM = "custom"


@dataclass
class AuditLogEntry:
    """Audit log entry."""
    log_id: str
    user_id: Optional[str]
    action: AuditLogAction
    category: AuditLogCategory
    level: AuditLogLevel
    message: str
    resource_type: Optional[str] = None
    resource_id: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)
    success: bool = True
    details: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AuditLogConfig:
    """Audit log configuration."""
    enable_logging: bool = True
    enable_persistence: bool = True
    log_level: AuditLogLevel = AuditLogLevel.INFO
    enable_ip_logging: bool = True
    enable_user_agent_logging: bool = True
    enable_details_logging: bool = True
    max_log_entries: int = 10000
    retention_days: int = 90
    enable_log_rotation: bool = True
    enable_compression: bool = False


@dataclass
class AuditLogResult:
    """Audit log result."""
    success: bool
    message: Optional[str] = None
    log_entry: Optional[AuditLogEntry] = None
    log_entries: List[AuditLogEntry] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)


class AuditLogger:
    """
    Audit logger.
    
    Özellikler:
    - Log entry creation
    - Log filtering
    - Log searching
    - Log export
    - Log retention
    - Log rotation
    - IP logging
    - User agent logging
    """
    
    def __init__(self, config: Optional[AuditLogConfig] = None):
        """
        Initialize audit logger.
        
        Args:
            config: Audit log configuration
        """
        self.config = config or AuditLogConfig()
        self.logs: List[AuditLogEntry] = []
        self.log_id_counter = 0
        self._next_log_id()
    
    def _next_log_id(self) -> str:
        """
        Generate next log ID.
        
        Returns:
            str: Log ID
        """
        self.log_id_counter += 1
        return f"log_{self.log_id_counter}"
    
    def log(self, user_id: Optional[str], action: AuditLogAction, category: AuditLogCategory, message: str, level: Optional[AuditLogLevel] = None, resource_type: Optional[str] = None, resource_id: Optional[str] = None, ip_address: Optional[str] = None, user_agent: Optional[str] = None, success: bool = True, details: Optional[Dict[str, Any]] = None) -> AuditLogResult:
        """
        Create audit log entry.
        
        Args:
            user_id: User ID
            action: Action
            category: Category
            message: Log message
            level: Log level
            resource_type: Resource type
            resource_id: Resource ID
            ip_address: IP address
            user_agent: User agent
            success: Success status
            details: Additional details
            
        Returns:
            AuditLogResult: Log result
        """
        result = AuditLogResult(success=False)
        
        try:
            if not self.config.enable_logging:
                result.errors.append("Logging is disabled")
                return result
            
            # Check log level
            log_level = level or self.config.log_level
            if not self._should_log(log_level):
                result.message = "Log level too low"
                return result
            
            # Create log entry
            log_entry = AuditLogEntry(
                log_id=self._next_log_id(),
                user_id=user_id,
                action=action,
                category=category,
                level=log_level,
                message=message,
                resource_type=resource_type,
                resource_id=resource_id,
                ip_address=ip_address if self.config.enable_ip_logging else None,
                user_agent=user_agent if self.config.enable_user_agent_logging else None,
                success=success,
                details=details if self.config.enable_details_logging else {}
            )
            
            self.logs.append(log_entry)
            
            # Cleanup old logs
            self._cleanup_old_logs()
            
            result.success = True
            result.log_entry = log_entry
            result.message = "Log entry created"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def _should_log(self, level: AuditLogLevel) -> bool:
        """
        Check if should log based on level.
        
        Args:
            level: Log level
            
        Returns:
            bool: Should log
        """
        level_priority = {
            AuditLogLevel.DEBUG: 0,
            AuditLogLevel.INFO: 1,
            AuditLogLevel.WARNING: 2,
            AuditLogLevel.ERROR: 3,
            AuditLogLevel.CRITICAL: 4
        }
        
        return level_priority[level] >= level_priority[self.config.log_level]
    
    def get_log(self, log_id: str) -> Optional[AuditLogEntry]:
        """
        Get log entry by ID.
        
        Args:
            log_id: Log ID
            
        Returns:
            Optional[AuditLogEntry]: Log entry
        """
        for log in self.logs:
            if log.log_id == log_id:
                return log
        return None
    
    def get_all_logs(self) -> List[AuditLogEntry]:
        """
        Get all log entries.
        
        Returns:
            List[AuditLogEntry]: All log entries
        """
        return list(self.logs)
    
    def get_user_logs(self, user_id: str) -> List[AuditLogEntry]:
        """
        Get logs for a user.
        
        Args:
            user_id: User ID
            
        Returns:
            List[AuditLogEntry]: User log entries
        """
        return [log for log in self.logs if log.user_id == user_id]
    
    def get_logs_by_category(self, category: AuditLogCategory) -> List[AuditLogEntry]:
        """
        Get logs by category.
        
        Args:
            category: Category
            
        Returns:
            List[AuditLogEntry]: Category log entries
        """
        return [log for log in self.logs if log.category == category]
    
    def get_logs_by_action(self, action: AuditLogAction) -> List[AuditLogEntry]:
        """
        Get logs by action.
        
        Args:
            action: Action
            
        Returns:
            List[AuditLogEntry]: Action log entries
        """
        return [log for log in self.logs if log.action == action]
    
    def get_logs_by_level(self, level: AuditLogLevel) -> List[AuditLogEntry]:
        """
        Get logs by level.
        
        Args:
            level: Level
            
        Returns:
            List[AuditLogEntry]: Level log entries
        """
        return [log for log in self.logs if log.level == level]
    
    def search_logs(self, query: str) -> List[AuditLogEntry]:
        """
        Search logs by message.
        
        Args:
            query: Search query
            
        Returns:
            List[AuditLogEntry]: Matching log entries
        """
        query_lower = query.lower()
        return [log for log in self.logs if query_lower in log.message.lower()]
    
    def filter_logs(self, user_id: Optional[str] = None, category: Optional[AuditLogCategory] = None, action: Optional[AuditLogAction] = None, level: Optional[AuditLogLevel] = None, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[AuditLogEntry]:
        """
        Filter logs by multiple criteria.
        
        Args:
            user_id: User ID
            category: Category
            action: Action
            level: Level
            start_date: Start date
            end_date: End date
            
        Returns:
            List[AuditLogEntry]: Filtered log entries
        """
        filtered = self.logs
        
        if user_id:
            filtered = [log for log in filtered if log.user_id == user_id]
        
        if category:
            filtered = [log for log in filtered if log.category == category]
        
        if action:
            filtered = [log for log in filtered if log.action == action]
        
        if level:
            filtered = [log for log in filtered if log.level == level]
        
        if start_date:
            filtered = [log for log in filtered if log.timestamp >= start_date]
        
        if end_date:
            filtered = [log for log in filtered if log.timestamp <= end_date]
        
        return filtered
    
    def export_logs(self, format: str = "json") -> AuditLogResult:
        """
        Export logs.
        
        Args:
            format: Export format (json, csv)
            
        Returns:
            AuditLogResult: Export result
        """
        result = AuditLogResult(success=False)
        
        try:
            if format == "json":
                log_data = []
                for log in self.logs:
                    log_dict = {
                        "log_id": log.log_id,
                        "user_id": log.user_id,
                        "action": log.action.value,
                        "category": log.category.value,
                        "level": log.level.value,
                        "message": log.message,
                        "resource_type": log.resource_type,
                        "resource_id": log.resource_id,
                        "ip_address": log.ip_address,
                        "user_agent": log.user_agent,
                        "timestamp": log.timestamp.isoformat(),
                        "success": log.success,
                        "details": log.details
                    }
                    log_data.append(log_dict)
                
                result.success = True
                result.message = f"Exported {len(log_data)} log entries as JSON"
                result.log_entries = self.logs
            else:
                result.errors.append("Unsupported export format")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def _cleanup_old_logs(self):
        """Cleanup old logs based on retention policy."""
        if self.config.retention_days <= 0:
            return
        
        if len(self.logs) > self.config.max_log_entries:
            # Remove oldest logs
            excess = len(self.logs) - self.config.max_log_entries
            self.logs = self.logs[excess:]
        
        # Remove logs older than retention period
        cutoff_date = datetime.now() - timedelta(days=self.config.retention_days)
        self.logs = [log for log in self.logs if log.timestamp > cutoff_date]
    
    def clear_logs(self) -> AuditLogResult:
        """
        Clear all logs.
        
        Returns:
            AuditLogResult: Clear result
        """
        result = AuditLogResult(success=True)
        
        try:
            self.logs.clear()
            result.message = "All logs cleared"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def update_config(self, config: AuditLogConfig) -> AuditLogResult:
        """
        Update audit log configuration.
        
        Args:
            config: New configuration
            
        Returns:
            AuditLogResult: Update result
        """
        result = AuditLogResult(success=True)
        
        try:
            self.config = config
            result.message = "Config updated"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def get_config(self) -> AuditLogConfig:
        """
        Get audit log configuration.
        
        Returns:
            AuditLogConfig: Configuration
        """
        return self.config


if __name__ == "__main__":
    # Basit test
    from datetime import timedelta
    
    config = AuditLogConfig()
    logger = AuditLogger(config)
    
    # Log entry oluştur
    result = logger.log(
        user_id="user_1",
        action=AuditLogAction.LOGIN,
        category=AuditLogCategory.AUTHENTICATION,
        message="User logged in",
        level=AuditLogLevel.INFO
    )
    
    print(f"Log entry created: {result.message}")
    
    # User log'larını al
    user_logs = logger.get_user_logs("user_1")
    
    print(f"User logs: {len(user_logs)}")
