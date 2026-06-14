import streamlit as st
from src.components.header import header_dashboard
from src.ui.base_layout import style_background_dashboard , style_base_layout
from src.database.db import check_teacher_exists, create_teacher , teacher_login, create_subject , get_teacher_subjects
from src.components.dialog_create_subject import create_subject_dialog
from src.components.dialog_share_subject import share_subject_dialog
from src.components.subject_card import subject_card
from src.components.dialog_add_photos import add_photos_dialog
from src.database.config import supabase
from src.pipelines.face_pipelines import predict_attendance
import numpy as np
from datetime import datetime
import pandas as pd
from src.components.dialog_attendance_results import attendance_result_dialog
from src.components.dialog_voice_attendance import voice_attendance_dialog
from src.database.db import get_attendance_for_teacher
def teacher_screen():
    style_background_dashboard()
    style_base_layout()
    
    if "teacher_data" in st.session_state:
        teacher_dashboard()
        return
    
    if 'teacher_login_type' not in st.session_state or st.session_state.teacher_login_type=="login":
        teacher_screen_login()
    elif st.session_state.teacher_login_type=="register":
        teacher_screen_register()

def teacher_dashboard():
    teacher_data = st.session_state.teacher_data
    c1, c2 = st.columns(2, gap="xxlarge",vertical_alignment="center") 
    with c1:
        header_dashboard()
    with c2:
        st.subheader(f"""Welcome, {teacher_data['name']}""")
        if st.button("Logout",type="secondary", key="loginbackhome", shortcut="control+backspace"):
            st.session_state["is_logged_in"] = False
            del st.session_state.teacher_data
            st.rerun()
    st.space()

    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab = "take_attendance"

    tab1 , tab2 , tab3 = st.columns(3)

    with tab1:
        type1 = "primary" if st.session_state.current_teacher_tab == "take_attendance" else "tertiary"
        if st.button('Take Attendance',type = type1, width='stretch',icon=':material/ar_on_you:'):
            st.session_state.current_teacher_tab = "take_attendance"
            st.rerun()

    with tab2:
        type2 = "primary" if st.session_state.current_teacher_tab == "manage_subjects" else "tertiary"
        if st.button('Manage Subjects',type = type2, width='stretch',icon=':material/book_ribbon:'):
            st.session_state.current_teacher_tab = "manage_subjects"
            st.rerun()

    with tab3:
        type3 = "primary" if st.session_state.current_teacher_tab == "attendance_record" else "tertiary"
        if st.button('Attendance Record',type = type3, width='stretch',icon=':material/cards_stack:'):
            st.session_state.current_teacher_tab = "attendance_record"
            st.rerun()

    st.divider()

    if st.session_state.current_teacher_tab == "take_attendance":
        teacher_tab_take_attendance()
    if st.session_state.current_teacher_tab == "manage_subjects":
        teacher_tab_manage_subjects()
    if st.session_state.current_teacher_tab == "attendance_record":
        teacher_tab_attendance_record()

