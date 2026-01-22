"""
Unit tests for CRUD operations.
"""

from unittest.mock import MagicMock, Mock

from sqlalchemy.orm import Query

from crud.contacts import (
    create,
    delete,
    get_all,
    get_by_email,
    get_by_id,
    get_by_phone,
    search,
    update,
)
from database.models import Contact


class TestCRUDOperations:
    """Test cases for CRUD functions."""

    def test_create_contact(self, mock_db_session, sample_contact):
        """Test creating a new contact."""
        # Arrange
        mock_db_session.refresh = MagicMock(side_effect=lambda x: None)

        # Act
        result = create(mock_db_session, sample_contact)

        # Assert
        mock_db_session.add.assert_called_once_with(sample_contact)
        mock_db_session.commit.assert_called_once()
        mock_db_session.refresh.assert_called_once_with(sample_contact)
        assert result == sample_contact

    def test_get_all_contacts(self, mock_db_session, sample_contact):
        """Test retrieving all contacts."""
        # Arrange
        mock_query = Mock(spec=Query)
        mock_query.order_by.return_value = mock_query
        mock_query.all.return_value = [sample_contact]
        mock_db_session.query.return_value = mock_query

        # Act
        result = get_all(mock_db_session)

        # Assert
        mock_db_session.query.assert_called_once_with(Contact)
        assert len(result) == 1
        assert result[0] == sample_contact

    def test_get_by_id_found(self, mock_db_session, sample_contact):
        """Test getting contact by ID when contact exists."""
        # Arrange
        mock_query = Mock(spec=Query)
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = sample_contact
        mock_db_session.query.return_value = mock_query

        # Act
        result = get_by_id(mock_db_session, 1)

        # Assert
        mock_db_session.query.assert_called_once_with(Contact)
        mock_query.filter.assert_called_once()
        assert result == sample_contact

    def test_get_by_id_not_found(self, mock_db_session):
        """Test getting contact by ID when contact doesn't exist."""
        # Arrange
        mock_query = Mock(spec=Query)
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = None
        mock_db_session.query.return_value = mock_query

        # Act
        result = get_by_id(mock_db_session, 999)

        # Assert
        assert result is None

    def test_get_by_phone_found(self, mock_db_session, sample_contact):
        """Test getting contact by phone number."""
        # Arrange
        mock_query = Mock(spec=Query)
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = sample_contact
        mock_db_session.query.return_value = mock_query

        # Act
        result = get_by_phone(mock_db_session, "+1234567890")

        # Assert
        mock_db_session.query.assert_called_once_with(Contact)
        assert mock_query.filter.called
        assert mock_query.filter.call_count == 1
        assert result == sample_contact

        filter_args = mock_query.filter.call_args[0]
        assert len(filter_args) == 1
        print(f"Filter was called with: {filter_args[0]}")

    def test_get_by_email_found(self, mock_db_session, sample_contact):
        """Test getting contact by email."""
        # Arrange
        mock_query = Mock(spec=Query)
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = sample_contact
        mock_db_session.query.return_value = mock_query

        # Act
        result = get_by_email(mock_db_session, "john.doe@example.com")

        # Assert
        mock_db_session.query.assert_called_once_with(Contact)
        assert mock_query.filter.called
        assert mock_query.filter.call_count == 1
        assert result == sample_contact

        filter_args = mock_query.filter.call_args[0]
        assert len(filter_args) == 1
        print(f"Filter was called with: {filter_args[0]}")

    def test_update_contact(self, mock_db_session, sample_contact):
        """Test updating a contact."""
        # Act
        result = update(mock_db_session, sample_contact)

        # Assert
        mock_db_session.commit.assert_called_once()
        mock_db_session.refresh.assert_called_once_with(sample_contact)
        assert result == sample_contact

    def test_delete_contact(self, mock_db_session, sample_contact):
        """Test deleting a contact."""
        # Act
        delete(mock_db_session, sample_contact)

        # Assert
        mock_db_session.delete.assert_called_once_with(sample_contact)
        mock_db_session.commit.assert_called_once()

    def test_search_with_query(self, mock_db_session, sample_contact):
        """Test search with query string."""
        # Arrange
        mock_query = Mock(spec=Query)
        mock_query.filter.return_value = mock_query
        mock_query.all.return_value = [sample_contact]
        mock_db_session.query.return_value = mock_query

        # Act
        result = search(mock_db_session, query="john", categories=[])

        # Assert
        mock_db_session.query.assert_called_once_with(Contact)
        assert len(result) == 1

    def test_search_with_categories(self, mock_db_session, sample_contact):
        """Test search with categories filter."""
        # Arrange
        mock_query = Mock(spec=Query)
        mock_query.filter.return_value = mock_query
        mock_query.all.return_value = [sample_contact]
        mock_db_session.query.return_value = mock_query

        # Act
        result = search(mock_db_session, query="", categories=["Friends"])

        # Assert
        mock_db_session.query.assert_called_once_with(Contact)
        assert len(result) == 1

    def test_search_with_both_filters(self, mock_db_session, sample_contact):
        """Test search with both query and categories."""
        # Arrange
        mock_query = Mock(spec=Query)
        mock_query.filter.return_value = mock_query
        mock_query.all.return_value = [sample_contact]
        mock_db_session.query.return_value = mock_query

        # Act
        result = search(mock_db_session, query="doe", categories=["Friends"])

        # Assert
        mock_db_session.query.assert_called_once_with(Contact)
        assert len(result) == 1

    def test_search_without_filters(self, mock_db_session, sample_contact):
        """Test search without any filters."""
        # Arrange
        mock_query = Mock(spec=Query)
        mock_query.all.return_value = [sample_contact]
        mock_db_session.query.return_value = mock_query

        # Act
        result = search(mock_db_session, query="", categories=[])

        # Assert
        mock_db_session.query.assert_called_once_with(Contact)
        mock_query.all.assert_called_once()
        assert len(result) == 1
