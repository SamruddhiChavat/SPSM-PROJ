import streamlit as st
from streamlit_option_menu import option_menu
# Added chat_ui to the imports
from modules import (auth_ui, profile_ui, privacy_ui, encryptfile_ui, 
                    upload_ui, chat_ui, recovery_ui, activity_ui, hacking_ui)

# Set the page configuration
st.set_page_config(page_title="Secure Social App", page_icon="🛡️", layout="wide")

# Initialize session state variables
if "user" not in st.session_state:
    st.session_state["user"] = None
if "jwt_token" not in st.session_state:
    st.session_state["jwt_token"] = None
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

def main():
    if not st.session_state["user"] and not st.session_state.get("logged_in"):
        st.markdown(
            """
            <style>
                [data-testid="stSidebar"] {display: none;}
                [data-testid="stHeader"] {background: rgba(0,0,0,0); color: rgba(0,0,0,0);}
            </style>
            """,
            unsafe_allow_html=True,
        )
        auth_ui.render()
        
    else:
        # --- SIDEBAR STYLING ---
        st.markdown(
            """
            <style>
            [data-testid="stSidebar"] {
                background-color: #171c1a !important;
                border-right: 1px solid rgba(255, 255, 255, 0.05);
            }
            [data-testid="stSidebar"] .stButton > button {
                width: 100%;
                background-color: transparent !important;
                border: 1px solid #ff4b4b !important;
                color: #ff4b4b !important;
                font-weight: bold;
                border-radius: 8px;
                transition: 0.3s;
                margin-top: 20px;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

        display_user = st.session_state["user"] if st.session_state["user"] else "admin"

        with st.sidebar:
            st.markdown(f"""
                <div style="text-align: center; padding-bottom: 20px; border-bottom: 1px solid rgba(255, 255, 255, 0.1); margin-bottom: 20px; margin-top: 20px;">
                    <div style="background-color: #5bb377; width: 40px; height: 40px; border-radius: 8px; display: inline-flex; align-items: center; justify-content: center; margin-bottom: 10px; box-shadow: 0 0 15px rgba(91, 179, 119, 0.4);">
                        <span style="color: #0a0e0c; font-size: 20px; font-weight: bold;">🖃</span>
                    </div>
                    <h3 style="color: #ffffff; margin: 0; font-family: 'Inter', sans-serif;">SecureApp</h3>
                    <p style="font-size: 13px; color: #8e918f; margin-top: 5px;">Logged in as: <span style="color: #ffffff; font-weight: bold;">{display_user}</span></p>
                </div>
            """, unsafe_allow_html=True)
            
            # --- UPDATED NAVIGATION MENU ---
            menu = option_menu(
                menu_title=None,
                options=[
                    "Profile & Posts",  
                    "File Encrypt & Decrypt", 
                    "Malware Scanner", 
                    "Global Chat",          # <--- New Option Added Here
                    "Account Recovery", 
                    "Activity Logs", 
                    "Security Scanner",
                    "Privacy Control"
                ],
                # Added "chat-dots" icon for the messaging feature
                icons=["person-circle", "shield-lock", "file-earmark-lock", "cloud-arrow-up", "chat-dots", "key", "clock-history", "bug"],
                default_index=0,
                styles={
                    "container": {"padding": "0!important", "background-color": "transparent"},
                    "icon": {"color": "#8e918f", "font-size": "16px"},
                    "nav-link": {
                        "font-size": "14px", 
                        "text-align": "left", 
                        "margin": "4px 0px", 
                        "color": "#8e918f",
                        "--hover-color": "rgba(91, 179, 119, 0.1)"
                    },
                    "nav-link-selected": {
                        "background-color": "rgba(91, 179, 119, 0.15)", 
                        "color": "#5bb377", 
                        "font-weight": "bold",
                        "border-left": "4px solid #5bb377"
                    },
                }
            )
            
            st.markdown("<br>", unsafe_allow_html=True)

            if st.button("Logout"):
                st.session_state["user"] = None
                st.session_state["jwt_token"] = None
                st.session_state["logged_in"] = False
                st.rerun()

        # --- UPDATED ROUTING LOGIC ---
        if menu == "Profile & Posts":
            profile_ui.render()
        
        elif menu == "File Encrypt & Decrypt":
            encryptfile_ui.render()
        elif menu == "Malware Scanner":
            upload_ui.render()
        elif menu == "Global Chat":    
            chat_ui.render()
        elif menu == "Account Recovery":
            recovery_ui.render()
        elif menu == "Activity Logs":
            activity_ui.render()
        elif menu == "Security Scanner":
            hacking_ui.render()
        elif menu == "Privacy Control":
            privacy_ui.render()

if __name__ == "__main__":
    main()