"""
This module ensures the database is initialized before use.
It checks for the existence of required tables and creates them if absent.
"""

from sqlalchemy import inspect

from .db import Base, engine


def ensure_database_initialized() -> None:
    """
    Ensure the database is initialized by creating necessary tables
    if they do not exist.
    """
    inspector = inspect(engine)

    if not inspector.has_table("contacts"):
        Base.metadata.create_all(bind=engine)
