"""
MuhammedAI Local Developer - XSS Protection
XSS protection system for security.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum
import re
import html


class XSSAttackType(Enum):
    """XSS attack type."""
    REFLECTED = "reflected"
    STORED = "stored"
    DOM_BASED = "dom_based"
    SELF = "self"
    CUSTOM = "custom"


class XSSSeverity(Enum):
    """XSS severity."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class XSSContext(Enum):
    """XSS context."""
    HTML = "html"
    JAVASCRIPT = "javascript"
    CSS = "css"
    URL = "url"
    ATTRIBUTE = "attribute"
    CUSTOM = "custom"


@dataclass
class XSSPattern:
    """XSS pattern."""
    pattern_id: str
    name: str
    pattern: str
    description: str
    severity: XSSSeverity
    enabled: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class XSSDetectionResult:
    """XSS detection result."""
    is_detected: bool
    attack_type: Optional[XSSAttackType] = None
    severity: Optional[XSSSeverity] = None
    pattern_id: Optional[str] = None
    matched_text: Optional[str] = None
    context: Optional[XSSContext] = None
    message: Optional[str] = None
    errors: List[str] = field(default_factory=list)


@dataclass
class XSSProtectionConfig:
    """XSS protection configuration."""
    enable_protection: bool = True
    enable_sanitization: bool = True
    enable_detection: bool = True
    enable_encoding: bool = True
    default_context: XSSContext = XSSContext.HTML
    strict_mode: bool = False
    allow_safe_html: bool = True
    enable_custom_patterns: bool = False


@dataclass
class XSSSanitizationResult:
    """XSS sanitization result."""
    success: bool
    sanitized_content: Optional[str] = None
    original_content: Optional[str] = None
    detections: List[XSSDetectionResult] = field(default_factory=list)
    message: Optional[str] = None
    errors: List[str] = field(default_factory=list)


