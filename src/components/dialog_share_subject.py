import streamlit as st

from src.database.db import create_subject


@st.dialog("Share class link")
def share_subject_dialog(subject_name, subject_code):
    app_domain = "http://localhost:8501/"
    join_url = f"{app_domain}/?join-code={subject_code}"

    st.header("Scan to join")
