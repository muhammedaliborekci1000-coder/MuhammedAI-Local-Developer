"""
Quality Test: Input Validation
Input validation system testleri for security module.
"""

import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from app.security.input_validation import (
    ValidationType,
    DataType,
    ValidationSeverity,
    ValidationRule,
    ValidationError,
    ValidationConfig,
    ValidationResult,
    InputValidator
)


def test_validation_type_enum():
    """
    Test: ValidationType enum.
    """
    print("=" * 70)
    print("TEST: ValidationType Enum")
    print("=" * 70)
    
    assert ValidationType.REQUIRED.value == "required"
    assert ValidationType.MIN_LENGTH.value == "min_length"
    assert ValidationType.MAX_LENGTH.value == "max_length"
    assert ValidationType.PATTERN.value == "pattern"
    assert ValidationType.EMAIL.value == "email"
    assert ValidationType.URL.value == "url"
    
    print(f"  All enum values verified")
    print(f"  Total types: {len(ValidationType)}")
    
    print("\n" + "=" * 70)
    print("PASS: ValidationType enum")
    print("=" * 70)


def test_data_type_enum():
    """
    Test: DataType enum.
    """
    print("=" * 70)
    print("TEST: DataType Enum")
    print("=" * 70)
    
    assert DataType.STRING.value == "string"
    assert DataType.INTEGER.value == "integer"
    assert DataType.FLOAT.value == "float"
    assert DataType.BOOLEAN.value == "boolean"
    assert DataType.LIST.value == "list"
    assert DataType.DICT.value == "dict"
    assert DataType.ANY.value == "any"
    
    print(f"  All enum values verified")
    print(f"  Total types: {len(DataType)}")
    
    print("\n" + "=" * 70)
    print("PASS: DataType enum")
    print("=" * 70)


def test_validation_severity_enum():
    """
    Test: ValidationSeverity enum.
    """
    print("=" * 70)
    print("TEST: ValidationSeverity Enum")
    print("=" * 70)
    
    assert ValidationSeverity.ERROR.value == "error"
    assert ValidationSeverity.WARNING.value == "warning"
    assert ValidationSeverity.INFO.value == "info"
    
    print(f"  All enum values verified")
    print(f"  Total severities: {len(ValidationSeverity)}")
    
    print("\n" + "=" * 70)
    print("PASS: ValidationSeverity enum")
    print("=" * 70)


def test_validation_rule_dataclass():
    """
    Test: ValidationRule dataclass.
    """
    print("=" * 70)
    print("TEST: ValidationRule Dataclass")
    print("=" * 70)
    
    rule = ValidationRule(
        rule_id="rule_1",
        validation_type=ValidationType.REQUIRED,
        data_type=DataType.STRING
    )
    
    assert rule.rule_id == "rule_1", "Rule ID eşleşmeli"
    assert rule.validation_type == ValidationType.REQUIRED, "Validation type eşleşmeli"
    assert rule.data_type == DataType.STRING, "Data type eşleşmeli"
    
    print(f"  Rule ID: {rule.rule_id}")
    print(f"  Validation type: {rule.validation_type.value}")
    
    print("\n" + "=" * 70)
    print("PASS: ValidationRule dataclass")
    print("=" * 70)


def test_validation_error_dataclass():
    """
    Test: ValidationError dataclass.
    """
    print("=" * 70)
    print("TEST: ValidationError Dataclass")
    print("=" * 70)
    
    error = ValidationError(
        field="email",
        validation_type=ValidationType.EMAIL,
        severity=ValidationSeverity.ERROR,
        message="Invalid email"
    )
    
    assert error.field == "email", "Field eşleşmeli"
    assert error.validation_type == ValidationType.EMAIL, "Validation type eşleşmeli"
    assert error.severity == ValidationSeverity.ERROR, "Severity eşleşmeli"
    
    print(f"  Field: {error.field}")
    print(f"  Message: {error.message}")
    
    print("\n" + "=" * 70)
    print("PASS: ValidationError dataclass")
    print("=" * 70)


