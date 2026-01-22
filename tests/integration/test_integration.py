"""
Integration tests for the Contact Book application.
"""

import pytest

from src.crud.contacts import create, delete, get_all, get_by_id, search, update
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


class TestIntegration:
    """Integration tests with real database session."""

    def test_full_crud_cycle(self, test_db_session):
        """Test complete CRUD cycle with real database."""
        # 1. Create contact
        contact = Contact(
            first_name="Integration",
            last_name="Test",
            phone="+1112223333",
            email="integration@test.com",
            category="Test",
        )

        created = create(test_db_session, contact)
        contact_id = created.id
        assert created.id is not None
        assert created.first_name == "Integration"

        # 2. Get by ID
        retrieved = get_by_id(test_db_session, created.id)
        assert retrieved is not None
        assert retrieved.id == created.id

        # 3. Get all
        all_contacts = get_all(test_db_session)
        assert len(all_contacts) == 1
        assert all_contacts[0].id == created.id

        # 4. Update
        retrieved.first_name = "Updated"
        updated = update(test_db_session, retrieved)
        assert updated.first_name == "Updated"

        # 5. Search
        search_results = search(test_db_session, query="Updated", categories=[])
        assert len(search_results) == 1

        # 6. Delete
        delete(test_db_session, retrieved)

        # 7. Verify deletion
        deleted = get_by_id(test_db_session, contact_id)
        assert deleted is None

    def test_service_layer_integration(self, test_db_session):
        """Test service layer integration with database."""
        # 1. Add contact through service
        contact_data = {
            "first_name": "Service",
            "last_name": "Test",
            "phone": "+9998887777",
            "email": "service@test.com",
            "category": "Work",
        }

        contact = add_contact(test_db_session, contact_data)
        assert contact.id is not None

        # 2. Get contact through service
        retrieved = get_contact(test_db_session, contact.id)
        assert retrieved.id == contact.id

        # 3. List contacts through service
        contacts = list_contacts(test_db_session)
        assert len(contacts) == 1

        # 4. Search through service
        search_results = search_contacts(
            test_db_session, query="Service", categories=["Work"]
        )
        assert len(search_results) == 1

        # 5. Update through service
        update_data = {"first_name": "UpdatedService", "phone": "+1112223333"}

        updated = update_contact(test_db_session, contact.id, update_data)
        assert updated.first_name == "UpdatedService"
        assert updated.phone == "+1112223333"

        # 6. Delete through service
        delete_contact(test_db_session, contact.id)

        # 7. Verify contact doesn't exist
        with pytest.raises(ContactServiceError):
            get_contact(test_db_session, contact.id)

    def test_duplicate_validation(self, test_db_session):
        """Test duplicate phone and email validation."""
        # Add first contact
        contact1_data = {
            "first_name": "First",
            "last_name": "Contact",
            "phone": "+1234567890",
            "email": "unique@test.com",
        }

        add_contact(test_db_session, contact1_data)

        # Try to add contact with same phone
        contact2_data = {
            "first_name": "Second",
            "last_name": "Contact",
            "phone": "+1234567890",  # Duplicate phone
            "email": "different@test.com",
        }

        with pytest.raises(ContactServiceError) as exc_info:
            add_contact(test_db_session, contact2_data)

        assert "Phone number already exists" in exc_info.value.errors[0]

        # Try to add contact with same email
        contact3_data = {
            "first_name": "Third",
            "last_name": "Contact",
            "phone": "+0987654321",
            "email": "unique@test.com",  # Duplicate email
        }

        with pytest.raises(ContactServiceError) as exc_info:
            add_contact(test_db_session, contact3_data)

        assert "Email already exists" in exc_info.value.errors[0]

    def test_search_functionality(self, test_db_session):
        """Test search functionality with multiple contacts."""
        # Create multiple test contacts
        contacts_data = [
            {
                "first_name": "Alice",
                "last_name": "Smith",
                "phone": "+1111111111",
                "category": "Friends",
            },
            {
                "first_name": "Bob",
                "last_name": "Johnson",
                "phone": "+2222222222",
                "category": "Work",
            },
            {
                "first_name": "Charlie",
                "last_name": "Brown",
                "phone": "+3333333333",
                "category": "Family",
            },
            {
                "first_name": "David",
                "last_name": "Smith",
                "phone": "+4444444444",
                "category": "Friends",
            },
        ]

        created_contacts = []
        for data in contacts_data:
            contact = add_contact(test_db_session, data)
            created_contacts.append(contact)

        # Test search by name
        results = search_contacts(test_db_session, query="smith", categories=[])
        assert len(results) == 2  # Alice Smith and David Smith

        # Test search by category
        results = search_contacts(test_db_session, query="", categories=["Friends"])
        assert len(results) == 2

        # Test combined search
        results = search_contacts(
            test_db_session, query="smith", categories=["Friends"]
        )
        assert len(results) == 2  # David Smith and Alice Smith

        # Test search with non-matching category
        results = search_contacts(test_db_session, query="smith", categories=["Work"])
        assert len(results) == 0
