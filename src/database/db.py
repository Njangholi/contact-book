"""
Contact Book Database Module

This module handles database engine creation, session management,
and ORM base initialization using SQLAlchemy.

The design is intentionally test-friendly:
- Lazy initialization
- Singleton pattern for shared components
- SQLite StaticPool support for reliable testing
"""

import atexit
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import StaticPool

from config import DATABASE_URL


# ------------------------------------------------------------
# Engine factory
# ------------------------------------------------------------
# Creates and configures the SQLAlchemy engine.
# Engine creation is separated to allow customization and
# easier testing (e.g., swapping DATABASE_URL).
def create_database_engine():
    """Create and configure the database engine."""
    engine_args = {
        "connect_args": {"check_same_thread": False},
        "echo": False,  # Enable SQL query logging for debugging if needed
    }

    # SQLite requires StaticPool to keep the same connection alive.
    # This is critical for in-memory databases during testing,
    # otherwise each session would see a fresh empty database.
    if DATABASE_URL.startswith("sqlite"):
        engine_args["poolclass"] = StaticPool

    return create_engine(DATABASE_URL, **engine_args)


# ------------------------------------------------------------
# Lazy singletons for database components
# ------------------------------------------------------------
# These globals ensure:
# - Only one engine is created
# - Session factory is shared
# - Declarative Base remains consistent across imports
#
# Lazy initialization prevents side effects at import time
# and gives tests full control over database lifecycle.

# pylint: disable=invalid-name
_engine = None
_SessionLocal = None
_Base = None


# ------------------------------------------------------------
# Engine accessor (singleton)
# ------------------------------------------------------------
# Creates the engine only when first requested.
# This avoids early database connections during import
# and makes the module safer for testing.


# pylint: disable=global-statement
def get_engine():
    """Get or create the database engine (singleton)."""
    global _engine
    if _engine is None:
        _engine = create_database_engine()
    return _engine


# ------------------------------------------------------------
# Session factory accessor (singleton)
# ------------------------------------------------------------
# Returns a configured sessionmaker bound to the shared engine.
# Keeping this centralized ensures consistent session behavior
# across the entire application.
def get_session_local():
    """Get or create the sessionmaker (singleton)."""
    global _SessionLocal
    if _SessionLocal is None:
        _SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=get_engine()
        )
    return _SessionLocal


# ------------------------------------------------------------
# Declarative Base accessor (singleton)
# ------------------------------------------------------------
# Ensures all ORM models inherit from the same Base instance.
# This is essential for correct table registration and metadata handling.
def get_base():
    """Get or create the declarative base (singleton)."""
    global _Base
    if _Base is None:
        _Base = declarative_base()
    return _Base


# ------------------------------------------------------------
# Backward-compatible exports
# ------------------------------------------------------------
# These allow importing engine, SessionLocal, and Base directly
# while still benefiting from lazy initialization internally.
engine = get_engine()
SessionLocal = get_session_local()
Base = get_base()


# ------------------------------------------------------------
# Cleanup logic
# ------------------------------------------------------------
# Properly disposes the engine when the application exits.
# This helps prevent hanging connections during development
# and repeated test runs.
def cleanup_database():
    """Clean up database connections."""
    global _engine
    if _engine:
        _engine.dispose()
        _engine = None
        print("Database connections cleaned up")


# ------------------------------------------------------------
# Context-managed session dependency
# ------------------------------------------------------------
# Provides a safe way to work with database sessions.
# Ensures sessions are always closed, even if an exception occurs.
#
# Suitable for:
# - service layer usage
# - CLI scripts
# - future integration with frameworks like FastAPI
@contextmanager
def get_db():
    """Dependency to get database session with automatic cleanup."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Register cleanup to run automatically on program exit
atexit.register(cleanup_database)
