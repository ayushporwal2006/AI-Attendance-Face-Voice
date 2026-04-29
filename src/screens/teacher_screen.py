import streamlit as st
from src.components.header import header_dashboard
from src.ui.base_layout import style_background_dashboard , style_base_layout
from src.database.db import check_teacher_exists, create_teacher , teacher_login

def teacher_screen():
    style_background_dashboard()
    style_base_layout()
    
    if 'teacher_login_type' not in st.session_state or st.session_state.teacher_login_type=="login":
        teacher_screen_login()
    elif st.session_state.teacher_login_type=="register":
        teacher_screen_register()

def login_teacher(username, password):
    if not username or not password:
        return False

    teacher= teacher_login(username, password)

    if teacher:
        st.session_state.user_role = 'teacher'
        st.session_state.teacher_data = teacher
        st.session_state.is_logged_in = True
        return True
    return False

def register_teacher(teacher_username, teacher_name , teacher_pass, teacher_pass_confirm):
    if not teacher_username or not teacher_name or not teacher_pass:
        return False, "All Fields are required! "
    if check_teacher_exists(teacher_username):
        return False, "Username already exists!"
    if teacher_pass != teacher_pass_confirm:
        return False, "Password doesn't match"
    
    try:
        create_teacher(teacher_username, teacher_pass, teacher_name)
        return True, "Successfully created! Login now"
    except Exception as e:
        return False, "Unexpected Error!"

def teacher_screen_register():
    c1, c2 = st.columns(2, gap="xxlarge",vertical_alignment="center") 
    with c1:
        header_dashboard()
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
        if st.button("Register now",type = "secondary",shortcut="control+enter", icon=":material/passkey:", width="stretch" ):
            success, message = register_teacher(teacher_username, teacher_name , teacher_pass, teacher_pass_confirm)
            if success:
                st.success(message)
                import time
                time.sleep(2)
                st.session_state.teacher_login_type = "login"
                st.rerun()
            else:
                st.error(message)
    with cb2:
        if st.button("Login instead", type="primary",icon=":material/passkey:", width="stretch"):
            st.session_state.teacher_login_type = 'login'
           


def teacher_screen_login():
    c1, c2 = st.columns(2, gap="xxlarge",vertical_alignment="center") 
    with c1:
        header_dashboard()
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
        if st.button("Login",type = "secondary",shortcut="control+enter", icon=":material/passkey:", width="stretch" ):
            if login_teacher(teacher_username, teacher_pass):
                st.toast("Welcome! back", icon="👋")
                import time
                time.sleep(1)
                st.rerun()
            else:
                st.error("Invalid username or password combo")
    with cb2:
        if st.button("Register instead", type="primary",icon=":material/passkey:", width="stretch"):
            st.session_state.teacher_login_type ="register"


