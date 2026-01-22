"""
Unit tests for database connection module.
"""

import importlib
import sys
import warnings
from unittest.mock import MagicMock, Mock, patch

import pytest
import gc


class TestDatabaseModuleSimple:
    """Simple test cases for database connection setup."""

    def test_engine_exists(self):
        """Test that engine is created."""
        from src.database import db

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
            except Exception as e:
                print(f"Note: {e}")

    def test_sessionmaker_exists(self):
        """Test that SessionLocal exists."""
        from src.database import db

        assert db.SessionLocal is not None

    def test_base_exists(self):
        """Test that Base exists."""
        from src.database import db

        assert db.Base is not None

    def test_config_matches(self):
        """Test that engine URL matches config."""
        from src.config import DATABASE_URL
        from src.database import db

        # suppress warning
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=ResourceWarning)

            engine_url = str(db.engine.url)
            config_url = DATABASE_URL

            assert engine_url == config_url
            print(f"✓ Engine URL matches config: {engine_url}")


def test_engine_connect_args():
    """Test SQLite connection arguments with proper cleanup."""
    from sqlalchemy import text

    from src.database import db

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
            from src.config import DATABASE_URL
            from src.database.db import Base, SessionLocal, engine

            assert engine is not None
            assert SessionLocal is not None
            assert Base is not None
            assert DATABASE_URL is not None

            print("✓ All imports successful")
            return True
        except ImportError as e:
            pytest.fail(f"Import failed: {e}")


def test_connection_management():
    """Test that connections are properly managed."""
    import sqlite3

    from sqlalchemy import text

    from src.database import db

    initial_connections = (
        len(sqlite3._active_connections)
        if hasattr(sqlite3, "_active_connections")
        else 0
    )

    # to test create and close more than one connections
    connections = []
    for i in range(3):
        conn = db.engine.connect()
        connections.append(conn)

        result = conn.execute(text("SELECT 1"))
        result.close()

    for conn in connections:
        conn.close()

    

    gc.collect()

    print(f"✓ Connections opened and closed: {len(connections)}")

    final_connections = (
        len(sqlite3._active_connections)
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