from sqlalchemy.orm import Session
from database.models import Contact


def create(db: Session, contact: Contact) -> Contact:
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


def get_all(db: Session) -> list[Contact]:
    return db.query(Contact).order_by(Contact.created_at.desc()).all()


def get_by_id(db: Session, contact_id: int) -> Contact | None:
    return db.query(Contact).filter(Contact.id == contact_id).first()


def get_by_phone(db: Session, phone: str) -> Contact | None:
    return db.query(Contact).filter(Contact.phone == phone).first()


def get_by_email(db: Session, email: str) -> Contact | None:
    return db.query(Contact).filter(Contact.email == email).first()


def update(db: Session, contact: Contact) -> Contact:
    # db.merge(contact)
    db.commit()
    db.refresh(contact)
    return contact


def delete(db: Session, contact: Contact) -> None:
    # contact = db.query(Contact).filter(Contact.id == contact_id).first()
    # if contact:
    db.delete(contact)
    db.commit()
