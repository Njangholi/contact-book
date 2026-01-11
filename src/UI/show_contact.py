import streamlit as st

# import os
# import sys
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.db import SessionLocal
from services.contact_service import get_contact  # ContactServiceError,

db = SessionLocal()


def render_show_contact():
    contact = get_contact(db, st.session_state.contact_id)

    st.header("👤 Contact Details")
    st.divider()

    st.subheader(f"**Name:** {contact.first_name} {contact.last_name}")
    st.write(f"📞 {contact.phone}")
    st.write(f"📧 {contact.email}")
    st.write(f"👥 {contact.category}")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅ Back", width="stretch"):
            st.session_state.page = "home"
            st.rerun()
    with col2:
        if st.button("Update", width="stretch"):
            st.session_state.page = "edit"
            st.rerun()


# if __name__ == "__main__":
#     render_show_contact()
# this file couldn't run individually, because it needs contact id to be passed
