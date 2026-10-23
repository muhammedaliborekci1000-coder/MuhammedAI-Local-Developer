"""
MuhammedAI Local Developer - Firewall Rules
Firewall rules system for security.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum


class FirewallProtocol(Enum):
    """Firewall protocol."""
    TCP = "tcp"
    UDP = "udp"
    ICMP = "icmp"
    ANY = "any"
    CUSTOM = "custom"


class FirewallDirection(Enum):
    """Firewall direction."""
    INBOUND = "inbound"
    OUTBOUND = "outbound"
    BOTH = "both"


class FirewallAction(Enum):
    """Firewall action."""
    ALLOW = "allow"
    DENY = "deny"
    DROP = "drop"
    REJECT = "reject"
    LOG = "log"


@dataclass
class FirewallRule:
    """Firewall rule."""
    rule_id: str
    protocol: FirewallProtocol
    direction: FirewallDirection
    action: FirewallAction
    source_ip: Optional[str] = None
    destination_ip: Optional[str] = None
    source_port: Optional[int] = None
    destination_port: Optional[int] = None
    enabled: bool = True
    priority: int = 100
    description: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class FirewallConfig:
    """Firewall configuration."""
    enable_firewall: bool = True
    default_action: FirewallAction = FirewallAction.DENY
    enable_logging: bool = True
    log_denied: bool = True
    log_allowed: bool = False
    max_rules: int = 1000


@dataclass
class FirewallResult:
    """Firewall result."""
    success: bool
    message: Optional[str] = None
    rule: Optional[FirewallRule] = None
    rules: List[FirewallRule] = field(default_factory=list)
    action: Optional[FirewallAction] = None
    errors: List[str] = field(default_factory=list)


class FirewallManager:
    """
    Firewall manager.
    
    Özellikler:
    - Rule management
    - Protocol filtering
    - Direction filtering
    - Port filtering
    - IP filtering
    - Priority handling
    - Action enforcement
    """
    
    def __init__(self, config: Optional[FirewallConfig] = None):
        """
        Initialize firewall manager.
        
        Args:
            config: Firewall configuration
        """
        self.config = config or FirewallConfig()
        self.rules: List[FirewallRule] = []
        self.rule_id_counter = 0
        self._next_rule_id()
    
    def _next_rule_id(self) -> str:
        """
        Generate next rule ID.
        
        Returns:
            str: Rule ID
        """
        self.rule_id_counter += 1
        return f"rule_{self.rule_id_counter}"
    
    def add_rule(self, protocol: FirewallProtocol, direction: FirewallDirection, action: FirewallAction, source_ip: Optional[str] = None, destination_ip: Optional[str] = None, source_port: Optional[int] = None, destination_port: Optional[int] = None, priority: int = 100, description: Optional[str] = None) -> FirewallResult:
        """
        Add firewall rule.
        
        Args:
            protocol: Protocol
            direction: Direction
            action: Action
            source_ip: Source IP
            destination_ip: Destination IP
            source_port: Source port
            destination_port: Destination port
            priority: Rule priority (lower = higher priority)
            description: Description
            
        Returns:
            FirewallResult: Add result
        """
        result = FirewallResult(success=False)
        
        try:
            if not self.config.enable_firewall:
                result.errors.append("Firewall disabled")
                return result
            
            if len(self.rules) >= self.config.max_rules:
                result.errors.append("Maximum rules reached")
                return result
            
            rule = FirewallRule(
                rule_id=self._next_rule_id(),
                protocol=protocol,
                direction=direction,
                action=action,
                source_ip=source_ip,
                destination_ip=destination_ip,
                source_port=source_port,
                destination_port=destination_port,
                priority=priority,
                description=description
            )
            
            self.rules.append(rule)
            # Sort by priority
            self.rules.sort(key=lambda r: r.priority)
            
            result.success = True
            result.rule = rule
            result.message = f"Rule '{rule.rule_id}' added"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def remove_rule(self, rule_id: str) -> FirewallResult:
        """
        Remove firewall rule.
        
        Args:
            rule_id: Rule ID
            
        Returns:
            FirewallResult: Remove result
        """
        result = FirewallResult(success=False)
        
        try:
            for i, rule in enumerate(self.rules):
                if rule.rule_id == rule_id:
                    self.rules.pop(i)
                    result.success = True
                    result.message = f"Rule '{rule_id}' removed"
                    return result
            
            result.errors.append("Rule not found")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def evaluate_packet(self, protocol: FirewallProtocol, direction: FirewallDirection, source_ip: Optional[str] = None, destination_ip: Optional[str] = None, source_port: Optional[int] = None, destination_port: Optional[int] = None) -> FirewallResult:
        """
        Evaluate packet against rules.
        
        Args:
            protocol: Protocol
            direction: Direction
            source_ip: Source IP
            destination_ip: Destination IP
            source_port: Source port
            destination_port: Destination port
            
        Returns:
            FirewallResult: Evaluation result
        """
        result = FirewallResult(success=True)
        
        try:
            if not self.config.enable_firewall:
                result.action = self.config.default_action
                result.message = "Firewall disabled, using default action"
                return result
            
            # Evaluate rules in priority order
            for rule in self.rules:
                if not rule.enabled:
                    continue
                
                # Check protocol
                if rule.protocol != FirewallProtocol.ANY and rule.protocol != protocol:
                    continue
                
                # Check direction
                if rule.direction != FirewallDirection.BOTH and rule.direction != direction:
                    continue
                
                # Check source IP
                if rule.source_ip and source_ip and rule.source_ip != source_ip:
                    continue
                
                # Check destination IP
                if rule.destination_ip and destination_ip and rule.destination_ip != destination_ip:
                    continue
                
                # Check source port
                if rule.source_port is not None and source_port is not None and rule.source_port != source_port:
                    continue
                
                # Check destination port
                if rule.destination_port is not None and destination_port is not None and rule.destination_port != destination_port:
                    continue
                
                # Rule matches
                result.action = rule.action
                result.rule = rule
                result.message = f"Packet matched rule '{rule.rule_id}'"
                return result
            
            # No matching rule, use default action
            result.action = self.config.default_action
            result.message = "No matching rule, using default action"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_rule(self, rule_id: str) -> Optional[FirewallRule]:
        """
        Get rule by ID.
        
        Args:
            rule_id: Rule ID
            
        Returns:
            Optional[FirewallRule]: Rule
        """
        for rule in self.rules:
            if rule.rule_id == rule_id:
                return rule
        return None
    
    def get_rules_by_protocol(self, protocol: FirewallProtocol) -> List[FirewallRule]:
        """
        Get rules by protocol.
        
        Args:
            protocol: Protocol
            
        Returns:
            List[FirewallRule]: Rules
        """
        return [r for r in self.rules if r.protocol == protocol]
    
    def get_rules_by_direction(self, direction: FirewallDirection) -> List[FirewallRule]:
        """
        Get rules by direction.
        
        Args:
            direction: Direction
            
        Returns:
            List[FirewallRule]: Rules
        """
        return [r for r in self.rules if r.direction == direction]
    
    def get_all_rules(self) -> List[FirewallRule]:
        """
        Get all rules.
        
        Returns:
            List[FirewallRule]: All rules
        """
        return self.rules.copy()
    
    def enable_rule(self, rule_id: str) -> FirewallResult:
        """
        Enable rule.
        
        Args:
            rule_id: Rule ID
            
        Returns:
            FirewallResult: Enable result
        """
        result = FirewallResult(success=False)
        
        try:
            rule = self.get_rule(rule_id)
            if rule:
                rule.enabled = True
                result.success = True
                result.message = f"Rule '{rule_id}' enabled"
            else:
                result.errors.append("Rule not found")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def disable_rule(self, rule_id: str) -> FirewallResult:
        """
        Disable rule.
        
        Args:
            rule_id: Rule ID
            
        Returns:
            FirewallResult: Disable result
        """
        result = FirewallResult(success=False)
        
        try:
            rule = self.get_rule(rule_id)
            if rule:
                rule.enabled = False
                result.success = True
                result.message = f"Rule '{rule_id}' disabled"
            else:
                result.errors.append("Rule not found")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def update_config(self, config: FirewallConfig) -> FirewallResult:
        """
        Update firewall configuration.
        
        Args:
            config: New configuration
            
        Returns:
            FirewallResult: Update result
        """
        result = FirewallResult(success=True)
        
        try:
            self.config = config
            result.message = "Config updated"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def get_config(self) -> FirewallConfig:
        """
        Get firewall configuration.
        
        Returns:
            FirewallConfig: Configuration
        """
        return self.config


if __name__ == "__main__":
    # Basit test
    config = FirewallConfig()
    manager = FirewallManager(config)
    
    # Rule ekle
    result = manager.add_rule(
        protocol=FirewallProtocol.TCP,
        direction=FirewallDirection.INBOUND,
        action=FirewallAction.ALLOW,
        destination_port=80
    )
    
    print(f"Rule added: {result.message}")
    
    # Packet evaluate et
    eval_result = manager.evaluate_packet(
        protocol=FirewallProtocol.TCP,
        direction=FirewallDirection.INBOUND,
        destination_port=80
    )
    
    print(f"Action: {eval_result.action.value}")
