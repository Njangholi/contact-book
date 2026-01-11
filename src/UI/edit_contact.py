import streamlit as st

# from database import db
from database.db import SessionLocal
from services.contact_service import ContactServiceError, get_contact, update_contact

# import os
# import sys
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# from database.db import SessionLocal, engine


db = SessionLocal()


def render_edit_contact():
    contact = get_contact(db, st.session_state.contact_id)

    st.header("✏️ Edit Contact")
    with st.form("add_contact"):
        data = {
            "first_name": st.text_input("First Name", value=contact.first_name),
            "last_name": st.text_input("Last Name", value=contact.last_name),
            "phone": st.text_input("Phone", value=contact.phone),
            "email": st.text_input("Email", value=contact.email),
            "category": st.selectbox(
                "Category",
                ["Family", "Friends", "Work", "Other"],
                index=(
                    ["Family", "Friends", "Work", "Other"].index(contact.category)
                    if contact.category in ["Family", "Friends", "Work", "Other"]
                    else 0
                ),
            ),
        }
        submitted = st.form_submit_button(
            "💾 Update", width="stretch", key="glass-button"
        )
        if submitted:
            try:
                update_contact(db, st.session_state.contact_id, data)
                st.success("✅ Contact added successfully!")
                st.session_state.page = "home"
                st.rerun()
            except ContactServiceError as e:
                st.error("❌ Failed to update contact due to the following errors:")
                for error in e.errors:
                    st.markdown(f" ❌ {error}")
    if st.button("⬅ Cancel"):
        st.session_state.page = "home"
        st.rerun()


# if __name__ == "__main__":
#     render_edit_contact()