def test_validation_config_dataclass():
    """
    Test: ValidationConfig dataclass.
    """
    print("=" * 70)
    print("TEST: ValidationConfig Dataclass")
    print("=" * 70)
    
    config = ValidationConfig(strict_mode=True)
    
    assert config.strict_mode == True, "Strict mode eşleşmeli"
    
    print(f"  Strict mode: {config.strict_mode}")
    
    print("\n" + "=" * 70)
    print("PASS: ValidationConfig dataclass")
    print("=" * 70)


def test_validation_result_dataclass():
    """
    Test: ValidationResult dataclass.
    """
    print("=" * 70)
    print("TEST: ValidationResult Dataclass")
    print("=" * 70)
    
    result = ValidationResult(is_valid=True)
    
    assert result.is_valid == True, "Is valid eşleşmeli"
    assert isinstance(result.errors, list), "Errors list olmalı"
    assert isinstance(result.warnings, list), "Warnings list olmalı"
    
    print(f"  Is valid: {result.is_valid}")
    
    print("\n" + "=" * 70)
    print("PASS: ValidationResult dataclass")
    print("=" * 70)


def test_input_validator_initialization():
    """
    Test: InputValidator initialization.
    """
    print("=" * 70)
    print("TEST: InputValidator Initialization")
    print("=" * 70)
    
    config = ValidationConfig()
    validator = InputValidator(config)
    
    assert validator.config == config, "Config eşleşmeli"
    assert len(validator.rules) == 0, "Rules boş olmalı"
    
    print(f"  Rules: {len(validator.rules)}")
    
    print("\n" + "=" * 70)
    print("PASS: InputValidator initialization")
    print("=" * 70)


def test_add_rule():
    """
    Test: Add rule.
    """
    print("=" * 70)
    print("TEST: Add Rule")
    print("=" * 70)
    
    validator = InputValidator()
    
    result = validator.add_rule("email", ValidationType.EMAIL)
    
    assert result.is_valid == True, "Ekleme başarılı olmalı"
    assert "email" in validator.rules, "Rule eklenmeli"
    
    print(f"  Rule added: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add rule")
    print("=" * 70)


def test_remove_rule():
    """
    Test: Remove rule.
    """
    print("=" * 70)
    print("TEST: Remove Rule")
    print("=" * 70)
    
    validator = InputValidator()
    
    result = validator.add_rule("email", ValidationType.EMAIL)
    rule_id = validator.rules["email"][0].rule_id
    
    result = validator.remove_rule("email", rule_id)
    
    assert result.is_valid == True, "Silme başarılı olmalı"
    
    print(f"  Rule removed: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Remove rule")
    print("=" * 70)


def test_validate_required():
    """
    Test: Validate required.
    """
    print("=" * 70)
    print("TEST: Validate Required")
    print("=" * 70)
    
    validator = InputValidator()
    validator.add_rule("username", ValidationType.REQUIRED)
    
    result = validator.validate("username", "")
    
    assert result.is_valid == False, "Required field boş olmamalı"
    
    print(f"  Valid: {result.is_valid}")
    
    print("\n" + "=" * 70)
    print("PASS: Validate required")
    print("=" * 70)


def test_validate_min_length():
    """
    Test: Validate min length.
    """
    print("=" * 70)
    print("TEST: Validate Min Length")
    print("=" * 70)
    
    validator = InputValidator()
    validator.add_rule("username", ValidationType.MIN_LENGTH, min_length=5)
    
    result = validator.validate("username", "abc")
    
    assert result.is_valid == False, "Min length hatası olmalı"
    
    print(f"  Valid: {result.is_valid}")
    
    print("\n" + "=" * 70)
    print("PASS: Validate min length")
    print("=" * 70)


