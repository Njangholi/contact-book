"""Contact Book Models Module
This module defines the database models using SQLAlchemy ORM.
"""

from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, String

from src.database.db import Base


class Contact(Base):
    """Contact ORM model representing the contacts table."""

    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True, nullable=False)
    last_name = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=True)
    phone = Column(String, unique=True, index=True, nullable=False)
    category = Column(String, index=True, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self):
        return f"""<Contact(id={self.id},
            name='{self.first_name} {self.last_name}',
            phone='{self.phone}')>"""

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.phone})"
