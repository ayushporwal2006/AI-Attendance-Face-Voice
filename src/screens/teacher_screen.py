import streamlit as st
from src.components.header import header_teacher_dashboard
from src.ui.base_layout import style_background_dashboard , style_base_layout
def teacher_screen():
    style_background_dashboard()
    style_base_layout()
    
    if 'teacher_login_type' not in st.session_state or st.session_state.teacher_login_type=="login":
        teacher_login()
    elif st.session_state.teacher_login_type=="register":
        teacher_register()


def teacher_register():
    c1, c2 = st.columns(2, gap="xxlarge",vertical_alignment="center") 
    with c1:
        header_teacher_dashboard()
    with c2:
        if st.button("Go back to home",type="secondary", key="loginbackhome", shortcut="control+backspace"):
            st.session_state["login_type"] = None
            st.rerun()
    st.header("Registered Your Teacher Profile")
    st.space()
    st.space()
    teacher_name = st.text_input("Enter your name", placeholder="AyushPorwal")
    teacher_username = st.text_input("Enter username", placeholder="Ayush31")
    teacher_pass = st.text_input("Enter  password",type="password", placeholder="Enter password")
    teacher_pass_confirm = st.text_input("Confirm Password",type="password", placeholder="Enter password")
    st.divider()

    cb1, cb2 = st.columns(2, gap="xxlarge",vertical_alignment="center")
    
    with cb1:
        st.button("Register now",type = "secondary",shortcut="control+enter", icon=":material/passkey:", width="stretch" )
    with cb2:
        if st.button("Login instead", type="primary",icon=":material/passkey:", width="stretch"):
            st.session_state.teacher_login_type = 'login'
           


def teacher_login():
    c1, c2 = st.columns(2, gap="xxlarge",vertical_alignment="center") 
    with c1:
        header_teacher_dashboard()
    with c2:
        if st.button("Go back to home",type="secondary", key="loginbackhome", shortcut="control+backspace"):
            st.session_state["login_type"] = None
            st.rerun()
    st.header("Login Using Password",text_alignment="center",)
    st.space()
    st.space()

    teacher_username = st.text_input("Enter username", placeholder="AyushPorwal")
    teacher_pass = st.text_input("Enter the password",type="password", placeholder="Enter password")

    st.divider()

    cb1, cb2 = st.columns(2, gap="xxlarge",vertical_alignment="center")

    with cb1:
        st.button("Login",type = "secondary",shortcut="control+enter", icon=":material/passkey:", width="stretch" )
    with cb2:
        if st.button("Register instead", type="primary",icon=":material/passkey:", width="stretch"):
            st.session_state.teacher_login_type ="register"


