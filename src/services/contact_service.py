from sqlalchemy.orm import Session

from crud import contacts as contact_crud
from database.models import Contact
from utils.validation import (normalize_email, normalize_phone, validate_email,
                              validate_name_pair, validate_phone)


class ContactServiceError(Exception):
    def __init__(self, errors: list[str]):
        self.errors = errors
        super().__init__("Contact service error")


def add_contact(db: Session, data: dict) -> Contact:
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
    return contact_crud.get_all(db)


def update_contact(db: Session, contact_id: int, data: dict) -> Contact:
    contact = contact_crud.get_by_id(db, contact_id)
    if not contact:
        raise ContactServiceError(["Contact not found"])

    if "first_name" in data:
        contact.first_name = data["first_name"]
    if "last_name" in data:
        contact.last_name = data["last_name"]

    if "phone" in data:
        phone_valid, phone_error = validate_phone(data["phone"])
        if not phone_valid:
            raise ContactServiceError([phone_error])
        contact.phone = normalize_phone(data["phone"])

    if "email" in data:
        email_valid, email_error = validate_email(data["email"])
        if not email_valid:
            raise ContactServiceError([email_error])
        contact.email = normalize_email(data["email"])

    if "category" in data:
        contact.category = data["category"]

    return contact_crud.update(db, contact)


def delete_contact(db: Session, contact_id: int) -> None:
    contact = contact_crud.get_by_id(db, contact_id)
    if not contact:
        raise ContactServiceError(["Contact not found"])

    contact_crud.delete(db, contact)
