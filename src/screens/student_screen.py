import streamlit as st
import numpy as np
from PIL import Image
from src.components.header import header_dashboard
from src.ui.base_layout import style_background_dashboard , style_base_layout

def student_screen():
    style_background_dashboard()
    style_base_layout()
    c1, c2 = st.columns(2, gap="xxlarge",vertical_alignment="center") 
    with c1:
        header_dashboard()
    with c2:
        if st.button("Go back to home",type="secondary", key="loginbackhome", shortcut="control+backspace"):
            st.session_state["login_type"] = None
            st.rerun()
    st.header("Login with FaceID",text_alignment="center",)
    st.space()
    st.space()

    photo_source = st.camera_input("Position your face in center")

    if photo_source:
        np.array(Image.open(photo_source))