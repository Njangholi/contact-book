import streamlit as st

from database.db import SessionLocal
from services.contact_service import ContactServiceError, add_contact

db = SessionLocal()


def render_add_contact():
    st.header("➕ Add New Contact")

    with st.form("add_contact"):
        data = {
            "first_name": st.text_input("First Name", placeholder="First Name"),
            "last_name": st.text_input("Last Name", placeholder="Last Name"),
            "phone": st.text_input("Phone", placeholder="+1-123-456-789"),
            "email": st.text_input("Email", placeholder="example@email.com"),
            "category": st.selectbox(
                "Category", ["Family", "Friends", "Work", "Other"]
            ),
        }
        submitted = st.form_submit_button(
            "💾 Save", width="stretch", key="glass-button"
        )
        if submitted:
            try:
                add_contact(db, data)
                st.success("✅ Contact added successfully!")
                st.session_state.page = "home"
                st.rerun()
            except ContactServiceError as e:
                st.error("❌ Failed to add contact due to the following errors:")
                for error in e.errors:
                    st.markdown(f" ❌ {error}")
    if st.button("⬅ Cancel"):
        st.session_state.page = "home"
        st.rerun()
