"""
Streamlit UI component for displaying detailed contact information.

This module provides the user interface for viewing complete contact details
in a read-only format.
"""

import streamlit as st

from src.database.db import SessionLocal
from src.services.contact_service import get_contact  # ContactServiceError,

# Initialize database session
db = SessionLocal()


def render_show_contact() -> None:
    """
    Render the 'Contact Details' page displaying all information for a specific contact.

    Retrieves contact based on session state contact_id and displays all fields
    in a formatted view with navigation options.
    """
    # Retrieve contact from database using session state contact_id
    contact = get_contact(db, st.session_state.contact_id)

    st.header("👤 Contact Details")
    st.divider()

    # Display all contact information
    st.subheader(f"**Name:** {contact.first_name} {contact.last_name}")
    st.write(f"📞 {contact.phone}")
    st.write(f"📧 {contact.email}")
    st.write(f"👥 {contact.category}")

    # Navigation buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅ Back", width="stretch"):
            st.session_state.page = "home"
            st.rerun()
    with col2:
        if st.button("Update", width="stretch"):
            st.session_state.page = "edit"
            st.rerun()
