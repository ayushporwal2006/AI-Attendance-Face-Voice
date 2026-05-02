import streamlit as st

from src.database.db import create_subject


@st.dialog("Create New Subject")
def create_subject_dialog(teacher_id):
    st.write("Enter the details of New Subjects")
    sub_id = st.text_input("Subject Code", placeholder="CS301")
    sub_name = st.text_input("Subject",placeholder="Operating System")
    sub_section = st.text_input("Section", palceholder="A")

    if st.button("Create Subject now",type="primary",width="stretch"):
        if sub_id and sub_name and sub_section:
            try:
                create_subject(sub_id,sub_name,sub_section,teacher_id)
                st.toast("Subject Created Succesfully!!")
                st.rerun()
            except Exception as e:
                st.error(f"Error: {str(e)}")
        else:
            st.warning("Please fill all the required details")
