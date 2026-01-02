"""Contact Book Models Module
This module defines the database models using SQLAlchemy ORM.
"""

from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String

from database.db import Base


class Contact(Base):
    """Contact Model

    :param Base: The base class for all ORM models.
    :type Base: declarative_base()
    """

    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True, nullable=False)
    last_name = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=True)
    phone = Column(String, unique=True, index=True, nullable=False)
    category = Column(String, index=True, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
