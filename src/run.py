"""
Main Streamlit application for the Contact Book web interface.

This module serves as the entry point for the Streamlit web application,
handling routing, database initialization checks, and CSS loading.
"""

import sys
from pathlib import Path

import streamlit as st
from sqlalchemy import inspect

from database.db import engine
from UI.add_contact import render_add_contact
from UI.edit_contact import render_edit_contact
from UI.home import render_home
from UI.router import init_router
from UI.show_contact import render_show_contact

st.set_page_config(page_title="Contact Book", layout="wide")


def check_database_initialized() -> bool:
    """
    Check if the database is properly initialized by verifying the contacts table exists.

    :return: True if the 'contacts' table exists, False otherwise
    """
    return inspect(engine).has_table("contacts")


def load_css(file_name: str) -> None:
    """
    Load a CSS file and apply its styles to the Streamlit app.

    :param file_name: Path to the CSS file to load
    :type file_name: str
    """
    css_path = Path(file_name)
    if css_path.exists():
        with open(css_path, encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        st.warning(f"⚠️ CSS file not found: {file_name}")


def main() -> None:
    """
    Main function to run the Streamlit Contact Book application.

    Handles database initialization check, routing, and page rendering.
    """

    # Check database initialization
    if not check_database_initialized():
        st.error(
            "❌ Database is not initialized.\n\n"
            "Please run the following command first:\n\n"
            "`python src/init_db.py`",
            icon="🚨",
        )
        st.stop()
    # Initialize router for session state management
    init_router()

    # Add the src directory to sys.path for module imports
    sys.path.append(str(Path(__file__).resolve().parent))

    # Load the CSS file
    load_css("src/styles/main.css")

    # Main application container with glass morphism styling
    with st.container(key="center"):
        with st.container(key="glass-container"):
            with st.container(key="glass-sections"):
                with st.container(key="glass-section-lower"):
                    if st.session_state.page == "home":
                        render_home()

                    elif st.session_state.page == "add":
                        render_add_contact()

                    elif st.session_state.page == "edit":
                        render_edit_contact()

                    elif st.session_state.page == "show":
                        render_show_contact()


if __name__ == "__main__":
    main()
