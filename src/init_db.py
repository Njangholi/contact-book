"""
Database Initialization Module
==============================

This module is responsible for initializing the application's database.
It imports the SQLAlchemy ``Base`` metadata and engine, loads all model
definitions, and ensures that the required tables are created before the
application starts.

The module is typically executed at the beginning of a CLI command
to guarantee that the database schema exists.
"""

# pylint: disable=unused-import
from database import models  # noqa: F401
from database.db import Base, engine


def init_db():
    """
    Initialize the database by creating all tables defined in the metadata.

    This function calls ``Base.metadata.create_all`` using the configured
    SQLAlchemy engine. If the tables already exist, the operation is skipped.

    :return: None
    :rtype: None
    """
    Base.metadata.create_all(bind=engine)
    print("Database initialized with all tables successfully.")


if __name__ == "__main__":
    init_db()