def test_validate_max_length():
    """
    Test: Validate max length.
    """
    print("=" * 70)
    print("TEST: Validate Max Length")
    print("=" * 70)
    
    validator = InputValidator()
    validator.add_rule("username", ValidationType.MAX_LENGTH, max_length=5)
    
    result = validator.validate("username", "abcdefghijk")
    
    assert result.is_valid == False, "Max length hatası olmalı"
    
    print(f"  Valid: {result.is_valid}")
    
    print("\n" + "=" * 70)
    print("PASS: Validate max length")
    print("=" * 70)


def test_validate_email():
    """
    Test: Validate email.
    """
    print("=" * 70)
    print("TEST: Validate Email")
    print("=" * 70)
    
    validator = InputValidator()
    validator.add_rule("email", ValidationType.EMAIL)
    
    result = validator.validate("email", "invalid-email")
    
    assert result.is_valid == False, "Invalid email hatası olmalı"
    
    print(f"  Valid: {result.is_valid}")
    
    print("\n" + "=" * 70)
    print("PASS: Validate email")
    print("=" * 70)


def test_validate_url():
    """
    Test: Validate URL.
    """
    print("=" * 70)
    print("TEST: Validate URL")
    print("=" * 70)
    
    validator = InputValidator()
    validator.add_rule("website", ValidationType.URL)
    
    result = validator.validate("website", "not-a-url")
    
    assert result.is_valid == False, "Invalid URL hatası olmalı"
    
    print(f"  Valid: {result.is_valid}")
    
    print("\n" + "=" * 70)
    print("PASS: Validate URL")
    print("=" * 70)


def test_validate_numeric():
    """
    Test: Validate numeric.
    """
    print("=" * 70)
    print("TEST: Validate Numeric")
    print("=" * 70)
    
    validator = InputValidator()
    validator.add_rule("age", ValidationType.NUMERIC)
    
    result = validator.validate("age", "not-a-number")
    
    assert result.is_valid == False, "Numeric hatası olmalı"
    
    print(f"  Valid: {result.is_valid}")
    
    print("\n" + "=" * 70)
    print("PASS: Validate numeric")
    print("=" * 70)


def test_sanitize():
    """
    Test: Sanitize.
    """
    print("=" * 70)
    print("TEST: Sanitize")
    print("=" * 70)
    
    config = ValidationConfig(enable_auto_sanitize=True)
    validator = InputValidator(config)
    
    result = validator.sanitize("<script>alert('xss')</script>")
    
    assert result.sanitized_value is not None, "Sanitized value olmalı"
    
    print(f"  Sanitized: {result.sanitized_value}")
    
    print("\n" + "=" * 70)
    print("PASS: Sanitize")
    print("=" * 70)


def test_validate_dict():
    """
    Test: Validate dict.
    """
    print("=" * 70)
    print("TEST: Validate Dict")
    print("=" * 70)
    
    validator = InputValidator()
    validator.add_rule("email", ValidationType.EMAIL)
    validator.add_rule("username", ValidationType.MIN_LENGTH, min_length=3)
    
    data = {"email": "test@example.com", "username": "john"}
    result = validator.validate_dict(data)
    
    assert result.is_valid == True, "Dict valid olmalı"
    
    print(f"  Valid: {result.is_valid}")
    
    print("\n" + "=" * 70)
    print("PASS: Validate dict")
    print("=" * 70)


def test_get_rules():
    """
    Test: Get rules.
    """
    print("=" * 70)
    print("TEST: Get Rules")
    print("=" * 70)
    
    validator = InputValidator()
    validator.add_rule("email", ValidationType.EMAIL)
    
    rules = validator.get_rules("email")
    
    assert len(rules) > 0, "Rule olmalı"
    
    print(f"  Rules: {len(rules)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get rules")
    print("=" * 70)


