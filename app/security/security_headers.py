"""
MuhammedAI Local Developer - Security Headers
Security headers system for security.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum


class SecurityHeaderType(Enum):
    """Security header type."""
    HSTS = "Strict-Transport-Security"
    X_FRAME_OPTIONS = "X-Frame-Options"
    X_CONTENT_TYPE_OPTIONS = "X-Content-Type-Options"
    X_XSS_PROTECTION = "X-XSS-Protection"
    CONTENT_SECURITY_POLICY = "Content-Security-Policy"
    REFERRER_POLICY = "Referrer-Policy"
    PERMISSIONS_POLICY = "Permissions-Policy"
    CROSS_ORIGIN_OPENER_POLICY = "Cross-Origin-Opener-Policy"
    CROSS_ORIGIN_EMBEDDER_POLICY = "Cross-Origin-Embedder-Policy"
    CROSS_ORIGIN_RESOURCE_POLICY = "Cross-Origin-Resource-Policy"
    CUSTOM = "custom"


@dataclass
class SecurityHeader:
    """Security header."""
    header_id: str
    header_type: SecurityHeaderType
    value: str
    enabled: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SecurityHeadersConfig:
    """Security headers configuration."""
    enable_headers: bool = True
    enable_hsts: bool = True
    hsts_max_age: int = 31536000
    hsts_include_subdomains: bool = True
    hsts_preload: bool = False
    enable_x_frame_options: bool = True
    x_frame_options_value: str = "DENY"
    enable_x_content_type_options: bool = True
    enable_x_xss_protection: bool = True
    enable_referrer_policy: bool = True
    referrer_policy_value: str = "strict-origin-when-cross-origin"


@dataclass
class SecurityHeadersResult:
    """Security headers result."""
    success: bool
    message: Optional[str] = None
    headers: Dict[str, str] = field(default_factory=dict)
    header: Optional[SecurityHeader] = None
    errors: List[str] = field(default_factory=list)


class SecurityHeadersManager:
    """
    Security headers manager.
    
    Özellikler:
    - Header management
    - Header generation
    - HSTS configuration
    - Frame options
    - XSS protection
    - Referrer policy
    """
    
    def __init__(self, config: Optional[SecurityHeadersConfig] = None):
        """
        Initialize security headers manager.
        
        Args:
            config: Security headers configuration
        """
        self.config = config or SecurityHeadersConfig()
        self.headers: Dict[str, SecurityHeader] = {}
        self.header_id_counter = 0
        self._next_header_id()
        self._initialize_default_headers()
    
    def _next_header_id(self) -> str:
        """
        Generate next header ID.
        
        Returns:
            str: Header ID
        """
        self.header_id_counter += 1
        return f"header_{self.header_id_counter}"
    
    def _initialize_default_headers(self):
        """Initialize default security headers."""
        if self.config.enable_hsts:
            hsts_value = f"max-age={self.config.hsts_max_age}"
            if self.config.hsts_include_subdomains:
                hsts_value += "; includeSubDomains"
            if self.config.hsts_preload:
                hsts_value += "; preload"
            
            self.headers["strict-transport-security"] = SecurityHeader(
                header_id=self._next_header_id(),
                header_type=SecurityHeaderType.HSTS,
                value=hsts_value
            )
        
        if self.config.enable_x_frame_options:
            self.headers["x-frame-options"] = SecurityHeader(
                header_id=self._next_header_id(),
                header_type=SecurityHeaderType.X_FRAME_OPTIONS,
                value=self.config.x_frame_options_value
            )
        
        if self.config.enable_x_content_type_options:
            self.headers["x-content-type-options"] = SecurityHeader(
                header_id=self._next_header_id(),
                header_type=SecurityHeaderType.X_CONTENT_TYPE_OPTIONS,
                value="nosniff"
            )
        
        if self.config.enable_x_xss_protection:
            self.headers["x-xss-protection"] = SecurityHeader(
                header_id=self._next_header_id(),
                header_type=SecurityHeaderType.X_XSS_PROTECTION,
                value="1; mode=block"
            )
        
        if self.config.enable_referrer_policy:
            self.headers["referrer-policy"] = SecurityHeader(
                header_id=self._next_header_id(),
                header_type=SecurityHeaderType.REFERRER_POLICY,
                value=self.config.referrer_policy_value
            )
    
    def add_header(self, header_type: SecurityHeaderType, value: str) -> SecurityHeadersResult:
        """
        Add security header.
        
        Args:
            header_type: Header type
            value: Header value
            
        Returns:
            SecurityHeadersResult: Add result
        """
        result = SecurityHeadersResult(success=False)
        
        try:
            if not self.config.enable_headers:
                result.errors.append("Security headers disabled")
                return result
            
            header = SecurityHeader(
                header_id=self._next_header_id(),
                header_type=header_type,
                value=value
            )
            
            self.headers[header_type.value.lower()] = header
            
            result.success = True
            result.header = header
            result.message = f"Header '{header_type.value}' added"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def remove_header(self, header_type: SecurityHeaderType) -> SecurityHeadersResult:
        """
        Remove security header.
        
        Args:
            header_type: Header type
            
        Returns:
            SecurityHeadersResult: Remove result
        """
        result = SecurityHeadersResult(success=False)
        
        try:
            key = header_type.value.lower()
            if key in self.headers:
                del self.headers[key]
                result.success = True
                result.message = f"Header '{header_type.value}' removed"
            else:
                result.errors.append("Header not found")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def generate_headers(self) -> SecurityHeadersResult:
        """
        Generate all security headers.
        
        Returns:
            SecurityHeadersResult: Headers generation result
        """
        result = SecurityHeadersResult(success=True)
        
        try:
            headers_dict = {}
            
            for header in self.headers.values():
                if header.enabled:
                    headers_dict[header.header_type.value] = header.value
            
            result.headers = headers_dict
            result.message = f"Generated {len(headers_dict)} security headers"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def get_header(self, header_type: SecurityHeaderType) -> Optional[SecurityHeader]:
        """
        Get header by type.
        
        Args:
            header_type: Header type
            
        Returns:
            Optional[SecurityHeader]: Header
        """
        return self.headers.get(header_type.value.lower())
    
    def get_all_headers(self) -> List[SecurityHeader]:
        """
        Get all headers.
        
        Returns:
            List[SecurityHeader]: All headers
        """
        return list(self.headers.values())
    
    def update_config(self, config: SecurityHeadersConfig) -> SecurityHeadersResult:
        """
        Update security headers configuration.
        
        Args:
            config: New configuration
            
        Returns:
            SecurityHeadersResult: Update result
        """
        result = SecurityHeadersResult(success=True)
        
        try:
            self.config = config
            self.headers.clear()
            self._initialize_default_headers()
            result.message = "Config updated"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def get_config(self) -> SecurityHeadersConfig:
        """
        Get security headers configuration.
        
        Returns:
            SecurityHeadersConfig: Configuration
        """
        return self.config


if __name__ == "__main__":
    # Basit test
    config = SecurityHeadersConfig()
    manager = SecurityHeadersManager(config)
    
    # Headers oluştur
    result = manager.generate_headers()
    
    print(f"Headers generated: {result.message}")
    
    for key, value in result.headers.items():
        print(f"  {key}: {value}")
