"""
MuhammedAI Local Developer - Input Validation
Input validation system for security.
"""

from typing import Dict, Any, Optional, List, Callable
from dataclasses import dataclass, field
from enum import Enum
import re
import email.utils


class ValidationType(Enum):
    """Validation type."""
    REQUIRED = "required"
    MIN_LENGTH = "min_length"
    MAX_LENGTH = "max_length"
    PATTERN = "pattern"
    EMAIL = "email"
    URL = "url"
    PHONE = "phone"
    NUMERIC = "numeric"
    INTEGER = "integer"
    FLOAT = "float"
    BOOLEAN = "boolean"
    DATE = "date"
    TIME = "time"
    DATETIME = "datetime"
    UUID = "uuid"
    IP_ADDRESS = "ip_address"
    CUSTOM = "custom"


class DataType(Enum):
    """Data type."""
    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    BOOLEAN = "boolean"
    LIST = "list"
    DICT = "dict"
    ANY = "any"


class ValidationSeverity(Enum):
    """Validation severity."""
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass
class ValidationRule:
    """Validation rule."""
    rule_id: str
    validation_type: ValidationType
    data_type: DataType
    enabled: bool = True
    min_length: Optional[int] = None
    max_length: Optional[int] = None
    pattern: Optional[str] = None
    custom_validator: Optional[Callable] = None
    error_message: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ValidationConfig:
    """Validation configuration."""
    enable_validation: bool = True
    strict_mode: bool = False
    stop_on_first_error: bool = False
    enable_auto_sanitize: bool = False
    default_data_type: DataType = DataType.STRING


@dataclass
class ValidationError:
    """Validation error."""
    field: str
    validation_type: ValidationType
    severity: ValidationSeverity
    message: str
    value: Optional[Any] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ValidationResult:
    """Validation result."""
    is_valid: bool
    field: Optional[str] = None
    value: Optional[Any] = None
    sanitized_value: Optional[Any] = None
    errors: List[Any] = None
    warnings: List[Any] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.errors is None:
            self.errors = []
        if self.warnings is None:
            self.warnings = []
        if self.metadata is None:
            self.metadata = {}


