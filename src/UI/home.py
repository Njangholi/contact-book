"""
Streamlit UI component for the home page displaying contacts.

This module provides the main interface showing all contacts with search,
filtering, and CRUD operation buttons.
"""

import streamlit as st
from sqlalchemy.orm import Session

from database.db import SessionLocal
from services.contact_service import delete_contact, list_contacts, search_contacts

# Initialize database session
db = SessionLocal()


@st.dialog("Delete the Contact")
def delete_dialog(db_session: Session, contact_id: int) -> None:
    """
    Display a confirmation dialog for contact deletion.

    :param db: Database session
    :param contact_id: ID of the contact to delete
    """
    with st.container(key="dialog"):
        st.write("Are you sure you want to delete this contact?")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Yes", key=f"yes_{contact_id}"):
                delete_contact(db_session, contact_id)
                st.rerun()
        with col2:
            if st.button("❌ No", key=f"no_{contact_id}"):
                st.rerun()


def render_home() -> None:
    """
    Render the home page with contact list, search functionality, and CRUD operations.

    Displays all contacts in a list with options to view, edit, or delete each contact.
    Includes search and category filtering capabilities.
    """
    # Header with title and add button
    col1, col2 = st.columns([5, 1])
    with col1:
        st.title("📒 Contact Book")
    with col2:
        if st.button("➕", help="Add New Contact", key="glass-button"):
            st.session_state.page = "add"
            st.rerun()

    # Search and filter section
    with st.container(key="glass-section-upper"):
        col1, col2 = st.columns([2, 1])

        with col1:
            search = st.text_input(
                "🔍 Search", placeholder="Name, Phone, Email ...", key="search_query"
            )
        with col2:
            categories = st.multiselect(
                "Filter by category",
                ["Family", "Friends", "Work", "Other"],
                default=[],
                key="search_categories",
            )

            # Initialize session state for search tracking
            if "last_query" not in st.session_state:
                st.session_state.last_query = None

            # Perform search when query or categories change
            if (
                search != st.session_state.last_query
                or categories != st.session_state.get("last_categories")
            ):
                st.session_state.last_query = search
                st.session_state.last_categories = categories

                contacts = search_contacts(db, search, categories)
                if not contacts:
                    st.info("No contact found")
            else:
                contacts = list_contacts(db)

    st.divider()

    # Contact list display section
    with st.container(key="glass-section-lower-upper", height=500):
        for contact in contacts:
            c1, c2, c3, c4 = st.columns([4, 1, 1, 1])

            # Display contact information
            c1.subheader(f"{contact.first_name} {contact.last_name} \n{contact.phone}")

            # View button
            if c2.button("👁️‍🗨️", help="show", key=f"show_{contact.id}"):
                st.session_state.page = "show"
                st.session_state.contact_id = contact.id
                st.rerun()

            # Edit button
            if c3.button("✏️", help="Edit", key=f"edit_{contact.id}"):
                st.session_state.page = "edit"
                st.session_state.contact_id = contact.id
                st.rerun()

            # Delete button with confirmation dialog
            if c4.button("🗑️", help="Delete", key=f"delete_{contact.id}"):
                delete_dialog(db, contact.id)

            st.divider()
