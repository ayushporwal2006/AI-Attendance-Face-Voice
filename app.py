import streamlit as st
# Import function from different folder file
from src.screens.home_screen import home_screen
from src.screens.student_screen import student_screen
from src.screens.teacher_screen import teacher_screen
def main():
    if 'login_type' not in st.session_state:
        st.session_state['login_type'] = None

    match st.session_state["login_type"]:
        case 'teacher':
            teacher_screen()
        case 'student':
            student_screen()
        case _:
            home_screen()
main()
# statefulness = Same info we can to show on multiple page      