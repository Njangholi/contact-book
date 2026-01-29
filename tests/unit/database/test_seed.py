"""
Tests for the database seeding module.
"""

from unittest.mock import Mock, patch

import pytest

from src.database.seed import seed_demo_contacts


def test_seed_demo_contacts_inserts_data_once():
    """
    Test that seed_demo_contacts adds contacts only when database is empty.
    """
    # Create mock objects
    mock_db = Mock()
    mock_list_contacts = Mock()
    mock_add_contact = Mock()

    # First call returns empty list (database empty)
    # Second call returns list with 3 items (after seeding)
    mock_list_contacts.side_effect = [
        [],  # First call - empty database
        [Mock(), Mock(), Mock()],  # Second call - after first seeding
        [Mock(), Mock(), Mock()],  # Third call - after second seeding attempt
    ]

    # Patch the dependencies
    with patch("src.database.seed.SessionLocal", return_value=mock_db), patch(
        "src.database.seed.list_contacts", mock_list_contacts
    ), patch("src.database.seed.add_contact", mock_add_contact):

        # First call - should add contacts
        seed_demo_contacts()

        # Verify add_contact was called 3 times
        assert mock_add_contact.call_count == 3

        # Reset mock to track second call
        mock_add_contact.reset_mock()

        # Second call - should NOT add contacts (database not empty)
        seed_demo_contacts()

        # Verify add_contact was NOT called again
        assert mock_add_contact.call_count == 0


def test_seed_demo_contacts_skips_if_data_exists():
    """
    Test that seed_demo_contacts does nothing when contacts already exist.
    """
    # Create mock objects
    mock_db = Mock()
    mock_list_contacts = Mock(return_value=[Mock(), Mock()])  # Non-empty list
    mock_add_contact = Mock()

    # Patch the dependencies
    with patch("src.database.seed.SessionLocal", return_value=mock_db), patch(
        "src.database.seed.list_contacts", mock_list_contacts
    ), patch("src.database.seed.add_contact", mock_add_contact):

        # Call seed function
        seed_demo_contacts()

        # Verify add_contact was NOT called
        mock_add_contact.assert_not_called()


def test_seed_demo_contacts_adds_correct_contacts():
    """
    Test that seed_demo_contacts adds the correct contact data.
    """
    # Create mock objects
    mock_db = Mock()

    # Expected contact data
    expected_contacts = [
        {
            "first_name": "Alice",
            "last_name": "Johnson",
            "phone": "+49 151 12345678",
            "email": "alice@example.com",
            "category": "Friends",
        },
        {
            "first_name": "Bob",
            "last_name": "Smith",
            "phone": "+49 160 98765432",
            "email": "bob@example.com",
            "category": "Work",
        },
        {
            "first_name": "John",
            "last_name": "Doe",
            "phone": "+49 170 1234567",
            "email": "John@example.com",
            "category": "Work",
        },
    ]

    # Patch the dependencies
    with patch("src.database.seed.list_contacts") as mock_list_contacts, patch(
        "src.database.seed.add_contact"
    ) as mock_add_contact, patch(
        "src.database.seed.SessionLocal", return_value=mock_db
    ):

        # Empty database
        mock_list_contacts.return_value = []

        # Call seed function
        seed_demo_contacts()

        # Verify add_contact was called 3 times
        assert mock_add_contact.call_count == 3

        # Get all calls
        calls = mock_add_contact.call_args_list

        # Verify each call has correct data
        for i, call in enumerate(calls):
            # call is a tuple of (args, kwargs)
            args = call[0]  # Positional arguments
            kwargs = call[1]  # Keyword arguments

            # The function is called as add_contact(db, data)
            # So args[0] is db, args[1] is data
            if args and len(args) >= 2:
                data_arg = args[1]
            elif kwargs:
                data_arg = kwargs.get("data")
            else:
                continue

            # Verify data matches expected
            assert data_arg["first_name"] == expected_contacts[i]["first_name"]
            assert data_arg["last_name"] == expected_contacts[i]["last_name"]
            assert data_arg["phone"] == expected_contacts[i]["phone"]
            assert data_arg["email"] == expected_contacts[i]["email"]
            assert data_arg["category"] == expected_contacts[i]["category"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