def teacher_tab_take_attendance():
    teacher_id = st.session_state.teacher_data['teacher_id']
    st.header("Take Student Attendance")

    if 'attendance_images' not in st.session_state:
        st.session_state.attendance_images = []

    subjects = get_teacher_subjects(teacher_id)

    if not subjects:
        st.warning("You haven't created any subject yet! Please create one to proceed")
        return
    subject_options = {f"{s['name']} - {s['subject_code']}": s['subject_id'] for s in subjects }

    col1, col2 = st.columns([3,1], vertical_alignment= "bottom")  # ratio of width of width of column
    with col1:
        selected_subject_label =st.selectbox('Select Subject', options=list(subject_options.keys()))
    with col2 :
       if st.button('Add Photos',type= "primary", icon= ":material/photo_prints:", width="stretch"):
           add_photos_dialog()

    selected_subject_id = subject_options[selected_subject_label]

    st.divider()

    if st.session_state.attendance_images:
        st.header("Add Photos")
        gallery_cols = st.columns(4)

        for idx, img in enumerate(st.session_state.attendance_images):
            with gallery_cols[idx % 4]:
                st.image(img, width='stretch',caption=f'photo{idx+1}')
    has_photos = bool(st.session_state.attendance_images)
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("Clear all photos", width = "stretch", icon = ":material/delete:", disabled=not has_photos):
            st.session_state.attendance_images = []
            st.rerun()

    with c2:
        
        if st.button("Run Face Analysis", width = "stretch", icon = ":material/analytics:", disabled=not has_photos):
            with st.spinner("Deep scanning classroom photos ...."):
                all_detected_ids = {}

                for idx, img in enumerate(st.session_state.attendance_images):
                    img_np = np.array(img.convert('RGB'))
                    detected , _, _ = predict_attendance(img_np)

                    if detected:
                        for sid in detected.keys():
                            student_id = int(sid)

                            all_detected_ids.setdefault(student_id, []).append(f"Photos {idx+1}")

                enrolled_res = supabase.table('subject_student').select("* , students(*)").eq("subject_id",selected_subject_id ).execute()
                enrolled_student = enrolled_res.data
                        
                if not enrolled_student:
                    st.warning("No Student enrolled in this course!")
                else:     
                    results, attendance_to_log = [], []
                    current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

                    for node in enrolled_student:
                        student = node["students"]
                        sources = all_detected_ids.get(int(student["student_id"]),[])

                        is_present = len(sources)>0

                        results.append({
                            "Name": student['name'],
                            "Id": student['student_id'],
                            "Source" : ", ".join(sources) if is_present else "-",
                            "Status" : "✅ Present" if is_present else "❌ Absent"
                        })

                        attendance_to_log.append({
                            "student_id": student["student_id"],
                            "subject_id": selected_subject_id,
                            "timestamp": current_timestamp,
                            "is_present": bool(is_present)
                        })
                attendance_result_dialog(pd.DataFrame(results), attendance_to_log)

    with c3:
        if st.button("Use Voice Attendance", type='primary', width='stretch',icon = ":material/mic:"):
            voice_attendance_dialog(selected_subject_id)

def teacher_tab_manage_subjects():
    teacher_id = st.session_state.teacher_data["teacher_id"]
    col1 , col2 = st.columns(2, gap= "large")
    with col1:
        st.markdown("""<h2> Manage<br>Subjects</h2>""", unsafe_allow_html=True)
    with col2:
        if st.button("Create Subject", type="secondary", width="stretch"):
            create_subject_dialog(teacher_id)

    # List all Subjects
    subjects = get_teacher_subjects(teacher_id)
    if subjects:
        for sub in subjects:
            stats = [   
                ("🫂", "<span style='color:black'>Students</span>", f"<span style='color:black'>{sub['total_students']}</span>"),
                ("🕰️", "<span style='color:black'>Classes</span>", f"<span style='color:black'>{sub['total_classes']}</span>")
            ]
            def share_btn():
                if st.button(f"Share code: {sub['name']}", key = f"share_{sub["subject_code"]}", icon= ":material/share:"):
                    share_subject_dialog(sub['name'], sub['subject_code'])
                    st.space()
                    pass

            subject_card(   
                name = sub["name"],
                code = f"<span style='background-color:pink'>{sub["subject_code"]}</span>",
                section = sub["section"],
                stats = stats,
                footer_callback = share_btn
            )
    else:
        st.info("No Subject Found! Create one Above")
            
    # st.button("Share Code: Introduction to memes", icon=":material/share:", type="secondary")
def teacher_tab_attendance_record():
    st.header("attendance_record")

    teacher_id = st.session_state.teacher_data['teacher_id']
    records = get_attendance_for_teacher(teacher_id)
    
    if not records:
        return
    
    data = []

    for r in records:
        ts = r.get('timestamp')
        data.append({
            "ts_group": ts.split(".")[0] if ts else None,
            "Time": datetime.fromisoformat(ts).strftime("%Y-%m-%d %I:%M %p") if ts else "N'A",
            "Subject":r["subjects"]['name'],
            "Subject code":r['subjects']['subject_code'],
            "is_present": bool(r.get('is_present', False))
        })

    df = pd.DataFrame(data)

    summary = (
        df.groupby(["ts_group","Time","Subject","Subject code"])
        .agg(
            Present_count =('is_present','sum'),
            Total_count = ('is_present','count')
        ).reset_index()
    )

    summary['Attendance Stats'] = (
        "✅" +summary['Present_count'].astype('str') + " /"+ summary["Total_count"].astype('str') + ' Students'
    )

    display_df = (summary.sort_values(by='ts_group', ascending=False)
                  [["Time", "Subject", "Subject code", "Attendance Stats"]]
                  )
    st.dataframe(display_df, width="stretch", hide_index= True)

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
        if st.button("Login",type = "secondary",key= "login",shortcut="control+enter", icon=":material/passkey:", width="stretch" ):
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


