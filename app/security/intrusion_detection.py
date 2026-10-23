"""
MuhammedAI Local Developer - Intrusion Detection
Intrusion detection system for security.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta


class IntrusionType(Enum):
    """Intrusion type."""
    BRUTE_FORCE = "brute_force"
    SQL_INJECTION = "sql_injection"
    XSS_ATTACK = "xss_attack"
    DDOS = "ddos"
    PORT_SCAN = "port_scan"
    MALWARE = "malware"
    UNAUTHORIZED_ACCESS = "unauthorized_access"
    ANOMALY = "anomaly"
    CUSTOM = "custom"


class IntrusionSeverity(Enum):
    """Intrusion severity."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class IntrusionStatus(Enum):
    """Intrusion status."""
    DETECTED = "detected"
    INVESTIGATING = "investigating"
    CONFIRMED = "confirmed"
    FALSE_POSITIVE = "false_positive"
    RESOLVED = "resolved"


@dataclass
class IntrusionAlert:
    """Intrusion alert."""
    alert_id: str
    intrusion_type: IntrusionType
    severity: IntrusionSeverity
    status: IntrusionStatus
    source_ip: Optional[str] = None
    target_ip: Optional[str] = None
    description: Optional[str] = None
    detected_at: str = field(default_factory=lambda: str(datetime.now().timestamp()))
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DetectionRule:
    """Detection rule."""
    rule_id: str
    name: str
    intrusion_type: IntrusionType
    pattern: str
    severity: IntrusionSeverity
    enabled: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class IntrusionDetectionConfig:
    """Intrusion detection configuration."""
    enable_detection: bool = True
    enable_auto_blocking: bool = False
    enable_alerting: bool = True
    max_alerts_per_minute: int = 100
    retention_days: int = 30
    enable_anomaly_detection: bool = True
    anomaly_threshold: float = 0.8


@dataclass
class IntrusionDetectionResult:
    """Intrusion detection result."""
    success: bool
    message: Optional[str] = None
    alert: Optional[IntrusionAlert] = None
    alerts: List[IntrusionAlert] = field(default_factory=list)
    is_intrusion: bool = False
    errors: List[str] = field(default_factory=list)


