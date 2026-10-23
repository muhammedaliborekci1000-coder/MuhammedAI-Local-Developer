"""
MuhammedAI Local Developer - Rate Limiting
Rate limiting system for security.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
import time


class RateLimitAlgorithm(Enum):
    """Rate limit algorithm."""
    TOKEN_BUCKET = "token_bucket"
    LEAKY_BUCKET = "leaky_bucket"
    FIXED_WINDOW = "fixed_window"
    SLIDING_WINDOW = "sliding_window"
    CUSTOM = "custom"


class RateLimitScope(Enum):
    """Rate limit scope."""
    GLOBAL = "global"
    USER = "user"
    IP = "ip"
    API_KEY = "api_key"
    ENDPOINT = "endpoint"
    CUSTOM = "custom"


@dataclass
class RateLimitRule:
    """Rate limit rule."""
    rule_id: str
    scope: RateLimitScope
    algorithm: RateLimitAlgorithm
    rate: int  # requests per period
    period: int  # period in seconds
    burst: int = 1  # burst capacity
    identifier: Optional[str] = None
    enabled: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RateLimitBucket:
    """Rate limit bucket."""
    bucket_id: str
    rule_id: str
    tokens: float
    last_update: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RateLimitConfig:
    """Rate limiting configuration."""
    enable_rate_limiting: bool = True
    default_algorithm: RateLimitAlgorithm = RateLimitAlgorithm.TOKEN_BUCKET
    default_rate: int = 100  # requests per minute
    default_period: int = 60
    enable_burst: bool = True
    default_burst: int = 10
    enable_whitelist: bool = False
    enable_blacklist: bool = False
    cleanup_interval: int = 3600  # seconds


@dataclass
class RateLimitResult:
    """Rate limit result."""
    allowed: bool
    message: Optional[str] = None
    rule_id: Optional[str] = None
    remaining: int = 0
    reset_time: Optional[datetime] = None
    retry_after: Optional[int] = None
    errors: List[str] = field(default_factory=list)


class RateLimiter:
    """
    Rate limiter.
    
    Özellikler:
    - Token bucket algorithm
    - Leaky bucket algorithm
    - Fixed window algorithm
    - Sliding window algorithm
    - Rate limit rules
    - Bucket management
    - Whitelist/Blacklist
    - Rate limit checking
    """
    
    def __init__(self, config: Optional[RateLimitConfig] = None):
        """
        Initialize rate limiter.
        
        Args:
            config: Rate limiting configuration
        """
        self.config = config or RateLimitConfig()
        self.rules: Dict[str, RateLimitRule] = {}
        self.buckets: Dict[str, RateLimitBucket] = {}
        self.whitelist: set = set()
        self.blacklist: set = set()
        self.rule_id_counter = 0
        self.bucket_id_counter = 0
        self._next_rule_id()
        self._next_bucket_id()
    
    def _next_rule_id(self) -> str:
        """
        Generate next rule ID.
        
        Returns:
            str: Rule ID
        """
        self.rule_id_counter += 1
        return f"rule_{self.rule_id_counter}"
    
    def _next_bucket_id(self) -> str:
        """
        Generate next bucket ID.
        
        Returns:
            str: Bucket ID
        """
        self.bucket_id_counter += 1
        return f"bucket_{self.bucket_id_counter}"
    
    def add_rule(self, scope: RateLimitScope, algorithm: RateLimitAlgorithm, rate: int, period: int, burst: int = 1, identifier: Optional[str] = None) -> RateLimitResult:
        """
        Add rate limit rule.
        
        Args:
            scope: Rate limit scope
            algorithm: Rate limit algorithm
            rate: Requests per period
            period: Period in seconds
            burst: Burst capacity
            identifier: Identifier for the rule
            
        Returns:
            RateLimitResult: Add result
        """
        result = RateLimitResult(allowed=False)
        
        try:
            rule = RateLimitRule(
                rule_id=self._next_rule_id(),
                scope=scope,
                algorithm=algorithm,
                rate=rate,
                period=period,
                burst=burst,
                identifier=identifier
            )
            
            self.rules[rule.rule_id] = rule
            
            result.allowed = True
            result.rule_id = rule.rule_id
            result.message = f"Rule '{rule.rule_id}' added successfully"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def remove_rule(self, rule_id: str) -> RateLimitResult:
        """
        Remove rate limit rule.
        
        Args:
            rule_id: Rule ID
            
        Returns:
            RateLimitResult: Remove result
        """
        result = RateLimitResult(allowed=False)
        
        try:
            if rule_id in self.rules:
                del self.rules[rule_id]
                # Remove associated buckets
                self.buckets = {k: v for k, v in self.buckets.items() if v.rule_id != rule_id}
                result.allowed = True
                result.message = f"Rule '{rule_id}' removed"
            else:
                result.errors.append("Rule not found")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_rule(self, rule_id: str) -> Optional[RateLimitRule]:
        """
        Get rule by ID.
        
        Args:
            rule_id: Rule ID
            
        Returns:
            Optional[RateLimitRule]: Rule
        """
        return self.rules.get(rule_id)
    
    def get_all_rules(self) -> List[RateLimitRule]:
        """
        Get all rules.
        
        Returns:
            List[RateLimitRule]: All rules
        """
        return list(self.rules.values())
    
    def check_rate_limit(self, identifier: str, rule_id: Optional[str] = None) -> RateLimitResult:
        """
        Check rate limit.
        
        Args:
            identifier: Identifier (user_id, ip, etc.)
            rule_id: Rule ID (optional, uses default if not provided)
            
        Returns:
            RateLimitResult: Check result
        """
        result = RateLimitResult(allowed=False)
        
        try:
            if not self.config.enable_rate_limiting:
                result.allowed = True
                result.message = "Rate limiting disabled"
                return result
            
            # Check whitelist
            if self.config.enable_whitelist and identifier in self.whitelist:
                result.allowed = True
                result.message = "Identifier whitelisted"
                return result
            
            # Check blacklist
            if self.config.enable_blacklist and identifier in self.blacklist:
                result.allowed = False
                result.message = "Identifier blacklisted"
                return result
            
            # Get rule
            rule = None
            if rule_id:
                rule = self.rules.get(rule_id)
            
            if not rule:
                # Use default settings
                rule = RateLimitRule(
                    rule_id="default",
                    scope=RateLimitScope.GLOBAL,
                    algorithm=self.config.default_algorithm,
                    rate=self.config.default_rate,
                    period=self.config.default_period,
                    burst=self.config.default_burst
                )
            
            # Get or create bucket
            bucket_key = f"{identifier}:{rule.rule_id}"
            bucket = self.buckets.get(bucket_key)
            
            if not bucket:
                bucket = RateLimitBucket(
                    bucket_id=self._next_bucket_id(),
                    rule_id=rule.rule_id,
                    tokens=float(rule.burst)
                )
                self.buckets[bucket_key] = bucket
            
            # Check based on algorithm
            if rule.algorithm == RateLimitAlgorithm.TOKEN_BUCKET:
                result = self._check_token_bucket(bucket, rule)
            elif rule.algorithm == RateLimitAlgorithm.LEAKY_BUCKET:
                result = self._check_leaky_bucket(bucket, rule)
            elif rule.algorithm == RateLimitAlgorithm.FIXED_WINDOW:
                result = self._check_fixed_window(bucket, rule)
            elif rule.algorithm == RateLimitAlgorithm.SLIDING_WINDOW:
                result = self._check_sliding_window(bucket, rule)
            else:
                result.errors.append("Unsupported algorithm")
            
            result.rule_id = rule.rule_id
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def _check_token_bucket(self, bucket: RateLimitBucket, rule: RateLimitRule) -> RateLimitResult:
        """
        Check token bucket algorithm.
        
        Args:
            bucket: Rate limit bucket
            rule: Rate limit rule
            
        Returns:
            RateLimitResult: Check result
        """
        result = RateLimitResult(allowed=False)
        
        now = datetime.now()
        elapsed = (now - bucket.last_update).total_seconds()
        
        # Refill tokens
        refill_rate = rule.rate / rule.period
        bucket.tokens = min(rule.burst, bucket.tokens + refill_rate * elapsed)
        bucket.last_update = now
        
        if bucket.tokens >= 1:
            bucket.tokens -= 1
            result.allowed = True
            result.remaining = int(bucket.tokens)
            result.message = "Request allowed"
        else:
            result.remaining = 0
            result.retry_after = int((1 - bucket.tokens) / refill_rate)
            result.message = "Rate limit exceeded"
        
        return result
    
    def _check_leaky_bucket(self, bucket: RateLimitBucket, rule: RateLimitRule) -> RateLimitResult:
        """
        Check leaky bucket algorithm.
        
        Args:
            bucket: Rate limit bucket
            rule: Rate limit rule
            
        Returns:
            RateLimitResult: Check result
        """
        result = RateLimitResult(allowed=False)
        
        now = datetime.now()
        elapsed = (now - bucket.last_update).total_seconds()
        
        # Leak tokens
        leak_rate = rule.rate / rule.period
        bucket.tokens = max(0, bucket.tokens - leak_rate * elapsed)
        bucket.last_update = now
        
        if bucket.tokens < rule.burst:
            bucket.tokens += 1
            result.allowed = True
            result.remaining = int(rule.burst - bucket.tokens)
            result.message = "Request allowed"
        else:
            result.remaining = 0
            result.retry_after = int((bucket.tokens - rule.burst + 1) / leak_rate)
            result.message = "Rate limit exceeded"
        
        return result
    
    def _check_fixed_window(self, bucket: RateLimitBucket, rule: RateLimitRule) -> RateLimitResult:
        """
        Check fixed window algorithm.
        
        Args:
            bucket: Rate limit bucket
            rule: Rate limit rule
            
        Returns:
            RateLimitResult: Check result
        """
        result = RateLimitResult(allowed=False)
        
        now = datetime.now()
        window_start = now - timedelta(seconds=rule.period)
        
        # Check if we need to reset
        if bucket.last_update < window_start:
            bucket.tokens = 0
            bucket.last_update = now
        
        if bucket.tokens < rule.rate:
            bucket.tokens += 1
            result.allowed = True
            result.remaining = int(rule.rate - bucket.tokens)
            result.message = "Request allowed"
        else:
            result.remaining = 0
            reset_time = bucket.last_update + timedelta(seconds=rule.period)
            result.retry_after = int((reset_time - now).total_seconds())
            result.message = "Rate limit exceeded"
        
        return result
    
    def _check_sliding_window(self, bucket: RateLimitBucket, rule: RateLimitRule) -> RateLimitResult:
        """
        Check sliding window algorithm.
        
        Args:
            bucket: Rate limit bucket
            rule: Rate limit rule
            
        Returns:
            RateLimitResult: Check result
        """
        # Simplified sliding window (similar to token bucket for now)
        return self._check_token_bucket(bucket, rule)
    
    def add_to_whitelist(self, identifier: str) -> RateLimitResult:
        """
        Add identifier to whitelist.
        
        Args:
            identifier: Identifier
            
        Returns:
            RateLimitResult: Add result
        """
        result = RateLimitResult(allowed=True)
        
        try:
            self.whitelist.add(identifier)
            result.message = f"Added '{identifier}' to whitelist"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.allowed = False
        
        return result
    
    def remove_from_whitelist(self, identifier: str) -> RateLimitResult:
        """
        Remove identifier from whitelist.
        
        Args:
            identifier: Identifier
            
        Returns:
            RateLimitResult: Remove result
        """
        result = RateLimitResult(allowed=True)
        
        try:
            self.whitelist.discard(identifier)
            result.message = f"Removed '{identifier}' from whitelist"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.allowed = False
        
        return result
    
    def add_to_blacklist(self, identifier: str) -> RateLimitResult:
        """
        Add identifier to blacklist.
        
        Args:
            identifier: Identifier
            
        Returns:
            RateLimitResult: Add result
        """
        result = RateLimitResult(allowed=True)
        
        try:
            self.blacklist.add(identifier)
            result.message = f"Added '{identifier}' to blacklist"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.allowed = False
        
        return result
    
    def remove_from_blacklist(self, identifier: str) -> RateLimitResult:
        """
        Remove identifier from blacklist.
        
        Args:
            identifier: Identifier
            
        Returns:
            RateLimitResult: Remove result
        """
        result = RateLimitResult(allowed=True)
        
        try:
            self.blacklist.discard(identifier)
            result.message = f"Removed '{identifier}' from blacklist"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.allowed = False
        
        return result
    
    def cleanup_buckets(self) -> RateLimitResult:
        """
        Cleanup old buckets.
        
        Returns:
            RateLimitResult: Cleanup result
        """
        result = RateLimitResult(allowed=True)
        
        try:
            cutoff = datetime.now() - timedelta(seconds=self.config.cleanup_interval)
            self.buckets = {k: v for k, v in self.buckets.items() if v.last_update > cutoff}
            result.message = f"Cleaned up old buckets"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.allowed = False
        
        return result
    
    def update_config(self, config: RateLimitConfig) -> RateLimitResult:
        """
        Update rate limiting configuration.
        
        Args:
            config: New configuration
            
        Returns:
            RateLimitResult: Update result
        """
        result = RateLimitResult(allowed=True)
        
        try:
            self.config = config
            result.message = "Config updated"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.allowed = False
        
        return result
    
    def get_config(self) -> RateLimitConfig:
        """
        Get rate limiting configuration.
        
        Returns:
            RateLimitConfig: Configuration
        """
        return self.config


if __name__ == "__main__":
    # Basit test
    config = RateLimitConfig()
    limiter = RateLimiter(config)
    
    # Rule oluştur
    result = limiter.add_rule(
        scope=RateLimitScope.USER,
        algorithm=RateLimitAlgorithm.TOKEN_BUCKET,
        rate=10,
        period=60,
        burst=5
    )
    
    print(f"Rule added: {result.message}")
    
    # Rate limit kontrolü
    check_result = limiter.check_rate_limit("user_1", result.rule_id)
    
    print(f"Rate limit check: {check_result.message}")
    print(f"Allowed: {check_result.allowed}")
