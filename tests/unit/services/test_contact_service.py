"""
Unit tests for contact service layer.
"""

from unittest.mock import Mock, patch

import pytest

from src.database.models import Contact
from src.services.contact_service import (
    ContactServiceError,
    add_contact,
    delete_contact,
    get_contact,
    list_contacts,
    search_contacts,
    update_contact,
)


class TestContactService:
    """Test cases for contact service functions."""

    def test_get_contact_found(self, mock_db_session, sample_contact):
        """Test getting contact when it exists."""
        # Arrange
        mock_crud = Mock()
        mock_crud.get_by_id.return_value = sample_contact

        with patch("src.services.contact_service.contact_crud", mock_crud):
            # Act
            result = get_contact(mock_db_session, 1)

            # Assert
            mock_crud.get_by_id.assert_called_once_with(mock_db_session, 1)
            assert result == sample_contact

    def test_get_contact_not_found(self, mock_db_session):
        """Test getting contact when it doesn't exist."""
        # Arrange
        mock_crud = Mock()
        mock_crud.get_by_id.return_value = None

        with patch("src.services.contact_service.contact_crud", mock_crud):
            # Act & Assert
            with pytest.raises(ContactServiceError) as exc_info:
                get_contact(mock_db_session, 999)

            assert "Contact not found" in exc_info.value.errors[0]

    def test_add_contact_success(self, mock_db_session):
        """Test successfully adding a new contact."""
        # Arrange
        contact_data = {
            "first_name": "John",
            "last_name": "Doe",
            "phone": "+12345678901",
            "email": "john.doe@example.com",
            "category": "Friends",
        }

        mock_contact = Mock(spec=Contact)
        mock_crud = Mock()
        mock_crud.get_by_phone.return_value = None
        mock_crud.get_by_email.return_value = None
        mock_crud.create.return_value = mock_contact

        with patch("src.services.contact_service.contact_crud", mock_crud):
            # Act
            result = add_contact(mock_db_session, contact_data)

            # Assert
            mock_crud.create.assert_called_once()
            assert result == mock_contact

    def test_add_contact_duplicate_phone(self, mock_db_session):
        """Test adding contact with duplicate phone number."""
        # Arrange
        contact_data = {
            "first_name": "John",
            "last_name": "Doe",
            "phone": "+12345678901",
            "email": "john.doe@example.com",
        }

        mock_crud = Mock()
        mock_crud.get_by_phone.return_value = Mock()  # Simulate existing contact
        mock_crud.get_by_email.return_value = None

        with patch("src.services.contact_service.contact_crud", mock_crud):
            # Act & Assert
            with pytest.raises(ContactServiceError) as exc_info:
                add_contact(mock_db_session, contact_data)

            assert "Phone number already exists" in exc_info.value.errors[0]

    def test_add_contact_duplicate_email(self, mock_db_session):
        """Test adding contact with duplicate email."""
        # Arrange
        contact_data = {
            "first_name": "John",
            "last_name": "Doe",
            "phone": "+12345678901",
            "email": "existing@example.com",
        }

        mock_crud = Mock()
        mock_crud.get_by_phone.return_value = None
        mock_crud.get_by_email.return_value = Mock()  # Simulate existing contact

        with patch("src.services.contact_service.contact_crud", mock_crud):
            # Act & Assert
            with pytest.raises(ContactServiceError) as exc_info:
                add_contact(mock_db_session, contact_data)

            assert "Email already exists" in exc_info.value.errors[0]

    def test_add_contact_invalid_name(self, mock_db_session):
        """Test adding contact with empty names."""
        # Arrange
        contact_data = {
            "first_name": "",
            "last_name": "",
            "phone": "+12345678901",
            "email": "test@example.com",
        }

        mock_crud = Mock()

        with patch("src.services.contact_service.contact_crud", mock_crud):
            # Act & Assert
            with pytest.raises(ContactServiceError) as exc_info:
                add_contact(mock_db_session, contact_data)

            assert "At least one of First Name or Last Name" in exc_info.value.errors[0]

    def test_list_contacts(self, mock_db_session, sample_contact):
        """Test listing all contacts."""
        # Arrange
        mock_crud = Mock()
        mock_crud.get_all.return_value = [sample_contact]

        with patch("src.services.contact_service.contact_crud", mock_crud):
            # Act
            result = list_contacts(mock_db_session)

            # Assert
            mock_crud.get_all.assert_called_once_with(mock_db_session)
            assert len(result) == 1
            assert result[0] == sample_contact

    def test_update_contact_success(self, mock_db_session):
        """Test successfully updating a contact."""
        # Arrange
        contact_id = 1
        update_data = {
            "first_name": "Updated",
            "last_name": "Name",
            "phone": "+9876543210",
        }

        existing_contact = Mock(spec=Contact)
        existing_contact.first_name = "Old"
        existing_contact.last_name = "Name"
        existing_contact.phone = "+1234567890"
        existing_contact.email = "old@example.com"

        mock_crud = Mock()
        mock_crud.get_by_id.return_value = existing_contact
        mock_crud.update.return_value = existing_contact

        with patch("src.services.contact_service.contact_crud", mock_crud):
            # Act
            result = update_contact(mock_db_session, contact_id, update_data)

            # Assert
            mock_crud.get_by_id.assert_called_once_with(mock_db_session, contact_id)
            mock_crud.update.assert_called_once_with(mock_db_session, existing_contact)
            assert result == existing_contact

    def test_update_contact_not_found(self, mock_db_session):
        """Test updating non-existent contact."""
        # Arrange
        mock_crud = Mock()
        mock_crud.get_by_id.return_value = None

        with patch("src.services.contact_service.contact_crud", mock_crud):
            # Act & Assert
            with pytest.raises(ContactServiceError) as exc_info:
                update_contact(mock_db_session, 999, {"first_name": "New"})

            assert "Contact not found" in exc_info.value.errors[0]

    def test_delete_contact_success(self, mock_db_session):
        """Test successfully deleting a contact."""
        # Arrange
        contact_id = 1
        mock_contact = Mock(spec=Contact)

        mock_crud = Mock()
        mock_crud.get_by_id.return_value = mock_contact

        with patch("src.services.contact_service.contact_crud", mock_crud):
            # Act
            delete_contact(mock_db_session, contact_id)

            # Assert
            mock_crud.get_by_id.assert_called_once_with(mock_db_session, contact_id)
            mock_crud.delete.assert_called_once_with(mock_db_session, mock_contact)

    def test_delete_contact_not_found(self, mock_db_session):
        """Test deleting non-existent contact."""
        # Arrange
        mock_crud = Mock()
        mock_crud.get_by_id.return_value = None

        with patch("src.services.contact_service.contact_crud", mock_crud):
            # Act & Assert
            with pytest.raises(ContactServiceError) as exc_info:
                delete_contact(mock_db_session, 999)

            assert "Contact not found" in exc_info.value.errors[0]

    def test_search_contacts(self, mock_db_session, sample_contact):
        """Test searching contacts."""
        # Arrange
        mock_crud = Mock()
        mock_crud.search.return_value = [sample_contact]

        with patch("src.services.contact_service.contact_crud", mock_crud):
            # Act
            result = search_contacts(
                mock_db_session, query="john", categories=["Friends"]
            )

            # Assert
            mock_crud.search.assert_called_once_with(
                db=mock_db_session, query="john", categories=["Friends"]
            )
            assert len(result) == 1
            assert result[0] == sample_contact

    def test_contact_service_error(self):
        """Test ContactServiceError exception."""
        # Arrange
        error_messages = ["Error 1", "Error 2"]

        # Act
        error = ContactServiceError(error_messages)

        # Assert
        assert error.errors == error_messages
        assert str(error) == "Contact service error"
