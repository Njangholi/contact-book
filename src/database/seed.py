"""
This module seeds the database with demo contacts if none exist.
It checks for existing contacts and adds predefined ones if the database is empty.
Suitable for initial setup or testing purposes.
"""

from sqlalchemy.orm import Session

from src.database.db import SessionLocal
from src.services.contact_service import add_contact, list_contacts

# Initialize database session
db: Session = SessionLocal()


def seed_demo_contacts() -> None:
    """Seeds the database with demo contacts if none exist."""

    if len(list_contacts(db)) > 0:
        return

    add_contact(
        db,
        data={
            "first_name": "Alice",
            "last_name": "Johnson",
            "phone": "+49 151 12345678",
            "email": "alice@example.com",
            "category": "Friends",
        },
    )

    add_contact(
        db,
        data={
            "first_name": "Bob",
            "last_name": "Smith",
            "phone": "+49 160 98765432",
            "email": "bob@example.com",
            "category": "Work",
        },
    )

    add_contact(
        db,
        data={
            "first_name": "John",
            "last_name": "Doe",
            "phone": "+49 170 1234567",
            "email": "John@example.com",
            "category": "Work",
        },
    )
