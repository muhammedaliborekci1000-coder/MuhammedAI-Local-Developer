"""
MuhammedAI Local Developer - Content Security Policy
Content security policy system for security.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum


class CSPDirective(Enum):
    """CSP directive."""
    DEFAULT_SRC = "default-src"
    SCRIPT_SRC = "script-src"
    STYLE_SRC = "style-src"
    IMG_SRC = "img-src"
    CONNECT_SRC = "connect-src"
    FONT_SRC = "font-src"
    OBJECT_SRC = "object-src"
    MEDIA_SRC = "media-src"
    FRAME_SRC = "frame-src"
    FRAME_ANCESTORS = "frame-ancestors"
    BASE_URI = "base-uri"
    FORM_ACTION = "form-action"
    MANIFEST_SRC = "manifest-src"
    WORKER_SRC = "worker-src"
    REPORT_URI = "report-uri"
    REPORT_TO = "report-to"
    UPGRADE_INSECURE_REQUESTS = "upgrade-insecure-requests"
    BLOCK_ALL_MIXED_CONTENT = "block-all-mixed-content"


class CSPSource(Enum):
    """CSP source."""
    SELF = "'self'"
    NONE = "'none'"
    UNSAFE_INLINE = "'unsafe-inline'"
    UNSAFE_EVAL = "'unsafe-eval'"
    STRICT_DYNAMIC = "'strict-dynamic'"
    HTTPS = "https:"
    HTTP = "http:"
    DATA = "data:"
    BLOB = "blob:"
    CUSTOM = "custom"


@dataclass
class CSPRule:
    """CSP rule."""
    rule_id: str
    directive: CSPDirective
    sources: List[str]
    enabled: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CSPConfig:
    """CSP configuration."""
    enable_csp: bool = True
    report_only_mode: bool = False
    enable_reporting: bool = True
    strict_mode: bool = False
    upgrade_insecure: bool = True
    block_mixed_content: bool = True


@dataclass
class CSPResult:
    """CSP result."""
    success: bool
    message: Optional[str] = None
    policy: Optional[str] = None
    rule: Optional[CSPRule] = None
    rules: List[CSPRule] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)


class CSPManager:
    """
    Content Security Policy manager.
    
    Özellikler:
    - CSP rule management
    - Policy generation
    - Source management
    - Directive management
    - Report-only mode
    - Strict mode
    """
    
    def __init__(self, config: Optional[CSPConfig] = None):
        """
        Initialize CSP manager.
        
        Args:
            config: CSP configuration
        """
        self.config = config or CSPConfig()
        self.rules: Dict[str, CSPRule] = {}
        self.rule_id_counter = 0
        self._next_rule_id()
        self._initialize_default_rules()
    
    def _next_rule_id(self) -> str:
        """
        Generate next rule ID.
        
        Returns:
            str: Rule ID
        """
        self.rule_id_counter += 1
        return f"rule_{self.rule_id_counter}"
    
    def _initialize_default_rules(self):
        """Initialize default CSP rules."""
        default_rules = [
            CSPRule(
                rule_id=self._next_rule_id(),
                directive=CSPDirective.DEFAULT_SRC,
                sources=[CSPSource.SELF.value]
            ),
            CSPRule(
                rule_id=self._next_rule_id(),
                directive=CSPDirective.SCRIPT_SRC,
                sources=[CSPSource.SELF.value]
            ),
            CSPRule(
                rule_id=self._next_rule_id(),
                directive=CSPDirective.STYLE_SRC,
                sources=[CSPSource.SELF.value, CSPSource.UNSAFE_INLINE.value]
            ),
            CSPRule(
                rule_id=self._next_rule_id(),
                directive=CSPDirective.IMG_SRC,
                sources=[CSPSource.SELF.value, CSPSource.DATA.value]
            ),
            CSPRule(
                rule_id=self._next_rule_id(),
                directive=CSPDirective.CONNECT_SRC,
                sources=[CSPSource.SELF.value]
            )
        ]
        
        for rule in default_rules:
            self.rules[rule.rule_id] = rule
    
    def add_rule(self, directive: CSPDirective, sources: List[str]) -> CSPResult:
        """
        Add CSP rule.
        
        Args:
            directive: CSP directive
            sources: List of sources
            
        Returns:
            CSPResult: Add result
        """
        result = CSPResult(success=False)
        
        try:
            rule = CSPRule(
                rule_id=self._next_rule_id(),
                directive=directive,
                sources=sources
            )
            
            self.rules[rule.rule_id] = rule
            
            result.success = True
            result.rule = rule
            result.rules = self.get_all_rules()
            result.message = f"Rule for '{directive.value}' added"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def remove_rule(self, rule_id: str) -> CSPResult:
        """
        Remove CSP rule.
        
        Args:
            rule_id: Rule ID
            
        Returns:
            CSPResult: Remove result
        """
        result = CSPResult(success=False)
        
        try:
            if rule_id in self.rules:
                del self.rules[rule_id]
                result.success = True
                result.rules = self.get_all_rules()
                result.message = f"Rule '{rule_id}' removed"
            else:
                result.errors.append("Rule not found")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def update_rule(self, rule_id: str, sources: Optional[List[str]] = None, enabled: Optional[bool] = None) -> CSPResult:
        """
        Update CSP rule.
        
        Args:
            rule_id: Rule ID
            sources: New sources
            enabled: Enabled status
            
        Returns:
            CSPResult: Update result
        """
        result = CSPResult(success=False)
        
        try:
            rule = self.rules.get(rule_id)
            if not rule:
                result.errors.append("Rule not found")
                return result
            
            if sources is not None:
                rule.sources = sources
            
            if enabled is not None:
                rule.enabled = enabled
            
            result.success = True
            result.rule = rule
            result.message = f"Rule '{rule_id}' updated"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_rule(self, rule_id: str) -> Optional[CSPRule]:
        """
        Get rule by ID.
        
        Args:
            rule_id: Rule ID
            
        Returns:
            Optional[CSPRule]: Rule
        """
        return self.rules.get(rule_id)
    
    def get_rule_by_directive(self, directive: CSPDirective) -> Optional[CSPRule]:
        """
        Get rule by directive.
        
        Args:
            directive: Directive
            
        Returns:
            Optional[CSPRule]: Rule
        """
        for rule in self.rules.values():
            if rule.directive == directive:
                return rule
        return None
    
    def get_all_rules(self) -> List[CSPRule]:
        """
        Get all rules.
        
        Returns:
            List[CSPRule]: All rules
        """
        return list(self.rules.values())
    
    def generate_policy(self) -> CSPResult:
        """
        Generate CSP policy string.
        
        Returns:
            CSPResult: Policy generation result
        """
        result = CSPResult(success=False)
        
        try:
            if not self.config.enable_csp:
                result.errors.append("CSP disabled")
                return result
            
            policy_parts = []
            
            # Add upgrade-insecure-requests if enabled
            if self.config.upgrade_insecure:
                policy_parts.append(CSPDirective.UPGRADE_INSECURE_REQUESTS.value)
            
            # Add block-all-mixed-content if enabled
            if self.config.block_mixed_content:
                policy_parts.append(CSPDirective.BLOCK_ALL_MIXED_CONTENT.value)
            
            # Add rules
            for rule in self.rules.values():
                if rule.enabled:
                    sources_str = " ".join(rule.sources)
                    policy_parts.append(f"{rule.directive.value} {sources_str}")
            
            policy = "; ".join(policy_parts) + ";"
            
            result.success = True
            result.policy = policy
            result.message = "Policy generated successfully"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def generate_header(self) -> CSPResult:
        """
        Generate CSP header value.
        
        Returns:
            CSPResult: Header generation result
        """
        result = self.generate_policy()
        
        if result.success:
            header_name = "Content-Security-Policy-Report-Only" if self.config.report_only_mode else "Content-Security-Policy"
            result.message = f"{header_name}: {result.policy}"
        
        return result
    
    def enable_strict_mode(self) -> CSPResult:
        """
        Enable strict CSP mode.
        
        Returns:
            CSPResult: Enable result
        """
        result = CSPResult(success=False)
        
        try:
            self.config.strict_mode = True
            
            # Update rules for strict mode
            for rule in self.rules.values():
                if rule.directive in [CSPDirective.SCRIPT_SRC, CSPDirective.STYLE_SRC]:
                    if CSPSource.UNSAFE_INLINE.value in rule.sources:
                        rule.sources.remove(CSPSource.UNSAFE_INLINE.value)
                    if CSPSource.UNSAFE_EVAL.value in rule.sources:
                        rule.sources.remove(CSPSource.UNSAFE_EVAL.value)
            
            result.success = True
            result.rules = self.get_all_rules()
            result.message = "Strict mode enabled"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def update_config(self, config: CSPConfig) -> CSPResult:
        """
        Update CSP configuration.
        
        Args:
            config: New configuration
            
        Returns:
            CSPResult: Update result
        """
        result = CSPResult(success=True)
        
        try:
            self.config = config
            result.message = "Config updated"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def get_config(self) -> CSPConfig:
        """
        Get CSP configuration.
        
        Returns:
            CSPConfig: Configuration
        """
        return self.config


if __name__ == "__main__":
    # Basit test
    config = CSPConfig()
    manager = CSPManager(config)
    
    # Policy oluştur
    result = manager.generate_policy()
    
    print(f"Policy: {result.policy}")
    
    # Header oluştur
    header_result = manager.generate_header()
    
    print(f"Header: {header_result.message}")
