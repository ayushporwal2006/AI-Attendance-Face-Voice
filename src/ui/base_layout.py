import streamlit as st
def style_background_home():
    st.markdown("""    
        <style> 
                .stApp{    /* apply to whole page i.e body we can also use it */
                    background: #5865F2 !important;
                }
                .stApp div[data-testid="stColumn"]{
                    background-color: #E0E3FF !important;
                    padding:2.5rem !important;
                    border-radius: 5rem !important
                }
        </style>
                """,
             unsafe_allow_html=True
    )
def style_background_dashboard():
    st.markdown("""
        <style> 
                .stApp{
                    background: #E0E3FF !important;
                }
        </style>
                """,
             unsafe_allow_html=True
    )


def style_base_layout():
    #jhbdjbjf
    st.markdown("""
        <style> 
                @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis:YEAR@1979&display=swap');
                @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@100..900&display=swap');
            /*  Hide top bar of streamlit */
                #MainMenu , header ,footer{
                    visibility:  hidden;
                }
                .stTextInput label {
                    color: black !important;   
                    font-weight: 600;
                }
                .block-container{
                    padding-top: 1.5rem !important;
                }
                .stButton button {
                    color: black !important;
                }
                h1{
                    font-family: "Climate Crisis",sans-serif !important;
                    font-size: 1.8vw !important;
                    line-height:1 !important;
                    margin-bottom: 0cm !important;
                    color: purple !important;
                    text-align:center !important;
                }
                h2{
                    font-family: "Climate Crisis",sans-serif !important;
                    font-size: 2rem !important;
                    line-height: 1.2 !important;
                    margin-bottom: 0cm !important;
                    color: black !important;
                    white-space: nowrap;
                    font-weight: 550 !important;
                }
                h3, h4, p{
                    font-family: "Outfit", sans-serif;
                }
                button{
                    color: white !important;
                    background-color: #5865F2 !important;
                    border-radius: 1.5rem !important;
                    padding : 10px 20px !important;
                    border: none !important;
                    transition: transform 0.25s ease-in-out !important;
                }
                button[kind = "secondary"]{
                    color: white !important;
                    background-color: #EB459E !important;
                    border-radius: 1.5rem !important;
                    padding : 10px 20px !important;
                    border: none !important;
                    transition: transform 0.25s ease-in-out !important;
                }
                button[kind = "tertiary"]{
                    color: white !important;
                    background-color: black !important;
                    border-radius: 1.5rem !important;
                    padding : 10px 20px !important;
                    border: none !important;
                    transition: transform 0.25s ease-in-out !important;
                }
                button:hover{
                    transform :scale(1.05) 
                }
                
        </style>
                """,
             unsafe_allow_html=True
    )