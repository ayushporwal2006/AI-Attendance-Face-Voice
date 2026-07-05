import streamlit as st
from src.database.config import supabase
from src.pipelines.voice_pipeline import process_bulk_audio

from datetime import datetime
import pandas as pd
from src.components.dialog_attendance_results import show_attendance_result
@st.dialog("Voice attendance")
def voice_attendance_dialog(selected_subject_id):
    st.write("Record audio of student saying I'm present. Then AI will recognize the students")

    audio_data = None

    audio_data = st.audio_input("Record classroom audio!")

    if st.button("Analyze audio", width='stretch', type='primary'):
        with st.spinner("Processing Audio data"):
            enrolled_res = supabase.table('subject_student').select("* , students(*)").eq("subject_id",selected_subject_id ).execute()
            enrolled_student = enrolled_res.data
                        
            if not enrolled_student:
                st.warning("No Student enrolled in this course!")
                return
            candidates_dict = {
                s['students']['student_id'] : s['students']['voice_embedding']
                for s in enrolled_student if s['students'].get('voice_embedding')
            }

            if not candidates_dict:
                st.warning("No enrolled students have voice data available")
                return
            audio_bytes=audio_data.read()
            detected_scores=process_bulk_audio(audio_bytes,candidates_dict)

            results,attendance_to_log=[],[]
            current_timestamps=datetime.now().isoformat(timespec="seconds")
            for node in enrolled_student:
                student=node.get('students')
                if not student:
                    continue
                scores=detected_scores.get(student['student_id'],0.0)
                is_present=bool(scores>0)

                results.append({
                    "Name": student['name'],
                    "Id": student['student_id'],
                    "Score" : score if is_present else "-",
                    "Status" : "✅ Present" if is_present else "❌ Absent"
                })

                attendance_to_log.append({
                    "student_id": student["student_id"],
                    "subject_id": selected_subject_id,
                    "timestamp": current_timestamp,
                    "is_present": bool(is_present)
                })
            st.session_state.voice_attendance_results = (pd.DataFrame(results), attendance_to_log)

            if st.session_state.get('voice_attendance_results'):
                st.divider()
                df_results, logs = st.session_state.voice_attendance_results
                show_attendance_result(df_results, logs)