def test_get_all_rules():
    """
    Test: Get all rules.
    """
    print("=" * 70)
    print("TEST: Get All Rules")
    print("=" * 70)
    
    validator = InputValidator()
    validator.add_rule("email", ValidationType.EMAIL)
    validator.add_rule("username", ValidationType.MIN_LENGTH, min_length=3)
    
    rules = validator.get_all_rules()
    
    assert len(rules) > 0, "Rules olmalı"
    
    print(f"  Fields: {len(rules)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get all rules")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    validator = InputValidator()
    
    new_config = ValidationConfig(strict_mode=True)
    result = validator.update_config(new_config)
    
    assert result.is_valid == True, "Update başarılı olmalı"
    assert validator.config.strict_mode == True, "Config güncellenmeli"
    
    print(f"  Strict mode: {validator.config.strict_mode}")
    
    print("\n" + "=" * 70)
    print("PASS: Update config")
    print("=" * 70)


def test_get_config():
    """
    Test: Get config.
    """
    print("=" * 70)
    print("TEST: Get Config")
    print("=" * 70)
    
    config = ValidationConfig(strict_mode=True)
    validator = InputValidator(config)
    
    retrieved_config = validator.get_config()
    
    assert retrieved_config.strict_mode == True, "Config eşleşmeli"
    
    print(f"  Strict mode: {retrieved_config.strict_mode}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_validation_type_enum()
        test2 = test_data_type_enum()
        test3 = test_validation_severity_enum()
        test4 = test_validation_rule_dataclass()
        test5 = test_validation_error_dataclass()
        test6 = test_validation_config_dataclass()
        test7 = test_validation_result_dataclass()
        test8 = test_input_validator_initialization()
        test9 = test_add_rule()
        test10 = test_remove_rule()
        test11 = test_validate_required()
        test12 = test_validate_min_length()
        test13 = test_validate_max_length()
        test14 = test_validate_email()
        test15 = test_validate_url()
        test16 = test_validate_numeric()
        test17 = test_sanitize()
        test18 = test_validate_dict()
        test19 = test_get_rules()
        test20 = test_get_all_rules()
        test21 = test_update_config()
        test22 = test_get_config()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"ValidationType Enum: {'PASS' if test1 else 'FAIL'}")
        print(f"DataType Enum: {'PASS' if test2 else 'FAIL'}")
        print(f"ValidationSeverity Enum: {'PASS' if test3 else 'FAIL'}")
        print(f"ValidationRule Dataclass: {'PASS' if test4 else 'FAIL'}")
        print(f"ValidationError Dataclass: {'PASS' if test5 else 'FAIL'}")
        print(f"ValidationConfig Dataclass: {'PASS' if test6 else 'FAIL'}")
        print(f"ValidationResult Dataclass: {'PASS' if test7 else 'FAIL'}")
        print(f"InputValidator Initialization: {'PASS' if test8 else 'FAIL'}")
        print(f"Add Rule: {'PASS' if test9 else 'FAIL'}")
        print(f"Remove Rule: {'PASS' if test10 else 'FAIL'}")
        print(f"Validate Required: {'PASS' if test11 else 'FAIL'}")
        print(f"Validate Min Length: {'PASS' if test12 else 'FAIL'}")
        print(f"Validate Max Length: {'PASS' if test13 else 'FAIL'}")
        print(f"Validate Email: {'PASS' if test14 else 'FAIL'}")
        print(f"Validate URL: {'PASS' if test15 else 'FAIL'}")
        print(f"Validate Numeric: {'PASS' if test16 else 'FAIL'}")
        print(f"Sanitize: {'PASS' if test17 else 'FAIL'}")
        print(f"Validate Dict: {'PASS' if test18 else 'FAIL'}")
        print(f"Get Rules: {'PASS' if test19 else 'FAIL'}")
        print(f"Get All Rules: {'PASS' if test20 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test21 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test22 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14, test15, test16, test17, test18, test19, test20, test21, test22])
        print(f"\nTOPLAM: {'PASS' if all_passed else 'FAIL'}")
        print("=" * 70)
        
        sys.exit(0 if all_passed else 1)
    except Exception as e:
        print(f"\nTEST HATASI:")
        print("-" * 70)
        import traceback
        traceback.print_exc()
        print("=" * 70)
        sys.exit(1)
