"""
MuhammedAI Local Developer - IP Filtering
IP filtering system for security.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum
import ipaddress


class IPFilterType(Enum):
    """IP filter type."""
    WHITELIST = "whitelist"
    BLACKLIST = "blacklist"
    CUSTOM = "custom"


class IPFilterAction(Enum):
    """IP filter action."""
    ALLOW = "allow"
    DENY = "deny"
    RATE_LIMIT = "rate_limit"
    LOG = "log"


@dataclass
class IPFilter:
    """IP filter."""
    filter_id: str
    ip_address: str
    filter_type: IPFilterType
    action: IPFilterAction
    enabled: bool = True
    description: Optional[str] = None
    expires_at: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class IPFilterConfig:
    """IP filter configuration."""
    enable_filtering: bool = True
    default_action: IPFilterAction = IPFilterAction.ALLOW
    enable_ipv4: bool = True
    enable_ipv6: bool = True
    enable_cidr: bool = True
    enable_range: bool = True


@dataclass
class IPFilterResult:
    """IP filter result."""
    success: bool
    message: Optional[str] = None
    filter: Optional[IPFilter] = None
    is_allowed: bool = False
    action: Optional[IPFilterAction] = None
    errors: List[str] = field(default_factory=list)


class IPFilterManager:
    """
    IP filter manager.
    
    Özellikler:
    - Whitelist management
    - Blacklist management
    - IP validation
    - CIDR support
    - IPv4/IPv6 support
    - Action enforcement
    """
    
    def __init__(self, config: Optional[IPFilterConfig] = None):
        """
        Initialize IP filter manager.
        
        Args:
            config: IP filter configuration
        """
        self.config = config or IPFilterConfig()
        self.filters: Dict[str, IPFilter] = {}
        self.filter_id_counter = 0
        self._next_filter_id()
    
    def _next_filter_id(self) -> str:
        """
        Generate next filter ID.
        
        Returns:
            str: Filter ID
        """
        self.filter_id_counter += 1
        return f"filter_{self.filter_id_counter}"
    
    def _validate_ip(self, ip_address: str) -> bool:
        """
        Validate IP address.
        
        Args:
            ip_address: IP address to validate
            
        Returns:
            bool: Is valid
        """
        try:
            if self.config.enable_cidr and "/" in ip_address:
                ipaddress.ip_network(ip_address, strict=False)
            else:
                ipaddress.ip_address(ip_address)
            return True
        except:
            return False
    
    def add_filter(self, ip_address: str, filter_type: IPFilterType, action: IPFilterAction, description: Optional[str] = None) -> IPFilterResult:
        """
        Add IP filter.
        
        Args:
            ip_address: IP address
            filter_type: Filter type
            action: Filter action
            description: Description
            
        Returns:
            IPFilterResult: Add result
        """
        result = IPFilterResult(success=False)
        
        try:
            if not self.config.enable_filtering:
                result.errors.append("IP filtering disabled")
                return result
            
            # Validate IP
            if not self._validate_ip(ip_address):
                result.errors.append("Invalid IP address")
                return result
            
            filter_obj = IPFilter(
                filter_id=self._next_filter_id(),
                ip_address=ip_address,
                filter_type=filter_type,
                action=action,
                description=description
            )
            
            self.filters[filter_obj.filter_id] = filter_obj
            
            result.success = True
            result.filter = filter_obj
            result.message = f"Filter added for '{ip_address}'"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def remove_filter(self, filter_id: str) -> IPFilterResult:
        """
        Remove IP filter.
        
        Args:
            filter_id: Filter ID
            
        Returns:
            IPFilterResult: Remove result
        """
        result = IPFilterResult(success=False)
        
        try:
            if filter_id in self.filters:
                del self.filters[filter_id]
                result.success = True
                result.message = f"Filter '{filter_id}' removed"
            else:
                result.errors.append("Filter not found")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def check_ip(self, ip_address: str) -> IPFilterResult:
        """
        Check IP against filters.
        
        Args:
            ip_address: IP address to check
            
        Returns:
            IPFilterResult: Check result
        """
        result = IPFilterResult(success=True)
        
        try:
            if not self.config.enable_filtering:
                result.is_allowed = True
                result.action = self.config.default_action
                result.message = "Filtering disabled, using default action"
                return result
            
            # Validate IP
            if not self._validate_ip(ip_address):
                result.errors.append("Invalid IP address")
                return result
            
            # Check filters
            for filter_obj in self.filters.values():
                if not filter_obj.enabled:
                    continue
                
                # Check if IP matches filter
                if self._ip_matches(ip_address, filter_obj.ip_address):
                    result.action = filter_obj.action
                    result.filter = filter_obj
                    
                    if filter_obj.action == IPFilterAction.ALLOW:
                        result.is_allowed = True
                        result.message = f"IP allowed by {filter_obj.filter_type.value}"
                    elif filter_obj.action == IPFilterAction.DENY:
                        result.is_allowed = False
                        result.message = f"IP denied by {filter_obj.filter_type.value}"
                    else:
                        result.is_allowed = True
                        result.message = f"IP action: {filter_obj.action.value}"
                    
                    return result
            
            # No matching filter, use default action
            result.is_allowed = self.config.default_action == IPFilterAction.ALLOW
            result.action = self.config.default_action
            result.message = f"No matching filter, using default action"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def _ip_matches(self, ip_address: str, filter_ip: str) -> bool:
        """
        Check if IP matches filter IP.
        
        Args:
            ip_address: IP address
            filter_ip: Filter IP (can be CIDR)
            
        Returns:
            bool: Matches
        """
        try:
            if "/" in filter_ip:
                # CIDR range
                network = ipaddress.ip_network(filter_ip, strict=False)
                return ipaddress.ip_address(ip_address) in network
            else:
                # Exact match
                return ip_address == filter_ip
        except:
            return False
    
    def get_whitelist(self) -> List[IPFilter]:
        """
        Get whitelist.
        
        Returns:
            List[IPFilter]: Whitelist filters
        """
        return [f for f in self.filters.values() if f.filter_type == IPFilterType.WHITELIST]
    
    def get_blacklist(self) -> List[IPFilter]:
        """
        Get blacklist.
        
        Returns:
            List[IPFilter]: Blacklist filters
        """
        return [f for f in self.filters.values() if f.filter_type == IPFilterType.BLACKLIST]
    
    def get_all_filters(self) -> List[IPFilter]:
        """
        Get all filters.
        
        Returns:
            List[IPFilter]: All filters
        """
        return list(self.filters.values())
    
    def update_config(self, config: IPFilterConfig) -> IPFilterResult:
        """
        Update IP filter configuration.
        
        Args:
            config: New configuration
            
        Returns:
            IPFilterResult: Update result
        """
        result = IPFilterResult(success=True)
        
        try:
            self.config = config
            result.message = "Config updated"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def get_config(self) -> IPFilterConfig:
        """
        Get IP filter configuration.
        
        Returns:
            IPFilterConfig: Configuration
        """
        return self.config


if __name__ == "__main__":
    # Basit test
    config = IPFilterConfig()
    manager = IPFilterManager(config)
    
    # Whitelist ekle
    result = manager.add_filter("192.168.1.1", IPFilterType.WHITELIST, IPFilterAction.ALLOW)
    
    print(f"Filter added: {result.message}")
    
    # IP kontrol et
    check = manager.check_ip("192.168.1.1")
    
    print(f"Allowed: {check.is_allowed}")
