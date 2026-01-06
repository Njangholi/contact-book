"""
Validation Utilities

This module provides helper functions for validating and normalizing
user input fields such as names, phone numbers, and email addresses.
It is used by the service layer before persisting data to the database.
"""

import re

EMAIL_REGEX = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"


def validate_name_pair(first_name: str, last_name: str) -> tuple[bool, str]:
    """
    Validate that at least one of the name fields is provided.

    :param first_name: The first name provided by the user.
    :param last_name: The last name provided by the user.
    :return: A tuple containing a boolean indicating validity and an error message if invalid.
    """
    if not first_name.strip() and not last_name.strip():
        return (False, "At least one of First Name or Last Name must be provided.")
    return True, ""


def normalize_phone(phone: str) -> str:
    """
    Normalize phone number by removing spaces, dashes, and parentheses.

    :param phone: Raw phone number input.
    :return: Normalized phone number containing only digits and optional leading '+'.
    """
    return re.sub(r"[\s\-\(\)]", "", phone)


def validate_phone(phone: str) -> tuple[bool, list[str]]:
    """
    Validate a phone number for format, allowed characters, and length.

    :param phone: Raw phone number input.
    :return: A tuple containing a boolean validity flag and a list of error messages.
    """
    errors = []
    validate = True
    phone = normalize_phone(phone)
    if not phone:
        validate = False
        errors.append("Please provide a phone number.")

    if not phone.startswith("+") and not phone.isdigit():
        validate = False
        errors.append(
            "Phone number must start with a '+' sign and contain only digits."
        )

    digits = phone[1:] if phone.startswith("+") else phone
    if len(digits) < 7 or len(digits) > 15:
        validate = False
        errors.append("Phone number must be between 7 and 15 digits long.")

    return validate, errors


def normalize_email(email: str | None) -> str | None:
    """
    Normalize an email address by trimming whitespace and converting to lowercase.

    If the email is empty or ``None``, the function returns ``None`` so that
    the database can store it as a NULL value.

    :param email: Raw email input.
    :return: Normalized email or ``None``.
    """
    if not email:
        return None
    return email.strip().lower()


def validate_email(email: str | None) -> tuple[bool, str | None]:
    """
    Validate an email address using a regular expression.

    :param email: Email address to validate.
    :return: A tuple containing a boolean validity flag and an optional error message.
    """
    if not email:
        return True, None

    if not re.match(EMAIL_REGEX, email):
        return False, "Email format is invalid (example: name@email.com)"
    return True, None
