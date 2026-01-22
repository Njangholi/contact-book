"""
Shared test fixtures for the Contact Book application.
"""

import gc
import warnings
from unittest.mock import Mock

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.database.db import Base, cleanup_database
from src.database.models import Contact

# Suprress some warnings
warnings.filterwarnings("ignore", category=ResourceWarning)


@pytest.fixture(scope="function")
def mock_db_session():
    """Create a mock database session for unit tests."""
    mock_session = Mock()

    # Mock common session methods
    mock_session.query = Mock()
    mock_session.add = Mock()
    mock_session.commit = Mock()
    mock_session.refresh = Mock()
    mock_session.delete = Mock()
    mock_session.filter = Mock()
    mock_session.all = Mock()
    mock_session.first = Mock()

    mock_query = Mock()
    mock_session.query.return_value = mock_query

    return mock_session


@pytest.fixture(scope="function")
def test_db_session():
    """
    Create a real in-memory SQLite database for integration tests.
    Properly closes connections after each test.
    """
    # Create an in-memory SQLite database
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        # Add pool to manage connection
        poolclass=None,
    )

    testing_session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Create all tables
    Base.metadata.create_all(bind=engine)

    # Create a session
    db = testing_session_local()

    try:
        yield db
    finally:
        # Close session
        db.close()

        # Close all connections
        engine.dispose()


@pytest.fixture
def sample_contact_data():
    """Return sample contact data for testing."""
    return {
        "first_name": "John",
        "last_name": "Doe",
        "phone": "+1234567890",
        "email": "john.doe@example.com",
        "category": "Friends",
    }


@pytest.fixture
def sample_contact():
    """Create and return a sample Contact object."""

    return Contact(
        id=1,
        first_name="John",
        last_name="Doe",
        phone="+1234567890",
        email="john.doe@example.com",
        category="Friends",
    )


@pytest.fixture(scope="session")
def test_engine():
    """Create engine for all tests, dispose at the end."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=None,
    )
    testing_session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Create all tables
    Base.metadata.create_all(bind=engine)

    # Create a session
    db = testing_session_local()

    try:
        yield db
    finally:
        # بستن session
        db.close()

        # dispose engine
        engine.dispose()

        # Help Garbage collector
        gc.collect()


@pytest.fixture(scope="session", autouse=True)
def cleanup_after_all_tests():
    """Clean up after all tests are done."""
    yield

    # Final cleanup
    cleanup_database()

    # Help Garbage collector

    gc.collect()
    print("All tests completed, resources cleaned up")


# To manage warnings
@pytest.fixture(autouse=True)
def setup_and_teardown():
    """Setup and teardown for each test."""
    # Before test
    warnings.simplefilter("always", ResourceWarning)

    yield

    # Help Garbage collector
    gc.collect()
