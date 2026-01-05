"""
Contact Repository Module

This module provides CRUD (Create, Read, Update, Delete) operations
for the Contact model using SQLAlchemy ORM.
It abstracts database
interactions and ensures a clean separation between business logic
and persistence layer.
"""

from sqlalchemy import func
from sqlalchemy.orm import Session

from database.models import Contact


def create(db: Session, contact: Contact) -> Contact:
    """
    Create a new contact in the database.

    :param db: SQLAlchemy session object.
    :param contact: Contact instance to be added.
    :return: The persisted Contact object.
    """
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


def get_all(db: Session) -> list[Contact]:
    """
    Retrieve all contacts from the database.

    :param db: SQLAlchemy session object.
    :return: List of Contact objects ordered by creation date (descending).
    """
    return db.query(Contact).order_by(func.lower(Contact.first_name)).all()


def get_by_id(db: Session, contact_id: int) -> Contact | None:
    """
    Retrieve a contact by its ID.

    :param db: SQLAlchemy session object.
    :param contact_id: Unique identifier of the contact.
    :return: Contact object if found, otherwise None.
    """
    return db.query(Contact).filter(Contact.id == contact_id).first()


def get_by_phone(db: Session, phone: str) -> Contact | None:
    """
    Retrieve a contact by its phone number.

    :param db: SQLAlchemy session object.
    :param phone: Phone number of the contact.
    :return: Contact object if found, otherwise None.
    """
    return db.query(Contact).filter(Contact.phone == phone).first()


def get_by_email(db: Session, email: str) -> Contact | None:
    """
    Retrieve a contact by its email address.

    :param db: SQLAlchemy session object.
    :param email: Email address of the contact.
    :return: Contact object if found, otherwise None.
    """
    return db.query(Contact).filter(Contact.email == email).first()


def update(db: Session, contact: Contact) -> Contact:
    """
    Update an existing contact in the database.

    :param db: SQLAlchemy session object.
    :param contact: Contact instance with updated fields.
    :return: The updated Contact object.
    """
    db.commit()
    db.refresh(contact)
    return contact


def delete(db: Session, contact: Contact) -> None:
    """
    Delete a contact from the database.

    :param db: SQLAlchemy session object.
    :param contact: Contact instance to be removed.
    :return: None
    """
    db.delete(contact)
    db.commit()