class IntrusionDetectionManager:
    """
    Intrusion detection manager.
    
    Özellikler:
    - Rule-based detection
    - Anomaly detection
    - Alert generation
    - Status tracking
    - Severity classification
    - IP tracking
    - Pattern matching
    """
    
    def __init__(self, config: Optional[IntrusionDetectionConfig] = None):
        """
        Initialize intrusion detection manager.
        
        Args:
            config: Intrusion detection configuration
        """
        self.config = config or IntrusionDetectionConfig()
        self.rules: Dict[str, DetectionRule] = {}
        self.alerts: List[IntrusionAlert] = []
        self.alert_id_counter = 0
        self.rule_id_counter = 0
        self.ip_attempts: Dict[str, int] = {}
        self._next_alert_id()
        self._next_rule_id()
        self._initialize_default_rules()
    
    def _next_alert_id(self) -> str:
        """
        Generate next alert ID.
        
        Returns:
            str: Alert ID
        """
        self.alert_id_counter += 1
        return f"alert_{self.alert_id_counter}"
    
    def _next_rule_id(self) -> str:
        """
        Generate next rule ID.
        
        Returns:
            str: Rule ID
        """
        self.rule_id_counter += 1
        return f"rule_{self.rule_id_counter}"
    
    def _initialize_default_rules(self):
        """Initialize default detection rules."""
        # SQL Injection pattern
        self.rules["sql_injection"] = DetectionRule(
            rule_id=self._next_rule_id(),
            name="SQL Injection Detection",
            intrusion_type=IntrusionType.SQL_INJECTION,
            pattern=r"(?i)(union\s+select|or\s+1\s*=\s*1|drop\s+table|where\s+1\s*=\s*1)",
            severity=IntrusionSeverity.HIGH
        )
        
        # XSS pattern
        self.rules["xss"] = DetectionRule(
            rule_id=self._next_rule_id(),
            name="XSS Attack Detection",
            intrusion_type=IntrusionType.XSS_ATTACK,
            pattern=r"(?i)(<script|javascript:|onerror=|onload=|alert\()",
            severity=IntrusionSeverity.HIGH
        )
        
        # Brute force pattern
        self.rules["brute_force"] = DetectionRule(
            rule_id=self._next_rule_id(),
            name="Brute Force Detection",
            intrusion_type=IntrusionType.BRUTE_FORCE,
            pattern=r"brute_force",
            severity=IntrusionSeverity.MEDIUM
        )
    
    def add_rule(self, name: str, intrusion_type: IntrusionType, pattern: str, severity: IntrusionSeverity) -> IntrusionDetectionResult:
        """
        Add detection rule.
        
        Args:
            name: Rule name
            intrusion_type: Intrusion type
            pattern: Detection pattern
            severity: Severity
            
        Returns:
            IntrusionDetectionResult: Add result
        """
        result = IntrusionDetectionResult(success=False)
        
        try:
            if not self.config.enable_detection:
                result.errors.append("Detection disabled")
                return result
            
            rule = DetectionRule(
                rule_id=self._next_rule_id(),
                name=name,
                intrusion_type=intrusion_type,
                pattern=pattern,
                severity=severity
            )
            
            self.rules[rule.rule_id] = rule
            
            result.success = True
            result.message = f"Rule '{name}' added"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def detect_intrusion(self, data: str, source_ip: Optional[str] = None, target_ip: Optional[str] = None) -> IntrusionDetectionResult:
        """
        Detect intrusion in data.
        
        Args:
            data: Data to analyze
            source_ip: Source IP
            target_ip: Target IP
            
        Returns:
            IntrusionDetectionResult: Detection result
        """
        result = IntrusionDetectionResult(success=True)
        
        try:
            if not self.config.enable_detection:
                result.message = "Detection disabled"
                return result
            
            import re
            
            # Check against rules
            for rule in self.rules.values():
                if not rule.enabled:
                    continue
                
                if re.search(rule.pattern, data):
                    alert = IntrusionAlert(
                        alert_id=self._next_alert_id(),
                        intrusion_type=rule.intrusion_type,
                        severity=rule.severity,
                        status=IntrusionStatus.DETECTED,
                        source_ip=source_ip,
                        target_ip=target_ip,
                        description=f"Pattern matched: {rule.name}"
                    )
                    
                    self.alerts.append(alert)
                    result.alert = alert
                    result.is_intrusion = True
                    result.message = f"Intrusion detected: {rule.intrusion_type.value}"
                    
                    if self.config.enable_alerting:
                        self._send_alert(alert)
                    
                    return result
            
            # Check for brute force by IP
            if source_ip:
                self.ip_attempts[source_ip] = self.ip_attempts.get(source_ip, 0) + 1
                if self.ip_attempts[source_ip] > 10:
                    alert = IntrusionAlert(
                        alert_id=self._next_alert_id(),
                        intrusion_type=IntrusionType.BRUTE_FORCE,
                        severity=IntrusionSeverity.HIGH,
                        status=IntrusionStatus.DETECTED,
                        source_ip=source_ip,
                        description="Too many attempts from single IP"
                    )
                    
                    self.alerts.append(alert)
                    result.alert = alert
                    result.is_intrusion = True
                    result.message = "Brute force detected"
            
            result.message = "No intrusion detected"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def _send_alert(self, alert: IntrusionAlert):
        """
        Send alert (placeholder).
        
        Args:
            alert: Alert to send
        """
        # In real implementation, this would send email, SMS, etc.
        pass
    
    def update_alert_status(self, alert_id: str, status: IntrusionStatus) -> IntrusionDetectionResult:
        """
        Update alert status.
        
        Args:
            alert_id: Alert ID
            status: New status
            
        Returns:
            IntrusionDetectionResult: Update result
        """
        result = IntrusionDetectionResult(success=False)
        
        try:
            for alert in self.alerts:
                if alert.alert_id == alert_id:
                    alert.status = status
                    result.success = True
                    result.alert = alert
                    result.message = f"Alert '{alert_id}' status updated"
                    return result
            
            result.errors.append("Alert not found")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_alert(self, alert_id: str) -> Optional[IntrusionAlert]:
        """
        Get alert by ID.
        
        Args:
            alert_id: Alert ID
            
        Returns:
            Optional[IntrusionAlert]: Alert
        """
        for alert in self.alerts:
            if alert.alert_id == alert_id:
                return alert
        return None
    
    def get_alerts_by_type(self, intrusion_type: IntrusionType) -> List[IntrusionAlert]:
        """
        Get alerts by type.
        
        Args:
            intrusion_type: Intrusion type
            
        Returns:
            List[IntrusionAlert]: Alerts
        """
        return [a for a in self.alerts if a.intrusion_type == intrusion_type]
    
    def get_alerts_by_severity(self, severity: IntrusionSeverity) -> List[IntrusionAlert]:
        """
        Get alerts by severity.
        
        Args:
            severity: Severity
            
        Returns:
            List[IntrusionAlert]: Alerts
        """
        return [a for a in self.alerts if a.severity == severity]
    
    def get_all_alerts(self) -> List[IntrusionAlert]:
        """
        Get all alerts.
        
        Returns:
            List[IntrusionAlert]: All alerts
        """
        return self.alerts.copy()
    
    def cleanup_old_alerts(self) -> IntrusionDetectionResult:
        """
        Cleanup old alerts based on retention policy.
        
        Returns:
            IntrusionDetectionResult: Cleanup result
        """
        result = IntrusionDetectionResult(success=True)
        
        try:
            cutoff_time = datetime.now() - timedelta(days=self.config.retention_days)
            cutoff_timestamp = cutoff_time.timestamp()
            
            original_count = len(self.alerts)
            self.alerts = [a for a in self.alerts if float(a.detected_at) > cutoff_timestamp]
            removed_count = original_count - len(self.alerts)
            
            result.message = f"Cleaned up {removed_count} old alerts"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def update_config(self, config: IntrusionDetectionConfig) -> IntrusionDetectionResult:
        """
        Update intrusion detection configuration.
        
        Args:
            config: New configuration
            
        Returns:
            IntrusionDetectionResult: Update result
        """
        result = IntrusionDetectionResult(success=True)
        
        try:
            self.config = config
            result.message = "Config updated"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def get_config(self) -> IntrusionDetectionConfig:
        """
        Get intrusion detection configuration.
        
        Returns:
            IntrusionDetectionConfig: Configuration
        """
        return self.config


if __name__ == "__main__":
    # Basit test
    config = IntrusionDetectionConfig()
    manager = IntrusionDetectionManager(config)
    
    # Detect et
    result = manager.detect_intrusion("SELECT * FROM users WHERE 1=1", source_ip="192.168.1.1")
    
    print(f"Detected: {result.message}")
    print(f"Is intrusion: {result.is_intrusion}")
