"""
Streamlit UI component for adding new contacts.

This module provides the user interface and logic for adding new contacts
to the Contact Book database.
"""

import streamlit as st
from sqlalchemy.orm import Session

from database.db import SessionLocal
from services.contact_service import ContactServiceError, add_contact

# Initialize database session
db: Session = SessionLocal()


def render_add_contact() -> None:
    """
    Render the 'Add New Contact' page with a form for inputting contact details.

    The form includes fields for first name, last name, phone, email, and category.
    Handles form submission and contact creation.
    """
    st.header("➕ Add New Contact")

    with st.form("add_contact"):
        # Form fields for contact information
        data = {
            "first_name": st.text_input("First Name", placeholder="First Name"),
            "last_name": st.text_input("Last Name", placeholder="Last Name"),
            "phone": st.text_input("Phone", placeholder="+1-123-456-789"),
            "email": st.text_input("Email", placeholder="example@email.com"),
            "category": st.selectbox(
                "Category", ["Family", "Friends", "Work", "Other"]
            ),
        }

        # Submit button with glass morphism styling
        submitted: bool = st.form_submit_button(
            "💾 Save", width="stretch", key="glass-button"
        )
        if submitted:
            # Attempt to add contact to database
            try:
                add_contact(db, data)
                st.success("✅ Contact added successfully!")
                st.session_state.page = "home"
                st.rerun()
            except ContactServiceError as e:
                # Display validation errors
                st.error("❌ Failed to add contact due to the following errors:")
                # pylint: disable=duplicate-code
                for error in e.errors:
                    st.markdown(f" ❌ {error}")
    # Cancel button to return to home page
    if st.button("⬅ Cancel"):
        st.session_state.page = "home"
        st.rerun()
