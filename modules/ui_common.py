import streamlit as st

def load_css():
    st.markdown("""
    <style>
    .stApp {
        background-color: #0b0f14;
        background-image: 
            linear-gradient(rgba(0,255,163,0.08) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0,255,163,0.08) 1px, transparent 1px);
        background-size: 40px 40px;
    }

    .card {
        background: rgba(17, 24, 39, 0.9);
        padding: 25px;
        border-radius: 15px;
        border: 1px solid rgba(0,255,163,0.2);
        box-shadow: 0 0 20px rgba(0,255,163,0.1);
        margin-bottom: 20px;
    }

    .title {
        color: #00FFA3;
        font-size: 26px;
        font-weight: bold;
    }

    .stButton button {
        background: linear-gradient(90deg, #00FFA3, #00C896);
        color: black;
        border-radius: 10px;
        width: 100%;
    }

    .stTextInput input, .stTextArea textarea {
        background-color: #020617 !important;
        color: #00FFA3 !important;
        border-radius: 10px !important;
    }

    </style>
    """, unsafe_allow_html=True)