class XSSProtection:
    """
    XSS protection manager.
    
    Özellikler:
    - XSS detection
    - XSS sanitization
    - XSS encoding
    - Pattern matching
    - Context-aware filtering
    - Custom patterns
    """
    
    def __init__(self, config: Optional[XSSProtectionConfig] = None):
        """
        Initialize XSS protection.
        
        Args:
            config: XSS protection configuration
        """
        self.config = config or XSSProtectionConfig()
        self.patterns: Dict[str, XSSPattern] = {}
        self.pattern_id_counter = 0
        self._next_pattern_id()
        self._initialize_default_patterns()
    
    def _next_pattern_id(self) -> str:
        """
        Generate next pattern ID.
        
        Returns:
            str: Pattern ID
        """
        self.pattern_id_counter += 1
        return f"pattern_{self.pattern_id_counter}"
    
    def _initialize_default_patterns(self):
        """Initialize default XSS patterns."""
        default_patterns = [
            XSSPattern(
                pattern_id=self._next_pattern_id(),
                name="Script Tag",
                pattern=r'<script[^>]*>.*?</script>',
                description="Script tag injection",
                severity=XSSSeverity.HIGH
            ),
            XSSPattern(
                pattern_id=self._next_pattern_id(),
                name="JavaScript Event Handler",
                pattern=r'on\w+\s*=',
                description="JavaScript event handler",
                severity=XSSSeverity.HIGH
            ),
            XSSPattern(
                pattern_id=self._next_pattern_id(),
                name="Javascript Protocol",
                pattern=r'javascript:',
                description="JavaScript protocol",
                severity=XSSSeverity.CRITICAL
            ),
            XSSPattern(
                pattern_id=self._next_pattern_id(),
                name="Data URI",
                pattern=r'data:text/html',
                description="Data URI with HTML",
                severity=XSSSeverity.HIGH
            ),
            XSSPattern(
                pattern_id=self._next_pattern_id(),
                name="Eval Expression",
                pattern=r'eval\s*\(',
                description="Eval expression",
                severity=XSSSeverity.CRITICAL
            ),
            XSSPattern(
                pattern_id=self._next_pattern_id(),
                name="Expression",
                pattern=r'expression\s*\(',
                description="CSS expression",
                severity=XSSSeverity.HIGH
            ),
            XSSPattern(
                pattern_id=self._next_pattern_id(),
                name="FromCharCode",
                pattern=r'fromCharCode\s*\(',
                description="String.fromCharCode",
                severity=XSSSeverity.MEDIUM
            ),
            XSSPattern(
                pattern_id=self._next_pattern_id(),
                name="Alert",
                pattern=r'alert\s*\(',
                description="Alert function",
                severity=XSSSeverity.LOW
            )
        ]
        
        for pattern in default_patterns:
            self.patterns[pattern.pattern_id] = pattern
    
    def add_pattern(self, name: str, pattern: str, description: str, severity: XSSSeverity) -> XSSDetectionResult:
        """
        Add custom XSS pattern.
        
        Args:
            name: Pattern name
            pattern: Regex pattern
            description: Description
            severity: Severity
            
        Returns:
            XSSDetectionResult: Add result
        """
        result = XSSDetectionResult(is_detected=False)
        
        try:
            if not self.config.enable_custom_patterns:
                result.errors.append("Custom patterns disabled")
                return result
            
            xss_pattern = XSSPattern(
                pattern_id=self._next_pattern_id(),
                name=name,
                pattern=pattern,
                description=description,
                severity=severity
            )
            
            self.patterns[xss_pattern.pattern_id] = xss_pattern
            
            result.is_detected = False
            result.pattern_id = xss_pattern.pattern_id
            result.message = f"Pattern '{name}' added"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def remove_pattern(self, pattern_id: str) -> XSSDetectionResult:
        """
        Remove XSS pattern.
        
        Args:
            pattern_id: Pattern ID
            
        Returns:
            XSSDetectionResult: Remove result
        """
        result = XSSDetectionResult(is_detected=False)
        
        try:
            if pattern_id in self.patterns:
                del self.patterns[pattern_id]
                result.message = f"Pattern '{pattern_id}' removed"
            else:
                result.errors.append("Pattern not found")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def detect_xss(self, content: str, context: Optional[XSSContext] = None) -> XSSDetectionResult:
        """
        Detect XSS in content.
        
        Args:
            content: Content to check
            context: XSS context
            
        Returns:
            XSSDetectionResult: Detection result
        """
        result = XSSDetectionResult(is_detected=False)
        
        try:
            if not self.config.enable_detection:
                result.message = "Detection disabled"
                return result
            
            context = context or self.config.default_context
            
            for pattern in self.patterns.values():
                if not pattern.enabled:
                    continue
                
                match = re.search(pattern.pattern, content, re.IGNORECASE | re.DOTALL)
                if match:
                    result.is_detected = True
                    result.attack_type = XSSAttackType.REFLECTED
                    result.severity = pattern.severity
                    result.pattern_id = pattern.pattern_id
                    result.matched_text = match.group()
                    result.context = context
                    result.message = f"XSS detected: {pattern.name}"
                    break
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def sanitize(self, content: str, context: Optional[XSSContext] = None) -> XSSSanitizationResult:
        """
        Sanitize content to remove XSS.
        
        Args:
            content: Content to sanitize
            context: XSS context
            
        Returns:
            XSSSanitizationResult: Sanitization result
        """
        result = XSSSanitizationResult(success=False)
        
        try:
            if not self.config.enable_sanitization:
                result.success = True
                result.sanitized_content = content
                result.message = "Sanitization disabled"
                return result
            
            context = context or self.config.default_context
            original_content = content
            sanitized = content
            detections = []
            
            # Detect XSS first
            detection = self.detect_xss(content, context)
            if detection.is_detected:
                detections.append(detection)
                
                # Remove detected patterns
                for pattern in self.patterns.values():
                    if pattern.enabled:
                        sanitized = re.sub(pattern.pattern, '', sanitized, flags=re.IGNORECASE | re.DOTALL)
            
            # HTML encode if needed
            if self.config.enable_encoding and context == XSSContext.HTML:
                sanitized = html.escape(sanitized)
            
            result.success = True
            result.sanitized_content = sanitized
            result.original_content = original_content
            result.detections = detections
            result.message = "Content sanitized"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def encode(self, content: str, context: Optional[XSSContext] = None) -> XSSSanitizationResult:
        """
        Encode content for safe output.
        
        Args:
            content: Content to encode
            context: XSS context
            
        Returns:
            XSSSanitizationResult: Encoding result
        """
        result = XSSSanitizationResult(success=False)
        
        try:
            if not self.config.enable_encoding:
                result.success = True
                result.sanitized_content = content
                result.message = "Encoding disabled"
                return result
            
            context = context or self.config.default_context
            
            if context == XSSContext.HTML:
                encoded = html.escape(content)
            elif context == XSSContext.JAVASCRIPT:
                # JSON encode for JavaScript
                import json
                encoded = json.dumps(content)[1:-1]  # Remove quotes
            elif context == XSSContext.URL:
                import urllib.parse
                encoded = urllib.parse.quote(content)
            else:
                encoded = html.escape(content)
            
            result.success = True
            result.sanitized_content = encoded
            result.original_content = content
            result.message = "Content encoded"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_pattern(self, pattern_id: str) -> Optional[XSSPattern]:
        """
        Get pattern by ID.
        
        Args:
            pattern_id: Pattern ID
            
        Returns:
            Optional[XSSPattern]: Pattern
        """
        return self.patterns.get(pattern_id)
    
    def get_all_patterns(self) -> List[XSSPattern]:
        """
        Get all patterns.
        
        Returns:
            List[XSSPattern]: All patterns
        """
        return list(self.patterns.values())
    
    def update_config(self, config: XSSProtectionConfig) -> XSSSanitizationResult:
        """
        Update XSS protection configuration.
        
        Args:
            config: New configuration
            
        Returns:
            XSSSanitizationResult: Update result
        """
        result = XSSSanitizationResult(success=True)
        
        try:
            self.config = config
            result.message = "Config updated"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def get_config(self) -> XSSProtectionConfig:
        """
        Get XSS protection configuration.
        
        Returns:
            XSSProtectionConfig: Configuration
        """
        return self.config


if __name__ == "__main__":
    # Basit test
    config = XSSProtectionConfig()
    protection = XSSProtection(config)
    
    # XSS detect et
    malicious = "<script>alert('XSS')</script>"
    detection = protection.detect_xss(malicious)
    
    print(f"XSS detected: {detection.is_detected}")
    print(f"Message: {detection.message}")
    
    # Sanitize et
    result = protection.sanitize(malicious)
    
    print(f"Sanitized: {result.sanitized_content}")