class InputValidator:
    """
    Input validator.
    
    Özellikler:
    - Type validation
    - Length validation
    - Pattern validation
    - Format validation (email, URL, phone, etc.)
    - Custom validators
    - Sanitization
    - Strict mode
    """
    
    def __init__(self, config: Optional[ValidationConfig] = None):
        """
        Initialize input validator.
        
        Args:
            config: Validation configuration
        """
        self.config = config or ValidationConfig()
        self.rules: Dict[str, List[ValidationRule]] = {}
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
    
    def add_rule(self, field: str, validation_type: ValidationType, data_type: DataType = DataType.STRING, **kwargs) -> ValidationResult:
        """
        Add validation rule for a field.
        
        Args:
            field: Field name
            validation_type: Validation type
            data_type: Data type
            **kwargs: Additional rule parameters
            
        Returns:
            ValidationResult: Add result
        """
        result = ValidationResult(is_valid=True)
        
        try:
            rule = ValidationRule(
                rule_id=self._next_rule_id(),
                validation_type=validation_type,
                data_type=data_type,
                **kwargs
            )
            
            if field not in self.rules:
                self.rules[field] = []
            
            self.rules[field].append(rule)
            result.field = field
            result.message = f"Rule added for field '{field}'"
        
        except Exception as e:
            result.is_valid = False
            result.errors.append(ValidationError(
                field=field,
                validation_type=validation_type,
                severity=ValidationSeverity.ERROR,
                message=f"Error adding rule: {str(e)}"
            ))
        
        return result
    
    def remove_rule(self, field: str, rule_id: str) -> ValidationResult:
        """
        Remove validation rule.
        
        Args:
            field: Field name
            rule_id: Rule ID
            
        Returns:
            ValidationResult: Remove result
        """
        result = ValidationResult(is_valid=True)
        
        try:
            if field in self.rules:
                self.rules[field] = [r for r in self.rules[field] if r.rule_id != rule_id]
                result.message = f"Rule '{rule_id}' removed from field '{field}'"
            else:
                result.is_valid = False
                result.errors.append(ValidationError(
                    field=field,
                    validation_type=ValidationType.CUSTOM,
                    severity=ValidationSeverity.ERROR,
                    message="Field not found"
                ))
        
        except Exception as e:
            result.is_valid = False
            result.errors.append(ValidationError(
                field=field,
                validation_type=ValidationType.CUSTOM,
                severity=ValidationSeverity.ERROR,
                message=f"Error removing rule: {str(e)}"
            ))
        
        return result
    
    def validate(self, field: str, value: Any, rules: Optional[List[ValidationRule]] = None) -> ValidationResult:
        """
        Validate a field value.
        
        Args:
            field: Field name
            value: Value to validate
            rules: Custom rules (optional, uses field rules if not provided)
            
        Returns:
            ValidationResult: Validation result
        """
        result = ValidationResult(is_valid=True, field=field, value=value)
        
        if not self.config.enable_validation:
            return result
        
        validation_rules = rules or self.rules.get(field, [])
        
        for rule in validation_rules:
            if not rule.enabled:
                continue
            
            validation_result = self._validate_rule(rule, value)
            
            if not validation_result.is_valid:
                result.is_valid = False
                result.errors.extend(validation_result.errors)
                
                if self.config.stop_on_first_error:
                    break
        
        return result
    
    def _validate_rule(self, rule: ValidationRule, value: Any) -> ValidationResult:
        """
        Validate a single rule.
        
        Args:
            rule: Validation rule
            value: Value to validate
            
        Returns:
            ValidationResult: Validation result
        """
        result = ValidationResult(is_valid=True)
        
        try:
            # Check required
            if rule.validation_type == ValidationType.REQUIRED:
                if value is None or value == "":
                    result.is_valid = False
                    result.errors.append(ValidationError(
                        field="",
                        validation_type=ValidationType.REQUIRED,
                        severity=ValidationSeverity.ERROR,
                        message=rule.error_message or "Field is required",
                        value=value
                    ))
            
            # Check min length
            elif rule.validation_type == ValidationType.MIN_LENGTH:
                if value is not None and len(str(value)) < rule.min_length:
                    result.is_valid = False
                    result.errors.append(ValidationError(
                        field="",
                        validation_type=ValidationType.MIN_LENGTH,
                        severity=ValidationSeverity.ERROR,
                        message=rule.error_message or f"Minimum length is {rule.min_length}",
                        value=value
                    ))
            
            # Check max length
            elif rule.validation_type == ValidationType.MAX_LENGTH:
                if value is not None and len(str(value)) > rule.max_length:
                    result.is_valid = False
                    result.errors.append(ValidationError(
                        field="",
                        validation_type=ValidationType.MAX_LENGTH,
                        severity=ValidationSeverity.ERROR,
                        message=rule.error_message or f"Maximum length is {rule.max_length}",
                        value=value
                    ))
            
            # Check pattern
            elif rule.validation_type == ValidationType.PATTERN:
                if value is not None and not re.match(rule.pattern, str(value)):
                    result.is_valid = False
                    result.errors.append(ValidationError(
                        field="",
                        validation_type=ValidationType.PATTERN,
                        severity=ValidationSeverity.ERROR,
                        message=rule.error_message or "Pattern does not match",
                        value=value
                    ))
            
            # Check email
            elif rule.validation_type == ValidationType.EMAIL:
                if value is not None and not self._is_valid_email(str(value)):
                    result.is_valid = False
                    result.errors.append(ValidationError(
                        field="",
                        validation_type=ValidationType.EMAIL,
                        severity=ValidationSeverity.ERROR,
                        message=rule.error_message or "Invalid email format",
                        value=value
                    ))
            
            # Check URL
            elif rule.validation_type == ValidationType.URL:
                if value is not None and not self._is_valid_url(str(value)):
                    result.is_valid = False
                    result.errors.append(ValidationError(
                        field="",
                        validation_type=ValidationType.URL,
                        severity=ValidationSeverity.ERROR,
                        message=rule.error_message or "Invalid URL format",
                        value=value
                    ))
            
            # Check numeric
            elif rule.validation_type == ValidationType.NUMERIC:
                if value is not None and not str(value).replace('.', '').replace('-', '').isdigit():
                    result.is_valid = False
                    result.errors.append(ValidationError(
                        field="",
                        validation_type=ValidationType.NUMERIC,
                        severity=ValidationSeverity.ERROR,
                        message=rule.error_message or "Value must be numeric",
                        value=value
                    ))
            
            # Check integer
            elif rule.validation_type == ValidationType.INTEGER:
                if value is not None and not str(value).replace('-', '').isdigit():
                    result.is_valid = False
                    result.errors.append(ValidationError(
                        field="",
                        validation_type=ValidationType.INTEGER,
                        severity=ValidationSeverity.ERROR,
                        message=rule.error_message or "Value must be an integer",
                        value=value
                    ))
            
            # Check custom validator
            elif rule.validation_type == ValidationType.CUSTOM and rule.custom_validator:
                if not rule.custom_validator(value):
                    result.is_valid = False
                    result.errors.append(ValidationError(
                        field="",
                        validation_type=ValidationType.CUSTOM,
                        severity=ValidationSeverity.ERROR,
                        message=rule.error_message or "Custom validation failed",
                        value=value
                    ))
        
        except Exception as e:
            result.is_valid = False
            result.errors.append(ValidationError(
                field="",
                validation_type=ValidationType.CUSTOM,
                severity=ValidationSeverity.ERROR,
                message=f"Validation error: {str(e)}",
                value=value
            ))
        
        return result
    
    def _is_valid_email(self, email: str) -> bool:
        """
        Check if email is valid.
        
        Args:
            email: Email address
            
        Returns:
            bool: Is valid
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email)) and '@' in email
    
    def _is_valid_url(self, url: str) -> bool:
        """
        Check if URL is valid.
        
        Args:
            url: URL
            
        Returns:
            bool: Is valid
        """
        pattern = r'^https?://[^\s/$.?#].[^\s]*$'
        return bool(re.match(pattern, url))
    
    def sanitize(self, value: Any) -> ValidationResult:
        """
        Sanitize input value.
        
        Args:
            value: Value to sanitize
            
        Returns:
            ValidationResult: Sanitization result
        """
        result = ValidationResult(is_valid=True, value=value)
        
        if not self.config.enable_auto_sanitize:
            result.sanitized_value = value
            return result
        
        try:
            if isinstance(value, str):
                # Remove potentially dangerous characters
                sanitized = value.strip()
                sanitized = re.sub(r'<script[^>]*>.*?</script>', '', sanitized, flags=re.IGNORECASE | re.DOTALL)
                sanitized = re.sub(r'on\w+\s*=', '', sanitized, flags=re.IGNORECASE)
                result.sanitized_value = sanitized
            else:
                result.sanitized_value = value
        
        except Exception as e:
            result.is_valid = False
            result.errors.append(ValidationError(
                field="",
                validation_type=ValidationType.CUSTOM,
                severity=ValidationSeverity.ERROR,
                message=f"Sanitization error: {str(e)}",
                value=value
            ))
        
        return result
    
    def validate_dict(self, data: Dict[str, Any]) -> ValidationResult:
        """
        Validate dictionary of fields.
        
        Args:
            data: Dictionary of field values
            
        Returns:
            ValidationResult: Validation result
        """
        result = ValidationResult(is_valid=True)
        
        for field, value in data.items():
            field_result = self.validate(field, value)
            
            if not field_result.is_valid:
                result.is_valid = False
                result.errors.extend(field_result.errors)
                
                if self.config.stop_on_first_error:
                    break
        
        return result
    
    def get_rules(self, field: str) -> List[ValidationRule]:
        """
        Get rules for a field.
        
        Args:
            field: Field name
            
        Returns:
            List[ValidationRule]: Rules
        """
        return self.rules.get(field, [])
    
    def get_all_rules(self) -> Dict[str, List[ValidationRule]]:
        """
        Get all rules.
        
        Returns:
            Dict[str, List[ValidationRule]]: All rules
        """
        return self.rules
    
    def update_config(self, config: ValidationConfig) -> ValidationResult:
        """
        Update validation configuration.
        
        Args:
            config: New configuration
            
        Returns:
            ValidationResult: Update result
        """
        result = ValidationResult(is_valid=True)
        
        try:
            self.config = config
            result.message = "Config updated"
        except Exception as e:
            result.is_valid = False
            result.errors.append(ValidationError(
                field="",
                validation_type=ValidationType.CUSTOM,
                severity=ValidationSeverity.ERROR,
                message=f"Error updating config: {str(e)}"
            ))
        
        return result
    
    def get_config(self) -> ValidationConfig:
        """
        Get validation configuration.
        
        Returns:
            ValidationConfig: Configuration
        """
        return self.config


if __name__ == "__main__":
    # Basit test
    config = ValidationConfig()
    validator = InputValidator(config)
    
    # Rule ekle
    validator.add_rule("email", ValidationType.EMAIL)
    validator.add_rule("username", ValidationType.MIN_LENGTH, min_length=3)
    
    # Validate et
    result = validator.validate("email", "test@example.com")
    
    print(f"Valid: {result.is_valid}")
    
    # Dict validate et
    data = {"email": "test@example.com", "username": "john"}
    dict_result = validator.validate_dict(data)
    
    print(f"Dict valid: {dict_result.is_valid}")
