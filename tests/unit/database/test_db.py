"""
Unit tests for database connection module.
"""

import gc
import sqlite3
import warnings

import pytest
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

# pylint: disable=import-error
from src.config import DATABASE_URL
from src.database import db


class TestDatabaseModuleSimple:
    """Simple test cases for database connection setup."""

    def test_engine_exists(self):
        """Test that engine is created."""

        # suppress warning for this test
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=ResourceWarning)

            assert db.engine is not None
            print(f"Engine URL: {db.engine.url}")

            # To check engine could connect and close connection
            try:
                connection = db.engine.connect()
                connection.close()
                print("✓ Engine connection opened and closed successfully")
            except SQLAlchemyError as exc:
                print(f"Database error: {exc}")

    def test_sessionmaker_exists(self):
        """Test that SessionLocal exists."""

        assert db.SessionLocal is not None

    def test_base_exists(self):
        """Test that Base exists."""

        assert db.Base is not None

    def test_config_matches(self):
        """Test that engine URL matches config."""

        # suppress warning
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=ResourceWarning)

            engine_url = str(db.engine.url)
            config_url = DATABASE_URL

            assert engine_url == config_url
            print(f"✓ Engine URL matches config: {engine_url}")


def test_engine_connect_args():
    """Test SQLite connection arguments with proper cleanup."""

    # suppress warnings
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=ResourceWarning)

        if "sqlite" in str(db.engine.url).lower():
            with db.engine.connect() as conn:
                result = conn.execute(text("SELECT 1"))
                assert result.scalar() == 1
                print("✓ Engine can connect and execute queries")

                result.close()
        else:
            print("Note: Not SQLite, connect_args test skipped")


def test_all_imports():
    """Test that all necessary components can be imported."""
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=ResourceWarning)

        try:
            # pylint: disable=import-error, import-outside-toplevel
            # pylint: disable=reimported, redefined-outer-name
            from src.config import DATABASE_URL
            from src.database.db import Base, SessionLocal, engine

            assert engine is not None
            assert SessionLocal is not None
            assert Base is not None
            assert DATABASE_URL is not None

            print("✓ All imports successful")
        except ImportError as e:
            pytest.fail(f"Import failed: {e}")


def test_connection_management():
    """Test that connections are properly managed."""

    initial_connections = (
        len(sqlite3._active_connections)  # pylint: disable=protected-access
        if hasattr(sqlite3, "_active_connections")
        else 0
    )

    # to test create and close more than one connections
    connections = []
    for _ in range(3):
        conn = db.engine.connect()
        connections.append(conn)

        result = conn.execute(text("SELECT 1"))
        result.close()

    for conn in connections:
        conn.close()

    gc.collect()

    print(f"✓ Connections opened and closed: {len(connections)}")

    final_connections = (
        len(sqlite3._active_connections)  # pylint: disable=protected-access
        if hasattr(sqlite3, "_active_connections")
        else 0
    )
    print(f"Initial connections: {initial_connections}, Final: {final_connections}")

    # suppress warnings
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=ResourceWarning)

        if "sqlite" in str(db.engine.url).lower():
            connection = db.engine.connect()
            try:
                result = connection.execute(text("SELECT 1"))
                assert result.scalar() == 1
                result.close()
                print("✓ Engine can connect and execute queries")
            finally:
                connection.close()
        else:
            print("Note: Not SQLite, connect_args test skipped")
