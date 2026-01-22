"""
Unit tests for validation utilities.
"""

import pytest

from src.utils.validation import (
    normalize_email,
    normalize_phone,
    validate_email,
    validate_name_pair,
    validate_phone,
)


class TestValidationUtilities:
    """Test cases for validation functions."""

    # Test validate_name_pair
    @pytest.mark.parametrize(
        "first_name, last_name, expected_valid, expected_msg_contains",
        [
            ("John", "Doe", True, ""),
            ("John", "", True, ""),
            ("", "Doe", True, ""),
            ("  ", "  ", False, "must be provided"),
            ("", "", False, "must be provided"),
            ("  John  ", "  Doe  ", True, ""),  # With spaces
        ],
    )
    def test_validate_name_pair(
        self, first_name, last_name, expected_valid, expected_msg_contains
    ):
        """Test name pair validation with various inputs."""
        # Act
        is_valid, message = validate_name_pair(first_name, last_name)

        # Assert
        assert is_valid == expected_valid
        if expected_msg_contains:
            assert expected_msg_contains in message
        else:
            assert message == ""

    # Test normalize_phone
    @pytest.mark.parametrize(
        "input_phone, expected_output",
        [
            ("+1 (234) 567-890", "+1234567890"),
            ("123-456-7890", "1234567890"),
            ("+98 912 345 6789", "+989123456789"),
            (" 123 456 7890 ", "1234567890"),
            ("(123)456-7890", "1234567890"),
            ("+1-800-555-1234", "+18005551234"),
            ("", ""),
            ("+1234567890", "+1234567890"),  # Already normalized
        ],
    )
    def test_normalize_phone(self, input_phone, expected_output):
        """Test phone number normalization."""
        # Act
        result = normalize_phone(input_phone)

        # Assert
        assert result == expected_output

    # Test validate_phone
    @pytest.mark.parametrize(
        "input_phone, expected_valid, expected_errors_count",
        [
            ("+1234567890", True, 0),  # Valid with plus
            ("1234567890", True, 0),  # Valid without plus
            ("+1 234 567 890", True, 0),  # Will be normalized
            ("", False, 1),  # Empty
            ("abc", False, 1),  # Non-digits with plus
            ("+123", False, 1),  # Too short
            ("+1234567890123456", False, 1),  # Too long
            ("123-456-7890", True, 0),  # Contains dashes (will be normalized)
            ("+1-800-555-1234", True, 0),  # Complex format
            ("+abc123", False, 1),  # Non-digits after +
        ],
    )
    def test_validate_phone(self, input_phone, expected_valid, expected_errors_count):
        """Test phone number validation."""
        # Act
        is_valid, errors = validate_phone(input_phone)

        # Assert
        assert is_valid == expected_valid
        assert len(errors) == expected_errors_count

    # Test normalize_email
    @pytest.mark.parametrize(
        "input_email, expected_output",
        [
            ("John.Doe@Example.com", "john.doe@example.com"),
            ("  test@example.com  ", "test@example.com"),
            ("", None),
            (None, None),
            ("UPPER@DOMAIN.COM", "upper@domain.com"),
            ("  mixed.CASE@Domain.Com  ", "mixed.case@domain.com"),
        ],
    )
    def test_normalize_email(self, input_email, expected_output):
        """Test email normalization."""
        # Act
        result = normalize_email(input_email)

        # Assert
        assert result == expected_output

    # Test validate_email
    @pytest.mark.parametrize(
        "input_email, expected_valid, expected_error_contains",
        [
            ("test@example.com", True, None),
            ("user.name@domain.co.uk", True, None),
            ("", True, None),  # Empty email is allowed
            (None, True, None),  # None is allowed
            ("invalid-email", False, "invalid"),
            ("missing@domain", False, "invalid"),
            ("@domain.com", False, "invalid"),
            ("test@.com", False, "invalid"),
            ("test@domain.", False, "invalid"),
            (" test@example.com ", True, None),  # Will be normalized
        ],
    )
    def test_validate_email(self, input_email, expected_valid, expected_error_contains):
        """Test email validation."""
        # Act
        is_valid, error_message = validate_email(input_email)

        # Assert
        assert is_valid == expected_valid
        if expected_error_contains:
            assert expected_error_contains in error_message
        else:
            assert error_message is None

    def test_validate_phone_error_messages(self):
        """Test specific error messages from phone validation."""
        # Test empty phone
        is_valid, errors = validate_phone("")
        assert not is_valid
        assert "Please provide a phone number" in errors[0]

        # Test invalid characters
        is_valid, errors = validate_phone("+abc123")
        assert not is_valid
        assert "must contain only digits after '+' sign" in errors[0]

        # Test invalid characters
        is_valid, errors = validate_phone("abcdefgh")
        assert not is_valid
        assert "must contain only digits" in errors[0]

        # Test too short
        is_valid, errors = validate_phone("+123")
        assert not is_valid
        assert "between 7 and 15 digits" in errors[0]

        # Test too long
        is_valid, errors = validate_phone("+1234567890123456")
        assert not is_valid
        assert "between 7 and 15 digits" in errors[0]
