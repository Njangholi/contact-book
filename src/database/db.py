"""Contact Book Database Module
This module sets up the database connection and session management
using SQLAlchemy."""

import atexit
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import StaticPool

from config import DATABASE_URL


def create_database_engine():
    """Create and configure the database engine."""
    engine_args = {
        "connect_args": {"check_same_thread": False},
        "echo": False,  # True for debug the sqlite queries
    }

    # Use static pool for sqlite
    if DATABASE_URL.startswith("sqlite"):
        engine_args["poolclass"] = StaticPool

    return create_engine(DATABASE_URL, **engine_args)


# create engine lazy(only it needed)
# pylint: disable=invalid-name
_engine = None
_SessionLocal = None
_Base = None


# pylint: disable=global-statement
def get_engine():
    """Get or create the database engine (singleton)."""
    global _engine
    if _engine is None:
        _engine = create_database_engine()
    return _engine


def get_session_local():
    """Get or create the sessionmaker (singleton)."""
    global _SessionLocal
    if _SessionLocal is None:
        _SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=get_engine()
        )
    return _SessionLocal


def get_base():
    """Get or create the declarative base (singleton)."""
    global _Base
    if _Base is None:
        _Base = declarative_base()
    return _Base


# for backward compatibility
engine = get_engine()
SessionLocal = get_session_local()
Base = get_base()


def cleanup_database():
    """Clean up database connections."""
    global _engine
    if _engine:
        _engine.dispose()
        _engine = None
        print("Database connections cleaned up")


@contextmanager
def get_db():
    """Dependency to get database session with automatic cleanup."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# print cleanup message after closing program
atexit.register(cleanup_database)
