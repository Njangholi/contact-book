"""
Unit tests for database models.
"""

from src.database.models import Contact


class TestContactModel:
    """Test cases for Contact model."""

    def test_contact_creation(self):
        """Test creating a Contact instance with all fields."""
        # Arrange
        contact_data = {
            "first_name": "Alice",
            "last_name": "Smith",
            "phone": "+9876543210",
            "email": "alice.smith@example.com",
            "category": "Family",
        }

        # Act
        contact = Contact(**contact_data)

        # Assert
        assert contact.first_name == "Alice"
        assert contact.last_name == "Smith"
        assert contact.phone == "+9876543210"
        assert contact.email == "alice.smith@example.com"
        assert contact.category == "Family"
        assert contact.id is None
        assert contact.created_at is None
        assert contact.updated_at is None

    def test_contact_without_email(self):
        """Test creating a Contact without email."""
        # Act
        contact = Contact(first_name="Bob", last_name="Johnson", phone="+1122334455")

        # Assert
        assert contact.first_name == "Bob"
        assert contact.last_name == "Johnson"
        assert contact.phone == "+1122334455"
        assert contact.email is None
        assert contact.category is None

    def test_contact_without_category(self):
        """Test creating a Contact without category."""
        # Act
        contact = Contact(
            first_name="Charlie",
            last_name="Brown",
            phone="+9988776655",
            email="charlie@example.com",
        )

        # Assert
        assert contact.first_name == "Charlie"
        assert contact.last_name == "Brown"
        assert contact.email == "charlie@example.com"
        assert contact.category is None

    def test_contact_table_name(self):
        """Test that the table name is correctly set."""
        # Assert
        assert Contact.__tablename__ == "contacts"

    def test_contact_string_representation(self):
        """Test the string representation of Contact."""
        # Arrange
        contact = Contact(id=1, first_name="John", last_name="Doe", phone="+1234567890")

        # Act & Assert
        assert "John" in str(contact)
        assert "Doe" in str(contact)
