from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from database.db import Base

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True, nullable=False)
    last_name = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=True) # Allow phone to be nullable
    phone = Column(String, unique=True, index=True, nullable=False) 
    category = Column(String, index=True, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)