"""
Streamlit UI component for editing existing contacts.

This module provides the user interface and logic for modifying
existing contact information in the database.
"""

import streamlit as st
from sqlalchemy.orm import Session

from src.database.db import SessionLocal
from src.services.contact_service import (
    ContactServiceError,
    get_contact,
    update_contact,
)

# Initialize database session
db: Session = SessionLocal()


def render_edit_contact() -> None:
    """
    Render the 'Edit Contact' page with a pre-filled form for editing contact details.

    Retrieves the contact based on session state contact_id and populates form fields
    with current values. Handles form submission and contact updates.
    """
    # Retrieve contact from database using session state contact_id
    contact = get_contact(db, st.session_state.contact_id)

    # Define choices
    category_options: list[str] = ["Family", "Friends", "Work", "Other"]

    # Extracting the category value in a safe and typed manner
    category_value: str = str(contact.category) if contact.category else "Other"

    index = (
        category_options.index(category_value)
        if category_value in category_options
        else 0
    )

    st.header("✏️ Edit Contact")
    with st.form("add_contact"):
        # Form fields pre-filled with current contact information
        data = {
            "first_name": st.text_input("First Name", value=contact.first_name),
            "last_name": st.text_input("Last Name", value=contact.last_name),
            "phone": st.text_input("Phone", value=contact.phone),
            "email": st.text_input("Email", value=contact.email),
            "category": st.selectbox(
                "Category",
                options=category_options,
                index=index,
            ),
        }
        submitted: bool = st.form_submit_button(
            "💾 Update", width="stretch", key="glass-button"
        )
        if submitted:
            try:
                # Attempt to update contact in database
                update_contact(db, st.session_state.contact_id, data)
                st.success("✅ Contact added successfully!")
                # Redirect to home page
                st.session_state.page = "home"
                st.rerun()
            except ContactServiceError as e:
                # Display validation errors
                st.error("❌ Failed to update contact due to the following errors:")
                for error in e.errors:
                    st.markdown(f" ❌ {error}")
    # Cancel button to return to home page
    if st.button("⬅ Cancel"):
        st.session_state.page = "home"
        st.rerun()
