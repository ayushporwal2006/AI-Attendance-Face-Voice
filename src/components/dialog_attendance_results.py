import streamlit as st
from src.database.db import create_attendance

def show_attendance_result(df, logs):
    st.write("Please Review attendance before confirming")
    st.dataframe(df, hide_index=True, width="stretch")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Discard", width="stretch"):
            st.session_state.voice_attendance_results = None
            st.session_state.attendance_images = []
            st.rerun()

    with col2:
        if st.button("Confirm and Save", width="stretch", type="primary"):
            st.write(logs)
        
            try:
                result = create_attendance(logs)
                st.write(result)
                st.success("Attendance Saved")
            except Exception as e:
                st.error("Sync failed!")
                print(e)
            st.rerun()
        
@st.dialog("Attendance_report")
def attendance_result_dialog(df, logs):
    show_attendance_result(df, logs)
