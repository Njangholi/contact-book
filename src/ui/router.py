"""
Session state router for Streamlit application navigation.

This module initializes and manages session state variables for page routing
and contact selection across the Contact Book application.
"""

import streamlit as st


def init_router() -> None:
    """
    Initialize session state variables for application routing.

    Sets up the following session state variables:
    - 'page': Current page/view (default: "home")
    - 'contact_id': Currently selected contact ID (default: None)
    """
    # Initialize page state if not exists
    if "page" not in st.session_state:
        st.session_state["page"] = "home"

    # Initialize contact_id state if not exists
    if "contact_id" not in st.session_state:
        st.session_state["contact_id"] = None
