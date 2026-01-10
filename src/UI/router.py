
import streamlit as st


def init_router():

    if "page" not in st.session_state:
        # st.session_state.page = "home"
        st.session_state["page"] = "home"

    if "contact_id" not in st.session_state:
        # st.session_state.contact_id = None
        st.session_state["contact_id"] = None
