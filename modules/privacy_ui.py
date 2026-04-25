import streamlit as st
from utils.firebase_init import get_db
from services import activity_service

def render():
    # --- PAGE HEADER ---
    st.markdown("""
        <h2 style='color: #ffffff; font-family: "Inter", sans-serif; margin-bottom: 0px;'>Profile & Privacy</h2>
        <p style='color: #8e918f; font-size: 14px; margin-bottom: 40px;'>Manage your identity and access controls</p>
    """, unsafe_allow_html=True)
    
    # --- DATABASE SETUP ---
    db = get_db()
    current_user = st.session_state.get("user")
    
    if not current_user:
        st.error("No active session found.")
        return

    # Fetch current visibility from DB
    try:
        user_ref = db.collection("users").document(current_user)
        user_data = user_ref.get().to_dict() or {}
        current_visibility = user_data.get("default_visibility", "Friends Only")
    except Exception as e:
        st.error("Database connection error.")
        current_visibility = "Friends Only"

    # Initialize session state so the UI highlights the correct card instantly
    if "privacy_setting" not in st.session_state:
        st.session_state.privacy_setting = current_visibility

    def update_privacy(level):
        st.session_state.privacy_setting = level
        try:
            user_ref.update({"default_visibility": level})
            activity_service.log_activity(current_user, f"Updated privacy to {level}")
            st.toast(f"Privacy successfully updated to {level}", icon="✅")
        except Exception:
            st.error("Failed to update database.")

    # --- PRIVACY LEVEL CONTAINER ---
    st.markdown("""
        <style>
        .privacy-container {
            background-color: #171c1a;
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 16px;
            padding: 30px;
            margin-bottom: 20px;
        }
        .section-title {
            color: #8e918f;
            font-size: 12px;
            font-weight: 700;
            letter-spacing: 1.5px;
            margin-bottom: 20px;
            text-transform: uppercase;
        }
        </style>
        <div class="privacy-container">
            <div class="section-title"><span style="color: #5bb377; margin-right: 8px; font-size: 16px;">🛡️</span> PRIVACY LEVEL</div>
        </div>
    """, unsafe_allow_html=True)

    # Use 3 columns for the horizontal cards
    col1, col2, col3 = st.columns(3)

    # --- CARD 1: PUBLIC ---
    with col1:
        is_active = st.session_state.privacy_setting == "Public"
        st.markdown(f"""
            <div style="border: 1px solid {'#5bb377' if is_active else 'rgba(255,255,255,0.1)'}; 
                        background-color: {'rgba(91, 179, 119, 0.05)' if is_active else '#141816'}; 
                        padding: 20px; border-radius: 12px; height: 130px; transition: 0.3s;">
                <div style="color: {'#5bb377' if is_active else '#8e918f'}; font-size: 20px; margin-bottom: 10px;">🌐</div>
                <div style="color: #ffffff; font-weight: 600; margin-bottom: 5px;">Public</div>
                <div style="color: #8e918f; font-size: 12px;">Anyone can view your profile</div>
            </div>
        """, unsafe_allow_html=True)
        # Invisible padding and standard button below the HTML card
        st.markdown("<div style='margin-top: -15px;'></div>", unsafe_allow_html=True)
        if st.button("Set Public", key="btn_pub", use_container_width=True):
            update_privacy("Public")
            st.rerun()

    # --- CARD 2: FRIENDS ONLY ---
    with col2:
        is_active = st.session_state.privacy_setting == "Friends Only"
        st.markdown(f"""
            <div style="border: 1px solid {'#5bb377' if is_active else 'rgba(255,255,255,0.1)'}; 
                        background-color: {'rgba(91, 179, 119, 0.05)' if is_active else '#141816'}; 
                        padding: 20px; border-radius: 12px; height: 130px; transition: 0.3s;">
                <div style="color: {'#5bb377' if is_active else '#8e918f'}; font-size: 20px; margin-bottom: 10px;">👥</div>
                <div style="color: #ffffff; font-weight: 600; margin-bottom: 5px;">Friends Only</div>
                <div style="color: #8e918f; font-size: 12px;">Only approved friends</div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='margin-top: -15px;'></div>", unsafe_allow_html=True)
        if st.button("Set Friends Only", key="btn_fri", use_container_width=True):
            update_privacy("Friends Only")
            st.rerun()

    # --- CARD 3: PRIVATE ---
    with col3:
        is_active = st.session_state.privacy_setting == "Private"
        st.markdown(f"""
            <div style="border: 1px solid {'#5bb377' if is_active else 'rgba(255,255,255,0.1)'}; 
                        background-color: {'rgba(91, 179, 119, 0.05)' if is_active else '#141816'}; 
                        padding: 20px; border-radius: 12px; height: 130px; transition: 0.3s;">
                <div style="color: {'#5bb377' if is_active else '#8e918f'}; font-size: 20px; margin-bottom: 10px;">🔒</div>
                <div style="color: #ffffff; font-weight: 600; margin-bottom: 5px;">Private</div>
                <div style="color: #8e918f; font-size: 12px;">Nobody can view your profile</div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='margin-top: -15px;'></div>", unsafe_allow_html=True)
        if st.button("Set Private", key="btn_prv", use_container_width=True):
            update_privacy("Private")
            st.rerun()