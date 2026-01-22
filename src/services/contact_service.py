"""
Contact Service Module

This module provides higher-level service functions for managing contacts.
It applies validation rules before delegating persistence operations to
the CRUD layer. Errors are wrapped in a custom ``ContactServiceError``.
"""

from sqlalchemy.orm import Session

from crud import contacts as contact_crud
from database.models import Contact
from utils.validation import (
    normalize_email,
    normalize_phone,
    validate_email,
    validate_name_pair,
    validate_phone,
)


class ContactServiceError(Exception):
    """
    Exception raised for errors in the contact service layer.

    :param errors: List of error messages describing validation or service issues.
    :type errors: list[str]
    """

    def __init__(self, errors: list[str]):
        self.errors = errors
        super().__init__("Contact service error")


def get_contact(db: Session, contact_id: int) -> Contact:
    """
    Getting contact by id from CRUD

    :param db: QLAlchemy session object.
    :param contact_id: Unique identifier of the contact.
    :raises ContactServiceError: If contact not found.
    :return: The Contact object.
    """
    contact = contact_crud.get_by_id(db, contact_id)
    if not contact:
        raise ContactServiceError(["Contact not found"])
    return contact


def add_contact(db: Session, data: dict) -> Contact:
    """
    Validate and add a new contact to the database.

    :param db: SQLAlchemy session object.
    :param data: Dictionary containing contact fields
    (first_name, last_name, phone, email, category).
    :raises ContactServiceError: If validation fails or duplicate phone/email exists.
    :return: The persisted Contact object.
    """
    errors = []

    # ---- Name rules ----
    valid, msg = validate_name_pair(data["first_name"], data["last_name"])
    if not valid:
        errors.append(msg)

    # ---- Phone rules ----
    phone_raw = data.get("phone", "")
    phone_valid, phone_error = validate_phone(phone_raw)
    phone = normalize_phone(phone_raw)
    if not phone_valid:
        errors.extend(phone_error)
    elif phone and contact_crud.get_by_phone(db, phone):
        errors.append("📞 Phone number already exists.")

    # ---- Email rules ----
    email_raw = data.get("email", "")
    email = normalize_email(email_raw)
    email_valid, email_error = validate_email(email)
    if not email_valid:
        errors.append(email_error)
    elif email and contact_crud.get_by_email(db, email):
        errors.append("📧 Email already exists.")

    if errors:
        raise ContactServiceError(errors)

    contact = Contact(
        first_name=data["first_name"].strip(),
        last_name=data["last_name"].strip(),
        phone=phone,
        email=email,
        category=data.get("category"),
    )

    return contact_crud.create(db, contact)


def list_contacts(db: Session) -> list[Contact]:
    """
    Retrieve all contacts from the database.

    :param db: SQLAlchemy session object.
    :return: List of Contact objects.
    """
    return contact_crud.get_all(db)


def update_contact(db: Session, contact_id: int, data: dict) -> Contact:
    """
    Update an existing contact in the database.

    :param db: SQLAlchemy session object.
    :param contact_id: Unique identifier of the contact to update.
    :param data: Dictionary of fields to update (first_name, last_name,
                phone, email, category).
    :raises ContactServiceError: If contact not found or validation fails.
    :return: The updated Contact object.
    """
    contact = contact_crud.get_by_id(db, contact_id)
    if not contact:
        raise ContactServiceError(["Contact not found"])

    errors: list[str] = []
    # ---- name validation (pair) ----
    first_name = data.get("first_name", contact.first_name)
    last_name = data.get("last_name", contact.last_name)

    name_valid, name_error = validate_name_pair(first_name, last_name)
    if not name_valid:
        errors.append(name_error)
    contact.first_name = first_name.strip()
    contact.last_name = last_name.strip()
    # ---- phone ----
    if "phone" in data:
        phone_valid, phone_error = validate_phone(data["phone"])
        if not phone_valid:
            errors.extend(phone_error)

        contact.phone = normalize_phone(data["phone"])

    # ---- email ----
    if "email" in data:
        email_valid, email_error = validate_email(data["email"])
        if not email_valid:
            errors.append(email_error)
        contact.email = normalize_email(data["email"])

    if errors:
        raise ContactServiceError(errors)

    if "category" in data:
        contact.category = data["category"]

    return contact_crud.update(db, contact)


def delete_contact(db: Session, contact_id: int) -> None:
    """
    Delete a contact from the database.

    :param db: SQLAlchemy session object.
    :param contact_id: Unique identifier of the contact to delete.
    :raises ContactServiceError: If contact not found.
    :return: None
    """
    contact = contact_crud.get_by_id(db, contact_id)
    if not contact:
        raise ContactServiceError(["Contact not found"])

    contact_crud.delete(db, contact)


def search_contacts(
    db: Session, query: str = "", categories: list[str] | None = None
) -> Contact:
    """
    Search contacts in the database by query string and optional categories.

    The function trims whitespace from the query string and ensures that
    categories is always a list. It then delegates the search operation
    to the CRUD layer.

    :param db: SQLAlchemy session object used to access the database.
    :param query: Free-text search query (e.g., part of a name, phone, or email).
    :param categories: Optional list of category names to filter contacts.
    :return: List of Contact objects matching the search criteria.
    """
    query = query.strip()
    categories = categories or []
    return contact_crud.search(db=db, query=query, categories=categories)
